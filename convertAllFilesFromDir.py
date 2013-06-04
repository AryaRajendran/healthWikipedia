
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
#    htmlFiles = [ htmlPath + "/" + f for f in files]
    htmlFiles = [ f for f in files]
#    textFiles = [ textPath + "/" + f for f in files]
    textFiles = [ f for f in files]

    print "Converting ", len(files), "files."

    error = []
    result = []
    for f in wikiFiles:
        try:
            result.append(convertFromWikiToHTML(f))
        except (RuntimeError, AttributeError):
            error.append(f.rsplit("/",1)[1])
            continue

    filesConvertedToHTML = result
    #filesConvertedToHTML = futures.map(convertFromWikiToHTML, wikiFiles)
    #filesConvertedToHTML = map(convertFromWikiToHTML, wikiFiles)


    for file, content in zip(htmlFiles, filesConvertedToHTML):
        with open(file, "w") as f:
            #print "Writing file:", f
            f.write(content)
    
    #remove errors:
    print "Error = ", error
    print "html files = ", htmlFiles
    htmlFiles = set(htmlFiles) - set(error)  
    textFiles = set(textFiles) - set(error)  
    print "html files = ", htmlFiles
    htmlFiles = [ htmlPath + "/" + f for f in htmlFiles]
    textFiles = [ textPath + "/" + f for f in files]
    
    #filesConvertedToText = map(convertFromHTMLToText, htmlFiles)
    filesConvertedToText = futures.map(convertFromHTMLToText, htmlFiles)

    for file, content in zip(textFiles, filesConvertedToText):
        with open(file, "w") as f:
            f.write(content)


if __name__ ==  "__main__":
    convertAll(sys.argv)

