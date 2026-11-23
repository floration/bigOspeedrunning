from fractions import Fraction as Q
GC=Q(17145637307,2**42); stop=Q(5,10**18); ETA=Q(39,10000)
def upper(ranks,debit,cB):
    rate=Q(0)
    for i,h in enumerate(ranks,1):
        rate=min(ETA,(249*(cB-debit/h)+rate)/250)
        if i<len(ranks): rate=Q((rate*10**21).__floor__()-1,10**21)
    return rate
def pos(G): return GC-Q(64939,524288*G)
def best(debit,cap,Grange,cB):
    out=[]
    for G in Grange:
        h2=(cap-1731-220*G)//320-8192-524288
        if not 8192<=h2<=524288: continue
        r=(8192,h2,524288); v=min(upper(r,debit,cB),pos(G))-stop
        out.append((v,G,r))
    return max(out)
D=Q(1430037,2**20); cap=318292011
cB0=Q(4391986206293,2**50)
b=best(D,cap,range(511000,512000),cB0); print('base',float(b[0]),b[1:])
for dc in [1e-9,2e-9,3e-9,4e-9,5e-9,6e-9,1e-8,1e-7,1.5e-6]:
    cB=cB0+Q(dc).limit_denominator(10**15)
    b=best(D,cap,range(505000,524289,1),cB); print('dc',dc,float(b[0]),b[1:], 'gain',float(b[0]-Q('0.003898224460300')))
