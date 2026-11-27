"""Clean the parsed Latin: join letter-spaced initials, decapitalise the first word, spacing before colons,
write the conclusions out in full (as data/orations.js does), i-spelling. raw.json -> la.json (+ manual corrections la_fix.json)."""
import re, json, os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H + '/../orat39'); os.chdir(H + '/../orat39')
import accent
PD = 'Per Dóminum nostrum Iesum Christum, Fílium tuum: qui tecum vivit et regnat in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum.'
PDS = 'Per Dóminum nostrum Iesum Christum, Fílium tuum: qui tecum vivit et regnat in unitáte eiúsdem Spíritus Sancti Deus, per ómnia sǽcula sæculórum.'
PE = 'Per eúndem Dóminum nostrum Iesum Christum Fílium tuum, qui tecum vivit et regnat in unitáte Spíritus Sancti, Deus, per ómnia sǽcula sæculórum.'
PES = 'Per eúndem Dóminum nostrum Iesum Christum Fílium tuum, qui tecum vivit et regnat in unitáte eiúsdem Spíritus Sancti, Deus, per ómnia sǽcula sæculórum.'
QV = 'Qui vivis et regnas cum Deo Patre, in unitáte Spíritus Sancti, Deus, per ómnia sǽcula sæculórum.'
QT = 'Qui tecum vivit et regnat in unitáte Spíritus Sancti Deus per ómnia sǽcula sæculórum.'
def join_initial(t):
    toks = t.split(' ')
    for k in range(6, 1, -1):
        w = ''.join(toks[:k]); m = re.fullmatch(r'([A-Za-z]+)([,:;.]?)', w)
        if m and accent.flat(m.group(1)) in accent.D and len(m.group(1)) > 3 and k > 1 and len(toks[0]) <= 3:
            return w + ' ' + ' '.join(toks[k:])
    return t
def first_word(t):
    m = re.match(r'^([A-Z]{2,})(\b.*)$', t, re.S)
    if m: t = m.group(1)[0] + m.group(1)[1:].lower() + m.group(2)
    return t
def concl(t):
    t = re.sub(r'\s+([:;])', r'\1', t).strip()
    t = re.sub(r'Per eúmdem', 'Per eúndem', t)
    m = re.search(r'(Per Dóminum|Per eúndem|Qui vivis|Qui tecum)((?:[^.]|\.\.\.)*)\.?\s*$', t)
    if not m or 'sǽcula' in m.group(0) or 'sæcula' in m.group(0): return t
    s, rest = m.group(1), m.group(2); body = t[:m.start()].rstrip()
    sanct = 'ejúsdem' in rest or 'eiúsdem' in rest or 'ejusdem' in rest
    c = {'Per Dóminum': PDS if sanct else PD, 'Per eúndem': PES if sanct else PE, 'Qui vivis': QV, 'Qui tecum': QT}[s]
    if body and body[-1] not in ':;.,': body += ':' if s.startswith('Per') or s.startswith('Qui') else ''
    return body + ' ' + c
def ispell(t): return t.replace('j', 'i').replace('J', 'I')
def clean(t):
    t = join_initial(t); t = first_word(t)
    t = re.sub(r'\bA cunctis\b|\bAcunctis\b', 'A cunctis', t, flags=re.I) if t.lower().startswith('acunctis') else t
    if t.lower().startswith('acunctis'): t = 'A cunctis' + t[8:]
    a, unk = accent.accent(t)
    return ispell(concl(a)), unk
if __name__ == '__main__':
    R = json.load(open(H + '/raw.json'))
    FX = json.load(open(H + '/la_fix.json')) if os.path.exists(H + '/la_fix.json') else {}
    out = []
    for x in R:
        y = {'n': x['n'], 'title': x['title'], 'unk': []}
        for k in ('or', 'se', 'pc'):
            t, unk = clean(x[k + '_ocr'])
            for a, b in FX.get(str(x['n']), {}).get(k, []) + FX.get('*', []):
                t = t.replace(a, b)
            m = re.search(r'(sæculórum\.|Per Dóminum\.)\s+(Si .*)$', t)
            if m: y['note'] = m.group(2); t = t[:m.start(2)].strip()
            y[k] = ispell(concl(t.replace('Iesum', 'Jesum'))); y['unk'] += unk
        out.append(y)
    json.dump(out, open(H + '/la.json', 'w'), ensure_ascii=False, indent=1)
    for y in out: print(y['n'], y['unk'])
