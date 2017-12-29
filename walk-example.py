#!/usr/bin/env python
from os import walk

mypath="/home/visteon/workspace/Release-13.1.1/DeliSpace/"
f=[]
for (dirpaths, dirnames, filenames) in walk(mypath) :
    f.extend(dirnames)
    break
print f
