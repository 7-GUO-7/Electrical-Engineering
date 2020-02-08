#!/usr/bin/env python

from operator import itemgetter
import sys

# current_word = None
# current_count = 0
# word = None

answer={}
answer['a']=0
answer['b']=0
answer['c']=0
answer['d']=0
answer['e']=0
answer['f']=0
answer['g']=0
answer['h']=0
answer['i']=0
answer['j']=0
answer['k']=0
answer['l']=0
answer['m']=0
answer['n']=0
answer['o']=0
answer['p']=0
answer['q']=0
answer['r']=0
answer['s']=0
answer['t']=0
answer['u']=0
answer['v']=0
answer['w']=0
answer['x']=0
answer['y']=0
answer['z']=0

answer_count = []
for i in range(27):
    answer_count.append(0)
# input comes from STDIN
i=0
for line in sys.stdin:
    line = line.strip()
    word, count = line.split('\t', 1)
    while True:
        if word[0] != chr(ord('a') + i):
            i+=1
        else:
            break;
    answer[chr(ord('a')+i)]+=len(word)
    answer_count[1+i]+=1

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    # if current_word == word:
    #     current_count += count
    # else:
    #     if current_word:
    #         # write result to STDOUT
    #         print '%s\t%s' % (current_word, current_count)
    #     current_count = count
    #     current_word = word

# do not forget to output the last word if needed!
# if current_word == word:
#     print '%s\t%s' % (current_word, current_count)
final=[]
for i in range(27):
    final.append(0)
for i in range(26):
    if answer_count[i+1]==0:
        {}
        # print chr(ord('a')+i),'\t',0
        # print chr(ord('a')+i),'\t',final[i + 1]
    else:

        final[i+1]=float(answer[chr(ord('a')+i)])/answer_count[i+1]
        print chr(ord('a')+i),'\t',final[i+1]