import sys,random
sys.path.insert(0,'/home/claude/work/binary')
from bscan import *
# unit test sub_in vs brute force
random.seed(1)
for _ in range(300):
    n=8; vs=[random.getrandbits(n) for _ in range(random.randint(1,6))]; m=random.getrandbits(n)
    sp=span(vs); want=rank([v for v in sp if v&~m==0]); got=len(sub_in(vs,m))
    assert want==got and all(v in sp and v&~m==0 for v in sub_in(vs,m)),(vs,m)
print('sub_in ok')
d=load(sys.argv[1])
res,w,moves,val,pairs,main=check(d,verbose=False)
madj,inadj=adjoint(w); pub=w.pub
groups=defaultdict(list)
for i in range(pub):
    if i not in main and d['start'][i]!=d['final'][i]: groups[(d['start'][i],d['final'][i])].append(i)
inp=defaultdict(list); arr=defaultdict(list); dep=defaultdict(list)
for i in range(pub): inp[d['start'][i]].append(1<<i)
for t,f,a,b,v in moves: arr[b].append(v); dep[a].append(madj[t])
mainm=sum(1<<i for i in main)
for (a,z),G in sorted(groups.items(),key=lambda t:-len(t[1])):
    mG=sum(1<<i for i in G); nW=nU=nc=0; wdim=udim=0
    for c in w.S:
        if not (w.S[a]<w.S[c]<w.S[z]): continue
        nc+=1
        U=sub_in(dep[c],mG) if dep[c] else []
        W=sub_in(inp[c]+arr[c],mG) if (inp[c] or arr[c]) else []
        nW+=bool(W); nU+=bool(U); wdim+=len(W); udim+=len(U)
    print((a,z),w.D[a],w.D[z],'|G|',len(G),'inner charts',nc,'charts with W',nW,'dimW',wdim,'charts with U',nU,'dimU',udim)
# what do helper-carrying moves look like
hm=sum(1<<i for i in range(pub) if i not in main)
c=Counter()
for t,f,a,b,v in moves:
    c[(bool(v&hm),bool(v&mainm), bool(madj[t]&hm), bool(madj[t]&mainm))]+=1
print('moves by (val has helper, val has main, adj has helper, adj has main):',c)
