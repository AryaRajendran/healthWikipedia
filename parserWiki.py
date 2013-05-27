import bz2
import xml.etree.ElementTree as ET 
import re
import csv

# categoryToCategory.csv contains all links among two categories
categoryLinksFile = "categoryToCategory.csv"
catCSV = open(categoryLinksFile, 'wb')
catWriter = csv.writer(catCSV, delimiter=',', quoting=csv.QUOTE_ALL, quotechar ='"', escapechar='\\', doublequote=False)

# pageToCategory.csv describes all the categories that a page belongs
pageFile = "pageToCategory.csv"
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

#print "Printing root..."
root = tree.getroot()
#print "Tag - ", root.tag,  "att ", root.attrib


#for page in root.findall('{http://www.mediawiki.org/xml/export-0.8/}title'):
#	print "tag - ", page.tag, " att ", page.attrib

for child in root:
    #print "tag - ", child.tag, " att ", child.attrib
    title = child.find('title')
    text = child.find('revision/text')

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

#print "Closing..."
wikifile.close()
catCSV.close()
pageCSV.close()

