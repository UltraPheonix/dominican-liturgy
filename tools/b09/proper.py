"""Proper Offices of the Sanctorale (Breviarium S.O.P. 1909) read from the text layer, one feast at a time, split at the book's
own labels (Ad I. Vesperas, Invitatorium, In I. Nocturno, Lectio n., Ad Laudes, Ad Benedictus, Ad II. Vesperas ...).
Output propers1909.json: 'MM-DD:n' -> dict in the shape of commons1909.C (v1, mat, laud, v2) + lessons, with a 'q' report of
pieces whose words are not all known (to check against the scans). Only what the book prints for the feast is taken;
everything else stays with the Common (build.py merges).
    python3 proper.py v1 768 1577 ; python3 proper.py v2 476 1369        (page = pdf page - 1)"""
import os, re, sys, json, collections
import offices as O, matins as M, latdict as LD, latcount as LC
from conform import conform
import witness as W
VOL = [None]   # the volume being read (for the second witness)
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'propers1909.json')
CAP = 'A-ZÁÉÍÓÚÝÆŒǼ'
ANT = r'(?:Ana|Aria|Aha|Aña|Arra|Ant|Atia|Ada|Aiia|An a|Ami|Aúa|Aja|Afa|Aiía|Aüa|Añia|Ana?)\s?[.,*:;]?\s'
SEC = [('v1', r'Ad I\. Vesperas|Ad i\. Vesperas|In I\. Vesperis'), ('mat', r'Ad Matutinum'), ('n1', r'In I\. Nocturno'),
       ('n2', r'In I[iI]\. Nocturno'), ('n3', r'In I[iI]{2}\. Nocturno'), ('laud', r'Ad Laudes'),
       ('hor', r'Ad (?:Primam|Tertiam|Horas)'), ('v2', r'(?:Ad|In) I[iI]\. Vesper(?:as|is)'), ('oct', r'Per Octavam|Infra Octavam|Ad Memóriam')]

def known(t):
    """the doubtful words of a piece: not (twice) in the reference corpora, or holding a character no Latin word has"""
    bad = []
    for w in t.split():
        core = w.strip('.,;:!?()«»"\'*—-')
        if not core: continue
        if re.search(r'[^A-Za-zÀ-ÿǽæœÆŒǼ]', core): bad.append(core); continue
        if len(core) > 2 and LC.N.get(LD.base(core), 0) < 2: bad.append(core)
    return bad
def fix(t, cov=0.6):
    """a short piece (antiphon, versicle, part of a responsory): the book's words, spelled after the matching Divinum Officium
    piece where there is one (conform), else word repairs only"""
    t = O.clean(t); t = O.dropcap(t) if re.match(r'^[a-zà-ÿ]|^[A-Z]{3,}|^.{0,3}[\\^/]', t) else t
    if VOL[0]: t = W.merge(t, VOL[0])
    ref = O.fix_short(t, cov)
    u = conform(t, ref)[0] if ref and ref != t else LC.fix_text(t)
    return re.sub(r'\s+', ' ', u).strip(' ,;:')
NOCT = re.compile(r'\b[Ii1l][nN]\s[IiLlH1!\]]{1,4}[.,]?\s?N[oO0]ctur[nm][oO0]', re.I)
def sections(ch):
    """{name: text} cut at the section labels, in the order of the book; the three nocturns by the order of their headings
    (the numeral is often misread)"""
    pos = []; last = 0
    for name, pat in SEC:
        if name in ('n1', 'n2', 'n3'): continue
        m = re.search(pat, ch[last:])
        if m: pos.append((last + m.start(), last + m.end(), name)); last = last + m.end()
    lo = next((e for s0, e, n in pos if n == 'mat'), 0); hi = next((s0 for s0, e, n in pos if n in ('laud', 'hor', 'v2', 'oct') and s0 > lo), len(ch))
    hs = list(NOCT.finditer(ch, lo, hi))[:3]
    def num(m):   # I / Ii / Iii as read ('H' = II)
        x = re.sub(r'(?i)^in\s|\s?noctur.*$|[.,]', '', m.group(0)); return sum(2 if c in 'Hh' else 1 for c in x if c in 'IiLl1!]Hh')
    ns = [num(m) for m in hs]
    if not (all(1 <= n <= 3 for n in ns) and ns == sorted(set(ns))):
        ns = list(range(1, len(hs) + 1)) if len(hs) == 3 else ([2, 3][:len(hs)] if len(hs) == 2 and not re.search(r'L[eé]ctio\s[ij1l]{1,3}\s?[.,]', ch[lo:hs[0].start()] + ch[hs[0].end():hs[1].start()]) else list(range(1, len(hs) + 1)))
    for n, m in zip(ns, hs): pos.append((m.start(), m.end(), 'n%d' % n))
    pos.sort()
    out = {}
    for i, (s0, e, name) in enumerate(pos):
        out[name] = ch[e:pos[i + 1][0] if i + 1 < len(pos) else len(ch)]
    out['head'] = ch[:pos[0][0]] if pos else ch
    return out
STOP = r'(?=\s?(?:Psalm[iu]s?\s?[A-Z]|\sPsalm[iu]s?\b|\sCapitulum|\sHymnus|Ad Magn|Ad Bened|Oratio|Lectio|De Ep[ií]st|De Act|De libro|Sermo|Homil|Incipit|\(Ex |Ex Act|Invitat|' + ANT + r')|$)'
def ants_of(t):
    """antiphons marked Ana. in a stretch of text"""
    out = []
    for m in re.finditer(ANT + r'\s*([' + CAP + r'].+?)' + STOP, ' ' + t):
        a = m.group(1).strip()
        if 12 < len(a) < 400: out.append(a)
    return out
VRS = None
def versicles():
    """known versicle pairs (Commons): the OCR of a ℣/℟ is matched to one of these"""
    global VRS
    if VRS is None:
        import commons1909 as CM
        VRS = set()
        def walk(x, k=None):
            if isinstance(x, dict): [walk(v, kk) for kk, v in x.items()]
            elif isinstance(x, (list, tuple)):
                if k in ('vr', 'op_v', 'al') and len(x) == 2 and all(isinstance(y, str) for y in x): VRS.add(tuple(x))
                elif k in ('t', 's', 'n') and len(x) >= 4: VRS.add((x[2] + ' ' + x[3], '')) if False else None
                else: [walk(v, k) for v in x]
        walk(CM.C)
        VRS = sorted(VRS)
    return VRS
def find_vr(t):
    """(antiphon text before the versicle, (℣, ℟)) — the last antiphon of a nocturn runs into its versicle"""
    import difflib
    nt = O.R.nb(t) if hasattr(O.R, 'nb') else t.lower()
    best = None
    for v, r in versicles():
        k = ' '.join(O.R.nb(w) for w in v.split()[:3])
        words = t.split()
        for i in range(len(words) - 2):
            if ' '.join(O.R.nb(w) for w in words[i:i + 3]) == k:
                tail = ' '.join(words[i:i + len(v.split()) + len(r.split()) + 3])
                sc = difflib.SequenceMatcher(None, O.R.nb(tail), O.R.nb(v + ' ' + r)).ratio()
                if sc > 0.75 and (not best or sc > best[0]): best = (sc, ' '.join(words[:i]), (v, r))
    if best: return re.sub(r'\s\S{0,3}$', '', best[1]).strip(), best[2]
    a, rest = split_at_junk(t)
    if rest:
        v, r = split_at_junk(rest)
        if r: return a, (fix(v, 0.7).rstrip('.') + '.', fix(r, 0.7).rstrip('.') + '.')
    return t, None
def nocturn(t):
    """antiphons and versicle of one nocturn (the text before its first lesson)"""
    pre = re.split(r'\sLectio [ivxj]+\b|\sDe Ep[ií]st|\sDe Act|\sDe libro|\sSermo |\sHomil|\sIncipit |\s\(Ex |\sEx Act|\sLectio sancti', t)[0]
    al = ants_of(pre); vr = None
    if al:
        last, vr = find_vr(al[-1]); al[-1] = last
    al = [fix(a) for a in al]
    return al, vr
JUNKSET = {'It', 'If', 'I', 'y', 'f', 'T', 'V', 'R', 'p', 'ly', 'Is', 'IT', 'Y', 'X', 'JF', 'jT', 'B', 'ty', 'l', 'Ep', 'i', 'r', 'F', 'P', 'v'}
def is_junk(tok):
    """an OCR rendering of the ℣ / ℟ sign: a token of 1-3 characters that is no Latin word"""
    core = tok.strip('.,;:*•<>-—\'"»«)(}{[]')
    if len(tok) > 5 or len(core) > 3: return False
    if core in JUNKSET or not core.isalpha(): return True
    return LC.N.get(LD.base(core), 0) < 20
def split_at_junk(t):
    """(before, after) at the first ℣/℟ sign after a sentence end; (t, None) if none"""
    m = re.search(r'\s*[℣℟]\.\s*', t)
    if m and m.start() > 8: return t[:m.start()], t[m.end():]
    w = t.split()
    for i in range(2, len(w) - 1):
        j = i
        while j < len(w) - 1 and is_junk(w[j]) and j - i < 3: j += 1
        if j > i and re.match('[' + CAP + ']', w[j]) and re.search(r'[.,;:!?»*]$|^\W+$', w[i - 1] + ('' if w[i - 1][-1:].isalpha() else '')) or \
           (j > i and re.match('[' + CAP + ']', w[j]) and not w[i].strip('.,').isalpha()):
            return ' '.join(w[:i]), ' '.join(w[j:])
    return t, None
RV = {1: '[ij1l]', 2: '[il1][ij1l]', 3: '[il1]{2}[ij1l]|in', 4: '[il1]v', 5: 'v', 6: 'v[ij1l]', 7: 'v[il1][ij1l]', 8: 'v[il1]{2}[ij1l]|vin', 9: '[il1]x'}
RNUM = {'i': 1, 'j': 1, 'ii': 2, 'ij': 2, 'iii': 3, 'iij': 3, 'in': 3, 'iv': 4, 'v': 5, 'vi': 6, 'vj': 6, 'vii': 7, 'vij': 7, 'viii': 8, 'viij': 8, 'ix': 9}
LMARK = re.compile(r'(?:^|\s)L[eé]ctio\s[ivxjlYyVI1n]{1,5}\s?[.,/]\s?')
RMARK = re.compile(r'(?<=[.,;:!?»\u2014] )(?:[^\s\w]?[A-Za-z℟$£7]{0,3}[.,*»]{0,2}\s?)?[ivxjl]{1,5}\s?[.,]\s+(?=[' + CAP + '])')
def split_lessons(t, first=1):
    """[(n, lesson text, responsory text or None)] of one nocturn. The numerals are often misread, so the lessons are numbered by
    their order in the nocturn (first, first+1, first+2); a responsory begins at the ℟ sign with its numeral after a lesson"""
    marks = [m for m in LMARK.finditer(t)]
    out = []
    for k, m in enumerate(marks):
        x = t[m.end():marks[k + 1].start() if k + 1 < len(marks) else len(t)]
        if k + 1 < len(marks): x = re.split(r'\s(?:L[eé]ctio sancti Evang|De Ep[ií]stola|De Act|De libro|Sermo sancti|\(Ex Act|Ex Act)', x)[0]
        r = None
        for r_ in RMARK.finditer(x):
            if r_.start() > 100 and re.search(r'\*|℣', x[r_.end():r_.end() + 400]) and not re.search(r'(?i)cap|lib|hom|serm|tract|epist$', x[max(0, r_.start() - 12):r_.start()]): r = r_; break
        if r: out.append((first + k, x[:r.start()], x[r.end():]))
        else: out.append((first + k, x, None))
    return out
def resp_of(n, rt):
    """Matins responsory: Divinum Officium's text and structure where it is the same responsory, else the OCR split at * / ℣ / —"""
    rt = re.split(r'\s(?:In I+[iI]*\. Nocturno|Ad Laudes|Lectio sancti|Dic[aá]tur C[aá]nticum|Te Deum)', rt)[0]
    whole = re.split(r'\sGl[oó] ?ria\b', rt)[0]
    gloria = bool(re.search(r'\sGl[oó] ?ria\b', rt))
    body = whole
    a, rest = (body.split('*', 1) + [''])[:2] if '*' in body else (body, '')
    if rest: b, v = split_at_junk(rest)
    else: a, v = split_at_junk(a); b = ''
    v = re.split(r'\s[—–]\s|\s—|\s-\s', v)[0] if v else None
    d = O.R.repair_resp(whole, 0.7); src = 'OCR'
    if d and d.get('a'):
        ref = ' '.join([d['a'], d.get('b') or ''] + list(d.get('v') or [])); src = 'DO %.2f' % d['cov']
        a = conform(a, ref)[0]; b = conform(b, ref)[0] if b else ''; v = conform(v, ref)[0] if v else None
    else:
        a = fix(a, 0.7); b = fix(b, 0.7) if b else ''; v = fix(v, 0.7) if v else None
    cl = lambda x: re.sub(r'\s*[*—]\s*$', '', x).strip()
    return {'n': n, 'a': cl(a).rstrip('.'), 'b': cl(b), 'v': [cl(v)] if v else [], 'gloria': gloria, 'src': src}
def lauds_ants(t):
    m = re.search(r'ANTIPHON\S*\.?\s*(.+?)(?=\sCapitul|\sHymnus|\sAd Bened)', t, re.I)
    if not m: return []
    body = re.sub(r'\sPsalm[iu]s?\b.*?pag\S*\s?\d+\S*\.?', ' ', m.group(1))
    parts = re.split(r'(?:^|\s)(?:[1lI2-5s]|ii|iii|iv|v)\s?[.\-*•:]\s+(?=[' + CAP + '])', ' ' + body)
    return [fix(p) for p in parts if len(p.strip()) > 12]
def one(pat, t, maxlen=500):
    m = re.search(pat + r'\s*([' + CAP + r'a-z/\\^].+?)' + STOP, t)
    if m and 12 < len(m.group(1)) < maxlen: return m.group(1).strip()
def parse(ch):
    S = sections(ch); P = {}; Q = []
    def put(sec, k, v):
        if v in (None, [], ''): return
        P.setdefault(sec, {})[k] = v
        flat = []
        for x in (v if isinstance(v, list) else [v]): flat += x if isinstance(x, list) else [x]
        for x in flat:
            if isinstance(x, str):
                b = known(x)
                if b: Q.append('%s.%s: %s' % (sec, k, ' '.join(b[:6])))
                elif VOL[0]:
                    dv = W.differences(x, VOL[0])
                    if dv: Q.append('%s.%s: witness %s' % (sec, k, ' ; '.join(dv[:4])))
    if 'v1' in S:
        t = S['v1']; a = ants_of(re.split(r'\sCapitulum|\sAd Magn', t)[0])
        if len(a) == 1: put('v1', 'ant', fix(a[0]))
        elif len(a) >= 4: put('v1', 'ants', [fix(x) for x in a[:5]])
        mg = one(r'Ad Magn\S+\s' + ANT, t)
        if mg: put('v1', 'magn', fix(mg))
    if 'mat' in S:
        iv = one(r'Invitatorium[.,]?', S['mat'], 260)
        if iv and '*' in iv: put('mat', 'invit', fix(iv.replace('*', ' * ')).replace(' : * ', ', * '))
    nants = []; nvr = []
    for k in ('n1', 'n2', 'n3'):
        if k in S:
            al, vr = nocturn(S[k]); nants.append(al); nvr.append(vr)
    if nants and all(len(a) == 3 for a in nants) and len(nants) == 3:
        put('mat', 'nants', nants); P['mat']['nvr'] = nvr
    elif nants and any(nants): Q.append('mat.nants: %s antiphons read %s' % (len(nants), [len(a) for a in nants]))
    # lessons and responsories (matins.py machinery, repaired against the Vulgate / Divinum Officium)
    ls = []
    for k in ('n1', 'n2', 'n3'):
        got = split_lessons(S.get(k, ''), {'n1': 1, 'n2': 4, 'n3': 7}[k])
        if got and len(got) != 3: Q.append('%s: %d lessons read' % (k, len(got)))
        for n, lt, rt in got:
            lt = W.merge(O.clean(lt), VOL[0]) if VOL[0] else O.clean(lt)
            x = M.build_lesson(n, lt)
            if x.get('src') == 'OCR' and x.get('la'): x['la'] = LC.fix_text(x['la'])
            if x.get('src') != 'OCR' and x.get('la'):
                body = M.lesson_parts(O.clean(lt))[1]
                hm = re.search(r'\s((?:Homilía|Sermo|Ex Tractátu|Ex libro)[^.]*\.(?:\s*\([^)]*\))?)\s', ' ' + body + ' ')
                if hm: body = body[hm.end() - 1:]
                la, cf = conform(body, x['la'])
                x['ref_src'] = x['src']; x['la'] = la; x['src'] = 'DO %.2f' % cf     # share of the book's words confirmed by the reference
                if cf < 0.9: x.pop('en', None)                                        # the reference's English no longer fits
            b = known(x.get('la', ''))
            if b: Q.append('lectio %d: %s' % (n, ' '.join(b[:8])))
            elif VOL[0]:
                dv = W.differences(x.get('la', ''), VOL[0])
                if dv: Q.append('lectio %d: witness %s' % (n, ' ; '.join(dv[:4])))
            if rt:
                x['resp'] = resp_of(n, rt); rr = ' '.join([x['resp']['a'], x['resp']['b']] + x['resp']['v'])
                b = known(rr)
                if b: Q.append('resp %d: %s' % (n, ' '.join(b[:8])))
                elif VOL[0]:
                    dv = W.differences(rr, VOL[0])
                    if dv: Q.append('resp %d: witness %s' % (n, ' ; '.join(dv[:4])))
                if x['resp']['src'] == 'OCR':
                    pass
            else: P.setdefault('info', []).append('no responsory read after lesson %d (from the Common, or missed)' % n)
            ls.append(x)
    if ls: P['lessons'] = ls
    if 'laud' in S:
        t = S['laud']; la = lauds_ants(t)
        if len(la) == 5: put('laud', 'ant', la)
        elif la: Q.append('laud.ant: %d read' % len(la))
        b = one(r'Ad Bened\S+\s' + ANT, t)
        if b: put('laud', 'bened', fix(b))
    if 'v2' in S:
        t = S['v2']; mg = one(r'Ad Magn\S+\s' + ANT, t)
        if mg: put('v2', 'magn', fix(mg))
        a = ants_of(re.split(r'\sCapitulum|\sAd Magn', t)[0])
        if len(a) == 1: put('v2', 'ant', fix(a[0]))
    if Q: P['q'] = Q
    return P
def chunks(vol, a, b):
    t = O.text_sancti(vol, a, b)
    plain = t.translate(str.maketrans('áéíóúýÁÉÍÓÚǽ', 'aeiouyAEIOUæ'))
    plain = re.sub(r'(bris|arii|rtii|rilis|[Mm]aii|[Mm]aji|unii|ulii|usti),(\s)', r'\1.\2', plain)   # 'Novembris,' (OCR)
    hs = []
    for m in O.SHEAD.finditer(plain):
        d = O.roman(m.group(1)); mo = O.MONTHS.get(m.group(2).lower())
        if d and mo and 1 <= d <= 31: hs.append((m.start(), '%02d-%02d' % (mo, d), O.clean(t[m.start(3):m.end(3)])))
    for i, (s, md, title) in enumerate(hs):
        e = hs[i + 1][0] if i + 1 < len(hs) else len(t)
        yield md, title, t[s:e]
# ---------- chunking by the calendar (the date headings are too often garbled by the OCR) ----------
RANKW = r'(?i:Totum\s?Dupl\w*|Dupl\w+|Semidupl\w*|Simpl\w+|Tres\.?|Trium Lect\w*|iij\. Lect\w*|Memoria|Solem\s?n\w+)'
def nrm(s):
    import unicodedata
    s = unicodedata.normalize('NFD', s.lower().replace('æ', 'ae').replace('œ', 'oe').replace('ǽ', 'ae'))
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn').replace('j', 'i')
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z ]', ' ', s)).strip()
def calendar():
    out = []
    for l in open(os.path.join(HERE, 'calendar1909.txt'), encoding='utf-8'):
        if l.startswith('#') or '|' not in l: continue
        md, ti, rk = (l.rstrip('\n').split('|') + ['', ''])[:3]
        out.append((md, ti, rk))
    return out
STOPW = set('conf ep mart virg vid et op eccl doct de a ab ss bb s b v mm abbatis papae apostoli sociorum in ord praed'.split())
def bigr(w): return {w[k:k + 2] for k in range(len(w) - 1)} or {w}
def chunks_cal(vol, a, b, start, stop=None):
    """(md, calendar title, rank, text) for the feasts found: a monotone alignment (dynamic programming) of the calendar entries,
    in the order of the book from entry `start` to `stop` (MM-DD), with the headings of the text (the words before each rank word)"""
    t = O.text_sancti(vol, a, b)
    cands = []
    for m in re.finditer(r'[.,]\s*' + RANKW + r'[.,*]', t):
        s0 = max(0, m.start() - 110); ws = nrm(t[s0:m.start()]).split()[-14:]
        cands.append((s0, m.end(), [bigr(w) for w in ws if len(w) > 2], nrm(m.group(0)).replace(' ', '')))
    cal = calendar(); i0 = next(i for i, c in enumerate(cal) if c[0] >= start)
    order = cal[i0:] + cal[:i0]
    if stop:
        i1 = max(i for i, c in enumerate(order) if c[0] == stop); order = order[:i1 + 1]
    ents = []
    for md, ti, rk in order:
        if not rk or rk == 'Memoria' or re.match(r'Vig[ií]lia', ti): continue
        key = [bigr(w) for w in nrm(ti).split() if len(w) > 3 and w not in STOPW]
        if key: ents.append((md, ti, rk, key, nrm(rk).split()[0][:4]))
    n, m_ = len(ents), len(cands)
    def score(e, c):
        tot = 0.0
        for kb in e[3]:
            tot += max((2.0 * len(kb & wb) / (len(kb) + len(wb)) for wb in c[2]), default=0.0)
        sc = tot / len(e[3])
        if e[4] in c[3]: sc += 0.06
        return sc
    best = [[0.0] * (m_ + 1) for _ in range(n + 1)]; back = [[0] * (m_ + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        e = ents[i - 1]; bi, bp = best[i], best[i - 1]; bk = back[i]
        for j in range(1, m_ + 1):
            v, w = bp[j], 0                       # entry i not in this volume / not found
            if bi[j - 1] > v: v, w = bi[j - 1], 1  # candidate j is no heading
            sc = score(e, cands[j - 1])
            if sc >= 0.74 and bp[j - 1] + sc > v: v, w = bp[j - 1] + sc, 2
            bi[j] = v; bk[j] = w
    found = []; i, j = n, m_
    while i > 0 and j > 0:
        w = back[i][j]
        if w == 2: found.append((ents[i - 1][0], ents[i - 1][1], ents[i - 1][2], cands[j - 1][0], cands[j - 1][1])); i -= 1; j -= 1
        elif w == 1: j -= 1
        else: i -= 1
    found.reverse()
    for k, (md, ti, rk, s0, e0) in enumerate(found):
        end = found[k + 1][3] if k + 1 < len(found) else len(t)
        yield md, ti, rk, t[s0:end]
VOLS = {'v1': (768, 1577, '11-29', '06-15'), 'v2': (476, 1369, '04-13', '12-02')}
if __name__ == '__main__':
    vol = sys.argv[1]; a, b, st, en = VOLS[vol]; VOL[0] = vol
    only = sys.argv[2] if len(sys.argv) > 2 else None
    D = json.load(open(OUT)) if os.path.exists(OUT) and not only else {}
    for md, ti, rk, ch in chunks_cal(vol, a, b, st, en):
        if only and md != only: continue
        if len(ch) > 60000: print(md, ti[:40], 'SKIPPED: chunk of %d characters holds several Offices (anchor missing)' % len(ch)); continue
        P = parse(ch); P['title'] = ti; P['rank'] = rk; P['vol'] = vol; P['len'] = len(ch)
        k = md + '|' + ti
        if k in D and D[k].get('vol') != vol and len(D[k].get('q', [])) <= len(P.get('q', [])) and D[k].get('lessons'): continue   # keep the cleaner reading of the two volumes
        D[k] = P
        print(md, '|', ti[:44], '|', {x: (list(v) if isinstance(v, dict) else len(v) if hasattr(v, '__len__') else v) for x, v in P.items() if x not in ('title', 'rank', 'vol', 'len')}, flush=True)
    if not only: json.dump(D, open(OUT, 'w'), ensure_ascii=False, indent=0)
