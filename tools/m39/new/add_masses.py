"""Add 1939 feasts to the site: tools/m39/new/spec_*.json (+ or_*.json orations) ->
data/masses.js (Mass from its Common, as the Missale O.P. 1939 directs), data/readings33.js + tools/m33/fixes_m39.json (applied last by tools/m33/run.sh) (readings copied
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
FX = json.load(open('tools/m33/fixes_m39.json')) if os.path.exists('tools/m33/fixes_m39.json') else {}
XF = json.load(open('tools/orat39/extra_final.json')); EF = json.load(open('tools/orat39/en_final.json'))
SPEC = [x for f in sorted(glob.glob(H + '/spec_*.json')) for x in json.load(open(f))]
OR = {}
for f in sorted(glob.glob(H + '/or_*.json')): OR.update(json.load(open(f)))
# Commons the site has no Mass for, put together from Masses that carry exactly those chants and readings:
# @BMV = In festis B. Mariae Virginis (Missale O.P. 1939, p. 1*); @ABB = In festo unius Abbatis (p. 25*).
VIRT = {
 '@BMV': {'title': 'Commune festorum B. Mariae Virginis (p. 1*)', 'parts': {'in': [{'id': 4289}], 'gr': [{'id': 6293}], 'al': [{'id': '7550s'}], 'of': [{'id': 8151}], 'co': [{'id': 7543}]},
          'season': {}, 'readings_from': 'S0805', 'req': ['in', 'gr', 'al', 'of', 'co'], 'jgabc': None},
 '@ABB': {'title': 'Commune unius Abbatis (p. 25*)', 'parts': {'in': [{'id': 5885}], 'gr': [{'id': 7142}], 'al': [{'id': 7042}], 'of': [{'id': 6021}], 'co': [{'id': 4856}]},
          'season': {'lent': {'tr': [{'id': 7125}]}, 'pasch': {'al': [{'id': 7042}, {'id': 6824}]}, 'asc': {'al': [{'id': 7042}, {'id': 5526}]}},
          'readings_from': 'S0207', 'req': ['in', 'gr', 'al', 'of', 'co'], 'jgabc': 'mass_i_confessor_not_bishop'}}
for v in VIRT.values():
    v['readings'] = D['masses'][v['readings_from']]['readings']
    for p in v['parts'].values():
        for x in p: assert str(x['id']) in D['chants'], x
import sqlite3
GB = sqlite3.connect('tools/gregobase/gb.sqlite').cursor()
PARTN = {'in': 'Introitus', 'gr': 'Graduale', 'al': 'Alleluia', 'tr': 'Tractus', 'of': 'Offertorium', 'co': 'Communio', 'se': 'Sequentia'}
def addchant(i):
    """a Graduale O.P. chant the site does not list yet: gabc file + chants entry from the GregoBase dump"""
    if str(i) in D['chants']: return
    r = GB.execute('select c.incipit,c."office-part",c.mode,c.gabc,c.transcriber,s.page from gregobase_chants c join gregobase_chant_sources s on s.chant_id=c.id where c.id=? and s.source=14', (i,)).fetchone()
    if not r: raise SystemExit('chant %s: not in the Graduale O.P. dump' % i)
    inc, p, mode, g, tr, pg = r; g = json.loads(g)
    open('gabc/%s.gabc' % i, 'w').write('name:%s;\noffice-part:%s;\nmode:%s;\nbook:Graduale O.P. (Suarez), 1950, p. %s;\ntranscriber:%s;\n%%%%\n%s\n' % (inc, PARTN.get(p, p), mode or '', pg, tr or '', g))
    D['chants'][str(i)] = {'p': p, 'i': inc, 'pg': pg}
BIB = {}
def verses(lang, book, ranges):
    if (lang, book) not in BIB:
        V = {}
        for l in open('bible/%s/%s.txt' % (lang, book), encoding='utf-8'):
            a = l.rstrip('\n').split('\t')
            if len(a) >= 3: V[(int(a[0]), int(a[1]))] = ' '.join(a[2:])
        BIB[(lang, book)] = V
    V = BIB[(lang, book)]
    return ' '.join(V[(c, v)] for c, a, b in ranges for v in range(a, b + 1))
REFS = {}
for _k, _v in RD.items():
    for _r in _v: REFS.setdefault(_r['ref'], _r)
TITLES = {}
for _r in REFS.values(): TITLES.setdefault((_r['type'], re.sub(r'\s[\d:, -]+$', '', _r['ref'])), (_r['title'], _r['title_en']))
def reading(typ, ref, ranges=None, pre_la='', pre_en=''):
    """the same pericope already on the site (Missale O.P. 1933 text), else the Vulgate/Douay verses with the Missal's opening"""
    if ranges is None:
        r = REFS.get(ref)
        if not r: raise SystemExit('no text on the site for ' + ref)
        return dict(copy.deepcopy(r), type=typ)
    la = verses('la', ref, ranges); en = verses('en', ref, ranges)
    if pre_la: la = pre_la + ': ' + la[0].upper() + la[1:]; en = pre_en + ': ' + en
    la = re.sub(r'[,;:]\s*$', '.', la.strip())
    rf = ref + ' ' + ', '.join('%d: %d-%d' % (c, a, b) for c, a, b in ranges)
    t = TITLES.get((typ, ref)) or TITLES.get(('Lesson' if typ == 'Epistle' else 'Epistle', ref)) or ('', '')
    return {'type': typ, 'ref': rf, 'title': t[0], 'title_en': t[1], 'la': la, 'en': en, 'p33': None, 'src': 'Vulgate verses (Missale O.P. 1939 pericope)'}
def order(k):   # the site's lists run from November
    m = D['masses'][k]; return ((m['month'] - 10) % 12, m['day']) if m.get('month') is not None else (99, 0)
n = 0; fix = {}
for x in SPEC:
    k = x['key']
    if 'parts' in x:   # a Mass printed in full in the Missal: its own chants (ids checked in the gabc folder / GregoBase dump)
        c = {'title': x['title'], 'parts': {q: [{'id': i, 'm39': True} for i in l] for q, l in x['parts'].items()},
             'season': {s_: {q: [{'id': i, 'm39': True} for i in l] for q, l in v.items()} for s_, v in x.get('season', {}).items()},
             'readings': [], 'req': [q for q in ('in', 'gr', 'al', 'tr', 'of', 'co') if q in x['parts']], 'jgabc': None}
        for q in c['parts'].values():
            for y in q: addchant(y['id'])
        for v in c['season'].values():
            for q in v.values():
                for y in q: addchant(y['id'])
    else: c = VIRT[x['common']] if x['common'] in VIRT else D['masses'][x['common']]
    if k in D['masses'] and not D['masses'][k].get('m39new'): raise SystemExit('key already used by another Mass: ' + k)
    mo, dd = int(x['d'][:2]) - 1, int(x['d'][2:])
    m = {'title': x['title'], 'en': '%s %d — %s' % (MEN[mo], dd, x['title'].split(' — ', 1)[1]), 'rank': x['rank'], 'op': x['op'],
         'page': OR[k]['p'] if k in OR else x.get('page', ''), 'conf': 'missal',
         'note': (x.get('note') + ' ' if x.get('note') and 'parts' in x else '') + ('Missale O.P. (1939), p. %s: proper Mass.' % OR.get(k, {}).get('p', '?') if 'parts' in x else '') if 'parts' in x else x.get('note') or 'Missale O.P. (1939), p. %s: Mass from the %s, with proper orations.' % (OR.get(k, {}).get('p', '?'), c['title']),
         'parts': copy.deepcopy(c['parts']), 'season': copy.deepcopy(c.get('season', {})), 'extras': [], 'month': mo, 'day': dd,
         'readings': copy.deepcopy(c['readings']), 'req': list(c['req']), 'jgabc': c.get('jgabc'), 'name_en': x['name_en'], 'color': x['color'], 'm39new': True}
    if 'pasch' in x:   # Tempore Paschali the Introit, Offertory and Communion (and Alleluias) of another Common
        pc = D['masses'][x['pasch']]
        m['season']['pasch'] = {q: copy.deepcopy(pc['parts'][q]) for q in ('in', 'of', 'co') if q in pc['parts']}
        m['season']['pasch']['al'] = copy.deepcopy(pc.get('season', {}).get('pasch', {}).get('al', pc['parts'].get('al', [])))
        if 'asc' in pc.get('season', {}): m['season']['asc'] = copy.deepcopy(pc['season']['asc'])
        m['note'] += ' Tempore Paschali: Introit, Offertory, Communion and Alleluias of the %s.' % pc['title']
    rd = copy.deepcopy(RD.get(c.get('readings_from', x.get('common')), []))
    if 'readings' in x:   # the Missal's own lessons: the text of the same pericope elsewhere on the site, or the Vulgate verses
        rd = [reading(*r) for r in x['readings']]
        m['readings'] = [{'type': r['type'], 'ref': r['ref'], 'm39': True} for r in rd]
    if 'pref' in x: m['pref'] = x['pref']
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
json.dump(FX, open('tools/m33/fixes_m39.json', 'w'), ensure_ascii=False, indent=1)
json.dump(XF, open('tools/orat39/extra_final.json', 'w'), ensure_ascii=False, indent=1)
json.dump(EF, open('tools/orat39/en_final.json', 'w'), ensure_ascii=False, indent=1)
json.dump({'%s|%s' % a: b for a, b in fix.items()}, open(H + '/kfix.json', 'w'), ensure_ascii=False, indent=0)
print(n, 'Masses added/updated')
subprocess.run(['python3', 'extra.py'], cwd='tools/orat39', check=True)
subprocess.run(['python3', 'merge.py', '--force'] + [x['key'] for x in SPEC if x['key'] in OR], cwd='tools/orat39', check=True)
