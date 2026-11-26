"""Put the saint's name for 'N.' in the Commons, in the case the text needs.
The calendar title gives the name in the genitive ('B. Simónis Ballácchii Conf. O.P.'); each word is declined from it.
The case of each 'N.' comes from the word before it (beáti N. = genitive, beátum N. = accusative, sancto suo N. = dative,
Sancte N. / beáte N. / Conféssor Dómini N., = vocative, Gloriósus Dei amícus N. / beáta N. Virgo = nominative).
A name that cannot be declined surely is left as 'N.' (never a guessed form)."""
import re, unicodedata

def plain(s):
    s = unicodedata.normalize('NFD', s); return ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower().replace('æ', 'ae')

# third declension: genitive -> nominative (accent as printed in the 1909 Breviary's usage)
NOM3 = {'felícis': 'Félix', 'cleméntis': 'Clemens', 'agnétis': 'Agnes', 'simónis': 'Simon', 'joánnis': 'Joánnes',
        'hugónis': 'Hugo', 'leónis': 'Leo', 'ludovíci': None, 'bertrándi': None, 'pétri': None, 'damiáni': None,
        'célsi': None, 'nazárii': None, 'gervásii': None, 'protásii': None, 'vitális': 'Vitális', 'pancrátii': None,
        'innocéntii': None, 'canúti': None, 'margarítæ': None, 'raymúndi': None, 'zenónis': 'Zeno', 'ottónis': 'Otto',
        'cypriáni': None, 'sebastiáni': None, 'fabiáni': None, 'tiburtíi': None, 'nérei': None, 'achíllei': None,
        'pétris': None, 'salvatóris': 'Salvátor', 'castóris': 'Castor', 'hippólyti': None, 'hermenegíldi': None,
        'anicéti': None, 'urbáni': None, 'félicis': 'Félix', 'felicitátis': 'Felícitas', 'perpétuæ': None,
        'chrysógoni': None, 'saturníni': None, 'eusébii': None, 'thomæ': None, 'barnabæ': None, 'matthíæ': None,
        'elísabeth': 'Elísabeth', 'ágnetis': 'Agnes', 'apollináris': 'Apollináris', 'bonifátii': None, 'próspéri': None,
        'luciæ': None, 'pii': None, 'damási': None, 'sylvéstri': None, 'hilariónis': 'Hilárion', 'macárii': None,
        'nicoláus': None, 'nicolái': None, 'januárii': None, 'cosmæ': None, 'damiáni ': None, 'lini': None, 'cleti': None,
        'marcellíni': None, 'pétronillæ': None, 'pauli': None, 'joséph': 'Joseph', 'joseph': 'Joseph', 'jacóbi': None,
        'basílii': None, 'antoníni': None, 'vincéntii': None, 'gregórii': None, 'catharínæ': None, 'cæcíliæ': None}
MASC_A = {'andreae': 'Andréas', 'thomae': 'Thomas', 'matthiae': 'Matthías', 'barnabae': 'Bárnabas', 'cosmae': 'Cosmas',
          'lucae': 'Lucas', 'nicolai': None}
INDECL = {'elísabeth', 'joseph', 'de', 'a', 'ab', 'e', 'ex'}

def forms(g, male):
    """the cases of one genitive word: dict nom acc dat abl voc, or None"""
    p = plain(g)
    if g.lower() in INDECL or p in ('elisabeth', 'joseph'): return dict(gen=g, nom=g, acc=g, dat=g, abl=g, voc=g)
    if p.endswith('ae'):
        st = g[:-1]   # 'Lúciæ' -> 'Lúci'
        if p in MASC_A and MASC_A[p]:   # Greek names in -as (Andréas, Thomas); Latin ones keep -a (Guala)
            nom = MASC_A[p]
            return dict(gen=g, nom=nom, acc=st + 'am', dat=g, abl=st + 'a', voc=st + 'a')
        return dict(gen=g, nom=st + 'a', acc=st + 'am', dat=g, abl=st + 'a', voc=st + 'a')
    if p.endswith('is'):
        nom = NOM3.get(g.lower()) or NOM3.get(g[0].lower() + g[1:])
        if not nom and p.endswith('onis') and p != 'simonis': nom = plain(g)[:-3].capitalize()   # Brunónis -> Bruno, Aimónis -> Aimo
        if not nom and p == 'mannis': nom = 'Mannes'
        if not nom: return None
        st = g[:-2]
        return dict(gen=g, nom=nom, acc=st + 'em', dat=st + 'i', abl=st + 'e', voc=nom)
    if p.endswith('ii'):
        st = g[:-2]
        return dict(gen=g, nom=st + 'ius', acc=st + 'ium', dat=st + 'io', abl=st + 'io', voc='Pie' if p == 'pii' else st + 'i')
    if p.endswith('i'):
        st = g[:-1]
        return dict(gen=g, nom=st + 'us', acc=st + 'um', dat=st + 'o', abl=st + 'o', voc=st + 'e')
    return dict(gen=g, nom=g, acc=g, dat=g, abl=g, voc=g)   # indeclinable surname ('Nolásco', 'Porres', 'Valois')

RANK = re.compile(r'\s(?:Conf|Ep|Mart|Virg|V|Vid|Víduæ|Abbátis|Abb|Papæ|Apóst|Apóstoli|Evang|Doct|Eccl|Pont|Regis|Reg|Presb|Diac|'
                  r'MM|O\.\s?P|Mon|Erem|Pœnit|Fundat|Reginæ|Imperat|Ord|Martyris|Vírginis|Confessóris)\b\.?')
def names(title):
    """[(words, male)] from a calendar title; [] if none can be read"""
    t = re.sub(r'\s*\((?:translatum|.*?)\)', '', title)
    t = re.sub(r'\bS\. P\. N\.', 'S.', t)   # S. P. N. Domínici = Sancti Patris nostri Domínici
    m = re.search(r'(?:^|\s)(SS?|BB?)\.\s+(.*)$', t)
    if not m: return []
    body = m.group(2)
    if re.match(r'(?:\w\.|Angel|Corón|Nómin|Salvat|Michaél|Gabriél|Raphaél|Ómnium|Innocéntium|Stigmat|Cordis|Trinit)', body): return []
    r = RANK.search(' ' + body)
    head = (' ' + body)[:r.start()].strip() if r else body
    tail = (' ' + body)[r.start():] if r else ''
    male = not re.search(r'Virg|Vid|Víduæ|Reginæ|\bV\.', tail)
    if m.group(1) in ('SS', 'BB'):
        parts = [x.strip() for x in re.split(r',\s*|\s+et\s+|\s+ac\s+', head) if x.strip() and not re.match(r'Soci', x)]
        return [(p.split(), male) for p in parts if not re.match(r'Quátuor|Septem|Sanctórum|Ómnium', p)]
    return [(head.split(), male)]

def decline(words, male, case):
    """the Christian name only, as the Breviary does in its proper Offices ('beáti Felícis', not 'de Valois')"""
    out = []; prep = False
    for w in words[:1]:
        if prep: out.append(w); continue   # after 'de', 'a': as printed ('a Cruce', 'de Valois')
        if w.lower() in ('de', 'a', 'ab', 'e', 'ex', 'von'): prep = True; out.append(w); continue
        if re.fullmatch(r'[IVXL]+', w): out.append(w); continue   # Gregórii Papæ X
        f = forms(w, male)
        if not f: return None
        out.append(f[case])
    return ' '.join(out)

def case_of(before, after):
    before = re.sub(r'</?\w+>', '', before); before = re.sub(r'<\w+>[^<]*$', '', before)
    b = plain(before.split()[-1]) if before.split() else ''
    b2 = plain(' '.join(before.split()[-3:]))
    if re.search(r'amicus$', b2) or (b == 'beata' and re.match(r'\s*Virgo', after)): return 'nom'
    if b in ('beati', 'beatae', 'sancti', 'sanctae', 'beatissimi') or re.search(r'(?:patris|matris) (?:nostri|nostrae)$', b2): return 'gen'
    if b in ('beatum', 'beatam', 'sanctum', 'sanctam'): return 'acc'
    if b2.endswith('sancto suo') or b2.endswith('beato suo'): return 'dat'
    if b in ('sancto', 'beato') and not re.search(r'\b(?:in|de|cum|pro|a|ab|ex|e)\s+\S+\s*$', before): return 'dat'
    if b in ('beate', 'sancte', 'beata', 'domini') or b2.endswith('o sancte'): return 'voc'
    return None

def fill(text, title):
    """'N.' -> the saint's name; text unchanged where unsure"""
    if 'N.' not in text: return text
    ns = names(title)
    if not ns: return text
    def rep(m):
        cs = case_of(text[max(0, m.start() - 60):m.start()], text[m.end():m.end() + 20])
        if not cs: return m.group(0)
        if m.group(0).startswith('N. et N.'):
            if len(ns) < 2: return m.group(0)
            dl = [decline(w, ml, cs) for w, ml in ns]
            if None in dl: return m.group(0)
            return (', '.join(dl[:-1]) + ' et ' + dl[-1]) + m.group(0)[8:]
        if len(ns) != 1: return m.group(0)
        d = decline(ns[0][0], ns[0][1], cs)
        return d + m.group(0)[2:] if d else m.group(0)
    return re.sub(r'\bN\.(?: et N\.)?', rep, text)

def fill_en(text, title):
    """English: the name in the nominative, without accents ('blessed N.' -> 'blessed Felix')"""
    ns = names(title)
    if len(ns) != 1: return text
    d = decline(ns[0][0], ns[0][1], 'nom')
    if not d: return text
    d = ''.join(c for c in unicodedata.normalize('NFD', d) if unicodedata.category(c) != 'Mn')
    return re.sub(r'\bN\.', d, text)
def fill_all(x, title):
    if isinstance(x, str): return fill(x, title)
    if isinstance(x, dict): return {k: fill_all(v, title) for k, v in x.items()}
    if isinstance(x, list): return [fill_all(v, title) for v in x]
    if isinstance(x, tuple): return tuple(fill_all(v, title) for v in x)
    return x

if __name__ == '__main__':
    for t in ['B. Simónis Ballácchii Conf. O.P.', 'S. Felícis de Valois Conf.', 'S. Cæcíliæ Virg. et Mart.', 'S. Andréæ Avellíni Conf.',
              'B. Gregórii Papæ X Conf.', 'S. Cleméntis Papæ et Mart.', 'S. Joánnis a Cruce Conf.', 'S. Petri Nolásco Conf. (translatum)',
              'S. Elísabeth Víduæ', 'Ordinátio S. Ambrósii Ep. Conf. et Eccl. Doct.', 'B. Lúciæ a Nárnia Virg. O.P.', 'S. Agnétis Virg. et Mart.']:
        ns = names(t); print(t, '->', [(w, m, decline(w, m, 'acc'), decline(w, m, 'voc')) for w, m in ns])
    print(fill('Ora pro nobis, beáte N. ut digni. Deus, qui nos beáti N. Confessóris tui ánnua. Conféssor Dómini N., astántem', 'S. Felícis de Valois Conf.'))
