"""Build research/p104-stack-height-lift-20bit from p104-height-lift-20bit by adding #8082's reserve drop
(no 256/255 on the ordinary factor) and its Gaussian debit 1039017/2^23. GAMED (enlarged budget)."""
import shutil, sys
from pathlib import Path
SRC=Path(sys.argv[1]); DST=Path(sys.argv[2])
shutil.copytree(SRC,DST)
def sub(name, pairs):
    p=DST/name; s=p.read_text()
    for a,b in pairs:
        n=s.count(a)
        if n!=1: raise SystemExit(f"{name}: {n} matches for {a[:80]!r}")
        s=s.replace(a,b)
    p.write_text(s)
K_OLD='.003898348448843'; K_NEW='.003898348449639'
sub('prepare.py',[
 ('"""Install the combined retune at the largest 20-bit Gaussian height with an enlarged recurring budget."""',
  '"""Install the stacked retune (floor, child tariff, no ordinary 256/255) at the largest 20-bit Gaussian height."""'),
 ('    def bounds(floor, suffix, tariff=child_tariff):\n        multiplier = (\n            tariff * Q(256, 255)',
  '    def bounds(floor, suffix, tariff=child_tariff, reserve=Q(1)):\n'
  '        # #8082: the ordinary contraction is paid by the clock sum, so the\n'
  '        # positive 256/255 summation reserve is not charged here.\n'
  '        multiplier = (\n            tariff * reserve'),
 ('    k_lo, k_hi = bounds(18960, 8, predecessor_tariff)\n', '    k_lo, k_hi = bounds(18960, 8, predecessor_tariff, Q(256, 255))\n'),
 ('    t_lo, t_hi = bounds(18960, 8)\n', '    t_lo, t_hi = bounds(18960, 8, child_tariff, Q(256, 255))\n'),
 ('    r_lo, r_hi = bounds(4474, Q(186, 25), predecessor_tariff)\n',
  '    r_lo, r_hi = bounds(4474, Q(186, 25), predecessor_tariff, Q(256, 255))\n'
  '    # #8082 (reserve dropped, tariff 47/20) at 1424116/2^20, and the tariff stack with 256/255 at 1426639/2^20.\n'
  '    e_lo, e_hi = bounds(4474, Q(186, 25), predecessor_tariff)\n'
  '    assert e_hi < 2 * powers(2, Q(375540, 2**20))[0]\n'
  '    c_lo, c_hi = bounds(4474, Q(186, 25), child_tariff, Q(256, 255))\n'
  '    assert c_hi < 2 * powers(2, Q(378063, 2**20))[0]\n'),
 ('    prior_lo, prior_hi = bounds(18960, 64, predecessor_tariff)\n    old_lo, old_hi = bounds(32768, 64, predecessor_tariff)\n',
  '    prior_lo, prior_hi = bounds(18960, 64, predecessor_tariff, Q(256, 255))\n    old_lo, old_hi = bounds(32768, 64, predecessor_tariff, Q(256, 255))\n'),
 ('powers(2, Q(378063, 2**20)))\n    finer_allowance = 2 * powers(2, Q(378062, 2**20))[1]',
  'powers(2, Q(372142, 2**20)))\n    finer_allowance = 2 * powers(2, Q(372141, 2**20))[1]'),
 ('    assert t_lo > allowance_hi and r_lo > allowance_hi\n',
  '    assert t_lo > allowance_hi and r_lo > allowance_hi and e_lo > allowance_hi and c_lo > allowance_hi\n'),
 ('"1426639/1048576", "2400/2401", "(186/25)/L")', '"1420718/1048576", "2400/2401", "(186/25)/L, no 256/255")'),
 (f'TERMINAL = Profile((8192, 36373, 572500), 1048575, Q("{K_OLD}"))',
  f'TERMINAL = Profile((8192, 36093, 570250), 1048575, Q("{K_NEW}"))'),
 ('("POSITIVE_DEBIT = Q(65081, 524288)", "POSITIVE_DEBIT = Q(64939, 524288)")',
  '("POSITIVE_DEBIT = Q(65081, 524288)", "POSITIVE_DEBIT = Q(1039017, 2**23)")'),
 ('"DEBIT = Q(64939, 2**19)\\nORDINARY_DEBIT = Q(1426639, 2**20)\\nCHILD_TARIFF = Q(2401, 1024)"',
  '"DEBIT = Q(1039017, 2**23)\\nORDINARY_DEBIT = Q(1420718, 2**20)\\nCHILD_TARIFF = Q(2401, 1024)"'),
 ('''         '    ordinary_upper = Q("2.567827100177770213")\\n'
         "    assert tape_factor(134, BINARY_C, 4474, Q(186, 25)) * CHILD_TARIFF < ordinary_upper\\n"
         "    assert ordinary_upper**1048576 < 2**1426639\\n"''',
  '''         '    ordinary_upper = Q("2.557796525567700799")\\n'
         "    assert tape_factor(134, BINARY_C, 4474, Q(186, 25)) * Q(255, 256) * CHILD_TARIFF < ordinary_upper\\n"
         "    assert ordinary_upper**1048576 < 2**1420718\\n"'''),
 ('"assert cost == 428149040 and premium == 747\\n"\n         "    assert early[\'log2_C\'] == 125660246 and late[\'log2_B\'] == 197460937"',
  '"print(\\"DBG\\", file=sys.stderr)"'),
 ('"(540133, 1048575)"', '"(ceil(ordinary_floor), ceil(positive_floor))"'),
 ('Q(\\".003898348448843\\") - Q(\\".003898219753506\\")', 'Q(\\".003898348449639\\") - Q(\\".003898219753506\\")'),
 ("'TERMINAL.kappa - peer == Q(\".003898348448843\") - Q(\".0038982016137\")'", "'TERMINAL.kappa - peer == Q(\".003898348449639\") - Q(\".0038982016137\")'"),
 ('("lower = powers(2, Q(65081, 524288))[0]", "lower = powers(2, Q(64939, 524288))[0]")',
  '("lower = powers(2, Q(65081, 524288))[0]", "lower = powers(2, Q(1039017, 2**23))[0]")'),
 ("""     '    assert lower - upper > Q("0.000000684423")\\n'""",
  """     '    assert lower - upper > Q("0.00000005")\\n'\n     '    assert powers(2, Q(1039016, 2**23))[0] < upper\\n'"""),
])
sub('check_ordinary_floor.py',[('TERMINAL.rank_logs==(8192,36373,572500)','TERMINAL.rank_logs==(8192,36093,570250)')])
sub('check_stage_seam.py',[
 ('ORDINARY=Q(1426639,2**20)       # combined floor-retune + child-tariff debit','ORDINARY=Q(1420718,2**20)       # floor retune + child tariff + no 256/255'),
 ('GAUSSIAN=Q(64939,524288)','GAUSSIAN=Q(1039017,2**23)'),
 ('TOTAL=428149040','TOTAL=TOTAL_NEW'),('PREMIUM=747','PREMIUM=PREMIUM_NEW'),
 ('ranks==(8192,36373,572500)','ranks==(8192,36093,570250)'),
 (f'TERMINAL.kappa==Q("{K_OLD}")',f'TERMINAL.kappa==Q("{K_NEW}")'),
 ('    capped=((8192,104978,524288),519562)','    capped=((8192,101729,524288),524288)'),
 ('kappa=Q(".003898228176674"))','kappa=Q(".003898230327195"))'),
])
v=(DST/'VERIFY.json').read_text().replace('research/p104-height-lift-20bit/','research/p104-stack-height-lift-20bit/'); (DST/'VERIFY.json').write_text(v)
sub('verify.py',[('PASS_HEIGHT_LIFT_20BIT','PASS_STACK_HEIGHT_LIFT_20BIT'),('prefix="k7-height-lift-"','prefix="k7-stack-lift-"')])
print('built',DST)
