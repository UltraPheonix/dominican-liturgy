"""From /tmp/x/audit.json: for each in/gr/of/co (and al, tr) mismatch, the Graduale O.P. 1950 chants (GregoBase source 14)
whose text begins with the incipit printed in the Missale O.P. 1939."""
import json, re, sqlite3, unicodedata, sys
R = '/home/claude/dominican-liturgy'
D = json.loads(open(R + '/data/masses.js').read().split('var DOMINICAN = ', 1)[1].rstrip().rstrip(';'))
def n(s): return ' '.join(re.sub(r'[^a-z ]', '', unicodedata.normalize('NFD', (s or '').lower().replace('æ','ae').replace('œ','oe').replace('j','i').replace('y','i')).encode('ascii','ignore').decode()).split())
c = sqlite3.connect(R + '/tools/gregobase/gb.sqlite')
ROWS = list(c.execute('select c.id,c."office-part",s.page,c.gabc from gregobase_chants c join gregobase_chant_sources s on s.chant_id=c.id where s.source=14'))
def text(g):
    try: g = json.loads(g)
    except Exception: pass
    t = n(re.sub(r'<[^>]+>|[{}*]', ' ', re.sub(r'\([^)]*\)', '', g or '')))
    t = re.sub(r'^(alleluia )+(v )?', '', t)
    return t
IDX = [(i, p, pg, text(g)) for i, p, pg, g in ROWS]
rows = json.load(open('/tmp/x/audit.json'))
out = []
for k, title, line, bad, common, conf in rows:
    if not isinstance(bad, dict): continue
    for p, (inc, site) in bad.items():
        q = n(re.split(r',?\s*(?:ut|de|sicut) (?:in )?(?:Comm|Festis|festo|eodem)', inc)[0])
        q = ' '.join(q.split()[:4])
        if len(q) < 6: continue
        hits = [(i, pp, pg) for i, pp, pg, t in IDX if t.startswith(q) or (len(q) > 10 and t[:len(q) + 12].find(q) >= 0)]
        hp = [h for h in hits if h[1] == p]
        out.append((k, p, inc[:50], site[:70], hp or hits))
for o in out: print(o[0], o[1], '|', o[2], '|', o[3], '|', o[4][:4])
