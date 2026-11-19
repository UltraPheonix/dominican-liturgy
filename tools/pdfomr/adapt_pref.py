"""Prefaces that have no chant in the Missale O.P. (1939) Appendix (Sacred Heart, St Thomas Aquinas), fitted to the
solemn tone as the Appendix's own Prefaces use it:
  - each sentence opens on f and recites on h;
  - the clause before the last ends with the mediant: syllable before the last accent gf, the accent fg, after it g;
  - the last clause recites on g and closes with the final cadence: fe ef g before the accent, fg on it, f after it;
  - the dialogue, the Vere dignum and the closing (Et ideo ... dicentes) are copied from the Preface of St Dominic.
writes gabc/op-m39-praef-<slug>-solemn.gabc, marked 'adapted'"""
import os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, HERE)
src = open(os.path.join(HERE, 'm39pref.py')).read()
ns = {}
exec("import unicodedata\nfrom syl import base, isv as _isv\n" + src[src.index('def isv'):src.index('\nROOT')], ns)
syllables = ns['syllables']
ACC = set('áéíóúýǽÁÉÍÓÚǼ')

def words(text):
    """[(syllables, accent index or None, trailing punctuation)]"""
    out = []
    for w in text.split():
        core = re.sub(r'[^A-Za-zÀ-ÿæœǽÆŒǼ]', '', w)
        if not core: continue
        lead = w[:w.index(core[0])]; tail = w[len(lead) + len(core):]
        st = syllables(core); sy = [core[a:b] for a, b in zip(st, st[1:] + [len(core)])]
        acc = next((i for i, s in enumerate(sy) if set(s) & ACC), None)
        if acc is None and len(sy) >= 2: acc = len(sy) - 2
        sy[0] = lead + sy[0]
        out.append((sy, acc, tail))
    return out

def clauses(text):
    """split into sentences (ending in . or :) of clauses (ending in , or ;)"""
    sents = []; cur = []; cl = []
    for w in words(text):
        cl.append(w)
        p = w[2]
        if any(c in p for c in '.:'): cur.append(cl); sents.append(cur); cur = []; cl = []
        elif any(c in p for c in ',;'): cur.append(cl); cl = []
    if cl: cur.append(cl)
    if cur: sents.append(cur)
    return sents

def flat(cl):
    """the clause as [syllable, is_accent, is_word_end, punct]"""
    out = []
    for sy, acc, p in cl:
        for i, s in enumerate(sy):
            out.append([s, i == acc, i == len(sy) - 1, p if i == len(sy) - 1 else ''])
    return out

def last_accent(f):
    for i in range(len(f) - 1, -1, -1):
        if f[i][1]: return i
    return len(f) - 1

def notes_for(sent):
    """notes for every syllable of a sentence: [(syllables, notes, bar after)]"""
    sent = list(sent)
    if len(sent) == 1 and len(flat(sent[0])) > 12:   # one long clause: a mediant at a word boundary near the middle
        cl = sent[0]; tot = len(flat(cl)); c = 0; best = None
        for i, w in enumerate(cl[:-1]):
            c += len(w[0])
            if best is None or abs(c - tot / 2) < abs(best[1] - tot / 2): best = (i + 1, c)
        sent = [cl[:best[0]], cl[best[0]:]]; virt = True
    else: virt = False
    n = len(sent)
    role = ['h'] * n
    role[-1] = 'final'
    if n >= 4: role[-2] = 'g'; role[-3] = 'mediant'
    elif n >= 2: role[-2] = 'mediant'
    res = []
    for k, cl in enumerate(sent):
        f = flat(cl); a = last_accent(f); r = role[k]
        if r == 'final':
            nt = ['g'] * len(f)
            for j in range(a + 1, len(f)): nt[j] = 'f'
            nt[a] = 'fg'
            for back, v in ((1, 'g'), (2, 'ef'), (3, 'fe')):
                if a - back >= 0: nt[a - back] = v
        elif r == 'g':                # recited on g, the last accent lifted to h
            nt = ['g'] * len(f); nt[a] = 'gh'
        elif r == 'mediant':
            nt = ['h'] * len(f)
            for j in range(a + 1, len(f)): nt[j] = 'g'
            nt[a] = 'fg'
            if a - 1 >= 0: nt[a - 1] = 'gf'
        else: nt = ['h'] * len(f)
        if k == 0: nt[0] = 'f'    # each sentence opens on f
        bar = ':' if k == n - 1 else (',' if virt else ';')
        res.append((f, nt, bar))
    return res

def gabc_of(body):
    g = []
    for sent in clauses(body):
        cls = notes_for(sent)
        for k, (f, nt, bar) in enumerate(cls):
            for (s, acc, end, p), n in zip(f, nt):
                g.append('%s%s(%s)%s' % (s, p, n, ' ' if end else ''))
            g.append('(%s) ' % bar)
    return ''.join(g)

dom = open(os.path.join(ROOT, 'gabc', 'op-m39-praef-dominico-solemn.gabc')).read().split('%%')[1].strip()
head = dom[:dom.index('De(fg)us:(g) (;)') + len('De(fg)us:(g) (;)')]
tail = dom[dom.index('Et(gf) í(ef)de(f)o(f)'):]
BODY = {
    'corde-iesu': ('Corde Iesu', 'Qui Unigénitum tuum in cruce pendéntem láncea mílitis transfígi voluísti: ut apértum Cor, divínæ largitátis sacrárium, torréntes nobis fúnderet miseratiónis et grátiæ: et quod amóre nostri flagráre numquam destítit, piis esset réquies, et pæniténtibus patéret salútis refúgium.'),
    'thoma': ('S. Thoma Aquinate', 'Qui beátum Thomam Doctórem, vitæ innocéntia et ingénii sublimitáte vere angélicum, in Ecclésia tua suscitáre voluísti, ut eam salubérrima et firmíssima communíret doctrína, et solis instar illustráret: cujus sapiéntiam, ómnibus præcípue commendátam, totus admirátur orbis terrárum.'),
}
for slug, (key, body) in BODY.items():
    g = head + ' ' + gabc_of(body) + tail
    hdr = 'name:Praefatio %s (tonus solemnis);\noffice-part:Praefatio;\ncommentary:Adapted to the solemn tone of the Missale O.P. (1939), Appendix (no chant printed there);\n%%%%\n(f3) ' % key
    open(os.path.join(ROOT, 'gabc', 'op-m39-praef-%s-solemn.gabc' % slug), 'w').write(hdr + g.strip() + '\n')
    print(slug, gabc_of(body))
