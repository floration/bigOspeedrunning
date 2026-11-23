# Necessary condition for a single closure after a same-link merge: some chart c with a resident form u (in the
# merged circuit C') with u.k=1 and a leaving adjoint b (C') with ell.b=1, where k / ell span the right / left
# kernels of the merged map. Then exact test of each hit (resident combo added into leaving rows, block check).
import sys,pickle
sys.path.insert(0,'/home/claude/work/binary')
from bfix import *
p=sys.argv[1]; d=load(p); res,w,moves,val,pairs,main=check(d,verbose=False); madj0,_=adjoint(w); pub=w.pub
X=[i for i in range(pub) if d['start'][i]!=0]; mX=sum(1<<i for i in X); m0=((1<<pub)-1)&~mX; Xs=set(X)
dep0,dlv0,out0=forward(d)
rows=pickle.load(open(p.split('/')[-1]+'.mergerank.pkl','rb'))
mvs={t:(f,a,b) for t,f,a,b,v in moves}
par=lambda x:bin(x).count('1')&1
stat=Counter(); hits=[]
for l,t1,t2,defi in rows:
    b1,b2=madj0[t1],madj0[t2]
    ov={t1:lambda dep,t1=t1,t2=t2:dep[t1]^dep0[t2], t2:lambda dep,t1=t1,t2=t2:dep0[t1]^dep[t2]}
    dp,dl,out=forward(d,over_deliver=ov)
    rk,ker=gf2_rank_kernel(out,pub); k=ker[0]; _,lk=gf2_rank_kernel(transpose(out,pub),pub); ell=lk[0]
    madjC=adjoint_ov(d,{t1:b1^b2,t2:b1^b2})
    madjC[t1]=b1^b2   # the merged transfer's adjoint
    resU=defaultdict(bool); resB=defaultdict(bool)
    for i in range(pub):
        if k>>i&1: resU[d['start'][i]]=True
    for t,(f,a,b) in mvs.items():
        if t==t2: continue
        if par(dl[t]&k): resU[b]=True
        if par(madjC[t]&ell): resB[a]=True
    for j in range(pub):
        if ell>>j&1: resB[d['final'][j]]=True
    cs=[c for c in w.S if resU[c] and resB[c]]
    stat[len(cs)>0]+=1
    if cs: hits.append((l,t1,t2,cs))
print(p,'merges',len(rows),'with a rank-restoring chart (necessary cond.)',dict(stat))
print(Counter(len(h[3]) for h in hits).most_common(10))
print(Counter(c for h in hits for c in h[3]).most_common(10))
pickle.dump(hits,open(p.split('/')[-1]+'.close.pkl','wb'))
