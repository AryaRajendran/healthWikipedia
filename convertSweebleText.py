from bs4 import BeautifulSoup
import sys, re

#exclusively built to run with the mediawiki-parser's output!

def convertFromHTMLToText(filename):

    #print "Converting from HTML to TEXT :  ", filename
    
    f = open(filename, "r")
    lines = f.read()
    
    # remove huge first comment
    lines = re.sub("<!--[\w\W]*?-->", "", lines, re.MULTILINE|  re.IGNORECASE | re.UNICODE)
    #remove gallery
    lines = re.sub("&lt;gallery>[\w\W]*&lt;/gallery>", "", lines, re.MULTILINE|  re.IGNORECASE | re.UNICODE)

    soup = BeautifulSoup(lines)
    removeTables(soup)
    removeHRefs(soup)
    removeTitles(soup)
    removeReferences(soup)
    removeLists(soup)
    removeImages(soup)
    removePreTag(soup)
    removeUnknown(soup)

    text = soup.get_text()
    text = re.sub("<ref.*?/>", "", text, re.MULTILINE|  re.IGNORECASE | re.UNICODE)
    text = re.sub("<ref name =.*?>", "", text, re.MULTILINE|  re.IGNORECASE | re.UNICODE)
    #remove table tag that bs could not remove
    text = re.sub("<table[\w\W]*</table>", "", text, re.MULTILINE | re.DOTALL | re.IGNORECASE | re.UNICODE)

    #Remove useless spaces:
    text = re.sub("\n", " ", text)
    text = re.sub("\s+", " ", text)

    print text.encode("utf-8")
    return text.encode("utf-8")


def removeHRefs(soup):
    #Remove href templates and categories
    for link in soup.find_all('a'):
        hrefValue = link.get("href")

        if hrefValue.startswith("Template"):
            #print "SHOULD DELETE", link
            link.extract()
        if hrefValue.startswith("Category"):
            #print "SHOULD DELETE", link
            link.extract()

        if re.match( "^[\w][\w]:" , hrefValue ):
            #print "LINK TO OTHER WIKIPEDIA ---- SHOULD DELETE", link
            link.extract()

def removeUnknown(soup):
    for link in soup.find_all('span'):
        linkclass = link.get('class')
        for l in linkclass:
            if l == "unknown-node":
                #print "SHOULD DELETE", link
                link.extract()
        

def removeTitles(soup):
    #Remove titles
    for link in soup.find_all('title'):
        link.extract()
    
    for link in soup.find_all('h1'):
        #print "SHOULD DELETE", link
        link.extract()
    for link in soup.find_all('h2'):
        #print "SHOULD DELETE", link
        link.extract()
    for link in soup.find_all('h3'):
        #print "SHOULD DELETE", link
        link.extract()
    for link in soup.find_all('h4'):
        #print "SHOULD DELETE", link
        link.extract()
    for link in soup.find_all('h5'):
        #print "SHOULD DELETE", link
        link.extract()
    for link in soup.find_all('h6'):
        #print "SHOULD DELETE", link
        link.extract()

def removeReferences(soup):
    #delete refs
    for link in soup.find_all('ref'):
        #print "SHOULD DELETE", link
        link.extract()

def removeTables(soup):
    #delete tables
    for link in soup.find_all('table'):
        link.extract()
    for link in soup.find_all('td'):
        link.extract()
    for link in soup.find_all('tr'):
        link.extract()

def removeLists(soup):
    #TODO: Another option is to retain the lists and treat them as sentences. Check what is better to do and add code for it.
    #Unorded lists
    for link in soup.find_all('ul'):
        #print "UNORDED LIST DELETED ---- ", link
        link.extract()

    for link in soup.find_all('ol'):
        #print "ORDED LIST DELETED ---- ", link
        link.extract()

    #Description lists
    for link in soup.find_all('dl'):
        #print "DESCRIPTION LIST DELETED ---- ", link
        link.extract()
        #listText = str(link)

    #for link in soup.find_all('li'):
        #listText = str(link)
        #print "List Item ----- ", listText
        #i = -5 # <\li>
        #while re.match("[\W]", listText[i]):
        #    i -= 1
        #print "Last char ----- ", listText[i+1]    
        #link.extract()

def removeImages(soup):
    for link in soup.find_all('div'):
        for sublink in link.get('class'):
            if sublink.startswith("thumb"):
                #print "SHOULD DELETE", link
                link.extract()

    for link in soup.find_all('gallery'):
        link.extract()


def removePreTag(soup):
    for link in soup.find_all('pre'):
        link.extract()

if __name__ == "__main__":
    convertFromHTMLToText(sys.argv[1])

