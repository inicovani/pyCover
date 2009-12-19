# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
#from PyQt4.QtCore import *
from PyQt4 import QtCore
from PyQt4.Qt import *
from loadiTunesLibrary import LoadiTunesLibrary
from pyCover_QListWidgetItem import pyCover_QListWidgetItem
from coverDownload import CoverDownload
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
        T_TrackList.header().setDefaultSectionSize(35)
        Btn_DownloadCover = QPushButton("&Download cover",self.GB_Options)
        Btn_DownloadCover.setObjectName("Btn_DownloadCover")
        Btn_SaveCoverToAlbum = QPushButton("&Save selected cover",self.GB_Options)
        Btn_SaveCoverToAlbum.setObjectName("Btn_SaveCoverToAlbum")
        Btn_SaveCoverToAlbum.setVisible(False)

        gl.addWidget(Lbl_Artist)
        gl.addWidget(Lbl_Album)
        gl.addWidget(T_TrackList)
        gl.addWidget(Btn_DownloadCover)
        gl.addWidget(Btn_SaveCoverToAlbum)
        self.GB_Options.setLayout(gl)
        self.GB_Options.setVisible(False)

        self.List_Artwork = QListWidget(self.mainWidget)
        self.List_Artwork.setMinimumHeight(200)
        self.List_Artwork.setMaximumHeight(200)
        self.List_Artwork.setSpacing(5)
        self.List_Artwork.setFlow(QListView.LeftToRight)
        self.List_Artwork.setViewMode(QListView.IconMode)
        self.List_Artwork.setIconSize(QSize(150,150))
        self.List_Artwork.setMovement(QListView.Static)
        self.List_Artwork.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.List_Artwork.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.List_Artwork.setProperty("isWrapping", False)
        # Posible feature, drop an image file as a cover for the album
        self.List_Artwork.setDragDropMode(QAbstractItemView.NoDragDrop)

        
        self.mainLayout.addWidget( self.List_Albums,0,0 )
        self.mainLayout.addWidget( self.GB_Options,0,1 )
        self.mainLayout.addWidget( self.List_Artwork,1,0,1,2 )

        QtCore.QObject.connect(self.loadLibraryThread, QtCore.SIGNAL("setMaxTracks"), self.progressDialogSetup)
        QtCore.QObject.connect(self.loadLibraryThread, QtCore.SIGNAL("tick"), self.updateProgressDialog)
        QtCore.QObject.connect(self.loadLibraryThread, QtCore.SIGNAL("doneLibraryLoad"), self.doneLibraryLoad)
        QtCore.QObject.connect(self.loadLibraryThread, QtCore.SIGNAL("newMissingArtworkAlbum"), self.insertAlbum)
        QtCore.QObject.connect(Btn_DownloadCover, QtCore.SIGNAL("clicked()"), self.handleDownloadCoverClick)

    def loadLibrary(self):
        self.PD_Progress.show()
        self.loadLibraryThread.start()

    def doneLibraryLoad(self, htAlbums):
        self.htAlbums = htAlbums
        QtCore.QObject.connect(self.List_Albums, QtCore.SIGNAL("currentItemChanged(QListWidgetItem*,QListWidgetItem*)"), self.handleAlbumSelection)
        self.List_Albums.setCurrentRow(0)

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
        itemSelected.showInformation(self.GB_Options, self.htAlbums[itemSelected.album])

    def handleDownloadCoverClick(self):
        selectedItem = self.List_Albums.selectedItems()[0]
        self.cd = CoverDownload(selectedItem.getArtist(), selectedItem.getAlbum())
        QtCore.QObject.connect(self.cd, QtCore.SIGNAL("doneCoverDownload()"), self.handleDoneCoverDownload)
        QtCore.QObject.connect(self.cd, QtCore.SIGNAL("coverDownloaded(PyQt_PyObject)"), self.handleCoverDownloaded)
        self.cd.getCovers()

    def handleDoneCoverDownload(self):
        selectedItem = self.List_Albums.selectedItems()[0]
        selectedItem.setCovers(self.cd.covers)

    def handleCoverDownloaded(self,cover):
        selectedItem = self.List_Albums.selectedItems()[0]
        selectedItem.appendCover(self.List_Artwork,cover)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.loadLibrary()
    mainWindow.show()
    sys.exit(app.exec_())

