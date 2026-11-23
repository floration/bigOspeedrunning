"""Build research/p104-floor-retune-child-tariff from our p104-k7-floor-retune package
by layering #8076's child tariff (2401/1024) and its clock charges on top."""
import shutil, sys
from pathlib import Path
SRC=Path('/mnt/project-files/integer-multiplication/p104-k7-floor-retune/package')
DST=Path(sys.argv[1])
if DST.exists(): shutil.rmtree(DST)
shutil.copytree(SRC,DST)
def sub(name, pairs):
    p=DST/name; s=p.read_text()
    for a,b in pairs:
        n=s.count(a)
        if n!=1: raise SystemExit(f"{name}: {n} matches for {a[:70]!r}")
        s=s.replace(a,b)
    p.write_text(s)
K_OLD='.003898224460300'; K_NEW='.003898228176674'
G_OLD,G_NEW=511587,519562
H_OLD,H_NEW=110461,104978
sub('prepare.py',[
 ('"""Install the K7 matched-suffix bound on the exact weighted producer."""',
  '"""Install the retuned K7 floor with the #8076 child tariff on the exact weighted producer."""'),
 ('''    delta = Q(1, 2**128)
    def bounds(floor, suffix):
        multiplier = (
            Q(47, 20) * Q(256, 255)''','''    delta = Q(1, 2**128)
    predecessor_tariff = Q(47, 20)
    child_tariff = Q(2401, 1024)

    def bounds(floor, suffix, tariff=child_tariff):
        multiplier = (
            tariff * Q(256, 255)'''),
 ('''    k_lo, k_hi = bounds(18960, 8)
''','''    k_lo, k_hi = bounds(18960, 8, predecessor_tariff)
    # #8076's own booking (floor 18960, 8/L, child tariff) at 11178/8192.
    t_lo, t_hi = bounds(18960, 8)
    assert t_hi < 2 * powers(2, Q(2986, 8192))[0]
    # Our earlier retune (floor 4474, (186/25)/L, tariff 47/20) at 1430037/2^20.
    r_lo, r_hi = bounds(4474, Q(186, 25), predecessor_tariff)
    assert r_hi < 2 * powers(2, Q(381461, 2**20))[0]
'''),
 ('    prior_lo, prior_hi = bounds(18960, 64)\n    old_lo, old_hi = bounds(32768, 64)\n',
  '    prior_lo, prior_hi = bounds(18960, 64, predecessor_tariff)\n    old_lo, old_hi = bounds(32768, 64, predecessor_tariff)\n'),
 ('powers(2, Q(381461, 2**20)))\n    finer_allowance = 2 * powers(2, Q(381460, 2**20))[1]',
  'powers(2, Q(378063, 2**20)))\n    finer_allowance = 2 * powers(2, Q(378062, 2**20))[1]'),
 ('''    assert k_lo > allowance_hi
''','''    assert k_lo > allowance_hi
    # Both parent bookings fail the combined allowance.
    assert t_lo > allowance_hi and r_lo > allowance_hi
'''),
 ('''    assert Q(75, 32) / Q(47, 20) == Q(375, 376)
    print("PASS_DIRECTED_ORDINARY_DEBIT", 4474, "1430037/1048576", "375/376", "(186/25)/L")''',
  '''    assert Q(75, 32) / Q(47, 20) == Q(375, 376)

    # #8076: an equal tariff gives unit contraction; 2401/1024 gives sum 2401.
    child_volume = Q(75, 32)
    old_ratio, new_ratio = child_volume / predecessor_tariff, child_volume / child_tariff
    assert new_ratio == Q(2400, 2401) and 1 / (1 - new_ratio) == 2401
    old_sum, new_sum = 1 / (1 - old_ratio), 1 / (1 - new_ratio)
    assert old_sum == 376 and old_sum < new_sum < 8 * old_sum
    assert 2**16 < (Q(7, 10) * old_sum)**2 < 2**17
    assert 2**21 < (Q(7, 10) * new_sum)**2 < 2**22
    print("PASS_DIRECTED_ORDINARY_DEBIT", 4474, "1426639/1048576", "2400/2401", "(186/25)/L")
    print("PASS_CHILD_TARIFF", "2401/1024", "volume<=75/32", "sum=2401", "entry+5", "terminal+9")'''),
 (f'TERMINAL = Profile((8192, {H_OLD}, 524288), {G_OLD}, Q("{K_OLD}"))',
  f'TERMINAL = Profile((8192, {H_NEW}, 524288), {G_NEW}, Q("{K_NEW}"))'),
 ('"DEBIT = Q(64939, 2**19)\\nORDINARY_DEBIT = Q(1430037, 2**20)"',
  '"DEBIT = Q(64939, 2**19)\\nORDINARY_DEBIT = Q(1426639, 2**20)\\nCHILD_TARIFF = Q(2401, 1024)"'),
 ('''        ("    assert (tape_factor(134, BINARY_C) * Q(47, 20)) ** 8 < 2**11",''',
  '''        ("        bound = 128 + 320 * sum(heights)",
         "        # The complete per-stage envelope grows by <8 (#8076).\\n"
         "        bound = 128 + 3 * len(heights) + 320 * sum(heights)"),
        ("        bound = 40 + 17 + 16384 * sum(heights) + sum(additions)",
         "        # Charge the square of the new geometric child sum (#8076).\\n"
         "        bound = 40 + 22 + 16384 * sum(heights) + sum(additions)"),
        ("    assert (tape_factor(134, BINARY_C) * Q(47, 20)) ** 8 < 2**11",'''),
 ('''         '    ordinary_upper = Q("2.573602304817903473")\\n'
         "    assert tape_factor(134, BINARY_C, 4474, Q(186, 25)) * Q(47, 20) < ordinary_upper\\n"
         "    assert ordinary_upper**1048576 < 2**1430037\\n"
         "    assert Q(75, 32) / Q(47, 20) == Q(375, 376)"),''',
  '''         '    ordinary_upper = Q("2.567827100177770213")\\n'
         "    assert tape_factor(134, BINARY_C, 4474, Q(186, 25)) * CHILD_TARIFF < ordinary_upper\\n"
         "    assert ordinary_upper**1048576 < 2**1426639\\n"
         "    assert Q(75, 32) / CHILD_TARIFF == Q(2400, 2401)"),'''),
 ('"assert cost == 318291991 and premium == 518"', '"assert cost == COST_NEW and premium == PREMIUM_NEW"'),
 ('("(516019, 511587)")' if False else '"(516019, 511587)"', '"FLOORS_NEW"'),
 ('"assert gain == Q(2353397, 500000000000000)"', '"assert gain == GAIN_NEW"'),
 ('''         '        ordinary_child_contraction="375/376",'),''',
  '''         "        ordinary_child_tariff=str(CHILD_TARIFF),\\n"
         '        ordinary_child_contraction="2400/2401",\\n'
         "        ordinary_child_geometric_sum=2401,\\n"
         "        ordinary_entry_clock_extra=5,\\n"
         "        ordinary_terminal_clock_extra=3 * len(TERMINAL.rank_logs),"),'''),
 ("""'TERMINAL.kappa - peer == Q("0.0000000228466")'""", """'TERMINAL.kappa - peer == PEER_NEW'"""),
])
for n in ('check_cutoff.py',):
    sub(n,[(f'(1024, {G_OLD})',f'(1024, {G_NEW})')])
sub('check_ordinary_floor.py',[
 (f'TERMINAL.rank_logs==(8192,{H_OLD},524288) and TERMINAL.complex_log=={G_OLD}',
  f'TERMINAL.rank_logs==(8192,{H_NEW},524288) and TERMINAL.complex_log=={G_NEW}'),
 (f'(1024,{G_OLD})',f'(1024,{G_NEW})')])
sub('check_stage_seam.py',[
 (f'assert TERMINAL.rank_logs==(8192,{H_OLD},524288) and TERMINAL.kappa==Q("{K_OLD}")',
  f'assert TERMINAL.rank_logs==(8192,{H_NEW},524288) and TERMINAL.kappa==Q("{K_NEW}")'),
 (f'assert TERMINAL.complex_log=={G_OLD}', f'assert TERMINAL.complex_log=={G_NEW}'),
 ('assert TERMINAL.kappa-baseline.kappa==Q(2353397,500000000000000)',
  'assert TERMINAL.kappa-baseline.kappa==Q(".003898228176674")-Q(".003898219753506")'),
 ('    debit=Q(1430037,2**20)\n', '    debit=Q(1426639,2**20)\n    retune_debit=Q(1430037,2**20)\n    tariff_debit=Q(11178,8192)\n'),
 ('    def capped_shape(height,cap):\n        ranks=(8192,(cap-1731-220*height)//320-8192-524288,524288)',
  '    def capped_shape(height,cap,base=1731):\n        ranks=(8192,(cap-base-220*height)//320-8192-524288,524288)'),
 ('    assert ranks==capped_shape(height,cap)==capped_shape(height,318291991)\n    assert capped_shape(height-1,cap)==(8192,110461,524288)\n    assert capped_shape(height+1,cap)==(8192,110460,524288)',
  '    # The child tariff adds 9 to the terminal clock base (1731 -> 1740).\n'
  '    assert ranks==capped_shape(height,cap,1740)==capped_shape(height,318291940,1740)\n'
  '    assert capped_shape(height-1,cap,1740)==(8192,104978,524288)\n'
  '    assert capped_shape(height+1,cap,1740)==(8192,104977,524288)'),
 ('    assert 1731+320*sum(ranks)+220*height==318291991',
  '    assert 1740+320*sum(ranks)+220*height==318291940'),
 ('overfunded=booked-integer_optimum(capped_shape(height+1,cap),debit)',
  'overfunded=booked-integer_optimum(capped_shape(height+1,cap,1740),debit)'),
 ('    assert prior_booking_shortfall>0\n',
  '    assert prior_booking_shortfall>0\n'
  '    # Neither parent booking alone funds the combined profile.\n'
  '    assert booked>upper(ranks,retune_debit,True) and booked>upper(ranks,tariff_debit,True)\n'
  '    # #8076 at its own profile (base 1740) stays below the combined rate.\n'
  '    p8076=((8192,111681,524288),509812)\n'
  '    assert min(upper(p8076[0],tariff_debit,True),positive(p8076[1]))<booked\n'),
 ('(TERMINAL,(8290,118815,643167))','(TERMINAL,CUTS_NEW)'),
 ('PASS_LITERAL_K7_FLOOR_RETUNE','PASS_LITERAL_FLOOR_RETUNE_CHILD_TARIFF'),
])
sub('verify.py',[('PASS_K7_FLOOR_RETUNE','PASS_FLOOR_RETUNE_CHILD_TARIFF'),('prefix="k7-floor-"','prefix="k7-floor-tariff-"')])
print("built",DST)
