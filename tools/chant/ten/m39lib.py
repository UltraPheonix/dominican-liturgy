import sys, os, re, json, difflib, unicodedata
sys.path.insert(0, '/home/claude/dominican-liturgy/tools/pdfomr')
from syl import isv as _isv, base
def isv(w, i):
    # 'i' after the u of qu/gu is a vowel (Qui-a), not the consonantal i between vowels
    if base(w[i]) == 'i' and i >= 2 and base(w[i - 1]) == 'u' and base(w[i - 2]) in 'qg': return True
    if i == 0 and base(w[0]) == 'i' and len(w) > 1 and base(w[1]) == 'i': return True   # i-ís-dem
    return _isv(w, i)
def syllables(w):
    """start indices of the syllables of a Latin word, as the chant books divide them (Sur-sum, sanc-tæ, Ec-clé-si-æ, ex-ér-ci-tus, dí-gnum)"""
    n = len(w); vs = []; i = 0
    while i < n:
        if isv(w, i):
            j = i + 1
            if j < n and isv(w, j) and (base(w[i]) + base(w[j])) in ('ae', 'oe', 'au') and w[j] not in 'éóúÉ': j += 1   # Mi-cha-é-lis
            vs.append((i, j)); i = j
        else: i += 1
    if len(vs) <= 1: return [0]
    starts = [0]
    for k in range(1, len(vs)):
        a, b = vs[k - 1][1], vs[k][0]; cl = w[a:b]; lc = cl.lower()
        if len(cl) == 0: starts.append(a)
        elif len(cl) == 1: starts.append(a + 1 if lc == 'x' else a)
        else:
            if len(lc) >= 3 and lc[-3] == 's' and lc[-2] in 'ptc' and lc[-1] in 'lr': cut = b - 3
            elif lc.endswith('qu') or lc[-2:] in ('ch', 'ph', 'th', 'gn', 'st', 'sp', 'sc') or (lc[-2] in 'bcdfgpt' and lc[-1] in 'lr'): cut = b - 2
            else: cut = b - 1
            if lc[0] == 'x': cut = max(cut, a + 1)
            starts.append(max(a, cut))
    return starts
def flat(s):
    s = s.replace('æ', 'ae').replace('Æ', 'ae').replace('œ', 'oe').replace('ǽ', 'ae')
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
    return re.sub(r'[^a-z]', '', s.lower().replace('j', 'i'))

def staff_syllables(x):
    """OCR words of one staff: [(word, x0, [syllables])], and the notes/bars on the staff"""
    s = x['s']; toks = []
    for a0, a1, tt in sorted(x['words']):
        tt = tt.translate(str.maketrans('16053', 'loosa'))   # OCR digit look-alikes (saecu-16-rum)
        t2 = re.sub(r'[^A-Za-zæœÆŒ\-]', '', tt)
        if not t2: continue
        sy = []
        for p in [p for p in t2.split('-') if p]:
            st = syllables(p); ends = st[1:] + [len(p)]
            sy += [p[st[k]:ends[k]] for k in range(len(st))]
        # a drop cap read as its own word ("P" + "er"): join it to the next word
        if toks and len(toks[-1][2]) == 1 and len(toks[-1][2][0]) == 1 and toks[-1][2][0].isupper() and a0 - toks[-1][1] < 4 * s:
            toks[-1] = (toks[-1][0] + t2, toks[-1][1], [toks[-1][2][0] + sy[0]] + sy[1:]); continue
        toks.append((t2, a0, sy))
    items = [it for it in x['items'] if (it[1] == 'bar') or (-1 <= it[2] <= 8 and 12 <= it[3] <= 40)]
    # a column of 4+ stacked 'notes' is a (thick) bar line
    xs_ = sorted(set(it[0] for it in items if it[1] == 'note'))
    drop = set()
    for xv in xs_:
        col = [it for it in items if it[1] == 'note' and abs(it[0] - xv) < 9]
        if len(col) >= 4: drop |= set(map(id, col))
    if drop: items = [it for it in items if id(it) not in drop]
    out = []
    for it in items:
        if it[1] == 'note' and it[0] < x.get('clef_end', x['x'][0] + 1.15 * s): continue   # clef
        if it[1] == 'note' and it[0] > x['x'][1] - 0.85 * s: continue    # custos at the right edge
        if it[1] == 'bar' and (it[0] < x['x'][0] + 1.5 * s or it[0] > x['x'][1] - 0.6 * s): continue   # staff ends
        out.append(it)
    return toks, out, s

def assign(toks, items, s):
    """notes to syllables. Note columns closer than 0.9 staff-spaces form one neume (one syllable); between syllables the text
    spreads the notes at least 1.4 spaces apart. When a staff has as many neumes as syllables they pair one to one; otherwise
    each word takes the neumes under it (from its start to the next word's), one per syllable, cutting at the widest gaps."""
    res = []
    if not toks: return res
    notes = sorted([it for it in items if it[1] == 'note'], key=lambda i: i[0])
    bars = [it for it in items if it[1] == 'bar']
    cols = []
    for n in notes:
        if cols and n[0] - cols[-1][-1][0] < 9: cols[-1].append(n)
        else: cols.append([n])
    neu = []
    for c in cols:
        if neu and c[0][0] - neu[-1][-1][-1][0] < 0.9 * s: neu[-1].append(c)
        else: neu.append([c])
    nsy = sum(len(tk[2]) for tk in toks)
    flatn = lambda nm: [(n[0], n[2]) for c in nm for n in c]
    if len(neu) == nsy:
        k = 0
        for w, x0, sy in toks:
            for sname in sy: res.append([sname, flatn(neu[k]), None]); k += 1
    else:
        xs = [tk[1] for tk in toks] + [1e9]
        for i, (w, x0, sy) in enumerate(toks):
            mine = [nm for nm in neu if x0 - 0.5 * s <= nm[0][0][0] < xs[i + 1] - 0.5 * s]
            k = len(sy)
            if len(mine) <= k: groups = [[nm] for nm in mine] + [[] for _ in range(k - len(mine))]
            else:
                gaps = sorted(range(1, len(mine)), key=lambda j: -(mine[j][0][0][0] - mine[j - 1][-1][-1][0]))[:k - 1]
                groups = []; prev = 0
                for c in sorted(gaps) + [len(mine)]: groups.append(mine[prev:c]); prev = c
            for j, sname in enumerate(sy):
                res.append([sname, [p for nm in (groups[j] if j < len(groups) else []) for p in flatn(nm)], None])
    # bars: after the syllable whose neume is the last one before the bar
    starts = []
    k = 0
    for r in res:
        starts.append(min([p[0] for p in r[1]], default=None))
    for bb in bars:
        cand = [i for i, st in enumerate(starts) if st is not None and st < bb[0]]
        if cand: res[max(cand)][2] = {'half': ';', 'full': ':', 'double': '::'}[bb[2]]
    return res

def groups_gabc(notes):
    notes = sorted(notes, key=lambda t: (round(t[0] / 12), -t[1]))
    # same x (a pes / stacked): lower first; else by x
    out = []; i = 0
    notes = sorted(notes, key=lambda t: t[0])
    while i < len(notes):
        j = i; grp = [notes[i]]
        while j + 1 < len(notes) and abs(notes[j + 1][0] - notes[i][0]) < 9: j += 1; grp.append(notes[j])
        grp.sort(key=lambda t: t[1])
        for x_, p in grp:   # the same head read twice a few pixels apart
            if out and out[-1][1] == p and x_ - out[-1][0] < 16: continue
            out.append((x_, p))
        i = j + 1
    r = ''.join(chr(ord('d') + p) for _, p in out)
    h = len(r) // 2
    return r


def correct_syllables(text):
    out = []   # [syllable text incl. punctuation and following space, flat start, flat end]
    pos = 0
    for w in re.findall(r'\S+', text):
        core = re.sub(r'[^A-Za-zÀ-ÿæœǽÆŒǼ]', '', w)
        if not core: 
            if out: out[-1][0] += ' ' + w
            continue
        lead = w[:w.index(core[0])]; tail = w[len(lead) + len(core):]
        st = syllables(core); ends = st[1:] + [len(core)]
        for k, (a, b) in enumerate(zip(st, ends)):
            s = core[a:b]; f = flat(s)
            out.append([(lead if k == 0 else '') + s + (tail if k == len(st) - 1 else ''), pos, pos + len(f), k == len(st) - 1])
            pos += len(f)
    return out
def neumes_of(items, s):
    notes = sorted([it for it in items if it[1] == 'note'], key=lambda i: i[0])
    cols = []
    for n in notes:
        if cols and n[0] - cols[-1][-1][0] < 9: cols[-1].append(n)
        else: cols.append([n])
    neu = []
    for c in cols:
        if neu and c[0][0] - neu[-1][-1][-1][0] < 0.9 * s: neu[-1].append(c)
        else: neu.append([c])
    return [[(n[0], n[2]) for c in nm for n in c] for nm in neu]
