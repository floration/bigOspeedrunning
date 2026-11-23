exec(open('four25.py').read().split('best=(0,)')[0])
best=(0,)
def ev(h1,h2):
    if not ok([h1,h2]): return Q(0),None
    h3=maxnext([h1,h2],TOP); return up((h1,h2,h3,TOP)),h3
c1,c2=131072,1966080
for step in (65536,16384,4096,1024,256,64,16,4,1):
    improved=True
    while improved:
        improved=False
        for a in (-step,0,step):
            for b in (-4*step,-step,0,step,4*step):
                v,h3=ev(c1+a,c2+b)
                if h3 and v>best[0]: best=(v,c1+a,c2+b,h3); improved=(a,b)!=(0,0)
        c1,c2=best[1],best[2]
print(best[0], float(best[0]), best[1:])
