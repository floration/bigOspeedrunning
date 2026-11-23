# Independent rebuild of #8027's final complex word (own code; reads package data files only).
import json,gzip,hashlib,sys,pickle
from fractions import Fraction
from graphlib import TopologicalSorter
D='/home/claude/cs/research/p104-live-relative-gain/'
def rd(n):
    raw=open(D+n,'rb').read()
    return json.loads(gzip.decompress(raw) if raw[:2]==b'\x1f\x8b' else raw)
def sha(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def recon(parent,delta):
    assert sha(parent)==delta['parent']
    moves={k:(a,b) for k,a,b in parent['moves']}; forms={k:dict(r) for k,r in parent['forms']}
    for k in delta['removed']: del moves[k],forms[k]
    for k,a,b in delta['moves']: moves[k]=(a,b); forms[k]={}
    lit={}
    for k,kind,ent in delta['differences']:
        w={j:Fraction(s) for j,s in ent}
        if kind=='add': ch=w; lit[k]=ch
        else:
            ch={}
            for j,x in w.items():
                for d,v in lit[j].items(): ch[d]=ch.get(d,0)+x*v
            ch={j:v for j,v in ch.items() if v}
        row=forms[k]
        for j,v in ch.items():
            c=Fraction(row.get(j,'0'))+v
            if c: row[j]=str(c)
            else: del row[j]
    deps={k:tuple(j for j in sorted(r) if j>=0) for k,r in sorted(forms.items())}
    w=dict(parent,forms=[[k,sorted(r.items())] for k,r in sorted(forms.items())],
           moves=[[k,a,b] for k,(a,b) in sorted(moves.items())],
           schedule=list(TopologicalSorter(deps).static_order()))
    w=json.loads(json.dumps(w))
    assert sha(w)==delta['word'],'hash'
    return w
def addto(row,donor,f):
    for i,v in donor.items():
        n=row.get(i,0)+v*f
        if n: row[i]=n
        else: row.pop(i,None)
def split(word,ev):
    first=word['first_output']; ini=word['initial'][:]; fin=word['final'][:]
    role,chart=ev['role'],ev['chart']; fresh=len(ini)
    L=lambda e:{i:Fraction(q) for i,q in e}
    rows={k:L(e) for k,e in word['forms']}
    s,w=L(ev['covector']),L(ev['direction'])
    pairing=sum(s.get(i,0)*v for i,v in w.items()); assert pairing and w.get(role)
    sub={~i:-v/pairing for i,v in s.items() if i!=role}; sub[~role]=1/pairing
    def cs(row):
        c=sum(row.get(~i,0)*v for i,v in w.items()); row.pop(~role,None)
        if c: addto(row,sub,c)
    for r in rows.values(): cs(r)
    obs=L(ev['read']); cs(obs)
    diff={~fresh:1/pairing}; addto(diff,obs,-1/pairing)
    for k,c in L(ev['inject']).items(): addto(rows[k],diff,c)
    rec={}
    for i,v in s.items(): addto(rec,rows[first+i],v)
    old=rows[first+role]
    for i,v in w.items():
        if i!=role: addto(rows[first+i],old,-v/w[role])
    rows[first+role]=obs; rows[first+fresh]=rec
    ini.append(chart); fin.append(fin[role]); fin[role]=chart
    deps={k:tuple(j for j in sorted(r) if j>=0) for k,r in sorted(rows.items())}
    return dict(word,initial=ini,final=fin,schedule=list(TopologicalSorter(deps).static_order()),
                forms=[[k,[[j,str(q)] for j,q in sorted(r.items())]] for k,r in sorted(rows.items())])
if __name__=='__main__':
    w=rd('WORD.json.gz')
    w=recon(w,rd('BIDIRECTIONAL.json.gz')); print('bidir ok')
    w=recon(w,rd('BIDIRECTIONAL-QUOTIENT.json.gz')); print('quot ok')
    j=rd('HELPER-SPLITS.json'); assert sha(w)==j['parent']
    pre=w
    for e in j['splits']: w=split(w,e)
    w=json.loads(json.dumps(w)); print('split', sha(w)==j['word'])
    w=recon(w,rd('BANK-FACTORS.json.gz')); print('bank ok')
    pickle.dump(dict(presplit=pre,final=w),open('/home/claude/work/words.pkl','wb'))
