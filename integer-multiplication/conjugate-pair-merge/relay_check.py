import json,gzip,sys,numpy as np,collections,time
sys.path.insert(0,'/home/claude/cp'); from uz import compute,p,rank_mod
from graphlib import TopologicalSorter, CycleError
w=json.load(gzip.open(sys.argv[1])); C=json.load(open(sys.argv[2]))
R=compute(w); forms,Minv,X=R['forms'],R['Minv'],R['X']
ini,fin,fo=w['initial'],w['final'],w['first_output']; n=len(ini)
Xs=set(X.tolist()); T3=[i for i in range(n) if i not in Xs]
newlab=max(k for k,_,_ in w['moves'])+1; assert newlab<fo
def build(c):
    x,y=c['x'],c['y']; nf={k:dict(v) for k,v in forms.items()}
    D=newlab; nf[D]=dict(forms[x]); del nf[x],nf[y]
    for k in nf:
        nf[k].pop(x,None)
        if y in nf[k]: nf[k].pop(y)
    for key,v in c['dK'].items():
        r,i=map(int,key.split(',')); nf[r][i]=(nf[r].get(i,0)+v)%p
        if not nf[r][i]: del nf[r][i]
    for r,v in c['cc'].items(): nf[int(r)][D]=(nf[int(r)].get(D,0)+v)%p
    return nf,D
def check(nf):
    deps={k:tuple(d for d in f if d>=0) for k,f in nf.items()}
    try: order=list(TopologicalSorter(deps).static_order())
    except CycleError: return 'cycle'
    idx2={k:i for i,k in enumerate(order)}; V=np.zeros((len(order),n),dtype=np.int64)
    for i,k in enumerate(order):
        v=np.zeros(n,dtype=np.int64)
        for d,cf in nf[k].items():
            if d<0: v[~d]=(v[~d]+cf)%p
            else: v=(v+V[idx2[d]]*cf)%p
        V[i]=v
    F=np.array([V[idx2[fo+j]] for j in range(n)])
    E=np.zeros((n,n),dtype=np.int64)
    for i in range(n):
        for j in np.nonzero(Minv[i])[0]: E[i]=(E[i]+Minv[i,j]*F[j])%p
    if not np.array_equal(E[np.ix_(X,X)],np.eye(len(X),dtype=np.int64)): return 'XX'
    if E[np.ix_(X,T3)].any(): return 'X3'
    if E[np.ix_(T3,X)].any(): return '3X'
    r=rank_mod(E[np.ix_(T3,T3)])
    return 'OK' if r==len(T3) else f'33 rank {r}'
out=collections.Counter(); good=[]
t0=time.time()
for k,c in enumerate(C):
    nf,D=build(c); msg=check(nf); out[msg.split(' rank')[0] if 'rank' in msg else msg]+=1
    if msg=='OK': good.append(c); print('PASS',c['x'],c['y'],c['a'],c['b'],c['c'],c['g'],flush=True)
    if k%25==0: print(k,dict(out),round(time.time()-t0),flush=True)
print('final',dict(out)); json.dump(good,open(sys.argv[3],'w'))
