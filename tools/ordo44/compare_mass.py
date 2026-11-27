"""Compare the conventual Mass the Ordo O.P. 1944 prescribes (where it says so) with the engine's first Mass.
usage: compare_mass.py /tmp/e44.json tools/ordo44/ordo1944b.json"""
import sys, json, re
E = {r['date']: r for r in json.load(open(sys.argv[1]))}; O = json.load(open(sys.argv[2]))
def sq(t): return re.sub(r'\s+', ' ', re.sub(r'(?<=\w) (?=\w\b)', '', t))
def ordo_kind(t):
    t = sq(t)
    m = re.search(r'1-a M\s?i\s?s\s?s\s?a\s+c\s?o\s?n\s?v\.?\s+i\s?n\s+C\s?h\s?o\s?r\s?[oa]\w*\s+d\s?e\s+(\w+)', t)
    if m: return 'choir:' + m.group(1).lower()[:4]
    if re.search(r'Missa\s+co[dn]v\.?\s+[un]nica\s+de\s+R\s?equiem', t): return 'requiem'
    if re.search(r'Missa\s+conv\.?\s+unica\s+de\s+A\s?nniv', t): return 'anniv'
    if re.search(r'2\s+Missae\s+conv(ent)?\.?\s+in\s+C\s?h\s?o\s?r\s?o\s*:?\s*u\s?n\s?a\s+de\s+(festo|die)', t): return 'feast+anniv'
    if re.search(r'Missa\s+conv\.?\s+unica\s+de\s+Dom', t): return 'dom'
    return None
def eng_kind(r):
    ms = r['masses']
    if not ms: return '-'
    k = ms[0]['key']; lab = ms[0]['label']
    if k == 'C114s': return 'requiem'
    if ms[0].get('anniv'): return 'anniv'
    if any(m.get('anniv') for m in ms): return 'feast+anniv'
    if 'Sunday (resumed' in lab: return 'choir:dom' if r['twoMasses'] else 'dom'
    if r['twoMasses']:
        if lab.startswith('In choir: the feast'): return 'choir:fest'
        if 'vigil' in lab: return 'choir:vigi'
        if 'Rogation' in lab: return 'choir:roga'
        return 'choir:feri'
    return 'single:' + (r['office']['kind'])
bad = 0
for o in O:
    if not o['text'] or o['date'] not in E: continue
    ok = ordo_kind(o['text'])
    if not ok: continue
    ek = eng_kind(E[o['date']])
    same = ek == ok or (ok == 'choir:dom' and ek == 'choir:dom') or (ok.startswith('choir:fe') and ek == 'choir:feri') or (ok == 'choir:dom.' and ek.startswith('single')) 
    if ok in ('choir:feri', 'choir:fer.') and ek == 'choir:feri': same = True
    if not same:
        bad += 1
        print(o['date'], 'Ordo:', ok, '| engine:', ek, [m['key'] for m in E[o['date']]['masses']], E[o['date']]['office'].get('title', '')[:40])
print(bad, 'differ')
