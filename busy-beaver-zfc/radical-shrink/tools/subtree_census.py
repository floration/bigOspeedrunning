import json,sys,collections
rows=json.load(open(sys.argv[1]))
root={}
for p,o,a in rows:
  at=root
  for b in p: at=at.setdefault(b,{})
  at['i']=(o,a)
memo={};kids={};leafs={}
def h(n):
  if 'i' in n: k=('L',n['i'])
  else: k=(h(n['0']),h(n['1']))
  if k not in memo:
    memo[k]=len(memo); kids[memo[k]]=() if k[0]=='L' else k
  return memo[k]
r=h(root)
def reach(x,s):
  if x in s: return
  s.add(x)
  for c in kids[x]: reach(c,s)
pathnode={}
def walk(n,p):
  pathnode[p]=h(n)
  if 'i' not in n: walk(n['0'],p+'0'); walk(n['1'],p+'1')
walk(root,'')
tot=set();reach(r,tot);print('total',len(tot))
# for each path up to depth D: nodes reachable from it, nodes lost if removed (exclusive)
def excl(p):
  # nodes reachable from root without passing through subtree at p (by path, occurrence-based approximated by node)
  x=pathnode[p]; s=set()
  def rr(y,q):
    pass
  allr=set(); reach(x,allr)
  # nodes reachable from others: compute reach from root but blocking node x entirely
  other=set()
  def rb(y):
    if y==x or y in other: return
    other.add(y)
    for c in kids[y]: rb(c)
  rb(r)
  return len(allr), len(allr-other)
leafcount=collections.Counter()
for p,o,a in rows:
  for d in range(len(p)+1): leafcount[p[:d]]+=1
for p in sorted(pathnode,key=lambda q:(len(q),q)):
  if len(p)<=int(sys.argv[2]) or (len(sys.argv)>3 and p in sys.argv[3:]):
    a,e=excl(p); print(f'{p or "root":12} leaves={leafcount[p]:5} reach={a:4} exclusive={e:4}')
