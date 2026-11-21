from mpmath import mp, mpf, log, findroot
mp.dps=40
H=lambda x: -x*log(x)-(1-x)*log(1-x)
def Gam(c,t): return (c*H(1/c)-c*H((1-t)/c)-t*log(9))/log(4)
def q(t): return (H(t)+t*log(9))/log(4)
def alpha(c):
    t=findroot(lambda t: Gam(c,t)+q(t)-mpf(1)/2, 0.113)
    B=(c-1)*log(3)/log(4)
    s=1/(2*B-mpf(1)/2+2*Gam(c,t))
    return 3-2*Gam(c,t)*s, t, s, Gam(c,t), q(t), B
for c in [12,14,16,18,19,20,21,22,24,26,30]:
    a,t,s,G,qq,B=alpha(mpf(c)); print(c, mp.nstr(a,16), mp.nstr(t,12), mp.nstr(s,12))
a,t,s,G,qq,B=alpha(mpf(20)); print("c=20 limit", a, "G",G,"q",qq,"B",B,"sigma",s)
print("fw sigma",mpf(136966)/4074237, "theta", mpf(155816)/1377219)
from mpmath import diff, findroot
f=lambda c: alpha(c)[0]
cs=findroot(lambda c: diff(f,c), 20.2)
print("best real c", cs, f(cs), "gain vs 20:", f(mpf(20))-f(cs))
for c in ["19.8","20.1","20.2","20.25","20.3"]:
    print(c, mp.nstr(f(mpf(c)),16))
