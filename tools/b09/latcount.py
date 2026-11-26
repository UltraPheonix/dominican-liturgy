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
