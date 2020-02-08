#!/usr/bin/env python
from typing import Union

import jieba
import sys

reload(sys)
sys.setdefaultencoding('UTF-8')

INDEX_DIR = "IndexFiles.index"
from bs4 import BeautifulSoup
import sys, os, lucene, threading, time
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""


class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            # sys.stdout.write('.')
            sys.stdout.flush()
            # time.sleep(1.0)


class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        ticker = Ticker()
        # print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, root, writer):

        t1 = FieldType()
        t1.setIndexed(False)
        t1.setStored(True)
        t1.setTokenized(False)

        t2 = FieldType()
        t2.setIndexed(True)
        t2.setStored(True)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                # if not filename.endswith('.txt'):
                #     continue
                print "adding", filename
                try:
                    path = os.path.join(root, filename)
                    file = open(path)
                    url = file.readline()
                    url = url.split('\n')
                    url = url[0]

                    contents = unicode(file.read(), 'UTF-8')

                    soup = BeautifulSoup(contents, "html.parser")
                    tmp = soup.find('title')
                    if tmp:
                        title = tmp.get_text().encode("UTF-8")
                    else:
                        title = "None title"

                    print title


                    img_list=[]
                    for url in soup.findAll('img'):
                        x = url.get('src', '')
                        img_list.append(x)
                    use_list=[]
                    for t in img_list:
                        if t[-3:] == 'jpg':
                            use_list.append(t)

                    picture=' '.join(use_list)


                    # url_set = []
                    # url_set.append(url)
                    # for t in soup.findAll('a'):
                    #     x = t.get('href', '')
                    #     tmp = x.encode('utf8')
                    #     if tmp[-4:] != 'html':
                    #         continue
                    #     url_set.append(tmp)
                    # url_string=' '.join(url_set)

                    seg_list = jieba.cut(contents)
                    string = ' '.join(seg_list)
                    # string=list((seg_list))
                    # use=''
                    # for i in string:
                    #     use+=i
                    use_index = string.encode("UTF-8")
                    # print use_index
                    file.close()

                    doc = Document()
                    doc.add(Field("name", filename, t1))
                    doc.add(Field("path", path, t1))
                    doc.add(Field("url", url, t2))
                    doc.add(Field("picture", picture, t2))
                    # doc.add(Field("domain", url_string, t2))
                    if len(use_index) > 0:
                        doc.add(Field("contents", use_index, t2))
                    else:
                        doc.add(Field("contents", "None content", t2))
                        print "warning: no content in %s" % filename

                    # if len(title)>0:
                    doc.add(Field("titles", title, t2))
                    # else:
                    #     print "warning: no title in %s" % filename

                    writer.addDocument(doc)
                except Exception, e:
                    print "Failed in indexDocs:", e


if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        IndexFiles('html', "index")
        # IndexFiles('testfolder', "index")
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        raise e
