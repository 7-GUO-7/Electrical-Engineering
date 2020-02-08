#!/usr/bin/env python

import sys
# f=open("PRtest")
# for line in f:
for line in sys.stdin:
    line = line.strip()
    if len(line) > 0:
        words = line.split()
        if len(words)>=3:
            for t in range(2,len(words)):
                words[t]=str(words[t])
            tmp=' '.join(words[2:])
        else:
            tmp=''
        print '%s\t%s\t%s' %(words[0],words[1],tmp)
