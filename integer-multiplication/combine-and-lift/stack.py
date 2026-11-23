# Stack: floor retune (L=4474, s=186/25) + #8076 child tariff 2401/1024 + #8082 reserve drop (no 256/255) + Gaussian debit 1039017/2^23.
exec(open('combo.py').read().split('if __name__')[0])
GD=Q(1039017,2**23)
def posd(G): return GC-GD/G
f=F_upper(4474,Q(186,25),T76)*D(255)/D(256)
num=int(f.ln()/ln2*2**20)+1; assert allow_lower(num,2**20)>f; Ds=Q(num,2**20)
print('stacked ordinary debit',Ds,float(Ds*8192),'log2F*2^20=%.4f'%float(f.ln()/ln2*2**20), 'upper approx',f)
# as intended: cap 318292011, base 1740, G<=524288
cap=318292011; out=[]
for G in range(515000,524289):
    h2=(cap-1740-220*G)//320-8192-524288
    if not 8192<=h2<=524288: continue
    r=(8192,h2,524288); out.append((min(upper(r,Ds),posd(G))-stop,G,r,1740+320*sum(r)+220*G))
v,G,r,clk=max(out); print('as-intended sup %.18f'%float(v),G,r,clk,'install',Q(int(v*10**15),10**15),float(Q(int(v*10**15),10**15)))
# minimal ordinary at G=524288
booked=Q(int(v*10**15),10**15)+stop
lo,hi=8192,524288
while hi-lo>1:
    m=(lo+hi)//2
    if upper((8192,m,524288),Ds)>booked: hi=m
    else: lo=m
print(' minimal h2 at G=524288:',hi,'clock',1740+320*(8192+hi+524288)+220*524288, ' #8082 value .003898230327195 diff', float(Q(int(v*10**15),10**15)-Q('.003898230327195')))
# lifted 20-bit
G=2**20-1; sup=posd(G)-stop; kap=Q(int(sup*10**15),10**15); booked=kap+stop
best=None
for h3 in range(520000,1048576,250):
    lo,hi=8192,1048575
    if upper((8192,hi,h3),Ds)<=booked: continue
    while hi-lo>1:
        m=(lo+hi)//2
        if upper((8192,m,h3),Ds)>booked: hi=m
        else: lo=m
    if best is None or 8192+hi+h3<best[0]: best=(8192+hi+h3,hi,h3)
for d in range(-300,301):
    H3=best[2]+d
    if H3>1048575: continue
    lo,hi=8192,1048575
    if upper((8192,hi,H3),Ds)<=booked: continue
    while hi-lo>1:
        m=(lo+hi)//2
        if upper((8192,m,H3),Ds)>booked: hi=m
        else: lo=m
    if 8192+hi+H3<best[0]: best=(8192+hi+H3,hi,H3)
s,h2,h3=best
print('lifted install',kap,float(kap),'ordinary',(8192,h2,h3),'clock',1740+320*s+220*G,'vs 8078 %.3e'%float(kap-Q('.00389834')),'vs our lift %.3e'%float(kap-Q('.003898348448843')))
