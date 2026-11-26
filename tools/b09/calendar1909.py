"""The Calendarium of the 1909 Breviary (vol. 1 pdf 24-37) -> calendar1909.json {MM-DD: [{title, rank}]}; the first entry is
the Office of the day, the others commemorations (Memoria). Accents restored with latdict."""
import gzip, re, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from latdict import fix_line
MON = ['JANUARIUS', 'FEBRUARIUS', 'MARTIUS', 'APRILIS', 'MAJUS', 'JUNIUS', 'JULIUS', 'AUGUSTUS', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
RANK = r'(Totum\s+Duplex|Duplex|Semiduplex|Simplex|Tres\s+Lectiones|Memoria|Alemoria)'
pages = gzip.open(os.path.join(HERE, 'text/v1.txt.gz'), 'rt').read().split('\f### ')[1:]
cal, month, cur = {}, None, None
for pg in pages[24:38]:
    body = pg.split('\n', 1)[1]
    for col in body.split('\n||\n'):
        lines = col.split('\n')
        for l in lines:
            l = l.strip()
            for i, m in enumerate(MON):
                if l.upper().startswith(m[:5]) and len(l) < 14: month = i + 1; cur = None
            if not month: continue
            m = re.match(r'^(\d{1,2})\s+(.*)$', l)
            if m and 1 <= int(m.group(1)) <= 31:
                day = int(m.group(1)); cur = '%02d-%02d' % (month, day)
                if m.group(2).strip(): cal.setdefault(cur, []).append(m.group(2).strip())
                else: cal.setdefault(cur, [])
                continue
            if re.match(r'^\d{1,2}$', l):
                cur = '%02d-%02d' % (month, int(l)); cal.setdefault(cur, []); continue
            if cur and l and not re.match(r'^(Dies|mensis|CALENDARIUM|[xvjil\.]+$|\.)', l) and re.search(r'[a-z]{3}', l):
                if cal[cur] and not re.search(RANK + r'\.?,?\s*$', cal[cur][-1]): cal[cur][-1] = (cal[cur][-1].rstrip('-') if cal[cur][-1].endswith('-') else cal[cur][-1] + ' ') + l
                else: cal[cur].append(l)
out = {}
for k, items in sorted(cal.items()):
    lst = []
    for it in items:
        it = re.sub(r'\s+', ' ', it).replace('Alemoria', 'Memoria').replace('Kvangelista', 'Evangelista')
        m = re.search(RANK + r'\.?,?\s*$', it)
        rank = re.sub(r'\s+', ' ', m.group(1)) if m else None
        title = fix_line(it[:m.start()].strip(' .,') if m else it.strip(' .,'))
        title = re.sub(r'\bO\. ?P\b|\b0\. ?P\b', 'O.P.', title).replace('O.P..', 'O.P.')
        lst.append({'title': title, 'rank': rank})
    out[k] = lst
json.dump(out, open(os.path.join(HERE, 'calendar1909.json'), 'w'), ensure_ascii=False, indent=0)
print(len(out), sum(1 for v in out.values() if v))
for k in ('01-15', '03-07', '08-04', '12-08', '11-30', '05-24', '04-29', '06-29', '12-03'): print(k, out.get(k))
