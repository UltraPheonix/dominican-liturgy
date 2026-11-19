# Thursday Vespers (Quad6h.src): sing the psalms and the Magnificat to the tones the 1927 book gives (pp. 75-81)
import re, json, subprocess, psalms
fn = '/home/claude/dominican-liturgy/tools/hw39/Quad6h.src'
s = open(fn).read()
TONES = {'115': ('II', 'D'), '119': ('VIII', 'G'), '139': ('VIII', 'G'), '140': ('VIII', 'G'), '141': ('VII', 'a'), 'mag': ('I', 'g')}
SPEC = []
lines = s.split('\n'); out = []; i = 0; stack = []
while i < len(lines):
    l = lines[i]
    m = re.match(r'F: (Psalmus (\d+)|Canticum Magníficat)', l)
    if m and not (i + 1 < len(lines) and lines[i + 1].startswith('G: op-hv-ps')):
        k = m.group(2) or 'mag'
        n = int(k) if k != 'mag' else 'Canticum B. Mariæ Virginis'
        tn, d = TONES[k]; pid = 'op-hv-ps-%s' % k
        SPEC.append(dict(id=pid, name=l[3:].split('|')[0].strip(), tone=tn, diff=d, solemn=(k == 'mag'), verses=[la for la, en in psalms.psalm(n)],
                         src='Ecclesiasticum Officium O.P. Triduo ante Pascha (1927): tone and ending as the book gives them on the first verse',
                         tr='set to the Dominican psalm tone (Tonorum communium regulae)'))
        out += [l, 'G: %s | Tonus %s %s' % (pid, tn, d), 'F: Textus et versio | Text and translation']
        i += 1
        while not lines[i].startswith('F/'): out.append(lines[i]); i += 1
        out += ['F/', 'F/']; i += 1; continue
    out.append(l); i += 1
open(fn, 'w').write('\n'.join(out))
print(subprocess.run(['node', '/home/claude/build/ten/gen_ps.js'], input=json.dumps(SPEC, ensure_ascii=False), capture_output=True, text=True))
