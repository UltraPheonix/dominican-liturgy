import os, re, json, difflib, collections
from parse import norm
D = '/home/claude/do/web/www/missa/Latin/'
DOR = []
for sub in ('Tempora', 'Sancti', 'Commune'):
    for fn in os.listdir(D + sub):
        try: t = open(D + sub + '/' + fn, encoding='utf-8').read()
        except Exception: continue
        for m in re.finditer(r'\[(Lectio\w*|Evangelium\w*)\]\n(.*?)(?=\n\[|\Z)', t, re.S):
            lines = [l for l in m.group(2).split('\n') if l.strip()]
            if len(lines) < 3 or not lines[1].startswith('!'): continue
            body = ' '.join(l for l in lines[2:] if not l.startswith(('!', '@', '(', '$', '&')))
            if len(body) < 80: continue
            DOR.append({'src': sub + '/' + fn, 'head': lines[0], 'ref': lines[1][1:], 'text': body, 'w': norm(body).split()})
IDX = collections.defaultdict(set)
for i, r in enumerate(DOR):
    w = r['w']
    for j in range(0, min(len(w) - 4, 60)): IDX[' '.join(w[j:j + 5])].add(i)
def best(text):
    w = norm(text).split(); c = collections.Counter()
    for j in range(0, min(len(w) - 4, 80)):
        for i in IDX.get(' '.join(w[j:j + 5]), ()): c[i] += 1
    out = []
    for i, n in c.most_common(5):
        r = DOR[i]; sm = difflib.SequenceMatcher(None, w, r['w'], autojunk=False)
        out.append((sm.ratio(), i))
    return max(out) if out else (0, None)
import vulg
FORMW = {'in', 'illo', 'tempore', 'diebus', 'illis', 'fratres', 'carissimi', 'carissime', 'haec', 'dicit', 'dominus', 'deus'}
import readings as R
def fix_opening(text, first=None):
    """replace a garbled opening by the clean one of the same reading in the Roman Missal (Divinum Officium), keeping the rest"""
    r, i = best(text)
    if i is None or r < 0.75: return text, None, r
    d = DOR[i]
    toks = text.split(); dt = d['text'].split()
    a = [norm(t).replace(' ', '') for t in toks]; b = [norm(t).replace(' ', '') for t in dt]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    blk = next((x for x in sm.get_matching_blocks() if x.size >= 4), None)
    if not blk or blk.a > 12 or blk.b > 14: return text, d, r
    mine = [x for x in a[:blk.a] if x not in FORMW]
    dop = set(b[:blk.b])
    verse = set()
    if first:
        for dv in (-1, 0):
            verse |= set(norm(vulg.VER.get((first[0], first[1], first[2] + dv), ('', ''))[0]).split())
    clean = all(x in R.LEX for x in mine) and all(re.fullmatch(r"[\w\u00C0-\u017F\u0300-\u036f.,:;?!'’]+", t) for t in toks[:blk.a])
    dup = any(a[q] == a[q + 1] for q in range(min(blk.a, 6)))
    broken = not clean or dup or (mine and not all(x in verse or x in dop for x in mine))
    extra = blk.b - blk.a
    fa = [x for x in a[:blk.a] if x in FORMW]; fb = [x for x in b[:blk.b] if x in FORMW]
    if not (broken or (0 < extra <= 3 and fa == fb)): return text, d, r
    rest = toks[blk.a:]
    if rest and dt[:blk.b] and not re.search(r'[:.?!]$', dt[blk.b - 1]):
        rest = [R.accent(rest[0].lower()) if not R.accent(rest[0].lower())[:1].isupper() else R.accent(rest[0])] + rest[1:]
    new = ' '.join(dt[:blk.b] + rest)
    return new, d, r
if __name__ == '__main__':
    print(len(DOR))
    O = json.load(open('/home/claude/m33/readings33.json'))
    n = 0; ch = []
    for k, v in O.items():
        for r in v['readings']:
            new, d, sc = fix_opening(r['la'], r.get('first'))
            if d is not None and new.split()[:6] != r['la'].split()[:6]:
                n += 1; ch.append((k, r['la'][:60], '=>', new[:60]))
            r['la_fixed'] = new; r['do'] = d and d['src']; r['do_sim'] = round(sc, 2)
    json.dump(O, open('/home/claude/m33/readings33b.json', 'w'), ensure_ascii=False, indent=0)
    print(n); [print(c) for c in ch[:80]]
