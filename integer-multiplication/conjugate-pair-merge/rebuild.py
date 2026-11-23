# Own re-implementation of the delta format (parent -> child) from #8027's BIDIRECTIONAL.md description.
import json,gzip,sys
from fractions import Fraction
from graphlib import TopologicalSorter
D='/home/claude/w27/research/p104-live-relative-gain/'
def rd(n): return json.load(gzip.open(D+n))
def apply(parent,delta):
    moves={k:(a,b) for k,a,b in parent['moves']}; forms={k:dict(r) for k,r in parent['forms']}
    for k in delta['removed']: del moves[k],forms[k]
    for k,a,b in delta['moves']: moves[k],forms[k]=(a,b),{}
    lit={}
    for k,kind,ent in delta['differences']:
        wts={j:Fraction(s) for j,s in ent}
        if kind=='add': ch=wts; lit[k]=ch
        else:
            ch={}
            for j,wt in wts.items():
                for d,v in lit[j].items(): ch[d]=ch.get(d,0)+wt*v
        row=forms[k]
        for j,v in ch.items():
            c=Fraction(row.get(j,'0'))+v
            if c: row[j]=str(c)
            else: row.pop(j,None)
    deps={k:tuple(j for j in sorted(r) if j>=0) for k,r in sorted(forms.items())}
    return dict(parent,forms=[[k,sorted(r.items())] for k,r in sorted(forms.items())],
                moves=[[k,a,b] for k,(a,b) in sorted(moves.items())],schedule=list(TopologicalSorter(deps).static_order()))
w=rd('WORD.json.gz'); w=apply(w,rd('BIDIRECTIONAL.json.gz')); json.dump(w,gzip.open('/home/claude/cp/w5680.json.gz','wt'))
w=apply(w,rd('BIDIRECTIONAL-QUOTIENT.json.gz')); json.dump(w,gzip.open('/home/claude/cp/w5676.json.gz','wt'))
print(len(w['moves']))
