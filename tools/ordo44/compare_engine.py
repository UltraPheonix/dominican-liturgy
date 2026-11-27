"""Compare the Missal ranking engine (engine_dump.js) with the Ordo O.P. 1944 (parse2.py) day by day.
usage: compare_engine.py /tmp/e44.json tools/ordo44/ordo1944b.json [--all]"""
import sys, json, re, unicodedata, datetime
E = {r['date']: r for r in json.load(open(sys.argv[1]))}; O = json.load(open(sys.argv[2]))
ALL = '--all' in sys.argv
def n(s):
    s = ''.join(c for c in unicodedata.normalize('NFD', (s or '').lower()) if not unicodedata.combining(c))
    s = s.replace('æ', 'ae').replace('œ', 'oe').replace('j', 'i')
    return re.sub(r'[^a-z]', '', s)
STOP = set('ordinis praedicatorum sociorum apostoli apostolorum sancti sanctae sanctorum beati beatae conf confessoris virg mart matris episc papae dupl duplex semid simpl offic festiv tot totum classis'.split())
def fold(s):  # the Ordo text has letter-spaced names: compare on letters only
    return n(s)
def toks(s):
    s = ''.join(c for c in unicodedata.normalize('NFD', (s or '').lower()) if not unicodedata.combining(c)).replace('æ','ae').replace('j','i')
    return [w[:5] for w in re.findall(r'[a-z]{4,}', s) if w not in STOP]
bad = 0
for o in O:
    r = E.get(o['date'])
    if not r: continue
    h = o['head'] or ''
    hf = fold(h[:90])
    off = r['office']; ttl = off.get('title') or ''
    m0 = r['masses'][0] if r['masses'] else {}
    mt = r.get('mtitle', '')
    ok = None
    if not o['text']: ok = '?'
    else:
        ws = [w for w in toks(ttl) if len(w) >= 4]
        if off['kind'] in ('temporal',) and re.search(r'deea|deeo|^[ivx]+p?o|dom|advent|quadr|septuag|sexag|quinquag|palmar|resurr|albis|cinerum|maior|cena|parasc|pentec|deoct', hf[:40]): ok = True
        elif off['kind'] == 'octave' and re.search(r'deoct|deoc', hf[:30]): ok = True
        elif off['kind'] == 'octday' and 'diesoct' in hf[:20]: ok = True
        elif off['kind'] == 'bvmSat' and 'bmvinsabb' in hf: ok = True
        elif off['kind'] == 'vigil' and 'vig' in hf[:30] and 'deea' in hf: ok = True
        elif ws and (ws[0] in hf[:60] or max(ws, key=len) in hf[:60]): ok = True
        else: ok = False
    if ALL or ok is False:
        if ok is False: bad += 1
        wd = 'MTWTFSS'[datetime.date.fromisoformat(o['date']).weekday()]
        print('%s %s %s | Ordo: %-60s | engine: %s %s [%s] -> %s' % ('X' if ok is False else ' ', o['date'][5:], wd, re.sub(r'\s+', ' ', h)[:60], off['kind'], ttl[:40], off.get('rank', ''), ','.join((m['key'] or '-') for m in r['masses'])))
print(bad, 'days differ (of', sum(1 for o in O if o['text']), 'read)')
