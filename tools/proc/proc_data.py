# Processionarium juxta ritum S. Ordinis Praedicatorum (ed. Cormier, Rome 1913), read from the CMAA scan
# (media.churchmusicassociation.org/dominican/processionarium-1913-Cormier.pdf; pdf page = printed page + 15).
# Items: ('rub', la, en) rubric; ('txt', la, en) sung or said text; ('scan', [pages]) the notation as printed;
# ('lit', [(la, resp_la, en, resp_en), ...]) invocations of a litany; ('h', la, en) a heading inside a section.
ORA = ('ora pro nobis.', 'pray for us.')
ORATE = ('oráte pro nobis.', 'pray for us.')
def saints(names, plural=False):
    r = ORATE if plural else ORA
    return [(n, r[0], e, r[1]) for n, e in names]
LIT_SANCT = [
 ('Kýrie, eléison.', 'Kýrie, eléison.', 'Lord, have mercy.', 'Lord, have mercy.'),
 ('Christe, eléison.', 'Christe, eléison.', 'Christ, have mercy.', 'Christ, have mercy.'),
 ('Kýrie, eléison.', 'Kýrie, eléison.', 'Lord, have mercy.', 'Lord, have mercy.'),
 ('Christe, audi nos.', 'Christe, exáudi nos.', 'Christ, hear us.', 'Christ, graciously hear us.'),
 ('Pater de cælis, Deus,', 'miserére nobis.', 'God the Father of heaven,', 'have mercy on us.'),
 ('Fili, Redémptor mundi, Deus,', 'miserére nobis.', 'God the Son, Redeemer of the world,', 'have mercy on us.'),
 ('Spíritus Sancte, Deus,', 'miserére nobis.', 'God the Holy Ghost,', 'have mercy on us.'),
 ('Sancta Trínitas, unus Deus,', 'miserére nobis.', 'Holy Trinity, one God,', 'have mercy on us.'),
] + saints([('Sancta María,', 'Holy Mary,'), ('Sancta Dei Génitrix,', 'Holy Mother of God,'), ('Sancta Virgo vírginum,', 'Holy Virgin of virgins,'),
            ('Sancte Míchaël,', 'St Michael,'), ('Sancte Gábriel,', 'St Gabriel,'), ('Sancte Ráphaël,', 'St Raphael,')]) + saints([
            ('Omnes sancti Ángeli et Archángeli,', 'All ye holy Angels and Archangels,'), ('Omnes sancti beatórum Spirítuum órdines,', 'All ye holy orders of blessed Spirits,')], True) + saints([
            ('Sancte Joánnes Baptísta,', 'St John the Baptist,'), ('Sancte Joseph,', 'St Joseph,')]) + saints([
            ('Omnes sancti Patriárchæ et Prophétæ,', 'All ye holy Patriarchs and Prophets,')], True) + saints([
            ('Sancte Petre,', 'St Peter,'), ('Sancte Paule,', 'St Paul,'), ('Sancte Andréa,', 'St Andrew,'), ('Sancte Jacóbe,', 'St James,'), ('Sancte Joánnes,', 'St John,'),
            ('Sancte Thoma,', 'St Thomas,'), ('Sancte Jacóbe,', 'St James,'), ('Sancte Philíppe,', 'St Philip,'), ('Sancte Bartholomǽe,', 'St Bartholomew,'), ('Sancte Matthǽe,', 'St Matthew,'),
            ('Sancte Simon,', 'St Simon,'), ('Sancte Thaddǽe,', 'St Thaddeus,'), ('Sancte Mathía,', 'St Matthias,'), ('Sancte Bárnaba,', 'St Barnabas,'), ('Sancte Marce,', 'St Mark,'), ('Sancte Luca,', 'St Luke,')]) + saints([
            ('Omnes sancti Discípuli Dómini,', 'All ye holy Disciples of the Lord,'), ('Omnes sancti Innocéntes,', 'All ye holy Innocents,')], True) + saints([
            ('Sancte Stéphane,', 'St Stephen,'), ('Sancte Clemens,', 'St Clement,'), ('Sancte Cornéli,', 'St Cornelius,'), ('Sancte Cypriáne,', 'St Cyprian,'), ('Sancte Laurénti,', 'St Lawrence,'),
            ('Sancte Vincénti,', 'St Vincent,'), ('Sancte Diónysi cum sóciis tuis,', 'St Denis, with thy companions,'), ('Sancte Mauríti cum sóciis tuis,', 'St Maurice, with thy companions,'),
            ('Sancte Januári cum sóciis tuis,', 'St Januarius, with thy companions,')]) + saints([('Sancti Fabiáne et Sebastiáne,', 'Sts Fabian and Sebastian,'), ('Sancti Cosma et Damiáne,', 'Sts Cosmas and Damian,')], True) + saints([
            ('Sancte Thoma,', 'St Thomas,'), ('Sancte Petre,', 'St Peter,'), ('Sancte Joánnes cum sóciis tuis,', 'St John, with thy companions,')]) + saints([('Omnes sancti Mártyres,', 'All ye holy Martyrs,')], True) + saints([
            ('Sancte Sylvéster,', 'St Sylvester,'), ('Sancte Gregóri,', 'St Gregory,'), ('Sancte Pie,', 'St Pius,'), ('Sancte Ambrósi,', 'St Ambrose,'), ('Sancte Augustíne,', 'St Augustine,'),
            ('Sancte Hierónyme,', 'St Jerome,'), ('Sancte Hilári,', 'St Hilary,'), ('Sancte Martíne,', 'St Martin,'), ('Sancte Nicoláe,', 'St Nicholas,'), ('Sancte Antoníne,', 'St Antoninus,')]) + [
 ('*', 'Vox exaltétur:', '*', 'The voice is raised:'),
 ('Sancte Pater Domínice,', ORA[0], 'Holy Father Dominic,', ORA[1]),
 ('Sancte Pater Domínice,', ORA[0], 'Holy Father Dominic,', ORA[1]),
] + saints([('Sancte Thoma,', 'St Thomas,'), ('Sancte Vincénti,', 'St Vincent,'), ('Sancte Hyacínthe,', 'St Hyacinth,'), ('Sancte Raymúnde,', 'St Raymond,'), ('Sancte Ludovíce,', 'St Louis,'),
            ('Sancte Antóni,', 'St Anthony,'), ('Sancte Benedícte,', 'St Benedict,'), ('Sancte Bernárde,', 'St Bernard,'), ('Sancte Francísce,', 'St Francis,')]) + saints([
            ('Omnes sancti Confessóres,', 'All ye holy Confessors,')], True) + saints([
            ('Sancta Anna,', 'St Anne,'), ('Sancta María Magdaléna,', 'St Mary Magdalene,'), ('Sancta Martha,', 'St Martha,'), ('Sancta Felícitas,', 'St Felicity,'), ('Sancta Perpétua,', 'St Perpetua,'),
            ('Sancta Ágatha,', 'St Agatha,'), ('Sancta Lúcia,', 'St Lucy,'), ('Sancta Agnes,', 'St Agnes,'), ('Sancta Cæcília,', 'St Cecilia,'), ('Sancta Catharína,', 'St Catherine,'),
            ('Sancta Margaríta,', 'St Margaret,'), ('Sancta Úrsula cum sodálibus tuis,', 'St Ursula, with thy companions,'), ('Sancta Catharína,', 'St Catherine,'), ('Sancta Rosa,', 'St Rose,'),
            ('Sancta Agnes,', 'St Agnes,'), ('Sancta Catharína,', 'St Catherine,')]) + saints([
            ('Omnes sanctæ Vírgines et Víduæ,', 'All ye holy Virgins and Widows,'), ('Omnes Sancti,', 'All ye Saints,')], True) + [
 ('Propítius esto,', 'parce nobis, Dómine.', 'Be merciful,', 'spare us, O Lord.'),
 ('Propítius esto,', 'exáudi nos, Dómine.', 'Be merciful,', 'graciously hear us, O Lord.'),
] + [(a, 'líbera nos, Dómine.', b, 'deliver us, O Lord.') for a, b in [
 ('A damnatióne perpétua,', 'From everlasting damnation,'), ('A subitánea et improvísa morte,', 'From sudden and unprovided death,'),
 ('Ab imminéntibus peccatórum nostrórum perículis,', 'From the dangers of our sins that threaten us,'), ('Ab infestatiónibus dæmonum,', 'From the assaults of the devils,'),
 ('Ab omni immundítia mentis et córporis,', 'From all uncleanness of mind and body,'), ('Ab ira, et ódio, et omni mala voluntáte,', 'From anger, and hatred, and all ill will,'),
 ('Ab immúndis cogitatiónibus,', 'From unclean thoughts,'), ('A cæcitáte cordis,', 'From blindness of heart,'), ('A fúlgure et tempestáte,', 'From lightning and tempest,'),
 ('A peste, fame, et bello,', 'From plague, famine and war,'), ('A flagéllo terræmótus,', 'From the scourge of earthquake,'), ('Ab omni malo,', 'From all evil,'),
 ('Per mystérium sanctæ Incarnatiónis tuæ,', 'Through the mystery of Thy holy Incarnation,'), ('Per Passiónem et Crucem tuam,', 'Through Thy Passion and Cross,'),
 ('Per gloriósam Resurrectiónem tuam,', 'Through Thy glorious Resurrection,'), ('Per admirábilem Ascensiónem tuam,', 'Through Thy wonderful Ascension,'),
 ('Per grátiam Sancti Spíritus Parácliti,', 'Through the grace of the Holy Ghost, the Paraclete,'), ('In die judícii,', 'In the day of judgement,')]] + [
 ('Peccatóres,', 'te rogámus, audi nos.', 'We sinners,', 'we beseech Thee, hear us.')] + [(a, 'te rogámus, audi nos.', b, 'we beseech Thee, hear us.') for a, b in [
 ('Ut pacem nobis dones,', 'That Thou wouldst give us peace,'), ('Ut misericórdia et píetas tua nos custódiat,', 'That Thy mercy and goodness may keep us,'),
 ('Ut Ecclésiam tuam sanctam régere et conserváre dignéris,', 'That Thou wouldst deign to rule and preserve Thy holy Church,'),
 ('Ut Domnum Apostólicum et omnes gradus Ecclésiæ in sancta religióne conserváre dignéris,', 'That Thou wouldst deign to preserve the Lord Apostolic and every rank of the Church in holy religion,'),
 ('Ut Epíscopos et Prælátos nostros et cunctas congregatiónes illis commíssas in tuo sancto servítio conserváre dignéris,', 'That Thou wouldst deign to keep our Bishops and Prelates and all the congregations committed to them in Thy holy service,'),
 ('Ut inimícos sanctæ Ecclésiæ humiliáre dignéris,', 'That Thou wouldst deign to humble the enemies of holy Church,'),
 ('Ut Régibus et Princípibus nostris pacem et veram concórdiam atque victóriam donáre dignéris,', 'That Thou wouldst deign to give our Kings and Princes peace, true concord and victory,'),
 ('Ut cunctum pópulum christiánum pretióso Sánguine tuo redémptum conserváre dignéris,', 'That Thou wouldst deign to preserve all the Christian people redeemed by Thy precious Blood,'),
 ('Ut ómnibus benefactóribus nostris sempitérna bona retríbuas,', 'That Thou wouldst repay all our benefactors with everlasting good things,'),
 ('Ut ánimas nostras et paréntum nostrórum ab ætérna damnatióne erípias,', 'That Thou wouldst snatch our souls and those of our parents from everlasting damnation,'),
 ('Ut fructus terræ dare et conserváre dignéris,', 'That Thou wouldst deign to give and preserve the fruits of the earth,'),
 ('Ut óculos misericórdiæ tuæ super nos redúcere dignéris,', 'That Thou wouldst deign to turn again upon us the eyes of Thy mercy,'),
 ('Ut omnes errántes ad unitátem Ecclésiæ revocáre, et infidéles univérsos ad Evangélii lumen perdúcere dignéris,', 'That Thou wouldst deign to call back all who stray to the unity of the Church, and lead all unbelievers to the light of the Gospel,'),
 ('Ut obséquium servitútis nostræ rationábile fácias,', 'That Thou wouldst make the service of our bondage a reasonable one,'),
 ('Ut mentes nostras ad cæléstia desidéria érigas,', 'That Thou wouldst lift up our minds to heavenly desires,'),
 ('Ut misérias páuperum et captivórum intuéri et releváre dignéris,', 'That Thou wouldst deign to look upon and relieve the miseries of the poor and of captives,'),
 ('Ut loca nostra et omnes habitántes in eis visitáre et consolári dignéris,', 'That Thou wouldst deign to visit and comfort our houses and all who dwell in them,'),
 ('Ut civitátem istam et omnem pópulum ejus protégere et conserváre dignéris,', 'That Thou wouldst deign to protect and preserve this city and all its people,'),
 ('Ut omnes fidéles navigántes et itinerántes ad portum salútis perdúcere dignéris,', 'That Thou wouldst deign to bring all the faithful who travel by sea and by land to the haven of salvation,'),
 ('Ut reguláribus disciplínis nos instrúere dignéris,', 'That Thou wouldst deign to instruct us in regular discipline,'),
 ('Ut ómnibus fidélibus defúnctis réquiem ætérnam dones,', 'That Thou wouldst give eternal rest to all the faithful departed,'),
 ('Ut nos exaudíre dignéris,', 'That Thou wouldst deign to hear us,'), ('Fili Dei,', 'Son of God,')]] + [
 ('Agnus Dei, qui tollis peccáta mundi,', 'parce nobis, Dómine.', 'Lamb of God, who takest away the sins of the world,', 'spare us, O Lord.'),
 ('Agnus Dei, qui tollis peccáta mundi,', 'exáudi nos, Dómine.', 'Lamb of God, who takest away the sins of the world,', 'graciously hear us, O Lord.'),
 ('Agnus Dei, qui tollis peccáta mundi,', 'miserére nobis.', 'Lamb of God, who takest away the sins of the world,', 'have mercy on us.'),
]
SECTIONS = [
 {'id': 'rogationes', 'la': 'Feria II in Rogationibus et duabus Feriis proxime subsequentibus', 'en': 'The Rogation Days: Monday and the two days after', 'pages': [124, 125, 126], 'items': [
  ('rub', 'Quando Missa cantanda fuerit, Sacerdos et Ministri induant se sacris véstibus sicut in ferialibus diébus. Et præcedentibus Acolytho sine céreo, et Subdiácono et Diácono deferénte Missále, subsequatur Sacerdos sine Casula. Deinde, finita Hora præcedente Missam, véniant ante gradus Presbytérii, et stent sicut in Domínicis diébus ad Aspersiónem Aquæ benedíctæ. Cantor autem incípiat Antíphonam Exsúrge.',
          'When the Mass is to be sung, the priest and ministers vest as on ferial days. The acolyte goes first without a candle, then the subdeacon and the deacon carrying the Missal, and the priest follows without the chasuble. When the Hour before Mass is finished they come before the steps of the presbytery and stand as on Sundays at the sprinkling of holy water. The cantor begins the antiphon Exsurge.'),
  ('rub', 'Si autem faciénda fúerit Procéssio, induat Sacerdos cappam séricam et duo Ceroferárii candélas accénsas déferant. Cum cantátur Antíphona, qui delatúri sunt Crucem et aquam benedíctam, accípiant quæ ad eos pértinent.',
          'If there is to be a procession, the priest puts on a silk cope and two candle-bearers carry lighted candles. While the antiphon is sung, those who are to carry the cross and the holy water take what belongs to them.'),
  ('txt', 'Ant. Exsúrge, Dómine, ádjuva nos: et líbera nos propter nomen tuum, allelúia. ℣. Deus, áuribus nostris audívimus: patres nostri annuntiavérunt nobis. Glória Patri. Sicut erat. Repetitur Exsúrge.',
          'Ant. Arise, O Lord, help us, and deliver us for Thy name’s sake, alleluia. ℣. We have heard, O God, with our ears: our fathers have declared to us. Glory be. As it was. Arise is repeated.'),
  ('txt', '℣. Osténde nobis, Dómine, misericórdiam tuam, allelúia. ℟. Et salutáre tuum da nobis, allelúia. ℣. Dóminus vobíscum. ℟. Et cum spíritu tuo. Orémus. Parce, Dómine, parce pópulo tuo: ut dignis flagellatiónibus castigátus, in tua miseratióne respíret: Per Christum Dóminum nostrum. ℟. Amen.',
          '℣. Show us, O Lord, Thy mercy, alleluia. ℟. And grant us Thy salvation, alleluia. ℣. The Lord be with you. ℟. And with thy spirit. Let us pray. Spare, O Lord, spare Thy people; that, chastised by deserved scourges, they may breathe again in Thy mercy. Through Christ our Lord. ℟. Amen.'),
  ('rub', 'Póstea duo Fratres in superpellíceis in médio Chori cantent Litaníam, utróque Choro simul respondénte, Frátribus stántibus versis vúltibus ad Altáre. Intérim (ubi Procéssio non fit) Sacerdos et Minístri sédeant in Presbytério, et ibi simul Litaníam voce submíssa legant, Acolytho tenénte Missále.',
          'Then two friars in surplices sing the Litany in the middle of the choir, both sides of the choir answering together, the friars standing turned towards the altar. Meanwhile (where there is no procession) the priest and ministers sit in the presbytery and read the Litany there together in a low voice, the acolyte holding the Missal.'),
  ('rub', 'Ubi vero Procéssio fíeri consuevérit, egrediátur hoc órdine: Primo præcédat Frater áliquis Clericus (vel áliquis Convérsus si pauci sint Fratres) cum Aqua benedícta, quam procedéndo aspérgat; post eum Ceroferárii in superpellíceis, deínde Cruciferárius in superpellíceo; póstea réliqui Fratres in órdine suo, junióribus præcedéntibus; último Sacerdos cum Diácono a dextris ipsíus áliquas Relíquias deferénte, et Subdiácono a sinístris.',
          'Where it is the custom to have the procession, it goes out in this order: first a clerical friar (or a lay brother if the friars are few) with holy water, sprinkling as he goes; after him the candle-bearers in surplices, then the cross-bearer in a surplice; then the other friars in their order, the younger first; last the priest, with the deacon on his right carrying some relics, and the subdeacon on his left.'),
  ('rub', 'Cum autem dictum fúerit Peccatóres te rogámus, audi nos, Sacerdos cum Minístris revértens in sacrístiam casulam assúmat, et Missa inchoáta, præcedénte uno Ceroferário et Diácono et Subdiácono more sólito, véniat ad Altáre.',
          'When "We sinners, we beseech Thee, hear us" has been sung, the priest returns with the ministers to the sacristy and puts on the chasuble; and when the Mass has begun, with one candle-bearer, the deacon and the subdeacon going before him in the usual way, he comes to the altar.'),
 ]},
 {'id': 'litaniae', 'la': 'Litaniæ Sanctorum', 'en': 'The Litany of the Saints', 'pages': [126, 127, 128, 129, 130], 'items': [
  ('lit', LIT_SANCT),
 ]},
 {'id': 'extraordinariae', 'la': 'In Processionibus extraordinariis', 'en': 'In processions for a particular occasion', 'pages': [131], 'items': [
  ('rub', 'Cum oportébit fácere áliquam Processiónem in claustro vel extra pro áliquo casu emergénte, ut est turbátio áëris, perículum guerrárum, tribulátio Ecclésiæ, status Terræ sanctæ, infírmitas Príncipis, recéptio Reliquiárum, reveréntia Papæ vel alicújus Magni cui occúrritur vel cum Processióne dedúcitur, occásio Capítuli generális vel provinciális, excelléntia defúncti et hujúsmodi: legátur et cantétur et fiant Statiónes secúndum ordinatiónem Prióris cum consílio discretórum, prout cómpetit matériæ cujus occasióne fit Procéssio, et visum fúerit ad ædificatiónem intuéntium expedíre.',
          'When a procession is to be made in the cloister or outside for some occurrence, such as a disturbance of the weather, the danger of war, a trial of the Church, the state of the Holy Land, the illness of the Prince, the reception of relics, the honour of the Pope or of some great person who is met or escorted in procession, a General or Provincial Chapter, the eminence of one who has died, and the like, what is read and sung and the stations made are as the Prior orders with the advice of the discreets, as befits the matter of the procession and seems useful for the edification of those who see it.'),
  ('rub', 'Si cantándæ fúerint Litaníæ, cantentur ut pp. 126-130, quibus finítis dicátur: Kýrie, eléison. Christe, eléison. Kýrie, eléison. Póstea ille qui indútus est Cappa sérica dicat: Pater noster. Et póstea subjúngat:',
          'If the Litany is to be sung, it is sung as on pp. 126-130; after it is said: Lord, have mercy. Christ, have mercy. Lord, have mercy. Then he who wears the silk cope says: Our Father. And then he adds:'),
  ('txt', '℣. Et ne nos indúcas in tentatiónem. ℟. Sed líbera nos a malo. ℣. Ora pro nobis, sancta Dei Génitrix. ℟. Ut digni efficiámur promissiónibus Christi. ℣. Dómine, non secúndum peccáta nostra fácias nobis. ℟. Neque secúndum iniquitátes nostras retríbuas nobis.',
          '℣. And lead us not into temptation. ℟. But deliver us from evil. ℣. Pray for us, O holy Mother of God. ℟. That we may be made worthy of the promises of Christ. ℣. O Lord, deal not with us according to our sins. ℟. Nor reward us according to our iniquities.'),
  ('rub', 'Póstea subjúngat álium Versum de infra pósitis ad propósitum Processiónis.', 'Then he adds another versicle, from those given below, suited to the purpose of the procession.'),
 ]},
]

ORA2 = ('ora pro nobis.', 'pray for us.')
LIT_LAUR = [
 ('Kýrie, eléison.', 'Christe, eléison.', 'Lord, have mercy.', 'Christ, have mercy.'),
 ('Kýrie, eléison.', '', 'Lord, have mercy.', ''),
 ('Christe, audi nos.', 'Christe, exáudi nos.', 'Christ, hear us.', 'Christ, graciously hear us.'),
 ('Pater de cælis, Deus,', 'miserére nobis.', 'God the Father of heaven,', 'have mercy on us.'),
 ('Fili, Redémptor mundi, Deus,', 'miserére nobis.', 'God the Son, Redeemer of the world,', 'have mercy on us.'),
 ('Spíritus Sancte, Deus,', 'miserére nobis.', 'God the Holy Ghost,', 'have mercy on us.'),
 ('Sancta Trínitas, unus Deus,', 'miserére nobis.', 'Holy Trinity, one God,', 'have mercy on us.'),
] + [(a, ORA2[0], b, ORA2[1]) for a, b in [
 ('Sancta María,', 'Holy Mary,'), ('Sancta Dei Génitrix,', 'Holy Mother of God,'), ('Sancta Virgo vírginum,', 'Holy Virgin of virgins,'),
 ('Mater Christi,', 'Mother of Christ,'), ('Mater divínæ grátiæ,', 'Mother of divine grace,'), ('Mater puríssima,', 'Mother most pure,'), ('Mater castíssima,', 'Mother most chaste,'),
 ('Mater invioláta,', 'Mother inviolate,'), ('Mater intemeráta,', 'Mother undefiled,'), ('Mater amábilis,', 'Mother most amiable,'), ('Mater admirábilis,', 'Mother most admirable,'),
 ('Mater boni consílii,', 'Mother of good counsel,'), ('Mater Creatóris,', 'Mother of our Creator,'), ('Mater Salvatóris,', 'Mother of our Saviour,'),
 ('Virgo prudentíssima,', 'Virgin most prudent,'), ('Virgo veneránda,', 'Virgin most venerable,'), ('Virgo prædicánda,', 'Virgin most renowned,'), ('Virgo potens,', 'Virgin most powerful,'),
 ('Virgo clemens,', 'Virgin most merciful,'), ('Virgo fidélis,', 'Virgin most faithful,'), ('Spéculum justítiæ,', 'Mirror of justice,'), ('Sedes sapiéntiæ,', 'Seat of wisdom,'),
 ('Causa nostræ lætítiæ,', 'Cause of our joy,'), ('Vas spirituále,', 'Spiritual vessel,'), ('Vas honorábile,', 'Vessel of honour,'), ('Vas insígne devotiónis,', 'Singular vessel of devotion,'),
 ('Rosa mýstica,', 'Mystical rose,'), ('Turris Davídica,', 'Tower of David,'), ('Turris ebúrnea,', 'Tower of ivory,'), ('Domus áurea,', 'House of gold,'), ('Fœderis arca,', 'Ark of the covenant,'),
 ('Jánua cæli,', 'Gate of heaven,'), ('Stella matutína,', 'Morning star,'), ('Salus infirmórum,', 'Health of the sick,'), ('Refúgium peccatórum,', 'Refuge of sinners,'),
 ('Consolátrix afflictórum,', 'Comforter of the afflicted,'), ('Auxílium Christianórum,', 'Help of Christians,'), ('Regína Angelórum,', 'Queen of Angels,'), ('Regína Patriarchárum,', 'Queen of Patriarchs,'),
 ('Regína Prophetárum,', 'Queen of Prophets,'), ('Regína Apostolórum,', 'Queen of Apostles,'), ('Regína Mártyrum,', 'Queen of Martyrs,'), ('Regína Confessórum,', 'Queen of Confessors,'),
 ('Regína Vírginum,', 'Queen of Virgins,'), ('Regína Sanctórum ómnium,', 'Queen of all Saints,'), ('Regína sine labe originali concépta,', 'Queen conceived without original sin,')]] + [
 ('*', 'Typed into the scanned copy (added to the Litany in 1950):', '*', 'Typed into the scanned copy (added to the Litany in 1950):'),
 ('Regína in cælum assúmpta,', ORA2[0], 'Queen assumed into heaven,', ORA2[1]),
 ('Agnus Dei, qui tollis peccáta mundi,', 'parce nobis, Dómine.', 'Lamb of God, who takest away the sins of the world,', 'spare us, O Lord.'),
 ('Agnus Dei, qui tollis peccáta mundi,', 'exáudi nos, Dómine.', 'Lamb of God, who takest away the sins of the world,', 'graciously hear us, O Lord.'),
 ('Agnus Dei, qui tollis peccáta mundi,', 'miserére nobis.', 'Lamb of God, who takest away the sins of the world,', 'have mercy on us.'),
]
SECTIONS.insert(0, {'id': 'salve', 'la': 'Ad Processionem de B. M. V. post Completorium', 'en': 'The procession of Our Lady after Compline (Salve Regina)', 'pages': [89, 95], 'items': [
  ('txt', 'Ant. Salve, Regína, Mater misericórdiæ; vita, dulcédo, et spes nostra, salve. Ad te clamámus, éxsules fílii Evæ. Ad te suspirámus, geméntes et flentes in hac lacrimárum valle. Eja ergo, advocáta nostra, illos tuos misericórdes óculos ad nos convérte. Et Jesum, benedíctum fructum ventris tui, nobis post hoc exsílium osténde. O clemens, O pia, O dulcis Virgo María. T. P. Allelúia.',
          'Ant. Hail, holy Queen, Mother of mercy, our life, our sweetness and our hope. To thee do we cry, poor banished children of Eve; to thee do we send up our sighs, mourning and weeping in this valley of tears. Turn then, most gracious advocate, thine eyes of mercy towards us; and after this our exile show unto us the blessed fruit of thy womb, Jesus. O clement, O loving, O sweet Virgin Mary. In Paschaltide: Alleluia.'),
  ('rub', 'Finíta Antíphona, Acólythi cantent:', 'When the antiphon is finished, the acolytes sing:'),
  ('txt', '℣. Dignáre me laudáre te, Virgo sacráta. ℟. Da mihi virtútem contra hostes tuos. (T. P. Allelúia.)', '℣. Make me worthy to praise thee, O sacred Virgin. ℟. Give me strength against thine enemies. (In Paschaltide: Alleluia.)'),
  ('rub', 'Hebdomadárius subjúngat:', 'The hebdomadary adds:'),
  ('txt', 'Orémus. Concéde nos fámulos tuos, quǽsumus, Dómine Deus, perpétua mentis et córporis salúte gaudére: et gloriósa beátæ Maríæ semper Vírginis intercessióne, a præsénti liberári tristítia, et ætérna pérfrui lætítia. Per Christum Dóminum nostrum. ℟. Amen.',
          'Let us pray. Grant, we beseech Thee, O Lord God, that we Thy servants may enjoy lasting health of mind and body, and by the glorious intercession of blessed Mary ever Virgin be delivered from present sorrow and enjoy eternal gladness. Through Christ our Lord. ℟. Amen.'),
  ('rub', 'Deínde Ceroferárii, vel Cantóres, incípiant Antíphonam O lumen, ut supra, pag. 76, et Fratres processionáliter revertántur in Chorum. Qua finíta, Ceroferárii dicant:',
          'Then the candle-bearers or the cantors begin the antiphon O lumen, as above, p. 76, and the friars return in procession to the choir. When it is finished, the candle-bearers say:'),
  ('txt', '℣. Ora pro nobis, beáte Pater Domínice. ℟. Ut digni efficiámur promissiónibus Christi. (T. P. Allelúia.) Orémus. Concéde, quǽsumus, omnípotens Deus: ut qui peccatórum nostrórum póndere prémimur, beáti Domínici Confessóris tui, Patris nostri, patrocínio sublevémur. Per Christum Dóminum nostrum. ℟. Amen.',
          '℣. Pray for us, blessed Father Dominic. ℟. That we may be made worthy of the promises of Christ. (In Paschaltide: Alleluia.) Let us pray. Grant, we beseech Thee, almighty God, that we who are weighed down by the burden of our sins may be raised up by the patronage of blessed Dominic, Thy Confessor, our Father. Through Christ our Lord. ℟. Amen.'),
  ('rub', 'Si consuetúdo Convéntus vel Provínciæ sit, ut loco Antíphonæ O lumen cantétur Antíphona de áliquo Sancto Órdinis, vel álio Sancto, talis consuetúdo servári póterit; et tunc Versículus et Orátio erunt páriter de illo cujus Antíphona cantáta fúerit.',
          'If it is the custom of the convent or province to sing, instead of the antiphon O lumen, an antiphon of some saint of the Order or of another saint, the custom may be kept; the versicle and prayer are then likewise of the saint whose antiphon was sung.'),
 ]})
SECTIONS.insert(1, {'id': 'lauretanae', 'la': 'Litaniæ Lauretanæ B. M. V.', 'en': 'The Litany of Loreto, on Saturdays', 'pages': [91, 95], 'items': [
  ('rub', 'Omni Sábbato, finíta post Antíphonam Salve Regína Oratióne Concéde nos, a duóbus Frátribus et Convéntu alternátim cantentur Litaníæ beátæ Maríæ V. tono sequénti, vel álio pro consuetúdine locórum.',
          'Every Saturday, when the prayer Concede nos after the antiphon Salve Regina is finished, the Litany of the Blessed Virgin Mary is sung alternately by two friars and the community, in the following tone or in another according to the custom of the place.'),
  ('lit', LIT_LAUR),
  ('rub', 'Deínde Prosa:', 'Then the Prose:'),
  ('txt', 'Invioláta, intácta et casta es, María, quæ es effécta fúlgida cæli porta. O Mater alma Christi caríssima, súscipe pia laudum præcónia. Nostra ut pura péctora sint et córpora, te nunc flágitant devóta corda et ora. Tua per precáta dulcísona nobis concédas véniam per sǽcula. O benígna, quæ sola invioláta permansísti. T. P. Allelúia.',
          'Inviolate, spotless and pure art thou, O Mary, who wast made the shining gate of heaven. O loving Mother, most dear to Christ, receive our devout songs of praise. That our hearts and bodies may be pure, our devoted hearts and lips now implore thee. By thy sweet-sounding prayers grant us pardon for ever. O kind one, who alone hast remained inviolate. In Paschaltide: Alleluia.'),
  ('rub', 'Póterit étiam, Témpore Pascháli, ubi usus obtinúerit, loco Prosæ Invioláta cantári Ant. Regína cæli, pag. 44. Post Prosam Invioláta vel Ant. Regína cæli dicátur:',
          'In Paschaltide, where it is the custom, the antiphon Regina caeli (p. 44) may be sung instead of the Prose Inviolata. After the Prose Inviolata or the antiphon Regina caeli is said:'),
  ('txt', '℣. Ora pro nobis, sancta Dei Génitrix. ℟. Ut digni efficiámur promissiónibus Christi. (T. P. Allelúia.) Orémus. Grátiam tuam, quǽsumus, Dómine, méntibus nostris infúnde: ut qui, Angelo nuntiánte, Christi Fílii tui Incarnatiónem cognóvimus, per Passiónem ejus et Crucem ad resurrectiónis glóriam perducámur. Per eúndem Christum Dóminum nostrum. ℟. Amen.',
          '℣. Pray for us, O holy Mother of God. ℟. That we may be made worthy of the promises of Christ. (In Paschaltide: Alleluia.) Let us pray. Pour forth, we beseech Thee, O Lord, Thy grace into our hearts; that we, to whom the Incarnation of Christ Thy Son was made known by the message of an Angel, may by His Passion and Cross be brought to the glory of His Resurrection. Through the same Christ our Lord. ℟. Amen.'),
  ('rub', 'Ubi consuétum fúerit, ℣. Ora et Orátio Grátiam immediáte post Litanías B. M. V. dicántur. Post Prosam vero Invioláta, vel post Ant. Regína cæli, dicátur:',
          'Where it is the custom, the versicle Ora and the prayer Gratiam are said immediately after the Litany of Our Lady; and after the Prose Inviolata, or after the antiphon Regina caeli, is said:'),
  ('txt', '℣. Post partum, Virgo, invioláta permansísti. ℟. Dei Génitrix, intercéde pro nobis. (T. P. Allelúia.) Orémus. Prótege, Dómine, fámulos tuos subsídiis pacis: et beátæ Maríæ semper Vírginis patrocíniis confidéntes, a cunctis hóstibus redde secúros. Per Christum Dóminum nostrum. ℟. Amen.',
          '℣. After childbirth, O Virgin, thou didst remain inviolate. ℟. Mother of God, intercede for us. (In Paschaltide: Alleluia.) Let us pray. Protect, O Lord, Thy servants with the help of peace; and make them, trusting in the patronage of blessed Mary ever Virgin, safe from all enemies. Through Christ our Lord. ℟. Amen.'),
  ('rub', 'Póstea dicátur Antíphona cum ℣. et Oratióne de S. P. Domínico, aut de álio Sancto.', 'Then the antiphon, with the versicle and prayer, of our holy Father Dominic or of another saint is said.'),
 ]})

SECTIONS.insert(0, {'id': 'purificatio', 'la': 'In Festo Purificationis B. M. V.', 'en': 'The Purification of Our Lady (Candlemas): blessing of candles and procession', 'pages': [66, 72], 'items': [
  ('rub', 'In festo Purificatiónis, finíta Tértia, Prior cum Cappa sérica, et Diáconus cum Missáli, et Subdiáconus cum Libéllo Processionáli, séricis indúti, præcedéntibus Acólythis in albis cum céreis accénsis, in Chorum véniant: et si Domínica fúerit, Aqua benedícta more sólito aspergátur. Finíta aspersióne Aquæ, vel si Aqua non fúerit aspergénda, postquam in Chorum venerint, Prior stans ante gradus Presbytérii verso vultu ad Altáre, Diácono coram ipso tenénte librum, candélas a Sacrísta super gradus Presbytérii collocátas, ita quod sint ad déxteram benedicéntis, benedícat voce mediócri, eo modo quo dicúntur Oratiónes ad Horas:',
          'On the feast of the Purification, when Terce is finished, the Prior in a silk cope, the deacon with the Missal and the subdeacon with the processional, in silk vestments, come into the choir, the acolytes going before in albs with lighted candles; and if it is a Sunday, holy water is sprinkled in the usual way. After the sprinkling, or when they have come into the choir if there is no sprinkling, the Prior, standing before the steps of the presbytery facing the altar, the deacon holding the book before him, blesses the candles which the sacristan has placed on the steps of the presbytery, so that they are on the right of the one blessing, in a moderate voice, in the way the prayers are said at the Hours:'),
  ('txt', '℣. Dóminus vobíscum. ℟. Et cum spíritu tuo. Orémus. Omnípotens sempitérne Deus, qui hodiérna die Unigénitum tuum ulnis sancti Simeónis in Templo sancto tuo suscipiéndum præsentásti: tuam súpplices deprecámur cleméntiam: ut has candélas, quas nos fámuli tui, in tui nóminis magnificéntiam suscipiéntes, gestáre cúpimus, luce accénsas, bene✠dícere et sancti✠ficáre, atque lúmine supérnæ benedictiónis accéndere dignéris: quátenus eas tibi Dómino Deo nostro offeréndo, digni, et sancto igne dulcíssimæ caritátis tuæ succénsi, in Templo sancto glóriæ tuæ repræsentári mereámur. Per eúndem Christum Dóminum nostrum. ℟. Amen.',
          '℣. The Lord be with you. ℟. And with thy spirit. Let us pray. Almighty, everlasting God, who on this day didst present Thine only-begotten Son in Thy holy Temple to be received in the arms of holy Simeon: we humbly entreat Thy mercy, that Thou wouldst deign to bless✠ and sanctify✠ these candles, which we Thy servants, receiving them to the glory of Thy name, desire to carry lighted, and to kindle them with the light of heavenly blessing; that, offering them to Thee, the Lord our God, we may be made worthy, and set on fire with the holy flame of Thy most sweet charity, to be presented in the holy Temple of Thy glory. Through the same Christ our Lord. ℟. Amen.'),
  ('rub', 'Finíta benedictióne aspérgat Prior candélas Aqua benedícta. Póstmodum Cantor, candélam ófferens Prióri, incípiat Antíphonam Lumen ad revelatiónem, et Convéntus prosequátur ipsam et Cánticum Nunc dimíttis, Cantóre incipiénte síngulos versus Cántici, et reincipiénte Antíphonam prædíctam post síngulos Versus, et repeténte, prout necésse fúerit, si ipsis complétis nondum fúerint expedíta quæ ante inchoatiónem Processiónis sunt faciénda.',
          'After the blessing the Prior sprinkles the candles with holy water. Then the cantor, offering a candle to the Prior, begins the antiphon Lumen ad revelationem, and the community continues it and the canticle Nunc dimittis, the cantor beginning each verse of the canticle and beginning the antiphon again after each verse, and repeating it as needed if, when these are finished, what is to be done before the procession begins is not yet done.'),
  ('txt', 'Ant. Lumen ad revelatiónem géntium, et glóriam plebis tuæ Israël. Cant. Nunc dimíttis servum tuum, Dómine, secúndum verbum tuum in pace. Lumen. ℣. Quia vidérunt óculi mei salutáre tuum. Lumen. ℣. Quod parásti ante fáciem ómnium populórum. Lumen. ℣. Glória Patri. Lumen. ℣. Sicut erat. Lumen.',
          'Ant. A light to the revelation of the Gentiles, and the glory of Thy people Israel. Cant. Now Thou dost dismiss Thy servant, O Lord, according to Thy word in peace. A light. ℣. Because my eyes have seen Thy salvation. A light. ℣. Which Thou hast prepared before the face of all peoples. A light. ℣. Glory be. A light. ℣. As it was. A light.'),
  ('rub', 'Sacrísta vero, postquam Cantor Prióri candélam obtúlerit, primo candélas Minístris distríbuat, deínde Frátribus, incípiens in dextro Choro a superióribus; et álius Frater, cui ipse innúerit, in sinístro; póstmodum Frátribus Convérsis. Dum Candélæ distribuúntur, qui delatúri sunt Crucem et Aquam benedíctam, accípiant quæ ad eos pértinent. Candélis vero distribútis, et terminátis quæ cantánda sunt, incipiéntibus Cantóribus Antíphonam Ave, grátia plena, egrediátur Procéssio secúndum órdinem et ritum qui in Festo Ascensiónis Dómini notátus est, pag. 46, et cantentur sequéntes Antíphonæ, ℣. et Orátio.',
          'After the cantor has offered the candle to the Prior, the sacristan gives out the candles, first to the ministers, then to the friars, beginning in the right choir with the seniors, while another friar whom he signals does so in the left; then to the lay brothers. While the candles are being given out, those who are to carry the cross and the holy water take what belongs to them. When the candles have been given out and what is to be sung is finished, the cantors begin the antiphon Ave, gratia plena and the procession goes out in the order and manner given for the Ascension, p. 46; and the following antiphons, versicle and prayer are sung.'),
  ('h', 'Ad primam Statiónem in prima parte Claustri', 'At the first station, in the first side of the cloister'),
  ('txt', 'Ant. Ave, grátia plena, Dei Génitrix Virgo: ex te enim ortus est Sol justítiæ, illúminans quæ in ténebris sunt. Lætáre tu, sénior juste, suscípiens in ulnas Liberatórem animárum nostrárum, donántem nobis et resurrectiónem.',
          'Ant. Hail, full of grace, Virgin Mother of God: for from thee hath risen the Sun of justice, enlightening those who are in darkness. Rejoice, thou just elder, receiving in thine arms the Deliverer of our souls, who giveth us also the resurrection.'),
  ('h', 'Ad secúndam Statiónem in tértia parte Claustri', 'At the second station, in the third side of the cloister'),
  ('txt', 'Ant. Adórna thálamum tuum, Sion, et súscipe Regem Christum: ampléctere Maríam, quæ est cæléstis porta: ipsa enim portat Regem glóriæ. Novo lúmine subsístit Virgo, addúcens in mánibus Fílium ante lucíferum génitum: quem accípiens Símeon in ulnas suas, prædicávit pópulis Dóminum eum esse vitæ et mortis, et Salvatórem mundi.',
          'Ant. Adorn thy bridal chamber, O Sion, and receive Christ the King; embrace Mary, who is the gate of heaven, for she carries the King of glory. In new light the Virgin stands, bringing in her hands the Son begotten before the day-star; whom Simeon, receiving into his arms, proclaimed to the peoples to be the Lord of life and death and the Saviour of the world.'),
  ('h', 'Ad tértiam Statiónem in quarta parte Claustri', 'At the third station, in the fourth side of the cloister'),
  ('txt', 'Ant. Respónsum accépit Símeon a Spíritu Sancto, non visúrum se mortem, nisi vidéret Christum Dómini: et cum indúcerent Púerum in templum, accépit eum in ulnas suas, et benedíxit Deum, et dixit: Nunc dimíttis, Dómine, servum tuum in pace.',
          'Ant. Simeon received an answer from the Holy Ghost that he should not see death before he had seen the Christ of the Lord; and when they brought the Child into the temple, he took Him into his arms and blessed God, and said: Now Thou dost dismiss Thy servant, O Lord, in peace.'),
  ('h', 'Ad introitum Ecclésiæ vel Chori', 'At the entrance of the church or choir'),
  ('rub', 'Incipiátur Antíphona Hódie, et Convéntu ipsam prosequénte, procéssio chorum ingrediátur. Cum Convéntus Chorum intrat, céteris eúntibus ad sedes suas, qui Aquam benedíctam portávit in Sacrístiam vadat. Prior vero et Minístri se órdinent sicut ad Aspersiónem Aquæ consuevérunt, Cruciferário tenénte Crucem ante gradus Presbytérii.',
          'The antiphon Hodie is begun and, the community continuing it, the procession enters the choir. As the community enters the choir and the others go to their places, he who carried the holy water goes to the sacristy. The Prior and the ministers take their places as they do for the sprinkling of holy water, the cross-bearer holding the cross before the steps of the presbytery.'),
  ('txt', 'Ant. Hódie beáta Virgo María Púerum Jesum præsentávit in templo: et Símeon replétus Spíritu Sancto accépit eum in ulnas suas, et benedíxit Deum, et dixit: Nunc dimíttis, Dómine, servum tuum in pace.',
          'Ant. Today the blessed Virgin Mary presented the Child Jesus in the temple; and Simeon, filled with the Holy Ghost, took Him into his arms and blessed God, and said: Now Thou dost dismiss Thy servant, O Lord, in peace.'),
  ('rub', 'Finíta prædícta Antíphona, Ceroferárii, Cantóre eis deferénte, dicant:', 'When the antiphon is finished, the candle-bearers, the cantor prompting them, say:'),
  ('txt', '℣. Post partum, Virgo, invioláta permansísti. ℟. Dei Génitrix, intercéde pro nobis.', '℣. After childbirth, O Virgin, thou didst remain inviolate. ℟. Mother of God, intercede for us.'),
  ('rub', 'Deínde Prior absque Dóminus vobíscum dicat:', 'Then the Prior, without "The Lord be with you", says:'),
  ('txt', 'Orémus. Exáudi, quǽsumus, Dómine, plebem tuam: et quæ extrínsecus ánnua tríbuis devotióne venerári, intérius ássequi grátiæ tuæ luce concéde. Per Christum Dóminum nostrum. ℟. Amen.',
          'Let us pray. Hear, we beseech Thee, O Lord, Thy people; and grant that what Thou givest them to venerate outwardly by yearly devotion they may attain inwardly by the light of Thy grace. Through Christ our Lord. ℟. Amen.'),
  ('rub', 'Dum autem Orátio dícitur, Cruciferárius Crucem repónat in loco suo. Oratióne finíta, Prior et Minístri in Sacrístiam vadant. Fratres vero Candélas téneant quoúsque fúerint offeréndæ.',
          'While the prayer is said, the cross-bearer puts the cross back in its place. When the prayer is finished, the Prior and the ministers go to the sacristy. The friars keep their candles until they are to be offered.'),
 ]})

SECTIONS.insert(0, {'id': 'ascensio', 'la': 'In Ascensione Domini ad Processionem', 'en': 'The Ascension: the procession (the model for processions after Terce)', 'pages': [46, 51], 'items': [
  ('rub', 'In die Ascensiónis, finíta Tértia, Prior cum Cappa sérica, Diáconus cum Relíquiis, et Subdiáconus séricis indúti, præcedéntibus Ceroferáriis cum céreis accénsis, et Cruciferário cum Cruce in albis ad Altáre véniant: et Cantóribus incipiéntibus ℟. Viri Galilǽi et Convéntu illud prosequénte, egrediátur Procéssio hoc órdine: primo præcédat Frater áliquis Cléricus in superpellíceo (vel áliquis Convérsus, si pauci sint Fratres) cum Aqua benedícta, quam procedéndo aspérgat; post eum Ceroferárii cum céreis accénsis; deínde Cruciferárius cum Cruce; póstea réliqui Fratres órdine suo, junióribus præcedéntibus; último Prior cum Diácono a dextris, áliquas Relíquias deferénte, et Subdiácono a sinístris, portánte Libéllum processionálem.',
          'On Ascension Day, when Terce is finished, the Prior in a silk cope, the deacon with relics and the subdeacon in silk vestments come to the altar, the candle-bearers going before with lighted candles and the cross-bearer with the cross, in albs. The cantors begin the responsory Viri Galilaei, the community continues it, and the procession goes out in this order: first a clerical friar in a surplice (or a lay brother if the friars are few) with holy water, sprinkling as he goes; after him the candle-bearers with lighted candles; then the cross-bearer with the cross; then the other friars in their order, the younger first; last the Prior, with the deacon on his right carrying some relics and the subdeacon on his left carrying the processional.'),
  ('txt', '℟. Viri Galilǽi, quid admirámini aspiciéntes in cælum? allelúia: * Quemádmodum vidístis eum ascendéntem in cælum, ita véniet, allelúia, allelúia, allelúia. ℣. Cumque intueréntur in cælum eúntem illum, ecce duo viri adstitérunt juxta illos in véstibus albis, qui et dixérunt. Quemádmodum.',
          '℟. Ye men of Galilee, why wonder you, looking up to heaven? alleluia: * As you have seen Him going up into heaven, so shall He come, alleluia, alleluia, alleluia. ℣. And while they were beholding Him going up to heaven, behold two men stood by them in white garments, who also said: As you have seen.'),
  ('rub', 'Dum prædíctum ℟. cantátur, fiat prima Státio in prima parte Claustri. In unaquáque autem Statióne Cruciferárius et Ceroferárii vultus suos et imáginem Crucifíxi versos hábeant ad Convéntum, nisi forte fíeret Státio ante exterióre introitum Ecclésiæ, vel Chori: tunc enim prædícti Minístri vértere debent vultus ad Altáre, imágine tamen Crucifíxi versa ad Convéntum. Prior autem stans último cum Diácono et Subdiácono, vultus suos hábeant versos ad Crucem: céteri Fratres stent semper versis vúltibus ad se ínvicem: deferens vero Aquam benedíctam, depósita Aqua ante Crucem, cóllocet se último loco in Choro suo, si est Cléricus; vel stet aliquántulum retro Crucem, si est Convérsus. Finíto prædícto primo Responsório, cantétur a duóbus Frátribus ℣. Cumque; quod étiam observétur in áliis Responsóriis. Finíta resumptióne post Versum, Cantóribus inchoántibus ℟. ij, procedátur ad secúndam statiónem, quæ fiat in tértia parte Claustri.',
          'While this responsory is sung, the first station is made in the first side of the cloister. At each station the cross-bearer and the candle-bearers face the community, with the image of the Crucified turned towards it, unless the station is made before the outer entrance of the church or choir: then these ministers face the altar, the image of the Crucified still turned towards the community. The Prior, standing last with the deacon and subdeacon, faces the cross; the other friars always stand facing one another; the one carrying the holy water sets it down before the cross and takes the last place in his choir if he is a cleric, or stands a little behind the cross if he is a lay brother. When the first responsory is finished, the verse Cumque is sung by two friars, and so in the other responsories. When the repetition after the verse is finished, the cantors begin the second responsory and the procession goes on to the second station, in the third side of the cloister.'),
  ('txt', '℟. Omnis pulchritúdo Dómini exaltáta est super sídera: spécies ejus in núbibus cæli, * Et nomen ejus in ætérnum pérmanet, allelúia. ℣. A summo cælo egréssio ejus, et occúrsus ejus usque ad summum ejus. Et nomen.',
          '℟. All the beauty of the Lord is exalted above the stars; His comeliness is in the clouds of heaven, * And His name endureth for ever, alleluia. ℣. His going out is from the end of heaven, and His circuit even to the end thereof. And His name.'),
  ('rub', 'Cantóribus inchoántibus ℟. iij, procedátur ad tértiam Statiónem, quæ fiat in quarta parte Claustri.', 'The cantors begin the third responsory and the procession goes on to the third station, in the fourth side of the cloister.'),
  ('txt', '℟. Non conturbétur cor vestrum, ego vado ad Patrem: et dum assúmptus fúero a vobis, mittam vobis, allelúia, Spíritum veritátis: * Et gaudébit cor vestrum, allelúia. ℣. Ego rogábo Patrem, et álium Paráclitum dabit vobis. Et gaudébit.',
          '℟. Let not your heart be troubled; I go to the Father: and when I am taken up from you, I will send you, alleluia, the Spirit of truth: * And your heart shall rejoice, alleluia. ℣. I will ask the Father, and He shall give you another Paraclete. And your heart.'),
  ('rub', 'Finíta resumptióne post Versum, inchoétur ad Introitum Ecclésiæ Antíphona O Rex glóriæ, et Convéntu ipsam prosequénte, procéssio Ecclésiam ingrediátur. Fratres intrent Chorum, et eant ad sedes suas; et qui aquam benedíctam portávit, in Sacrístiam vadat: Prior vero et Minístri órdinent se sicut ad aspersiónem Aquæ benedíctæ consuevérunt, Cruciferário tenénte Crucem ante gradus Presbytérii.',
          'When the repetition after the verse is finished, the antiphon O Rex gloriae is begun at the entrance of the church and, the community continuing it, the procession enters the church. The friars enter the choir and go to their places, and he who carried the holy water goes to the sacristy; the Prior and the ministers take their places as for the sprinkling of holy water, the cross-bearer holding the cross before the steps of the presbytery.'),
  ('h', 'Ad introitum Ecclésiæ', 'At the entrance of the church'),
  ('txt', 'Ant. O Rex glóriæ, Dómine virtútum, qui triumphátor hódie super omnes cælos ascendísti: ne derelínquas nos órphanos, sed mitte promíssum Patris in nos, Spíritum veritátis, allelúia.',
          'Ant. O King of glory, Lord of hosts, who this day didst ascend in triumph above all the heavens: leave us not orphans, but send upon us the promise of the Father, the Spirit of truth, alleluia.'),
  ('rub', 'Finíta Antíphona, Ceroferárii, Cantóre eis deferénte, dicant sequéntem ℣.:', 'When the antiphon is finished, the candle-bearers, the cantor prompting them, say the following versicle:'),
  ('txt', '℣. Ascéndit Deus in jubilatióne, allelúia. ℟. Et Dóminus in voce tubæ, allelúia.', '℣. God is ascended with jubilee, alleluia. ℟. And the Lord with the sound of trumpet, alleluia.'),
  ('rub', 'Deínde Prior, absque Dóminus vobíscum, præmísso Orémus, dicat sequéntem Oratiónem; quæ dum dícitur, Cruciferárius repónat Crucem in loco suo.', 'Then the Prior, without "The Lord be with you", saying "Let us pray", says the following prayer; while it is said, the cross-bearer puts the cross back in its place.'),
  ('txt', 'Orémus. Deus, cujus Fílius in alta cælórum poténter ascéndens, captivitátem nostram sua duxit virtúte captívam: tríbue, quǽsumus, ut dona, quæ suis particípibus cóntulit, largiátur et nobis, Jesus Christus Fílius tuus Dóminus noster: Qui tecum vivit et regnat per ómnia sǽcula sæculórum. ℟. Amen.',
          'Let us pray. O God, whose Son, ascending in power to the heights of heaven, by His might led our captivity captive: grant, we beseech Thee, that the gifts He bestowed on those who share with Him He may bestow on us also, Jesus Christ Thy Son our Lord, who liveth and reigneth with Thee for ever and ever. ℟. Amen.'),
  ('rub', 'Oratióne finíta, Prior et Minístri in Sacrístiam vadant. Hic ritus et ordo procedéndi servétur in ómnibus Processiónibus, quæ finíta Tértia fíeri solent, nisi áliter notétur.',
          'When the prayer is finished, the Prior and the ministers go to the sacristy. This rite and order of going in procession is kept in all the processions that are made after Terce, unless otherwise noted.'),
 ]})
# the book's order: Ascension before Purification
S = {s['id']: s for s in SECTIONS}
order = ['ascensio', 'purificatio', 'salve', 'lauretanae', 'rogationes', 'litaniae', 'extraordinariae']
SECTIONS[:] = [S[k] for k in order] + [s for s in SECTIONS if s['id'] not in order]

# ---- the chant, typeset from the scan (tools/proc/gabc; each file read note by note, see its header)
def _at(sec, pred, items, after=False):
    it = S[sec]['items']
    i = next(n for n, x in enumerate(it) if pred(x))
    it[i + (1 if after else 0):i + (1 if after else 0)] = items
_t = lambda p: (lambda x: x[0] == 'txt' and x[1].startswith(p))
_r = lambda p: (lambda x: x[0] == 'rub' and x[1].startswith(p))
_at('salve', _t('Ant. Salve'), [('gabc', 'salve_regina', 'Ant.', '1')])
_at('lauretanae', lambda x: x[0] == 'lit', [
    ('h', 'Tonus Litaniarum (pp. 91-94)', 'The tone of the Litany: the Kyrie, then each kind of invocation as printed'),
    ('gabc', 'lor_kyrie', '', '6'),
    ('rub', 'Pater de cælis Deus, Fili Redémptor mundi Deus, Spíritus sancte Deus, Sancta Trínitas unus Deus:', 'The invocations of the Holy Trinity:'),
    ('gabc', 'lor_invocation_miserere', '', ''),
    ('rub', 'Sancta María … Virgo fidélis:', 'Holy Mary to Virgin most faithful (the shorter lines leave out notes of the recitation):'),
    ('gabc', 'lor_invocation_maria', '', ''),
    ('rub', 'Spéculum justítiæ … Auxílium Christianórum:', 'Mirror of justice to Help of Christians:'),
    ('gabc', 'lor_invocation_speculum', '', ''),
    ('rub', 'Regína Angelórum … Regína sine labe origináli concépta:', 'Queen of Angels to Queen conceived without original sin:'),
    ('gabc', 'lor_invocation_regina', '', ''),
    ('gabc', 'lor_agnus', '', '')])
_at('lauretanae', _t('Invioláta'), [('gabc', 'inviolata', 'Prosa', '6')])
_at('lauretanae', _r('Póterit étiam'), [('gabc', 'regina_caeli', 'Ant.', '5')], after=True)
_at('rogationes', _t('Ant. Exsúrge'), [('gabc', 'rog_exsurge', 'Ant.', '2')])
_at('litaniae', lambda x: x[0] == 'lit', [
    ('h', 'Tonus Litaniarum (pp. 126-130)', 'The tone of the Litany: each kind of invocation as printed; the others are sung like the first of their kind'),
    ('gabc', 'lit_kyrie', '', ''), ('gabc', 'lit_christe_audi', '', ''), ('gabc', 'lit_miserere', '', ''),
    ('rub', 'Sancta María, Sancta Dei Génitrix, Sancta Virgo vírginum; et sic de céteris:', 'Holy Mary, Holy Mother of God, Holy Virgin of virgins; and so the other saints:'),
    ('gabc', 'lit_ora', '', ''),
    ('rub', 'Sancte Míchaël, Sancte Gábriel, Sancte Ráphaël:', 'St Michael, St Gabriel, St Raphael:'),
    ('gabc', 'lit_ora_michael', '', ''),
    ('rub', 'Omnes sancti Ángeli et Archángeli; et sic de céteris in plurali:', 'All ye holy Angels and Archangels; and so the others in the plural:'),
    ('gabc', 'lit_orate', '', ''), ('gabc', 'lit_propitius', '', ''),
    ('rub', 'A damnatióne perpétua … In die judícii:', 'From everlasting damnation … In the day of judgement:'),
    ('gabc', 'lit_libera', '', ''),
    ('rub', 'Peccatóres … Fili Dei:', 'We sinners … Son of God:'),
    ('gabc', 'lit_rogamus', '', ''), ('gabc', 'lit_agnus', '', ''),
    ('h', 'Litaniæ', 'The Litany in full (texts)')])
_at('extraordinariae', _r('Si cantándæ'), [('gabc', 'lit_extra_kyrie', '', ''), ('gabc', 'lit_extra_pater', '', '')], after=True)
_at('ascensio', _t('℟. Viri Galil'), [('gabc', 'asc_viri', '℟.', '7')])
_at('ascensio', _t('℟. Omnis pulchr'), [('gabc', 'asc_omnis', '℟.', '2')])
_at('ascensio', _t('℟. Non conturb'), [('gabc', 'asc_nonconturbetur', '℟.', '3')])
_at('ascensio', _t('Ant. O Rex'), [('gabc', 'asc_orex', 'Ant.', '2')])
