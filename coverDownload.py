import urllib2
from BeautifulSoup import BeautifulSoup
import re

class CoverDownload():
    def __init__(self,artist,album):
        self.artist = artist.encode("utf-8")
        self.album = album.encode("utf-8")
        search = self.artist.replace(' ', '+') + '+' + self.album.replace(' ','+')
        self.searchPage = "http://www.amazon.com/s/ref=nb_ss_m?url=search-alias%3Dpopular&field-keywords=" + search + "&x=0&y=0"

    def getCovers(self,top = 4):
        """
        This method attempts to download at least 4 covers from the amazon site
        It uses BeautifulSoup and regular expressions to parse out the links to
        the images.
        returns an array containing the covers for the album required.
        """
        covers = []
        src = urllib2.urlopen(self.searchPage).read()
        soup = BeautifulSoup(src)
        rePage = re.compile('<a href="(.+?)">')
        reImg = re.compile('registerImage\("original_image", "(.+?)"')
        found = False
        i = 0
 
        # It appears that amazon has 2 different pages for a search query,
        # this handles the first kind...
        for res in soup.findAll('div', {'class' : 'productImage'}):
            discSrc =  urllib2.urlopen(rePage.findall(str(res))[0]).read()
            cover = urllib2.urlopen(reImg.findall(discSrc)[0]).read()
            covers.append(cover)
            found = True
            i += 1
            if i >= top: break
 
        # ... and this handles the second kind of page.
        if not found:
            for res in soup.findAll('td', {'class' : 'imageColumn'}):
                discoSrc =  urllib2.urlopen(rePage.findall(str(res))[0]).read()
                cover = urllib2.urlopen(reImg.findall(discoSrc)[0]).read()
                covers.append(cover)
                i += 1
                if i >= top: break

        self.covers = covers
        return covers