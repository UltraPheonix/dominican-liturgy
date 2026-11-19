import re, sys, pickle, difflib, unicodedata, json
sys.path.insert(0, '/home/claude/build/ten')
import os
R = pickle.load(open(os.environ.get('RES', '/home/claude/build/ten/res.pkl'), 'rb'))
CAND = {'a02': [7192], 'a03': [6425], 'a05': [7038], 'a07': [5643], 'a08': [5329, 5961], 'a09': [6908], 'a10': [6523], 'a11': [9990, 4734],
        'a12': [4592], 'a13': [5985], 'a14': [6007], 'a16': [5785], 'a17': [6858], 'a18': [15236], 'a21': [5890], 'a22': [4985], 'a25': [5513],
        'a27': [5871], 'a28': [6732], 'a29': [5500], 'a30': [5606, 9870], 'a31': [5974], 'a32': [18467], 'a01': [15297]}
def flat(s):
    s = s.replace('æ', 'ae').replace('œ', 'oe').replace('ǽ', 'ae')
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
    return re.sub(r'[^a-z]', '', s.lower().replace('j', 'i'))
def gb_tokens(fn):
    t = open(fn).read().split('%%', 1)[1]
    t = re.sub(r'<[^>]+>', '', t)
    clef = re.search(r'\(([cf][1-4])\)', t).group(1)
    toks = []
    for syl, n in re.findall(r'([^()\s]*)\(([^)]*)\)', t):
        if re.fullmatch(r'[cf]b?[1-4]', n): continue
        ps = re.findall(r'[a-mA-M]', re.sub(r'[xy][a-m]?', '', n))
        toks.append((syl, n, ''.join(p.lower() for p in ps)))
    return clef, toks
def iv(seq): return [ord(b) - ord(a) for a, b in zip(seq, seq[1:])]
if __name__ == '__main__':
    out = {}
    for code, ids in CAND.items():
        omr = ''.join(n for t, n, b in R[code]['out'] if n != '?')
        for gid in ids:
            clef, toks = gb_tokens('/home/claude/dl/gb/%d.gabc' % gid)
            gseq = ''.join(p for _, _, p in toks)
            sm = difflib.SequenceMatcher(None, iv(omr), iv(gseq), autojunk=False)
            # text similarity
            tx = flat(''.join(s for s, _, _ in toks)); bt = flat(' '.join(t for t, n, b in R[code]['out']))
            ts = difflib.SequenceMatcher(None, bt, tx, autojunk=False).ratio()
            print(code, gid, clef, 'notes %.2f' % sm.ratio(), 'text %.2f' % ts, len(omr), len(gseq))

def merge(code, gid):
    """book text (from the OMR result) with the GregoBase notes; returns (clef, [(syl, notes, bar)], unmatched book syllables)"""
    clef, toks = gb_tokens('/home/claude/dl/gb/%d.gabc' % gid)
    # gabc tokens with bars kept separately
    t = open('/home/claude/dl/gb/%d.gabc' % gid).read().split('%%', 1)[1]
    t = re.sub(r'<i>T\. ?P\.</i>.*$', '', t, flags=re.S)          # paschal alleluia appended
    t = re.sub(r'<[^>]+>', '', t)
    seq = []
    for syl, n in re.findall(r'([^()\s]*)\(([^)]*)\)', t):
        if re.fullmatch(r'[cf]b?[1-4]', n): continue
        if not flat(syl) and re.fullmatch(r'[:;,]+[0-9]?|::', n.strip()):
            if seq: seq[-1][2] = n.strip()
            continue
        if not flat(syl): continue
        seq.append([syl, n, None])
    book = R[code]['out']
    BF = [flat(s) for s, n, b in book]; GF = [flat(s) for s, n, b in seq]
    # align syllable by syllable on flat text
    sm = difflib.SequenceMatcher(None, BF, GF, autojunk=False)
    res = [[s, '?', b] for s, n, b in book]; miss = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal' or (tag == 'replace' and i2 - i1 == j2 - j1):
            for k in range(i2 - i1):
                res[i1 + k][1] = seq[j1 + k][1]; res[i1 + k][2] = seq[j1 + k][2]
        else:
            for k in range(i1, i2): miss.append((k, book[k][0]))
    return clef, res, miss
