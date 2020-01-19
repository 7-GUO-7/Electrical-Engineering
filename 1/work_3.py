import sys
reload(sys)
sys.setdefaultencoding('UTF-8')
import re
import urlparse
import urllib2
from bs4 import BeautifulSoup

def parseQiushibaikePic(content):
    req=urllib2.Request("http://www.qiushibaike.com/pic",None,{'User-agent':'guo'})
    resp=urllib2.urlopen(req)
    soup = BeautifulSoup(resp)
    docs={}
    nextpage=''

    list_id=[]
    for url_1 in soup.findAll('div',{'id':re.compile('^qiushi_tag')}):

        t=url_1.get('id','')
        tmp=t.split('_')[-1]
        list_id.append(tmp)

    list_content=[]
    for url_2 in soup.findAll('div',{'class','content'}):
        for url_2_1 in url_2.findAll('span'):
    #findAll can deal with the element( or the definite html string, not a list)
            tmp2=url_2_1.get_text()
            list_content.append(tmp2)

    url_original = 'http://www.qiushibaike.com/pic'
    list_url=[]
    for url_3 in soup.findAll('div',{'class','thumb'}):
        for url_3_1 in url_3.findAll('img'):
            tmp3=url_3_1.get('src','')
            tmp3 = urlparse.urljoin(url_original, tmp3)
            list_url.append(tmp3)

    num=len(list_id)  # how many groups of information
    for i in range(num):
        docs[list_id[i]]={'content':list_content[i],'imgurl':list_url[i]}

    url_next=soup.findAll('ul',{'class','pagination'})
    # the last "pagination class" contains the next page
    flag=1
    # url_next is a list, you must take its elements to use findAll
    for i in url_next:
        for use in i.findAll('li'):
            if flag==2:
                key=use
                break
            flag += 1
    for tmp in key.findAll('a'):
        key_url=tmp.get('href','')

    url_original = 'http://www.qiushibaike.com/pic'
    nextPage=urlparse.urljoin(url_original,key_url)
    nextpage=str(nextPage)

    # if it is a list, you cannot find its children.
    # you need to get the element in it, because there may be many different elements in it, you cannot take its children.
    return docs,nextpage

def main():
    url = 'http://www.baidu.com'
    #url = 'http://www.sjtu.edu.cn'
    if len(sys.argv) > 1:
        url = sys.argv[1]
    content = urllib2.urlopen(url).read()
    docs,nextPage=parseQiushibaikePic(content)
    file=open('res3.txt','w')
    file.write(nextPage+'\n')
    for key in docs.keys():
        file.write(key + '\t' + docs[key]['content'] +'\t'+ docs[key]['imgurl']+ '\n') #.encode('utf8')

if __name__ == '__main__':
    main()