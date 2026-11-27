"""The prayers of the Memoriae of the Kalendarium (Missale O.P. 1939): each is printed in the Mass of its day as
"De S. N." Oratio / Secreta / Postcommunio. Finds the blocks in tools/orat39/m39lin.txt (the Missal's text layer) under the
"Die N Mensis" heading of the date (or the day before, for vigils printed there) and writes tools/orat39/memoriae_raw.json for
review. Run: python3 tools/orat39/memoriae.py"""
import json, re, os, subprocess
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(H))
L = open(H + '/m39lin.txt', encoding='utf8').read().split('\n')
K = json.loads(subprocess.check_output(['node', '-e', "global.window={};require('%s/data/kalendar39.js');console.log(JSON.stringify(window.KAL39))" % R]))
MON = ['Januarii', 'Februarii', 'Martii', 'Aprilis', 'Maji', 'Junii', 'Julii', 'Augusti', 'Septembris', 'Octobris', 'Novembris', 'Decembris']
# the date headings
heads = []
for i, l in enumerate(L):
    m = re.match(r'^Die\s+(\d(?: ?\d)?)\s+([A-Z][a-z]+)', l.strip())
    P3 = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'Mai': 5, 'Maj': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    if m and m.group(2)[:3] in P3:
        heads.append((i, '%02d%02d' % (P3[m.group(2)[:3]], int(m.group(1).replace(' ', '')))))
def section(md):
    out = []
    for j, (i, d) in enumerate(heads):
        if d == md: out.append((i, heads[j + 1][0] if j + 1 < len(heads) else len(L)))
    return out
KIND = {'Oratio': 'or', 'Secreta': 'se', 'Postcommunio': 'pc'}
END = re.compile(r'(Per\s*D[oó]\s*-?\s*mi|Per\s+eum|Per\s+eun|Qui\s+vivis|Qui\s+vivit|Qui\s+tecum|qui\s+tecum)')
STOP = re.compile(r'^(De |Oratio|Secreta|Postcommunio|Lectio|Sequentia|Graduale|Communio|Offertorium|Praefatio|Die |Officium|Alleluia|Tractus|Evangel|Initium|Memoria)')
def grab(a, b):
    """the "De S. ..." blocks between lines a and b: [(heading, kind, text)]"""
    res = []; i = a
    while i < b:
        l = L[i].strip()
        if re.match(r'^De (S|SS|B|BB)\.|^De (Inventione|Octava|Vigilia)|^De sanct|^Pro Octava|^De die Oct', l) or (re.match(r'^(SS?|BB?)\. ', l) and len(l) < 60 and i + 1 < b and re.match(r'^(Oratio|Secreta|Postcommunio)', L[i + 1].strip())):
            head = l; j = i + 1
            # the heading may run on one more line; the kind on the same line or the next
            km = re.search(r'(Oratio|Secreta|Postcommunio)\s*$', head)
            while not km and j < min(b, i + 3):
                n = L[j].strip()
                km = re.match(r'^(Oratio|Secreta|Postcommunio)\b', n)
                if km: j += 1; break
                head += ' ' + n; j += 1
                km = re.search(r'(Oratio|Secreta|Postcommunio)\s*$', n)
            if not km: i += 1; continue
            kind = KIND[km.group(1)]; txt = []
            while j < b:
                n = L[j].strip()
                if txt and STOP.match(n): break
                j += 1
                if not n or n.startswith('@@PAGE') or re.match(r'^(Festa|Proprium|\d+)\b.*\d', n) and len(n) < 40: continue
                txt.append(n)
                t = ' '.join(txt)
                if END.search(t) and re.search(r'(num|eumdem|eundem|Domi|regnas|Patre|saeculorum)[.:]?\s*$', n.rstrip(':')) : break
                if len(txt) > 25: break
            t = re.sub(r'\s*­\s*', '', ' '.join(txt)); t = re.sub(r'-\s+(?=[a-z])', '', t); t = re.sub(r'\s+', ' ', t)
            res.append((head, kind, t)); i = j; continue
        i += 1
    return res
def same(a, b):
    n = 0
    while n < min(len(a), len(b)) and a[n] == b[n]: n += 1
    return n >= 3 and n >= min(4, min(len(a), len(b)) - 1)
def stem(title):
    t = re.sub(r'^(SS?\.|BB?\.)\s*', '', title)
    t = re.sub(r'^(Octava)\s+(S\.|SS\.)?\s*', '', t)
    return re.sub(r'[^A-Za-z]', '', t.split()[0])[:4].lower()
out = {}
for md, es in K.items():
    for e in es:
        if e[1] != 'Memoria': continue
        st = stem(e[0])
        found = {}
        for d2 in (md, '%04d' % (int(md) - 1), '%04d' % (int(md) + 1)):
            for a, b in section(d2):
                for head, kind, t in grab(a, b):
                    hs = re.sub(r'^(De\s+)?(SS?\.|BB?\.)?\s*(Mm?\.|Mart\.)?\s*', '', head); hs = re.sub(r'^Inventione', 'Inventio', hs); hs = re.sub(r'^(sancto|sancta|sanctis)\s+', '', hs)
                    hs = re.sub(r'[^A-Za-z]', '', hs.split()[0] if hs.split() else '')[:4].lower()
                    if (same(hs, st) or (e[0].startswith('Octava') and re.match(r'^(De|Pro) (die )?Oct', head) and st in re.sub(r'[^a-z]', '', head.lower()))) and kind not in found:
                        found[kind] = {'t': t, 'head': head, 'from': d2, 'line': a}
            if len(found) == 3: break
        if len(found) < 3:
            for a, b in section(md):
                top = ' '.join(L[a:a + 8])
                if e[0].startswith('Octava') or 'Memoria' not in top or stem(e[0]) not in re.sub(r'[^a-z]', '', top.lower().replace('j', 'i')) and stem(e[0]) not in re.sub(r'[^a-z]', '', top.lower()): continue
                i = a
                while i < b:
                    km = re.match(r'^(Oratio|Secreta|Postcommunio)\b', L[i].strip())
                    if km and KIND[km.group(1)] not in found:
                        j = i + 1; txt = []
                        while j < b:
                            n = L[j].strip()
                            if txt and STOP.match(n): break
                            j += 1
                            if n and not n.startswith('@@PAGE'): txt.append(n)
                        t = re.sub(r'\s*\u00ad\s*', '', ' '.join(txt)); t = re.sub(r'-\s+(?=[a-z])', '', t); t = re.sub(r'\s+', ' ', t)
                        found[KIND[km.group(1)]] = {'t': t, 'head': 'own section', 'from': md, 'line': i}
                        i = j; continue
                    i += 1
        out['%s|%s' % (md, e[0])] = found
json.dump(out, open(H + '/memoriae_raw.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
full = sum(1 for v in out.values() if len(v) == 3); print(len(out), 'Memoriae;', full, 'with all three prayers')
for k, v in out.items():
    if len(v) < 3: print('  missing', k, sorted(v))
