"""Ordo O.P. 1944 from the text layer of the PDF (ABBYY, pdftotext -layout), one entry per day.
Each day begins with its printed day of the month and weekday (Dom., Fer. 2.-6., Sabb.); the date is resolved from the
day number and weekday near the previous date. Duplicated pages in the scan are skipped (first reading kept).
usage: parse2.py o44.pdf out.json"""
import re, json, sys, subprocess, datetime
pdf, out = sys.argv[1], sys.argv[2]
npages = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
E = re.compile(r'^\s{0,12}(?:(\d{1,2})[^\w]{1,4})?(Dom\.|Dom\s|Fer\.?\s*[2-6]\w?\.?|Sabb\.)\s*(.*)$')
def wd(tok):
    if tok.startswith('Dom'): return 6
    if tok.startswith('Sabb'): return 5
    return int(re.search(r'[2-6]', tok).group()) - 2
lines = []
for p in range(1, npages + 1):
    t = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), '-layout', pdf, '-'], capture_output=True, text=True).stdout
    for l in t.split('\n'): lines.append((p, l))
MON = ['JANUARIUS','FEBRUARIUS','MARTIUS','APRILIS','MAJUS','JUNIUS','JULIUS','AUGUSTUS','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER']
d = datetime.date(1943, 12, 31); days = {}; cur = None; mon = 1
for p, l in lines:
    sq = re.sub(r'[^A-Z]', '', l.replace('Ś', 'S').replace('Ü','U'))
    if 6 <= len(sq) <= 12 and len(l.strip()) < 60:
        for i, M in enumerate(MON):
            if sq.startswith(M) or sq == M: mon = i + 1
    m = E.match(l)
    x = None
    if m and not m.group(1) and (len(l) - len(l.lstrip()) > 8 or re.match(r'^\s*([—\-–).,;:]|praec|\w{0,3}ae\b|Compl)', m.group(3)) or not m.group(3).strip()):
        m = None
    if m:
        n = int(m.group(1)) if m.group(1) else None; w = wd(m.group(2))
        base = d
        rng = range(-12, 15) if n else range(1, 2)
        for off in sorted(rng, key=abs):
            y = base + datetime.timedelta(days=off)
            if y.weekday() == w and (n is None or y.day == n) and y.year == 1944:
                x = y; break
        if x is None and n:
            for mm in (mon, mon - 1, mon + 1):
                try: y = datetime.date(1944, mm, n)
                except ValueError: continue
                if y.weekday() == w and abs((y - d).days) < 45: x = y; break
    if x:
        d = x
        if x.isoformat() in days: cur = None; continue
        cur = days[x.isoformat()] = {'date': x.isoformat(), 'page': p, 'head': m.group(3).strip(), 'text': l.strip()}
    elif cur is not None:
        cur['text'] += '\n' + l.strip()
        if len(cur['head']) < 160 and l.strip() and not re.match(r'^(In |Vesp|VF|Compl|Nota|NOTA|Hodie)', l.strip()):
            cur['head'] += ' ' + l.strip()
res = []
for k in range(366):
    x = (datetime.date(1944, 1, 1) + datetime.timedelta(days=k)).isoformat()
    res.append(days.get(x, {'date': x, 'head': '(not found)', 'text': ''}))
print('missing', [r['date'] for r in res if not r['text']], file=sys.stderr)
json.dump(res, open(out, 'w'), ensure_ascii=False, indent=0)
