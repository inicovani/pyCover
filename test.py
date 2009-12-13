import coverDownload

cd = coverDownload.CoverDownload('Skunk Anansie', 'Stoosh')
covers = cd.getCovers()
i = 0
for cover in covers:
    fp = open("Skunk Anansie - Stoosh - %d.jpg" % i, "wb")
    fp.write(cover)
    fp.close()
    i += 1
