#!/usr/bin/env python
import sh
output = sh.tail(sh.cat('words.txt'), '-2')
print output


import subprocess

#The following code does work.

#p = subprocess.Popen("cat words.txt | tail -1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
#Try shell=True if the above doesn't work with shell=False
#p_stdout = p.stdout.read()
#p_stderr = p.stderr.read()
#print p_stdout

p1 = subprocess.Popen(["cat", "words.txt"], stdout=subprocess.PIPE)
p2 = subprocess.Popen(["tail", "-1"], stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
output,err = p2.communicate()
print output
#print "'cat words.txt | tail -1' produces %s" % output
