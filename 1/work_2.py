import sys
import urllib2
from bs4 import BeautifulSoup

def parselMG(content):
    imgset=set()
    soup = BeautifulSoup(content)
    for url in soup.findAll('img'):
        x = url.get('src','')
        imgset.add(x)
    return imgset

def write_outputs(urls, filename):
    with open(filename, 'w') as f:
        for url in urls:
            f.write(url)
            f.write('\n')

def main():
    url = 'http://www.baidu.com'
    #url = 'http://www.sjtu.edu.cn'
    if len(sys.argv) > 1:
        url = sys.argv[1]
    content = urllib2.urlopen(url).read()
    urls_2=parselMG(content)

    write_outputs(urls_2, 'res2.txt')

if __name__ == '__main__':
    main()