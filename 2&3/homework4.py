# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import urlparse
import os
import urllib
import sys


def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s


def get_page(page):
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


def union_dfs(a, b):
    for e in b:
        if e not in a:
            a.append(e)


def union_bfs(a,b):
    len_b=len(b)
    for i in range(len_b):
        if not b[len_b-i-1] in a:
            a.insert(i,b[len_b-i-1])


def add_page_to_folder(page, content):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index.txt'  # index.txt中每行是'网址 对应的文件名'
    folder = 'html'  # 存放网页的文件夹
    filename = valid_filename(page)  # 将网址变成合法的文件名
    index = open(index_filename, 'a')
    index.write(page.encode('ascii', 'ignore') + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(content)  # 将网页存入文件
    f.close()


def crawl(seed, method, max_page):
    tocrawl = [seed]
    crawled = []
    graph = {}
    count = 0

    while tocrawl:
        if count<=max_page:
            page = tocrawl.pop()
            if page not in crawled:
                print page
                content = get_page(page)
                add_page_to_folder(page, content)
                outlinks = get_all_links(content, page)
                globals()['union_%s' % method](tocrawl, outlinks)
                graph[page] = content
                crawled.append(page)
                count =count+1
        else:
            break
    return graph, crawled


if __name__ == '__main__':
    seed =  "http://www.sjtu.edu.cn"
    method='dfs'
    max_page=10

    # seed = sys.argv[1]
    # method = sys.argv[2]
    # max_page = sys.argv[3]

    graph, crawled = crawl(seed, method, max_page)
