"""Builds Quad6s.src (Holy Saturday, Missale O.P. 1939 pp. 179-191) from the cleaned draft pieces
(sat_parts.py: Exsultet + Litany; sat_parts2.py: lessons, tracts, Epistle, Gospel; s.txt: draft lines)."""
import re, os
P = eval(open('sat_parts.py').read()); Q = eval(open('sat_parts2.py').read())
S = open('s.txt').read().split('\n')
BK = os.listdir('/home/claude/build/site/bible/en')
def B(name): return [b[:-4] for b in BK if b.lower().startswith(name.lower())][0]
def verses(book, a, b):
    c0, v0 = map(int, a.split(':')); c1, v1 = map(int, b.split(':')); out = []
    for l in open('/home/claude/build/site/bible/en/%s.txt' % book, encoding='utf8'):
        c, v, t = l.rstrip('\n').split('\t', 2); c, v = int(c), int(v)
        if (c0, v0) <= (c, v) <= (c1, v1): out.append(t)
    return ' '.join(out)
DOE = open('/home/claude/src/do/web/www/missa/English/Tempora/Quad6-6.txt').read().split('\n')
ex1e = DOE[47][3:].strip(); ex2e = DOE[55][3:].strip()
ex3e = DOE[64][3:].strip().replace('our Bishop N....', 'our Bishop N., and also our most glorious Emperor N. (or King, or Duke)')
T = []
def t(tag, la, en): T.append('%s: %s\n = %s' % (tag, la, en))
def c(p, i): T.append('C: %s %d' % (p, i))
T.append('# Missale O.P. (1939), pp. 179–191: Sabbato Sancto.\n== Benedictio ignis et Cerei | The blessing of the fire and of the Candle')
t('H', 'SABBATO SANCTO PASCHÆ', 'HOLY SATURDAY')
t('I', 'Statio ad S. Joannem in Laterano', 'Station at St John Lateran')
t('R', '^DICTA Nona, Prior cum cappa serica, et Diaconus, qui benedicturus est Cereum, cum Missali, et Subdiaconus cum libro Evangeliorum, præcedentibus Ceroferariis in albis cum cereis non accensis, ad presbyterium veniant. Deinde Prior stans ante gradus presbyterii, verso vultu ad altare, Diacono coram ipso tenente Missale, et Sacrista, vel alio, cui ipse injunxerit, ad dexteram ejus tenente patellam cum carbonibus ignitis, absque *Dóminus vobíscum,* et absque *Orémus,* legendo sine nota, benedicat ignem hoc modo.',
  'When None has been said, the Prior in a silk cope, the Deacon who is to bless the Candle, with the Missal, and the Subdeacon with the book of the Gospels, preceded by the candle-bearers in albs with unlit candles, come to the presbytery. Then the Prior, standing before the steps of the presbytery facing the altar, the Deacon holding the Missal before him, and the Sacristan, or another whom he has charged, holding at his right a pan of burning coals, without *Dóminus vobíscum* and without *Orémus,* reading without chant, blesses the fire in this way.')
t('T', '^DOMINE sancte, Pater omnípotens, ætérne Deus, bene{✠}dícere, et sanctificáre dignéris ignem istum, quem nos indígni per invocatiónem unigéniti Fílii tui Dómini nostri Jesu Christi benedícere præsúmimus : tu clementíssime eum tua benedictióne sanctífica, et ad proféctum humáni géneris proveníre concéde. Per eúmdem Christum.',
  'O holy Lord, almighty Father, eternal God, vouchsafe to {✠} bless and sanctify this fire, which we, though unworthy, presume to bless by calling upon Your only-begotten Son our Lord Jesus Christ; most merciful, sanctify it with Your blessing, and grant that it may be for the good of mankind. Through the same Christ.')
t('R', 'Finita benedictione, aspergat ignem aqua benedicta. Deinde candela de igne benedicto accendatur. Patella vero cum carbonibus accensis in presbyterio dimittatur, donec cereus benedicendus accensus fuerit; ut si candela fuerit exstincta, eodem igne possit reaccendi. Diaconus vero, assumpto a Subdiacono libro Evangeliorum, et accepta benedictione a Priore dicente : *In nómine Patris, et Fílii, et Spíritus Sancti. Amen,* stante a dextris ejus Subdiacono cum candela de igne benedicto accensa, et Ceroferariis astantibus a dextris et a sinistris cum cereis non accensis, (qui omnes stent versis vultibus ad altare) Cereum benedicat. Prior autem, dum Cereus benedicitur, stet ad cornu Epistolæ, sicut ad Evangelium consuevit stare in Missa solemni. Sacrista vero, vel alius frater, cui ipse innuerit, stet post Subdiaconum, tenens quinque grana incensi, Cereo infigenda.',
  'The blessing finished, he sprinkles the fire with holy water. Then a candle is lit from the blessed fire. The pan with the burning coals is left in the presbytery until the candle to be blessed has been lit, so that if the candle goes out it can be relit from the same fire. The Deacon, having taken the book of the Gospels from the Subdeacon and received the blessing from the Prior, who says: *In nómine Patris, et Fílii, et Spíritus Sancti. Amen,* blesses the Candle, the Subdeacon standing on his right with the candle lit from the blessed fire, and the candle-bearers standing on the right and left with unlit candles (all facing the altar). While the Candle is blessed, the Prior stands at the Epistle corner, as he usually stands at the Gospel in a solemn Mass. The Sacristan, or another brother at his sign, stands behind the Subdeacon holding the five grains of incense to be fixed in the Candle.')
t('L', 'Benedictio Cerei', 'The blessing of the Candle')
t('T', '^' + P['ex1'].replace('Fratres caríssimi', 'fratres caríssimi'), ex1e)
t('T', '^' + P['ex2a'].replace(' R. ', ' {℟.} '), 'World without end. {℟.} Amen. The Lord be with you. {℟.} And with your spirit. Lift up your hearts. {℟.} We have lifted them up to the Lord. Let us give thanks to the Lord our God. {℟.} It is meet and just. ' + ex2e)
t('R', 'Hic imprimatur unum granum incensi a Diacono in Cereo : reliqua quatuor ab eo, qui tenuit grana incensi.', 'Here one grain of incense is fixed in the Candle by the Deacon; the other four by the one who held the grains of incense.')
t('T', P['ex2b'], 'Wherefore, in the grace of this night, receive, O holy Father, the evening sacrifice of this incense, which holy Church renders to You by the hands of Your ministers in the solemn offering of this wax candle, made out of the work of bees. Now also we know the praises of this pillar, which the shining fire enkindles to the honour of God.')
t('R', 'Hic accenditur Cereus ab eo, qui grana incensi tenuit, cum candela accensa de igne benedicto, quam tenuit Subdiaconus.', 'Here the Candle is lit by the one who held the grains of incense, with the candle lit from the blessed fire, which the Subdeacon held.')
t('T', 'Qui licet sit divísus in partes,', 'Which fire, though divided into parts,')
t('R', 'Hic cerei Acolythorum eadem candela accendantur', 'Here the Acolytes’ candles are lit from the same candle')
t('T', 'mutuáti tamen lúminis detriménta non novit. Alitur enim liquántibus ceris, quas in substántiam pretiósæ hujus lampadis', 'suffers no loss from its light being borrowed. For it is fed by the melting wax, which for the substance of this precious lamp')
t('R', 'Hic accendantur lampades ecclesiæ cum eadem candela', 'Here the lamps of the church are lit from the same candle')
t('T', P['ex3'], 'the mother bee produced. ' + ex3e + ' {℟.} Amen.')
t('R', 'Completa benedictione Cerei, Prior cum ministris in sacristiam revertatur, et deposita cappa serica, assumpta casula, dum legitur prima Lectio, cum ministris more solito procedens ad altare, cum pervenerit ante illud, non dicat *In nómine Patris,* nec *Confíteor,* sed inclinans, sessum eat in presbyterio, et Acolythi depositis candelabris (quorum candelæ per totam Missam debent esse accensæ) venient ad audiendas cum aliis ministris Lectiones, Acolytho seniore tenente Missale coram Priore, qui sedens legat illas submissa voce. Quatuor Lectiones sequentes legantur sine titulo in superpelliceis in loco, in quo Epistola ferialibus diebus legi solet.',
  'When the blessing of the Candle is completed, the Prior returns with the ministers to the sacristy and, having put off the silk cope and put on the chasuble, goes to the altar with the ministers in the usual way while the first Lesson is read; when he arrives before it, he does not say *In nómine Patris* nor *Confíteor,* but, bowing, goes to sit in the presbytery; and the Acolytes, having set down their candlesticks (whose candles must remain lit throughout the Mass), come with the other ministers to hear the Lessons, the senior Acolyte holding the Missal before the Prior, who, seated, reads them in a low voice. The four following Lessons are read without title, in surplices, in the place where the Epistle is usually read on ferial days.')
T.append('\n== Lectiones | The Lessons')
LES = [
 ('Lectio prima | Gen. 1 et 2', 'First Lesson | Gen. 1 and 2', 'les1', 'Genesis', '1:1', '2:2', None,
  'DEUS, qui mirabíliter creásti hóminem, et mirabílius redemísti : da nobis, quǽsumus, contra oblectaménta peccáti mentis ratióne persístere; ut mereámur ad gáudia ætérna perveníre : Per Dóminum.',
  'O God, who wonderfully created man and more wonderfully redeemed him, grant us, we beseech You, to stand firm by reason of mind against the allurements of sin, that we may deserve to attain to everlasting joys: through our Lord.'),
 ('Lectio secunda | Exod. 14 et 15', 'Second Lesson | Exod. 14 and 15', 'les2', 'Exodus', '14:24', '15:1',
  ('tr1', 'Tractus Exod. 15', 'Tract Exod. 15', 0, 'Let us sing to the Lord, for He is gloriously magnified: the horse and the rider He has thrown into the sea; He is become my helper and protector unto salvation. This is my God, and I will honour Him: the God of my father, and I will exalt Him. {℣.} The Lord is as a man of war: the Lord is His name.'),
  'DEUS, cujus antíqua mirácula étiam nostris sǽculis coruscáre sentímus : præsta, quǽsumus, ut sicut priórem pópulum ab Ægýptiis liberásti; hoc ad salútem Géntium per aquas baptísmatis operéris : Per Dóminum.',
  'O God, whose wonders of old we perceive shining even in our own days, grant, we beseech You, that as You delivered the former people from the Egyptians, so You may work this for the salvation of the nations through the waters of baptism: through our Lord.'),
 ('Lectio tertia | Isai. 4', 'Third Lesson | Isa. 4', 'les3', 'Isaias', '4:1', '4:6',
  ('tr2', 'Tractus Isai. 5', 'Tract Isa. 5', 1, 'My beloved had a vineyard on a hill in a fruitful place. {℣.} And he fenced it in, and dug about it, and planted it with the choicest vines, and built a tower in the midst of it. {℣.} And set up a winepress therein; for the vineyard of the Lord of hosts is the house of Israel.'),
  'DEUS, qui nos ad celebrándum Paschále sacraméntum utriúsque testaménti páginis ínstruis : da nobis intellígere misericórdiam tuam; ut ex perceptióne præséntium múnerum firma sit exspectátio futurórum : Per Dóminum.',
  'O God, who by the pages of both Testaments instruct us to celebrate the Paschal mystery, grant us to understand Your mercy, that from the receiving of present gifts our expectation of those to come may be made firm: through our Lord.'),
 ('Lectio quarta | Isai. 54 et 55', 'Fourth Lesson | Isa. 54 and 55', 'les4', 'Isaias', '54:17', '55:11', None,
  'DEUS, qui Ecclésiam tuam semper Géntium vocatióne multíplicas : concéde propítius, ut quos aqua baptísmatis ábluis; contínua protectióne tueáris : Per Dóminum.',
  'O God, who ever multiply Your Church by the calling of the nations, mercifully grant that You may guard with continual protection those whom You wash with the water of baptism: through our Lord.')]
for la, en, k, book, a, b, tr, orla, oren in LES:
    t('L', la, en); t('T', '^' + Q[k], verses(B(book), a, b))
    if tr:
        t('T', '{%s} %s' % (tr[1], Q[tr[0]]), '{%s} %s' % (tr[2], tr[4])); c('tr', tr[3])
    if k == 'les4':
        t('T', '{Tractus Ps. 41} ' + Q['tr3'], '{Tract Ps. 41} As the hart pants after the fountains of water, so my soul pants after You, O God. {℣.} My soul has thirsted for the living God; when shall I come and appear before the face of God? {℣.} My tears have been my bread day and night, while they say to me daily: Where is your God?'); c('tr', 2)
    if k == 'les1':
        t('R', 'Quinque Orationes sequentes ad altare in cornu Epistolæ dicantur, sine *Dóminus vobíscum,* et sine *Flectámus génua,* præmisso *Orémus.*', 'The five following Orations are said at the altar at the Epistle corner, without *Dóminus vobíscum* and without *Flectámus génua,* *Orémus* being said first.')
    t('T', 'Orémus.', 'Let us pray.'); t('L', 'Oratio', 'Prayer'); t('T', '^' + orla, oren)
t('T', 'Orémus.', 'Let us pray.'); t('L', 'Oratio', 'Prayer')
t('T', '^CONCEDE, quǽsumus omnípotens Deus : ut qui festa Paschália ágimus; cæléstibus desidériis accénsi fontem vitæ sitiámus : Per Dóminum.', 'Grant, we beseech You, almighty God, that we who keep the Paschal feast, inflamed with heavenly desires, may thirst for the fountain of life: through our Lord.')
T.append('\n== Litaniæ | The Litany')
t('R', 'Deinde sequuntur Litaniæ', 'Then follows the Litany')
t('T', '^' + P['lit'], P['lit_en'])
T.append('\n== Ad Missam | The Mass')
t('R', 'Finitis Litaniis, Sacerdos cum ministris ad altare accedens, incipiat Missam more solito, et facta confessione, ac dicta Oratione solita ante altare, eoque osculato, dicat *Kyrie eléison,* quibus a Choro finitis, intonet solemniter *Glória in excélsis Deo.* Quo finito, dicat *Dóminus vobíscum.*',
  'When the Litany is finished, the Priest with the ministers goes to the altar and begins the Mass in the usual way; and the confession having been made, and the usual Oration said before the altar, and the altar kissed, he says *Kyrie eléison;* when the Choir has finished it, he solemnly intones *Glória in excélsis Deo.* When this is finished, he says *Dóminus vobíscum.*')
T.append('X: start, ky, gl')
t('T', 'Orémus.', 'Let us pray.'); t('L', 'Oratio', 'Collect')
t('T', '^DEUS, qui hanc sacratíssimam noctem glória Domínicæ resurrectiónis illústras : consérva in nova famíliæ tuæ progénie adoptiónis spíritum, quem dedísti; ut córpore et mente renováti, puram tibi exhíbeant servitútem : Per eúmdem.', 'O God, who make this most sacred night illustrious by the glory of the Lord’s resurrection, preserve in the new offspring of Your family the spirit of adoption which You have given, that, renewed in body and mind, they may render You a pure service: through the same Lord.')
t('T', '{L}éctio Epístolæ beáti Pauli Apóstoli ad Colossénses. {c. 3}', 'The Lesson from the Epistle of blessed Paul the Apostle to the Colossians. {Ch. 3}')
t('T', '^' + Q['epi'].replace('Fratres', 'FRATRES', 1), 'Brethren: If you be risen with Christ, seek the things that are above, where Christ is sitting at the right hand of God. Mind the things that are above, not the things that are upon the earth. For you are dead, and your life is hid with Christ in God. When Christ shall appear, who is your life, then you also shall appear with Him in glory.')
t('T', Q['all'], 'Alleluia, alleluia. {℣. Ps. 106} Give praise to the Lord, for He is good: for His mercy endures for ever.'); c('al', 0)
t('R', 'Non repetatur *Allelúia.*', 'The *Allelúia* is not repeated.')
t('T', '{Tractus Ps. 116} ' + Q['trm'], '{Tract Ps. 116} O praise the Lord, all you nations; and praise Him, all you peoples. {℣.} For His mercy is confirmed upon us, and the truth of the Lord remains for ever.'); c('tr', 3)
t('R', 'Ad Evangelium cerei non deferantur, sed tantum thus : petatur benedictio, et alia fiant ut moris est.', 'At the Gospel candles are not carried, but only incense; the blessing is asked, and the rest is done as usual.')
T.append('X: gospel')
t('T', '{✠ S}equéntia sancti Evangélii secúndum Matthǽum. {c. 28}', '{✠} The continuation of the holy Gospel according to Matthew. {Ch. 28}')
t('T', '^' + Q['gos'], verses(B('Matth'), '28:1', '28:7'))
t('R', 'Non dicatur *Credo,* nec Offertorium, sed tantum *Dóminus vobíscum. Orémus.* Dicto *Orémus,* statim Diaconus offerat calicem Sacerdoti. Qui facta oblatione, et thurificato altari, ac ablutis digitis more solito, vertens se ad Conventum, seu populum dicat *Oráte fratres,* et postea Secretam, quæ hic sequitur.', 'The *Credo* is not said, nor the Offertory, but only *Dóminus vobíscum. Orémus.* When *Orémus* has been said, the Deacon at once offers the chalice to the Priest; who, having made the oblation, incensed the altar and washed his fingers in the usual way, turns to the Community or the people and says *Oráte fratres,* and then the Secret, which follows here.')
T.append('X: offer, offertory')
t('L', 'Secreta', 'Secret')
t('T', '^SUSCIPE, quǽsumus Dómine, preces pópuli tui cum oblatiónibus hostiárum : ut Paschálibus initiáta mystériis, ad æternitátis nobis medélam, te operánte, profíciant. Per Dóminum.', 'Receive, we beseech You, O Lord, the prayers of Your people together with the offerings of these victims, that what has been begun by the Paschal mysteries may, by Your working, avail us as a healing remedy for eternity: through our Lord.')
t('R', 'Præfatio *Te quidem Dómine omni témpore, sed in hac potíssimum nocte.*', 'Preface *Te quidem Dómine omni témpore, sed in hac potíssimum nocte* (of Easter).')
T.append('X: offertoryEnd, pref')
t('R', 'Deinde dicatur : *Sanctus.*', 'Then the *Sanctus* is said.')
T.append('X: sa')
t('L', 'Infra Canonem', 'Within the Canon')
t('T', '^C' + S[70][2:], 'In the unity of holy fellowship, and celebrating the most sacred night of the Resurrection of our Lord Jesus Christ according to the flesh; and also honouring in the first place the memory of the ever-glorious Virgin Mary, Mother of the same our God and Lord Jesus Christ; as also of Your blessed Apostles and Martyrs Peter and Paul, Andrew, James, John, Thomas, James, Philip, Bartholomew, Matthew, Simon and Thaddeus; Linus, Cletus, Clement, Xystus, Cornelius, Cyprian, Lawrence, Chrysogonus, John and Paul, Cosmas and Damian, and of all Your Saints; by whose merits and prayers grant that we may in all things be defended by the help of Your protection. Through the same Christ our Lord. Amen.')
t('R', 'Item', 'Likewise')
hanc = S[72][2:]; hanc = 'H' + hanc[:hanc.index(' ⟦Postea')]
t('T', '^' + hanc, 'We therefore beseech You, O Lord, graciously to accept this oblation of our service, and that of all Your household, which we offer You also for those whom You have vouchsafed to bring to a new birth by water and the Holy Spirit, granting them remission of all their sins; and to order our days in Your peace, and to command that we be delivered from eternal damnation and numbered in the flock of Your elect. Through Christ our Lord. Amen.')
T.append('X: canonNoAg')
t('R', 'Postea dicente Sacerdote *Pax Dómini,* respondeatur *Et cum spíritu tuo,* sed *Agnus Dei* non dicatur, nec pax detur; sed incipiatur ad Vesperas Antiphona :', 'Afterwards, when the Priest says *Pax Dómini,* *Et cum spíritu tuo* is answered; but the *Agnus Dei* is not said, nor is the pax given; but at Vespers the Antiphon is begun:')
T.append('\n== Ad Vesperas | Vespers')
t('T', '{Aña} Allelúia, allelúia, allelúia.', '{Ant.} Alleluia, alleluia, alleluia.'); c('an', 0)
t('R', 'quæ tota dicatur ante Psalmum 116 *Laudáte Dóminum omnes gentes,* et *Glória Patri.* Repetita Antiphona post Psalmum, Sacerdos ad altare, Cantore ei deferente, incipiat ad *Magníficat* Antiphonam', 'which is said in full before Psalm 116 *Laudáte Dóminum omnes gentes,* and the *Glória Patri.* When the Antiphon has been repeated after the Psalm, the Priest at the altar, the Cantor bringing it to him, begins the Antiphon at the *Magníficat:*')
t('T', '{Aña} Véspere autem sábbati, quæ lucéscit in prima sábbati, venit María Magdaléne, et áltera María vidére sepúlcrum, allelúia.', '{Ant.} And in the end of the sabbath, when it began to dawn towards the first day of the week, came Mary Magdalen and the other Mary to see the sepulchre, alleluia.'); c('an', 1)
t('R', 'Dicitur tota ante Canticum *Magníficat.* Deinde illa repetita, et finita post *Magníficat,* Sacerdos conversus ad populum, seu Conventum dicat *Dóminus vobíscum,* et reversus ad librum, prosequatur *Orémus.*', 'It is said in full before the Canticle *Magníficat.* Then, when it has been repeated and finished after the *Magníficat,* the Priest, turning to the people or the Community, says *Dóminus vobíscum,* and returning to the book continues *Orémus.*')
t('L', 'Postcommunio', 'Postcommunion')
t('T', '^SPIRITUM nobis, Dómine, tuæ caritátis infúnde : ut quos sacraméntis Paschálibus satiásti; tua fácias pietáte concórdes : Per Dóminum.', 'Pour forth upon us, O Lord, the Spirit of Your love, that those whom You have filled with the Paschal sacraments may by Your goodness be of one mind: through our Lord.')
t('R', 'Postea convertat se iterum Sacerdos ad populum, et dicat *Dóminus vobíscum.* Et Diaconus subjungat *Ite missa est, allelúia, allelúia.* Deinde dicta Oratione *Pláceat tibi,* det benedictionem, et dicat Evangelium *In princípio,* et sic Missa simul, ac Vesperæ finiantur.', 'Afterwards the Priest turns again to the people and says *Dóminus vobíscum.* And the Deacon adds *Ite missa est, allelúia, allelúia.* Then, the Oration *Pláceat tibi* having been said, he gives the blessing and says the Gospel *In princípio;* and so the Mass and Vespers end together.')
T.append('X: end')
s = '\n'.join(T) + '\n'
s = re.sub(r'⟦([^⟧]*)⟧\{[^}]*\}', r'\1', s); s = re.sub(r'⟦([^⟧]*)⟧', r'\1', s)
open('Quad6s.src', 'w').write(s); print(len(s))
