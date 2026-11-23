"""Build research/p104-shortcut-word-eta-25bit from p104-shortcut-word-lift-20bit: 25-bit heights (#8081/#8087 setup)
and the ordinary clamp eta = 1/256 (#8084). GAMED (enlarged budget)."""
import shutil, sys
from pathlib import Path
SRC=Path(sys.argv[1]); DST=Path(sys.argv[2])
shutil.copytree(SRC,DST)
def sub(name, pairs):
    p=DST/name; s=p.read_text()
    for a,b in pairs:
        n=s.count(a)
        if n!=1: raise SystemExit(f"{name}: {n} matches for {a[:90]!r}")
        s=s.replace(a,b)
    p.write_text(s)
K_OLD='.003899574328473'; K_NEW='.003900826718768'
R=(1991687, 31554614, 33554431); G=198448
sub('prepare.py',[
 ('"""Install the stacked retune on the five-shortcut Gaussian word at 20-bit ordinary heights (enlarged budget)."""',
  '"""Install the stacked retune on the five-shortcut Gaussian word at 25-bit heights with eta 1/256 (enlarged budget)."""'),
 (f'TERMINAL = Profile((62186, 986008, 1048575), 66037, Q("{K_OLD}"))', f'TERMINAL = Profile({R}, {G}, Q("{K_NEW}"), Q(1, 256))'),
 ('TERMINAL.rank_logs, TERMINAL.complex_log)) <= 20',
  'TERMINAL.rank_logs, TERMINAL.complex_log)) <= 25\n'
  '    # 25-bit indexed setup (#8081/#8087 SETUP-PROOF): fields, carriers and scalar steps stay in the same bounds.\n'
  '    assert 92*(2**25-1) < 2**32 and 1024*(2**25-1)+3 < 2**35\n'
  '    assert 2*2048*(2**25+1) + 7*2**24 == 137556398080 < 2**40\n'
  '    assert TERMINAL.eta == Q(1, 256) and all(abs(x).bit_length() <= 128 for x in (TERMINAL.eta.numerator, TERMINAL.eta.denominator, TERMINAL.kappa.numerator, TERMINAL.kappa.denominator))'),
 ('"assert cost == 685495960 and premium == 973\\n"\n         "    assert early[\'log2_C\'] == 125660246 and late[\'log2_B\'] == 670966217"', '"print(\\"DBG\\", file=sys.stderr)"'),
 ('"(1047843, 66037)"', '"(ceil(ordinary_floor), ceil(positive_floor))"'),
 ('Q(\\".003899574328473\\") - Q(\\".003898219753506\\")', 'Q(\\".003900826718768\\") - Q(\\".003898219753506\\")'),
 ("'TERMINAL.kappa - peer == Q(\".003899574328473\") - Q(\".0038982016137\")'", "'TERMINAL.kappa - peer == Q(\".003900826718768\") - Q(\".0038982016137\")'"),
])
sub('check_ordinary_floor.py',[('TERMINAL.rank_logs==(62186,986008,1048575) and TERMINAL.complex_log==66037','TERMINAL.rank_logs==(1991687,31554614,33554431) and TERMINAL.complex_log==198448'),('(1024,66037)','(1024,198448)')])
sub('check_cutoff.py',[('(1024, 66037)','(1024, 198448)')])
sub('check_stage_seam.py',[
 ('    assert log_width % 10000 == 0\n', '    eta=profile.eta\n    assert log_width % 10000 == 0 and log_width*eta.numerator % eta.denominator == 0 and log_width % 250 == 0\n'),
 ('    component = 1 << (39*log_width//10000)', '    component = 1 << (log_width*eta.numerator//eta.denominator)'),
 ('TOTAL=685495960','TOTAL=TOTAL_NEW'),('PREMIUM=973','PREMIUM=PREMIUM_NEW'),
 ('ranks==(62186,986008,1048575) and TERMINAL.complex_log==66037', 'ranks==(1991687,31554614,33554431) and TERMINAL.complex_log==198448'),
 (f'TERMINAL.kappa==Q("{K_OLD}")',f'TERMINAL.kappa==Q("{K_NEW}")'),
 ('    assert all(8192<=h<2**20 for h in ranks) and 1024<=TERMINAL.complex_log<2**20\n    assert TERMINAL.eta==Q(39,10000) and TERMINAL.eta*8192-1>30\n',
  '    assert all(8192<=h<2**25 for h in ranks) and 1024<=TERMINAL.complex_log<2**25\n'
  '    # #8084: q < eta < 1/250 with eta = 1/256; the former 39/10000 clamp rejects this booking.\n'
  '    assert TERMINAL.eta==Q(1,256) and paid<TERMINAL.eta<Q(1,250) and TERMINAL.eta*8192-1>30\n'
  '    assert 2*TERMINAL.eta>Q(1,250) and TERMINAL.eta>Q(1,258)\n'
  '    assert all(ordinary_upper(ranks[:i])<TERMINAL.eta for i in (1,2))\n'
  '    assert all(-(-(2*h+64)*256//255)<3*h for h in ranks)\n'),
 ('    capped=((62186,986008,1048575),66037)' if False else '    capped=((26384,417171,524288),39002)', '    capped=((62186,986008,1048575),66037)'),
 ('kappa=Q(".003898273237647"))','kappa=Q(".003899574328473"),eta=Q(39,10000))'),
 ('    # A 21-bit Gaussian height would need a fresh setup census.\n    assert (2**20).bit_length()==21\n',
  '    # A 26-bit height would need a fresh setup certificate.\n    assert (2**25).bit_length()==26\n'),
 ('        lo,hi=a,2**20-1','        lo,hi=a,2**25-1'),
 ('    assert max_h2(h1)==h2 and h3==2**20-1','    assert max_h2(h1)==h2 and h3==2**25-1'),
 ('        return ((n+9999)//10000)*10000','        return ((n+79999)//80000)*80000'),
])
# controls: eta 39/10000 rejects
sub('check_stage_seam.py',[('        rejected(lambda:require_budget(TOTAL-1),"recurring-bound-minus-one"),\n',
  '        rejected(lambda:require_budget(TOTAL-1),"recurring-bound-minus-one"),\n'
  '        rejected(lambda:(_ for _ in ()).throw(AssertionError()) if min(Q(39,10000),ordinary_upper(ranks))<=paid else None,"old-eta-39/10000"),\n')])
v=(DST/'VERIFY.json').read_text().replace('research/p104-shortcut-word-lift-20bit/','research/p104-shortcut-word-eta-25bit/'); (DST/'VERIFY.json').write_text(v)
sub('verify.py',[('PASS_SHORTCUT_WORD_LIFT_20BIT','PASS_SHORTCUT_WORD_ETA_25BIT'),('prefix="k7-shortcut-lift-"','prefix="k7-shortcut-eta25-"')])
print('built',DST)
