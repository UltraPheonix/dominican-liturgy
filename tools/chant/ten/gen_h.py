# Feria V in Cena Domini: Matins (Tenebrae) and Lauds from the Triduum book O.P. (1927) -> tools/hw39/Quad6h_ten.src
import psalms, json
out = []
def w(*l): out.extend(l)
def T(la, en): w('T: ' + la, ' = ' + en)
def R(la, en): w('R: ' + la, ' = ' + en)
def ps(n, title_la, title_en):
    w('F: %s | %s' % (title_la, title_en))
    for la, en in psalms.psalm(n): T(la, en)
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
  ('t04', 71, 'Liberávit Dóminus páuperem a poténte: et ínopem, cui non erat adjútor.', 'The Lord hath delivered the poor from the mighty, and the needy that had no helper.', 'Antiphona 4 · VIII'),
  ('t05', 72, 'Cogitavérunt ímpii, et locúti sunt nequítiam: iniquitátem in excélso locúti sunt.', 'The wicked have thought and spoken wickedness: they have spoken iniquity on high.', 'Antiphona 5 · VIII'),
  ('t06', 73, 'Exsúrge, Dómine, et júdica causam meam.', 'Arise, O Lord, and judge my cause.', 'Antiphona 6')],
  ('v02', '{℣.} Deus meus, éripe me de manu peccatóris. {℟.} Et de manu contra legem agéntis et iníqui.', '{℣.} Deliver me, O my God, out of the hand of the sinner. {℟.} And out of the hand of the transgressor of the law and of the unjust.')),
 ('IN III NOCTURNO', 'THIRD NOCTURN', [
  ('t07', 74, 'Dixi iníquis: Nolíte loqui advérsus Deum iniquitátem.', 'I said to the wicked: Speak not iniquity against God.', 'Antiphona 7 · VIII'),
  ('t08', 75, 'Terra trémuit et quiévit, dum resúrgeret in judícium Deus.', 'The earth trembled and was still, when God arose in judgement.', 'Antiphona 8 · VIII'),
  ('t09', 76, 'In die tribulatiónis meæ Deum exquisívi mánibus meis.', 'In the day of my trouble I sought God with my hands.', 'Antiphona 9 · VIII')],
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
LA = [('u01', 50, 'Psalmus 50 Miserére', 'Psalm 50', 'Justificéris, Dómine, in sermónibus tuis, et vincas cum judicáris.', 'That thou mayest be justified, O Lord, in thy words, and mayest overcome when thou art judged.', 'Antiphona 1'),
      ('u02', 89, 'Psalmus 89 Dómine, refúgium', 'Psalm 89', 'Dóminus tamquam ovis ad víctimam ductus est, et non apéruit os suum.', 'The Lord was led as a sheep to the slaughter, and he opened not his mouth.', 'Antiphona 2'),
      ('u03', 62, 'Psalmus 62 Deus, Deus meus', 'Psalm 62', 'Contrítum est cor meum in médio mei: contremuérunt ómnia ossa mea.', 'My heart is broken within me; all my bones tremble.', 'Antiphona 3'),
      ('u04', 'Canticum Moysis', 'Canticum Moysis (Exod. 15) Cantémus Dómino', 'Canticle of Moses (Exod. 15)', 'Exhortátus es in virtúte tua, et in refectióne sancta tua, Dómine.', 'Thou hast encouraged us in thy strength, and in thy holy refreshment, O Lord.', 'Antiphona 4'),
      ('u05', 148, 'Psalmus 148 Laudáte Dóminum de cælis', 'Psalm 148', 'Oblátus est, quia ipse vóluit: et peccáta nostra ipse portávit.', 'He was offered because it was his own will, and he bore our sins.', 'Antiphona 5')]
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
ps(50, 'Psalmus 50 Miserére', 'Psalm 50')
R('Deinde, absque *Dóminus vobíscum,* et absque *Orémus,* dicatur:', 'Then, without *Dóminus vobíscum* and without *Orémus,* is said:')
w('L: Oratio', ' = Prayer')
T('^Réspice, quǽsumus, Dómine, super hanc famíliam tuam, pro qua Dóminus noster Jesus Christus non dubitávit mánibus tradi nocéntium, et crucis subíre torméntum.',
  'Look down, we beseech thee, O Lord, upon this thy family, for which our Lord Jesus Christ did not hesitate to be delivered into the hands of the wicked, and to undergo the torment of the Cross.')
R('Non dicatur *Qui tecum,* neque *Amen,* neque *Benedicámus Dómino,* neque *Fidélium,* sed dicto post Orationem *Pater noster,* facto signo a Prælato, surgant omnes, et lumen a Sacrista proferatur. Et sic hoc triduo Matutinum terminetur.',
  '*Qui tecum,* *Amen,* *Benedicámus Dómino* and *Fidélium* are not said; but after the Prayer the *Pater noster* is said, and at a sign from the Prelate all rise, and the light is brought out by the Sacristan. And so Matins ends on these three days.')
R('Hac die non fiant prostrationes ad Horas, propter solemnitatem Cenæ, nisi in hac Hora Laudum tantum.', 'On this day there are no prostrations at the Hours, because of the solemnity of the Supper, except at this Hour of Lauds only.')
open('/home/claude/dominican-liturgy/tools/hw39/Quad6h_ten.src', 'w').write('\n'.join(out) + '\n')
print(len(out))
