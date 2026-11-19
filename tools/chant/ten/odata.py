import json, glob, re
R = '/home/claude/dominican-liturgy/data/office/'
com = json.load(open(R + 'common.json')); sh = {}
for f in glob.glob(R + 'psalter/*.json'): sh.update(json.load(open(f)))
def day(d): return json.load(open(R + d + '.json'))
def T(d, i): return d['b'].get(i) or com.get(i) or sh.get(i) or ''
def expand(t):
    out = []
    for l in t.split('\n'):
        if l.startswith('§'): out += expand(sh.get(l[1:].strip(), com.get(l[1:].strip(), '')))
        else: out.append(l)
    return out
def hour(d, h):
    D = day(d); return [(expand(T(D, a)), expand(T(D, b))) for a, b in D['h'][h]]
