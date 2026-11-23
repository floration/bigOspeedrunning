"""Tiny structured compiler into the K215 source language (CI/CD/CB/CC/CH binary trees),
plus an exact simulator of its semantics (copied from ProveIt's graph_intervals resolver).

Semantics (ProveIt source_language.py, graph_intervals):
  leaves run in order, wrapping; CI r: r+=1; CD r: if r==0 jump to the end of the nearest
  ancestor whose 0-child holds us, else r-=1 and fall through; CB k: jump to end of k-th
  0-ancestor; CC k: jump to start of k-th 1-ancestor; CH halts. Unwinding past the root -> 0.
"""
import itertools

_ids = itertools.count()

class Node:
    __slots__ = ('a', 'b', 'label')
    def __init__(self, a, b, label=None):
        self.a, self.b, self.label = a, b, label

class Leaf:
    __slots__ = ('op', 'arg')   # arg: register for CI/CD, label for CB/CC
    def __init__(self, op, arg=None):
        self.op, self.arg = op, arg

def CI(r): return Leaf('CI', r)
def CH(): return Leaf('CH')

def fresh(): return next(_ids)

def seq(*xs, style='right'):
    xs = [x for x in flatten(xs)]
    assert xs, 'empty seq'
    if len(xs) == 1: return xs[0]
    if style == 'right':
        return Node(xs[0], seq(*xs[1:], style=style))
    m = len(xs) // 2
    return Node(seq(*xs[:m], style=style), seq(*xs[m:], style=style))

def flatten(xs):
    for x in xs:
        if isinstance(x, (list, tuple)):
            yield from flatten(x)
        elif x is not None:
            yield x

def while_dec(r, body=None):
    """while r>0: r-=1; body"""
    L = fresh()
    if body is None:
        return Node(Leaf('CD', r), Leaf('CC', L), L)
    return Node(Leaf('CD', r), Node(seq(body), Leaf('CC', L)), L)

def ifpos(r, then=None, els=None):
    """if r>0: r-=1; then  else: els"""
    T = fresh()
    inner_then = Leaf('CB', T) if then is None else Node(seq(then), Leaf('CB', T))
    inner = Node(Leaf('CD', r), inner_then)
    if els is None:
        assert then is not None
        return Node(Leaf('CD', r), seq(then))
    return Node(inner, seq(els), T)

def loop(body_fn):
    """body_fn(brk) builds the body; Leaf('CB', brk) exits the loop."""
    L = fresh()
    return Node(seq(body_fn(L)), Leaf('CC', L), L)

def brk(label): return Leaf('CB', label)

# ---------------- resolution to rows ----------------
def resolve(root):
    rows = []
    def walk(n, path, anc):  # anc: list of (edge_bit, node) from root
        if isinstance(n, Leaf):
            op, arg = n.op, n.arg
            if op in ('CB', 'CC'):
                edge = '0' if op == 'CB' else '1'
                k = 0
                if arg == 'RESTART':
                    rows.append([path, op, sum(1 for b, _ in anc if b == edge) + 1]); return
                for bit, node in reversed(anc):
                    if bit == edge:
                        k += 1
                        if node.label == arg: break
                else:
                    raise ValueError(f'{op} target {arg} not an ancestor of the right kind at {path}')
                rows.append([path, op, k])
            elif op == 'CH':
                rows.append([path, 'CH', None])
            else:
                rows.append([path, op, arg])
            return
        walk(n.a, path + '0', anc + [('0', n)])
        walk(n.b, path + '1', anc + [('1', n)])
    walk(root, '', [])
    return rows

# ---------------- exact simulator (ProveIt graph_intervals) ----------------
def graph(rows):
    indices = {p: i for i, (p, _, _) in enumerate(rows)}
    intervals = {}
    def visit(p):
        if p in indices: ans = indices[p], indices[p] + 1
        else:
            a, b = visit(p + '0'), visit(p + '1'); assert a[1] == b[0]; ans = a[0], b[1]
        intervals[p] = ans; return ans
    assert visit('') == (0, len(rows))
    def unwind(path, edge, count):
        while path:
            last, path = path[-1], path[:-1]
            if last == edge:
                count -= 1
                if count == 0:
                    return intervals[path][1] % len(rows) if edge == '0' else intervals[path][0]
        return 0
    g = []
    for i, (p, op, arg) in enumerate(rows):
        after = (i + 1) % len(rows)
        if op == 'CI': g.append((op, arg, after, None))
        elif op == 'CD': g.append((op, arg, unwind(p, '0', 1), after))
        elif op == 'CB': g.append((op, None, unwind(p, '0', arg), None))
        elif op == 'CC': g.append((op, None, unwind(p, '1', arg), None))
        else: g.append(('CH', None, None, None))
    return g

def run(rows, regs=None, max_steps=10**7, stop_at_wrap=False):
    g = graph(rows); r = list(regs or [0] * 9); pc = 0; steps = 0
    while steps < max_steps:
        op, a, t1, t2 = g[pc]; steps += 1
        if op == 'CH': return 'halt', r, steps
        if op == 'CI': r[a] += 1; nxt = t1
        elif op == 'CD':
            if r[a] == 0: nxt = t1
            else: r[a] -= 1; nxt = t2
        else: nxt = t1
        if stop_at_wrap and nxt == 0 and pc != 0 and nxt <= pc and op != 'CC':
            return 'wrap', r, steps
        pc = nxt
    return 'timeout', r, steps

def dag_size(rows):
    root = {}
    for p, o, a in rows:
        at = root
        for b in p: at = at.setdefault(b, {})
        at['i'] = (o, a)
    memo = {}
    def h(n):
        k = ('L', n['i']) if 'i' in n else (h(n['0']), h(n['1']))
        return memo.setdefault(k, len(memo))
    h(root)
    return len(memo), sum(1 for k in memo if k[0] == 'L')
