import random, math
from rmc import graph, resolve, dag_size, run
import checker2 as ck
def P(a,b): return (a+b)*(a+b+1)//2+b
def U(z):
    w=(math.isqrt(8*z+1)-1)//2; t=w*(w+1)//2; y=z-t; return w-y,y
def term(sym,env):
    st=[]
    for s in sym:
        if s=='=': b=st.pop();a=st.pop();st.append(P(a,b))
        elif s in ('-','~'): st.append(P(1 if s=='-' else 2, st.pop()))
        elif s in ('+',';'): b=st.pop();a=st.pop();st.append(P(3 if s=='+' else 4,P(a,b)))
        elif s[0]=='v': st.append(env[s[1]])
        else: st.append(0)
    return st[-1]
def ref(Mv, AXS):
    N=Mv; S=[]
    def pop(): return S.pop() if S else 0
    def read():
        nonlocal N; a,N=U(N); return a
    while N>0:
        cmd=read()
        if cmd==0:
            V=read(); x,yz=U(V); y,z=U(yz); j=min(read(),len(AXS)-1); S.append(term(AXS[j],[x,y,z]))
        elif cmd==1: l,r=U(pop()); S.append(P(r,l))
        elif cmd==2:
            e2=pop(); e1=pop(); b2,c=U(e2); a,b=U(e1); S.append(P(a,c) if b==b2 else 0)
        elif cmd in (3,4):
            k=1 if cmd==3 else 2; l,r=U(pop()); S.append(P(P(k,l),P(k,r)))
        else:
            k=3 if cmd==5 else 4; c,d=U(pop()); a,b=U(pop()); S.append(P(P(k,P(a,c)),P(k,P(b,d))))
        t,r=U(S[-1]) if S else (0,0)
        if r==P(1,t): return 'halt',S
    return 'end',S
def machine(g, Mv, maxsteps=3_000_000):
    r=[0]*9; r[0]=Mv; pc=0; started=False
    for _ in range(maxsteps):
        op,a,t1,t2=g[pc]
        if op=='CH': return 'halt',r
        if op=='CI': r[a]+=1; nxt=t1
        elif op=='CD':
            if r[a]==0: nxt=t1
            else: r[a]-=1; nxt=t2
        else: nxt=t1
        if nxt==0 and started: return 'end', r
        started=True; pc=nxt
    return 'timeout',r
def stack_list(Sv):
    out=[]
    while Sv>0: e,Sv=U(Sv-1); out.append(e)
    return out[::-1]
def enc(cmds):
    N=0
    for c in reversed(cmds): N=P(c,N)
    return N
x,y,z=('v',0),('v',1),('v',2)
AXS=ck.RA_SYMS
rows=resolve(ck.program()); g=graph(rows)
print('leaves',len(rows),'distinct subtrees',dag_size(rows)[0])
random.seed(2); ok=bad=0
for trial in range(1500):
    cmds=[]
    for _ in range(random.randrange(1,4)):
        c=random.choice([0,0,1,2,3,4,5,6]); cmds.append(c)
        if c==0: cmds += [random.randrange(4), random.randrange(10)]
    Mv=enc(cmds)
    if Mv>4000: continue
    rs,rS=ref(Mv,AXS); ms,mr=machine(g,Mv)
    if ms=='timeout': continue
    good = (ms=='halt') if rs=='halt' else (ms=='end' and stack_list(mr[2])==rS and mr[0]==Mv+1)
    ok+=good; bad+=not good
    if not good and bad<4: print('MISMATCH',cmds,Mv,rs,rS,ms,stack_list(mr[2]),mr)
print('agree',ok,'disagree',bad)
bog=resolve(ck.program([[x,x,'-','=']]+AXS)); print('bogus axiom x = -x, search from blank:', run(bog,[0]*9,max_steps=10**7)[0])
