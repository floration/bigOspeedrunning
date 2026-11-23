# Gamed: lift the recurring clock cap, keep every height within 20 bits (the source setup census guard).
exec(open('combo.py').read().split('if __name__')[0])
Dc=Q(1426639,2**20); BASE=1740
G=2**20-1
sup=pos(G)-stop; kap=Q(int(sup*10**15),10**15); booked=kap+stop
print('gauss sup %.18f'%float(sup),'install',kap, float(kap))
# minimal ordinary sum funding booked: for each h3, smallest h2
best=None
for h3 in range(530000,1048576,500):
    lo,hi=8192,1048575
    if upper((8192,hi,h3),Dc)<=booked: continue
    while hi-lo>1:
        m=(lo+hi)//2
        if upper((8192,m,h3),Dc)>booked: hi=m
        else: lo=m
    s=8192+hi+h3
    if best is None or s<best[0]: best=(s,hi,h3)
s,h2,h3=best
# refine around h3
for d in range(-600,601):
    H3=h3+d
    if H3>1048575: continue
    lo,hi=8192,1048575
    if upper((8192,hi,H3),Dc)<=booked: continue
    while hi-lo>1:
        m=(lo+hi)//2
        if upper((8192,m,H3),Dc)>booked: hi=m
        else: lo=m
    if 8192+hi+H3<best[0]: best=(8192+hi+H3,hi,H3)
s,h2,h3=best; r=(8192,h2,h3)
print('ordinary',r,'sum',s,'ord rate %.18f'%float(upper(r,Dc)),'clock',BASE+320*s+220*G)
print('controls: G-1', pos(G-1)>booked, ' h2-1', upper((8192,h2-1,h3),Dc)>booked, ' h3-1', upper((8192,h2,h3-1),Dc)>booked)
print('gain over #8078 .00389834:', float(kap-Q('.00389834')), ' over combined .003898228176674:', float(kap-Q('.003898228176674')))
for bits in (21,22,24,30):
    Gb=2**bits-1; print(bits,'bit limit gauss %.13f'%float(pos(Gb)-stop))
