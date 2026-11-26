"""Add 1939 feasts to the site: tools/m39/new/spec_*.json (+ or_*.json orations) ->
data/masses.js (Mass from its Common, as the Missale O.P. 1939 directs), data/readings33.js + tools/m33/fixes.json (readings copied
from the Common, or the Gospel the Missal names), tools/orat39/extra_final.json + en_final.json (orations, then extra.py + merge.py),
tools/m39/k_build.py FIX (calendar -> Mass key). Idempotent. Run from the repo root: python3 tools/m39/new/add_masses.py"""
import json, glob, os, re, subprocess, copy
R = os.getcwd(); H = os.path.join(R, 'tools/m39/new')
MON = ['Ian.', 'Feb.', 'Mart.', 'Apr.', 'Maii', 'Iun.', 'Iul.', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']
MEN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
F = 'data/masses.js'; s = open(F, encoding='utf8').read(); head, js = s.split('var DOMINICAN = ', 1)
D = json.loads(js.rstrip().rstrip(';'))
RF = 'data/readings33.js'; rs = open(RF, encoding='utf8').read(); rhead, rjs = rs.split('var READINGS33 = ', 1)
RD = json.loads(rjs.rstrip().rstrip(';'))
FX = json.load(open('tools/m33/fixes.json')) if os.path.exists('tools/m33/fixes.json') else {}
XF = json.load(open('tools/orat39/extra_final.json')); EF = json.load(open('tools/orat39/en_final.json'))
SPEC = [x for f in sorted(glob.glob(H + '/spec_*.json')) for x in json.load(open(f))]
OR = {}
for f in sorted(glob.glob(H + '/or_*.json')): OR.update(json.load(open(f)))
def order(k):   # the site's lists run from November
    m = D['masses'][k]; return ((m['month'] - 10) % 12, m['day']) if m.get('month') is not None else (99, 0)
n = 0; fix = {}
for x in SPEC:
    k = x['key']; c = D['masses'][x['common']]
    if k in D['masses'] and not D['masses'][k].get('m39new'): raise SystemExit('key already used by another Mass: ' + k)
    mo, dd = int(x['d'][:2]) - 1, int(x['d'][2:])
    m = {'title': x['title'], 'en': '%s %d — %s' % (MEN[mo], dd, x['title'].split(' — ', 1)[1]), 'rank': x['rank'], 'op': x['op'],
         'page': OR[k]['p'] if k in OR else x.get('page', ''), 'conf': 'missal',
         'note': x.get('note') or 'Missale O.P. (1939), p. %s: Mass from the %s, with proper orations.' % (OR.get(k, {}).get('p', '?'), c['title']),
         'parts': copy.deepcopy(c['parts']), 'season': copy.deepcopy(c.get('season', {})), 'extras': [], 'month': mo, 'day': dd,
         'readings': copy.deepcopy(c['readings']), 'req': list(c['req']), 'jgabc': c.get('jgabc'), 'name_en': x['name_en'], 'color': x['color'], 'm39new': True}
    rd = copy.deepcopy(RD.get(x['common'], []))
    if 'gospel' in x:
        src, ref = x['gospel']
        g = next(r for r in RD[src] if r['ref'] == ref)
        rd = [r for r in rd if r['type'] != 'Gospel'] + [copy.deepcopy(g)]
        m['readings'] = [r for r in m['readings'] if r['type'] != 'Gospel'] + [{'type': 'Gospel', 'ref': ref, 'm39': True}]
    D['masses'][k] = m
    if rd: RD[k] = rd; FX[k] = rd
    sec = next(z for z in D['sections'] if z['id'] == x['sec'])
    if k not in sec['items']:
        sec['items'].append(k); sec['items'].sort(key=order)
    if k in OR:
        o = OR[k]; XF[k] = {'p': o['p'], 'or': o['or'], 'se': o['se'], 'pc': o['pc']}; EF[k] = o['en']
    fix[(x['d'], x['kal'])] = k; n += 1
open(F, 'w', encoding='utf8').write(head + 'var DOMINICAN = ' + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + ';\n')
open(RF, 'w', encoding='utf8').write(rhead + 'var READINGS33 = ' + json.dumps(RD, ensure_ascii=False, separators=(',', ':')) + ';\n')
json.dump(FX, open('tools/m33/fixes.json', 'w'), ensure_ascii=False, indent=1)
json.dump(XF, open('tools/orat39/extra_final.json', 'w'), ensure_ascii=False, indent=1)
json.dump(EF, open('tools/orat39/en_final.json', 'w'), ensure_ascii=False, indent=1)
json.dump({'%s|%s' % a: b for a, b in fix.items()}, open(H + '/kfix.json', 'w'), ensure_ascii=False, indent=0)
print(n, 'Masses added/updated')
subprocess.run(['python3', 'extra.py'], cwd='tools/orat39', check=True)
subprocess.run(['python3', 'merge.py', '--force'] + [x['key'] for x in SPEC if x['key'] in OR], cwd='tools/orat39', check=True)
