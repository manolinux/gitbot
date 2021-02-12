# -*- coding: utf-8 -*-

#Import block
import sys, os, traceback, random
import json


##### Exception handing class
class GitbotException(Exception):
    #class variables
    VALUE_NAMED_DICT = {
        1: 'No configuration file provided',
        2: 'Too many parameters (provide only a file name or stdin pipe containing JSON)',
        3: 'Provided configuration file not found',
        4: 'Error reading JSON config file',
        5: 'Invalid syntax in JSON config file',
        6: 'JSON config file has no "keywords" key',
        7: 'JSON config file has no "proxies" key',
        8: 'JSON config file has no "type" key',
        9: 'JSON config file invalid key: {0}',
        10: 'JSON config file invalid key content: {0}',
        11: 'Type of search {0} is not in {1}',
        12: 'Incorrect parameters for search - did you invoke preParse?',
        13: 'Coud not get an impersonation proxy, list is empty'
    }
    
    def __init__(self,code,*extra):
        """
        code is a numeric code for checking into descriptive error messages
        extra is an extra parameter in case is needed for formatting message
        """
        if len(extra) == 0: self.message  = GitbotException.VALUE_NAMED_DICT[code]
        else: 
            self.message = GitbotException.VALUE_NAMED_DICT[code].format(*extra)
        self.code = code
        self.extra = extra
        super().__init__(self.message)
    
        
#### Gitbot parser class
class Gitbot():
    #Class variables
    GITHUB_SEARCH_URL = 'https://github.com/search'
    SEARCH_TYPES = ['Repositories','Issues','Wikis']
    KEYS_TYPES = {
        'keywords' : list,
        'proxies' : list,
        'type' : str
    }
   
    def __init__ (self,arguments):
        self.file = None
        self.configuration = None
        #No arguments? Let's try with stdin
        if len(arguments) < 2:
            raise GitbotException(1)
        #Too many arguments? That's confusing
        elif len(arguments) > 2:
            raise GitbotException(2)
        #One argument
        else:
            #Is it file accessible?
            self.file = os.path.abspath(arguments[1])
            if not os.path.isfile(self.file):
                raise GitbotException(3)
            
            
    def preParse (self):
        #Open file
        if self.file is not None:
            with open(self.file,'r') as configFile:
                try:
                    #Load configuration
                    self.configuration = json.load(configFile)
                    #Check for JSON keys and types, raises exception
                    self.checkForKeys()
                    self.keywords = self.configuration["keywords"]
                    self.proxies = self.configuration["proxies"]
                    self.typeSearch = self.configuration["type"]
                    #Type of search must be one of allowed types
                    if typeSearch not in Gitbot.SEARCH_TYPES:
                        raise GitbotException(11,typeSearch,Gitbot.SEARCH_TYPES)
                except GitbotException as gbe:
                    raise gbe
                except IOError as ioe:
                    raise GitbotException(4)
                except json.decoder.JSONDecodeError as je:
                    raise GitbotException(5)        
        
    def parse(self):
        #Are parameters correctly setted by preParse?
        #Avoid checking proxies
        if isinstance(self.keywords,list) and self.typeSearch in Gitbot.SEARCH_TYPES:    

            #Here we go!
            proxy = self.getProxy()
            
            #Could not get a proxy
            if proxy is None: raise GitbotException(13)
            
        
        #Something went wrong, probably preParse was not invoked first                
        else:
            raise GitbotException(12)
        
    def getProxy(self):
        if isinstance(self.proxies):
            return self.proxies[random.randint(0,len(self.proxies))]
        return None
             
    def checkForKeys(self):
       if isinstance(self.configuration,dict):
           for key in self.configuration:
                try:
                    if not isinstance(self.configuration[key],Gitbot.KEYS_TYPES[key]):
                        raise GitbotException(10)
                        
                #Will throw exception when accessing a non-existing key
                except:
                    raise GitbotException(9,key)
       else:
            #Should not reach here, checkForKeys was probably invoked before
            #reading configuration
            pass   
        
#### Entry point #####
#Usage: gitbot.py file.json

try:
    if __name__ == '__main__':
        parser = Gitbot(sys.argv)
        parser.preParse()
        result = parser.parse()
        sys.exit(0)
except GitbotException as e:
    sys.stderr.write(e.message+'\n')
    sys.exit(e.code)
except Exception as e:
    traceback.print_tb(e.__traceback__)
    sys.exit(1000)


    