import pickle, json, re, sys, os
sys.path.insert(0, '/home/claude/build/ten')
import pieces, gbcmp
import importlib.util
spec = importlib.util.spec_from_file_location('m39lib', '/home/claude/build/ten/m39lib.py'); L_ = importlib.util.module_from_spec(spec); spec.loader.exec_module(L_)
R = pickle.load(open('/home/claude/build/ten/res.pkl', 'rb'))
DAY = sys.argv[1] if len(sys.argv) > 1 else 'h'
CLEF = dict(t01='c3', t02='c3', t03='c3', t04='c3', t05='c4', t06='c4', t07='c3', t08='c3', t09='c3', v01='c3', v02='c4', v03='c4',
            l01='c4', l02='c4', l03='c4', k04='c4', k05='c4', k06='c4', k08='c4', k10='c4', k13='c4', k19='c4')
GB = {'l01': 8261, 'l02': 8262, 'l03': 8263, 'u01': 7158, 'u02': 5691, 'u03': 5695, 'u04': 4698, 'u05': 5605, 'u06': 6734}
HAND = {'c01': '(c3) Chri(e)stus(f) fac(h)tus(h) est(h) (::) pro(h) no(h)bis(h) o(h)bé(h)di(h)ens(h) us(h)que(h) ad(h) mor(i)tem,(h) (;) mor(h)tem(h) au(g)tem(h) cru(f)cis.(e) (::)', 'k01': '(c4) Ký(dh)ri(g)e,(g) (;) e(h)léi(gfd)son.(e) (::)', 'k07': '(c4) Chri(dh)ste,(g) (;) e(h)léi(gfd)son.(e) (::)'}
GBSRC = {'l': 'Officium Hebdomadæ Sanctæ O.P. (1965)', 'u': 'Antiphonarium O.P. (1933)'}
def text_of(code): return [p[4] for p in pieces.P if p[0] == code][0]
res = {}
REFRAIN = None
for code in [p[0] for p in pieces.P]:
    if code in ('b01',) or code.startswith('q') or code.startswith('p'): continue
    if code in HAND or code in ('k02', 'k03', 'k09', 'k11', 'k14', 'k15', 'k16', 'k12', 'k17', 'k18'):
        continue
    out = [list(t) for t in R[code]['out']]
    src = 'read from the 1927 book, proofed against the scan'
    clef = CLEF.get(code, 'c4')
    if code in GB:
        clef, merged, miss = gbcmp.merge(code, GB[code])
        keep = []
        if code[0] == 'l':   # the refrain Jerusalem, Jerusalem is sung differently in 1927: keep the book's notes
            js = [i for i, (t, n, b) in enumerate(out) if t.startswith('Je') and i > len(out) - 25]
            keep = list(range(js[0], js[0] + 8))
        for i, (s, n, b) in enumerate(merged):
            if n != '?' and i not in keep:
                out[i][1] = n; out[i][2] = b
        src = 'read from the 1927 book; notes as in the %s, which agrees with it%s' % (GBSRC[code[0]], ' (the refrain Jerusalem as in 1927)' if keep else '')
    C = L_.correct_syllables(text_of(code))
    g = ''
    for (t, n, b), c in zip(out, C):
        g += '%s(%s)' % (t, n) + (' (%s)' % b if b else '') + (' ' if c[3] or b else '')
    g = re.sub(r'\s+', ' ', g).strip()
    if code == 'l01': REFRAIN = g[g.rindex('con('):]
    if code in ('l02', 'l03') and REFRAIN:
        g = re.sub(r'\s*\(::\)\s*$', '', g).rstrip('.').replace('lem.(', 'lem,(')
        g = re.sub(r'lem\.?\(([a-m]+)\)\s*$', r'lem,(\1)', g) + ' ' + REFRAIN
    g = g.replace('i(fe)ni(fe)mí', 'i(g)ni(fe)mí').replace('rú(ii)', 'rú(i)').replace('lem,(h) con(', 'lem,(h) (;) con(')
    g = re.sub(r'(\s*\([;:,][0-9]?\))+\s*\(::\)$', ' (::)', g)
    if not g.endswith('(::)'): g += ' (::)'
    res[code] = {'gabc': '(%s) ' % clef + g, 'src': src, 'name': [p[1] for p in pieces.P if p[0] == code][0]}
for k, v in HAND.items(): res[k] = {'gabc': v, 'src': 'read from the 1927 book, proofed against the scan', 'name': [p[1] for p in pieces.P if p[0] == k][0]}
for code, v in sorted(res.items()): print(code, v['gabc'][:110], '...', v['gabc'][-60:])
json.dump(res, open('/home/claude/build/ten/final_%s.json' % DAY, 'w'), ensure_ascii=False, indent=1)
