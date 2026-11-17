"""Group the Graduale O.P. (1950) chants into Masses and align them to the Temporale.

Input:  graduale/index.csv (GregoBase source 14, in book order), roman_temporale.json (from jgabc)
Output: groups.json, temporale.json
"""
import csv, json, re, sys, unicodedata

IDX = sys.argv[1] if len(sys.argv) > 1 else 'sources/graduale_index.csv'
rows = list(csv.DictReader(open(IDX, encoding='utf8')))
roman = json.load(open('sources/roman_temporale.json'))

CODE = {'in': 'in', 're': 'gr', 'gr': 'gr', 'al': 'al', 'tr': 'tr', 'se': 'se', 'of': 'of', 'co': 'co'}


def norm(s):
    s = re.sub(r'<i>.*?</i>', ' ', s or '')
    s = s.replace('æ', 'ae').replace('œ', 'oe').replace('Æ', 'Ae').replace('j', 'i').replace('J', 'I')
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'\bps\.?\s.*$', '', s, flags=re.I)  # "Rorate... Ps. Caeli" -> Rorate
    s = re.sub(r'[^a-zA-Z ]+', ' ', s).lower()
    return ' '.join(s.split())


import difflib


def same(a, b, words=2):
    a, b = norm(a).split(), norm(b).split()
    if not a or not b:
        return False
    n = min(words, len(a), len(b))
    if a[:n] == b[:n]:
        return True
    k = min(3, len(a), len(b))
    x, y = ' '.join(a[:k]), ' '.join(b[:k])
    return difflib.SequenceMatcher(None, x, y).ratio() >= 0.88 and a[0][:4] == b[0][:4]


def page_key(p):
    star = p.endswith('*')
    p = p.rstrip('*')
    roman_num = re.fullmatch(r'[IVXL]+', p)
    if roman_num:
        return (0, 0)
    try:
        return (2 if star else 1, float(p))
    except ValueError:
        return (1, 0)


# ---- group chants into Masses: a new Mass starts at each Introit -----------------
groups, cur = [], None
front = {'title': 'Ad aspersionem aquae et toni communes', 'section': 'front', 'chants': []}
for r in rows:
    c = {'id': int(r['gregobase_id']), 'code': r['part_code'], 'part': CODE.get(r['part_code']),
         'incipit': re.sub(r'<[^>]+>', '', r['incipit']).strip(), 'page': r['page']}
    if c['code'] == 'in':
        cur = {'chants': [c], 'page': r['page'], 'introit': c['incipit']}
        groups.append(cur)
    elif cur is None:
        front['chants'].append(c)
    else:
        cur['chants'].append(c)

for i, g in enumerate(groups):
    g['gid'] = i
    pk = page_key(g['page'])
    if pk[0] == 2:
        g['section'] = 'commune' if pk[1] < 61 else ('defunctorum' if pk[1] >= 114 else 'votivae')
    elif pk[1] >= 369:
        g['section'] = 'sanctorum'
    else:
        g['section'] = 'tempore'

# split the Kyriale (and Requiem Kyrie) away from the Mass propers
kyriale = []
for g in groups + [front]:
    keep = []
    for c in g['chants']:
        (kyriale if c['code'] == 'ky' else keep).append(c)
    g['chants'] = keep

# ---- align Temporale (global sequence alignment) ---------------------------------
temp = [g for g in groups if g['section'] == 'tempore']
R = [rk for rk in roman if (rk['parts'].get('in') or [''])[0] and not re.search(r'(ss|_v|_sd|-lotio)$', rk['key'])]


def score(rk, g):
    rin = rk['parts']['in'][0]
    if same(g['introit'], rin, 2):
        return 3.0
    if same(g['introit'], rin, 1):
        return 1.5
    return -0.6


n, m = len(R), len(temp)
GAP_R, GAP_D = -0.05, -0.3
F = [[0.0] * (m + 1) for _ in range(n + 1)]
B = [[None] * (m + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    F[i][0] = F[i - 1][0] + GAP_R; B[i][0] = 'r'
for j in range(1, m + 1):
    F[0][j] = F[0][j - 1] + GAP_D; B[0][j] = 'd'
for i in range(1, n + 1):
    for j in range(1, m + 1):
        opts = [(F[i - 1][j - 1] + score(R[i - 1], temp[j - 1]), 'm'), (F[i - 1][j] + GAP_R, 'r'), (F[i][j - 1] + GAP_D, 'd')]
        F[i][j], B[i][j] = max(opts)
i, j, pairs = n, m, []
while i > 0 or j > 0:
    b = B[i][j]
    if b == 'm':
        pairs.append((R[i - 1], temp[j - 1])); i -= 1; j -= 1
    elif b == 'r':
        i -= 1
    else:
        j -= 1
pairs.reverse()
out, used = [], set()
for rk, g in pairs:
    sc = score(rk, g)
    conf = 'introit' if sc > 0 else 'position'
    used.add(g['gid'])
    out.append({'key': rk['key'], 'title': rk['title'], 'en': rk['en'], 'gid': g['gid'], 'roman': rk['parts'], 'conf': conf})
done = {o['key'] for o in out}
# Roman days whose Mass is repeated from another Dominican Mass (e.g. Sundays IV-VI after Epiphany)
for rk in R:
    if rk['key'] in done:
        continue
    cands = [g for g in temp if same(g['introit'], rk['parts']['in'][0], 2)]
    if cands:
        out.append({'key': rk['key'], 'title': rk['title'], 'en': rk['en'], 'gid': cands[0]['gid'], 'roman': rk['parts'], 'conf': 'shared'})
# ...and Roman days whose Dominican Mass is printed elsewhere in the book
done = {o['key'] for o in out}
for rk in R:
    if rk['key'] in done:
        continue
    cands = [g for g in groups if same(g['introit'], rk['parts']['in'][0], 2)]
    if cands:
        out.append({'key': rk['key'], 'title': rk['title'], 'en': rk['en'], 'gid': cands[0]['gid'], 'roman': rk['parts'], 'conf': 'shared'})
# Days where the Dominican Mass differs from the Roman one (checked against the Missale O.P.)
bypage = {g['page']: g for g in groups}
MANUAL = [  # key, after-key, latin, english, page
    ('Adv4', 'Adv3s', 'Dominica IV Adventus', '4th Sunday of Advent', '20'),
    ('Litaniis', 'Pasc5', 'In Litaniis Majoribus et Minoribus', 'Rogation Days (Major and Minor Litanies)', '234'),
    ('Pasc2w', 'Pasc2', 'Solemnitas S. Joseph', 'Solemnity of St Joseph', '365'),
    ('Quad5f', 'Quad5w', 'Septem Dolorum B.M.V. (Feria VI post Dom. Passionis)', 'Seven Sorrows of the BVM (Friday in Passion Week)', '358'),
    ('Quad5s', 'Quad5f', 'Sabbato post Dominicam Passionis', 'Saturday in Passion Week', '147'),
    ('AscVig', 'Litaniis', 'In Vigilia Ascensionis', 'Vigil of the Ascension', '237'),
    ('Pasc6s', 'Pasc6', 'Sabbato in Vigilia Pentecostes', 'Vigil of Pentecost', '76*'),
    ('Quad4w', 'Quad4t', 'Feria IV post Dominicam IV Quadragesimae', 'Wednesday in the 4th week of Lent', '76*'),
    ('Dedicatio', None, 'In Dedicatione Ecclesiae', 'Dedication of a Church', '353'),
]
romankeys = [rk['key'] for rk in roman]
for key, after, la, en, page in MANUAL:
    out = [o for o in out if o['key'] != key]
    rk = next((r for r in roman if r['key'] == key), {'parts': {}})
    out.append({'key': key, 'title': la, 'en': en, 'gid': bypage[page]['gid'], 'roman': rk['parts'], 'conf': 'shared' if page.endswith('*') else 'manual',
                'after': after})
    used.add(bypage[page]['gid'])
pos = {k: i for i, k in enumerate(romankeys)}
def sortkey(o):
    if o['key'] in pos:
        return (pos[o['key']], 0)
    if o.get('after') in pos:
        return (pos[o['after']], 1)
    return (10 ** 6, 0)
out.sort(key=sortkey)
order = None
json.dump({'groups': groups, 'front': front, 'kyriale': kyriale}, open('groups.json', 'w'), ensure_ascii=False)
json.dump(out, open('temporale_align.json', 'w'), ensure_ascii=False, indent=0)
unmatched = [g for g in temp if g['gid'] not in used]
print('groups', len(groups), 'tempore', len(temp), 'aligned', len(out), 'unmatched dominican', len(unmatched))
for o in out:
    g = groups[o['gid']]
    if o['conf'] != 'introit': print('  %-8s %-14s %-38s -> p.%s %s' % (o['conf'], o['key'], o['en'][:38], g['page'], g['introit']))
for g in unmatched:
    print('  UNMATCHED p.%s %s' % (g['page'], g['introit']))
missing = [rk['key'] + ' ' + str((rk['parts'].get('in') or [''])[0]) for rk in roman if rk['key'] not in {o['key'] for o in out}]
print('roman keys without dominican mass:', len(missing))
print('  ' + '\n  '.join(missing))
