"""Merge the proofed orations (new_or.json, built by build_or.py) into data/orations.js.
Latin: the Missal's j-spelling becomes the site's i (Jesum -> Iesum, ejus -> eius, Joánnis -> Ioánnis).
Source: the printed page of the Missale O.P. 1939 where the Collect stands (pages.json; S0118 is in the bound-in supplement).
Existing keys are never overwritten unless --force KEY is given."""
import json, re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', '..', 'data', 'orations.js')
PFX = 'window.ORATIONS = '
force = set(sys.argv[sys.argv.index('--force') + 1:]) if '--force' in sys.argv else set()
s = open(SITE, encoding='utf8').read()
O = json.loads(s[len(PFX):].rstrip().rstrip(';'))
N = json.load(open(os.path.join(HERE, 'new_or.json')))
P = json.load(open(os.path.join(HERE, 'pages.json')))
def i_spelling(t): return t.replace('j', 'i').replace('J', 'I')
def src(k):
    if k == 'S0118': where = 'supplement (S. Margarita ab Hungaria), p. 1'
    else: where = 'p. %s' % P[k]
    return 'Missale O.P. (1939), %s; English after the St Dominic Missal (1959), checked against the Latin' % where
added = []
for k, e in N.items():
    if k in O and k not in force: continue
    O[k] = {'src': src(k)}
    for kind in ('or', 'se', 'pc'):
        O[k][kind] = [i_spelling(e[kind][0]), e[kind][1]]
    added.append(k)
# the site's Latin uses i throughout; S1112 (done by hand earlier) still had Jesum
for k, v in O.items():
    for kind in ('or', 'se', 'pc'):
        if kind in v and re.search(r'[Jj]', v[kind][0]): v[kind][0] = i_spelling(v[kind][0])
open(SITE, 'w', encoding='utf8').write(PFX + json.dumps(O, ensure_ascii=False) + ';\n')
print(len(added), 'added;', len(O), 'Masses with orations now')
