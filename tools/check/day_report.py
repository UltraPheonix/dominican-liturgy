"""Read the output of day_audit.py and list the days that break a rule. usage: python3 tools/check/day_report.py /tmp/year.json"""
import sys, json, datetime, subprocess, collections
Y = json.load(open(sys.argv[1]))
K = json.loads(subprocess.run(['node', '-e', "global.window={};require('./data/kalendar39.js');console.log(JSON.stringify(window.KAL39))"], capture_output=True, text=True).stdout)
def easter(y):
    a = y % 19; b = y // 100; c = y % 100; d = b // 4; e = b % 4; f = (b + 8) // 25; g = (b - f + 1) // 3; h = (19 * a + b - d - g + 15) % 30
    i = c // 4; k = c % 4; l = (32 + 2 * e + 2 * i - h - k) % 7; m = (a + 11 * h + 22 * l) // 451; mo = (h + l - 7 * m + 114) // 31; da = (h + l - 7 * m + 114) % 31 + 1
    return datetime.date(y, mo, da)
RANK = {'Totum Duplex I classis': 7, 'Totum Duplex II classis': 6, 'Totum Duplex': 5, 'Duplex': 4, 'Semiduplex': 3, 'Novem Lectiones': 3, 'Tres Lectiones': 2, 'Simplex': 2, 'Vigilia': 2, 'Memoria': 1, 'Octava solemnis': 5, 'Octava solemnissima': 6}
P = collections.defaultdict(list)
for r in Y:
    d = datetime.date.fromisoformat(r['date']); E = easter(d.year); f = (d - E).days
    key = r['hash'][1:].split('&')[0]; parts = [x for x in r['parts'] if not x['extra']]
    have = collections.Counter(x['p'] for x in parts)
    sept = -63 <= f < 0; pasch = 0 <= f < 56; holy = -7 <= f <= -1
    tag = '%s %s %-10s' % (r['date'], 'MTWTFSS'[d.weekday()], key)
    if r['errors']: P['page errors'].append(tag + ' ' + r['errors'][0][:80])
    if holy: continue
    for p in ('in', 'of', 'co'):
        if not have[p]: P['missing ' + p].append(tag)
    if not (have['gr'] or have['tr'] or have['al'] >= 2): P['no Gradual/Tract/2 Alleluias'].append(tag)
    if sept and have['al']: P['Alleluia between Septuagesima and Easter'].append(tag)
    if pasch and f >= 7 and have['gr'] and not have['al']: P['Gradual without Alleluia in Paschaltide'].append(tag)
    if [x for x in parts if x['empty']]: P['chant not transcribed'].append(tag + ' ' + ','.join(x['p'] + ':' + x['inc'][:20] for x in parts if x['empty']))
    if [x for x in parts if x['noen']]: P['chant without English'].append(tag + ' ' + ','.join(x['p'] for x in parts if x['noen']))
    ks = [x['k'] for x in r['parts'] if x['p'] == 'oratio' and not x['extra']]
    for k in ('or', 'se', 'pc'):
        if k not in ks: P['missing oration ' + k].append(tag)
    if len(r['reads']) < 2: P['fewer than 2 readings'].append(tag + ' %d' % len(r['reads']))
    elif any(x['la'] < 20 or x['en'] < 20 for x in r['reads']): P['reading without Latin or English'].append(tag)
    # the calendar of 1939: the highest feast of the day with a Mass, against the Mass shown
    md = '%02d%02d' % (d.month, d.day); ent = [e for e in K.get(md, []) if e[2]]
    if ent:
        top = max(ent, key=lambda e: RANK.get(e[1], 0))
        if top[2] != key and RANK.get(top[1], 0) >= 4 and key not in [e[2] for e in ent]:
            P['the calendar has a Double or higher, the page shows another Mass'].append(tag + ' calendar: %s (%s)' % (top[0][:40], top[1]))
    if not ent and not (key.startswith(('Adv', 'Epi', 'Quad', 'Pasc', 'Pent', '7a', '6a', '5a', 'Emb', 'Nat', 'Jan', 'Dec')) or key in ('Litaniis', 'Asc', 'CorpusChristi', 'SCJ', 'ChristusRex')):
        P['a saint\'s Mass on a day the calendar has no feast'].append(tag)
for k, v in P.items():
    print('\n## %s (%d)' % (k, len(v)))
    for x in v[:200]: print('  ' + x)
    if len(v) > 40: print('  ... %d more' % (len(v) - 40))
