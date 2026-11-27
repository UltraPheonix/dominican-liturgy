"""The English of the Mass prayers (Collect, Secret, Postcommunion, Oratio super populum) verbatim from the St Dominic Missal
(1959) wherever it prints the same Latin; otherwise the Divinum Officium English (labelled) or the site's own AI English
(labelled). Only the English and its source label are touched; the Latin is never changed.

Run AFTER every script that writes these files (tools/requiem/build.py, tools/orat39/conclusions.py, tools/g28/apply.py,
tools/addiv/build.py, tools/orat39/memoriae_build.py):
    python3 tools/orat39/dm1959/dmrec.py          # once, needs the crop OCR in tools/orat39/dm1959/work (see english_1959.md)
    python3 tools/orat39/dm_verbatim.py           # report only
    python3 tools/orat39/dm_verbatim.py --write   # write data/orations.js, data/addiv.js, data/memoriae.js
Idempotent: the DM match is made on the Latin, so a second run gives the same result. The table of matches is kept in
tools/orat39/dm1959/dm_en.json (so the data can be rebuilt without the OCR cache).

Matching is strict: the Latin of the site's prayer and the Latin the 1959 Missal prints beside the English must agree word
for word (OCR confusions such as rn/m and li/u aside, and the conclusion aside). If the 1959 Latin differs at all (a revised
text, another name, N. for the name, singular/plural), the 1959 English is not used.
"""
import json, os, re, sys, pickle, collections, difflib, unicodedata
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(H)); DM = H + '/dm1959'
sys.path.insert(0, DM)
TABLE = DM + '/dm_en.json'

def load(path, var):
    s = open(R + path, encoding='utf8').read(); i = s.index(var) + len(var); j = s.rindex('}') + 1
    return s[:i], json.loads(s[i:j]), s[j:]

CONCL_LA = re.compile(r'\s*(Per (?:Dóminum|eúndem|eúmdem|Christum)|Qui (?:vivis|tecum|vivit)|qui tecum vivit|Dóminum nostrum I[eé]sum Christum Fílium tuum: Qui)\b(?!.*\b(?:Per Dóminum|Per eúndem|Qui vivis)\b).*$', re.S)
# as js/app.js CONCL_EN (splitConcl)
CONCL_EN = re.compile(r'[;:,.]?\s*(?:through|who (?:live|lives|livest|liveth)|Who (?:live|lives|livest|liveth)|Through|our Lord Jesus Christ, Your Son, who|our Lord Jesus Christ, thy Son)\b(?!.*\b(?:[Tt]hrough|[Ww]ho liv)).*$', re.S)

def F(s):
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
    s = s.replace('æ', 'ae').replace('œ', 'oe').replace('Æ', 'ae').replace('Œ', 'oe').lower()
    s = re.sub(r'[^a-z]', '', s).replace('j', 'i').replace('v', 'u').replace('y', 'i')
    return s.replace('ae', 'e').replace('oe', 'e')
DMCL = re.compile(r'(Per\s+(Dominum|D[o0]min|eumdem|eundem|Christum|eund|eumd)|Qui\s+(vivis|tecum|vivit|cum\s+Deo|cum\s+Patre|vivi))')
def dm_body(t):
    ms = list(DMCL.finditer(t))
    return t[:ms[-1].start()] if ms else t

def site_prayers():
    """[(file, id, field, latin_body, english, current_src_kind)]"""
    out = []
    _, O, _ = load('/data/orations.js', 'window.ORATIONS = ')
    for k, v in O.items():
        isdo = not v.get('src', '').startswith('Missale')
        for f in ('or', 'se', 'pc', 'sp'):
            if f in v and v[f] and v[f][0]:
                m = CONCL_LA.search(v[f][0]); out.append(('orations', k, f, v[f][0][:m.start()] if m else v[f][0], v[f][1], 'do' if isdo else 'ai'))
    _, M, _ = load('/data/memoriae.js', 'window.MEMORIAE = ')
    for k, v in M.items():
        for f in ('or', 'se', 'pc'):
            if f in v and v[f] and v[f][0]:
                m = CONCL_LA.search(v[f][0]); out.append(('memoriae', k, f, v[f][0][:m.start()] if m else v[f][0], v[f][1], None))
    _, A, _ = load('/data/addiv.js', 'window.ADDIV = ')
    for k, v in A['sets'].items():
        for f in ('or', 'se', 'pc'):
            if f in v and v[f]:
                out.append(('addiv', k, f, v[f]['la'], v[f]['en'], v[f].get('s')))
    return out

def build_table():
    """match every site prayer against the DM records (work/dmrec.pkl) -> dict id -> result"""
    import cmp as C
    recs = [r for r in pickle.load(open(DM + '/work/dmrec.pkl', 'rb')) if r]
    for r in recs:
        r['ft'] = F(dm_body(r['la'])); r['fl'] = F(dm_body(r['la_l']))
    idx = collections.defaultdict(set)
    for n, r in enumerate(recs):
        for f in (r['ft'], r['fl']):
            for k in range(0, max(1, len(f) - 8), 3): idx[f[k:k + 8]].add(n)
    def cands(f):
        c = collections.Counter()
        for k in range(0, max(1, len(f) - 8), 2):
            for n in idx.get(f[k:k + 8], ()): c[n] += 1
        return [n for n, _ in c.most_common(10)]
    res = {}
    SP = site_prayers()
    for file, k, f, la, en, cur in SP:
        fs = F(la); best = []
        for n in cands(fs):
            r = recs[n]
            ratio = max(difflib.SequenceMatcher(None, fs, r['ft'], autojunk=False).ratio(), difflib.SequenceMatcher(None, fs, r['fl'], autojunk=False).ratio())
            if ratio < 0.6: continue
            rt, _ = C.compare(la, dm_body(r['la'])); rl, _ = C.compare(la, dm_body(r['la_l']))
            real = rt if len(rt) <= len(rl) else rl
            best.append((len(real) == 0, ratio, n, real))
        best.sort(key=lambda b: (b[0], b[1]), reverse=True)
        res[(file, k, f)] = {'la': la, 'cands': [(ok, ratio, recs[n], real) for ok, ratio, n, real in best[:5]], 'cur': cur, 'en_old': en}
    return res, recs

# ---------------------------------------------------------------- Divinum Officium English (to label it honestly)
DO_DIR = os.environ.get('DO_DIR', '/home/claude/divinumofficium/divinum-officium/web/www/missa/English')
def E(s):
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
    return re.sub(r'[^a-z]', '', s.lower())
def do_index():
    idx = set(); paras = []
    for root, _, fs in os.walk(DO_DIR):
        for fn in fs:
            for line in open(os.path.join(root, fn), encoding='utf8', errors='ignore'):
                line = line.strip()
                if len(line) > 40 and not line.startswith(('[', '!', '@', '&', '$')):
                    e = E(CONCL_EN.sub('', line)); paras.append(e)
                    for k in range(0, max(1, len(e) - 24), 12): idx.add(e[k:k + 24])
    return idx, paras
def is_do(en, DOI):
    if not DOI or not en: return False
    idx, paras = DOI
    m = CONCL_EN.search(en); e = E(en[:m.start()] if m else en)
    if len(e) < 30: return False
    grams = [e[k:k + 24] for k in range(0, max(1, len(e) - 24), 6)]
    hit = sum(g in idx for g in grams) / max(1, len(grams))
    if hit < 0.5: return False
    return any(difflib.SequenceMatcher(None, e, p, autojunk=False).ratio() >= 0.95 for p in paras if abs(len(p) - len(e)) < 0.1 * len(e) + 10 and p[:12] == e[:12] or e[:20] in p)

def en_concl_ok(en):
    # js splitConcl must cut the 1959 English exactly at its printed conclusion
    m = CONCL_EN.search(en)
    return bool(m) and bool(re.match(r'[;:,.]?\s*(?:[Tt]hrough|[Ww]ho (?:live|lives))', en[m.start():])) and len(en) - m.start() < 160

def choose(key, v, pages_of_mass):
    oks = [c for c in v['cands'] if c[0]]
    if not oks: return None, None
    f = key[2]
    def score(c):
        ok, ratio, r, real = c
        same_typ = (r['typ'] == f) or (f == 'sp' and r['typ'] in ('or', 'sp'))
        pm = pages_of_mass.get(key[:2]); dist = min(abs(r['p'] - p) for p in pm) if pm else 0
        return (same_typ, -dist, r['en_concl'], ratio)
    oks.sort(key=score, reverse=True)
    alts = len(set(E(c[2]['en']) for c in oks))
    return oks[0], alts

def classify(res):
    """res -> {key: {'s': 'dm'|'do'|'ai', 'en': ..., 'why': ...}}"""
    pages = collections.defaultdict(list)
    for key, v in res.items():
        for c in v['cands']:
            if c[0]: pages[key[:2]].append(c[2]['p'])
    pages_med = {k: sorted(p)[len(p) // 2:len(p) // 2 + 1] for k, p in pages.items()}
    DOI = do_index()
    out = {}
    for key, v in res.items():
        c, alts = choose(key, v, pages_med)
        if c:
            r = c[2]; en = r['en']
            flags = []
            if not r['en_concl']: flags.append('no-concl')
            if not en_concl_ok(en): flags.append('concl-split')
            if r['unk']: flags.append('unk:' + ','.join(r['unk']))
            L = len(v['la']); 
            if not (0.8 <= len(en) / max(1, L) <= 2.4): flags.append('len')
            if alts > 1: flags.append('alts:%d' % alts)
            out[key] = {'s': 'dm', 'en': en, 'p': r['p'], 'i': r['i'], 'flags': flags}
        else:
            why = 'none'
            if v['cands']:
                real = v['cands'][0][3]; why = 'differs'
                ws = ' '.join(a + ' ' + b for a, b in real)
                if re.search(r'\bn\b', ' '.join(b for a, b in real)): why = 'differs:N.'
                elif len(real) == 1 and len(real[0][0].split()) <= 1 and len(real[0][1].split()) <= 1: why = 'differs:one-word'
                elif v['cands'][0][1] < 0.8: why = 'none'   # nearest DM prayer is another prayer
            s = 'do' if is_do(v['en_old'], DOI) else 'ai'
            out[key] = {'s': s, 'why': why, 'real': v['cands'][0][3] if v['cands'] else None, 'near': v['cands'][0][2]['i'] if v['cands'] else None}
    return out

DM_LABEL = 'St Dominic Missal (1959)'
def src_note(kinds):
    ks = sorted(set(kinds.values()))
    names = {'dm': 'the St Dominic Missal (1959), verbatim', 'do': 'Divinum Officium', 'ai': 'translated for this site (AI)'}
    if len(ks) == 1: return 'English: ' + names[ks[0]]
    return 'English: ' + '; '.join(names[k] + ' (' + ', '.join(f for f in ('or', 'se', 'pc', 'sp') if kinds.get(f) == k) + ')' for k in ('dm', 'do', 'ai') if k in ks)
OLD_NOTE = re.compile(r'English (?:after|from) the St Dominic Missal(?: \(1959\))?(?:, checked against the Latin)?(?:, in the plural)?|English translated for this site \(AI\)(?:, checked against the Latin| where not already on the site)?|English: [^;]*(?:;[^;]*\([a-z, ]+\))*$')

def write(out):
    h, O, t = load('/data/orations.js', 'window.ORATIONS = ')
    n = collections.Counter()
    for k, v in O.items():
        kinds = {}
        for f in ('or', 'se', 'pc', 'sp'):
            x = out.get(('orations', k, f))
            if not x or f not in v: continue
            if x['s'] == 'dm': v[f][1] = x['en']
            kinds[f] = x['s']; n[x['s']] += 1
        if kinds:
            v['en_src'] = kinds
            if v.get('src', '').startswith('Missale'):
                note = src_note(kinds)
                v['src'] = OLD_NOTE.sub(note, v['src']) if OLD_NOTE.search(v['src']) else v['src'] + '; ' + note
    open(R + '/data/orations.js', 'w', encoding='utf8').write(h + json.dumps(O, ensure_ascii=False) + t)
    print('orations.js', dict(n))
    h, M, t = load('/data/memoriae.js', 'window.MEMORIAE = ')
    n = collections.Counter()
    for k, v in M.items():
        kinds = {}
        for f in ('or', 'se', 'pc'):
            x = out.get(('memoriae', k, f))
            if not x or f not in v: continue
            if x['s'] == 'dm': v[f][1] = x['en']
            kinds[f] = x['s']; n[x['s']] += 1
        if kinds:
            v['en_src'] = kinds
            note = src_note(kinds)
            v['src'] = OLD_NOTE.sub(note, v['src']) if OLD_NOTE.search(v['src']) else v['src'] + '; ' + note
    open(R + '/data/memoriae.js', 'w', encoding='utf8').write(h + json.dumps(M, ensure_ascii=False, separators=(',', ':')) + t)
    print('memoriae.js', dict(n))
    h, A, t = load('/data/addiv.js', 'window.ADDIV = ')
    n = collections.Counter()
    for k, v in A['sets'].items():
        kinds = {}
        for f in ('or', 'se', 'pc'):
            x = out.get(('addiv', k, f))
            if not x or f not in v: continue
            if x['s'] == 'dm':
                m = CONCL_EN.search(x['en'])
                v[f]['en'] = x['en'][:m.start()].strip()
                ec = re.sub(r'^[;:,.]?\s*', '', m.group(0)); v[f]['ec'] = ec[0].upper() + ec[1:]
            v[f]['s'] = x['s']; kinds[f] = x['s']; n[x['s']] += 1
        if kinds and 'src' in v:
            note = src_note(kinds)
            v['src'] = OLD_NOTE.sub(note, v['src']) if OLD_NOTE.search(v['src']) else v['src']
    open(R + '/data/addiv.js', 'w', encoding='utf8').write(h + json.dumps(A, ensure_ascii=False, separators=(',', ':')) + t)
    print('addiv.js', dict(n))

if __name__ == '__main__':
    if '--table' in sys.argv or not os.path.exists(DM + '/work/res.pkl'):
        res, recs = build_table(); pickle.dump(res, open(DM + '/work/res.pkl', 'wb'))
    res = pickle.load(open(DM + '/work/res.pkl', 'rb'))
    out = classify(res)
    json.dump({'|'.join(k): v for k, v in out.items()}, open(TABLE, 'w'), ensure_ascii=False, indent=0)
    cnt = collections.Counter((k[0], v['s'], v.get('why', '')) for k, v in out.items())
    for x in sorted(cnt.items()): print(x)
    print('flagged dm:', sum(1 for v in out.values() if v.get('flags')))
    if '--write' in sys.argv: write(out)
