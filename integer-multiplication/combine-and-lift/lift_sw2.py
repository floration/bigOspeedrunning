exec(open('combo.py').read().split('if __name__')[0])
Ds=Q(710359,524288); M=2**20-1
GC2=Q(17158764376,2**42); GD2=Q(1039776,2**23)
def cuts(rs):
    c=[]
    for h in rs:
        mn=(250*(h+64)+248)//249
        c.append(max(mn,h+64+c[-1] if c else 0))
    return c
def ok(rs):
    c=cuts(rs); return all(c[i-1]+2<rs[i] for i in range(1,len(rs)))
def maxh2(h1):
    lo,hi=h1,M
    while hi-lo>1:
        m=(lo+hi)//2
        if ok((h1,m,M)): lo=m
        else: hi=m
    return lo
best=None
for h1 in range(8192,200000,512):
    h2=maxh2(h1); v=upper((h1,h2,M),Ds)
    if best is None or v>best[0]: best=(v,h1,h2)
for a in range(best[1]-600,best[1]+600):
    b=maxh2(a); w=upper((a,b,M),Ds)
    if w>best[0]: best=(w,a,b)
v,h1,h2=best; r=(h1,h2,M)
kap=Q(int((v-stop)*10**15),10**15); booked=kap+stop
lo,hi=1024,M
while hi-lo>1:
    m=(lo+hi)//2
    if GC2-GD2/m>booked: hi=m
    else: lo=m
G=hi
print(r,cuts(r),ok(r),'sup %.18f'%float(v-stop),'install',kap,float(kap),'G',G)
