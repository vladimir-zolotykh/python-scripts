#!/usr/bin/env python
#import subprocess

import os
path = "words2.txt"
#os.path.exists(path) # returns whether the path (dir or file) exists or not
if os.path.isfile(path) :
    print "The file %s exists" % path
dirpath = "foodir"
if os.path.isdir(dirpath):
    print "The file %s is a directory." % dirpath