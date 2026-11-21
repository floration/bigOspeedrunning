import json,sys
exec(open('rect.py').read())
d=json.load(open(sys.argv[1])); tx,ty=d['tx'],d['ty']
rects=[]
for X in range(15):
    for Y in range(15):
        nx=NODES[tx[X]]; ny=NODES[ty[Y]]
        memo={}
        def dp(s,t):
            if (s,t) in memo: return memo[(s,t)]
            src=[bases[X][p] for p in nx[s]]; tgt=[bases[Y][p] for p in ny[t]]
            if not any(orth[u][v] for u in src for v in tgt): memo[(s,t)]=(0,None); return memo[(s,t)]
            best=(float('inf'),None)
            if all(orth[u][v] for u in src for v in tgt): best=(pen(len(src),len(tgt)),'R')
            if s<8:
                c=dp(2*s,t)[0]+dp(2*s+1,t)[0]
                if c<best[0]: best=(c,'S')
            if t<8:
                c=dp(s,2*t)[0]+dp(s,2*t+1)[0]
                if c<best[0]: best=(c,'T')
            memo[(s,t)]=best; return best
        def emit(s,t):
            ch=dp(s,t)[1]
            if ch is None: return
            if ch=='R': rects.append((X,s,Y,t,[bases[X][p] for p in sorted(nx[s])],[bases[Y][p] for p in sorted(ny[t])]))
            elif ch=='S': emit(2*s,t); emit(2*s+1,t)
            else: emit(s,2*t); emit(s,2*t+1)
        emit(1,1)
cov=set()
for X,s,Y,t,src,tgt in rects:
    assert all(orth[u][v] for u in src for v in tgt)
    assert len(src)+len(tgt)<=8
    for u in src:
        for v in tgt:
            assert (u,v) not in cov; cov.add((u,v))
need={(u,v) for u in range(120) for v in range(120) if orth[u][v]}
assert cov==need, (len(cov),len(need))
print("rectangles",len(rects),"directed contacts",len(cov),"all orthogonal, disjoint, exact cover: OK")
hist={}
for r in rects: k=(len(r[4]),len(r[5])); hist[k]=hist.get(k,0)+1
print("histogram",sorted(hist.items()))
json.dump([{"src_basis":X,"src_node":s,"tgt_basis":Y,"tgt_node":t,"src_lines":src,"tgt_lines":tgt} for X,s,Y,t,src,tgt in rects],open(sys.argv[2],'w'))
json.dump({"roots":roots,"bases":bases,"source_trees":[TREES[i] for i in tx],"target_trees":[TREES[i] for i in ty]},open(sys.argv[3],'w'))
