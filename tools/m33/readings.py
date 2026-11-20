import json, re, collections, difflib
from collections import namedtuple
B = namedtuple('B', 'a b size')
from parse import norm, HR, L
import vulg
ANCH = json.load(open('/home/claude/m33/anchors.json'))
LEX = collections.defaultdict(collections.Counter)
for (b, c, v), (la, en) in vulg.VER.items():
    for t in la.split():
        n = norm(t)
        if n and ' ' not in n: LEX[n][re.sub(r'[^\wæœǽÆŒ̀-ͯ]', '', t, flags=re.U)] += 1
FORM = {'in illo tempore': ('In illo témpore', 'At that time'), 'fratres': ('Fratres', 'Brethren'), 'carissimi': ('Caríssimi', 'Dearly beloved'),
        'in diebus illis': ('In diébus illis', 'In those days'), 'haec dicit dominus': ('Hæc dicit Dóminus', 'Thus saith the Lord'),
        'haec dicit dominus deus': ('Hæc dicit Dóminus Deus', 'Thus saith the Lord God'), 'dixit dominus': ('Dixit Dóminus', 'The Lord said'),
        'fratres mei': ('Fratres mei', 'My brethren'), 'dilectissimi': ('Dilectíssimi', 'Dearly beloved')}
STOP = {'gradual', 'alleluia', 'tract', 'offertory', 'credo', 'introit', 'oratio', 'secret', 'communion', 'postcommunion', 'lesson', 'gospel', 'sequence', 'gloria'}
def fuzzy(a, b):
    return a == b or (len(a) > 3 and len(b) > 3 and (a[-4:] == b[-4:] or difflib.SequenceMatcher(None, a, b).ratio() >= 0.75))
def accent(tok):
    n = norm(tok)
    if not n or ' ' in n: return tok
    best = LEX.get(n)
    if not best: return tok
    w = best.most_common(1)[0][0]
    lead = re.match(r'^\W*', tok).group(); trail = re.search(r'\W*$', tok).group()
    if tok[len(lead):len(lead) + 1].isupper(): w = w[0].upper() + w[1:]
    return lead + w + trail
def readings_of(key):
    a = ANCH[key]['line']; out = []
    i = a; started = False
    # go to the next lesson/gospel headings until the next Mass (introit) or offertory after a gospel
    cur = None
    while i < len(L) and i < a + 1500:
        pg, kind, l = L[i]
        k = next((k for k, r in HR if r.match(l)), None)
        if k == 'introit' and i > a + 2: break
        if k in ('lesson', 'gospel'):
            cur = {'kind': k, 'head': l, 'body': [], 'page': pg}; out.append(cur)
        elif k in STOP:
            if cur and cur['kind'] == 'gospel' and k in ('offertory', 'credo'): cur = None; break
            cur = None
        elif cur is not None: cur['body'].append(l)
        i += 1
    for r in out:
        b = r['body']; cut = 0
        for j in range(min(4, len(b))):
            if re.search(r'(^|\s)(c|cap)\.\s*\d+\s*\S{0,3}$', b[j]) or re.match(r'^[A-Z][a-z]{1,6}\.\s*\d+(\s*et\s*\d+)?\s*\S{0,2}$', b[j]): cut = j + 1
        if not cut and (r['head'].endswith('\xad') or r['head'].endswith('-')): cut = 1
        r['head'] = join([r['head']] + b[:cut]); r['body'] = b[cut:]
    return out
def join(ls):
    s = ''
    for l in ls:
        if s.endswith('\xad') or s.endswith('-'): s = s[:-1] + l
        else: s += (' ' if s else '') + l
    return re.sub(r'\s+', ' ', s).strip()
HINT = [('matth', 'Matthæus'), ('marcum', 'Marcus'), ('lucam', 'Lucas'), ('joannem', 'Joannes'), ('romanos', 'Ad Romanos'), ('corinth', 'Ad Corinthios'), ('galatas', 'Ad Galatas'), ('ephes', 'Ad Ephesios'), ('philipp', 'Ad Philippenses'), ('coloss', 'Ad Colossenses'), ('thessal', 'Ad Thessalonicenses'), ('timoth', 'Ad Timotheum'), ('titum', 'Ad Titum'), ('hebr', 'Ad Hebræos'), ('isaiae', 'Isaias'), ('jeremiae', 'Jeremias'), ('ezechiel', 'Ezechiel'), ('daniel', 'Daniel'), ('actuum', 'Actus Apostolorum'), ('apocal', 'Apocalypsis'), ('petri', 'Petri'), ('jacobi', 'Jacobi'), ('eccli', 'Ecclesiasticus'), ('prov', 'Proverbia'), ('cant', 'Canticum Canticorum'), ('exodi', 'Exodus'), ('genesis', 'Genesis'), ('regum', 'Regum'), ('joel', 'Joel'), ('osee', 'Osee'), ('zachar', 'Zacharias'), ('malach', 'Malachias')]
def align(raw, head=''):
    toks = []
    for t in raw.split():
        if norm(t): toks.append(t)
        elif toks: toks[-1] += t
    ow = [norm(t).replace(' ', '') for t in toks]
    loc = vulg.locate(raw, 12)
    hn = norm(head).replace(' ', '')
    hint = [b for k, b in HINT if k in hn]
    if hint:
        l2 = [x for x in loc if any(x[0][0].startswith(h) for h in hint)]
        if l2: loc = l2
    if not loc: return None
    (book, ch), score = loc[0]
    V = vulg.chapter_words(book, ch); vw = [x[1] for x in V]
    sm = difflib.SequenceMatcher(None, ow, vw, autojunk=False)
    blocks = [b for b in sm.get_matching_blocks() if b.size >= 3]
    if not blocks: return None
    # keep the largest consistent run of blocks (drop strays far away in the chapter)
    a0, b0 = blocks[0].a, blocks[0].b
    out = []; en_vs = []; omitted = False
    # prefix
    # the opening: the Missal's first words often differ a little from the Vulgate (a word left out), so match the words before the
    # first long run one by one against the Vulgate just before it
    lo = max(0, b0 - 40)
    sm2 = difflib.SequenceMatcher(None, ow[:a0], vw[lo:b0], autojunk=False)
    FORMW = {'fratres', 'in', 'illo', 'tempore', 'diebus', 'illis', 'carissimi', 'carissime', 'haec', 'dicit', 'dominus', 'deus'}
    for bl in sm2.get_matching_blocks():
        if bl.size and bl.a <= 10 and not all(ow[bl.a + q] in FORMW for q in range(bl.size)):
            b0 = lo + bl.b - bl.a + bl.a if False else lo + bl.b; a0 = bl.a; break
    pre = toks[:a0]
    k = b0
    while pre and k > 0 and (fuzzy(norm(pre[-1]).replace(' ', ''), vw[k - 1]) or (len(pre) == 1 and norm(pre[-1]).replace(' ', '')[-2:] == vw[k - 1][-2:] and len(norm(pre[-1])) <= len(vw[k - 1]) + 3)):
        pre.pop(); k -= 1
    vstart = k
    prefix = ' '.join(accent(t) for t in pre)
    words = []; used = []
    last = None
    blocks = [B(a0, b0, 0)] + [b for b in blocks if b.b >= b0 and b.a >= a0]
    for j, bl in enumerate(blocks):
        if j == 0:
            words += [V[x][0] for x in range(vstart, bl.b + bl.size)]; used += [V[x][2] for x in range(vstart, bl.b + bl.size)]
        else:
            pa = blocks[j - 1]; go = bl.a - (pa.a + pa.size); gv = bl.b - (pa.b + pa.size)
            if gv < 0 or go < 0: continue
            og = toks[pa.a + pa.size:bl.a]
            clean = all(norm(t).replace(' ', '') in LEX for t in og)
            if gv > 8 and go <= 3: omitted = True                               # verses left out by the Missal
            elif go == 0: pass                                                   # words the Missal leaves out
            elif clean and go <= 4 and go != gv: words += [accent(t) for t in og]   # the Missal's own words
            elif gv == 0: pass                                                   # stray text (another column, a rubric)
            else: words += [V[x][0] for x in range(pa.b + pa.size, bl.b)]; used += [V[x][2] for x in range(pa.b + pa.size, bl.b)]
            words += [V[x][0] for x in range(bl.b, bl.b + bl.size)]; used += [V[x][2] for x in range(bl.b, bl.b + bl.size)]
        last = bl
    # tail: extend while OCR keeps matching fuzzily
    ea, eb = last.a + last.size, last.b + last.size
    while ea < len(ow) and eb < len(vw) and fuzzy(ow[ea], vw[eb]): words.append(V[eb][0]); used.append(V[eb][2]); ea += 1; eb += 1
    first_v = V[vstart][2]; last_v = V[eb - 1][2]
    words[-1] = re.sub(r'[,;:]$', '.', words[-1])
    return {'book': book, 'from': first_v, 'to': last_v, 'prefix': prefix, 'text': ' '.join(words), 'omitted': omitted,
            'tail_left': len(ow) - ea, 'verses': sorted(set(used)), 'midverse': vstart > 0 and V[vstart - 1][2] == V[vstart][2], 'pre_ocr': ' '.join(toks[:a0]), 'matched': sum(b.size for b in blocks), 'n': len(ow)}
if __name__ == '__main__':
    import sys
    for key in sys.argv[1:]:
        for r in readings_of(key):
            body = join(r['body'])
            res = align(body)
            print(key, r['kind'], '|', r['head'][:90]); print('   ', res and {k: v for k, v in res.items() if k != 'text'}); print('   ', res and (res['prefix'] + ' || ' + res['text'])[:600])
