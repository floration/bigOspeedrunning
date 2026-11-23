import pickle,json,numpy as np,sys
sys.path.insert(0,'/home/claude/work')
from lin import *
from rebuild import rd,split
ws=pickle.load(open('/home/claude/work/words.pkl','rb'))
w=ws['presplit']; j=rd('HELPER-SPLITS.json')
for ev in j['splits']:
    val=forward(w); b=adjoint(w)
    s={i:fm(q) for i,q in ev['covector']}; wd={i:fm(q) for i,q in ev['direction']}
    rd_=np.zeros(len(w['initial']),dtype=np.int64)
    for k,q in ev['read']: rd_=(rd_+val[k]*fm(q))%P
    nzr={i:int(x) for i,x in enumerate(rd_) if x}
    print('read form support',len(nzr),'covector',len(s),'equal up to scale?')
    sc=nzr[ev['role']]*pow(s[ev['role']],P-2,P)%P if ev['role'] in nzr else None
    print(' match', sc is not None and all((s.get(i,0)*sc-nzr.get(i,0))%P==0 for i in set(s)|set(nzr)), 'scale',sc)
    psi=np.zeros(len(w['initial']),dtype=np.int64)
    for k,q in ev['inject']: psi=(psi+b[k]*fm(q))%P
    nzp={i:int(x) for i,x in enumerate(psi) if x}
    print(' psi support',sorted(nzp),'direction',sorted(wd))
    print(' initial/final of w roles',[(w['initial'][i],w['final'][i]) for i in wd])
    moves={k:(a,bb) for k,a,bb in w['moves']}
    print(' read donors',[(k, moves.get(k)) for k,_ in ev['read']],'inject rows',[(k,moves.get(k)) for k,_ in ev['inject']])
    print(' support of s: start charts',set(w['initial'][i] for i in s),'end',set(w['final'][i] for i in s))
    w=json.loads(json.dumps(split(w,ev)))
