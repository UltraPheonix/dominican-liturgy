import sys, pickle
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, '/home/claude/build/abl')
import pieces, gcache
S = pickle.load(open('/home/claude/build/tri_staves.pkl', 'rb'))
R = pickle.load(open('/home/claude/build/abl/res.pkl', 'rb'))
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
F2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 19)
COL = [(220, 0, 0), (0, 140, 0), (0, 0, 230), (200, 0, 200), (0, 150, 160), (210, 120, 0)]
def sheet(code, per=3, only=None):
    r = R[code]; spans = r['spans']; nx = r['nx']; out = r['out']
    tiles = []
    for (key, lo, hi) in spans:
        if only and key[2] not in only: continue
        x = S[key[:2]][key[2]]; s = x['s']; L = x['L']; g = gcache.G(*key[:2])
        x0 = int(max(0, x['x'][0] - 0.5 * s)); x1 = int(x['x'][1] + 0.5 * s); y0 = int(L[0] - 2.6 * s); y1 = int(L[3] + 2.8 * s)
        im = Image.fromarray(g[y0:y1, x0:x1].astype('uint8')).convert('RGB'); d = ImageDraw.Draw(im)
        for i in range(lo, hi + 1):
            c = COL[i % len(COL)]
            for k, (nxx, p) in enumerate(sorted(nx[i])):
                yy = L[3] - p * s / 2 - y0; xx = nxx - x0
                d.rectangle([xx - 2, yy - s * 0.32, xx + s * 0.55, yy + s * 0.32], outline=c, width=3)
                if k == 0: d.text((xx, 2 + (i % 2) * 22), '%d' % i, fill=c, font=F)
        sc = 1100 / im.width; im = im.resize((1100, int(im.height * sc)))
        lines = []; cur = ''
        for i in range(lo, hi + 1):
            t = '%d:%s(%s)%s  ' % (i, out[i][0], out[i][1], ' ' + out[i][2] if out[i][2] else '')
            if len(cur) + len(t) > 95: lines.append(cur); cur = ''
            cur += t
        lines.append(cur)
        T = Image.new('RGB', (1100, im.height + 24 * len(lines) + 6), 'white'); T.paste(im, (0, 0)); dd = ImageDraw.Draw(T)
        for k, l in enumerate(lines): dd.text((4, im.height + 2 + 24 * k), l, fill=(160, 0, 0), font=F2)
        tiles.append(T)
    files = []
    for n in range(0, len(tiles), per):
        grp = tiles[n:n + per]; H = sum(t.height for t in grp)
        G = Image.new('RGB', (1100, H), 'white'); y = 0
        for t in grp: G.paste(t, (0, y)); y += t.height
        fn = '/home/claude/build/abl/pf_%s_%d.png' % (code, n // per); G.save(fn); files.append(fn)
    return files
if __name__ == '__main__':
    only = [int(v) for v in sys.argv[2].split(',')] if len(sys.argv) > 2 else None
    print(sheet(sys.argv[1], only=only))
