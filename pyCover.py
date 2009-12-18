# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
#from PyQt4.QtCore import *
from PyQt4 import QtCore
from PyQt4.Qt import *
from loadiTunesLibrary import LoadiTunesLibrary
from pyCover_QListWidgetItem import pyCover_QListWidgetItem
import win32com.client
import pythoncom

class MainWindow(QMainWindow):
    def __init__(self, *args):
        apply(QMainWindow.__init__, (self, ) + args)
        self.mainWidget = QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.mainLayout = QGridLayout(self.mainWidget)
        self.setWindowTitle("pyCover")

        self.loadLibraryThread = LoadiTunesLibrary(self)

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

        gl = QVBoxLayout(self.GB_Options)
        Lbl_Artist = QLabel("Artist: ",self.GB_Options)
        Lbl_Artist.setObjectName("Lbl_Artist")
        Lbl_Album = QLabel("Album: ",self.GB_Options)
        Lbl_Album.setObjectName("Lbl_Album")
        T_TrackList = QTreeWidget(self.GB_Options)
        T_TrackList.setObjectName("T_TrackList")
        T_TrackList.setRootIsDecorated(False)
        T_TrackList.headerItem().setText(0, "N.")
        T_TrackList.headerItem().setText(1, "Track Name")
        Btn_DownloadCover = QPushButton("Download cover",self.GB_Options)
        Btn_SaveCoverToAlbum = QPushButton("Save selected cover",self.GB_Options)

        gl.addWidget(Lbl_Artist)
        gl.addWidget(Lbl_Album)
        gl.addWidget(T_TrackList)
        gl.addWidget(Btn_DownloadCover)
        gl.addWidget(Btn_SaveCoverToAlbum)
        self.GB_Options.setLayout(gl)
        self.GB_Options.setVisible(False)

        self.List_Artwork = QListWidget(self.mainWidget)
        self.List_Artwork.setMinimumHeight(180)
        self.List_Artwork.setMaximumHeight(180)
        self.List_Artwork.setSpacing(5)
        self.List_Artwork.setFlow(QListView.LeftToRight)
        self.List_Artwork.setViewMode(QListView.IconMode)
        self.List_Artwork.setIconSize(QSize(150,150))
        self.List_Artwork.setMovement(QListView.Static)
        # Posible feature, drop an image file as a cover for the album
        self.List_Artwork.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)

        self.List_Artwork.setCurrentRow(0)
        self.mainLayout.addWidget( self.List_Albums,0,0 )
        self.mainLayout.addWidget( self.GB_Options,0,1 )
        self.mainLayout.addWidget( self.List_Artwork,1,0,1,2 )

        QtCore.QObject.connect(self.loadLibraryThread, QtCore.SIGNAL("setMaxTracks"), self.progressDialogSetup)
        QtCore.QObject.connect(self.loadLibraryThread, QtCore.SIGNAL("tick"), self.updateProgressDialog)
        QtCore.QObject.connect(self.loadLibraryThread, QtCore.SIGNAL("doneLibraryLoad"), self.doneLibraryLoad)
        QtCore.QObject.connect(self.loadLibraryThread, QtCore.SIGNAL("newMissingArtworkAlbum"), self.insertAlbum)
        QtCore.QObject.connect(self.List_Albums, QtCore.SIGNAL("currentItemChanged(QListWidgetItem*,QListWidgetItem*)"), self.handleAlbumSelection)

    def loadLibrary(self):
        self.PD_Progress.show()
        self.loadLibraryThread.start()

    def doneLibraryLoad(self, htAlbums):
        self.htAlbums = htAlbums

    def progressDialogSetup(self, maximum):
        self.PD_Progress.setMaximum(maximum)
        self.PD_Progress.setValue(0)

    def updateProgressDialog(self):
        self.PD_Progress.setValue(self.PD_Progress.value() + 1)

    def insertAlbum(self,artist, album):
        newItem = pyCover_QListWidgetItem(artist, album)
        self.List_Albums.addItem(newItem)

    def handleAlbumSelection(self, itemSelected, previousItemSelected):
        itemSelected.showArtwork(self.List_Artwork)
        itemSelected.showInformation(self.GB_Options, self.htAlbums[itemSelected.getAlbum()])

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.loadLibrary()
    mainWindow.show()
    sys.exit(app.exec_())

