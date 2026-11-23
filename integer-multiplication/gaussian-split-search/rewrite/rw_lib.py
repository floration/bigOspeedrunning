import pickle,json,numpy as np,sys,random
from fractions import Fraction
from collections import defaultdict
from graphlib import TopologicalSorter
sys.path.insert(0,'/home/claude/work')
from lin import *
from chk import expected,span,check
def root(T,P,lo=0.0,hi=0.02):
    f=lambda c:sum(n*r**(1-c) for r,n in T.items())-sum(n*r**(1-c) for r,n in P.items())
    for _ in range(200):
        m=(lo+hi)/2
        if f(m)>0: lo=m
        else: hi=m
    return (lo+hi)/2
def kappa(r): return root({int(k):v for k,v in r['tg'].items()},{int(k):v for k,v in r['paid'].items()})
_main=None
def scan(w,classes=None,want_vectors=False):
    """return list of (a,z,c,pairing-matrix nonzero, V,Psi data)"""
    n=len(w['initial']); fr=w['frames']; S=[span(f) for f in fr]
    E,main=expected(n)
    moves={k:(a,b) for k,a,b in w['moves']}
    val=forward(w); b=adjoint(w)
    groups=defaultdict(list)
    for i,(a,c) in enumerate(zip(w['initial'],w['final'])):
        if i not in main and a!=c: groups[(a,c)].append(i)
    src=defaultdict(list); dst=defaultdict(list); inp=defaultdict(list)
    for k,(a,bb) in moves.items(): src[a].append(k); dst[bb].append(k)
    for i,a in enumerate(w['initial']): inp[a].append(i)
    out=[]
    for (a,z),G in groups.items():
        if classes and (a,z) not in classes: continue
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
            V=[(m,mm(m,A[:,G])) for m in mu]; V=[v for v in V if v[1].any()]
            if not V: continue
            M=np.array([[int(mm(v,p)) for _,p in Psi] for _,v in V])
            rec=dict(a=a,z=z,c=c,pair=bool(M.any()),nV=len(V),nPsi=len(Psi))
            if want_vectors:
                rec.update(G=G,V=[({keys[i]:int(m[i]) for i in np.nonzero(m)[0]},{G[i]:int(v[i]) for i in np.nonzero(v)[0]}) for m,v in V],
                           Psi=[({K[i]:int(l[i]) for i in np.nonzero(l)[0]},{G[i]:int(p[i]) for i in np.nonzero(p)[0]}) for l,p in Psi],M=M)
            out.append(rec)
    return out
def ancestors(w,keys):
    forms=dict(w['forms']); seen=set(); st=[k for k in keys if k>=0]
    while st:
        k=st.pop()
        if k in seen: continue
        seen.add(k); st.extend(d for d,_ in forms[k] if d>=0)
    return seen
def cross_edit(w,mu,lam,s,h,delta):
    """rows lam[k] += delta*lam_k*sum mu_d d ; outputs j -= delta*h_j*sum_i s_i out_i.  all coefficients mod p (ints).
    returns word with forms as mod-p ints-as-strings (rationals reconstructed later) -> we keep Fraction via modp ints."""
    first=w['first_output']
    forms={k:{d:Fraction(q) for d,q in r} for k,r in w['forms']}
    anc=ancestors(w,list(mu))
    assert not (set(lam)&anc),'cycle'
    for k,lk in lam.items():
        for d,md in mu.items():
            forms[k][d]=forms[k].get(d,0)+delta*lk*md
    outs={j:dict(forms[first+j]) for j in s}
    for j,hj in h.items():
        row=forms[first+j]
        for i,si in s.items():
            for d,q in outs[i].items(): row[d]=row.get(d,0)-delta*hj*si*q
    for k in forms: forms[k]={d:q for d,q in forms[k].items() if q}
    deps={k:tuple(d for d in sorted(r) if d>=0) for k,r in sorted(forms.items())}
    return dict(w,forms=[[k,[[d,str(q)] for d,q in sorted(r.items())]] for k,r in sorted(forms.items())],
                schedule=list(TopologicalSorter(deps).static_order()))
from build import ratrec
def ratvec(dv,scale_key=None):
    k0=scale_key if scale_key is not None else min(dv); inv=pow(dv[k0],P-2,P)
    out={k:ratrec(v*inv%P) for k,v in dv.items()}
    assert all(q is not None for q in out.values()); return out
def realize(w,mu,lam,val=None,b=None):
    """exact s (input form of mu-combo) and h (adjoint of lam-combo) as rationals (via ratrec)."""
    n=len(w['initial'])
    if val is None: val=forward(w)
    if b is None: b=adjoint(w)
    sv=np.zeros(n,dtype=np.int64); hv=np.zeros(n,dtype=np.int64)
    for d,q in mu.items(): sv=(sv+(val[d] if d>=0 else np.eye(n,dtype=np.int64)[~d])*fm(q))%P
    for k,q in lam.items(): hv=(hv+b[k]*fm(q))%P
    s={i:ratrec(int(sv[i])) for i in np.nonzero(sv)[0]}; h={i:ratrec(int(hv[i])) for i in np.nonzero(hv)[0]}
    assert all(q is not None for q in list(s.values())+list(h.values()))
    return s,h
def zspaces(w,z,charts=None,val=None,b=None):
    """for helpers H with final chart z: at every chart c, value combos with form supported on H and row combos with adjoint supported on H."""
    n=len(w['initial']); E,main=expected(n)
    H=sorted(i for i in range(n) if i not in main and w['final'][i]==z); Hs=set(H); nonH=[j for j in range(n) if j not in Hs]
    moves={k:(a,bb) for k,a,bb in w['moves']}
    if val is None: val=forward(w)
    if b is None: b=adjoint(w)
    src=defaultdict(list); dst=defaultdict(list); inp=defaultdict(list)
    for k,(a,bb) in moves.items(): src[a].append(k); dst[bb].append(k)
    for i,a in enumerate(w['initial']): inp[a].append(i)
    out={}
    for c in (charts if charts is not None else range(len(w['frames']))):
        K=src[c]; keys=dst[c]+[~i for i in inp[c]]
        if not K or not keys: continue
        B=np.array([b[k] for k in K]); lam=nullspace(B[:,nonH].T)
        Psi=[({K[i]:int(l[i]) for i in np.nonzero(l)[0]},mm(l,B[:,H])) for l in lam]; Psi=[p for p in Psi if p[1].any()]
        if not Psi: continue
        A=np.array([val[k] for k in dst[c]]+[np.eye(n,dtype=np.int64)[i] for i in inp[c]])
        mu=nullspace(A[:,nonH].T)
        V=[({keys[i]:int(m[i]) for i in np.nonzero(m)[0]},mm(m,A[:,H])) for m in mu]; V=[v for v in V if v[1].any()]
        if not V: continue
        out[c]=dict(H=H,V=V,Psi=Psi)
    return out
def input_edit(w,mu,lam,s,h,delta):
    """rows lam += delta*mu-combo at c (map += delta h s^T); compensate at inputs: x -> x - delta h (s.x):
    every use of input ~j (j in h) gets  -delta*q*h_j*sum_i s_i ~i  (needs all ~i resident with ~j)."""
    forms={k:{d:Fraction(q) for d,q in r} for k,r in w['forms']}
    anc=ancestors(w,list(mu)); assert not (set(lam)&anc),'cycle'
    for k,lk in lam.items():
        for d,md in mu.items(): forms[k][d]=forms[k].get(d,0)+delta*lk*md
    hj={~j:v for j,v in h.items()}
    ini=w['initial']; assert len({ini[i] for i in list(s)+list(h)})==1
    for k,row in forms.items():
        add={}
        for d,q in row.items():
            if d in hj:
                for i,si in s.items(): add[~i]=add.get(~i,0)-delta*q*hj[d]*si
        for d,q in add.items(): row[d]=row.get(d,0)+q
    for k in forms: forms[k]={d:q for d,q in forms[k].items() if q}
    deps={k:tuple(d for d in sorted(r) if d>=0) for k,r in sorted(forms.items())}
    return dict(w,forms=[[k,[[d,str(q)] for d,q in sorted(r.items())]] for k,r in sorted(forms.items())],
                schedule=list(TopologicalSorter(deps).static_order()))
