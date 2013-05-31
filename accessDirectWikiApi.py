#!/usr/bin/env python
# encoding: utf-8

import re
from myWikiApi import myWikiApi
wikibase = "en"

def convertUnicode(de):
  #print "original =", name
  de = de.decode("utf-8")
  #print "decoded utf-8 =", de
  de = de.replace("\u2013", "-")  
  #print "replaced =", de
  de = de.encode("utf-8")
  #print "encoded utf-8 =", de
  de = de.decode('unicode-escape')
  #print "decoded unicode-escap =", de
  de = re.sub(ur'[\xc2-\xf4][\x80-\xbf]+',lambda m: m.group(0).encode('latin1').decode('utf8'),de)
  return de.encode("utf-8")

if __name__ == "__main__":
  api = myWikiApi("http://"+wikibase+".wikipedia.org/w/api.php?")

  #categories = ["Category:B-Class_medicine_articles"]
  categories = ["Category:FA-Class_medicine_articles", "Category:FL-Class_medicine_articles", "Category:FM-Class_medicine_articles", "Category:A-Class_medicine_articles", "Category:GA-Class_medicine_articles", "Category:B-Class_medicine_articles", "Category:C-Class_medicine_articles", "Category:Start-Class_medicine_articles", "Category:Book-Class_medicine_articles", "Category:Category-Class_medicine_articles", "Category:List-Class_medicine_articles", "Category:NA-Class_medicine_articles", "Category:Portal-Class_medicine_articles", "Category:Portal-Class_medicine_articles", "Category:Project-Class_medicine_articles", "Category:Redirect-Class_medicine_articles", "Category:Template-Class_medicine_articles", "Category:Unassessed_medicine_articles"]
  # removed:  "Category:File-Class_medicine_articles"
  result = map(api.getAllPagesBelongingToACategory, categories)

  for listOfPages in result:
    for page in listOfPages:
      print convertUnicode(page).replace("Talk:","")


