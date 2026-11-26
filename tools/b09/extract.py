"""Extract the text layer of the 1909 Breviary PDFs (Joseph's cropped '_text' scans) column by column.
usage: python3 extract.py v1.pdf v1   -> tools/b09/text/v1.txt  (pages separated by '\f### <pdf index>\n')"""
import fitz, sys, os
pdf, tag = sys.argv[1], sys.argv[2]
d = fitz.open(pdf); out = []
for i, p in enumerate(d):
    W = p.rect.width; words = p.get_text('words')
    if not words: out.append('\f### %d\n' % i); continue
    # the gutter: the x (between 35% and 65% of the width) crossed by the fewest words
    best = None
    for x in range(int(W * 0.35), int(W * 0.65)):
        c = sum(1 for w in words if w[0] < x < w[2])
        if best is None or c < best[0] or (c == best[0] and abs(x - W / 2) < abs(best[1] - W / 2)): best = (c, x)
    mid = best[1]
    cols = [[w for w in words if w[2] <= mid + 1], [w for w in words if w[2] > mid + 1]]
    # a running head spanning the middle stays in the left column at the top
    txt = []
    for c in cols:
        c.sort(key=lambda w: (round(w[1] / 4), w[0]))
        lines, cur, y = [], [], None
        for w in c:
            if y is None or abs(w[1] - y) > 3.5:
                if cur: lines.append(' '.join(cur))
                cur, y = [w[4]], w[1]
            else: cur.append(w[4])
        if cur: lines.append(' '.join(cur))
        txt.append('\n'.join(lines))
    out.append('\f### %d\n%s\n||\n%s\n' % (i, txt[0], txt[1]))
dst = os.path.join(os.path.dirname(__file__), 'text', tag + '.txt')
open(dst, 'w').write(''.join(out)); print(dst, len(d))
