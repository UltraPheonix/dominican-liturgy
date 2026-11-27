"""Graduale O.P. (Suarez 1950) chants in the GregoBase dump (tools/gregobase/gb.sqlite, source 14), by part and incipit.
python3 tools/m39/new/gb14.py in "Sacerdotes Dei" gr "Juravit" ...  (part '*' = any). Marks ids the site already has."""
import sqlite3, sys, re, json, unicodedata
D = json.loads(open('data/masses.js').read().split('var DOMINICAN = ', 1)[1].rstrip().rstrip(';'))
c = sqlite3.connect('tools/gregobase/gb.sqlite'); cur = c.cursor()
def n(s): return ' '.join(re.sub(r'[^a-z ]', '', unicodedata.normalize('NFD', (s or '').lower().replace('æ', 'ae').replace('œ', 'oe').replace('j', 'i')).encode('ascii', 'ignore').decode()).split())
ROWS = list(cur.execute('select c.id,c.incipit,c."office-part",s.page,c.gabc from gregobase_chants c join gregobase_chant_sources s on s.chant_id=c.id where s.source=14'))
def text(g):
    try: g = json.loads(g)
    except Exception: pass
    return n(re.sub(r'\([^)]*\)|<[^>]+>|[{}*]', '', g or ''))
IDX = [(i, inc, p, pg, text(g)) for i, inc, p, pg, g in ROWS]
a = sys.argv[1:]
for p, q in zip(a[::2], a[1::2]):
    qq = n(q)
    h = [(i, inc, pp, pg) for i, inc, pp, pg, t in IDX if (p == '*' or pp == p) and (n(inc).startswith(qq) or t.startswith(qq) or t[:300].find(qq) >= 0 and t.find(qq) < 15)]
    print('%-3s %-28s ->' % (p, q), '; '.join('%s%s[%s p%s]' % (i, '*' if str(i) in D['chants'] else '', pp, pg) for i, inc, pp, pg in h[:6]) or 'NONE')
