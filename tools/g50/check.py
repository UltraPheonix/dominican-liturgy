"""Full check of the saints' chants against the Graduale O.P. (1950) itself.
Reads the OCR of the sanctoral (tools/g50/ocr.tgz: tesseract -l ita of pdf pp. 380-760 at 250 dpi), splits it at each
'Die N MENSIS' heading, and for each feast works out what the Graduale sings:
  - references:  "Officium Os justi, pag. 42*.", "Responsorium In lege, pag. 503.", "Allelúia. V. Inveni David, pag. 34*."
                 "Missa X, de Communi ..., pag. 42*" (the whole Common Mass), "Missa ... ut in die ..., pag. N"
  - chants printed in the block: GregoBase source 14 chants on its pages whose text is in the block's OCR.
Then compares with the site's Mass for that day (data/masses.js). Report: tools/g50/check_report.txt, data: /tmp/x/g50.json"""
import re, json, os, tarfile, io, sqlite3, unicodedata, difflib
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
D = json.loads(open(R + '/data/masses.js').read().split('var DOMINICAN = ', 1)[1].rstrip().rstrip(';'))
tf = tarfile.open(R + '/tools/g50/ocr.tgz')
OCR = {}
for m in tf.getmembers():
    k = re.search(r'o-(\d+)\.txt', m.name)
    if k: OCR[int(k.group(1))] = tf.extractfile(m).read().decode('utf8', 'replace')
def n(s): return ' '.join(re.sub(r'[^a-z ]', ' ', unicodedata.normalize('NFD', (s or '').lower().replace('æ','ae').replace('œ','oe').replace('ǽ','ae').replace('j','i').replace('y','i').replace('v','u')).encode('ascii','ignore').decode()).split())
def flat(s): return n(s).replace(' ', '')
# printed page number of each pdf page
def pno(i):
    if i >= 651: return '%d*' % (i - 650)
    for j in range(0, 12):
        for k in (i - j, i + j):
            t = OCR.get(k, '').strip().split('\n')[0] if OCR.get(k) else ''
            m = re.match(r'^\s*(\d{3})\b', t) or re.search(r'\b(\d{3})\s*$', t)
            if m and 0 < k - int(m.group(1)) < 30: return str(i - (k - int(m.group(1))))
    return '?'
PNO = {i: pno(i) for i in OCR}
# GregoBase source 14
c = sqlite3.connect(R + '/tools/gregobase/gb.sqlite')
GB = {}
for i, inc, part, pg, seq, g in c.execute('select c.id,c.incipit,c."office-part",s.page,s.sequence,c.gabc from gregobase_chants c join gregobase_chant_sources s on s.chant_id=c.id where s.source=14'):
    try: g = json.loads(g)
    except Exception: pass
    t = n(re.sub(r'<[^>]+>|[{}*]', ' ', re.sub(r'\([^)]*\)', '', g or '')))
    GB.setdefault(str(pg).replace(' ', ''), []).append({'id': i, 'inc': inc, 'p': part, 'seq': seq, 't': t})
PART = {'in': 'in', 're': 'gr', 'gr': 'gr', 'al': 'al', 'tr': 'tr', 'se': 'se', 'of': 'of', 'co': 'co'}
REFP = {'officium': 'in', 'responsorium': 'gr', 'graduale': 'gr', 'tractus': 'tr', 'sequentia': 'se', 'offertorium': 'of', 'communio': 'co'}
MON = {'jan': 1, 'feb': 2, 'mart': 3, 'apr': 4, 'mai': 5, 'jun': 6, 'jul': 7, 'aug': 8, 'sept': 9, 'oct': 10, 'nov': 11, 'dec': 12}
def mon(w):
    w = n(w).replace('u', 'u')
    for k, v in MON.items():
        if w.startswith(k.replace('j', 'i')) or w.startswith(k): return v
    return None
# the text of the sanctoral, with page markers
lines = []
for i in sorted(OCR):
    if i >= 651: continue
    for l in OCR[i].split('\n'): lines.append((i, l))
blocks = []
for j, (i, l) in enumerate(lines):
    m = re.match(r'^\W{0,3}D[il1I]e\s+(\d{1,2})\s+(?:ve[lL]\s+\d{1,2}\s+)?([A-Za-z]{3,})', l.strip())
    if not m or re.search(r'\s[-—]\s', l): continue
    mo = mon(m.group(2))
    if not mo: continue
    title = ' '.join(x.strip() for _, x in lines[j + 1:j + 3] if x.strip())[:90]
    blocks.append({'j': j, 'pdf': i, 'day': int(m.group(1)), 'month': mo, 'title': title})
for b, nb in zip(blocks, blocks[1:] + [None]):
    seg = lines[b['j']:(nb['j'] if nb else b['j'] + 120)]
    b['pdfs'] = sorted(set(i for i, _ in seg))
    b['pages'] = [PNO[i] for i in b['pdfs']]
    b['text'] = ' '.join(x.strip() for _, x in seg)
def pagekey(s):
    s = s.replace(' ', '').replace('’', '*').replace("'", '*').replace('°', '*')
    s = re.sub(r'[^0-9*]', '', s); return s
def gb_on(page, part, inc):
    """the chant of this part on that page whose text begins like inc"""
    cand = [x for x in GB.get(page, []) if PART.get(x['p']) == part or (part == 'gr' and x['p'] in ('re', 'gr'))]
    q = flat(inc)[:12]
    best = None
    for x in cand:
        t = flat(x['t']); t = re.sub(r'^(alleluia)+(u)?', '', t)
        r = max(difflib.SequenceMatcher(None, q, t[o:o + len(q)]).ratio() for o in range(0, 6))
        if best is None or r > best[0]: best = (r, x)
    return best[1]['id'] if best and best[0] > 0.6 else (cand[0]['id'] if len(cand) == 1 else None)
for b in blocks:
    T = b['text']; exp = {}; notes = []
    # the whole Mass from a Common or another feast
    mm = re.search(r'Missa\s+(.{2,40}?),?\s*(?:de|ut in|sicut in)\s+(.{0,70}?)pag\.?\s*([0-9]{1,3}\s*[*’\'°]?)', T)
    if mm: exp['_missa'] = [mm.group(1).strip(), mm.group(2).strip(), pagekey(mm.group(3))]
    for m in re.finditer(r'(Officium|Responsorium|Graduale|Tractus|Sequentia|Offertorium|Communio|All?el\S{0,6}\s*(?:[y.]\s*){0,3})\s+([^,.]{2,40}?)\s*,\s*(?:[^.]{0,40}?)pag\.?\s*([0-9]{1,3}\s*[*’\'°]?)', T):
        w = n(m.group(1)).split()[0] if n(m.group(1)) else ''
        part = REFP.get(w, 'al' if w.startswith('al') else None)
        if not part: continue
        pre = T[max(0, m.start() - 60):m.start()]
        if re.search(r'Temp\S*\s*(Resurr|Pasch|Ascens)|Paschal|In Missis votivis|II\.\s*$|I\.\s*$', pre): continue   # seasonal: checked apart
        pg = pagekey(m.group(3)); gid = gb_on(pg, part, m.group(2))
        exp.setdefault(part, []).append([m.group(2).strip(), pg, gid])
    # chants printed in this block
    ft = flat(T)
    for i in b['pdfs']:
        for x in GB.get(PNO[i], []):
            part = 'gr' if x['p'] == 're' else x['p']
            if part not in ('in', 'gr', 'al', 'tr', 'se', 'of', 'co'): continue
            t = flat(x['t']); t = re.sub(r'^(alleluia)+(u)?', '', t)
            if len(t) > 14 and t[:14] in ft and not any(e[2] == x['id'] for e in exp.get(part, [])):
                exp.setdefault(part, []).append(['(printed)', PNO[i], x['id']])
    b['exp'] = exp
# the site's Masses for each day
def words(s): return set(w for w in n(s).split() if len(w) > 3 and w not in ('confessoris', 'martyris', 'virginis', 'praed', 'episcopi', 'pontificis', 'sancti', 'beati'))
rep = []; out = []
for b in blocks:
    cands = [(k, m) for k, m in D['masses'].items() if m.get('month') == b['month'] - 1 and m.get('day') == b['day']]
    if not cands: rep.append('%2d.%02d %-50s  NO SITE MASS' % (b['day'], b['month'], b['title'][:50])); continue
    cands.sort(key=lambda km: -len(words(km[1]['title']) & words(b['title'])))
    k, m = cands[0]
    if not (words(m['title']) & words(b['title'])) and len(cands) > 1: rep.append('%2d.%02d %-50s  ? %s' % (b['day'], b['month'], b['title'][:50], [x[0] for x in cands]))
    site = {p: [str(x['id']) for x in v] for p, v in m.get('parts', {}).items()}
    for sv in m.get('season', {}).values():
        for p, v in sv.items(): site.setdefault(p, []); site[p] += [str(x['id']) for x in v]
    diff = []
    for p in ('in', 'gr', 'al', 'tr', 'se', 'of', 'co'):
        e = [str(x[2]) for x in b['exp'].get(p, []) if x[2]]
        if e and not set(e) & set(site.get(p, [])): diff.append('%s: Graduale %s  site %s' % (p, b['exp'][p], site.get(p)))
        if not e and b['exp'].get(p): diff.append('%s: Graduale %s (no GregoBase id)  site %s' % (p, b['exp'][p], site.get(p)))
    out.append({'key': k, 'title': m['title'], 'g': b['title'], 'pages': b['pages'], 'pdfs': b['pdfs'], 'exp': b['exp'], 'site': site, 'diff': diff})
    if diff: rep.append('%-8s %-45s p.%s %s\n   %s' % (k, m['title'][:45], b['pages'][0], b['exp'].get('_missa', ''), '\n   '.join(diff)))
open(R + '/tools/g50/check_report.txt', 'w').write('\n'.join(rep) + '\n')
json.dump(out, open('/tmp/x/g50.json', 'w'), ensure_ascii=False)
print(len(blocks), 'feasts in the Graduale;', sum(1 for o in out if o['diff']), 'with differences')
