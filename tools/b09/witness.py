"""Second witness: the text layer of the PDFs (an older OCR, worse letter by letter but with its own, independent mistakes).
differences(piece, vol) aligns a piece read from the tesseract re-OCR with the same passage of the old layer and lists the places
where the two disagree in WORDS (a word missing, added or different while both are real words) — e.g. tesseract drops words at the
gutter ('quem vocávit Apóstolum, dum esset in mari' read as 'vocávit Apóstolum, dum in mari'). Such a piece must be read on the page."""
import os, re, gzip, collections, difflib
import latdict as LD, latcount as LC
HERE = os.path.dirname(os.path.abspath(__file__))
_W = {}
WORD = re.compile(r"[A-Za-zÀ-ÿǽæœÆŒǼ]+")
def load(vol):
    if vol not in _W:
        t = gzip.open(os.path.join(HERE, 'text/%s.txt.gz' % vol), 'rt', encoding='utf-8').read()
        t = re.sub(r'-\n(\S)', r'\1', t)
        ws = WORD.findall(t); bs = [LD.base(w) for w in ws]
        idx = collections.defaultdict(list)
        for i in range(len(bs) - 2): idx[(bs[i], bs[i + 1], bs[i + 2])].append(i)
        _W[vol] = (ws, bs, idx)
    return _W[vol]
def differences(piece, vol):
    """-> list of 'new|old' disagreements; ['not located'] if the passage is not found in the old layer"""
    ws, bs, idx = load(vol)
    pw = WORD.findall(piece); pb = [LD.base(w) for w in pw]
    if len(pb) < 4: return []
    votes = collections.Counter()
    for i in range(len(pb) - 2):
        for p in idx.get((pb[i], pb[i + 1], pb[i + 2]), ())[:50]: votes[(p - i) // 8] += 1
    if not votes: return ['not located']
    off = votes.most_common(1)[0][0] * 8
    lo = max(0, off - 6); hi = min(len(bs), off + len(pb) + 14)
    ob = bs[lo:hi]; ow = ws[lo:hi]
    sm = difflib.SequenceMatcher(None, pb, ob, autojunk=False)
    ops = sm.get_opcodes(); out = []
    # trim the old window to the span of the piece
    first = next((o for o in ops if o[0] == 'equal'), None); last = next((o for o in reversed(ops) if o[0] == 'equal'), None)
    if not first: return ['not located']
    real = lambda b: LC.N.get(b, 0) >= (3 if len(b) >= 4 else 300)   # short tokens of the old layer are mostly misread signs (y, f, JT)
    for tag, i1, i2, j1, j2 in ops:
        if tag == 'equal' or j2 <= first[3] or j1 >= last[4]: continue
        nb_, ob_ = pb[i1:i2], ob[j1:j2]
        if tag == 'insert' and any(real(b) for b in ob_): out.append('+' + ' '.join(ow[j1:j2]))            # the old layer has words the re-OCR lacks
        elif tag == 'delete' and any(real(b) for b in nb_): out.append('-' + ' '.join(pw[i1:i2]))
        elif tag == 'replace':
            if len(nb_) == len(ob_):
                for a, b, x, y in zip(nb_, ob_, pw[i1:i2], ow[j1:j2]):
                    if real(a) and real(b): out.append('%s|%s' % (x, y))                                       # two different real words
            elif any(real(b) for b in ob_) and sum(len(b) for b in ob_) > sum(len(b) for b in nb_) + 3: out.append('+' + ' '.join(ow[j1:j2]))
    return out
if __name__ == '__main__':
    print(differences('Dignum sibi Dóminus computávit Mártyrem, vocávit Apóstolum, dum in mari, allelúja.', 'v1'))
    print(differences('Mox ut vocem Dómini prædicántis audívit beátus Andréas, relíctis rátibus, quorum usu actúque vivébat', 'v1'))

def merge(piece, vol):
    """the re-OCR piece with the old layer's help: a word the re-OCR garbled (not a real word) is replaced by the old layer's word
    in the same place when that one is real; up to three small real words the re-OCR dropped between two agreeing words (the
    gutter) are restored. Everything else is left as read. -> text"""
    ws, bs, idx = load(vol)
    toks = re.findall(r"[A-Za-zÀ-ÿǽæœÆŒǼ]+|[^A-Za-zÀ-ÿǽæœÆŒǼ]+", piece)
    wi = [i for i, x in enumerate(toks) if WORD.fullmatch(x)]
    pb = [LD.base(toks[i]) for i in wi]
    if len(pb) < 4: return piece
    votes = collections.Counter()
    for i in range(len(pb) - 2):
        for p in idx.get((pb[i], pb[i + 1], pb[i + 2]), ())[:50]: votes[(p - i) // 8] += 1
    if not votes: return piece
    off = votes.most_common(1)[0][0] * 8
    lo = max(0, off - 6); hi = min(len(bs), off + len(pb) + 14)
    ob = bs[lo:hi]; ow = ws[lo:hi]
    real = lambda b: LC.N.get(b, 0) >= (3 if len(b) >= 4 else 300)
    ops = difflib.SequenceMatcher(None, pb, ob, autojunk=False).get_opcodes()
    eq = [o for o in ops if o[0] == 'equal']
    if not eq: return piece
    j_lo, j_hi = eq[0][3], eq[-1][4]
    def spell(b, like):
        h = LD.D.get(b, b)
        return h[:1].upper() + h[1:] if like[:1].isupper() else h
    ins = {}
    for tag, i1, i2, j1, j2 in ops:
        if j1 < j_lo or j2 > j_hi: continue
        if tag == 'replace' and i2 - i1 == j2 - j1:
            for d in range(i2 - i1):
                if not real(pb[i1 + d]) and real(ob[j1 + d]) and ob[j1 + d] in LD.D: toks[wi[i1 + d]] = spell(ob[j1 + d], toks[wi[i1 + d]])
        elif tag == 'insert' and 0 < i1 < len(pb) and j2 - j1 <= 3 and all(real(b) and b in LD.D and ow[j1 + k][:1].islower() for k, b in enumerate(ob[j1:j2])):
            ins[wi[i1]] = ' '.join(LD.D[b] for b in ob[j1:j2]) + ' '
    return ''.join(ins.get(i, '') + x for i, x in enumerate(toks))
