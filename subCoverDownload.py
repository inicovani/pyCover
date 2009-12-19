from PyQt4 import QtCore
import urllib2
from BeautifulSoup import BeautifulSoup
import re

class SubCoverDownload(QtCore.QThread):
    def __init__(self,url):
        QtCore.QThread.__init__(self)
        self.url = url
        self.reImg = re.compile('registerImage\("original_image", "(.+?)"')

    def run(self):
        discSrc =  urllib2.urlopen(self.url).read()
        cover = urllib2.urlopen(self.reImg.findall(discSrc)[0]).read()
        self.emit(QtCore.SIGNAL("coverDownloaded(PyQt_PyObject)"),cover)
