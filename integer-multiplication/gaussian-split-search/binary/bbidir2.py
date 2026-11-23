# Generalised merge screen: any two transfers on one link. Merge w=v1+v2 (readers of both take w).
# Output-space error E = b1 (x) u2 + b2 (x) u1. A term b(x)u is absorbable by re-encoding the chart-0 inputs
# iff u_X = 0 and (Minv b)_X = 0. The other term(s) must be cancelled by a closure: a chart c not on the link where
# u is in the span of residents at c and b is in the span of adjoints of rows leaving c (moves out + outputs at c).
import sys,pickle
sys.path.insert(0,'/home/claude/work/binary')
from bbidir import inspan
from bscan import *
for p in sys.argv[1:]:
    d=load(p); res,w,moves,val,pairs,main=check(d,verbose=False); madj,inadj=adjoint(w); pub=w.pub
    X=[i for i in range(pub) if d['start'][i]!=0]; mX=sum(1<<i for i in X)
    def Minv(bm):
        r=bm
        for x,y in pairs:
            if bm>>x&1: r^=1<<y
        return r
    T=[(t,f,a,b,v,madj[t]) for t,f,a,b,v in moves]
    absb=lambda bm,u: u&mX==0 and Minv(bm)&mX==0
    link=defaultdict(list)
    for x in T: link[(x[2],x[3])].append(x)
    inp=defaultdict(list); arr=defaultdict(list); dep=defaultdict(list)
    for i in range(pub): inp[d['start'][i]].append(1<<i)
    for x in T: arr[x[3]].append(x[4]); dep[x[2]].append(x[5])
    for j in range(pub): dep[d['final'][j]].append(1<<j)
    allpairs=0; one=[]; both=0
    for l,xs in link.items():
        for i in range(len(xs)):
            for j in range(i+1,len(xs)):
                v1,v2=xs[i],xs[j]; allpairs+=1
                a12=absb(v1[5],v2[4]); a21=absb(v2[5],v1[4])
                if a12 and a21: both+=1; one.append((l,v1,v2,None))
                elif a12: one.append((l,v1,v2,(v2[5],v1[4])))   # need to cancel b2 (x) u1
                elif a21: one.append((l,v1,v2,(v1[5],v2[4])))
    print(p,'same-link pairs',allpairs,'both terms absorbable',both,'exactly one absorbable',len(one)-both,
          sorted(Counter(w.grade(*o[0]) for o in one).items()))
    need=[o for o in one if o[3] is not None]
    B=[o[3][0] for o in need]; U=[o[3][1] for o in need]
    hit=defaultdict(set)
    for c in w.S:
        if not dep[c]: continue
        oku=inspan(inp[c]+arr[c],U); okb=inspan(dep[c],B)
        for k in range(len(need)):
            if oku[k] and okb[k] and c not in need[k][0]: hit[k].add(c)
    print(' with a single third-chart closure:',len(hit),sorted(Counter(w.grade(*need[k][0]) for k in hit).items()))
    # u-only and b-only availability
    ucount=sum(1 for k in range(len(need)) if any(inspan(inp[c]+arr[c],[U[k]])[0] for c in w.S if c not in need[k][0]))
    print(' cancel-term u in some off-link resident span:',ucount)
    pickle.dump(dict(one=[(o[0],o[1][0],o[2][0],o[3] is None) for o in one],hit={k:sorted(s) for k,s in hit.items()}),open(p.split('/')[-1]+'.bidir2.pkl','wb'))
