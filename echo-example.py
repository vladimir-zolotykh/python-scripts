#!/usr/bin/env python
import  subprocess
name = "Hello!"
proc = subprocess.Popen(['echo', name],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                        )
(out, err) = proc.communicate()
print out
