import json, re, subprocess
from parse import norm, HR, L
# site masses + orations
js = subprocess.run(['node', '-e', '''
global.window={}; const fs=require('fs');
eval(fs.readFileSync('/home/claude/dominican-liturgy/data/masses.js','utf8').replace(/^var /mg,'global.'));
eval(fs.readFileSync('/home/claude/dominican-liturgy/data/orations.js','utf8'));
const out={}; for (const k in DOMINICAN.masses){const m=DOMINICAN.masses[k]; const o=(window.ORATIONS||{})[k]||{}; out[k]={title:m.title,page:m.page,readings:m.readings||[],or:o.or?o.or[0]:'',se:o.se?o.se[0]:'',pc:o.pc?o.pc[0]:''};}
console.log(JSON.stringify(out));'''], capture_output=True, text=True).stdout
SITE = json.loads(js)
# normalized stream of words with line index
W = []; WL = []; carry = ''
for li, (pg, kind, l) in enumerate(L):
    l = l.replace('\xad', '-').strip()
    hy = l.endswith('-')
    ws = norm(l).split()
    if carry and ws: ws[0] = carry + ws[0]; carry = ''
    if hy and ws: carry = ws.pop()
    for w in ws:
        W.append(w); WL.append(li)
# rejoin hyphenated words: crude: also index word pairs
S = ' '.join(W)
pos2word = []
off = 0
for k, w in enumerate(W): pos2word.append(off); off += len(w) + 1
import bisect
def find(text, minw=11):
    ws = norm(text).split()
    if len(ws) < minw + 2: return None
    for mw in (minw, 8):
        for start in (2, 3, 5, 8):
            q = ' '.join(ws[start:start + mw])
            if len(q.split()) < mw: continue
            hits = [m.start() for m in re.finditer(re.escape(q), S)]
            if hits: return WL[bisect.bisect_right(pos2word, hits[0]) - 1]
    return None
res = {}
miss = []
for k, m in SITE.items():
    li = None
    for f in ('or', 'se', 'pc'):
        if m[f]: li = find(m[f])
        if li is not None: res[k] = {'line': li, 'via': f}; break
    if li is None: miss.append(k)
json.dump(res, open('anchors.json', 'w'))
print(len(res), 'found;', len(miss), 'missing:', miss)
