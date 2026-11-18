"""Split a transcribed reading into paragraphs of a few verses, each paired with the Douay-Rheims
English of the same verses (site/bible).  usage: mkpassion.py latin.txt "Book" "14:1-15:46" name [verses-per-para]"""
import re, sys, unicodedata
def strip(s): return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
def n(w): return re.sub(r'[^a-z]', '', strip(w.lower()).replace('æ', 'ae').replace('œ', 'oe').replace('j', 'i'))
lat, book, rng, name = sys.argv[1:5]; per = int(sys.argv[5]) if len(sys.argv) > 5 else 4
a, b = rng.split('-'); c0, v0 = map(int, a.split(':')); c1, v1 = map(int, b.split(':'))
def verses(lang):
    out = []
    for l in open('/home/claude/build/site/bible/%s/%s.txt' % (lang, book), encoding='utf8'):
        c, v, t = l.rstrip('\n').split('\t', 2); c, v = int(c), int(v)
        if (c0, v0) <= (c, v) <= (c1, v1): out.append(((c, v), t))
    return out
VL, VE = verses('la'), dict(verses('en'))
W = open(lat, encoding='utf8').read().split(); NW = [n(w) for w in W]
SKIP = {'c', 's', ''}
idx = [i for i, x in enumerate(NW) if x not in SKIP]
starts = []
pos = 0
for cv, t in VL:
    key = [n(w) for w in t.split() if n(w)][:3]
    found = None
    for k in range(pos, min(len(idx), pos + 400)):
        if [NW[j] for j in idx[k:k + 3]] == key: found = k; break
    if found is None:
        for k in range(pos, min(len(idx), pos + 120)):
            if [NW[j] for j in idx[k:k + 2]] == key[:2]: found = k; break
    if found is not None:
        i = idx[found]
        while i > 0 and (NW[i - 1] in ('c', 's') or W[i - 1] == '✠'): i -= 1
        starts.append((cv, i)); pos = found + 1
    else:
        starts.append((cv, None))
miss = [cv for cv, i in starts if i is None]
groups = []; cur = []
for cv, i in starts:
    if i is not None and (not cur or len(cur) >= per):
        if cur: groups.append(cur)
        cur = [(cv, i)]
    else: cur.append((cv, i))
if cur: groups.append(cur)
groups[0][0] = (groups[0][0][0], 0)
la, en = [], []
for k, g in enumerate(groups):
    s = g[0][1]; e = groups[k + 1][0][1] if k + 1 < len(groups) else len(W)
    la.append(' '.join(W[s:e])); en.append(' '.join(VE[cv] for cv, _ in g))
open(name + '_parts.txt', 'w', encoding='utf8').write('\n\n'.join(la) + '\n')
open(name + '_en.txt', 'w', encoding='utf8').write('\n\n'.join(en) + '\n')
print(len(VL), 'verses,', len(groups), 'paragraphs; unmatched verse starts:', miss, file=sys.stderr)
