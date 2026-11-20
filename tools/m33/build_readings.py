import json, re, collections
import readings as R
from parse import norm
import vulg
MAP = json.load(open('/home/claude/m33/map.json'))
from anchor import SITE
FORMS = [('in illo tempore', 'In illo témpore', 'At that time'), ('in diebus illis', 'In diébus illis', 'In those days'),
         ('fratres', 'Fratres', 'Brethren'), ('carissimi', 'Caríssimi', 'Dearly beloved'), ('carissime', 'Caríssime', 'Dearly beloved'),
         ('haec dicit dominus deus', 'Hæc dicit Dóminus Deus', 'Thus saith the Lord God'), ('haec dicit dominus', 'Hæc dicit Dóminus', 'Thus saith the Lord'),
         ('dixit dominus', 'Dixit Dóminus', 'The Lord said'), ('dilectissimi', 'Dilectíssimi', 'Dearly beloved'), ('fili', 'Fili', 'Son')]
def clean_tokens(pre):
    toks = [t for t in pre.split() if norm(t)]
    # junk from the drop-cap and the margin: single letters, digits
    while toks and (len(norm(toks[0]).replace(' ', '')) <= 1 or not re.search(r'[a-zA-Z]{2}', toks[0])): toks.pop(0)
    out = []
    for t in toks:
        n = norm(t).replace(' ', '')
        if out and norm(out[-1]).replace(' ', '') + n in R.LEX and n not in R.LEX: out[-1] = re.sub(r'\W+$', '', out[-1]) + t; continue
        out.append(t)
    if out:
        n = norm(out[0]).replace(' ', '')
        if n not in R.LEX and len(n) >= 2:
            cands = [(c.most_common(1)[0][1] + sum(c.values()), w) for w, c in R.LEX.items() if w.endswith(n[-min(len(n), 5):]) and len(n) - 1 <= len(w) <= len(n) + 2 and w[-len(n) + 1:] == n[1:]]
            if cands:
                w = max(cands)[1]; out[0] = w.capitalize() + re.search(r'\W*$', out[0]).group()
    return out
def fix_prefix(pre):
    """the incipit before the Vulgate text: a standard formula (its first letters are often a garbled drop-cap) + Missal words"""
    toks0 = clean_tokens(pre); pre = ' '.join(toks0)
    t = norm(pre); en = ''
    for f, la, e in FORMS:
        m = re.match(r'^\w{0,3}?' + re.escape(f[1:]) + r'\b', t) if len(f) > 4 else (re.match(r'^' + f + r'\b', t))
        if not m and f.startswith('in '): m = re.match(r'^(\w{0,3} )?' + re.escape(f[3:]) + r'\b', t)
        if m:
            rest_n = t[m.end():].split()
            # take the remaining OCR tokens (same count from the end)
            toks = pre.split()
            rest = toks[len(toks) - len(rest_n):] if rest_n else []
            rest = [R.accent(x) for x in rest if norm(x)]
            if rest: rest[0] = rest[0][0].upper() + rest[0][1:]
            return (la + ': ' + ' '.join(rest)).strip(), e, len(rest)
    toks = [R.accent(x) for x in pre.split() if norm(x)]
    return ' '.join(toks), '', len(toks)
BOOK_EN = {'Matthæus': 'Matthew', 'Marcus': 'Mark', 'Lucas': 'Luke', 'Joannes': 'John'}
def heading(book, kind):
    if kind == 'gospel':
        la = {'Matthæus': 'Matthǽum', 'Marcus': 'Marcum', 'Lucas': 'Lucam', 'Joannes': 'Joánnem'}.get(book, book)
        return 'Sequéntia sancti Evangélii secúndum %s.' % la, 'Continuation of the holy Gospel according to %s.' % BOOK_EN.get(book, book)
    P = {'Ad Romanos': ('ad Romános', 'to the Romans'), 'Ad Corinthios 1': ('ad Corínthios', 'to the Corinthians'), 'Ad Corinthios 2': ('ad Corínthios', 'to the Corinthians'),
         'Ad Galatas': ('ad Gálatas', 'to the Galatians'), 'Ad Ephesios': ('ad Ephésios', 'to the Ephesians'), 'Ad Philippenses': ('ad Philippénses', 'to the Philippians'),
         'Ad Colossenses': ('ad Colossénses', 'to the Colossians'), 'Ad Thessalonicenses 1': ('ad Thessalonicénses', 'to the Thessalonians'),
         'Ad Thessalonicenses 2': ('ad Thessalonicénses', 'to the Thessalonians'), 'Ad Timotheum 1': ('ad Timótheum', 'to Timothy'), 'Ad Timotheum 2': ('ad Timótheum', 'to Timothy'),
         'Ad Titum': ('ad Titum', 'to Titus'), 'Ad Hebræos': ('ad Hebrǽos', 'to the Hebrews'), 'Ad Philemonem': ('ad Philemónem', 'to Philemon')}
    if book in P: return 'Léctio Epístolæ beáti Pauli Apóstoli %s.' % P[book][0], 'Lesson from the Epistle of blessed Paul the Apostle %s.' % P[book][1]
    O = {'Petri 1': ('Léctio Epístolæ beáti Petri Apóstoli.', 'Lesson from the Epistle of blessed Peter the Apostle.'), 'Petri 2': ('Léctio Epístolæ beáti Petri Apóstoli.', 'Lesson from the Epistle of blessed Peter the Apostle.'),
         'Jacobi': ('Léctio Epístolæ beáti Jacóbi Apóstoli.', 'Lesson from the Epistle of blessed James the Apostle.'),
         'Joannis 1': ('Léctio Epístolæ beáti Joánnis Apóstoli.', 'Lesson from the Epistle of blessed John the Apostle.'), 'Joannis 2': ('Léctio Epístolæ beáti Joánnis Apóstoli.', 'Lesson from the Epistle of blessed John the Apostle.'),
         'Judæ': ('Léctio Epístolæ beáti Judæ Apóstoli.', 'Lesson from the Epistle of blessed Jude the Apostle.'),
         'Actus Apostolorum': ('Léctio Actuum Apostolórum.', 'Lesson from the Acts of the Apostles.'), 'Apocalypsis': ('Léctio libri Apocalýpsis beáti Joánnis Apóstoli.', 'Lesson from the Book of the Apocalypse of blessed John the Apostle.'),
         'Isaias': ('Léctio Isaíæ Prophétæ.', 'Lesson from the Prophet Isaias.'), 'Jeremias': ('Léctio Jeremíæ Prophétæ.', 'Lesson from the Prophet Jeremias.'),
         'Ezechiel': ('Léctio Ezechiélis Prophétæ.', 'Lesson from the Prophet Ezechiel.'), 'Daniel': ('Léctio Daniélis Prophétæ.', 'Lesson from the Prophet Daniel.'),
         'Osee': ('Léctio Osée Prophétæ.', 'Lesson from the Prophet Osee.'), 'Joel': ('Léctio Joélis Prophétæ.', 'Lesson from the Prophet Joel.'), 'Jonas': ('Léctio Jonæ Prophétæ.', 'Lesson from the Prophet Jonas.'),
         'Zacharias': ('Léctio Zacharíæ Prophétæ.', 'Lesson from the Prophet Zacharias.'), 'Malachias': ('Léctio Malachíæ Prophétæ.', 'Lesson from the Prophet Malachias.'),
         'Michæa': ('Léctio Michǽæ Prophétæ.', 'Lesson from the Prophet Micheas.'), 'Baruch': ('Léctio Baruch Prophétæ.', 'Lesson from the Prophet Baruch.'),
         'Sapientia': ('Léctio libri Sapiéntiæ.', 'Lesson from the Book of Wisdom.'), 'Ecclesiasticus': ('Léctio libri Sapiéntiæ.', 'Lesson from the Book of Wisdom.'),
         'Proverbia': ('Léctio libri Sapiéntiæ.', 'Lesson from the Book of Wisdom.'), 'Canticum Canticorum': ('Léctio libri Sapiéntiæ.', 'Lesson from the Book of Wisdom.'),
         'Genesis': ('Léctio libri Genesis.', 'Lesson from the Book of Genesis.'), 'Exodus': ('Léctio libri Exodi.', 'Lesson from the Book of Exodus.'),
         'Leviticus': ('Léctio libri Levítici.', 'Lesson from the Book of Leviticus.'), 'Numeri': ('Léctio libri Numerórum.', 'Lesson from the Book of Numbers.'),
         'Deuteronomium': ('Léctio libri Deuteronómii.', 'Lesson from the Book of Deuteronomy.'), 'Regum 1': ('Léctio libri Regum.', 'Lesson from the Book of Kings.'),
         'Regum 2': ('Léctio libri Regum.', 'Lesson from the Book of Kings.'), 'Regum 3': ('Léctio libri Regum.', 'Lesson from the Book of Kings.'), 'Regum 4': ('Léctio libri Regum.', 'Lesson from the Book of Kings.'),
         'Esther': ('Léctio libri Esther.', 'Lesson from the Book of Esther.'), 'Judith': ('Léctio libri Judith.', 'Lesson from the Book of Judith.'), 'Tobiæ': ('Léctio libri Tobíæ.', 'Lesson from the Book of Tobias.'),
         'Machabæorum 1': ('Léctio libri Machabæórum.', 'Lesson from the Book of Machabees.'), 'Machabæorum 2': ('Léctio libri Machabæórum.', 'Lesson from the Book of Machabees.'),
         'Job': ('Léctio libri Job.', 'Lesson from the Book of Job.'), 'Lamentationes': ('Léctio Jeremíæ Prophétæ.', 'Lesson from the Prophet Jeremias.'),
         'Sophonias': ('Léctio Sophoníæ Prophétæ.', 'Lesson from the Prophet Sophonias.'), 'Habacuc': ('Léctio Habacuc Prophétæ.', 'Lesson from the Prophet Habacuc.'),
         'Amos': ('Léctio Amos Prophétæ.', 'Lesson from the Prophet Amos.'), 'Aggæus': ('Léctio Aggǽi Prophétæ.', 'Lesson from the Prophet Aggeus.')}
    return O.get(book, ('Léctio libri %s.' % book, 'Lesson from the Book of %s.' % book))
def ref_str(book, verses):
    out = []; prev = None; run = None
    for c, v in verses:
        if run and c == run[0] and v == run[2] + 1: run[2] = v; continue
        if run: out.append(run)
        run = [c, v, v]
    if run: out.append(run)
    s = []; lastc = None
    for c, a, b in out:
        r = ('%d-%d' % (a, b)) if b > a else str(a)
        s.append(('%d: ' % c if c != lastc else '') + r); lastc = c
    return book + ' ' + '; '.join(x if ':' in x else x for x in s).replace('; ', ', ').replace(', %d: ' % 0, '')
def english(book, verses):
    return ' '.join(vulg.VER.get((book, c, v), ('', ''))[1] for c, v in verses).strip()
FREQ = {w: sum(c.values()) for w, c in R.LEX.items()}
def fix_first(tok, nxt=''):
    nn = norm(nxt)
    if nn in ('illo', 'diebus', 'initio', 'principio') and norm(tok) not in ('in',): return 'In'
    tail = re.search(r'[A-ZÆŒ][A-ZÆŒ]*[a-zæœáéíóú]*$', re.sub(r'[^A-Za-zÆŒæœáéíóúÁÉÍÓÚ]', '', tok))
    if tail and tail.start() > 0:
        t = norm(tail.group())
        if t in ('ec', 'aec'): return 'Hæc'
        c = [w for w in R.LEX if w.endswith(t) and len(w) == len(t) + 1]
        if c: return R.accent(max(c, key=lambda w: FREQ[w])).capitalize() + re.search(r'\W*$', tok).group()
    m = re.match(r'^(\W*)(.*?)(\W*)$', tok); core = m.group(2); trail = m.group(3)
    n = norm(core).replace(' ', '')
    if n in R.LEX and re.fullmatch(r'[A-Za-zÀ-ÿæœǽ]+', core): return tok
    for k in range(0, 4):
        rem = n[k:]
        if len(rem) < 2: break
        if k and rem in R.LEX and len(rem) > 3: return R.accent(rem).capitalize() + trail
        c = [w for w in R.LEX if w.endswith(rem) and len(rem) < len(w) <= len(rem) + 2]
        if k == 0: c = [w for w in R.LEX if w.endswith(rem) and len(w) == len(rem) + 1]
        if c:
            w = max(c, key=lambda w: FREQ[w]); return R.accent(w).capitalize() + trail
    return tok
def tidy(text, kind, book):
    t = text.strip()
    t = re.sub(r'^(\W*)', '', t)
    w = t.split(' ')
    if len(w) > 1 and len(re.sub(r'\W', '', w[0])) <= 3 and w[1][:1].isupper() and norm(w[1]) not in R.LEX: w = [w[0] + w[1]] + w[2:]
    w[0] = fix_first(w[0], w[1] if len(w) > 1 else '')
    t = ' '.join(w)
    t = re.sub(r'^Illo témpore:?\s*', 'In illo témpore: ', t); t = re.sub(r'^Diébus illis:?\s*', 'In diébus illis: ', t)
    t = re.sub(r'^(In illo témpore|In diébus illis|Fratres|Caríssimi|Caríssime|Hæc dicit Dóminus( Deus)?)\s*:?\s+(\w)', lambda m: m.group(1) + ': ' + m.group(3).upper(), t)
    return t
OUT = {}; REP = []
for k, mp in MAP.items():
    rs = []
    for r in mp['readings']:
        body = R.join(r['body']); al = R.align(body, r['head'])
        if not al: REP.append((k, 'noalign', r['head'][:60])); continue
        if al['matched'] < 0.6 * al['n']: REP.append((k, 'weak %d/%d' % (al['matched'], al['n']), r['head'][:50], al['book']))
        pre, pre_en, nrest = fix_prefix(al['prefix'])
        la_h, en_h = heading(al['book'], r['kind'])
        body_t = al['text']
        if pre.endswith(':') or re.search(r'[:.?!]$', pre): body_t = body_t[0].upper() + body_t[1:]
        elif pre and re.search(r'\b(dicens|dicéntes|ait|dixit)\W*$', pre) is None and False: pass
        text = (pre + ' ' if pre else '') + body_t
        text = re.sub(r'^(\w)', lambda m: m.group(1).upper(), text.strip())
        en = english(al['book'], al['verses'])
        if pre_en and not nrest: en = pre_en + ': ' + (en[0].lower() + en[1:] if en[:2] not in ('I ', 'O ') and not en[:1].isupper() else en)
        elif pre_en: en = pre_en + ': ' + en
        text = tidy(text, r['kind'], al['book'])
        text = re.sub(r'([.?!]) ([a-zæœáéíóú])', lambda m: m.group(1) + ' ' + m.group(2).upper(), text)
        flag = []
        if al['midverse'] and not pre: flag.append('starts mid-verse')
        if al['matched'] < 0.6 * al['n']: flag.append('weak')
        rs.append({'flag': flag, 'type': 'Gospel' if r['kind'] == 'gospel' else ('Epistle' if 'Epíst' in la_h else 'Lesson'), 'ref': ref_str(al['book'], al['verses']),
                   'title': la_h, 'title_en': en_h, 'first': [al['book']] + list(al['verses'][0]) if al['verses'] else None, 'la': text, 'en': en, 'p33': r['page']})
    OUT[k] = {'how': mp['how'], 'readings': rs}
# the same reading printed in several places: where one copy came out badly (two columns mixed in the scan), use the best copy
groups = collections.defaultdict(list)
for k, v in OUT.items():
    for r in v['readings']:
        b = r['ref'].split(' ')[0]; groups[(r['ref'].rsplit(' ', 1)[0] if False else r['type'], r['la'][:0] + r['ref'].split(':')[0])].append(r)
def score(r): return (0 if r['flag'] else 1, len(r['la']))
byfirst = collections.defaultdict(list)
for k, v in OUT.items():
    for r in v['readings']: byfirst[(r['type'], r['ref'].split(',')[0].split('-')[0])].append(r)
fixed = 0
for g in byfirst.values():
    best = max(g, key=score)
    for r in g:
        if r is not best and r['flag'] and not best['flag']: r.update({x: best[x] for x in ('la', 'en', 'ref', 'title', 'title_en')}); r['flag'] = ['from another copy']; fixed += 1
print('consensus fixed', fixed)
json.dump(OUT, open('/home/claude/m33/readings33.json', 'w'), ensure_ascii=False, indent=0)
for x in REP: print(x)
print(len(REP), 'issues;', sum(1 for v in OUT.values() if v['readings']), 'masses with readings')
