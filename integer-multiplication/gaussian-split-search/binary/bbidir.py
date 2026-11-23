# #8027-style bidirectional merge screen on the binary word (GF(2)); own code.
import sys,pickle
sys.path.insert(0,'/home/claude/work/binary')
from bscan import *
def inspan(vs,targets):
    basis=[]
    for v in vs:
        for b in basis: v=min(v,v^b)
        if v: basis.append(v)
    basis.sort(reverse=True)
    out=[]
    for t in targets:
        for b in basis: t=min(t,t^b)
        out.append(t==0)
    return out
for p in sys.argv[1:]:
    d=load(p); res,w,moves,val,pairs,main=check(d,verbose=False); madj,inadj=adjoint(w); pub=w.pub
    big=Counter(d['start'][i] for i in range(pub) if i not in main).most_common(1)[0][0]
    X=[i for i in range(pub) if d['start'][i]!=big]; mX=sum(1<<i for i in X)
    partner={y:x for x,y in pairs}
    def Minv(bm):  # recovered-coordinate effect of output perturbation bm; Minv: y = out_y + out_x
        r=bm
        for x,y in pairs:
            if bm>>x&1: r^=1<<y
        return r
    T=[]  # (t,f,a,b,val,adj,uX0,zX0)
    for t,f,a,b,v in moves:
        z=Minv(madj[t]); T.append((t,f,a,b,v,madj[t],v&mX==0,z&mX==0))
    print(p,'chart',big,'|X|',len(X),'transfers',len(T),'u_X=0',sum(x[6] for x in T),'z_X=0',sum(x[7] for x in T),'both',sum(x[6] and x[7] for x in T))
    print(' grade of u_X=0',sorted(Counter(w.grade(x[2],x[3]) for x in T if x[6]).items()))
    print(' grade of z_X=0',sorted(Counter(w.grade(x[2],x[3]) for x in T if x[7]).items()))
    link=defaultdict(list)
    for x in T: link[(x[2],x[3])].append(x)
    pl=[];pp=[]
    for l,xs in link.items():
        A=[x for x in xs if not x[6] and x[7]]   # v1: u_X!=0, z_X=0
        B=[x for x in xs if x[6] and not x[7]]   # v2: u_X=0, z_X!=0
        A2=[x for x in xs if x[7]]; B2=[x for x in xs if x[6]]
        if any(x is not y for x in A2 for y in B2): pl.append((l,w.grade(*l)))
        for v1 in A:
            for v2 in B: pp.append((l,w.grade(*l),v1,v2))
    print(' links with one u_X=0 and another z_X=0 transfer:',len(pl),sorted(Counter(g for l,g in pl).items()))
    print(' strict pattern pairs (v1 u!=0,z=0; v2 u=0,z!=0):',len(pp),'on links',len({x[0] for x in pp}),sorted(Counter(g for l,g,a,b in pp).items()))
    # GF(2) invertibility of chart-0 block after absorbing z1(x)u2: need u2.z1 = 0
    inv=[bin(v2[4]&Minv(v1[5])).count('1')%2==0 for l,g,v1,v2 in pp]
    print(' pairs whose block I+z1u2 is invertible:',sum(inv))
    # third-chart closure
    inp=defaultdict(list); arr=defaultdict(list); dep=defaultdict(list)
    for i in range(pub): inp[d['start'][i]].append(1<<i)
    for x in T: arr[x[3]].append(x[4]); dep[x[2]].append(x[5])
    for j in range(pub): dep[d['final'][j]].append(1<<j)
    U1=[v1[4] for l,g,v1,v2 in pp]; B2=[v2[5] for l,g,v1,v2 in pp]
    hitU=defaultdict(set); hit=defaultdict(set)
    for c in w.S:
        oku=inspan(inp[c]+arr[c],U1); okb=inspan(dep[c],B2)
        for i in range(len(pp)):
            if oku[i]: hitU[i].add(c)
            if oku[i] and okb[i] and c not in pp[i][0]: hit[i].add(c)
    print(' pairs with u1 in a resident span somewhere:',len(hitU),' pairs with a third closure chart:',len(hit),sorted(Counter(pp[i][1] for i in hit).items()))
    pickle.dump(dict(pp=[(l,g,v1[0],v2[0]) for l,g,v1,v2 in pp],hit={i:sorted(s) for i,s in hit.items()},inv=inv),open(p.split('/')[-1]+'.bidir.pkl','wb'))
