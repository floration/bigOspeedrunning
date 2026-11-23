import sys,pickle; sys.path.insert(0,'/home/claude/work/lf'); sys.path.insert(0,'/home/claude/work')
from lf_build import *
from collections import Counter
d=pickle.load(open('/home/claude/work/lf/cands.pkl','rb')); pairs=d['pairs']
w=W0; val0=forward(w); b0=adjoint(w); m0={k:(a,bb) for k,a,bb in w['moves']}
EYE=np.eye(n,dtype=np.int64)
fcache={}
out=[]; st=Counter()
Js={}
for i,cs in d['hit'].items():
    l,g,v1,v2=pairs[i]
    if v1 not in Js: Js[v1]=sens(w,{v1:1})
    if v2 not in Js: Js[v2]=sens(w,{v2:1})
    for c in cs:
        res=[k for k,(a,bb) in m0.items() if bb==c]+[~j for j in range(n) if w['initial'][j]==c]
        rows=[k for k,(a,bb) in m0.items() if a==c]+[first+j for j in range(n) if w['final'][j]==c]
        mu=solve_left(np.array([val0[k] if k>=0 else EYE[~k] for k in res]),val0[v1])
        lam=solve_left(np.array([b0[k] for k in rows]),b0[v2])
        muq={res[j]:int(x) for j,x in enumerate(mu) if x}; lamq={rows[j]:int(x) for j,x in enumerate(lam) if x}
        p1=sum(q*Js[v1].get(k,0) for k,q in muq.items() if k>=0)%P; p2=sum(q*Js[v2].get(k,0) for k,q in muq.items() if k>=0)%P
        Jl=sens(w,lamq); q1=Jl.get(v1,0); q2=Jl.get(v2,0)
        rec=(l,g,v1,v2,c,ratrec(p1),ratrec(p2),ratrec(q1),ratrec(q2))
        out.append(rec); st[(rec[5],rec[6],rec[7],rec[8])]+=1
for k,v in st.most_common(): print(k,v)
pickle.dump(out,open('/home/claude/work/lf/screen.pkl','wb'))
