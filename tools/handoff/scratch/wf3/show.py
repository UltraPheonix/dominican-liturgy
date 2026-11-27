import json, sys, re
S = {r['date']: r for r in json.load(open('/tmp/wf3/site44.json'))}
O = {r['date']: r for r in json.load(open('/home/claude/dominican-liturgy/tools/ordo44/ordo1944b.json'))}
mon = sys.argv[1]
def sq(t): return re.sub(r'(?<=\b\w) (?=\w\b)', '', re.sub(r'[ \t]+', ' ', t))
for d in sorted(S):
    if d[5:7] != mon: continue
    s = S[d]; o = O.get(d, {})
    print('=' * 8, d, '[Ordo p.%s]' % o.get('page'))
    print(sq(o.get('text') or '(not parsed: see previous day)').strip())
    of = s['office']
    print('  >> SITE office: %s | %s | %s%s | two=%s' % (of.get('kind'), of.get('title'), of.get('rank'), (' (transf. from %s)' % of['transferredFrom']) if of.get('transferredFrom') else '', s['twoMasses']))
    print('  >> commems:', [(c.get('title'), c.get('rank'), 'priv' if c.get('privateOnly') else '') for c in s['commems']], 'missing:', [(m.get('label'), m.get('title') or m.get('key')) for m in s['missing']])
    for m in s['masses']:
        print('  >> MASS %s [%s] %s | %s | G=%s C=%s | Pf=%s | Ky=%s%s | %s | prayers=%s' % (m['key'], m['label'], re.sub(r'<[^>]+>', '', m['title'])[:60], m.get('color'), 'Y' if m.get('gloria') else 'n', 'Y' if m.get('credo') else 'n', m.get('pref'), m.get('kyr'), '+IV' if m.get('pk') else '', m.get('dismiss'), m.get('prn')))
