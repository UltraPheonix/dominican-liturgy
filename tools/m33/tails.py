"""Readings cut at a page break in the 1933 scan, completed from the Missale O.P. 1939 (tools/m33/tails.json).
Idempotent: each [old, new] pair is a suffix replacement, applied only while the field still ends with `old`
(and not already with `new`). Works on the dict before run.sh writes it, or standalone on data/readings33.js
(also after tools/requiem/build.py):  python3 tools/m33/tails.py"""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(H))
def apply(out, log=print):
    n = 0
    for t in json.load(open(H + '/tails.json', encoding='utf8')):
        for r in out.get(t['k'], []):
            if r.get('ref') not in (t['ref'], t.get('new_ref', t['ref'])): continue
            for f in ('la', 'en'):
                for old, new in t.get(f, []):
                    s = r.get(f, '').rstrip()
                    if s.endswith(new): continue
                    if s.endswith(old): r[f] = s[:len(s) - len(old)] + new; n += 1
                    else: log('tails: %s %s %s: ending not found' % (t['k'], t['ref'], f))
            if t.get('new_ref'): r['ref'] = t['new_ref']
    return n
if __name__ == '__main__':
    P = R + '/data/readings33.js'; V = 'var READINGS33 = '
    s = open(P, encoding='utf8').read(); i = s.index(V) + len(V); j = s.rstrip().rstrip(';').rindex('}') + 1
    D = json.loads(s[i:j]); n = apply(D)
    open(P, 'w', encoding='utf8').write(s[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:])
    print(n, 'tail fixes applied from tools/m33/tails.json')
