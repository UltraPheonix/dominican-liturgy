"""Build the 1909 Dominican Office (Cormier) -> data/office1909/ (same format as data/office/).
Stage 1 (this file): the Ordinary + Psalter for every day of the range (tools/b09/psalter1909.json); parts that belong to the
Proprium de Tempore / Sanctorale are marked 'in preparation'. Days whose Office is wholly proper (Christmas to the Epiphany
octave, the Triduum, Easter week, Ascension to the octave of Corpus Christi) get a notice only.
usage: python3 tools/b09/build.py   (needs the Divinum Officium clone, see HANDOFF)"""
import json, os, re, glob, hashlib, datetime, difflib, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
DO = '/home/claude/divinumofficium/divinum-officium/web/www/horas'
OUT = os.path.join(REPO, 'data', 'office1909')
FROM, TO = datetime.date(2026, 11, 1), datetime.date(2027, 12, 31)
P = json.load(open(os.path.join(HERE, 'psalter1909.json')))
T = json.load(open(os.path.join(HERE, 'tempora1909.json')))
LES = json.load(open(os.path.join(HERE, 'lessons1909.json')))
def tkey(d):
    s, wk, n, prop = season(d); w = (d.weekday() + 1) % 7
    if s == 'adv': return 'adv%d-%d' % (n, w)
    if s != 'adv' and okey(d): return None
    if s == 'pt' and w == 6 and (d + datetime.timedelta(days=1)) == adv1(d.year): return 'pre-adv'
    return None
OFF = json.load(open(os.path.join(HERE, 'offices1909.json'))) if os.path.exists(os.path.join(HERE, 'offices1909.json')) else {}
RANKS = [('totum duplex', 4), ('duplex', 3), ('semiduplex', 2), ('simplex', 1), ('trium lect', 1), ('iij. lect', 1)]
def san_rank(o):
    t = (o.get('title', '') + ' ' + (o.get('rank') or '')).lower().replace('dupi.ex', 'duplex').replace('dupl ex', 'duplex')
    for k, v in RANKS:
        if k in t: return v, k
    return 0, None
SAN = {}
for k, o in OFF.items():
    if not k.startswith('S:'): continue
    md = k.split(':')[1]; ti = re.sub(r'\s+', ' ', o.get('title', '')).strip()
    if not re.match(r'^(S|Ss|B|Bb|In|Cáth|Cath)\b', ti) or len(ti) < 10 or not o.get('oratio'): continue
    r, rn = san_rank(o)
    ti = re.split(r'\s(?:In [IL1]\. Vesperis|In i\. Vesperis|Hymnus|Oratio|Ad |Omnia|Invitatorium|In I\. Nocturno)', ti)[0]
    ti = re.sub(r'\s*(Totum Duplex|Totum DUPL\S*|duplex|Duplex|Semiduplex|Simplex|simplex)\.?.*$', '', ti, flags=re.I).strip(' .,')
    ti = re.sub(r'Ord\.?,?\s*\S{1,3}[\.,]?\s*\S{0,4}[A-Z<>/\^\*\.]{2,6}\S*', 'Ord. Præd.', ti)
    ti = re.sub(r'\bViro\.', 'Virg.', ti); ti = re.sub(r'\bCONE\.', 'Conf.', ti); ti = re.sub(r'\bCONF\b', 'Conf', ti)
    ti = ' '.join(w if not (w.isupper() and len(w) > 3) else w.capitalize() for w in ti.split())
    if md not in SAN or r > SAN[md]['r']: SAN[md] = {'r': r, 'rank': rn, 'title': ti, 'oratio': o['oratio']}
CAL = {}
for l in open(os.path.join(HERE, 'calendar1909.txt'), encoding='utf-8'):
    if l.startswith('#') or '|' not in l: continue
    md, ti, rk = (l.rstrip('\n').split('|') + ['', ''])[:3]
    CAL.setdefault(md, []).append({'title': ti, 'rank': rk or None})
RV = {'Totum Duplex': 4, 'Solemnis': 3, 'Duplex': 3, 'Semiduplex': 2, 'Simplex': 1, 'Tres Lectiones': 1, 'Novem Lectiones': 0, 'Memoria': 0}
def celebrable(d, s, w, rk):
    """provisional precedence (Rubricae generales to be applied fully): privileged Sundays (Advent, Septuagesima–Passiontide)
    and the ferias of Ash Wednesday and Holy Week exclude every feast; other Sundays yield to Duplex and Totum Duplex; Lenten
    ferias admit Duplex and Totum Duplex; other ferias admit every feast of three or more lessons"""
    if w == 0: return s not in ('adv', 'sept', 'quad', 'pass') and rk >= 3
    if s in ('cin',) and d.weekday() == 2: return False
    if s == 'pass' and (d - (easter(d.year) - datetime.timedelta(days=7))).days >= 0: return False
    if s in ('quad', 'pass', 'cin'): return rk >= 3
    return rk >= 1
PAIRS = {('b', 'o'), ('d', 'e'), ('d', 'a'), ('b', 'a'), ('h', 'o'), ('f', 'i'), ('t', 'i'), ('r', 'i'), ('d', 'o'), ('c', 'e'), ('a', 'e'), ('i', 'e'), ('i', 'l'), ('l', 'i'), ('n', 'u'), ('u', 'n'), ('t', 'f'), ('r', 'c'), ('e', 'c'), ('o', 'a'),
         ('a', 'o'), ('k', 'e'), ('h', 'b'), ('b', 'h'), ('i', 't'), ('f', 's'), ('s', 'f'), ('e', 'a'), ('m', 'n'), ('n', 'm')}
def ocr_word(x, LD):
    """an OCR word not in the dictionary: one substitution of a usual OCR confusion (pastdris -> pastóris, concade -> concéde);
    junk of 1-3 letters not in the dictionary is dropped (None)"""
    m = re.match(r'^(\W*)([A-Za-z]+)(\W*)$', x)
    if not m: return x
    import latcount as LC
    pre, core, post = m.groups(); b = LD.base(core); n = LC.N.get(b, 0)
    if n >= 3: return x
    if len(core) <= 3 and re.fullmatch(r'[Il][il]+', core): return pre.strip() + post.strip() or None
    if len(core) <= 3 and n == 0 and core.lower() not in ('et', 'in', 'ad', 'ut', 'a', 'e', 'o'): return pre.strip() + post.strip() or None
    c = [k for k in LD.near(b) if [(p, q) for p, q in zip(b, k) if p != q][0] in PAIRS and LC.N.get(k, 0) >= max(10, 20 * n)]
    if len(c) > 1: c = sorted(c, key=lambda k: -LC.N.get(k, 0))[:1] if LC.N.get(c[0], 0) > 0 and sorted((LC.N.get(k, 0) for k in c))[-1] >= 5 * sorted((LC.N.get(k, 0) for k in c))[-2] else []
    if len(c) != 1: return x
    h = LD.D[c[0]]; h = h[:1].upper() + h[1:] if core[:1].isupper() else h
    return pre + h + post
def clean_prayer(t):
    """last repairs of a saint's prayer from the OCR: end at the conclusion, the drop-capital, æ read as 'se' / 'a?' / 'a:', dictionary words"""
    import latdict as LD
    m = re.search(r'\s(?:Ad (?:Utr|Matut|Laudes|Benedi|Magni|Mem|I+\. Vesp|Vesp|ii?j?\.)|Super Psalm|Invitatorium|Lectio [ivx]|Hymnus|In I+\. Noct|Capitulum|Die [IVXLivxl]+\.)', t)
    if m: t = t[:m.start()]
    m = re.search(r'\b(?:Per (?:Dóminum|Dominum|eúndem|eumdem|Christum)\b[^.]{0,120}|Qui (?:tecu\w|vivis|cum Patre)\b[^.]{0,160}|[PF][eo]r)\s*[.*,]', t)
    if m:
        c = m.group(0)
        end = ' Qui vivis.' if 'vivis' in c else ' Qui tecum.' if re.match(r'Qui (?:tecu|cum)', c) else ' Per eúndem.' if re.search(r'e[uú]n?m?dem', c) else ' Per Christum.' if 'Christum' in c else ' Per Dóminum.'
        t = t[:m.start()].rstrip(' ,;:.*') + '.' + end
    w = t.split()
    if w and w[0][:1].islower():   # drop-capital displaced: 'ómine Jesu Christe, qui D beátum' -> 'Dómine Jesu Christe, qui beátum'
        for i in range(1, min(len(w), 14)):
            if re.fullmatch(r'[A-Z]', w[i]): w[0] = w[i] + w[0]; del w[i]; break
    out = []
    for x in w:
        m = re.match(r'^(\W*)([A-Za-z]+?)(se|a\?|a:|ae|æ)(\W*)$', x)
        if m and m.group(3) != 'æ' and LD.base(m.group(2) + 'ae') in LD.D and LD.base(m.group(2) + m.group(3)) not in LD.D:
            h = LD.D[LD.base(m.group(2) + 'ae')]; h = h[:1].upper() + h[1:] if m.group(2)[:1].isupper() else h
            out.append(m.group(1) + h + m.group(4).replace('?', '').replace(':', '')); continue
        y = LD.fix_word(x)
        if y == x: y = ocr_word(x, LD)
        if y is not None: out.append(y)
    t = ' '.join(out)
    t = re.sub(r'(\w) i (?=[a-z])', r'\1; ', t); t = re.sub(r'[*"]', '', t); t = re.sub(r'a\?(?=\s|$)', 'æ', t); t = re.sub(r'\s{2,}', ' ', t)
    t = re.sub(r'\s+([;:,.])', r'\1', t); t = re.sub(r'([;:,])(?=\w)', r'\1 ', t)
    return t
_OFFM = None; _FP = {}
def final_prayer(t):
    """clean_prayer, then align once more with the Divinum Officium corpus (offices.fix_short) now that run-ons are cut"""
    global _OFFM
    if not t: return t
    if t in _FP: return _FP[t]
    if _OFFM is None:
        import offices as _o; _OFFM = _o
    k = t; t = clean_prayer(t); u = _OFFM.fix_short(t, 0.6)
    u = clean_prayer(u) if u else t
    if not re.search(r'(?:Per [^.]{0,40}|Qui [^.]{0,40})\.$', u):   # conclusion lost by the OCR: the book's rule (to the Son: Qui vivis)
        u = u.rstrip(' .') + ('. Qui vivis.' if re.match(r'(?:Dómine )?Jesu Christe|Dómine Jesu', u) else '. Per Dóminum.')
    _FP[k] = u
    return _FP[k]
def san_oratio(d, title):
    """the prayer of a saint from the extracted Sanctorale (offices.py), matched by date and name"""
    md = d.strftime('%m-%d'); best, br = None, 0.0
    tn = nb(title)
    for k, o in OFF.items():
        if not k.startswith('S:' + md + ':') or not o.get('oratio'): continue
        r_ = difflib.SequenceMatcher(None, tn[:40], nb(o.get('title', ''))[:40]).ratio()
        if r_ > br: best, br = o['oratio'], r_
    return final_prayer(best) if best and br >= 0.45 else None
def okey(d):
    """key of the extracted Proprium de Tempore (offices.py) for a date"""
    s, wk, n, prop = season(d); w = (d.weekday() + 1) % 7; E = easter(d.year)
    if s == 'pe': return 'pe%d-%d' % (n, w) if n else None
    if s == 'sept': return 'sept%d-%d' % (1 + (d - (E - datetime.timedelta(days=63))).days // 7, w)
    if s == 'cin': return 'cin-%d' % w
    if s == 'quad': return 'quad%d-%d' % (n, w)
    if s == 'pass': return 'pass%d-%d' % (1 + (d - (E - datetime.timedelta(days=14))).days // 7, w)
    if s == 'pasch': return 'pasch%d-%d' % (n, w)
    if s == 'pt' and n and w == 0:   # after Trinity only the Sunday propers are keyed by number (ferial lessons follow the 'historiae')
        for k in ('pt%d-0' % n, 'pt%d-0+' % n):
            if 'post' in OFF.get(k, {}).get('title', '').lower(): return k
    return None
def TP(d, k):
    x = T['days'].get(tkey(d) or '', {})
    if k in x: return x.get(k)
    ok = okey(d)
    if not ok: return None
    o = OFF.get(ok, {}); w = ok.rsplit('-', 1)[1]
    if k == 'oratio_week':
        return final_prayer(o.get('oratio') or OFF.get(ok.rsplit('-', 1)[0] + '-0', {}).get('oratio'))
    if k == 'magn' and w == '6':   # First Vespers of the coming Sunday
        nx = okey(d + datetime.timedelta(days=1)); return OFF.get(nx or '', {}).get('magn1') or o.get('magn2')
    if k == 'oratio_vesp' and w == '6':
        nx = okey(d + datetime.timedelta(days=1)); return final_prayer(OFF.get(nx or '', {}).get('oratio'))
    m = {'invit': 'invit', 'laudes': 'laudes', 'bened': 'bened', 'magn': 'magn2'}.get(k)
    v = o.get(m) if m else None
    if k == 'laudes' and v and len(v) < 5: return None
    return v

def nb(s):
    s = unicodedata.normalize('NFD', s.lower()); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z]', '', s.replace('æ', 'ae').replace('œ', 'oe').replace('j', 'i'))

# ---------- 1954 library (fixed texts and hymns, with their English) ----------
lib, pair = {}, {}
lib.update(json.load(open(os.path.join(REPO, 'data/office/common.json'))))
for f in sorted(glob.glob(os.path.join(REPO, 'data/office/20*/*.json'))):
    d = json.load(open(f)); lib.update(d['b'])
    for rows in d['h'].values():
        for r in rows:
            if len(r) == 2: pair.setdefault(r[0], r[1])
OLDSH = {}
def inline_old(t):
    """a block borrowed from the 1954 data may point to a 1954 psalm shard (§NN.hash): put the psalm text in instead"""
    def rep(m):
        sh = m.group(1)
        if sh not in OLDSH:
            f = os.path.join(REPO, 'data/office/psalter', sh + '.json')
            OLDSH[sh] = json.load(open(f)) if os.path.exists(f) else {}
        return OLDSH[sh].get(sh + '.' + m.group(2), m.group(0))
    return re.sub(r'^§(\d\d)\.(\S+)$', lambda m: m.group(0) if m.group(2)[:1] in 'LE' and m.group(2)[1:2].isdigit() else rep(m), t, flags=re.M)
def L(i): return inline_old(lib[i]), inline_old(lib[pair[i]])
HYMN = {}
for k, v in lib.items():
    m = re.search(r'(?:<r>Hymnus</r>|<h>Hymnus</h>)\n(<c>.</c>[^\n]+)', v)
    if m and k in pair:
        key = nb(re.sub(r'<[^>]+>', '', m.group(1)))[:18]
        HYMN.setdefault(key, k)
def hymn_body(text):
    """the hymn part of a 1954 block: from the Hymnus heading to the Amen"""
    m = re.search(r'(?:<r>Hymnus</r>|<h>Hymnus</h>|<r>Hymn</r>|<h>Hymn</h>)\n([\s\S]*?Amen\.)', text)
    return m.group(1).strip() if m else None
def hymn(incipit):
    q = nb(incipit)[:18]; k = HYMN.get(q) or next((v for kk, v in HYMN.items() if kk.startswith(q) or q.startswith(kk)), None)
    if not k: raise SystemExit('hymn not found: ' + incipit)
    la, en = hymn_body(lib[k]), hymn_body(lib[pair[k]])
    return la, en

# ---------- Divinum Officium: Latin -> English for single lines (antiphons, versicles, chapters) ----------
def do_sections(path):
    out, cur = {}, None
    for l in open(path, encoding='utf-8'):
        l = l.rstrip('\n')
        m = re.match(r'^\[(.+)\]', l)
        if m: cur = m.group(1); out[cur] = []; continue
        if cur is not None and l.strip(): out[cur].append(l)
    return out
EN = {}
for lf in glob.glob(DO + '/Latin/**/*.txt', recursive=True):
    ef = lf.replace('/Latin/', '/English/')
    if not os.path.exists(ef) or 'Psalmorum' in lf: continue
    try: ls, es = do_sections(lf), do_sections(ef)
    except Exception: continue
    for sec, ll in ls.items():
        el = es.get(sec)
        if not el or len(el) != len(ll): continue
        for a, b in zip(ll, el):
            a = re.sub(r'^(V\.|R\.|Ant\.|v\.|r\.)\s*', '', a.split(';;')[0]); b = re.sub(r'^(V\.|R\.|Ant\.|v\.|r\.)\s*', '', b.split(';;')[0])
            if a.startswith(('!', '@', '$', '&', '_')) or len(nb(a)) < 6: continue
            EN.setdefault(nb(a), b.replace('*', '').replace('  ', ' ').strip())
ENKEYS = list(EN)
def en(la):
    k = nb(la)
    if k in EN: return EN[k]
    m = difflib.get_close_matches(k, [x for x in ENKEYS if abs(len(x) - len(k)) < 6], n=1, cutoff=0.93)
    return EN[m[0]] if m else None

# ---------- psalms: shards '§NN.Lxxx' / '§NN.Exxx' ----------
SH = {}
OCT = {chr(ord('a') + i): (1 + 8 * i, 8 + 8 * i) for i in range(22)}
def psalm_lines(num, lang):
    n = int(re.match(r'\d+', str(num)).group())
    f = '%s/%s/Psalterium/Psalmorum/Psalm%d.txt' % (DO, 'Latin' if lang == 'la' else 'English', n)
    out = []
    for l in open(f, encoding='utf-8'):
        l = l.strip()
        m = re.match(r'^(\d+):(\d+)\s+(.*)$', l)
        if not m:
            if l and not l.startswith('(') and n == 234: out.append((0, l))
            continue
        v = int(m.group(2)); t = re.sub(r'\s*[+‡]\s*', ' ', m.group(3)); t = re.sub(r'^\((?:Fit reverentia:|Bow head)\)\s*', '', t)
        out.append((v, '<n>%s:%s</n> %s' % (m.group(1), m.group(2), t.strip())))
    s = str(num)
    if s.startswith('118') and len(s) == 4: a, b = OCT[s[3]]; out = [x for x in out if a <= x[0] <= b]
    if s == '30a': out = [x for x in out if x[0] <= 6]
    if n == 234: out = [(0, l if l.startswith('<n>') else l) for _, l in out]
    return [x[1] for x in out]
def psref(num, lang):
    n = int(re.match(r'\d+', str(num)).group()); shard = '%02d' % min(n // 10, 99)
    key = '%s.%s%s' % (shard, 'L' if lang == 'la' else 'E', num)
    if key not in SH.setdefault(shard, {}): SH[shard][key] = '\n'.join(psalm_lines(num, lang))
    return '§' + key
CANT = {210: ('Canticum trium Puerorum', 'Canticle of the Three Children', 'Dan 3'), 221: ('Canticum Isaiæ', 'Canticle of Isaias', 'Isa 12'),
        222: ('Canticum Ezechíæ', 'Canticle of Ezechias', 'Isa 38'), 223: ('Canticum Annæ', 'Canticle of Anna', '1 Reg 2'),
        224: ('Canticum Moysis', 'Canticle of Moses', 'Exod 15'), 225: ('Canticum Habacuc', 'Canticle of Habacuc', 'Hab 3'),
        226: ('Canticum Moysis', 'Canticle of Moses', 'Deut 32'), 231: ('Canticum Zachariæ', 'Canticle of Zachary', 'Luc 1'),
        232: ('Canticum B. Mariæ Virginis', 'Canticle of the Blessed Virgin Mary', 'Luc 1'), 233: ('Canticum Simeonis', 'Canticle of Simeon', 'Luc 2'),
        234: ('Symbolum S. Athanasii', 'Athanasian Creed', '')}
def pstitle(num, lang):
    s = str(num); n = int(re.match(r'\d+', s).group())
    if n in CANT: c = CANT[n]; return (c[0] if lang == 'la' else c[1]) + (' (%s)' % c[2] if c[2] else '')
    w = 'Psalmus' if lang == 'la' else 'Psalm'
    if s.startswith('118') and len(s) == 4: a, b = OCT[s[3]]; return '%s 118(%d-%d)' % (w, a, b)
    if s == '30a': return '%s 30(2-6)' % w
    return '%s %d' % (w, n)

# ---------- blocks ----------
COMMON = {}
NMT = [None]   # title of the feast being built: its 'N.' (Common lessons, responsories) get the saint's name
def put(la, en_):
    if NMT[0] and 'N.' in la:
        import names1909 as _nm
        la = _nm.fill(la, NMT[0])
        if en_ and 'N.' in en_: en_ = _nm.fill_en(en_, NMT[0])
    ids = []
    for t in (la, en_ if en_ is not None else la):
        i = hashlib.sha1(t.encode()).hexdigest()[:10]; COMMON[i] = t; ids.append(i)
    return ids
GP = {'la': '<r>℣.</r> Glória Patri, et Fílio, * et Spirítui Sancto.\n<r>℟.</r> Sicut erat in princípio, et nunc, et semper, * et in sǽcula sæculórum. Amen.',
      'en': '<r>℣.</r> Glory be to the Father, and to the Son, * and to the Holy Ghost.\n<r>℟.</r> As it was in the beginning, is now, * and ever shall be, world without end. Amen.'}
NOGP = {210, 62}   # no Gloria after the Benedicite; Ps 62 joined to 66
PROPER = {'la': '<n>De Proprio de Tempore (in præparatione).</n>', 'en': '<n>From the Proper of Time (in preparation).</n>'}
def ant_en(a):
    e = en(a); return e if e else a
def psalms_block(groups, ants, head=None, lang='la', single=None, gp=True):
    """groups: [[ps,...],...]; ants: list (one per group) or None; single: one antiphon over all"""
    rows = []
    for gi, g in enumerate(groups):
        L_ = []
        if head and gi == 0: L_.append('<h>%s</h>' % head[lang])
        a = single if single is not None else (ants[gi] if ants else None)
        if a is None and (gi == 0 or single is None) and ants is not None: L_.append(PROPER[lang])
        at = (a if lang == 'la' else ant_en(a)) if a else None
        if at and (single is None or gi == 0): L_.append('<r>Ant.</r> ' + at)
        for p in g:
            L_ += ['<r>%s</r>' % pstitle(p, lang), psref(p, lang)]
        if gp and g[-1] not in NOGP and not (len(g) == 1 and g[0] == 210): L_.append(GP[lang])
        if at and (single is None or gi == len(groups) - 1): L_.append('<r>Ant.</r> ' + at)
        rows.append('\n'.join(L_))
    return rows
def psalm_rows(groups, ants=None, head=('Psalmi', 'Psalms'), single=None, gp=True):
    la = psalms_block(groups, ants, {'la': head[0], 'en': head[1]}, 'la', single, gp)
    en_ = psalms_block(groups, ants, {'la': head[0], 'en': head[1]}, 'en', single, gp)
    return [put(a, b) for a, b in zip(la, en_)]
def VR(v, lang):
    if lang == 'la': return '<r>℣.</r> %s\n<r>℟.</r> %s' % (v[0], v[1])
    return '<r>℣.</r> %s\n<r>℟.</r> %s' % (ant_en(v[0]), ant_en(v[1]))
def vr_row(v): return put(VR(v, 'la'), VR(v, 'en'))
def note_row(la, en_): return put('<n>%s</n>' % la, '<n>%s</n>' % en_)

# ---------- calendar ----------
def easter(y):
    a = y % 19; b, c = divmod(y, 100); d, e = divmod(b, 4); f = (b + 8) // 25; g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30; i, k = divmod(c, 4); l = (32 + 2 * e + 2 * i - h - k) % 7; m = (a + 11 * h + 22 * l) // 451
    mo, da = divmod(h + l - 7 * m + 114, 31); return datetime.date(y, mo, da + 1)
def adv1(y):
    x = datetime.date(y, 12, 25); return x - datetime.timedelta(days=(x.weekday() + 1) % 7 or 7) - datetime.timedelta(weeks=3)
ROM = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI', 'XXII', 'XXIII', 'XXIV', 'XXV', 'XXVI', 'XXVII', 'XXVIII']
FER = ['Feria Secunda', 'Feria Tertia', 'Feria Quarta', 'Feria Quinta', 'Feria Sexta', 'Sabbato']
def season(d):
    """(season, week title, wholly proper?)"""
    y = d.year; E = easter(y); A = adv1(y); dd = lambda n: E + datetime.timedelta(days=n)
    if d >= A and d <= datetime.date(y, 12, 23): return 'adv', 'Adventus', 1 + (d - A).days // 7, False
    if d >= datetime.date(y, 12, 24) or d <= datetime.date(y, 1, 13): return 'nat', None, 0, True
    if d < dd(-63): sun1 = datetime.date(y, 1, 14) + datetime.timedelta(days=(6 - datetime.date(y, 1, 14).weekday()) % 7); return 'pe', 'post Octavam Epiphaniæ', 1 + (d - sun1).days // 7 if d >= sun1 else 0, False
    if d < dd(-46): return 'sept', ['Septuagesimæ', 'Sexagesimæ', 'Quinquagesimæ'][(d - dd(-63)).days // 7], 0, False
    if d < dd(-42): return 'cin', 'post Cineres', 0, False
    if d < dd(-14): return 'quad', 'Quadragesimæ', 1 + (d - dd(-42)).days // 7, False
    if d < dd(-3): return 'pass', ['in Passione', 'in Ramis Palmarum'][(d - dd(-14)).days // 7], 0, False
    if d < dd(7): return 'tri', None, 0, True
    if d < dd(39): return 'pasch', 'post Pascha', (d - dd(7)).days // 7, False
    if d < dd(68): return 'pent', None, 0, True
    sun1 = dd(70); return 'pt', 'post Octavam Trinitatis', 0 if d < sun1 else 1 + (d - sun1).days // 7, False
def title(d, s, wk, n):
    w = (d.weekday() + 1) % 7
    if s == 'adv': base = 'Hebdomadam %s Adventus' % ROM[n]; sun = 'Dominica %s Adventus' % ROM[n]
    elif s in ('pe', 'pt'): base = 'Hebdomadam %s %s' % (ROM[n], wk) if n else wk; sun = 'Dominica %s %s' % (ROM[n], wk)
    elif s == 'sept': sun = 'Dominica in ' + wk.replace('æ', 'a'); base = 'Hebdomadam ' + wk
    elif s == 'cin': return (FER[d.weekday()] if w else '') + ' post Cineres'
    elif s == 'quad': sun = 'Dominica %s in Quadragesima' % ROM[n]; base = 'Hebdomadam %s Quadragesimæ' % ROM[n]
    elif s == 'pass': sun = 'Dominica ' + wk; base = 'Hebdomadam ' + ('Passionis' if wk == 'in Passione' else 'Majorem')
    elif s == 'pasch': sun = 'Dominica in Albis' if n == 0 else 'Dominica %s post Octavam Paschæ' % ROM[n]; base = 'Hebdomadam %s post Octavam Paschæ' % ROM[n] if n else 'Hebdomadam in Albis'
    else: return ''
    if w == 0: return sun
    return '%s infra %s' % (FER[d.weekday()], base)

# ---------- the Hours ----------
LIB = {'mat_incipit': 'f6e9c602cd', 'incipit': '1cd0d177c3', 'conclusio': 'b1197cf6e2', 'compl_incipit': '36189bfff7', 'compl_lectio': '15ad8f25a1',
       'compl_conf': '0516270dcd', 'compl_deus': '35d01ad901', 'compl_oratio': '690c2baea0', 'compl_concl': 'e5045c9ece', 'compl_salve': '54ef816215',
       'pretiosa': '31b1e06fb7', 'pret2': '41aa67ac4c', 'regula': 'a92d9fb405'}
def lib_row(name, fix=None):
    la, en_ = L(LIB[name])
    if fix: la, en_ = fix(la, 'la'), fix(en_, 'en')
    return put(la, en_)
def laus(t, lang, s):
    """Laus tibi instead of Alleluia from Septuagesima to Holy Thursday"""
    if s in ('sept', 'cin', 'quad', 'pass'):
        return t.replace('<c>A</c>llelúia.', '<c>L</c>aus tibi, Dómine, Rex ætérnæ glóriæ.').replace('<c>A</c>lleluia.', '<c>P</c>raise be to thee, O Lord, King of eternal glory.')
    return t
BEN = {0: ['Benedictióne perpétua benedícat nos Pater ætérnus.', 'Unigénitus Dei Fílius nos benedícere et adjuváre dignétur.', 'Spíritus Sancti grátia illumináre dignétur sensus et corda nostra.'],
       1: ['Deus Pater omnípotens sit nobis propítius et clemens.', 'Ad gáudia paradísi perdúcat nos misericórdia Christi.', 'Ignem sui amóris accéndat Deus in córdibus nostris.'],
       2: ['Evangélica léctio sit nobis salus et protéctio.', 'Divínum auxílium máneat semper nobíscum.', 'Ad societátem cívium supernórum perdúcat nos Rex Angelórum.']}
BEN_EN = {0: ['May the everlasting Father bless us with an everlasting blessing.', 'May the only-begotten Son of God vouchsafe to bless and help us.', 'May the grace of the Holy Spirit vouchsafe to enlighten our senses and hearts.'],
          1: ['May God the Father almighty be gracious and merciful unto us.', 'May the mercy of Christ bring us to the joys of paradise.', 'May God kindle in our hearts the fire of his love.'],
          2: ['May the Gospel reading be our salvation and protection.', 'May the divine assistance remain with us always.', 'May the King of Angels bring us to the fellowship of the citizens of heaven.']}
ROMN = ['', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix']
def resp_block(r, lang, last):
    a, b, vs = r['a'], r['b'], r['v']
    if r.get('ferial') and len(vs) > 1: vs = vs[-1:]; b2 = None
    if lang == 'en': a, b, vs = ant_en(a), ant_en(b), [ant_en(v) for v in vs]
    out = ['<r>℟.</r> %s * %s' % (a, b)]
    rep = ' '.join(b.split()[:3]).rstrip(',:;') + '.'
    for v in vs:
        out.append('<r>℣.</r> %s %s' % (v, '' if nb(v)[-12:] in nb(a + b) else rep))
    if r.get('gloria') and not r.get('ferial'):
        out.append(('<r>℣.</r> Glória Patri, et Fílio, et Spirítui Sancto. ' if lang == 'la' else '<r>℣.</r> Glory be to the Father, and to the Son, and to the Holy Ghost. ') + rep)
    return '\n'.join(out)
def day_lessons(d):
    k = tkey(d)
    if k and k in LES: return LES[k]
    ok = okey(d)
    return OFF.get(ok, {}).get('lessons', []) if ok else []
def sunday_resp_source(d):
    """the Sunday whose responsories ('historia') serve the week: this week's Sunday, else the nearest earlier one that has them"""
    for back in range(0, 8):
        x = d - datetime.timedelta(days=(d.weekday() + 1) % 7 + 7 * back)
        ls = day_lessons(x)
        if sum(1 for y in ls if 'resp' in y) >= 6: return ls
        if season(x)[0] != season(d)[0]: break
    return []
_CL = {}
def cut_lesson(t):
    """a lesson ends before the responsory, the next lesson or the next Hour (the OCR parse can run on, e.g. the third lesson
    into its responsory and Lauds); OCR words repaired as in clean_prayer"""
    if t in _CL: return _CL[t]
    import latdict as LD
    k = t
    m = re.search(r'\s(?:Ante Laudes|Ad Laudes|Ad Matutinum|Capitulum\.|Hymnus\.|In I+\. Nocturno|Super Psalm|Invitatorium|Dicátur Cánticum|Psalmi(?:,| et| de| ut)|Lectio [ivxj]+\.|'
                  r'\S{1,3}\.?\s?(?:j|ij|iij|iv|v|vj|vij|viij|ix)\.\s+[A-Z])', t)
    if m and m.start() > 80: t = t[:m.start()].rstrip()
    out = []
    for x in t.split():
        y = LD.fix_word(x)
        if y == x: y = ocr_word(x, LD)
        if y is not None: out.append(y)
    t = ' '.join(out); t = re.sub(r'\s+([;:,.?!])', r'\1', t)
    _CL[k] = t
    return t
def lessons_rows(d, ls, noc, sunday):
    rows = [put('<n>Pater noster secreto.</n>', '<n>Our Father silently.</n>')]
    hom = any(x.get('homily_head') for x in ls)
    for i, x in enumerate(ls):
        bi = (x['n'] - 1) % 3; bset = 2 if (sunday and noc == 2) or (not sunday and hom) else (noc if sunday else 0)
        if bset == 2 and not hom: b_la, b_en = 'Ille nos benedícat, qui sine fine vivit et regnat.', 'May he bless us who liveth and reigneth without end.'
        else: b_la, b_en = BEN[bset][bi], BEN_EN[bset][bi]
        la = ['<h>Lectio %s</h>' % ROMN[x['n']], '<r>℣.</r> Jube, domne, benedícere.', '<r>Benedictio.</r> ' + b_la, '<r>℟.</r> Amen.']
        en_ = ['<h>Lesson %d</h>' % x['n'], '<r>℣.</r> Pray, sir, a blessing.', '<r>Blessing.</r> ' + b_en, '<r>℟.</r> Amen.']
        head = [h for h in x.get('head', []) if not h.startswith('Cap')]
        if head: la.append('<r>%s</r>' % ' '.join(head))
        if x.get('ref'): la.append('<r>%s</r>' % x['ref']); en_.append('<r>%s</r>' % x['ref'])
        if x.get('gospel'):
            la.append('<c>%s</c>%s' % (x['gospel'][0], x['gospel'][1:])); en_.append(ant_en(x['gospel']) if en(x['gospel']) else x['gospel'])
            la.append('<r>%s</r>' % x['homily_head']); en_.append('<r>%s</r>' % x['homily_head'])
        t = cut_lesson(x['la']); la.append('<c>%s</c>%s' % (t[0], t[1:])); en_.append(x.get('en') or t)
        if x.get('close') == 'haec' or (x.get('ref', '').startswith('Isa') and d.month == 12):
            la.append('Hæc dicit Dóminus Deus: Convertímini ad me, et salvi éritis.\n<r>℟.</r> Deo grátias.'); en_.append('Thus saith the Lord God: Be converted to me, and you shall be saved.\n<r>℟.</r> Thanks be to God.')
        else:
            la.append('Tu autem, Dómine, miserére nostri.\n<r>℟.</r> Deo grátias.'); en_.append('But thou, O Lord, have mercy on us.\n<r>℟.</r> Thanks be to God.')
        if x.get('resp'):
            la.append('\n<h>Responsorium %s</h>\n' % ROMN[x['n']] + resp_block(x['resp'], 'la', i == len(ls) - 1)); en_.append('\n<h>Responsory</h>\n' + resp_block(x['resp'], 'en', i == len(ls) - 1))
        rows.append(put('\n'.join(la), '\n'.join(en_)))
    return rows
def resp_text(r, lang):
    a, b, v = r; rep = b.split()[0].rstrip(',.:') + '.'
    if lang == 'la': return '<r>℟.</r> %s * %s\n<r>℣.</r> %s %s\n<r>℣.</r> Glória Patri, et Fílio, et Spirítui Sancto. %s\n\n' % (a, b, v, rep, rep)
    return '<r>℟.</r> %s * %s\n<r>℣.</r> %s\n\n' % (ant_en(a), ant_en(b), ant_en(v))
def week_oratio(d, s):
    if s != 'adv': return TP(d, 'oratio_week')
    return T['WEEK_OR'][str(season(d)[2])]
def six_before_vigil(d):
    if d.month != 12 or d.day < 17 or d.day > 23 or d.weekday() == 6: return False
    n = sum(1 for k in range(d.day + 1, 24) if datetime.date(d.year, 12, k).weekday() != 6)
    return n < 6
def chapter_hymn_row(cap, extra_head=('Capitulum Hymnus Versus', 'Chapter Hymn Verse'), resp=None):
    if not cap: return put('<h>Capitulum Hymnus Versus</h>\n' + PROPER['la'], '<h>Chapter Hymn Verse</h>\n' + PROPER['en'])
    ref, txt, hy, v, r = cap; hla, hen = hymn(hy)
    la = '<h>%s</h>\n<r>%s</r>\n<c>%s</c>%s\n<r>℟.</r> Deo grátias.\n\n%s<r>Hymnus</r>\n%s\n\n%s' % (extra_head[0], ref, txt[0], txt[1:], resp_text(resp, 'la') if resp else '', hla, VR([v, r], 'la'))
    e = en(txt); e = e if e else txt
    en_ = '<h>%s</h>\n<r>%s</r>\n<c>%s</c>%s\n<r>℟.</r> Thanks be to God.\n\n%s<r>Hymn</r>\n%s\n\n%s' % (extra_head[1], ref, e[0], e[1:], resp_text(resp, 'en') if resp else '', hen or hla, VR([v, r], 'en'))
    return put(la, en_)
def gospel_row(which, ant):
    num, h = (231, ('Canticum: Benedictus', 'Canticle: Benedictus')) if which == 'b' else (232, ('Canticum: Magnificat', 'Canticle: Magnificat')) if which == 'm' else (233, ('Canticum: Nunc dimittis', 'Canticle: Nunc dimittis'))
    return psalm_rows([[num]], [ant], head=h)[0]
def oratio_row(ferial_preces=False, text=None):
    la = '<h>Oratio</h>\n'; en_ = '<h>Prayer</h>\n'
    if ferial_preces:
        la += '<n>Preces feriales:</n>\n<c>K</c>ýrie, eléison. Christe, eléison. Kýrie, eléison.\n<n>Pater noster secreto.</n>\n<r>℣.</r> Et ne nos indúcas in tentatiónem.\n<r>℟.</r> Sed líbera nos a malo.\n'
        en_ += '<n>Ferial preces:</n>\n<c>L</c>ord, have mercy. Christ, have mercy. Lord, have mercy.\n<n>Our Father silently.</n>\n<r>℣.</r> And lead us not into temptation.\n<r>℟.</r> But deliver us from evil.\n'
    if text:
        la += '<r>℣.</r> Dóminus vobíscum.\n<r>℟.</r> Et cum spíritu tuo.\n<c>O</c>rémus.\n<c>%s</c>%s\n<r>℟.</r> Amen.' % (text[0], text[1:])
        e = en(text); en_ += '<r>℣.</r> The Lord be with you.\n<r>℟.</r> And with thy spirit.\n<c>L</c>et us pray.\n%s\n<r>℟.</r> Amen.' % (e or text)
        return put(la, en_)
    la += '<r>℣.</r> Dóminus vobíscum.\n<r>℟.</r> Et cum spíritu tuo.\n<c>O</c>rémus.\n' + PROPER['la']
    en_ += '<r>℣.</r> The Lord be with you.\n<r>℟.</r> And with thy spirit.\n<c>L</c>et us pray.\n' + PROPER['en']
    return put(la, en_)
def memoria_row(hour, s):
    rows = []
    if s == 'pasch':
        m = P['MEM_CRUCIS']; a = m[hour][0]
        rows.append(put('<h>Memoria de Cruce</h>\n<r>Ant.</r> %s\n%s\n<c>O</c>rémus.\n<c>%s</c>%s' % (a, VR(m['v'], 'la'), m['oratio'][0], m['oratio'][1:]),
                        '<h>Commemoration of the Cross</h>\n<r>Ant.</r> %s\n%s\n<c>L</c>et us pray.\n%s' % (ant_en(a), VR(m['v'], 'en'), ant_en(m['oratio']))))
    m = P['MEM_BVM']; a, v, r = m[hour]
    rows.append(put('<h>Memoria de Beata Maria</h>\n<r>Ant.</r> %s%s\n%s\n<c>O</c>rémus.\n<c>%s</c>%s' % (a, ' Allelúja.' if s == 'pasch' else '', VR([v, r], 'la'), m['oratio'][0], m['oratio'][1:]),
                    '<h>Commemoration of Our Lady</h>\n<r>Ant.</r> %s\n%s\n<c>L</c>et us pray.\n%s' % (ant_en(a), VR([v, r], 'en'), ant_en(m['oratio']))))
    return rows
def sv(dct, s, default=None):
    """seasonal value: s, or the per-annum group"""
    if s in dct: return dct[s]
    if s in ('pe', 'sept', 'pt', 'cin') and 'pa' in dct: return dct['pa']
    if s == 'cin' and 'sept' in dct: return dct['sept']
    if s in ('sept', 'cin') and 'pe' in dct: return dct['pe']
    return default
def matins(d, s, w):
    rows = [put('<h>Ante Matutinum</h>\n<n>Pater noster et Credo in Deum secreto.</n>', '<h>Before Matins</h>\n<n>Our Father and the Apostles\' Creed silently.</n>'),
            lib_row('mat_incipit', lambda t, l: laus(t, l, s))]
    inv = TP(d, 'invit') or (P['INVIT'][str(w)] if s in ('pe', 'sept', 'pt') else None)
    rows.append(invit_row(inv, w))
    hy = sv(P['HYMN_MAT'], s)
    rows.append(put('<h>Hymnus</h>\n' + (hymn(hy)[0] if hy else PROPER['la']), '<h>Hymn</h>\n' + ((hymn(hy)[1] or hymn(hy)[0]) if hy else PROPER['en'])))
    if w == 0:
        for ni, noc in enumerate(P['SUN_MAT']):
            a = noc['ant'].get('pt' if s == 'pt' else 'pe' if s in ('pe', 'sept', 'cin', 'quad') else s)
            head = ('In %s Nocturno' % ['I', 'II', 'III'][ni], '%s Nocturn' % ['First', 'Second', 'Third'][ni])
            if s == 'pasch': a = None
            if a and len(a) == 1: rows += psalm_rows(noc['groups'], None, head, single=a[0])
            else: rows += psalm_rows(noc['groups'], a or [None] * len(noc['groups']), head)
            v = sv(noc['v'], s) if s != 'cin' else noc['v']['pa']
            rows.append(vr_row(v) if v else put(PROPER['la'], PROPER['en']))
            ls = day_lessons(d)
            if ls: rows += lessons_rows(d, [x for x in ls if 3 * ni < x['n'] <= 3 * ni + 3], ni, True)
            else: rows.append(note_row('Lectiones et Responsoria de Proprio de Tempore (in præparatione).', 'Lessons and responsories from the Proper of Time (in preparation).'))
        if s not in ('adv', 'sept', 'cin', 'quad', 'pass'):
            rows.append(put('<h>Te Deum</h>\n<r>%s</r>\n%s' % (pstitle(0, 'la') if False else 'Canticum SS. Ambrosii et Augustini', TEDEUM[0]), '<h>Te Deum</h>\n%s' % TEDEUM[1]))
    else:
        groups, ants, v = P['FER_MAT'][str(w)]
        ok = s in ('pe', 'sept', 'cin', 'quad', 'pass', 'pt', 'adv')
        rows += psalm_rows(groups, ants if ok else [None] * 6, ('In Nocturno', 'Nocturn'))
        if s in P['FER_MAT_V']: v = P['FER_MAT_V'][s][(w - 1) % 3]
        rows.append(vr_row(v) if ok else put(PROPER['la'], PROPER['en']))
        ls = day_lessons(d)
        if ls:
            sun = sunday_resp_source(d)
            if not any('resp' in x for x in ls) and sun:      # 'Responsoria Historiæ Dominicalis … secundum ordinem Nocturnorum'
                noc = {1: 0, 4: 0, 2: 1, 5: 1, 3: 2, 6: 2}[w]
                ls = [dict(x, resp=dict(sun[3 * noc + i]['resp'], ferial=(noc == 0 and i == 0))) if 3 * noc + i < len(sun) and 'resp' in sun[3 * noc + i] else x for i, x in enumerate(ls)]
            rows += lessons_rows(d, ls, 0, False)
        else: rows.append(note_row('Tres Lectiones cum Responsoriis de Proprio de Tempore (in præparatione).', 'Three lessons with responsories from the Proper of Time (in preparation).'))
    return rows
def invit_row(ant, w):
    if not ant: return put('<h>Invitatorium</h>\n' + PROPER['la'], '<h>Invitatory</h>\n' + PROPER['en'])
    full = ant; half = ant.split('* ')[-1]
    first = {0: 'Præoccupémus fáciem ejus in confessióne, et in psalmis jubilémus ei.', 1: 'Jubilémus Deo salutári nostro: præoccupémus fáciem ejus in confessióne, et in psalmis jubilémus ei.',
             2: 'Præoccupémus fáciem ejus in confessióne, et in psalmis jubilémus ei.'}.get(w, 'Veníte, exsultémus Dómino, jubilémus Deo salutári nostro: præoccupémus fáciem ejus in confessióne, et in psalmis jubilémus ei.')
    vs = [first, 'Quóniam Deus magnus Dóminus, et Rex magnus super omnes deos: quóniam non repéllet Dóminus plebem suam: quia in manu ejus sunt omnes fines terræ, et altitúdines móntium ipse cónspicit.',
          'Quóniam ipsíus est mare, et ipse fecit illud, et áridam fundavérunt manus ejus: <n>(genuflectitur)</n> veníte, adorémus, et procidámus ante Deum: plorémus coram Dómino, qui fecit nos: quia ipse est Dóminus Deus noster: nos autem pópulus ejus, et oves páscuæ ejus.',
          'Hódie, si vocem ejus audiéritis, nolíte obduráre corda vestra, sicut in exacerbatióne secúndum diem tentatiónis in desérto: ubi tentavérunt me patres vestri, probavérunt, et vidérunt ópera mea.',
          'Quadragínta annis próximus fui generatióni huic, et dixi: Semper hi errant corde: ipsi vero non cognovérunt vias meas: quibus jurávi in ira mea: Si introíbunt in réquiem meam.']
    out = ['<h>Invitatorium</h>', '<r>Ant.</r> ' + full]
    for i, v in enumerate(vs):
        out += ['<r>℣.</r> ' + v, '<r>Ant.</r> ' + (full if i % 2 == 0 else half)]
    out += [GP['la'].split('\n')[0] + ' ' + GP['la'].split('\n')[1].replace('<r>℟.</r> ', ''), '<r>Ant.</r> ' + half, '<r>Ant.</r> ' + full]
    la = '\n'.join(out).replace('<r>Ant.</r> ' + full + '\n<r>℣.</r> ' + vs[0], '<n>Quo dicto, séquitur:</n>\n<r>℣.</r> ' + vs[0], 1)
    e = ant_en(full)
    en_ = '<h>Invitatory</h>\n<r>Ant.</r> %s\n<n>Psalm 94 (Venite), the antiphon repeated after each verse, whole or in part, as in the Latin.</n>' % e
    return put(la, en_)
def lauds(d, s, w):
    va = P['V_ANTE_LAUDES']; v = va.get(s) or (va['sun_pa'] if w == 0 else va['fer_pa'])
    if s in ('sept', 'cin') and w == 0: v = va['sun_pa']
    inc_la, inc_en = L(LIB['incipit'])
    rows = [put(laus(inc_la.replace('<h>Incipit</h>\n', '<h>Incipit</h>\n' + VR(v, 'la') + '\n'), 'la', s), laus(inc_en.replace('<h>Start</h>\n', '<h>Start</h>\n' + VR(v, 'en') + '\n'), 'en', s))]
    if w == 0:
        groups = P['LAUDS_SUN_SEPT'] if s in ('sept', 'quad', 'pass') else P['LAUDS_SUN']
        a = P['LAUDS_SUN_ANT'].get(s); la5 = TP(d, 'laudes')
        rows += psalm_rows(groups, la5, single=None) if la5 else psalm_rows(groups, None if a else [None] * 5, single=a)
        cap = sv(P['CAP']['laud_sun'], s)
    else:
        groups, ants = P['LAUDS_FER'][str(w)]
        if six_before_vigil(d): ants = T['SIX'][str(w)]
        if s == 'pasch': groups = P['LAUDS_SUN']; rows += psalm_rows(groups, None, single='Allelúja, allelúja.')
        else: rows += psalm_rows(groups, ants)
        cap = sv(P['CAP']['laud_fer'], s)
    rows.append(chapter_hymn_row(cap))
    b = TP(d, 'bened') or (P['BENED_FER'].get(str(w)) if w and s in ('pe', 'pt') else None)
    rows.append(gospel_row('b', b))
    rows.append(oratio_row(ferial_preces=bool(w) and s != 'pasch', text=TP(d, 'oratio_laudes') or week_oratio(d, s)))
    if w == 0 and s in ('pe', 'pt', 'sept', 'pasch'): rows += memoria_row('Laudes', s)
    elif w and s == 'pasch': rows += memoria_row('Laudes', s)[:1]
    rows.append(lib_row('conclusio'))
    return rows
def little(d, s, w, hour):
    rows = [lib_row('incipit', lambda t, l: laus(t, l, s))]
    hla, hen = hymn(P['HOUR_HYMN'][hour]); rows.append(put('<h>Hymnus</h>\n' + hla, '<h>Hymn</h>\n' + (hen or hla)))
    sa = sv(P['HOUR_ANT'][hour], s) if s != 'cin' else P['HOUR_ANT'][hour]['pe']
    a = sa[0 if w == 0 else 1] if sa else None
    la5 = TP(d, 'laudes') if w == 0 else None
    if la5: a = la5[{'Prima': 0, 'Tertia': 1, 'Sexta': 2, 'Nona': 4}[hour]]
    if hour == 'Prima':
        groups = P['PRIME_PS_SUN_SEPT'] if (w == 0 and s in ('sept', 'quad', 'pass')) else P['PRIME_PS']
        if w == 0 and s not in ('sept', 'quad', 'pass'): groups = groups + [[234]]
        if w == 0 and s in ('sept', 'quad', 'pass'): groups = groups + [[234]]
    else: groups = P['HOUR_PS'][hour]
    rows += psalm_rows(groups, None, single=a) if a else psalm_rows(groups, [None] + [False] * (len(groups) - 1))
    if hour == 'Prima':
        sun_cap = w == 0 or s == 'pasch'
        cap = ('1 Tim 1', 'Regi sæculórum immortáli et invisíbili, soli Deo honor et glória in sǽcula sæculórum. Amen.') if sun_cap else ('Zach 8', 'Pacem et veritátem dilígite, ait Dóminus omnípotens.')
        js = s not in ('pass',)
        la = '<h>Capitulum Responsorium Versus</h>\n<r>%s</r>\n<c>%s</c>%s\n<r>℟.</r> Deo grátias.\n\n' % (cap[0], cap[1][0], cap[1][1:])
        if js: la += '<r>℟.br.</r> Jesu Christe, Fili Dei vivi, * Miserére nobis. Jesu Christe.\n<r>℣.</r> %s Miserére nobis.\n<r>℣.</r> Glória Patri, et Fílio, et Spirítui Sancto. Jesu Christe.\n\n' % ('Qui ventúrus es in mundum.' if s == 'adv' else 'Qui sedes ad déxteram Patris.')
        la += '<r>℣.</r> Exsúrge, Dómine, ádjuva nos.\n<r>℟.</r> Et líbera nos propter nomen tuum.'
        e1 = en(cap[1]) or cap[1]
        en_ = '<h>Chapter Responsory Verse</h>\n<r>%s</r>\n%s\n<r>℟.</r> Thanks be to God.\n\n' % (cap[0], e1)
        if js: en_ += '<r>℟.br.</r> Jesus Christ, Son of the living God, * Have mercy on us. Jesus Christ.\n<r>℣.</r> Who sittest at the right hand of the Father. Have mercy on us.\n<r>℣.</r> Glory be to the Father, and to the Son, and to the Holy Ghost. Jesus Christ.\n\n'
        en_ += '<r>℣.</r> Arise, O Lord, help us.\n<r>℟.</r> And deliver us for thy name\'s sake.'
        rows.append(put(la, en_))
        rows.append(lib_row('compl_conf', lambda t, l: re.sub(r'\n<r>℣.</r> Convérte nos[\s\S]*$|\n<r>℣.</r> Turn us[\s\S]*$', '', t).replace('<r>℣.</r> Adjutórium nostrum in nómine Dómini.\n<r>℟.</r> Qui fecit cælum et terram.\n', '').replace('<r>℣.</r> Our help is in the name of the Lord.\n<r>℟.</r> Who made heaven and earth.\n', '')))
        orat = ('In hac hora hujus diéi tua nos, Dómine, reple misericórdia: ut per totum diem exsultántes in tuis láudibus júgiter delectémur. Per Dóminum nostrum.') if sun_cap else \
               ('Dómine Deus omnípotens, qui ad princípium hujus diéi nos perveníre fecísti, tua nos hódie salva virtúte: ut in hac die ad nullum declinémus peccátum, sed semper ad tuam justítiam faciéndam nostra procédant elóquia, dirigántur cogitatiónes et ópera. Per Dóminum nostrum.')
        rows.append(put('<h>Oratio</h>\n<r>℣.</r> Dóminus vobíscum.\n<r>℟.</r> Et cum spíritu tuo.\n<c>O</c>rémus.\n<c>%s</c>%s\n<r>℟.</r> Amen.\n<r>℣.</r> Dóminus vobíscum.\n<r>℟.</r> Et cum spíritu tuo.\n<r>℣.</r> Benedicámus Dómino.\n<r>℟.</r> Deo grátias.' % (orat[0], orat[1:]),
                        '<h>Prayer</h>\n<r>℣.</r> The Lord be with you.\n<r>℟.</r> And with thy spirit.\n<c>L</c>et us pray.\n%s\n<r>℟.</r> Amen.\n<r>℣.</r> The Lord be with you.\n<r>℟.</r> And with thy spirit.\n<r>℣.</r> Let us bless the Lord.\n<r>℟.</r> Thanks be to God.' % (en(orat) or orat)))
        rows.append(put('<h>Ad Pretiosa</h>\n<n>Finítis quæ de Martyrologio pronuntiánda sunt (in præparatione), et respónso Deo grátias, dicitur:</n>', '<h>Pretiosa</h>\n<n>After the Martyrology (in preparation) and the answer Thanks be to God:</n>'))
        rows += [lib_row('pretiosa'), lib_row('pret2'), lib_row('regula')]
        return rows
    hc = P['HOUR_CAP'][hour]; c = hc.get(s) or (hc['sun_pa'] if w == 0 else hc['fer_pa'])
    if s == 'cin': c = hc['fer_pa'] if w else hc['sun_pa']
    ref, txt = c[0], c[1]; e = en(txt) or txt
    la = '<h>Capitulum Responsorium Versus</h>\n<r>%s</r>\n<c>%s</c>%s\n<r>℟.</r> Deo grátias.\n\n' % (ref, txt[0], txt[1:]); en_ = '<h>Chapter Responsory Verse</h>\n<r>%s</r>\n%s\n<r>℟.</r> Thanks be to God.\n\n' % (ref, e)
    if c[2] is None:
        la += PROPER['la'].replace('De Proprio de Tempore', 'Responsorium breve et Versus de Dominica'); en_ += PROPER['en']
    else:
        r1, r2, rv, v, r = c[2:]; inc = r1.split()[0].rstrip(',:')
        gl = '' if s == 'pass' else '\n<r>℣.</r> Glória Patri, et Fílio, et Spirítui Sancto. %s' % r1.rstrip(',:')
        la += '<r>℟.br.</r> %s * %s %s\n<r>℣.</r> %s %s%s\n\n%s' % (r1, r2, r1.rstrip(',:') if s != 'pass' else inc + '.', rv, r2.split()[0].rstrip(',.:') + '.', gl, VR([v, r], 'la'))
        en_ += '<r>℟.br.</r> %s * %s\n<r>℣.</r> %s\n\n%s' % (ant_en(r1 + ' ' + r2), '', ant_en(rv), VR([v, r], 'en'))
    rows.append(put(la, en_))
    rows.append(oratio_row(ferial_preces=bool(w) and s != 'pasch', text=week_oratio(d, s)))
    rows.append(lib_row('conclusio'))
    return rows
def vespers(d, s, w):
    if tkey(d) == 'pre-adv': s = 'adv'
    rows = [lib_row('incipit', lambda t, l: laus(t, l, s))]
    groups, ants = P['VESP'][str(w)]
    if s == 'pasch': rows += psalm_rows(groups, None, single=P['VESP_PASCH_ANT'].get(str(w), P['VESP_PASCH_ANT']['fer']))
    elif w == 0 and s not in ('pe', 'sept', 'pt', 'quad', 'pass', 'cin', 'adv'): rows += psalm_rows(groups, [None] * 5)
    else: rows += psalm_rows(groups, ants)
    key = 'vesp_sun' if w == 0 else 'vesp_sat' if w == 6 else 'vesp_fer'
    rows.append(chapter_hymn_row(sv(P['CAP'][key], s), resp=TP(d, 'vesp_r')))
    m = TP(d, 'magn')
    if s == 'adv' and d.month == 12 and d.day >= 17: m = T['OANT'][str(d.day)]
    if s in ('pe', 'pt') and 1 <= w <= 5 and not m: m = P['MAGN_FER'][str(w)]
    if s == 'pe' and w == 6: m = P['MAGN_SAT_PE']
    rows.append(gospel_row('m', m))
    rows.append(oratio_row(ferial_preces=1 <= w <= 5 and s not in ('pasch',) and not (s == 'adv' and d.month == 12 and d.day >= 17),
                           text=TP(d, 'oratio_vesp') or (week_oratio(d, s) if w != 6 else None)))
    if w == 0 and s in ('pe', 'pt', 'sept', 'pasch'): rows += memoria_row('Vespera', s)
    elif s == 'pasch': rows += memoria_row('Vespera', s)[:1]
    rows.append(lib_row('conclusio'))
    return rows
def compline(d, s, w):
    E = easter(d.year)
    rows = [lib_row('compl_incipit'), lib_row('compl_lectio'), lib_row('compl_conf'), lib_row('compl_deus', lambda t, l: laus(t, l, s))]
    C = P['COMPL']
    rows += psalm_rows(C['ps'], None, single=C['ant']['pasch'] if s == 'pasch' else C['ant']['pa'])
    inpace = w in (0, 6) and s not in ('pass',)
    la = '<h>Capitulum</h>\n<r>Jer 14</r>\n<c>T</c>u in nobis es, Dómine, et nomen sanctum tuum invocátum est super nos: ne derelínquas nos, Dómine Deus noster.\n<r>℟.</r> Deo grátias.\n\n<h>Responsorium</h>\n'
    en_ = '<h>Chapter</h>\n<r>Jer 14</r>\n<c>T</c>hou, O Lord, art among us, and thy holy name is called upon by us: forsake us not, O Lord our God.\n<r>℟.</r> Thanks be to God.\n\n<h>Responsory</h>\n'
    if inpace:
        la += '<r>℟.br.</r> In pace in idípsum * Dórmiam et requiéscam.\n<r>℣.</r> Si dédero somnum óculis meis, et pálpebris meis dormitatiónem. Dórmiam.\n<r>℣.</r> Glória Patri, et Fílio, et Spirítui Sancto. In pace.'
        en_ += '<r>℟.br.</r> In peace, in the selfsame, * I will sleep and I will rest.\n<r>℣.</r> If I shall give sleep to my eyes, or slumber to my eyelids. I will sleep.\n<r>℣.</r> Glory be to the Father, and to the Son, and to the Holy Ghost. In peace.'
    else:
        al = ' Allelúja, allelúja.' if s == 'pasch' else ''
        la += '<r>℟.br.</r> In manus tuas, Dómine, * Comméndo spíritum meum.%s\n<r>℣.</r> Redemísti me, Dómine, Deus veritátis. Comméndo.%s' % (al, '' if s == 'pass' else '\n<r>℣.</r> Glória Patri, et Fílio, et Spirítui Sancto. In manus.')
        en_ += '<r>℟.br.</r> Into thy hands, O Lord, * I commend my spirit.\n<r>℣.</r> Thou hast redeemed us, O Lord, God of truth. I commend.' + ('' if s == 'pass' else '\n<r>℣.</r> Glory be to the Father, and to the Son, and to the Holy Ghost. Into thy hands.')
    rows.append(put(la, en_))
    hy = C['hymn'].get(s, C['hymn']['pa']) if not (s == 'cin' and d.weekday() != 5) else C['hymn']['pa']
    if s == 'cin' and d.weekday() == 5: hy = C['hymn']['quad']
    hla, hen = hymn(hy); al = ', allelúja' if s == 'pasch' else ''
    rows.append(put('<h>Hymnus</h>\n%s\n\n<r>℣.</r> Custódi nos, Dómine, ut pupíllam óculi%s.\n<r>℟.</r> Sub umbra alárum tuárum prótege nos%s.' % (hla, al, al),
                    '<h>Hymn</h>\n%s\n\n<r>℣.</r> Keep us, O Lord, as the apple of thine eye.\n<r>℟.</r> Protect us under the shadow of thy wings.' % (hen or hla)))
    n = C['nunc']['pa']
    if s in ('quad',) or (s == 'cin' and d.weekday() == 5):
        n = C['nunc']['quad1'] if d < E - datetime.timedelta(days=29) else 'Média vita in morte sumus: quem quǽrimus adjutórem, nisi te, Dómine? qui pro peccátis nostris juste irascéris. Sancte Deus, Sancte fortis, Sancte et miséricors Salvátor, amáræ morti ne tradas nos.'
    if s == 'pass': n = C['nunc']['pass']
    if s == 'pasch': n = C['nunc']['pasch']
    rows.append(gospel_row('n', n))
    prec = False
    rows += [lib_row('compl_oratio'), lib_row('compl_concl'), lib_row('compl_salve')]
    return rows
def proper_day(d):
    r = note_row('Officium hujus diéi totum próprium est (Proprium de Tempore): in præparatione.', 'The Office of this day is entirely proper (Proper of Time): in preparation.')
    return {h: [r] for h in ('Matutinum', 'Laudes', 'Prima', 'Tertia', 'Sexta', 'Nona', 'Vespera', 'Completorium')}

def hard_proper(d):
    """days whose proper Office excludes every feast: Christmas to the Epiphany octave, Holy Thursday to Low Saturday,
    Ascension Day, Pentecost and its octave, Corpus Christi"""
    s = season(d)[0]
    if s in ('nat', 'tri'): return True
    if s == 'pent':
        k = (d - easter(d.year)).days
        return k == 39 or 49 <= k <= 56 or k == 60
    return False
ECAL = {}
def effective_calendar():
    """the calendar entries of each date, with impeded Duplex and Totum Duplex feasts transferred to the next free day
    (Rubricae generales: translatio); a transferred feast is marked '(translatum)'"""
    d = FROM - datetime.timedelta(days=40); pending = []
    while d <= TO + datetime.timedelta(days=1):
        s, wk, n, prop = season(d); w = (d.weekday() + 1) % 7
        ents = [dict(c) for c in CAL.get(d.strftime('%m-%d'), [])]
        main_ = ents[0] if ents else None
        if main_ and RV.get(main_['rank'] or '', 0) >= 3 and main_['rank'] != 'Solemnis' and s not in ('nat',) and (hard_proper(d) or (not prop and not celebrable(d, s, w, RV[main_['rank']]))):
            pending.append(dict(main_, title=main_['title'] + ' (translatum)')); ents = ents[1:]
            ents.append(dict(main_, rank='Memoria'))
        free = not hard_proper(d) and (not ents or RV.get(ents[0]['rank'] or '', 0) < 3)
        if pending and free and (prop or celebrable(d, s, w, 3)):
            pending.sort(key=lambda c: (-RV.get(c['rank'] or '', 0), 0 if re.search(r'Dómini|B\. M', c['title']) else 1)); ents.insert(0, pending.pop(0))
        if d >= FROM: ECAL[d] = ents
        d += datetime.timedelta(days=1)

# ---------- 1909 Commune Sanctorum -> whole feast Offices ----------
import commons1909 as CM
import names1909 as NM
LP = [[112], [116], [145], [146], [147]]          # 'Laudate pueri cum ceteris' (In Totis Duplicibus ad I. Vesperas, psalter p. 230)
CLES = json.load(open(os.path.join(HERE, 'commonlessons1909.json'))) if os.path.exists(os.path.join(HERE, 'commonlessons1909.json')) else {}
RUNHEAD = re.compile(r'\s(?:(?:Commúne|Commune|Apostolórum|Mártyr(?:is|um)|Confessór(?:is|um)|Pontíf(?:icis|icum)|Vírgin(?:is|um)|Doctóris|Abbátis)\s?){1,4}\.\s(?=[a-zæœáéíóúý])')
RUNHEAD2 = re.compile(r'(?<=[.:;!?])\s(?:(?:Commúne|Commune|Apostolórum|Mártyr(?:is|um)|Confessór(?:is|um)|Pontíf(?:icis|icum)|Vírgin(?:is|um)|Doctóris|Abbátis)\s?){2,4}\.(?=\s[A-Z])')
def unhead(t):
    """drop a page's running head (e.g. 'Mártyris Pontíficis.') that the OCR left inside a lesson"""
    if not isinstance(t, str): return t
    t = RUNHEAD.sub(' ', t)
    return RUNHEAD2.sub(' ', t)
for _ls in CLES.values():
    for _x in _ls: _x['la'] = unhead(_x.get('la'))
AI = ' [AI translation]'
def cmerge(a, b):
    out = dict(a)
    for k, v in b.items():
        if k in ('base', 'overlay'): continue
        if v == 'by_noct': out[k + '_by_noct'] = True; continue
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            m = dict(out[k])
            for kk, vv in v.items():
                if vv == 'by_noct': m[kk + '_by_noct'] = True
                else: m[kk] = vv
            out[k] = m
        else: out[k] = v
    return out
def cres(cn):
    c = CM.C[cn]
    return cmerge(cres(c['base']), c) if c.get('base') else cmerge({}, c)
def common_full(cn, tp):
    F = cres(cn); F['_cn'] = cn
    if tp and cn in CM.TP_OF:
        F = cmerge(F, cres(CM.TP_OF[cn])); F['_tp'] = True
    return F
def lesson_chain(cn):
    out, c = [], cn
    while c:
        out.append(c); c = CM.C[c].get('base')
    return out
def common_of(t):
    if re.search(r'Vigíl|Anniversár|Defunct', t): return None
    if re.search(r'Dedicát|Dedicat', t): return 'ded'
    if re.search(r'Sponsi|Patris B', t): return 'conf'
    if re.search(r'Matris B', t): return 'nec'
    if re.search(r'B\. ?Maríæ|B\. ?M\. ?V|Maríæ Virg|Maríæ ad Nives|Deíparæ|Rosárii|Lauretán', t): return 'bvm'
    if re.search(r'Dómini|Nóminis Jesu|Jesu Christi|Crucis|Trinit|Ómnium|Archáng|Angelórum|Michaél|Baptíst|Relíqui|S\. P\. N\. Domínici|Epiph|Sacrament|Cordis|Sepult', t): return None
    if re.search(r'Stigmatum S\. Francísci', t): return 'conf'
    if re.search(r'Catharínæ', t) and re.search(r'Stigmat', t): return 'virg'
    if re.search(r'Cáthedra|ante Portam', t): return 'apost'
    if re.search(r'Maríæ Magdal', t): return 'nec'
    if re.search(r'Apóst|Apostol', t): return 'apost'
    if re.search(r'Evang', t): return 'evang'
    if re.search(r'\bMM\.|Mártyrum|Sociórum|Sóciis', t): return 'mm'
    if re.search(r'V(?:irg)?\. et M(?:art)?\.|feminárum Protomárt', t): return 'virg_mart'
    if re.search(r'\bVirg\.|\bV\. O\.P|Vírginum', t): return 'virg'
    if re.search(r'Mart\.|Mártyris', t) and re.search(r'\bEp\.|Papæ|Pont', t): return 'mart_pont'
    if re.search(r'Mart\.|Protomárt|Mártyris', t): return 'mart'
    if re.search(r'Doct', t): return 'doct'
    if re.search(r'Abb', t): return 'abb'
    if re.search(r'Conf\.', t) and re.search(r'\bEp\.|Papæ|Pont', t): return 'conf_pont'
    if re.search(r'Conf\.|Confessórum|Regis', t): return 'conf'
    if re.search(r'Vid\.|Víduæ|Pœnit|Reg[íi]næ', t): return 'nec'
    return None
def feast_common(d, t):
    """the Common of a calendar entry; an octave day takes the Common of its feast"""
    m = re.match(r'(?:Dies )?Octava (.+)$', t)
    if m:
        key = nb(m.group(1))[:12]
        for back in range(7, 9):
            for c in CAL.get((d - datetime.timedelta(days=back)).strftime('%m-%d'), []):
                if key and key[:10] in nb(c['title']): return common_of(c['title'])
        return None
    return common_of(t)
def alla(t):
    if not t or 'allelúja' in t.lower(): return t
    return re.sub(r'[\s.:;,!?]*$', '', t) + ', allelúja.'
def tp_of(d):
    k = (d - easter(d.year)).days; return 0 <= k <= 55
# hymns: every hymn of the 1954 library, matched on its whole incipit (several hymns share 18 letters)
HYALL = []
for k, v in lib.items():
    if k not in pair: continue
    for m in re.finditer(r'(?:<r>Hymnus</r>|<h>Hymnus</h>)\n(?:<n>[^\n]*</n>\n)?((?:<c>.</c>)[\s\S]*?Amen\.)', v):
        la = m.group(1); e = hymn_body(lib[pair[k]]); HYALL.append((nb(re.sub(r'<[^>]+>', '', la)), la, e or la))
def stanza(lines): return '<h>%s</h>%s' % (lines[0][0], '\n'.join([lines[0][1:]] + lines[1:]))
TP_LA = {'resurr': [['Quǽsumus, Auctor ómnium,', 'In hoc Paschali gáudio,', 'Ab omni mortis ímpetu', 'Tuum defénde pópulum.'],
                    ['Glória tibi, Dómine,', 'Qui surrexísti a mórtuis,', 'Cum Patre et Sancto Spíritu,', 'In sempitérna sǽcula.', 'Amen.']],
         'ascens': [['Tu esto nostrum gáudium,', 'Qui es futúrus prǽmium:', 'Sit nostra in te glória', 'Per cuncta semper sǽcula.'],
                    ['Glória tibi, Dómine,', 'Qui scandis supra sídera,', 'Cum Patre et Sancto Spíritu,', 'In sempitérna sǽcula.', 'Amen.']],
         'bvm': [['María Mater grátiæ,', 'Mater misericórdiæ,', 'Tu nos ab hoste prótege,', 'Et hora mortis súscipe.'],
                 ['Glória tibi, Dómine,', 'Qui natus es de Vírgine,', 'Cum Patre et Sancto Spíritu,', 'In sempitérna sǽcula.', 'Amen.']]}
TP_EN = {'resurr': [['Paschal triumph, paschal joy,', 'Only sin can this destroy;', 'From the death of sin set free,', 'Souls re-born, dear Lord, in Thee.'],
                    ['Hymns of glory, songs of praise,', 'Father, unto thee we raise;', 'Risen Lord, all praise to thee,', 'Ever with the Spirit be.', 'Amen.']],
         'ascens': [['Be thou our joy, who art to be our reward:', 'may our glory be in thee', 'through all the ages for ever.' + AI],
                    ['Glory be to thee, O Lord,', 'who mountest above the stars,', 'with the Father and the Holy Spirit,', 'for everlasting ages.' + AI, 'Amen.']],
         'bvm': [['Mary, Mother of grace,', 'Mother of mercy,', 'shield us from the enemy', 'and receive us at the hour of death.' + AI],
                 ['Glory be to thee, O Lord,', 'who wast born of the Virgin,', 'with the Father and the Holy Spirit,', 'for everlasting ages.' + AI, 'Amen.']]}
def swap_doxology(t, which, lang):
    """replace the hymn's last stanza (its doxology) by the Paschal / Marian stanzas"""
    st = t.rstrip().split('\n\n')
    if len(st) < 3: return t
    new = [stanza(s) for s in (TP_LA if lang == 'la' else TP_EN)[which]]
    have = {nb(re.sub(r'<[^>]+>', '', x))[:30] for x in st[:-1]}
    new = [x for x in new if nb(re.sub(r'<[^>]+>', '', x))[:30] not in have]   # a hymn that already has 'María Mater grátiæ'
    return '\n\n'.join(st[:-1] + new)
FIXHY = set()
def hymn9(spec, d=None, dox=None):
    """a 1909 hymn: spec = incipit or (incipit, word the right variant contains); dox = 'tp' | 'bvm' | None"""
    inc, must = (spec if isinstance(spec, tuple) else (spec, None))
    if inc in CM.HYMN_TEXT: la, e = CM.HYMN_TEXT[inc]
    if inc in FIXHY: return la, e    # printed in the feast itself, doxology included
    if inc in CM.HYMN_TEXT: pass
    else:
        q = nb(inc); c = [(la, e) for n, la, e in HYALL if n.startswith(q[:36])]
        if must: c = [x for x in c if nb(must) in nb(x[0])] or c
        la, e = c[0] if c else hymn(inc)
    if dox == 'tp' and d is not None:
        k = (d - easter(d.year)).days; which = 'ascens' if 39 <= k <= 48 else 'resurr'
        la, e = swap_doxology(la, which, 'la'), swap_doxology(e, which, 'en')
    elif dox == 'bvm': la, e = swap_doxology(la, 'bvm', 'la'), swap_doxology(e, 'bvm', 'en')
    return la, e
def resp9(r, lang):
    """Matins responsory (a, b, [verses], gloria); gloria: False | True | (repeat after verse, repeat after Gloria)"""
    a, b, vs, g = r
    rep_v = rep_g = None
    if isinstance(g, tuple): rep_v, rep_g = g
    dflt = ' '.join(b.split()[:3]).rstrip(',:;.') + '.'
    rep_v = rep_v or dflt; rep_g = rep_g or rep_v
    if lang == 'en': a, b, vs = ant_en(a), ant_en(b), [ant_en(v) for v in vs]
    out = ['<r>℟.</r> %s * %s' % (a, b)]
    for v in vs: out.append('<r>℣.</r> %s %s' % (v, rep_v if lang == 'la' else ''))
    if g and not (isinstance(g, tuple) and g[1] is False): out.append(('<r>℣.</r> Glória Patri, et Fílio, et Spirítui Sancto. %s' % rep_g) if lang == 'la' else '<r>℣.</r> Glory be to the Father, and to the Son, and to the Holy Ghost.')
    return '\n'.join(x.rstrip() for x in out)
def v1resp(r, lang):
    """the Responsory of I Vespers: (a, b, verse, repeat after verse, repeat after Gloria)"""
    a, b, v, rv, rg = r
    if lang == 'la': return '<r>℟.</r> %s * %s\n<r>℣.</r> %s %s\n<r>℣.</r> Glória Patri, et Fílio, et Spirítui Sancto. %s\n\n' % (a, b, v, rv, rg)
    return '<r>℟.</r> %s * %s\n<r>℣.</r> %s\n<r>℣.</r> Glory be to the Father, and to the Son, and to the Holy Ghost.\n\n' % (ant_en(a), ant_en(b), ant_en(v))
def chapter_of(F, part):
    c = F[part]['cap'] if isinstance(F.get(part), dict) else None
    while isinstance(c, str): c = F[c]['cap']
    return c
def cap_hymn9(cap, hy, vr, d, dox=None, resp=None, head=('Capitulum Hymnus Versus', 'Chapter Hymn Verse')):
    ref, txt = cap; hla, hen = hymn9(hy, d, dox)
    e = en(txt) or txt
    la = '<h>%s</h>\n<r>%s</r>\n<c>%s</c>%s\n<r>℟.</r> Deo grátias.\n\n%s<r>Hymnus</r>\n%s\n\n%s' % (head[0], ref, txt[0], txt[1:], v1resp(resp, 'la') if resp else '', hla, VR(vr, 'la'))
    en_ = '<h>%s</h>\n<r>%s</r>\n<c>%s</c>%s\n<r>℟.</r> Thanks be to God.\n\n%s<r>Hymn</r>\n%s\n\n%s' % (head[1], ref, e[0], e[1:], v1resp(resp, 'en') if resp else '', hen, VR(vr, 'en'))
    return put(la, en_)
def good_lessons(ls):
    out = {}
    for x in ls or []:
        try: n = int(x.get('n'))
        except Exception: continue
        m = re.match(r'(?:vulgate|DO) ([\d.]+)', str(x.get('src', '')))
        if n in out or not m or float(m.group(1)) < 0.75 or len(x.get('la', '')) < 80: 
            out.setdefault(n, None); continue
        out[n] = dict(x, n=n)
    return out
def lesson9(n, x, bl, rsp, lang_note):
    la = ['<h>Lectio %s</h>' % ROMN[n], '<r>℣.</r> Jube, domne, benedícere.', '<r>Benedictio.</r> ' + bl[0], '<r>℟.</r> Amen.']
    en_ = ['<h>Lesson %d</h>' % n, '<r>℣.</r> Pray, sir, a blessing.', '<r>Blessing.</r> ' + bl[1], '<r>℟.</r> Amen.']
    if x:
        if x.get('ref'): la.append('<r>%s</r>' % x['ref']); en_.append('<r>%s</r>' % x['ref'])
        if x.get('gospel'):
            la.append('<c>%s</c>%s' % (x['gospel'][0], x['gospel'][1:])); en_.append(ant_en(x['gospel']))
            if x.get('homily_head'): la.append('<r>%s</r>' % x['homily_head']); en_.append('<r>%s</r>' % x['homily_head'])
        t = x['la']; la.append('<c>%s</c>%s' % (t[0], t[1:])); en_.append(x.get('en') or t)
    else:
        la.append('<n>%s</n>' % lang_note[0]); en_.append('<n>%s</n>' % lang_note[1])
    la.append('Tu autem, Dómine, miserére nostri.\n<r>℟.</r> Deo grátias.'); en_.append('But thou, O Lord, have mercy on us.\n<r>℟.</r> Thanks be to God.')
    if rsp:
        la.append('\n<h>Responsorium %s</h>\n' % ROMN[n] + resp9(rsp, 'la')); en_.append('\n<h>Responsory</h>\n' + resp9(rsp, 'en'))
    return put('\n'.join(la), '\n'.join(en_))
FEAST_NOTE = []
def noct_of_feria(w): return {0: 0, 1: 0, 4: 0, 2: 1, 5: 1, 3: 2, 6: 2}[w]
def feast_matins(d, s, w, F, fe, o, rk):
    tp = F.get('_tp'); M_ = F['mat']; three = fe['rank'] == 'Tres Lectiones'
    rows = [put('<h>Ante Matutinum</h>\n<n>Pater noster et Credo in Deum secreto.</n>', '<h>Before Matins</h>\n<n>Our Father and the Apostles\' Creed silently.</n>'),
            lib_row('mat_incipit', lambda t, l: laus(t, l, s))]
    inv = (o or {}).get('invit') if (o or {}).get('invit') and len(o['invit']) < 160 and '*' in o['invit'] else None
    if three and not tp: inv = inv or (M_.get('tl') or {}).get('invit')
    rows.append(invit_row(inv or M_['invit'], 9))
    hla, hen = hymn9(M_['hymn'], d, 'tp' if tp and F.get('v1', {}).get('tp_stanzas') else ('bvm' if F['_cn'] == 'bvm' else None))
    rows.append(put('<h>Hymnus</h>\n' + hla, '<h>Hymn</h>\n' + hen))
    PL = good_lessons((o or {}).get('lessons')); has_proper = bool((o or {}).get('lessons'))
    CL = {}
    for c in lesson_chain(F['_cn']):
        for x in CLES.get(c, []): CL.setdefault(x['n'], x)
    bset = M_.get('benedictiones')
    def bless(n, noc):
        if bset: return bset[n - 1], en(bset[n - 1]) or bset[n - 1]
        return BEN[noc][(n - 1) % 3], BEN_EN[noc][(n - 1) % 3]
    def lesson_src(n):
        if PL.get(n): return PL[n]
        if has_proper and n in PL: return None    # the feast prints its own lesson n, not yet verified: never the Common's in its place    # a proper legend exists but its text is not clean yet
        return CL.get(n)
    NOTE = ('Lectio (in præparatione).', 'Lesson (in preparation).')
    if tp:
        noc = noct_of_feria(w); ps, ants, v = M_['noct'][noc]
        if M_.get('op_rule') and re.search(r'O\.\s?P|Ord', fe['title']):
            ps0, ants0, _ = M_['noct'][0]; rows += psalm_rows([ps0], None, ('In Nocturno', 'Nocturn'), single=None) if False else []
            rows += psalm_rows([[p] for p in ps0], [alla(a) for a in ants0], ('In Nocturno', 'Nocturn')); rows.append(vr_row(M_['op_v']))
        else:
            rows += psalm_rows([[p] for p in ps], None, ('In Nocturno', 'Nocturn'), single=M_['ant']); rows.append(vr_row([alla(v[0]), alla(v[1])]))
        rs = M_['resp']
        if M_.get('resp_by_noct') or not isinstance(rs, list) or len(rs) != 3:
            base9 = cres(F['_cn'])['mat']['resp']; rs = [(a, alla(b), vv, g) for a, b, vv, g in base9[3 * noc:3 * noc + 3]]
        for i in range(3):
            n = [1, 4, 5][i]; x = lesson_src(n) if i else (lesson_src(1) or lesson_src(4))
            rows.append(lesson9(i + 1, x, bless(3 * noc + i + 1, noc), rs[i], NOTE))
        rows.append(put('<h>Te Deum</h>\n<r>Canticum SS. Ambrosii et Augustini</r>\n%s' % TEDEUM[0], '<h>Te Deum</h>\n%s' % TEDEUM[1]))
        return rows
    if three:
        tl = M_.get('tl') or {}
        allps = [p for noc in M_['noct'] for p in noc[0]]
        rows += psalm_rows([[p] for p in allps], None, ('In Nocturno', 'Nocturn'), single=tl.get('ant') or M_['noct'][0][1][0])
        rows.append(vr_row(M_['noct'][0][2]))
        noc = noct_of_feria(w); rs = M_['resp'][3 * noc:3 * noc + 3]
        if F['_cn'] in ('virg', 'virg_mart'): rs = M_['resp'][6:9]
        for i in range(3):
            x = PL.get(i + 1) or (PL.get(4 + i) if i == 2 else None)
            rows.append(lesson9(i + 1, x, bless(i + 1, 0), rs[i], NOTE))
        return rows
    for ni in range(3):
        ps, ants, v = M_['noct'][ni]
        head = ('In %s Nocturno' % ['I', 'II', 'III'][ni], '%s Nocturn' % ['First', 'Second', 'Third'][ni])
        rows += psalm_rows([[p] for p in ps], ants, head)
        rows.append(vr_row(v))
        for k in range(3):
            n = 3 * ni + k + 1
            rows.append(lesson9(n, lesson_src(n), bless(n, ni), M_['resp'][n - 1], NOTE))
    if not (rk == 1 and s in ('sept', 'cin', 'quad', 'pass')):
        rows.append(put('<h>Te Deum</h>\n<r>Canticum SS. Ambrosii et Augustini</r>\n%s' % TEDEUM[0], '<h>Te Deum</h>\n%s' % TEDEUM[1]))
    return rows
def clean_proper(o, k, maxlen=420):
    v = (o or {}).get(k)
    if not v or not isinstance(v, str) or len(v) > maxlen or re.search(r'Psalm|pag\.|Capitul|Hymnus|Ana\.|\bT\.|\?\.', v): return None
    return v
def feast_oratio(d, fe, F):
    t0 = re.sub(r'\s*\(translatum\)', '', fe['title'])
    if (PFIX.get(t0) or {}).get('oratio'): return PFIX[t0]['oratio']
    o = san_oratio(d, fe['title'])
    if o and re.search(r'prævení|vigíli', o, re.I): o = None
    return o or F.get('oratio')
def feast_lauds(d, s, w, F, fe, o, rk, oratio, comms):
    tp = F.get('_tp'); La = F['laud']; three = fe['rank'] == 'Tres Lectiones'
    v = F['al']
    inc_la, inc_en = L(LIB['incipit'])
    rows = [put(laus(inc_la.replace('<h>Incipit</h>\n', '<h>Incipit</h>\n' + VR(v, 'la') + '\n'), 'la', s), laus(inc_en.replace('<h>Start</h>\n', '<h>Start</h>\n' + VR(v, 'en') + '\n'), 'en', s))]
    ants = La['ant'] if not F.get('add_alleluia') else [alla(a) for a in La['ant']]
    pl = (o or {}).get('laudes')
    if isinstance(pl, list) and len(pl) == 5 and all(isinstance(a, str) and len(a) < 300 for a in pl) and not tp: ants = pl
    groups = P['LAUDS_SUN_SEPT'] if s in ('sept', 'quad', 'pass', 'cin') else P['LAUDS_SUN']
    rows += psalm_rows(groups, None, single=ants[0]) if three else psalm_rows(groups, ants)
    vr = La['vr'] if not F.get('add_alleluia') else [alla(x) for x in La['vr']]
    dox = 'tp' if tp and La.get('tp_stanzas') else ('bvm' if F['_cn'] == 'bvm' else None)
    rows.append(cap_hymn9(chapter_of(F, 'laud'), La['hymn'], vr, d, dox))
    b = clean_proper(o, 'bened') or (alla(La['bened']) if F.get('add_alleluia') else La['bened'])
    rows.append(gospel_row('b', b))
    rows.append(oratio_row(False, oratio))
    rows += comms('Laudes')
    rows.append(lib_row('conclusio'))
    return rows, ants
NOMINA = re.compile(r'^(Deus|De[io]|Dómin|Christ|Jesu|Jesus|María|Marí|Spirit|Spírit|Patr|Fíli|Sanct|Israël|Jerúsalem|Sion)')
def lc1(x):
    """lower-case the first letter of a joined clause, except a sacred or proper name"""
    return x if not x or NOMINA.match(x) else x[0].lower() + x[1:]
def rbr(r1, r2, rv, alle, lang):
    """short responsory of the Hours; alle = the Totum Duplex form with a double Allelúja"""
    if lang == 'en':
        return '<r>℟.br.</r> %s\n<r>℣.</r> %s' % (ant_en(r1 + ' ' + r2), ant_en(rv))
    if alle and 'allelúja' not in r2.lower():
        R = (r1.rstrip(' ,:;') + ' ' + lc1(r2)).rstrip(' .,:;')
        return '<r>℟.br.</r> %s, * Allelúja, allelúja. %s.\n<r>℣.</r> %s Allelúja.\n<r>℣.</r> Glória Patri, et Fílio, et Spirítui Sancto. %s.' % (R, R, rv.rstrip(' .,:;') + '.', R)
    rep1 = r1.rstrip(' ,:;'); rep2 = r2.rstrip(' .,:;')
    return '<r>℟.br.</r> %s * %s %s, %s.\n<r>℣.</r> %s %s.\n<r>℣.</r> Glória Patri, et Fílio, et Spirítui Sancto. %s, %s.' % (r1, r2, rep1, lc1(rep2), rv, rep2, rep1, lc1(rep2))
def feast_little(d, s, w, hour, F, fe, ants, oratio, rk):
    tp = F.get('_tp')
    rows = [lib_row('incipit', lambda t, l: laus(t, l, s))]
    dox = 'bvm' if F['_cn'] == 'bvm' else None
    hla, hen = hymn9(P['HOUR_HYMN'][hour], d, dox); rows.append(put('<h>Hymnus</h>\n' + hla, '<h>Hymn</h>\n' + hen))
    a = ants[{'Prima': 0, 'Tertia': 1, 'Sexta': 2, 'Nona': 4}[hour]]
    groups = P['PRIME_PS'] if hour == 'Prima' else P['HOUR_PS'][hour]
    rows += psalm_rows(groups, None, single=a)
    if hour == 'Prima':
        pv = 'Qui natus es de Vírgine María.' if F['_cn'] == 'bvm' else 'Qui surrexísti a mórtuis.' if tp else 'Qui sedes ad déxteram Patris.'
        cap = ('1 Tim 1', 'Regi sæculórum immortáli et invisíbili, soli Deo honor et glória in sǽcula sæculórum. Amen.')
        la = '<h>Capitulum Responsorium Versus</h>\n<r>%s</r>\n<c>%s</c>%s\n<r>℟.</r> Deo grátias.\n\n' % (cap[0], cap[1][0], cap[1][1:])
        la += '<r>℟.br.</r> Jesu Christe, Fili Dei vivi, * Miserére nobis%s. Jesu Christe.\n<r>℣.</r> %s Miserére nobis.\n<r>℣.</r> Glória Patri, et Fílio, et Spirítui Sancto. Jesu Christe.\n\n' % (', allelúja, allelúja' if tp else '', pv)
        la += '<r>℣.</r> Exsúrge, Dómine, ádjuva nos%s.\n<r>℟.</r> Et líbera nos propter nomen tuum%s.' % ((', allelúja',) * 2 if tp else ('', ''))
        en_ = '<h>Chapter Responsory Verse</h>\n<r>%s</r>\n%s\n<r>℟.</r> Thanks be to God.\n\n<r>℟.br.</r> Jesus Christ, Son of the living God, * Have mercy on us.\n<r>℣.</r> %s\n\n<r>℣.</r> Arise, O Lord, help us.\n<r>℟.</r> And deliver us for thy name\'s sake.' % (cap[0], en(cap[1]) or cap[1], ant_en(pv))
        rows.append(put(la, en_))
        rest = little(d, s, w, 'Prima')
        i = next((k for k, r in enumerate(rest) if 'Capitulum Responsorium' in COMMON[r[0]]), None)
        rows += rest[i + 1:] if i is not None else []
        return rows
    t = F[{'Tertia': 't', 'Sexta': 's', 'Nona': 'n'}[hour]]
    ref, txt = t[0], t[1]
    if isinstance(txt, str) and txt in ('v1', 'laud'): txt = chapter_of(F, txt)[1]
    r1, r2, rv, V, R = t[2:]
    alle = rk >= 4 and s not in ('sept', 'cin', 'quad', 'pass') and not tp
    if F.get('add_alleluia') and tp: r2 = 'Allelúja, allelúja.' if 'allelúja' not in r2.lower() else r2; V, R = alla(V), alla(R)
    e = en(txt) or txt
    la = '<h>Capitulum Responsorium Versus</h>\n<r>%s</r>\n<c>%s</c>%s\n<r>℟.</r> Deo grátias.\n\n%s\n\n%s' % (ref, txt[0], txt[1:], rbr(r1, r2, rv, alle, 'la'), VR([V, R], 'la'))
    en_ = '<h>Chapter Responsory Verse</h>\n<r>%s</r>\n%s\n<r>℟.</r> Thanks be to God.\n\n%s\n\n%s' % (ref, e, rbr(r1, r2, rv, alle, 'en'), VR([V, R], 'en'))
    rows.append(put(la, en_))
    rows.append(oratio_row(False, oratio))
    rows.append(lib_row('conclusio'))
    return rows
def feast_vespers(d, s, w, F, fe, o, which, oratio, comms, ants_l=None, split_from=None):
    """which = 1 (I Vespers, on the eve) or 2; split_from = (F, fe, o, oratio) of the following feast when Vespers are divided
    'a capitulo de sequenti'"""
    tp = F.get('_tp'); rk = RV.get(fe['rank'] or '', 0)
    rows = [lib_row('incipit', lambda t, l: laus(t, l, s))]
    if which == 1:
        V1 = F['v1']; ant = V1['ant'] if not F.get('add_alleluia') else alla(V1['ant'])
        if rk >= 4 and V1.get('ps', 'lp') == 'lp': rows += psalm_rows(LP, None, single=ant)
        elif rk >= 2: g, _ = P['VESP'][str(w)]; rows += psalm_rows(g, None, single=ant)
        else: g, a = P['VESP'][str(w)]; rows += psalm_rows(g, a)
    else:
        V2 = F['v2']; ant = V2.get('ant') or (ants_l[0] if ants_l else F['laud']['ant'][0])
        if F.get('add_alleluia'): ant = alla(ant)
        rows += psalm_rows([[p] for p in V2.get('ps') or cres(F['_cn'])['v2']['ps']], None, single=ant)
    if split_from:
        F, fe, o, oratio = split_from; which = 1; tp = F.get('_tp'); rk = RV.get(fe['rank'] or '', 0)
        rows.append(note_row('A capítulo de sequénti: %s.' % fe['title'], 'From the chapter, of the following feast: %s.' % fe['title']))
    part = 'v1' if which == 1 else 'v2'
    X = F[part]
    vr = X.get('vr') or F['v1']['vr']
    if F.get('add_alleluia'): vr = [alla(x) for x in vr]
    hy = X.get('hymn') or F['v1']['hymn']
    dox = 'tp' if tp and (X.get('tp_stanzas') or F['v1'].get('tp_stanzas')) else None
    rows.append(cap_hymn9(chapter_of(F, part) if X.get('cap') else chapter_of(F, 'v1'), hy, vr, d, dox, resp=F['v1'].get('resp') if which == 1 and rk >= 3 else None))
    m = clean_proper(o, 'magn1' if which == 1 else 'magn2') or X.get('magn')
    if F.get('add_alleluia'): m = alla(m)
    rows.append(gospel_row('m', m))
    rows.append(oratio_row(False, oratio))
    rows += comms('Vespera')
    rows.append(lib_row('conclusio'))
    return rows
def proper_entry(d, title):
    """the extracted Sanctorale entry (offices.py) of a feast, matched by date and name"""
    md = d.strftime('%m-%d'); best, br = None, 0.0; tn = nb(title)
    for k, o in OFF.items():
        if not k.startswith('S:' + md + ':'): continue
        r_ = difflib.SequenceMatcher(None, tn[:40], nb(o.get('title', ''))[:40]).ratio()
        if r_ > br: best, br = o, r_
    return best if br >= 0.45 else None

def office_season(d, s):
    """the season used for a feast's Office on a day whose Tempore is wholly proper but admits feasts"""
    if s in ('pent', 'tri', 'nat'): return 'pasch' if (d - easter(d.year)).days < 49 else 'pt'
    return s
FD_CACHE = {}
PROP = {}
try:
    for _k, _v in json.load(open(os.path.join(HERE, 'propers1909.json'), encoding='utf-8')).items(): PROP[_k.split('|', 1)[1]] = _v
except FileNotFoundError: pass
PFIX = {}
try: PFIX = json.load(open(os.path.join(HERE, 'propers_fix.json'), encoding='utf-8'))
except FileNotFoundError: pass
for _f in sorted(glob.glob(os.path.join(HERE, 'fix', '*.json'))):   # one file per helper / stretch of the calendar, same format
    try: PFIX.update({k: v for k, v in json.load(open(_f, encoding='utf-8')).items() if not k.startswith('_')})
    except Exception as _e: print('fix file', _f, _e)
def with_proper(F, o, title):
    """the feast's own pieces over its Common. ONLY texts verified by eye against the page images are used (propers_fix.json and
    fix/*.json; EYEPASS.md): explicit pieces, and the machine reading (propers1909.json) when its entry says 'ok' (after 'sub').
    An unverified machine reading is never shown: its lessons only mark that the feast prints lessons of its own (so that the
    Common's are not put in their place) when the feast has no verified entry yet."""
    M0 = PROP.get(title) or {}; X = PFIX.get(title) or {}
    # the old machine reading of the Sanctorale (offices1909.json: magn, bened, laudes, invit …) was never verified: only its title is kept
    o = {k: v for k, v in (o or {}).items() if k in ('title', 'rank')}
    if not M0 and not X: return F, o
    P = {}
    if X.get('ok'):
        def sb(v):
            if isinstance(v, str):
                for a_, b_ in X.get('sub', []): v = v.replace(a_, b_)
                return v
            if isinstance(v, dict): return {k: sb(x) for k, x in v.items()}
            if isinstance(v, list): return [sb(x) for x in v]
            return v
        P = sb(M0); no = set(X.get('not_ok', []))
        P['lessons'] = [dict(x, src='DO 1.00 (verified by eye)') for x in P.get('lessons', []) if ('lectio %s' % x.get('n')) not in no]
        for sec in ('v1', 'mat', 'laud', 'v2'):
            if isinstance(P.get(sec), dict): P[sec] = {k: v for k, v in P[sec].items() if '%s.%s' % (sec, k) not in no}
        for x in P['lessons']:
            if x.get('resp') and ('resp %s' % x.get('n')) in no: x.pop('resp')
    F = dict(F)
    def get(sec, k):
        if '%s.%s' % (sec, k) in X: return X['%s.%s' % (sec, k)]
        return (P.get(sec) or {}).get(k)
    for sec, keys in (('v1', ('ant', 'ants', 'magn', 'resp', 'cap', 'vr')), ('laud', ('ant', 'bened')), ('v2', ('ant', 'magn'))):
        for k in keys:
            v = get(sec, k)
            if v and isinstance(F.get(sec), dict):
                if k == 'resp' and len(v) == 4: v = list(v) + [v[3]]
                if k == 'resp' and v[4] is False: v = list(v[:4]) + [v[3]]
                F[sec] = dict(F[sec], **{k: tuple(v) if k in ('resp', 'vr') else v})
    if X.get('al'): F['al'] = tuple(X['al'])
    for sec in ('v1', 'mat', 'laud', 'v2'):       # a hymn printed in the feast itself (verified by eye)
        hy = X.get(sec + '.hymn')
        if hy and isinstance(F.get(sec), dict):
            inc = hy[0].split(' / ')[0].rstrip(',.:;')
            CM.HYMN_TEXT[inc] = (CM._hy(hy), CM._hy(hy)); FIXHY.add(inc)
            F[sec] = dict(F[sec], hymn=inc)
    M_ = dict(F['mat']); tp = F.get('_tp')
    iv = get('mat', 'invit')
    if iv and len(iv) < 220 and '*' in iv: M_['invit'] = iv
    na = get('mat', 'nants')
    if X.get('psalms') and not tp and len(M_.get('noct', [])) == 3 and len(X['psalms']) == 3:   # the feast prints its own Matins psalms
        M_['noct'] = [(list(X['psalms'][i]),) + tuple(M_['noct'][i][1:]) for i in range(3)]
    if na and not tp and len(M_.get('noct', [])) == 3 and len(na) == 3:
        nv = X.get('mat.nvr') or (P.get('mat') or {}).get('nvr') or [None] * 3
        nv = list(nv) + [None] * (3 - len(nv))
        M_['noct'] = [(M_['noct'][i][0], na[i] if len(na[i]) == len(M_['noct'][i][1]) else M_['noct'][i][1], tuple(nv[i]) if nv[i] and len(nv[i]) == 2 else M_['noct'][i][2]) for i in range(3)]
    if not tp and isinstance(M_.get('resp'), list) and len(M_['resp']) == 9:
        rs = {}
        for x in P.get('lessons', []):
            r = x.get('resp'); n = x.get('n')
            if r and isinstance(n, int) and 1 <= n <= 9 and r.get('a') and r.get('b'): rs[n] = (r['a'], r['b'], r.get('v') or [], bool(r.get('gloria')))
        for n, r in (X.get('resp') or {}).items():
            if str(n).isdigit() and 1 <= int(n) <= 9 and len(r) >= 4: rs[int(n)] = (r[0], r[1], r[2] if isinstance(r[2], list) else [r[2]], tuple(r[3]) if isinstance(r[3], list) else r[3])
        if rs: M_['resp'] = [rs.get(n, M_['resp'][n - 1]) for n in range(1, 10)]   # verified responsories; the others are the Common's, as the page directs
    F['mat'] = M_
    ls = list(P.get('lessons', []))
    if X.get('lessons'):
        def les(n, t):
            x = dict(n=int(n), la=t, src='DO 1.00 (verified by eye)', head=[], close=None)
            if X.get('gospel%s' % n): x['gospel'] = X['gospel%s' % n]; x['homily_head'] = X.get('homily%s' % n)
            return x
        ls = [x for x in ls if str(x.get('n')) not in X['lessons']] + [les(n, t) for n, t in X['lessons'].items() if str(n).isdigit() and isinstance(t, str)]
    if not X and M0.get('lessons'):   # not yet read by eye: the feast's own lessons are marked 'in preparation', never shown unverified
        ls = [dict(x, src='doubtful') for x in M0['lessons']]
    if ls:
        o = dict(o or {}); o['lessons'] = sorted(ls, key=lambda x: x.get('n') or 0)
    elif X:
        o = dict(o or {}); o.pop('lessons', None)
    return F, o
def feast_day(d):
    """the winning feast of a day with a Common to render it: dict(fe, cn, F, o, rk) or None"""
    if d in FD_CACHE: return FD_CACHE[d]
    r = None; s = season(d)[0]; w = (d.weekday() + 1) % 7
    if not hard_proper(d):
        for c in ECAL.get(d, []):
            rk = RV.get(c['rank'] or '', 0)
            if rk >= 1 and (season(d)[3] or celebrable(d, s, w, rk)):
                cn = feast_common(d, re.sub(r'\s*\(translatum\)', '', c['title']))
                if cn:
                    ti0 = re.sub(r'\s*\(translatum\)', '', c['title'])
                    F0, o0 = with_proper(NM.fill_all(common_full(cn, tp_of(d)), c['title']), proper_entry(d, ti0), ti0)
                    r = dict(fe=c, cn=cn, F=F0, o=o0, rk=rk)
                break
    FD_CACHE[d] = r; return r
def day_rank(d):
    """rank of the Office of a day for concurrence (Vespers)"""
    if hard_proper(d): return 6
    s = season(d)[0]; w = (d.weekday() + 1) % 7
    for c in ECAL.get(d, []):
        rk = RV.get(c['rank'] or '', 0)
        if rk >= 1 and (season(d)[3] or celebrable(d, s, w, rk)): return rk
    if w == 0: return 5 if s in ('adv', 'sept', 'quad', 'pass') else 2.5
    return 0
def comm_ant(c, hour):
    """antiphon and versicle of a commemoration: the feast's proper Benedictus / Magnificat antiphon where clean, else its
    Common's (Lauds: Benedictus antiphon and Lauds versicle; Vespers: of I Vespers for tomorrow's feast, else of II Vespers)"""
    try:
        cn = feast_common(c['_d'], c['title'])
        if not cn or cn not in CM.C: return None
        F = NM.fill_all(common_full(cn, tp_of(c['_d'])), c['title']); o = proper_entry(c['_d'], c['title'])
        if hour == 'Laudes': a = clean_proper(o, 'bened') or F['laud'].get('bened'); v = F['laud'].get('vr')
        elif c.get('_v1'): a = clean_proper(o, 'magn1') or F['v1'].get('magn'); v = F['v1'].get('vr')
        else: a = clean_proper(o, 'magn2') or F.get('v2', {}).get('magn') or F['v1'].get('magn'); v = F.get('v2', {}).get('vr') or F['v1'].get('vr')
        if not a or not v: return None
        if F.get('_tp') or F.get('add_alleluia'): a, v = alla(a), [alla(x) for x in v]
        return a, v
    except (KeyError, TypeError):
        return None
def comm_rows(entries):
    def f(hour):
        out = []
        for c in entries:
            if c['rank'] in (None, ''): continue
            orat = san_oratio(c['_d'], c['title'])
            if orat and re.search(r'prævení', orat): orat = None
            if orat: orat = NM.fill(orat, c['title'])
            la = '<h>Commemoratio</h>\n<n>%s%s</n>' % (c['title'], '' if orat else ' (Oratio in præparatione)')
            en_ = '<h>Commemoration</h>\n<n>%s%s</n>' % (c['title'], '' if orat else ' (prayer in preparation)')
            av = comm_ant(c, hour)
            if av:
                a, v = av
                la += '\n<r>Ant.</r> %s\n%s' % (a, VR(v, 'la')); en_ += '\n<r>Ant.</r> %s\n%s' % (ant_en(a), VR(v, 'en'))
            if orat: la += '\n<c>O</c>rémus.\n<c>%s</c>%s\n<r>℟.</r> Amen.' % (orat[0], orat[1:]); en_ += '\n<c>L</c>et us pray.\n%s\n<r>℟.</r> Amen.' % (en(orat) or orat)
            out.append(put(la, en_))
        return out
    return f
def others(d, win_title):
    return [dict(c, _d=d) for c in ECAL.get(d, []) if c['title'] != win_title]

TEDEUM = None
def main():
    effective_calendar()
    global TEDEUM
    for k, v in lib.items():
        if '<r>Te Deum</r>\n<c>T</c>e Deum laudámus' in v and k in pair:
            m = re.search(r'<r>Te Deum</r>\n(<c>T</c>e Deum laudámus[\s\S]*)$', v); e = re.search(r'<r>Te Deum</r>\n(<c>W</c>e praise thee[\s\S]*)$', lib[pair[k]])
            if m: TEDEUM = (m.group(1), e.group(1) if e else m.group(1)); break
    if not TEDEUM: raise SystemExit('no Te Deum')
    n = 0; d = FROM; NF = 0
    while d <= TO:
        s, wk, num, prop = season(d); w = (d.weekday() + 1) % 7
        if prop: H = proper_day(d); t = {'nat': 'Tempus Nativitatis', 'tri': 'Triduum Sacrum et Octava Paschæ', 'pent': 'Ab Ascensione ad Octavam Corporis Christi'}[s]
        else:
            H = {'Matutinum': matins(d, s, w), 'Laudes': lauds(d, s, w), 'Vespera': vespers(d, s, w), 'Completorium': compline(d, s, w)}
            for h in ('Prima', 'Tertia', 'Sexta', 'Nona'): H[h] = little(d, s, w, h)
            t = title(d, s, wk, num)
        rank = 'Psalterium et Proprium de Tempore (Sanctorale in præparatione)'
        cal = ECAL.get(d, [])
        if cal and prop and not hard_proper(d) and RV.get(cal[0]['rank'] or '', 0) >= 1:
            ss = 'pasch' if (d - easter(d.year)).days < 49 else 'pt'
            H = {'Matutinum': matins(d, ss, w), 'Laudes': lauds(d, ss, w), 'Vespera': vespers(d, ss, w), 'Completorium': compline(d, ss, w)}
            for h in ('Prima', 'Tertia', 'Sexta', 'Nona'): H[h] = little(d, ss, w, h)
            prop = False; t = ''
        FX = feast_day(d) if not hard_proper(d) else None
        NMT[0] = FX['fe']['title'] if FX else None
        if FX:
            fe, F, o, rk = FX['fe'], FX['F'], FX['o'], FX['rk']; fs = office_season(d, s); NF += 1
            orat = feast_oratio(d, fe, F)
            cm = comm_rows(others(d, fe['title']))
            H['Matutinum'] = feast_matins(d, fs, w, F, fe, o, rk)
            H['Laudes'], ants_l = feast_lauds(d, fs, w, F, fe, o, rk, orat, cm)
            for h in ('Prima', 'Tertia', 'Sexta', 'Nona'): H[h] = feast_little(d, fs, w, h, F, fe, ants_l, orat, rk)
            H['Completorium'] = compline(d, fs, w)
            t = '%s ~ %s' % (fe['title'], fe['rank']); rank = None
        elif cal and not prop:
            w_ = (d.weekday() + 1) % 7
            win, comms = None, []
            for i, c in enumerate(cal):
                rk = RV.get(c['rank'] or '', 0)
                if win is None and rk >= 1 and celebrable(d, s, w_, rk): win = c
                else: comms.append(c)
            if win:
                rk = win['rank']; t = '%s ~ %s' % (win['title'], rk); rank = None
                note = note_row('Hodie: %s (%s). Officium proprium in præparatione; intérim Psalterium de Tempore cum Oratióne Sancti.' % (win['title'], rk),
                                'Today: %s (%s). The proper Office is in preparation; meanwhile the Psalter of the day with the Saint’s prayer.' % (win['title'], rk))
                for h in H: H[h].insert(0, note)
                orat = san_oratio(d, win['title'])
                if orat:
                    mem = put('<h>Oratio de Sancto</h>\n<n>%s</n>\n<c>O</c>rémus.\n<c>%s</c>%s\n<r>℟.</r> Amen.' % (win['title'], orat[0], orat[1:]),
                              '<h>Prayer of the Saint</h>\n<n>%s</n>\n<c>L</c>et us pray.\n%s\n<r>℟.</r> Amen.' % (win['title'], en(orat) or orat))
                    for h in ('Laudes', 'Vespera'): H[h].insert(len(H[h]) - 1, mem)
            for c in comms:
                if c['rank'] in (None, ''): continue
                mem = comm_rows([dict(c, _d=d)])('Laudes')[0]
                for h in ('Laudes', 'Vespera'): H[h].insert(len(H[h]) - 1, mem)
        # Vespers by concurrence: I Vespers of tomorrow's feast, II Vespers of today's, or divided a capitulo
        dn = d + datetime.timedelta(days=1); TX = feast_day(dn) if not hard_proper(dn) else None
        rt, rn = day_rank(d), day_rank(dn)
        if TX and TX['fe']['rank'] != 'Memoria' and (rn > rt or (rn == rt and not FX)):
            Fn = TX['F']; orn = (PFIX.get(re.sub(r'\s*\(translatum\)', '', TX['fe']['title'])) or {}).get('v1.oratio') or feast_oratio(dn, TX['fe'], Fn)
            cmv = comm_rows(([dict(FX['fe'], _d=d)] if FX else []) + others(d, FX['fe']['title'] if FX else ''))
            NMT[0] = TX['fe']['title']   # I Vespers of tomorrow's feast: its name
            H['Vespera'] = feast_vespers(d, office_season(dn, season(dn)[0]), w, Fn, TX['fe'], TX['o'], 1, orn, cmv)
            NMT[0] = FX['fe']['title'] if FX else None
        elif FX and TX and rn == rt and FX['fe']['rank'] != 'Tres Lectiones':
            Fn = TX['F']; orn = (PFIX.get(re.sub(r'\s*\(translatum\)', '', TX['fe']['title'])) or {}).get('v1.oratio') or feast_oratio(dn, TX['fe'], Fn)
            cmv = comm_rows([dict(FX['fe'], _d=d)] + others(d, FX['fe']['title']))
            H['Vespera'] = feast_vespers(d, office_season(d, s), w, FX['F'], FX['fe'], FX['o'], 2, None, cmv, ants_l, split_from=(Fn, TX['fe'], TX['o'], orn))
        elif FX and FX['fe']['rank'] != 'Tres Lectiones' and rt >= rn:
            nxt = ([dict(TX['fe'], _d=dn, _v1=True)] if TX else [])
            H['Vespera'] = feast_vespers(d, office_season(d, s), w, FX['F'], FX['fe'], FX['o'], 2, orat, comm_rows(nxt + others(d, FX['fe']['title'])), ants_l)
        elif FX:
            H['Vespera'] = vespers(d, office_season(d, s), w)
            mem = comm_rows([dict(FX['fe'], _d=d)])('Vespera')[0]; H['Vespera'].insert(len(H['Vespera']) - 1, mem)
        day = {'t': [t if rank is None else '%s ~ %s' % (t, rank)], 'tv': [], 'h': H, 'p': {}, 'b': {}}
        os.makedirs(os.path.join(OUT, str(d.year)), exist_ok=True)
        json.dump(day, open(os.path.join(OUT, str(d.year), d.strftime('%m-%d') + '.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
        d += datetime.timedelta(days=1); n += 1
    json.dump(COMMON, open(os.path.join(OUT, 'common.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    os.makedirs(os.path.join(OUT, 'psalter'), exist_ok=True)
    for k, v in SH.items(): json.dump(v, open(os.path.join(OUT, 'psalter', k + '.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    json.dump({'from': FROM.isoformat(), 'to': TO.isoformat()}, open(os.path.join(OUT, 'range.json'), 'w'))
    print(n, 'days;', NF, 'feasts from the Commons;', len(COMMON), 'blocks;', len(SH), 'shards')
if __name__ == '__main__': main()
