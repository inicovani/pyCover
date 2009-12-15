# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
#from PyQt4.QtCore import *
from PyQt4 import QtCore
from PyQt4.Qt import *
import win32com.client

class LoadLibrary(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.htArtists = {}
        self.htAlbums = {}

    def run(self):
        import pythoncom
        pythoncom.CoInitialize()
        iTunes = win32com.client.gencache.EnsureDispatch("iTunes.Application")
        tracks = iTunes.LibraryPlaylist.Tracks

        self.emit(QtCore.SIGNAL("setMaxTracks"), tracks.Count)
        for song in tracks:
            if song.Artist not in self.htArtists:        
                self.htArtists[song.Artist] = [song.Album]
            elif song.Album not in self.htArtists[song.Artist]:
                self.htArtists[song.Artist].append(song.Album)

            if song.Album not in self.htAlbums:
                self.htAlbums[song.Album] = [False]
                if song.Artwork.Count >= 1:
                    self.htAlbums[song.Album].append(song.Artwork[0])
                else:
                    self.emit(QtCore.SIGNAL("newMissingArtworkAlbum"), song.Artist, song.Album)
                    self.htAlbums[song.Album].append(None)

            self.htAlbums[song.Album].append(song)
            self.emit(QtCore.SIGNAL("tick"))


class MainWindow(QMainWindow):
    def __init__(self, *args):
        apply(QMainWindow.__init__, (self, ) + args)
        self.mainWidget = QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.mainLayout = QGridLayout(self.mainWidget)
        self.setWindowTitle("pyCover")

        self.loadLibrary = LoadLibrary()

        self.PD_Progress = QProgressDialog("Loading iTunes Library","Cancel",0,0,self.mainWidget)
        self.PD_Progress.setWindowTitle("Loading...")
        self.PD_Progress.setWindowModality(Qt.ApplicationModal)

        self.List_Albums = QListWidget(self.mainWidget)
        self.List_Albums.setMinimumHeight(300)
        self.List_Albums.setMinimumWidth(400)
        self.List_Albums.setIconSize(QSize(100,100))
        self.List_Albums.setSpacing(2)
        self.List_Albums.setSortingEnabled(True)

        self.GB_Options = QGroupBox("Information", self.mainWidget)
        self.GB_Options.setMinimumWidth(250)

        self.List_Artwork = QListWidget(self.mainWidget)
        self.List_Artwork.setMinimumHeight(180)
        self.List_Artwork.setMaximumHeight(180)
        self.List_Artwork.setSpacing(5)
        self.List_Artwork.setFlow(QListView.LeftToRight)
        self.List_Artwork.setViewMode(QListView.IconMode)
        self.List_Artwork.setIconSize(QSize(150,150))

        #test1 = QListWidgetItem(QIcon(QPixmap('resources/icon_no_cover_150.png')),'(No Cover)')
        #List_Artwork.addItem(test1)
        self.List_Artwork.setCurrentRow(0)
        self.mainLayout.addWidget( self.List_Albums,0,0 )
        self.mainLayout.addWidget( self.GB_Options,0,1 )
        self.mainLayout.addWidget( self.List_Artwork,1,0,1,2 )

        QtCore.QObject.connect(self.loadLibrary, QtCore.SIGNAL("setMaxTracks"), self.progressDialogSetup)
        QtCore.QObject.connect(self.loadLibrary, QtCore.SIGNAL("tick"), self.updateProgressDialog)
        QtCore.QObject.connect(self.loadLibrary, QtCore.SIGNAL("newMissingArtworkAlbum"), self.insertAlbum)

    def loadLibrary(self):
        self.PD_Progress.show()
        self.loadLibrary.start()

    def progressDialogSetup(self, maximum):
        self.PD_Progress.setMaximum(maximum)
        self.PD_Progress.setValue(0)

    def updateProgressDialog(self):
        self.PD_Progress.setValue(self.PD_Progress.value() + 1)

    def insertAlbum(self,artist, album):
        newItem = pyCover_QListWidgetItem(artist, album)
        self.List_Albums.addItem(newItem)


class pyCover_QListWidgetItem(QListWidgetItem):
    """
    We inherit from QListWidgetItem so we can add it to a List
    and still keep information about the artist and album.
    """
    def __init__(self, artist, album):
        QListWidgetItem.__init__(self,QIcon(QPixmap('resources/icon_unknown_cover_100.png')),"{0} - {1}".format(artist.encode("utf-8"), album.encode("utf-8")))
        self.artist = artist
        self.album = album

    def getArtist(self):
        return self.artist

    def getAlbum(self):
        return self.album

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.loadLibrary()
    mainWindow.show()
    sys.exit(app.exec_())

