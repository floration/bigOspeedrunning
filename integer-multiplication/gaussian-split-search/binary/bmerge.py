# Exact GF(2) analysis of merging two same-link transfers (t1<t2) into w = s1+s2 on the binary word.
import sys,pickle
sys.path.insert(0,'/home/claude/work/binary')
from bscan import *
def forward(d,over_deliver=None,inject=None):
    """virtual forward replay; over_deliver: t->value delivered by MOVE t; inject: t->value added to the field
    just before MOVE t departs. returns departure values, delivered values, final outputs"""
    pub=d['public']; val={i:1<<i for i in range(pub)}; dep={}; dlv={}
    for t,ins in enumerate(d['program']):
        op=ins[0]
        if op=='INIT': val[ins[1]]=0
        elif op=='ADD': val[ins[1]]^=val[ins[2]]
        elif op=='MOVE':
            f=ins[1]
            if inject and t in inject: val[f]^=inject[t]
            dep[t]=val[f]
            if over_deliver and t in over_deliver: val[f]=over_deliver[t](dep)
            dlv[t]=val[f]
        elif op=='SWAP': a,b=ins[1:]; val[a],val[b]=val[b],val[a]
        elif op=='CLEAR': val.pop(ins[1])
    return dep,dlv,[val[i] for i in range(pub)]
def gf2_rank_kernel(rows,n):
    """rows: list of n ints (row j = output j form). returns rank and a basis of right kernel {k: rows[j].k=0}"""
    piv={}  # pivot bit -> (row, combo)
    R=[]
    for j,r in enumerate(rows):
        for pb,(pr_,_) in list(piv.items()):
            pass
    # Gaussian elimination
    basis=[]
    for r in rows:
        for b in basis:
            if r & (1<<(b.bit_length()-1)): r^=b
        if r:
            hb=r.bit_length()-1
            basis=[b^r if b>>hb&1 else b for b in basis]; basis.append(r)
    pivs={b.bit_length()-1:b for b in basis}
    free=[i for i in range(n) if i not in pivs]
    ker=[]
    for f in free:
        k=1<<f
        for p_,b in pivs.items():
            if b>>f&1: k|=1<<p_
        ker.append(k)
    return len(basis),ker
if __name__=='__main__':
    p=sys.argv[1]; d=load(p); res,w,moves,val,pairs,main=check(d,verbose=False); madj,inadj=adjoint(w); pub=w.pub
    dep0,dlv0,out0=forward(d)
    assert sorted(expected_from_outputs({i:out0[i] for i in range(pub)},pub)[0])==sorted(pairs)
    link=defaultdict(list)
    for t,f,a,b,v in moves: link[(a,b)].append(t)
    stats=Counter(); rows=[]
    for l,ts in link.items():
        for i in range(len(ts)):
            for j in range(i+1,len(ts)):
                t1,t2=ts[i],ts[j]
                # feedback: does s2 depend on d1?  perturb d1 by a fresh symbol bit (bit pub)
                dp,_,_=forward(d,over_deliver={t1:lambda dep,t1=t1:dep[t1]^(1<<pub)})
                if dp[t2]>>pub&1: stats['cycle']+=1; continue
                ov={t1:lambda dep,t1=t1,t2=t2:dep[t1]^dep0[t2], t2:lambda dep,t1=t1,t2=t2:dep0[t1]^dep[t2]}
                dp,dl,out=forward(d,over_deliver=ov)
                assert dp[t1]==dep0[t1] and dp[t2]==dep0[t2]
                rk,ker=gf2_rank_kernel(out,pub)
                stats[('rank',pub-rk)]+=1
                rows.append((l,t1,t2,pub-rk))
    print(p,dict(stats))
    pickle.dump(rows,open(p.split('/')[-1]+'.mergerank.pkl','wb'))
