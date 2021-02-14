# gitbot
Bot for searching Github

# Contents
- [Requirements](#Requirements)
- [Usage](#Usage)
- [JSON entry](#JSON-entry)
- [JSON output](#JSON-output)
- [Tests and coverage metrics](#Tests-and-coverage-metrics)
- [TODOs](#TODOs)
## Requirements

Python3.
According to pipreqs (https://pypi.org/project/pipreqs/), generated requirements.txt is:

```
urllib3==1.24.3
requests==2.20.0
```
## Usage

```[shell]
$ gitbot.py <path_to_configuration_json>
```
Configuration contains the terms of the search, anonymizing proxies to use, whether we want to search Repositories, Issues or Wikis. See [JSON entry](#JSON-entry) for reference.

And, as a result we'll receive a JSON in stdout ontaining the results of the search. 
See [JSON output](#JSON-output) for details.
Errors are sent to stderr.

## JSON entry 
```[JSON]
    {
        #List of keywords to search
        "keywords" : ["openstack","nova","css"],
        #List of anonymizer proxies from http://free-proxy.net, format is ip:port
        "proxies" : ["100.101.102.103:8080","104.105.106.107:443"],
        #Type, one of Repositories | Issues | Wikis 
    }   "type" : "Repositories"

```
## JSON output

```[JSON]
    [
        #Array of results
        {
        #URL 
        "url" : "https://github.com/manolinux/foo",
        #Extra only present when querying repositories
        "extra": {
            #Owner of the repository
            "owner" : "manolinux",
            "language_stats": {
                "JavaScript" : 50.0
                "Python" : 50.0
            }
        }
    ]

```
## Tests and coverage metrics

Json directory in project distribution has some tests, covering many scenarios of failures and success.
Given Coverage  - https://pypi.org/project/coverage/ - is installed, we can check about the sentences visited.  A program test, called gitbotTest.py, executes all the tests in the json/ directory. So, firing gitbotTest.py with coverage gives us an idea of the quality of the project:

```[shell]
 $ pip install coverage
 $ coverage3 run --source . --omit gitbot.py gitbotTest.py json
    ... Errors in stderr
    ... Output in stdout
    [
    {
        "url": "https://github.com/atuldjadhav/DropBox-Cloud-Storage"
    },
    {
        "url": "https://github.com/michealbalogun/Horizon-dashboard"
    }
    ]
    ...
 $ coverage3 report
 Name                  Stmts   Miss  Cover
-----------------------------------------
__init__.py               1      1     0%
gitbotException.py        8      0   100%
gitbotHtmlParser.py      33      2    94%
gitbotParser.py         108      9    92%
gitbotSaxParser.py       27     13    52%
gitbotTest.py            37      6    84%
-----------------------------------------
TOTAL                   214     31    86%
```
In this case, gitbot.py is ommited, as it is not used by gitbotTest.py.

## TODOs
* One proxy is chosen amongst the ones in the list randomly, but there is no checking about it's availability. Probably should be pinged somehow before using, and discard if it is down.
* Accept JSON configuration via stdin
* Accept multy-entry JSON, so that you don't have to invoke the program many times.
* Convert this into a ready-to-install package via setup.py