import os,sys,traceback
import json
import ipaddress
import requests
import requests
import random
from xml.sax import make_parser,handler
import urllib3
from gitbotException import GitbotException
from gitbotSaxParser import GitbotSaxParser
from gitbotHtmlParser import GitbotHtmlParser
        
#### Gitbot parser class
class Gitbot():
    #Class variables
    GITHUB_SEARCH_URL = 'https://github.com/search'
    SEARCH_TYPES = ['Repositories','Issues','Wikis']
    SEARCH_TAGS = ['a']
    SEPARATORS = ['\r',' ','\t','\n',',','"',";",":"]
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
                    #Verify proxies comply with ipaddress:port
                    if not self.verifyProxies(): raise GitbotException(14,self.proxies)
                    self.typeSearch = self.configuration["type"]
                    #Type of search must be one of allowed types
                    if self.typeSearch not in Gitbot.SEARCH_TYPES:
                        raise GitbotException(11,self.typeSearch,Gitbot.SEARCH_TYPES)
                except GitbotException as gbe:
                    raise gbe
                except IOError as ioe:
                    raise GitbotException(4)
                except json.decoder.JSONDecodeError as je:
                    raise GitbotException(5)        
        return True
    
    def scrapeData(self,url,parameters,proxy,htmlParser):
        try:
            r = requests.get(url, 
                 proxies={'http' : 'http://' + proxy, 'https' : 'https://' + proxy}, 
                 timeout=20, params=parameters, stream=True)    
             
        #https://github.com/psf/requests/issues/5297
        except urllib3.exceptions.ProxySchemeUnknown:
                r = requests.get(url, 
                proxies={'http' :proxy,
                             'https' : proxy}, 
                timeout=20,
                params=parameters, stream=True)          

        r.raw.decode_content = True
      
        for chunk in r.iter_content(1024):
            htmlParser.feed(str(chunk))
            
        data = htmlParser.getData()
        return data

    def parse(self):
        """
        Processing itself, will take the configuration loaded before,
        get a proxy, emit the search, pick and collect results, and
        output them
        """
        #Are parameters correctly setted by preParse?
        #Avoid checking proxies
        if isinstance(self.keywords,list) and self.typeSearch in Gitbot.SEARCH_TYPES:    

            #Here we go!
            #Verify keywords don't contain separators
            if not self.verifyKeywords(): raise GitbotException(15,self.keywords)
            
            #Get a proxy
            proxy = self.getProxy()
            #Could not get a proxy
            if proxy is None: raise GitbotException(13)
            
            #We've got a proxy, let's connect 
            parameters = {'q': "+".join(self.keywords),'type': self.typeSearch}

            #Full data = generalData + extra
            data = []

            #Let's use anoter strategy
            htmlParser = GitbotHtmlParser()
            generalData =  self.scrapeData(Gitbot.GITHUB_SEARCH_URL,parameters,proxy,htmlParser)
            htmlParser.reset()
            return generalData

        #Something went wrong, probably preParse was not invoked first                
        else:
            raise GitbotException(12)
            
    def verifyKeyword(self,keyword):
        """
        Verify that a keyword does not contain separators
        """
        if isinstance(keyword,str):
            for char in Gitbot.SEPARATORS:
                if char in keyword: return False
        else:
            return False
        return True
        
    def verifyProxy(self,proxy):
        """
        Verify that a proxy complies with ipaddress:port schema
        """
        try:
             (ipPart,portPart) = proxy.split(":")
             ipaddress.ip_address(ipPart)
             if int(portPart) < 0 or int(portPart) > 65535: return False
        #Any exception means not validated 
        except:
            return False
        return True
    
    def verifyKeywords(self):
        """
        Verify that keywords doe not contain separators
        """    
        if isinstance(self.keywords,list):
            if len(self.keywords) < 1: return False
            for proxy in self.keywords:
                if not self.verifyKeyword(proxy): return False
        return True
         
    def verifyProxies(self):
        """
        Verify that a proxy complies with ipaddress:port schema
        """    
        if isinstance(self.proxies,list):
            if len(self.proxies) < 1: return False
            for proxy in self.proxies:
                if not self.verifyProxy(proxy): return False
        return True
        
    
    def getProxy(self):
        if isinstance(self.proxies,list):
            if len(self.proxies) < 1: return None
            position = random.randint(0,len(self.proxies)-1)  
            return self.proxies[position]
            
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