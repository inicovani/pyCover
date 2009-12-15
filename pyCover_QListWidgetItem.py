from PyQt4.QtGui import *

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

    def getArtist(self):
        return self.artist

    def getAlbum(self):
        return self.album
