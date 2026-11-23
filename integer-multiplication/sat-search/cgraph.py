from model import *
import pickle
w,l=load(); R=[len(f) for f in w['frames']]; F=w['frames']
SP=[span(f) for f in F]; NC=len(F)
n=len(w['initial']); first=w['first_output']
forms=dict((k,r) for k,r in w['forms'])
loc={}; src={}
for i in range(n): loc[~i]=w['initial'][i]
for k,a,b in w['moves']: loc[k]=b; src[k]=a
for i in range(n): src[first+i]=w['final'][i]
par={}
def find(x):
    while par.setdefault(x,x)!=x: par[x]=par[par[x]]; x=par[x]
    return x
for k,r in forms.items():
    for d,_ in r: par[find(('c',k))]=find(('d',d))
node={}; label={}; fixed={}
def nid(key,ch):
    r=(ch,find(key))
    if r not in node: node[r]=len(node); label[node[r]]=ch; fixed[node[r]]=False
    return node[r]
for k,r in forms.items():
    v=nid(('c',k),src[k])
    if first<=k<first+n: fixed[v]=True
for d in loc:
    if ('d',d) in par:
        v=nid(('d',d),loc[d])
        if d<0: fixed[v]=True
edges=[]
for k,a,b in w['moves']:
    u=nid(('c',k),a); v=nid(('d',k),b) if ('d',k) in par else None
    edges.append((k,u,v))
print('nodes',len(node),'fixed',sum(fixed.values()),'edges',len(edges),'dangling',sum(1 for e in edges if e[2] is None))
NE=[[SP[x]<SP[y] or SP[y]<SP[x] for y in range(NC)] for x in range(NC)]
pickle.dump(dict(label=label,fixed=fixed,edges=edges,R=R,NE=NE),open('cgraph.pkl','wb'))
adj=defaultdict(set)
for k,u,v in edges: adj[u].add(v); adj[v].add(u)
dom={}
for v in label:
    if fixed[v]: dom[v]={label[v]}; continue
    fx=[u for u in adj[v] if fixed[u]]
    dom[v]={L for L in range(NC) if all(NE[L][label[u]] for u in fx) and all(L!=label[u] for u in fx)}
ch=True; it=0
while ch:
    ch=False; it+=1
    for v in label:
        if fixed[v]: continue
        nd={L for L in dom[v] if all(any(NE[L][M] for M in dom[u]) for u in adj[v])}
        if nd!=dom[v]: dom[v]=nd; ch=True
sz=Counter(min(len(dom[v]),50) for v in label if not fixed[v])
print('domain sizes',sorted(sz.items()))
print('labels in own domain', all(label[v] in dom[v] for v in label))
pickle.dump(dom,open('dom.pkl','wb'))
