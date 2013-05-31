import bz2, re, csv, sys
import xml.etree.ElementTree as ET 

inFile = sys.argv[1]

prefix= inFile.split(".",1)[0]
outDir = prefix + "wiki"
print "Using prefix = ", prefix


targetTitles = []

with open(inFile, "r") as f:
    for l in f.readlines():
        targetTitles.append( l.strip() )

if prefix == "simple":
    filename="simplewiki-20130501-pages-articles-multistream.xml.bz2"
elif prefix == "small": 
    filename="small-simplewiki-20130501-pages-articles.xml.bz2"
elif prefix == "en":
    filename="enwiki-20130503-pages-articles-multistream.xml.bz2"
if prefix == "bla":
    filename="simplewiki-20130501-pages-articles-multistream.xml.bz2"

print "Started..."
print "Reading file...%s" % (filename)
wikifile = bz2.BZ2File(filename)

print "Parsing tree..."
root = ET.iterparse(wikifile)


def fast_iter(context, func):
    
    hasPage, hasTitle, hasText = False, False, False
    title = None
    text = None
    for event, elem in context:
        #print elem, " hasPage = ", hasPage

        if elem.tag == 'page':
            hasPage = True
            elem.clear()
            #print "Page"

        elif elem.tag == 'title' and hasPage == True:
            hasTitle = True
            title = elem
            #print "Title"

        elif elem.tag == 'text' and hasPage == True:
            hasText = True
            text = elem
            #print "Text"
        else:
            elem.clear()

        if hasPage and hasTitle and hasText:
            hasPage, hasTitle, hasText = False, False, False
            func(title, text)
            title.clear()
            text.clear()

    del context

def process_element(wikititle, text):
    #title = elem.xpath('title/text()')
    #text = elem.xpath('revision/text/text()')
    
    title = wikititle.text.encode('utf-8').strip()
    title = title.replace("\t","")
    title = title.replace("\t","")
    title = title.replace("<200e>","")
    title = title.replace("\xe2\x80\x8e","")

    if title in targetTitles:
        if title.startswith("Template:"):
            return
        
        if text.text is None:
            print "TEXT IS NONE: ", title
            import sys
            sys.exit(0)

        wikiText = text.text.encode('utf-8')

        title = title.replace(" ","_")
        title = title.replace("/","_")
        outFileName = outDir + "/" + title + "." + prefix
        with open(outFileName, "w") as f:
            f.write(wikiText)

        print "Processed: " + outFileName


fast_iter(root, process_element)

print "Closing..."
wikifile.close()

