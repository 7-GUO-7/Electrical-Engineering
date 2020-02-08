#!/usr/bin/env python
import jieba
INDEX_DIR = "IndexFiles.index"
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')
import sys, os, lucene

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause

"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
def run(searcher, analyzer):
    while True:
        print "Please choose which information you want to search"
        print "1 for pictures, 2 for texts"
        choice=input()
        if choice==2:
            print
            print "Hit enter with no input to quit."
            command = raw_input("Query:")
            command = unicode(command, 'UTF-8')

            if command == '':
                return

            print "Searching for:", command
            print '\n'
            command_list=command.split(' ')
            command=''
            for i in command_list:
                if ":" in i:
                    length=len(i.split(':'))
                    if length==2:
                        site_command,value=i.split(':')[:2]
                    if length == 3:
                        site_command, value1, value2 = i.split(':')[:3]
                        value = value1 + ':'+ value2
                    break

                else:
                    value=unicode('https',"UTF-8") # if the custom did not enter site
            command=command_list[0]+command
            #print command,' ',site_command,' ',value


            command = jieba.cut(command)
            # string=''
            # for i in command:
            #     string+=i
            string=' '.join(command)
            use=string.encode('UTF-8')

            # query = QueryParser(Version.LUCENE_CURRENT, "url",
            #                     analyzer).parse(value)
            # scoreDocs = searcher.search(query,1).scoreDocs
            # print "%s total matching documents." % len(scoreDocs)

            # for i, scoreDoc in enumerate(scoreDocs):
            #     doc = searcher.doc(scoreDoc.doc)
            #     # print 'path:', doc.get("path")
            #     # print 'name:', doc.get("name")
            #     # print 'title:', (doc.get("titles")).decode("UTF-8")
            #     # print 'score:', scoreDoc.score
            #     # print 'url:', doc.get("url")
            #     # print 'domain:',doc.get("domain")
            #     # print '\n'
            #     domain=doc.get("domain")
            #     domain=domain.split(' ')
            #     print domain
            #     # print 'content: ', (doc.get("contents")).decode("UTF-8")
            #     # print 'explain:', searcher.explain(query, scoreDoc.doc)

            querys = BooleanQuery()

            query1 = QueryParser(Version.LUCENE_CURRENT, "contents",
                                    analyzer).parse(use)
            querys.add(query1, BooleanClause.Occur.MUST)
            query2 = QueryParser(Version.LUCENE_CURRENT, "url",
                                 analyzer).parse(value)
            querys.add(query2, BooleanClause.Occur.MUST)
            scoreDocs = searcher.search(querys,10).scoreDocs
            print "%s total matching documents." % len(scoreDocs)
            for i, scoreDoc in enumerate(scoreDocs):
                doc = searcher.doc(scoreDoc.doc)
                print 'path:', doc.get("path")
                # print 'name:', doc.get("name")
                print 'title:', (doc.get("titles")).decode("UTF-8")
                print 'score:', scoreDoc.score
                print 'url:', doc.get("url")
                # print 'domain:',doc.get("domain")
                print '\n'


        if choice==1:
            print
            print "Hit enter with no input to quit."
            command = raw_input("Query:")
            command = unicode(command, 'UTF-8')

            if command == '':
                return

            print "Searching for:", command
            print '\n'
            command_list = command.split(' ')
            command = ''
            for i in command_list:
                if ":" in i:
                    length = len(i.split(':'))
                    if length == 2:
                        site_command, value = i.split(':')[:2]
                    if length == 3:
                        site_command, value1, value2 = i.split(':')[:3]
                        value = value1 + ':' + value2
                    break

                else:
                    value = unicode('https', "UTF-8")  # if the custom did not enter site
            command = command_list[0] + command
            # print command,' ',site_command,' ',value

            command = jieba.cut(command)
            # string=''
            # for i in command:
            #     string+=i
            string = ' '.join(command)
            use = string.encode('UTF-8')

            # query = QueryParser(Version.LUCENE_CURRENT, "url",
            #                     analyzer).parse(value)
            # scoreDocs = searcher.search(query,1).scoreDocs
            # print "%s total matching documents." % len(scoreDocs)

            # for i, scoreDoc in enumerate(scoreDocs):
            #     doc = searcher.doc(scoreDoc.doc)
            #     # print 'path:', doc.get("path")
            #     # print 'name:', doc.get("name")
            #     # print 'title:', (doc.get("titles")).decode("UTF-8")
            #     # print 'score:', scoreDoc.score
            #     # print 'url:', doc.get("url")
            #     # print 'domain:',doc.get("domain")
            #     # print '\n'
            #     domain=doc.get("domain")
            #     domain=domain.split(' ')
            #     print domain
            #     # print 'content: ', (doc.get("contents")).decode("UTF-8")
            #     # print 'explain:', searcher.explain(query, scoreDoc.doc)

            querys = BooleanQuery()

            query1 = QueryParser(Version.LUCENE_CURRENT, "titles",
                                 analyzer).parse(use)
            querys.add(query1, BooleanClause.Occur.MUST)
            query2 = QueryParser(Version.LUCENE_CURRENT, "url",
                                 analyzer).parse(value)
            querys.add(query2, BooleanClause.Occur.MUST)
            query3 = QueryParser(Version.LUCENE_CURRENT, "picture_flag",
                                 analyzer).parse('1')
            querys.add(query3, BooleanClause.Occur.MUST)
            scoreDocs = searcher.search(querys, 10).scoreDocs
            print "%s total matching documents." % len(scoreDocs)
            for i, scoreDoc in enumerate(scoreDocs):
                doc = searcher.doc(scoreDoc.doc)
                print 'path:', doc.get("path")
                # print 'name:', doc.get("name")
                print 'title:', (doc.get("titles")).decode("UTF-8")
                print 'score:', scoreDoc.score
                print 'url:', doc.get("url")
                print 'picture:'
                picture_print=doc.get("picture")
                # print type(picture_print)
                if picture_print.decode("UTF-8")=="No picture":
                    print picture_print
                else:
                    picture_print=picture_print.split(' ')
                    for i in picture_print:
                        print i



                # print 'domain:',doc.get("domain")
                print '\n'




if __name__ == '__main__':
    STORE_DIR = "index"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    del searcher