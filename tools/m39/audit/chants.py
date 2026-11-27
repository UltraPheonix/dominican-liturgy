"""Audit: the chants of every dated site Mass against the Missale O.P. 1939 (text layer tools/orat39/m39lin.txt).
For each Mass: the M39 entry for its day (title words matched), the chant incipits printed there (or the Common it points to),
and the site's chants (gabc text). Writes tools/m39/audit/chants_report.md + /tmp/x/audit.json."""
import re, json, os, unicodedata, sys
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
L = open(R + '/tools/orat39/m39lin.txt').read().split('\n')
D = json.loads(open(R + '/data/masses.js').read().split('var DOMINICAN = ', 1)[1].rstrip().rstrip(';'))
MON = ['Januarii','Februarii','Martii','Aprilis','Maii','Junii','Julii','Augusti','Septembris','Octobris','Novembris','Decembris']
def n(s): return ' '.join(re.sub(r'[^a-z ]', ' ', unicodedata.normalize('NFD', (s or '').lower().replace('æ','ae').replace('œ','oe').replace('ǽ','ae').replace('j','i').replace('y','i')).encode('ascii','ignore').decode()).split())
def gtext(cid):
    f = R + '/gabc/%s.gabc' % cid
    if not os.path.exists(f): return ''
    g = open(f).read().split('%%', 1)[-1]
    t = n(re.sub(r'<[^>]+>|[{}*]', ' ', re.sub(r'\([^)]*\)', '', g)))
    t = re.sub(r'^(alleluia )+(v )?', '', t)
    return re.sub(r'^v ', '', t)
STOPW = set('s ss b bb et conf ep mart virg vid op o p eccl doct papae papa apostoli mm sociorum soc in de a ab ad i ii v iii c e m d abb ord praed'.split())
def words(s): return [w for w in n(s).split() if w not in STOPW and len(w) > 2]
def segment(mo, dd, title):
    pat = re.compile(r'^Die %s %s\b' % (r'\s?'.join(str(dd)), MON[mo]))
    best = None
    for h, l in enumerate(L):
        if h < 30000 or not pat.match(l.strip()): continue
        end = next((j for j in range(h + 1, min(len(L), h + 900)) if re.match(r'^Die \d', L[j].strip())), h + 900)
        seg = L[h:end]
        # several Masses on one day: split at the titles (capital lines after the date)
        t = ' '.join(x.strip() for x in seg if not x.startswith('@@')).replace('\xad ', '').replace('­ ', '')
        sc = len(set(words(title)) & set(words(t[:400])))
        if best is None or sc > best[0]: best = (sc, h, t)
    return best
PART = [('in', r'Officium'), ('of', r'Offertorium'), ('co', r'Communio')]
def incipits(t):
    out = {}
    m = re.search(r'Officium\s+(?:[A-Z][a-z]*\.\s*\d[\d ,;.]*)?\s*([A-Za-z][^.:;]{3,60})', t)
    if m: out['in'] = m.group(1)
    m = re.search(r'Offertorium\s+(?:[A-Z][a-z]*\.\s*\d[\d ,;.]*)?\s*([A-Za-z][^.:;]{3,60})', t)
    if m: out['of'] = m.group(1)
    m = re.search(r'Communio\s+(?:[A-Z][a-z]*\.\s*\d[\d ,;.]*)?\s*([A-Za-z][^.:;]{3,60})', t)
    if m: out['co'] = m.group(1)
    # Alleluia verse
    m = re.search(r'Alleluia,\s*alleluia\.\s*\S*\s*(?:[A-Z][a-z]*\.\s*\d[\d ,;.]*)?\s*([A-Z][^.:;]{3,60})', t)
    if m: out['al'] = m.group(1)
    m = re.search(r'Tractus\s+(?:[A-Z][a-z]*\.\s*\d[\d ,;.]*)?\s*([A-Z][^.:;]{3,60})', t)
    if m: out['tr'] = m.group(1)
    # Gradual: the first chant after the Lesson/Epistle text: a scripture reference followed by text, before Alleluia/Tractus/Sequentia
    i = t.find('Lectio'); j = t.find('Sequentia sancti', i)
    if i >= 0 and j > i:
        z = t[i:j]
        ms = list(re.finditer(r'(?:Ps\.|Eccli\.|Eccl\.|Sap\.|Exodi|Matth\.|Luc\.|Joann\.|Isai\.|Prov\.|Cant\.|Jac\.|Apoc\.|Dan\.|Hebr\.|Gal\.|Rom\.|Phil\.|Osee|Judith|Thren\.|Gen\.|Jer\.|Act\.)\s*[\d ,;et]*\s*([A-Z][^.:;]{3,60})', z))
        ms = [x for x in ms if not re.search(r'(Alleluia|Tractus)', z[max(0, x.start() - 30):x.start()])]
        if ms: out['gr'] = ms[0].group(1)
    common = re.search(r'(?:ut|de) in (?:Comm\.?|Communi|eodem Communi|Festis)[^.]{0,80}?pag\.\s*(\d+\*)', t[:500])
    return out, (common.group(0) if common else None)
import difflib
def match(inc, cids):
    inc = re.split(r',?\s*(?:ut|de|sicut) (?:in )?(?:Comm|Festis|festo|eodem)', inc)[0]
    q = n(inc).replace(' ', '')[:22]
    if len(q) < 4: return True
    for c in cids:
        g = gtext(c).replace(' ', '')
        for off in range(0, 12):
            if difflib.SequenceMatcher(None, q, g[off:off + len(q)]).ratio() >= 0.72: return True
    return False
rows = []
for k, m in D['masses'].items():
    if m.get('month') is None or not m.get('day') or not k.startswith('S'): continue
    seg = segment(m['month'], m['day'], m['title'])
    if not seg or seg[0] == 0: rows.append((k, m['title'], 'NO M39 ENTRY', {}, None, m.get('conf'))); continue
    inc, common = incipits(seg[2][:6000])
    bad = {}
    for p, txt in inc.items():
        cids = [x['id'] for x in m['parts'].get(p, [])] + [x['id'] for s in m.get('season', {}).values() for x in s.get(p, [])]
        if p in ('gr', 'al', 'tr') and common: continue
        if not cids: bad[p] = (txt, 'MISSING on site')
        elif not match(txt, cids): bad[p] = (txt, 'site: ' + ' / '.join(' '.join(gtext(c).split()[:5]) for c in cids))
    rows.append((k, m['title'], seg[1] + 1, bad, common, m.get('conf')))
json.dump(rows, open('/tmp/x/audit.json', 'w'), ensure_ascii=False)
nb = [r for r in rows if r[3] or r[2] == 'NO M39 ENTRY']
print(len(rows), 'Masses;', len(nb), 'with differences')
for r in nb: print(r[0], '|', r[1][:45], '|', r[2], '|', r[5], '|', r[4] and r[4][:50], '|', json.dumps(r[3], ensure_ascii=False)[:400])
