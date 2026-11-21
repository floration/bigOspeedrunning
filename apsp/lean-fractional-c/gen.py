from fractions import Fraction as F
import math
c=F(502,25); th=F(225677,1996332); sg=F(152980,4570079)
w=1-th; cm1=c-1; s=cm1+th; r=s/cm1
def ser(z,n=40):
    S=sum(z**(2*i+1)/(2*i+1) for i in range(n))
    return 2*S, 2*(S+z**(2*n+1)/(1-z*z))
P=10**24
def encl(y):
    z=(y-1)/(y+1); lo,hi=ser(z)
    a=math.floor(lo*P); b=a+1
    # need a/P < lo and hi < b/P  (strict); else widen
    while not (F(a,P)<lo): a-=1
    b=math.ceil(hi*P)
    if F(b,P)<=hi: b+=1
    return z,a,b
items={ # name: (y, description)
 'Two':F(2),'ThreeHalf':F(3,2),'W2':2*w,'R':r,'S16':s/16,'Theta16':16*th,'C16':c/16,'Cm116':cm1/16}
out={}
for k,y in items.items():
    assert 1<y<2 or y==2, (k,y)
    z,a,b=encl(y); out[k]=(y,z,a,b); print(k,y,z,a,b, b-a)
import json; json.dump({k:[str(v[0]),str(v[1]),v[2],v[3]] for k,v in out.items()},open('encl.json','w'),indent=1)
