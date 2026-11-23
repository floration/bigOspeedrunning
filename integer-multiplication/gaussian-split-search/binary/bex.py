import sys,pickle
sys.path.insert(0,'/home/claude/work/binary')
from bscan import *
p=sys.argv[1]
d=load(p); res,w,moves,val,pairs,main=check(d,verbose=False); madj,inadj=adjoint(w); pub=w.pub
X=[i for i in range(pub) if d['start'][i]!=0]; mX=sum(1<<i for i in X)
def Minv(bm):
    r=bm
    for x,y in pairs:
        if bm>>x&1: r^=1<<y
    return r
o=pickle.load(open(p.split('/')[-1]+'.bidir2.pkl','rb'))['one']
bt={t:(t,f,a,b,v) for t,f,a,b,v in moves}
both=[x for x in o if x[3]]
sup=lambda m:[i for i in range(pub) if m>>i&1]
det=Counter()
for l,t1,t2,_ in both:
    _,f1,a,b,u1=bt[t1]; _,f2,_,_,u2=bt[t2]
    z1=Minv(madj[t1]); z2=Minv(madj[t2]); pr=lambda x,y:bin(x&y).count('1')&1
    D=((1^pr(u2,z1))*(1^pr(u1,z2)) ^ pr(u2,z2)*pr(u1,z1))&1
    det[D]+=1
print('invertible',det)
for l,t1,t2,_ in both[:6]:
    _,f1,a,b,u1=bt[t1]; _,f2,_,_,u2=bt[t2]
    print(l,w.D[l[0]],w.D[l[1]],'t',t1,t2,'u1',sup(u1)[:8],len(sup(u1)),'u2',sup(u2)[:8],len(sup(u2)),'b1',sup(madj[t1])[:6],len(sup(madj[t1])),'b2',sup(madj[t2])[:6],len(sup(madj[t2])))
print(Counter((w.D[l[0]],w.D[l[1]]) for l,t1,t2,_ in both))
# are u's helpers only?
hm=sum(1<<i for i in range(pub) if i not in main)
print('u supports on helpers only', Counter((bt[t1][4]&~hm==0, bt[t2][4]&~hm==0) for l,t1,t2,_ in both))
print('b supports on helpers only', Counter((madj[t1]&~hm==0, madj[t2]&~hm==0) for l,t1,t2,_ in both))
