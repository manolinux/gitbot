from html.parser import HTMLParser
import json
class GitbotExtraParser(HTMLParser):

    def __init__(self):
        self.data = []
        self.last_tag = None
        self.last_tag_attrs = None
        self.inside_interesting_a_tag = False

        # initialize the base class
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        #Language is under a span containing class "text-gray-dark text-bold mr-1"
        self.last_tag = tag
        self.last_tag_attrs = attrs
        
        
        #We're labelling an <a> tag with data-ga-click containging language stats
        if tag == 'a':
            for attr in attrs:
                key,value = attr
                #Is there data-ga-click attr?
                if key=='data-ga-click':
                    #Have we got language stats in it?
                    if 'language stats' in value.lower():
                        self.last_a_tag = tag
                        self.last_tag_attrs = attrs
                        self.inside_interesting_a_tag = True


       
    def handle_endtag(self, tag):
        if tag == 'a':
            self.inside_interesting_a_tag = False

    def handle_data(self, data):
        #Are we inside a <span>
        hasInfo = False
        if self.last_tag == 'span':
            #Are we inside a cool <a> tag
            if self.inside_interesting_a_tag:
                attrs = self.last_tag_attrs
                #Ok we're inside language stats
                #Let's check for text-gray-dark text-bold mr-1
                for attr in attrs:
                    key,value = attr
                    if key == 'class':
                        if 'text-gray-dark' in value.lower() and 'text-bold mr-1' in value.lower():
                            hasInfo = True
                #Found language
                if hasInfo:
                    if data.isalnum():
                        self.data.append(data)
                else:
                    #We're a percentage
                    if data.endswith('%'):
                        self.data.append(data)

    
    def reset(self):
        self.data = []
        HTMLParser.reset(self)

    def getData(self):
        return self.data