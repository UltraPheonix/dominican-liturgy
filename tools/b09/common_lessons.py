"""Matins lessons of the 1909 Commune Sanctorum (v1 pdf 1306-1432) from the OCR, repaired against the Vulgate / Divinum Officium
(matins.build_lesson) -> commonlessons1909.json {common: [lesson dicts]}. Only lessons whose text was matched against a reference
text ('src' vulgate/DO with a score >= 0.75) are kept; the rest are left out (the build shows 'in preparation').
usage: python3 tools/b09/common_lessons.py"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import matins as M, commune as C
OUT = os.path.join(HERE, 'commonlessons1909.json')
def score(x):
    m = re.match(r'(?:vulgate|DO) ([\d.]+)', x.get('src', '')); return float(m.group(1)) if m else 0.0
res = {}
for name, a, b in C.COMMONS:
    if name.endswith('_tp'): continue
    t = M.text_range(a, b); seen = {}
    for n, lt, rt in M.parse_day(t):
        if n in seen or not 1 <= n <= 9: continue          # the first set only (later 'Lectio iii' are octave/alternative sets)
        x = M.build_lesson(n, lt); seen[n] = x
    keep = [dict(x, score=score(x)) for n, x in sorted(seen.items()) if score(x) >= 0.75 and len(x.get('la', '')) > 80]
    res[name] = keep
    print(name, 'kept', [x['n'] for x in keep], 'of', sorted(seen))
json.dump(res, open(OUT, 'w'), ensure_ascii=False, indent=0)
