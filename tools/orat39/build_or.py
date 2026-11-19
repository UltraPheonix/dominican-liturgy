"""Collect, Secret and Postcommunion for the Masses that lack them: Latin from the Missale O.P. (1939), accented;
English from the St Dominic Missal (1959) where its Latin is the same prayer."""
import json, re, difflib
from accent import accent, flat, D as ACC
from spellchecker import SpellChecker
SP = SpellChecker(distance=1); SP.word_frequency.load_words(['thee', 'thy', 'thou', 'unto', 'beseech', 'vouchsafe', 'confessor', 'virgin', 'martyr', 'martyrs', 'Dominic', 'Raymond', 'Hyacinth', 'pontiff', 'intercession', 'sacraments', 'oblation', 'oblations', 'propitiation', 'merciful', 'mercifully', 'graciously', 'sanctify', 'partaken', 'heavenly', 'everlasting', 'Holy', 'Ghost', 'evangelist', 'apostle', 'defence', 'favour', 'honour', 'Saviour', 'Magdalene', 'Thomas', 'Aquinas', 'Siena', 'Ferrer', 'Bertrand', 'Pius', 'Agnes', 'Montepulciano'])
PD = 'Per Dóminum nostrum Iesum Christum, Fílium tuum: qui tecum vivit et regnat in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum.'
PDS = 'Per Dóminum nostrum Iesum Christum, Fílium tuum: qui tecum vivit et regnat in unitáte eiúsdem Spíritus Sancti Deus, per ómnia sǽcula sæculórum.'
PE = 'Per eúndem Dóminum nostrum Iesum Christum Fílium tuum, qui tecum vivit et regnat in unitáte Spíritus Sancti, Deus, per ómnia sǽcula sæculórum.'
QV = 'Qui vivis et regnas cum Deo Patre, in unitáte Spíritus Sancti, Deus, per ómnia sǽcula sæculórum.'
QT = 'Qui tecum vivit et regnat in unitáte Spíritus Sancti Deus per ómnia sǽcula sæculórum.'
EPD = 'Through our Lord Jesus Christ, Your Son, who lives and reigns with You in the unity of the Holy Spirit, God, world without end.'
EPDS = 'Through our Lord Jesus Christ, Your Son, who lives and reigns with You in the unity of the same Holy Spirit, God, world without end.'
EPE = 'Through the same Jesus Christ, Your Son, our Lord, who lives and reigns with You in the unity of the Holy Spirit, God, world without end.'
EQV = 'Who live and reign with God the Father, in the unity of the Holy Spirit, God, world without end.'
EQT = 'Who lives and reigns with You in the unity of the Holy Spirit, God, world without end.'

def fix_spaced(t):
    # "Su sc ipe Domine" -> "Suscipe Domine"; "Ac c e p t a" -> "Accepta"
    w = t.split(' ')
    for n in range(min(9, len(w)), 1, -1):
        if all(len(re.sub(r'[^A-Za-z]', '', x)) <= 4 for x in w[:n]):
            j = ''.join(w[:n])
            core = re.sub(r'[^A-Za-z]', '', j)
            if flat(core) in ACC and len(core) >= 4:
                return j + (' ' if len(w) > n else '') + ' '.join(w[n:])
    return t
# candidate words bucketed by (first letter, length): get_close_matches over all 75k keys was far too slow
BUCK = {}
for k in ACC:
    if len(k) > 3: BUCK.setdefault((k[0], len(k)), []).append(k)
MANUAL = json.load(open('manual_acc.json')) if __import__('os').path.exists('manual_acc.json') else {}
def known(w): return flat(re.sub(r'[^A-Za-zæœÆŒ]', '', w)) in ACC
_OCR = {}
FUZZY = []
DET = []
FUZZY_ON = False  # fuzzy matching replaced right rare forms (trahant->trahat, Guala->gula): use ocr_sub.json
OCRSUB = json.load(open('ocr_sub.json')) if __import__('os').path.exists('ocr_sub.json') else {}
def ocr_fix(w):
    core = re.sub(r'[^A-Za-z]', '', w)
    fk = flat(core)
    if fk in OCRSUB:
        r = OCRSUB[fk]
        if r and core[0].isupper(): r = r.capitalize()
        return re.sub(r"[A-Za-z0-9'&.]*[A-Za-z][A-Za-z0-9'&.]*", r, w, count=1) if r else re.sub(r'[A-Za-z\'&.0-9]+', '', w)
    # junk inside a known word: aeter'nae, mer&emur
    if core and known(core) and re.search(r"[A-Za-z]['&][A-Za-z]", w): return re.sub(r"(?<=[A-Za-z])['&](?=[A-Za-z])", '', w)
    if not core or len(core) < 4 or known(core) or flat(core) in MANUAL: return w
    if core in _OCR:
        r = _OCR[core]
        return w if r is None else w.replace(core, r)
    r = None
    fc = flat(core)
    f = fc.replace('se', 'ae').replace('tuse', 'tuae')
    for g in (f, fc.replace('ss', 'ae').replace('ls', 'ae').replace('ee', 'ae').replace('il', 'u').replace('d', 'ae'), fc):
        if g in ACC: r = g; DET.append((core, g)); break
    if r is None and FUZZY_ON:
        cand = []
        for L in range(len(f) - 1, len(f) + 2):
            cand += BUCK.get((f[0], L), [])
        m = difflib.get_close_matches(f, cand, n=1, cutoff=0.85)
        if m: r = m[0]; FUZZY.append((core, r))
    if r is not None:
        if core[0].isupper(): r = r.capitalize()
        if core.isupper() and len(core) > 1: r = r.upper()
    _OCR[core] = r
    return w if r is None else w.replace(core, r)
def latin(t):
    t = t.replace('^', 'AE').strip()
    # running heads caught inside a line: "Festa Maii (1)", "Festa N ovem bris (7, 8, 9)"
    t = re.sub(r'\s*Festa\s+[A-Z]\s?[a-z][a-z ]*?\s*\([\d ,]*\)\s*', ' ', t)
    t = re.sub(r'(Jesus Christus Dominus noster,? qui tecum)[^.]*\..*$', r'\1.', t)
    t = re.sub(r'\s*Praefatio .*$', '', t)
    # page numbers, running-head dashes, stray quotes and lone consonants left by the text layer
    t = t.replace('Q17ESUMUS', 'QUAESUMUS').replace('Co n c ed e nos', 'Concede nos')
    t = re.sub(r'\s*—\s*', ' ', t); t = re.sub(r'(?<![A-Z])\d+[a-z]?', ' ', t); t = re.sub(r"\s*'\s*", ' ', t); t = re.sub(r'\be s(?=[:;,. ])', 'es', t)
    # abbreviated conclusions: "Per Dominum... in unitate ejusdem (Spiritus)." / "Dominum nostrum Jesum Christum..."
    t = re.sub(r'(Per )?Dominum(\.\.\.| nostrum Jesum Christum\.*)\s*(in unitate ejusdem( Spiritus)?\.?)?\s*$', lambda m: 'Per Dominum ejusdem.' if m.group(3) else 'Per Dominum.', t)
    # words cut in two by letter-spacing: "inflam m asti", "hum anitas", "D eu s"
    for _ in range(3):
        w = t.split(' ')
        out = []
        i = 0
        while i < len(w):
            done = False
            for n in (5, 4, 3, 2):
                if i + n <= len(w):
                    j = ''.join(w[i:i + n]); core = re.sub(r'[^A-Za-z]', '', j)
                    if len(core) >= 3 and known(core) and not all(known(x) and len(re.sub(r'[^A-Za-z]', '', x)) >= 2 for x in w[i:i + n]):
                        out.append(j); i += n; done = True; break
            if not done: out.append(w[i]); i += 1
        t = ' '.join(out)
    t = ' '.join(ocr_fix(x) if re.search(r'[A-Za-z]', x) else x for x in t.split(' '))
    t = re.sub(r'(?<= )[b-df-hj-np-tv-z](?= )', '', t)
    t = re.sub(r'^[^A-Za-z]+', '', t)
    t = fix_spaced(t)
    # the drop-cap word in capitals
    t = re.sub(r'^([A-Z]{2,})', lambda m: m.group(1).capitalize(), t)
    t = re.sub(r'\s*:\s*', ': ', t); t = re.sub(r'\s*;\s*', '; ', t); t = re.sub(r'\s+', ' ', t)
    # the conclusion, in full
    concl = None
    t = re.sub(r'[,;:]?\s*qui tecum\.?\s*$', ': Qui tecum.', t)
    t = re.sub(r'Per eumdem\.?\s*$', 'Per eumdem Dominum.', t)
    m = re.search(r'(Per (eumdem )?Dominum[^.]*|Qui vivis[^.]*|Qui tecum[^.]*)\.?\s*$', t)
    if m:
        s = m.group(0); body = t[:m.start()].rstrip(' :;,')
        if s.startswith('Per eumdem'): concl, ec = PE, EPE
        elif s.startswith('Per'): concl, ec = (PDS, EPDS) if 'ejusdem' in s or 'eiusdem' in s else (PD, EPD)
        elif s.startswith('Qui vivis'): concl, ec = QV, EQV
        else: concl, ec = QT, EQT
    else: body, ec = t.rstrip(), ''
    a, unk = accent(body)
    for w0 in list(unk):
        if flat(w0) in MANUAL:
            a = re.sub(r'\b' + re.escape(w0) + r'\b', MANUAL[flat(w0)] if w0[0].islower() else MANUAL[flat(w0)].capitalize(), a); unk.remove(w0)
    # hand accents win over the dictionary (it holds some unaccented forms: restaurare, Raymundi)
    def _man(m):
        w0 = m.group(0); r0 = MANUAL.get(flat(w0))
        if not r0: return w0
        if w0[0].isupper(): r0 = r0[0].upper() + r0[1:]
        if 'j' in w0.lower() and 'i' in r0: r0 = ''.join('j' if (c in 'iI' and i < len(w0) and w0[i] in 'jJ') else c for i, c in enumerate(r0))
        return r0
    a = re.sub(r"[A-Za-zÀ-ÿæœǽÆŒǼ]+", _man, a)
    a = re.sub(r'^([ÁÉÍÓÚ])', lambda m: {'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'}[m.group(1)], a)
    a = re.sub(r'(?<=[:;] )([ÁÉÍÓÚ])', lambda m: m.group(1), a)
    if not re.search(r'[.:;]$', a): a += ':' if concl and concl.startswith('Per') else '.'
    if concl and concl.startswith('Per') and a.endswith('.'): a = a[:-1] + ':'
    if concl == QV and a.endswith(':'): a = a[:-1] + '.'
    if concl == QT and a.endswith('.'): a = a[:-1] + ':'
    return (a + ' ' + concl if concl else a), ec, unk

P = json.load(open('dm_prayers.json'))
DM = [(x[0][1:], flat(x[1])[:160], x[2]) for m in P for x in m['pr'] if x[2]]
def english(kind, la_flat):
    best = (0, None)
    for k, f, en in DM:
        if k != kind or abs(len(f) - len(la_flat)) > 80: continue
        sm = difflib.SequenceMatcher(None, f[:120], la_flat[:120], autojunk=False)
        if sm.real_quick_ratio() <= best[0] or sm.quick_ratio() <= best[0]: continue
        r = sm.ratio()
        if r > best[0]: best = (r, en)
    return best
_SPC = {}
def _corr(w):
    if w not in _SPC: _SPC[w] = SP.correction(w)
    return _SPC[w]
def clean_en(t, ec):
    t = re.sub(r'^\s*\W*\s*(Collect|Secret|Post\s?communion|Prayer)\.\s*', '', t)
    # the DM column often runs on into the next Latin text: stop at the prayer's own conclusion
    m = re.search(r'(?i)(through (our|the same) Lord[^.]*|who (live|lives) and reigns?[^.]*|world without end|for ?ever and ever)\.', t)
    if m: t = t[:m.end()]
    t = re.sub(r'\b(Let us pray\.|Bow down your heads before God\.).*$', '', t)
    t = re.sub(r'(?i)[,:;]?\s*(through (our|the same) Lord|who live[s]? and reign[s]?( with You)?|through,? etc|through)\.?\s*$', '', t.strip()).strip()
    t = re.sub(r'\s+([,.;:!?])', r'\1', t); t = re.sub(r'([a-z])- ([a-z])', r'\1\2', t)
    t = t.replace('0 Lord', 'O Lord').replace(' 0 ', ' O ').replace('YOU', 'You')
    fixes = []
    def fw(m):
        w = m.group(0)
        if not re.search(r'[a-z]', w) or w[0].isupper() and w.lower() not in SP: return w
        if w.lower() in SP: return w
        c = _corr(re.sub(r'[^A-Za-z]', '', w).lower())
        if c and c != w.lower(): fixes.append((w, c))
        return w  # suggestions only: autocorrect damaged real words (serve/servant, interne/intercession)
        return w
    t = re.sub(r"[A-Za-z][A-Za-z;'\"\.]*[A-Za-z]", lambda m: fw(m) if re.search(r"[;'\".]", m.group(0)[1:-1]) or m.group(0).lower() not in SP else m.group(0), t)
    t = t.rstrip(' ,;:')
    if ec: t = t + ('; ' if not t.endswith('.') else ' ') + ec[0].lower() + ec[1:] if not t.endswith('.') else t + ' ' + ec
    return t, fixes
if __name__ == '__main__':
    M = json.load(open('matched.json'))
    OV = json.load(open('overrides.json'))
    EF = json.load(open('en_final.json'))
    for k, d in OV.items():
        for kind, txt in d.items(): M[k]['pr'][kind] = txt
    out, report = {}, []
    REJECT = {'S0508b', 'S1119b', 'G481'}  # wrong date matches: post-1939 Blesseds / a votive Mass
    for k, m in M.items():
        if k in REJECT: continue
        if not (len(m['pr']) == 3 and all(m['pr'].values())): continue
        e = {'src': 'Missale O.P. (1939), p. ' + str(m.get('page') or '') + '; English: St Dominic Missal (1959)'}
        for kind in ('or', 'se', 'pc'):
            la, ec, unk = latin(m['pr'][kind])
            r, en = english(kind, flat(m['pr'][kind]))
            if kind in EF.get(k, {}):
                # hand-checked English (en_final.json): the body only; the conclusion follows the Latin
                b0 = EF[k][kind].rstrip(' .;:,')
                en, fx = (b0 + '; ' + ec[0].lower() + ec[1:] if ec else b0 + '.'), []
                if ec == EQT or ec == EQV: en = b0 + '; ' + ec[0].lower() + ec[1:]
                r = 'final'
            elif en and r >= 0.8: en, fx = clean_en(en, ec)
            else: en, fx = '', []
            e[kind] = [la, en]
            report.append({'k': k, 'p': kind, 'unk': unk, 'fix': fx, 'r': r if isinstance(r, str) else round(r, 2), 'la': la, 'en': en})
        out[k] = e
    json.dump(out, open('new_or.json', 'w'), ensure_ascii=False, indent=0)
    json.dump(report, open('report.json', 'w'), ensure_ascii=False, indent=0)
    json.dump(sorted(set(map(tuple, FUZZY))), open('fuzzy.json', 'w'), ensure_ascii=False)
    json.dump(sorted(set(map(tuple, DET))), open('det.json', 'w'), ensure_ascii=False)
    print(len(set(DET)), 'rule OCR fixes (det.json)')
    print(len(out), 'Masses;', sum(1 for r in report if not r['en']), 'prayers without English;', sum(len(r['unk']) for r in report), 'unknown Latin words;', sum(len(r['fix']) for r in report), 'English fixes')
