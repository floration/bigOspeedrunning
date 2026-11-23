# Merge two same-link transfers, then try a chart-0 closure (add a chart-0 input combination u into one
# transfer rho leaving chart 0) plus re-encoding of the chart-0 inputs. Exact GF(2), virtual replay.
import sys,pickle
sys.path.insert(0,'/home/claude/work/binary')
from bscan import *
from bmerge import forward,gf2_rank_kernel
def adjoint_ov(d,pre_override):
    """backward pass; pre_override: t -> function(post_adj, madj_dict)->pre-move adjoint"""
    pub=d['public']; prog=d['program']; adj=defaultdict(int)
    for i in range(pub): adj[i]=1<<i
    madj={}
    for t in range(len(prog)-1,-1,-1):
        ins=prog[t]; op=ins[0]
        if op=='ADD': adj[ins[2]]^=adj[ins[1]]
        elif op=='MOVE':
            madj[t]=adj[ins[1]]
            if t in pre_override: adj[ins[1]]=pre_override[t]
        elif op=='SWAP': a,b=ins[1:]; adj[a],adj[b]=adj[b],adj[a]
        elif op in('CLEAR','INIT'): adj[ins[1]]=0
    return madj
def transpose(rows,n):
    cols=[0]*n
    for j,r in enumerate(rows):
        x=r
        while x:
            lb=x&-x; i=lb.bit_length()-1; cols[i]|=1<<j; x^=lb
    return cols
if __name__=='__main__':
    p=sys.argv[1]; d=load(p); res,w,moves,val,pairs,main=check(d,verbose=False); madj0,_=adjoint(w); pub=w.pub
    X=[i for i in range(pub) if d['start'][i]!=0]; mX=sum(1<<i for i in X); m0=((1<<pub)-1)&~mX
    def Minv(bm):
        r=bm
        for x,y in pairs:
            if bm>>x&1: r^=1<<y
        return r
    dep0,dlv0,out0=forward(d)
    rows=pickle.load(open(p.split('/')[-1]+'.mergerank.pkl','rb'))
    mv={t:(f,a,b) for t,f,a,b,v in moves}
    from0=[t for t,f,a,b,v in moves if a==0]
    stat=Counter(); found=[]; why=Counter()
    for l,t1,t2,defi in rows:
        b1,b2=madj0[t1],madj0[t2]
        ov={t1:lambda dep,t1=t1,t2=t2:dep[t1]^dep0[t2], t2:lambda dep,t1=t1,t2=t2:dep0[t1]^dep[t2]}
        _,_,out=forward(d,over_deliver=ov)
        rk,ker=gf2_rank_kernel(out,pub); assert pub-rk==1
        k=ker[0]; _,lker=gf2_rank_kernel(transpose(out,pub),pub); ell=lker[0]
        # sanity: F k = 0
        assert all(bin(r&k).count('1')%2==0 for r in out)
        kin0=k&m0
        if not kin0: stat['kernel has no chart-0 part']+=1; continue
        madjC=adjoint_ov(d,{t1:b1^b2,t2:b1^b2})
        cands=[]
        for r in from0:
            if r==t2: continue
            br=madjC[r]
            if bin(br&ell).count('1')%2 and Minv(br)&mX==0: cands.append(r)
        if not cands: stat['no rho with ell.b=1 and absorbable']+=1; continue
        stat['rho candidates exist']+=1
        # exact test with first few candidates
        ok=False
        i0=(kin0&-kin0).bit_length()-1; u=1<<i0
        for r in cands[:8]:
            inj={r:u}
            S2=dep0[t2]
            for it in range(4):
                ovr={t1:lambda dep,S2=S2,t1=t1:dep[t1]^S2, t2:lambda dep,t1=t1,t2=t2:dep[t1]^dep[t2]}
                dpr,dlr,out2=forward(d,over_deliver=ovr,inject=inj)
                if dpr[t2]==S2: break
                S2=dpr[t2]
            else: continue
            assert dlr[t1]==dlr[t2]   # one merged value
            rk2,_=gf2_rank_kernel(out2,pub)
            N=list(out2)
            for x,y in pairs: N[y]^=out2[x]
            Xs=set(X)
            offX=any((N[j]&mX)!=((1<<j) if j in Xs else 0) for j in range(pub))
            off2=any(N[j]&m0 for j in X)
            why[(rk2==pub, not offX, not off2, r==t1, dpr[t2]!=dep0[t2] or dpr[t1]!=dep0[t1])]+=1
            if rk2==pub and not offX and not off2: ok=True; found.append((l,t1,t2,r,i0)); break
        stat['exact fix' if ok else 'exact fails']+=1
    print(p,dict(stat)); print('why (fullrank, Xcols ok, Xrows ok, rho is w, injection feeds s1/s2):',dict(why))
    for f in found[:10]: print(f)
    pickle.dump(found,open(p.split('/')[-1]+'.fix.pkl','wb'))
