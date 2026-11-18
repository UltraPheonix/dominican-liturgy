/* Ordo Missæ secundum ritum Ordinis Prædicatorum (Missale O.P. 1933, with the rubrics of 1960).
   Latin after the Missale O.P.; English after the St Dominic Missal (1959) and Divinum Officium.
   Each section is a list of lines: {r: rubric} or {w: speaker, la: Latin, en: English};
   m limits a line to some forms of Mass: l = Low Mass, s = Sung Mass, m = Solemn Mass (default: all). */
window.ORDO = {
  // the chalice is prepared at the altar: before the prayers at the foot (Low Mass), during the Gradual (Sung Mass),
  // during the Gradual by the subdeacon, the priest seated (Solemn Mass)
  chalice: {la: 'Præparatio calicis', en: 'Preparation of the chalice', lines: [
    {m: 'l', r: 'The priest, having come to the altar, unfolds the corporal and prepares the chalice, pouring in wine and water. When presenting the water the server says:'},
    {m: 's', r: 'At a Sung Mass the chalice is prepared after the Epistle, while the Gradual is sung. When presenting the water the server says:'},
    {m: 'm', r: 'At a Solemn Mass the priest sits at the Epistle side after the Epistle; the subdeacon brings the chalice and prepares it, the deacon presenting the water with the words:'},
    {w: 'S', la: 'Benedícite.', en: 'Bless.'},
    {r: 'The priest blesses the water (not in Masses for the Dead):'},
    {w: 'P', la: 'In nómine Patris, et Fílii, et Spíritus Sancti.', en: 'In the name of the Father, and of the Son, and of the Holy Ghost.'},
    {w: 'S', la: 'Amen.', en: 'Amen.'}
  ]},
  foot: {la: 'Ad pedem altaris', en: 'At the foot of the altar', lines: [
    {r: 'Standing at the altar, the priest says in a low voice:'},
    {w: 'P', la: 'Actiónes nostras, quǽsumus, Dómine, aspirándo prǽveni et adiuvándo proséquere: ut cuncta nostra operátio a te semper incípiat, et per te cœpta finiátur. Per Christum Dóminum nostrum. Amen.', en: 'Prevent, O Lord, we beseech thee, our actions by thy inspiration, and continue them by thine assistance; that every one of our works may begin always from thee, and through thee be ended. Through Christ our Lord. Amen.'},
    {r: 'He descends to the foot of the altar, bows profoundly, and signs himself:'},
    {w: 'P', la: 'In nómine Patris, et Fílii, et Spíritus Sancti. Amen.', en: 'In the name of the Father, and of the Son, and of the Holy Ghost. Amen.'},
    {w: 'P', la: 'Confitémini Dómino quóniam bonus.', en: 'Give praise to the Lord, for he is good.'},
    {w: 'S', la: 'Quóniam in sǽculum misericórdia eius.', en: 'For his mercy endureth for ever.'},
    {w: 'P', la: 'Confíteor Deo omnipoténti, et beátæ Maríæ semper Vírgini, et beáto Domínico patri nostro, et ómnibus Sanctis, et vobis, fratres, quia peccávi nimis cogitatióne, locutióne, ópere et omissióne, mea culpa: precor vos oráre pro me.', en: 'I confess to almighty God, to blessed Mary ever a virgin, to blessed Dominic our father, to all the saints, and to you, brethren, that I have sinned exceedingly in thought, word, deed and omission, through my fault: I beseech you to pray for me.'},
    {w: 'S', la: 'Misereátur tui omnípotens Deus, et dimíttat tibi ómnia peccáta tua: líberet te ab omni malo, salvet et confírmet in omni ópere bono, et perdúcat te ad vitam ætérnam.', en: 'May almighty God have mercy on thee and forgive thee all thy sins: may he deliver thee from all evil, save and strengthen thee in every good work, and bring thee to life everlasting.'},
    {w: 'P', la: 'Amen.', en: 'Amen.'},
    {w: 'S', la: 'Confíteor Deo omnipoténti, et beátæ Maríæ semper Vírgini, et beáto Domínico patri nostro, et ómnibus Sanctis, et tibi, pater, quia peccávi nimis cogitatióne, locutióne, ópere et omissióne, mea culpa: precor te oráre pro me.', en: 'I confess to almighty God, to blessed Mary ever a virgin, to blessed Dominic our father, to all the saints, and to thee, father, that I have sinned exceedingly in thought, word, deed and omission, through my fault: I beseech thee to pray for me.'},
    {w: 'P', la: 'Misereátur vestri omnípotens Deus, et dimíttat vobis ómnia peccáta vestra: líberet vos ab omni malo, salvet et confírmet in omni ópere bono, et perdúcat vos ad vitam ætérnam.', en: 'May almighty God have mercy on you and forgive you all your sins: may he deliver you from all evil, save and strengthen you in every good work, and bring you to life everlasting.'},
    {w: 'S', la: 'Amen.', en: 'Amen.'},
    {w: 'P', la: 'Absolutiónem et remissiónem ómnium peccatórum vestrórum tríbuat vobis omnípotens et miséricors Dóminus.', en: 'May the almighty and merciful Lord grant you pardon and remission of all your sins.'},
    {w: 'S', la: 'Amen.', en: 'Amen.'},
    {w: 'P', la: 'Adiutórium nostrum in nómine Dómini.', en: 'Our help is in the name of the Lord.'},
    {w: 'S', la: 'Qui fecit cælum et terram.', en: 'Who made heaven and earth.'},
    {r: 'Going up to the altar, the priest bows and says:'},
    {w: 'P', la: 'Aufer a nobis, Dómine, cunctas iniquitátes nostras: ut ad Sancta sanctórum puris mereámur méntibus introíre. Per Christum Dóminum nostrum. Amen.', en: 'Take away from us all our iniquities, O Lord, that we may be worthy to enter with pure minds into the Holy of Holies. Through Christ our Lord. Amen.'},
    {r: 'He signs the altar with the cross and kisses it, then signs himself and goes to the missal.'},
    {m: 'm', r: 'At a Solemn Mass the altar is incensed after the Introit has been begun.'}
  ]},
  // Kyrie, Gloria, Credo, Sanctus, Agnus Dei said, at Low Mass (sung at Sung and Solemn Mass from the Kyriale)
  kyLow: {la: 'Kyrie', en: 'Kyrie', lines: [
    {w: 'P', la: 'Kýrie, eléison.', en: 'Lord, have mercy.'}, {w: 'S', la: 'Kýrie, eléison.', en: 'Lord, have mercy.'},
    {w: 'P', la: 'Kýrie, eléison.', en: 'Lord, have mercy.'}, {w: 'S', la: 'Christe, eléison.', en: 'Christ, have mercy.'},
    {w: 'P', la: 'Christe, eléison.', en: 'Christ, have mercy.'}, {w: 'S', la: 'Christe, eléison.', en: 'Christ, have mercy.'},
    {w: 'P', la: 'Kýrie, eléison.', en: 'Lord, have mercy.'}, {w: 'S', la: 'Kýrie, eléison.', en: 'Lord, have mercy.'},
    {w: 'P', la: 'Kýrie, eléison.', en: 'Lord, have mercy.'}
  ]},
  glLow: {la: 'Gloria', en: 'Gloria', lines: [
    {w: 'P', la: 'Glória in excélsis Deo. Et in terra pax homínibus bonæ voluntátis. Laudámus te. Benedícimus te. Adorámus te. Glorificámus te. Grátias ágimus tibi propter magnam glóriam tuam. Dómine Deus, Rex cæléstis, Deus Pater omnípotens. Dómine Fili unigénite, Iesu Christe. Dómine Deus, Agnus Dei, Fílius Patris. Qui tollis peccáta mundi, miserére nobis. Qui tollis peccáta mundi, súscipe deprecatiónem nostram. Qui sedes ad déxteram Patris, miserére nobis. Quóniam tu solus Sanctus. Tu solus Dóminus. Tu solus Altíssimus, Iesu Christe. Cum Sancto Spíritu, in glória Dei Patris. Amen.', en: 'Glory to God in the highest. And on earth peace to men of good will. We praise thee. We bless thee. We adore thee. We glorify thee. We give thee thanks for thy great glory. O Lord God, heavenly King, God the Father almighty. O Lord Jesus Christ, the only-begotten Son. O Lord God, Lamb of God, Son of the Father. Who takest away the sins of the world, have mercy on us. Who takest away the sins of the world, receive our prayer. Who sittest at the right hand of the Father, have mercy on us. For thou alone art holy. Thou alone art Lord. Thou alone, O Jesus Christ, art most high. With the Holy Ghost, in the glory of God the Father. Amen.'}
  ]},
  collect: {la: 'Oratio', en: 'Collect', lines: [
    {r: 'The priest kisses the altar, turns to the people and says:'},
    {w: 'P', la: 'Dóminus vobíscum.', en: 'The Lord be with you.'},
    {w: 'S', la: 'Et cum spíritu tuo.', en: 'And with thy spirit.'},
    {w: 'P', la: 'Orémus.', en: 'Let us pray.'}
  ]},
  collectEnd: {la: 'Epistola', en: 'Epistle', lines: [
    {m: 'm', r: 'The subdeacon then sings the Epistle; at its end the priest blesses him.'},
    {m: 'l', r: 'Then the Epistle, after which the server answers: Deo grátias.'}
  ]},
  gospel: {la: 'Ante Evangelium', en: 'Before the Gospel', lines: [
    {m: 'ls', r: 'At the Gospel side of the altar the priest says in a low voice:'},
    {m: 'ls', w: 'P', la: 'Dóminus sit in corde meo et in lábiis meis ad pronuntiándum sanctum Evangélium pacis.', en: 'May the Lord be in my heart and on my lips, that I may announce the holy Gospel of peace.'},
    {m: 'm', r: 'The deacon places incense, kneels before the priest and asks his blessing:'},
    {m: 'm', w: 'D', la: 'Iube, domne, benedícere.', en: 'Pray, sir, a blessing.'},
    {m: 'm', w: 'P', la: 'Dóminus sit in corde tuo et in lábiis tuis ad pronuntiándum sanctum Evangélium pacis.', en: 'May the Lord be in thy heart and on thy lips, that thou mayest announce the holy Gospel of peace.'},
    {m: 'm', r: 'The deacon goes in procession, with the subdeacon, thurifer and acolytes, to the place of the Gospel.'},
    {w: 'P', la: 'Dóminus vobíscum.', en: 'The Lord be with you.'},
    {w: 'S', la: 'Et cum spíritu tuo.', en: 'And with thy spirit.'},
    {w: 'P', la: 'Sequéntia sancti Evangélii secúndum N.', en: 'The continuation of the holy Gospel according to N.'},
    {w: 'S', la: 'Glória tibi, Dómine.', en: 'Glory be to thee, O Lord.'},
    {r: 'Priest and people sign themselves on forehead, lips and breast.'}
  ]},
  afterGospel: {la: 'Post Evangelium', en: 'After the Gospel', lines: [
    {w: 'S', la: 'Laus tibi, Christe.', en: 'Praise be to thee, O Christ.'},
    {r: 'The priest (at a Solemn Mass, the deacon bringing him the book) kisses the Gospel, saying:'},
    {w: 'P', la: 'Per evangélica dicta deleántur nostra delícta.', en: 'By the words of the Gospel may our sins be blotted out.'},
    {m: 'ls', r: 'On Sundays and feasts there may follow the sermon.'}
  ]},
  crLow: {la: 'Credo', en: 'Credo', lines: [
    {w: 'P', la: 'Credo in unum Deum, Patrem omnipoténtem, factórem cæli et terræ, visibílium ómnium et invisibílium. Et in unum Dóminum Iesum Christum, Fílium Dei unigénitum. Et ex Patre natum ante ómnia sǽcula. Deum de Deo, lumen de lúmine, Deum verum de Deo vero. Génitum, non factum, consubstantiálem Patri: per quem ómnia facta sunt. Qui propter nos hómines et propter nostram salútem descéndit de cælis. (Hic genuflectitur.) Et incarnátus est de Spíritu Sancto ex María Vírgine: et homo factus est. Crucifíxus étiam pro nobis: sub Póntio Piláto passus, et sepúltus est. Et resurréxit tértia die, secúndum Scriptúras. Et ascéndit in cælum: sedet ad déxteram Patris. Et íterum ventúrus est cum glória iudicáre vivos et mórtuos: cuius regni non erit finis. Et in Spíritum Sanctum, Dóminum et vivificántem: qui ex Patre Filióque procédit. Qui cum Patre et Fílio simul adorátur et conglorificátur: qui locútus est per Prophétas. Et unam sanctam cathólicam et apostólicam Ecclésiam. Confíteor unum baptísma in remissiónem peccatórum. Et exspécto resurrectiónem mortuórum. Et vitam ventúri sǽculi. Amen.', en: 'I believe in one God, the Father almighty, maker of heaven and earth, and of all things visible and invisible. And in one Lord Jesus Christ, the only-begotten Son of God. Born of the Father before all ages. God of God, light of light, true God of true God. Begotten, not made, consubstantial with the Father: by whom all things were made. Who for us men and for our salvation came down from heaven. (Here all kneel.) And became incarnate by the Holy Ghost of the Virgin Mary: and was made man. He was crucified also for us, suffered under Pontius Pilate, and was buried. And on the third day he rose again according to the Scriptures. And ascended into heaven, and sitteth at the right hand of the Father. And he shall come again with glory to judge the living and the dead: of whose kingdom there shall be no end. And in the Holy Ghost, the Lord and giver of life, who proceedeth from the Father and the Son. Who together with the Father and the Son is adored and glorified: who spoke by the Prophets. And one holy, catholic and apostolic Church. I confess one baptism for the remission of sins. And I look for the resurrection of the dead. And the life of the world to come. Amen.'}
  ]},
  offerDial: {la: 'Offertorium', en: 'Offertory', lines: [
    {w: 'P', la: 'Dóminus vobíscum.', en: 'The Lord be with you.'},
    {w: 'S', la: 'Et cum spíritu tuo.', en: 'And with thy spirit.'},
    {w: 'P', la: 'Orémus.', en: 'Let us pray.'},
    {r: 'The Offertory antiphon is read (or sung):'}
  ]},
  offertory: {la: 'Oblatio', en: 'The offering', lines: [
    {m: 'm', r: 'The deacon hands the chalice, with the paten and host upon it, to the priest.'},
    {r: 'Uncovering the chalice, with the paten and host upon it, the priest says:'},
    {w: 'P', la: 'Quid retríbuam Dómino pro ómnibus quæ retríbuit mihi? Cálicem salutáris accípiam, et nomen Dómini invocábo.', en: 'What shall I render to the Lord for all the things that he hath rendered unto me? I will take the chalice of salvation, and I will call upon the name of the Lord.'},
    {r: 'Raising the chalice with the host upon the paten, he offers both together:'},
    {w: 'P', la: 'Súscipe, sancta Trínitas, hanc oblatiónem, quam tibi óffero in memóriam passiónis Dómini nostri Iesu Christi: et præsta, ut in conspéctu tuo tibi placens ascéndat, et meam et ómnium fidélium salútem operétur ætérnam.', en: 'Receive, O holy Trinity, this oblation which I offer to thee in memory of the passion of our Lord Jesus Christ: and grant that it may ascend before thee and be pleasing to thee, and work my eternal salvation and that of all the faithful.'},
    {r: 'He places the host on the corporal and the chalice behind it, and covers the chalice with the pall.'},
    {m: 'm', r: 'At a Solemn Mass the offerings, the altar, the priest, the ministers, the choir and the people are now incensed.'},
    {r: 'At the Epistle side he washes his fingers, saying:'},
    {w: 'P', la: 'Lavábo inter innocéntes manus meas: et circúmdabo altáre tuum, Dómine: ut áudiam vocem laudis, et enárrem univérsa mirabília tua. Dómine, diléxi decórem domus tuæ, et locum habitatiónis glóriæ tuæ.', en: 'I will wash my hands among the innocent, and will compass thine altar, O Lord, that I may hear the voice of thy praise, and tell of all thy wondrous works. I have loved, O Lord, the beauty of thy house, and the place where thy glory dwelleth.'},
    {r: 'Bowing in the middle of the altar, with joined hands, he says:'},
    {w: 'P', la: 'In spíritu humilitátis et in ánimo contríto suscipiámur, Dómine, a te: et sic fiat sacrifícium nostrum, ut a te suscipiátur hódie, et pláceat tibi, Dómine Deus.', en: 'In a humble spirit and a contrite heart may we be received by thee, O Lord; and so may our sacrifice be offered in thy sight this day, that it be received by thee and be pleasing to thee, O Lord God.'},
    {r: 'He kisses the altar, turns to the people and says:'},
    {w: 'P', la: 'Oráte, fratres, ut meum ac vestrum páriter in conspéctu Dómini sit accéptum sacrifícium.', en: 'Pray, brethren, that my sacrifice and yours may be equally acceptable in the sight of the Lord.'},
    {r: 'Turning back to the altar, he says:'},
    {w: 'P', la: 'Dómine, exáudi oratiónem meam: et clamor meus ad te véniat.', en: 'O Lord, hear my prayer; and let my cry come unto thee.'},
    {r: 'Then, in a low voice, the Secret of the day:'}
  ]},
  offertoryEnd: {la: 'Præfatio', en: 'Preface', lines: [
    {m: 'sm', r: 'Its conclusion and the dialogue before the Preface are sung (below).'},
    {m: 'l', w: 'P', la: 'Dóminus vobíscum.', en: 'The Lord be with you.'},
    {m: 'l', w: 'S', la: 'Et cum spíritu tuo.', en: 'And with thy spirit.'},
    {m: 'l', w: 'P', la: 'Sursum corda.', en: 'Lift up your hearts.'},
    {m: 'l', w: 'S', la: 'Habémus ad Dóminum.', en: 'We have lifted them up to the Lord.'},
    {m: 'l', w: 'P', la: 'Grátias agámus Dómino Deo nostro.', en: 'Let us give thanks to the Lord our God.'},
    {m: 'l', w: 'S', la: 'Dignum et iustum est.', en: 'It is meet and just.'}
  ]},
  saLow: {la: 'Sanctus', en: 'Sanctus', lines: [
    {w: 'P', la: 'Sanctus, Sanctus, Sanctus Dóminus Deus Sábaoth. Pleni sunt cæli et terra glória tua. Hosánna in excélsis. Benedíctus qui venit in nómine Dómini. Hosánna in excélsis.', en: 'Holy, holy, holy, Lord God of hosts. Heaven and earth are full of thy glory. Hosanna in the highest. Blessed is he that cometh in the name of the Lord. Hosanna in the highest.'}
  ]},
  canon: {la: 'Canon Missæ', en: 'The Canon of the Mass', lines: [
    {r: 'The priest raises his eyes, bows, and with joined hands says in a low voice:'},
    {w: 'P', la: 'Te ígitur, clementíssime Pater, per Iesum Christum Fílium tuum Dóminum nostrum, súpplices rogámus ac pétimus, uti accépta hábeas et benedícas hæc ✠ dona, hæc ✠ múnera, hæc ✠ sancta sacrifícia illibáta: in primis, quæ tibi offérimus pro Ecclésia tua sancta cathólica: quam pacificáre, custodíre, adunáre et régere dignéris toto orbe terrárum: una cum fámulo tuo Papa nostro N. et Antístite nostro N. et ómnibus orthodóxis, atque cathólicæ et apostólicæ fídei cultóribus.', en: 'We therefore humbly pray and beseech thee, most merciful Father, through Jesus Christ thy Son our Lord, that thou wouldst accept and bless these ✠ gifts, these ✠ offerings, these ✠ holy unspotted sacrifices, which in the first place we offer thee for thy holy catholic Church: deign to grant her peace, to protect, unite and govern her throughout the whole world, together with thy servant N. our Pope, and N. our Bishop, and all orthodox believers and professors of the catholic and apostolic faith.'},
    {r: 'Commemoration of the living:'},
    {w: 'P', la: 'Meménto, Dómine, famulórum famularúmque tuárum N. et N. et ómnium circumstántium, quorum tibi fides cógnita est et nota devótio, pro quibus tibi offérimus: vel qui tibi ófferunt hoc sacrifícium laudis, pro se suísque ómnibus: pro redemptióne animárum suárum, pro spe salútis et incolumitátis suæ: tibíque reddunt vota sua ætérno Deo, vivo et vero.', en: 'Be mindful, O Lord, of thy servants and handmaids N. and N., and of all here present, whose faith and devotion are known to thee; for whom we offer, or who offer up to thee, this sacrifice of praise for themselves and all their own, for the redemption of their souls, for the hope of their safety and salvation, and who pay their vows to thee, the eternal, living and true God.'},
    {w: 'P', la: 'Communicántes, et memóriam venerántes, in primis gloriósæ semper Vírginis Maríæ, Genetrícis Dei et Dómini nostri Iesu Christi: sed et beáti Ioseph, eiúsdem Vírginis Sponsi, et beatórum Apostolórum ac Mártyrum tuórum, Petri et Pauli, Andréæ, Iacóbi, Ioánnis, Thomæ, Iacóbi, Philíppi, Bartholomǽi, Matthǽi, Simónis et Thaddǽi: Lini, Cleti, Cleméntis, Xysti, Cornélii, Cypriáni, Lauréntii, Chrysógoni, Ioánnis et Pauli, Cosmæ et Damiáni: et ómnium Sanctórum tuórum; quorum méritis precibúsque concédas, ut in ómnibus protectiónis tuæ muniámur auxílio. Per eúndem Christum Dóminum nostrum. Amen.', en: 'In communion with, and honouring the memory in the first place of the glorious ever-virgin Mary, Mother of our God and Lord Jesus Christ; and also of blessed Joseph, her Spouse, and of thy blessed Apostles and Martyrs, Peter and Paul, Andrew, James, John, Thomas, James, Philip, Bartholomew, Matthew, Simon and Thaddeus; Linus, Cletus, Clement, Xystus, Cornelius, Cyprian, Laurence, Chrysogonus, John and Paul, Cosmas and Damian, and of all thy Saints; by whose merits and prayers grant that we may in all things be defended by the help of thy protection. Through the same Christ our Lord. Amen.'},
    {r: 'Extending his hands over the offerings:'},
    {w: 'P', la: 'Hanc ígitur oblatiónem servitútis nostræ, sed et cunctæ famíliæ tuæ, quǽsumus, Dómine, ut placátus accípias: diésque nostros in tua pace dispónas, atque ab ætérna damnatióne nos éripi, et in electórum tuórum iúbeas grege numerári. Per Christum Dóminum nostrum. Amen.', en: 'We therefore beseech thee, O Lord, graciously to accept this oblation of our service and that of all thy household; order our days in thy peace, and bid us be delivered from eternal damnation and numbered in the flock of thine elect. Through Christ our Lord. Amen.'},
    {w: 'P', la: 'Quam oblatiónem tu, Deus, in ómnibus, quǽsumus, bene ✠ díctam, adscríp ✠ tam, ra ✠ tam, rationábilem, acceptabilémque fácere dignéris: ut nobis Cor ✠ pus et San ✠ guis fiat dilectíssimi Fílii tui Dómini nostri Iesu Christi.', en: 'Which oblation do thou, O God, vouchsafe in all things to make ✠ blessed, ✠ approved, ✠ ratified, reasonable and acceptable; that it may become for us the ✠ Body and ✠ Blood of thy most beloved Son, our Lord Jesus Christ.'},
    {w: 'P', la: 'Qui prídie quam paterétur, accépit panem in sanctas ac venerábiles manus suas, et elevátis óculis in cælum ad te Deum Patrem suum omnipoténtem, tibi grátias agens, bene ✠ díxit, fregit, dedítque discípulis suis, dicens: Accípite, et manducáte ex hoc omnes. HOC EST ENIM CORPUS MEUM.', en: 'Who the day before he suffered took bread into his holy and venerable hands, and with his eyes lifted up to heaven, unto thee, O God, his almighty Father, giving thanks to thee, he ✠ blessed it, broke it, and gave it to his disciples, saying: Take and eat ye all of this. FOR THIS IS MY BODY.'},
    {r: 'He adores, elevates the Sacred Host, and adores again. At a Sung or Solemn Mass the bell is rung and (at a Solemn Mass) the Host is incensed.'},
    {w: 'P', la: 'Símili modo postquam cenátum est, accípiens et hunc præclárum Cálicem in sanctas ac venerábiles manus suas: item tibi grátias agens, bene ✠ díxit, dedítque discípulis suis, dicens: Accípite, et bíbite ex eo omnes. HIC EST ENIM CALIX SÁNGUINIS MEI, NOVI ET ÆTÉRNI TESTAMÉNTI: MYSTÉRIUM FÍDEI: QUI PRO VOBIS ET PRO MULTIS EFFUNDÉTUR IN REMISSIÓNEM PECCATÓRUM.', en: 'In like manner, after he had supped, taking also this excellent chalice into his holy and venerable hands, and giving thanks to thee, he ✠ blessed it, and gave it to his disciples, saying: Take and drink ye all of this. FOR THIS IS THE CHALICE OF MY BLOOD, OF THE NEW AND ETERNAL TESTAMENT: THE MYSTERY OF FAITH: WHICH SHALL BE SHED FOR YOU AND FOR MANY UNTO THE REMISSION OF SINS.'},
    {w: 'P', la: 'Hæc quotiescúmque fecéritis, in mei memóriam faciétis.', en: 'As often as ye shall do these things, ye shall do them in remembrance of me.'},
    {r: 'He adores, elevates the Chalice, and adores again. Then, with his arms extended in the form of a cross:'},
    {w: 'P', la: 'Unde et mémores, Dómine, nos servi tui, sed et plebs tua sancta, eiúsdem Christi Fílii tui Dómini nostri tam beátæ passiónis, nec non et ab ínferis resurrectiónis, sed et in cælos gloriósæ ascensiónis: offérimus præcláræ maiestáti tuæ de tuis donis ac datis, hóstiam ✠ puram, hóstiam ✠ sanctam, hóstiam ✠ immaculátam, Panem ✠ sanctum vitæ ætérnæ, et Cálicem ✠ salútis perpétuæ.', en: 'Wherefore, O Lord, we thy servants, as also thy holy people, calling to mind the blessed passion of the same Christ thy Son our Lord, his resurrection from the dead, and his glorious ascension into heaven, offer unto thy most excellent majesty, of thine own gifts bestowed upon us, a pure ✠ victim, a holy ✠ victim, a spotless ✠ victim, the holy ✠ Bread of eternal life, and the Chalice ✠ of everlasting salvation.'},
    {w: 'P', la: 'Supra quæ propítio ac seréno vultu respícere dignéris: et accépta habére, sícuti accépta habére dignátus es múnera púeri tui iusti Abel, et sacrifícium patriárchæ nostri Abrahæ: et quod tibi óbtulit summus sacérdos tuus Melchísedech, sanctum sacrifícium, immaculátam hóstiam.', en: 'Upon which vouchsafe to look with a propitious and serene countenance, and to accept them, as thou wert graciously pleased to accept the gifts of thy just servant Abel, and the sacrifice of our patriarch Abraham, and that which thy high priest Melchisedech offered to thee, a holy sacrifice, an unspotted victim.'},
    {r: 'Bowing profoundly, with his hands crossed before his breast:'},
    {w: 'P', la: 'Súpplices te rogámus, omnípotens Deus: iube hæc perférri per manus sancti Angeli tui in sublíme altáre tuum, in conspéctu divínæ maiestátis tuæ: ut quotquot ex hac altáris participatióne sacrosánctum Fílii tui Cor ✠ pus et Sán ✠ guinem sumpsérimus, omni benedictióne cælésti et grátia repleámur. Per eúndem Christum Dóminum nostrum. Amen.', en: 'We most humbly beseech thee, almighty God, command these things to be carried by the hands of thy holy Angel to thine altar on high, in the sight of thy divine majesty; that as many of us as, by this participation at the altar, shall receive the most sacred ✠ Body and ✠ Blood of thy Son, may be filled with every heavenly blessing and grace. Through the same Christ our Lord. Amen.'},
    {r: 'Commemoration of the dead:'},
    {w: 'P', la: 'Meménto étiam, Dómine, famulórum famularúmque tuárum N. et N., qui nos præcessérunt cum signo fídei, et dórmiunt in somno pacis. Ipsis, Dómine, et ómnibus in Christo quiescéntibus, locum refrigérii, lucis et pacis, ut indúlgeas, deprecámur. Per eúndem Christum Dóminum nostrum. Amen.', en: 'Be mindful also, O Lord, of thy servants and handmaids N. and N., who are gone before us with the sign of faith, and sleep in the sleep of peace. To these, O Lord, and to all who rest in Christ, grant, we beseech thee, a place of refreshment, light and peace. Through the same Christ our Lord. Amen.'},
    {r: 'Striking his breast and raising his voice a little:'},
    {w: 'P', la: 'Nobis quoque peccatóribus fámulis tuis, de multitúdine miseratiónum tuárum sperántibus, partem áliquam et societátem donáre dignéris, cum tuis sanctis Apóstolis et Martýribus: cum Ioánne, Stéphano, Matthía, Bárnaba, Ignátio, Alexándro, Marcellíno, Petro, Felicitáte, Perpétua, Agatha, Lúcia, Agnéte, Cæcília, Anastásia, et ómnibus Sanctis tuis: intra quorum nos consórtium, non æstimátor mériti, sed véniæ, quǽsumus, largítor admítte. Per Christum Dóminum nostrum.', en: 'To us sinners also, thy servants, hoping in the multitude of thy mercies, vouchsafe to grant some part and fellowship with thy holy Apostles and Martyrs: with John, Stephen, Matthias, Barnabas, Ignatius, Alexander, Marcellinus, Peter, Felicitas, Perpetua, Agatha, Lucy, Agnes, Cecilia, Anastasia, and all thy Saints: into whose company we beseech thee to admit us, not weighing our merits, but freely pardoning our offences. Through Christ our Lord.'},
    {w: 'P', la: 'Per quem hæc ómnia, Dómine, semper bona creas, sancti ✠ fícas, vivi ✠ fícas, bene ✠ dícis, et præstas nobis. Per ip ✠ sum, et cum ip ✠ so, et in ip ✠ so, est tibi Deo Patri ✠ omnipoténti, in unitáte Spíritus ✠ Sancti, omnis honor et glória.', en: 'By whom, O Lord, thou dost always create, ✠ sanctify, ✠ quicken, ✠ bless and bestow upon us all these good things. Through ✠ him, and with ✠ him, and in ✠ him, is unto thee, God the Father ✠ almighty, in the unity of the Holy ✠ Ghost, all honour and glory.'},
    {w: 'P', la: 'Per ómnia sǽcula sæculórum.', en: 'World without end.'},
    {w: 'S', la: 'Amen.', en: 'Amen.'}
  ]},
  pater: {la: 'Pater noster', en: 'The Lord’s Prayer', lines: [
    {w: 'P', la: 'Orémus. Præcéptis salutáribus móniti, et divína institutióne formáti, audémus dícere:', en: 'Let us pray. Admonished by saving precepts, and following the divine institution, we make bold to say:'},
    {w: 'P', la: 'Pater noster, qui es in cælis, sanctificétur nomen tuum: advéniat regnum tuum: fiat volúntas tua, sicut in cælo, et in terra. Panem nostrum quotidiánum da nobis hódie: et dimítte nobis débita nostra, sicut et nos dimíttimus debitóribus nostris. Et ne nos indúcas in tentatiónem.', en: 'Our Father, who art in heaven, hallowed be thy name; thy kingdom come; thy will be done on earth as it is in heaven. Give us this day our daily bread; and forgive us our trespasses, as we forgive them that trespass against us. And lead us not into temptation.'},
    {w: 'S', la: 'Sed líbera nos a malo.', en: 'But deliver us from evil.'},
    {w: 'P', la: 'Amen.', en: 'Amen.'},
    {w: 'P', la: 'Líbera nos, quǽsumus, Dómine, ab ómnibus malis prætéritis, præséntibus et futúris: et intercedénte beáta et gloriósa semper Vírgine Dei Genetríce María, cum beátis Apóstolis tuis Petro et Paulo, atque Andréa, et ómnibus Sanctis, da propítius pacem in diébus nostris: ut, ope misericórdiæ tuæ adiúti, et a peccáto simus semper líberi et ab omni perturbatióne secúri. Per eúndem Dóminum nostrum Iesum Christum Fílium tuum, qui tecum vivit et regnat in unitáte Spíritus Sancti Deus,', en: 'Deliver us, we beseech thee, O Lord, from all evils, past, present and to come; and by the intercession of the blessed and glorious ever-virgin Mary, Mother of God, together with thy blessed Apostles Peter and Paul, and Andrew, and all the Saints, mercifully grant peace in our days; that, aided by the help of thy mercy, we may be always free from sin and secure from all disturbance. Through the same Jesus Christ thy Son our Lord, who liveth and reigneth with thee in the unity of the Holy Ghost, God,'},
    {r: 'Having broken the Host, he says aloud:'},
    {w: 'P', la: 'Per ómnia sǽcula sæculórum.', en: 'World without end.'},
    {w: 'S', la: 'Amen.', en: 'Amen.'},
    {r: 'Making the sign of the cross three times over the chalice with the particle:'},
    {w: 'P', la: 'Pax ✠ Dómini sit ✠ semper vobís ✠ cum.', en: 'The peace ✠ of the Lord ✠ be always with ✠ you.'},
    {w: 'S', la: 'Et cum spíritu tuo.', en: 'And with thy spirit.'}
  ]},
  agLow: {la: 'Agnus Dei', en: 'Agnus Dei', lines: [
    {w: 'P', la: 'Agnus Dei, qui tollis peccáta mundi: miserére nobis. Agnus Dei, qui tollis peccáta mundi: miserére nobis. Agnus Dei, qui tollis peccáta mundi: dona nobis pacem.', en: 'Lamb of God, who takest away the sins of the world, have mercy on us. Lamb of God, who takest away the sins of the world, have mercy on us. Lamb of God, who takest away the sins of the world, grant us peace.'},
    {r: 'In Masses for the Dead: dona eis réquiem (twice), dona eis réquiem sempitérnam.'}
  ]},
  communion: {la: 'Communio', en: 'Communion', lines: [
    {r: 'Placing the particle in the chalice, the priest says:'},
    {w: 'P', la: 'Hæc sacrosáncta commíxtio Córporis et Sánguinis Dómini nostri Iesu Christi fiat mihi et ómnibus suméntibus salus mentis et córporis, et ad vitam ætérnam promeréndam et capesséndam præparátio salutáris. Per eúndem Christum Dóminum nostrum. Amen.', en: 'May this most holy mingling of the Body and Blood of our Lord Jesus Christ be to me and to all who receive it health of mind and body, and a saving preparation for the meriting and the obtaining of eternal life. Through the same Christ our Lord. Amen.'},
    {m: 'm', r: 'At a Solemn Mass the priest gives the kiss of peace to the deacon, who gives it to the subdeacon, and he to the choir (not in Masses for the Dead).'},
    {r: 'Bowing, he says:'},
    {w: 'P', la: 'Dómine Iesu Christe, Fili Dei vivi, qui ex voluntáte Patris, cooperánte Spíritu Sancto, per mortem tuam mundum vivificásti: líbera me per hoc sacrosánctum Corpus et Sánguinem tuum ab ómnibus iniquitátibus meis et univérsis malis: et fac me tuis semper inhærére mandátis, et a te numquam separári permíttas. Qui cum eódem Deo Patre et Spíritu Sancto vivis et regnas Deus, in sǽcula sæculórum. Amen.', en: 'O Lord Jesus Christ, Son of the living God, who by the will of the Father, the Holy Ghost cooperating, hast by thy death given life to the world: deliver me by this thy most sacred Body and Blood from all my iniquities and from all evils; make me always cleave to thy commandments, and never suffer me to be separated from thee. Who with the same God the Father and the Holy Ghost livest and reignest God, world without end. Amen.'},
    {r: 'Taking the Host and the chalice together, he says:'},
    {w: 'P', la: 'Corpus et Sanguis Dómini nostri Iesu Christi custódiant me in vitam ætérnam. Amen.', en: 'May the Body and Blood of our Lord Jesus Christ keep me unto life everlasting. Amen.'},
    {r: 'Communion of the faithful. The priest, holding up a Host, says:'},
    {w: 'P', la: 'Ecce Agnus Dei, ecce qui tollit peccáta mundi.', en: 'Behold the Lamb of God, behold him who taketh away the sins of the world.'},
    {r: 'And three times:'},
    {w: 'P', la: 'Dómine, non sum dignus, ut intres sub tectum meum: sed tantum dic verbo, et sanábitur ánima mea.', en: 'Lord, I am not worthy that thou shouldst enter under my roof; but only say the word, and my soul shall be healed.'},
    {r: 'Giving Communion to each:'},
    {w: 'P', la: 'Corpus Dómini nostri Iesu Christi custódiat te in vitam ætérnam. Amen.', en: 'May the Body of our Lord Jesus Christ keep thee unto life everlasting. Amen.'},
    {r: 'At the ablutions the priest says:'},
    {w: 'P', la: 'Quod ore súmpsimus, Dómine, pura mente capiámus: ut de Córpore et Sánguine Dómini nostri Iesu Christi fiat nobis remédium sempitérnum. Amen.', en: 'What we have taken with our mouth, O Lord, may we receive with a pure mind; that from the Body and Blood of our Lord Jesus Christ there may come to us an everlasting remedy. Amen.'},
    {r: 'Then he reads the Communion antiphon at the Epistle side:'}
  ]},
  post: {la: 'Postcommunio', en: 'Postcommunion', lines: [
    {w: 'P', la: 'Dóminus vobíscum.', en: 'The Lord be with you.'},
    {w: 'S', la: 'Et cum spíritu tuo.', en: 'And with thy spirit.'},
    {w: 'P', la: 'Orémus.', en: 'Let us pray.'}
  ]},
  postEnd: {la: 'Dimissio', en: 'Dismissal', lines: [
    {w: 'P', la: 'Dóminus vobíscum.', en: 'The Lord be with you.'},
    {w: 'S', la: 'Et cum spíritu tuo.', en: 'And with thy spirit.'},
    {m: 'm', r: 'The deacon sings the dismissal.'}
  ]},
  end: {la: 'Finis Missæ', en: 'The end of Mass', lines: [
    {r: 'Bowing before the middle of the altar, the priest says:'},
    {w: 'P', la: 'Pláceat tibi, sancta Trínitas, obséquium servitútis meæ: et præsta, ut sacrifícium, quod óculis tuæ maiestátis indígnus óbtuli, tibi sit acceptábile, mihíque et ómnibus pro quibus illud óbtuli, sit, te miseránte, propitiábile. Per Christum Dóminum nostrum. Amen.', en: 'May the homage of my service be pleasing to thee, O holy Trinity; and grant that the sacrifice which I, unworthy, have offered in the sight of thy majesty may be acceptable to thee, and through thy mercy be a propitiation for me and for all those for whom I have offered it. Through Christ our Lord. Amen.'},
    {r: 'He kisses the altar, turns to the people and blesses them (not in Masses for the Dead):'},
    {w: 'P', la: 'Benedíctio Dei omnipoténtis, Pa ✠ tris, et Fílii, et Spíritus Sancti, descéndat super vos et máneat semper.', en: 'May the blessing of almighty God, the Father ✠, and the Son, and the Holy Ghost, descend upon you and remain for ever.'},
    {w: 'S', la: 'Amen.', en: 'Amen.'},
    {r: 'At the Gospel side:'},
    {w: 'P', la: 'Dóminus vobíscum.', en: 'The Lord be with you.'},
    {w: 'S', la: 'Et cum spíritu tuo.', en: 'And with thy spirit.'},
    {w: 'P', la: 'Inítium sancti Evangélii secúndum Ioánnem.', en: 'The beginning of the holy Gospel according to John.'},
    {w: 'S', la: 'Glória tibi, Dómine.', en: 'Glory be to thee, O Lord.'},
    {w: 'P', la: 'In princípio erat Verbum, et Verbum erat apud Deum, et Deus erat Verbum. Hoc erat in princípio apud Deum. Omnia per ipsum facta sunt: et sine ipso factum est nihil, quod factum est: in ipso vita erat, et vita erat lux hóminum: et lux in ténebris lucet, et ténebræ eam non comprehendérunt. Fuit homo missus a Deo, cui nomen erat Ioánnes. Hic venit in testimónium, ut testimónium perhibéret de lúmine, ut omnes créderent per illum. Non erat ille lux, sed ut testimónium perhibéret de lúmine. Erat lux vera, quæ illúminat omnem hóminem veniéntem in hunc mundum. In mundo erat, et mundus per ipsum factus est, et mundus eum non cognóvit. In própria venit, et sui eum non recepérunt. Quotquot autem recepérunt eum, dedit eis potestátem fílios Dei fíeri, his, qui credunt in nómine eius: qui non ex sanguínibus, neque ex voluntáte carnis, neque ex voluntáte viri, sed ex Deo nati sunt. (Hic genuflectitur.) Et Verbum caro factum est, et habitávit in nobis: et vídimus glóriam eius, glóriam quasi Unigéniti a Patre, plenum grátiæ et veritátis.', en: 'In the beginning was the Word, and the Word was with God, and the Word was God. The same was in the beginning with God. All things were made by him: and without him was made nothing that was made. In him was life, and the life was the light of men: and the light shineth in darkness, and the darkness did not comprehend it. There was a man sent from God, whose name was John. This man came for a witness, to give testimony of the light, that all men might believe through him. He was not the light, but was to give testimony of the light. That was the true light, which enlighteneth every man that cometh into this world. He was in the world, and the world was made by him, and the world knew him not. He came unto his own, and his own received him not. But as many as received him, he gave them power to be made the sons of God, to them that believe in his name: who are born, not of blood, nor of the will of the flesh, nor of the will of man, but of God. (Here all kneel.) And the Word was made flesh, and dwelt among us: and we saw his glory, the glory as it were of the only-begotten of the Father, full of grace and truth.'},
    {w: 'S', la: 'Deo grátias.', en: 'Thanks be to God.'}
  ]},
  dismiss: {
    ite: [{w: 'P', la: 'Ite, missa est.', en: 'Go, the Mass is ended.'}, {w: 'S', la: 'Deo grátias.', en: 'Thanks be to God.'}],
    ben: [{w: 'P', la: 'Benedicámus Dómino.', en: 'Let us bless the Lord.'}, {w: 'S', la: 'Deo grátias.', en: 'Thanks be to God.'}],
    req: [{w: 'P', la: 'Requiéscant in pace.', en: 'May they rest in peace.'}, {w: 'S', la: 'Amen.', en: 'Amen.'}]
  }
};
