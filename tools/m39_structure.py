"""Split the Temporale of the Missale O.P. 1939 into Masses and record what each contains."""
import re, json, sys
sys.path.insert(0, '/tmp')
from adj import flat
PAGES = list(range(35, 130)) + list(range(144, 198))
def clean(n):
    T = open('/home/claude/dl/m39cols/%d.txt' % n).read()
    return re.sub(r'[­-]\s*\n', '', T)
lines = []
for n in PAGES:
    for l in clean(n).split('\n'):
        lines.append((n, l.strip()))
masses = []; cur = None
for n, l in lines:
    if re.match(r'^Officium\b', l) or re.match(r'^Ad Missam\b', l):
        cur = {'page': n, 'lines': []}; masses.append(cur)
    if cur is not None: cur['lines'].append(l)
out = []
for m in masses:
    L = m['lines']; txt = '\n'.join(L)
    # introit text: the lines after "Officium"
    intro = flat(re.sub(r'^Officium\s*(Ps\.|P s\.|\w+\.)?\s*\d*', '', ' '.join(L[:4])))
    intro = re.sub(r'\d', '', intro)[:60]
    lessons = len(re.findall(r'(?m)^\W{0,3}Lectio\b', txt))
    gospel = len(re.findall(r'Sequentia sancti\s+Evangelii|Initium sancti\s+Evangelii|Passio Domini', txt))
    alls = len(re.findall(r'(?m)^\W{0,3}Alleluia, alleluia\.', txt))
    tract = len(re.findall(r'(?m)^\W{0,3}Tractus\b', txt))
    seq = len(re.findall(r'(?m)^\W{0,3}Sequentia\s*$|^\W{0,3}Sequentia\s+[A-Z]{2}', txt)) - len(re.findall(r'(?m)^\W{0,3}Sequentia sancti', txt))
    credo = bool(re.search(r'Credo\.', txt))
    off = bool(re.search(r'(?m)^\W{0,3}Offertorium', txt)); com = bool(re.search(r'(?m)^\W{0,3}Communio', txt))
    flect = len(re.findall(r'Flectamus genua', txt))
    out.append({'page': m['page'], 'intro': intro, 'head': ' '.join(L[:3])[:90], 'lessons': lessons, 'gospel': gospel, 'alleluia': alls,
                'tract': tract, 'seq': max(seq, 0), 'credo': credo, 'of': off, 'co': com, 'flectamus': flect})
json.dump(out, open('rubrics/m39_temporale_structure.json', 'w'), ensure_ascii=False, indent=0)
print(len(out))
for o in out: print(o['page'], o['head'][:60], '| L', o['lessons'], 'G', o['gospel'], 'A', o['alleluia'], 'T', o['tract'], 'S', o['seq'], 'C', int(o['credo']))
