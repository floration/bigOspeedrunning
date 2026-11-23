"""Optimized version of checker.py: every pairing goes through one canonical register triple
(A,B -> X), so the pairing code is one shared subtree. Same proof calculus and same halting
condition as checker.py (see its docstring). Registers: M N S A B X C D Y."""
from rmc import *

M, N, S, A, B, X, C, D, Y = range(9)
RESTART = 'RESTART'

def blk(*xs): return seq(list(xs))
def clr(r): return while_dec(r)
def mov(a, b): return while_dec(a, CI(b))
def setk(r, k): return [CI(r)] * k
def restart(): return brk(RESTART)

PAIRC = lambda: loop(lambda L: ifpos(B, [CI(A), CI(X)], ifpos(A, [mov(A, B), CI(X)], brk(L))))  # X=P(A,B)
UNPAIRC = lambda: while_dec(X, ifpos(A, CI(B), [mov(B, A), CI(A)]))                            # A,B=U(X)

def uncons(r): return blk(mov(r, X), UNPAIRC(), mov(B, r), mov(A, X))     # X := head(r), r := tail(r)
def push(): return blk(mov(X, A), mov(S, B), PAIRC(), mov(X, S), CI(S))   # S := P(X,S)+1
def pop(): return ifpos(S, uncons(S))                                     # X := top (0 = "1'=1'" if empty)
def read(): return uncons(N)
def wrap(k): return blk(*setk(A, k), PAIRC())                             # X := P(k, B)

def copy(a, b, t): return blk(while_dec(a, [CI(b), CI(t)]), mov(t, a))

def eqd(a, b, on_ne, on_eq):
    return loop(lambda L: ifpos(a, ifpos(b, None, [clr(a), on_ne, brk(L)]),
                                [ifpos(b, [clr(b), on_ne, brk(L)], [on_eq, brk(L)])]))

# ---- axiom term building (vars packed in C = P(x, P(y, z))) ----
FIRST = lambda: blk(UNPAIRC(), clr(B), mov(A, X))
REST = lambda: blk(UNPAIRC(), clr(A), mov(B, X))
def PUSHV(i):
    get = [copy(C, X, A)] + {0: [FIRST()], 1: [REST(), FIRST()], 2: [REST(), REST()]}[i]
    return blk(*get, push())
def PUSHC0(): return push()
def UN(k): return blk(pop(), mov(X, B), wrap(k), push())
def BIN(k): return blk(pop(), mov(X, D), pop(), mov(X, A), mov(D, B), PAIRC(), mov(X, B), wrap(k), push())
def EQ(): return blk(pop(), mov(X, D), pop(), mov(X, A), mov(D, B), PAIRC(), push())

COMP, CONV, UNION, COMPOSE = 1, 2, 3, 4
x, y, z, one = ('v', 0), ('v', 1), ('v', 2), ('c', 0)
def rpn(*syms):
    out = []
    for s in syms:
        out.append({'=': EQ, '-': lambda: UN(COMP), '~': lambda: UN(CONV), '+': lambda: BIN(UNION),
                    ';': lambda: BIN(COMPOSE)}[s]() if isinstance(s, str) else
                   (PUSHV(s[1]) if s[0] == 'v' else PUSHC0()))
    return out

RA_SYMS = [
    [x, y, '+', y, x, '+', '='],
    [x, y, z, '+', '+', x, y, '+', z, '+', '='],
    [x, '-', y, '+', '-', x, '-', y, '-', '+', '-', '+', x, '='],
    [x, y, z, ';', ';', x, y, ';', z, ';', '='],
    [x, y, '+', z, ';', x, z, ';', y, z, ';', '+', '='],
    [x, one, ';', x, '='],
    [x, '~', '~', x, '='],
    [x, y, '+', '~', x, '~', y, '~', '+', '='],
    [x, y, ';', '~', y, '~', x, '~', ';', '='],
    [x, '~', x, y, ';', '-', ';', y, '-', '+', y, '-', '='],
]

def dispatch(reg, branches):
    if len(branches) == 1:
        return blk(clr(reg), branches[0])
    return ifpos(reg, dispatch(reg, branches[1:]), branches[0])

def AX(axiom_syms):
    return blk(read(), mov(X, C), read(),
               dispatch(X, [blk(*rpn(*a), clr(C)) for a in axiom_syms]))

def SYM(): return blk(pop(), UNPAIRC(), mov(A, Y), mov(B, A), mov(Y, B), PAIRC(), push())
def TRANS():
    return blk(pop(), UNPAIRC(), mov(B, D), mov(A, Y), pop(), UNPAIRC(),
               eqd(B, Y, [clr(A), clr(D)], []), mov(D, B), PAIRC(), push())
def CONG_UN(k):
    return blk(pop(), UNPAIRC(), mov(B, D), mov(A, B), wrap(k), mov(X, Y), mov(D, B), wrap(k),
               mov(X, B), mov(Y, A), PAIRC(), push())
def CONG_BIN(k):
    return blk(pop(), UNPAIRC(), mov(B, D), mov(A, Y), pop(), UNPAIRC(), mov(B, C), mov(Y, B), PAIRC(),
               mov(X, B), wrap(k), mov(X, Y), mov(C, A), mov(D, B), PAIRC(), mov(X, B), wrap(k),
               mov(X, B), mov(Y, A), PAIRC(), push())
def CHECK():
    return blk(pop(), copy(X, D, Y), push(), mov(D, X), UNPAIRC(), mov(B, X), mov(A, D), UNPAIRC(),
               ifpos(A, ifpos(A, None, eqd(B, D, [], CH())), None), clr(A), clr(B), clr(D))

def program(axiom_syms=None):
    axiom_syms = RA_SYMS if axiom_syms is None else axiom_syms
    return seq(clr(S), clr(N), clr(A), clr(B), clr(X), clr(C), clr(D), clr(Y),
               copy(M, N, X), CI(M),
               loop(lambda L: [ifpos(N, CI(N), restart()), read(),
                               dispatch(X, [AX(axiom_syms), SYM(), TRANS(), CONG_UN(COMP), CONG_UN(CONV),
                                            CONG_BIN(UNION), CONG_BIN(COMPOSE)]),
                               CHECK()]))
