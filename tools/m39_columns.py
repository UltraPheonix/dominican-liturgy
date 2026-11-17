"""Rebuild clean column text of the Missale O.P. 1939 from word boxes: split each PDF page at its empty gutters."""
import subprocess, re, html, sys, os
P = '/home/claude/dl/missal/Missale OP 1939.pdf'; OUT = '/home/claude/dl/m39cols'
def page(n):
    x = subprocess.run(['pdftotext', '-f', str(n), '-l', str(n), '-bbox', P, '-'], capture_output=True, text=True).stdout
    W = []
    for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', x):
        a, b, c, d = map(float, m.groups()[:4]); W.append((a, b, c, d, html.unescape(m.group(5))))
    if not W: return ''
    width = int(max(w[2] for w in W)) + 2
    cov = [0] * (width + 1)
    for a, b, c, d, t in W:
        if c - a > 140: continue  # very long runs (headers across) do not block a gutter
        for i in range(int(a), min(width, int(c) + 1)): cov[i] += 1
    # gutters: runs of x with (almost) no coverage, at least 6pt wide, not at the margins
    gut, i = [], 0
    lo, hi = min(int(w[0]) for w in W), max(int(w[2]) for w in W)
    while i <= width:
        if cov[i] <= 1 and lo + 40 < i < hi - 40:
            j = i
            while j <= width and cov[j] <= 1: j += 1
            if j - i >= 6: gut.append((i + j) / 2)
            i = j
        else: i += 1
    cuts = [0] + gut + [width + 1]
    cols = []
    for k in range(len(cuts) - 1):
        ws = [w for w in W if cuts[k] <= (w[0] + w[2]) / 2 < cuts[k + 1]]
        if not ws: continue
        ws.sort(key=lambda w: (round(w[1] / 4), w[0]))
        lines, cur, y = [], [], None
        for w in ws:
            if y is not None and abs(w[1] - y) > 4: lines.append(' '.join(cur)); cur = []
            cur.append(w[4]); y = w[1] if y is None or abs(w[1]-y) > 4 else y
        lines.append(' '.join(cur)); cols.append('\n'.join(lines))
    return '\n\f\n'.join(cols)
if __name__ == '__main__':
    a, b = int(sys.argv[1]), int(sys.argv[2])
    for n in range(a, b + 1):
        open('%s/%d.txt' % (OUT, n), 'w').write(page(n))
