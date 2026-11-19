"""OMR of the Triduum (1927) chant pieces -> gabc.
Notes go to the OCR syllable they stand over (syllable x from the OCR word box, split by its letters);
the OCR syllables are aligned letter by letter with the right text, and each right syllable takes their notes."""
import sys, os, re, json, pickle, difflib
sys.path.insert(0, '/home/claude/dominican-liturgy/tools/pdfomr'); sys.path.insert(0, '/home/claude/build/abl')
import importlib.util
spec = importlib.util.spec_from_file_location('m39lib', '/home/claude/build/abl/m39lib.py'); L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
import pieces
S = pickle.load(open(os.environ.get('TRI_CACHE', '/home/claude/build/tri_staves.pkl'), 'rb'))
import numpy as np, gcache
def clef_end(x, g):
    L_ = x['L']; s = x['s']; xa = int(x['x'][0] - 0.3 * s); xb = int(x['x'][0] + 1.8 * s)
    B = g[int(L_[0] - 1.2 * s):int(L_[3] + 1.2 * s), xa:xb] < 110
    B[B.mean(1) > 0.6] = False
    xs = np.where(B.sum(0) > 2)[0]
    if not len(xs): return x['x'][0] + 0.6 * s
    pv = xs[0]
    for c in xs[1:]:
        if c - pv > 3: break
        pv = c
    w = (pv - xs[0]) / s
    end = xa + pv
    # an F clef: punctum + C, the two runs close together
    rest = [c for c in xs if c > pv]
    if w < 0.45 and rest and (rest[0] - pv) < 0.3 * s:
        pv2 = rest[0]
        for c in rest[1:]:
            if c - pv2 > 3: break
            pv2 = c
        end = xa + pv2
    return end + 0.15 * s
def obliques(items):
    """a wide component read as head-wide slices: when its path runs diagonally (porrectus, oblique clivis) the slices in
    between are not notes; keep the two ends (and anything else in the end slices)"""
    by = {}
    for it in items:
        if it[1] == 'note' and len(it) > 7: by.setdefault(it[4], []).append(it)
    drop = set()
    for cid, its in by.items():
        nsl = its[0][6]
        if nsl < 3: continue
        sl = {}
        for it in its: sl.setdefault(it[5], []).append(it)
        if len(sl) < 3: continue
        qs = sorted(sl); path = [min(sl[qs[0]], key=lambda t: t[7])]
        for q in qs[1:]:
            path.append(min(sl[q], key=lambda t: abs(t[7] - path[-1][7])))
        ys = [p[7] for p in path]
        d = [b_ - a_ for a_, b_ in zip(ys, ys[1:])]
        if abs(ys[-1] - ys[0]) >= 0.4 and (all(v >= -0.05 for v in d) or all(v <= 0.05 for v in d)):
            for p in path[1:-1]: drop.add(id(p))
    # the same pitch in neighbouring slices of one component is one head cut in two (the end of an oblique, a wide head)
    for cid, its in by.items():
        for it in its:
            if id(it) in drop: continue
            for jt in its:
                if jt is not it and id(jt) not in drop and jt[5] == it[5] + 1 and jt[2] == it[2]: drop.add(id(jt))
    return [it for it in items if id(it) not in drop]
for k in S:
    for x in S[k]: x['items'] = obliques(x['items'])
for k in S:
    g = None
    for x in S[k]:
        if 'clef_end' not in x:
            g = gcache.G(*k) if g is None else g
            x['clef_end'] = clef_end(x, g)
MODES = dict(r01=8, r02=8, r03=5, r04=8, r05=8, r06=7, r07=7, r08=1, r09=1, r10=2, a01=1, a02=7, a03=7, a04=5, a05=7, a06=1, a07=1, a08=3,
             a09=3, a10=4, a11=8, a12=1, a13=1, a14=7, a15=2, a16=8, a17=1, a18=None, a19=2, a20=1, a21=1, a22=4, a23=8, a24=2, a25=8,
             a26=5, a27=5, a28=1, a29=1, a30=7, a31=1, a32=6)
FINAL = {1: 're', 2: 're', 3: 'mi', 4: 'mi', 5: 'fa', 6: 'fa', 7: 'sol', 8: 'sol'}
NAMES = ['do', 're', 'mi', 'fa', 'sol', 'la', 'si']
CLEFS = {'c4': ('j', 0), 'c3': ('h', 0), 'c2': ('f', 0), 'f3': ('h', 3), 'f4': ('j', 3)}
def pitch(letter, clef):
    cl, base = CLEFS[clef]
    return NAMES[(base + ord(letter) - ord(cl)) % 7]

def ocr_sylls(x):
    """[(syllable, x0)]: OCR syllables with the x of their start. Inside a hyphenated word the syllables are found at the
    widest blank gaps of the printed lyric (the hyphen's thin stroke counts as blank)."""
    toks, items, s = L.staff_syllables(x)
    g = gcache.G(x['page'], x['side']); L_ = x['L']
    y0 = int(L_[3] + 0.6 * s); y1 = int(L_[3] + 3.0 * s)
    band = g[y0:y1] < 110
    out = []
    for a0, a1, tt in sorted(x['words']):
        tt = tt.translate(str.maketrans('16053', 'loosa'))
        t2 = re.sub(r'[^A-Za-zæœÆŒÀ-ÿ\-]', '', tt)
        if not t2.replace('-', ''): continue
        parts = []
        for p in [p for p in t2.split('-') if p]:
            st = L.syllables(p); ends = st[1:] + [len(p)]
            parts.append([p[st[k]:ends[k]] for k in range(len(st))])
        syl = [y for p in parts for y in p]
        k = len(syl) - 1
        a0i, a1i = int(a0), int(a1)
        starts = [a0]
        if k > 0 and a1i - a0i > 10:
            ink = band[:, a0i:a1i].sum(0)
            blank = ink < 0.12 * (y1 - y0)
            runs = []; i = 0
            while i < len(blank):
                if blank[i]:
                    j = i
                    while j < len(blank) and blank[j]: j += 1
                    if i > 0 and j < len(blank): runs.append((j - i, i, j))
                    i = j
                else: i += 1
            # the hyphen breaks (between the printed parts) are the widest gaps; inside a part, letters' share
            nh = len(parts) - 1
            best = sorted(sorted(runs, reverse=True)[:nh], key=lambda r: r[1])
            cuts = [a0 + r[2] for r in best]
            bounds = [a0] + cuts + [a1]
            starts = []
            for pi, p in enumerate(parts):
                b0, b1 = bounds[pi], bounds[pi + 1] if pi + 1 < len(bounds) else a1
                n = sum(len(z) for z in p) or 1; acc = 0
                for z in p: starts.append(b0 + (b1 - b0) * acc / n); acc += len(z)
        for z, sx in zip(syl, starts): out.append((z, sx))
    return out, items, s

def build(code, text, staves):
    C = L.correct_syllables(text); CF = ''.join(L.flat(c[0]) for c in C); cstart = [c[1] for c in C]
    notes = [[] for _ in C]; bars = [None] * len(C)
    F = ''; recs = []
    for key in staves:
        x = S[key[:2]][key[2]]
        sy, items, s = ocr_sylls(x)
        f0 = len(F)
        for t, x0 in sy:
            recs.append((key, t, x0, len(F), s)); F += L.flat(t)
        recs.append((key, None, None, len(F), s))
    sm = difflib.SequenceMatcher(None, F, CF, autojunk=False); blocks = sm.get_matching_blocks()
    def fmap(i):
        best = 0
        for a, b, n in blocks:
            if a <= i < a + n: return b + (i - a)
            if a + n <= i: best = b + n + (i - a - n)
        return best
    def syl_at(ci): return max([k for k, c in enumerate(cstart) if c <= ci], default=0)
    spans = []; sxs = {}
    for key in staves:
        x = S[key[:2]][key[2]]
        sy, items, s = ocr_sylls(x)
        mine = [r for r in recs if r[0] == key and r[1] is not None]
        if not mine: continue
        # x of every OCR letter (spread over its syllable), then each right syllable starts at the x of its first letter
        xF = {}
        for k, r in enumerate(mine):
            nxt = mine[k + 1][2] if k + 1 < len(mine) else r[2] + 1.2 * s * max(1, len(L.flat(r[1])))
            ln = max(1, len(L.flat(r[1])))
            w = min(nxt - r[2], 0.55 * s * ln)
            for q in range(ln): xF[r[3] + q] = r[2] + w * q / ln
        first = {}
        for i in sorted(xF):
            kk = min(syl_at(fmap(i)), len(C) - 1)
            if kk not in first: first[kk] = xF[i]
        ks = sorted(first)
        # syllables of the span the OCR skipped entirely get a place between their neighbours
        if ks:
            for kk in range(ks[0], ks[-1] + 1):
                if kk not in first:
                    a_ = max(k2 for k2 in first if k2 < kk); b_ = min(k2 for k2 in first if k2 > kk)
                    first[kk] = first[a_] + (first[b_] - first[a_]) * (kk - a_) / (b_ - a_)
        ks = sorted(first)
        tgt = ks; xs = [first[k] for k in ks] + [1e9]
        # keep x increasing
        for k in range(1, len(ks)): xs[k] = max(xs[k], xs[k - 1] + 1)
        mine = [None] * len(ks)
        nts = [it for it in items if it[1] == 'note']
        for it in nts:
            j = max([k for k in range(len(ks)) if xs[k] - 0.45 * s <= it[0]], default=0)
            notes[tgt[j]].append((it[0], it[2]))
        for bb in [it for it in items if it[1] == 'bar']:
            cand = [tgt[k] for k in range(len(mine)) if xs[k] < bb[0] and any(xs[k] - 0.45 * s <= n[0] < bb[0] for n in nts)]
            if cand: bars[max(cand)] = {'half': ';', 'full': ':', 'double': '::'}[bb[2]]
        spans.append((key, tgt[0], tgt[-1]))
        for k in range(len(mine)):
            sxs.setdefault(tgt[k], (key, xs[k], s))
    # a syllable left without notes takes the nearest neume of a neighbour that has more than one
    def clusters(ns, s):
        ns = sorted(ns); cl = []
        for n in ns:
            if cl and n[0] - cl[-1][-1][0] < 0.9 * s: cl[-1].append(n)
            else: cl.append([n])
        return cl
    for _ in range(2):
        for i in range(len(C)):
            if notes[i] or i not in sxs: continue
            key, sx, s = sxs[i]
            best = None
            for j, side in ((i - 1, -1), (i + 1, 0)):
                if j < 0 or j >= len(C) or not notes[j] or sxs.get(j, (None,))[0] != key: continue
                cl = clusters(notes[j], s)
                if len(cl) < 2: continue
                c = cl[side]; d = abs(c[0][0] - sx)
                if best is None or d < best[0]: best = (d, j, c)
            if best and best[0] < 3 * s:
                d, j, c = best
                notes[j] = [n for n in notes[j] if n not in c]; notes[i] = list(c)
    return C, notes, bars, spans

def gabc(C, notes, bars, fix={}):
    g = []; out = []
    for i, (c, n, b) in enumerate(zip(C, notes, bars)):
        nn = fix.get(str(i)) or (L.groups_gabc(n) or '?')
        if str(i) + 'bar' in fix: b = fix[str(i) + 'bar'] or None
        t = c[0].rstrip()
        out.append((t, nn, b))
        g.append('%s(%s)' % (t, nn) + (' (%s)' % b if b else '') + (' ' if c[3] else ''))
    return ''.join(g).replace('  ', ' '), out

if __name__ == '__main__':
    FIX = json.load(open('/home/claude/build/abl/fix.json')) if os.path.exists('/home/claude/build/abl/fix.json') else {}
    RES = {}
    for code, name, a, b, text in pieces.P + [(m, r, a, b, t) for m, r, a, b, t in pieces.PM]:
        st = pieces.rng(a, b)
        C, notes, bars, spans = build(code, text, st)
        g, out = gabc(C, notes, bars, FIX.get(code, {}))
        # the clef: the one that ends the piece on the mode's final
        last = [n for t, n, b_ in out if n and n != '?']
        fin = last[-1][-1] if last else None
        m = MODES.get(code); want = FINAL.get(m)
        ok = [cl for cl in CLEFS if fin and pitch(fin, cl) == want]
        RES[code] = {'gabc': g, 'out': out, 'spans': spans, 'final': fin, 'clefs': ok, 'nx': [list(n) for n in notes]}
        unread = [i for i, (t, n, b_) in enumerate(out) if n == '?']
        print('%s %-24s final %s mode %s -> %s  unread %d %s' % (code, name, fin, m, ok, len(unread), [out[i][0] for i in unread][:8]))
    pickle.dump(RES, open(os.environ.get('RES', '/home/claude/build/abl/res.pkl'), 'wb'))
