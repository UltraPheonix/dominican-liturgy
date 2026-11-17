"""English for chants with no translation in the St. Dominic Missal: find the Latin of the chant in the
Vulgate (by shared words), and give the Douay-Rheims of the same verses."""
import re, os, json, glob, unicodedata, collections
JG = '/home/claude/src/jgabc'
def norm(s):
    s = ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if not unicodedata.combining(c))
    return s.replace('j', 'i').replace('æ', 'ae').replace('œ', 'oe')
def words(s): return re.findall(r'[a-z]+', norm(s))
VUL, DR = {}, {}
for f in glob.glob(JG + '/vulgate/*.txt'):
    b = os.path.basename(f)[:-4]
    for l in open(f, encoding='utf8'):
        p = l.rstrip('\n').split('\t')
        if len(p) >= 3: VUL[(b, int(p[0]), int(p[1]))] = ' '.join(p[2:])
for f in glob.glob(JG + '/douay-rheims/*.txt'):
    b = os.path.basename(f)[:-4]
    for l in open(f, encoding='utf8'):
        p = l.rstrip('\n').split('\t')
        if len(p) >= 3: DR[(b, int(p[0]), int(p[1]))] = ' '.join(p[2:])
keys = list(VUL)
vw = {k: words(v) for k, v in VUL.items()}
# index: word trigram -> verses
idx = collections.defaultdict(set)
for k, w in vw.items():
    for i in range(len(w) - 2):
        idx[' '.join(w[i:i + 3])].add(k)
def gabc_text(g):
    body = g.split('%%', 1)[-1]
    t = re.sub(r'<sp>V/</sp>\.?', ' | ', body)
    t = re.sub(r'\([^)]*\)', '', t); t = re.sub(r'\[[^\]]*\]', '', t); t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'[{}*†_^]', '', t)
    t = re.sub(r'\bGl[oó]ri\s*-?\s*a\b.*$', '', t)              # stop at the Gloria Patri
    t = re.sub(r'T\.\s*P\..*?(?=\||$)', '', t)
    return re.sub(r'\s+', ' ', t).strip()
def best_verses(seg):
    w = [x for x in words(seg) if x not in ('alleluia',)]
    if len(w) < 4: return None
    votes = collections.Counter()
    for i in range(len(w) - 2):
        for k in idx.get(' '.join(w[i:i + 3]), ()): votes[k] += 1
    if not votes: return None
    tri = max(1, len(w) - 2)
    # the best verse, and its neighbours that also share words (a chant often spans two verses)
    k, v = votes.most_common(1)[0]
    if v / tri < 0.25: return None
    out = [k]
    for d in (1, 2):
        nk = (k[0], k[1], k[2] + d)
        if votes.get(nk, 0) >= 2: out.append(nk)
        pk = (k[0], k[1], k[2] - d)
        if votes.get(pk, 0) >= 2: out.insert(0, pk)
    return out
REF = {'Psalmi': 'Ps.', 'Isaias': 'Isa.', 'Ecclesiasticus': 'Ecclus.', 'Sapientia': 'Wisd.', 'Matthæus': 'Matt.', 'Lucas': 'Luke',
       'Joannes': 'John', 'Marcus': 'Mark', 'Jeremias': 'Jer.', 'Canticum Canticorum': 'Cant.', 'Daniel': 'Dan.', 'Apocalypsis': 'Apoc.'}
def ref_of(vs):
    b, c, v = vs[0]; e = vs[-1][2]
    return '%s %d, %d%s' % (REF.get(b, b), c, v, ('-%d' % e) if e != v else '')
if __name__ == '__main__':
    D = json.loads(open('site/data/masses.js', encoding='utf8').read().split('var DOMINICAN = ', 1)[1].rstrip().rstrip(';'))
    used = set()
    for m in D['masses'].values():
        for p, v in m['parts'].items():
            for c in v: used.add(str(c['id']))
        for se in (m.get('season') or {}).values():
            for v in se.values():
                for c in v: used.add(str(c['id']))
    out = {}
    for cid in used:
        if cid in D['trans'] and not D['trans'][cid].get('s') == 'douay': continue
        f = ('site/gabc/r/%s.gabc' % cid[1:]) if cid.startswith('r') else ('site/gabc/%s.gabc' % cid)
        if not os.path.exists(f): continue
        text = gabc_text(open(f, encoding='utf8').read())
        segs = [s.strip() for s in text.split('|') if s.strip()]
        en, refs = [], []
        for i, s in enumerate(segs):
            vs = best_verses(s)
            if not vs: continue
            en.append(('℣. ' if i else '') + ' '.join(DR.get(k, '') for k in vs).strip())
            refs.append(ref_of(vs))
        if en:
            out[cid] = {'t': ' '.join(en), 'r': refs[0], 'douay': True}
    json.dump(out, open('douay_trans.json', 'w'), ensure_ascii=False, indent=0)
    print('chants needing English', sum(1 for c in used if c not in D['trans'] and not c.startswith('r')), '; given Douay-Rheims', len(out))
    for k in list(out)[:4]: print(k, out[k]['r'], '|', out[k]['t'][:160])
