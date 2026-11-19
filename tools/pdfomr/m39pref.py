"""Prefaces (and the other chants) of the Appendix of the Missale O.P. 1939 -> gabc.
1. m39app.main reads every staff of pdf pages 445-461 (notes with positions, bars, OCR lyric words with x).
2. Notes go to the OCR syllable over which they stand; the staves are cut into pieces at the headings.
3. The OCR syllables are aligned letter by letter with the right Latin (data/prefaces.js + the dialogue), and each right
   syllable takes the notes of the OCR syllables that fall in it.
usage: m39pref.py M39.pdf  -> gabc/op-praef-*.gabc + tools/pdfomr/m39pref_report.txt"""
import sys, os, re, json, difflib, unicodedata, subprocess, pickle
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from m39app import main as read_page
from syl import isv as _isv, base
def isv(w, i):
    # 'i' after the u of qu/gu is a vowel (Qui-a), not the consonantal i between vowels
    if base(w[i]) == 'i' and i >= 2 and base(w[i - 1]) == 'u' and base(w[i - 2]) in 'qg': return True
    return _isv(w, i)
def syllables(w):
    """start indices of the syllables of a Latin word, as the chant books divide them (Sur-sum, sanc-tæ, Ec-clé-si-æ, ex-ér-ci-tus, dí-gnum)"""
    n = len(w); vs = []; i = 0
    while i < n:
        if isv(w, i):
            j = i + 1
            if j < n and isv(w, j) and (base(w[i]) + base(w[j])) in ('ae', 'oe', 'au'): j += 1
            vs.append((i, j)); i = j
        else: i += 1
    if len(vs) <= 1: return [0]
    starts = [0]
    for k in range(1, len(vs)):
        a, b = vs[k - 1][1], vs[k][0]; cl = w[a:b]; lc = cl.lower()
        if len(cl) == 0: starts.append(a)
        elif len(cl) == 1: starts.append(a + 1 if lc == 'x' else a)
        else:
            if len(lc) >= 3 and lc[-3] == 's' and lc[-2] in 'ptc' and lc[-1] in 'lr': cut = b - 3
            elif lc.endswith('qu') or lc[-2:] in ('ch', 'ph', 'th', 'gn', 'st', 'sp', 'sc') or (lc[-2] in 'bcdfgpt' and lc[-1] in 'lr'): cut = b - 2
            else: cut = b - 1
            if lc[0] == 'x': cut = max(cut, a + 1)
            starts.append(max(a, cut))
    return starts
ROOT = os.path.join(HERE, '..', '..')
PDF = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/dl_m39/M39.pdf'
CACHE = '/tmp/m39app_cache_%s_%s_%s.pkl' % (os.environ.get('THR', 115), os.environ.get('OPN', 0.28), os.environ.get('KH', 0.85))
if os.path.exists(CACHE): STAVES = pickle.load(open(CACHE, 'rb'))
else:
    STAVES = []
    import pymupdf
    d = pymupdf.open(PDF)
    for pg in range(445, 462):
        for side in 'LR':
            r, g = read_page(PDF, pg, side)
            # headings on this half page (text layer), with their y in the same (deskewed) pixel space ~ unrotated y is close enough
            p = d[pg]; W2 = p.rect.width / 2; x0 = 0 if side == 'L' else W2
            heads = []
            for b in p.get_text('dict')['blocks']:
                for l in b.get('lines', []):
                    t = ''.join(s['text'] for s in l['spans']).strip()
                    if x0 <= l['bbox'][0] < x0 + W2 and re.match(r'^(PR.{1,3}EFATIO|PR.?EFA ?TIO|AD PATER|ANTE AGNUS|TONI |TONUS|CANTUS (SOLEMNIS|FERIALIS))', t):
                        heads.append(((l['bbox'][1]) * 400 / 72, t))
            for x in r:
                x['page'] = pg; x['side'] = side
            STAVES.append({'page': pg, 'side': side, 'staves': r, 'heads': heads})
    pickle.dump(STAVES, open(CACHE, 'wb'))

def flat(s):
    s = s.replace('æ', 'ae').replace('Æ', 'ae').replace('œ', 'oe').replace('ǽ', 'ae')
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
    return re.sub(r'[^a-z]', '', s.lower().replace('j', 'i'))

def staff_syllables(x):
    """OCR words of one staff: [(word, x0, [syllables])], and the notes/bars on the staff"""
    s = x['s']; toks = []
    for a0, a1, tt in sorted(x['words']):
        tt = tt.translate(str.maketrans('16053', 'loosa'))   # OCR digit look-alikes (saecu-16-rum)
        t2 = re.sub(r'[^A-Za-zæœÆŒ\-]', '', tt)
        if not t2: continue
        sy = []
        for p in [p for p in t2.split('-') if p]:
            st = syllables(p); ends = st[1:] + [len(p)]
            sy += [p[st[k]:ends[k]] for k in range(len(st))]
        # a drop cap read as its own word ("P" + "er"): join it to the next word
        if toks and len(toks[-1][2]) == 1 and len(toks[-1][2][0]) == 1 and toks[-1][2][0].isupper() and a0 - toks[-1][1] < 4 * s:
            toks[-1] = (toks[-1][0] + t2, toks[-1][1], [toks[-1][2][0] + sy[0]] + sy[1:]); continue
        toks.append((t2, a0, sy))
    items = [it for it in x['items'] if (it[1] == 'bar') or (-1 <= it[2] <= 6 and 12 <= it[3] <= 40)]
    # a column of 4+ stacked 'notes' is a (thick) bar line
    xs_ = sorted(set(it[0] for it in items if it[1] == 'note'))
    drop = set()
    for xv in xs_:
        col = [it for it in items if it[1] == 'note' and abs(it[0] - xv) < 9]
        if len(col) >= 4: drop |= set(map(id, col))
    if drop: items = [it for it in items if id(it) not in drop]
    out = []
    for it in items:
        if it[1] == 'note' and it[0] < x['x'][0] + 1.15 * s: continue   # clef
        if it[1] == 'note' and it[0] > x['x'][1] - 0.85 * s: continue    # custos at the right edge
        if it[1] == 'bar' and (it[0] < x['x'][0] + 1.5 * s or it[0] > x['x'][1] - 0.6 * s): continue   # staff ends
        out.append(it)
    return toks, out, s

def assign(toks, items, s):
    """notes to syllables. Note columns closer than 0.9 staff-spaces form one neume (one syllable); between syllables the text
    spreads the notes at least 1.4 spaces apart. When a staff has as many neumes as syllables they pair one to one; otherwise
    each word takes the neumes under it (from its start to the next word's), one per syllable, cutting at the widest gaps."""
    res = []
    if not toks: return res
    notes = sorted([it for it in items if it[1] == 'note'], key=lambda i: i[0])
    bars = [it for it in items if it[1] == 'bar']
    cols = []
    for n in notes:
        if cols and n[0] - cols[-1][-1][0] < 9: cols[-1].append(n)
        else: cols.append([n])
    neu = []
    for c in cols:
        if neu and c[0][0] - neu[-1][-1][-1][0] < 0.9 * s: neu[-1].append(c)
        else: neu.append([c])
    nsy = sum(len(tk[2]) for tk in toks)
    flatn = lambda nm: [(n[0], n[2]) for c in nm for n in c]
    if len(neu) == nsy:
        k = 0
        for w, x0, sy in toks:
            for sname in sy: res.append([sname, flatn(neu[k]), None]); k += 1
    else:
        xs = [tk[1] for tk in toks] + [1e9]
        for i, (w, x0, sy) in enumerate(toks):
            mine = [nm for nm in neu if x0 - 0.5 * s <= nm[0][0][0] < xs[i + 1] - 0.5 * s]
            k = len(sy)
            if len(mine) <= k: groups = [[nm] for nm in mine] + [[] for _ in range(k - len(mine))]
            else:
                gaps = sorted(range(1, len(mine)), key=lambda j: -(mine[j][0][0][0] - mine[j - 1][-1][-1][0]))[:k - 1]
                groups = []; prev = 0
                for c in sorted(gaps) + [len(mine)]: groups.append(mine[prev:c]); prev = c
            for j, sname in enumerate(sy):
                res.append([sname, [p for nm in (groups[j] if j < len(groups) else []) for p in flatn(nm)], None])
    # bars: after the syllable whose neume is the last one before the bar
    starts = []
    k = 0
    for r in res:
        starts.append(min([p[0] for p in r[1]], default=None))
    for bb in bars:
        cand = [i for i, st in enumerate(starts) if st is not None and st < bb[0]]
        if cand: res[max(cand)][2] = {'half': ';', 'full': ':', 'double': '::'}[bb[2]]
    return res

def groups_gabc(notes):
    notes = sorted(notes, key=lambda t: (round(t[0] / 12), -t[1]))
    # same x (a pes / stacked): lower first; else by x
    out = []; i = 0
    notes = sorted(notes, key=lambda t: t[0])
    while i < len(notes):
        j = i; grp = [notes[i]]
        while j + 1 < len(notes) and abs(notes[j + 1][0] - notes[i][0]) < 9: j += 1; grp.append(notes[j])
        grp.sort(key=lambda t: t[1])
        out += [chr(ord('d') + p) for _, p in grp]
        i = j + 1
    r = ''.join(out)
    h = len(r) // 2
    if len(r) >= 2 and len(r) % 2 == 0 and r[:h] == r[h:]: r = r[:h]   # one neume read twice
    return r

# pieces: consecutive staves between headings
pieces = []; cur = None
for half in STAVES:
    hs = sorted(half['heads'])
    for x in half['staves']:
        y = x['L'][0]
        for hy, ht in hs:
            if hy < y and (not cur or cur.get('_hy') != (half['page'], half['side'], hy)) and all(not (hy < z['L'][0] < y) for z in half['staves'] if z is not x):
                cur = {'title': ht, 'staves': [], '_hy': (half['page'], half['side'], hy)}; pieces.append(cur)
        if cur is None: continue
        cur['staves'].append(x)
json.dump([{'title': p['title'], 'n': len(p['staves']), 'pages': sorted(set((z['page'], z['side']) for z in p['staves']))} for p in pieces], open('/tmp/m39pieces.json', 'w'), indent=0)
for p in pieces: print(p['title'], len(p['staves']), sorted(set((z['page'], z['side']) for z in p['staves']))[:4])
pickle.dump(pieces, open('/tmp/m39pieces.pkl', 'wb'))

# ---------------------------------------------------------------- the right text, and gabc
def node_prefaces():
    js = "global.window={};eval(require('fs').readFileSync('%s','utf8')+';process.stdout.write(JSON.stringify(PREFACES))')" % os.path.join(ROOT, 'data', 'prefaces.js')
    return json.loads(subprocess.run(['node', '-e', js], capture_output=True, text=True).stdout)
PREF = node_prefaces()
DIALOGUE = 'Per ómnia sǽcula sæculórum. Amen. Dóminus vobíscum. Et cum spíritu tuo. Sursum corda. Habémus ad Dóminum. Grátias agámus Dómino Deo nostro. Dignum et justum est.'
KEYS = [('NATIVITATE', 'Nativitate'), ('EPIPHANIA', 'Epiphania'), ('QUADRAGESIMA', 'Quadragesima'), ('CRUCE', 'Sancta Cruce'), ('PASCH', 'Paschalis'),
        ('ASCENSIONE', 'Ascensione'), ('SPIRITU', 'Spiritu Sancto'), ('TRINITATE', 'SS. Trinitate'), ('REGIS', 'D. N. Iesu Christo'), ('MARIA', 'B. Maria Virgine'),
        ('JOSEPH', 'S. Ioseph'), ('APOSTOLIS', 'Apostolis'), ('DOMINICO', 'Dominico'), ('FRANCISCO', 'Francisco'), ('COMMUNIS', 'Communis'), ('DEFUNCTIS', 'Defunctorum')]
def text_for(title):
    for k, v in KEYS:
        if k in title.upper().replace('^', 'A'):
            la = PREF[v]['la']
            la = la.replace('{in hoc potíssimum}', 'in hac potíssimum die' if 'DIE' in title.upper() else 'in hoc potíssimum')
            la = re.sub(r'\{([^}]*)\}', r'\1', la).replace(' hodiérna die', ' hodiérna die')
            return v, DIALOGUE + ' ' + la
    return None, None
def correct_syllables(text):
    out = []   # [syllable text incl. punctuation and following space, flat start, flat end]
    pos = 0
    for w in re.findall(r'\S+', text):
        core = re.sub(r'[^A-Za-zÀ-ÿæœǽÆŒǼ]', '', w)
        if not core: 
            if out: out[-1][0] += ' ' + w
            continue
        lead = w[:w.index(core[0])]; tail = w[len(lead) + len(core):]
        st = syllables(core); ends = st[1:] + [len(core)]
        for k, (a, b) in enumerate(zip(st, ends)):
            s = core[a:b]; f = flat(s)
            out.append([(lead if k == 0 else '') + s + (tail if k == len(st) - 1 else ''), pos, pos + len(f), k == len(st) - 1])
            pos += len(f)
    return out
def neumes_of(items, s):
    notes = sorted([it for it in items if it[1] == 'note'], key=lambda i: i[0])
    cols = []
    for n in notes:
        if cols and n[0] - cols[-1][-1][0] < 9: cols[-1].append(n)
        else: cols.append([n])
    neu = []
    for c in cols:
        if neu and c[0][0] - neu[-1][-1][-1][0] < 0.9 * s: neu[-1].append(c)
        else: neu.append([c])
    return [[(n[0], n[2]) for c in nm for n in c] for nm in neu]
def build(piece):
    key, text = text_for(piece['title'])
    if not text: return key, None, [], []
    C = correct_syllables(text); CF = ''.join(flat(c[0]) for c in C)
    cstart = [c[1] for c in C]
    st_info = []; F = ''
    for x in piece['staves']:
        toks, items, s = staff_syllables(x)
        a0 = len(F); F += ''.join(flat(tk[0]) for tk in toks)
        st_info.append((x, toks, items, s, a0, len(F)))
    sm = difflib.SequenceMatcher(None, F, CF, autojunk=False)
    blocks = sm.get_matching_blocks()
    def fmap(i):
        best = None
        for a, b, n in blocks:
            if a <= i < a + n: return b + (i - a)
            if a + n <= i: best = b + n + (i - a - n)
        return best if best is not None else 0
    def syl_at(ci): return max([k for k, c in enumerate(cstart) if c <= ci], default=0)
    notes = [[] for _ in C]; bars = [None] * len(C); prev_end = -1; how = []; SPANS = []
    for (x, toks, items, s, f0, f1) in st_info:
        if f1 <= f0: continue
        lo = max(prev_end + 1, syl_at(fmap(f0))); hi = syl_at(fmap(f1 - 1))
        if hi < lo: continue
        neu = neumes_of(items, s)
        span = list(range(lo, hi + 1))
        if len(neu) == len(span):
            for k, nm in zip(span, neu): notes[k] += nm
            how.append('1:1')
        else:
            # fall back: OCR syllables with notes, mapped letter by letter
            ocr = assign(toks, items, s); pos = f0
            for t_, n_, b_ in ocr:
                k = syl_at(fmap(pos)); k = min(max(k, lo), hi)
                notes[k] += n_
                if b_: bars[k] = b_
                pos += len(flat(t_))
            how.append('fb(%d/%d)' % (len(neu), len(span)))
        # bars by x: after the syllable whose first note is the last one before the bar
        if len(neu) == len(span):
            for bb in [it for it in items if it[1] == 'bar']:
                cand = [k for k, nm in zip(span, neu) if nm and nm[0][0] < bb[0]]
                if cand: bars[max(cand)] = {'half': ';', 'full': ':', 'double': '::'}[bb[2]]
        SPANS.append((x['page'], x['side'], x['L'], x['x'], lo, hi, how[-1]))
        prev_end = hi
    # hand corrections from proofing against the scan: {file: {syllable index: notes}}
    FIX = json.load(open(os.path.join(HERE, 'm39pref_fix.json'))) if os.path.exists(os.path.join(HERE, 'm39pref_fix.json')) else {}
    piece['_spans'] = SPANS; piece['_C'] = C
    warn = [C[i][0] for i in range(len(C)) if not notes[i]]
    piece['_nx'] = [list(n) for n in notes]
    g = []; piece['_notes'] = []
    fx = FIX.get(piece['title'], {})
    for i, (c, n, b) in enumerate(zip(C, notes, bars)):
        nn = fx[str(i)] if str(i) in fx else (groups_gabc(n) or '?')
        if str(i) + 'bar' in fx: b = fx[str(i) + 'bar'] or None
        piece['_notes'].append((c[0].rstrip(), nn, b))
        g.append('%s(%s)' % (c[0].rstrip(), nn) + (' (%s)' % b if b else '') + (' ' if c[3] else ''))
    return key, ''.join(g).replace('  ', ' '), how, warn
REPORT = []
OUT = {}
for p in pieces:
    if 'PRAEFATIO' not in p['title'].upper().replace('^', 'A').replace('J', 'A').replace(' ', '').replace('PREFATIO', 'PRAEFATIO'): continue
    key, gabc, how, warn = build(p)
    sol = 'FERIAL' not in p['title'].upper()
    name = (key or p['title']) + (' (tonus solemnis)' if sol else ' (tonus ferialis)')
    OUT[name] = gabc
    if gabc:
        slug = {'Nativitate': 'nativitate', 'Epiphania': 'epiphania', 'Quadragesima': 'quadragesima', 'Sancta Cruce': 'cruce', 'Paschalis': 'paschalis',
                'Ascensione': 'ascensione', 'Spiritu Sancto': 'spiritu-sancto', 'SS. Trinitate': 'trinitate', 'D. N. Iesu Christo': 'christo-rege',
                'B. Maria Virgine': 'bmv', 'S. Ioseph': 'ioseph', 'Apostolis': 'apostolis', 'Dominico': 'dominico', 'Francisco': 'francisco', 'Communis': 'communis',
                'Defunctorum': 'defunctorum'}[key]
        if 'DIE PASCH' in p['title'].upper(): slug = 'paschalis-die'
        fn = 'op-m39-praef-%s-%s.gabc' % (slug, 'solemn' if sol else 'ferial')
        hdr = 'name:Praefatio %s (%s);\noffice-part:Praefatio;\ncommentary:Missale O.P. (1939), Appendix (OMR, proofed);\n%%%%\n(f3) ' % (key, 'tonus solemnis' if sol else 'tonus ferialis')
        open(os.path.join(ROOT, 'gabc', fn), 'w').write(hdr + gabc.strip() + ' (::)\n')
        p['_fn'] = fn
    REPORT.append('## %s  [%s]  %d/%d staves 1:1; %d syllables without notes: %s' % (p['title'], key, how.count('1:1'), len(how), len(warn), ' | '.join(warn[:30])))
json.dump(OUT, open('/tmp/m39pref_gabc.json', 'w'), ensure_ascii=False, indent=1)
pickle.dump([{k: p.get(k) for k in ('title', '_spans', '_notes', '_fn', '_nx')} for p in pieces], open('/tmp/m39pref_spans.pkl', 'wb'))
open(os.path.join(HERE, 'm39pref_report.txt'), 'w').write('\n'.join(REPORT) + '\n')
print('\n'.join(REPORT))
