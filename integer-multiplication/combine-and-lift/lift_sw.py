exec(open('combo.py').read().split('if __name__')[0])
Ds=Q(710359,524288); M=2**20-1
GC2=Q(17158764376,2**42); GD2=Q(1039776,2**23)
def f(h1,h2):
    return upper((h1,h2,M),Ds)
best=None
# coarse
for h1 in range(8192,200000,1024):
    h2=M-h1-165
    v=f(h1,h2)
    if best is None or v>best[0]: best=(v,h1,h2)
v,h1,h2=best
for a in range(h1-1100,h1+1100):
    if a<8192: continue
    b=M-a-165; w=f(a,b)
    if w>best[0]: best=(w,a,b)
v,h1,h2=best
kap=Q(int((v-stop)*10**15),10**15); booked=kap+stop
assert upper((h1,h2,M),Ds)>booked
# minimal G
lo,hi=1024,M
while hi-lo>1:
    m=(lo+hi)//2
    if GC2-GD2/m>booked: hi=m
    else: lo=m
G=hi
print('heights',(h1,h2,M),'sup %.18f'%float(v-stop),'install',kap,'G',G,'clock',1740+320*(h1+h2+M)+220*G)
print('controls h1-1',upper((h1-1,h2,M),Ds)>booked,'h1+1',upper((h1+1,h2-1,M),Ds)>booked, 'gauss G-1', GC2-GD2/(G-1)>booked)
print('vs #8086', float(kap-Q('.003898348449639')),'vs capped sw', float(kap-Q('.003898273237647')))
