# Feria V in Cena Domini: Matins (Tenebrae) and Lauds from the Triduum book O.P. (1927) -> tools/hw39/Quad6h_ten.src
import psalms, json
out = []
def w(*l): out.extend(l)
def T(la, en): w('T: ' + la, ' = ' + en)
def R(la, en): w('R: ' + la, ' = ' + en)
TONE = {68: ('VIII', 'c'), 69: ('VIII', 'c'), 70: ('VIII', 'c'), 71: ('VII', 'd'), 72: ('VIII', 'c'), 73: ('I', 'a'), 74: ('VII', 'd'), 75: ('VIII', 'c'),
        76: ('VII', 'a'), 53: ('VIII', 'G'), '118(1-16)': ('VIII', 'G'), '118(17-32)': ('VIII', 'G'), '118(33-48)': ('VIII', 'G'), '118(49-64)': ('VIII', 'G'),
        '118(65-80)': ('VIII', 'G'), '118(81-96)': ('VIII', 'G'), '118(97-112)': ('VIII', 'G'), '118(113-128)': ('VIII', 'G'), '118(129-144)': ('VIII', 'G'),
        '118(145-160)': ('VIII', 'G'), '118(161-176)': ('VIII', 'G'), 50: ('VIII', 'G'), 89: ('II', 'D'), 62: ('VIII', 'G'), 'Canticum Moysis': ('IVA', 'A'), 148: ('II', 'D'), 'Canticum Zachariæ': ('I', 'g')}
PSPEC = []
def ps(n, title_la, title_en, sung=True):
    vs = psalms.psalm(n)
    w('F: %s | %s' % (title_la, title_en))
    if sung:
        tn, d = TONE[n]; pid = 'op-ten-h-ps-%s' % (str(n) if isinstance(n, int) else ('moysis' if 'Moysis' in n else 'zachariae' if 'Zach' in n else n.replace('(', '-').replace(')', '')))
        PSPEC.append(dict(id=pid, name=title_la, tone=tn, diff=d, solemn=(n == 'Canticum Zachariæ'), verses=[la for la, en in vs],
                          src='Ecclesiasticum Officium O.P. Triduo ante Pascha (1927): tone and ending as the book gives them on the first verse',
                          tr='set to the Dominican psalm tone (Tonorum communium regulae)'))
        w('G: %s | Tonus %s %s' % (pid, tn.replace('IVA', 'IV A'), d))
        w('F: Textus et versio | Text and translation')
    for la, en in vs: T(la, en)
    if sung: w('F/')
    w('F/')
def ant(code, inc, ps_ref, la, en, mode=''):
    T('{Aña} %s {%s}' % (inc, ps_ref), '{Ant.} %s {%s}' % (en.split(' ')[0] + '…', ps_ref.replace('Ps.', 'Ps.')))
def ANT(code, la, en, label):
    T('{Aña} ' + la, '{Ant.} ' + en); w('G: op-ten-h-%s | %s' % (code, label))
F = json.load(open('/home/claude/build/ten/final_h.json'))
# ---------------------------------------------------------------- Matins
w('== Ad Matutinum (Tenebræ) | Matins (Tenebrae)', 'H: FERIA QUINTA IN CENA DOMINI', ' = MAUNDY THURSDAY', 'H: AD MATUTINUM', ' = MATINS')
w('S: Ecclesiasticum Officium O.P. Triduo ante Pascha (1927), pp. 1-31')
R('Officium celebratur ad modum Festi Duplicis. Feria V in Cena Domini et duabus sequentibus, Prior (ex choro dextro) faciat Officium ad Horas in quibus in festis solemnibus est notatum. In Matutinis quindecim candelæ coram altari præparentur et ante Matutinum accendantur; quarum singulæ ad inceptionem cujuslibet Psalmi, una hinc et alia inde, a Sacrista exstinguantur. Similiter fiat in Feria sexta et Sabbato.',
  'The Office is celebrated in the manner of a Double feast. On Maundy Thursday and the two following days the Prior (from the right-hand choir) does the Office at the Hours at which he does it on solemn feasts. At Matins fifteen candles are set before the altar and lit before Matins; one of them is put out by the Sacristan at the beginning of each Psalm, one on this side and one on the other. The same is done on Good Friday and Holy Saturday.')
R('Hoc triduo ante Matutinum non dicatur *Dómine, lábia mea apéries,* nec *Deus, in adjutórium,* neque Invitatórium, neque Hymnus; sed dicto *Pater noster,* et *Credo in Deum,* postquam versis vultibus ad altare signaverint se Fratres, statim ex choro dextro incipiatur:',
  'On these three days *Dómine, lábia mea apéries,* *Deus, in adjutórium,* the Invitatory and the Hymn are not said before Matins; but when the *Pater noster* and the *Credo* have been said, and the brethren, turned towards the altar, have signed themselves, the right-hand choir at once begins:')
R('Non dicatur *Glória Patri* in fine Psalmorum et Canticorum. Ultimi Versus Psalmorum et Canticorum secundum tonorum differentias terminentur sicut et alii.',
  'The *Glória Patri* is not said at the end of the Psalms and Canticles. The last verses of the Psalms and Canticles end according to the endings of the tones, like the others.')
NOCT = [
 ('IN I NOCTURNO', 'FIRST NOCTURN', [
  ('t01', 68, 'Zelus domus tuæ comédit me, et oppróbria exprobrántium tibi cecidérunt super me.', 'The zeal of thy house hath eaten me up, and the reproaches of them that reproached thee are fallen upon me.', 'Antiphona 1 · VIII'),
  ('t02', 69, 'Avertántur retrórsum, et erubéscant, qui cógitant mihi mala.', 'Let them be turned backward and blush for shame that desire evils to me.', 'Antiphona 2 · VIII'),
  ('t03', 70, 'Deus meus, éripe me de manu peccatóris.', 'Deliver me, O my God, out of the hand of the sinner.', 'Antiphona 3 · VIII')],
  ('v01', '{℣.} Exsúrge, Dómine. {℟.} Et júdica causam meam.', '{℣.} Arise, O Lord. {℟.} And judge my cause.')),
 ('IN II NOCTURNO', 'SECOND NOCTURN', [
  ('t04', 71, 'Liberávit Dóminus páuperem a poténte: et ínopem, cui non erat adjútor.', 'The Lord hath delivered the poor from the mighty, and the needy that had no helper.', 'Antiphona 4 · VII'),
  ('t05', 72, 'Cogitavérunt ímpii, et locúti sunt nequítiam: iniquitátem in excélso locúti sunt.', 'The wicked have thought and spoken wickedness: they have spoken iniquity on high.', 'Antiphona 5 · VIII'),
  ('t06', 73, 'Exsúrge, Dómine, et júdica causam meam.', 'Arise, O Lord, and judge my cause.', 'Antiphona 6 · I')],
  ('v02', '{℣.} Deus meus, éripe me de manu peccatóris. {℟.} Et de manu contra legem agéntis et iníqui.', '{℣.} Deliver me, O my God, out of the hand of the sinner. {℟.} And out of the hand of the transgressor of the law and of the unjust.')),
 ('IN III NOCTURNO', 'THIRD NOCTURN', [
  ('t07', 74, 'Dixi iníquis: Nolíte loqui advérsus Deum iniquitátem.', 'I said to the wicked: Speak not iniquity against God.', 'Antiphona 7 · VII'),
  ('t08', 75, 'Terra trémuit et quiévit, dum resúrgeret in judícium Deus.', 'The earth trembled and was still, when God arose in judgement.', 'Antiphona 8 · VIII'),
  ('t09', 76, 'In die tribulatiónis meæ Deum exquisívi mánibus meis.', 'In the day of my trouble I sought God with my hands.', 'Antiphona 9 · VII')],
  ('v03', '{℣.} Homo pacis meæ, in quo sperávi. {℟.} Ampliávit advérsum me supplantatiónem.', '{℣.} The man of my peace, in whom I trusted. {℟.} Hath greatly supplanted me.')),
]
PSN = {68: 'Salvum me fac, Deus', 69: 'Deus, in adjutórium', 70: 'In te, Dómine, sperávi', 71: 'Deus, judícium tuum', 72: 'Quam bonus Israël Deus', 73: 'Ut quid, Deus', 74: 'Confitébimur tibi', 75: 'Notus in Judǽa', 76: 'Voce mea ad Dóminum'}
import pieces_abl
RN = [p[1] for p in pieces_abl.P[:9]]
LECT = json.load(open('/home/claude/build/ten/lessons_h.json'))
RESP = json.load(open('/home/claude/build/ten/resp_h.json'))
for n, (h_la, h_en, ants, (vc, vla, ven)) in enumerate(NOCT):
    w('H: ' + h_la, ' = ' + h_en)
    for code, p, la, en, lab in ants:
        T('{Aña} %s {Ps. %d} %s.' % (la.split(' ')[0].rstrip(',:'), p, PSN[p]), '{Ant.} %s {Ps. %d}' % (en.split(' ')[0] + ' ' + en.split(' ')[1] + '…', p))
        ps(p, 'Psalmus %d %s' % (p, PSN[p]), 'Psalm %d' % p)
        ANT(code, la, en, lab)
    w('G: op-ten-h-%s | Versus' % vc); T(vla, ven)
    R('Dicto *Pater noster* secreto, non pronuntietur *Et ne nos,* sed facto signo a Prælato, Lector incipiat legere; et hoc etiam fiat ante quartam et septimam Lectionem. *Jube, domne,* et *Tu autem,* non dicantur, sed finita Lectione sive Lamentatione, immediate inchoëtur Responsorium.' if n == 0 else 'Pater noster, secreto.',
      'The *Pater noster* is said silently, and *Et ne nos* is not said aloud; but at a sign from the Prelate the Reader begins to read; and the same is done before the fourth and seventh Lessons. *Jube, domne,* and *Tu autem* are not said; when the Lesson or Lamentation is finished the Responsory is begun at once.' if n == 0 else 'The Our Father, silently.')
    for k in range(3):
        L = LECT[3 * n + k]; Rr = RESP[3 * n + k]
        w('L: ' + L['title'], ' = ' + L['title_en'])
        if L.get('src'): w('I: ' + L['src'], ' = ' + L['src_en'])
        if L.get('g'):
            w('G: op-ten-h-%s | Lamentatio' % L['g'])
            w('F: Textus et versio | Text and translation')
        T('^' + L['la'], L['en'])
        if L.get('g'): w('F/')
        w('L: Responsorium %s' % ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'][3 * n + k], ' = Responsory %d' % (3 * n + k + 1))
        T(Rr['la'], Rr['en'])
        w('G: op-abl-r%02d | %s' % (3 * n + k + 1, RN[3 * n + k]))
        if k == 2:
            R('Repetitur Responsorium a principio usque ad Versum.', 'The Responsory is repeated from the beginning as far as the Verse.')
R('Hoc triduo, finito IX ℟., non dicatur ℣. ante Laudes, sed statim inchoëtur in Laudibus Antiphona prima.',
  'On these three days, when the ninth Responsory is finished, no Versicle is said before Lauds, but the first Antiphon of Lauds is begun at once.')
# ---------------------------------------------------------------- Lauds
w('== Ad Laudes | Lauds', 'H: AD LAUDES', ' = LAUDS', 'S: Ecclesiasticum Officium O.P. Triduo ante Pascha (1927), pp. 31-44')
LA = [('u01', 50, 'Psalmus 50 Miserére', 'Psalm 50', 'Justificéris, Dómine, in sermónibus tuis, et vincas cum judicáris.', 'That thou mayest be justified, O Lord, in thy words, and mayest overcome when thou art judged.', 'Antiphona 1 · VIII'),
      ('u02', 89, 'Psalmus 89 Dómine, refúgium', 'Psalm 89', 'Dóminus tamquam ovis ad víctimam ductus est, et non apéruit os suum.', 'The Lord was led as a sheep to the slaughter, and he opened not his mouth.', 'Antiphona 2 · II'),
      ('u03', 62, 'Psalmus 62 Deus, Deus meus', 'Psalm 62', 'Contrítum est cor meum in médio mei: contremuérunt ómnia ossa mea.', 'My heart is broken within me; all my bones tremble.', 'Antiphona 3 · VIII'),
      ('u04', 'Canticum Moysis', 'Canticum Moysis (Exod. 15) Cantémus Dómino', 'Canticle of Moses (Exod. 15)', 'Exhortátus es in virtúte tua, et in refectióne sancta tua, Dómine.', 'Thou hast encouraged us in thy strength, and in thy holy refreshment, O Lord.', 'Antiphona 4 · IV'),
      ('u05', 148, 'Psalmus 148 Laudáte Dóminum de cælis', 'Psalm 148', 'Oblátus est, quia ipse vóluit: et peccáta nostra ipse portávit.', 'He was offered because it was his own will, and he bore our sins.', 'Antiphona 5 · II')]
for code, p, tla, ten, la, en, lab in LA:
    inc = {'u01': 'Justificéris', 'u02': 'Dóminus', 'u03': 'Contrítum est', 'u04': 'Exhortátus es', 'u05': 'Oblátus est'}[code]
    T('{Aña} %s. {%s}' % (inc, tla.split(' ', 2)[0] + ' ' + tla.split(' ', 2)[1] if code != 'u04' else 'Cant. Moysis'), '{Ant.} %s {%s}' % (en.split(',')[0].split(':')[0] + '…', ten))
    ps(p, tla, ten)
    ANT(code, la, en, lab)
R('Capitulum non dicatur, neque Hymnus, neque Versiculus; sed dum Psalmus *Laudate* dicitur, lumen, ubi videri nequeat, abscondatur; et lampades, quæ sunt per Ecclesiam, exstinguantur. Finita quinta Antiphona post *Laudate,* mox Antiphona ad *Benedictus,* ab eo, qui præest, incipiatur; et cereus, qui usque tunc solus ardens remansit, extinguatur, sicque *Benedictus,* et omnia, quæ sequuntur, in tenebris dicantur.',
  'The Chapter, Hymn and Versicle are not said; but while the Psalm *Laudate* is said, the light is hidden where it cannot be seen, and the lamps throughout the church are put out. When the fifth Antiphon after *Laudate* is finished, the one presiding at once begins the Antiphon at the *Benedictus,* and the candle that alone has remained burning until then is put out; and so the *Benedictus* and all that follows are said in darkness.')
w('L: Ad Benedictus', ' = At the Benedictus')
T('{Aña} Tráditor. {Cant. Zachariæ} Benedíctus Dóminus Deus Israël.', '{Ant.} The traitor… {Canticle of Zachary}')
ps('Canticum Zachariæ', 'Canticum Zachariæ (Luc. 1) Benedíctus', 'Canticle of Zachary (Luke 1)')
ANT('u06', 'Tráditor autem dedit eis signum, dicens: Quem osculátus fúero, ipse est, tenéte eum.', 'Now the traitor had given them a sign, saying: Whomsoever I shall kiss, that is he: hold him fast.', 'Antiphona ad Benedictus · I')
K = [('R', 'Finita Antiphona post *Benedictus,* duo Fratres stantes ante gradus Altaris cantent:', 'When the Antiphon after the *Benedictus* is finished, two brethren standing before the altar steps sing:'),
     ('G', 'k01', 'Kyrie eleison'), ('R', 'Et Choro respondente:', 'And the Choir answering:'), ('G', 'k01', 'Kyrie eleison'),
     ('R', 'Iterum illi duo Fratres cantent:', 'Again those two brethren sing:'), ('G', 'k01', 'Kyrie eleison'),
     ('R', 'Deinde alii duo Fratres stantes in medio Chori cantent:', 'Then two other brethren standing in the middle of the Choir sing:'), ('G', 'k04', 'Domine miserere'),
     ('R', 'Et Chorus respondeat:', 'And the Choir answers:'), ('G', 'k05', 'Christus Dominus factus est'),
     ('T', '{℣.} Qui passúrus advenísti propter nos.', '{℣.} Thou who camest to suffer for us.'),
     ('R', 'Fratres ante gradus cantent:', 'The brethren before the steps sing:'), ('G', 'k06', 'Qui passurus'),
     ('R', 'Chorus:', 'Choir:'), ('G', 'k07', 'Christe eleison'),
     ('T', '{℣.} Qui expánsis in cruce mánibus, traxísti ómnia ad te sǽcula.', '{℣.} Thou who, with thy hands stretched out upon the Cross, didst draw all ages to thee.'),
     ('R', 'Fratres ante gradus:', 'The brethren before the steps:'), ('G', 'k08', 'Qui expansis'),
     ('R', 'Chorus:', 'Choir:'), ('G', 'k07', 'Christe eleison'),
     ('T', '{℣.} Qui prophétice prompsísti: Ero mors tua, o mors.', '{℣.} Thou who didst say by the prophet: O death, I will be thy death.'),
     ('R', 'Fratres ante gradus:', 'The brethren before the steps:'), ('G', 'k10', 'Qui prophetice'),
     ('R', 'Chorus:', 'Choir:'), ('G', 'k07', 'Christe eleison'),
     ('R', 'Deinde duo Fratres in medio Chori cantent:', 'Then two brethren in the middle of the Choir sing:'), ('G', 'k04', 'Domine miserere'),
     ('R', 'Et Chorus respondeat:', 'And the Choir answers:'), ('G', 'k05', 'Christus Dominus factus est'),
     ('R', 'Item Fratres ante gradus cantent:', 'Again the brethren before the steps sing:'), ('G', 'k01', 'Kyrie eleison'),
     ('R', 'Et Chorus respondeat:', 'And the Choir answers:'), ('G', 'k01', 'Kyrie eleison'),
     ('R', 'Et Fratres ante gradus:', 'And the brethren before the steps:'), ('G', 'k01', 'Kyrie eleison'),
     ('R', 'Deinde duo Fratres in medio Chori cantent:', 'Then two brethren in the middle of the Choir sing:'), ('G', 'k04', 'Domine miserere'),
     ('R', 'Et Chorus respondeat:', 'And the Choir answers:'), ('G', 'k05', 'Christus Dominus factus est'),
     ('R', 'Denique duo Fratres ante gradus alta voce cantent:', 'Lastly two brethren before the steps sing in a loud voice:'), ('G', 'k19', 'Mortem autem crucis'),
     ('R', 'Interim dum hæc cantantur, Fratres stent versi ad Altare.', 'Meanwhile, while these are sung, the brethren stand turned towards the altar.')]
w('L: Kyrie', ' = Kyrie')
T('Kýrie, eléison. Dómine, miserére. Christus Dóminus factus est obédiens usque ad mortem.', 'Lord, have mercy. O Lord, have mercy. Christ the Lord became obedient unto death.')
for k in K:
    if k[0] == 'R': R(k[1], k[2])
    elif k[0] == 'T': T(k[1], k[2])
    else: w('G: op-ten-h-%s | %s' % (k[1], k[2]))
R('Finito Versu *Mortem autem crucis,* prosternant se omnes super formas, et dicant *Pater noster,* secreto, et facto signo a Prælato dicant mediocri voce alternatim Psalmum 50 *Miserére mei Deus.*',
  'When the Verse *Mortem autem crucis* is finished, all prostrate themselves on the forms and say the *Pater noster* silently, and at a sign from the Prelate they say Psalm 50 *Miserére mei Deus* alternately in a moderate voice.')
ps(50, 'Psalmus 50 Miserére', 'Psalm 50', sung=False)
R('Deinde, absque *Dóminus vobíscum,* et absque *Orémus,* dicatur:', 'Then, without *Dóminus vobíscum* and without *Orémus,* is said:')
w('L: Oratio', ' = Prayer')
T('^Réspice, quǽsumus, Dómine, super hanc famíliam tuam, pro qua Dóminus noster Jesus Christus non dubitávit mánibus tradi nocéntium, et crucis subíre torméntum.',
  'Look down, we beseech thee, O Lord, upon this thy family, for which our Lord Jesus Christ did not hesitate to be delivered into the hands of the wicked, and to undergo the torment of the Cross.')
R('Non dicatur *Qui tecum,* neque *Amen,* neque *Benedicámus Dómino,* neque *Fidélium,* sed dicto post Orationem *Pater noster,* facto signo a Prælato, surgant omnes, et lumen a Sacrista proferatur. Et sic hoc triduo Matutinum terminetur.',
  '*Qui tecum,* *Amen,* *Benedicámus Dómino* and *Fidélium* are not said; but after the Prayer the *Pater noster* is said, and at a sign from the Prelate all rise, and the light is brought out by the Sacristan. And so Matins ends on these three days.')
R('Hac die non fiant prostrationes ad Horas, propter solemnitatem Cenæ, nisi in hac Hora Laudum tantum.', 'On this day there are no prostrations at the Hours, because of the solemnity of the Supper, except at this Hour of Lauds only.')
# ---------------------------------------------------------------- the Little Hours
w('== Ad Horas | The Little Hours', 'S: Ecclesiasticum Officium O.P. Triduo ante Pascha (1927), pp. 44-56')
R('Usque ad Completorium Sabbati exclusive, non dicatur *Deus, in adjutórium,* in principio Horarum; nec *Convérte nos,* ad Completorium; nec *Glória Patri,* in fine Psalmorum et Canticorum, nisi in Vesperis Sabbati; nec Capitulum, nec Hymnus, nec ℟., nec Versiculus, nec *Dóminus vobíscum,* nec *Orémus,* nec *Qui tecum vivit,* nec *Benedicámus Dómino,* nec *Fidélium,* post Horas. More tamen solito dicatur *Pater noster.*',
  'Until Compline of Holy Saturday exclusive, *Deus, in adjutórium* is not said at the beginning of the Hours; nor *Convérte nos* at Compline; nor *Glória Patri* at the end of the Psalms and Canticles, except at Vespers of Holy Saturday; nor the Chapter, Hymn, Responsory or Versicle, nor *Dóminus vobíscum,* *Orémus,* *Qui tecum vivit,* *Benedicámus Dómino* or *Fidélium* after the Hours. But the *Pater noster* is said as usual.')
R('Antiphonæ vero *Salve Regína,* et *Pie Pater Domínice,* cum Versiculis et Orationibus in terminatione Horarum dici solitis omittantur usque ad Pascha exclusive.',
  'The antiphons *Salve Regína* and *Pie Pater Domínice,* with the Versicles and Prayers usually said at the end of the Hours, are left out until Easter exclusive.')
RESP_OR = ('^Réspice, quǽsumus, Dómine, super hanc famíliam tuam, pro qua Dóminus noster Jesus Christus non dubitávit mánibus tradi nocéntium, et crucis subíre torméntum.',
           'Look down, we beseech thee, O Lord, upon this thy family, for which our Lord Jesus Christ did not hesitate to be delivered into the hands of the wicked, and to undergo the torment of the Cross.')
CF = ('Christus factus est pro nobis obédiens usque ad mortem, mortem autem crucis.', 'Christ became obedient for us unto death, even the death of the Cross.')
def hour(h_la, h_en, pss, first=False):
    w('H: ' + h_la, ' = ' + h_en)
    R('Dicto *Pater noster,*%s postquam versis vultibus ad Altare Fratres se signaverint, inchoëtur:' % (' et *Credo in Deum,*' if first else ''),
      'When the *Pater noster*%s has been said, and the brethren, turned towards the altar, have signed themselves, there is begun:' % (' and the *Credo*' if first else ''))
    T('{Aña} Christus factus est. {Ps. %s}' % pss[0][1], '{Ant.} Christ became obedient… {Ps. %s}' % pss[0][1])
    for n, num, inc in pss: ps(n, 'Psalmus %s %s' % (num, inc), 'Psalm %s' % num)
    ANT('c01', CF[0], CF[1], 'Antiphona · VIII')
    if first: R('Dicta post Psalmos Antiphona, absque *Kýrie, eléison,* et Precibus, et sine Psalmo *Miserére,* dicatur Oratio:',
                'When the Antiphon has been said after the Psalms, without *Kýrie, eléison,* the Preces and the Psalm *Miserére,* the Prayer is said:')
    w('L: Oratio', ' = Prayer'); T(*RESP_OR)
hour('AD PRIMAM', 'PRIME', [(53, '53', 'Deus, in nómine tuo'), ('118(1-16)', '118, i', 'Beáti immaculáti'), ('118(17-32)', '118, ii', 'Retríbue servo tuo')], True)
R('*Confíteor* non dicatur usque ad Completorium Sabbati exclusive.', 'The *Confíteor* is not said until Compline of Holy Saturday exclusive.')
w('H: AD PRETIOSAM', ' = AT THE PRETIOSA')
R('Pronuntiatis Luna et quæ de Kalendario et Martyrologio pronuntianda sunt, et responso *Deo grátias,* dicatur *Pretiósa,* hoc modo:',
  'When the Moon and what is to be announced from the Calendar and the Martyrology have been read, and *Deo grátias* answered, the *Pretiósa* is said in this way:')
T('{℣.} Pretiósa est in conspéctu Dómini. {℟.} Mors sanctórum ejus.', '{℣.} Precious in the sight of the Lord. {℟.} Is the death of his saints.')
R('Oratio absque *Orémus*', 'The Prayer, without *Orémus*')
T('^Sancta María et omnes Sancti intercédant pro nobis ad Dóminum: ut mereámur adjuvári ab eo, qui vivit et regnat per ómnia sǽcula sæculórum. {℟.} Amen.',
  'May holy Mary and all the Saints intercede for us with the Lord, that we may be worthy to be helped by him who lives and reigns for ever and ever. {℟.} Amen.')
T('{℣.} Deus, in adjutórium meum inténde. {℟.} Dómine, ad adjuvándum me festína.', '{℣.} O God, come to my assistance. {℟.} O Lord, make haste to help me.')
R('Hic ℣. *Deus, in adjutórium,* cum ℟. *Dómine, ad adjuvándum,* ter dicatur. Deinde, omisso *Glória Patri,* subjungatur:',
  'Here the ℣. *Deus, in adjutórium* with the ℟. *Dómine, ad adjuvándum* is said three times. Then, the *Glória Patri* being left out, is added:')
T('Kýrie, eléison. Christe, eléison. Kýrie, eléison. Pater noster… {℣.} Et ne nos indúcas in tentatiónem. {℟.} Sed líbera nos a malo.',
  'Lord, have mercy. Christ, have mercy. Lord, have mercy. Our Father… {℣.} And lead us not into temptation. {℟.} But deliver us from evil.')
T('{℣.} Réspice, Dómine, in servos tuos, et in ópera tua, et dírige fílios eórum. {℟.} Et sit splendor Dómini Dei nostri super nos, et ópera mánuum nostrárum dírige super nos: et opus mánuum nostrárum dírige.',
  '{℣.} Look upon thy servants, O Lord, and upon thy works, and direct their children. {℟.} And let the brightness of the Lord our God be upon us, and direct thou the works of our hands over us: yea, the work of our hands do thou direct.')
R('Oratio absque *Orémus*', 'The Prayer, without *Orémus*')
T('^Dirígere et sanctificáre dignéris, Dómine sancte, Pater omnípotens, ætérne Deus, hódie corda et córpora nostra in lege tua, et in opéribus mandatórum tuórum: ut hic, et in ætérnum, te auxiliánte, semper salvi esse mereámur: Per Christum Dóminum nostrum. {℟.} Amen.',
  'Vouchsafe, O holy Lord, almighty Father, eternal God, to direct and sanctify this day our hearts and bodies in thy law and in the works of thy commandments, that here and for ever, by thy help, we may be worthy to be always saved: Through Christ our Lord. {℟.} Amen.')
T('Jube, domne, benedícere. {Benedictio} Divínum auxílium máneat semper nobíscum. {℟.} Amen.', 'Pray, father, a blessing. {Blessing} May the divine help remain with us always. {℟.} Amen.')
w('L: Evangelium', ' = Gospel')
T('^Secúndum Joánnem. Cap. 13. Ante diem festum Paschæ, sciens Jesus quia venit hora ejus ut tránseat ex hoc mundo ad Patrem: cum dilexísset suos, qui erant in mundo, in finem diléxit eos. Tu autem, Dómine, miserére nostri. {℟.} Deo grátias.',
  'According to John, chapter 13. Before the festival day of the Pasch, Jesus, knowing that his hour was come that he should pass out of this world to the Father, having loved his own who were in the world, he loved them unto the end. But thou, O Lord, have mercy on us. {℟.} Thanks be to God.')
R('Commemoratio Fratrum, Sororum, Familiarium, Benefactorum defunctorum Ordinis nostri.', 'Commemoration of the departed brethren, sisters, familiars and benefactors of our Order.')
T('Requiéscant in pace. {℟.} Amen.', 'May they rest in peace. {℟.} Amen.')
T('{Ps. 116} Laudáte Dóminum, omnes gentes: * laudáte eum, omnes pópuli. Quóniam confirmáta est super nos misericórdia ejus: * et véritas Dómini manet in ætérnum.',
  '{Ps. 116} O praise the Lord, all ye nations: praise him, all ye people. For his mercy is confirmed upon us: and the truth of the Lord remaineth for ever.')
R('Deinde, omisso *Glória Patri,* sequitur:', 'Then, the *Glória Patri* being left out, there follows:')
T('{℣.} Osténde nobis, Dómine, misericórdiam tuam. {℟.} Et salutáre tuum da nobis. {℣.} Dóminus vobíscum. {℟.} Et cum spíritu tuo. Orémus.',
  '{℣.} Show us, O Lord, thy mercy. {℟.} And grant us thy salvation. {℣.} The Lord be with you. {℟.} And with thy spirit. Let us pray.')
w('L: Oratio', ' = Prayer')
T('^Actiónes nostras, quǽsumus, Dómine, aspirándo prǽveni et adjuvándo proséquere: ut cuncta nostra operátio a te semper incípiat, et per te cœpta finiátur. Per Christum Dóminum nostrum. {℟.} Amen.',
  'Go before our actions, we beseech thee, O Lord, by thy inspiration, and further them by thy help, that every work of ours may always begin with thee, and through thee be ended. Through Christ our Lord. {℟.} Amen.')
T('{℣.} Adjutórium nostrum in nómine Dómini. {℟.} Qui fecit cælum et terram.', '{℣.} Our help is in the name of the Lord. {℟.} Who made heaven and earth.')
R('Non dicatur *Fidélium ánimæ.*', '*Fidélium ánimæ* is not said.')
hour('AD TERTIAM', 'TERCE', [('118(33-48)', '118, iii', 'Legem pone'), ('118(49-64)', '118, iv', 'Memor esto'), ('118(65-80)', '118, v', 'Bonitátem fecísti')])
hour('AD SEXTAM', 'SEXT', [('118(81-96)', '118, vi', 'Defécit'), ('118(97-112)', '118, vii', 'Quómodo diléxi'), ('118(113-128)', '118, viii', 'Iníquos ódio hábui')])
hour('AD NONAM', 'NONE', [('118(129-144)', '118, ix', 'Mirabília'), ('118(145-160)', '118, x', 'Clamávi'), ('118(161-176)', '118, xi', 'Príncipes')])
R('Fratres privatas Missas non celebrent, sed omnes in Missa conventuali communicent. Sacrista vero ante Nonam omnia altaria detegat, præter majus, (quod dum Vesperæ cantantur detegatur, una sola mappa super ipsum usque post finem Missæ relicta, qua finita removeatur) et usque ad horam Tertiam Sabbati sequentis detecta remaneant, præter majus, quod in crastino hora Officii cooperiatur.',
  'The brethren do not celebrate private Masses, but all receive Communion at the conventual Mass. Before None the Sacristan strips all the altars except the high altar (which is stripped while Vespers are sung, a single cloth being left on it until after the end of the Mass, and removed when the Mass is over); and they remain bare until the hour of Terce on the following Saturday, except the high altar, which is covered on the morrow at the time of the Office.')
open('/home/claude/dominican-liturgy/tools/hw39/Quad6h_ten.src', 'w').write('\n'.join(out) + '\n')
import subprocess
print(subprocess.run(['node', '/home/claude/build/ten/gen_ps.js'], input=json.dumps(PSPEC, ensure_ascii=False), capture_output=True, text=True))
print(len(out))
