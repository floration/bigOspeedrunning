import json,gzip,sys
from collections import defaultdict,Counter
d=json.load(gzip.open(sys.argv[1]))
pub=d['public']; prog=d['program']; F=d['frames']
dim={int(k):v['dim'] for k,v in F.items()}
fr=dict(enumerate(d['start'])); val={i:1<<i for i in range(pub)}
L=defaultdict(list)   # chart -> available values (inputs)
for i in range(pub): L[d['start'][i]].append(('in',i,1<<i))
Dl=defaultdict(list); Ol=defaultdict(list)
for t,ins in enumerate(prog):
    op=ins[0]
    if op=='INIT': fr[ins[1]]=ins[2]; val[ins[1]]=0
    elif op=='ADD':
        y,x,s=ins[1],ins[2],ins[3]; assert fr[y]==fr[x]==s; val[y]^=val[x]
    elif op=='MOVE':
        f,a,b=ins[1],ins[2],ins[3]; assert fr[f]==a
        Ol[a].append((t,f,val[f])); Dl[b].append((t,f,val[f])); fr[f]=b
    elif op=='SWAP':
        a,b=ins[1],ins[2]; fr[a],fr[b]=fr[b],fr[a]; val[a],val[b]=val[b],val[a]
    elif op=='CLEAR':
        fr.pop(ins[1]); val.pop(ins[1])
for i in range(pub): Ol[d['final'][i]].append(('out',i,val[i]))
def rk(vs):
    basis=[]
    for v in vs:
        for b in basis: v=min(v,v^b)
        if v: basis.append(v)
    return len(basis)
tot=0; rows=[]
for c in sorted(set(L)|set(Dl)|set(Ol)):
    l=[x[2] for x in L[c]]; dd=[x[2] for x in Dl[c]]; o=[x[2] for x in Ol[c]]
    rl,rld,rlo,rall=rk(l),rk(l+dd),rk(l+o),rk(l+dd+o)
    assert rall==rld,c
    ex=rld-rlo; dep=len(dd)-(rld-rl)
    if ex or dep: rows.append((c,dim[c],len(l),len(dd),len(o),ex,dep)); tot+=ex
print('moves',sum(len(v) for v in Dl.values()),'charts with excess/dependency',len(rows),'total excess',tot,'total dep',sum(r[6] for r in rows))
for r in rows[:60]: print(r)
