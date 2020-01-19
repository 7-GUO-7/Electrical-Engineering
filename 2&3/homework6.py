import threading
import Queue
import time
from bs4 import BeautifulSoup
import urllib2
import re
import urlparse
import os
import urllib
import sys

def get_page(page):
    print 'downloading page %s' % page
    # time.sleep(0.5)
    try:
        content = urllib2.urlopen(page,timeout=10)
        content=content.read()
    except:
        return ''
    else:
        return content

def get_all_links(content, page):
    links = []
    # req = urllib2.Request(page, None, {'User-agent': 'guo'})
    # resp = urllib2.urlopen(req)
    soup = BeautifulSoup(content,"html.parser")
    urls=soup.findAll('a',{'href': re.compile('^http|^/')})
    for url in urls:
        t=url.get('href','')
        tmp=t.encode('utf8')
        if tmp[0]=='/':
            if tmp[-3:]=='rar':
                continue
            else:
                t=urlparse.urljoin(page,t)
        links.append(t)
    return links

# def get_page(page):
#     print 'downloading page %s' % page
#     time.sleep(0.5)
#     return g.get(page, [])
#
# def get_all_links(content):
#     return content

def working(max_pages):
    t=0
    # while True:
    while t<max_pages:
        page = q.get()
##        if varLock.acquire():
        if page not in crawled:
        # no matter how many threads do this job, the url in crawled is still max_page(10), so it only prints 10 urls,not 20 for 2 threads.
##                varLock.release()
##        else:
##                varLock.release()
            content = get_page(page)
            outlinks = get_all_links(content,page)
            for link in outlinks:
                q.put(link)
            if varLock.acquire():
                graph[page] = outlinks
                crawled.append(page)
                varLock.release()
            q.task_done()
        t=t+1
    else:
        exit()

# g = {'A':['B', 'C', 'D'],\
#      'B':['E', 'F'],\
#      'C':['1','2'],\
#      '1':['3','4'],\
#      'D':['G', 'H'],\
#      'E':['I', 'J'],\
#      'G':['K', 'L'],\
#      }

# def crawl(seed, method, max_page):
#     tocrawl = [seed]
#     crawled = []
#     graph = {}
#     count = 0
#
#     while tocrawl:
#         if count<=max_page:
#             page = tocrawl.pop()
#             if page not in crawled:
#                 print page
#                 content = get_page(page)
#                 add_page_to_folder(page, content)
#                 outlinks = get_all_links(content, page)
#                 globals()['union_%s' % method](tocrawl, outlinks)
#                 graph[page] = content
#                 crawled.append(page)
#                 count =count+1
#         else:
#             break
#     return graph, crawled

start = time.clock()
NUM = 10
crawled = []
graph = {}
varLock = threading.Lock()
q = Queue.Queue()
q.put('http://www.sjtu.edu.cn')
max_pages=10
for i in range(NUM):
    t = threading.Thread(target=working(max_pages))
    t.setDaemon(True)
    t.start()
q.join()
end = time.clock()
# print end-start