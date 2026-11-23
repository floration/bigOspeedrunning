import sys; sys.path.insert(0,'/tmp/claude-0/w/s')
from load import *
w,moves,forms,val,chart,src=load(sys.argv[1])
F=w['frames']; n=len(w['initial'])
L=defaultdict(list); D=defaultdict(list); O=defaultdict(list)
for i,s in enumerate(w['initial']): L[s].append(~i)
for k,(a,b) in moves.items(): D[b].append(k); O[a].append(k)
for k in forms:
    if k not in moves: O[src[k]].append(k)
avail=lambda c: [val[x] for x in L[c]+D[c]]
def intersect_pair(A,B):
    # vectors in span(A)∩span(B): solve sum a_i A_i - sum b_j B_j=0 ; return coefficient vectors on A
    M=np.array(A+B,dtype=np.int64).T  # n x (|A|+|B|)
    ks=nullvec(M)
    return [z[:len(A)]%p for z in ks]
charts=[int(x) for x in sys.argv[2:]] or [243,394,470,477,517,518,529,531,541,543,591,595,599,1091]
for b in charts:
    ins=L[b]+D[b]; idx={x:i for i,x in enumerate(ins)}
    C=[]
    for o in O[b]:
        row=np.zeros(len(ins),dtype=np.int64)
        for d,co in forms[o]: row[idx[d]]=(row[idx[d]]+modq(co))%p
        C.append(row)
    z=nullvec(C)[0]
    supp=[ins[i] for i in np.nonzero(z)[0]]
    groups=defaultdict(list)
    for x in supp: groups[moves[x][0]].append(x)
    for a,Da in groups.items():
        za=np.array([z[idx[x]] for x in Da])
        ok=True; det=[]
        for a2,Da2 in groups.items():
            if a2==a: continue
            cs=intersect_pair([val[x] for x in Da], avail(a2))
            good=any(int((c*za%p).sum()%p) for c in cs)
            det.append((a2,len(cs),good)); ok&=good
        g=abs(len(F[b])-len(F[a]))
        print('chart',b,'drop from',a,'(k=%d, grade %d)'%(len(Da),g),'OK' if ok else '-',det)
