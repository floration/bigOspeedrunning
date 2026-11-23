from rmc import *
import random
def mov(a,b): return while_dec(a, CI(b))
def unpair(c,x,y): return while_dec(c, ifpos(x, CI(y), [mov(y,x), CI(x)]))
def pair(x,y,z): return loop(lambda L: ifpos(y, [CI(x), CI(z)], ifpos(x, [mov(x,y), CI(z)], brk(L))))
def P(a,b): return (a+b)*(a+b+1)//2+b
def prog(*xs): return resolve(seq(*xs, CH()))
for _ in range(200):
    a,b=random.randrange(30),random.randrange(30)
    st,r,_=run(prog(pair(0,1,2)), [a,b,0]+[0]*6); assert st=='halt' and r[2]==P(a,b) and r[0]==r[1]==0,(a,b,r)
    st,r,_=run(prog(unpair(2,0,1)), [0,0,P(a,b)]+[0]*6); assert st=='halt' and (r[0],r[1])==(a,b),(a,b,r)
print('pair/unpair ok')
