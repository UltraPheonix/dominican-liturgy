"""Orationes ad diversa, Missale O.P. 1939 pp. 100*-113* (tools/orat39/m39lin.txt): parse the 38 sets of Oratio, Secreta,
Postcommunio from the OCR, clean, accent. Output raw.json for proofing."""
import re, json, sys, os
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H + '/../orat39'); os.chdir(H + '/../orat39')
import accent
L = open('m39lin.txt', encoding='utf8').read().split('\n')
a = next(i for i in range(79200, 79300) if L[i].startswith('1. Ad poscenda'))
b = next(i for i in range(80380, 80500) if L[i].startswith('Observandum'))
lines = [l for l in L[a:b] if not re.match(r'^(@@PAGE.*|\d+\*|Orationes ad diversa|Prsed\..*|Praed\..*)\s*$', l.strip())]
sets = []; cur = None; part = None
for l in lines:
    s = l.strip()
    m = re.match(r'^(\d{1,2})\.\s*(.*)$', s)
    if m and int(m.group(1)) == len(sets) + 1:
        cur = {'n': int(m.group(1)), 'title': m.group(2), 'or': '', 'se': '', 'pc': ''}; sets.append(cur); part = 'title'; continue
    if s in ('Oratio', 'Secreta', 'Postcommunio'): part = {'Oratio': 'or', 'Secreta': 'se', 'Postcommunio': 'pc'}[s]; continue
    if part == 'title' and cur['n'] == 2 and s.startswith('ACUNCTIS'): part = 'or'; cur['or'] += '\n' + s; continue
    if part == 'title': cur['title'] += ' ' + s
    elif part: cur[part] += '\n' + s
def clean(t):
    t = t.replace('­\n', '').replace('­\n', '')
    t = re.sub(r'-\s*\n', '', t).replace('\n', ' ')
    t = re.sub(r'\s+', ' ', t).strip()
    return t
for x in sets:
    x['title'] = clean(x['title'])
    for k in ('or', 'se', 'pc'):
        t = clean(x[k]); x[k + '_ocr'] = t
        acc, unk = accent.accent(t); x[k] = acc; x[k + '_unk'] = unk
json.dump(sets, open(H + '/raw.json', 'w'), ensure_ascii=False, indent=1)
print(len(sets))
for x in sets: print(x['n'], x['title'], '| unk:', x['or_unk'] + x['se_unk'] + x['pc_unk'])
