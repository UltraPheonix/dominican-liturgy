"""Find the chants of each Mass on its page of the Missale O.P. (1939).

The Ordo gives the Missal page of every day's Mass.  On that page the Mass is printed with its parts
labelled ("Officium ...", "Graduale ...", "Offertorium ..."), whether the chant is proper or taken
"ut in Communi".  The OCR text of the page is searched for each label followed by the incipit of a
chant of the Graduale O.P. of that part.
"""
import re, json, os, sys, io, unicodedata
_o = sys.stdout; sys.stdout = io.StringIO()
from build_temporale import groups
sys.stdout = _o

PAGES = os.environ.get('M39PAGES', 'sources/m39pages')
NPDF = 463
MONTHS = ['ianuarii', 'februarii', 'martii', 'aprilis', 'maii', 'iunii', 'iulii', 'augusti', 'septembris',
          'octobris', 'novembris', 'decembris']


def flat(s, digits=False):
    s = s.replace('æ', 'ae').replace('œ', 'oe').replace('Æ', 'ae').replace('j', 'i').replace('J', 'i')
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z0-9]' if digits else r'[^a-z]', '', s)


page_text = {p: open('%s/%d.txt' % (PAGES, p), encoding='utf8').read() for p in range(1, NPDF + 1)}

# ---- printed page number -> PDF page -------------------------------------------
anchors = {'': [], '*': []}
for p, t in page_text.items():
    ls = t.split('\n')
    for l in ls[:6] + ls[-6:]:
        m = re.fullmatch(r'(\d{1,3})(\*?)', l.strip())
        if m:
            anchors[m.group(2)].append((int(m.group(1)), p))
anchors = {k: sorted(v) for k, v in anchors.items()}


def pdf_page(ref):
    m = re.match(r'(\d+)(\*?)', ref or '')
    if not m:
        return None
    n, star = int(m.group(1)), m.group(2)
    a = [x for x in anchors[star] if (star or 30 <= x[1] <= 370) and (not star or x[1] > 370)]
    if not a:
        return None
    best = min(a, key=lambda x: abs(x[0] - n))
    return max(1, min(NPDF, best[1] + round((n - best[0]) / 2)))


# ---- chants and their probes -------------------------------------------------------
PARTS = ['in', 'gr', 'al', 'tr', 'se', 'of', 'co']
LABEL = {'in': 'officium', 'gr': '(?:graduale|responsorium)', 'al': 'alleluia', 'tr': 'tractus',
         'se': '(?:sequentia|prosa)', 'of': 'offertorium', 'co': 'communio'}
chants = []
for g in groups:
    for c in g['chants']:
        t = 'gr' if c['code'] in ('re', 'gr') else c['code']
        if t in PARTS:
            inc = flat(re.sub(r'\(.*?\)|\.\.\..*$|….*$', '', c['incipit']))
            chants.append({'id': c['id'], 'part': t, 'inc': inc, 'page': c['page'], 'gid': g['gid'], 'section': g['section']})


LABELS_ANY = r'(?:officium|tractus|alleluia|offertorium|communio|sequentia|prosa)'
PSREF = r'(?:ps|is|eccli|ier|dan|cant|sap|eccl|prov|mal|ioel|hab|ion|mich|iob|reg|esth|iudith|tob|bar|ez|ezech)'


def season_of(f, pos):
    before = f[max(0, pos - 45):pos]
    if 'pasch' in before or 'ascens' in before:
        return 'pasch'
    if 'septuag' in before or 'quadrag' in before:
        return 'lent'
    return ''


def find_parts(text, prefer_gids=(), flat_text=None):
    """{part: [(chant, season, score)]}; season '' (per annum), 'lent' (Septuagesima-Lent) or 'pasch'."""
    f = flat_text if flat_text is not None else flat(text)
    found = {}
    for c in chants:
        inc = c['inc']
        if len(inc) < 5:
            continue
        probe = re.escape(inc[:12])
        m, score = re.search(LABEL[c['part']] + r'(?:[a-z]{0,10}?)' + probe, f), 2
        if not m and c['part'] == 'in' and len(inc) >= 8:
            m, score = re.search(re.escape(inc[1:13]), f), 1
        if not m and c['part'] == 'gr':
            pat = (PSREF if len(inc) >= 10 else 'ps') + probe
            for mm in re.finditer(pat, f):
                if not re.search(LABELS_ANY, f[max(0, mm.start() - 18):mm.start()]):
                    m, score = mm, 2
                    break
        if not m and c['part'] in ('al', 'se', 'of', 'co') and len(inc) >= 10:
            m, score = re.search(re.escape(inc[1:11]), f), 1
        if m:
            found.setdefault(c['part'], []).append((score, m.start(), c, season_of(f, m.start())))
    out = {}
    for p, hits in found.items():
        hits.sort(key=lambda h: (-h[0], h[1], h[2]['gid'] not in prefer_gids, h[2]['section'] != 'commune', len(h[2]['inc'])))
        chosen, seen = [], set()
        for h in hits:
            key = (h[2]['inc'][:12], h[3])
            if key in seen:
                continue
            if chosen and h[0] < 2:
                continue
            limit = {'al': 3, 'gr': 5}.get(p, 1)
            if sum(1 for x in chosen if x[1] == h[3]) >= (2 if (p == 'al' and h[3] == 'pasch') else (limit if p == 'gr' else 1)):
                continue
            chosen.append((h[2], h[3], h[0])); seen.add(key)
        chosen.sort(key=lambda x: f.find(x[0]['inc'][:12]))
        out[p] = chosen
    return out


COMMREF = re.compile(r'officium([a-z]{3,30}?)utin(?:comm|communi)[a-z]*?pag(\d{1,3})')


def resolve(p, day=None, month=None, prefer_gids=(), depth=0):
    seg = segment(p, day, month)
    parts = find_parts(None, prefer_gids, re.sub(r'\d', '', seg))
    # "Officium X, ut in Comm. ..., pag. N*": the Mass, or the parts not printed here, are those of the Common
    m = COMMREF.search(seg[:500])
    ref = None
    if m and depth == 0:
        ref = m.group(2) + '*'
        cp = pdf_page(ref)
        if cp:
            intro = (parts.get('in') or [[None]])[0][0]
            cseg = common_segment(cp, intro)
            cparts = find_parts(None, prefer_gids, cseg)
            for k, v in cparts.items():
                if k not in parts:
                    parts[k] = v
    return parts, ref, seg


def common_segment(p, intro):
    f = flat(page_text.get(p - 1, '') + page_text.get(p, '') + page_text.get(p + 1, ''))
    if intro is None:
        return f
    i = f.find(intro['inc'][1:13])
    if i < 0:
        return f
    j = f.find('officium', i + 400)
    return f[i: j if j > 0 else i + 7000]


def segment(p, day=None, month=None):
    """Text of the Mass that starts on PDF page p (and may run onto the next)."""
    t = page_text.get(p, '') + '\n' + page_text.get(p + 1, '')
    f = flat(t, digits=True)
    if day is None:
        return f
    key = 'die%d%s' % (day, MONTHS[month][:4])
    i = f.find(key)
    if i < 0:
        return flat(page_text.get(p, ''), digits=True)
    j = re.search(r'die\d{1,2}(?:ian|fe|mar|ap|mai|iu|au|se|oc|no|de)', f[i + 6:])
    seg = f[i: i + 6 + j.start()] if j else f[i:]
    return seg


if __name__ == '__main__':
    ordo = json.load(open('ordo2026.json'))
    for o in ordo:
        if o['region'] or not o['m39']:
            continue
        if not re.search(r'Agnetis|Agath|THOM|Thom|Vincentii Ferr|Petri M|DOMINICI|Hyacinth|Ros|Ludovici|Alberti|Catharin|Antonini|Raymundi|Martini de', o['name']):
            continue
        y, mo, d = map(int, o['date'].split('-'))
        p = pdf_page(o['m39'])
        parts, ref, seg = resolve(p, d, mo - 1)
        print(o['date'], o['name'][:38], 'M39', o['m39'], '-> pdf', p, 'seglen', len(seg), 'common', ref)
        for k in PARTS:
            if k in parts:
                print('    %s: %s' % (k, ' / '.join('%s%s (p.%s)%s' % (c['inc'][:22], ('['+se+']') if se else '', c['page'], '' if sc == 2 else '?') for c, se, sc in parts[k])))
