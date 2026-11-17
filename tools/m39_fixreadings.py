"""Propose the correct reference for readings the Missal does not confirm: read the Missal's reading after the Introit and locate it in the Vulgate."""
import re, json, sys, os
sys.path.insert(0, '/tmp')
from adj import F, flat
import m39_confirm as C
# Vulgate, flattened per book, with verse offsets
VB = {}
for fn in os.listdir('site/bible/la'):
    b = fn[:-4]; s = []; offs = []; n = 0
    for l in open('site/bible/la/' + fn, encoding='utf8'):
        c, v, t = l.rstrip('\n').split('\t', 2); f = re.sub(r'\d', '', flat(t))
        offs.append((n, int(c), int(v))); s.append(f); n += len(f)
    VB[b] = (''.join(s), offs)
def verse_at(b, pos):
    offs = VB[b][1]; lo = 0
    for i, (n, c, v) in enumerate(offs):
        if n > pos: break
        lo = i
    return offs[lo][1], offs[lo][2]
FORMULA = r'^(fratres|carissimi|carissime|inillotempore|indiebusillis|haecdicitdominusdeus|haecdicitdominus|indiebusillisdixit\w{0,12}|dixitiesus\w{0,20}?suis|inprincipio)'
LABEL = r'(graduale|alleluiaalleluia|tractus|offertorium|credo|sequentiasanctievangelii|initiumsanctievangelii|lectio|psps|communio|secreta|oratio)'
def readings_after(a):
    w = F[a:a + 14000]
    out = []
    for m in re.finditer(r'(lectio\w{0,60}?|sequentiasanctievangeliisecundum(?:matthaeum|marcum|lucam|ioannem)|initiumsanctievangelii\w{0,30}?)(?=fratres|carissim|inillotempore|indiebus|haec|in|[a-z])', w):
        typ = 'Gospel' if 'evangel' in m.group(1) else 'Epistle'
        start = m.end()
        nx = re.search(LABEL, w[start + 30:])
        body = w[start: start + 30 + (nx.start() if nx else 1500)]
        out.append((typ, m.start(), body))
        if typ == 'Gospel': break
    return out
def locate(body, prefer=None):
    body = re.sub(FORMULA, '', body)
    best = None
    for b, (s, offs) in VB.items():
        if b == 'Psalmi': continue
        hits = []
        for o in range(0, max(1, len(body) - 14), 12):
            k = body[o:o + 14]
            i = s.find(k)
            if i >= 0 and s.find(k, i + 1) < 0: hits.append((o, i))
        if len(hits) >= 3 and (best is None or len(hits) > len(best[1]) or (len(hits) == len(best[1]) and b == prefer)):
            best = (b, hits)
    if not best: return None
    b, hits = best
    # keep the main run of hits (consistent order)
    hits.sort(); base = [h for h in hits if abs((h[1] - hits[0][1]) - (h[0] - hits[0][0])) < 400 + h[0]]
    c1, v1 = verse_at(b, base[0][1]); c2, v2 = verse_at(b, base[-1][1] + 13)
    return b, c1, v1, c2, v2, len(base)
def fmt(b, c1, v1, c2, v2):
    return '%s %d: %d-%d' % (b, c1, v1, v2) if c1 == c2 else '%s %d: %d-%d; %d: %d-%d' % (b, c1, v1, 99, c2, 1, v2)
if __name__ == '__main__':
    R = json.load(open('m39_confirm.json'))
    keys = sorted({x[0] for x in R['bad']} | {x[0] for x in R['noanchor']}) if len(sys.argv) < 2 else sys.argv[1:]
    out = {}
    for k in keys:
        M = C.D['masses'][k]; A = C.anchors(M)
        found = None
        for a in A:
            rs = readings_after(a)
            loc = [(t, locate(body)) for t, pos, body in rs]
            loc = [(t, l) for t, l in loc if l]
            if loc: found = loc; break
        out[k] = {'ours': [r['ref'] for r in M['readings']], 'missal': [(t, fmt(*l[:5]), l[5]) for t, l in found] if found else None}
        print(k, M['title'][:40], '\n    ours  :', out[k]['ours'], '\n    missal:', out[k]['missal'])
    json.dump(out, open('m39_fix_proposals.json', 'w'), ensure_ascii=False, indent=1)
