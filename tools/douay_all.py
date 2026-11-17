"""Douay-Rheims English for every chant whose every verse is found in the Vulgate (douay_all.json).
Preferred over the 1959 St. Dominic Missal English, which has OCR damage and uncertain copyright."""
import json, os, re, sys
sys.argv = [sys.argv[0]]
import douay_match as M
D = json.loads(open('site/data/masses.js', encoding='utf8').read().split('var DOMINICAN = ', 1)[1].rstrip().rstrip(';'))
used = set()
for m in D['masses'].values():
    for p, v in m['parts'].items():
        for c in v: used.add(str(c['id']))
    for se in (m.get('season') or {}).values():
        for v in se.values():
            for c in v: used.add(str(c['id'] if isinstance(c, dict) else c))

import collections
def greedy(seg):
    w = [x for x in M.words(seg) if x != 'alleluia']
    if len(w) < 4: return None
    tri = [' '.join(w[i:i + 3]) for i in range(len(w) - 2)]
    left = set(range(len(tri))); picked = []
    while left:
        votes = collections.Counter(); first = {}
        for i in left:
            for k in M.idx.get(tri[i], ()):
                votes[k] += 1; first.setdefault(k, i)
        if not votes: break
        k, v = votes.most_common(1)[0]
        if v < (2 if picked else max(2, 0.25 * len(tri))): break
        if picked and picked[0][0][0] != k[0]: break      # stay in one book
        picked.append((k, first[k]))
        vt = set(' '.join(M.vw[k][i:i + 3]) for i in range(len(M.vw[k]) - 2))
        left = {i for i in left if tri[i] not in vt}
        if len(picked) > 5: break
    if not picked: return None
    return [k for k, _ in sorted(picked, key=lambda x: x[1])]
out, partial = {}, 0
for cid in sorted(used):
    f = ('site/gabc/r/%s.gabc' % cid[1:]) if cid.startswith('r') else ('site/gabc/%s.gabc' % cid)
    if not os.path.exists(f): continue
    text = M.gabc_text(open(f, encoding='utf8').read())
    segs = [s.strip() for s in text.split('|') if s.strip()]
    segs = [s for s in segs if len(M.words(s)) >= 3 and not re.fullmatch(r'(?i)[\s,.]*(alleluia[\s,.!]*)+', s)]
    if not segs: continue
    en, refs, ok = [], [], True
    for s in segs:
        vs = greedy(s)
        if not vs: ok = False; break
        w = [x for x in M.words(s) if x != 'alleluia']
        cbi = set(' '.join(w[i:i + 2]) for i in range(len(w) - 1)); cw = set(w)
        def inchant(ws):
            if len(ws) < 2: return 1.0 if (ws and ws[0] in cw) else 0.0
            return sum(1 for i in range(len(ws) - 1) if ' '.join(ws[i:i + 2]) in cbi) / (len(ws) - 1)
        selL, selE = [], []
        for k in vs:
            L = [c for c in re.split(r'(?<=[:;.?!])\s+', M.VUL[k]) if c.strip()]
            E_ = [c for c in re.split(r'(?<=[:;.?!])\s+', M.DR.get(k, '')) if c.strip()]
            if len(L) == len(E_):
                for lc, ec in zip(L, E_):
                    if inchant(M.words(lc)) >= 0.5: selL.append(lc); selE.append(ec)
            else:
                lv = M.words(M.VUL[k]); n = len(lv)
                hit = [i for i in range(n) if (i + 1 < n and ' '.join(lv[i:i + 2]) in cbi) or (i > 0 and ' '.join(lv[i - 1:i + 1]) in cbi)]
                if not hit: continue
                a, b = hit[0], hit[-1] + 1
                if a <= 0.12 * n: a = 0
                if b >= 0.88 * n: b = n
                ev = M.DR.get(k, ''); etoks = ev.split(); en_ = len(etoks)
                cuts = [0] + [i + 1 for i, t in enumerate(etoks) if re.search(r'[,:;.?!]$', t)] + [en_]
                ea = 0 if a == 0 else min(cuts, key=lambda c: abs(c - a * en_ / n))
                eb = en_ if b == n else min(cuts, key=lambda c: abs(c - b * en_ / n))
                if eb <= ea: continue
                selL.append(' '.join(lv[a:b])); selE.append(' '.join(etoks[ea:eb]))
        lw = M.words(' '.join(selL))
        ltri = set(' '.join(lw[i:i + 3]) for i in range(len(lw) - 2))
        ctri = [' '.join(w[i:i + 3]) for i in range(len(w) - 2)]
        cov = sum(1 for t in ctri if t in ltri) / max(1, len(ctri))
        prec = inchant(lw)
        if not selE or cov < 0.7 or prec < 0.75: ok = False; break
        seg_en = ' '.join(selE).strip()
        seg_en = re.sub(r'^((Unto the end|A psalm|A canticle|A song|For David|To David|Of David|The prayer of|An instruction|For the octave|For them that|Alleluia\.?)[^.:]*[.:]\s*)+', '', seg_en)
        if not re.match(r'(et|sed|at)\b', M.norm(s.strip())): seg_en = re.sub(r'^(And|But)\s+(?=[a-z])', '', seg_en)
        seg_en = re.sub(r'[;:,]\s*$', '.', seg_en)
        en.append(seg_en[:1].upper() + seg_en[1:])
        refs.append(M.ref_of(vs))
    if not ok: partial += 1; continue
    part = D['chants'].get(cid, {}).get('p')
    body = ' ℣. '.join(en)
    if part == 'al':
        body = 'Alleluia, alleluia. ℣. ' + body + ' Alleluia.'
    out[cid] = {'t': body, 'r': refs[0]}
json.dump(out, open('douay_all.json', 'w'), ensure_ascii=False, indent=0)
print('chants', len(used), '; wholly scriptural, Douay-Rheims given', len(out), '; not wholly found', partial)
for k in list(out)[:3]: print(k, out[k]['r'], '|', out[k]['t'][:140])
