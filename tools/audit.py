"""Audit: chants of every Temporale Mass against the St. Dominic Missal (1959) for the same day."""
import json, re, sys, io, unicodedata
D = json.loads(open('site/data/masses.js', encoding='utf8').read().split('var DOMINICAN = ', 1)[1].rstrip().rstrip(';'))
dm = json.load(open('dm_masses.json'))['masses']
temp = D['sections'][0]['items']
dmt = [m for m in dm if m['kind'] == 'tempore' and m['parts'].get('in')]
inc = lambda i: D['chants'].get(str(i), {}).get('i', '?')
def fl(s): return re.sub(r'[^a-z]', '', ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if not unicodedata.combining(c)).replace('j','i'))
# global alignment of our Temporale with the Missal's, by Introit text
n, m = len(temp), len(dmt)
def same_in(k, d):
    a = (D['masses'][k]['parts'].get('in') or [{}])[0].get('id')
    return a is not None and any(fl(inc(a))[:10] == fl(inc(b))[:10] for b in d['parts']['in'])
F = [[0]*(m+1) for _ in range(n+1)]; B = [[None]*(m+1) for _ in range(n+1)]
for i in range(1, n+1):
    for j in range(1, m+1):
        o = [(F[i-1][j-1] + (2 if same_in(temp[i-1], dmt[j-1]) else -5), 'm'), (F[i-1][j], 'a'), (F[i][j-1], 'b')]
        F[i][j], B[i][j] = max(o)
i, j, pairs = n, m, []
while i > 0 and j > 0:
    if B[i][j] == 'm': pairs.append((temp[i-1], dmt[j-1])); i -= 1; j -= 1
    elif B[i][j] == 'a': i -= 1
    else: j -= 1
pairs.reverse()
json.dump({k: dmt.index(d) for k, d in pairs}, open('temporale_dm_pairs.json', 'w'))
diff = 0
for k, d in pairs:
    M = D['masses'][k]; out = []
    for p, ids in d['parts'].items():
        ours = [c['id'] for c in M['parts'].get(p, [])]
        a = [fl(inc(x))[:12] for x in ours]; b = [fl(inc(x))[:12] for x in ids]
        if p in ('gr', 'al') and len(ids) > 1: b = b[:len(a)] if a else b
        if not set(b) <= set(a): out.append('%s: ours %s / Missal %s' % (p, [inc(x)[:22] for x in ours], [inc(x)[:22] for x in ids]))
    if out:
        diff += 1
        if '-v' in sys.argv: print(k, M['en'][:40], '\n   ' + '\n   '.join(out))
print('Temporale paired with the Missal:', len(pairs), 'of', len(temp), '; with differences:', diff)
