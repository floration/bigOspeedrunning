import sympy as sp
a,s,t=sp.symbols('a s t',positive=True)
W=lambda x: sp.cos(a*x)
I1=sp.integrate(W(t),(t,-sp.Rational(1,2),sp.Rational(1,2)))
I2=sp.integrate(W(t)**2,(t,-sp.Rational(1,2),sp.Rational(1,2)))
inner=sp.integrate(W(t)*(s-t),(t,-sp.Rational(1,2),s))
I3=2*sp.integrate(W(s)*inner,(s,-sp.Rational(1,2),sp.Rational(1,2)))
H=sp.simplify(2-(I2+I3)/I1**2)
print("H(a) =",H)
for av in [sp.sqrt(2),sp.Rational(3,2)]:
    print(av, sp.nsimplify(sp.simplify(H.subs(a,av))), sp.N(H.subs(a,av),20))
print("MT closed form", sp.N(sp.Rational(3,2)-sp.cot(1/sp.sqrt(2))/sp.sqrt(2),20))
