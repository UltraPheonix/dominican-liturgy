import pickle, json, re, sys, os
sys.path.insert(0, '/home/claude/build/abl')
import pieces, gbcmp
import importlib.util
spec = importlib.util.spec_from_file_location('m39lib', '/home/claude/build/abl/m39lib.py'); L_ = importlib.util.module_from_spec(spec); spec.loader.exec_module(L_)
R = pickle.load(open('/home/claude/build/abl/res.pkl', 'rb'))
CLEF = dict(r01='c3', r02='c3', r03='c3', r04='c4', r05='c3', r06='c3', r07='c3', r08='c4', r09='c4', r10='f3',
            a01='c4', a02='c3', a03='c3', a04='c3', a05='c3', a06='c4', a07='c4', a08='c4', a09='c4', a10='c3', a11='c4', a12='c4',
            a13='c4', a14='c3', a15='f3', a16='c4', a17='c4', a18='c4', a19='f3', a20='c4', a21='c4', a22='c3', a23='c4', a24='f3',
            a25='c4', a26='c3', a27='f3', a28='c4', a29='c4', a30='c3', a31='c4', a32='c4')
FLAT = {'a12': 'i', 'a20': 'i'}          # key-signature flat after the clef
DO = {'c4': 'j', 'c3': 'h', 'c2': 'f', 'c1': 'd', 'f3': 'e', 'f4': 'g'}
GB = {'a03': 6425, 'a05': 7038, 'a07': 5643, 'a08': 5961, 'a09': 6908, 'a10': 6523, 'a11': 4734, 'a12': 4592, 'a13': 5985, 'a16': 5785,
      'a17': 6858, 'a22': 4985, 'a27': 5871, 'a28': 6732, 'a29': 5500, 'a30': 5606, 'a31': 5974, 'a32': 18467}
def shift(n, k):
    out = []
    for c in n:
        if 'a' <= c <= 'm': c = chr(ord(c) + k)
        elif 'A' <= c <= 'M': c = chr(ord(c) + k)
        out.append(c)
    return ''.join(out)
NAMES = {p[0]: p[1] for p in pieces.P}
res = {}
for code in CLEF:
    out = [list(t) for t in R[code]['out']]
    src = 'OMR of the 1927 book, proofed against the scan'
    if code in GB:
        clef_gb, merged, miss = gbcmp.merge(code, GB[code])
        k = (ord(DO[CLEF[code]]) - ord(DO[clef_gb])) % 7
        if k > 3: k -= 7
        for i, (s, n, b) in enumerate(merged):
            if n != '?':
                n = n.split()[0]
                out[i][1] = shift(n, k)
                if b: out[i][2] = b
        src = 'read from the 1927 book; notes checked against the Antiphonarium O.P. (1933)'
    g = '(%s) ' % CLEF[code]
    if code in FLAT: g = '(%s) ' % CLEF[code]   # the flat is written before its note in the melody
    C = L_.correct_syllables([p[4] for p in pieces.P if p[0] == code][0])
    for (t, n, b), c in zip(out, C):
        g += '%s(%s)' % (t, n) + (' (%s)' % b if b else '') + (' ' if c[3] or b else '')
    g = re.sub(r'\s+', ' ', g).strip()
    if not g.endswith('(::)'): g += ' (::)'
    res[code] = {'gabc': g, 'src': src, 'name': NAMES[code], 'unread': [t for t, n, b in out if n == '?']}
    print(code, CLEF[code], res[code]['unread'], g[:150])
json.dump(res, open('/home/claude/build/abl/final.json', 'w'), ensure_ascii=False, indent=1)
