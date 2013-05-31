#!/usr/bin/env python
# encoding: utf-8

import urllib, re
import logging, time, ast, sys

'''
'' Class myWikiApi:
''      Public Methods:
''          list getAllPagesBelongingToACategory(self, category)
''          map getPageContent(self, pageName, format=[html|wikitext]):
'''

class myWikiApi:

    def __init__(self, apiUrl="http://en.wikipedia.org/w/api.php?"):
        self.__apibase = apiUrl
        logging.info("The WikiAPI has as base %s", self.__apibase)

    def getAllPagesBelongingToACategory(self, category, filterUserPages=True, filterTemplates=True):
        pages = self.__getAllDataWithContinue(category, "page")
        
        if filterUserPages and filterTemplates:
            pages = [page for page in pages if not page.startswith("User:") and not page.startswith("Template:")]
        elif filterUserPages:
            pages = [page for page in pages if not page.startswith("User:")]
        elif filterTemplates:
            pages = [page for page in pages if not page.startswith("Template:")]

        #logging.info("Got all pages %d from category %s: %s", len(pages), category, pages)
        return pages
    
    def __makeRequest(self, urlApiBase, params, pageName):
        OK = False
        raw = ""
        data = {}

        while not OK:
            try:
                response = urllib.urlopen(urlApiBase + "%s" % params)
                raw = response.read()
                if "<title>Wikimedia Error</title>" in raw:
                    print "[makeRequest] GOT HTML data...", pageName
                    logging.error("[makeRequest] GOT HTML data in page %s", pageName)
                    time.sleep(0.3)
                else:
                    OK = True
            
            except IOError:
                logging.error("[MakeRequest] Network is unreacheable. Sleeping... Page: %s  -  Raw: %s", pageName, raw)
                time.sleep(0.3)
        
        try: 
            return ast.literal_eval(raw)
        except SyntaxError:
            logging.error("[MakeRequest] Syntax error found on title %s and data %s", pageName, raw)
            print "[MakeRequest] Error on title: ", pageName, " Data:", raw
            return {}

    def __getPageContentWikiText(self, pageName):

        params = urllib.urlencode({'format': 'json', 'action': 'query', 'prop': 'revisions', 'rvprop': 'content|timestamp', 'rvlimit': 1, 'titles': pageName, 'redirects':1})
        data = self.__makeRequest(self.__apibase, params, pageName)

        pageid = data["query"]["pages"].keys()[0]
        if int(pageid) < 0:
            return []

        wikitext = data["query"]["pages"][pageid]["revisions"][0]["*"]
        
        return words

    def __encode_name(self, page):
        #http://stackoverflow.com/questions/6480723/urllib-urlencode-doesnt-like-unicode-values-how-about-this-workaround
        if isinstance(page, unicode):
            return page.encode('utf8')
        elif isinstance(page, str):
            # Must be encoded in UTF-8
            return page.decode("unicode_escape").encode('utf8')
        return page

    def __getPageContentHTML(self, pageName):
        
        pageNameUTF8 = self.__encode_name(pageName)
        
        params = urllib.urlencode({'format': 'json', 'action': 'parse', 'prop': 'text|headhtml', 'page': pageNameUTF8, 'redirects':1})
        data = self.__makeRequest(self.__apibase, params, pageNameUTF8)
        
        if "error" in data:
            return ""

        htmlText = data["parse"]["text"]["*"]
        return htmlText
    
    def getPageContent(self, pageName, format="html"):
        if format == "html":
          return self.__getPageContentHTML(pageName)
        elif format == "wikitext":
          return self.__getPageContentWikiText(pageName)
        else:
          print "Wrong format received: " + format

####--------------------------------------------------------------------------------------------------------------------####

    def __getAllDataWithContinue(self, category, typeToGet="subcat"):

        logging.debug("Getting data from category %s", category)

        continueMember = None
        data = self.__getSubCat(category, typeToGet, None)
        #print " ==== data = ", data
        dataCollected = [data["query"]["categorymembers"][i]["title"] for i in range(len(data["query"]["categorymembers"]))]

        if ("query-continue" in data) and ("categorymembers" in data["query-continue"]) and ("cmcontinue" in data["query-continue"]["categorymembers"]):
            continueMember = data["query-continue"]["categorymembers"]["cmcontinue"]

        while continueMember is not None:

            data = self.__getSubCat(category, typeToGet, continueMember)
            dataCollected += [data["query"]["categorymembers"][i]["title"] for i in range(len(data["query"]["categorymembers"]))]

            if ("query-continue" in data) and ("categorymembers" in data["query-continue"]) and ("cmcontinue" in data["query-continue"]["categorymembers"]):
                continueMember = data["query-continue"]["categorymembers"]["cmcontinue"]
            else:
                continueMember = None

        #print "Data colleted: ", dataCollected
        return dataCollected

    def __getSubCat(self, category, typeToGet="subcat", continueElement=None):
        
        #take care...i am not using the utf8 gived by wikipedia because it messes with the dash ("-")

        if continueElement is None:
            #params = urllib.urlencode({'format': 'json', 'utf8': 'true', 'action': 'query', 'list': 'categorymembers', 'cmdir': 'asc', 'cmtype': typeToGet, 'cmtitle': category})
            params = urllib.urlencode({'format': 'json', 'action': 'query', 'list': 'categorymembers', 'cmdir': 'asc', 'cmtype': typeToGet, 'cmtitle': category})
        else:
            #params = urllib.urlencode({'format': 'json', 'utf8': 'true', 'action': 'query', 'list': 'categorymembers', 'cmdir': 'asc', 'cmtype': typeToGet, 'cmtitle': category, "cmcontinue": continueElement})
           params = urllib.urlencode({'format': 'json', 'action': 'query', 'list': 'categorymembers', 'cmdir': 'asc', 'cmtype': typeToGet, 'cmtitle': category, "cmcontinue": continueElement})

        return self.__makeRequest(self.__apibase, params, category)

