import re, json
from ext import d
def page_lines(i):
    p = d[i]; W = p.rect.width; mid = W / 2
    bl = [b for b in p.get_text('blocks') if b[6] == 0 and b[4].strip()]
    full, colb = [], []
    for b in bl:
        x0, y0, x1, y1, t = b[:5]
        t = t.strip()
        if re.fullmatch(r'[\divxlIVXL\s.;:,\'"|!?i]{1,7}', t): continue           # page numbers, specks
        if x0 < mid - 25 and x1 > mid + 25 and (x1 - x0 > 0.55 * W or y0 < 128):
            if y0 < 128 and (y1 - y0) < 34: continue                              # running header
            full.append(b)
        else: colb.append(b)
    full.sort(key=lambda b: b[1])
    cuts = [-1] + [b[1] for b in full] + [1e9]
    out = []
    for k in range(len(cuts) - 1):
        if k > 0:
            out += [('T', l.strip()) for l in full[k - 1][4].split('\n') if l.strip()]
        band = [b for b in colb if cuts[k] <= b[1] < cuts[k + 1]]
        for side in (0, 1):
            for b in sorted([b for b in band if ((b[0] + b[2]) / 2 >= mid) == bool(side)], key=lambda b: b[1]):
                out += [('L', re.sub(r'^[|Il!]\s+(?=[A-Za-z])', '', l.strip())) for l in b[4].split('\n') if l.strip()]
    return out
lines = []
for i in range(len(d)):
    for kind, l in page_lines(i): lines.append((i, kind, l))
json.dump(lines, open('lines.json', 'w'), ensure_ascii=False)
print(len(lines))
