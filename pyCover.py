# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
#from PyQt4.QtCore import *
from PyQt4 import QtCore
from PyQt4.Qt import *
from loadiTunesLibrary import LoadiTunesLibrary
from pyCover_QListWidgetItem import pyCover_QListWidgetItem

class MainWindow(QMainWindow):
    def __init__(self, *args):
        apply(QMainWindow.__init__, (self, ) + args)
        self.mainWidget = QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.mainLayout = QGridLayout(self.mainWidget)
        self.setWindowTitle("pyCover")

        self.loadLibraryThread = LoadiTunesLibrary()

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

        QtCore.QObject.connect(self.loadLibraryThread, QtCore.SIGNAL("setMaxTracks"), self.progressDialogSetup)
        QtCore.QObject.connect(self.loadLibraryThread, QtCore.SIGNAL("tick"), self.updateProgressDialog)
        QtCore.QObject.connect(self.loadLibraryThread, QtCore.SIGNAL("newMissingArtworkAlbum"), self.insertAlbum)

    def loadLibrary(self):
        self.PD_Progress.show()
        self.loadLibraryThread.start()

    def progressDialogSetup(self, maximum):
        self.PD_Progress.setMaximum(maximum)
        self.PD_Progress.setValue(0)

    def updateProgressDialog(self):
        self.PD_Progress.setValue(self.PD_Progress.value() + 1)

    def insertAlbum(self,artist, album):
        newItem = pyCover_QListWidgetItem(artist, album)
        self.List_Albums.addItem(newItem)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.loadLibrary()
    mainWindow.show()
    sys.exit(app.exec_())

