"""Seasonal tunes of Te lucis at Compline (Completorium O.P. 1949 pp. 40-45, 70-76): each is the melody of the feast's own
hymn in the Antiphonarium O.P. 1933 (GregoBase ids below), set to the words of Te lucis with the doxology of the feast.
usage: python3 tools/chant/telucis_seasonal.py   (writes data/chant/op/C49-telucis-*.gabc)"""
import sqlite3, json, re, os
DB = os.path.join(os.path.dirname(__file__), '..', 'gregobase', 'gb.sqlite')
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'chant', 'op')
S1 = "Te lu-cis an-te tér-mi-num, Re-rum Cre-á-tor, pó-sci-mus, Ut só-li-ta cle-mén-ti-a Sis præ-sul ad cu-stó-di-am."
S2 = "Pro-cul re-cé-dant sóm-ni-a, Et nó-cti-um phan-tás-ma-ta: Ho-stém-que no-strum cóm-pri-me, Ne pol-lu-án-tur cór-po-ra."
PRAESTA = "Præ-sta, Pa-ter om-ní-po-tens, Per Je-sum Chri-stum Dó-mi-num, Qui te-cum in per-pé-tu-um Re-gnat cum San-cto Spí-ri-tu."
NATUS = "Gló-ri-a ti-bi, Dó-mi-ne, Qui na-tus es de Vír-gi-ne, Cum Pa-tre~et San-cto Spí-ri-tu, In sem-pi-tér-na sǽ-cu-la."
MARIA = "Ma-rí-a, Ma-ter grá-ti-æ, Ma-ter mi-se-ri-cór-di-æ, Tu nos ab ho-ste pró-te-ge, Et ho-ra mor-tis sú-sci-pe."
FAMILIA = "Je-su, tu-is o-bé-di-ens Qui fa-ctus es pa-rén-ti-bus, Cum Pa-tre sum-mo~ac Spí-ri-tu Sem-per ti-bi sit gló-ri-a."
CORDE = "Gló-ri-a ti-bi, Dó-mi-ne, Qui Cor-de fun-dis grá-ti-am, Cum Pa-tre~et San-cto Spí-ri-tu, In sem-pi-tér-na sǽ-cu-la."
PII = "Pi-i Ma-rí-æ sér-vu-li, Chri-sti red-ém-pti sán-gui-ne, Tan-tum do-ló-rem flé-bi-li Re-co-gi-tá-te lú-mi-ne."
SIT = "Sit sum-ma Chri-sto gló-ri-a, A-má-ra cu-jus pás-si-o Æ-tér-na no-bis gáu-di-a Ma-trís-que det com-pás-si-o."
SCEPTRA = "Gló-ri-a ti-bi, Dó-mi-ne, Qui scep-tra mun-di tém-pe-ras, Cum Pa-tre~et San-cto Spí-ri-tu, In sem-pi-tér-na sǽ-cu-la."
APPAR = "Gló-ri-a ti-bi, Dó-mi-ne, Qui~ap-pa-ru-í-sti hó-di-e, Cum Pa-tre~et San-cto Spí-ri-tu, In sem-pi-tér-na sǽ-cu-la."
TUNES = {  # key: (GregoBase id, stanzas after the first two, Amen if the source has none)
    'hn':   (6485, [NATUS], None),             # Holy Name (p. 40) = Jesu dulcis memoria, IV
    'hn2':  (7169, [NATUS], 'A(fgf)men.(ef)'),  # Holy Name, tonus alter (p. 41) = Jesu decus angelicum, II
    'hf':   (5494, [FAMILIA], None),            # Holy Family (p. 45) = O lux beata Caelitum, II
    'tri':  (5432, [PRAESTA], None),            # Trinity (p. 70) = Adesto sancta Trinitas, I
    'cc':   (5303, [NATUS], 'A(ghg)men.(fg)'),  # Corpus Christi (p. 71) = Verbum supernum prodiens, VIII
    'bvma': (4884, [MARIA, NATUS], None),       # B.V.M., I and II class (p. 75): the Antiphonarium's own tune, I
    'bvmb': (5081, [MARIA, NATUS], 'A(hih)men.(gh)'),  # B.V.M., Totum Duplex (p. 76) = Aurora soli praevia, II
    # the saints (pp. 83-117): again the melody of the feast's own hymn
    'crc':  (7032, [PRAESTA], None),            # St Catherine de' Ricci (p. 84) = Caelestis aulae nuntius, VI
    'tom':  (6180, [PRAESTA], None),            # St Thomas, and his patronage (pp. 85, 116) = Lauda Mater... Thomae, I
    'pb':   (6830, [PRAESTA], None),            # Precious Blood (p. 96) = Salvete Christi vulnera, VIII
    'mm':   (6136, [PRAESTA], None),            # St Mary Magdalene (p. 97) = Lauda Mater Ecclesia, II
    'spd':  (4696, [PRAESTA], None),            # St Dominic (p. 98) = Gaude Mater Ecclesia, VII
    'domtr':(4696, [APPAR], None),              # Transfiguration (p. 99): St Dominic's tune, 'qui apparuisti hodie'
    'mdol': (5254, [PII, SIT], None),           # Seven Sorrows and Compassion (pp. 86, 101-102) = Summae Deus clementiae, II
    'ros':  (7032, [MARIA, NATUS], None),       # Rosary (pp. 104-105) = Caelestis aulae nuntius, VI
    'ang':  (5798, [PRAESTA], None),            # Guardian Angels (p. 106) = Orbis patrator optime, VIII
    'fra':  (6595, [PRAESTA], None),            # St Francis (p. 108) = Plaude turba paupercula, V
    'ter':  (4866, [PRAESTA], None),            # St Teresa (p. 111) = Haec est dies, II
    'ck':   (5550, [SCEPTRA], None),            # Christ the King (p. 113) = Vexilla Christus inclita, I
    'os':   (6475, [PRAESTA], None),            # All Saints and its octave; All Saints O.P. (pp. 114-115) = Jesu Salvator saeculi, I
    'alb':  (5975, [PRAESTA], None),            # St Albert (p. 117) = Noctis tenebras dissipans, VIII
}
MODE = {'crc': '6', 'tom': '1', 'pb': '8', 'mm': '2', 'spd': '7', 'domtr': '7', 'mdol': '2', 'ros': '6', 'ang': '8', 'fra': '5', 'ter': '2', 'ck': '1', 'os': '1', 'alb': '8', 'hn': '4', 'hn2': '2', 'hf': '2', 'tri': '1', 'cc': '8', 'bvma': '1', 'bvmb': '2'}
db = sqlite3.connect(DB)
def build(key, gid, extra, amen):
    g = db.execute('select gabc from gregobase_chants where id=?', (gid,)).fetchone()[0]
    g = json.loads(g) if g.startswith('"') else g
    g = g[g.index('('):]
    clef = re.match(r'\(([cf]b?\d)\)', g).group(1)
    st1 = g[len(clef) + 2:].split('2.')[0]
    seq = []
    for t, n in re.findall(r'([^()]*)\(([^)]*)\)', st1):
        t = t.strip()
        if t: seq.append(('s', n))
        elif n.strip() in (':', ';', '::', ',', ';1', ';2', ';3', ';4', ';5', ';6', ''): seq.append(('b', n))
        else: seq.append(('n', n))
    while seq and seq[-1][0] == 'b': seq.pop()
    m = re.search(r'A\(([^)]*)\)men\.?\(([^)]*)\)', g)
    if not amen and m: amen = 'A(%s)men.(%s)' % m.groups()
    if not amen:   # the usual Amen on the final: a torculus on it, then the note below rising to it
        fin = [n for k, n in seq if k == 's'][-1][-1]; L = 'abcdefghijklm'; i = L.index(fin)
        amen = 'A(%s%s%s)men.(%s%s)' % (fin, L[i + 1], fin, L[i - 1], fin)
    out = ['(%s)' % clef]
    for si, st in enumerate([S1, S2] + extra):
        syls = []
        for w in st.split():
            p = w.split('-')
            for i, s in enumerate(p): syls.append(s.replace('~', ' ') + (' ' if i == len(p) - 1 else ''))
        nsyl = sum(1 for k, _ in seq if k == 's')
        assert len(syls) == nsyl, (key, si, len(syls), nsyl)
        if si: syls[0] = '%d. ' % (si + 1) + syls[0]
        it = iter(syls); line = ''
        for k, n in seq:
            if k == 's': x = next(it); line += x.rstrip(' ') + '(' + n + ')' + (' ' if x.endswith(' ') else '')
            else: line += '(' + n + ') '
        out.append(line.strip() + ' (::)')
    body = ' '.join(out) + ' ' + amen + ' (::)'
    hdr = 'name:Te lucis ante terminum;\noffice-part:Hymnus;\nmode:%s;\nbook:Completorium O.P. 1949 (melody: GregoBase %d, Antiphonarium O.P. 1933);\n' % (MODE[key], gid)
    open(os.path.join(OUT, 'C49-telucis-%s.gabc' % key), 'w').write(hdr + '%%\n' + body + '\n')
for k, v in TUNES.items(): build(k, *v)
# Sacred Heart (pp. 72-73): transcribed from the page (no source in GregoBase); lines 3-4 repeat the shape of 2
SCJ_MEL = ("(c4) Te(dh) lu(hg)cis(h) an(g)te(fe) tér(g)mi(g)num,(h) (;) Re(hj)rum(ji) Cre(gh)á(hg)tor,(fe) pó(g)sci(g)mus(h) (:) "
           "Ut(d) só(f)li(e)ta(ghg) cle(fe)mén(dc)ti(de)a(e) (;) Sis(g) præ(fgh)sul(hg) ad(fe) cu(c)stó(ef)di(d)am.(d) (::) A(ded)men.(cd) (::)")
open('/tmp/scj.gabc', 'w').write(SCJ_MEL)
def build_text(key, mel, extra):
    toks = re.findall(r'([^()]*)\(([^)]*)\)', mel.split('A(')[0])
    seq = [('s', n) if t.strip() else ('b', n) for t, n in toks[1:]]
    out = ['(c4)']
    for si, st in enumerate([S1, S2] + extra):
        syls = []
        for w in st.split():
            q = w.split('-')
            for i, x in enumerate(q): syls.append(x.replace('~', ' ') + (' ' if i == len(q) - 1 else ''))
        if si: syls[0] = '%d. ' % (si + 1) + syls[0]
        it = iter(syls); line = ''
        for k, n in seq:
            if k == 's': x = next(it); line += x.rstrip(' ') + '(' + n + ')' + (' ' if x.endswith(' ') else '')
            else: line += '(' + n + ') '
        out.append(line.strip())
    body = ' '.join(out) + ' A(ded)men.(cd) (::)'
    open(os.path.join(OUT, 'C49-telucis-%s.gabc' % key), 'w').write('name:Te lucis ante terminum;\noffice-part:Hymnus;\nmode:1;\nbook:Completorium O.P. 1949, pp. 72-73 (transcribed from the page);\n%%\n' + body + '\n')
build_text('scj', SCJ_MEL, [CORDE])
# Epiphany (pp. 42-44): the Christmas tune, with 'Qui apparuisti hodie' (the extra syllable repeats the first note)
nat = open(os.path.join(OUT, 'C49-telucis-nat.gabc')).read()
epi = nat.replace('Qui(g) na(hj)tus(j) es(ji) de(hg) Vír(hi)gi(i)ne,(i)', 'Qui(g) ap(g)pa(hj)ru(j)í(ji)sti(hg) hó(hi)di(i)e,(i)')
assert epi != nat
open(os.path.join(OUT, 'C49-telucis-epi.gabc'), 'w').write(epi)
print('ok')
