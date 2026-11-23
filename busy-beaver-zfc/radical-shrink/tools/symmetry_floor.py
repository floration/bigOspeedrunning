import json,sys
rows=json.load(open(sys.argv[1]))
root={}
for p,o,a in rows:
  at=root
  for b in p: at=at.setdefault(b,{})
  at['i']=(o,a)
def T(n): return n['i'] if 'i' in n else (T(n['0']),T(n['1']))
t=T(root)
def leaves(x):
  return [x] if isinstance(x[0],str) else leaves(x[0])+leaves(x[1])
def canon_regs(x):
  # rename registers by first occurrence
  m={}
  def f(y):
    if isinstance(y[0],str):
      o,a=y
      if o in('CI','CD'):
        if a not in m: m[a]=len(m)
        return (o,m[a])
      return y
    return (f(y[0]),f(y[1]))
  return f(x)
def canon_ctrl(x):
  def f(y):
    if isinstance(y[0],str):
      o,a=y; return (o,'*') if o in ('CB','CC') else y
    return (f(y[0]),f(y[1]))
  return f(x)
def count(t,key):
  seen={}
  def v(x):
    k=key(x)
    if k in seen: return
    seen[k]=1
    if not isinstance(x[0],str): v(x[0]); v(x[1])
  v(t); return len(seen)
print('plain',count(t,lambda x:x))
print('mod register renaming',count(t,canon_regs))
print('mod control-depth args',count(t,canon_ctrl))
print('mod both',count(t,lambda x:canon_ctrl(canon_regs(x))))
print('shape only',count(t,lambda x: (lambda f: f(f,x))(lambda f,y: 'L' if isinstance(y[0],str) else (f(f,y[0]),f(f,y[1])))))
