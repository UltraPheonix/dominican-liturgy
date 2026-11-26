#!/bin/bash
# One command: rebuild the 1933 Missal readings and data/readings33.js.  bash tools/m33/run.sh
set -e
R=$(cd "$(dirname "$0")/../.." && pwd); W=/home/claude/m33
mkdir -p $W; cp $R/tools/m33/*.py $R/tools/m33/*.json $W/; sed -i "s#R = '/home/claude/dominican-liturgy/'#R = '$R/'#" $W/vfix.py
[ -f $W/lines.json ] || gunzip -c $R/tools/m33/lines.json.gz > $W/lines.json
[ -f /tmp/M33.pdf ] || curl -sS -o /tmp/M33.pdf https://media.churchmusicassociation.org/dominican/M33.pdf
python3 -c "import fitz" 2>/dev/null || pip install -q --break-system-packages pymupdf
[ -d /home/claude/do ] || git clone -q --depth 1 https://github.com/DivinumOfficium/divinum-officium /home/claude/do
[ -e /home/claude/dominican-liturgy ] || ln -s $R /home/claude/dominican-liturgy
cd $W && python3 mapall.py >/dev/null && python3 build_readings.py | tail -1 && python3 dofix.py | tail -1 && { [ -f site_refs.json ] && python3 cmp.py || true; } && python3 vfix.py >/dev/null && cp vfix.py /dev/null
python3 - <<PY
import json
O=json.load(open('$W/readings33b.json')); out={}
for k,v in O.items():
    import re
    def ok(r): return not re.search(r'[a-zà-ÿæœǽ][A-ZÀ-ÞÆŒ]|[<>^|0-9]', r['la']) and re.match(r'[A-ZÀ-ÞÆŒ]', r['la'])   # scan junk left: keep the Vulgate
    rs=[{x:r[x] for x in ('type','ref','title','title_en','la','en','p33')} for r in v['readings'] if 'weak' not in r['flag'] and ok(r)]
    if k.startswith('S') and any(r['type']=='Gospel' for r in rs):   # sanctoral: the next (undated) Mass in the book can follow; stop at the first Gospel
        rs=rs[:[r['type'] for r in rs].index('Gospel')+1]
    if rs: out[k]=rs
import os
F='$R/tools/m33/fixes.json'          # hand corrections: {"MassKey": [ full list of readings ]} replaces that Mass
if os.path.exists(F):
    fx=json.load(open(F)); out.update(fx); print(len(fx),'hand fixes applied from tools/m33/fixes.json')
for k in json.load(open('$R/tools/m33/absent.json')): out.pop(k, None)   # not in the 1933 Missal: no readings
F2='$R/tools/m33/fixes_m39.json'     # Masses added from the Missale O.P. 1939 (tools/m39/new/add_masses.py): kept as built there
if os.path.exists(F2): fx2=json.load(open(F2)); out.update(fx2); print(len(fx2),'Masses from tools/m33/fixes_m39.json')
open('$R/data/readings33.js','w').write('/* Epistles and Gospels as printed in the Missale O.P. (1933), read from the scan (tools/m33). p33 = pdf page. */\nvar READINGS33 = '+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n')
print(len(out),'masses -> data/readings33.js')
PY
gzip -c $W/readings33b.json > $R/tools/m33/readings33b.json.gz
echo "Now: bump VERSION in sw.js, commit, push."
