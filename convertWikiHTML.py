# -*- coding: utf8 -*-
import sys
from pijnu import makeParser
#necessary to set: export PYTHONPATH=/home/palotti/healthWikipedia/mediaWikiDependences/pinjnu

def convertFromWikiToHTML(infile):

    print "Converting from Wiki to HTML: ", infile

    #print "Loading dependences."
    # get the parser
    preprocessorGrammar = file("mediaWikiDependences/preprocessor.pijnu").read()
    makeParser(preprocessorGrammar)

    mediawikiGrammar = file("mediaWikiDependences/mediawiki.pijnu").read()
    makeParser(mediawikiGrammar)

    allowed_tags = ['p', 'span', 'b', 'i', 'small', 'center', 'ref', 'gallery']
    allowed_autoclose_tags = ['br', 'hr']
    allowed_parameters = ['class', 'style', 'name', 'id', 'scope']
    interwiki = {'ar': 'http://ar.wikipedia.org/wiki/',
                 'az': 'http://az.wikipedia.org/wiki/',
                 'zh': 'http://zh.wikipedia.org/wiki/',
                 'it': 'http://it.wikipedia.org/wiki/',
                 'jp': 'http://jp.wikipedia.org/wiki/',
                 'ja': 'http://ja.wikipedia.org/wiki/',
                 'jv': 'http://jv.wikipedia.org/wiki/',
                 'pt': 'http://pt.wikipedia.org/wiki/',
                 'br': 'http://br.wikipedia.org/wiki/',
                 'ca': 'http://ca.wikipedia.org/wiki/',
                 'cs': 'http://cs.wikipedia.org/wiki/',
                 'da': 'http://da.wikipedia.org/wiki/',
                 'de': 'http://de.wikipedia.org/wiki/',
                 'en': 'http://en.wikipedia.org/wiki/',
                 'eo': 'http://eo.wikipedia.org/wiki/',
                 'es': 'http://es.wikipedia.org/wiki/',
                 'simple': 'http://simple.wikipedia.org/wiki/',
                 'sco': 'http://sco.wikipedia.org/wiki/',
                 'ro': 'http://ro.wikipedia.org/wiki/',
                 'pl': 'http://pl.wikipedia.org/wiki/',
                 'kk': 'http://kk.wikipedia.org/wiki/',
                 'fr': 'http://fr.wikipedia.org/wiki/'}

    namespaces = {'Template':   10,
                  u'Catégorie': 14,
                  'Category':   14,
                  'File':        6,
                  'Fichier':     6,
                  'Image':       6}
    templates = {'listen': u"""{| style="text-align:center; background: #f9f9f9; color: #000;font-size:90%; line-height:1.1em; float:right;clear:right; margin:1em 1.5em 1em 1em; width:300px; border: 1px solid #aaa; padding: 0.1em;" cellspacing="7"
#! class="media audio" style="background-color:#ccf; line-height:3.1em" | Fichier audio
#|-
#|<span style="height:20px; width:100%; padding:4pt; padding-left:0.3em; line-height:2em;" cellspacing="0">'''[[Media:{{{filename|{{{nomfichier|{{{2|}}}}}}}}}|{{{title|{{{titre|{{{1|}}}}}}}}}]]''' ''([[:Fichier:{{{filename|{{{nomfichier|{{{2|}}}}}}}}}|info]])''<br /><small>{{{suitetexte|{{{description|}}}}}}</small>
#<center>[[Fichier:{{{filename|{{{nomfichier|{{{2|}}}}}}}}}|noicon]]</center></span><br /><span style="height:20px; width:100%; padding-left:0.3em;" cellspacing="0"><span title="Des difficultés pour écouter le fichier ?">[[Image:Circle question mark.png|14px|link=Aide:Écouter des sons ogg|Des difficultés  pour  écouter le fichier ?]] ''[[Aide:Écouter des sons ogg|Des problèmes pour écouter le fichier ?]]''</span>
#|}
#""",'3e': '3<sup>e</sup>'}

    #print "Importing preprocessor parser."
    from preprocessor import make_parser
    preprocessor = make_parser(templates)

    #print "Importing html parser."
    from html import make_html_parser
    parser = make_html_parser(allowed_tags, allowed_autoclose_tags, allowed_parameters, interwiki, namespaces)
    
    #from text import make_parser
    #parser = make_parser()

    # import the source in a utf-8 string
    #print "Importing codecs."
    import codecs
    fileObj = codecs.open(infile, "r", "utf-8")
    source = fileObj.read()

    # The last line of the file will not be parsed correctly if
    # there is no newline at the end of file, so, we add one.
    if source[-1] != '\n':
      source += '\n'

    #print "Processing text"
    preprocessed_text = preprocessor.parse(source)
    #print "Parsing tree"
    tree = parser.parse(preprocessed_text.leaves())

    #output = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
    #<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">
    #head><title>Test!</title></head>""" + tree.leaves() + "</html>"
    #print "Take output"
    output = tree.leaves()

    #print "Encode utf8 and Returns"
    return output.encode('UTF-8')
    #file("article.htm", "w").write(output.encode('UTF-8'))
    #file("article.txt", "w").write(output.encode('UTF-8'))


if __name__ == "__main__":
    print convertFromWikiToHTML(sys.argv[1])
    
