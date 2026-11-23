import sys,pickle
sys.path.insert(0,'/home/claude/work/binary')
from bfix import *
p=sys.argv[1]; d=load(p); res,w,moves,val,pairs,main=check(d,verbose=False); madj0,_=adjoint(w); pub=w.pub
dep0,dlv0,out0=forward(d)
rows=pickle.load(open(p.split('/')[-1]+'.mergerank.pkl','rb'))
mvs={t:(f,a,b) for t,f,a,b,v in moves}; par=lambda x:bin(x).count('1')&1
for l,t1,t2,defi in rows[:3]+rows[300:302]:
    b1,b2=madj0[t1],madj0[t2]
    ov={t1:lambda dep,t1=t1,t2=t2:dep[t1]^dep0[t2], t2:lambda dep,t1=t1,t2=t2:dep0[t1]^dep[t2]}
    dp,dl,out=forward(d,over_deliver=ov)
    rk,ker=gf2_rank_kernel(out,pub); k=ker[0]; _,lk=gf2_rank_kernel(transpose(out,pub),pub); ell=lk[0]
    madjC=adjoint_ov(d,{t1:b1^b2,t2:b1^b2}); madjC[t1]=b1^b2
    U=set(d['start'][i] for i in range(pub) if k>>i&1); B=set(d['final'][j] for j in range(pub) if ell>>j&1)
    for t,(f,a,b) in mvs.items():
        if t==t2: continue
        if par(dl[t]&k): U.add(b)
        if par(madjC[t]&ell): B.add(a)
    sup=lambda m:[i for i in range(pub) if m>>i&1]
    print(l,t1,t2,'k',sup(k)[:6],'ell',sup(ell)[:6],'U charts',sorted(U)[:10],len(U),'B charts',sorted(B)[:10],len(B))
    # control: in the ORIGINAL circuit, info of k reaching b via t1/t2
    print('   orig: k seen by s1,s2', par(dep0[t1]&k), par(dep0[t2]&k), ' ell sees b1,b2', par(b1&ell), par(b2&ell))
