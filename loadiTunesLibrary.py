from PyQt4 import QtCore
import win32com.client
import pythoncom

class LoadiTunesLibrary(QtCore.QThread):
    def __init__(self, parent):
        QtCore.QThread.__init__(self, parent)
        self.htArtists = {}
        self.htAlbums = {}

    def run(self):
        pythoncom.CoInitialize()
        #self.iTunes = win32com.client.gencache.EnsureDispatch("iTunes.Application")
        #self.iTunes = win32com.client.Dispatch("iTunes.Application")
        #self.emit(QtCore.SIGNAL("saveiTunesRef"),self.iTunes)
        self.iTunes = win32com.client.gencache.EnsureDispatch("iTunes.Application")
        tracks = self.iTunes.LibraryPlaylist.Tracks

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

            trackData = [song.TrackNumber, song.Name, \
                self.iTunes.ITObjectPersistentIDHigh(song), \
                self.iTunes.ITObjectPersistentIDLow(song)]

            #idedTrack = tracks.ItemByPersistentID(trackData[2],trackData[3])
            self.htAlbums[song.Album].append(trackData)
            self.emit(QtCore.SIGNAL("tick"))
        
        self.emit(QtCore.SIGNAL("doneLibraryLoad"),self.htAlbums)
