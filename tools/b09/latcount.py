"""word counts of the Divinum Officium Latin corpus (bases as latdict.base), to tell a real word from a typo in DO itself
(DO has a few OCR forms, e.g. 'pastdris'); cached in /tmp/b09/latcnt.json"""
import os, re, json, collections
import latdict as LD
CACHE = '/tmp/b09/latcnt.json'
def build():
    C = collections.Counter()
    for dp, dn, fn in os.walk(LD.ROOT):
        for f in fn:
            if f.endswith('.txt'):
                try: t = open(os.path.join(dp, f), encoding='utf-8').read()
                except Exception: continue
                C.update(LD.base(w) for w in re.findall(r"[A-Za-zÀ-ÿæœǽÆŒ]+", t))
    json.dump(C, open(CACHE, 'w')); return C
N = json.load(open(CACHE)) if os.path.exists(CACHE) else build()

import re
PAIRS = {('b', 'o'), ('d', 'e'), ('d', 'a'), ('b', 'a'), ('h', 'o'), ('f', 'i'), ('t', 'i'), ('r', 'i'), ('d', 'o'), ('c', 'e'), ('a', 'e'), ('i', 'e'), ('i', 'l'), ('l', 'i'), ('n', 'u'), ('u', 'n'), ('t', 'f'), ('r', 'c'), ('e', 'c'), ('o', 'a'),
         ('a', 'o'), ('k', 'e'), ('h', 'b'), ('b', 'h'), ('i', 't'), ('f', 's'), ('s', 'f'), ('e', 'a'), ('m', 'n'), ('n', 'm')}
def ocr_word(x, LD):
    """an OCR word not in the dictionary: one substitution of a usual OCR confusion (pastdris -> pastóris, concade -> concéde);
    junk of 1-3 letters not in the dictionary is dropped (None)"""
    m = re.match(r'^(\W*)([A-Za-z]+)(\W*)$', x)
    if not m: return x
    pre, core, post = m.groups(); b = LD.base(core); n = N.get(b, 0)
    if n >= 3: return x
    if len(core) <= 3 and re.fullmatch(r'[Il][il]+', core): return pre.strip() + post.strip() or None
    if len(core) <= 3 and n == 0 and core.lower() not in ('et', 'in', 'ad', 'ut', 'a', 'e', 'o'): return pre.strip() + post.strip() or None
    c = [k for k in LD.near(b) if [(p, q) for p, q in zip(b, k) if p != q][0] in PAIRS and N.get(k, 0) >= max(10, 20 * n)]
    if len(c) > 1: c = sorted(c, key=lambda k: -N.get(k, 0))[:1] if N.get(c[0], 0) > 0 and sorted((N.get(k, 0) for k in c))[-1] >= 5 * sorted((N.get(k, 0) for k in c))[-2] else []
    if len(c) != 1: return x
    h = LD.D[c[0]]; h = h[:1].upper() + h[1:] if core[:1].isupper() else h
    return pre + h + post
def fix_text(t):
    """word repairs of an OCR text: accents (latdict), usual OCR confusions against the corpus counts, æ read as 'a?' / 'se'"""
    out = []
    for x in t.split():
        m = re.match(r'^(\W*)([A-Za-z]+?)(se|a\?|a:|qua\?)(\W*)$', x)
        if m and LD.base(m.group(2) + 'ae') in LD.D and N.get(LD.base(m.group(2) + m.group(3)), 0) < 3:
            h = LD.D[LD.base(m.group(2) + 'ae')]; h = h[:1].upper() + h[1:] if m.group(2)[:1].isupper() else h
            out.append(m.group(1) + h + m.group(4).replace('?', '').replace(':', '')); continue
        y = LD.fix_word(x)
        if y == x: y = ocr_word(x, LD)
        if y is not None: out.append(y)
    t = ' '.join(out); t = re.sub(r'\s+([;:,.?!])', r'\1', t); t = re.sub(r'[»«]', ',', t); t = re.sub(r'a\?(?=\s|$)', 'æ', t)
    return re.sub(r',\s*,', ',', t)
