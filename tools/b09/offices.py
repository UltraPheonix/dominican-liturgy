"""Generic extraction of the proper Offices of the 1909 Breviary (Temporale and Sanctorale) from the OCR, repaired word by word
against Divinum Officium / the Vulgate (the 1909 text decides; see repair.py).
-> offices1909.json {key: {title, rank, invit, laudes[5], bened, magn1, magn2, oratio, ants_mat[], lessons[], vesp1_r, ...}}
Keys: Temporale 'adv1-0', 'pe2-3', 'sept1-0', 'quad3-5', 'pass1-0', 'pasch2-0', 'pt4-2', named feasts 'T:<title>';
Sanctorale 'S:MM-DD:<n>'.
usage: python3 offices.py tempora1 | tempora2 | sancti1 | sancti2"""
import json, os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import repair as R, matins as M
OUT = os.path.join(HERE, 'offices1909.json')

# ---------- a generic corpus of DO short texts (antiphons, prayers, chapters, versicles, invitatories) ----------
SHORT = R.Corpus()
def _build_short():
    import glob
    for f in glob.glob(R.DO + '/Latin/Tempora/*.txt') + glob.glob(R.DO + '/Latin/Sancti/*.txt') + glob.glob(R.DO + '/Latin/Commune/*.txt') + glob.glob(R.DO + '/Latin/SanctiOP/*.txt') + glob.glob(R.DO + '/Latin/TemporaOP/*.txt') + glob.glob(R.DO + '/Latin/CommuneOP/*.txt') + glob.glob(R.DO + '/Latin/Psalterium/**/*.txt', recursive=True):
        try: S = R._sections(f)
        except Exception: continue
        for k, ls in S.items():
            if re.match(r'^(Lectio|Responsory)\d', k): continue
            for l in ls:
                if l.startswith(('!', '@', '&', '$', '_', '#')) or len(l) < 12: continue
                l = re.sub(r'^(?:V\.|R\.|Ant\.|v\.|r\.)\s*', '', l.split(';;')[0]).replace('* ', '').replace('$Per Dominum', '').strip()
                if l: SHORT.add([(w, (f, k)) for w in R.words(l)], (f, k))
if os.environ.get("NOSHORT") != "1": _build_short()
def fix_short(t, min_cov=0.7):
    t = re.sub(r'\s+', ' ', t).strip()
    if not t: return t
    r = SHORT.align(t, min_cov)
    if r:
        out = ' '.join(w for w, _ in r[0])
        if len(out.split()) >= 0.6 * len(t.split()): return out
    return t
def clean(t):
    t = re.sub(r'\s+', ' ', t).strip(' .;:,')
    return t + ('.' if t and t[-1] not in '.?!' else '')

def cut_prayer(t):
    """end a prayer at its conclusion; never run on into the next rubric or Office (OCR of the conclusion may be broken)"""
    m = re.search(r'\s(?:Ad (?:Utr|Matut|Laudes|Benedi|Magni|Memor|I+\. Vesp|Vesp)|Super Psalm|Invitatorium|Lectio [ivx]|Hymnus|In I+\. Noct|Capitulum|Die [IVXLivxl]+\.)', t)
    if m: t = t[:m.start()]
    m = re.search(r'\b(Per (?:Dóminum|Dominum|eúndem|eumdem|Christum)\b[^.]{0,120}|Qui (?:tecu\w|vivis|cum Patre)\b[^.]{0,160}|Per)\s*[.*]', t)
    if m: t = t[:m.end()]
    return t
def dropcap(t):
    """repair the drop-capital of a prayer as the OCR gives it: 'T\\eus, qui', 'r\\EUS, qui', 'eus, qui beátam Maríam D semper' -> 'Deus, qui ...'"""
    t = re.sub(r'^[^A-Za-zÀ-ÿ]*[A-Za-z]?[\\^\]|/]+\s*', '', t).strip()
    m = re.match(r'^(?:[A-Z]\s)?(eus|EUS|kus)\b', t)
    if m:
        t = 'Deus' + t[m.end():]
        t = re.sub(r'^(Deus\b.{0,70}?)\s[A-Z](?=\s)', r'\1', t, count=1)   # the displaced initial
    t = re.sub(r'^([A-ZÆ])([A-ZÆǼ]{2,})', lambda m: m.group(1) + m.group(2).lower(), t)
    return t
# ---------- fields of one Office ----------
END = r'(?=\s(?:Ad (?:Benedíctus|Magníficat|Laudes|Primam|Tertiam|Sextam|Nonam|Vesperas|I+\. Vesperas|Completorium|Memóriam)|Oratio\b|Capitulum|Hymnus|In I+\. Nocturno|In Iii?\. Nocturno|Lectio [ivx]+|Psalmus|Invitatorium|Feria|Sabbato|Dominica|T [A-Z]|¶|Antiphonae|Memória|Commemoratio)|$)'
CONC = r'(?:Per Dóminum[^.]*|Per eúndem[^.]*|Per eumdem[^.]*|Qui vivis[^.]*|Qui tecum[^.]*|Per Christum[^.]*|Qui cum Patre[^.]*|Per\.?)'
def field(pat, chunk, n=None):
    out = []
    for m in re.finditer(pat + r'\s*(.+?)' + END, chunk):
        out.append(clean(m.group(1)))
    return out
def parse_office(chunk):
    o = {}
    m = re.search(r'Invitatorium\.\s*(.+?\*\s*.+?)[.!?]', chunk)
    if m: o['invit'] = fix_short(clean(m.group(1)))
    a = field(r'Ad Benedíctus,?\s*A\w{1,3}\.', chunk)
    if a: o['bened'] = fix_short(a[0])
    mg = field(r'Ad Magníficat\s*A\w{1,3}\.', chunk)
    if mg:
        # a Magnificat antiphon before Matins is of I Vespers
        mi = chunk.find('Ad Matutinum'); first = chunk.find('Ad Magníficat')
        if mi > 0 and first < mi: o['magn1'] = fix_short(mg[0]); mg = mg[1:]
        if mg: o['magn2'] = fix_short(mg[-1])
    # prayers: 'Oratio.' / 'Oratio,' (OCR); the FIRST one after the heading is the saint's (a later one may belong to the next Office
    # when the OCR lost its heading). A prayer of the vigil ('cujus prævenímus festivitátem') is the I Vespers prayer only.
    ors = [x for x in re.finditer(r'Oratio[.,;:]\s*(.+?' + CONC + r')\.?', chunk)]
    ors = [x for x in ors if not re.match(r'\s*(?:\w+\s+){0,4}(?:ut in Laud|ut supra|ut in I|de Communi|pag\.)', x.group(1))]
    pr = [fix_short(dropcap(clean(cut_prayer(x.group(1)))), 0.6) for x in ors[:3]]
    pr = [p for p in pr if len(p) > 40]
    if pr:
        if re.search(r'prævení?mus|praevenimus', pr[0], re.I) and len(pr) > 1: o['oratio_v1'] = pr[0]; o['oratio'] = pr[1]
        else: o['oratio'] = pr[0]
    lm = re.search(r'Ad Laudes(?: Et Per Horas)? Antiphonae\.\s*(.+?)(?=Capitulum|Psalmi|Ad Benedíctus|Hymnus)', chunk)
    if lm:
        parts = re.split(r'(?:^|\s)(?:[1lI2-5s]|ii|iii|iv|v)[\.\-]\s', ' ' + lm.group(1))
        parts = [re.sub(r'Psalmus [^.]*?(?:pag\.\s*[\d\s]+\.?|céteris[^.]*\.)', '', p).strip() for p in parts if len(p.strip()) > 8]
        o['laudes'] = [fix_short(clean(p)) for p in parts[:5]]
    ants = field(r'(?:Super Psalm(?:os|um)(?: sola)?\s*)?\bA(?:na|ha|fia|tia|iia)\.', chunk)
    if ants: o['ants'] = [fix_short(x) for x in ants[:40]]
    # lessons and responsories (generic)
    L = []
    for n, x, r in M.parse_day(chunk):
        les = M.build_lesson(n, x)
        if r: les['resp'] = M.build_resp(n, r)
        L.append(les)
    if L: o['lessons'] = L
    rk = re.search(r'(Totum Duplex|Totum Dúplici|Duplex|Semiduplex|Simplex|Trium Lectionum|iij\. Lect)', chunk[:600])
    if rk: o['rank'] = rk.group(1).replace('Totum Dúplici', 'Totum Duplex')
    return o

# ---------- Temporale: titles -> keys ----------
ORD = {'prima': 1, 'i': 1, 'secunda': 2, 'ii': 2, 'tertia': 3, 'iii': 3, 'quarta': 4, 'iv': 4, 'quinta': 5, 'v': 5, 'sexta': 6, 'vi': 6,
       'septima': 7, 'vii': 7, 'octava': 8, 'viii': 8, 'ix': 9, 'x': 10, 'xi': 11, 'xii': 12, 'xiii': 13, 'xiv': 14, 'xv': 15, 'xvi': 16,
       'xvii': 17, 'xviii': 18, 'xix': 19, 'xx': 20, 'xxi': 21, 'xxii': 22, 'xxiii': 23, 'xxiv': 24, 'xxv': 25}
FERIA = {'secunda': 1, 'ii': 1, 'tertia': 2, 'iii': 2, 'quarta': 3, 'iv': 3, 'quinta': 4, 'v': 4, 'sexta': 5, 'vi': 5}
HEAD = re.compile(r'(?:(?<=\.\s)|(?<=^))((?:Dominica In Albis[^.]*|Dominica|DOMINICA|I\)OM\.|Dom\.)\s[^.]{2,70}?\.(?:\s(?:Post|POST)\s[^.]{2,40}\.)?|(?:Feria|FERIA|EERIA|KER1A|1ERIA)\s(?:Secunda|Tertia|Quarta|Quinta|Sexta|II|III|IV|V|VI|Iv|Vi)\b[^.]{0,50}\.|Sabbato\b[^.]{0,50}\.|In (?:Vigilia|Festo|Die|Nativitate|Circumcisione|Epiphania|Inventione|Octava|Cena|Ascensione|Monte|Compassióne|Commemoratione|Translatione)[^.]{0,80}\.|In Septuag[^.]{0,20}\.|In Sexag[^.]{0,20}\.|Feria V\. In Cena Dómini\.|Feria Vi\. In Parascéve\.|Sabbato Sancto\.)')
def temporale_key(title, ctx):
    """sequential: a Sunday title sets (season, n) when it names them, else continues the current season; a feria whose
    weekday is not after the previous one starts a new week (a Sunday heading lost by the OCR)"""
    t = title.lower().replace('111', 'iii').replace(' l.', ' i.')
    def num(s):
        m = re.search(r'\b(prima|secunda|tertia|quarta|quinta|sexta|septima|octava|[ivxl]{1,6})\b', s); return ORD.get(m.group(1)) if m else None
    def week(): return '%s%d' % (ctx['s'], ctx['n']) if ctx.get('s') not in (None, 'cin', 'asc', 'ew') else (ctx.get('s') or 'x')
    if re.match(r'^(dominica|dom\.|i\)om\.|in septuag|in sexag|in quinquag)', t) and not re.match(r'^dominica[,]', t):
        n = num(t.split('post')[0] if 'post' in t else t)
        for key, s_ in (('advent', 'adv'), ('epiphan', 'pe'), ('quadrag', 'quad'), ('passi', 'pass'), ('ramis', 'pass'), ('albis', 'pasch'),
                        ('pasch', 'pasch'), ('ascens', 'asc'), ('pentecost', 'pent'), ('trinit', 'pt')):
            if key in t:
                if s_ == 'pass': n = 2 if 'ramis' in t else 1
                if s_ == 'pasch' and 'albis' in t: n = 0
                if 'infra octavam' in t and s_ == 'pe': return 'T:' + title
                ctx.update(s=s_, n=n if n is not None else ctx.get('n', 0) + 1 if ctx.get('s') == s_ else 1); break
        else:
            if 'septuag' in t: ctx.update(s='sept', n=1)
            elif 'sexag' in t: ctx.update(s='sept', n=2)
            elif 'quinquag' in t: ctx.update(s='sept', n=3)
            elif ctx.get('s') == 'cin': ctx.update(s='quad', n=n or 1)
            elif 'oct' in t and ctx.get('s') in ('pasch', 'ew'): ctx.update(s='pasch', n=0)
            elif ctx.get('s'): ctx.update(n=n if n and n > ctx.get('n', 0) else ctx.get('n', 0) + 1)
            else: return 'T:' + title
        ctx['w'] = 0
        return week() + '-0'
    m = re.match(r'^(?:feria|eeria|ker1a|1eria)\s+(secunda|tertia|quarta|quinta|sexta|ii|iii|iv|v|vi)\b', t)
    if m:
        if 'cinerum' in t: ctx.update(s='cin', n=0, w=3); return 'cin-3'
        if ctx.get('s') == 'tri' or ('totum' in t and ctx.get('s') in ('tri', 'ew')):
            ctx.update(s='ew', n=0, w=FERIA[m.group(1)]); return 'ew-%d' % FERIA[m.group(1)]
        if 'cena' in t: return 'tri-4'
        if 'parasc' in t: return 'tri-5'
        w = FERIA[m.group(1)]
        if ctx.get('w') is not None and w <= ctx['w'] and ctx.get('s'):
            ctx['n'] = ctx.get('n', 0) + 1
            if ctx['s'] == 'cin': ctx.update(s='quad', n=1)
        ctx['w'] = w
        return week() + '-%d' % w if ctx.get('s') else 'T:' + title
    if t.startswith('sabbato'):
        if 'sancto' in t: ctx.update(s='tri', w=6); return 'tri-6'
        if ctx.get('s') == 'ew': ctx['w'] = 6; return 'ew-6'
        if ctx.get('s') and 'ante' not in t: ctx['w'] = 6; return week() + '-6'
    return 'T:' + title
def temporale(vol, a, b):
    t = M.text_range(a, b) if vol == 'v1' else text_range2(a, b)
    hs = []
    for m in HEAD.finditer(t):
        look = t[m.end(): m.end() + 260]
        if re.search(r'Ad Matutinum|Invitatorium|Lectio i\b|Ad I\. Vesperas|De Epístola|De Isaía|Incipit|De libro|Lectio sancti|In I\. Nocturno|Totum Duplex|Duplex', look):
            hs.append((m.start(), m.group(1)))
    out, ctx = collections.OrderedDict(), {}
    for i, (s, title) in enumerate(hs):
        e = hs[i + 1][0] if i + 1 < len(hs) else len(t)
        k = temporale_key(title + ' ' + t[s + len(title): s + len(title) + 40] if re.match(r'^(Feria|Dom)', title) else title, ctx)
        o = parse_office(t[s:e]); o['title'] = title
        if k in out: k = k + '+'
        out[k] = o
        print(k, '|', title[:50], '|', ','.join(x for x in o if x not in ('title',)), len(o.get('lessons', [])))
    return out
def text_range2(a, b):
    import gzip
    pages = gzip.open(os.path.join(HERE, 'text/v2.txt.gz'), 'rt').read().split('\f### ')[1:]
    out = []
    for pg in pages[a:b]:
        i, body = pg.split('\n', 1)
        for c in body.split('\n||\n'):
            ls = [l.strip() for l in c.split('\n') if l.strip()]
            if ls and re.match(r'^[\W\dIVXLivxl]{0,6}\s*(DOMINICA|INFRA|IN |FERIA|SABBATO|DIE |PER OCT)', ls[0]): ls = ls[1:]
            out.append('\n'.join(ls))
    t = '\n'.join(out); t = re.sub(r'-\n(\S)', r'\1', t); t = re.sub(r'\s+', ' ', t)
    t = R.fix_ocr(t)
    t = re.sub(r'Lec\s?\.?tio', 'Lectio', t); t = re.sub(r'Lectio i v\.', 'Lectio iv.', t); t = re.sub(r'Lectio in\.', 'Lectio iii.', t)
    return t

# ---------- Sanctorale ----------
MONTHS = {'januarii': 1, 'jan': 1, 'februarii': 2, 'febr': 2, 'martii': 3, 'aprilis': 4, 'apr': 4, 'maii': 5, 'maji': 5, 'junii': 6, 'julii': 7,
          'augusti': 8, 'aug': 8, 'septembris': 9, 'sept': 9, 'octobris': 10, 'novembris': 11, 'nov': 11, 'decembris': 12, 'dec': 12}
SHEAD = re.compile(r'(?:Die|DIE)\s+([IVXLivxlj\. ]{1,12})\s*(Januarii|Februarii|Martii|Aprilis|Maii|Maji|Junii|Julii|Augusti|Septembris|Octobris|Novembris|Decembris)\.\s*(.{0,160}?)(?=\s(?:Ad (?:I\. )?Vesperas|Ad Matutinum|Oratio|Invitatorium|Omnia de Communi|Lectio|In I\. Nocturno|Memoria|Commemoratio))', re.I)
def roman(s):
    s = s.lower().replace('j', 'i').replace(' ', '').replace('.', '')
    v = {'i': 1, 'v': 5, 'x': 10, 'l': 50}; n = 0
    for i, c in enumerate(s):
        if c not in v: return None
        n += -v[c] if i + 1 < len(s) and v.get(s[i + 1], 0) > v[c] else v[c]
    return n
FULLDAY = re.compile(r'DIE\s.*(?:ARII|ARTII|PRILIS|MAII|MAJI|UNII|ULII|USTI|BRIS)\b', re.I)
def is_head(l):
    """running head of a Sanctorale column: short, mostly capitals ('S. FELICIS DE VAT.OIS.', 'JACOBI DE BENEFACTIS, 685', 'DIE XXIX. NOY. 15,')"""
    if len(l) > 60 or FULLDAY.search(l): return False
    let = [c for c in l if c.isalpha()]
    return len(let) >= 4 and sum(c.isupper() for c in let) >= 0.6 * len(let)
def caps_line(l):
    let = [c for c in l if c.isalpha()]
    return len(let) >= 4 and sum(c.isupper() for c in let) >= 0.6 * len(let)
OCRDIR = '/tmp/b09/ocr'   # tools/b09/reocr.sh: tesseract (lat, best) at 300 dpi of the text PDFs, one txt per pdf page
ACC = str.maketrans('üïöàèìòùÜâêîôûäãõñ', 'úíóáéíóúÚáéíóúááón')
def ocr_page(vol, p):
    f = os.path.join(OCRDIR, '%s-%04d.txt' % (vol, p))
    if not os.path.exists(f): return None
    ls = [l.strip() for l in open(f, encoding='utf-8').read().split('\n')]
    ls = [re.sub(r'\s*[|\[\]{}]+\s*$', '', l).strip() for l in ls]; ls = [l for l in ls if l]
    k = 0
    while k < len(ls) and k < 3 and (re.match(r'^[\W\dIl]{1,8}$', ls[k]) or is_head(ls[k]) or (FULLDAY.search(ls[k]) and len(ls[k]) < 60)): k += 1
    return ls[k:]
def rejoin(m):
    import latcount as LC, latdict as LD
    a, b = m.group(1), m.group(2)
    if LC.N.get(LD.base(a + b), 0) >= 2 and LC.N.get(LD.base(a), 0) < 200: return a + b
    return m.group(0)
def text_ocr(vol, a, b):
    """the Sanctorale text from the tesseract re-OCR (page index a..b as in text_sancti: pdf page = index + 1); None if a page is missing"""
    out = []
    for i in range(a, b):
        ls = ocr_page(vol, i + 1)
        if ls is None: return None
        out.append('\n'.join(ls))
    t = '\n'.join(out).translate(ACC)
    t = re.sub(r'(\w)-\n(\w)', r'\1\2', t)
    t = re.sub(r'([A-Za-zÀ-ÿ]{2,})[.,]\n([a-zà-ÿ]{2,})', rejoin, t)   # a line-end hyphen read as a period
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'\b[KRBEFI][RKrk7y]?\.\s?(?=(?:[ivxj]+\.\s)?[A-ZÁÉÍÓÚÆ])', lambda m: m.group(0) if m.group(0).strip() in ('B.', 'E.', 'F.', 'I.') else '℟. ', t)
    t = re.sub(r'(?<=[.,:;!?»] )[YVy¥]\s?[.,]\s?(?=[A-ZÁÉÍÓÚÆ])', '℣. ', t)
    t = re.sub(r'\bA[nñfi][aàá]\.', 'Ana.', t)
    t = R.fix_ocr(t)
    return t
def text_sancti(vol, a, b):
    if os.environ.get('REOCR', '1') == '1':
        t = text_ocr(vol, a, b)
        if t: return t
    import gzip
    pages = gzip.open(os.path.join(HERE, 'text/%s.txt.gz' % vol), 'rt').read().split('\f### ')[1:]
    out = []
    for pg in pages[a:b]:
        i, body = pg.split('\n', 1)
        for c in body.split('\n||\n'):
            ls = [l.strip() for l in c.split('\n') if l.strip()]
            # a 'DIE II. DECEMBRIS. B.' line at the top of a column is the running head unless the saint's title (capitals) follows it
            while ls and (is_head(ls[0]) or re.match(r'^[\W\d]{1,8}$', ls[0]) or
                          (FULLDAY.search(ls[0]) and len(ls[0]) < 60 and len(ls) > 1 and not caps_line(ls[1]))): ls = ls[1:]
            out.append('\n'.join(ls))
    t = '\n'.join(out); t = re.sub(r'-\n(\S)', r'\1', t); t = re.sub(r'\s+', ' ', t)
    t = R.fix_ocr(t)
    t = re.sub(r'Lec\s?\.?tio', 'Lectio', t); t = re.sub(r'Lectio i v\.', 'Lectio iv.', t); t = re.sub(r'Lectio in\.', 'Lectio iii.', t)
    return t
def sanctorale(vol, a, b):
    t = text_sancti(vol, a, b)
    hs = []
    plain = t.translate(str.maketrans('áéíóúýÁÉÍÓÚǽ', 'aeiouyAEIOUæ'))
    for m in SHEAD.finditer(plain):
        d = roman(m.group(1)); mo = MONTHS.get(m.group(2).lower())
        if d and mo and 1 <= d <= 31: hs.append((m.start(), '%02d-%02d' % (mo, d), clean(t[m.start(3):m.end(3)])))
    out = collections.OrderedDict(); seen = collections.Counter()
    for i, (s, md, title) in enumerate(hs):
        e = hs[i + 1][0] if i + 1 < len(hs) else len(t)
        if i + 1 < len(hs) and hs[i + 1][1] == md and hs[i + 1][2] == title: continue
        seen[md] += 1; k = 'S:%s:%d' % (md, seen[md])
        o = parse_office(t[s:e]); o['title'] = title
        m = re.search(r'(Totum Duplex|Duplex(?: majus)?|Semiduplex|Simplex|Trium Lectionum|iij\. Lect\w*|Memoria)', title + ' ' + t[s:s + 400])
        if m: o['rank'] = m.group(1)
        out[k] = o
        print(k, '|', title[:60], '|', o.get('rank'), '|', ','.join(x for x in o if x not in ('title', 'rank')), len(o.get('lessons', [])))
    return out
if __name__ == '__main__':
    D = json.load(open(OUT)) if os.path.exists(OUT) else {}
    job = sys.argv[1]
    if job == 'tempora1': D.update(temporale('v1', 284, 768))
    if job == 'tempora2': D.update(temporale('v2', 242, 476))
    if job == 'sancti1': D.update(sanctorale('v1', 768, 1577))
    if job == 'sancti2': D.update(sanctorale('v2', 476, 1369))
    json.dump(D, open(OUT, 'w'), ensure_ascii=False)
