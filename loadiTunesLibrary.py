from PyQt4 import QtCore
import win32com.client

class LoadiTunesLibrary(QtCore.QThread):
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

