#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Import block
import sys, os, traceback, random
from os import listdir
from os.path import isfile, isdir, join
from gitbotException import GitbotException
from gitbotParser import Gitbot
import json

        
#### Entry point #####
#Usage: gitbotTest.py directory

if __name__ == '__main__':
    if len(sys.argv) < 2:
       sys.stdout.write('Uso: gitbotTest.py directorio\n')
       sys.stdout.flush()
    else: 
        exit_status = 0
        count_errors = 0
        count_success = 0
        
        try:    
            if not isdir(sys.argv[1]):
                raise GitbotException(17)
            else:
                jsonFiles = [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]
                
                for fich in jsonFiles:
                    try:
                        parser = Gitbot([sys.argv[0],os.path.join(sys.argv[1],fich)])
                        parser.preParse()
                        data = parser.parse()
                        sys.stdout.write(json.dumps(data,indent=4))
                        sys.stdout.flush()
                        exit_status = 0  
                        count_success += 1
                    except GitbotException as e:
                        sys.stderr.write(e.message+'\n')
                        sys.stderr.flush()
                        count_errors += 1
                    except Exception as e:
                        sys.stderr.write(str(e)+'\n')
                        sys.stderr.flush()
                        count_errors += 1
        except GitbotException as gbe:
            sys.stderr.write(gbe.message+'\n')
            sys.stderr.flush()