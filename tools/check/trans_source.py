"""Label the source of the English of each chant honestly.
An English text marked 'own' (AI) is relabelled when its wording is in fact the Douay-Rheims of the verses cited:
  'douay' - every word pair of the English is found in the Douay-Rheims of those verses;
  'dra'   - Douay-Rheims adapted to the words of the chant (at least 90% of word pairs, at most 3 words not in it).
Run from the repository root: python3 tools/check/trans_source.py [--write]"""
import sys, os, re, json
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, R + '/tools')
import douay_match as dm
BK = {v: k for k, v in dm.REF.items()}
BK.update({'Deut.': 'Deuteronomium', 'Prov.': 'Proverbia', 'Gal.': 'Ad Galatas', 'Rom.': 'Ad Romanos', 'Phil.': 'Ad Philippenses',
           'Heb.': 'Ad Hebræos', 'Eph.': 'Ad Ephesios', 'Col.': 'Ad Colossenses', 'Judith': 'Judith', 'Job': 'Job', 'Mal.': 'Malachias',
           'Ezech.': 'Ezechiel', 'Exod.': 'Exodus', 'Gen.': 'Genesis', 'Esth.': 'Esther', 'Tob.': 'Tobiæ', 'Bar.': 'Baruch',
           'Lam.': 'Lamentationes', 'Joel': 'Joel', 'Mich.': 'Michæa', 'Zach.': 'Zacharias', 'Acts': 'Actus Apostolorum',
           'Apoc.': 'Apocalypsis', 'Ecclus.': 'Ecclesiasticus', 'Wisd.': 'Sapientia', 'Cant.': 'Canticum Canticorum', 'Isa.': 'Isaias',
           'Jer.': 'Jeremias', 'Dan.': 'Daniel', 'Lev.': 'Leviticus', 'Num.': 'Numeri', '1 Cor.': 'Ad Corinthios 1', '2 Cor.': 'Ad Corinthios 2',
           'Jas.': 'Jacobi', '1 Pet.': 'Petri 1', '2 Pet.': 'Petri 2', 'Osee': 'Osee', 'Agg.': 'Aggæus', 'Soph.': 'Sophonias'})
def refverses(r):
    out = []; book = None
    for part in re.split(r';\s*', r or ''):
        m = re.match(r'^\s*((?:[1-4]\s)?[A-Z][A-Za-z]*\.?)?\s*(\d+),\s*([\d.\-, ]+)', part)
        if not m: continue
        if m.group(1): book = BK.get(m.group(1), m.group(1))
        ch = int(m.group(2))
        for x in re.split(r'[.,]\s*', m.group(3)):
            x = x.strip()
            if not x: continue
            a, _, b = x.partition('-')
            try: a = int(a); b = int(b) if b else a
            except ValueError: continue
            out += [(book, ch, v) for v in range(a, b + 1)]
    return out
def pairs(w): return [w[i] + ' ' + w[i + 1] for i in range(len(w) - 1)]
def judge(cid, v):
    ks = set(refverses(v.get('r')))
    f = R + '/gabc/%s.gabc' % cid
    if os.path.exists(f):
        for s in dm.gabc_text(open(f, encoding='utf8').read()).split('|'):
            b = dm.best_verses(s)
            if b: ks |= set(b)
    if not ks: return None
    drw = []
    for k in sorted(ks, key=lambda k: (k[0] or '', k[1], k[2])): drw += dm.words(dm.DR.get(k, ''))
    if not drw: return None
    en = re.sub(r'\(P\.\s*T\.[^)]*\)', '', v['t'])
    ew = [w for w in dm.words(en) if w != 'alleluia']
    if len(ew) < 6: return None
    dset, dp = set(drw), set(pairs(drw))
    extra = [w for w in ew if w not in dset]
    pp = pairs(ew); hit = sum(p in dp for p in pp) / max(1, len(pp))
    if not extra and hit >= 0.97: return 'douay'
    if len(extra) <= 3 and hit >= 0.9: return 'dra'
    return None
if __name__ == '__main__':
    F = R + '/data/masses.js'
    s = open(F, encoding='utf8').read(); head, js = s.split('var DOMINICAN = ', 1); D = json.loads(js.rstrip().rstrip(';'))
    G = R + '/tools/g50/trans.json'; GT = json.load(open(G, encoding='utf8'))
    ch = {}
    for cid, v in D['trans'].items():
        if v.get('s') != 'own': continue
        j = judge(cid, v)
        if j: ch[cid] = j
    import collections
    print(collections.Counter(ch.values()), 'of', sum(v.get('s') == 'own' for v in D['trans'].values()), 'own')
    for cid, j in list(ch.items()):
        print(cid, j, D['trans'][cid]['r'], '|', D['trans'][cid]['t'][:90])
    if '--write' in sys.argv:
        for cid, j in ch.items():
            D['trans'][cid]['s'] = j
            if cid in GT: GT[cid]['s'] = j
        open(F, 'w', encoding='utf8').write(head + 'var DOMINICAN = ' + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + ';\n')
        json.dump(GT, open(G, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        print('written')
