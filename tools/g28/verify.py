"""Check the chants marked "inferred" in data/masses.js against the Graduale O.P. (1928): for each Mass, find its section
in the text layer of the scan, read what the book gives under each part label (the chant printed, or "pag. N" reference),
and compare with the site's chant (incipit, fuzzy: the text layer is OCR of notated text). Writes tools/g28/verify.txt.
Needs /tmp/g28pages.json (the text layer by printed page; see tools/g28/README)."""
import json, re, unicodedata, difflib, os
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(H))
P = json.load(open('/tmp/g28pages.json'))
D = json.loads(open(R + '/data/masses.js').read().split('var DOMINICAN = ', 1)[1].rstrip().rstrip(';'))
def norm(s):
    s = unicodedata.normalize('NFD', s); s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    s = s.replace('æ', 'ae').replace('œ', 'oe').replace('j', 'i').replace('v', 'u').replace('<5', 'o').replace('6', 'o')
    return re.sub(r'[^a-z]', '', s)
L = []
for p in P:
    pg = p['lines'][0] if p['lines'] else ''
    for i, l in enumerate(p['lines'][1:]): L.append((p['djvu'], p['half'], l))
LABEL = {'in': r'^OFFICIUM', 'gr': r'^(RESPONSORIUM|GRADUALE)', 'al': r'^ALLEL', 'tr': r'^TRACTUS', 'of': r'^OFFERTORIUM', 'co': r'^COMMUNIO', 'se': r'^SEQUENTIA'}
INLINE = {'in': r'Officium', 'gr': r'(Responsorium|Graduale)', 'al': r'Allel', 'tr': r'Tractus', 'of': r'Offertorium', 'co': r'Communio'}
def title_keys(t):
    t = re.sub(r'^\d+ \w+\. — ', '', t)
    t = unicodedata.normalize('NFD', t); t = ''.join(c for c in t if not unicodedata.combining(c)).lower().replace('æ', 'ae')
    return re.sub(r'[^a-z ]', ' ', t).split()
def find_start(title):
    k = [w for w in title_keys(title) if len(w) > 1 or w in ('i', 'v')]
    want = norm(' '.join(k))
    best = (0, None)
    for i in range(len(L)):
        txt = norm(' '.join(x[2] for x in L[i:i + 3]))
        if want in txt: r = 1.0 + (1 if norm(L[i][2])[:4] == want[:4] else 0)
        elif want[:12] in txt:
            r = difflib.SequenceMatcher(None, want, txt[txt.index(want[:12]):][:len(want)]).ratio()
        else: r = 0
        if r > best[0]: best = (r, i)
    return best
def section(i0):
    # from the title to the end of the Communio that follows
    j = i0; seen_co = False
    while j < len(L) and j < i0 + 400:
        if re.match(LABEL['co'], L[j][2].strip()): seen_co = True
        elif seen_co and (re.match(LABEL['in'], L[j][2].strip()) or re.match(r'^(Feria|Dominica|Sabbato|In |Die )', L[j][2].strip())): break
        j += 1
    return L[i0:j + 4]
def label_text(sec, part):
    out = []
    full = ' '.join(x[2] for x in sec)
    for mm in re.finditer(INLINE[part] + r'\s+([^,.]{3,40})', full): out.append(mm.group(0))
    for k, (_, _, l) in enumerate(sec):
        s = l.strip()
        if re.match(LABEL[part], s):
            out.append(' '.join(x[2] for x in sec[k + 1:k + 5]))
        elif re.match(INLINE[part] + r'\b', s):
            out.append(s)
    return out
lines = []; stats = {'ok': 0, 'ref': 0, 'diff': 0, 'nosec': 0}
items = [(k, p, x['id']) for k, m in D['masses'].items() for p, l in m.get('parts', {}).items() for x in l if isinstance(x, dict) and x.get('inferred')]
for k, part, cid in items:
    m = D['masses'][k]; inc = D['chants'].get(str(cid), {}).get('i', '?')
    r, i0 = find_start(m.get('title', ''))
    if (i0 is None or r < 0.95) and re.match(r'^S\d{4}', k):
        MO = ['IANUAR', 'FEBRUAR', 'MART', 'APRIL', 'MAI', 'IUNI', 'IULI', 'AUGUST', 'SEPTEMBR', 'OCTOBR', 'NOVEMBR', 'DECEMBR']
        mo, dd = int(k[1:3]), int(k[3:5])
        for i in range(len(L)):
            t = L[i][2].strip().upper().replace('J', 'I')
            mm = re.match(r'^DIE\s+(\d+)\s+([A-Z]+)', t)
            if mm and int(mm.group(1)) == dd and mm.group(2).startswith(MO[mo - 1][:4] if mo != 5 else 'MA'):
                if mo == 3 and not mm.group(2).startswith('MART'): continue
                if mo == 5 and not mm.group(2).startswith(('MAI', 'MAJ')): continue
                r, i0 = 1.0, i; break
    if i0 is None or r < 0.95:
        stats['nosec'] += 1; lines.append('NOSEC %-8s %s | %s | %s' % (k, part, inc, m.get('title'))); continue
    sec = section(i0); lt = label_text(sec, part)
    n = norm(re.sub(r'\(.*?\)|<[^>]+>', '', inc).split()[0] if inc.split() else inc)[:8]
    best = 0
    for t in lt:
        tn = norm(t)
        for a in range(0, max(1, len(tn) - len(n) + 1)):
            best = max(best, difflib.SequenceMatcher(None, n, tn[a:a + len(n)]).ratio())
            if best > 0.95: break
    st = 'OK' if best >= 0.78 else 'DIFF'
    stats['ok' if st == 'OK' else 'diff'] += 1
    lines.append('%-4s %-8s %s | %s | g28 p.%s/%s | %s' % (st, k, part, inc, sec[0][0], sec[0][1], ' // '.join(t[:70] for t in lt[:2])))
open(H + '/verify.txt', 'w').write('\n'.join(lines) + '\n' + json.dumps(stats) + '\n')
print(stats)
