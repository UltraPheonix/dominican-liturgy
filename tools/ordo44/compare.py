"""Compare the Mass the site gives for each day of 1944 (tools/check/day_audit.py output) with the Ordo O.P. 1944 (parse.py output).
usage: compare.py /tmp/y44.json /tmp/o44.json"""
import sys, json, re, unicodedata
Y = {r['date']: r for r in json.load(open(sys.argv[1]))}; O = json.load(open(sys.argv[2]))
D = json.loads(open('data/masses.js').read().split('var DOMINICAN = ', 1)[1].rstrip().rstrip(';'))
def n(s):
    s = ''.join(c for c in unicodedata.normalize('NFD', (s or '').lower()) if not unicodedata.combining(c))
    return re.sub(r'[^a-z ]', ' ', s.replace('æ', 'ae').replace('œ', 'oe').replace('j', 'i'))
STOP = set('sancti sanctae sanctorum beati beatae ss bb conf confessoris episcopi martyris martyrum virginis viduae doct doctoris eccl ecclesiae ord praed dupl duplex semid simpl tot toz cl cum oct solemni festiv offic fer dom sabb abb apost apostoli evang'.split())
def words(s): return set(w[:6] for w in n(s).split() if len(w) > 3 and w not in STOP)
TEMP = re.compile(r'^(Adv|Epi|Quad|Pasc|Pent|7a|6a|5a|Emb|Nat|Jan|Dec|Asc|Litaniis|CorpusChristi|SCJ|ChristusRex)')
bad = []
for o in O:
    if not o['text'] or o['date'] not in Y: continue
    r = Y[o['date']]; key = r['hash'][1:].split('&')[0]; m = D['masses'].get(key, {})
    head = re.sub(r'^\W*\d{0,2}\W*(Dom\.|Fer\.\s*\S+|Sabb\.)\s*', '', o['head'])
    ordo_temporal = bool(re.match(r'^(De ea|[IVX]+\.?\s*(P\.|Advent|Quadr)|Major|in Albis|Palmarum|Pasch|Pentec|Cinerum|post|infra|Feria|Vigil|.{0,40}De ea)', head)) or ' De ea' in head[:60]
    site_temporal = bool(TEMP.match(key))
    w1 = words(head[:70]); w2 = words(m.get('title', '') + ' ' + (m.get('en') or ''))
    ok = (ordo_temporal and site_temporal) or (w1 & w2)
    if key == 'C79s': ok = ok or 'B. M. V.' in head[:40] and 'Sabb' in o['head']
    if not ok: bad.append('%s %s | Ordo: %s | site: %s %s' % (o['date'], 'MTWTFSS'[__import__('datetime').date.fromisoformat(o['date']).weekday()], head[:75], key, m.get('title', '')[:40]))
print(len(bad), 'days differ'); print('\n'.join(bad))
