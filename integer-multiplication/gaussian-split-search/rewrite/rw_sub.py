import pickle,json,numpy as np,sys
sys.path.insert(0,'/home/claude/work')
from lin import *
from chk import expected
ws=pickle.load(open('/home/claude/work/words.pkl','rb')); w=ws['final']
n=len(w['initial']); first=w['first_output']
moves={k:(a,b) for k,a,b in w['moves']}; forms=dict(w['forms'])
val=forward(w); b=adjoint(w)
F=[int(x) for x in sys.argv[1].split(',')]
pos={k:i for i,k in enumerate(w['schedule'])}
print('fields',[(i,w['initial'][i],w['final'][i]) for i in F])
from build import ratrec
def show(v): 
    nz=np.nonzero(v)[0]; return ' '.join(f'{i}:{ratrec(int(v[i]))}' for i in nz[:10])+(f' ...({len(nz)})' if len(nz)>10 else '')
for k in w['schedule']:
    if any(val[k][i] for i in F) or any(b[k][i] for i in F):
        loc=moves.get(k,('out',w['final'][k-first] if k>=first else None))
        print(pos[k],k,loc,'form',show(val[k]),'| adj',show(b[k]),'| row',forms[k][:6])
