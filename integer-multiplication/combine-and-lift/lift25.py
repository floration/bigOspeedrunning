# Gamed: five-shortcut word + stacked ordinary side + 25-bit heights (#8081/#8087 setup) + eta 1/256 (#8084).
exec(open('combo.py').read().split('if __name__')[0])
ETA=Q(1,256); Ds=Q(710359,524288); M=2**25-1
GC2=Q(17158764376,2**42); GD2=Q(1039776,2**23)
def up(rs):
    rate=Q(0)
    for i,h in enumerate(rs,1):
        rate=min(ETA,(249*(cB-Ds/h)+rate)/250)
        if i<len(rs): rate=Q((rate*10**21).__floor__()-1,10**21)
    return rate
def cuts(rs):
    c=[]
    for h in rs:
        mn=(250*(h+64)+248)//249; c.append(max(mn,h+64+c[-1] if c else 0))
    return c
def maxh2(h1):
    lo,hi=h1,M
    while hi-lo>1:
        m=(lo+hi)//2; c=cuts((h1,m,M))
        if c[0]+2<m and c[1]+2<M: lo=m
        else: hi=m
    return lo
best=max((up((h1,maxh2(h1),M)),h1) for h1 in range(8192,8000000,8192))
c=best[1]
for step in (1024,64,1):
    best=max((up((h1,maxh2(h1),M)),h1) for h1 in range(max(8192,c-20*step),c+20*step,step)); c=best[1]
v,h1=best; h2=maxh2(h1); r=(h1,h2,M)
kap=Q(int((v-stop)*10**15),10**15); booked=kap+stop
lo,hi=1024,M
while hi-lo>1:
    m=(lo+hi)//2
    if GC2-GD2/m>booked: hi=m
    else: lo=m
print(r,cuts(r),'sup %.18f'%float(v-stop),'install',kap,float(kap),'G',hi,'unclamped stages <eta:',[float(x) for x in (up(r[:1]),up(r[:2]))])
print('vs current', float(kap-Q('.003899574328473')), 'vs 8087', float(kap-Q('.003898460000505')))
