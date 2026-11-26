"""Graduale O.P. (1950), sanctoral: what each feast sings, read from the text layer of the scan (tools/g50/g_text.txt.gz,
pdftotext -layout of g.pdf; pages split by form feeds, index = pdf page - 1).
For each 'DIE n MENSIS' block: the references ("Officium Os justi, pag. 36*", "Missa X, de Communi ..., pag. N*") and the
parts printed in full (headings OFFICIUM, RESPONSORIUM, ALLELUIA, TRACTUS, SEQUENTIA, OFFERTORIUM, COMMUNIO) on its pages.
Output: tools/g50/feasts.json  [{pdf, page, day, month, name, refs: [[part, incipit, page]], printed: [part,...], text}]"""
import gzip, re, json, os
H = os.path.dirname(os.path.abspath(__file__))
P = gzip.open(H + '/g_text.txt.gz', 'rt').read().split('\f')
MON = {'IAN': 1, 'JAN': 1, 'FEB': 2, 'MART': 3, 'APR': 4, 'MAI': 5, 'IUN': 6, 'JUN': 6, 'IUL': 7, 'JUL': 7, 'AUG': 8, 'SEPT': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}
def mon(w):
    w = w.upper().replace('0', 'O').replace('1', 'I')
    for k, v in MON.items():
        if w.startswith(k): return v
    return None
# printed page numbers from the running heads, smoothed: printed = pdf - offset, offset constant over runs
def head_no(p):
    top = p.strip('\n').split('\n')[0] if p.strip() else ''
    m = re.match(r'^\s*(\d{2,3})\s', top) or re.search(r'\s(\d{2,3})\s*$', top)
    return int(m.group(1)) if m else None
off = {}
for i, p in enumerate(P):
    n = head_no(p)
    if n and 0 < (i + 1) - n < 40: off[i] = (i + 1) - n
def printed(i):
    near = sorted(off, key=lambda j: abs(j - i))[:5]
    vals = [off[j] for j in near]
    o = max(set(vals), key=vals.count) if vals else 14
    return (i + 1) - o
blocks = []
for i, p in enumerate(P):
    lines = p.split('\n')
    for j, l in enumerate(lines):
        s = l.strip()
        m = re.match(r'^DIE\s+(\d{1,2})\.?\s+([A-Z0-9]{3,})', s)
        if not m or ' - ' in s or '- ' in s[:20] and len(s) > 40: continue
        if j < 2: continue   # running head
        mo = mon(m.group(2))
        if not mo: continue
        name = next((x.strip() for x in lines[j + 1:j + 4] if x.strip()), '')
        blocks.append({'pdf': i + 1, 'line': j, 'day': int(m.group(1)), 'month': mo, 'name': name})
# text of each block: up to the next block
for b, nb in zip(blocks, blocks[1:] + [None]):
    ps = range(b['pdf'] - 1, (nb['pdf'] if nb else b['pdf'] + 1))
    chunks = []
    for i in ps:
        ls = P[i].split('\n')
        a = b['line'] if i == b['pdf'] - 1 else 1
        z = nb['line'] if nb and i == nb['pdf'] - 1 else len(ls)
        chunks.append('\n'.join(ls[a:z]))
    T = '\n'.join(chunks)
    b['page'] = printed(b['pdf'] - 1)
    b['pages'] = [printed(i) for i in ps]
    flat = ' '.join(T.split())
    refs = []
    for m in re.finditer(r'(Officium|Responsorium|Graduale|Tractus|Sequentia|Offertorium|Communio|Missa|Alle[l1I]+[uú]+ia\.?\s*[^A-Za-z]{0,4})\s+([A-Z][^.,;]{2,40}?)\s*[,.]\s*((?:ut|de|sicut|pag)[^.]{0,80}?(?:pag\.?\s*([0-9IlOo]{1,3}\s*\*?))?)[.;]', flat):
        part = m.group(1); part = 'Alleluia' if part.startswith('Alle') else part
        refs.append([part, m.group(2), m.group(3)[:90]])
    b['refs'] = refs
    b['printed'] = sorted(set(x for x in re.findall(r'\b(OFFICIUM|RESPONSORIUM|GRADUALE|ALLELUIA|TRACTUS|SEQUENTIA|OFFERTORIUM|COMMUNIO)\b', T)))
    b['text'] = flat[:1500]
json.dump(blocks, open(H + '/feasts.json', 'w'), ensure_ascii=False, indent=0)
print(len(blocks), 'feasts')
