#!/usr/bin/env python

import sys
if __name__ == "__main__":
    if len(sys.arg) > 2:
        num1=long(sys.argv[1])
        num2=long(sys.argv[2])
    else:
        print "Two or more arguments expected."
        sys.exit(1)
    print "%s" % str(num1+num2)
    