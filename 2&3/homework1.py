# -*- coding:utf-8 -*-
import urllib2, cookielib, urllib
from bs4 import BeautifulSoup
import sys

def bbs_set(id, pw, text):
    import urllib2, cookielib, urllib
    from bs4 import BeautifulSoup
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    postdata = urllib.urlencode({
        'id': id,
        'pw': pw,
        'submit': 'login'
    })

    new_data = urllib.urlencode({
        'type':'update',
        'text': text
    })
    print new_data
    req1 = urllib2.Request(url='https://bbs.sjtu.edu.cn/bbslogin', data=postdata)
    urllib2.urlopen(req1)
    req2= urllib2.Request(url='https://bbs.sjtu.edu.cn/bbsplan', data=new_data)
    req3= urllib2.Request(url='https://bbs.sjtu.edu.cn/bbsplan')

    urllib2.urlopen(req2).read()
    content1 = urllib2.urlopen(req3).read()

    soup = BeautifulSoup(content1)
    print str(soup.find('textarea').string).strip().encode('utf8')

if __name__ == '__main__':

    # id = 'guox'
    # pw = '000000'
    # text = 'hello i am GUO'

    id = sys.argv[1]
    pw = sys.argv[2]
    text = sys.argv[3].decode('utf-8').encode('gbk')

    bbs_set(id, pw, text)
