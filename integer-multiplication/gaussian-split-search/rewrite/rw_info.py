import pickle,json,numpy as np,sys
from collections import defaultdict,Counter
sys.path.insert(0,'/home/claude/work')
from lin import *
from chk import expected,span
ws=pickle.load(open('/home/claude/work/words.pkl','rb')); w=ws['final']
n=len(w['initial']); first=w['first_output']
fr=w['frames']; S=[span(f) for f in fr]; R=[len(f) for f in fr]
E,main=expected(n)
moves={k:(a,b) for k,a,b in w['moves']}
val=forward(w); b=adjoint(w)
pos={k:i for i,k in enumerate(w['schedule'])}
groups=defaultdict(list)
for i,(a,c) in enumerate(zip(w['initial'],w['final'])):
    if i not in main and a!=c: groups[(a,c)].append(i)
src=defaultdict(list); dst=defaultdict(list); inp=defaultdict(list)
for k,(a,bb) in moves.items(): src[a].append(k); dst[bb].append(k)
for i,a in enumerate(w['initial']): inp[a].append(i)
for (a,z),G in groups.items():
    G=sorted(G); Gs=set(G); nonG=[j for j in range(n) if j not in Gs]
    for c in range(len(fr)):
        if not (S[a]<S[c]<S[z]): continue
        K=src[c]
        if not K: continue
        B=np.array([b[k] for k in K])
        lam=nullspace(B[:,nonG].T)
        Psi=[(l,mm(l,B[:,G])) for l in lam]; Psi=[p for p in Psi if p[1].any()]
        if not Psi: continue
        keys=dst[c]+[~i for i in inp[c]]
        Rv=[val[k] for k in dst[c]]+[np.eye(n,dtype=np.int64)[i] for i in inp[c]]
        if not Rv: continue
        A=np.array(Rv)
        mu=nullspace(A[:,nonG].T)
        V=[(m,mm(m,A[:,G])) for m in mu]; V=[v for v in V if v.any()] if False else [v for v in V if v[1].any()]
        if not V: continue
        print('G',(a,z),len(G),'c',c,'rank',R[c])
        for m,v in V:
            sup=[G[i] for i in np.nonzero(v)[0]]
            used=[keys[i] for i in np.nonzero(m)[0]]
            print('  s sup',sup[:8],len(sup),'from',[(k if k<0 else (k,moves[k])) for k in used][:6], 'times',[pos.get(k) for k in used if k>=0][:6])
        for l,p in Psi:
            sup=[G[i] for i in np.nonzero(p)[0]]
            used=[K[i] for i in np.nonzero(l)[0]]
            print('  h sup',sup[:8],len(sup),'rows',[(k,moves[k]) for k in used][:6],'times',[pos[k] for k in used][:6])
