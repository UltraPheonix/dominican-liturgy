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
  ('scan', [124, 125]),
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
  ('scan', [126, 127, 128, 129, 130]),
  ('lit', LIT_SANCT),
 ]},
 {'id': 'extraordinariae', 'la': 'In Processionibus extraordinariis', 'en': 'In processions for a particular occasion', 'pages': [131], 'items': [
  ('rub', 'Cum oportébit fácere áliquam Processiónem in claustro vel extra pro áliquo casu emergénte, ut est turbátio áëris, perículum guerrárum, tribulátio Ecclésiæ, status Terræ sanctæ, infírmitas Príncipis, recéptio Reliquiárum, reveréntia Papæ vel alicújus Magni cui occúrritur vel cum Processióne dedúcitur, occásio Capítuli generális vel provinciális, excelléntia defúncti et hujúsmodi: legátur et cantétur et fiant Statiónes secúndum ordinatiónem Prióris cum consílio discretórum, prout cómpetit matériæ cujus occasióne fit Procéssio, et visum fúerit ad ædificatiónem intuéntium expedíre.',
          'When a procession is to be made in the cloister or outside for some occurrence, such as a disturbance of the weather, the danger of war, a trial of the Church, the state of the Holy Land, the illness of the Prince, the reception of relics, the honour of the Pope or of some great person who is met or escorted in procession, a General or Provincial Chapter, the eminence of one who has died, and the like, what is read and sung and the stations made are as the Prior orders with the advice of the discreets, as befits the matter of the procession and seems useful for the edification of those who see it.'),
  ('rub', 'Si cantándæ fúerint Litaníæ, cantentur ut pp. 126-130, quibus finítis dicátur: Kýrie, eléison. Christe, eléison. Kýrie, eléison. Póstea ille qui indútus est Cappa sérica dicat: Pater noster. Et póstea subjúngat:',
          'If the Litany is to be sung, it is sung as on pp. 126-130; after it is said: Lord, have mercy. Christ, have mercy. Lord, have mercy. Then he who wears the silk cope says: Our Father. And then he adds:'),
  ('scan', [131]),
  ('txt', '℣. Et ne nos indúcas in tentatiónem. ℟. Sed líbera nos a malo. ℣. Ora pro nobis, sancta Dei Génitrix. ℟. Ut digni efficiámur promissiónibus Christi. ℣. Dómine, non secúndum peccáta nostra fácias nobis. ℟. Neque secúndum iniquitátes nostras retríbuas nobis.',
          '℣. And lead us not into temptation. ℟. But deliver us from evil. ℣. Pray for us, O holy Mother of God. ℟. That we may be made worthy of the promises of Christ. ℣. O Lord, deal not with us according to our sins. ℟. Nor reward us according to our iniquities.'),
  ('rub', 'Póstea subjúngat álium Versum de infra pósitis ad propósitum Processiónis.', 'Then he adds another versicle, from those given below, suited to the purpose of the procession.'),
 ]},
]
