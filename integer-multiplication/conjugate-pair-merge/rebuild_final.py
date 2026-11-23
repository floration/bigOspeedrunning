import json,gzip,hashlib,sys
from fractions import Fraction as Q
from graphlib import TopologicalSorter
sys.path.insert(0,'/home/claude/cp')
D='/home/claude/w27/research/p104-live-relative-gain/'
canon=lambda v: hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
exec(open('/home/claude/cp/rebuild.py').read().split("w=rd('WORD")[0])
def add(row,donor,f):
    for i,v in donor.items():
        x=row.get(i,0)+v*f
        if x: row[i]=x
        else: row.pop(i,None)
def split(word,ev):
    first=word['first_output']; ini,fin=word['initial'][:],word['final'][:]
    role,chart=int(ev['role']),int(ev['chart']); fresh=len(ini)
    assert (ini[role],fin[role])==(3,127)
    L=lambda e:{int(i):Q(q) for i,q in e}
    rows={k:L(e) for k,e in word['forms']}
    s,wv=L(ev['covector']),L(ev['direction'])
    pr=sum(s.get(i,0)*v for i,v in wv.items())
    sub={~i:-v/pr for i,v in s.items() if i!=role}; sub[~role]=1/pr
    def cs(row):
        c=sum(row.get(~i,0)*v for i,v in wv.items()); row.pop(~role,None)
        if c: add(row,sub,c)
    for r in rows.values(): cs(r)
    obs=L(ev['read']); cs(obs)
    diff={~fresh:1/pr}; add(diff,obs,-1/pr)
    for k,c in L(ev['inject']).items(): add(rows[k],diff,c)
    rec={}
    for i,v in s.items(): add(rec,rows[first+i],v)
    old=rows[first+role]
    for i,v in wv.items():
        if i!=role: add(rows[first+i],old,-v/wv[role])
    rows[first+role]=obs; rows[first+fresh]=rec
    ini.append(chart); fin.append(fin[role]); fin[role]=chart
    deps={k:tuple(j for j in sorted(r) if j>=0) for k,r in sorted(rows.items())}
    return dict(word,initial=ini,final=fin,schedule=list(TopologicalSorter(deps).static_order()),
        forms=[[k,[[j,str(q)] for j,q in sorted(r.items())]] for k,r in sorted(rows.items())])
w=json.load(gzip.open('/home/claude/cp/w5676.json.gz'))
J=json.load(open(D+'HELPER-SPLITS.json'))
for ev in J['splits']: w=split(w,ev)
print('split hash',canon(w)==J['word'])
B=rd('BANK-FACTORS.json.gz'); w=apply(w,B); print('bank hash',canon(w)==B['word'],len(w['moves']))
json.dump(w,gzip.open('/home/claude/cp/w5674.json.gz','wt'))
