# Build a loop-flow merge: merge v1,v2 on link a->b into one transfer, cancel the rank-1 error at a third chart c,
# then re-encode the chart-3 inputs to absorb the remaining chart-3 x chart-3 block.  Own code only.
import sys,pickle,time,json
sys.path.insert(0,'/home/claude/work')
from rw_lib import *
from graphlib import TopologicalSorter,CycleError
W0=pickle.load(open('/home/claude/work/words.pkl','rb'))['final']
n=len(W0['initial']); first=W0['first_output']
E_,main=expected(n)
Mmat=np.zeros((n,n),dtype=np.int64)
for i,col in enumerate(E_):
    for j,q in col.items(): Mmat[j,i]=fm(q)
def inverse(Wm):
    A=np.concatenate([Wm%P,np.eye(len(Wm),dtype=np.int64)],axis=1); m=len(Wm)
    for c in range(m):
        nzc=np.nonzero(A[c:,c])[0]
        if len(nzc)==0: return None
        p=c+nzc[0]; A[[c,p]]=A[[p,c]]
        A[c]=A[c]*pow(int(A[c,c]),P-2,P)%P
        col=A[:,c].copy(); col[c]=0; nz=np.nonzero(col)[0]
        if len(nz): A[nz]=(A[nz]-mm(col[nz][:,None],A[c][None,:]))%P
    return A[:,m:]
Minv=inverse(Mmat)
C3=[i for i in range(n) if W0['initial'][i]==3]; X=[i for i in range(n) if W0['initial'][i]!=3]
def F_of(w,val=None):
    if val is None: val=forward(w)
    return np.array([val[first+j] for j in range(n)]),val
def recov_err(w,val=None):
    F,val=F_of(w,val); D=(F-Mmat)%P; rows=np.nonzero(D.any(1))[0]
    if len(rows)==0: return np.zeros((n,n),dtype=np.int64),val
    return mm(Minv[:,rows],D[rows]),val
def solve_left(A,v):
    """x with x@A = v (mod P), or None"""
    Mt=np.column_stack([A.T%P,v%P]); ns=nullspace(Mt)
    for x in ns:
        if x[-1]:
            inv=(-pow(int(x[-1]),P-2,P))%P; return x[:-1]*inv%P
    return None
def tofrac(x):
    q=ratrec(int(x)); 
    if q is None: raise ValueError('ratrec')
    return q
def finish(forms,w):
    for k in list(forms): forms[k]={d:q for d,q in forms[k].items() if q}
    deps={k:tuple(d for d in sorted(r) if d>=0) for k,r in sorted(forms.items())}
    sched=list(TopologicalSorter(deps).static_order())
    return dict(w,forms=[[k,[[d,str(q)] for d,q in sorted(r.items())]] for k,r in sorted(forms.items())],schedule=sched)
def sens(w,seed):
    forms={k:[(d,fm(q)) for d,q in r] for k,r in w['forms']}; J={}
    for k in w['schedule']:
        x=seed.get(k,0)
        for d,q in forms[k]:
            if d>=0 and J.get(d): x=(x+J[d]*q)%P
        if x: J[k]=x
    return J
def build(w,v1,v2,c,t=Fraction(1),log=None):
    L=log if log is not None else {}
    val0=forward(w); b0=adjoint(w); u1=val0[v1]; bv2=b0[v2]
    m0={k:(a,bb) for k,a,bb in w['moves']}
    res=[k for k,(a,bb) in m0.items() if bb==c]+[~i for i in range(n) if w['initial'][i]==c]
    rows=[k for k,(a,bb) in m0.items() if a==c]+[first+j for j in range(n) if w['final'][j]==c]
    EYE=np.eye(n,dtype=np.int64)
    mu=solve_left(np.array([val0[k] if k>=0 else EYE[~k] for k in res]),u1)
    lam=solve_left(np.array([b0[k] for k in rows]),bv2)
    if mu is None or lam is None: L['fail']='span'; return None
    try:
        muq={res[i]:tofrac(x) for i,x in enumerate(mu) if x}; lamq={rows[i]:tofrac(x) for i,x in enumerate(lam) if x}
    except ValueError: L['fail']='ratrec mu/lam'; return None
    J1=sens(w,{v1:1}); J2=sens(w,{v2:1})
    p1=sum(fm(q)*J1.get(k,0) for k,q in muq.items() if k>=0)%P; p2=sum(fm(q)*J2.get(k,0) for k,q in muq.items() if k>=0)%P
    # upstream sensitivities (lam rows feeding the v-slots)
    Jl=sens(w,{k:fm(q) for k,q in lamq.items()}); q1=Jl.get(v1,0); q2=Jl.get(v2,0)
    L.update(p1=ratrec(p1),p2=ratrec(p2),q1=ratrec(q1),q2=ratrec(q2))
    if q1 or q2: L['note']='lam upstream of slots'
    if L['p1'] is None or L['p2'] is None: L['fail']='ratrec p'; return None
    p1,p2=L['p1'],L['p2']; q1,q2=L['q1'],L['q2']
    if q1 is None or q2 is None: L['fail']='ratrec q'; return None
    if (q1 or q2) and (p1 or p2): L['fail']='both up- and downstream'; return None
    if q1 or q2:
        if q2: L['fail']='q2!=0'; return None
        if q1+t==0: t=Fraction(2)
        beta=1/t; sig=1/(q1+t)
    else:
        if 1-p1==0 and p2==0: L['fail']='den0 (p1=1,p2=0)'; return None
        if t*(1-p1)+p2==0: t=t+1
        sig=1/(t*(1-p1)+p2)
        if 1-sig*p2==0: L['fail']='beta'; return None
        beta=sig/(1-sig*p2)
    L['t']=t; L['sigma']=sig; L['beta']=beta
    forms={k:{d:Fraction(q) for d,q in r} for k,r in w['forms']}
    for d,q in forms[v2].items(): forms[v1][d]=forms[v1].get(d,0)+t*q
    del forms[v2]
    for k,r in forms.items():
        if v2 in r:
            q=r.pop(v2); r[v1]=r.get(v1,0)+beta*q
    for k,lk in lamq.items():
        for d,md in muq.items(): forms[k][d]=forms[k].get(d,0)-sig*lk*md
    try: w2=finish(forms,dict(w,moves=[[k,a,b] for k,a,b in w['moves'] if k!=v2]))
    except CycleError: L['fail']='cycle'; return None
    Er,_=recov_err(w2)
    offX=int((Er[X]!=0).sum()+(Er[:,X]!=0).sum())
    L['offblock']=offX
    if offX: L['fail']='off-block error %d'%offX; return None
    Bblk=(np.eye(len(C3),dtype=np.int64)+Er[np.ix_(C3,C3)])%P
    Binv=inverse(Bblk)
    if Binv is None: L['fail']='B singular'; return None
    nzb=np.nonzero((Binv-np.eye(len(C3),dtype=np.int64))%P)
    sub={}
    try:
        for r_,c_ in zip(*nzb): sub.setdefault(C3[r_],{})[C3[c_]]=tofrac(Binv[r_,c_])
    except ValueError: L['fail']='ratrec Binv'; return None
    forms={k:{d:Fraction(q) for d,q in r} for k,r in w2['forms']}
    for k,r in forms.items():
        add={}
        for d,q in r.items():
            if d<0 and (~d) in sub:
                for i,x in sub[~d].items(): add[~i]=add.get(~i,0)+q*(x-(1 if i==~d else 0))
        for d,q in add.items(): r[d]=r.get(d,0)+q
    L['Bchanges']=len(nzb[0])
    return finish(forms,w2)
if __name__=='__main__':
    d=pickle.load(open('/home/claude/work/lf/cands.pkl','rb'))
    pairs=d['pairs']; order=sorted(d['hit'],key=lambda i:-pairs[i][1])
    lim=int(sys.argv[1]) if len(sys.argv)>1 else len(order)
    results=[]
    base=check(W0); k0=kappa(base)
    for i in order[:lim]:
        l,g,v1,v2=pairs[i]
        for c in sorted(d['hit'][i]):
            L={}; t0=time.time()
            try: w3=build(W0,v1,v2,c,log=L)
            except Exception as e: L['fail']='exc '+repr(e)[:80]; w3=None
            rec=dict(link=l,grade=g,v1=v1,v2=v2,c=c,**L)
            if w3 is not None:
                r=check(w3); rec.update(bad=r['bad_outputs'],moves=r['moves'],paid=r['paid'],tg=r['tg'],kappa=kappa(r),gain=kappa(r)-k0)
                if r['bad_outputs']==0: pickle.dump(w3,open('/home/claude/work/lf/word_%d_%d_%d.pkl'%(v1,v2,c),'wb'))
            rec['sec']=round(time.time()-t0,1)
            print({k:v for k,v in rec.items() if k not in ('paid','tg')},flush=True)
            results.append(rec)
            pickle.dump(results,open('/home/claude/work/lf/results.pkl','wb'))
