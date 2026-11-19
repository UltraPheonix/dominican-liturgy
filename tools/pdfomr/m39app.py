"""OMR for the notated Appendix of the Missale O.P. 1939 (M39.pdf, pdf pages 445-461: Prefaces, Pater, Ite...).
usage: m39app.py M39.pdf PAGE SIDE(L|R) -> JSON lines: per staff {y, clef_pos, items:[[x,'note',pos]|[x,'bar',kind]], words:[[x0,x1,'ocr']]}
Positions: 0 = bottom line, 1 = first space ... (gabc letter = 'd' + pos).  The lyrics come from the scan's text layer (OCR, no
accents) and only give x positions and syllable counts; the right words are put in later (m39pref.py)."""
import sys, json, re, numpy as np, pymupdf
from scipy import ndimage as ndi
DPI = 400; Z = DPI / 72
def vrun(B):
    H, W = B.shape; up = np.zeros((H, W), int); dn = np.zeros((H, W), int)
    for y in range(H): up[y] = np.where(B[y], (up[y - 1] if y else 0) + 1, 0)
    for y in range(H - 1, -1, -1): dn[y] = np.where(B[y], (dn[y + 1] if y < H - 1 else 0) + 1, 0)
    return up + dn - 1
def ocr_line(g, y0, y1, x0, x1):
    """tesseract on one lyric line (the scan's own text layer misses some lines): [[x0, x1, word]]"""
    import subprocess, re, tempfile
    from PIL import Image
    x0 = max(0, x0); y0 = max(0, y0)
    im = Image.fromarray(np.clip((g[y0:y1, x0:x1] - 60) * 1.6, 0, 255).astype(np.uint8))
    f = tempfile.NamedTemporaryFile(suffix='.png', delete=False); im.save(f.name)
    h = subprocess.run(['tesseract', f.name, '-', '--psm', '7', '-l', 'lat+eng', 'hocr'], capture_output=True, text=True).stdout
    out = []
    for m in re.finditer(r"bbox (\d+) (\d+) (\d+) (\d+); x_wconf \d+'>([^<]+)<", h):
        out.append([int(m.group(1)) + x0, int(m.group(3)) + x0, m.group(5)])
    return out
def deskew(g):
    from PIL import Image
    im = Image.fromarray(g.astype(np.uint8)); W = g.shape[1]; best = None
    small = im.resize((W // 4, g.shape[0] // 4))
    for ang in np.arange(-1.5, 1.51, 0.1):
        r = np.array(small.rotate(ang, resample=Image.BILINEAR, fillcolor=150)).astype(float)
        row = (r[:, int(r.shape[1] * .15):int(r.shape[1] * .85)] < 128).mean(1); sc = (row ** 2).sum()
        if best is None or sc > best[0]: best = (sc, ang)
    ang = best[1]
    for a2 in np.arange(ang - 0.08, ang + 0.081, 0.02):
        r = np.array(im.rotate(a2, resample=Image.BILINEAR, fillcolor=150)).astype(float)
        row = (r[:, int(W * .15):int(W * .85)] < 128).mean(1); sc = (row ** 2).sum()
        if sc > best[0] or a2 == ang - 0.08: best = (sc, a2) if sc > best[0] else best
    return np.array(im.rotate(best[1], resample=Image.BICUBIC, fillcolor=150)).astype(float), best[1]
def staves(g):
    """staff lines found two ways (row-threshold groups and row-profile peaks); both readings kept, overlaps merged"""
    H, W = g.shape; c = g[:, int(W * .12):int(W * .88)]
    r0 = (c < 128).mean(1)
    rs = np.convolve(r0, np.ones(3) / 3, mode='same')
    cand = []
    # 1. threshold groups
    rows = []
    for i in range(H):
        if r0[i] > 0.26:
            if rows and i - rows[-1][-1] <= 3: rows[-1].append(i)
            else: rows.append([i])
    cand.append([sum(x) / len(x) for x in rows])
    # 2. local maxima
    pk = [i for i in range(2, H - 2) if rs[i] > 0.4 and rs[i] == rs[max(0, i - 12):i + 13].max()]
    rows = []
    for i in pk:
        if rows and i - rows[-1][-1] <= 6: rows[-1].append(i)
        else: rows.append([i])
    cand.append([sum(x) / len(x) for x in rows])
    found = []
    for L in cand:
        M = []
        for v in L:
            if M and v - M[-1] < 10: M[-1] = (M[-1] + v) / 2
            else: M.append(v)
        L = M
        def ok(i):
            if i + 3 >= len(L): return None
            d = [L[i + k + 1] - L[i + k] for k in range(3)]
            return (max(d) - min(d)) if all(32 < x < 56 for x in d) and max(d) - min(d) < 13 else None
        i = 0
        while i + 3 < len(L):
            a_ = ok(i)
            if a_ is not None:
                b_ = ok(i + 1)
                if b_ is not None and b_ < a_ - 3: i += 1; a_ = b_
                found.append((a_, L[i:i + 4])); i += 4
            else: i += 1
    out = []
    for spread, L in sorted(found, key=lambda t: t[0]):
        if all(abs(L[0] - o[0]) > 60 for o in out): out.append(L)
    return sorted(out)
_FIT = {}
def local_lines(g, L, x, half=60):
    """the 4 staff lines at column x: each line fitted as a straight line across the staff (the scan is slightly skewed)"""
    key = (id(g), tuple(round(v) for v in L))
    if key not in _FIT:
        H, W = g.shape; fits = []
        for y in L:
            pts = []
            for xc in range(int(W * 0.15), int(W * 0.85), 80):
                y0 = int(y) - 12; win = (g[y0:int(y) + 13, xc - half:xc + half] < 128).mean(1)
                if win.max() > 0.5: pts.append((xc, y0 + float(np.argmax(win))))
            if len(pts) >= 4:
                X = np.array([p[0] for p in pts]); Y = np.array([p[1] for p in pts])
                for _ in range(2):
                    k, c = np.polyfit(X, Y, 1); res = np.abs(Y - (k * X + c)); keep = res < max(2.5, np.median(res) * 3)
                    X, Y = X[keep], Y[keep]
                fits.append((k, c))
            else: fits.append((0.0, y))
        _FIT[key] = fits
    return [k * x + c for k, c in _FIT[key]]
import os
THR = int(os.environ.get('THR', 115)); OPN = float(os.environ.get('OPN', 0.28)); KH = float(os.environ.get('KH', 0.85))
def read_staff(g, L, x_lo, x_hi):
    s = (L[3] - L[0]) / 3; y0 = int(L[0] - 3.2 * s); y1 = int(L[3] + 2.2 * s)
    G = g[y0:y1, x_lo:x_hi]
    B = G < THR
    R = vrun(B); C = B.copy()
    # remove the staff lines where they really run (fitted per column; the scan is skewed)
    Fa, Fb = local_lines(g, L, x_lo), local_lines(g, L, x_hi)
    nx = x_hi - x_lo
    for li in range(4):
        for xc in range(0, nx, 8):
            yy = int(round(Fa[li] + (Fb[li] - Fa[li]) * (xc + 4) / max(1, nx))) - y0
            a, b = max(0, yy - 5), yy + 6
            C[a:b, xc:xc + 8] &= (R[a:b, xc:xc + 8] > s * 0.3)
    C = ndi.binary_closing(C, structure=np.ones((5, 5))); C = ndi.binary_fill_holes(C)
    O = ndi.binary_opening(C, structure=np.ones((int(s * OPN), int(s * OPN))))
    lab, n = ndi.label(O); items = []
    hw = s * 0.52   # the width of a note head
    for sl in ndi.find_objects(lab):
        ys, xs = sl; h = ys.stop - ys.start; w = xs.stop - xs.start
        if w < s * 0.33 or h < s * 0.3 or w > s * 4.5: continue
        if h > s * 2.2 and w < s * 0.8: continue   # a bar line, not a stack of notes
        sub = O[sl]
        nsl = max(1, int(round(w / hw)))
        for q in range(nsl):
            xa = int(q * w / nsl); xb = int((q + 1) * w / nsl)
            col = sub[:, xa:xb].mean(1) > 0.5
            # runs of ink down this slice: each run is one or more stacked heads
            yy = np.where(col)[0]
            if not len(yy): continue
            runs = []; r0 = yy[0]; pv = yy[0]
            for v in yy[1:]:
                if v - pv > 2: runs.append((r0, pv)); r0 = v
                pv = v
            runs.append((r0, pv))
            for r0, r1 in runs:
                hh = r1 - r0 + 1
                if hh < s * 0.28: continue
                k = 1 if hh < s * KH else max(1, int(round(hh / (s * 0.5))))
                for j in range(k):
                    cy = ys.start + r0 + (j + 0.5) * hh / k + y0
                    x_ = xs.start + xa + x_lo
                    LL = local_lines(g, L, x_ + int(hw / 2))
                    sl2 = (LL[3] - LL[0]) / 3
                    items.append([x_, 'note', int(round((LL[3] - cy) / (sl2 / 2))), int(xb - xa)])
    # bar lines: thin vertical strokes (from the un-opened mask) not part of a note
    lab2, n2 = ndi.label(C)
    for sl in ndi.find_objects(lab2):
        ys, xs = sl; h = ys.stop - ys.start; w = xs.stop - xs.start
        if w <= s * 0.32 and h >= s * 1.2:
            top = (L[3] - (ys.start + y0)) / (s / 2); bot = (L[3] - (ys.stop + y0)) / (s / 2)
            kind = 'full' if h >= s * 2.6 else 'half'
            items.append([xs.start + x_lo, 'bar', kind, round(top, 1), round(bot, 1)])
    seen = set(); its = []
    for it in items:   # one head read twice in the same column
        if it[1] == 'note':
            if (it[0], it[2]) in seen: continue
            seen.add((it[0], it[2]))
        its.append(it)
    items = its
    items.sort(key=lambda t: (t[0], -t[2] if t[1] == 'note' else 0))
    # merge double bars
    out = []
    for it in items:
        if it[1] == 'bar' and out and out[-1][1] == 'bar' and it[0] - out[-1][0] < s * 0.9 and it[2] == 'full' and out[-1][2] == 'full':
            out[-1][2] = 'double'; continue
        out.append(it)
    return out
def main(pdf, page, side):
    d = pymupdf.open(pdf); p = d[page]; W2 = p.rect.width / 2
    clip = pymupdf.Rect(0, 0, W2, p.rect.height) if side == 'L' else pymupdf.Rect(W2, 0, p.rect.width, p.rect.height)
    pix = p.get_pixmap(dpi=DPI, clip=clip)
    g = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)[:, :, :3].mean(2)
    g0 = g
    g, ang = deskew(g0)
    st = staves(g)
    # the staff count is sensitive to the angle: try the neighbours and keep the reading with most staves
    from PIL import Image
    for da in (-0.1, 0.1):
        g2 = np.array(Image.fromarray(g0.astype(np.uint8)).rotate(ang + da, resample=Image.BICUBIC, fillcolor=150)).astype(float)
        st2 = staves(g2)
        if len(st2) > len(st): g, st, ang = g2, st2, ang + da
    # words of the text layer, in pixel coords of the clip
    H0, W0 = g.shape; th = np.radians(ang); cx, cy = W0 / 2, H0 / 2
    def tr(x, y):   # pdf point -> deskewed pixel (PIL rotates counter-clockwise about the centre)
        x = (x - clip.x0) * Z; y = (y - clip.y0) * Z
        return cx + (x - cx) * np.cos(th) + (y - cy) * np.sin(th), cy - (x - cx) * np.sin(th) + (y - cy) * np.cos(th)
    words = []
    for w in p.get_text('words'):
        if clip.x0 - 2 <= w[0] < clip.x1:
            x0, y0 = tr(w[0], w[1]); x1, y1 = tr(w[2], w[3]); words.append((x0, y0, x1, y1, w[4]))
    res = []
    for i, L in enumerate(st):
        s = (L[3] - L[0]) / 3
        nxt = st[i + 1][0] if i + 1 < len(st) else L[3] + 6 * s
        # the staff's horizontal extent: where line 2 is dark
        Wd = g.shape[1]; xsamp = np.arange(0, Wd)
        fits = [local_lines(g, L, 0), local_lines(g, L, Wd)]
        dk = np.ones(Wd, bool)
        y_a = int(max(0, min(fits[0][0], fits[1][0]) - s)); y_b = int(max(fits[0][3], fits[1][3]) + s)
        bgc = np.percentile(g[y_a:y_b], 80, axis=0)   # the paper's tone in each column (darker towards the gutter)
        for li in range(4):
            yv = fits[0][li] + (fits[1][li] - fits[0][li]) * xsamp / Wd
            col = np.zeros(Wd, bool)
            for dy in range(-4, 5):
                yy = np.clip(np.round(yv + dy).astype(int), 0, g.shape[0] - 1)
                col |= g[yy, xsamp] < np.minimum(135, bgc - 40)
            dk &= col
        sm = np.convolve(dk.astype(float), np.ones(41) / 41, mode='same') > 0.6
        xs = np.where(sm)[0]
        runs = []; a0 = xs[0]; prev = xs[0]
        for v in xs[1:]:
            if v - prev > 200: runs.append((a0, prev)); a0 = v
            prev = v
        runs.append((a0, prev))
        x_lo, x_hi = max(runs, key=lambda r: r[1] - r[0])
        x_lo, x_hi = int(x_lo), int(x_hi)
        # the staff runs at least as far as its lyrics (the line test fails near the spine)
        lyr = [ (tr(w[2], w[3])[0]) for w in p.get_text('words') if clip.x0 - 2 <= w[0] < clip.x1 and L[3] + 0.3 * s < tr(w[0], w[1])[1] < min(nxt - 0.5 * s, L[3] + 3.4 * s)]
        if lyr: x_hi = int(min(g.shape[1] - 5, max(x_hi, max(lyr) + 0.3 * s)))
        it = read_staff(g, L, x_lo, x_hi + 1)
        ly = []
        lo_y, hi_y = L[3] + 0.3 * s, min(nxt - 0.5 * s, L[3] + 3.4 * s)
        for (a0, b0, a1, b1, t) in words:
            if lo_y < b0 < hi_y and b1 < nxt:
                ly.append([round(a0), round(a1), t])
        if len([w for w in ly if re.search('[A-Za-z]{2}', w[2])]) < 2:
            ly = ocr_line(g, int(L[3] + 0.6 * s), int(L[3] + 3.0 * s), x_lo - 60, x_hi + 20)
        # per character x positions for the lyric words (syllable starts inside unbroken words)
        chars = []
        raw = p.get_text('rawdict', clip=clip)
        for b in raw['blocks']:
            for l in b.get('lines', []):
                for sp in l['spans']:
                    for ch in sp['chars']:
                        bx = ch['bbox']; xx, yy = tr(bx[0], bx[1])
                        if lo_y < yy < hi_y: chars.append([round(xx), ch['c']])
        res.append({'staff': i, 'L': [round(v) for v in L], 's': round(s, 1), 'x': [x_lo, x_hi], 'items': it, 'words': ly, 'chars': chars})
    return res, g
if __name__ == '__main__':
    r, g = main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    for x in r:
        print(json.dumps({k: v for k, v in x.items() if k != 'chars'}))
