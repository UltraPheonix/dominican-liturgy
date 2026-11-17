"""Assemble the site's data file (data/masses.js) from the aligned Temporale and Sanctorale.

Every Mass lists its chants by part; each chant is a GregoBase ID of the Graduale O.P. (1950).
'inferred': the chant is not printed in this Mass's place in the Graduale (it is used again from
elsewhere in the book); it was found by the incipit the same day has in the Roman Graduale.
"""
import json, re, sys, io, csv, os
_o = sys.stdout; sys.stdout = io.StringIO()
from build_temporale import norm, same
sys.stdout = _o

G = json.load(open('groups.json'))
groups, front, kyriale = G['groups'], G['front'], G['kyriale']
temporale = json.load(open('temporale_align.json'))
sdates = {int(k): v for k, v in json.load(open('sanct_dates.json')).items()}
cal = json.load(open('calendar.json'))
lines = open('/home/claude/dl/txt/M39r.txt', encoding='utf8').read().split('\n')
_o = sys.stdout; sys.stdout = io.StringIO()
from build_sanctorale import bydate, find_common, GUESS
sys.stdout = _o

import resolve_m39 as R
ORDO = [o for o in json.load(open('ordo2026.json')) if not o['region']]
PARTS = ['in', 'gr', 'al', 'tr', 'se', 'of', 'co']
allchants = {}
for g in groups + [front]:
    for c in g['chants']:
        allchants[c['id']] = c
for c in kyriale:
    allchants[c['id']] = c


def ptype(c):
    return 'gr' if c['code'] in ('re', 'gr') else c['code']


def core(g, roman=None):
    taken, extras, seen_co, last, co_page = {}, [], False, None, None
    for c in g['chants']:
        t = ptype(c)
        if t not in PARTS:
            extras.append(c['id']); last = t; continue
        ok = False
        if t not in taken:
            ok = not seen_co or (roman is not None and t in roman) or (roman is None and c['page'] == co_page)
        elif t in ('gr', 'al', 'tr') and not seen_co and last == t:
            ok = True  # Ember days: several Graduals; Paschaltide: two Alleluias
        if ok:
            taken.setdefault(t, []).append({'id': c['id']})
        else:
            extras.append(c['id'])
        if t == 'co' and not seen_co:
            seen_co, co_page = True, c['page']
        last = t
    return taken, extras


def lookup(part, incipit):
    for c in allchants.values():
        if ptype(c) == part and same(c['incipit'], incipit, 2):
            return c['id']
    return None


masses, sections = {}, []


def add(key, m):
    masses[key] = m
    return key


# ---- Temporale ----------------------------------------------------------------
items = []
for t in temporale:
    g = groups[t['gid']]
    roman = t.get('roman') or {}
    taken, extras = core(g, roman if roman else None)
    if t['conf'] == 'shared':
        parts = {'in': taken.get('in', [])}
        for p in PARTS[1:]:
            ids = [lookup(p, inc) for inc in roman.get(p, [])]
            ids = [i for i in ids if i]
            parts[p] = [{'id': i, 'inferred': True} for i in ids]
        extras = []
    else:
        parts = dict(taken)
        for p in PARTS[1:]:
            if p not in parts and roman.get(p):
                ids = [i for i in (lookup(p, inc) for inc in roman[p]) if i]
                if ids:
                    parts[p] = [{'id': i, 'inferred': True} for i in ids]
    note = {'introit': None, 'manual': 'Mass identified from the Missale O.P.; it differs from the Roman Mass of this day.',
            'shared': 'This day repeats an Introit printed elsewhere in the Graduale (p. %s); the other chants were found by the incipits of the same day in the Roman Graduale.' % g['page']}[t['conf']]
    items.append(add(t['key'], {'title': t['title'], 'en': t['en'], 'page': g['page'], 'conf': t['conf'], 'note': note,
                                'parts': {p: v for p, v in parts.items() if v}, 'extras': extras}))
# Good Friday is printed inside the Holy Thursday Mass (pp. 171-180)
ht = masses.get('Quad6h')
if ht:
    gf_ids = [c['id'] for c in groups[[t for t in temporale if t['key'] == 'Quad6h'][0]['gid']]['chants'] if c['page'] in ('171', '173', '176', '178', '179', '180')]
    gf = {'tr': [{'id': i} for i in gf_ids if ptype(allchants[i]) == 'tr']}
    pos = items.index('Quad6h') + 1
    masses['Quad6f'] = {'title': 'Feria VI in Parasceve', 'en': 'Good Friday', 'page': '171', 'conf': 'manual',
                        'note': 'Tracts of the Mass of the Presanctified; the Improperia and antiphons of the Adoration of the Cross are under "Other chants".',
                        'parts': gf, 'extras': [i for i in gf_ids if ptype(allchants[i]) != 'tr']}
    items.insert(pos, 'Quad6f')
    ht['extras'] = [i for i in ht['extras'] if i not in gf_ids]
sections.append({'id': 'tempore', 'title': 'Proprium de Tempore', 'en': 'Proper of the Time', 'items': items})

# ---- Commune & votive Masses -------------------------------------------------------
COMMON_TITLES = {
    '1*': ('Commune Apostolorum', 'Common of Apostles'),
    '7*': ('Commune unius Martyris', 'Common of One Martyr'),
    '11*': ('Commune unius Martyris Pontificis', 'Common of a Martyr Bishop'),
    '15*': ('Commune unius Martyris Tempore Paschali', 'Common of One Martyr in Paschaltide'),
    '18*': ('Commune unius Martyris (alia Missa)', 'Common of One Martyr (another Mass)'),
    '21*': ('Commune plurimorum Martyrum', 'Common of Several Martyrs'),
    '25*': ('Commune plurimorum Martyrum (alia Missa)', 'Common of Several Martyrs (another Mass)'),
    '28*': ('Commune plurimorum Martyrum Tempore Paschali', 'Common of Several Martyrs in Paschaltide'),
    '30*': ('Commune Confessoris Pontificis (alia Missa)', 'Common of a Confessor Bishop (another Mass)'),
    '32*': ('Commune Confessoris Pontificis', 'Common of a Confessor Bishop'),
    '35*': ('Commune Doctorum', 'Common of Doctors'),
    '39*': ('Commune Confessoris non Pontificis', 'Common of a Confessor not a Bishop'),
    '42*': ('Commune Confessoris non Pontificis (alia Missa)', 'Common of a Confessor not a Bishop (another Mass)'),
    '45*': ('Commune Virginis et Martyris', 'Common of a Virgin Martyr'),
    '48*': ('Commune Virginis et Martyris (alia Missa)', 'Common of a Virgin Martyr (another Mass)'),
    '51*': ('Commune Sanctarum Mulierum', 'Common of Holy Women'),
    '55*': ('Commune Virginum', 'Common of Virgins'),
    '62*': ('Missa votiva de SS. Sacramento', 'Votive Mass of the Blessed Sacrament'),
    '64*': ('Missa votiva de D.N.J.C. Summo et Aeterno Sacerdote', 'Votive Mass of Christ the High Priest'),
    '68*': ('Missa votiva de Passione Domini', 'Votive Mass of the Passion'),
    '75*': ('Missa votiva de Spiritu Sancto', 'Votive Mass of the Holy Spirit'),
    '79*': ('Missa votiva de B. Maria Virgine (Salve sancta parens)', 'Votive Mass of Our Lady (Salve sancta parens)'),
    '82*': ('Missa votiva de B. Maria Virgine (Salve radix sancta)', 'Votive Mass of Our Lady (Salve radix sancta)'),
    '89*': ('Missa in electione Summi Pontificis', 'Mass for the Election of a Pope'),
    '93*': ('Missa pro Fidei propagatione', 'Mass for the Propagation of the Faith'),
    '104*': ('Missa tempore mortalitatis', 'Mass in Time of Pestilence'),
    '110*': ('Missa pro Sponso et Sponsa', 'Nuptial Mass'),
    '114*': ('Missa pro Defunctis', 'Mass for the Dead'),
}
citems, vitems = [], []
for g in groups:
    if g['section'] not in ('commune', 'votivae', 'defunctorum'):
        continue
    la, en = COMMON_TITLES.get(g['page'], ('Missa «%s»' % g['introit'], 'Mass "%s"' % g['introit']))
    taken, extras = core(g)
    key = 'C' + g['page'].replace('*', 's')
    add(key, {'title': la, 'en': en, 'page': g['page'], 'conf': 'graduale', 'note': None,
              'parts': taken, 'extras': extras, 'introit': g['introit']})
    (citems if g['section'] == 'commune' else vitems).append(key)
    g['key'] = key
sections.append({'id': 'commune', 'title': 'Commune Sanctorum', 'en': 'Commons of Saints', 'items': citems})
sections.append({'id': 'votivae', 'title': 'Missae Votivae et pro Defunctis', 'en': 'Votive Masses and Requiem', 'items': vitems})

# ---- Sanctorale -------------------------------------------------------------------
MON = ['Ian.', 'Feb.', 'Mart.', 'Apr.', 'Maii', 'Iun.', 'Iul.', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']
MEN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
proper_by_date = {}
for gid, d in sdates.items():
    if d['score'] >= 2:
        proper_by_date.setdefault((d['month'], d['day']), []).append(gid)
attached = set()
TEMPORAL = re.compile(r'NATIVITATIS DOMINI|NATIVITAS DOMINI|EPIPHANI|Infra Octavam|in Octava|VIGILIA$|Baptismatis|CHRISTI REGIS|Missa', re.I)


def common_ref(month, day):
    for t in bydate.get((month, day), []):
        m = re.search(r'Officium\s+([A-Z][^,\n]{2,40}?),?\s+(?:ut\s+in\s+Comm|in\s+Comm|de\s+Comm|ut\s+supra)', t)
        if m:
            return m.group(1).strip()
    return None


def feast_mass(f):
    mo, d = f['month'], f['day']
    for gid in proper_by_date.get((mo, d), []):
        return gid, 'proper', None
    ref = common_ref(mo, d)
    if ref:
        g = find_common(ref)
        if g:
            return g['gid'], 'common', ref
    for pat, inc in GUESS:
        if re.search(pat, f['name']):
            g = find_common(inc)
            if g:
                return g['gid'], 'guess', inc
            break
    return None, None, None


import unicodedata as _ud


def _w(s):
    s = ''.join(c for c in _ud.normalize('NFD', s) if not _ud.combining(c)).lower().replace('j', 'i').replace('æ', 'ae')
    return set(w for w in re.findall(r'[a-z]{4,}', s) if w not in ('sancti', 'sanctae', 'beati', 'beatae', 'virg', 'conf', 'mart', 'feria', 'missa', 'ordinis'))


def ordo_page(f):
    """The Missal page the 2026 Ordo gives for this feast (if it is celebrated in 2026)."""
    for o in ORDO:
        y, mo, d = map(int, o['date'].split('-'))
        if mo - 1 == f['month'] and d == f['day'] and (_w(o['name']) & _w(f['name'])):
            return o['m39']
    return None


TEMPORE_PAGES = lambda c: c['section'] == 'tempore'


def missal_mass(f, prefer):
    """Parts of the feast read from its page in the Missale O.P. 1939."""
    ref = ordo_page(f)
    if not ref:
        return None
    p = R.pdf_page(ref)
    parts, commref, seg = R.resolve(p, f['day'], f['month'], prefer)
    # a saint's Introit never comes from the Proper of the Time; a stray match there is OCR noise
    parts['in'] = [h for h in parts.get('in', []) if h[0]['section'] != 'tempore']
    if not parts['in']:
        return None
    return {'parts': parts, 'commref': commref, 'm39': ref}


sitems, bitems = [], []
for f in cal:
    if not f['beatus'] and TEMPORAL.search(f['name']):
        continue
    prefer = tuple(proper_by_date.get((f['month'], f['day']), []))
    mm = missal_mass(f, prefer)
    season = {}
    if mm:
        intro, isc = mm['parts']['in'][0][0], mm['parts']['in'][0][2]
        if prefer and groups[prefer[0]]['section'] == 'sanctorum' and not mm['commref']:
            gid, conf = prefer[0], 'missal'
        else:
            gid, conf = intro['gid'], 'missal'
        g = groups[gid]
        taken, extras = core(g)
        if g['section'] == 'commune' and gid != intro['gid']:
            pass
        # the Introit as the Missal gives it (e.g. without the Paschal alleluias)
        if intro['gid'] != gid or not taken.get('in'):
            if taken.get('in') and groups[gid]['section'] == 'sanctorum' and 'all' in allchants[taken['in'][0]['id']]['incipit']:
                season.setdefault('pasch', {})['in'] = taken['in']
            taken['in'] = [{'id': intro['id']}]
        # parts the Missal labels clearly override the Graduale's default
        for p, hits in mm['parts'].items():
            if p == 'in':
                continue
            for c, se, sc in hits:
                if sc < 2:
                    continue
                if p == 'al' and c['section'] == 'tempore':
                    se = 'pasch'
                if se == 'pasch':
                    if p == 'al':
                        season.setdefault('pasch', {}).setdefault('al', []).append({'id': c['id']})
                    continue
                elif se == 'lent' or p == 'tr':
                    season.setdefault('lent', {}).setdefault('tr', []).append({'id': c['id']})
                else:
                    if p not in [k for k in taken if taken.get(k) and k + '_set' in taken]:
                        taken[p] = []
                        taken[p + '_set'] = True
                    taken[p].append({'id': c['id']})
        for k in [k for k in taken if k.endswith('_set')]:
            del taken[k]
        if season.get('pasch', {}).get('al') and len(season['pasch']['al']) > 2:
            season['pasch']['al'] = season['pasch']['al'][:2]
        if 'tr' in taken and taken.get('al'):
            season.setdefault('lent', {})['tr'] = taken.pop('tr')
        # one Gradual, Alleluia, Offertory and Communion: alternatives from the Common go to the extras
        for p in ('gr', 'al', 'of', 'co'):
            if len(taken.get(p, [])) > 1:
                extras = [c['id'] for c in taken[p][1:]] + extras
                taken[p] = taken[p][:1]
        ref = mm['commref']
        note = ('Chants as given on p. %s of the Missale O.P. 1939 (the page cited by the 2026 Ordo)' % mm['m39']) + \
               ((', from the Common (Missal p. %s).' % ref) if ref else '.')
        if gid in prefer:
            attached.add(gid)
    else:
        gid, conf, ref = feast_mass(f)
        if gid is None:
            continue
        g = groups[gid]
        taken, extras = core(g)
        note = {'proper': 'Proper Mass, Graduale p. %s (matched to this date in the Missale O.P. 1939).' % g['page'],
                'common': 'The Missale O.P. 1939 gives Officium «%s» for this day: %s.' % (ref, masses.get(g.get('key'), {}).get('en', 'Graduale p. %s' % g['page'])),
                'guess': 'Common chosen from the saint\'s title (%s): check the Ordo.' % (masses.get(g.get('key'), {}).get('en', ref))}[conf]
        if conf == 'proper':
            attached.add(gid)
        for p in ('gr', 'al', 'of', 'co'):
            if len(taken.get(p, [])) > 1:
                extras = [c['id'] for c in taken[p][1:]] + extras
                taken[p] = taken[p][:1]
        if 'tr' in taken and taken.get('al'):
            season.setdefault('lent', {})['tr'] = taken.pop('tr')
    date_la = '%d %s' % (f['day'], MON[f['month']])
    key = 'S%02d%02d' % (f['month'] + 1, f['day']) + ('b' if f['beatus'] else '')
    while key in masses:
        key += 'x'
    add(key, {'title': '%s — %s' % (date_la, f['name']), 'en': '%s %d — %s' % (MEN[f['month']], f['day'], f['name']),
              'rank': f['rank'], 'op': f['op'], 'page': g['page'], 'conf': conf, 'note': note,
              'parts': {k: v for k, v in taken.items() if v}, 'season': season,
              'extras': extras, 'month': f['month'], 'day': f['day']})
    (bitems if f['beatus'] else sitems).append(key)
# proper Masses of the Graduale not attached to a calendar date
for g in groups:
    if g['section'] != 'sanctorum' or g['gid'] in attached:
        continue
    d = sdates.get(g['gid'])
    taken, extras = core(g)
    key = 'G' + g['page'].replace('.', '_')
    when = (' (c. %d %s)' % (d['day'], MON[d['month']])) if d else ''
    add(key, {'title': 'Missa «%s»%s' % (g['introit'], when), 'en': 'Mass "%s", Graduale p. %s' % (g['introit'], g['page']),
              'page': g['page'], 'conf': 'graduale', 'note': 'A proper Mass of the Sanctorale that could not be tied to a date in the calendar automatically.',
              'parts': taken, 'extras': extras, 'month': d['month'] if d else 12, 'day': d['day'] if d else 0})
    sitems.append(key)


def liturgical(k):  # year begins with Advent (St Andrew)
    m = masses[k]
    mo = m['month'] if m['month'] < 12 else 13
    return ((mo - 10) % 12 if mo < 12 else 99, m['day'])


sitems.sort(key=liturgical)
bitems.sort(key=liturgical)
sections.insert(1, {'id': 'sanctorum', 'title': 'Proprium Sanctorum', 'en': 'Proper of the Saints', 'items': sitems})
sections.insert(2, {'id': 'beati', 'title': 'Beati Ordinis (Missae pro opportunitate)', 'en': 'Dominican Blesseds', 'items': bitems})

# ---- complete every Mass from the St. Dominic Missal (1959) ---------------------------
import dm_merge
st = dm_merge.merge(masses, sections, groups, allchants, core, json.load(open('sources_roman_lectiones.json')), None, None)
print('St. Dominic Missal:', st)
import complete
ROMAN_FILES, st2 = complete.run(masses, sections, groups, allchants, temporale, os.environ.get('JGABC', '/home/claude/src/jgabc'), os.environ.get('SITE', 'site'))
print('Completion from jgabc:', st2)

# ---- English names of the feasts, from the 2026 Ordo O.P. ---------------------------
for k, M in masses.items():
    if 'month' not in M or M['month'] > 11 or M.get('name_en'):
        continue
    for o in ORDO:
        y, mo, d = map(int, o['date'].split('-'))
        if mo - 1 == M['month'] and d == M['day'] and o.get('en') and (_w(o['name']) & _w(M['title'])):
            M['name_en'] = re.split(r'\s{2,}', o['en'].strip())[0].rstrip('.')
            break

# ---- corrections identified by hand -----------------------------------------------
FIX_TITLES = {'G494': ('Vigilia S. Ioannis Baptistae', 'Vigil of St John the Baptist', 5, 23),
              'G502_3': ('Vigilia Ss. Petri et Pauli', 'Vigil of Sts Peter and Paul', 5, 28)}
for k, (la, en, mo, dy) in FIX_TITLES.items():
    if k in masses:
        masses[k].update(title='%d %s — %s' % (dy, MON[mo], la), en='%s %d — %s' % (MEN[mo], dy, en), name_en=en, month=mo, day=dy, req=['in', 'gr', 'of', 'co'])
        masses[k].pop('note', None)
for s_ in sections:
    if s_['id'] == 'votivae' and 'C76s' in s_['items']:
        s_['items'].remove('C76s')
    if s_['id'] == 'sanctorum':
        s_['items'].sort(key=lambda k: liturgical(k))
if 'Pasc6s' in masses:
    al = [c for c in allchants.values() if c['code'] == 'al' and c['incipit'].lower().startswith('confitemini')]
    if al and not masses['Pasc6s']['parts'].get('al'):
        masses['Pasc6s']['parts']['al'] = [{'id': al[0]['id']}]
if 'S0709' in masses and len(masses['S0709'].get('readings') or []) < 2:
    masses['S0709']['readings'] = [{'type': 'Epistle', 'ref': 'Ad Hebræos 10: 32-38', 'roman': True}, {'type': 'Gospel', 'ref': 'Lucas 21: 9-19', 'roman': True}]

# ---- chants used -----------------------------------------------------------------
chants = {}
for c in allchants.values():
    chants[c['id']] = {'p': ptype(c) if ptype(c) in PARTS else c['code'], 'i': c['incipit'], 'pg': c['page']}
chants.update(ROMAN_FILES)
# English translations of the chants (St. Dominic Missal, 1959): text and scripture reference
TRANS = {}
for cid, t in json.load(open('dm_trans.json')).items():
    t = re.sub(r"(?:\s|^)(?:Y[fIl'1]?|J[I1l]|V/|Yf|y|Y|Ji|Yl|f|1/)\.\s*(?=[A-Z0-9])", ' ℣. ', ' ' + t).strip()
    t = re.sub(r'\.\.+', '.', t).replace('.,', '.').strip(' ,')
    t = re.sub(r'(?<=[a-z])\.(?=[a-z])', ' ', t)
    t = re.sub(r'\s*(Gospel|Epistle|Lesson|Collect|Secret|Postcommunion|Prayer)[,.]\s*p\.\s*\d+\.?.*$', '', t)
    t = re.sub(r"\s+['\"`]+\s*$", '', t).strip()
    m = re.match(r'^((?:Alleluia, alleluia!\s*)?)(?:℣\.\s*)?((?:[1-4]\s?)?[A-Z][a-z]{1,7}\.?\s*\d+[,;.]\s*[\d\-,. ]*\d\.?)\s*(.*)$', t)
    ref = ''
    if m:
        ref = m.group(2).strip().rstrip('.')
        t = (m.group(1) + ('℣. ' if m.group(1) else '') + m.group(3)).strip()
    TRANS[cid] = {'t': t, 'r': ref}
data_trans = TRANS
data = {'sections': sections, 'trans': data_trans, 'masses': masses, 'chants': chants,
        'kyriale': [c['id'] for c in kyriale], 'front': [c['id'] for c in front['chants']]}
import os
os.makedirs('site/data', exist_ok=True)
with open('site/data/masses.js', 'w', encoding='utf8') as f:
    f.write('// Generated by build_masses.py from the Graduale O.P. (1950, GregoBase source 14), the Missale O.P. (1939)\n')
    f.write('// and the Calendarium O.P. reformatum. Do not edit by hand; edit the build scripts.\n')
    f.write('var DOMINICAN = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
from collections import Counter
print({s['id']: len(s['items']) for s in sections})
print('sanctorale conf', Counter(masses[k]['conf'] for k in sitems + bitems))
print('with seasonal variants', sum(1 for k in sitems+bitems if masses[k].get('season')))
print('temporale inferred parts', sum(1 for k in items for p in masses[k]['parts'].values() for c in p if c.get('inferred')))
