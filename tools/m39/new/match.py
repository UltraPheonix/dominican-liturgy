"""Find site chant ids by part and incipit.  python3 tools/m39/new/match.py in "Laetabitur justus" gr "Posuisti" ...
Searches data/masses.js chants (the ids the site can show) by the gabc text's first words."""
import json, re, sys, unicodedata, os
D = json.loads(open('data/masses.js').read().split('var DOMINICAN = ', 1)[1].rstrip().rstrip(';'))
def n(s): return re.sub(r'[^a-z ]', '', unicodedata.normalize('NFD', s.lower().replace('æ', 'ae').replace('œ', 'oe').replace('j', 'i')).encode('ascii', 'ignore').decode())
TX = {}
for cid, c in D['chants'].items():
    f = 'gabc/%s.gabc' % cid
    t = ''
    if os.path.exists(f):
        g = open(f).read().split('%%', 1)[-1]; t = re.sub(r'\([^)]*\)|<[^>]+>|[{}*]', '', g)
    TX[cid] = (c['p'], n(c.get('i', '')), ' '.join(n(t).split()), c.get('pg'))
USE = {}
for k, m in D['masses'].items():
    for p, l in m.get('parts', {}).items():
        for x in l: USE.setdefault(str(x['id']), []).append(k)
a = sys.argv[1:]
for p, inc in zip(a[::2], a[1::2]):
    q = ' '.join(n(inc).split())
    hits = [(cid, v) for cid, v in TX.items() if (v[0] == p or p == '*') and (v[2].startswith(q) or v[1].startswith(q))]
    print('%-3s %-30s ->' % (p, inc), '; '.join('%s[%s p%s %s]' % (cid, v[0], v[3], ','.join(USE.get(cid, [])[:3])) for cid, v in hits[:8]) or 'NONE')
