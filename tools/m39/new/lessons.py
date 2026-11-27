"""Epistle/Lesson and Gospel of a Mass in the Missale O.P. 1939 text layer: book, verse range (found in the Vulgate), opening formula.
python3 tools/m39/new/lessons.py LINE [LINE...]   (LINE = the Mass's title line in tools/orat39/m39lin.txt)"""
import re, sys, unicodedata, os
L = open('tools/orat39/m39lin.txt').read().split('\n')
def n(s): return re.sub(r'[^a-z ]', ' ', unicodedata.normalize('NFD', s.lower().replace('æ', 'ae').replace('œ', 'oe').replace('j', 'i')).encode('ascii', 'ignore').decode())
BOOKS = {'Corinthios': 'Ad Corinthios', 'Timotheum': 'Ad Timotheum', 'Hebraeos': 'Ad Hebræos', 'Philippenses': 'Ad Philippenses', 'Galatas': 'Ad Galatas',
  'Romanos': 'Ad Romanos', 'Ephesios': 'Ad Ephesios', 'Colossenses': 'Ad Colossenses', 'Thessalonicenses': 'Ad Thessalonicenses', 'Petri': 'Petri', 'Jacobi': 'Jacobi',
  'Joannis Apostoli': 'Joannis', 'Apocalypsis': 'Apocalypsis', 'Actuum': 'Actus Apostolorum', 'Matthaeum': 'Matthæus', 'Marcum': 'Marcus', 'Lucam': 'Lucas', 'Joannem': 'Joannes'}
SAP = {'Eccli': 'Ecclesiasticus', 'Sap': 'Sapientia', 'Prov': 'Proverbia', 'Cant': 'Canticum Canticorum', 'Isai': 'Isaias'}
VER = {}
def chap(book):
    if book not in VER:
        V = {}
        for l in open('bible/la/%s.txt' % book):
            a = l.rstrip('\n').split('\t')
            if len(a) >= 3: V[(int(a[0]), int(a[1]))] = n(' '.join(a[2:])).split()
        VER[book] = V
    return VER[book]
def where(book, q, ch):
    V = chap(book); hits = [(c, v) for (c, v), w in V.items() if (not ch or abs(c - ch) <= 1) and q in ' '.join(w)]
    hits.sort(key=lambda x: (x[0] != ch, x)); return hits
def find(book, words, ch):
    for i in range(0, 8):
        q = ' '.join(words[i:i + 4]); h = where(book, q, ch) if len(q.split()) == 4 else []
        if len(h) == 1 or (h and i > 3): return h[0]
    return None
def findend(book, words, ch, a1=None):
    for i in range(0, 14):
        q = ' '.join(words[len(words) - 4 - i:len(words) - i]); h = where(book, q, ch)
        h = [x for x in h if not a1 or x >= a1]
        if h: return h[0]
    return None
FORM = r'^(in illo tempore|in diebus illis|fratres|carissimi|carissime|haec dicit dominus|dilectissimi)\b\s*'
for a in sys.argv[1:]:
    s = int(a) - 1
    end = next(j for j in range(s + 3, s + 900) if re.match(r'^Die \d', L[j].strip()))
    t = ' '.join(x.strip() for x in L[s:end] if not x.startswith('@@')).replace('­ ', '')
    print('=====', L[s].strip())
    for m in re.finditer(r'(Lectio (Epistolae beati (Pauli|Petri|Jacobi|Joannis) Apostoli(?: ad (\w+))?\.?|Actuum Apostolorum,?|Libri Apocalypsis beati Joannis Apostoli\.?|Libri Sapientiae[.,]?)|Sequentia sancti Evangelii secundum (\w+)\.?)\s*([^A-Z]{0,25}?)\s*([A-Z].*?)(?=\s(?:Ps\.|Alleluia|Graduale|Tractus|Offertorium|Credo|Prov\.|Osee|Eccli\.|Sap\.|Cant\.|Matth\.|Luc\.|Joann\.|Dan\.|Apoc\.|Isai\.)\s)', t):
        head = m.group(1); ref = m.group(6); body = m.group(7)
        if m.group(5): book = BOOKS[m.group(5)]
        elif m.group(3): book = BOOKS.get(m.group(4) or m.group(3), BOOKS.get(m.group(3) + ' Apostoli', m.group(3)))
        elif 'Actuum' in head: book = 'Actus Apostolorum'
        elif 'Apocalypsis' in head: book = 'Apocalypsis'
        else:
            mm = re.match(r'(Eccli|Sap|Prov|Cant|Isai)\.?\s*(\d+)', body); book = SAP.get(mm.group(1)) if mm else None
            if mm: body = body[mm.end():]
        num = re.findall(r'\d+', ref.replace(' ', ''))
        if book in ('Ad Corinthios', 'Ad Timotheum', 'Ad Thessalonicenses', 'Petri', 'Joannis') and num: book += ' ' + num[0]; num = num[1:]
        ch = int(num[0]) if num else None
        w = n(body).split(); f = re.match(FORM, ' '.join(w))
        w2 = ' '.join(w)[f.end():].split() if f else w
        a1 = find(book, w2, ch) if book and os.path.exists('bible/la/%s.txt' % book) else None
        a2 = findend(book, [x for x in w if x not in ('credo', 'alleluia')], ch, a1) if a1 else None
        print('  %-55s | %s %s -> %s | %s ... %s' % (head[:55], book, a1, a2, ' '.join(w[:8]), ' '.join(w[-6:])))
