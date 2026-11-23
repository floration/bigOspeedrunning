exec(open('bypass.py').read().split("CNT=Counter()")[0])
def span_excl(ch,bad):
    Bs=Basis(n)
    for k in at[ch]:
        if not any((desc[x]>>idx[k])&1 for x in bad): Bs.add(U[k])
    return Bs
def check(a1,b,c,a2):
    bc=edge[(b,c)]; Bv=[U[k] for k in bc]
    ab=set(edge[(a1,b)])
    Q=Basis(n)
    for k in at[b]:
        if k not in ab: Q.add(U[k])
    for k in outof[b]:
        if k not in bc: Q.add(U[k])
    C=span_excl(c,bc); SA=span_excl(a2,bc)
    J=Basis(n)
    for M_ in (SA,C):
        for row in M_.M: J.add(row)
    res=[J.reduce(v) for v in Bv]
    ker=kernel_combos(res) if any(r.any() for r in res) else [np.eye(len(bc),dtype=np.int64)[i] for i in range(len(bc))]
    I2=[sum((Bv[t]*int(x[t]))%P for t in range(len(bc)))%P for x in ker]
    ok=[u for u in I2 if not Q.contains(u)]
    print(a1,b,c,a2,'|SA|',len(SA),'full',len(span_at(a2)),'|C|',len(C),'I2',len(I2),'escape',len(ok))
    return ok
if __name__=='__main__':
    import sys
    for h in json.load(open(sys.argv[1])) if len(sys.argv)>1 else [(0,3,597,652,653),(0,3,597,652,773)]:
        check(*h[1:])
