"""Draft a Holy Week day of the Missale O.P. (1939) from the column OCR, repaired against
the Divinum Officium text of the same day (letters only; accents and punctuation as printed).
usage: draft39.py bp0 c0 bp1 c1 REF1[,REF2..] > day.draft
Output lines:  TAG| text      (TAG = L label, R rubric, T text, H heading)"""
import json, re, sys, unicodedata, difflib
sys.path.insert(0, '/home/claude/build/m39hw'); import accent

def strip(s): return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
def norm(w):
    w = strip(w.lower()).replace('æ', 'ae').replace('œ', 'oe')
    return re.sub(r'[^a-z]', '', w).replace('j', 'i')

LABELS = r'^(Officium|Oratio|Secreta|Postcommunio|Communio|Offertorium|Tractus|Graduale|Praefatio|Præfatio|Prophetia|Lectio|Léctio|Responsorium|Oratio super populum|Secunda et tertia|Antiphona|Hymnus|Canticum|Ad Vesperas|Benedictio|Ps\.)'

p0, c0, p1, c1 = map(int, sys.argv[1:5]); refs = sys.argv[5].split(',')
lines = []
for p in range(p0, p1 + 1):
    L = json.load(open('/home/claude/build/m39hw/p%d.json' % p))
    for c in (0, 1):
        if (p, c) < (p0, c0) or (p, c) > (p1, c1): continue
        cl = [l for l in L if l['c'] == c][1:]
        for l in cl:
            t = l['t'].strip()
            t = re.sub(r'^(?:[|;,.:\'"()\-!\]\[]+\s*)+', '', t)
            t = re.sub(r'(?:\s*[|\]\[])+\s*$', '', t)
            t = t.replace('ü', 'ú').replace('»I«', '✠').replace('»J«', '✠')
            if t: lines.append((t, l['red']))

# blocks
blocks = []
def push(tag, t): blocks.append([tag, t])
cur = None
for t, red in lines:
    lab = re.match(LABELS, t) and len(t) < 60
    cap = re.match(r'^[A-Z/ÆŒ]{2,}[ ,]', t) and not re.match(r'^(FERIA|DOMINICA|SABBATO|IN |AD |DE |ORATIO)', t)
    head = re.match(r'^(FERIA|SABBATO|IN CENA|IN PARASCEVE|Statio)', t)
    if head: push('H', t); cur = None; continue
    tag = 'R' if red and not lab else ('L' if lab else 'T')
    if lab:
        mm = re.match(r'^((?:Oratio super populum|Secunda et tertia \w+,?|\S+)(?:\s+(?:Ps|Matth|Marc|Luc|Joann?|Is|Isai|Jerem|Zach|Os|Exod|Gal|Phil|Hebr|Sap|Dan|c)\.\s*[0-9]+(?:,\s*[0-9]+)?)?)\s*(.*)$', t)
        if mm and mm.group(2) and not t.startswith('Secunda'):
            cur = ['L', mm.group(1)]; blocks.append(cur); cur = ['T', mm.group(2)]; blocks.append(cur); continue
    new = cur is None or lab or cap or tag != cur[0] or cur[0] == 'L'
    if new:
        cur = [tag, t]; blocks.append(cur)
    else:
        if cur[1].endswith('-'): cur[1] = cur[1][:-1] + t
        else: cur[1] += ' ' + t

# repair text blocks against the reference
R = []
for r in refs:
    s = open(r, encoding='utf8').read()
    s = re.sub(r'^\[.*?\].*$|^[!@&$#].*$|^v\. ', ' ', s, flags=re.M)
    R += s.split()
RN = [norm(w) for w in R]
ACC = {'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú', 'y': 'ý'}
def transfer(core, ow):
    acc = [ch in 'áéíóúý' for ch in ow if ch.isalpha()]
    base = strip(core.replace('ǽ', 'æ'))
    flat = []
    for ch in base: flat += ['a', 'e'] if ch in 'æÆ' else ['o', 'e'] if ch in 'œŒ' else [ch]
    if len(flat) != len(acc) or not any(acc): return core if not any(acc) and len(flat) == len(acc) else None
    out = ''; i = 0
    for ch in base:
        n = 2 if ch in 'æœÆŒ' else 1; a = any(acc[i:i + n]); i += n
        if a and ch in 'æ': out += 'ǽ'
        elif a and ch.lower() in ACC: out += ACC[ch.lower()].upper() if ch.isupper() else ACC[ch.lower()]
        else: out += ch
    return out

def repair(text):
    W0 = text.split(); W = []
    for w in W0:
        if not norm(w) and W: W[-1] += ' ' + w
        else: W.append(w)
    A = [norm(accent.fix_word(w)) for w in W]
    if len(A) < 4: return text, 0
    sm = difflib.SequenceMatcher(None, A, RN, autojunk=False)
    m = sm.find_longest_match(0, len(A), 0, len(RN))
    if m.size < 4: return text, 0
    b0 = max(0, m.b - m.a - 20); b1 = min(len(RN), m.b + (len(A) - m.a) + 20)
    sm = difflib.SequenceMatcher(None, A, RN[b0:b1], autojunk=False)
    out = []; matched = 0
    ops = sm.get_opcodes()
    while ops and ops[0][0] != 'equal' and ops[0][1] == ops[0][2]: ops.pop(0)
    while ops and ops[-1][0] != 'equal' and ops[-1][1] == ops[-1][2]: ops.pop()
    for n_, (op, a0, a1, x0, x1) in enumerate(ops):
        if op != 'equal' and (n_ == 0 or n_ == len(ops) - 1):
            out.append('⟦' + ' '.join(accent.fix_word(w) for w in W[a0:a1]) + '⟧'); continue
        if op == 'equal':
            for k in range(a1 - a0):
                o = W[a0 + k]; r = R[b0 + x0 + k]; matched += 1
                core = re.sub(r'[,.;:?!]+$', '', r); pun = re.search(r'(?:\s*[,.;:?!])*$', o).group()
                ow = re.sub(r'(?:\s*[,.;:?!])+$', '', o)
                if ow[:1].isupper() and core[:1].islower(): core = core[0].upper() + core[1:]
                if ow[:1].islower() and core[:1].isupper(): core = core[0].lower() + core[1:]
                if ow.isupper() and len(ow) > 1: core = core.upper()
                t = transfer(core, ow)
                out.append((t if t else accent.fix_word(ow)) + pun)
        else:
            out.append('⟦' + ' '.join(accent.fix_word(w) for w in W[a0:a1]) + '⟧' + ('{' + ' '.join(R[b0 + x0:b0 + x1]) + '}' if x1 > x0 else ''))
    return ' '.join(out), matched / len(A)

for b in blocks:
    if b[0] == 'T':
        t, q = repair(b[1])
        if q > 0.5: b[1] = t
        else: b[1] = ' '.join(accent.fix_word(w) for w in b[1].split())
    elif b[0] == 'R':
        b[1] = b[1].replace('æ', 'æ')
    print(b[0] + '| ' + b[1])
