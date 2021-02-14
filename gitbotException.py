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
        13: 'Could not get an impersonation proxy, list is empty',
        14: 'Could not verify proxies, list is not correct: {0}',
        15: 'Keyword entry must be a single one, not a list: {0}',
        16: 'Exception connecting or parsing HTML: {0}',
        17: 'Should provide a directory as argument',
        18: 'Error decoding JSON in HTML {0}'
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
    