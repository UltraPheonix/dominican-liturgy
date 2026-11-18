"""mkps.py CH [CH...] -> .src lines for whole psalms/canticles (Latin + English from the site's psalter), one T per verse.
CH is the first verse tag as in the psalter, e.g. 115:1  119:1  139:2  140:1  141:2  1:46 (Magnificat)."""
import json, glob, re, sys
D = {}
for f in glob.glob('/home/claude/build/site/data/office/psalter/*.json'): D.update(json.load(open(f)))
def verses(v): return [(m.group(1), m.group(2).strip()) for m in re.finditer(r'<n>([\d:]+)</n>\s*([^\n]*)', v)]
la = {}; en = {}
for k, v in D.items():
    vs = verses(v)
    if not vs: continue
    first = vs[0][0]
    isla = bool(re.search(r'[áéíóúǽ]', v[:400]))
    (la if isla else en).setdefault(first, vs)
for ch in sys.argv[1:]:
    L, E = la[ch], en.get(ch)
    E = E or []
    assert len(E) == len(L), (ch, len(L), len(E))
    for (n, t), (n2, e) in zip(L, E):
        print('T: ' + t.replace('j', 'i').replace('J', 'I'))
        if e: print(' = ' + e)
    print('#---')
