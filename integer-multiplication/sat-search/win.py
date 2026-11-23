import pickle,sys,random
from collections import defaultdict,deque
from ortools.sat.python import cp_model
g=pickle.load(open('cgraph.pkl','rb')); dom0=pickle.load(open('dom.pkl','rb'))
label=g['label']; fixed=g['fixed']; edges=g['edges']; R=g['R']; NE=g['NE']
c=0.00389848144654994
Wt=[0]+[round((k**(1-c))*1e10) for k in range(1,10)]
adj=defaultdict(list)
for k,u,v in edges: adj[u].append((k,v)); adj[v].append((k,u))
cur=dict(label)
def cost_of(lab,es): return sum(Wt[abs(R[lab[u]]-R[lab[v]])] for k,u,v in es)
def solve(W,cur,tl=20):
    Wset=set(W)
    es=[(k,u,v) for k,u,v in edges if u in Wset or v in Wset]
    dom={}
    for v in W:
        dom[v]={L for L in dom0[v] if all(NE[L][cur[u]] for k,u in adj[v] if u not in Wset)}
    ch=True
    while ch:
        ch=False
        for v in W:
            nd={L for L in dom[v] if all(any(NE[L][M] for M in dom[u]) for k,u in adj[v] if u in Wset)}
            if nd!=dom[v]: dom[v]=nd; ch=True
    if any(len(dom[v])<=1 for v in W) and all(len(dom[v])==1 for v in W): return None
    m=cp_model.CpModel(); X={}
    for v in W:
        X[v]={L:m.NewBoolVar('') for L in dom[v]}; m.AddExactlyOne(X[v].values())
        m.AddHint(X[v][cur[v]],1)
    obj=[]
    for k,u,v in es:
        if u in Wset and v in Wset:
            for L,x in X[u].items():
                m.AddBoolOr([X[v][M] for M in dom[v] if NE[L][M]]).OnlyEnforceIf(x)
            # cost via dims
            du={}; dv={}
            gv=m.NewIntVar(1,9,'')
            dU=sum(R[L]*x for L,x in X[u].items()); dV=sum(R[M]*x for M,x in X[v].items())
            m.AddAbsEquality(gv,dU-dV)
            bs=[m.NewBoolVar('') for _ in range(10)]
            m.AddExactlyOne(bs); m.Add(gv==sum(i*b for i,b in enumerate(bs)))
            obj+= [Wt[i]*b for i,b in enumerate(bs) if i]
        else:
            a,o=(u,v) if u in Wset else (v,u)
            for L,x in X[a].items(): obj.append(Wt[abs(R[L]-R[cur[o]])]*x)
    m.Minimize(sum(obj))
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=tl; s.parameters.num_workers=4
    st=s.Solve(m)
    if st not in (cp_model.OPTIMAL,cp_model.FEASIBLE): return None
    new={v:next(L for L,x in X[v].items() if s.Value(x)) for v in W}
    lab=dict(cur); lab.update(new)
    return cost_of(cur,es)-cost_of(lab,es), new, st==cp_model.OPTIMAL
if __name__=='__main__':
    size=int(sys.argv[1]); seeds=[v for v in label if not fixed[v]]
    random.seed(int(sys.argv[2]) if len(sys.argv)>2 else 0); random.shuffle(seeds)
    tot=0; found=[]
    for i,s0 in enumerate(seeds):
        W=[s0]; seen={s0}; q=deque([s0])
        while q and len(W)<size:
            x=q.popleft()
            for k,y in adj[x]:
                if y not in seen and not fixed[y] and len(W)<size: seen.add(y); W.append(y); q.append(y)
        r=solve(W,cur)
        if r and r[0]>0:
            print('GAIN',r[0],s0,{v:(cur[v],L) for v,L in r[1].items() if cur[v]!=L},flush=True)
            found.append((r[0],s0,r[1])); cur.update(r[1])
        if i%50==0: print('done',i,'opt' if r and r[2] else '',flush=True)
    pickle.dump((cur,found),open(f'win_{size}.pkl','wb'))
    print('total gain',sum(f[0] for f in found))
