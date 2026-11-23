# Enumerate chart-3 data relay chains a->...->127 (all transfers uX0) and the concavity value of a direct a->127 shortcut.
import json,gzip,sys,numpy as np,collections,math
sys.path.insert(0,'/home/claude/cp'); from uz import compute,p
w=json.load(gzip.open(sys.argv[1])); R=compute(w)
U,Z,X,idx,forms=R['U'],R['Z'],R['X'],R['idx'],R['forms']
mv={k:(a,b) for k,a,b in w['moves']}; F=w['frames']; rk=[len(f) for f in F]
uX0={k for k in mv if not U[idx[k]][X].any()}; z0={k for k in mv if not Z[idx[k]].any()}
def span(B):
    s={0}
    for v in B: s|={o^v for o in s}
    return frozenset(s)
S=[span(f) for f in F]
c=0.0038984814
def gain(gs):  # paid mass saved per call by one direct move of grade sum(gs)
    return sum(g**(1-c) for g in gs)-sum(gs)**(1-c)
out=[]
for t,(a,b) in mv.items():
    if b!=127 or t not in uX0: continue
    # walk back: donors of t that are uX0 transfers into a
    chain=[t]; cur=t
    while True:
        prev=[d for d,_ in forms[cur] if d>=0 and d in uX0 and d in mv and mv[d][1]==mv[cur][0]]
        if len(prev)!=1: break
        cur=prev[0]; chain.append(cur)
    if len(chain)<2: continue
    chain=chain[::-1]; a0=mv[chain[0]][0]
    gs=[rk[mv[k][1]]-rk[mv[k][0]] for k in chain]
    out.append(dict(chain=chain,charts=[mv[chain[0]][0]]+[mv[k][1] for k in chain],grades=gs,z0=[k in z0 for k in chain],gain_per_call=gain(gs)))
out.sort(key=lambda d:-d['gain_per_call'])
print('uX0 transfers into 127:',sum(1 for t,(a,b) in mv.items() if b==127 and t in uX0),' chains (single-predecessor walk, len>=2):',len(out))
for d in out[:15]: print(d)
json.dump(out,open(sys.argv[2],'w'),indent=0)
