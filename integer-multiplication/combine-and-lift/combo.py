# Combined model: #8073 base + our floor retune (L=4474, s=186/25, 2^-20 grid) + #8076 child tariff 2401/1024.
from fractions import Fraction as Q
from decimal import Decimal as D, getcontext
getcontext().prec=90
cB=Q(4391986206293,2**50); GC=Q(17145637307,2**42); stop=Q(5,10**18); ETA=Q(39,10000)
delta=Q(1,2**128); ln2=D(2).ln()
def dec(q): return D(q.numerator)/D(q.denominator)
def F_upper(L,s,tariff):
    m=tariff*Q(256,255)*Q(4097,4096)*Q(1028,1024)*(1+Q(s)/L+delta)/((1-Q(10,L))*(1-delta)**3)
    return dec(m)*(D(1024*134*L).ln()*dec(cB)).exp()*(1+D(10)**-70)
def allow_lower(num,den): return (ln2*D(num)/D(den)).exp()*(1-D(10)**-70)
def upper(ranks,debit):
    rate=Q(0)
    for i,h in enumerate(ranks,1):
        rate=min(ETA,(249*(cB-debit/h)+rate)/250)
        if i<len(ranks): rate=Q((rate*10**21).__floor__()-1,10**21)
    return rate
def pos(G): return GC-Q(64939,524288*G)
def best(debit,cap,base,Grange,hmax=524288):
    out=[]
    for G in Grange:
        h2=(cap-base-220*G)//320-8192-hmax
        if not 8192<=h2<=hmax: continue
        r=(8192,h2,hmax); v=min(upper(r,debit),pos(G))-stop
        out.append((v,G,r,base+320*sum(r)+220*G))
    return max(out)
def debit(L,s,tariff,den):
    f=F_upper(L,s,tariff); num=int(f.ln()/ln2*den)+1
    assert allow_lower(num,den)>f; return Q(num,den)
T76=Q(2401,1024); T73=Q(47,20)
if __name__=="__main__":
    # sanity: reproduce 8076 and our 1b
    D76=Q(11178,8192)
    print('8076 repro', best(D76,318291911,1740,range(509000,510500)))
    D1b=Q(1430037,2**20); print('1b repro', best(D1b,318292011,1731,range(511000,512000)))
    s=Q(186,25)
    bL=min(range(3000,8000,2),key=lambda L:F_upper(L,s,T76)); print('best L',bL)
    for den in (8192,2**20):
        Dc=debit(4474,s,T76,den); print('combined debit',den,Dc,float(Dc*8192))
        for cap in (318292011,318291911):
            v,G,r,clk=best(Dc,cap,1740,range(511000,520000)); print(' cap',cap,'G',G,r,'clk',clk,'sup %.18f'%float(v), 'install', str(Q(int(v*10**15),10**15)))
