import web
# render = web.template.render('template_new')

import jieba
import re
from web import form
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')
import urllib2
import os
from bs4 import BeautifulSoup
import lucene

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause

def run(searcher, analyzer,command):
    if command == '':
        return

    # print "Searching for:", command
    # print '\n'
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
            # command=command+command_list[i]
            value=unicode('https',"UTF-8") # if the custom did not enter site
    command=command_list[0]+command
    #print command,' ',site_command,' ',value


    command = jieba.cut(command)
    string=' '.join(command)

    key_word1=string.split(' ')[0]

    use=string.encode('UTF-8')


    querys = BooleanQuery()

    query1 = QueryParser(Version.LUCENE_CURRENT, "contents",
                            analyzer).parse(use)
    querys.add(query1, BooleanClause.Occur.MUST)
    query2 = QueryParser(Version.LUCENE_CURRENT, "url",
                         analyzer).parse(value)
    querys.add(query2, BooleanClause.Occur.MUST)
    scoreDocs = searcher.search(querys,10).scoreDocs
    # print "%s total matching documents." % len(scoreDocs)
    answer_all=[]
    for i, scoreDoc in enumerate(scoreDocs):
        tmp={}
        doc = searcher.doc(scoreDoc.doc)

        # print 'path:', doc.get("path")
        tmp['path']=(doc.get("path"))
        # #print 'name:', doc.get("name")
        tmp['name']=(doc.get("name"))
        # print 'title:',
        tmp['titles']=((doc.get("titles")))
        # return (doc.get("titles")).decode("UTF-8")
        # print 'score:', scoreDoc.score
        tmp['url']=doc.get("url")


        # key_word=use.decode('UTF-8')
        key_word = key_word1

        contents=doc.get("original_web")
        # print contents

        # url_to_open=tmp['url']
        # content = urllib2.urlopen(url_to_open).read()
        # print content
        soup = BeautifulSoup(contents, "html.parser")
        text = soup.findAll(text=re.compile(key_word))
        # print key_word
        # print type(key_word)
        # print text
        text_list = []
        for i in text:
            # print i
            text_final = ''
            for letter in i:
                if letter != ' ' and letter != '\n':
                    text_final += letter
            # print text_final
            text_list.append(text_final)
        # pattern=re.compile(".{0,10}%s.{0,10} "%key_word)
        # final=pattern.findall(text_list[0])
        # text_string = '...'.join(text_list)
        length=len(text_list)
        if length<=3:
            text_string='...'.join(text_list)
        else:
            text_string=text_list[0]+"..."+text_list[1]+'...'+text_list[2]+'...'
        if len(text_string)>100:
            text_string=text_string[0:100]+'...'
        if len(text_string)==0:
            text_string='...'

        # if text_list[0]:
        #     text_sring=text_list[0]+'...'
        #     if text_list[1]:
        #         text_string=text_string+text_list[1]+'...'
        #         if text_final[2]:
        #             text_string = text_string + text_list[2] + '...'
        # else:
        #     text_string=''


        # print text_string
        tmp['relative_content'] = text_string
        # print final
        # tmp['abstract']=text_list[0]


        # print 'url:', doc.get("url")

        # #print 'domain:',doc.get("domain")
        # print '\n'
        answer_all.append(tmp)
    return [use,answer_all]


def run2(searcher, analyzer, command):
    if command == '':
        return

    # print "Searching for:", command
    # print '\n'
    command_list=command.split(' ')
    command=''
    for i in command_list:
        if ":" in i:
            length = len(i.split(':'))
            if length == 2:
                site_command,value=i.split(':')[:2]
            if length == 3:
                site_command, value1, value2 = i.split(':')[:3]
                value = value1 + ':'+ value2
            break

        else:
            # command=command+command_list[i]
            value=unicode('https',"UTF-8") # if the custom did not enter site
    command=command_list[0]+command
    #print command,' ',site_command,' ',value


    command = jieba.cut(command)
    string=' '.join(command)

    key_word1=string.split(' ')[0]

    use=string.encode('UTF-8')

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
    # print "%s total matching documents." % len(scoreDocs)
    answer_all=[]
    for i, scoreDoc in enumerate(scoreDocs):
        tmp={}
        doc = searcher.doc(scoreDoc.doc)

        # print 'path:', doc.get("path")
        tmp['path']=(doc.get("path"))
        # #print 'name:', doc.get("name")
        tmp['name']=(doc.get("name"))
        # print 'title:',
        tmp['titles']=((doc.get("titles")))
        # return (doc.get("titles")).decode("UTF-8")
        # print 'score:', scoreDoc.score
        tmp['url']=doc.get("url")


        # key_word=use.decode('UTF-8')
        key_word = key_word1

        contents=doc.get("original_web")
        # print contents

        # url_to_open=tmp['url']
        # content = urllib2.urlopen(url_to_open).read()
        # print content
        soup = BeautifulSoup(contents, "html.parser")
        text = soup.findAll(text=re.compile(key_word))
        # print key_word
        # print type(key_word)
        # print text
        text_list = []
        for i in text:
            # print i
            text_final = ''
            for letter in i:
                if letter != ' ' and letter != '\n':
                    text_final += letter
            # print text_final
            text_list.append(text_final)
        # pattern=re.compile(".{0,10}%s.{0,10} "%key_word)
        # final=pattern.findall(text_list[0])
        # text_string = '...'.join(text_list)
        length=len(text_list)
        if length<=3:
            text_string='...'.join(text_list)
        else:
            text_string=text_list[0]+"..."+text_list[1]+'...'+text_list[2]+'...'
        if len(text_string)>100:
            text_string=text_string[0:100]+'...'
        if len(text_string)==0:
            text_string='...'

        # if text_list[0]:
        #     text_sring=text_list[0]+'...'
        #     if text_list[1]:
        #         text_string=text_string+text_list[1]+'...'
        #         if text_final[2]:
        #             text_string = text_string + text_list[2] + '...'
        # else:
        #     text_string=''


        # print text_string
        tmp['relative_content'] = text_string

        picture_print = doc.get("picture")
        picture_list=[]
        if picture_print.decode("UTF-8")=="No picture":
            {}
        else:
            picture_print = picture_print.split(' ')
            for i in picture_print:
                picture_list.append(i)
        tmp['picture'] = picture_list
        # print final
        # print '\n'
        # tmp['abstract']=text_list[0]


        # print 'url:', doc.get("url")

        # #print 'domain:',doc.get("domain")
        # print '\n'
        answer_all.append(tmp)
    return [use,answer_all]





def func(command):

    STORE_DIR = "index"
    # global count1
    # if count1==0:
    # lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    global init
    init.attachCurrentThread()
        # count1+=1
    # print 'lucene', lucene.VERSION
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    answer=run(searcher, analyzer,command)
    del searcher
    # print answer[0]
    # print answer[1]
    return answer
    # command = unicode(command, 'UTF-8')

    # if command == '':
    #     return
    #
    # command_list = command.split(' ')
    # command = ''
    #
    # for i in command_list:
    #     if ":" in i:
    #         length = len(i.split(':'))
    #         if length == 2:
    #             site_command, value = i.split(':')[:2]
    #         if length == 3:
    #             site_command, value1, value2 = i.split(':')[:3]
    #             value = value1 + ':' + value2
    #         break
    #
    #     else:
    #         value = unicode('https', "UTF-8")  # if the custom did not enter site
    # command = command_list[0] + command
    # # print command,' ',site_command,' ',value
    #
    # command = jieba.cut(command)
    #
    # string = ' '.join(command)
    # use = string.encode('UTF-8')
    # querys = BooleanQuery()
    #
    # query1 = QueryParser(Version.LUCENE_CURRENT, "contents",
    #                      analyzer).parse(use)
    # querys.add(query1, BooleanClause.Occur.MUST)
    # query2 = QueryParser(Version.LUCENE_CURRENT, "url",
    #                      analyzer).parse(value)
    # querys.add(query2, BooleanClause.Occur.MUST)
    # scoreDocs = searcher.search(querys, 10).scoreDocs
    # print "%s total matching documents." % len(scoreDocs)
    # for i, scoreDoc in enumerate(scoreDocs):
    #     doc = searcher.doc(scoreDoc.doc)
    #     print 'path:', doc.get("path")
    #     # print 'name:', doc.get("name")
    #     print 'title:', (doc.get("titles")).decode("UTF-8")
    #     print 'score:', scoreDoc.score
    #     print 'url:', doc.get("url")
    #     # print 'domain:',doc.get("domain")
    #     print '\n'
    #
    # return use



def func2(command):

    STORE_DIR = "index"
    # global count1
    # if count1==0:
    # lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    global init
    init.attachCurrentThread()
        # count1+=1
    # print 'lucene', lucene.VERSION
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    answer=run2(searcher, analyzer,command)
    del searcher
    # print answer[0]
    # print answer[1]
    return answer


urls = (
    '/' , 'first_page',
    '/text_home', 'text_home',
    '/text_search', 'text_search',
    '/image_home', 'image_home',
    '/image_search', 'image_search'
)
# urls=( '/(.*)', 'index')


# render = web.template.render('templates') # your templates
render = web.template.render('templates',cache=False)

login1=form.Form(
    form.Textbox('Search_For_Text'),
    # form.Password('password'),
    form.Button('GO'),
)

login2=form.Form(
    form.Textbox('Search_For_Picture'),
    # form.Password('password'),
    form.Button('GO'),
)
# login = form.Form(
#     form.Textbox('keyword'),
#     form.Button('Search'),
# )


# def func(command):
#     return 'Your input is '+command

class first_page:
    def GET(self):
        # name=login()
        x=[] #useless
        return render.first_page_1(x)
         # render.index(name)




class text_home:
    def GET(self):

        f = login1()
        # name=login()
        return render.formtest(f)
         # render.index(name)

class image_home:
    def GET(self):

        f = login2()
        # name=login()
        return render.formtest2(f)
         # render.index(name)

class text_search:
    def GET(self):
        t = login1()
        user_data = web.input()
        answer = func(user_data.Search_For_Text)
        # a = func(user_data.keyword)
        return render.result_text(t,answer)


class image_search:
    def GET(self):
        t = login2()
        user_data = web.input()
        answer = func2(user_data.Search_For_Picture)
        # a = func(user_data.keyword)
        return render.result_picture(t,answer)


if __name__ == "__main__":

    init=lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    app = web.application(urls, globals(),False)
    app.run()
