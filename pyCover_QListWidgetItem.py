from PyQt4.QtGui import *
from coverDownload import CoverDownload
from PyQt4 import QtCore

class pyCover_QListWidgetItem(QListWidgetItem):
    """
    We inherit from QListWidgetItem so we can add it to a QListWidget
    and still keep information about the artist and album, and
    associate this item with List_Artwork.
    """
    def __init__(self, artist, album):
        QListWidgetItem.__init__(self,QIcon(QPixmap('resources/icon_unknown_cover_100.png')),"{0} - {1}".format(artist.encode("utf-8"), album.encode("utf-8")))
        self.artist = artist
        self.album = album
        self.covers = []
        self.coversDownloaded = False

    def getArtist(self):
        return self.artist.encode("utf-8")

    def getAlbum(self):
        return self.album.encode("utf-8")

    def showArtwork(self, artworkList):
        artworkList.clear()
        artworkList.addItem(QListWidgetItem(QIcon(QPixmap('resources/icon_no_cover_150.png')),'(No Cover)'))
        for cover in self.covers:
            pm = QPixmap()
            pm.loadFromData(cover)
            artworkList.addItem(QListWidgetItem(QIcon(pm),''))

    def appendCover(self, artworkList, cover):
        pm = QPixmap()
        pm.loadFromData(cover)
        artworkList.addItem(QListWidgetItem(QIcon(pm),''))

    def showInformation(self, infoBox, albumTrackList):
        infoBox.setVisible(True)
        infoBox.findChild(QLabel,"Lbl_Artist").setText("Artist: {0}".format(self.getArtist()))
        infoBox.findChild(QLabel,"Lbl_Album").setText("Album: {0}".format(self.getAlbum()))
        trackListBox = infoBox.findChild(QTreeWidget,"T_TrackList")
        trackListBox.clear()
        albumTrackList2 = albumTrackList[2:]

        i = 0
        for track in albumTrackList2:
            item_0 = QTreeWidgetItem(trackListBox)
            trackListBox.topLevelItem(i).setText(0, str(track[0])) # Track Number
            trackListBox.topLevelItem(i).setText(1, track[1]) # Track Name
            i += 1

    def setCovers(self, covers):
        self.coversDownloaded = True
        self.covers = covers
