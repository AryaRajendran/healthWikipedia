import bz2
#import xml.etree.ElementTree as ET 
from lxml import etree
import re
import csv

prefix="en."

# categoryToCategory.csv contains all links among two categories
categoryLinksFile = prefix + "categoryToCategory.csv"
catCSV = open(categoryLinksFile, 'wb')
catWriter = csv.writer(catCSV, delimiter=',', quoting=csv.QUOTE_ALL, quotechar ='"', escapechar='\\', doublequote=False)

# pageToCategory.csv describes all the categories that a page belongs
pageFile = prefix + "pageToCategory.csv"
pageCSV = open(pageFile, 'wb')
pageWriter = csv.writer(pageCSV, delimiter=',', quoting=csv.QUOTE_ALL, quotechar ='"', escapechar='\\', doublequote=False)

#filename="simplewiki-20130501-pages-articles-multistream.xml.bz2"
#filename="small-simplewiki-20130501-pages-articles.xml.bz2"
filename="enwiki-20130503-pages-articles-multistream.xml.bz2"

#print "Started..."
#print "Reading file...%s" % (filename)
wikifile = bz2.BZ2File(filename)

#print "Parsing tree..."
tree = ET.parse(wikifile)
root = etree.iterparse( MYFILE, tag='page')

#print "Printing root..."
#root = tree.getroot()
#print "Tag - ", root.tag,  "att ", root.attrib

def fast_iter(context, func):
    # http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
    # Author: Liza Daly
    for event, elem in context:
        func(elem)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context

def process_element(elem):
    title = elem.xpath('title/text()')
    text = elem.xpath('revision/text/text()')

    #print "Title = ", title
    if title is not None:
        #print title.text
        wikiText = text.text
        listOfRelatedCats = re.findall("\[\[Category:(.*)\]\]", unicode(wikiText))
        for outCat in listOfRelatedCats:
            #print "Category - " , cat		
            #print title.text, "\t", cat
            inLink = title.text.encode('utf-8').strip()
            inLink = inLink.replace("\t","")
            inLink = inLink.replace("\t","")
            inLink = inLink.replace("<200e>","")
            inLink = inLink.replace("\xe2\x80\x8e","")

            outLink = outCat.encode('utf-8').split("|")[0].strip()
            outLink = outLink.replace("]","")
            outLink = outLink.replace("[","")
            outLink = outLink.replace("\xe2\x80\x8e","")

            outLink = outLink.replace("<200e>","")

            if "Category:" in inLink:
                catWriter.writerow([inLink, "Category:"+outLink])
            else:
                pageWriter.writerow([inLink, "Category:"+outLink])


fast_iter(root,process_element)

#print "Closing..."
wikifile.close()
catCSV.close()
pageCSV.close()

