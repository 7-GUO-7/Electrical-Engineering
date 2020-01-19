
def union_bfs(a,b):
    len_b=len(b)
    for i in range(len_b):
        if not b[len_b-i-1] in a:
            a.insert(i,b[len_b-i-1])

a = [1, 2, 3]
b = [2, 4, 4, 5]
union_bfs(a, b)
print a, b
    # tmp=[]

    # for i in a:
    #     if not i in tmp:
    #         tmp.append(i)
    # len_a = len(a)
    # for i in range(0,len_a):
    #     if not a[len_a-i-1] in tmp:
    #         tmp.append(a[len_a-i-1])
    # del a[:]
    # for i in tmp:
    #     a.append(i)
