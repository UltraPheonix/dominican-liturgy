"""Build hymn gabc: melody of stanza 1 from a gabc string, words of every stanza from a text file.
usage: hymn.py melody.gabc stanzas.txt out.gabc "header lines"   (stanzas: one per paragraph, syllables split by '-', words by space;
       a line 'AMEN' at the end adds A()men.() with no notes, as the book prints it)"""
import re, sys
mel = open(sys.argv[1]).read()
mel = mel.split('%%')[-1].strip()
toks = re.findall(r'([^()]*)\(([^)]*)\)', mel)
clef = toks[0][1] if re.match(r'^[cf]b?\d$', toks[0][1]) else None
if clef: toks = toks[1:]
seq = []
for t, n in toks:
    t = t.strip()
    if t: seq.append(('s', n))
    elif n.strip() in (':', ';', '::', ',', ';1', ':?', "'", ''): seq.append(('b', n))
    else: seq.append(('n', n))          # notes with no text (a melisma after a syllable) stay untexted
syl_n = [n for k, n in seq if k == 's']
text = open(sys.argv[2]).read().strip().split('\n\n')
amen = text[-1].strip() == 'AMEN'
if amen: text = text[:-1]
out = ['(%s)' % clef] if clef else []
for si, st in enumerate(text):
    words = st.split()
    syls = []
    for w in words:
        p = w.split('-')
        for i, s in enumerate(p): syls.append(s + (' ' if i == len(p) - 1 else ''))
    assert len(syls) == len(syl_n), 'stanza %d has %d syllables, melody %d: %s' % (si + 1, len(syls), len(syl_n), st[:40])
    if si: syls[0] = '%d. ' % (si + 1) + syls[0]
    line = ''; it = iter(syls)
    for k, n in seq:
        if k == 's':
            x = next(it); line += x.rstrip(' ') + '(' + n + ')' + (' ' if x.endswith(' ') else '')
        elif k == 'n': line += '(' + n + ') '
        else: line += '(' + n + ') '
    out.append(line.strip())
g = ' '.join(out)
if amen: g = g.rstrip() + ' A()men.() (::)'
hdr = sys.argv[4] if len(sys.argv) > 4 else ''
open(sys.argv[3], 'w').write(hdr.replace('\\n', '\n') + '\n%%\n' + g + '\n')
print(g[:300], '...', g[-200:])
