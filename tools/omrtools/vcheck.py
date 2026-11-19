"""compare my page gabc (flattened pitch letters) with OMR pitches of the same page; print mismatching spans"""
import sys, re, subprocess, difflib
page, f = sys.argv[1], sys.argv[2]
mine = open(f).read()
mine = '\n'.join(l for l in mine.split('\n') if not l.startswith('@'))
groups = re.findall(r'\(([^)]*)\)', mine)
m = []
for g in groups:
    if re.fullmatch(r'[cf]\d|[,;:]+|::|', g.strip()): continue
    letters = [c.lower() for c in g if c.lower() in 'abcdefghijklm']
    m += sorted(letters)
out = subprocess.run(['python3', '/tmp/rt/groups2.py', page], capture_output=True, text=True).stdout
o = []
for line in out.split('\n'):
    if line.startswith('staff'):
        for tok in line.split('|', 1)[1].split():
            if '@' in tok: o += sorted(tok.split('@')[0])
sm = difflib.SequenceMatcher(None, m, o, autojunk=False)
print('mine', len(m), 'omr', len(o), 'ratio', round(sm.ratio(), 3))
for op, a1, a2, b1, b2 in sm.get_opcodes():
    if op != 'equal': print(op, 'mine@%d %s' % (a1, ''.join(m[a1:a2])), 'omr %s' % ''.join(o[b1:b2]), '| ctx', ''.join(m[max(0,a1-8):a1]))
