import xml.etree.ElementTree as ET 
#from lxml import etree
import re, csv, sys, bz2

prefix= sys.argv[1] + "."

# categoryToCategory.csv contains all links among two categories
categoryLinksFile = prefix + "categoryToCategory.csv"
catCSV = open(categoryLinksFile, 'wb')
catWriter = csv.writer(catCSV, delimiter=',', quoting=csv.QUOTE_ALL, quotechar ='"', escapechar='\\', doublequote=False)

# pageToCategory.csv describes all the categories that a page belongs
pageFile = prefix + "pageToCategory.csv"
pageCSV = open(pageFile, 'wb')
pageWriter = csv.writer(pageCSV, delimiter=',', quoting=csv.QUOTE_ALL, quotechar ='"', escapechar='\\', doublequote=False)

if prefix == "en.":
  filename="enwiki-20130503-pages-articles-multistream.xml.bz2"
elif prefix == "simple.":
  filename="simplewiki-20130501-pages-articles-multistream.xml.bz2"
elif prefix == "small":
  filename="small-simplewiki-20130501-pages-articles.xml.bz2"

#print "Started..."
#print "Reading file...%s" % (filename)
wikifile = bz2.BZ2File(filename)

#print "Parsing tree..."
root = ET.iterparse(wikifile)
#root = etree.iterparse( MYFILE, tag='page')

#print "Printing root..."
#root = tree.getroot()
#print "Tag - ", root.tag,  "att ", root.attrib

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

        #elem.clear()
        #while elem.getprevious() is not None:
        #del elem.getparent()[0]
    del context

def process_element(title, text):
    #title = elem.xpath('title/text()')
    #text = elem.xpath('revision/text/text()')
 
    inLink = title.text.encode('utf-8').strip()
    inLink = inLink.replace("\t","")
    inLink = inLink.replace("\t","")
    inLink = inLink.replace("<200e>","")
    inLink = inLink.replace("\xe2\x80\x8e","")
    
    #print "Going to process ", inLink, text.text

    #print title.text
    wikiText = text.text
    listOfRelatedCats = re.findall("\[\[Category:(.*)\]\]", unicode(wikiText))
    outCats = []
    for outCat in listOfRelatedCats:
        #print "Category - " , cat		
        #print title.text, "\t", cat
        inLink = inLink.replace("\t","")
        inLink = inLink.replace("\t","")
        inLink = inLink.replace("<200e>","")
        inLink = inLink.replace("\xe2\x80\x8e","")

        outLink = outCat.encode('utf-8').split("|")[0].strip()
        outLink = outLink.replace("]","")
        outLink = outLink.replace("[","")
        outLink = outLink.replace("\xe2\x80\x8e","")

        outLink = outLink.replace("<200e>","")
        
        #store category
        outCats.append( "Category:"+outLink)
     
    if len(outCats) == 0:
        #Wikipedia article alone...
        return

    if "Category:" in inLink:
        catWriter.writerow([inLink] + outCats)
    else:
        pageWriter.writerow([inLink] + outCats)

    #print "Element processed:" + inLink

fast_iter(root, process_element)

#print "Closing..."
wikifile.close()
catCSV.close()
pageCSV.close()

