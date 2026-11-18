"""Word-level diff of a built 1939 Holy Week day against the column OCR of the Missal.
usage: proof.py DAY BP0 BP1 [ctx]   prints every disagreement with page/column/y of the OCR side."""
import sys, json, re, unicodedata, difflib
day, b0, b1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
CTX = int(sys.argv[4]) if len(sys.argv) > 4 else 4
js = open('/home/claude/build/site/data/holyweek_text.js').read()
HT = json.loads(js[js.index('{'):js.rindex('}') + 1])
def walk(x, out):
    if isinstance(x, dict):
        t = x.get('t')
        if t in ('C', 'G'): out.append(('«CHANT»', None)); return
        if 'la' in x and isinstance(x['la'], str):
            red = t in ('R', 'H', 'L', 'I')
            # *...* is black inside a rubric, {...} red inside text
            for k, part in enumerate(re.split(r'(\*[^*]*\*|\{[^}]*\})', x['la'])):
                if not part: continue
                r = (not red) if (part[0] in '*{') else red
                out.append((part, r))
        for k, v in x.items():
            if k not in ('la', 'en') and isinstance(v, (list, dict)): walk(v, out)
    elif isinstance(x, list):
        for v in x: walk(v, out)
src = []; walk(HT['1939'][day], src)
def norm(w):
    w = w.lower().replace('æ', 'ae').replace('œ', 'oe').replace('ǽ', 'ae').replace('j', 'i')
    w = ''.join(c for c in unicodedata.normalize('NFD', w) if unicodedata.category(c)[0] == 'L')
    return w
def toks(s, tag):
    s = re.sub(r'[{}*^]', '', s).replace('✠', ' ').replace('℣', ' ').replace('℟', ' ')
    return [(norm(w), w, tag) for w in s.split() if norm(w) or w == '«CHANT»']
A = []
for s, _ in src:
    if s == '«CHANT»': A.append(('#chant', '«CHANT»', None)); continue
    A += toks(s, _)
B = []
for bp in range(b0, b1 + 1):
    L = json.load(open('/home/claude/build/m39hw/p%d.json' % bp))
    L.sort(key=lambda l: (l['c'], l['y']))
    carry = ''
    for i, l in enumerate(L):
        t = l['t']
        if l['y'] < 240 and re.match(r'^\d+\s|.*\s\d+$', t.strip()): continue  # running head
        t = carry + t; carry = ''
        if t.endswith('-'): carry = t.split()[-1][:-1]; t = ' '.join(t.split()[:-1])
        B += toks(t, (bp, l['c'], l['y'], 'R' if l['red'] else ''))
a = [x[0] for x in A]; b = [x[0] for x in B]
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
n = 0
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op == 'equal': continue
    if op == 'delete' and a[i1:i2] == ['#chant']: continue
    sa = ' '.join(a[i1:i2]); sb = ' '.join(b[j1:j2])
    if op == 'replace' and len(sa) < 40 and (difflib.SequenceMatcher(None, sa, sb.replace('z', 'ae')).ratio() >= 0.66 or sb.replace(' ', '') in sa or (sa[1:] == sb)): continue
    if op == 'replace' and set(a[i1:i2]) == {'#chant'}: continue
    if op == 'insert' and sb in ('x', 'y', 'v', 'xx', 'r', 'i'): continue
    n += 1
    tag = B[j1][2] if j1 < len(B) else B[-1][2]
    ctxa = ' '.join(x[1] for x in A[max(0, i1 - CTX):i1])
    print('%-7s p%s c%s y%s %s | ...%s [SITE: %s] [BOOK: %s]' % (op, tag[0], tag[1], tag[2], tag[3], ctxa,
          ' '.join(x[1] for x in A[i1:i2])[:300], ' '.join(x[1] for x in B[j1:j2])[:300]))
# colour: runs of 3+ words red in one and black in the other
run = []
def flush():
    if len(run) >= 3:
        i, j = run[0]; tag = B[j][2]
        print('COLOUR  p%s c%s y%s site=%s | %s' % (tag[0], tag[1], tag[2], 'red' if A[i][2] else 'black', ' '.join(A[k][1] for k, _ in run)[:200]))
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op != 'equal': flush(); run = []; continue
    for k in range(i2 - i1):
        i, j = i1 + k, j1 + k
        if bool(A[i][2]) != (B[j][2][3] == 'R') and A[i][0] not in ('per', 'dominum'): run.append((i, j))
        else: flush(); run = []
flush()
print('#', n, 'differences;', len(a), 'site words,', len(b), 'book words', file=sys.stderr)
