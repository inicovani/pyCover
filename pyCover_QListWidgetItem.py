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
        self.coverDownloaded = False

    def getArtist(self):
        return self.artist

    def getAlbum(self):
        return self.album

    def showArtwork(self, artworkList):
        artworkList.clear()
        artworkList.addItem(QListWidgetItem(QIcon(QPixmap('resources/icon_no_cover_150.png')),'(No Cover)'))

    def showInformation(self, infoBox, albumTrackList):
        infoBox.setVisible(True)
        infoBox.findChild(QLabel,"Lbl_Artist").setText("Artist: {0}".format(self.artist))
        infoBox.findChild(QLabel,"Lbl_Album").setText("Album: {0}".format(self.album))
        trackListBox = infoBox.findChild(QTreeWidget,"T_TrackList")
        trackListBox.clear()
        albumTrackList2 = albumTrackList[2:]

        i = 0
        for track in albumTrackList2:
            item_0 = QTreeWidgetItem(trackListBox)
            trackListBox.topLevelItem(i).setText(0, str(track[0])) # Track Number
            trackListBox.topLevelItem(i).setText(1, track[1]) # Track Name
            i += 1


