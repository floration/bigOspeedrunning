"""Core of a variable-free (Tarski-Givant style) equational consistency checker, written in the
K215 source language. Registers (9, as K215): M N S A B C D X Y.

Proof search: for M = 0,1,2,...: the number M is read as a command stream (Cantor unpairing).
Commands act on a stack S of equations P(lhs, rhs). Terms are numbers P(op, payload):
op 0 = atom (1' = P(0,0) = 0, E = P(0,1)), 1 = complement, 2 = converse,
3 = union P(x,y), 4 = composition P(x,y). Any other number is an extra uninterpreted atom.
Halts iff some stack top has the form  t = complement(t), which in a Boolean algebra
(hence any relation algebra) forces 1 = 0, i.e. inconsistency.
"""
from rmc import *

M, N, S, A, B, C, D, X, Y = range(9)
RESTART = 'RESTART'

def clr(r): return while_dec(r)
def mov(a, b): return while_dec(a, CI(b))
def mov2(a, b, c): return while_dec(a, [CI(b), CI(c)])
def blk(xs): return seq(xs)
def copy(a, b, t): return blk([mov2(a, b, t), mov(t, a)])
def setk(r, k): return [CI(r)] * k if k else []
def unpair(c, x, y): return while_dec(c, ifpos(x, CI(y), [mov(y, x), CI(x)]))
def pair(x, y, z): return loop(lambda L: ifpos(y, [CI(x), CI(z)], ifpos(x, [mov(x, y), CI(z)], brk(L))))
def restart(): return brk(RESTART)
def push(r): return blk([pair(r, S, X), mov(X, S), CI(S)])  # S := P(r,S)+1
def pop(r): return ifpos(S, [unpair(S, r, X), mov(X, S)])  # empty stack yields 0 = (1'=1'), a true equation
def read(r): return blk([unpair(N, r, X), mov(X, N)])

# ---- term-building macros on the stack (used by axioms) ----
def PUSHV(v): return blk([copy(v, B, A), push(B)])
def PUSHC(c): return blk([setk(B, c), push(B)] if c else [push(B)])
def UN(k): return blk([pop(B), setk(A, k), pair(A, B, X), mov(X, B), push(B)])
def BIN(k): return blk([pop(B), pop(A), pair(A, B, X), setk(A, k), pair(A, X, B), push(B)])
def EQ(): return blk([pop(B), pop(A), pair(A, B, X), mov(X, B), push(B)])

COMP, CONV, UNION, COMPOSE = 1, 2, 3, 4
x, y, z = ('v', C), ('v', D), ('v', Y)
ONE_ID = ('c', 0)
def rpn(*syms):
    out = []
    for s in syms:
        if s == '=': out.append(EQ())
        elif s == '-': out.append(UN(COMP))
        elif s == '~': out.append(UN(CONV))
        elif s == '+': out.append(BIN(UNION))
        elif s == ';': out.append(BIN(COMPOSE))
        elif s[0] == 'v': out.append(PUSHV(s[1]))
        elif s[0] == 'c': out.append(PUSHC(s[1]))
    return out

# Tarski's ten relation-algebra axioms, in reverse Polish notation
RA = [
    rpn(x, y, '+', y, x, '+', '='),                                   # x+y = y+x
    rpn(x, y, z, '+', '+', x, y, '+', z, '+', '='),                   # x+(y+z) = (x+y)+z
    rpn(x, '-', y, '+', '-', x, '-', y, '-', '+', '-', '+', x, '='),  # Huntington
    rpn(x, y, z, ';', ';', x, y, ';', z, ';', '='),                   # ; associative
    rpn(x, y, '+', z, ';', x, z, ';', y, z, ';', '+', '='),           # right distributivity
    rpn(x, ONE_ID, ';', x, '='),                                      # x;1' = x
    rpn(x, '~', '~', x, '='),                                         # x~~ = x
    rpn(x, y, '+', '~', x, '~', y, '~', '+', '='),                    # (x+y)~ = x~+y~
    rpn(x, y, ';', '~', y, '~', x, '~', ';', '='),                    # (x;y)~ = y~;x~
    rpn(x, '~', x, y, ';', '-', ';', y, '-', '+', y, '-', '='),       # Tarski/De Morgan axiom
]

def dispatch(reg, branches):
    """branch i runs when reg == i (the last branch also takes every reg >= its index)."""
    if len(branches) == 1:
        return [clr(reg), branches[0]]
    return ifpos(reg, dispatch(reg, branches[1:]), branches[0])

def AX(extra_axioms=()):
    axioms = list(RA) + list(extra_axioms)
    return [read(C), read(D), read(Y), read(B), mov(B, A),
            dispatch(A, [blk(a + [clr(C), clr(D), clr(Y)]) for a in axioms])]

def SYM(): return blk([pop(B), unpair(B, C, D), pair(D, C, B), push(B)])

def eqd(a, b, on_ne, on_eq):
    """destructive equality test of a and b"""
    return loop(lambda L: ifpos(a, ifpos(b, None, [clr(a), on_ne, brk(L)]),
                                [ifpos(b, [clr(b), on_ne, brk(L)], [on_eq, brk(L)])]))

def TRANS():
    # e2=(b',c) on top, e1=(a,b) below; require b == b'; push (a,c)
    return blk([pop(B), pop(C), unpair(B, A, D), unpair(C, B, Y),
            eqd(A, Y, [clr(B), clr(D)], []), pair(B, D, Y), push(Y)])

def CONG_UN(k):
    return blk([pop(B), unpair(B, C, D), setk(A, k), pair(A, C, Y), setk(A, k), pair(A, D, C),
            pair(Y, C, B), push(B)])

def CONG_BIN(k):
    return blk([pop(B), pop(C), unpair(B, A, D), unpair(C, B, Y), pair(B, A, C), pair(Y, D, B),
            setk(A, k), pair(A, C, Y), setk(A, k), pair(A, B, D), pair(Y, D, B), push(B)])

def CHECK():
    # top = (t, r): halt iff r = P(1, t)
    return blk([pop(B), copy(B, C, D), push(C), unpair(B, C, D), unpair(D, A, Y),
            ifpos(A, ifpos(A, None, eqd(Y, C, [], CH())), None),
            clr(A), clr(B), clr(C), clr(D), clr(Y)])

def program(extra_axioms=(), style='right'):
    body = [clr(S), clr(N), clr(A), clr(B), clr(C), clr(D), clr(X), clr(Y),
            copy(M, N, X), CI(M),
            loop(lambda L: [ifpos(N, CI(N), restart()), read(A),
                            dispatch(A, [AX(extra_axioms), SYM(), TRANS(), CONG_UN(COMP),
                                         CONG_UN(CONV), CONG_BIN(UNION), CONG_BIN(COMPOSE)]),
                            CHECK()])]
    return seq(*body, style=style)
