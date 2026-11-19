"""Masses of the Proper of Saints (and other sections) in the 1939 Missal, with their own Collect, Secret, Postcommunion."""
import re, json
L = open('m39lin.txt').read().split('\n')
MON = ['Januarii','Februarii','Martii','Aprilis','Maii','Junii','Julii','Augusti','Septembris','Octobris','Novembris','Decembris']
DIE = re.compile(r'^Die (\d(?: ?\d)?) (' + '|'.join(MON) + r')\b')
LAB = re.compile(r'^(Oratio|Secreta|Postcommunio)\s*$')
END = re.compile(r'(Per (?:eumdem )?Dominum[^.]*|Qui (?:vivis|tecum|cum Patre|cum Deo)[^.]*|Per Christum[^.]*)\.\s*$')
def is_title(l):
    if l.startswith('@@'): return False
    w = l.strip().split()
    if not w or not (re.match(r'^(S|SS|B|BB)\.', w[0]) or len(w) >= 2 or re.match(r'^(OMNIUM|IN|COMMEMORATIO|DEDICATIO|PATROCINII|CATHEDRA|CONVERSIO|VIGILIA)$', w[0])): return False
    s = re.sub(r'[^A-Za-z]', '', l)
    if re.match(r'^(FESTA|OREMUS|ALLELUIA|AMEN)', l.strip()): return False
    if len(s) >= 4 and sum(c.isupper() for c in s) >= 0.85 * len(s): return True
    # "S. VINCENTII Martyris (t. d.)": the name in capitals, the rest in small letters
    return bool(re.match(r'^(S|SS|B|BB)\.\s?[A-Z^]{3,}[A-Z^ .,]*\s+[A-Z][a-z]', l.strip()))
def clean(lines):
    t = ''
    for l in lines:
        l = l.rstrip()
        if t.endswith('\xad'): t = t[:-1] + l.lstrip()
        elif t.endswith('-') and not t.endswith(' -'): t = t[:-1] + l.lstrip()
        else: t += (' ' if t else '') + l.strip()
    t = re.sub(r'\s+', ' ', t).replace('\xad', '')
    t = re.sub(r'\s+([:;,.!?])', r'\1', t)
    return t.strip()
def prayer(i):
    """text of the prayer whose label is at line i"""
    out = []
    j = i + 1
    while j < len(L) and len(out) < 40:
        l = L[j]
        if l.startswith('@@PAGE'): j += 2 if j + 1 < len(L) and re.match(r'^\d{1,4}\s*$', L[j+1]) else 1; continue
        if re.match(r'^Festa \w+ \(|^\d{1,4}\s*$|^[A-Z]\s*$', l.strip()): j += 1; continue
        if LAB.match(l) or DIE.match(l) or re.match(r'^(De |Lectio|Officium|Sequentia|Graduale|Offertorium|Communio|Alleluia)', l): break
        out.append(l)
        if END.search(clean(out)): break
        j += 1
    return clean(out)
masses = []; cur = None; day = None; region = None
for i, l in enumerate(L):
    m = DIE.match(l)
    if m:
        day = (MON.index(m.group(2)), int(m.group(1).replace(' ', ''))); cur = None; continue
    if day and is_title(l) and not LAB.match(l) and not any(LAB.match(L[k]) or re.match(r'^(Officium|Lectio|Sequentia|Offertorium|Communio|Graduale)', L[k]) for k in range(max(0, i - 2), i)):
        prev = L[i-1] if i else ''
        if cur and cur['start'] >= i - 2 and not cur['pr']: cur['title'] += ' ' + l.strip(); continue
        cur = {'month': day[0], 'day': day[1], 'title': l.strip(), 'start': i, 'pr': {}, 'page': None}
        masses.append(cur); continue
    if cur is None: continue
    if 'comm' not in cur:
        cm = re.search(r'ut in\s+Comm[a-z.]*\s*(.{0,60}?)p(?:a)?g\.\s*(\d+\*?)', ' '.join(L[i:i + 2]))
        if cm and re.match(r'^Officium', l): cur['comm'] = cm.group(2); cur['commTxt'] = cm.group(1)
    mm = LAB.match(l)
    if mm:
        prev = L[i-1].strip()
        if prev.startswith('De ') or re.match(r'^(Pro |Alia |Ad )', prev): continue
        k = {'Oratio': 'or', 'Secreta': 'se', 'Postcommunio': 'pc'}[mm.group(1)]
        if k not in cur['pr']: cur['pr'][k] = prayer(i)
    if re.match(r'^(De .*|Pro .*|.*)\b(Oratio|Secreta|Postcommunio)$', l) and not LAB.match(l):
        pass
json.dump(masses, open('m39masses.json', 'w'), ensure_ascii=False, indent=0)
print(len(masses), sum(1 for m in masses if len(m['pr']) == 3), 'with all three')
for m in masses[:6]: print(m['month'], m['day'], m['title'], {k: v[:70] for k, v in m['pr'].items()})
