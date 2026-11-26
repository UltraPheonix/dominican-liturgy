"""conform(ocr, ref): the BOOK's wording with the reference's spelling.
The OCR of the 1909 Breviary decides which words stand and in what order; a reference text (Divinum Officium, Vulgate) only lends
its accents, capitals and punctuation to the words that are the same, and settles a word the OCR garbled when the reference has a
near-identical word in the same place. Words are never added or removed on the reference's authority: the Dominican text often
differs from the Roman one (other cuts of a lesson, other wording of a responsory)."""
import re, difflib
import latdict as LD, latcount as LC
TOK = re.compile(r"[A-Za-zÀ-ÿǽæœÆŒǼ]+(?:\?(?=[a-zà-ÿ]))?[A-Za-zÀ-ÿǽæœÆŒǼ]*|[^\sA-Za-zÀ-ÿǽæœÆŒǼ]+")
def toks(t): return TOK.findall(t)
def isw(x): return bool(re.match(r"[A-Za-zÀ-ÿǽæœÆŒǼ]", x))
def ed1(a, b):
    """edit distance <= 2 on the bases"""
    if abs(len(a) - len(b)) > 2: return False
    return difflib.SequenceMatcher(None, a, b).ratio() >= (0.8 if max(len(a), len(b)) > 5 else 0.74)
def conform(ocr, ref):
    """-> (text, share of the OCR words confirmed by the reference)"""
    ow = [x for x in toks(ocr) if isw(x)]; rt = toks(ref)
    rw = [(i, x) for i, x in enumerate(rt) if isw(x)]
    ob = [LD.base(x) for x in ow]; rb = [LD.base(x) for _, x in rw]
    sm = difflib.SequenceMatcher(None, ob, rb, autojunk=False)
    out = []; conf = 0
    def punct_after(k):   # the reference's punctuation after its word k
        i = rw[k][0]; s = ''
        j = i + 1
        while j < len(rt) and not isw(rt[j]): s += rt[j]; j += 1
        return re.sub(r'[^.,;:!?]', '', s)[:1]
    opun = {}   # the OCR's own punctuation after each of its words
    k = -1
    for x in toks(ocr):
        if isw(x): k += 1
        elif k >= 0: opun[k] = opun.get(k, '') + x
    def own(k):
        w = LC.fix_text(ow[k]) or ow[k]
        p = re.sub(r'[^.,;:!?*—]', '', opun.get(k, ''))
        p = re.sub(r'^([.,;:!?]).*?(\*|—)?$', lambda m: m.group(1) + (' ' + m.group(2) if m.group(2) else ''), p) if p else ''
        return w + p
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for d in range(i2 - i1):
                w = rw[j1 + d][1]
                if ow[i1 + d][:1].isupper() and not w[:1].isupper() and (i1 + d == 0): w = w[:1].upper() + w[1:]
                star = ' *' if '*' in opun.get(i1 + d, '') else ''
                dash = ' —' if '—' in opun.get(i1 + d, '') else ''
                out.append(w + punct_after(j1 + d) + star + dash); conf += 1
        elif tag == 'replace' and i2 - i1 == j2 - j1:
            for d in range(i2 - i1):
                o, r = ow[i1 + d], rw[j1 + d][1]
                dc = i1 + d == 0 and len(ob[0]) >= 2 and rb[j1 + d].endswith(ob[0][1:] if len(ob[0]) > 3 else ob[0]) and len(rb[j1 + d]) - len(ob[0]) <= 2   # drop-capital lost or misread
                if LC.N.get(ob[i1 + d], 0) < 3 and (ed1(ob[i1 + d], rb[j1 + d]) or dc):   # garbled in the OCR, near-identical in the reference
                    out.append(r + punct_after(j1 + d) + (' *' if '*' in opun.get(i1 + d, '') else '')); conf += 1
                else: out.append(own(i1 + d))
        elif tag in ('replace', 'delete'):
            for k2 in range(i1, i2): out.append(own(k2))
        # 'insert': words only the reference has — not the book's
    t = ' '.join(out)
    t = re.sub(r'\s+([.,;:!?])', r'\1', t)
    return t, (conf / len(ow) if ow else 0.0)
if __name__ == '__main__':
    o = "ASEN Apóstolus Beth. sáidae vico Galilzeze natu frater Petri, discípulus Joánnis Baptístze, una cum fratre ante álios Apóstolos a Christo vo. cátus"
    r = "Andréas Apóstolus, Bethsáidæ natus, qui est Galilǽæ vicus, frater Petri, discípulus Joánnis Baptístæ, hoc testimónium de Christo dicéntis audívit"
    print(conform(o, r))
    print(conform("Cum perambuláret Dóminus juxta mare secus litus Galilzeze, vidit Petrum et Andréam rétia mitténtes in mare, et Vocávit eos dicens : * Veníte post me, fáciam vos piscatóreshóminum.",
                  "Cum perambuláret Dóminus juxta mare Galilǽæ, vidit Petrum et Andréam rétia mitténtes in mare, et vocávit eos, dicens: * Veníte post me, fáciam vos fíeri piscatóres hóminum."))
