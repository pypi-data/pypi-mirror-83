import time
import io
import os.path
import os
import json
import orjson
import tempfile
import uuid
import aiofiles
import shutil
import pkg_resources
import asyncio
import aiohttp
import re

from aiohttp.web_exceptions import HTTPOk
from yarl import URL
from pathlib import Path
from datetime import datetime
from cachetools import TTLCache

from PyQt5.QtCore import QFile

import async_timeout

from galacteek.ipfs.cidhelpers import joinIpfs
from galacteek.ipfs.cidhelpers import joinIpns
from galacteek.ipfs.cidhelpers import stripIpfs
from galacteek.ipfs.cidhelpers import stripIpns
from galacteek.ipfs.cidhelpers import cidConvertBase32
from galacteek.ipfs.cidhelpers import IPFSPath
from galacteek.ipfs.cidhelpers import ipnsKeyCidV1
from galacteek.ipfs.multi import multiAddrTcp4
from galacteek.ipfs.stat import StatInfo

from galacteek.core.asynccache import amlrucache
from galacteek.core.asynccache import cachedcoromethod
from galacteek.core.asynclib import async_enterable
from galacteek.core.asynclib import asyncReadFile
from galacteek.core.jtraverse import traverseParser
from galacteek.core import jsonSchemaValidate
from galacteek.ld.ldloader import aioipfs_document_loader
from galacteek.ld import asyncjsonld as jsonld

from galacteek import log
from galacteek import logUser
from galacteek import AsyncSignal

import aioipfs


GFILES_ROOT_PATH = '/galacteek/'


def isDict(data):
    return isinstance(data, dict)


class OperatorError(Exception):
    pass


class UnixFSTimeoutError(Exception):
    pass


class IPFSLogWatcher(object):
    def __init__(self, operator):
        self.op = operator

    async def analyze(self):
        async for msg in self.op.client.log.tail():
            event = msg.get('event', None)

            if not event:
                continue

            if event == 'handleAddProvider':
                # Handle add provider
                if self.op.ctx:
                    self.op.ctx.logAddProvider.emit(msg)


class IPFSOperatorOfflineContext(object):
    def __init__(self, operator):
        self.operator = operator
        self.prevOff = self.operator.offline

    async def __aenter__(self):
        self.operator.offline = True
        return self.operator

    async def __aexit__(self, *args):
        self.operator.offline = self.prevOff


class GetContext(object):
    def __init__(self, operator, path, dstdir, **kwargs):
        self.operator = operator
        self.path = IPFSPath(path)
        self.dstdir = Path(dstdir)
        self.finaldir = None

    async def __aenter__(self):
        try:
            await self.operator.client.core.get(
                str(self.path), dstdir=str(self.dstdir))
        except Exception as err:
            self.operator.debug(f'Unknown error: {self.path}: {err}')
            return self
        except aioipfs.APIError as err:
            self.operator.debug(f'Get error: {self.path}: {err}')
            return self
        else:
            self.finaldir = self.dstdir.joinpath(self.path.basename)
            self.operator.debug(
                f'Get {self.path}: OK, fetched in {self.finaldir}')
            return self

    async def __aexit__(self, *args):
        self.operator.debug(
            f'Get {self.path}: cleaning up {self.dstdir}')
        await self.operator.asyncRmTree(self.dstdir)


class TunnelDialerContext(object):
    def __init__(self, operator, peerId, proto, maddr):
        self.operator = operator
        self.peerId = peerId
        self.protocol = proto
        self.maddr = maddr

    @property
    def maddrPort(self):
        if self.maddr:
            return multiAddrTcp4(self.maddr)[1]

    @property
    def maddrHost(self):
        if self.maddr:
            return multiAddrTcp4(self.maddr)[0]

    @property
    def failed(self):
        return self.maddr is None

    def httpUrl(self, path):
        return str(URL.build(
            host=self.maddrHost,
            port=self.maddrPort,
            scheme='http',
            path=path
        ))

    async def __aenter__(self):
        self.operator.debug('Tunnel dialer: {0} {1} {2}: enter'.format(
            self.protocol, self.maddrHost, self.maddrPort))
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *args):
        self.operator.debug('Tunnel dialer: {0} {1} {2}: aexit'.format(
            self.protocol, self.maddrHost, self.maddrPort))

        await self.session.close()

        if not self.operator.ctx:
            return

        manager = self.operator.ctx.p2p.tunnelsMgr

        streams = await manager.streamsForListenAddr(self.maddr)
        if streams:
            self.operator.debug(streams)
            for stream in streams:
                self.operator.debug('Tunnel dialer: closing {!r}'.format(
                    stream))
                await self.operator.client.p2p.listener_close(
                    self.protocol,
                    listen_address=self.maddr
                )


class LDOpsContext(object):
    def __init__(self, operator, ldDocLoader):
        self.operator = operator
        self.ldLoader = ldDocLoader

    async def __aenter__(self):
        return self

    async def expandDocument(self, doc):
        """
        Perform a JSON-LD expansion on a JSON document
        """

        try:
            expanded = await jsonld.expand(
                await self.operator.ldInline(doc), {
                    'documentLoader': self.ldLoader
                }
            )

            if isinstance(expanded, list) and len(expanded) > 0:
                return expanded[0]
        except Exception as err:
            self.operator.debug('Error expanding document: {}'.format(
                str(err)))

    async def __aexit__(self, *args):
        pass


class APIErrorDecoder:
    def __init__(self, exc):
        self.exc = exc

    def errIsDirectory(self):
        return self.exc.message == 'this dag node is a directory'

    def errNoSuchLink(self):
        return self.exc.message.startswith('no link named') or \
            self.exc.message == 'no such link found'

    def errUnknownNode(self):
        return self.exc.message == 'unknown node type'


ppRe = r"^(/ipns/[\w<>\:\;\,\?\!\*\%\&\=\@\$\~/\s\.\-_\\\'\(\)\+]{1,1024}$)"
nsCacheSchema = {
    "title": "NS cache",
    "description": "NS cache schema",
    "type": "object",
    "patternProperties": {
        ppRe: {
            "properties": {
                "resolved": {
                    "type": "string"
                },
                "resolvedLast": {
                    "type": "integer"
                },
                "cacheOrigin": {
                    "type": "string"
                }
            }
        }
    }
}


# Stream-resolve cache
sResolveCache = TTLCache(512, 30)


class IPFSOperator(object):
    """
    IPFS operator, for your daily operations!
    """

    def __init__(self, client, ctx=None, rsaAgent=None, debug=False,
                 offline=False, nsCachePath=None,
                 objectMapping=False):
        self._lock = asyncio.Lock()
        self._id = uuid.uuid1()
        self._cache = {}
        self._offline = offline
        self._objectMapping = objectMapping
        self._rsaAgent = rsaAgent
        self._curve25519Agent = None
        self._nsCache = {}
        self._nsCachePath = nsCachePath
        self._noPeers = True
        self._ldDocLoader = None
        self.debugInfo = debug
        self.client = client

        self.ctx = ctx

        self.filesChroot = None
        self._commands = None

        self.evReady = asyncio.Event()
        self.gotNoPeers = AsyncSignal()
        self.gotPeers = AsyncSignal(int)

        if self._nsCachePath:
            self.nsCacheLoad()

    @property
    def nsCache(self):
        return self._nsCache

    @property
    def offline(self):
        return self._offline

    @offline.setter
    def offline(self, v):
        self._offline = v

    @property
    def noPeers(self):
        return self._noPeers

    @noPeers.setter
    def noPeers(self, v):
        self._noPeers = v

    @property
    def uid(self):
        return self._id

    @property
    def rsaAgent(self):
        return self._rsaAgent

    @property
    def curve25519Agent(self):
        return self._curve25519Agent

    @property
    def logwatch(self):
        return IPFSLogWatcher(self)

    @property
    def availCommands(self):
        """ Cached property: available IPFS commands """
        return self._commands

    def debug(self, msg):
        log.debug('IPFSOp({0}): {1}'.format(self.uid, msg))

    def info(self, msg):
        log.info('IPFSOp({0}): {1}'.format(self.uid, msg))

    def setRsaAgent(self, agent):
        self._rsaAgent = agent

    def setCurve25519Agent(self, agent):
        self._curve25519Agent = agent

    @async_enterable
    async def offlineMode(self):
        clone = IPFSOperator(self.client, ctx=self.ctx)
        return IPFSOperatorOfflineContext(clone)

    async def __aenter__(self):
        await self.client.agent_version_get()
        return self

    async def __aexit__(self, *args):
        return

    async def asyncRmTree(self, path):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            shutil.rmtree,
            path
        )

    async def sleep(self, t=0):
        await asyncio.sleep(t)

    async def waitReady(self, timeout=10):
        return await self.waitFor(self.evReady.wait(), timeout)

    async def waitFor(self, fncall, timeout):
        try:
            with async_timeout.timeout(timeout):
                return await fncall
        except asyncio.TimeoutError:
            self.debug('Timeout waiting for coroutine {0}'.format(fncall))
            return None
        except asyncio.CancelledError:
            self.debug('Cancelled coroutine {0}'.format(fncall))
            raise

    @amlrucache
    async def daemonConfig(self):
        try:
            return await self.client.config.show()
        except Exception:
            return None

    async def daemonConfigGet(self, attr):
        """
        Get an attribute from the daemon's config JSON document
        """
        config = await self.daemonConfig()
        if config:
            try:
                parser = traverseParser(config)
                return parser.traverse(attr)
            except Exception:
                return None

    async def getCommands(self):
        if self.availCommands is not None:
            return self.availCommands
        try:
            self._commands = await self.client.core.commands()
        except aioipfs.APIError:
            self.debug('Cannot find available IPFS commands')
            return None
        else:
            return self.availCommands

    async def filesDelete(self, path, name, recursive=False):
        try:
            await self.client.files.rm(os.path.join(path, name),
                                       recursive=recursive)
        except aioipfs.APIError:
            self.debug('Exception on removing {0} in {1}'.format(
                name, path))
            return False
        await self.client.files.flush(path)
        return True

    async def filesLookup(self, path, name):
        """
        Looks for a file (files API) with a given name in this path

        :param str path: the path to search
        :param str name: the entry name to look for
        :return: IPFS entry
        """
        listing = await self.filesList(path)
        if listing is None:
            return
        for entry in listing:
            if entry['Name'] == name:
                return entry

    async def filesLookupHash(self, path, mhash):
        """
        Searches for a file (files API) with a given hash in this path

        :param str path: the path to search
        :param str hash: the multihash to look for
        :return: IPFS entry
        """
        listing = await self.filesList(path)
        b32CID = cidConvertBase32(mhash)

        for entry in listing:
            if cidConvertBase32(entry['Hash']) == b32CID:
                return entry

    async def filesRm(self, path, recursive=False):
        try:
            await self.client.files.rm(path, recursive=recursive)
        except aioipfs.APIError as err:
            self.debug(err.message)

    async def filesMkdir(self, path, parents=True, cidversion=1):
        try:
            await self.client.files.mkdir(
                path, parents=parents, cid_version=cidversion)
        except aioipfs.APIError as err:
            self.debug(err.message)
            return None

    async def filesMove(self, source, dest):
        try:
            return await self.client.files.mv(source, dest)
        except aioipfs.APIError as err:
            self.debug(err.message)
            return None

    async def filesList(self, path, sort=False):
        try:
            listing = await self.client.files.ls(path, long=True)
        except aioipfs.APIError as err:
            self.debug(err.message)
            return None

        if 'Entries' not in listing or listing['Entries'] is None:
            return []

        if sort is True:
            return sorted(listing['Entries'])

        return listing['Entries']

    async def filesStat(self, path, timeout=3):
        try:
            return await self.waitFor(
                self.client.files.stat(path),
                timeout
            )
        except aioipfs.APIError as err:
            self.debug(err.message)
            return None

    async def filesWrite(self, path, data, create=False, truncate=False,
                         offset=-1, count=-1, cidversion=1):
        try:
            await self.client.files.write(
                path, data,
                create=create, truncate=truncate,
                offset=offset, count=count,
                cid_version=cidversion
            )
        except aioipfs.APIError as err:
            self.debug('filesWrite error {}'.format(err.message))
            return None
        else:
            return True

    async def filesWriteJsonObject(self, path, obj, create=True,
                                   truncate=True):
        try:
            serialized = orjson.dumps(obj)
            resp = await self.filesWrite(path, serialized,
                                         create=create, truncate=truncate)
        except aioipfs.APIError as err:
            self.debug('filesWriteJson error {}'.format(err.message))
            return None
        else:
            return resp

    async def filesReadJsonObject(self, path):
        try:
            resp = await self.client.files.read(path)
        except aioipfs.APIError as err:
            self.debug('filesReadJson ({0}): error {1}'.format(
                path, err.message))
            return None
        except Exception as err:
            self.debug('filesReadJson ({0}): unknown error {1}'.format(
                path, str(err)))
            return None
        else:
            return orjson.loads(resp.decode())

    async def chroot(self, path):
        self.filesChroot = path

    async def vMkdir(self, path):
        if self.filesChroot:
            return await self.filesMkdir(os.path.join(self.filesChroot,
                                                      path))

    async def vFilesList(self, path):
        if self.filesChroot:
            return await self.filesList(os.path.join(self.filesChroot,
                                                     path))
        else:
            raise OperatorError('No chroot provided')

    async def filesCp(self, source, dest):
        try:
            await self.client.files.cp(source, dest)
        except aioipfs.APIError:
            return False

        return True

    async def filesMv(self, source, dest):
        try:
            await self.client.files.mv(source, dest)
        except aioipfs.APIError:
            return False

        return True

    async def filesLink(self, entry, dest, flush=True, name=None):
        """ Given an entry (as returned by /files/ls), make a link
            in ``dest`` """

        try:
            await self.client.files.cp(
                joinIpfs(entry['Hash']),
                os.path.join(dest, name if name else entry['Name'])
            )
        except aioipfs.APIError:
            self.debug('Exception on copying entry {0} to {1}'.format(
                entry, dest))
            return False

        if flush:
            await self.client.files.flush(dest)
        return True

    async def filesLinkFp(self, entry, dest):
        try:
            await self.client.files.cp(joinIpfs(entry['Hash']),
                                       dest)
        except aioipfs.APIError:
            self.debug('Exception on copying entry {0} to {1}'.format(
                entry, dest))
            return False

        return True

    async def peersList(self):
        try:
            peers = await self.client.swarm.peers()
        except aioipfs.APIError:
            self.debug('Cannot fetch list of peers')
            return []
        except Exception:
            return []
        else:
            if isDict(peers) and 'Peers' in peers:
                pList = peers['Peers']
                return pList if isinstance(pList, list) else []

    async def nodeId(self):
        info = await self.client.core.id()
        if isDict(info):
            return info.get('ID', 'Unknown')

    async def nodeWsAdresses(self):
        addrs = []
        nid = await self.client.core.id()

        for addr in nid['Addresses']:
            # use re instead of multiaddr module
            if re.search(r"/ip4/[0-9.]+/tcp/[0-9]+/ws/p2p/[\w]+", addr):
                addrs.append(addr)

        return addrs

    async def keysNames(self):
        keys = await self.keys()
        return [key['Name'] for key in keys]

    async def keyGen(self, keyName, type='rsa', keySize=2048,
                     checkExisting=False):
        if checkExisting is True:
            if keyName in await self.keysNames():
                return

        return await self.waitFor(
            self.client.key.gen(keyName,
                                type=type, size=keySize), 30
        )

    async def keys(self):
        kList = await self.client.key.list(long=True)
        if isDict(kList):
            return kList.get('Keys', [])

    async def keyFind(self, name):
        keys = await self.keys()
        for key in keys:
            if key['Name'] == name:
                return key

    async def keyFindById(self, ident):
        keys = await self.keys()
        for key in keys:
            if key['Id'] == ident:
                return key

    async def keysRemove(self, name):
        try:
            await self.client.key.rm(name)
        except aioipfs.APIError as err:
            self.debug('Exception on removing key {0}: {1}'.format(
                name, err.message))
            return False
        return True

    async def publish(self, path, key='self', timeout=60 * 6,
                      allow_offline=None, lifetime='24h',
                      resolve=True,
                      ttl=None, cache=None, cacheOrigin='unknown'):
        usingCache = cache == 'always' or \
            (cache == 'offline' and self.noPeers and 0)
        aOffline = allow_offline if isinstance(allow_offline, bool) else \
            self.noPeers
        try:
            if usingCache:
                self.debug('Caching IPNS key: {key} (origin: {origin})'.format(
                    key=key, origin=cacheOrigin))

                await self.nsCacheSet(
                    joinIpns(key), path, origin=cacheOrigin)

            self.debug(
                'Publishing {path} to {dst} '
                '(cache: {cache}/{cacheOrigin}, allowoffline: {off})'.format(
                    path=path, dst=key, off=aOffline,
                    cache=cache, cacheOrigin=cacheOrigin)
            )

            result = await self.waitFor(
                self.client.name.publish(
                    path, key=key,
                    allow_offline=aOffline,
                    lifetime=lifetime,
                    ttl=ttl,
                    resolve=resolve
                ), timeout
            )
        except aioipfs.APIError as err:
            self.debug('Error publishing {path} to {key}: {msg}'.format(
                path=path, key=key, msg=err.message))
            return None
        else:
            return result

    async def resolve(self, path, timeout=20, recursive=False):
        """
        Use /api/vx/resolve to resolve pretty much anything
        """
        try:
            resolved = await self.waitFor(
                self.client.core.resolve(await self.objectPathMapper(path),
                                         recursive=recursive), timeout)
        except asyncio.TimeoutError:
            self.debug('resolve timeout for {0}'.format(path))
            return None
        except aioipfs.APIError as e:
            self.debug('resolve error: {0}: {1}'.format(path, e.message))
            return None
        else:
            if isDict(resolved):
                return resolved.get('Path')

    async def noPeersFound(self):
        self.noPeers = True
        await self.gotNoPeers.emit()

    async def peersCountStatus(self, peerCount):
        self.noPeers = False
        await self.gotPeers.emit(peerCount)

    def nsCacheLoad(self):
        try:
            with open(self._nsCachePath, 'r') as fd:
                cache = json.load(fd)

            if not jsonSchemaValidate(cache, nsCacheSchema):
                raise Exception('Invalid NS cache schema')
        except Exception as err:
            self.debug(f'Error loading NS cache: {err}')
        else:
            self.debug(f'NS cache: loaded from {self._nsCachePath}')
            self._nsCache = cache

    async def nsCacheSave(self):
        if not self._nsCachePath or not isinstance(self.nsCache, dict):
            return

        async with self._lock:
            async with aiofiles.open(self._nsCachePath, 'w+t') as fd:
                await fd.write(json.dumps(self.nsCache))

    def nsCacheGet(self, path, maxLifetime=None, knownOrigin=False):
        entry = self.nsCache.get(path)

        if isinstance(entry, dict):
            rLast = entry['resolvedLast']

            if knownOrigin is True and entry.get('cacheOrigin') == 'unknown':
                return None

            if not maxLifetime or (int(time.time()) - rLast) < maxLifetime:
                return entry['resolved']

    async def nsCacheSet(self, path, resolved, origin=None):
        self._nsCache[path] = {
            'resolved': resolved,
            'resolvedLast': int(time.time()),
            'cacheOrigin': origin
        }

        # Cache v1
        v1 = ipnsKeyCidV1(stripIpns(path))
        if v1:
            self._nsCache[joinIpns(v1)] = {
                'resolved': resolved,
                'resolvedLast': int(time.time()),
                'cacheOrigin': origin
            }

        await self.nsCacheSave()

    async def nameResolve(self, path, timeout=20, recursive=False,
                          useCache='never',
                          cache='never',
                          maxCacheLifetime=None,
                          cacheOrigin='unknown'):
        usingCache = useCache == 'always' or \
            (useCache == 'offline' and self.noPeers and 0)
        cache = cache == 'always' or (cache == 'offline' and self.noPeers)
        try:
            if usingCache:
                # The NS cache is used only for IPIDs when offline

                rPath = self.nsCacheGet(
                    path, maxLifetime=maxCacheLifetime,
                    knownOrigin=True)

                if rPath and IPFSPath(rPath).valid:
                    self.debug(
                        'nameResolve: Feeding entry from NS cache: {}'.format(
                            rPath))
                    return {
                        'Path': rPath
                    }

            resolved = await self.waitFor(
                self.client.name.resolve(path, recursive=recursive),
                timeout)
        except asyncio.TimeoutError:
            self.debug('resolve timeout for {0}'.format(path))
            return None
        except aioipfs.APIError as e:
            self.debug('resolve error: {0}: {1}'.format(path, e.message))
            return None
        else:
            if cache and resolved:
                await self.nsCacheSet(
                    path, resolved['Path'], origin=cacheOrigin)

            return resolved

    async def nameResolveStreamLegacy(self, path, count=3,
                                      timeout=20,
                                      useCache='never',
                                      cache='never',
                                      cacheOrigin='unknown',
                                      recursive=True,
                                      maxCacheLifetime=60 * 10):
        usingCache = useCache == 'always' or \
            (useCache == 'offline' and self.noPeers and 0)
        cache = cache == 'always' or (cache == 'offline' and self.noPeers)
        rTimeout = '{t}s'.format(t=timeout) if isinstance(timeout, int) else \
            timeout

        try:
            gotFromCache = False
            if usingCache:
                # The NS cache is used only for IPIDs when offline

                rPath = self.nsCacheGet(
                    path, maxLifetime=maxCacheLifetime,
                    knownOrigin=True
                )

                if rPath and IPFSPath(rPath).valid:
                    self.debug(
                        'nameResolve: Feeding from cache: {0} for {1}'.format(
                            rPath, path))
                    yield {
                        'Path': rPath
                    }

                    gotFromCache = True

            if not gotFromCache:
                async for nentry in self.client.name.resolve_stream(
                        name=path,
                        recursive=recursive,
                        stream=True,
                        dht_record_count=count,
                        dht_timeout=rTimeout):
                    yield nentry
        except asyncio.TimeoutError:
            self.debug('streamed resolve timeout for {0}'.format(path))
        except aioipfs.APIError as e:
            self.debug('streamed resolve error: {}'.format(e.message))

    async def nameResolveStream(self, path, count=3,
                                timeout=20,
                                useCache='never',
                                cache='never',
                                cacheOrigin='unknown',
                                recursive=True,
                                maxCacheLifetime=60 * 10,
                                debug=True):
        """
        DHT is used first for resolution.
        NS cache is used as last option (used by local IPID).
        """

        usingCache = useCache == 'always' or \
            (useCache == 'offline' and self.noPeers and 0)
        cache = cache == 'always' or (cache == 'offline' and self.noPeers)
        rTimeout = '{t}s'.format(t=timeout) if isinstance(timeout, int) else \
            timeout
        _yieldedcn = 0

        try:
            async for nentry in self.client.name.resolve_stream(
                    name=path,
                    recursive=recursive,
                    stream=True,
                    dht_record_count=count,
                    dht_timeout=rTimeout):
                if cache:
                    self.debug(f'nameResolveStream ({path}): caching {nentry}')
                    await self.nsCacheSet(
                        path, nentry['Path'], origin=cacheOrigin)

                if debug:
                    self.debug(
                        f'nameResolveStream (timeout: {timeout}) '
                        f'({path}): {nentry}')

                yield nentry
                _yieldedcn += 1
        except asyncio.TimeoutError:
            self.debug(
                f'nameResolveStream (timeout: {timeout}) '
                f'({path}): Timed out')
        except aioipfs.APIError as e:
            self.debug('nameResolveStream API error: {}'.format(e.message))
        except Exception as gerr:
            self.debug(f'nameResolveStream ({path}) unknown error: {gerr}')

        if _yieldedcn == 0 and usingCache:
            # The NS cache is used only for IPIDs when offline
            rPath = self.nsCacheGet(
                path, maxLifetime=maxCacheLifetime,
                knownOrigin=True
            )

            if rPath and IPFSPath(rPath).valid:
                self.debug(
                    'nameResolveStream: from cache: {0} for {1}'.format(
                        rPath, path))
                yield {
                    'Path': rPath
                }

    async def nameResolveStreamFirst(self, path, count=2,
                                     timeout=10,
                                     cache='never',
                                     cacheOrigin='unknown',
                                     useCache='never',
                                     maxCacheLifetime=60 * 10,
                                     debug=True):
        """
        A wrapper around the nameResolveStream async gen,
        returning the last result of the yielded values

        :rtype: dict
        """
        matches = []
        async for entry in self.nameResolveStream(
                path,
                timeout=timeout,
                cache=cache, cacheOrigin=cacheOrigin,
                maxCacheLifetime=maxCacheLifetime,
                useCache=useCache,
                debug=debug):
            found = entry.get('Path')
            if found:
                matches.append(found)

            if len(matches) >= count:
                break

        if len(matches) > 0:
            return {
                'Path': matches[-1]
            }

    async def objectDiff(self, obja, objb, verbose=True):
        """
        Returns the diff between two objects
        """
        try:
            diff = await self.client.object.diff(
                obja, objb, verbose=verbose)
        except aioipfs.APIError as e:
            self.debug(
                f'objectDiff error: {obja} {objb}: {e.message}')
        else:
            if isinstance(diff, dict) and 'Changes' in diff:
                return diff['Changes']

    async def purge(self, hashRef, rungc=False):
        """ Unpins an object and optionally runs the garbage collector """
        try:
            await self.client.pin.rm(hashRef, recursive=True)
            if rungc:
                await self.client.repo.gc()
            return True
        except aioipfs.APIError as e:
            self.debug('purge error: {}'.format(e.message))
            return False
        else:
            self.debug('purge OK: {}'.format(hashRef))

    async def gCollect(self, quiet=True):
        """
        Run a garbage collector sweep
        """
        return await self.client.repo.gc(quiet=quiet)

    async def isPinned(self, hashRef):
        """
        Returns True if the IPFS object referenced by hashRef is pinned,
        False otherwise
        """
        try:
            mHash = stripIpfs(hashRef)
            result = await self.client.pin.ls(multihash=mHash)
            keys = result.get('Keys', {})
            return mHash in keys
        except aioipfs.APIError as e:
            self.debug('isPinned error: {}'.format(e.message))
            return False

    async def pinned(self, type='all'):
        """
        Returns all pinned keys of a given type
        """
        try:
            result = await self.client.pin.ls(pintype=type)
            return result.get('Keys', {})
        except aioipfs.APIError:
            return None

    async def pin(self, path, recursive=False, timeout=3600):
        async def _pin(ppath, rec):
            try:
                async for pinStatus in self.client.pin.add(
                        ppath, recursive=rec):
                    self.debug('Pin status: {0} {1}'.format(
                        ppath, pinStatus))
                    pins = pinStatus.get('Pins', None)
                    if pins is None:
                        continue
                    if isinstance(pins, list) and ppath in pins:
                        # Ya estamos
                        return True
                return False
            except aioipfs.APIError as err:
                self.debug('Pin error: {}'.format(err.message))
                return False
        return await self.waitFor(_pin(path, recursive), timeout)

    async def pin2(self, path, recursive=True, timeout=3600):
        try:
            async for pinStatus in self.client.pin.add(
                    path, recursive=recursive):
                self.debug('Pin status: {0} {1}'.format(
                    path, pinStatus))
                pins = pinStatus.get('Pins', None)
                progress = pinStatus.get('Progress', None)

                yield path, 0, progress

                if pins is None:
                    continue

                if isinstance(pins, list) and len(pins) > 0:
                    # Ya estamos
                    yield path, 1, progress

        except aioipfs.APIError as err:
            self.debug('Pin error: {}'.format(err.message))
            yield path, -1, None

    async def unpin(self, obj):
        """
        Unpin an object
        """

        self.debug('unpinning: {0}'.format(obj))
        try:
            result = await self.client.pin.rm(obj)
        except aioipfs.APIError as e:
            self.debug('unpin error: {}'.format(e.message))
            return None
        else:
            self.debug('unpin success: {}'.format(result))
            return result

    async def pinUpdate(self, old, new, unpin=True):
        """
        Update a pin
        """

        try:
            result = await self.client.pin.update(old, new, unpin=unpin)
        except aioipfs.APIError as e:
            self.debug('pinUpdate error: {}'.format(e.message))
            return None
        else:
            self.debug('pinUpdate success: {}'.format(result))
            return result

    async def list(self, path, resolve_type=True):
        """
        Lists objects in a given path and yields them
        """
        try:
            listing = await self.client.ls(
                await self.objectPathMapper(path),
                headers=True,
                resolve_type=resolve_type)
            objects = listing.get('Objects', [])

            for obj in objects:
                await self.sleep()
                yield obj
        except BaseException:
            pass

    async def listStreamed(self, path, resolve_type=True, egenCount=8):
        """
        Lists objects in a UnixFS directory referenced by its
        path and yields lists of entries (8 entries by yield is
        the default).
        """
        try:
            ePack = []
            async for listing in self.client.core.ls_streamed(
                    await self.objectPathMapper(path),
                    headers=True,
                    resolve_type=resolve_type):

                objects = listing.get('Objects', [])

                for obj in objects:
                    if not isinstance(obj['Links'], list):
                        continue

                    ePack += obj['Links']

                    if len(ePack) >= egenCount:
                        yield ePack
                        ePack.clear()

                    await self.sleep()

            if len(ePack) > 0:
                # Yield remaining entries
                yield ePack
        except GeneratorExit:
            self.debug(f'listStreamed ({path}): generator exit')
            raise
        except aioipfs.APIError as e:
            raise e
        except BaseException as err:
            import traceback
            traceback.print_exc()
            self.debug(str(err))
            raise err

    async def listStreamedMonitored(self, path, resolve_type=True,
                                    egenCount=16, genTimeout=10):
        eGenerator = self.listStreamed(path, resolve_type,
                                       egenCount=egenCount)

        fetching = True
        while fetching:
            try:
                entries = await self.waitFor(
                    eGenerator.__anext__(),
                    genTimeout
                )

                if entries is None:
                    # No entries were produced
                    raise UnixFSTimeoutError()

                for entry in entries:
                    yield entry
            except StopAsyncIteration:
                fetching = False

    async def objStat(self, path, timeout=30):
        try:
            stat = await self.waitFor(
                self.client.object.stat(await self.objectPathMapper(path)),
                timeout)
        except Exception:
            return None
        except aioipfs.APIError as err:
            self.debug(f'objStat {path}: error {err.message}')
            return None
        else:
            return stat

    async def objStatInfo(self, path, **kw):
        return StatInfo(await self.objStat(path, **kw))

    async def objStatCtxUpdate(self, path, timeout=30):
        exStat = self.objStatCtxGet(path)
        if exStat:
            return exStat
        try:
            self.ctx.objectStats[path] = await self.objStat(
                await self.objectPathMapper(path), timeout=timeout)
            return self.ctx.objectStats[path]
        except aioipfs.APIError:
            self.ctx.objectStats[path] = None

    def objStatCtxGet(self, path):
        return self.ctx.objectStats.get(path, None)

    async def hashComputePath(self, path, recursive=True):
        """
        Use the only-hash flag of the ipfs add command to compute
        the hash of a resource (does not add the data)
        """

        return await self.addPath(path, recursive=recursive, only_hash=True)

    async def hashComputeString(self, s, **kw):
        return await self.addString(s, only_hash=True, **kw)

    async def addPath(self, path, recursive=True, wrap=False,
                      callback=None, cidversion=1, offline=False,
                      dagformat='balanced', rawleaves=False,
                      hashfunc='sha2-256',
                      pin=True, useFileStore=False,
                      ignRulesPath=None,
                      hidden=False, only_hash=False, chunker=None):
        """
        Add files from ``path`` in the repo, and returns the top-level
        entry (the root directory), optionally wrapping it with a
        directory object

        :param str path: the path to the directory/file to import
        :param bool wrap: add a wrapping directory
        :param bool recursive: recursive import
        :param bool offline: offline mode
        :return: the IPFS top-level entry
        :rtype: dict
        """
        added = None
        exopts = {}
        callbackvalid = asyncio.iscoroutinefunction(callback)
        origPath = Path(path)

        if not origPath.exists():
            return None

        if dagformat == 'trickle':
            exopts['trickle'] = True

        if isinstance(chunker, str):
            exopts['chunker'] = chunker

        if ignRulesPath:
            exopts['ignore_rules_path'] = ignRulesPath

        if rawleaves:
            exopts['raw_leaves'] = rawleaves

        fileStoreEnabled = await self.daemonConfigGet(
            'Experimental.FilestoreEnabled')

        goIpfsPathEnv = os.environ.get('IPFS_PATH')
        ipfsRepoPath = Path(goIpfsPathEnv) if goIpfsPathEnv else None

        if fileStoreEnabled and useFileStore and ipfsRepoPath:
            # We'll only use the filestore in standalone mode, because
            # the filestore at the moment requires symlinking from $IPFS_PATH
            #
            # Root filestore path from where we symlink
            #
            # $IPFS_PATH/_gfstore/YYYYMM/<timefloat>

            fStorePath = ipfsRepoPath.joinpath(
                '_gfstore/{sep}/{t}'.format(
                    sep=datetime.today().strftime('%Y%m'),
                    t=time.time()
                )
            )

            try:
                if not fStorePath.exists():
                    # Create the root from where we store symlinks
                    fStorePath.mkdir(parents=True)

                # Link path uses the original path's basename
                linkPath = fStorePath.joinpath(origPath.name)

                if not linkPath.exists():
                    linkPath.symlink_to(
                        path,
                        target_is_directory=origPath.is_dir()
                    )

                    # Linking OK, set the right options for the filestore
                    # Dereference symlinks when using the filestore
                    exopts['dereference_args'] = True
                    exopts['nocopy'] = True

                    # What we pass to go-ipfs now is the symlink path
                    path = str(linkPath)
            except Exception as err:
                # Can't symlink ? Won't use the filestore
                self.debug(
                    f'Error symlinking {linkPath} to the filestore: {err}')

        try:
            async for entry in self.client.add(path, quiet=True,
                                               recursive=recursive,
                                               cid_version=cidversion,
                                               only_hash=only_hash,
                                               hash=hashfunc,
                                               hidden=hidden,
                                               wrap_with_directory=wrap,
                                               pin=pin,
                                               **exopts):
                await self.sleep()
                added = entry
                if callbackvalid:
                    await callback(entry)
        except aioipfs.APIError as err:
            self.debug('addPath: {path}: API error: {e}'.format(
                path=path, e=err.message))
            return None
        except asyncio.CancelledError:
            self.debug('addPath: cancelled')
            return None
        except Exception as e:
            self.debug('addPath: unknown exception {}'.format(str(e)))
            return None
        else:
            return added

    async def addFileEncrypted(self, path):
        basename = os.path.basename(path)
        buffSize = 262144
        readTotal = 0
        whole = io.BytesIO()

        try:
            async with aiofiles.open(path, 'rb') as fd:
                while True:
                    buff = await fd.read(buffSize)
                    if not buff:
                        break
                    await self.sleep()
                    readTotal += len(buff)
                    whole.write(buff)
        except:
            self.debug('Error occured while encrypting {path}'.format(
                path=path))
        else:
            whole.seek(0, 0)
            logUser.info('{n}: encrypting'.format(n=basename))
            return await self.rsaAgent.storeSelf(whole)

    async def addBytes(self, data, cidversion=1, **kw):
        try:
            return await self.client.core.add_bytes(
                data, cid_version=cidversion, **kw)
        except aioipfs.APIError as err:
            self.debug(err.message)
            return None

    async def addString(self, string, cidversion=1, **kw):
        try:
            return await self.client.core.add_str(
                string, cid_version=cidversion, **kw)
        except aioipfs.APIError as err:
            self.debug(err.message)
            return None

    async def addJson(self, obj, cidversion=1, **kw):
        try:
            return await self.client.core.add_bytes(
                orjson.dumps(obj),
                cid_version=cidversion, **kw)
        except aioipfs.APIError as err:
            self.debug(err.message)
            return None

    async def getJson(self, cid, timeout=5):
        try:
            data = await self.catObject(cid, timeout=timeout)
            return orjson.loads(data.decode())
        except aioipfs.APIError as err:
            self.debug(err.message)
            return None
        except Exception:
            self.debug(f'Cannot load JSON from CID {cid}')
            pass

    async def importQtResource(self, path):
        rscFile = QFile(':{0}'.format(path))

        try:
            rscFile.open(QFile.ReadOnly)
            data = rscFile.readAll().data()
            entry = await self.addBytes(data)
        except Exception as e:
            self.debug('importQtResource: {}'.format(str(e)))
        else:
            return entry

    async def closestPeers(self):
        peers = []
        try:
            info = await self.client.core.id()
            async for queryR in self.client.dht.query(info['ID']):
                responses = queryR.get('Responses', None)
                if not responses:
                    return None
                for resp in responses:
                    peers.append(resp['ID'])
            return peers
        except aioipfs.APIError:
            return None

    async def jsonLoad(self, path):
        try:
            data = await self.client.cat(path)
            return orjson.loads(data)
        except aioipfs.APIError as err:
            self.debug(err.message)
            return None

    async def ldInline(self, dagData):
        # In-line the JSON-LD contexts for JSON-LD usage

        async def process(data):
            if isinstance(data, dict):
                for objKey, objValue in data.items():
                    if objKey == '@context' and isinstance(objValue, dict):
                        link = objValue.get('/')
                        if not link:
                            continue

                        try:
                            ctx = await self.client.cat(link)
                            if ctx:
                                data.update(orjson.loads(ctx.decode()))
                        except Exception as err:
                            self.debug('ldInline error: {}'.format(
                                str(err)))
                    else:
                        await process(objValue)
            elif isinstance(data, list):
                for node in data:
                    await process(node)

            return data

        return await process(dagData)

    def ldContextsRootPath(self):
        return pkg_resources.resource_filename('galacteek.ld', 'contexts')

    async def ldContext(self, cName: str, source=None,
                        key=None):
        specPath = os.path.join(
            self.ldContextsRootPath(),
            '{context}'.format(
                context=cName
            )
        )

        if not os.path.isfile(specPath):
            return None

        try:
            with open(specPath, 'r') as fd:
                data = fd.read()

            entry = await self.addString(data)
        except Exception as err:
            self.debug(str(err))
        else:
            return self.ipld(entry)

    async def ldContextJson(self, cName: str):
        specPath = os.path.join(
            self.ldContextsRootPath(),
            '{context}'.format(
                context=cName
            )
        )

        if not os.path.isfile(specPath):
            return None

        try:
            data = await asyncReadFile(specPath, mode='rt')
            return orjson.loads(data)
        except Exception as err:
            self.debug(str(err))

    def ipld(self, cid):
        if isinstance(cid, str):
            return {"/": cid}
        elif isinstance(cid, dict) and 'Hash' in cid:
            return {"/": cid['Hash']}

    @cachedcoromethod(sResolveCache)
    async def objectPathMapCacheResolve(self, path):
        """
        Simple async TTL cache for results from nameResolveStreamFirst()
        """
        return await self.nameResolveStreamFirst(path, debug=False)

    def sResolveCacheClear(self, time=None):
        sResolveCache.expire(time)

    def sResolveCacheLog(self):
        self.debug('sResolveCacheDump: start')

        for path, r in sResolveCache.items():
            self.debug(f'sResolveCache: path {path} => {r}')

        self.debug('sResolveCacheDump: end')

    async def objectPathMapper(self, path):
        ipfsPath = path if isinstance(path, IPFSPath) else \
            IPFSPath(path, autoCidConv=True)

        if ipfsPath.isIpns:
            resolved = await self.objectPathMapCacheResolve(path)

            if resolved:
                return resolved['Path']
            else:
                self.debug(
                    'objectPathMapper: {o}: stream-resolve failed'.format(
                        o=path))

        return path

    async def catObject(self, path, offset=None, length=None, timeout=30):
        return await self.waitFor(
            self.client.cat(
                await self.objectPathMapper(path),
                offset=offset, length=length
            ), timeout
        )

    async def listObject(self, path, timeout=30):
        return await self.waitFor(
            self.client.core.ls(
                await self.objectPathMapper(path)
            ), timeout
        )

    async def walk(self, path):
        """
        Walks over UnixFS nodes and yields only paths of
        file objects.
        """
        try:
            result = await self.listObject(path)
        except aioipfs.APIError:
            pass
        else:
            _olist = result.get('Objects', [])
            if len(_olist) > 0:
                links = _olist.pop()['Links']

                for entry in links:
                    if entry['Type'] == 1:
                        async for value in self.walk(entry['Hash']):
                            yield value
                    elif entry['Type'] == 2:
                        fPath = IPFSPath(path).child(entry['Name'])
                        if fPath.valid:
                            yield (str(fPath), path)

    async def dagPut(self, data, pin=True, offline=False):
        """
        Create a new DAG object from data and returns the root CID of the DAG
        """
        dagFile = tempfile.NamedTemporaryFile()
        if not dagFile:
            return None
        try:
            dagFile.write(orjson.dumps(data))
        except Exception as e:
            self.debug('Cannot convert DAG object: {}'.format(str(e)))
            return None

        dagFile.seek(0, 0)
        try:
            output = await self.client.dag.put(
                dagFile.name, pin=pin, offline=offline)

            if isinstance(output, dict) and 'Cid' in output:
                return output['Cid'].get('/', None)
            else:
                self.debug('dagPut: no CID in output')
                return None
        except aioipfs.APIError as err:
            self.debug(err.message)
            return None

    async def dagPutOffline(self, data, pin=False):
        """
        Offline DAG put operation
        """
        return await self.dagPut(data, pin=pin, offline=True)

    async def dagGet(self, dagPath, timeout=10):
        """
        Get the DAG object referenced by the DAG path and returns a JSON object
        """

        output = await self.waitFor(
            self.client.dag.get(await self.objectPathMapper(dagPath)), timeout)

        if output is not None:
            return orjson.loads(output)

    async def dagStatBlocks(self, cid, timeout=360):
        # TODO
        # { 'Size': .., 'NumBlocks': ... }

        last = None

        async for stat in self.client.dag.stat(cid, progress=True):
            last = stat

        if last:
            return last['NumBlocks']

    async def dagResolve(self, dagPath):
        """
        Resolve DAG path and return CID if path is valid and rempath empty,
        None otherwise

        Relying on RemPath is tricky and should be changed asap
        """
        try:
            resolved = await self.client.dag.resolve(dagPath)
            log.debug('dagResolve {0} {1}'.format(dagPath, resolved))
            if isDict(resolved):
                return resolved['Cid'].get('/', None) if \
                    resolved['RemPath'] == '' else None
        except aioipfs.APIError as err:
            self.debug(err.message)
            return None

    async def findProviders(self, cid, peers, verbose, nproviders):
        """
        Don't call directly, use whoProvides instead

        :param str cid: CID key to lookup
        :param list peers: a list that will be updated with the peers found
        :param int nproviders: max number of providers to look for
        """
        try:
            self.debug('finding providers for: {}'.format(cid))

            async for prov in self.client.dht.findprovs(
                    cid, verbose=verbose,
                    numproviders=nproviders):
                pResponses = prov.get('Responses', None)
                pType = prov.get('Type', None)

                if pType != 4:  # WTF++
                    continue

                if isinstance(pResponses, list):
                    peers += pResponses
            return True
        except aioipfs.APIError as err:
            self.debug('findProviders: {}'.format(str(err.message)))
            return False
        except Exception as gerr:
            self.debug('findProviders: unknown error: {}'.format(
                str(gerr)))

    async def whoProvides(self, path, numproviders=20, timeout=20):
        """
        Return a list of peers which provide a given key, using the DHT
        'findprovs' API call.

        Because go-ipfs's findprovs will keep looking on the dht until it
        reaches the given numproviders, we use wait_for and a timeout so that
        you always get some information about the providers.

        :param int numproviders: max number of providers to look for
        :param int timeout: timeout (seconds)
        """

        peers = []
        try:
            resolved = await self.resolve(path)

            if not resolved:
                raise Exception(f'Cannot resolve {path}')

            await self.waitFor(
                self.findProviders(resolved, peers, True,
                                   numproviders), timeout)
        except asyncio.TimeoutError:
            # It timed out ? Return what we got
            self.debug('whoProvides: timed out')
            return peers
        except Exception:
            return peers

        return peers

    async def provide(self, multihash, recursive=False):
        """
        Announce to the network that we are providing this multihash

        :param str multihash: The multihash to announce
        :param bool recursive: Recursively provide the whole graph
        """
        provideRespCount = 0
        try:
            # Not much exception handling here.. if we get out of the
            # async generator alive, we consider that it's a success
            async for resp in self.client.dht.provide(
                    multihash, recursive=recursive):
                if not isinstance(resp, dict):
                    continue
                provideRespCount += 1

            self.debug('DHT provide {multihash}: {count} messages'.format(
                multihash=multihash, count=provideRespCount))
            return True
        except aioipfs.APIError:
            return False

    async def pingWrapper(self, peer, count=3):
        """
        Peer ping async generator, used internally by the operator for specific
        ping functions.

        Items yielded are tuples of the form (time, success, text) where time
        is the latency for the ping packet, success is boolean (True if ping
        ok) and text is the ping message

        :param str peer: Peer ID
        :param int count: ping count
        """

        async for pingReply in self.client.core.ping(peer, count=count):
            if pingReply is None:
                break

            pTime = pingReply.get('Time', None)
            pSuccess = pingReply.get('Success', None)
            pText = pingReply.get('Text', '')

            self.debug('PING: {peer} ({time}) {text} {success}'.format(
                peer=peer, time=pTime, text=pText,
                success='OK' if pSuccess is True else 'ERR'))

            yield (pTime, pSuccess, pText.strip())

            await self.sleep()

    async def pingLowest(self, peer, count=3):
        """
        Return lowest ping latency for a peer

        :param str peer: Peer ID
        :param int count: ping count
        """

        lowest = 0
        try:
            async for pTime, success, text in self.pingWrapper(
                    peer, count=count):
                if lowest == 0 and pTime != 0 and success is True:
                    lowest = pTime
                if pTime > 0 and pTime < lowest and success is True:
                    lowest = pTime
        except aioipfs.APIError:
            return 0
        else:
            return lowest

    async def pingAvg(self, peer, count=3):
        """
        Return average ping latency for a peer in msecs

        :param str peer: Peer ID
        :param int count: ping count
        :return: average latency in milliseconds or 0 if ping failed
        """

        received = []

        try:
            async for pTime, success, text in self.pingWrapper(
                    peer, count=count):
                if pTime != 0 and success is True:
                    received.append(pTime)
        except aioipfs.APIError:
            return 0

        if len(received) > 0:
            return float((sum(received) / len(received)) / 1000000)
        else:
            return 0

    async def rsaPubKeyCheckImport(self, pubKeyCid: str, pin=True):
        from galacteek.ipfs import kilobytes
        try:
            pubKeyStatInfo = await self.objStatInfo(pubKeyCid)
            if not pubKeyStatInfo.valid or \
                    pubKeyStatInfo.dataLargerThan(kilobytes(32)):
                return False

            pubKeyPem = await self.catObject(pubKeyCid, timeout=15)

            if not pubKeyPem:
                raise Exception(
                    f'Cannot fetch pubkey with CID: {pubKeyCid}')

            if pin:
                await self.pin(pubKeyCid, recursive=False, timeout=10)

            return pubKeyPem
        except aioipfs.APIError as err:
            self.debug(err.message)
            return None
        except Exception as err:
            self.debug(f'Err: {err}')
            return None

    async def pubsubPeers(self, topic=None, timeout=10):
        try:
            resp = await self.waitFor(self.client.pubsub.peers(
                topic=topic), timeout)
            return resp['Strings']
        except aioipfs.APIError as err:
            self.debug(err.message)
            return None
        except Exception as err:
            self.debug(f'pubsubPeers error: {err}')
            return None

    async def versionNum(self):
        try:
            vInfo = await self.client.core.version()
            return vInfo.get('Version', None)
        except aioipfs.APIError as err:
            self.debug(err.message)
            return None

    async def hasCommand(self, name, subcmd=None):
        """
        Determines whether a given command is available on this IPFS daemon,
        and if specified, if a subcommand of this command is available.

        :param str name: command name
        :param str subcmd: subcommand name
        """
        try:
            availCmds = await self.getCommands()
            if availCmds is None:
                return False

            for command in availCmds['Subcommands']:
                if subcmd is not None:
                    for subcommand in command['Subcommands']:
                        if subcommand['Name'] == subcmd:
                            return True
                if command['Name'] == name and subcmd is None:
                    return True
            return False
        except aioipfs.APIError as err:
            self.debug(err.message)
            return False

    def ourNode(self, peerId):
        return self.ctx.node.id == peerId

    async def hasDagCommand(self):
        return await self.hasCommand('dag')

    async def hasP2PCommand(self):
        return await self.hasCommand('p2p')

    @async_enterable
    async def ldOps(self):
        if not self._ldDocLoader:
            self._ldDocLoader = await aioipfs_document_loader(self.client)

        return LDOpsContext(
            self,
            self._ldDocLoader
        )

    @async_enterable
    async def p2pDialer(self, peer, protocol, address=None, addressAuto=True):
        from galacteek.core import unusedTcpPort
        from galacteek.ipfs.tunnel import protocolFormat

        if addressAuto is True and not address:
            address = '/ip4/127.0.0.1/tcp/{}'.format(unusedTcpPort())

        if await self.client.agent_version_post0418():
            proto = protocolFormat(protocol)
        else:
            proto = protocol

        log.debug('Stream dial {0} {1}'.format(peer, proto))
        try:
            peerAddr = joinIpfs(peer) if not peer.startswith('/ipfs/') else \
                peer
            resp = await self.client.p2p.dial(proto, address, peerAddr)
        except aioipfs.APIError as err:
            log.debug('Stream dial error: {}'.format(err.message))
            return TunnelDialerContext(self, peer, proto, None)
        else:
            log.debug('Stream dial {0} {1}: OK'.format(peer, proto))

        if resp:
            maddr = resp.get('Address', None)
            if not maddr:
                return TunnelDialerContext(self, peer, proto, None)

            ipaddr, port = multiAddrTcp4(maddr)

            if ipaddr is None or port == 0:
                return TunnelDialerContext(self, peer, proto, None)

            return TunnelDialerContext(self, peer, proto, maddr)
        else:
            return TunnelDialerContext(self, peer, proto, address)

    @async_enterable
    async def getContexted(self, path, dstdir, **kwargs):
        return GetContext(self, path, dstdir, **kwargs)


class IPFSOpRegistry:
    _registry = {}
    _key_default = 0

    @staticmethod
    def reg(key, inst):
        if key not in IPFSOpRegistry._registry:
            IPFSOpRegistry._registry[key] = inst

    @staticmethod
    def get(key):
        return IPFSOpRegistry._registry.get(key, None)

    @staticmethod
    def regDefault(inst):
        return IPFSOpRegistry.reg(IPFSOpRegistry._key_default, inst)

    @staticmethod
    def getDefault():
        return IPFSOpRegistry._registry.get(IPFSOpRegistry._key_default)


class GalacteekOperator(IPFSOperator):
    """
    Extend IPFSOperator with stuff specific to galacteek
    like P2P tunnel calls
    """

    async def didPing(self, peerId, did, token):
        """
        Does a POST on /didping on the didauth-vc-pss P2P service

        Returns a tuple (ms, pongPayload)
        """
        req = {
            'did': did,
            'ident_token': token
        }

        try:
            log.debug(f'didPing({did}) for peer {peerId} with token: {token}')

            async with self.p2pDialer(
                    peerId, 'didauth-vc-pss',
                    addressAuto=True) as sCtx:
                if sCtx.failed:
                    raise Exception(f'Cannot ping {peerId}')

                startt = self.client.loop.time()
                async with sCtx.session.post(
                        sCtx.httpUrl('/didping'),
                        json=req) as resp:

                    diff = self.client.loop.time() - startt
                    if resp.status != HTTPOk.status_code:
                        raise Exception(f'DID Ping error for {did}')

                    payload = await resp.json()
                    assert isinstance(payload['didpong'], dict)
                    assert did in payload['didpong']

                    return diff * 1000, payload
        except Exception as err:
            log.debug(f'didPing error: {err}')
            return -1, None
