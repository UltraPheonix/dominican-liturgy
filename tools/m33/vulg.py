import os, re, collections, unicodedata
from parse import norm
B = '/home/claude/dominican-liturgy/bible/'
VER = {}   # (book, ch, v) -> (la, en)
ORDER = {}
for fn in sorted(os.listdir(B + 'la')):
    book = fn[:-4]
    en = {}
    if os.path.exists(B + 'en/' + fn):
        for l in open(B + 'en/' + fn):
            a = l.rstrip('\n').split('\t')
            if len(a) >= 3: en[(int(a[0]), int(a[1]))] = ' '.join(a[2:])
    for l in open(B + 'la/' + fn):
        a = l.rstrip('\n').split('\t')
        if len(a) >= 3:
            c, v = int(a[0]), int(a[1]); VER[(book, c, v)] = (' '.join(a[2:]), en.get((c, v), ''))
TRI = collections.defaultdict(set)
for key, (la, en) in VER.items():
    if key[0] == 'Psalmi': continue
    w = norm(la).split()
    for i in range(len(w) - 2): TRI[' '.join(w[i:i + 3])].add(key)
def locate(text, n=3):
    w = norm(text).split(); cnt = collections.Counter()
    for i in range(len(w) - 2):
        for key in TRI.get(' '.join(w[i:i + 3]), ()): cnt[(key[0], key[1])] += 1
    return cnt.most_common(n)
def chapter_words(book, ch):
    out = []  # (accented word, norm word, (ch, v))
    for c in (ch - 1, ch, ch + 1):
        v = 1
        while (book, c, v) in VER or v == 1:
            if (book, c, v) not in VER:
                if v > 1: break
                v += 1; continue
            for tok in VER[(book, c, v)][0].split():
                n = norm(tok)
                if n: out.append((tok, n, (c, v)))
            v += 1
    return out
