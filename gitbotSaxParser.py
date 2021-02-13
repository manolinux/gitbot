import xml.sax
from xml.sax import saxutils
import sys


class GitbotSaxParser(xml.sax.handler.ContentHandler,
        xml.sax.handler.ErrorHandler):
    def __init__(self, out = sys.stdout):
        xml.sax.handler.ContentHandler.__init__(self)
        
    def startDocument(self):
        pass

    def startElement(self, name, attrs):
        if name == 'a':
            for attr in attrs.getNames():
                print (attr,attrs.getValue(attr))
                print("\n")


    def endElement(self, name):
        pass

    def characters(self, content):
        pass

    def ignorableWhitespace(self, content):
        pass
        
    def processingInstruction(self, target, data):
        pass

    def error(exception):
        sys.stderr.write(str(exception))

    def characters(self, chars):
        pass
    
    #It turns out that attributes without values fire this, as
    #in strictly well-formed XHTML shoudln't occur
    def fatalError(object,exception):
        pass
        #sys.stderr.write(str(exception))   