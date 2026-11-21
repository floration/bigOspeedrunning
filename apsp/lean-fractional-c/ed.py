import sys
def ed(p, pairs):
    t=open(p).read()
    for a,b in pairs:
        if t.count(a)==0: raise SystemExit(f"MISSING in {p}: {a[:80]!r}")
        t=t.replace(a,b)
    open(p,'w').write(t)
