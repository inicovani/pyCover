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
import os

class MainWindow(QMainWindow):
    def __init__(self, *args):
        apply(QMainWindow.__init__, (self, ) + args)
        self.mainWidget = QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.mainLayout = QGridLayout(self.mainWidget)
        self.setWindowTitle("pyCover")

        icon = QIcon()
        icon.addPixmap(QPixmap("resources/pyCover_ico32.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        self.loadLibraryThread = LoadiTunesLibrary(self)

        self.PD_Progress = QProgressDialog("Loading iTunes Library","Cancel",0,0,self.mainWidget)
        self.PD_Progress.setValue(0)
        self.PD_Progress.setWindowTitle("Loading...")
        self.PD_Progress.setWindowModality(Qt.ApplicationModal)

        self.GB_AlbumList = QGroupBox("Albums with missing covers", self.mainWidget)
        self.GB_AlbumList.setMinimumWidth(450)
        self.GB_AlbumList.setMinimumHeight(300)
        gl = QVBoxLayout(self.GB_AlbumList)
        
        self.List_Albums = QListWidget(self.GB_AlbumList)
        self.List_Albums.setIconSize(QSize(100,100))
        self.List_Albums.setSpacing(2)
        self.List_Albums.setSortingEnabled(True)

        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        palette.setBrush(QPalette.Active, QPalette.Light, brush)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush)

        brush = QBrush(QColor(234, 229, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush)
        brush = QBrush(QColor(128, 128, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush)
        brush = QBrush(QColor(141, 139, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush)
        brush = QBrush(QColor(108, 104, 152))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)

        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush)

        brush = QBrush(QColor(234, 229, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush)
        brush = QBrush(QColor(128, 128, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush)
        brush = QBrush(QColor(141, 139, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush)
        brush = QBrush(QColor(108, 104, 152))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        brush = QBrush(QColor(128, 128, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        brush = QBrush(QColor(234, 229, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush)
        brush = QBrush(QColor(128, 128, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush)
        brush = QBrush(QColor(141, 139, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush)
        brush = QBrush(QColor(128, 128, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        brush = QBrush(QColor(128, 128, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        brush = QBrush(QColor(108, 104, 152))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        brush = QBrush(QColor(108, 104, 152))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)

        font = QFont()
        font.setWeight(75)
        font.setBold(True)
#        self.List_Albums.setPalette(palette)
#        self.List_Albums.setFont(font)


        gl.addWidget(self.List_Albums)
        self.GB_AlbumList.setLayout(gl)

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
        self.List_Artwork.setVisible(False)

        self.List_Artwork.setPalette(palette)
        self.List_Artwork.setFont(font)

        
        self.mainLayout.addWidget( self.GB_AlbumList,0,0 )
        self.mainLayout.addWidget( self.GB_Options,0,1 )
        self.mainLayout.addWidget( self.List_Artwork,1,0,1,2 )

        QtCore.QObject.connect(self.loadLibraryThread, QtCore.SIGNAL("setMaxTracks(PyQt_PyObject)"), self.PD_Progress.setMaximum)
        QtCore.QObject.connect(self.loadLibraryThread, QtCore.SIGNAL("tick(PyQt_PyObject)"), self.updateProgressDialog)
        QtCore.QObject.connect(self.loadLibraryThread, QtCore.SIGNAL("doneLibraryLoad(PyQt_PyObject)"), self.doneLibraryLoad)
        QtCore.QObject.connect(self.loadLibraryThread, QtCore.SIGNAL("newMissingArtworkAlbum(PyQt_PyObject,PyQt_PyObject)"), self.insertAlbum)
        QtCore.QObject.connect(Btn_DownloadCover, QtCore.SIGNAL("clicked()"), self.handleDownloadCoverClick)
        QtCore.QObject.connect(Btn_SaveCoverToAlbum, QtCore.SIGNAL("clicked()"), self.handleSaveCoverClick)
        QtCore.QObject.connect(self.List_Artwork, QtCore.SIGNAL("currentItemChanged(QListWidgetItem*,QListWidgetItem*)"), self.handleCoverSelection)

    def loadLibrary(self):
        """
        Shows the progress dialog, and starts the library loading thread.
        The data about missing albums with missing covers will be passed via
        signals from the loadLibraryThread.
        """
        self.PD_Progress.show()
        self.loadLibraryThread.start()

    def doneLibraryLoad(self, htAlbums):
        """
        This will receive the albums with missing covers (a dictionary)
        and save them for later use.
        It will also hide the initial loading dialog, and enable the option
        of selecting an album from the list.
        """
        self.htAlbums = htAlbums
        self.PD_Progress.reset()
        QtCore.QObject.connect(self.List_Albums, QtCore.SIGNAL("currentItemChanged(QListWidgetItem*,QListWidgetItem*)"), self.handleAlbumSelection)
        self.List_Albums.setCurrentRow(0)

    def progressDialogSetup(self, maximum, title, label):
        self.PD_Progress.reset()
        self.PD_Progress.setMaximum(maximum)
        self.PD_Progress.setWindowTitle(title)   
        self.PD_Progress.setLabelText(label)
        self.PD_Progress.setValue(0)

    def updateProgressDialog(self, step):
        self.PD_Progress.setValue(self.PD_Progress.value() + step)

    def insertAlbum(self,artist, album):
        newItem = pyCover_QListWidgetItem(artist, album)
        self.List_Albums.addItem(newItem)

    def handleAlbumSelection(self, itemSelected, previousItemSelected):
        self.List_Artwork.setVisible(True)
        itemSelected.showArtwork(self.List_Artwork)
        itemSelected.showInformation(self.GB_Options, self.htAlbums[itemSelected.album])

        # If covers are already downloaded, no need to download them again
        if itemSelected.coversDownloaded:
            self.GB_Options.findChild(QPushButton,"Btn_DownloadCover").setDisabled(True)
            self.GB_Options.findChild(QPushButton,"Btn_SaveCoverToAlbum").setDisabled(False)
            self.GB_Options.findChild(QPushButton,"Btn_SaveCoverToAlbum").setVisible(True)

        else:
            self.GB_Options.findChild(QPushButton,"Btn_DownloadCover").setDisabled(False)
            self.GB_Options.findChild(QPushButton,"Btn_SaveCoverToAlbum").setDisabled(True)
            self.GB_Options.findChild(QPushButton,"Btn_SaveCoverToAlbum").setVisible(False)

    def handleCoverSelection(self, itemSelected, previousItemSelected):
        if self.List_Artwork.currentRow() > 0:
            self.GB_Options.findChild(QPushButton,"Btn_SaveCoverToAlbum").setDisabled(False)
        else:
            self.GB_Options.findChild(QPushButton,"Btn_SaveCoverToAlbum").setDisabled(True)

    def handleDownloadCoverClick(self):
        selectedItem = self.List_Albums.selectedItems()[0]
        self.cd = CoverDownload(selectedItem.getArtist(), selectedItem.getAlbum())
        QtCore.QObject.connect(self.cd, QtCore.SIGNAL("doneCoverDownload()"), self.handleDoneCoverDownload)
        QtCore.QObject.connect(self.cd, QtCore.SIGNAL("coverDownloaded(PyQt_PyObject)"), self.handleCoverDownloaded)
        self.progressDialogSetup(100,"Please wait...","Downloading covers...")
        self.PD_Progress.show()
        self.cd.getCovers()

    def handleDoneCoverDownload(self):
        self.GB_Options.findChild(QPushButton,"Btn_DownloadCover").setDisabled(True)
        self.GB_Options.findChild(QPushButton,"Btn_SaveCoverToAlbum").setVisible(True)
        self.PD_Progress.setValue(100)
        selectedItem = self.List_Albums.selectedItems()[0]
        selectedItem.setCovers(self.cd.covers)

    def handleCoverDownloaded(self,cover):
        self.PD_Progress.setValue(self.PD_Progress.value() + 20)
        selectedItem = self.List_Albums.selectedItems()[0]
        selectedItem.appendCover(self.List_Artwork,cover)

    def handleSaveCoverClick(self):
        # TODO: This should happen in a different thread
        currentAlbum = self.List_Albums.currentItem()
        coverToSave = currentAlbum.covers[self.List_Artwork.currentRow()-1]
        pixmap = QPixmap()
        pixmap.loadFromData(coverToSave)

        tempFileName = "pyCover_tempcover.jpg"
        fp = open(tempFileName,"wb")
        fp.write(coverToSave)
        fp.flush()
        os.fsync(fp.fileno())
        fp.close()
        
        trackList = self.htAlbums[currentAlbum.album][2:]
        iTunes = win32com.client.gencache.EnsureDispatch("iTunes.Application")

        for track in trackList:
            trackRef = iTunes.LibraryPlaylist.Tracks.ItemByPersistentID(track[2],track[3])
            trackRef.AddArtworkFromFile(tempFileName)

        os.remove(tempFileName)
        currentAlbum.setIcon(QIcon(pixmap))

        infoDialog = QMessageBox(QMessageBox.Information,"Information:",\
            "Cover successfully saved to tracks.",QMessageBox.Ok,\
            self.mainWidget)
        infoDialog.show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.loadLibrary()
    mainWindow.show()
    sys.exit(app.exec_())

