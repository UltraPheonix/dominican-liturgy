"""Generic Commune-copy writer."""
import re
from fx import add, get, refresh
RF = 'data/readings33.js'
def fixed(key, idx, reps):
    la = get(RF, [key, idx, 'la'])
    for a, b in reps:
        n = la.count(a)
        assert n == 1, (key, idx, a, n)
        la = la.replace(a, b)
    return la
def canon_entry(key, idx, reps, src, why):
    la = fixed(key, idx, reps)
    if add(RF, [key, idx, 'la'], la, src, why): print('  +', key, idx, 'la')
    return la
def copies(la, en, en_src, tgts, src, why, whyen):
    n = 0
    for k, i in tgts:
        if add(RF, [k, i, 'la'], la, src, why): print('  +', k, i, 'la'); n += 1
        if en is not None:
            if add(RF, [k, i, 'en'], en, src, whyen): print('  +', k, i, 'en'); n += 1
            e = get(RF, [k, i])
            if en_src is not None and e.get('en_src') != en_src:
                if 'en_src' in e: ok = add(RF, [k, i, 'en_src'], en_src, src, 'label as the Commune copy: ' + whyen)
                else: ok = add(RF, [k, i, 'en_src'], en_src, src, 'label as the Commune copy: ' + whyen, op='add')
                if ok: print('  +', k, i, 'en_src'); n += 1
    return n
