import sys, random, time

exec(open('rect.py').read())
# linear flags subset (21 trees from affine structure over positions 0..7 labelled as x in F2^3)
def lin_trees():
    res=[]
    for a in range(1,8):
        for b in range(1,8):
            if b!=a and b<(b^a):
                c=1
                while c in (a,b,a^b): c+=1
                perm=[0]*8
                for x in range(8):
                    j=4*par(a&x)+2*par(b&x)+par(c&x); perm[j]=x
                # find tree index
                ns=nodes(perm)
                key=frozenset(ns.values())
                for i,N in enumerate(NODES):
                    if frozenset(N.values())==key: res.append(i); break
                else: res.append(None)
    return res
LIN=lin_trees(); print("linear flags found:",len([x for x in LIN if x is not None]))
cand=list(range(315)) if (len(sys.argv)>1 and sys.argv[1]=='all') else LIN
random.seed(int(sys.argv[2]) if len(sys.argv)>2 else 0)
tx=[random.choice(cand) for _ in range(15)]; ty=[random.choice(cand) for _ in range(15)]
def total(tx,ty): return sum(solve(X,Y,tx[X],ty[Y]) for X in range(15) for Y in range(15))
cur=total(tx,ty)
for p in range(12):
    improved=False
    for axis in (0,1):
        for F in range(15):
            best=None
            for c in cand:
                if axis==0: v=sum(solve(F,Y,c,ty[Y]) for Y in range(15))
                else: v=sum(solve(X,F,tx[X],c) for X in range(15))
                if best is None or v<best[0]-1e-12: best=(v,c)
            if axis==0:
                if best[1]!=tx[F]: improved=True
                tx[F]=best[1]
            else:
                if best[1]!=ty[F]: improved=True
                ty[F]=best[1]
    H,T,P=profile(tx,ty); s=root(T,P)
    print("pass",p,"rects",sum(H.values()),"T",T,"P",P,"s*",s,"1/kappa",None if s is None else (2-s)/(1-s),flush=True)
    if not improved: break
import json; json.dump({"tx":tx,"ty":ty,"T":T,"P":P,"H":{f"{a}x{b}":n for (a,b),n in H.items()}},open(f"best_{sys.argv[2]}.json","w"))
