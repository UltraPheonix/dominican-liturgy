#!/bin/bash
# One command: rebuild the 1933 Missal readings and data/readings33.js.  bash tools/m33/run.sh
set -e
R=$(cd "$(dirname "$0")/../.." && pwd); W=/home/claude/m33
mkdir -p $W; cp $R/tools/m33/*.py $R/tools/m33/*.json $W/
[ -f $W/lines.json ] || gunzip -c $R/tools/m33/lines.json.gz > $W/lines.json
[ -f /tmp/M33.pdf ] || curl -sS -o /tmp/M33.pdf https://media.churchmusicassociation.org/dominican/M33.pdf
python3 -c "import fitz" 2>/dev/null || pip install -q --break-system-packages pymupdf
[ -d /home/claude/do ] || git clone -q --depth 1 https://github.com/DivinumOfficium/divinum-officium /home/claude/do
[ -e /home/claude/dominican-liturgy ] || ln -s $R /home/claude/dominican-liturgy
cd $W && python3 dpmap.py >/dev/null && python3 mapall.py >/dev/null && python3 build_readings.py | tail -1 && python3 dofix.py | tail -1 && python3 cmp.py
python3 - <<PY
import json
O=json.load(open('$W/readings33b.json')); out={}
for k,v in O.items():
    rs=[{x:r[x] for x in ('type','ref','title','title_en','la','en','p33')} for r in v['readings'] if 'weak' not in r['flag']]
    if rs: out[k]=rs
import os
F='$R/tools/m33/fixes.json'          # hand corrections: {"MassKey": [ full list of readings ]} replaces that Mass
if os.path.exists(F):
    fx=json.load(open(F)); out.update(fx); print(len(fx),'hand fixes applied from tools/m33/fixes.json')
open('$R/data/readings33.js','w').write('/* Epistles and Gospels as printed in the Missale O.P. (1933), read from the scan (tools/m33). p33 = pdf page. */\nvar READINGS33 = '+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n')
print(len(out),'masses -> data/readings33.js')
PY
gzip -c $W/readings33b.json > $R/tools/m33/readings33b.json.gz
echo "Now: bump VERSION in sw.js, commit, push."
