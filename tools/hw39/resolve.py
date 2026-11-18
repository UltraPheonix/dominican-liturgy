"""Resolve the ⟦printed⟧{reference} marks of a draft: keep the book's spelling, take the
reference's letters where the scan is plainly misread.  usage: resolve.py file  (prints, lists the rest)"""
import re, sys, unicodedata
sys.path.insert(0, '/home/claude/build/hw39')
def strip(s): return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
def n(w): return re.sub(r'[^a-z ]', '', strip(w.lower()).replace('æ', 'ae').replace('œ', 'oe').replace('j', 'i'))
def lev(a, b):
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, y in enumerate(b, 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (x != y))
    return d[-1]
KEEP = [('md', 'nd'), ('quoti', 'coti'), ('nunq', 'numq'), ('manu f', 'manuf'), ('etiams', 'etiam s'), ('plusq', 'plus q'), ('solem', 'sollem'), ('retul', 'rettul'), ('quemd', 'quend')]
ACC = {'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú'}
def accents_from(printed, ref):
    # reference letters, printed accent positions when the skeletons agree
    pa = [c for c in printed if c.isalpha()]; acc = [c in 'áéíóúǽ' for c in pa]
    base = strip(ref)
    letters = [c for c in base if c.isalpha()]
    if len(letters) != len(acc) or not any(acc): return ref
    out = ''; k = 0
    for c in base:
        if c.isalpha():
            a = acc[k]; k += 1
            out += (ACC.get(c.lower(), c).upper() if c.isupper() else ACC.get(c, c)) if a and c.lower() in ACC else ('ǽ' if a and c == 'æ' else c)
        else: out += c
    return out
rest = []
def fix(m):
    a, b = m.group(1), m.group(2)
    if b is None: return a
    if re.match(r'^\s*\(?(sed |deinde|rubrica)', b) or 'rubrica' in b: return a
    if b.strip() in ('J.', '++') and (not n(a).strip() or re.match(r'^[»:«\d\sA-Za-zÀ*.]{0,5}$', a)): return (' ' if not a.strip() else '') + '✠'
    if not a.strip(): return ''
    na, nb = n(a), n(b)
    for x, y in KEEP:
        if (x in na and y in nb) or (x in na.replace(' ', '') and y in nb.replace(' ', '')): return a
    if na.replace(' ', '') == nb.replace(' ', ''): return accents_from(a, b) if ' ' not in a else a
    if lev(na, nb) <= max(2, len(nb) // 4):
        pun = re.search(r'[,.;:?!]*$', a).group(); bb = re.sub(r'[,.;:?!]+$', '', b)
        return accents_from(re.sub(r'[,.;:?!]+$', '', a), bb) + pun
    rest.append(m.group(0)); return m.group(0)
s = open(sys.argv[1], encoding='utf8').read()
s = re.sub(r'⟦([^⟧]*)⟧(?:\{([^}]*)\})?', fix, s)
s = s.replace(' S. ', ' S ').replace('  ', ' ')
print(s, end='')
print('\n'.join(rest), file=sys.stderr)
