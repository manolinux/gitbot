#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Import block
import sys, os, traceback, random
from os import listdir
from os.path import isfile, join
from gitbotException import GitbotException
from gitbotParser import Gitbot
import json
        
#### Entry point #####
#Usage: gitbotTest.py jsonDirectory

if __name__ == '__main__':
    exit_status = 0
    try:
        parser = Gitbot(sys.argv)
        parser.preParse()
        data = parser.parse()
        sys.stdout.write(json.dumps(data,indent = 4)+"\n")
        sys.stdout.flush()
        exit_status = 0
    except GitbotException as e:
        sys.stderr.write(e.message+'\n')
        sys.stderr.flush()
        exit_status = e.code
    except Exception as e:
        sys.stderr.write(str(e)+'\n')
        sys.stderr.flush()
        exit_status = 1000
    finally:
        sys.exit(exit_status)


    