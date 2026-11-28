# Build one record per DM (St Dominic Missal 1959) prayer pair from the crop OCR: cleaned English (verbatim, OCR noise only
# removed), Tesseract Latin and the PDF text-layer Latin/English as second witnesses. -> work/dmrec.pkl
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from dmpaths import *
import pickle, re, glob, difflib, collections, json
from readocr import text_of
pairs, _, _ = pickle.load(open(W_('pairs.pkl'), 'rb'))

# English lexicon (for hyphenated line ends): the site's English + the Douay Bible
EW = collections.Counter()
for f in glob.glob(REPO + '/bible/en/*') + glob.glob(REPO + '/data/*.js'):
    try: t = open(f, encoding='utf8', errors='ignore').read()
    except IsADirectoryError: continue
    for w in re.findall(r"[A-Za-z]+", t): EW[w.lower()] += 1
# + every word the PDF text layer of the 1959 Missal itself has at least 3 times
for rows in pickle.load(open(W_('rows.pkl'), 'rb')):
    for r in rows:
        for o in r:
            for w in re.findall(r"[A-Za-z]+", o['t']): EW['~' + w.lower()] += 1
for w in [w for w in EW if w.startswith('~')]:
    if EW[w] >= 3: EW[w[1:]] += EW[w]

LAB_E = ['collect', 'secret', 'postcommunion', 'prayer']
LAB_L = ['oratio', 'secreta', 'postcommunio']
def strip_label(t, labs):
    m = re.match(r'^\W*([A-Za-z]{4,16})\W{0,3}\s*', t)
    if m and max(difflib.SequenceMatcher(None, m.group(1).lower(), l).ratio() for l in labs) >= 0.75:
        t = t[m.end():]
        t = re.sub(r'^(over\s+the\s+[Pp]eople|super\s+populum)\W*\s*', '', t)
    return t
# where a prayer ends: its conclusion (EN "through our Lord." / "who live(s) and reign(s)..."; LA "Per Dominum." / "Qui vivis...")
END_E = re.compile(r"\b(?:[Tt]hrough (?:(?:the same |Christ |Jesus Christ )?(?:our )?Lord|the same|Christ our Lord|Jesus Christ)|[Ww]ho (?:live|lives|livest|liveth|reigns|with)\b)[^.]{0,120}?\.")
END_L = re.compile(r"\b(?:Per (?:D[o0]min|eu[mn]dem|eum|Christum)|Qui (?:vivis|tecum|vivit|cum)|Qui\s+cum)\w*[^.]{0,120}?\.")
STOP_E = re.compile(r"\b(?:Let us pray|Bow down your heads|Absolution\.|Offertory\.|Communion\.|Gospel\.|Lesson\.|Epistle\.|Gradual\.|Introit\.|Tract\.)")
STOP_L = re.compile(r"\b(?:Oremus\.|Humiliate capita|Officium\.|Offertorium\.|Communio\.|Evangelium\.|Lectio\.|Graduale\.|Tractus\.)")
def joinlines(lines, lex):
    t = ''
    for l in lines:
        l = l.strip()
        if not l: continue
        if t.endswith('-') and re.match(r'[A-Za-z]', l):
            a = re.search(r'([A-Za-z]+)-$', t); b = re.match(r'([A-Za-z]+)', l)
            if a and b and lex is not None:
                whole = (a.group(1) + b.group(1)).lower()
                keep = lex.get(whole, 0) == 0 and lex.get(a.group(1).lower(), 0) > 0 and lex.get(b.group(1).lower(), 0) > 0 and b.group(1)[0].isupper()
                t = t + l if keep else t[:-1] + l
            else: t = t[:-1] + l
        else: t = (t + ' ' + l) if t else l
    return re.sub(r'\s+', ' ', t).strip()
def cut(t, END, STOP):
    m = END.search(t)
    c = None
    # the last conclusion before any stop marker
    s = STOP.search(t); lim = s.start() if s else len(t)
    ms = [m for m in END.finditer(t) if m.start() < lim]
    if ms:
        # a conclusion is the end only if no prayer text follows before the stop (take the first one followed by nothing)
        m = ms[0]
        return t[:m.end()].strip(), True
    return t[:lim].strip(), False
def clean_en(t):
    t = re.sub(r'(?<![A-Za-z])0(?= [A-Z])', 'O', t)          # "0 Lord" -> "O Lord"
    t = re.sub(r'\bY ou\b', 'You', t)
    t = re.sub(r'[·~|_©®«»¢™]', ' ', t)
    t = re.sub(r'\s+([,;:.!?])', r'\1', t)
    t = t.replace('“', '"').replace('”', '"').replace("’", "'").replace('‘', "'")
    return re.sub(r'\s+', ' ', t).strip()
import unicodedata
def noise(t):
    t = ''.join(c for c in unicodedata.normalize('NFD', t) if not unicodedata.combining(c))
    t = re.sub(r'(?<=[A-Za-z])[.,;:]*([.,;:])[.,;:-]+(?=\s|$)', r'\1', t)     # ",." -> ","
    t = re.sub(r'(?<=[a-z])[.,;:-]*[.,;:](?=[A-Za-z])', ' ', t)     # "see.Him", "You,.almighty"
    t = re.sub(r'(?<=[a-z,;:])-(?=[A-Z])', ' ', t)                # "victims,-O"
    t = re.sub(r'(?:(?<=\s)|^)-(?=[A-Za-z])', '', t)              # "-You"
    t = re.sub(r'(?<=[a-z])[.,;:](?=[a-z])', ' ', t)            # "we.receive"
    t = re.sub(r'(?<=\s)[-.,;:\'"]+(?=[a-z])', '', t)            # "-deliverance", ";the"
    t = re.sub(r'\.(?=\s+[a-z])', '', t)                         # "with. fitting"
    t = re.sub(r'\s[.,;:\'"]+(?=\s)', ' ', t)                     # stray marks
    return re.sub(r'\s+', ' ', t).strip()
def letters(w): return re.sub(r'[^A-Za-z]', '', w)
def known(w): return all(p.lower() in EW for p in re.findall(r'[A-Za-z]+', w))
def merge(tess, layer):
    a = tess.split(); b = noise(clean_en(layer)).split()
    sm = difflib.SequenceMatcher(None, [letters(w).lower() for w in a], [letters(w).lower() for w in b], autojunk=False)
    out = list(a); fixes = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'replace' and i2 - i1 == 1 and j2 - j1 == 2 and letters(a[i1]).lower() == (letters(b[j1]) + letters(b[j1 + 1])).lower() and not known(letters(a[i1])):
            m = re.match(r'^(.*?)([.,;:!?]*)$', a[i1]); out[i1] = b[j1] + ' ' + re.sub(r'[.,;:!?]+$', '', b[j1 + 1]) + m.group(2); fixes.append((a[i1], out[i1]))
        if tag == 'replace' and i2 - i1 == j2 - j1:
            for k in range(i2 - i1):
                ta, tb = letters(a[i1 + k]), letters(b[j1 + k])
                if not known(ta) and tb and known(tb):
                    out[i1 + k] = a[i1 + k].replace(ta, tb) if ta else tb + a[i1 + k]
                    fixes.append((a[i1 + k], out[i1 + k]))
    return ' '.join(out), fixes
recs = []
for i, x in enumerate(pairs):
    el = [' '.join(w['t'] for w in l) for l in text_of(i, 'e')]
    ll = [' '.join(w['t'] for w in l) for l in text_of(i, 'l')] or [l if isinstance(l, str) else str(l) for l in x['llines']]   # E1: text layer when no Latin crop
    if not el or not ll:
        recs.append(None); continue
    el[0] = strip_label(el[0], LAB_E); ll[0] = strip_label(ll[0], LAB_L)
    en_raw = clean_en(joinlines(el, EW)); la_raw = joinlines(ll, None)
    en_raw, fixes = merge(noise(en_raw), x['en'])
    en, ecut = cut(en_raw, END_E, STOP_E); la, lcut = cut(la_raw, END_L, STOP_L)
    unk = [w for w in en.split() if letters(w) and not known(w)]
    conf = [w['conf'] for l in text_of(i, 'e') for w in l]
    recs.append({'i': i, 'typ': x['typ'], 'p': x['p'], 'en': en, 'la': la, 'en_concl': ecut, 'la_concl': lcut,
                 'en_l': x['en'], 'la_l': x['la'], 'minconf': min(conf) if conf else 0, 'fixes': fixes, 'unk': unk})
pickle.dump(recs, open(W_('dmrec.pkl'), 'wb'))
ok = [r for r in recs if r]
print('records', len(ok), 'of', len(recs), 'no EN concl', sum(not r['en_concl'] for r in ok), 'no LA concl', sum(not r['la_concl'] for r in ok))
