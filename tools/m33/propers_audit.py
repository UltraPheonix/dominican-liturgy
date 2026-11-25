"""Step 3: the sung propers of every Mass on the site against the Missale O.P. 1933 (scan OCR, tools/m33/lines.json).
For each Mass (anchored by dpmap.json / map.json) the first words after Officium / Graduale / Offertorium / Communio are compared with
the incipit of the chant the site uses (data/masses.js). Writes tools/m33/propers_audit.md. Run after run.sh."""
import json, re, subprocess, sys
sys.path.insert(0, '/home/claude/m33')
from parse import norm
R = '/home/claude/dominican-liturgy/'
L = json.load(open('/home/claude/m33/lines.json')); M = json.load(open('/home/claude/m33/map.json'))
site = json.loads(subprocess.check_output(['node', '-e', """
global.window={};eval(require('fs').readFileSync('%sdata/masses.js','utf8').replace(/^var /mg,'global.'));
const o={};for(const [k,m] of Object.entries(DOMINICAN.masses)){o[k]={t:m.title,p:{}};for(const p of ['in','gr','al','tr','of','co'])o[k].p[p]=((m.parts||{})[p]||[]).map(c=>(DOMINICAN.chants[c.id]||{}).i||'')}
console.log(JSON.stringify(o))""" % R]))
HEAD = {'in': r'^(Officium|Introitus)\b', 'gr': r'^Graduale\b', 'of': r'^Offertorium\b', 'co': r'^Communio\b'}
def words(s, n=3): return ' '.join(norm(s).split()[:n])
out, bad = [], 0
for k, v in M.items():
    st = v.get('start')
    if st is None or k not in site: continue
    # the Mass runs to the next Officium
    end = next((j for j in range(st + 1, min(len(L), st + 400)) if re.match(HEAD['in'], L[j][2])), min(len(L), st + 400))
    for p, rx in HEAD.items():
        hit = next((j for j in range(st, end) if re.match(rx, L[j][2])), None)
        if hit is None or not site[k]['p'].get(p): continue
        txt = re.sub(rx, '', L[hit][2]); txt = re.sub(r'^\W*(?:Ps(?:alm)?|[A-Z][a-z]{1,6})\.?/?\s*\d+\s*', '', txt).strip()
        j = hit + 1
        while len(norm(txt).split()) < 4 and j < end: txt += ' ' + L[j][2]; j += 1
        m33 = words(txt, 3); s = words(site[k]['p'][p][0], 3)
        a, b = norm(txt).split(), s.split()
        a = [w for w in a if len(w) > 1 or w in ('a', 'e', 'o')]
        flat_a, flat_b = ''.join(a)[:30], ''.join(b)
        import difflib
        ok = bool(a and b) and (flat_b[1:9] in flat_a[:24] or (len(b) > 1 and b[1][:5] in flat_a[:30]) or
             difflib.SequenceMatcher(None, flat_a[:len(flat_b) + 4], flat_b).ratio() > 0.7)
        if not ok:
            bad += 1; out.append('| %s | %s | %s | %s | %s |' % (k, p, site[k]['p'][p][0], txt[:50].replace('|', '/'), L[hit][0] + 1))
open(R + 'tools/m33/propers_audit.md', 'w').write('# Propers vs Missale O.P. 1933 (OCR) — %d possible mismatches\n\nThe OCR loses drop caps and '
    'mixes columns, so each line needs a look at the pdf page before anything is changed.\n\n| Mass | part | site chant | M33 (OCR) | pdf page |\n|---|---|---|---|---|\n' % bad + '\n'.join(out) + '\n')
print(bad, 'possible mismatches')
