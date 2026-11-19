"""Accent the Missal's unaccented Latin from a dictionary of accented forms (Divinum Officium, the site's texts)."""
import os, re, json, unicodedata, collections
def flat(w):
    w = w.replace('æ', 'ae').replace('Æ', 'Ae').replace('œ', 'oe').replace('Œ', 'Oe').replace('ǽ', 'ae').replace('Ǽ', 'Ae')
    w = ''.join(c for c in unicodedata.normalize('NFD', w) if not unicodedata.combining(c))
    return w.lower().replace('j', 'i')
WORD = re.compile(r"[A-Za-zÀ-ÿæœǽÆŒǼ]+")
def build():
    cnt = collections.defaultdict(collections.Counter)
    roots = ['/home/claude/src/do/web/www/missa/Latin', '/home/claude/src/do/web/www/horas/Latin']
    files = []
    for r in roots:
        for dp, dn, fn in os.walk(r):
            files += [os.path.join(dp, f) for f in fn if f.endswith('.txt')]
    files += ['/home/claude/build/site/data/orations.js', '/home/claude/build/site/data/ordo.js', '/home/claude/build/site/data/prefaces.js', '/home/claude/build/site/data/holyweek_text.js']
    for f in files:
        try: t = open(f, encoding='utf8', errors='ignore').read()
        except Exception: continue
        for w in WORD.findall(t):
            lw = w.lower()
            if lw == flat(lw) and len(lw) > 2 and not re.search(r'[áéíóúýǽ]', lw):
                # unaccented forms count only for words of two syllables
                pass
            cnt[flat(w)][lw.replace('j', 'i')] += 1
    D = {}
    for k, c in cnt.items():
        acc = [(n, w) for w, n in c.items() if re.search(r'[áéíóúýǽæœ]', w)]
        plain = c.get(k, 0)
        if acc:
            n, w = max(acc)
            if n >= plain * 0.3: D[k] = w
            else: D[k] = k
        else: D[k] = k
    json.dump(D, open('accdict.json', 'w'), ensure_ascii=False)
    return D
D = json.load(open('accdict.json')) if os.path.exists('accdict.json') else build()
def accent_word(w, unknown):
    k = flat(w)
    if k not in D:
        unknown.append(w); return w
    a = D[k]
    # keep the Missal's j and the capital
    out = ''
    for i, ch in enumerate(a):
        src = w[i] if i < len(w) else ''
        if ch in 'iíì' and src in 'jJ': ch = 'j'
        out += ch
    # ae/oe ligatures change the length; rebuild by walking
    if len(a) != len(w):
        out = a
        if 'j' in w.lower():
            # put the j back where the Missal has it
            fw = flat(w); out2 = ''; j = 0
            for ch in a:
                out2 += ch
            out = out2
    if w[0].isupper(): out = out[0].upper() + out[1:]
    if w.isupper() and len(w) > 1: out = out[0] + out[1:].lower() if not w.isupper() else out.capitalize()
    return out
def accent(t):
    unknown = []
    r = WORD.sub(lambda m: accent_word(m.group(0), unknown), t)
    return r, unknown
if __name__ == '__main__':
    import sys
    D = build()
    print(len(D))
    for s in ['DEUS, qui Praedicatorum Ordinem copiosa Sanctorum sobole fecundare dignatus es, atque in ipsis heroica omnium virtutum merita sublimiter coronasti; da nobis illorum sequi vestigia: ut quos hodie sub una celebritate veneramur in terris; iis perpetua tandem festivitate associemur in caelis: Per Dominum.', 'Su sc ipe Domine munera, quae in ejus tibi solemnitate deferimus, cujus nos confidimus patrocinio liberari.']:
        print(accent(s))
