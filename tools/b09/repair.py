"""Repair OCR'd Latin by aligning it to a reference text (Vulgate in bible/la, or Divinum Officium lessons/responsories).
repair_scripture(ocr) -> (latin, english, ref) | None ;  repair_do(ocr, kind) -> (latin, english_or_None) | None ; fix_ocr(text)"""
import os, re, glob, collections, difflib, unicodedata, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from latdict import fix_line
DO = '/home/claude/divinumofficium/divinum-officium/web/www/horas'
def nb(s):
    s = unicodedata.normalize('NFD', s.lower()); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z]', '', s.replace('æ', 'ae').replace('œ', 'oe').replace('j', 'i').replace('v', 'u'))
def words(t): return [w for w in re.findall(r"\S+", t)]
from latdict import D as LATD, base as latbase
def is_word(w):
    x = latbase(re.sub(r'[^\w]', '', w))
    if len(x) == 1: return w in ('a', 'e', 'o')
    return x in LATD
def fix_word_keep(w): return fix_line(w)
def fix_ocr(t):
    t = re.sub(r'\s+', ' ', t).strip()
    t = re.sub(r'\bArnen\b', 'Amen', t)
    return fix_line(t)

class Corpus:
    """a list of documents, each a list of (word, unit-id); index of word 3-grams"""
    def __init__(self):
        self.docs = []; self.idx = collections.defaultdict(list)
    def add(self, toks, meta):
        di = len(self.docs); self.docs.append((toks, meta)); n = [nb(w) for w, _ in toks]
        for i in range(len(n) - 2):
            self.idx[(n[i], n[i + 1], n[i + 2])].append((di, i))
    def locate(self, ocr_n):
        votes = collections.Counter()
        for i in range(len(ocr_n) - 2):
            for di, j in self.idx.get((ocr_n[i], ocr_n[i + 1], ocr_n[i + 2]), [])[:50]:
                votes[(di, (j - i) // 40)] += 1
        return votes.most_common(3)
    def align(self, ocr, min_cov=0.6):
        """word-level merge of the OCR with the best reference passage; the OCR (the 1909 book) decides:
        matched words take the reference spelling; a replaced stretch takes the reference only if it looks like an OCR misreading
        of it; extra OCR words that are real words are kept (a textual variant); reference words missing from the OCR are added
        only in gaps of <= 3 words (dropped by the OCR)."""
        raw = words(ocr); ow = [w for w in raw if nb(w)]; on2 = [nb(w) for w in ow]
        if len(on2) < 4: return None
        best = None
        for (di, blk), v in self.locate(on2):
            toks, meta = self.docs[di]; rn = [nb(w) for w, _ in toks]
            a = max(0, blk * 40 - 60); b = min(len(rn), blk * 40 + len(on2) + 120)
            sm = difflib.SequenceMatcher(None, on2, rn[a:b], autojunk=False)
            ms = [m for m in sm.get_matching_blocks() if m.size]
            if not ms: continue
            cov = sum(m.size for m in ms) / len(on2)
            if not best or cov > best[0]: best = (cov, di, a, b, sm)
        if not best or best[0] < min_cov: return None
        cov, di, a, b, sm = best; toks, meta = self.docs[di]
        ops = sm.get_opcodes()
        eq = [k for k, o in enumerate(ops) if o[0] == 'equal']
        fe, le = eq[0], eq[-1]
        def best_ref(o, cands):
            """o: joined OCR string; cands: list of (m, joined ref string) -> m or 0"""
            bm, br = 0, 0.0
            for m, r in cands:
                x = difflib.SequenceMatcher(None, o, r).ratio()
                if x > br + 0.02: bm, br = m, x
            return bm if br >= 0.5 else 0
        out = []
        i0, j0 = ops[fe][1], ops[fe][3]          # leading OCR words (drop capitals, first line): match against the reference before
        if i0:
            o = ''.join(on2[:i0]); m = best_ref(o, [(m, ''.join(nb(toks[a + j][0]) for j in range(j0 - m, j0))) for m in range(1, min(j0, i0 + 3) + 1)])
            out += [toks[a + j] for j in range(j0 - m, j0)] if m else [(fix_word_keep(w), None) for w in ow[:i0] if is_word(w)]
        for k in range(fe, le + 1):
            tag, i1, i2, j1, j2 = ops[k]
            if tag == 'equal':
                out += [toks[a + j] for j in range(j1, j2)]
            elif tag == 'replace':
                o = ''.join(on2[i1:i2]); r = ''.join(nb(toks[a + j][0]) for j in range(j1, j2))
                if (j2 - j1) <= (i2 - i1) + 3 and difflib.SequenceMatcher(None, o, r).ratio() >= 0.6:
                    out += [toks[a + j] for j in range(j1, j2)]
                else:
                    out += [(fix_word_keep(w), None) for w in ow[i1:i2] if is_word(w)]
            elif tag == 'insert':   # reference words not in the OCR: only short gaps (dropped by the OCR)
                if j2 - j1 <= 3: out += [toks[a + j] for j in range(j1, j2)]
            elif tag == 'delete':   # OCR words not in the reference: a variant if they are real words of 3+ letters
                out += [(fix_word_keep(w), None) for w in ow[i1:i2] if is_word(w) and len(nb(w)) >= 3]
        i9, j9 = ops[le][2], ops[le][4]          # trailing OCR words
        if i9 < len(on2):
            o = ''.join(on2[i9:]); n_ = len(on2) - i9
            m = best_ref(o, [(m, ''.join(nb(toks[a + j][0]) for j in range(j9, j9 + m))) for m in range(1, min(len(toks) - a - j9, n_ + 3) + 1)])
            out += [toks[a + j] for j in range(j9, j9 + m)] if m else [(fix_word_keep(w), None) for w in ow[i9:] if is_word(w) and len(nb(w)) >= 3]
        while out and out[0][1] is None: out.pop(0)          # OCR-only words at the edges: drop capitals, running heads
        while out and out[-1][1] is None: out.pop()
        if len(out) > 1 and re.search(r'[.:;]$', out[0][0]): out.pop(0)
        txt = [w for w, _ in out]; j = len(txt)               # a closing formula caught by the alignment
        for k in range(max(0, j - 8), j):
            if nb(txt[k]) in ('haec', 'hac') and k + 1 < j and nb(txt[k + 1]) == 'dicit': out = out[:k]; break
        if not out: return None
        self.last = (di, out)
        return out, meta, cov
# ---- Vulgate ----
BIB = Corpus(); BIBEN = {}
for f in sorted(glob.glob(os.path.join(REPO, 'bible/la/*.txt'))):
    book = os.path.basename(f)[:-4]; toks = []
    for l in open(f, encoding='utf-8'):
        p = l.rstrip('\n').split('\t')
        if len(p) < 3: continue
        for w in words(p[2]): toks.append((w, (int(p[0]), int(p[1]))))
    BIB.add(toks, book)
    ef = os.path.join(REPO, 'bible/en', os.path.basename(f))
    if os.path.exists(ef):
        for l in open(ef, encoding='utf-8'):
            p = l.rstrip('\n').split('\t')
            if len(p) >= 3: BIBEN[(book, int(p[0]), int(p[1]))] = p[2]
ABBR = {'Isaias': 'Isa', 'Jeremias': 'Jer', 'Ad Romanos': 'Rom', 'Lucas': 'Luc', 'Matthæus': 'Matt', 'Marcus': 'Marc', 'Joannes': 'Joann'}
def repair_scripture(ocr, min_cov=0.7):
    r = BIB.align(ocr, min_cov)
    if not r: return None
    toks, book, cov = r
    la = ' '.join(w for w, _ in toks); la = la[0].upper() + la[1:]
    vs = []
    for _, v in toks:
        if v and v not in vs: vs.append(v)
    en = ' '.join(BIBEN.get((book, c, v), '') for c, v in vs).strip()
    runs = []
    for c, v in vs:
        if runs and runs[-1][0] == c and runs[-1][2] + 1 == v: runs[-1][2] = v
        else: runs.append([c, v, v])
    parts, lastc = [], None
    for c, a, b in runs:
        x = ('%d-%d' % (a, b)) if b > a else '%d' % a
        parts.append(('%d:' % c if c != lastc else '') + x); lastc = c
    ref = '%s %s' % (ABBR.get(book, book), ', '.join(parts))
    return la, en, ref, cov

# ---- Divinum Officium lessons and responsories (Latin, with English of whole sections) ----
LESS = Corpus(); RESP = Corpus()
def _sections(path):
    out, cur = collections.OrderedDict(), None
    for l in open(path, encoding='utf-8'):
        l = l.rstrip('\n'); m = re.match(r'^\[(.+?)\]\s*$', l)
        if m: cur = m.group(1); out[cur] = []; continue
        if cur is not None: out[cur].append(l)
    return out
for f in glob.glob(DO + '/Latin/Tempora/*.txt') + glob.glob(DO + '/Latin/Sancti/*.txt') + glob.glob(DO + '/Latin/Commune/*.txt'):
    try: S = _sections(f)
    except Exception: continue
    toks = []
    for k in [k for k in S if re.match(r'^Lectio\d+$', k)]:
        for l in S[k]:
            if l.startswith(('!', '@', '&', '$', '_')) or not l.strip(): continue
            for w in words(l): toks.append((w, (f, k)))
    if toks: LESS.add(toks, f)
    for k in [k for k in S if re.match(r'^Responsory\d+$', k)]:
        t = []; seenv = False; li = 0
        for l in S[k]:
            if l.startswith(('!', '@', '&', '$', '_')) or not l.strip(): continue
            role = 'V' if l.startswith('V.') else 'R'
            if role == 'V': seenv = True; li += 1
            elif seenv: continue
            l = re.sub(r'^[RV]\.\s*', '', l)
            if role == 'R' and l.startswith('*'): role = 'Rb'
            for w in words(l):
                if w == '*': role = 'Rb'; continue
                t.append((w, (f, k, li, role)))
        if t: RESP.add(t, (f, k))
def repair_do(ocr, kind='lesson', min_cov=0.75):
    C = LESS if kind == 'lesson' else RESP
    r = C.align(ocr, min_cov)
    if not r: return None
    toks, meta, cov = r
    la = ' '.join(w for w, _ in toks if not re.match(r'^\d+$', w))
    units = collections.Counter(u for _, u in toks if u)
    return la, meta, cov, units

def repair_resp(ocr, min_cov=0.8):
    """-> dict(a, b, v=[...], meta, cov) built from the DO responsory structure, or None"""
    r = RESP.align(ocr, min_cov)
    if not r: return None
    toks, meta, cov = r
    role, li, seq = 'R', 0, []
    for w, u in toks:
        if u: role, li = u[3], u[2]
        seq.append((w, role, li))
    a = [w for w, r_, _ in seq if r_ == 'R']; b = [w for w, r_, _ in seq if r_ == 'Rb']
    vs = {}
    for w, r_, l_ in seq:
        if r_ == 'V': vs.setdefault(l_, []).append(w)
    return {'a': ' '.join(a), 'b': ' '.join(b), 'v': [' '.join(vs[i]) for i in sorted(vs)], 'meta': meta, 'cov': cov}

def do_english(units, total):
    """English of a DO lesson span if it is (nearly) one whole DO section"""
    if not units: return None
    (u, n), = units.most_common(1)
    f, k = u
    try:
        L = [l for l in _sections(f)[k] if l.strip() and not l.startswith(('!', '@', '&', '$', '_'))]
        E = [l for l in _sections(f.replace('/Latin/', '/English/'))[k] if l.strip() and not l.startswith(('!', '@', '&', '$', '_'))]
    except Exception: return None
    secn = sum(len(words(l)) for l in L)
    if n < 0.9 * total or n < 0.9 * secn: return None
    return ' '.join(E) if E else None
