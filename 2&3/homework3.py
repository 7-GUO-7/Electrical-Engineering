def get_page(page):
    return g.get(page, [])

def get_all_links(content):
    return content

def union_dfs(a,b):
    for e in b:
        if e not in a:
            a.append(e)

def union_bfs(a,b):
    len_b=len(b)
    for i in range(len_b):
        if not b[len_b-i-1] in a:
            a.insert(i,b[len_b-i-1])

def crawl(seed, method):
    tocrawl = [seed]
    crawled = []
    graph = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            outlinks = get_all_links(content)
            globals()['union_%s' % method](tocrawl, outlinks)
            # use the union function (above) with the name :method
            graph[page]=content
            crawled.append(page)
    return graph, crawled

g = {'A':['B', 'C', 'D'],\
     'B':['E', 'F'],\
     'D':['G', 'H'],\
     'E':['I', 'J'],\
     'G':['K', 'L']}


graph_dfs, crawled_dfs = crawl('A', 'dfs')
print 'graph_dfs:', graph_dfs
print 'crawled_dfs:', crawled_dfs

graph_bfs, crawled_bfs = crawl('A', 'bfs')
print 'graph_bfs:', graph_bfs
print 'crawled_bfs:', crawled_bfs