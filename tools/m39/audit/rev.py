"""Reverse audit: is every chant the site sings for a dated Mass (in, gr, al, tr, se, of, co) printed in that day's
entry of the Missale O.P. 1939 (tools/orat39/m39lin.txt)? A chant whose first words are not found anywhere in the entry is
listed, unless the entry refers that part (or the whole Mass) to a Common. Output: tools/m39/audit/rev_report.txt"""
import re, json, os, unicodedata, difflib, sys
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
L = open(R + '/tools/orat39/m39lin.txt').read().split('\n')
D = json.loads(open(R + '/data/masses.js').read().split('var DOMINICAN = ', 1)[1].rstrip().rstrip(';'))
MON = ['Januarii','Februarii','Martii','Aprilis','Maii','Junii','Julii','Augusti','Septembris','Octobris','Novembris','Decembris']
def n(s): return ' '.join(re.sub(r'[^a-z ]', ' ', unicodedata.normalize('NFD', (s or '').lower().replace('æ','ae').replace('œ','oe').replace('ǽ','ae').replace('j','i').replace('y','i').replace('v','u')).encode('ascii','ignore').decode()).split())
def gtext(cid):
    f = R + '/gabc/%s.gabc' % cid
    if not os.path.exists(f): return ''
    g = open(f).read().split('%%', 1)[-1]
    t = n(re.sub(r'<[^>]+>|[{}*]', ' ', re.sub(r'\([^)]*\)', '', g)))
    t = re.sub(r'^(alleluia )+(u )?', '', t)
    return re.sub(r'^u ', '', t)
STOPW = set('s ss b bb et conf ep mart uirg uid op o p eccl doct papae papa apostoli mm sociorum soc in de a ab ad i ii u iii c e m d abb ord praed die'.split())
def words(s): return [w for w in n(s).split() if w not in STOPW and len(w) > 2]
STARTS = [h for h, l in enumerate(L) if h > 30000 and re.match(r'^Die \d', l.strip())]
def entries(mo, dd):
    pat = re.compile(r'^Die %s %s\b' % (r'\s?'.join(str(dd)), MON[mo]))
    out = []
    for i, h in enumerate(STARTS):
        if pat.match(L[h].strip()):
            end = STARTS[i + 1] if i + 1 < len(STARTS) else h + 900
            out.append((h, ' '.join(x.strip() for x in L[h:end] if not x.startswith('@@')).replace('\xad ', '').replace('- ', '')))
    return out
def found(q, T):
    q = q.replace(' ', '')[:18]
    if len(q) < 6: return True
    T = T.replace(' ', '')
    if q in T: return True
    sm = difflib.SequenceMatcher(None, T, q, autojunk=False)
    m = sm.find_longest_match(0, len(T), 0, len(q))
    if m.size >= len(q) * 0.6:
        a = max(0, m.a - m.b)
        return difflib.SequenceMatcher(None, T[a:a + len(q) + 2], q).ratio() >= 0.75
    return False
PN = {'in': 'Officium', 'gr': 'Graduale', 'al': 'Alleluia', 'tr': 'Tractus', 'se': 'Sequentia', 'of': 'Offertorium', 'co': 'Communio'}
rep = []
for k, m in D['masses'].items():
    if m.get('month') is None or not m.get('day') or not k.startswith('S'): continue
    es = entries(m['month'], m['day'])
    if not es: rep.append('%-9s %-48s NO ENTRY in M39' % (k, m['title'][:48])); continue
    tw = set(words(m['title']))
    es.sort(key=lambda e: -len(tw & set(words(e[1][:300]))))
    h, T = es[0]; Tn = n(T)
    if not (tw & set(words(T[:300]))): rep.append('%-9s %-48s no matching title (l.%d)' % (k, m['title'][:48], h + 1)); continue
    commonref = re.search(r'(ut|sicut|de) in (Comm|Communi|eodem|festo|Festis)', T[:600])
    bad = []
    for p in ('in', 'gr', 'al', 'tr', 'se', 'of', 'co'):
        for c in m['parts'].get(p, []):
            t = gtext(c['id'])
            if not t: bad.append('%s %s NO GABC' % (p, c['id'])); continue
            if not found(t, Tn): bad.append('%s %s "%s"' % (p, c['id'], ' '.join(t.split()[:5])))
    if bad: rep.append('%-9s %-48s l.%-6d %s%s\n          %s' % (k, m['title'][:48], h + 1, m.get('conf'), ' COMMONREF' if commonref else '', '\n          '.join(bad)))
open(R + '/tools/m39/audit/rev_report.txt', 'w').write('\n'.join(rep) + '\n')
print(len(rep))
