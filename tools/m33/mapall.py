import json, re, difflib
from parse import norm, HR, L
import readings as R
from anchor import SITE
P2 = json.load(open('/home/claude/m33/printed2pdf.json'))
E = json.load(open('/home/claude/m33/sanct.json'))
ANCH = json.load(open('/home/claude/m33/anchors.json'))
INTR = json.load(open('/home/claude/m33/introits.json'))
def pdf_of(printed):
    star = printed.endswith('*'); n = int(printed.rstrip('*'))
    best = None
    for k, v in P2.items():
        if k.endswith('*') != star: continue
        kn = int(k.rstrip('*'))
        if best is None or abs(kn - n) < abs(best[0] - n): best = (kn, v)
    return best[1] + (n - best[0]) if best else None
LINE_OF_PAGE = {}
for i, (pg, k, l) in enumerate(L): LINE_OF_PAGE.setdefault(pg, i)
def kind(l): return next((k for k, r in HR if r.match(l)), None)
def inc_words(inc): return [w for w in norm(inc).split()][:4]
def starts_with_inc(i, inc):
    t = norm(' '.join(x[2] for x in L[i:i + 4]))
    ws = inc_words(inc)
    if len(ws) < 2: return ws[0][1:] in t[:60] if ws else False
    return (' '.join(ws[1:3]) in t[:90]) or (ws[0][2:] in t[:40] and ws[1] in t[:80])
def introit_near(pdfpage, inc, span=1):
    if pdfpage is None: return None
    for p in range(pdfpage - span, pdfpage + span + 1):
        i0 = LINE_OF_PAGE.get(p)
        if i0 is None: continue
        i = i0
        while i < len(L) and L[i][0] == p:
            if kind(L[i][2]) == 'introit' and starts_with_inc(i, inc): return i
            i += 1
    return None
def readings_from(start, end=None):
    out = []; cur = None; i = start + 1
    end = end or len(L)
    while i < end:
        pg, kd, l = L[i]; k = kind(l)
        if k == 'introit' and end == len(L): break
        if k in ('lesson', 'gospel'): cur = {'kind': k, 'head': l, 'body': [], 'page': pg, 'line': i}; out.append(cur)
        elif k in R.STOP:
            if k in ('offertory', 'credo') and cur and cur['kind'] == 'gospel' and end == len(L): break
            cur = None
        elif cur is not None: cur['body'].append(l)
        i += 1
    for r in out:
        b = r['body']; cut = 0
        for j in range(min(4, len(b))):
            if re.search(r'(^|\s)(c|cap)\.\s*\d+(\s*et\s*\d+)?\s*\S{0,3}$', b[j]) or re.match(r'^[A-Z][a-z]{1,6}\.\s*\d+(\s*et\s*\d+)?\s*\S{0,2}$', b[j]): cut = j + 1
        if not cut and (r['head'].endswith('\xad') or r['head'].endswith('-')): cut = 1
        r['head'] = R.join([r['head']] + b[:cut]); r['body'] = b[cut:]
    return out
def gospel_at(printed, inc):
    p = pdf_of(printed)
    for q in (p, p - 1, p + 1, p + 2):
        i = LINE_OF_PAGE.get(q)
        if i is None: continue
        while i < len(L) and L[i][0] == q:
            if kind(L[i][2]) == 'gospel':
                rs = readings_from(i - 1, i + 60)
                if rs and norm(inc).split()[0][1:] in norm(' '.join(rs[0]['body'][:3]))[:80]: return rs[0]
            i += 1
    return None
import anchor as A_, bisect
def collect_hits(text):
    ws = norm(text).split(); out = []
    if len(ws) < 10: return out
    for st in (2, 5, 9, 13):
        q = ' '.join(ws[st:st + 7])
        if len(q.split()) < 7: continue
        for mm in re.finditer(re.escape(q), A_.S):
            li = A_.WL[bisect.bisect_right(A_.pos2word, mm.start()) - 1]
            if all(abs(li - o) > 15 for o in out): out.append(li)
    return sorted(out)
def nameScore(a, b):
    A = set(w for w in norm(a).split() if len(w) > 3); B = set(w for w in norm(b).split() if len(w) > 3)
    return len(A & B)
COMMONS = ['In medio', 'Os justi', 'Statuit', 'Sacerdotes tui', 'Laetabitur', 'In virtute', 'Gaudeamus', 'Dilexisti', 'Me exspectaverunt', 'Loquebar', 'Cognovi', 'Vultum tuum', 'Intret', 'Salus autem', 'Sapientiam', 'Sancti tui', 'Clamaverunt', 'Justus ut palma', 'Mihi autem', 'Protexisti', 'Multae tribulationes', 'Exsultabunt', 'Terribilis', 'Sitivit', 'Salve sancta Parens', 'Timete Dominum', 'Benedicta sit', 'Lux perpetua', 'Requiem aeternam', 'Si diligis me', 'Sacerdotes Dei', 'Justi epulentur', 'Judicant Sancti', 'Laetabitur justus', 'Justus ut palma', 'Venite benedicti', 'Gaudete in Domino']
def common_inc(s):
    m = difflib.get_close_matches(s.strip(), COMMONS, 1, 0.6)
    return m[0] if m else s
def introit_any(inc, near=None):
    best = None
    for i, (pg, kd, l) in enumerate(L):
        if pg < 40 or kind(l) != 'introit': continue
        if starts_with_inc(i, inc) or norm(l).find(norm(inc)) >= 0:
            d = abs(pg - near) if near else 0
            if best is None or d < best[0]: best = (d, i)
    return best[1] if best else None
REF = re.compile(r'Officium\s+([A-Z][^,]{2,30}?),?\s+(?:ut\s+)?(?:in|de)\s+Comm[^\n]*?pag\.\s*(\d+\*?)')
DP = json.load(open('/home/claude/m33/dpmap.json'))
PAGEMAP = {'Epi1': 80, 'Quad1t': 106, 'Quad4s': 148, 'Quad5f': 382, 'Pasc0w': 294, 'Pent4': 344, 'Pasc6s': 316}
def first_introit(p):
    i0 = LINE_OF_PAGE.get(p)
    while i0 is not None and i0 < len(L) and L[i0][0] <= p + 1:
        if kind(L[i0][2]) == 'introit': return i0
        i0 += 1
    return None
def map_key(k, m):
    if DP.get(k) is not None:
        st = DP[k]; return {'key': k, 'how': 'dp', 'readings': readings_from(st), 'start': st}
    if k in PAGEMAP:
        st = first_introit(PAGEMAP[k])
        if st is not None: return {'key': k, 'how': 'page %d' % PAGEMAP[k], 'readings': readings_from(st), 'start': st}
    m['introit'] = INTR.get(k, '')
    res = {'key': k, 'how': None, 'readings': []}
    if re.match(r'S\d{4}', k):
        date = k[1:5]; cands = [e for e in E if e['date'] == date]
        if not cands: res['how'] = 'no-date'; return res
        e = max(cands, key=lambda e: nameScore(e['name'], m['title']) * 10 - cands.index(e))
        j = E.index(e); end = E[j + 1]['line'] if j + 1 < len(E) else len(L)
        region = ' '.join(x[2] for x in L[e['line']:min(end, e['line'] + 60)])
        rs = readings_from(e['line'], end)
        res['entry'] = e['name'][:60]; res['how'] = 'sanct'
        mm = REF.search(region.replace('\xad', '').replace('- ', ''))
        if mm:
            inc2 = common_inc(mm.group(1)); pp = pdf_of(mm.group(2))
            st = introit_near(pp, inc2, 2)
            if st is None: st = introit_any(inc2, pp)
            res['common'] = (mm.group(1), mm.group(2), st)
            if st is not None:
                com = readings_from(st)
                have = {r['kind'] for r in rs}
                rs = [r for r in com if r['kind'] not in have] + rs if have != {'lesson', 'gospel'} else rs
                rs.sort(key=lambda r: 0 if r['kind'] == 'lesson' else 1)
            g = re.search(r'cum\s+Evang\w*\.?\s+([A-Z]\w+)[^p]{0,30}pag\.\s*(\d+\*?)', region.replace('\xad', '').replace('- ', ''))
            if g:
                gg = gospel_at(g.group(2), g.group(1))
                if gg: rs = [r for r in rs if r['kind'] != 'gospel'] + [gg]
        if not rs and not mm:
            g = re.search(r'(Officium|Missa)\s+([A-Z][a-z]+(?:\s[a-z]+)?)?.{0,120}?pag[.-]\s*(\d+\*?)', region.replace('\xad', '').replace('- ', ''))
            if g:
                pp = pdf_of(g.group(3)); st = None
                if g.group(2) and g.group(2) not in ('ut', 'Ut', 'dicitur'): st = introit_near(pp, common_inc(g.group(2)), 2) or introit_any(common_inc(g.group(2)), pp)
                if st is None and pp:
                    i0 = LINE_OF_PAGE.get(pp)
                    while i0 is not None and i0 < len(L) and L[i0][0] <= pp + 1:
                        if kind(L[i0][2]) == 'introit': st = i0; break
                        i0 += 1
                if st is not None: rs = readings_from(st); res['how'] = 'sanct-ref'; res['ref_to'] = g.group(0)[:80]
        res['readings'] = rs
        return res
    inc = m.get('introit') or ''
    hits = collect_hits(m.get('or') or '') or collect_hits(m.get('se') or '') or collect_hits(m.get('pc') or '')
    for h in hits:
        if L[h][0] < 44: continue
        for i in range(h, max(h - 80, 0), -1):
            if kind(L[i][2]) == 'introit':
                if not inc or starts_with_inc(i, inc):
                    res['how'] = 'collect+introit'; res['readings'] = readings_from(i); res['start'] = i; return res
                break
    if inc:
        for p in range(44, 380):
            st = introit_near(p, inc, 0)
            if st is not None: res['how'] = 'introit p%d' % p; res['readings'] = readings_from(st); res['start'] = st; return res
    # commons / votives: by the introit incipit, anywhere in the commune and supplement pages
    for p in range(640, 790):
        st = introit_near(p, inc, 0) if inc else None
        if st is not None: res['how'] = 'introit p%d' % p; res['readings'] = readings_from(st); return res
    res['how'] = 'missing'; return res
if __name__ == '__main__':
    import sys
    OUT = {}
    for k, m in SITE.items():
        m['introit'] = INTR.get(k, '')
        OUT[k] = map_key(k, m)
    json.dump(OUT, open('/home/claude/m33/map.json', 'w'), ensure_ascii=False, default=str)
    import collections
    print(collections.Counter(v['how'].split(' ')[0] if v['how'] else None for v in OUT.values()))
    print([k for k, v in OUT.items() if not v['readings']])
