from PyQt4 import QtCore
import win32com.client
import pythoncom

class LoadiTunesLibrary(QtCore.QThread):
    def __init__(self, parent):
        QtCore.QThread.__init__(self, parent)
        self.htAlbums = {}

    def run(self):
        pythoncom.CoInitialize()
        iTunes = win32com.client.gencache.EnsureDispatch("iTunes.Application")
        tracks = iTunes.LibraryPlaylist.Tracks

        self.emit(QtCore.SIGNAL("setMaxTracks(PyQt_PyObject)"), tracks.Count)
        for song in tracks:
            if song.Album not in self.htAlbums:
                self.htAlbums[song.Album] = [False]
                if song.Artwork.Count >= 1:
                    self.htAlbums[song.Album].append(song.Artwork[0])
                else:
                    self.emit(QtCore.SIGNAL("newMissingArtworkAlbum(PyQt_PyObject,PyQt_PyObject)"), song.Artist, song.Album)
                    self.htAlbums[song.Album].append(None)

            trackData = [song.TrackNumber, song.Name, \
                iTunes.ITObjectPersistentIDHigh(song), \
                iTunes.ITObjectPersistentIDLow(song)]

            self.htAlbums[song.Album].append(trackData)
            self.emit(QtCore.SIGNAL("tick(PyQt_PyObject)"), 1)
        
        self.emit(QtCore.SIGNAL("doneLibraryLoad(PyQt_PyObject)"),self.htAlbums)
