import json, re
F = json.load(open('/home/claude/build/abl/final.json'))
import pieces
MODE = dict(r01=8, r02=8, r03=5, r04=8, r05=8, r06=7, r07=7, r08=1, r09=1, r10=2, a01=1, a02=7, a03=7, a04=5, a05=7, a06=1, a07=1, a08=3, a09=3,
            a10=4, a11=8, a12=1, a13=1, a14=7, a15=2, a16=8, a17=1, a18=1, a19=2, a20=1, a21=1, a22=4, a23=8, a24=2, a25=8, a26=5, a27=5,
            a28=1, a29=1, a30=7, a31=1, a32=6)
PAGES = {}
for code, name, a, b, t in pieces.P:
    p0 = int(re.match(r'\d+', a).group()) + 40; p1 = int(re.match(r'\d+', b).group()) + 40
    PAGES[code] = '%d' % p0 if p0 == p1 else '%d-%d' % (p0, p1)
def ispell(s): return s.replace('j', 'i').replace('J', 'I')
for code, d in F.items():
    g = d['gabc']
    clef, body = g.split(' ', 1)
    toks = re.findall(r'([^()]*)\(([^)]*)\)(\s*)', body)
    out = []; pend = ''
    for t, n, sp in toks:
        lead = ' ' if t.startswith(' ') else ''
        t = t.strip()
        if '℣.' in t:
            t2 = t.replace('℣.', '').strip()
            out.append('%s(%s)%s' % (ispell(t2), n, sp)); pend = '<sp>V/</sp>. '; continue
        if t: t = pend + ispell(t); pend = ''
        out.append('%s(%s)%s' % (t, n, sp))
    body = ''.join(out).strip()
    kind = 'Responsorium' if code[0] == 'r' else 'Antiphona'
    name = ispell(pieces.P[[p[0] for p in pieces.P].index(code)][1])
    hdr = ('name:%s (Ablutio altarium);\noffice-part:%s;\nmode:%d;\nbook:Ecclesiasticum Officium O.P. Triduo ante Pascha (1927), p. %s;\n'
           'transcriber:%s for dominicanrite.com;\n%%%%\n' % (name, kind, MODE[code], PAGES[code],
           'read from the 1927 book (both printings compared: Tenebrae and the washing of the altars)' if code[0] == 'r' else d['src']))
    fn = '/home/claude/dominican-liturgy/gabc/op-abl-%s.gabc' % code
    open(fn, 'w').write(hdr + clef + ' ' + body + '\n')
print('ok')
