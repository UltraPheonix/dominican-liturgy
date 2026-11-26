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
def tkey(d):
    s, wk, n, prop = season(d); w = (d.weekday() + 1) % 7
    if s == 'adv': return 'adv%d-%d' % (n, w)
    if s == 'pt' and w == 6 and (d + datetime.timedelta(days=1)) == adv1(d.year): return 'pre-adv'
    return None
def TP(d, k):
    x = T['days'].get(tkey(d) or '', {}); return x.get(k)

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
def L(i): return lib[i], lib[pair[i]]
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
def put(la, en_):
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
def resp_text(r, lang):
    a, b, v = r; rep = b.split()[0].rstrip(',.:') + '.'
    if lang == 'la': return '<r>℟.</r> %s * %s\n<r>℣.</r> %s %s\n<r>℣.</r> Glória Patri, et Fílio, et Spirítui Sancto. %s\n\n' % (a, b, v, rep, rep)
    return '<r>℟.</r> %s * %s\n<r>℣.</r> %s\n\n' % (ant_en(a), ant_en(b), ant_en(v))
def week_oratio(d, s):
    if s != 'adv': return None
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
            rows.append(note_row('Lectiones et Responsoria de Proprio de Tempore (in præparatione).', 'Lessons and responsories from the Proper of Time (in preparation).'))
        if s not in ('adv', 'sept', 'cin', 'quad', 'pass'):
            rows.append(put('<h>Te Deum</h>\n<r>%s</r>\n%s' % (pstitle(0, 'la') if False else 'Canticum SS. Ambrosii et Augustini', TEDEUM[0]), '<h>Te Deum</h>\n%s' % TEDEUM[1]))
    else:
        groups, ants, v = P['FER_MAT'][str(w)]
        ok = s in ('pe', 'sept', 'cin', 'quad', 'pass', 'pt', 'adv')
        rows += psalm_rows(groups, ants if ok else [None] * 6, ('In Nocturno', 'Nocturn'))
        if s in P['FER_MAT_V']: v = P['FER_MAT_V'][s][(w - 1) % 3]
        rows.append(vr_row(v) if ok else put(PROPER['la'], PROPER['en']))
        rows.append(note_row('Tres Lectiones cum Responsoriis de Proprio de Tempore (in præparatione).', 'Three lessons with responsories from the Proper of Time (in preparation).'))
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

TEDEUM = None
def main():
    global TEDEUM
    for k, v in lib.items():
        if '<r>Te Deum</r>\n<c>T</c>e Deum laudámus' in v and k in pair:
            m = re.search(r'<r>Te Deum</r>\n(<c>T</c>e Deum laudámus[\s\S]*)$', v); e = re.search(r'<r>Te Deum</r>\n(<c>W</c>e praise thee[\s\S]*)$', lib[pair[k]])
            if m: TEDEUM = (m.group(1), e.group(1) if e else m.group(1)); break
    if not TEDEUM: raise SystemExit('no Te Deum')
    n = 0; d = FROM
    while d <= TO:
        s, wk, num, prop = season(d); w = (d.weekday() + 1) % 7
        if prop: H = proper_day(d); t = {'nat': 'Tempus Nativitatis', 'tri': 'Triduum Sacrum et Octava Paschæ', 'pent': 'Ab Ascensione ad Octavam Corporis Christi'}[s]
        else:
            H = {'Matutinum': matins(d, s, w), 'Laudes': lauds(d, s, w), 'Vespera': vespers(d, s, w), 'Completorium': compline(d, s, w)}
            for h in ('Prima', 'Tertia', 'Sexta', 'Nona'): H[h] = little(d, s, w, h)
            t = title(d, s, wk, num)
        rank = 'Psalterium et Ordinarium (Proprium et Sanctorale in præparatione)'
        day = {'t': ['%s ~ %s' % (t, rank)], 'tv': [], 'h': H, 'p': {}, 'b': {}}
        os.makedirs(os.path.join(OUT, str(d.year)), exist_ok=True)
        json.dump(day, open(os.path.join(OUT, str(d.year), d.strftime('%m-%d') + '.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
        d += datetime.timedelta(days=1); n += 1
    json.dump(COMMON, open(os.path.join(OUT, 'common.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    os.makedirs(os.path.join(OUT, 'psalter'), exist_ok=True)
    for k, v in SH.items(): json.dump(v, open(os.path.join(OUT, 'psalter', k + '.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    json.dump({'from': FROM.isoformat(), 'to': TO.isoformat()}, open(os.path.join(OUT, 'range.json'), 'w'))
    print(n, 'days;', len(COMMON), 'blocks;', len(SH), 'shards')
if __name__ == '__main__': main()
