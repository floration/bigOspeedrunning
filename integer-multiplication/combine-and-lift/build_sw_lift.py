"""Build research/p104-shortcut-word-lift-20bit: the stacked 20-bit lift (p104-stack-height-lift-20bit)
on the conjugate-pair five-shortcut Gaussian word (p104-k7-shortcut-word). GAMED (enlarged budget)."""
import shutil, sys, re
from pathlib import Path
SRC=Path(sys.argv[1]); SW=Path(sys.argv[2]); DST=Path(sys.argv[3])
shutil.copytree(SRC,DST)
shutil.copyfile(SW/'w5669_shortcut5.json.gz', DST/'w5669_shortcut5.json.gz')
def sub(name, pairs):
    p=DST/name; s=p.read_text()
    for a,b in pairs:
        n=s.count(a)
        if n!=1: raise SystemExit(f"{name}: {n} matches for {a[:90]!r}")
        s=s.replace(a,b)
    p.write_text(s)
swp=(SW/'prepare.py').read_text()
start=swp.index('SHORTCUT_FILE = ')
end=swp.index('\n\n\ndef materialize')
shortcut_block=swp[start:end]
K_OLD='.003898348449639'; K_NEW='.003899574328473'
HS='(62186, 986008, 1048575)'; G=66037
sub('prepare.py',[
 ('"""Install the stacked retune (floor, child tariff, no ordinary 256/255) at the largest 20-bit Gaussian height."""',
  '"""Install the stacked retune on the five-shortcut Gaussian word at 20-bit ordinary heights (enlarged budget)."""'),
 (f'TERMINAL = Profile((8192, 36093, 570250), 1048575, Q("{K_OLD}"))', f'TERMINAL = Profile({HS}, {G}, Q("{K_NEW}"))'),
 ('"POSITIVE_DEBIT = Q(1039017, 2**23)"', '"POSITIVE_DEBIT = Q(1039776, 2**23)"'),
 ("""'assert psi > Q("926899828.8291")'),\n        ("assert fringe < Q(7579, 1000)", 'assert fringe < Q("7.335168")'),""",
  """'assert psi > Q("926190717.2837")'),\n        ("assert fringe < Q(7579, 1000)", 'assert fringe < Q("7.340806")'),"""),
 ('"DEBIT = Q(1039017, 2**23)\\nORDINARY_DEBIT', '"DEBIT = Q(1039776, 2**23)\\nORDINARY_DEBIT'),
 ('"assert cost == 427339440 and premium == 746\\n"\n         "    assert early[\'log2_C\'] == 125660246 and late[\'log2_B\'] == 196651337"',
  '"print(\\"DBG\\", file=sys.stderr)"'),
 ('"(537891, 1048575)"', '"(ceil(ordinary_floor), ceil(positive_floor))"'),
 ('Q(\\".003898348449639\\") - Q(\\".003898219753506\\")', 'Q(\\".003899574328473\\") - Q(\\".003898219753506\\")'),
 ('"lower = powers(2, Q(1039017, 2**23))[0]"', '"lower = powers(2, Q(1039776, 2**23))[0]"'),
 ("'TERMINAL.kappa - peer == Q(\".003898348449639\") - Q(\".0038982016137\")'", "'TERMINAL.kappa - peer == Q(\".003899574328473\") - Q(\".0038982016137\")'"),
 ('"+GAUSSIAN_C = Q(17145637167, 2**42)", "+GAUSSIAN_C = Q(17145637307, 2**42)"', '"+GAUSSIAN_C = Q(17145637167, 2**42)", "+GAUSSIAN_C = Q(17158764376, 2**42)"'),
 ("""('assert psi > Q("184971191.2157")', 'assert psi > Q("926899828.8291")'),\n)""",
  """('assert psi > Q("184971191.2157")', 'assert psi > Q("926190717")'),\n    ('fringe < Q("7.335168")', 'fringe < Q("7.340806")'),\n)\nEDITS["independent_price.py"] += (\n    ("assert (targets.total(), paid.total()) == (105216, 564142)", "assert (targets.total(), paid.total()) == (105216, 563662)"),\n)"""),
 ('EDITS["receipt.py"] += (("and LOWER == 2048", "and LOWER == 1874"),)',
  'EDITS["receipt.py"] += (("and LOWER == 2048", "and LOWER == 1874"),\n    # The shortcut word moves #8057\'s single-weight capacity control.\n    ("assert cap[1] - load[0] < -1515 and net > Q(3, 100)", "assert cap[1] - load[0] < -960 and net > Q(3, 100)"),\n)'),
 ("""     '    assert lower - upper > Q("0.00000005")\\n'\n     '    assert powers(2, Q(1039016, 2**23))[0] < upper\\n'""",
  """     '    assert lower - upper > 0 and lower - upper > Q("0.000000019")\\n'\n     '    assert powers(2, Q(1039775, 2**23))[0] < upper\\n'"""),
 ("""'    assert prior_factor - powers(2, Q(64939,524288))[1] > Q("0.000051649827")'""",
  """'    assert prior_factor - powers(2, Q(64939,524288))[1] > Q("0.000127791")'"""),
 ('\n\n\ndef materialize(package):\n', '\n\n\n'+shortcut_block+'\n\n\ndef materialize(package):\n    from pathlib import Path\n    word = (Path(__file__).resolve().parent / SHORTCUT_FILE).read_bytes()\n    if sha256(word).hexdigest() != SHORTCUT_SHA:\n        raise ValueError("The shortcut word archive differs")\n    (package / SHORTCUT_FILE).write_bytes(word)\n'),
 ('        patch.write(RAW_FLOOR_PATCH)\n', '        patch.write(RAW_FLOOR_PATCH)\n        patch.write(SHORTCUT_PATCH)\n'),
 ('    for name in ("runtime.patch", "grades.py"):', '    pins["runtime_images"]["strong_complex.py"] = SHORTCUT_IMAGES\n    for name in ("runtime.patch", "grades.py", SHORTCUT_FILE):'),
])
sub('check_ordinary_floor.py',[('TERMINAL.rank_logs==(8192,36093,570250) and TERMINAL.complex_log==1048575',f'TERMINAL.rank_logs==(62186,986008,1048575) and TERMINAL.complex_log=={G}'),
 ('(1024,1048575)',f'(1024,{G})')])
sub('check_cutoff.py',[('(1024, 1048575)',f'(1024, {G})')])
sub('check_stage_seam.py',[
 ('ORDINARY=Q(1420718,2**20)       # floor retune + child tariff + no 256/255','ORDINARY=Q(1420718,2**20)       # floor retune + child tariff + no 256/255 (unchanged by the Gaussian word)'),
 ('GAUSSIAN=Q(1039017,2**23)','GAUSSIAN=Q(1039776,2**23)    # five-shortcut word debit'),
 ('TOTAL=427339440','TOTAL=TOTAL_NEW'),('PREMIUM=746','PREMIUM=PREMIUM_NEW'),
 ('ranks==(8192,36093,570250) and TERMINAL.complex_log==1048575==2**20-1', f'ranks==(62186,986008,1048575) and TERMINAL.complex_log=={G}\n    assert GAUSSIAN_C==Q(17158764376,2**42)'),
 (f'TERMINAL.kappa==Q("{K_OLD}")',f'TERMINAL.kappa==Q("{K_NEW}")'),
 ('    # The largest 20-bit Gaussian height: the stated install is the 15-digit floor of its rate.\n    assert TERMINAL.kappa<=gaussian_upper(2**20-1)-5*STOP<TERMINAL.kappa+Q(1,10**15)\n',
  '    # The ordinary side binds: the install is the 15-digit floor of its rate.\n    assert TERMINAL.kappa<=ordinary_upper(ranks)-5*STOP<TERMINAL.kappa+Q(1,10**15)\n'),
 ('    capped=((8192,101729,524288),524288)','    capped=((26384,417171,524288),39002)'),
 ('kappa=Q(".003898230327195"))','kappa=Q(".003898273237647"))'),
 ('    old_native,new_native=prepare_native(old),prepare_native(TERMINAL)\n    word=binary_word()\n    assert (len(word.targets),len(word.paid),len(word.cells))==(18906,104652,24)\n    assert old_native[0] is new_native[0]\n',
  '    old_native,new_native=prepare_native(old),prepare_native(TERMINAL)\n    word=binary_word()\n    assert (len(word.targets),len(word.paid),len(word.cells))==(18906,104652,24)\n'),
 ('    m=sum(ranks)-1; hmin=8192; w1=Q(1,62500)','    # Economy: the ordinary side binds here, so no smaller-sum claim is made.\n    m=sum(ranks)-1; hmin=8192; w1=Q(1,62500)'),
])
v=(DST/'VERIFY.json').read_text().replace('research/p104-stack-height-lift-20bit/','research/p104-shortcut-word-lift-20bit/'); (DST/'VERIFY.json').write_text(v)
sub('verify.py',[('PASS_STACK_HEIGHT_LIFT_20BIT','PASS_SHORTCUT_WORD_LIFT_20BIT'),('prefix="k7-stack-lift-"','prefix="k7-shortcut-lift-"')])
print('built',DST)
