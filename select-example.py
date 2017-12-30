#!/usr/bin/env python
import os

path="."
files=dict((str(i), f) for i,f in 
    enumerate(f for f in os.listdir(path) if f.endswith(('.py', '.txt'))))
print files
for item in sorted(files.items()):
    print '[%s] %s' % item  
choice = None
while choice is None:
    choice = files.get(raw_input('Enter selection: '))
    print choice
    if not choice:
        print 'Please make a valid selection'
    else:
        print "You selected '%s'" % choice
            