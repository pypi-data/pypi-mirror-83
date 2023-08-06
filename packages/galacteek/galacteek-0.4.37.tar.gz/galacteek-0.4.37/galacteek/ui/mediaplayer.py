import os.path
import functools

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QFont

from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtMultimedia import QMediaPlaylist
from PyQt5.QtMultimedia import QMultimedia

from PyQt5.QtMultimediaWidgets import QVideoWidget

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QTime
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QItemSelectionModel

from galacteek.core.jsono import *
from galacteek.ipfs.cidhelpers import joinIpfs
from galacteek.ipfs.cidhelpers import qurlPercentDecode
from galacteek.ipfs.ipfsops import *

from . import ui_mediaplaylist

from .clipboard import iClipboardEmpty
from .widgets import *
from .helpers import *


def iPlayerUnavailable():
    return QCoreApplication.translate(
        'MediaPlayer',
        'No media player support available on your system')


def iPlayerError(code):
    return QCoreApplication.translate(
        'MediaPlayer',
        'Media player error (code: {0})').format(code)


def iFullScreen():
    return QCoreApplication.translate('MediaPlayer', 'Fullscreen')


def iCopyPlaylistPath():
    return QCoreApplication.translate(
        'MediaPlayer',
        "Copy playlist's IPFS path to the clipboard")


def iLoadPlaylistFromPath():
    return QCoreApplication.translate(
        'MediaPlayer',
        'Load playlist from the clipboard')


def iCannotLoadPlaylist():
    return QCoreApplication.translate('MediaPlayer',
                                      'Cannot load playlist')


def iPlaylistExists():
    return QCoreApplication.translate(
        'MediaPlayer',
        'A playlist with this name already exists')


def iPlaylistRemoveMedia():
    return QCoreApplication.translate(
        'MediaPlayer',
        'Remove media from playlist')


def iPlaylistName():
    return QCoreApplication.translate(
        'MediaPlayer',
        'Playlist name')


def iAlreadyInPlaylist():
    return QCoreApplication.translate('MediaPlayer',
                                      'Already queued in the current playlist')


def iNoMediaInPlaylist():
    return QCoreApplication.translate(
        'MediaPlayer', 'No media in playlist')


def mediaPlayerAvailable(player=None):
    if player is None:
        player = QMediaPlayer()
    availability = player.availability()
    return availability == QMultimedia.Available


def durationConvert(duration):
    return QTime((duration / 3600) % 60, (duration / 60) % 60,
                 duration % 60, (duration * 1000) % 1000)


class JSONPlaylistV1(QJSONObj):
    """
    V1 JSON playlist document
    """

    def prepare(self, root):
        root['playlist'] = {
            'name': self.listName,
            'formatv': 1,
            'items': []
        }

        for path in self.itemPaths:
            root['playlist']['items'].append({
                'path': path
            })
        self.changed.emit()

    def items(self):
        return self.root['playlist']['items']


class MPlayerVideoWidget(QVideoWidget):
    def __init__(self, player, parent=None):
        super(MPlayerVideoWidget, self).__init__(parent)
        self.player = player

    def keyPressEvent(self, event):
        mSecMove = 3000
        pos = self.player.position()

        if event.key() == Qt.Key_Escape:
            self.viewFullScreen(False)

        if event.key() == Qt.Key_Right:
            self.player.setPosition(pos + mSecMove)
        if event.key() == Qt.Key_Left:
            pos = self.player.position()
            if pos > mSecMove:
                self.player.setPosition(pos - mSecMove)
            else:
                self.player.setPosition(0)

        if event.key() == Qt.Key_Up:
            pos = self.player.position()
            self.player.setPosition(pos + mSecMove * 2)

        if event.key() == Qt.Key_Down:
            pos = self.player.position()
            if pos > mSecMove * 2:
                self.player.setPosition(pos - mSecMove * 2)
            else:
                self.player.setPosition(0)
        if event.key() == Qt.Key_F:
            self.viewFullScreen(not self.isFullScreen())

        super(MPlayerVideoWidget, self).keyPressEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.viewFullScreen(not self.isFullScreen())
        super(MPlayerVideoWidget, self).mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        self.changeFocus()
        super(MPlayerVideoWidget, self).mousePressEvent(event)

    def viewFullScreen(self, fullscreen):
        self.setFullScreen(fullscreen)
        if fullscreen:
            self.setCursor(Qt.BlankCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        self.changeFocus()

    def changeFocus(self):
        QTimer.singleShot(0, functools.partial(self.setFocus,
                                               Qt.OtherFocusReason))


class MediaPlayerTab(GalacteekTab):
    statePlaying = QMediaPlayer.PlayingState
    statePaused = QMediaPlayer.PausedState
    stateStopped = QMediaPlayer.StoppedState

    def __init__(self, gWindow):
        super(MediaPlayerTab, self).__init__(gWindow, sticky=True)

        self.playlistIpfsPath = None
        self.playlist = QMediaPlaylist()
        self.model = ListModel(self.playlist)

        self.playlistsMenu = QMenu(self)
        self.playlistsMenu.triggered.connect(self.onPlaylistsMenu)

        self.pListWidget = QWidget(self)
        self.uipList = ui_mediaplaylist.Ui_MediaPlaylist()
        self.uipList.setupUi(self.pListWidget)
        self.uipList.savePlaylistButton.clicked.connect(self.onSavePlaylist)
        self.uipList.savePlaylistButton.setEnabled(False)
        self.uipList.loadPlaylistButton.setPopupMode(
            QToolButton.InstantPopup)
        self.uipList.loadPlaylistButton.setMenu(self.playlistsMenu)

        self.clipMenu = QMenu(self)
        self.copyPathAction = QAction(getIconIpfsIce(),
                                      iCopyPlaylistPath(), self,
                                      triggered=self.onCopyPlaylistPath)
        self.loadPathAction = QAction(getIconIpfsIce(),
                                      iLoadPlaylistFromPath(), self,
                                      triggered=self.onLoadPlaylistPath)

        self.copyPathAction.setEnabled(False)
        self.clipMenu.addAction(self.copyPathAction)
        self.clipMenu.addAction(self.loadPathAction)

        self.uipList.clipPlaylistButton.setPopupMode(
            QToolButton.InstantPopup)
        self.uipList.clipPlaylistButton.setMenu(self.clipMenu)
        self.uipList.clearButton.clicked.connect(self.onClearPlaylist)

        self.uipList.nextButton.clicked.connect(self.onPlaylistNext)
        self.uipList.previousButton.clicked.connect(self.onPlaylistPrevious)
        self.uipList.nextButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.uipList.previousButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSkipBackward))

        self.pListView = self.uipList.listView
        self.pListView.mousePressEvent = self.playlistMousePressEvent
        self.pListView.setModel(self.model)
        self.pListView.setResizeMode(QListView.Adjust)
        self.pListView.setMinimumWidth(self.width() / 2)

        self.duration = None
        self.playerState = None
        self.player = QMediaPlayer(self)
        self.player.setPlaylist(self.playlist)

        self.videoWidget = MPlayerVideoWidget(self.player, self)
        self.useUpdates(True)
        self.videoWidget.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.player.setVideoOutput(self.videoWidget)

        self.player.error.connect(self.onError)
        self.player.stateChanged.connect(self.onStateChanged)
        self.player.metaDataChanged.connect(self.onMetaData)
        self.player.durationChanged.connect(self.mediaDurationChanged)
        self.player.positionChanged.connect(self.mediaPositionChanged)
        self.player.videoAvailableChanged.connect(self.onVideoAvailable)

        self.pListView.activated.connect(self.onListActivated)
        self.playlist.currentIndexChanged.connect(self.playlistPositionChanged)
        self.playlist.currentMediaChanged.connect(self.playlistMediaChanged)
        self.playlist.mediaInserted.connect(self.playlistMediaInserted)
        self.playlist.mediaRemoved.connect(self.playlistMediaRemoved)

        self.togglePList = QToolButton(self)
        self.togglePList.setIcon(self.style().standardIcon(
            QStyle.SP_ArrowRight))
        self.togglePList.setFixedSize(32, 128)
        self.togglePList.clicked.connect(self.onTogglePlaylist)

        self.clipboardMediaItem = None
        self.clipboardButton = QToolButton(clicked=self.onClipboardClicked)
        self.clipboardButton.setIcon(getIconClipboard())
        self.clipboardButton.setEnabled(False)
        self.clipboardButton.setToolTip('Load media from clipboard')

        self.pinButton = QToolButton(clicked=self.onPinMediaClicked)
        self.pinButton.setIcon(getIcon('pin.png'))

        self.processClipboardItem(self.app.clipTracker.current, force=True)
        self.app.clipTracker.currentItemChanged.connect(self.onClipItemChange)

        self.playButton = QToolButton(clicked=self.onPlayClicked)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        self.pauseButton = QToolButton(clicked=self.onPauseClicked)
        self.pauseButton.setIcon(self.style().standardIcon(
            QStyle.SP_MediaPause))
        self.pauseButton.setEnabled(False)

        self.stopButton = QToolButton(clicked=self.onStopClicked)
        self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopButton.setEnabled(False)

        self.fullscreenButton = QToolButton(clicked=self.onFullScreen)
        self.fullscreenButton.setIcon(getIcon('fullscreen.png'))
        self.fullscreenButton.setToolTip(iFullScreen())

        self.seekSlider = QSlider(Qt.Horizontal, sliderMoved=self.onSeek)
        self.seekSlider.sliderReleased.connect(self.onSliderReleased)
        self.seekSlider.setObjectName('mediaPlayerSlider')
        self.durationLabel = QLabel()

        vLayout = QVBoxLayout()
        hLayoutControls = QHBoxLayout()
        hLayoutControls.setContentsMargins(0, 0, 0, 0)
        hLayoutControls.addWidget(self.clipboardButton)
        hLayoutControls.addWidget(self.pinButton)
        hLayoutControls.addWidget(self.playButton)
        hLayoutControls.addWidget(self.pauseButton)
        hLayoutControls.addWidget(self.stopButton)
        hLayoutControls.addWidget(self.seekSlider)
        hLayoutControls.addWidget(self.durationLabel)
        hLayoutControls.addWidget(self.fullscreenButton)
        vLayout.addWidget(self.videoWidget)
        vLayout.addLayout(hLayoutControls)

        hLayout = QHBoxLayout()
        hLayout.addLayout(vLayout)
        hLayout.addWidget(self.pListWidget)
        hLayout.addWidget(self.togglePList)

        self.pListWidget.hide()

        self.vLayout.addLayout(hLayout)
        self.update()
        self.videoWidget.changeFocus()

    @property
    def isPlaying(self):
        return self.playerState == self.statePlaying

    @property
    def isPaused(self):
        return self.playerState == self.statePaused

    @property
    def isStopped(self):
        return self.playerState == self.stateStopped

    def useUpdates(self, updates=True):
        # Enable widget updates or not on the video widget
        self.videoWidget.setUpdatesEnabled(updates)

    def update(self):
        self.app.task(self.updatePlaylistsMenu)

    def onFullScreen(self):
        self.videoWidget.viewFullScreen(True)

    def onClearPlaylist(self):
        self.copyPathAction.setEnabled(False)
        self.player.stop()
        self.clearPlaylist()

    def onLoadPlaylistPath(self):
        current = self.app.clipTracker.getCurrent()
        if current:
            self.app.task(self.loadPlaylistFromPath, current.path)

    def onCopyPlaylistPath(self):
        if self.playlistIpfsPath:
            self.app.setClipboardText(self.playlistIpfsPath)

    def onPinMediaClicked(self):
        currentMedia = self.playlist.currentMedia()
        if currentMedia.isNull():
            return messageBox(iNoMediaInPlaylist())

        ensure(self.pinMedia(currentMedia))

    @ipfsOp
    async def pinMedia(self, ipfsop, media):
        mediaUrl = qurlPercentDecode(media.canonicalUrl())
        path = IPFSPath(mediaUrl, autoCidConv=True)

        if path.valid:
            await ipfsop.ctx.pin(str(path), qname='mediaplayer')

    @ipfsOp
    async def updatePlaylistsMenu(self, ipfsop):
        currentList = [action.text() for action in
                       self.playlistsMenu.actions()]
        listing = await ipfsop.filesList(self.profile.pathPlaylists)
        for entry in listing:
            if entry['Name'] in currentList:
                continue
            action = QAction(entry['Name'], self)
            action.setData(entry)
            self.playlistsMenu.addAction(action)

    def playlistShowContextMenu(self, event):
        selModel = self.pListView.selectionModel()
        idx = self.pListView.indexAt(event.pos())
        if not idx.isValid():
            return

        path = self.model.data(idx)
        if path:
            selModel.reset()
            selModel.select(
                idx, QItemSelectionModel.Select
            )

            menu = QMenu(self)
            menu.addAction(
                getIcon('clear-all.png'),
                iPlaylistRemoveMedia(), functools.partial(
                    self.onRemoveMediaFromIndex, idx))
            menu.exec_(event.globalPos())

    def onRemoveMediaFromIndex(self, idx):
        self.playlist.removeMedia(idx.row())

    def playlistMousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.pListView.selectionModel().reset()
            self.playlistShowContextMenu(event)
        else:
            if not self.pListView.indexAt(event.pos()).isValid():
                self.deselectPlaylistItems()

            QListView.mousePressEvent(self.pListView, event)

    def onPlaylistsMenu(self, action):
        entry = action.data()
        self.app.task(self.loadPlaylistFromPath, joinIpfs(entry['Hash']))

    def onSavePlaylist(self):
        paths = self.playlistGetPaths()
        listName = inputText(title=iPlaylistName(), label=iPlaylistName())
        if not listName:
            return

        obj = JSONPlaylistV1(listName=listName, itemPaths=paths)
        self.app.task(self.savePlaylist, obj, listName)

    @ipfsOp
    async def savePlaylist(self, ipfsop, obj, name):
        objPath = os.path.join(self.profile.pathPlaylists, name)
        exists = await ipfsop.filesStat(objPath)

        if exists:
            await ipfsop.filesRm(objPath)

        ent = await ipfsop.client.core.add_json(obj.root)

        if ent:
            await ipfsop.filesLinkFp(ent, objPath)
            self.playlistIpfsPath = joinIpfs(ent['Hash'])
            self.copyPathAction.setEnabled(True)

        self.update()

    @ipfsOp
    async def loadPlaylistFromPath(self, ipfsop, path):
        try:
            obj = await ipfsop.jsonLoad(path)
        except Exception:
            return messageBox(iCannotLoadPlaylist())

        if obj is None:
            return messageBox(iCannotLoadPlaylist())

        try:
            # Assume v1 format for now, when the format evolves we'll just
            # use json validation
            pList = JSONPlaylistV1(data=obj)
            self.clearPlaylist()

            for item in pList.items():
                self.queueFromPath(item['path'])

            self.playlistIpfsPath = path
            self.copyPathAction.setEnabled(True)
        except Exception:
            return messageBox(iCannotLoadPlaylist())

    def playlistMediaInserted(self, start, end):
        self.uipList.savePlaylistButton.setEnabled(
            self.playlist.mediaCount() > 0)

    def playlistMediaRemoved(self, start, end):
        self.uipList.savePlaylistButton.setEnabled(
            self.playlist.mediaCount() > 0)

        self.model.modelReset.emit()

    def playlistGetPaths(self):
        return [u.path() for u in self.playlistGetUrls()]

    def playlistGetUrls(self):
        urls = []
        for idx in range(0, self.playlist.mediaCount()):
            media = self.playlist.media(idx)
            urls.append(media.canonicalUrl())
        return urls

    def onClipItemChange(self, item):
        self.processClipboardItem(item)

    def processClipboardItem(self, item, force=False):
        if not item:
            return

        def analyzeMimeType(cItem):
            if cItem.mimeCategory in ['audio', 'video', 'image']:
                self.clipboardMediaItem = cItem
                self.clipboardButton.setEnabled(True)
                self.clipboardButton.setToolTip(cItem.path)
            else:
                self.clipboardButton.setEnabled(False)
                self.clipboardButton.setToolTip(iClipboardEmpty())

        if force:
            analyzeMimeType(item)
        else:
            item.mimeTypeAvailable.connect(
                lambda mType: analyzeMimeType(item))

    def onClipboardClicked(self):
        if self.clipboardMediaItem:
            self.playFromPath(self.clipboardMediaItem.path)
        else:
            messageBox('Not a multimedia resource')

    def onSliderReleased(self):
        pass

    def onPlaylistNext(self):
        self.playlist.next()

    def onPlaylistPrevious(self):
        self.playlist.previous()

    def onPlayClicked(self):
        self.player.play()

    def onPauseClicked(self):
        if self.isPlaying:
            self.player.pause()
        elif self.isPaused:
            self.player.play()

    def onStopClicked(self):
        self.player.stop()
        self.player.setPosition(0)
        self.seekSlider.setValue(0)
        self.seekSlider.setRange(0, 0)

    def onSeek(self, seconds):
        if self.player.isSeekable():
            self.player.setPosition(seconds * 1000)

    def showEvent(self, event):
        if self.playlist.mediaCount() == 0:
            self.pListWidget.setVisible(True)

        super().showEvent(event)

    def onTogglePlaylist(self):
        self.togglePlaylist()

    def togglePlaylist(self):
        self.pListWidget.setVisible(self.pListWidget.isHidden())

    def onError(self, error):
        messageBox(iPlayerError(error))

    def onStateChanged(self, state):
        self.playerState = state
        self.updateControls(state)

    def updateControls(self, state):
        if self.isStopped:
            self.stopButton.setEnabled(False)
            self.pauseButton.setEnabled(False)
            self.playButton.setEnabled(True)
            self.seekSlider.setEnabled(False)
            self.duration = None
        elif self.isPlaying:
            self.seekSlider.setRange(0, self.player.duration() / 1000)
            self.seekSlider.setEnabled(True)
            self.pauseButton.setEnabled(True)
            self.playButton.setEnabled(False)
            self.stopButton.setEnabled(True)

    def onListActivated(self, index):
        if index.isValid():
            self.playlist.setCurrentIndex(index.row())
            self.player.play()

    def onMetaData(self):
        # Unfinished
        if self.player.isMetaDataAvailable():
            availableKeys = self.player.availableMetaData()

            for key in availableKeys:
                self.player.metaData(key)

    def playFromUrl(self, url, mediaName=None):
        if self.isPlaying:
            self.player.stop()

        cUrls = self.playlistGetUrls()
        for u in cUrls:
            if u.toString() == url.toString():
                return messageBox(iAlreadyInPlaylist())

        media = QMediaContent(url)
        if self.playlist.addMedia(media):
            count = self.model.rowCount()
            if count > 0:
                self.playlist.setCurrentIndex(count - 1)

        self.player.play()

    def playFromPath(self, path, mediaName=None):
        mediaUrl = self.app.subUrl(path)
        self.playFromUrl(mediaUrl)

    def queueFromPath(self, path, playLast=False, mediaName=None):
        mediaUrl = self.app.subUrl(path)
        self.playlist.addMedia(QMediaContent(mediaUrl))

        if playLast:
            count = self.playlist.mediaCount()

            if count > 0:
                self.player.stop()
                self.playlist.setCurrentIndex(count - 1)
                self.player.play()

    def clearPlaylist(self):
        self.playlist.clear()
        self.pListView.reset()

    def playlistPositionChanged(self, position):
        self.pListView.setCurrentIndex(self.model.index(position, 0))

    def deselectPlaylistItems(self):
        self.pListView.selectionModel().reset()

    def playlistMediaChanged(self, media):
        selModel = self.pListView.selectionModel()

        self.deselectPlaylistItems()

        self.model.modelReset.emit()
        idx = self.model.index(self.playlist.currentIndex(), 0)
        if idx.isValid():
            selModel.select(idx, QItemSelectionModel.Select)

    def onVideoAvailable(self, available):
        if available:
            if self.isPlaying:
                self.useUpdates(False)
            elif self.isStopped or self.isPaused:
                self.useUpdates(True)
        else:
            self.useUpdates(True)

    def mediaDurationChanged(self, duration):
        self.duration = duration / 1000
        self.seekSlider.setMaximum(self.duration)

    def mediaPositionChanged(self, progress):
        progress /= 1000

        if self.duration:
            cTime = durationConvert(progress)
            tTime = durationConvert(self.duration)
            self.durationLabel.setText('{0} ({1})'.format(
                cTime.toString(), tTime.toString()))

        if not self.seekSlider.isSliderDown():
            self.seekSlider.setValue(progress)

    async def onClose(self):
        self.player.stop()
        self.player.setMedia(QMediaContent(None))
        return True

    def playerAvailable(self):
        return mediaPlayerAvailable(player=self.player)


class ListModel(QAbstractItemModel):
    def __init__(self, playlist, parent=None):
        super(ListModel, self).__init__(parent)
        self.playlist = playlist
        self.playlist.mediaAboutToBeInserted.connect(
            self.beginInsertItems)
        self.playlist.mediaInserted.connect(self.endInsertItems)
        self.playlist.mediaChanged.connect(self.changeItems)

    def rowCount(self, parent=QModelIndex()):
        return self.playlist.mediaCount()

    def columnCount(self, parent=QModelIndex()):
        return 1 if not parent.isValid() else 0

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column)

    def parent(self, child):
        return QModelIndex()

    def beginInsertItems(self, start, end):
        self.beginInsertRows(QModelIndex(), start, end)

    def endInsertItems(self):
        self.endInsertRows()

    def changeItems(self, start, end):
        self.dataChanged.emit(self.index(start, 0), self.index(end, 1))

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return

        if role == Qt.DisplayRole:
            if index.column() == 0:
                media = self.playlist.media(index.row())
                if media is None:
                    return iUnknown()
                location = media.canonicalUrl()
                path = location.path()
                basename = os.path.basename(path)
                if basename:
                    return basename
                else:
                    return path
            return self.m_data[index]
        elif role == Qt.FontRole:
            curPlIndex = self.playlist.currentIndex()

            font = QFont('Times', pointSize=12)

            if curPlIndex == index.row():
                font = QFont('Times', pointSize=14)
                font.setBold(True)
                return font
            else:
                return QFont('Times', pointSize=12)

        return None
