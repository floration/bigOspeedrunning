"""Build research/p104-height-lift-20bit from the combined package (floor retune + child tariff):
lift the recurring clock cap and fund the largest 20-bit Gaussian height. GAMED (resource tradeoff)."""
import shutil, sys
from pathlib import Path
SRC=Path(sys.argv[1]); DST=Path(sys.argv[2])
if DST.exists(): shutil.rmtree(DST)
shutil.copytree(SRC,DST)
def sub(name, pairs):
    p=DST/name; s=p.read_text()
    for a,b in pairs:
        n=s.count(a)
        if n!=1: raise SystemExit(f"{name}: {n} matches for {a[:80]!r}")
        s=s.replace(a,b)
    p.write_text(s)
K_OLD='.003898228176674'; K_NEW='.003898348448843'
sub('prepare.py',[
 ('"""Install the retuned K7 floor with the #8076 child tariff on the exact weighted producer."""',
  '"""Install the combined retune at the largest 20-bit Gaussian height with an enlarged recurring budget."""'),
 (f'TERMINAL = Profile((8192, 104978, 524288), 519562, Q("{K_OLD}"))',
  f'TERMINAL = Profile((8192, 36373, 572500), 1048575, Q("{K_NEW}"))'),
 ('max(heights[-1].bit_length() for heights in (ENTRY.rank_logs, TERMINAL.rank_logs)) <= 20',
  'max(h.bit_length() for h in (*ENTRY.rank_logs, ENTRY.complex_log, *TERMINAL.rank_logs, TERMINAL.complex_log)) <= 20'),
 ('"assert cost == 318291940 and premium == 519\\n"\n         "    assert early[\'log2_C\'] == 125660246 and late[\'log2_B\'] == 203986697"',
  '"print(\\"DBG_COST\\", cost, premium, early[\\"log2_C\\"], late[\\"log2_B\\"], file=sys.stderr, flush=True)"'),
 ('"(515518, 519562)"', '"(ceil(ordinary_floor), ceil(positive_floor)) and print(\\"DBG_FLOORS\\", ceil(ordinary_floor), ceil(positive_floor), file=sys.stderr, flush=True) is None"'),
 ('Q(\\".003898228176674\\") - Q(\\".003898219753506\\")', 'Q(\\".003898348448843\\") - Q(\\".003898219753506\\")'),
 ("'TERMINAL.kappa - peer == Q(\"0.000000026562974\")'", "'TERMINAL.kappa - peer == Q(\".003898348448843\") - Q(\".0038982016137\")'"),
])
sub('check_cutoff.py',[('(1024, 519562)','(1024, 1048575)')])
sub('check_ordinary_floor.py',[
 ('TERMINAL.rank_logs==(8192,104978,524288) and TERMINAL.complex_log==519562',
  'TERMINAL.rank_logs==(8192,36373,572500) and TERMINAL.complex_log==1048575'),
 ('(1024,519562)','(1024,1048575)')])
# Replace the capped-allocation check with the enlarged-budget check (after #8078's check_scaled.py).
p=DST/'check_stage_seam.py'; s=p.read_text()
head=s[:s.index('def check():')]
p.write_text(head+(Path(__file__).parent/'lift_check.py.txt').read_text())
sub('verify.py',[('PASS_FLOOR_RETUNE_CHILD_TARIFF','PASS_HEIGHT_LIFT_20BIT'),('prefix="k7-floor-tariff-"','prefix="k7-height-lift-"')])
sub('VERIFY.json',[])
v=(DST/'VERIFY.json').read_text().replace('research/p104-floor-retune-child-tariff/','research/p104-height-lift-20bit/')
(DST/'VERIFY.json').write_text(v)
print('built',DST)
