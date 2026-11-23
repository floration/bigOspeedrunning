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
groups=defaultdict(list)
for i,(a,c) in enumerate(zip(w['initial'],w['final'])):
    if i not in main and a!=c: groups[(a,c)].append(i)
print('groups',sorted(((k,len(v)) for k,v in groups.items()),key=lambda t:-t[1])[:12])
src=defaultdict(list); dst=defaultdict(list); inp=defaultdict(list)
for k,(a,bb) in moves.items(): src[a].append(k); dst[bb].append(k)
for i,a in enumerate(w['initial']): inp[a].append(i)
res=[]
for (a,z),G in groups.items():
    G=sorted(G); Gs=set(G); nonG=[j for j in range(n) if j not in Gs]
    for c in range(len(fr)):
        if not (S[a]<S[c]<S[z]): continue
        K=src[c]
        if not K: continue
        B=np.array([b[k] for k in K])
        lam=nullspace(B[:,nonG].T)   # lam: combos of rows killing non-G outputs
        Psi=[mm(l,B[:,G]) for l in lam] if lam else []
        Psi=[p for p in Psi if p.any()]
        if not Psi: continue
        # read space: residents at c
        Rv=[val[k] for k in dst[c]]+[np.eye(n,dtype=np.int64)[i] for i in inp[c]]
        if not Rv: continue
        A=np.array(Rv)
        mu=nullspace(A[:,nonG].T)
        V=[mm(m,A[:,G]) for m in mu]; V=[v for v in V if v.any()]
        if not V: continue
        M=np.array([[int(mm(v,p)) for p in Psi] for v in V])
        ok=M.any()
        res.append(dict(a=a,z=z,c=c,rc=R[c],ga=R[z]-R[a],K=len(K),psi=len(Psi),V=len(V),pair=bool(ok)))
        if ok: print(res[-1],flush=True)
pickle.dump(res,open('/home/claude/work/scan.pkl','wb'))
print('done',len(res),sum(r['pair'] for r in res))
