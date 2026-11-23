exec(open('bypass.py').read().split("CNT=Counter()")[0])
CNT=Counter(); hits=[]; t0=time.time()
for ei,((b,c),bc) in enumerate(edge.items()):
    if ei%200==0: print("progress",ei,len(edge),dict(CNT),round(time.time()-t0),flush=True)
    Bv=[U[k] for k in bc]
    good_a1=[]
    for a1 in inn[b]:
        ab=set(edge[(a1,b)])
        Q=Basis(n)
        for k in at[b]:
            if k not in ab: Q.add(U[k])
        for k in outof[b]:
            if k not in bc: Q.add(U[k])
        if any(not Q.contains(v) for v in Bv): good_a1.append((a1,Q))
    if not good_a1: continue
    CNT['edges escaping']+=1
    Cv=[U[k] for k in at[c] if not any((desc[x]>>idx[k])&1 for x in bc)]
    if len(Cv)>60: CNT['skip big C']+=1; continue
    for a2 in at:
        if a2==b or not nested(a2,c): continue
        gs=[(pr(abs(R[b]-R[a1]))+pr(abs(R[c]-R[b]))-pr(abs(R[c]-R[a2])),a1,Q) for a1,Q in good_a1]
        gs=[g for g in gs if g[0]>1e-9]
        if not gs: continue
        CNT['a2 tested']+=1
        SA=span_at(a2)
        rB=[SA.reduce(v) for v in Bv]; rC=[SA.reduce(v) for v in Cv]
        ker=kernel_combos(rB+rC)
        X=[x[:len(bc)] for x in ker if x[:len(bc)].any()]
        if not X: continue
        CNT['I2']+=1
        I2=[sum((Bv[t]*int(x[t]))%P for t in range(len(bc)))%P for x in X]
        for g,a1,Q in gs:
            if any(not Q.contains(u) for u in I2):
                hits.append((g,a1,b,c,a2)); print('HIT',hits[-1],flush=True)
print(CNT); print('hits',len(hits),time.time()-t0)
json.dump(hits,open('bypass3_hits.json','w'))
