"""Check the generated Office against the psalter rules of the Breviarium S.O.P. (1962),
Rubricae generales nn. 150-153 and the Compline rubric (Psalterium, Dominica ad Completorium)."""
import datetime as D
import glob, os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from parse import parse

SRC = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/dl/do_out'
PS = '/home/claude/src/do/web/www/horas/Latin/Psalterium/Psalmi'
DAYS = ['Dominica', 'Feria II', 'Feria III', 'Feria IV', 'Feria V', 'Feria VI', 'Sabbato']


def table(section):
    txt = open(f'{PS}/Psalmi minor.txt', encoding='utf-8').read()
    m = re.search(r'^\[' + section + r'\]\n(.*?)(?=^\[|\Z)', txt, re.S | re.M)
    lines = [l for l in m.group(1).split('\n') if l.strip()]
    out = {}
    for i in range(0, len(lines) - 1, 2):
        k = lines[i].split('=')[0].strip()
        out[k] = [p.strip() for p in re.sub(r'\[\d+\]', '', lines[i + 1]).split(',') if p.strip()]
    return out


MINOR = {h: table(h) for h in ('Prima', 'Tertia', 'Sexta', 'Nona', 'Completorium')}


def first_num(p):
    return re.match(r'\d+', p).group(0)


def psalms(rows):
    out = []
    for la, en in rows:
        for l in la.split('\n'):
            m = re.match(r'<r>Psalmus (\d+)(?:\(([^)]*)\))?', l)
            if m:
                out.append(m.group(1))
    return out


def cls_of(head):
    m = re.search(r'~\s*(I|II|III|IV)\. classis', head or '')
    return {'I': 1, 'II': 2, 'III': 3, 'IV': 4}.get(m.group(1)) if m else 4


def easter(y):
    a = y % 19; b = y // 100; c = y % 100; d = b // 4; e = b % 4; f = (b + 8) // 25; g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30; i = c // 4; k = c % 4; l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451; mo = (h + l - 7 * m + 114) // 31; da = ((h + l - 7 * m + 114) % 31) + 1
    return D.date(y, mo, da)


problems = collections.defaultdict(list)
n = 0
for f in sorted(glob.glob(f'{SRC}/*/*.Laudes.html')):
    ds = os.path.basename(f)[:10]
    d = D.date.fromisoformat(ds)
    y = d.year
    E = easter(y)
    fe = (d - E).days
    dow = (d.weekday() + 1) % 7   # 0 = Sunday
    get = lambda h: parse(open(f'{SRC}/{y}/{ds}.{h}.html', encoding='utf-8').read())
    try:
        L, P, T3, C, V = get('Laudes'), get('Prima'), get('Tertia'), get('Completorium'), get('Vespera')
    except FileNotFoundError:
        continue
    n += 1
    head = L['head'][0] if L['head'] else ''
    vhead = V['head'][0] if V['head'] else ''
    cls = cls_of(head)
    feria = bool(re.match(r'(Feria|Sabbato|Die |Dominica|In Vigilia|Hebdomad|Quattuor)', head)) and 'octav' not in head.lower()
    fcls = 9 if feria else cls   # rank used by the feast rules (ferias follow the ferial rules)
    sunday = dow == 0
    christmastide = (d.month == 12 and d.day >= 25) or (d.month == 1 and d.day <= 13)
    octaves = 0 <= fe <= 6 or 49 <= fe <= 55 or fe == 6
    triduum = -3 <= fe <= -1
    allsouls = d.month == 11 and d.day == 2 or (d.month == 11 and d.day == 3 and dow == 1)
    vcls = cls_of(vhead)
    first_vesp_feast = vhead and vhead != head and vcls == 1
    sat_before_sunday = dow == 6 and 'Dominica' in vhead
    # Compline
    want = MINOR['Completorium']['Dominica'] if (sunday or fcls <= 2 or christmastide or octaves or triduum or allsouls or first_vesp_feast) \
        else MINOR['Completorium'][DAYS[dow]]
    if sat_before_sunday and not (fcls <= 2 or christmastide or 0 <= fe <= 7):
        want = MINOR['Completorium']['Sabbato']
    got = psalms(C['rows'])
    if [first_num(p) for p in want] != got[:len(want)]:
        problems['Completorium'].append((ds, head[:50], got, [first_num(p) for p in want]))
    # Prime
    if not triduum:
        if (fcls == 1 or 0 <= fe <= 6) and not sunday:
            wantp = ['53', '118', '118']
        elif sunday:
            wantp = [first_num(p) for p in MINOR['Prima']['Dominica']]
        else:
            wantp = [first_num(p) for p in MINOR['Prima'][DAYS[dow]]]
        gotp = psalms(P['rows'])
        if gotp[:3] != wantp[:3] and not (sunday and gotp[:1] in (['53'], ['92'])):
            problems['Prima'].append((ds, head[:50], gotp, wantp))
    # Terce
    if not triduum:
        wantt = [first_num(p) for p in MINOR['Tertia']['Dominica' if (fcls == 1 or sunday or 0 <= fe <= 6) else DAYS[dow]]]
        gott = psalms(T3['rows'])
        if gott[:3] != wantt[:3]:
            problems['Tertia'].append((ds, head[:50], gott, wantt))
    # Lauds: I and II class feasts take the Sunday psalms (Lauds I)
    gotl = psalms(L['rows'])
    if fcls <= 2 and not sunday and not triduum and gotl[:1] not in (['92'], ['50']):
        problems['Laudes'].append((ds, head[:50], gotl, ['92', '99', '62', '148']))

print(n, 'days checked')
for h, ps in problems.items():
    print(f'\n{h}: {len(ps)} days differ')
    for p in ps[:12]:
        print('  ', p)
