import urllib2
from BeautifulSoup import BeautifulSoup
import re
from PyQt4 import QtCore
from subCoverDownload import SubCoverDownload

class CoverDownload(QtCore.QThread):
    def __init__(self,artist,album):
        QtCore.QThread.__init__(self)
        self.artist = artist.encode("utf-8")
        self.album = album.encode("utf-8")
        search = self.artist.replace(' ', '+') + '+' + self.album.replace(' ','+')
        self.searchPage = "http://www.amazon.com/s/ref=nb_ss_m?url=search-alias%3Dpopular&field-keywords=" + search + "&x=0&y=0"
        self.covers = []

    def getCovers(self,top = 4):
        """
        This method attempts to download at least 4 covers from the amazon site
        It uses BeautifulSoup and regular expressions to parse out the links to
        the images.
        Since it's threaded, it will append the artwork to self.covers on
        each successfull download.
        """
        self.top = top
        self.start()

    def run(self):
        src = urllib2.urlopen(self.searchPage).read()
        soup = BeautifulSoup(src)
        rePage = re.compile('<a href="(.+?)">')
        found = False
        i = 0
        threads = []
 
        # It appears that amazon has 2 different pages for a search query,
        # this handles the first kind...
        for res in soup.findAll('div', {'class' : 'productImage'}):
            scd = SubCoverDownload(rePage.findall(str(res))[0])
            threads.append(scd)
            scd.setParent(self)
            QtCore.QObject.connect(scd, QtCore.SIGNAL("coverDownloaded(PyQt_PyObject)"), self.handleCoverDownloaded)
            scd.start()
            found = True
            i += 1
            if i >= self.top: break
 
        # ... and this handles the second kind of page.
        if not found:
            for res in soup.findAll('td', {'class' : 'imageColumn'}):
                scd = SubCoverDownload(rePage.findall(str(res))[0])
                threads.append(scd)
                QtCore.QObject.connect(scd, QtCore.SIGNAL("coverDownloaded(PyQt_PyObject)"), self.handleCoverDownloaded)
                scd.start()
                i += 1
                if i >= self.top: break

        while True:
            running = False
            for thread in threads:
                if thread.isRunning():
                    running = True
            if not running: break
            else: QtCore.QThread.sleep(1)
            
        self.emit(QtCore.SIGNAL("doneCoverDownload()"))
    
    def saveCoversToFile(self):
        i = 0
        for cover in self.covers:
            fp = open("{0} - {1} - {2}.jpg".format(self.artist,self.album,i), "wb")
            fp.write(cover)
            fp.close()
            i += 1

    def handleCoverDownloaded(self,cover):
        self.emit(QtCore.SIGNAL("coverDownloaded(PyQt_PyObject)"),cover)
        self.covers.append(cover)
