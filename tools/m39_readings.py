"""Check every Mass's Epistle/Lesson and Gospel (book and chapter) against the Missale O.P. 1939, using the Ordo's page."""
import io, sys, re, json
_o = sys.stdout; sys.stdout = io.StringIO()
import resolve_m39 as R
sys.stdout = _o
D = json.loads(open('site/data/masses.js', encoding='utf8').read().split('var DOMINICAN = ', 1)[1].rstrip().rstrip(';'))
ordo = json.load(open('ordo2026.json')); wins = json.load(open('wins2026.json'))
fl = lambda s: R.flat(s, digits=True)
BOOKS = [  # (pattern in the Missal heading, our book names)
 (r'adcorinthios\D{0,3}2|corinthios2|2adcorinth', ['Ad Corinthios 2']), (r'adcorinthios', ['Ad Corinthios 1']),
 (r'adthessalonicenses\D{0,3}2', ['Ad Thessalonicenses 2']), (r'adthessalonicenses', ['Ad Thessalonicenses 1']),
 (r'adtimotheum\D{0,3}2|2\D{0,2}c\d+$', ['Ad Timotheum 2']), (r'adtimotheum', ['Ad Timotheum 1']),
 (r'adromanos', ['Ad Romanos']), (r'adgalatas', ['Ad Galatas']), (r'adephesios', ['Ad Ephesios']), (r'adphilippenses', ['Ad Philippenses']),
 (r'adcolossenses', ['Ad Colossenses']), (r'adtitum', ['Ad Titum']), (r'adhebraeos', ['Ad Hebræos']), (r'iacobi', ['Jacobi']),
 (r'petri', ['Petri 1', 'Petri 2']), (r'ioannisapostoli|beatiioannis', ['Joannis 1', 'Joannis 2', 'Joannis 3']), (r'iudae', ['Judæ']),
 (r'actibusapostolorum|actuum', ['Actus Apostolorum']), (r'apocalyps', ['Apocalypsis']),
 (r'sapientiae', ['Sapientia', 'Ecclesiasticus', 'Proverbia', 'Canticum Canticorum', 'Ecclesiastes']), (r'ecclesiastic', ['Ecclesiasticus']),
 (r'isaiae', ['Isaias']), (r'ieremiae', ['Jeremias']), (r'ezechielis', ['Ezechiel']), (r'danielis', ['Daniel']), (r'ioel', ['Joel']), (r'osee', ['Osee']),
 (r'zachariae', ['Zacharias']), (r'malachiae', ['Malachias']), (r'ionae', ['Jonas']), (r'michaeae', ['Michæa']), (r'baruch', ['Baruch']),
 (r'exodi', ['Exodus']), (r'genesis', ['Genesis']), (r'levitici', ['Leviticus']), (r'numeri', ['Numeri']), (r'deuteronom', ['Deuteronomium']),
 (r'regum', ['Regum 1', 'Regum 2', 'Regum 3', 'Regum 4']), (r'esther', ['Esther']), (r'iudith', ['Judith']), (r'machabaeorum', ['Machabæorum 1', 'Machabæorum 2']),
 (r'sophoniae', ['Sophonias']), (r'aggaei', ['Aggæus']), (r'abdiae', ['Abdias']), (r'tobiae', ['Tobias']), (r'iob', ['Job']),
]
GOSP = {'matthaeum': 'Matthæus', 'marcum': 'Marcus', 'lucam': 'Lucas', 'ioannem': 'Joannes'}
def missal_readings(seg):
    out = []
    for m in re.finditer(r'lectio(\w{0,90}?)c(\d{1,3})', seg):
        head, ch = m.group(1), int(m.group(2))
        bk = next((b for p, b in BOOKS if re.search(p, head)), None)
        if bk: out.append(('E', bk, ch, m.start()))
    for m in re.finditer(r'(?:sequentia|initium)sanctievang\w{0,6}secundum(matthaeum|marcum|lucam|ioannem)\w{0,12}?c(\d{1,2})', seg):
        out.append(('G', [GOSP[m.group(1)]], int(m.group(2)), m.start()))
    return out
def gabc_text(i):
    try: t = open('site/gabc/%s.gabc' % i, encoding='utf8').read().split('%%', 1)[1]
    except Exception: return ''
    t = re.sub(r'\([^)]*\)', '', t); t = re.sub(r'<[^>]*>', '', t)
    return fl(t)
def ourref(r):
    m = re.match(r'(.+?) (\d+):', r['ref']); return (m.group(1), int(m.group(2))) if m else (None, None)
report = []; seen = set(); checked = 0
for o in ordo:
    if o['region'] or not o.get('m39') or o['date'] not in wins: continue
    k = wins[o['date']]
    if not k or k in seen: continue
    M = D['masses'].get(k)
    if not M or not M.get('readings'): continue
    p = R.pdf_page(o['m39'])
    if not p: continue
    text = fl(R.page_text.get(p, '') + R.page_text.get(p + 1, '') + R.page_text.get(p + 2, ''))
    intro = (M['parts'].get('in') or [{}])[0].get('id')
    it = gabc_text(intro)
    it = re.sub(r'^\w{0,4}?', '', it)
    a = -1
    for L in (24, 16, 12):
        a = text.find(it[1:1 + L]) if len(it) > L else -1
        if a >= 0: break
    if a < 0: continue
    # the Mass runs to the next Introit ("officium") at least 1500 letters on
    nxt = re.search(r'officium', text[a + 1500:])
    seg = text[max(0, a - 200): a + 1500 + (nxt.start() if nxt else 6000)]
    mr = missal_readings(seg)
    if not mr: continue
    seen.add(k); checked += 1
    ours = [(r['type'], ) + ourref(r) for r in M['readings']]
    for t, bks, ch, pos in mr:
        if not any((('G' if ot == 'Gospel' else 'E') == t) and ob in bks and och == ch for ot, ob, och in ours):
            report.append({'key': k, 'date': o['date'], 'name': o['name'], 'missal': '%s %s %d' % (t, '/'.join(bks), ch), 'ours': [r['ref'] for r in M['readings']], 'page': o['m39']})
json.dump(report, open('m39_readings_report.json', 'w'), ensure_ascii=False, indent=1)
print('Masses checked:', checked, 'differences:', len(report))
for r in report: print(r['date'], r['key'], r['name'][:30], '| M39:', r['missal'], '| ours:', r['ours'])
