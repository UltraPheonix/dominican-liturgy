"""Split a transcribed Passion into paragraphs at the paragraph starts of the Divinum Officium text,
pairing each with its English there.  usage: mkpassion.py latin.txt DOfile section name"""
import re, sys, unicodedata
def strip(s): return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
def n(w): return re.sub(r'[^a-z]', '', strip(w.lower()).replace('æ', 'ae').replace('œ', 'oe').replace('j', 'i'))
lat, dofile, sec, name = sys.argv[1:5]
def section(path):
    s = open(path, encoding='utf8').read()
    m = re.search(r'^\[' + re.escape(sec) + r'\]\n(.*?)(?=^\[|\Z)', s, re.S | re.M)
    out = []
    for l in m.group(1).split('\n'):
        l = l.strip()
        if not l or l.startswith(('(', '@', '!', '_', 'v. ')): continue
        out.append(l)
    return out
LA = section(dofile); EN = section(dofile.replace('/Latin/', '/English/'))
assert len(LA) == len(EN), (len(LA), len(EN))
text = open(lat, encoding='utf8').read().strip()
W = text.split(); NW = [n(w) for w in W]
cuts = [0]
for p in LA[1:]:
    key = [n(w) for w in p.split()[:8] if n(w) and n(w) not in ('c','s','j')][:4]
    lastc = max([c for c in cuts if c is not None])
    for i in range(lastc + 1, len(W)):
        seq = [x for x in NW[i:i + 8] if x and x not in ('c','s')][:4]
        if seq == key: cuts.append(i); break
    else:
        cuts.append(None)
paras = []
for c, e in zip(cuts, EN):
    if c is None: paras[-1][1] += ' ' + e
    else: paras.append([c, e])
paras_la = [' '.join(W[paras[k][0]:(paras[k + 1][0] if k + 1 < len(paras) else len(W))]) for k in range(len(paras))]
paras_en = [p[1] for p in paras]
open(name + '_parts.txt', 'w', encoding='utf8').write('\n\n'.join(paras_la) + '\n')
open(name + '_en.txt', 'w', encoding='utf8').write('\n\n'.join(re.sub(r'\s+', ' ', e) for e in paras_en) + '\n')
print(len(paras_la), 'paragraphs', [c for c in cuts], file=sys.stderr)
