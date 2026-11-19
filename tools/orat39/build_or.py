"""Collect, Secret and Postcommunion for the Masses that lack them: Latin from the Missale O.P. (1939), accented;
English from the St Dominic Missal (1959) where its Latin is the same prayer."""
import json, re, difflib
from accent import accent, flat, D as ACC
from spellchecker import SpellChecker
SP = SpellChecker(); SP.word_frequency.load_words(['thee', 'thy', 'thou', 'unto', 'beseech', 'vouchsafe', 'confessor', 'virgin', 'martyr', 'martyrs', 'Dominic', 'Raymond', 'Hyacinth', 'pontiff', 'intercession', 'sacraments', 'oblation', 'oblations', 'propitiation', 'merciful', 'mercifully', 'graciously', 'sanctify', 'partaken', 'heavenly', 'everlasting', 'Holy', 'Ghost', 'evangelist', 'apostle'])
PD = 'Per Dóminum nostrum Iesum Christum, Fílium tuum: qui tecum vivit et regnat in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum.'
PDS = 'Per Dóminum nostrum Iesum Christum, Fílium tuum: qui tecum vivit et regnat in unitáte eiúsdem Spíritus Sancti Deus, per ómnia sǽcula sæculórum.'
PE = 'Per eúmdem Dóminum nostrum Iesum Christum Fílium tuum, qui tecum vivit et regnat in unitáte Spíritus Sancti, Deus, per ómnia sǽcula sæculórum.'
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
KEYS = [k for k in ACC if len(k) > 3]
BYLEN = {}
for k in KEYS: BYLEN.setdefault(len(k), []).append(k)
MANUAL = json.load(open('manual_acc.json')) if __import__('os').path.exists('manual_acc.json') else {}
def known(w): return flat(re.sub(r'[^A-Za-zæœÆŒ]', '', w)) in ACC
def ocr_fix(w):
    core = re.sub(r'[^A-Za-z]', '', w)
    if not core or known(core) or flat(core) in MANUAL: return w
    f = flat(core).replace('se', 'ae').replace('tuse', 'tuae')
    for g in (f, flat(core).replace('ss', 'ae').replace('ls', 'ae').replace('ee', 'ae').replace('il', 'u').replace('d', 'ae') , flat(core)):
        if g in ACC: return g if core.islower() else g.capitalize()
    cand = []
    for L in range(len(f) - 2, len(f) + 3):
        cand += BYLEN.get(L, [])
    m = difflib.get_close_matches(f, cand, n=1, cutoff=0.8)
    if m: return m[0] if core.islower() else m[0].capitalize()
    return w
def latin(t):
    t = t.replace('^', 'AE').strip()
    # running heads caught inside a line: "Festa Maii (1)", "Festa N ovem bris (7, 8, 9)"
    t = re.sub(r'\s*Festa\s+[A-Z]\s?[a-z][a-z ]*?\s*\([\d ,]*\)\s*', ' ', t)
    t = re.sub(r'(Jesus Christus Dominus noster,? qui tecum)[^.]*\..*$', r'\1.', t)
    t = re.sub(r'\s*Praefatio .*$', '', t)
    # words cut in two by letter-spacing: "inflam m asti", "hum anitas", "D eu s"
    for _ in range(3):
        w = t.split(' ')
        out = []
        i = 0
        while i < len(w):
            done = False
            for n in (3, 2):
                if i + n <= len(w):
                    j = ''.join(w[i:i + n]); core = re.sub(r'[^A-Za-z]', '', j)
                    if len(core) >= 3 and known(core) and not all(known(x) and len(re.sub(r'[^A-Za-z]', '', x)) > 2 for x in w[i:i + n]):
                        out.append(j); i += n; done = True; break
            if not done: out.append(w[i]); i += 1
        t = ' '.join(out)
    t = ' '.join(ocr_fix(x) if re.search(r'[A-Za-z]', x) else x for x in t.split(' '))
    t = re.sub(r'^[^A-Za-z]+', '', t)
    t = fix_spaced(t)
    # the drop-cap word in capitals
    t = re.sub(r'^([A-Z]{2,})', lambda m: m.group(1).capitalize(), t)
    t = re.sub(r'\s*:\s*', ': ', t); t = re.sub(r'\s*;\s*', '; ', t); t = re.sub(r'\s+', ' ', t)
    # the conclusion, in full
    concl = None
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
    a = re.sub(r'^([ÁÉÍÓÚ])', lambda m: {'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'}[m.group(1)], a)
    a = re.sub(r'(?<=[:;] )([ÁÉÍÓÚ])', lambda m: m.group(1), a)
    if not re.search(r'[.:;]$', a): a += ':' if concl and concl.startswith('Per') else '.'
    if concl and concl.startswith('Per') and a.endswith('.'): a = a[:-1] + ':'
    if concl and concl.startswith('Qui') and a.endswith(':'): a = a[:-1] + '.'
    return (a + ' ' + concl if concl else a), ec, unk

P = json.load(open('/home/claude/build/orat/dm_prayers.json'))
DM = [(x[0][1:], flat(x[1])[:160], x[2]) for m in P for x in m['pr'] if x[2]]
def english(kind, la_flat):
    best = (0, None)
    for k, f, en in DM:
        if k != kind or abs(len(f) - len(la_flat)) > 80: continue
        r = difflib.SequenceMatcher(None, f[:120], la_flat[:120], autojunk=False).ratio()
        if r > best[0]: best = (r, en)
    return best
def clean_en(t, ec):
    t = re.sub(r'^\s*\W*\s*(Collect|Secret|Post\s?communion|Prayer)\.\s*', '', t)
    t = re.sub(r'\b(Let us pray\.|Bow down your heads before God\.).*$', '', t)
    t = re.sub(r'(?i)[,:;]?\s*(through (our|the same) Lord|who live[s]? and reign[s]?( with You)?|through,? etc|through)\.?\s*$', '', t.strip()).strip()
    t = re.sub(r'\s+([,.;:!?])', r'\1', t); t = re.sub(r'([a-z])- ([a-z])', r'\1\2', t)
    t = t.replace('0 Lord', 'O Lord').replace(' 0 ', ' O ').replace('YOU', 'You')
    fixes = []
    def fw(m):
        w = m.group(0)
        if not re.search(r'[a-z]', w) or w[0].isupper() and w.lower() not in SP: return w
        if w.lower() in SP: return w
        c = SP.correction(re.sub(r'[^A-Za-z]', '', w).lower())
        if c and c != w.lower(): fixes.append((w, c)); return c if not w[0].isupper() else c.capitalize()
        return w
    t = re.sub(r"[A-Za-z][A-Za-z;'\"\.]*[A-Za-z]", lambda m: fw(m) if re.search(r"[;'\".]", m.group(0)[1:-1]) or m.group(0).lower() not in SP else m.group(0), t)
    t = t.rstrip(' ,;:')
    if ec: t = t + ('; ' if not t.endswith('.') else ' ') + ec[0].lower() + ec[1:] if not t.endswith('.') else t + ' ' + ec
    return t, fixes
if __name__ == '__main__':
    M = json.load(open('matched.json'))
    out, report = {}, []
    for k, m in M.items():
        if not (len(m['pr']) == 3 and all(m['pr'].values())): continue
        e = {'src': 'Missale O.P. (1939), p. ' + str(m.get('page') or '') + '; English: St Dominic Missal (1959)'}
        for kind in ('or', 'se', 'pc'):
            la, ec, unk = latin(m['pr'][kind])
            r, en = english(kind, flat(m['pr'][kind]))
            if en and r >= 0.8: en, fx = clean_en(en, ec)
            else: en, fx = '', []
            e[kind] = [la, en]
            report.append({'k': k, 'p': kind, 'unk': unk, 'fix': fx, 'r': round(r, 2), 'la': la, 'en': en})
        out[k] = e
    json.dump(out, open('new_or.json', 'w'), ensure_ascii=False, indent=0)
    json.dump(report, open('report.json', 'w'), ensure_ascii=False, indent=0)
    print(len(out), 'Masses;', sum(1 for r in report if not r['en']), 'prayers without English;', sum(len(r['unk']) for r in report), 'unknown Latin words;', sum(len(r['fix']) for r in report), 'English fixes')
