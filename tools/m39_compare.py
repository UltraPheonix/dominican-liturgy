"""Compare every dated Mass on the site with its Mass in the Missale O.P. (1939)."""
import io, sys, re, json
_o = sys.stdout; sys.stdout = io.StringIO()
import resolve_m39 as R
sys.stdout = _o
import m39seg as S
D = json.loads(open('site/data/masses.js', encoding='utf8').read().split('var DOMINICAN = ', 1)[1].rstrip().rstrip(';'))
inc = lambda i: D['chants'].get(str(i), {}).get('i', '?')
fl = R.flat
def words(s): return set(w[:5] for w in re.findall(r'[a-z]{4,}', fl_keep(s)))
def fl_keep(s):
    import unicodedata
    s = s.replace('æ','ae').replace('œ','oe').replace('j','i').replace('J','i')
    return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c)).lower()
out = []
for sec in D['sections']:
    if sec['id'] not in ('sanctorum', 'beati'): continue
    for k in sec['items']:
        M = D['masses'][k]
        if 'month' not in M or M['month'] > 11: continue
        segs = S.seg(M['day'], M['month'])
        if not segs: continue
        nm = [w for w in words(M['title']) if w not in ('missa','confe','marty','virgi','episc','sanct','beati','ordin','praed')]
        best = max(segs, key=lambda s: sum(1 for w in nm if w in s[:160]))
        if not any(w in best[:160] for w in nm): continue
        # cut the segment at the next feast heading within it (another "officium" after a "die" was already cut)
        found = R.find_parts(None, (), re.sub(r'\d', '', best))
        comm = R.COMMREF.search(best[:600])
        for p, hits in found.items():
            pa = [h for h in hits if h[1] == '' and h[2] == 2]
            if len(pa) != 1: continue
            c = pa[0][0]
            ours = [x['id'] for x in M['parts'].get(p, [])]
            if not ours or any(fl(inc(o))[:10] == c['inc'][:10] for o in ours): continue
            out.append({'key': k, 'title': M['title'], 'part': p, 'ours': [inc(o) for o in ours], 'ours_inferred': any(x.get('inferred') for x in M['parts'].get(p, [])),
                        'm39': c['inc'], 'm39_id': c['id'], 'm39_page': c['page'], 'common': bool(comm)})
json.dump(out, open('m39_diffs.json', 'w'), ensure_ascii=False, indent=1)
print(len(out))
for o in out: print(o['key'], o['title'][:34], o['part'], o['ours'][:1], '->', o['m39'][:24], o['m39_id'], 'p.'+o['m39_page'], 'INF' if o['ours_inferred'] else '', 'COMM' if o['common'] else '')
