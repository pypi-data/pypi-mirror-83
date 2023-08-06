import os
import os.path
import re
import sys
import codecs
import subprocess
import glob
import shutil
import json

from setuptools import setup
from setuptools import Command
from distutils.command.build import build

PY_VER = sys.version_info

if PY_VER >= (3, 6):
    pass
else:
    print('You need python3.6 or newer')
    print('Your python version is {0}'.format(PY_VER))
    raise RuntimeError('Invalid python version')

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(
        __file__)), 'galacteek', '__init__.py'), 'r', 'latin1') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'\r?$",
                             fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


def run(*args):
    p = subprocess.Popen(*args, stdout=subprocess.PIPE)
    stdout, err = p.communicate()
    return stdout


class build_docs(Command):
    user_options = [
        ("all=", None, "Build all docs"),
    ]

    def initialize_options(self):
        self.all = None

    def finalize_options(self):
        pass

    def run(self):
        from sphinx import build_main
        args = [sys.argv[0], '-b', 'html',
                'galacteek/docs/manual/en',
                'galacteek/docs/manual/en/html']

        if self.all:
            args.append('-a')

        build_main(args)


class build_contracts(Command):
    user_options = [
        ("deploy=", None, "Deploy given contracts"),
        ("contracts=", None, "Contracts list to build"),
        ("rpcurl=", None, "Ethereum RPC url"),
    ]

    def initialize_options(self):
        self.deploy = None
        self.contracts = None
        self.rpcurl = 'http://127.0.0.1:7545'

    def finalize_options(self):
        pass

    def run(self):
        from web3 import Web3
        from galacteek.smartcontracts import listContracts
        from galacteek.smartcontracts import solCompileFile
        from galacteek.smartcontracts import vyperCompileFile
        from galacteek.dweb.ethereum.contract import contractDeploy

        usrcontracts = [c for c in self.contracts.split(',')] if \
            self.contracts else ['*']
        cdeploy = [c for c in self.deploy.split(',')] if \
            self.deploy else []

        w3 = Web3(Web3.HTTPProvider(self.rpcurl))
        w3.eth.defaultAccount = w3.eth.accounts[0]

        for contract in listContracts():
            print('>', contract, contract.dir)

            if usrcontracts != ['*'] and contract not in usrcontracts:
                continue

            ifacePath = os.path.join(contract.dir, 'interface.json')

            if contract.type == 'vyper':
                iface = vyperCompileFile(contract.sourcePath)
                if not iface:
                    print('Error compiling vyper contract')
                    continue
            elif contract.type == 'solidity':
                compiled = solCompileFile(contract.sourcePath)
                if not compiled:
                    print('Error compiling solidity contract')
                    continue
                contractId, iface = compiled.popitem()
            else:
                continue

            try:
                with open(ifacePath, 'w+t') as ifacefd:
                    ifacefd.write(json.dumps(iface, indent=4))
            except Exception as err:
                print(str(err))
            else:
                print(contract.name, 'compiled')
                if contract.name in cdeploy:
                    addr = contractDeploy(w3, iface)
                    print(contract.name, 'deployed at', addr)


class build_ui(Command):
    user_options = [
        ("uiforms=", None, "UI forms list to build, separated by ','"),
    ]

    def initialize_options(self):
        self.uiforms = None

        # Forms where we don't want to have automatic slots
        # connection with connectSlotsByName()
        self.uiforms_noSlotConnect = [
            'galacteek/ui/browsertab.ui',
            'galacteek/ui/dagview.ui',
            'galacteek/ui/files.ui',
            'galacteek/ui/qschemecreatemapping.ui'
        ]

    def finalize_options(self):
        pass

    def filterUic(self, uifile, uicpath):
        if uifile in self.uiforms_noSlotConnect:
            print('* {ui}: Removing automatic slots connection'.format(
                ui=uifile))

            with open(uicpath, 'rt') as fd:
                code = fd.read()

            nCode = re.sub(
                r'^\s*QtCore.QMetaObject.connectSlotsByName.*\n$', '',
                code,
                flags=re.MULTILINE
            )

            with open(uicpath, 'wt') as fd:
                print('* {ui}: Rewriting {path}'.format(
                    ui=uifile, path=uicpath))
                fd.write(nCode)

    def run(self):
        uifiles = []
        uidir = 'galacteek/ui'

        if self.uiforms:
            uifiles = [os.path.join(uidir, '{0}.ui'.format(form)) for form
                       in self.uiforms.split(',')]
        else:
            uifiles = glob.iglob('{}/*.ui'.format(uidir))

        for uifile in uifiles:
            print('* Building UI form:', uifile)
            base = os.path.basename(uifile).replace('.ui', '')
            out = 'ui_{}.py'.format(base)
            fp_out = os.path.join(uidir, out)

            run(['pyuic5', '--from-imports',
                 uifile,
                 '-o', fp_out])

            self.filterUic(uifile, fp_out)

        run(['pylupdate5', '-verbose', 'galacteek.pro'])

        trdir = './share/translations'
        lrelease = shutil.which('lrelease-qt5')

        if not lrelease:
            lrelease = shutil.which('lrelease')

        for lang in ['en', 'fr']:
            if lrelease:
                run([lrelease,
                     os.path.join(trdir, 'galacteek_{}.ts'.format(lang)),
                     '-qm',
                     os.path.join(trdir, 'galacteek_{}.qm'.format(lang))])
            else:
                print('lrelease was not found, cannot build translation files')

        run(['pyrcc5', os.path.join(uidir, 'galacteek.qrc'), '-o',
             os.path.join(uidir, 'galacteek_rc.py')])


class _build(build):
    sub_commands = [('build_ui', None)] + build.sub_commands


with open('README.rst', 'r') as fh:
    long_description = fh.read()

deps_links = []
install_reqs = []
with open('requirements.txt') as f:
    lines = f.read().splitlines()
    for line in lines:
        if line.startswith('-e'):
            link = line.split().pop()
            deps_links.append(link)
        else:
            install_reqs.append(line)

setup(
    name='galacteek',
    version=version,
    license='GPL3',
    author='David Ferlier',
    author_email='galacteek@protonmail.com',
    url='https://github.com/pinnaculum/galacteek',
    description='Browser for the distributed web',
    long_description=long_description,
    include_package_data=True,
    cmdclass={
        'build': _build,
        'build_ui': build_ui,
        'build_docs': build_docs,
        'build_contracts': build_contracts
    },
    packages=[
        'galacteek',
        'galacteek.docs',
        'galacteek.docs.manual',
        'galacteek.core',
        'galacteek.core.edags',
        'galacteek.core.models',
        'galacteek.crypto',
        'galacteek.database',
        'galacteek.database.models',
        'galacteek.did',
        'galacteek.ipfs',
        'galacteek.ipfs.pubsub',
        'galacteek.ipfs.pubsub.srvs',
        'galacteek.ipfs.pubsub.messages',
        'galacteek.ipfs.pb',
        'galacteek.ipfs.p2pservices',
        'galacteek.ipdapps',
        'galacteek.ld',
        'galacteek.ld.contexts',
        'galacteek.hashmarks',
        'galacteek.hashmarks.default',
        'galacteek.templates',
        'galacteek.dweb',
        'galacteek.dweb.ethereum',
        'galacteek.smartcontracts',
        'galacteek.space',
        'galacteek.ui',
        'galacteek.ui.dwebspace',
        'galacteek.ui.orbital'
    ],
    install_requires=install_reqs,
    dependency_links=deps_links,
    package_data={
        'galacteek': [
            'docs/manual/en/html/*.html',
            'docs/manual/en/html/_images/*',
            'docs/manual/en/html/_static/*',
            'ld/contexts/*',
            'ld/contexts/messages/*',
            'templates/*.html',
            'templates/layouts/*',
            'templates/usersite/*.html',
            'templates/usersite/assets/*',
            'templates/usersite/assets/css/*',
            'templates/usersite/macros/*',
            'templates/imggallery/*.html',
            'hashmarks/default/*.yaml'
        ]
    },
    entry_points={
        'gui_scripts': [
            'galacteek = galacteek.guientrypoint:start'
        ]
    },
    extras_require={
        'docs': [
            'sphinx>=1.7.0'
        ]
    },
    classifiers=[
        'Environment :: X11 Applications :: Qt',
        'Framework :: AsyncIO',
        'Topic :: Desktop Environment :: File Managers',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: System :: Filesystems',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords=[
        'asyncio',
        'aiohttp',
        'ipfs'
    ]
)
