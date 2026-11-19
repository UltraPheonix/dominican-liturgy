import json, re, difflib, unicodedata
M = json.load(open('m39masses.json'))
D = json.loads(open('/home/claude/build/site/data/masses.js', encoding='utf8').read().split('var DOMINICAN = ', 1)[1].rstrip().rstrip(';'))
O = json.loads(open('/home/claude/build/site/data/orations.js').read()[len('window.ORATIONS = '):].rstrip().rstrip(';'))
def flat(s):
    s = s.replace('æ', 'ae').replace('Æ', 'AE').replace('œ', 'oe').replace('^', 'AE')
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
    return s.lower().replace('j', 'i')
GEN = set('sancti sanctae sanctorum beati beatae virg virginis conf confessoris mart martyris martyrum ordinis praed praedicatorum episc episcopi pontificis abbatis doct doctoris eccl ecclesiae viduae papae presb regis reginae apostoli evangelistae et de in ii iii class festum duplex totum memoria semiduplex ian feb mart apr mai iun iul aug sept oct nov dec'.split())
def toks(s): return [w for w in re.findall(r'[a-z]{3,}', flat(s)) if w not in GEN]
def score(a, b):
    A, B = toks(a), toks(b)
    if not A or not B: return 0
    return sum(max(difflib.SequenceMatcher(None, x, y).ratio() for y in B) for x in A[:3]) / min(3, len(A))
miss = [k for k in D['masses'] if k not in O]
res = {}
for k in miss:
    m = D['masses'][k]
    if 'month' not in m: res[k] = None; continue
    title = re.sub(r'^\d+ \w+\.? — ', '', m['title'])
    best = None
    for x in M:
        dd = abs((x['month'] * 31 + x['day']) - (m['month'] * 31 + m['day']))
        if dd > 2: continue
        s = score(title, x['title']) - 0.05 * dd
        # the saint's name in the Collect confirms the match
        nm = [w for w in toks(title) if len(w) >= 5][:1]
        txt = flat(' '.join(x['pr'].values()))
        if nm and x['pr'] and any(difflib.SequenceMatcher(None, nm[0][:-2], txt[i:i + len(nm[0]) - 2]).ratio() > 0.85 for i in range(0, max(1, len(txt) - 4))): s += 0.4
        if not best or s > best[0]: best = (s, x)
    res[k] = best
ok = [k for k in res if res[k] and res[k][0] >= 0.7]
print(len(miss), 'missing;', len(ok), 'matched')
for k in miss:
    b = res[k]
    if not b or b[0] < 0.7: print('NO ', k, D['masses'][k]['title'][:50], '->', b and (round(b[0], 2), b[1]['month'] + 1, b[1]['day'], b[1]['title'][:40]))
json.dump({k: res[k][1] for k in ok}, open('matched.json', 'w'), ensure_ascii=False, indent=0)
