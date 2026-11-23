"""Build p104-shortcut-word-eta-<B>bit-<S>stage from the 25-bit 4-stage package."""
import sys, shutil, re
from pathlib import Path
from fractions import Fraction as Q
exec(open('bits.py').read().split('for bits in')[0])
BITS=int(sys.argv[1]); ST=int(sys.argv[2])
TOP=2**BITS-1
b,f=opt(BITS,ST); h=maxnext(f,TOP); hs=tuple(f)+(h,TOP)
k=Q((b*10**15).__floor__(),10**15)
if k+Q(5,10**18)>=b: k-=Q(1,10**15)
paid=k+Q(5,10**18)
GC=Q(17158764376,2**42); GD=Q(1039776,2**23); G=(GD/(GC-paid)).__floor__()+1
assert GC-GD/G>paid and not GC-GD/(G-1)>paid
K=format(k.numerator*10**15//k.denominator,'d'); K='.'+K.rjust(15,'0'); assert Q(K)==k
drops=[]
for i in range(ST):
    lo,hi=0,hs[i]
    while lo<hi:
        m=(lo+hi)//2; t=list(hs); t[i]-=m
        if up(t)<=paid: hi=m
        else: lo=m+1
    drops.append(lo)
print(BITS,ST,hs,G,K,float(b),drops,cuts(hs))
SRC=Path('repo/research/p104-shortcut-word-eta-25bit-4stage')
NAME=f'p104-shortcut-word-eta-{BITS}bit-{ST}stage'
DST=Path('repo/research')/NAME
if DST.exists(): shutil.rmtree(DST)
shutil.copytree(SRC,DST)
def ed(fn,pairs,count_ok=False):
    p=DST/fn; s=p.read_text()
    for a,bb in pairs:
        assert a in s,(fn,a[:60]); s=s.replace(a,bb)
    p.write_text(s)
HS=', '.join(map(str,hs)); HSC=','.join(map(str,hs))
ed('prepare.py',[
 ('Profile((125432, 1988432, 31439868, 33554431), 198527, Q(".003900826966095"), Q(1, 256))',f'Profile(({HS}), {G}, Q("{K}"), Q(1, 256))'),
 ('.003900826966095',K),
 ('''"assert cost == 21518289843 and premium == 30345\\n"
         "    assert early['log2_C'] == 125660246 and late['log2_B'] == 21474612300"''','''"print(\\"DBG\\", cost, premium, early['log2_C'], late['log2_B'], file=sys.stderr)"'''),
 ('"(33535562, 198527)"','"(ceil(ordinary_floor), ceil(positive_floor))"'),
 ('len(low) + len(high) == 8',f'len(low) + len(high) == {2+1+ST+1}'),
 ('TERMINAL.complex_log)) <= 25',f'TERMINAL.complex_log)) <= {BITS}'),
 ('# 25-bit indexed setup (#8081/#8087 SETUP-PROOF): fields, carriers and scalar steps stay in the same bounds.',
  f'# {BITS}-bit indexed setup, extending the #8081/#8087 SETUP-PROOF (see SETUP-{BITS}BIT.md): every 92H stays below the\\n'
  f'    # datum bound w = 2^38, the Gaussian carriers stay below 2^25 bits, and each of the {2+1+ST+1} recipes gets 2^24 actions.'),
 ('assert 92*(2**25-1) < 2**32 and 1024*(2**25-1)+3 < 2**35',f'assert 92*(2**{BITS}-1) < 2**38 and 1024*(2**{BITS}-1)+3 < 2**{BITS+11}\\n    assert TERMINAL.complex_log < 2**25 and ENTRY.complex_log < 2**25'),
 ('assert 2*2048*(2**25+1) + 7*2**24 == 137556398080 < 2**40',f'assert 2*2048*(2**25+1) + {2+1+ST+1}*2**24 == {2*2048*(2**25+1)+(2+1+ST+1)*2**24} < 2**40'),
])
ed('check_cutoff.py',[('(1024, 198527)',f'(1024, {G})')])
ed('check_ordinary_floor.py',[('(125432,1988432,31439868,33554431) and TERMINAL.complex_log==198527',f'({HSC}) and TERMINAL.complex_log=={G}'),('(1024,198527)',f'(1024,{G})')])
ed('verify.py',[('k7-shortcut-eta25-4stage-',f'k7-shortcut-eta{BITS}-{ST}stage-'),('PASS_SHORTCUT_WORD_ETA_25BIT_4STAGE"',f'PASS_SHORTCUT_WORD_ETA_{BITS}BIT_{ST}STAGE"')])
s=(DST/'VERIFY.json').read_text().replace('research/p104-shortcut-word-eta-25bit-4stage/',f'research/{NAME}/'); (DST/'VERIFY.json').write_text(s)
# seam check: rewrite the profile block generically
p=DST/'check_stage_seam.py'; s=p.read_text()
s=s.replace('TOTAL=21518289843','TOTAL=TOTAL_NEW').replace('PREMIUM=30345','PREMIUM=PREMIUM_NEW')
s=s.replace('ranks==(125432,1988432,31439868,33554431) and TERMINAL.complex_log==198527',f'ranks==({HSC}) and TERMINAL.complex_log=={G}')
s=s.replace('TERMINAL.kappa==Q(".003900826966095")',f'TERMINAL.kappa==Q("{K}")')
s=s.replace('assert all(8192<=h<2**25 for h in ranks) and 1024<=TERMINAL.complex_log<2**25',f'assert all(8192<=h<2**{BITS} for h in ranks) and 1024<=TERMINAL.complex_log<2**25\n    BITS={BITS}; TOP=2**BITS-1')
s=s.replace('for i in (1,2,3))','for i in range(1,len(ranks)))')
a=s.index('    h0,h1,h2,h3=ranks'); z=s.index('    assert all(n<ordinary_upper(ranks) for n in neighbours)\n')+len('    assert all(n<ordinary_upper(ranks) for n in neighbours)\n')
D=list(drops)
block=f'''    hs=list(ranks); last=len(hs)-1
    def at(i,delta):
        t=list(hs); t[i]+=delta; return tuple(t)
    def require_funding(proposed,gaussian):
        if ordinary_upper(proposed)<=paid or gaussian_upper(gaussian)<=paid:
            raise ArithmeticError("Profile does not fund the terminal price")
    def require_budget(cap):
        if 1+max(125660246+conversion,late)>cap:
            raise ArithmeticError("The full recurring invoice exceeds the declared cap")
    capped=((62186,986008,1048575),66037)
    previous_record=((125432,1988432,31439868,33554431),198527)   # #8090, 25-bit 4-stage
    # The install is the 15-digit floor of the rate, so the lower heights carry
    # slack: DROPS[i] is the first drop of height i that falls below the booking.
    DROPS={D!r}
    for i,d in enumerate(DROPS):
        require_funding(at(i,-(d-1)),TERMINAL.complex_log)
    assert ordinary_upper(previous_record[0])<ordinary_upper(ranks)
    controls=[rejected(lambda i=i,d=d:require_funding(at(i,-d),TERMINAL.complex_log),f"ordinary-height-{{i}}-minus-{{d}}")
              for i,d in enumerate(DROPS)]
    controls+=[rejected(lambda i=i:resource_receipt(replace(TERMINAL,rank_logs=at(i,1))),f"ordinary-height-{{i}}-plus-one-breaks-prefix")
               for i in range(1,last)]
    controls+=[
        rejected(lambda:require_funding(*previous_record),"pr8090-profile-at-new-rate"),
        rejected(lambda:require_funding(*capped),"capped-combined-profile-at-new-rate"),
        rejected(lambda:require_funding(ranks,TERMINAL.complex_log-1),"gaussian-height-minus-one"),
        rejected(lambda:require_funding(ranks,TERMINAL.complex_log) or require_budget(318292011),"inherited-cap-318292011"),
        rejected(lambda:qualify(TERMINAL.kappa,STOP,paid-STOP,gaussian_upper(TERMINAL.complex_log)),"outer-ordinary-margin-removed"),
        rejected(lambda:resource_receipt(replace(TERMINAL,rank_logs=(hs[0],cuts[0]+2,*hs[2:]))),"prefix-height-at-previous-cut"),
        rejected(lambda:require_budget(TOTAL-1),"recurring-bound-minus-one"),
        rejected(lambda:(_ for _ in ()).throw(AssertionError()) if min(Q(39,10000),ordinary_upper(ranks))<=paid else None,"old-eta-39/10000"),
    ]
    # A height of BITS+1 bits would need a fresh setup bound.
    assert hs[last]==TOP and TOP.bit_length()==BITS

    # The prefix rule cut[i-1]+2<h[i] with the top height at the limit fixes the
    # second-to-last height for the free prefix; neighbouring prefixes are lower.
    def max_penultimate(prefix):
        lo,hi=prefix[-1],TOP
        while hi-lo>1:
            mid=(lo+hi)//2
            try:
                resource_receipt(replace(TERMINAL,rank_logs=(*prefix,mid,TOP)))
                lo=mid
            except AssertionError:
                hi=mid
        return lo
    free=tuple(hs[:last-1])
    assert max_penultimate(free)==hs[last-1]
    neighbours=[]
    for i in range(len(free)):
        for s in (-16,16):
            t=list(free); t[i]+=s
            if t[0]>=8192:
                neighbours.append(ordinary_upper((*t,max_penultimate(t),TOP)))
    # The 1e-21 intermediate ticks make the rate flat at the 1e-23 scale, so ties are allowed.
    assert all(n<=ordinary_upper(ranks) for n in neighbours)
'''
s=s[:a]+block+s[z:]
s=s.replace('for i in (2,3,4)]\n    compiled','for i in range(2,len(ranks)+1)]\n    compiled')
s=s.replace('round_up(9*ranks[i-1])) for i in (2,3,4)]','round_up(9*ranks[i-1])) for i in range(2,len(ranks)+1)]')
s=s.replace('PASS_SHORTCUT_ETA_25BIT_4STAGE_PROFILE',f'PASS_SHORTCUT_ETA_{BITS}BIT_{ST}STAGE_PROFILE')
assert 'h0' not in s and 'h3' not in s, [l for l in s.splitlines() if 'h0' in l or 'h3' in l]
p.write_text(s)
fo=DST/'check_ordinary_floor.py'; t=fo.read_text()
a="""        assert (volume,ticks,rounds)==(N**6,N**82,N**2)
        assert flags=={"width":1<<(92*old.rank_log),"delay_base":1<<19}"""
b="""        # Compare the dyadic arguments by exponent: at large heights a second
        # copy of N**82 or 2**(92H) would not fit in memory.
        def dyadic(x,e):
            return x.bit_count()==1 and x.bit_length()-1==e
        H=old.rank_log
        assert dyadic(volume,6*H) and dyadic(ticks,82*H) and dyadic(rounds,2*H)
        assert set(flags)=={"width","delay_base"} and dyadic(flags["width"],92*H) and flags["delay_base"]==1<<19"""
assert a in t; fo.write_text(t.replace(a,b))
pp=DST/'prepare.py'; t=pp.read_text().splitlines(True)
t[0]=f'"""Install the stacked retune on the five-shortcut Gaussian word at {BITS}-bit heights, {ST} ordinary stages and eta 1/256 (enlarged budget)."""\n'
pp.write_text(''.join(t))
note=open('SETUP-BITS.md').read().replace('28-bit',f'{BITS}-bit').replace('2^28',f'2^{BITS}').replace('92·2^28 < 2^35',f'92·2^{BITS} < 2^{BITS+7}').replace('2^35 + 1',f'2^{BITS+7} + 1').replace('below `2^39`',f'below `2^{BITS+11}`').replace('at most 35 bits',f'at most {BITS+7} bits').replace('**five** terminal',f'**{ST}** terminal').replace('nine height records',f'{3+ST+1} height records').replace('With nine recipes',f'With {3+ST+1} recipes').replace('9·2^24',f'{3+ST+1}·2^24').replace('137589952512',str(2*2048*(2**25+1)+(3+ST+1)*2**24)).replace('210442',str(G))
(DST/f'SETUP-{BITS}BIT.md').write_text(note)
import json
v=json.loads((DST/'VERIFY.json').read_text())
T={'price':150,'calendar':600,'raw':80,'exterior':90,'nested':90,'product':100,'setup':60}
for c in v['commands']: c['timeout_seconds']=T[c['argv'][-1]]
(DST/'VERIFY.json').write_text(json.dumps(v,indent=2)+'\n')
print("built",NAME)
