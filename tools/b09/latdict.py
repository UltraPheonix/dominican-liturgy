"""Accent restoration for the 1909 OCR: a dictionary of accented Latin word forms from Divinum Officium
(/home/claude/divinumofficium/divinum-officium/web/www/horas/Latin), and a fixer for OCR words.
usage: from latdict import fix_line"""
import os, re, unicodedata, collections, json
ROOT = '/home/claude/divinumofficium/divinum-officium/web/www/horas/Latin'
CACHE = '/tmp/b09/latdict2.json'
def base(w):
    w = unicodedata.normalize('NFD', w.lower()); w = ''.join(c for c in w if unicodedata.category(c) != 'Mn')
    return w.replace('æ', 'ae').replace('œ', 'oe').replace('j', 'i')
def build():
    C = collections.defaultdict(collections.Counter)
    for dp, dn, fn in os.walk(ROOT):
        for f in fn:
            if not f.endswith('.txt'): continue
            try: t = open(os.path.join(dp, f), encoding='utf-8').read()
            except Exception: continue
            for w in re.findall(r"[A-Za-zÀ-ÿæœǽÆŒ]+", t): C[base(w)][w.lower()] += 1
    D = {k: v.most_common(1)[0][0] for k, v in C.items()}
    json.dump(D, open(CACHE, 'w'), ensure_ascii=False); return D
D = json.load(open(CACHE)) if os.path.exists(CACHE) else build()
BYLEN = collections.defaultdict(list)
for k in D: BYLEN[len(k)].append(k)
OCRMAP = str.maketrans({'6': 'o', '0': 'o', '1': 'l', '5': 's', '8': 'a', '$': 's'})
def near(w):
    """words in D at edit distance 1 (substitution) from w"""
    out = []
    for k in BYLEN.get(len(w), []):
        if sum(a != b for a, b in zip(k, w)) == 1: out.append(k)
    return out
def fix_word(w):
    m = re.match(r"^([^A-Za-z0-9$]*)([A-Za-z0-9$]+)([^A-Za-z0-9$]*)$", w)
    if not m: return w
    pre, core, post = m.groups()
    cap = core[:1].isupper()
    b = base(core.translate(OCRMAP))
    hit = D.get(b)
    if not hit:
        # 'd' / 'a' confusion for an accented a (declindmus -> declinámus): try replacing letters
        cands = near(b)
        if len(cands) == 1: hit = D[cands[0]]
        elif cands:
            best = max(cands, key=lambda k: 0)  # ambiguous: leave as is
            hit = None
    if not hit: return w
    if cap: hit = hit[:1].upper() + hit[1:]
    return pre + hit + post
def fix_line(l): return ' '.join(fix_word(w) for w in l.split())
if __name__ == '__main__':
    import sys
    for l in sys.stdin: print(fix_line(l.rstrip('\n')))
