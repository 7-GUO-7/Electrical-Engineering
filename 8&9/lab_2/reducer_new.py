#!/usr/bin/env python

import sys
page_count=0
page_rank_list=[]
point_url={}
original_url=[]
# f=open("PRtest")
# for line in f:
for line in sys.stdin:
    line = line.strip()
    if len(line) > 0:
        words = line.split()
        original_url.append(int(words[0]))
        page_rank_list.append(float(words[1]))
        if len(words)>=3:
            url_length=len(words)-2
        else:
            url_length=0
        point_url_list = []
        for i in range(url_length):
            point_url_list.append(int(words[2+i]))
        point_url[page_count]=point_url_list
        page_count += 1

for i in range(page_count):
    if len(point_url[i])==0:
        continue
    else:
        giving_rank=float(page_rank_list[i])/(len(point_url[i]))
        for t in range(len(point_url[i])):
            page_rank_list[point_url[i][t]-1]+=giving_rank


sum=0
for i in range(page_count):
    sum+=page_rank_list[i]

a=float(sum)/100

for i in range(page_count):
    page_rank_list[i]/=a

for i in range(page_count):

    # print original_url[i],'\t',page_rank_list[i],'\t',
    for t in range(len(point_url[i])):
        point_url[i][t]=str(point_url[i][t])
    print_point_url='\t'.join(point_url[i])
    print '%s\t%s\t%s' % (original_url[i], page_rank_list[i], print_point_url)