import win32com.client
import sys
#from coverDownload import CoverDownload
        
def main():
    print 'Connecting to iTunes'
    iTunes = win32com.client.gencache.EnsureDispatch("iTunes.Application")
    lib = iTunes.LibraryPlaylist
    tracks = lib.Tracks
    htArtists = {}
    htAlbums = {}

    print 'Reading iTunes library'
    for song in tracks:
        if song.Artist not in htArtists:        
            htArtists[song.Artist] = [song.Album]
        elif song.Album not in htArtists[song.Artist]:
            htArtists[song.Artist].append(song.Album)

        if song.Album not in htAlbums:
            htAlbums[song.Album] = [False]
            if song.Artwork.Count >= 1:
                htAlbums[song.Album].append(song.Artwork[0])
            else:
                htAlbums[song.Album].append(None)

        htAlbums[song.Album].append(song)

    print 'Albums with missing artwork from your iTunes library:'
    for (artist, discs) in htArtists.items():
        i = 1
        for disc in discs:
            if htAlbums[disc][1] == None:
                print "[{0} - {1}]".format(artist, disc.encode("utf-8"))
                #cd = CoverDownload(artist, disc)
                #cd.getCovers()
            i += 1
            

if __name__ == "__main__":
    main()