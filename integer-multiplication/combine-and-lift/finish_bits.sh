#!/bin/bash
# usage: finish_bits.sh <package-name>
set -e
S=/tmp/claude-0/-home-claude/7a0856cc-d91d-5be0-89da-1d23e0b6894e/scratchpad; cd $S/repo; Q=research/$1
H=$(python3.12 -IB $S/hashes.py $Q 2>&1 | grep "^installations.py" | awk '{print $5}')
sed -i "s/6f34146361b3e517c47ffbfbc949dafaa5571656f5498e275def0517e5fe6846/$H/" $Q/prepare.py
timeout 3000 python3.12 -IB $S/seam.py $Q receipt.py > $S/$1.receipt.out 2>&1 || true
python3 - "$Q" "$S/$1.receipt.out" <<'PY'
import sys,re
Q,out=sys.argv[1],open(sys.argv[2]).read()
m=re.search(r'DBG (\d+) (\d+) (\d+) (\d+)',out); cost,prem,early,late=m.groups()
f=re.search(r'"fixed_funding_height_floors": \[\s*(\d+),\s*(\d+)',out); f1,f2=f.groups()
assert early=='125660246'
p=f'{Q}/prepare.py'; s=open(p).read()
a='''"print(\\"DBG\\", cost, premium, early['log2_C'], late['log2_B'], file=sys.stderr)"'''; assert a in s
s=s.replace(a,f'''"assert cost == {cost} and premium == {prem}\\n"
         "    assert early['log2_C'] == 125660246 and late['log2_B'] == {late}"''')
a='"(ceil(ordinary_floor), ceil(positive_floor))"'; assert a in s; s=s.replace(a,f'"({f1}, {f2})"'); open(p,'w').write(s)
c=f'{Q}/check_stage_seam.py'; s=open(c).read(); assert 'TOTAL_NEW' in s
s=s.replace("TOTAL=TOTAL_NEW",f"TOTAL={cost}").replace("PREMIUM=PREMIUM_NEW",f"PREMIUM={prem}"); open(c,'w').write(s)
print("filled",cost,prem,late,f1,f2)
PY
timeout 1500 python3.12 -I -B $Q/verify.py regenerate > $S/$1.result.json
cp $S/$1.result.json $Q/RESULT.json
timeout 1500 python3.12 -I -B $Q/verify.py price | tail -1
