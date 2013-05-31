
from os import listdir
from os.path import isfile, join
import sys
from scoop import futures

from convertHTMLText import convertFromHTMLToText 
from convertWikiHTML import convertFromWikiToHTML


def convertAll(argv):

    wpath, hpath, tpath = "", "", ""

    for i, arg in zip(range(len(argv)), sys.argv):
        if arg == "-w":
            wpath = argv[i+1]
        if arg == "-t":
            tpath = argv[i+1]
        if arg == "-h":
            hpath = argv[i+1]

    wikiPath = wpath
    htmlPath = hpath
    textPath = tpath
    if wikiPath == "" or htmlPath == "" or textPath == "":
        print "Check if you set the path correctly. Use -w -t and -h"
        sys.exit(0)

    print "Wiki = ", wikiPath, " html = ", htmlPath , " text = ", textPath

    files = [ f for f in listdir(wikiPath) if isfile(join(wikiPath,f)) ]
    wikiFiles = [ wikiPath + "/" + f for f in files]
    htmlFiles = [ htmlPath + "/" + f for f in files]
    textFiles = [ textPath + "/" + f for f in files]


    print "Converting ", len(files), "files."

    filesConvertedToHTML = futures.map(convertFromWikiToHTML, wikiFiles)

    for file, content in zip(htmlFiles, filesConvertedToHTML):
        with open(file, "w") as f:
            f.write(content)

    filesConvertedToText = futures.map(convertFromHTMLToText, htmlFiles)


    for file, content in zip(htmlFiles, filesConvertedToHTML):
        with open(file, "w") as f:
            f.write(content)


if __name__ ==  "__main__":
    convertAll(sys.argv)

