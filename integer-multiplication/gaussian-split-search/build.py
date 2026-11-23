import pickle,json,numpy as np,sys
from fractions import Fraction
from collections import defaultdict
sys.path.insert(0,'/home/claude/work')
from lin import *
from chk import expected,span,check
from rebuild import split,sha
def ratrec(a,m=P):
    a%=m
    r0,r1,s0,s1=m,a,0,1
    while r1*r1*2>m: q=r0//r1; r0,r1=r1,r0-q*r1; s0,s1=s1,s0-q*s1
    if s1==0 or s1*s1*2>m: return None
    return Fraction(r1,s1) if s1>0 else Fraction(-r1,-s1)
def normalize(vec,keys):
    # scale so first nonzero = 1, then rational-reconstruct
    nz=[i for i,x in enumerate(vec) if x]
    inv=pow(int(vec[nz[0]]),P-2,P); out={}
    for i in nz:
        q=ratrec(int(vec[i])*inv%P); assert q is not None,'ratrec'
        out[keys[i]]=q
    return out
def make_event(w,c,a=3,z=127,role=None):
    n=len(w['initial']); fr=w['frames']
    E,main=expected(n)
    moves={k:(x,y) for k,x,y in w['moves']}
    G=sorted(i for i in range(n) if i not in main and w['initial'][i]==a and w['final'][i]==z)
    Gs=set(G); nonG=[j for j in range(n) if j not in Gs]
    val=forward(w); b=adjoint(w)
    K=[k for k,(x,y) in moves.items() if x==c]
    B=np.array([b[k] for k in K]); lam=[l for l in nullspace(B[:,nonG].T) if mm(l,B[:,G]).any()]
    assert len(lam)==1,len(lam)
    lamq=normalize(lam[0],K)
    Rk=[k for k,(x,y) in moves.items() if y==c]; Ri=[i for i in range(n) if w['initial'][i]==c]
    A=np.array([val[k] for k in Rk]+[np.eye(n,dtype=np.int64)[i] for i in Ri])
    mu=[m for m in nullspace(A[:,nonG].T) if mm(m,A[:,G]).any()]
    assert len(mu)==1
    keys=Rk+[~i for i in Ri]; muq=normalize(mu[0],keys)
    # exact-ish covector/direction via mod p then ratrec
    s=np.zeros(n,dtype=np.int64)
    for k,q in muq.items(): s=(s+(val[k] if k>=0 else np.eye(n,dtype=np.int64)[~k])*fm(q))%P
    h=np.zeros(n,dtype=np.int64)
    for k,q in lamq.items(): h=(h+b[k]*fm(q))%P
    sq={i:ratrec(int(s[i])) for i in range(n) if s[i]}; hq={i:ratrec(int(h[i])) for i in range(n) if h[i]}
    assert all(v is not None for v in list(sq.values())+list(hq.values()))
    assert set(sq)<=Gs and set(hq)<=Gs
    if role is None: role=min(hq)
    ev=dict(role=role,chart=c,covector=[[i,str(q)] for i,q in sorted(sq.items())],
            direction=[[i,str(q)] for i,q in sorted(hq.items())],
            read=[[k,str(q)] for k,q in sorted(muq.items())],inject=[[k,str(q)] for k,q in sorted(lamq.items())])
    return ev
if __name__=='__main__':
    ws=pickle.load(open('/home/claude/work/words.pkl','rb')); w=ws['final']
    evs=[]
    for c in map(int,sys.argv[1:]):
        ev=make_event(w,c); print(c,'role',ev['role'],'cov',len(ev['covector']),'dir',len(ev['direction']),'read',ev['read'],'inject',ev['inject'])
        w2=json.loads(json.dumps(split(w,ev)))
        r=check(w2); print(' check',r['bad_outputs'],r['moves'],r['n'],r['tg'])
        if r['bad_outputs']==0: w=w2; evs.append(ev)
    json.dump(evs,open('/home/claude/work/events.json','w'),indent=1)
    pickle.dump(w,open('/home/claude/work/stacked.pkl','wb'))
    print('stacked',len(evs),sha(w))
