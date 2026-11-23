import sys; sys.path.insert(0,'/tmp/claude-0/w/s')
from load import *
from collections import Counter
w,moves,forms,val,chart,src=load(sys.argv[1])
frames=w['frames']
def span(basis):
    pts={0}
    for v in basis: pts|={o^v for o in pts}
    return frozenset(pts)
S=[span(f) for f in frames]; R=[len(f) for f in frames]; nf=len(frames)
L=defaultdict(list); D=defaultdict(list)
for i,s in enumerate(w['initial']): L[s].append(~i)
for k,(a,b) in moves.items(): D[b].append(k)
def coords_intersection(Vvecs, Wvecs):
    # solve sum x_i V_i = sum y_j W_j ; return y-part basis (coords in W basis)
    if not Vvecs or not Wvecs: return []
    M=np.array(Vvecs+[(-x)%p for x in Wvecs],dtype=np.int64).T
    return [z[len(Vvecs):] for z in nullvec(M)]
hits=[]; tested=0
for b in range(nf):
    if not D[b]: continue
    Wl=L[b]+D[b]; Wv=[val[x] for x in Wl]
    gmax=max(abs(R[b]-R[moves[k][0]]) for k in D[b])
    for a2 in range(nf):
        if a2==b or not (S[a2]<S[b] or S[b]<S[a2]): continue
        g2=abs(R[b]-R[a2])
        if g2>=gmax: continue
        Vv=[val[x] for x in L[a2]+D[a2]]
        if not Vv: continue
        tested+=1
        ys=coords_intersection(Vv,Wv)
        for i,x in enumerate(Wl):
            if x<0: continue
            g=abs(R[b]-R[moves[x][0]])
            if g2<g and any(int(y[i]) for y in ys):
                hits.append((x,moves[x],g,a2,g2))
print('pairs tested',tested,'hits',len(hits)); print(Counter((h[2],h[4]) for h in hits))
for h in hits[:30]: print(h)
import json; json.dump(hits,open('/tmp/claude-0/w/d/cres_hits.json','w'))
