from html.parser import HTMLParser
import json
from gitbotException import GitbotException
class GitbotHtmlParser(HTMLParser):

    def __init__(self):
        self.data = []
        # initialize the base class
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        #Results are under <a> tags within an atribute called data-hydro-click
        if tag == 'a':
            hasInfo = False
            info = None
            for attr in attrs:
                key,value = attr
                #Info we care abo
                if key=='data-hydro-click':
                    hasInfo = True
                    info = value
            if hasInfo:
                #We are near our target, event_type must be search.result.type
                try:
                    jsonInfo = json.loads(info)
                    #And also event_type must be search_result.click
                    if jsonInfo['event_type'] == 'search_result.click':
                        result = jsonInfo['payload']['result']
                        newData = {
                            'url' : result['url']
                        }
                        self.data.append(newData)
                #In case it has no event_type (we don't care)    
                except json.decoder.JSONDecodeError as jse:
                    raise GitbotException(18,info)
                except Exception as e:
                    pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass
    
    def reset(self):
        self.data = []
        HTMLParser.reset(self)

    def getData(self):
        return self.data