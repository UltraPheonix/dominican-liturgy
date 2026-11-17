"""Read the chants and readings of every Mass from the St. Dominic Missal (Latin-English, 1959).

Each page prints the same text in English (above) and Latin (below).  On every page the English part
labels (Office, Responsory, Alleluia, Tract, Sequence, Offertory, Communion), which follow the Mass
headings, are aligned with the Latin labels (Officium, Responsorium, ...), so each Latin chant gets the
Mass of its English counterpart.  Reading references come from the English labels ("Epistle. Rom. 13,
11-14."; "Gospel, p. 75." points to another page).  "Mass: No. 13, p. 701, except the following" names
the Common that supplies the parts not printed.
Output: dm_masses.json
"""
import re, json, sys, io, unicodedata, difflib, os
_o = sys.stdout; sys.stdout = io.StringIO()
from build_temporale import groups
sys.stdout = _o

TXT = os.environ.get('DMTXT', '/home/claude/dl/txt/dm.txt')
PAGES = open(TXT, encoding='utf8', errors='replace').read().split('\f')

MON = {'jan': 0, 'feb': 1, 'mar': 2, 'apr': 3, 'may': 4, 'jun': 5, 'jul': 6, 'aug': 7, 'sep': 8, 'oct': 9, 'nov': 10, 'dec': 11}
HEAD = re.compile(r'^\s{0,40}(JAN|FEB|MARCH|MAR|APRIL|APR|MAY|JUNE|JULY|AUG|SEPT|OCT|NOV|DEC|Jan|Feb|March|Mar|April|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec)\.?\s?(\d{1,2})\s*[:.]?\s*[-—~]+\s*(.*?)\s*$')
COMMON = re.compile(r'^\s*\.?NO\.\s?(\d{1,2})\.\s*[_·.]?\s*(?:OF|op)\b')
EN = [('in', r'^\s*(Office|Introit)\.'), ('gr', r'^\s*(Responsory|Gradual)\.'), ('al', r'^\s*Alleluia,\s*alleluia!'),
      ('tr', r'^\s*Tract\.'), ('se', r'^\s*Sequence\.'), ('of', r'^\s*Offertory\.'), ('co', r'^\s*Communion\.')]
LA = [('in', r'^\s*Officium\.'), ('gr', r'^\s*(Responsorium|Graduale)\.'), ('al', r'^\s*Alleluia,\s*alleluia\.'),
      ('tr', r'^\s*Tractus\.'), ('se', r'^\s*Sequentia\.(?!\s*sancti)'), ('of', r'^\s*Offertorium\.'), ('co', r'^\s*Communio\.')]
EN = [(p, re.compile(r)) for p, r in EN]
LA = [(p, re.compile(r)) for p, r in LA]
READ = re.compile(r'^\s*[^A-Za-z]{0,3}(Epistle|Lesson|Gospel)\s*([.,:]?)\s*(.*)$')
RUNNING = re.compile(r'^\s*\d{1,4}\s{3,}\S|\S\s{3,}\d{1,4}[\'.]?\s*$|^\s*\d{1,4}\s*$')
TEMPHEAD = re.compile(r'^\s{4,}((?:[A-Z][A-Z\'\.]*[ ,\-]+){1,9}[A-Z][A-Z\'\.]*)\s*$')
TEMP_WORDS = re.compile(r'SUNDAY|WEEK|DAY|VIGIL|ADVENT|LENT|EASTER|PENTECOST|EPIPHANY|NATIVITY|CHRISTMAS|ASCENSION|SEPTUAGESIMA|SEXAGESIMA|QUINQUAGESIMA|PASSION|EMBER|ROGATION|CORPUS|TRINITY|HEART|KING|CIRCUMCISION|HOLY NAME|HOLY FAMILY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|ASH', re.I)
SKIP_HEAD = re.compile(r'PROPER OF|CONTENTS|ORDINARY|COMMON OF|PREFACE|CANON|PART [IV]+|MEMORY OF|COMMEMORATION OF', re.I)


def flat(s):
    s = s.replace('æ', 'ae').replace('œ', 'oe').replace('j', 'i').replace('J', 'i')
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z]', '', s)


masses, cur = [], None


def new_mass(kind, key, title, page):
    global cur
    cur = {'kind': kind, 'key': key, 'title': title, 'page': page, 'pages': [page], 'ref': None, 'refPasch': None,
           'refpage': None, 'labels': [], 'readings': [], 'la': []}
    masses.append(cur)


region = 'tempore'
last_head = ''
for pno, text in enumerate(PAGES):
    lines = text.split('\n')
    # the printed page number
    page = None
    for l in lines[:3] + lines[-3:]:
        m = re.search(r'(?:^\s*|\s{3,})[i1l]?(\d{1,4})[\'.]?\s*$', l) or re.match(r'^\s*(\d{1,4})\s{3,}', l)
        if m and len(l.strip()) < 75:
            page = int(m.group(1)); break
    en_on_page, la_on_page = [], []
    for i, l in enumerate(lines):
        if re.search(r'NO\. ?1\. OF ONE MARTYR', l):
            region = 'commune'
        if region == 'commune' and re.search(r'PROPER\s+OF\s+THE\s+SAINTS', l) and not RUNNING.search(l):
            pass
        m = COMMON.match(l)
        if m:
            region = 'commune' if region == 'tempore' else region
            n = int(m.group(1))
            if not cur or cur['key'] != 'No%d' % n:
                new_mass('common', 'No%d' % n, 'No. %d' % n, page)
            continue
        m = HEAD.match(l)
        if m and int(m.group(2)) <= 31 and len(m.group(3)) > 2 and region != 'tempore':
            region = 'sanctorum'
            mon = MON.get(m.group(1).lower()[:3])
            key = '%02d%02d' % (mon + 1, int(m.group(2)))
            name = re.sub(r'\s+[i1l]?\d{3,4}[\'.]?\s*$', '', m.group(3)).strip()
            is_running = bool(re.search(r'\s{3,}[i1l]?\d{3,4}[\'.]?\s*$', l)) or l.lstrip()[:3].isupper() and cur and cur['key'] == key
            if not is_running and (not cur or cur['key'] != key or flat(name)[:10] != flat(cur['title'])[:10]):
                new_mass('saint', key, name, page)
            continue
        if region == 'tempore' and pno > 20:
            m = TEMPHEAD.match(l)
            if m and not RUNNING.search(l) and TEMP_WORDS.search(m.group(1)) and not SKIP_HEAD.search(m.group(1)):
                last_head = m.group(1).strip()
                continue
            if EN[0][1].match(l):
                new_mass('tempore', 'T%d' % len(masses), last_head, page)
        if cur is None:
            continue
        if page and page not in cur['pages']:
            cur['pages'].append(page)
        m = re.search(r'Mass:\s*(?:No\.\s?(\d+))?[,;]?\s*(?:p\.\s?(\d+))?(.{0,40})', l)
        if m and (m.group(1) or m.group(2)):
            ctx = (lines[i - 1] if i else '') + ' ' + l[:m.start()]
            if re.search(r'within\s+paschal|in\s+paschal\s+time', ctx, re.I) and not re.search(r'out\s*of\s*paschal', l[:m.start()], re.I):
                cur['refPasch'] = int(m.group(1)) if m.group(1) else cur['refPasch']
            elif cur['ref'] is None and cur['refpage'] is None:
                cur['ref'] = int(m.group(1)) if m.group(1) else None
                cur['refpage'] = int(m.group(2)) if m.group(2) else None
        r = READ.match(l)
        if r:
            pm = re.match(r'p\.\s?(\d+)', r.group(3))
            if pm:
                cur['readings'].append({'type': r.group(1), 'page': int(pm.group(1))})
            else:
                rest = re.sub(r'(?<=\d)[Oo]|[Oo](?=\d)', '0', r.group(3))
                rest = re.sub(r'(?<=[\d,\-])[lI](?=[\d,\-.])|(?<=\s)[lI](?=\d)', '1', rest).replace('..', '-').replace('~', '').replace('/(', 'k')
                rm = re.match(r'((?:[1-4]\s?)?[A-Z][A-Za-z]+\.?)\s*(\d+\s*[,.]\s*[\d\s,;\-–a-c]*\d[a-c]?)', rest)
                if rm:
                    cur['readings'].append({'type': r.group(1), 'book': rm.group(1).strip(), 'ref': re.sub(r'\s+', '', rm.group(2))})
        for p, rx in EN:
            if rx.match(l):
                ctx = ' '.join(lines[max(0, i - 2):i + 1]).lower()
                season = 'pasch' if (p == 'al' and re.search(r'paschal\s*time|easter', ctx)) else ''
                en_on_page.append((p, len(masses) - 1, season))
        for p, rx in LA:
            if rx.match(l):
                txt = rx.sub('', l, count=1) + ' ' + ' '.join(lines[i + 1:i + 3])
                txt = re.sub(r'^\s*(?:V\.|Y[fl]\.|[1lI]f\.|V/\.|Yf|Y\.)', '', txt.strip())
                la_on_page.append((p, flat(txt)))
    # align this page's Latin labels with its English labels
    a, b = [x[0] for x in en_on_page], [x[0] for x in la_on_page]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        for k in range(min(i2 - i1, j2 - j1)):
            if a[i1 + k] == b[j1 + k]:
                p, mi, season = en_on_page[i1 + k]
                masses[mi]['la'].append((p, la_on_page[j1 + k][1], season))
            elif cur is not None and tag != 'equal':
                pass
    # Latin labels left over on a page that belongs to a single Mass
    used = set()
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        for k in range(min(i2 - i1, j2 - j1)):
            if a[i1 + k] == b[j1 + k]:
                used.add(j1 + k)
    owners = {x[1] for x in en_on_page}
    if len(owners) <= 1 and cur is not None:
        mi = owners.pop() if owners else len(masses) - 1
        for j, (p, t) in enumerate(la_on_page):
            if j not in used:
                masses[mi]['la'].append((p, t, ''))

# ---- Latin incipit -> Graduale chant --------------------------------------------------------
PARTS = ['in', 'gr', 'al', 'tr', 'se', 'of', 'co']
chants = []
for g in groups:
    for c in g['chants']:
        t = 'gr' if c['code'] in ('re', 'gr') else c['code']
        if t in PARTS:
            inc = flat(re.sub(r'\(.*?\)|\.\.\..*$|….*$|<[^>]+>', '', c['incipit']))
            if len(inc) >= 4:
                chants.append((t, inc, c['id'], g['section'], c['page']))


def _ocr(s):
    return s.replace('rn', 'm').replace('ii', 'u').replace('li', 'h')


def match(part, text):
    text = re.sub(r'^(?:y[a-z]?|ii|ps|ri|iy)(?=[a-z]{8})', '', text) if not any(text.startswith(inc[:8]) for t, inc, cid, sec, pg in chants if t == part) else text
    best, bl = None, 0
    for t, inc, cid, sec, pg in chants:
        if t == part:
            k = min(len(inc), 16)
            if text.startswith(inc[:k]) and k > bl:
                best, bl = cid, k
    if best:
        return best
    T = _ocr(text)
    cand = []
    for t, inc, cid, sec, pg in chants:
        if t != part or len(inc) < 6:
            continue
        I = _ocr(inc)
        k = min(len(I), 16)
        r = max(difflib.SequenceMatcher(None, T[o:o + k], I[:k]).ratio() for o in range(0, 3))
        cand.append((r, k, cid))
    cand.sort(reverse=True)
    return cand[0][2] if cand and cand[0][0] >= 0.8 and cand[0][1] >= 7 else None


unmatched = []
for m in masses:
    m['parts'], m['season'] = {}, {}
    for p, text, season in m.pop('la'):
        cid = match(p, text)
        if cid is None:
            unmatched.append((masses.index(m), m['title'][:30], p, text[:60]))
            continue
        if season == 'pasch' and p == 'al':
            m['season'].setdefault('pasch', {}).setdefault('al', [])
            if cid not in m['season']['pasch']['al']:
                m['season']['pasch']['al'].append(cid)
        else:
            lst = m['parts'].setdefault(p, [])
            if cid not in lst:
                lst.append(cid)
    m.pop('labels', None)

json.dump({'masses': masses, 'unmatched': unmatched}, open('dm_masses.json', 'w'), ensure_ascii=False, indent=0)
from collections import Counter
print('masses', len(masses), Counter(m['kind'] for m in masses))
print('with an Introit', sum(1 for m in masses if m['parts'].get('in')), '; with a Mass reference', sum(1 for m in masses if m['ref'] or m['refpage']))
print('readings', sum(len(m['readings']) for m in masses), '; Latin chants not matched', len(unmatched))
