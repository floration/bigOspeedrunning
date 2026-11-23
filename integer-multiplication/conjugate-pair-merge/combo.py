import json,sys
exec(open('relay_check.py').read().split('out=collections')[0])
G=json.load(open('good5674.json'))
def buildmany(cs):
    nf={k:dict(v) for k,v in forms.items()}; labs=[]
    for t,c in enumerate(cs):
        x,y=c['x'],c['y']; D=newlab+t; labs.append(D)
        nf[D]=dict(nf[x]); del nf[x],nf[y]
        for k in nf:
            nf[k].pop(x,None); nf[k].pop(y,None)
        for key,v in c['dK'].items():
            r,i=map(int,key.split(',')); nf[r][i]=(nf[r].get(i,0)+v)%p
        for r,v in c['cc'].items(): nf[int(r)][D]=(nf[int(r)].get(D,0)+v)%p
    return nf,labs
nf,labs=buildmany(G); print('all five jointly:',check(nf))
