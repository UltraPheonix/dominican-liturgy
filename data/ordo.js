/* Ordo Missæ secundum ritum Ordinis Prædicatorum (Missale O.P. 1939).
   Latin after the Missale O.P.; English of the prayers after the St Dominic Missal (1959) and Divinum Officium; the English of the
   rubrics is our own (AI) translation. Each section is a list of lines: {r: rubric} or {w: speaker, la: Latin, en: English}.
   m limits a line to some forms of Mass: l = Low Mass, s = Sung Mass, m = Solemn Mass, c = Conventual Mass (default: all).
   if limits a line to a circumstance: chosen on the Mass page, tab (the Sacrament in the tabernacle on this altar), exp (exposed),
   sac (either), pope, bp (a Cardinal Legate, Patriarch, Archbishop or Bishop in his jurisdiction), prel (either), mo (the Master
   of the Order), one (one acolyte), full (acolytes and thurifer); or of the day, req (a Mass for the Dead), flect (Flectamus genua),
   sp (a Prayer over the people), adjuva (the Tract Domine non secundum), veni (the Alleluia Veni Sancte Spiritus), nogl (no Gloria),
   sun (Sunday), dup (a Double or higher), td (Totum Duplex), sd (Sunday or Double), thur (a day with incense: Sundays, Simple feasts
   and above, the weekday votive Masses of the Order), sol (the greatest feasts), chgl / chky / chin (the subdeacon brings the
   chalice during the Gloria / during the Kyrie / at the entrance); "!" negates, "," joins (all must hold).
   ref: the paragraphs of the Missal's rubrics (rubrics.html, data/rubtext.js) behind a direction, opened from it on the Mass page.
   Sections marked strip are directions without a heading, set before a chant of the Proper or the Ordinary.
   Each section has two forms: lines, with only the rubrics printed in the Ordo Missae of the Missal (pp. 191-193, 205-210), and adv,
   the full directions of its Ritus servandus (shown when "Full" rubrics is chosen); a section without adv is the same in both.
   Built by tools/rubrics/ordo_directions.py. */
window.ORDO = {
  chalice: {la: "Præparatio calicis", en: "Preparation of the chalice", lines: [
    {"w": "S", "la": "Benedícite.", "en": "Bless.", "if": "!req"},
    {"w": "P", "la": "In nómine Patris, et Fílii, et Spíritus Sancti.", "en": "In the name of the Father, and of the Son, and of the Holy Ghost.", "if": "!req"},
    {"w": "S", "la": "Amen.", "en": "Amen.", "if": "!req"}
  ], adv: [
    {"m": "l", "if": "!sac", "r": "Coming to the altar, he bows profoundly at the middle, goes up, and sets the chalice towards the Gospel side.", "ref": ["praeparatio-ii-8"]},
    {"m": "l", "if": "tab", "r": "Coming to the altar, he genuflects at the middle (the Sacrament is in the tabernacle), goes up, and sets the chalice towards the Gospel side.", "ref": ["praeparatio-ii-8"]},
    {"m": "l", "if": "exp", "r": "Coming to the altar, he kneels on both knees before the Sacrament exposed, then goes up and sets the chalice towards the Gospel side.", "ref": ["praeparatio-ii-8", "varia-ii-3"]},
    {"m": "l", "r": "He spreads the corporal in the middle, lays the paten with the host on it, and the purificator at its right.", "ref": ["praeparatio-ii-8"]},
    {"m": "l", "if": "!req", "r": "He pours a little wine into the chalice. Holding out the water, the server says:", "ref": ["praeparatio-ii-9"]},
    {"m": "l", "if": "req", "r": "He pours a little wine into the chalice, and adds a very little water.", "ref": ["praeparatio-ii-9"]},
    {"m": "s", "if": "!req", "r": "The chalice is prepared while the Gradual is sung. Holding out the water, the server says:"},
    {"m": "mc", "r": "After reading the Gospel at his seat, the priest sits again. The subdeacon, wearing the veil, brings the chalice and prepares it before him.", "ref": ["ministri-vi-4"]},
    {"m": "mc", "r": "He hands the paten with the host to the deacon, who shows it to the priest, and pours in as much wine as the priest indicates.", "ref": ["ministri-vi-4"]},
    {"m": "mc", "if": "!req", "r": "Holding out the water, the subdeacon says:", "ref": ["ministri-vi-4"]},
    {"w": "S", "la": "Benedícite.", "en": "Bless.", "if": "!req"},
    {"m": "mc", "if": "!req", "w": "D", "la": "Dóminus.", "en": "The Lord."},
    {"if": "!req", "r": "The priest blesses the water:", "ref": ["praeparatio-ii-9"]},
    {"w": "P", "la": "In nómine Patris, et Fílii, et Spíritus Sancti.", "en": "In the name of the Father, and of the Son, and of the Holy Ghost.", "if": "!req"},
    {"w": "S", "la": "Amen.", "en": "Amen.", "if": "!req"},
    {"m": "l", "if": "!req", "r": "He adds so little water that it can very easily be changed into wine, and wipes the chalice.", "ref": ["praeparatio-ii-9"]},
    {"m": "l", "r": "He sets the paten with the host on the chalice, covers it with the pall and veil, and places it on the corporal.", "ref": ["praeparatio-ii-9"]},
    {"m": "l", "r": "He opens the Missal at the Epistle corner and finds the Mass.", "ref": ["praeparatio-ii-9"]},
    {"m": "mc", "r": "The subdeacon adds a little water, takes back the paten, carries the chalice to the middle of the altar, covers it, and returns to his seat.", "ref": ["ministri-vi-4"]}
  ]},
  foot: {la: "Ad pedem altaris", en: "At the foot of the altar", lines: [
    {"w": "P", "la": "Actiónes nostras, quǽsumus, Dómine, aspirándo prǽveni et adiuvándo proséquere: ut cuncta nostra operátio a te semper incípiat, et per te cœpta finiátur. Per Christum Dóminum nostrum. Amen.", "en": "Prevent, O Lord, we beseech thee, our actions by thy inspiration, and continue them by thine assistance; that every one of our works may begin always from thee, and through thee be ended. Through Christ our Lord. Amen."},
    {"r": "The priest, when he is about to celebrate, comes to the middle of the altar, makes a profound bow, and standing signs himself with the sign of the cross, saying in a clear and audible voice:"},
    {"w": "P", "la": "In nómine Patris, et Fílii, et Spíritus Sancti. Amen.", "en": "In the name of the Father, and of the Son, and of the Holy Ghost. Amen."},
    {"r": "Then in the same voice:"},
    {"w": "P", "la": "Confitémini Dómino quóniam bonus.", "en": "Give praise to the Lord, for he is good."},
    {"w": "S", "la": "Quóniam in sǽculum misericórdia eius.", "en": "For his mercy endureth for ever."},
    {"r": "Then, bowing profoundly, he says:"},
    {"w": "P", "la": "Confíteor Deo omnipoténti, et beátæ Maríæ semper Vírgini, et beáto Domínico patri nostro, et ómnibus Sanctis, et vobis, fratres, quia peccávi nimis cogitatióne, locutióne, ópere et omissióne, mea culpa: precor vos oráre pro me.", "en": "I confess to almighty God, to blessed Mary ever a virgin, to blessed Dominic our father, to all the saints, and to you, brethren, that I have sinned exceedingly in thought, word, deed and omission, through my fault: I beseech you to pray for me."},
    {"w": "S", "la": "Misereátur tui omnípotens Deus, et dimíttat tibi ómnia peccáta tua: líberet te ab omni malo, salvet et confírmet in omni ópere bono, et perdúcat te ad vitam ætérnam.", "en": "May almighty God have mercy on thee and forgive thee all thy sins: may he deliver thee from all evil, save and strengthen thee in every good work, and bring thee to life everlasting."},
    {"w": "P", "la": "Amen.", "en": "Amen."},
    {"m": "l", "r": "Then the server repeats the Confession, and where the priest said vobis, fratres and vos, he says tibi, pater and te."},
    {"m": "smc", "r": "Then the ministers repeat the Confession, and where the priest said vobis, fratres and vos, they say tibi, pater and te."},
    {"w": "S", "la": "Confíteor Deo omnipoténti, et beátæ Maríæ semper Vírgini, et beáto Domínico patri nostro, et ómnibus Sanctis, et tibi, pater, quia peccávi nimis cogitatióne, locutióne, ópere et omissióne, mea culpa: precor te oráre pro me.", "en": "I confess to almighty God, to blessed Mary ever a virgin, to blessed Dominic our father, to all the saints, and to thee, father, that I have sinned exceedingly in thought, word, deed and omission, through my fault: I beseech thee to pray for me."},
    {"r": "This said, the priest says:"},
    {"w": "P", "la": "Misereátur vestri omnípotens Deus, et dimíttat vobis ómnia peccáta vestra: líberet vos ab omni malo, salvet et confírmet in omni ópere bono, et perdúcat vos ad vitam ætérnam.", "en": "May almighty God have mercy on you and forgive you all your sins: may he deliver you from all evil, save and strengthen you in every good work, and bring you to life everlasting."},
    {"w": "S", "la": "Amen.", "en": "Amen."},
    {"w": "P", "la": "Absolutiónem et remissiónem ómnium peccatórum vestrórum tríbuat vobis omnípotens et miséricors Dóminus.", "en": "May the almighty and merciful Lord grant you pardon and remission of all your sins."},
    {"w": "S", "la": "Amen.", "en": "Amen."},
    {"r": "The Confession and absolution made, the priest stands erect and says:"},
    {"w": "P", "la": "Adiutórium nostrum in nómine Dómini.", "en": "Our help is in the name of the Lord."},
    {"w": "S", "la": "Qui fecit cælum et terram.", "en": "Who made heaven and earth."},
    {"r": "And going up to the altar, bowing profoundly again, he says the prayer:"},
    {"w": "P", "la": "Aufer a nobis, Dómine, cunctas iniquitátes nostras: ut ad Sancta sanctórum puris mereámur méntibus introíre. Per Christum Dóminum nostrum. Amen.", "en": "Take away from us all our iniquities, O Lord, that we may be worthy to enter with pure minds into the Holy of Holies. Through Christ our Lord. Amen."},
    {"r": "This prayer said, he kisses the altar, first signing it in the middle with his right thumb; and standing erect he signs himself, and going to the book with hands joined before his breast, begins the Office, or Introit, of the Mass."}
  ], adv: [
    {"m": "l", "r": "He returns to the middle of the altar, uncovers his head, and says secretly:", "ref": ["praeparatio-ii-10"]},
    {"m": "mc", "if": "!chin,!req", "r": "When the choir begins the Gloria Patri of the Introit, the ministers go to the altar: the acolytes with their candles, the subdeacon with the Gospel book, the deacon with the Missal, and last the priest.", "ref": ["ministri-iii-1"]},
    {"m": "mc", "if": "chin,!req", "r": "When the choir begins the Gloria Patri of the Introit, the ministers go to the altar: the acolytes with their candles, the subdeacon carrying the prepared chalice, the deacon with the Missal, and last the priest.", "ref": ["ministri-iii-1"]},
    {"m": "mc", "if": "!chin,req", "r": "When the choir begins the verse Te decet of the Introit (there is no Gloria Patri), the ministers go to the altar: the acolytes with their candles, the subdeacon with the Gospel book, the deacon with the Missal, and last the priest.", "ref": ["ministri-iii-1"]},
    {"m": "mc", "if": "chin,req", "r": "When the choir begins the verse Te decet of the Introit (there is no Gloria Patri), the ministers go to the altar: the acolytes with their candles, the subdeacon carrying the prepared chalice, the deacon with the Missal, and last the priest.", "ref": ["ministri-iii-1"]},
    {"m": "mc", "if": "!sac", "r": "Below the lowest step they stand in line, the deacon at the priest’s right, the subdeacon at his left, an acolyte at each end. All bow profoundly and uncover their heads.", "ref": ["ministri-iii-2"]},
    {"m": "mc", "if": "tab", "r": "Below the lowest step they stand in line, the deacon at the priest’s right, the subdeacon at his left, an acolyte at each end. All genuflect and uncover their heads.", "ref": ["ministri-iii-2", "praeparatio-ii-8"]},
    {"m": "mc", "if": "exp", "r": "Below the lowest step they stand in line, the deacon at the priest’s right, the subdeacon at his left, an acolyte at each end. All kneel on both knees and uncover their heads.", "ref": ["ministri-iii-2", "varia-ii-3"]},
    {"m": "mc", "r": "Rising, the priest says secretly:", "ref": ["ministri-iii-2"]},
    {"m": "s", "r": "Before beginning, the priest says secretly:"},
    {"w": "P", "la": "Actiónes nostras, quǽsumus, Dómine, aspirándo prǽveni et adiuvándo proséquere: ut cuncta nostra operátio a te semper incípiat, et per te cœpta finiátur. Per Christum Dóminum nostrum. Amen.", "en": "Prevent, O Lord, we beseech thee, our actions by thy inspiration, and continue them by thine assistance; that every one of our works may begin always from thee, and through thee be ended. Through Christ our Lord. Amen."},
    {"if": "exp", "r": "Whenever the priest comes to the middle of the altar, leaves it or passes it, he genuflects (the server or ministers with him); no one ever turns his back to the Sacrament.", "ref": ["varia-ii-4", "varia-ii-6"]},
    {"m": "l", "if": "exp", "r": "The server genuflects whenever he passes the middle.", "ref": ["varia-vi-6"]},
    {"m": "mc", "if": "exp", "r": "The deacon kisses neither the priest’s hand nor his shoulder when he hands him anything.", "ref": ["varia-ii-6"]},
    {"if": "pope", "r": "The priest first kneels below the lowest step on the Gospel side, facing the Pope, and waits for his blessing; then he rises and, turned partly towards the altar, begins.", "ref": ["varia-iii-1"]},
    {"if": "bp", "r": "The priest first stands below the lowest step on the Gospel side; at the Bishop’s sign he bows profoundly to him, then turns to the altar and begins.", "ref": ["varia-iii-1"]},
    {"m": "ls", "r": "Standing just below the top step, he bows profoundly and signs himself, saying aloud:", "ref": ["modus-i-1"]},
    {"m": "mc", "r": "He signs himself, saying aloud:", "ref": ["ministri-iii-2"]},
    {"w": "P", "la": "In nómine Patris, et Fílii, et Spíritus Sancti. Amen.", "en": "In the name of the Father, and of the Son, and of the Holy Ghost. Amen."},
    {"w": "P", "la": "Confitémini Dómino quóniam bonus.", "en": "Give praise to the Lord, for he is good."},
    {"w": "S", "la": "Quóniam in sǽculum misericórdia eius.", "en": "For his mercy endureth for ever."},
    {"r": "Bowing profoundly, with hands joined, he says in a moderate voice (he does not strike his breast):", "ref": ["modus-i-2"]},
    {"m": "mc", "r": "The ministers bow with him, without bending the knee; the acolytes stand upright, facing each other.", "ref": ["ministri-iii-2"]},
    {"m": "mc", "if": "pope", "r": "He makes the Confession with the Pope, standing at his left, and says tibi, Pater and te, Pater instead of vobis, fratres and vos, fratres.", "ref": ["varia-iii-2"]},
    {"m": "mc", "if": "bp", "r": "He makes the Confession with the Bishop, standing at his left, and says tibi, Pater and te, Pater instead of vobis, fratres and vos, fratres.", "ref": ["varia-iii-2"]},
    {"w": "P", "la": "Confíteor Deo omnipoténti, et beátæ Maríæ semper Vírgini, et beáto Domínico patri nostro, et ómnibus Sanctis, et vobis, fratres, quia peccávi nimis cogitatióne, locutióne, ópere et omissióne, mea culpa: precor vos oráre pro me.", "en": "I confess to almighty God, to blessed Mary ever a virgin, to blessed Dominic our father, to all the saints, and to you, brethren, that I have sinned exceedingly in thought, word, deed and omission, through my fault: I beseech you to pray for me."},
    {"m": "l", "r": "The server, kneeling at his left, answers:", "ref": ["varia-vi-4"]},
    {"w": "S", "la": "Misereátur tui omnípotens Deus, et dimíttat tibi ómnia peccáta tua: líberet te ab omni malo, salvet et confírmet in omni ópere bono, et perdúcat te ad vitam ætérnam.", "en": "May almighty God have mercy on thee and forgive thee all thy sins: may he deliver thee from all evil, save and strengthen thee in every good work, and bring thee to life everlasting."},
    {"w": "P", "la": "Amen.", "en": "Amen."},
    {"r": "Then the Confiteor is said to the priest, with tibi, pater and te, pater:", "ref": ["modus-i-2"]},
    {"w": "S", "la": "Confíteor Deo omnipoténti, et beátæ Maríæ semper Vírgini, et beáto Domínico patri nostro, et ómnibus Sanctis, et tibi, pater, quia peccávi nimis cogitatióne, locutióne, ópere et omissióne, mea culpa: precor te oráre pro me.", "en": "I confess to almighty God, to blessed Mary ever a virgin, to blessed Dominic our father, to all the saints, and to thee, father, that I have sinned exceedingly in thought, word, deed and omission, through my fault: I beseech thee to pray for me."},
    {"w": "P", "la": "Misereátur vestri omnípotens Deus, et dimíttat vobis ómnia peccáta vestra: líberet vos ab omni malo, salvet et confírmet in omni ópere bono, et perdúcat vos ad vitam ætérnam.", "en": "May almighty God have mercy on you and forgive you all your sins: may he deliver you from all evil, save and strengthen you in every good work, and bring you to life everlasting."},
    {"w": "S", "la": "Amen.", "en": "Amen."},
    {"r": "Without making the sign of the cross:", "ref": ["modus-i-3"]},
    {"w": "P", "la": "Absolutiónem et remissiónem ómnium peccatórum vestrórum tríbuat vobis omnípotens et miséricors Dóminus.", "en": "May the almighty and merciful Lord grant you pardon and remission of all your sins."},
    {"w": "S", "la": "Amen.", "en": "Amen."},
    {"r": "Standing erect, with hands joined:", "ref": ["modus-i-3"]},
    {"w": "P", "la": "Adiutórium nostrum in nómine Dómini.", "en": "Our help is in the name of the Lord."},
    {"w": "S", "la": "Qui fecit cælum et terram.", "en": "Who made heaven and earth."},
    {"m": "mc", "if": "pope", "r": "He genuflects to the Pope.", "ref": ["varia-iii-3"]},
    {"m": "mc", "if": "bp", "r": "He bows profoundly to the Bishop.", "ref": ["varia-iii-3"]},
    {"r": "He goes up to the altar and, bowing profoundly towards its middle, says secretly:", "ref": ["modus-i-4", "ministri-iii-3"]},
    {"w": "P", "la": "Aufer a nobis, Dómine, cunctas iniquitátes nostras: ut ad Sancta sanctórum puris mereámur méntibus introíre. Per Christum Dóminum nostrum. Amen.", "en": "Take away from us all our iniquities, O Lord, that we may be worthy to enter with pure minds into the Holy of Holies. Through Christ our Lord. Amen."},
    {"r": "At Per Christum he makes a cross on the altar with his thumb and kisses it, his hands laid on the altar.", "ref": ["modus-i-4"]},
    {"r": "Standing, he signs himself, saying secretly In nomine Patris, et Filii, et Spiritus Sancti. Amen, and goes with hands joined to the Missal at the Epistle corner.", "ref": ["modus-i-4"]},
    {"m": "mc", "r": "Meanwhile the deacon places the Missal at the Epistle corner and the subdeacon the Gospel book at the Gospel corner; the acolytes set their candles down on the steps and put them out.", "ref": ["ministri-iii-3"]}
  ]},
  rAs: {la: "", en: "", strip: 1, lines: [

  ], adv: [
    {"m": "mc", "r": "On Sundays, when the Hour before Mass is finished, the priest (in alb, stole and maniple, or in a cope if there is to be a procession) comes to the sanctuary with the ministers and acolytes; all bow profoundly before the altar.", "ref": ["ministri-ii-1"]},
    {"m": "mc", "r": "As the cantors begin Asperges me, the priest sprinkles the altar, then the deacon, subdeacon and acolytes.", "ref": ["ministri-ii-2"]},
    {"m": "c", "if": "mo", "r": "He is sprinkled next.", "ref": ["ministri-ii-2"]},
    {"m": "c", "if": "dup", "r": "Then the cantors, and the brethren, beginning with the right choir; then the lay brothers, and the seculars in choir.", "ref": ["ministri-ii-2"]},
    {"m": "c", "if": "!dup", "r": "Then the brethren, beginning with the right choir; then the lay brothers, and the seculars in choir.", "ref": ["ministri-ii-2"]},
    {"m": "m", "r": "Then the people.", "ref": ["ministri-ii-2"]},
    {"m": "mc", "r": "When the antiphon is finished, standing before the steps, the priest says the versicles and the prayer; then all return to the sacristy.", "ref": ["ministri-ii-3"]}
  ]},
  rIn: {la: "", en: "", strip: 1, lines: [

  ], adv: [
    {"m": "ls", "if": "!req", "r": "At the Epistle corner he reads the Introit aloud, bowing towards the cross at Gloria Patri, and repeats the antiphon.", "ref": ["modus-ii-1"]},
    {"m": "ls", "if": "req", "r": "At the Epistle corner he reads the Introit aloud and repeats the antiphon.", "ref": ["modus-ii-1", "varia-iv-1"]},
    {"m": "mc", "r": "The ministers stand at the priest’s right in order, and say the Introit and the Kyrie with him; the deacon turns the pages.", "ref": ["ministri-iii-4"]},
    {"m": "mc", "r": "Then the deacon stands behind the priest and the subdeacon behind the deacon; the acolytes stand below the steps.", "ref": ["ministri-iii-5"]}
  ]},
  rKy: {la: "", en: "", strip: 1, lines: [
    {"m": "l", "r": "The Introit finished, he says alternately with the server:"},
    {"m": "smc", "r": "The Introit finished, he says alternately with the ministers:"}
  ], adv: [
    {"m": "l", "r": "He says the Kyrie alternately with the server.", "ref": ["modus-ii-1"]},
    {"m": "mc", "if": "sd", "r": "They may sit at the Epistle side, the deacon at the priest’s left and the subdeacon at the deacon’s left; an acolyte spreads a cloth over their knees.", "ref": ["ministri-iii-6"]},
    {"m": "mc", "if": "sd", "r": "At the last Kyrie an acolyte takes up the cloth, beginning with the priest and kissing his hand.", "ref": ["ministri-iii-6"]},
    {"m": "mc", "if": "chky", "r": "During the Kyrie the subdeacon, wearing the veil, brings the chalice from the sacristy and sets it on the Epistle corner.", "ref": ["ministri-iv-2"]}
  ]},
  rGl: {la: "", en: "", strip: 1, lines: [
    {"r": "Then, going to the middle of the altar, he says the Gloria (if it is to be said), bowing his head at Deo, at Adoramus te, at Gratias agimus tibi, at Jesu Christe, at suscipe deprecationem nostram, and again at Jesu Christe."}
  ], adv: [
    {"m": "ls", "if": "exp", "r": "He genuflects as he comes to the middle, and again as he leaves it.", "ref": ["varia-ii-4"]},
    {"m": "l", "r": "He goes to the middle. At Gloria he lays his hands on the altar; at in excelsis he raises them; at Deo he joins them and bows.", "ref": ["modus-ii-2"]},
    {"m": "l", "r": "He continues at the Epistle corner with hands joined, bowing at Adoramus te, Gratias agimus tibi, Jesu Christe and Suscipe deprecationem nostram.", "ref": ["modus-ii-2"]},
    {"m": "s", "r": "He intones the Gloria at the middle of the altar, with the same gestures, and continues it at the Epistle corner, bowing at the same words.", "ref": ["modus-ii-2", "ministri-iv-1"]},
    {"m": "mc", "r": "All rise and bow before the middle; the priest goes up and intones the Gloria. They continue it with him at the Epistle corner, standing at his right.", "ref": ["ministri-iv-1"]},
    {"m": "mc", "r": "When they have said it, the priest and deacon stand until the choir has finished.", "ref": ["ministri-iv-1"]},
    {"m": "mc", "if": "chgl", "r": "Meanwhile the subdeacon goes with an acolyte to the sacristy and brings the chalice, wearing the veil; he sets it on the Epistle corner.", "ref": ["ministri-iv-2"]}
  ]},
  kyLow: {la: "Kyrie", en: "Kyrie", lines: [
    {"w": "P", "la": "Kýrie, eléison.", "en": "Lord, have mercy."},
    {"w": "S", "la": "Kýrie, eléison.", "en": "Lord, have mercy."},
    {"w": "P", "la": "Kýrie, eléison.", "en": "Lord, have mercy."},
    {"w": "S", "la": "Christe, eléison.", "en": "Christ, have mercy."},
    {"w": "P", "la": "Christe, eléison.", "en": "Christ, have mercy."},
    {"w": "S", "la": "Christe, eléison.", "en": "Christ, have mercy."},
    {"w": "P", "la": "Kýrie, eléison.", "en": "Lord, have mercy."},
    {"w": "S", "la": "Kýrie, eléison.", "en": "Lord, have mercy."},
    {"w": "P", "la": "Kýrie, eléison.", "en": "Lord, have mercy."}
  ]},
  glLow: {la: "Gloria", en: "Gloria", lines: [
    {"w": "P", "la": "Glória in excélsis Deo. Et in terra pax homínibus bonæ voluntátis. Laudámus te. Benedícimus te. Adorámus te. Glorificámus te. Grátias ágimus tibi propter magnam glóriam tuam. Dómine Deus, Rex cæléstis, Deus Pater omnípotens. Dómine Fili unigénite, Iesu Christe. Dómine Deus, Agnus Dei, Fílius Patris. Qui tollis peccáta mundi, miserére nobis. Qui tollis peccáta mundi, súscipe deprecatiónem nostram. Qui sedes ad déxteram Patris, miserére nobis. Quóniam tu solus Sanctus. Tu solus Dóminus. Tu solus Altíssimus, Iesu Christe. Cum Sancto Spíritu, in glória Dei Patris. Amen.", "en": "Glory to God in the highest. And on earth peace to men of good will. We praise thee. We bless thee. We adore thee. We glorify thee. We give thee thanks for thy great glory. O Lord God, heavenly King, God the Father almighty. O Lord Jesus Christ, the only-begotten Son. O Lord God, Lamb of God, Son of the Father. Who takest away the sins of the world, have mercy on us. Who takest away the sins of the world, receive our prayer. Who sittest at the right hand of the Father, have mercy on us. For thou alone art holy. Thou alone art Lord. Thou alone, O Jesus Christ, art most high. With the Holy Ghost, in the glory of God the Father. Amen."}
  ]},
  collect: {la: "Oratio", en: "Collect", lines: [
    {"w": "P", "la": "Dóminus vobíscum.", "en": "The Lord be with you."},
    {"w": "S", "la": "Et cum spíritu tuo.", "en": "And with thy spirit."},
    {"w": "P", "la": "Orémus.", "en": "Let us pray."}
  ], adv: [
    {"if": "!sac", "r": "Without kissing the altar, he turns to the people by his left, hands raised and extended:", "ref": ["modus-iii-1"]},
    {"if": "tab", "r": "He goes to the middle, bows his head, steps a little towards the Gospel side, and turns to the people by his right, so as not to turn his back to the tabernacle:", "ref": ["varia-ii-9"]},
    {"if": "exp", "r": "He genuflects at the middle, steps towards the Gospel corner, and turns to the people there, his back to the corner of the altar:", "ref": ["varia-ii-5"]},
    {"m": "mc", "r": "The deacon lifts the hem of the chasuble and goes with him.", "ref": ["ministri-v-1"]},
    {"w": "P", "la": "Dóminus vobíscum.", "en": "The Lord be with you."},
    {"w": "S", "la": "Et cum spíritu tuo.", "en": "And with thy spirit."},
    {"if": "!sac", "r": "He turns back by the same way and, at the book, bowing towards the cross, says:", "ref": ["modus-iii-2"]},
    {"if": "tab", "r": "He turns back by the same way, bowing again before the tabernacle, and, at the book, bowing towards the cross, says:", "ref": ["varia-ii-9"]},
    {"if": "exp", "r": "He returns the same way, genuflecting at the middle, and, at the book, bowing towards the cross, says:", "ref": ["varia-ii-5"]},
    {"w": "P", "la": "Orémus.", "en": "Let us pray."},
    {"m": "ls", "if": "flect", "r": "He kneels for Flectamus genua, laying the front of the chasuble on the altar; the server answers Levate, and he rises.", "ref": ["modus-iii-3"]},
    {"m": "mc", "if": "flect", "r": "The deacon, kneeling with the lower ministers, sings Flectamus genua, and rising sings Levate; the priest does not kneel.", "ref": ["ministri-v-2", "varia-i-2"]},
    {"r": "He reads the Collect with hands extended, joining them and bowing at Per Dominum nostrum.", "ref": ["modus-iii-2"]}
  ]},
  collectEnd: {la: "Epistola", en: "Epistle", lines: [

  ], adv: [
    {"m": "l", "r": "With his hands on the book or on the altar he reads the Epistle; then, with hands joined, the Gradual and what follows.", "ref": ["modus-iv-1"]},
    {"m": "l", "r": "The server kneels on the Gospel side until the end of the Alleluia or Tract.", "ref": ["varia-vi-4", "varia-vi-5"]},
    {"m": "s", "r": "The Epistle is read and the Gradual sung."},
    {"m": "mc", "r": "After the last prayer the priest and deacon go down to the lowest step; all bow and go to sit.", "ref": ["ministri-v-2"]},
    {"m": "mc", "r": "The subdeacon, an acolyte going before, sings the Epistle at the lectern before the steps, facing the altar.", "ref": ["ministri-vi-1"]},
    {"m": "mc", "r": "Seated, the priest reads the Epistle, and the Gradual and Alleluia verse by verse with the deacon; then he stands and reads the Gospel at his seat.", "ref": ["ministri-vi-2", "ministri-vi-3"]},
    {"m": "mc", "r": "Meanwhile the deacon spreads the corporal on the altar.", "ref": ["ministri-vi-3"]}
  ]},
  rGr: {la: "", en: "", strip: 1, lines: [

  ], adv: [
    {"m": "ls", "if": "adjuva", "r": "He genuflects at the verse Adjuva nos, Deus salutaris noster.", "ref": ["varia-i-1"]},
    {"m": "mc", "if": "adjuva", "r": "All genuflect at the verse Adjuva nos, Deus salutaris noster.", "ref": ["varia-i-1", "varia-i-2"]},
    {"m": "ls", "if": "veni", "r": "He genuflects while he says the verse Veni Sancte Spiritus, as far as reple.", "ref": ["varia-i-1"]},
    {"m": "mc", "if": "veni", "r": "At the verse Veni Sancte Spiritus the priest and ministers stand, bowing profoundly, as far as reple; they sit again when the choir rises.", "ref": ["ministri-vii-1", "varia-i-2"]},
    {"m": "mc", "if": "full,thur", "r": "Towards the end of the chant the acolytes light their candles, and the thurifer comes.", "ref": ["ministri-vii-2"]},
    {"m": "mc", "if": "!thur", "r": "Towards the end of the chant the acolytes light their candles.", "ref": ["ministri-vii-2"]},
    {"m": "mc", "if": "full,td", "r": "The acolytes go with the thurifer to the sacristy and bring back the processional cross.", "ref": ["ministri-vii-3"]},
    {"m": "mc", "if": "full,thur", "r": "The thurifer offers incense to the priest, saying Benedicite; the priest blesses it, saying In nomine Patris, et Filii, et Spiritus Sancti.", "ref": ["ministri-vii-3"]}
  ]},
  gospel: {la: "Ante Evangelium", en: "Before the Gospel", lines: [
    {"if": "!req", "r": "Then, having said the Collect, the Epistle and the Responsory with the Alleluia or Tract, he goes to the Gospel corner, bowing his head at the middle of the altar, and says:"},
    {"if": "req", "r": "Then, having said the Collect, the Epistle and the Responsory with the Tract, he goes to the Gospel corner, bowing his head at the middle of the altar."},
    {"m": "ls", "w": "P", "la": "Dóminus sit in corde meo et in lábiis meis ad pronuntiándum sanctum Evangélium pacis.", "en": "May the Lord be in my heart and on my lips, that I may announce the holy Gospel of peace.", "if": "!req"},
    {"m": "mc", "w": "D", "la": "Iube, domne, benedícere.", "en": "Pray, sir, a blessing."},
    {"m": "mc", "w": "P", "la": "Dóminus sit in corde tuo et in lábiis tuis ad pronuntiándum sanctum Evangélium pacis.", "en": "May the Lord be in thy heart and on thy lips, that thou mayest announce the holy Gospel of peace."},
    {"r": "And standing before the book, with his hands joined upon it, he says:"},
    {"w": "P", "la": "Dóminus vobíscum.", "en": "The Lord be with you."},
    {"w": "S", "la": "Et cum spíritu tuo.", "en": "And with thy spirit."},
    {"m": "l", "r": "And saying Sequentia (or Initium) sancti Evangelii, he signs the Gospel with his right thumb, and himself on the forehead, mouth and breast; then with his right hand he signs himself with a larger sign of the cross, from forehead to breast and shoulders. The server answers Gloria tibi Domine:"},
    {"m": "smc", "r": "And saying Sequentia (or Initium) sancti Evangelii, he signs the Gospel with his right thumb, and himself on the forehead, mouth and breast; then with his right hand he signs himself with a larger sign of the cross, from forehead to breast and shoulders. The ministers answer Gloria tibi Domine:"},
    {"w": "P", "la": "Sequéntia sancti Evangélii secúndum N.", "en": "The continuation of the holy Gospel according to N."},
    {"w": "S", "la": "Glória tibi, Dómine.", "en": "Glory be to thee, O Lord."},
    {"r": "Then he continues the Gospel with hands joined, as before."}
  ], adv: [
    {"m": "ls", "if": "!req,!exp", "r": "The server carries the Missal to the Gospel corner. The priest follows, bowing to the cross as he passes the middle, and says secretly:", "ref": ["modus-iv-2", "varia-vi-4"]},
    {"m": "ls", "if": "!req,exp", "r": "The server carries the Missal to the Gospel corner. The priest follows, genuflecting as he passes the middle, and says secretly:", "ref": ["modus-iv-2", "varia-ii-4"]},
    {"m": "ls", "if": "req", "r": "The server carries the Missal to the Gospel corner, and the priest follows, bowing to the cross as he passes the middle.", "ref": ["modus-iv-2"]},
    {"w": "P", "la": "Dóminus sit in corde meo et in lábiis meis ad pronuntiándum sanctum Evangélium pacis.", "en": "May the Lord be in my heart and on my lips, that I may announce the holy Gospel of peace.", "m": "ls", "if": "!req"},
    {"m": "mc", "r": "The deacon takes the Gospel book and, bowing to the priest, says:", "ref": ["ministri-viii-1"]},
    {"w": "D", "la": "Iube, domne, benedícere.", "en": "Pray, sir, a blessing.", "m": "mc"},
    {"m": "mc", "r": "The priest stands and answers:", "ref": ["ministri-viii-1"]},
    {"w": "P", "la": "Dóminus sit in corde tuo et in lábiis tuis ad pronuntiándum sanctum Evangélium pacis.", "en": "May the Lord be in thy heart and on thy lips, that thou mayest announce the holy Gospel of peace.", "m": "mc"},
    {"m": "mc", "w": "P", "la": "In nómine Patris, et Fílii, et Spíritus Sancti.", "en": "In the name of the Father, and of the Son, and of the Holy Ghost."},
    {"m": "mc", "w": "D", "la": "Amen.", "en": "Amen."},
    {"m": "mc", "if": "full,td", "r": "They go to the lectern at the Gospel side: the thurifer, the acolytes with the cross between them, the subdeacon with the cushion, and the deacon carrying the book.", "ref": ["ministri-viii-1", "ministri-viii-2"]},
    {"m": "mc", "if": "full,thur,!td", "r": "They go to the lectern at the Gospel side: the thurifer, the acolytes, the subdeacon with the cushion, and the deacon carrying the book.", "ref": ["ministri-viii-1", "ministri-viii-2"]},
    {"m": "mc", "if": "!full", "r": "They go to the lectern at the Gospel side: the acolytes, the subdeacon with the cushion, and the deacon carrying the book.", "ref": ["ministri-viii-1", "ministri-viii-2"]},
    {"m": "mc", "if": "full,!thur", "r": "They go to the lectern at the Gospel side: the acolytes, the subdeacon with the cushion, and the deacon carrying the book.", "ref": ["ministri-viii-1", "ministri-viii-2"]},
    {"m": "ls", "r": "With his hands joined on the book:", "ref": ["modus-v-1"]},
    {"w": "P", "la": "Dóminus vobíscum.", "en": "The Lord be with you.", "m": "ls"},
    {"w": "S", "la": "Et cum spíritu tuo.", "en": "And with thy spirit.", "m": "ls"},
    {"m": "mc", "w": "D", "la": "Dóminus vobíscum.", "en": "The Lord be with you."},
    {"m": "mc", "w": "S", "la": "Et cum spíritu tuo.", "en": "And with thy spirit."},
    {"m": "ls", "r": "At Sequentia he signs the book with his thumb, then his forehead, lips and breast:", "ref": ["modus-v-1"]},
    {"m": "mc", "r": "At Sequentia the deacon signs the book and himself; the priest and subdeacon sign themselves, facing the altar:", "ref": ["ministri-viii-3"]},
    {"w": "P", "la": "Sequéntia sancti Evangélii secúndum N.", "en": "The continuation of the holy Gospel according to N.", "m": "ls"},
    {"m": "mc", "w": "D", "la": "Sequéntia sancti Evangélii secúndum N.", "en": "The continuation of the holy Gospel according to N."},
    {"w": "S", "la": "Glória tibi, Dómine.", "en": "Glory be to thee, O Lord."},
    {"m": "mc", "if": "full,thur", "r": "The deacon incenses the book three times.", "ref": ["ministri-viii-3"]},
    {"m": "ls", "r": "He reads the Gospel with hands joined on the book, bowing at the names of Jesus and Mary.", "ref": ["modus-v-2"]},
    {"m": "mc", "r": "The deacon sings the Gospel with hands joined. The priest stands at the Epistle corner facing it; all the brethren turn towards it.", "ref": ["ministri-viii-3", "ministri-viii-4"]}
  ]},
  afterGospel: {la: "Post Evangelium", en: "After the Gospel", lines: [
    {"if": "!req", "r": "When it is finished, he signs himself again with the larger sign of the cross; and at once signing the Gospel with the cross with his thumb, he kisses it, saying:"},
    {"w": "P", "la": "Per evangélica dicta deleántur nostra delícta.", "en": "By the words of the Gospel may our sins be blotted out.", "if": "!req"}
  ], adv: [
    {"m": "ls", "if": "!prel,!req", "r": "At the end he signs himself, then kisses the Gospel, saying:", "ref": ["modus-v-3"]},
    {"m": "mc", "if": "!prel,!req", "r": "The ministers return to the altar. The subdeacon brings the book to the priest, the deacon pointing to the Gospel; the priest kisses it, saying:", "ref": ["ministri-viii-5", "ministri-ix-1"]},
    {"m": "mc", "if": "prel", "r": "The ministers return to the altar.", "ref": ["ministri-viii-5"]},
    {"if": "pope,!req", "r": "The Gospel book is taken to the Pope to kiss.", "ref": ["varia-iii-4"]},
    {"if": "bp,!req", "r": "The Gospel book is taken to the Bishop to kiss.", "ref": ["varia-iii-4"]},
    {"w": "P", "la": "Per evangélica dicta deleántur nostra delícta.", "en": "By the words of the Gospel may our sins be blotted out.", "if": "!prel,!req"},
    {"m": "mc", "if": "!prel,!req", "w": "D", "la": "Amen.", "en": "Amen."},
    {"m": "mc", "if": "!prel,!req", "r": "The deacon kisses the book after him.", "ref": ["ministri-ix-1"]},
    {"m": "ls", "if": "sun", "r": "The sermon may follow."}
  ]},
  rCr: {la: "", en: "", strip: 1, lines: [
    {"r": "Then at the middle of the altar, extending, raising and joining his hands, he says (if it is to be said) Credo in unum Deum, and going to the book continues it with hands joined. At Deum he bows his head to the cross, and does the same at Jesum Christum and at simul adoratur; at Et incarnatus est he kneels on both knees; at the end, at Et vitam venturi saeculi, he signs himself with the sign of the cross from forehead to breast and shoulders."}
  ], adv: [
    {"m": "ls", "if": "exp", "r": "He genuflects as he comes to the middle for the Credo, and as he goes to and from the book.", "ref": ["varia-ii-4"]},
    {"m": "l", "r": "At the middle, his hands laid on the altar, he says Credo; at in unum he raises them, at Deum he joins them and bows.", "ref": ["modus-vi-1"]},
    {"m": "l", "r": "He continues at the Gospel corner, bowing at Jesum Christum. At Et incarnatus est he comes to the middle and kneels, rising after Homo factus est.", "ref": ["modus-vi-1", "modus-vi-2"]},
    {"m": "l", "r": "He bows at simul adoratur and signs himself at Et vitam venturi saeculi.", "ref": ["modus-vi-2"]},
    {"m": "s", "r": "He intones the Credo at the middle of the altar, with the same gestures, and continues it at the Gospel corner; at Et incarnatus est he kneels at the middle.", "ref": ["modus-vi-1", "modus-vi-2"]},
    {"m": "mc", "r": "The priest intones the Credo at the middle; the ministers stand at his left, one behind the other, and continue it with him in a low voice.", "ref": ["ministri-ix-2"]},
    {"m": "mc", "r": "At Et incarnatus est, as the choir sings it, the priest kneels at the middle, the deacon and subdeacon on the step behind him, the acolytes lower down.", "ref": ["ministri-ix-2"]},
    {"m": "mc", "r": "All bow at simul adoratur.", "ref": ["ministri-ix-3"]},
    {"m": "mc", "if": "full,td", "r": "Then the acolytes and thurifer take the cross back to the sacristy.", "ref": ["ministri-ix-3"]}
  ]},
  crLow: {la: "Credo", en: "Credo", lines: [
    {"w": "P", "la": "Credo in unum Deum, Patrem omnipoténtem, factórem cæli et terræ, visibílium ómnium et invisibílium. Et in unum Dóminum Iesum Christum, Fílium Dei unigénitum. Et ex Patre natum ante ómnia sǽcula. Deum de Deo, lumen de lúmine, Deum verum de Deo vero. Génitum, non factum, consubstantiálem Patri: per quem ómnia facta sunt. Qui propter nos hómines et propter nostram salútem descéndit de cælis. (Hic genuflectitur.) Et incarnátus est de Spíritu Sancto ex María Vírgine: et homo factus est. Crucifíxus étiam pro nobis: sub Póntio Piláto passus, et sepúltus est. Et resurréxit tértia die, secúndum Scriptúras. Et ascéndit in cælum: sedet ad déxteram Patris. Et íterum ventúrus est cum glória iudicáre vivos et mórtuos: cuius regni non erit finis. Et in Spíritum Sanctum, Dóminum et vivificántem: qui ex Patre Filióque procédit. Qui cum Patre et Fílio simul adorátur et conglorificátur: qui locútus est per Prophétas. Et unam sanctam cathólicam et apostólicam Ecclésiam. Confíteor unum baptísma in remissiónem peccatórum. Et exspécto resurrectiónem mortuórum. Et vitam ventúri sǽculi. Amen.", "en": "I believe in one God, the Father almighty, maker of heaven and earth, and of all things visible and invisible. And in one Lord Jesus Christ, the only-begotten Son of God. Born of the Father before all ages. God of God, light of light, true God of true God. Begotten, not made, consubstantial with the Father: by whom all things were made. Who for us men and for our salvation came down from heaven. (Here all kneel.) And became incarnate by the Holy Ghost of the Virgin Mary: and was made man. He was crucified also for us, suffered under Pontius Pilate, and was buried. And on the third day he rose again according to the Scriptures. And ascended into heaven, and sitteth at the right hand of the Father. And he shall come again with glory to judge the living and the dead: of whose kingdom there shall be no end. And in the Holy Ghost, the Lord and giver of life, who proceedeth from the Father and the Son. Who together with the Father and the Son is adored and glorified: who spoke by the Prophets. And one holy, catholic and apostolic Church. I confess one baptism for the remission of sins. And I look for the resurrection of the dead. And the life of the world to come. Amen."}
  ]},
  offerDial: {la: "Offertorium", en: "Offertory", lines: [
    {"r": "Then, turned to the people, he says:"},
    {"w": "P", "la": "Dóminus vobíscum.", "en": "The Lord be with you."},
    {"w": "S", "la": "Et cum spíritu tuo.", "en": "And with thy spirit."},
    {"r": "Then he says Oremus, and the Offertory."},
    {"w": "P", "la": "Orémus.", "en": "Let us pray."}
  ], adv: [
    {"if": "!sac", "r": "At the middle, without kissing the altar, he turns to the people by his left, hands raised and extended:", "ref": ["modus-iii-1"]},
    {"if": "tab", "r": "He goes to the middle, bows his head, steps a little towards the Gospel side, and turns to the people by his right, so as not to turn his back to the tabernacle:", "ref": ["varia-ii-9"]},
    {"if": "exp", "r": "He genuflects at the middle, steps towards the Gospel corner, and turns to the people there, his back to the corner of the altar:", "ref": ["varia-ii-5"]},
    {"w": "P", "la": "Dóminus vobíscum.", "en": "The Lord be with you."},
    {"w": "S", "la": "Et cum spíritu tuo.", "en": "And with thy spirit."},
    {"if": "!sac", "r": "He turns back by the same way and, bowing to the cross, says:", "ref": ["modus-iii-2"]},
    {"if": "tab", "r": "He turns back by the same way, bowing again before the tabernacle, and, bowing to the cross, says:", "ref": ["varia-ii-9"]},
    {"if": "exp", "r": "He returns the same way, genuflecting at the middle, and, bowing to the cross, says:", "ref": ["varia-ii-5"]},
    {"w": "P", "la": "Orémus.", "en": "Let us pray."},
    {"m": "ls", "r": "At the book he reads the Offertory.", "ref": ["modus-vii-2"]},
    {"m": "mc", "r": "At the book he says the Offertory with the ministers.", "ref": ["ministri-x-1"]}
  ]},
  offertory: {la: "Oblatio", en: "The offering", lines: [
    {"if": "!req", "r": "The Offertory said, raising and joining his hands, he says Quid retribuam; and taking the chalice, with the host laid on the paten, in both hands and raising it above the corporal before his breast, he says Calicem salutaris:"},
    {"w": "P", "la": "Quid retríbuam Dómino pro ómnibus quæ retríbuit mihi? Cálicem salutáris accípiam, et nomen Dómini invocábo.", "en": "What shall I render to the Lord for all the things that he hath rendered unto me? I will take the chalice of salvation, and I will call upon the name of the Lord.", "if": "!req"},
    {"r": "Then, offering, he says:"},
    {"w": "P", "la": "Súscipe, sancta Trínitas, hanc oblatiónem, quam tibi óffero in memóriam passiónis Dómini nostri Iesu Christi: et præsta, ut in conspéctu tuo tibi placens ascéndat, et meam et ómnium fidélium salútem operétur ætérnam.", "en": "Receive, O holy Trinity, this oblation which I offer to thee in memory of the passion of our Lord Jesus Christ: and grant that it may ascend before thee and be pleasing to thee, and work my eternal salvation and that of all the faithful."},
    {"r": "This said, setting the chalice down on the corporal, he lifts the paten from the chalice, lays the host before its foot, and covers the chalice with the pall. Then, going to the Epistle corner for the washing of the fingers, he says (and no further):"},
    {"w": "P", "la": "Lavábo inter innocéntes manus meas: et circúmdabo altáre tuum, Dómine: ut áudiam vocem laudis, et enárrem univérsa mirabília tua. Dómine, diléxi decórem domus tuæ, et locum habitatiónis glóriæ tuæ.", "en": "I will wash my hands among the innocent, and will compass thine altar, O Lord, that I may hear the voice of thy praise, and tell of all thy wondrous works. I have loved, O Lord, the beauty of thy house, and the place where thy glory dwelleth."},
    {"r": "After the washing of the fingers, the priest, coming to the middle of the altar with hands joined before his breast, bows profoundly, saying:"},
    {"w": "P", "la": "In spíritu humilitátis et in ánimo contríto suscipiámur, Dómine, a te: et sic fiat sacrifícium nostrum, ut a te suscipiátur hódie, et pláceat tibi, Dómine Deus.", "en": "In a humble spirit and a contrite heart may we be received by thee, O Lord; and so may our sacrifice be offered in thy sight this day, that it be received by thee and be pleasing to thee, O Lord God."},
    {"r": "This said, standing erect and turning to the people, extending and joining his hands, he says in a moderate voice Orate fratres, these two words only, continuing the rest secretly:"},
    {"w": "P", "la": "Oráte, fratres, ut meum ac vestrum páriter in conspéctu Dómini sit accéptum sacrifícium.", "en": "Pray, brethren, that my sacrifice and yours may be equally acceptable in the sight of the Lord."},
    {"r": "With hands joined he adds:"},
    {"w": "P", "la": "Dómine, exáudi oratiónem meam: et clamor meus ad te véniat.", "en": "O Lord, hear my prayer; and let my cry come unto thee."},
    {"r": "and Oremus. Then, with hands extended, he says the Secret prayer or prayers; when they are finished, at the conclusion, he says in a clear and audible voice Per omnia saecula saeculorum, with the Preface proper to the Mass."}
  ], adv: [
    {"m": "ls", "if": "!req", "r": "At the middle he uncovers the chalice and sets the veil aside; laying his hands on the altar, he says:", "ref": ["modus-vii-2"]},
    {"m": "ls", "if": "req", "r": "At the middle he uncovers the chalice and sets the veil aside.", "ref": ["modus-vii-2"]},
    {"w": "P", "la": "Quid retríbuam Dómino pro ómnibus quæ retríbuit mihi? Cálicem salutáris accípiam, et nomen Dómini invocábo.", "en": "What shall I render to the Lord for all the things that he hath rendered unto me? I will take the chalice of salvation, and I will call upon the name of the Lord.", "m": "ls", "if": "!req"},
    {"m": "mc", "if": "!req", "r": "At the middle the priest says:", "ref": ["ministri-x-1"]},
    {"m": "mc", "if": "!req", "w": "P", "la": "Quid retríbuam Dómino pro ómnibus quæ retríbuit mihi?", "en": "What shall I render to the Lord for all the things that he hath rendered unto me?"},
    {"m": "mc", "if": "!req", "r": "The subdeacon uncovers the chalice; the deacon hands it to the priest, holding it by the foot and kissing his hand, and says:", "ref": ["ministri-x-1"]},
    {"m": "mc", "if": "!req", "w": "D", "la": "Immola Deo sacrifícium laudis, et redde Altíssimo vota tua.", "en": "Offer to God the sacrifice of praise, and pay thy vows to the Most High."},
    {"m": "mc", "if": "!req", "r": "Taking it, the priest says:", "ref": ["ministri-x-1"]},
    {"m": "mc", "if": "!req", "w": "P", "la": "Cálicem salutáris accípiam, et nomen Dómini invocábo.", "en": "I will take the chalice of salvation, and I will call upon the name of the Lord."},
    {"m": "mc", "if": "req", "r": "The subdeacon uncovers the chalice and the deacon hands it to the priest.", "ref": ["ministri-x-1"]},
    {"r": "Raising the chalice, with the paten and host on it, to the height of his breast, he offers them:", "ref": ["modus-vii-3"]},
    {"w": "P", "la": "Súscipe, sancta Trínitas, hanc oblatiónem, quam tibi óffero in memóriam passiónis Dómini nostri Iesu Christi: et præsta, ut in conspéctu tuo tibi placens ascéndat, et meam et ómnium fidélium salútem operétur ætérnam.", "en": "Receive, O holy Trinity, this oblation which I offer to thee in memory of the passion of our Lord Jesus Christ: and grant that it may ascend before thee and be pleasing to thee, and work my eternal salvation and that of all the faithful."},
    {"r": "He sets the chalice down, slides the host onto the corporal before it, puts the paten partly under the corporal, and covers the chalice with the pall.", "ref": ["modus-vii-3"]},
    {"m": "mc", "if": "full,thur", "r": "The deacon presents incense; the priest blesses it and takes the thurible from him.", "ref": ["ministri-xi-1"]},
    {"m": "mc", "if": "full,thur,!exp", "r": "He incenses the chalice (a sign of the cross and three swings), then the tabernacle or the cross, then the top of the altar on either side, then its front.", "ref": ["ministri-xi-1", "ministri-xi-2"]},
    {"m": "mc", "if": "full,thur,exp", "r": "He incenses the chalice; then, kneeling on both knees on the top step with the ministers, he incenses the Sacrament, bowing profoundly before and after; then, standing, the altar, genuflecting as he passes the middle.", "ref": ["varia-ii-6", "ministri-xi-2"]},
    {"m": "mc", "if": "full,thur,!exp", "r": "Standing at the Epistle corner, the priest is incensed by the deacon.", "ref": ["ministri-xi-4"]},
    {"m": "mc", "if": "full,thur,exp", "r": "He goes down to the Epistle corner below the top step and, facing the people, is incensed by the deacon.", "ref": ["varia-ii-6"]},
    {"m": "ls", "if": "exp", "r": "He genuflects as he leaves the middle for the washing of the hands, and again on his return.", "ref": ["varia-ii-4"]},
    {"m": "ls", "r": "At the Epistle corner he washes his fingers, saying:", "ref": ["modus-vii-4", "varia-vi-6"]},
    {"m": "mc", "r": "At the Epistle corner the subdeacon pours the water and the deacon hands the towel; the priest says:", "ref": ["ministri-xii-1"]},
    {"w": "P", "la": "Lavábo inter innocéntes manus meas: et circúmdabo altáre tuum, Dómine: ut áudiam vocem laudis, et enárrem univérsa mirabília tua. Dómine, diléxi decórem domus tuæ, et locum habitatiónis glóriæ tuæ.", "en": "I will wash my hands among the innocent, and will compass thine altar, O Lord, that I may hear the voice of thy praise, and tell of all thy wondrous works. I have loved, O Lord, the beauty of thy house, and the place where thy glory dwelleth."},
    {"r": "He returns to the middle and, bowing profoundly, says:", "ref": ["modus-vii-4"]},
    {"w": "P", "la": "In spíritu humilitátis et in ánimo contríto suscipiámur, Dómine, a te: et sic fiat sacrifícium nostrum, ut a te suscipiátur hódie, et pláceat tibi, Dómine Deus.", "en": "In a humble spirit and a contrite heart may we be received by thee, O Lord; and so may our sacrifice be offered in thy sight this day, that it be received by thee and be pleasing to thee, O Lord God."},
    {"if": "!sac", "r": "Without kissing the altar he turns to the people, says Orate fratres aloud and the rest secretly, and turns back completing the circle:", "ref": ["modus-vii-5"]},
    {"if": "tab", "r": "He steps towards the Gospel side and turns to the people by his right, so as not to turn his back to the tabernacle; he says Orate fratres aloud and the rest secretly, and returns the same way:", "ref": ["varia-ii-10"]},
    {"if": "exp", "r": "He genuflects, steps towards the Gospel corner and turns to the people; he says Orate fratres aloud and the rest secretly, and returns the same way, genuflecting:", "ref": ["varia-ii-7"]},
    {"w": "P", "la": "Oráte, fratres, ut meum ac vestrum páriter in conspéctu Dómini sit accéptum sacrifícium.", "en": "Pray, brethren, that my sacrifice and yours may be equally acceptable in the sight of the Lord."},
    {"r": "Facing the altar, with hands joined:", "ref": ["modus-vii-5"]},
    {"w": "P", "la": "Dómine, exáudi oratiónem meam: et clamor meus ad te véniat.", "en": "O Lord, hear my prayer; and let my cry come unto thee."},
    {"r": "Then Oremus, and the Secret in a low voice.", "ref": ["modus-vii-5"]}
  ]},
  offertoryEnd: {la: "Præfatio", en: "Preface", lines: [
    {"m": "l", "w": "P", "la": "Dóminus vobíscum.", "en": "The Lord be with you."},
    {"m": "l", "w": "S", "la": "Et cum spíritu tuo.", "en": "And with thy spirit."},
    {"m": "l", "w": "P", "la": "Sursum corda.", "en": "Lift up your hearts."},
    {"m": "l", "w": "S", "la": "Habémus ad Dóminum.", "en": "We have lifted them up to the Lord."},
    {"m": "l", "w": "P", "la": "Grátias agámus Dómino Deo nostro.", "en": "Let us give thanks to the Lord our God."},
    {"m": "l", "w": "S", "la": "Dignum et iustum est.", "en": "It is meet and just."}
  ]},
  rPf: {la: "", en: "", strip: 1, lines: [

  ], adv: [
    {"r": "His hands lie on the altar for Per omnia saecula saeculorum and Dominus vobiscum; at Sursum corda he raises them; at Gratias agamus he joins them and bows; he opens them for the Preface and joins them at supplici confessione dicentes.", "ref": ["modus-viii-1", "modus-viii-2"]},
    {"m": "mc", "if": "full,thur", "r": "After Gratias agamus the thurifer incenses the deacon, the subdeacon and the acolytes, who stand facing one another at the two corners.", "ref": ["ministri-xiii-1"]},
    {"m": "c", "if": "mo,full,thur", "r": "The thurifer then incenses him.", "ref": ["ministri-xiii-2"]},
    {"m": "c", "if": "full,thur", "r": "Then the thurifer incenses the brethren in both choirs, seniors first, and the lay brothers, and returns to stand behind the subdeacon.", "ref": ["ministri-xiii-2"]}
  ]},
  rSa: {la: "", en: "", strip: 1, lines: [

  ], adv: [
    {"m": "ls", "r": "With hands joined he says the Sanctus, signing himself at Benedictus qui venit. The server rings the bell a few times and lights the elevation candle.", "ref": ["modus-viii-2", "varia-vi-7"]},
    {"m": "mc", "r": "At supplici confessione the deacon goes to the Gospel corner and the subdeacon to the Epistle corner, each with an acolyte; facing one another they say the Sanctus with the priest, signing themselves at Benedictus. An acolyte rings the bell.", "ref": ["ministri-xiv-1"]},
    {"m": "mc", "if": "thur", "r": "The subdeacon takes the veil, receives the paten from the deacon, and holds it raised behind the deacon until after the Pater noster; the acolytes light the elevation candles.", "ref": ["ministri-xiv-2"]},
    {"m": "smc", "r": "The choir does not draw out the Sanctus, and the priest goes slowly enough that the elevation never comes before it ends.", "ref": ["ministri-xv-2"]},
    {"m": "mc", "if": "one", "r": "With only one acolyte, he stands at the deacon’s right during the Sanctus and the consecration.", "ref": ["ministri-xx-4"]}
  ]},
  saLow: {la: "Sanctus", en: "Sanctus", lines: [
    {"w": "P", "la": "Sanctus, Sanctus, Sanctus Dóminus Deus Sábaoth. Pleni sunt cæli et terra glória tua. Hosánna in excélsis. Benedíctus qui venit in nómine Dómini. Hosánna in excélsis.", "en": "Holy, holy, holy, Lord God of hosts. Heaven and earth are full of thy glory. Hosanna in the highest. Blessed is he that cometh in the name of the Lord. Hosanna in the highest."}
  ]},
  canon: {la: "Canon Missæ", en: "The Canon of the Mass", lines: [
    {"w": "P", "la": "Te ígitur, clementíssime Pater, per Iesum Christum Fílium tuum Dóminum nostrum, súpplices rogámus ac pétimus, uti accépta hábeas et benedícas hæc ✠ dona, hæc ✠ múnera, hæc ✠ sancta sacrifícia illibáta: in primis, quæ tibi offérimus pro Ecclésia tua sancta cathólica: quam pacificáre, custodíre, adunáre et régere dignéris toto orbe terrárum: una cum fámulo tuo Papa nostro N. et Antístite nostro N. et ómnibus orthodóxis, atque cathólicæ et apostólicæ fídei cultóribus.", "en": "We therefore humbly pray and beseech thee, most merciful Father, through Jesus Christ thy Son our Lord, that thou wouldst accept and bless these ✠ gifts, these ✠ offerings, these ✠ holy unspotted sacrifices, which in the first place we offer thee for thy holy catholic Church: deign to grant her peace, to protect, unite and govern her throughout the whole world, together with thy servant N. our Pope, and N. our Bishop, and all orthodox believers and professors of the catholic and apostolic faith."},
    {"w": "P", "la": "Meménto, Dómine, famulórum famularúmque tuárum N. et N. et ómnium circumstántium, quorum tibi fides cógnita est et nota devótio, pro quibus tibi offérimus: vel qui tibi ófferunt hoc sacrifícium laudis, pro se suísque ómnibus: pro redemptióne animárum suárum, pro spe salútis et incolumitátis suæ: tibíque reddunt vota sua ætérno Deo, vivo et vero.", "en": "Be mindful, O Lord, of thy servants and handmaids N. and N., and of all here present, whose faith and devotion are known to thee; for whom we offer, or who offer up to thee, this sacrifice of praise for themselves and all their own, for the redemption of their souls, for the hope of their safety and salvation, and who pay their vows to thee, the eternal, living and true God."},
    {"w": "P", "la": "Communicántes, et memóriam venerántes, in primis gloriósæ semper Vírginis Maríæ, Genetrícis Dei et Dómini nostri Iesu Christi: sed et beatórum Apostolórum ac Mártyrum tuórum, Petri et Pauli, Andréæ, Iacóbi, Ioánnis, Thomæ, Iacóbi, Philíppi, Bartholomǽi, Matthǽi, Simónis et Thaddǽi: Lini, Cleti, Cleméntis, Xysti, Cornélii, Cypriáni, Lauréntii, Chrysógoni, Ioánnis et Pauli, Cosmæ et Damiáni: et ómnium Sanctórum tuórum; quorum méritis precibúsque concédas, ut in ómnibus protectiónis tuæ muniámur auxílio. Per eúndem Christum Dóminum nostrum. Amen.", "en": "In communion with, and honouring the memory in the first place of the glorious ever-virgin Mary, Mother of our God and Lord Jesus Christ as also of thy blessed Apostles and Martyrs, Peter and Paul, Andrew, James, John, Thomas, James, Philip, Bartholomew, Matthew, Simon and Thaddeus; Linus, Cletus, Clement, Xystus, Cornelius, Cyprian, Laurence, Chrysogonus, John and Paul, Cosmas and Damian, and of all thy Saints; by whose merits and prayers grant that we may in all things be defended by the help of thy protection. Through the same Christ our Lord. Amen."},
    {"w": "P", "la": "Hanc ígitur oblatiónem servitútis nostræ, sed et cunctæ famíliæ tuæ, quǽsumus, Dómine, ut placátus accípias: diésque nostros in tua pace dispónas, atque ab ætérna damnatióne nos éripi, et in electórum tuórum iúbeas grege numerári. Per Christum Dóminum nostrum. Amen.", "en": "We therefore beseech thee, O Lord, graciously to accept this oblation of our service and that of all thy household; order our days in thy peace, and bid us be delivered from eternal damnation and numbered in the flock of thine elect. Through Christ our Lord. Amen."},
    {"w": "P", "la": "Quam oblatiónem tu, Deus, in ómnibus, quǽsumus, bene ✠ díctam, adscríp ✠ tam, ra ✠ tam, rationábilem, acceptabilémque fácere dignéris: ut nobis Cor ✠ pus et San ✠ guis fiat dilectíssimi Fílii tui Dómini nostri Iesu Christi.", "en": "Which oblation do thou, O God, vouchsafe in all things to make ✠ blessed, ✠ approved, ✠ ratified, reasonable and acceptable; that it may become for us the ✠ Body and ✠ Blood of thy most beloved Son, our Lord Jesus Christ."},
    {"w": "P", "la": "Qui prídie quam paterétur, accépit panem in sanctas ac venerábiles manus suas, et elevátis óculis in cælum ad te Deum Patrem suum omnipoténtem, tibi grátias agens, bene ✠ díxit, fregit, dedítque discípulis suis, dicens: Accípite, et manducáte ex hoc omnes. HOC EST ENIM CORPUS MEUM.", "en": "Who the day before he suffered took bread into his holy and venerable hands, and with his eyes lifted up to heaven, unto thee, O God, his almighty Father, giving thanks to thee, he ✠ blessed it, broke it, and gave it to his disciples, saying: Take and eat ye all of this. FOR THIS IS MY BODY."},
    {"w": "P", "la": "Símili modo postquam cenátum est, accípiens et hunc præclárum Cálicem in sanctas ac venerábiles manus suas: item tibi grátias agens, bene ✠ díxit, dedítque discípulis suis, dicens: Accípite, et bíbite ex eo omnes. HIC EST ENIM CALIX SÁNGUINIS MEI, NOVI ET ÆTÉRNI TESTAMÉNTI: MYSTÉRIUM FÍDEI: QUI PRO VOBIS ET PRO MULTIS EFFUNDÉTUR IN REMISSIÓNEM PECCATÓRUM.", "en": "In like manner, after he had supped, taking also this excellent chalice into his holy and venerable hands, and giving thanks to thee, he ✠ blessed it, and gave it to his disciples, saying: Take and drink ye all of this. FOR THIS IS THE CHALICE OF MY BLOOD, OF THE NEW AND ETERNAL TESTAMENT: THE MYSTERY OF FAITH: WHICH SHALL BE SHED FOR YOU AND FOR MANY UNTO THE REMISSION OF SINS."},
    {"w": "P", "la": "Hæc quotiescúmque fecéritis, in mei memóriam faciétis.", "en": "As often as ye shall do these things, ye shall do them in remembrance of me."},
    {"w": "P", "la": "Unde et mémores, Dómine, nos servi tui, sed et plebs tua sancta, eiúsdem Christi Fílii tui Dómini nostri tam beátæ passiónis, nec non et ab ínferis resurrectiónis, sed et in cælos gloriósæ ascensiónis: offérimus præcláræ maiestáti tuæ de tuis donis ac datis, hóstiam ✠ puram, hóstiam ✠ sanctam, hóstiam ✠ immaculátam, Panem ✠ sanctum vitæ ætérnæ, et Cálicem ✠ salútis perpétuæ.", "en": "Wherefore, O Lord, we thy servants, as also thy holy people, calling to mind the blessed passion of the same Christ thy Son our Lord, his resurrection from the dead, and his glorious ascension into heaven, offer unto thy most excellent majesty, of thine own gifts bestowed upon us, a pure ✠ victim, a holy ✠ victim, a spotless ✠ victim, the holy ✠ Bread of eternal life, and the Chalice ✠ of everlasting salvation."},
    {"w": "P", "la": "Supra quæ propítio ac seréno vultu respícere dignéris: et accépta habére, sícuti accépta habére dignátus es múnera púeri tui iusti Abel, et sacrifícium patriárchæ nostri Abrahæ: et quod tibi óbtulit summus sacérdos tuus Melchísedech, sanctum sacrifícium, immaculátam hóstiam.", "en": "Upon which vouchsafe to look with a propitious and serene countenance, and to accept them, as thou wert graciously pleased to accept the gifts of thy just servant Abel, and the sacrifice of our patriarch Abraham, and that which thy high priest Melchisedech offered to thee, a holy sacrifice, an unspotted victim."},
    {"w": "P", "la": "Súpplices te rogámus, omnípotens Deus: iube hæc perférri per manus sancti Angeli tui in sublíme altáre tuum, in conspéctu divínæ maiestátis tuæ: ut quotquot ex hac altáris participatióne sacrosánctum Fílii tui Cor ✠ pus et Sán ✠ guinem sumpsérimus, omni benedictióne cælésti et grátia repleámur. Per eúndem Christum Dóminum nostrum. Amen.", "en": "We most humbly beseech thee, almighty God, command these things to be carried by the hands of thy holy Angel to thine altar on high, in the sight of thy divine majesty; that as many of us as, by this participation at the altar, shall receive the most sacred ✠ Body and ✠ Blood of thy Son, may be filled with every heavenly blessing and grace. Through the same Christ our Lord. Amen."},
    {"w": "P", "la": "Meménto étiam, Dómine, famulórum famularúmque tuárum N. et N., qui nos præcessérunt cum signo fídei, et dórmiunt in somno pacis. Ipsis, Dómine, et ómnibus in Christo quiescéntibus, locum refrigérii, lucis et pacis, ut indúlgeas, deprecámur. Per eúndem Christum Dóminum nostrum. Amen.", "en": "Be mindful also, O Lord, of thy servants and handmaids N. and N., who are gone before us with the sign of faith, and sleep in the sleep of peace. To these, O Lord, and to all who rest in Christ, grant, we beseech thee, a place of refreshment, light and peace. Through the same Christ our Lord. Amen."},
    {"w": "P", "la": "Nobis quoque peccatóribus fámulis tuis, de multitúdine miseratiónum tuárum sperántibus, partem áliquam et societátem donáre dignéris, cum tuis sanctis Apóstolis et Martýribus: cum Ioánne, Stéphano, Matthía, Bárnaba, Ignátio, Alexándro, Marcellíno, Petro, Felicitáte, Perpétua, Agatha, Lúcia, Agnéte, Cæcília, Anastásia, et ómnibus Sanctis tuis: intra quorum nos consórtium, non æstimátor mériti, sed véniæ, quǽsumus, largítor admítte. Per Christum Dóminum nostrum.", "en": "To us sinners also, thy servants, hoping in the multitude of thy mercies, vouchsafe to grant some part and fellowship with thy holy Apostles and Martyrs: with John, Stephen, Matthias, Barnabas, Ignatius, Alexander, Marcellinus, Peter, Felicitas, Perpetua, Agatha, Lucy, Agnes, Cecilia, Anastasia, and all thy Saints: into whose company we beseech thee to admit us, not weighing our merits, but freely pardoning our offences. Through Christ our Lord."},
    {"w": "P", "la": "Per quem hæc ómnia, Dómine, semper bona creas, sancti ✠ fícas, vivi ✠ fícas, bene ✠ dícis, et præstas nobis. Per ip ✠ sum, et cum ip ✠ so, et in ip ✠ so, est tibi Deo Patri ✠ omnipoténti, in unitáte Spíritus ✠ Sancti, omnis honor et glória.", "en": "By whom, O Lord, thou dost always create, ✠ sanctify, ✠ quicken, ✠ bless and bestow upon us all these good things. Through ✠ him, and with ✠ him, and in ✠ him, is unto thee, God the Father ✠ almighty, in the unity of the Holy ✠ Ghost, all honour and glory."},
    {"w": "P", "la": "Per ómnia sǽcula sæculórum.", "en": "World without end."},
    {"w": "S", "la": "Amen.", "en": "Amen."}
  ], adv: [
    {"r": "Bowing profoundly, with hands joined, he begins secretly. At uti he stands erect; at benedicas he makes three crosses over the offerings; at In primis he joins his hands.", "ref": ["modus-ix-1"]},
    {"w": "P", "la": "Te ígitur, clementíssime Pater, per Iesum Christum Fílium tuum Dóminum nostrum, súpplices rogámus ac pétimus, uti accépta hábeas et benedícas hæc ✠ dona, hæc ✠ múnera, hæc ✠ sancta sacrifícia illibáta: in primis, quæ tibi offérimus pro Ecclésia tua sancta cathólica: quam pacificáre, custodíre, adunáre et régere dignéris toto orbe terrárum: una cum fámulo tuo Papa nostro N. et Antístite nostro N. et ómnibus orthodóxis, atque cathólicæ et apostólicæ fídei cultóribus.", "en": "We therefore humbly pray and beseech thee, most merciful Father, through Jesus Christ thy Son our Lord, that thou wouldst accept and bless these ✠ gifts, these ✠ offerings, these ✠ holy unspotted sacrifices, which in the first place we offer thee for thy holy catholic Church: deign to grant her peace, to protect, unite and govern her throughout the whole world, together with thy servant N. our Pope, and N. our Bishop, and all orthodox believers and professors of the catholic and apostolic faith."},
    {"r": "At Papa he names the Pope; at Antistite the Bishop of the diocese.", "ref": ["modus-ix-1"]},
    {"r": "With hands joined; after tuarum he pauses to remember in silence those he wishes to commend to God:", "ref": ["modus-ix-2"]},
    {"w": "P", "la": "Meménto, Dómine, famulórum famularúmque tuárum N. et N. et ómnium circumstántium, quorum tibi fides cógnita est et nota devótio, pro quibus tibi offérimus: vel qui tibi ófferunt hoc sacrifícium laudis, pro se suísque ómnibus: pro redemptióne animárum suárum, pro spe salútis et incolumitátis suæ: tibíque reddunt vota sua ætérno Deo, vivo et vero.", "en": "Be mindful, O Lord, of thy servants and handmaids N. and N., and of all here present, whose faith and devotion are known to thee; for whom we offer, or who offer up to thee, this sacrifice of praise for themselves and all their own, for the redemption of their souls, for the hope of their safety and salvation, and who pay their vows to thee, the eternal, living and true God."},
    {"r": "With hands extended; he bows at the names of Mary and Jesus:", "ref": ["modus-ix-3"]},
    {"w": "P", "la": "Communicántes, et memóriam venerántes, in primis gloriósæ semper Vírginis Maríæ, Genetrícis Dei et Dómini nostri Iesu Christi: sed et beatórum Apostolórum ac Mártyrum tuórum, Petri et Pauli, Andréæ, Iacóbi, Ioánnis, Thomæ, Iacóbi, Philíppi, Bartholomǽi, Matthǽi, Simónis et Thaddǽi: Lini, Cleti, Cleméntis, Xysti, Cornélii, Cypriáni, Lauréntii, Chrysógoni, Ioánnis et Pauli, Cosmæ et Damiáni: et ómnium Sanctórum tuórum; quorum méritis precibúsque concédas, ut in ómnibus protectiónis tuæ muniámur auxílio. Per eúndem Christum Dóminum nostrum. Amen.", "en": "In communion with, and honouring the memory in the first place of the glorious ever-virgin Mary, Mother of our God and Lord Jesus Christ as also of thy blessed Apostles and Martyrs, Peter and Paul, Andrew, James, John, Thomas, James, Philip, Bartholomew, Matthew, Simon and Thaddeus; Linus, Cletus, Clement, Xystus, Cornelius, Cyprian, Laurence, Chrysogonus, John and Paul, Cosmas and Damian, and of all thy Saints; by whose merits and prayers grant that we may in all things be defended by the help of thy protection. Through the same Christ our Lord. Amen."},
    {"r": "With hands extended as for the prayers (not over the offerings):", "ref": ["modus-ix-3"]},
    {"w": "P", "la": "Hanc ígitur oblatiónem servitútis nostræ, sed et cunctæ famíliæ tuæ, quǽsumus, Dómine, ut placátus accípias: diésque nostros in tua pace dispónas, atque ab ætérna damnatióne nos éripi, et in electórum tuórum iúbeas grege numerári. Per Christum Dóminum nostrum. Amen.", "en": "We therefore beseech thee, O Lord, graciously to accept this oblation of our service and that of all thy household; order our days in thy peace, and bid us be delivered from eternal damnation and numbered in the flock of thine elect. Through Christ our Lord. Amen."},
    {"r": "He makes three crosses over the offerings, then one over the Host and one over the chalice; he bows at Jesu Christi:", "ref": ["modus-ix-4"]},
    {"w": "P", "la": "Quam oblatiónem tu, Deus, in ómnibus, quǽsumus, bene ✠ díctam, adscríp ✠ tam, ra ✠ tam, rationábilem, acceptabilémque fácere dignéris: ut nobis Cor ✠ pus et San ✠ guis fiat dilectíssimi Fílii tui Dómini nostri Iesu Christi.", "en": "Which oblation do thou, O God, vouchsafe in all things to make ✠ blessed, ✠ approved, ✠ ratified, reasonable and acceptable; that it may become for us the ✠ Body and ✠ Blood of thy most beloved Son, our Lord Jesus Christ."},
    {"r": "He wipes his fingers on the corporal and takes the Host; he raises his eyes at elevatis oculis and blesses the Host at benedixit. Bending a little, he says the words of consecration secretly and without pause:", "ref": ["modus-x-1", "modus-x-2"]},
    {"w": "P", "la": "Qui prídie quam paterétur, accépit panem in sanctas ac venerábiles manus suas, et elevátis óculis in cælum ad te Deum Patrem suum omnipoténtem, tibi grátias agens, bene ✠ díxit, fregit, dedítque discípulis suis, dicens: Accípite, et manducáte ex hoc omnes. HOC EST ENIM CORPUS MEUM.", "en": "Who the day before he suffered took bread into his holy and venerable hands, and with his eyes lifted up to heaven, unto thee, O God, his almighty Father, giving thanks to thee, he ✠ blessed it, broke it, and gave it to his disciples, saying: Take and eat ye all of this. FOR THIS IS MY BODY."},
    {"r": "He kneels and adores; rising, he elevates the Host so that it can be seen, lays it on the corporal, and adores again. From now on he keeps thumb and forefinger joined.", "ref": ["modus-x-2"]},
    {"m": "l", "r": "Kneeling behind the priest, the server rings the bell at each elevation and raises the chasuble.", "ref": ["varia-vi-7"]},
    {"m": "s", "r": "The bell is rung at each elevation.", "ref": ["varia-vi-7"]},
    {"m": "mc", "if": "thur", "r": "The deacon and the subdeacon (with the paten) kneel on the top step at the priest’s right and left, an acolyte beside each; one acolyte rings the bell.", "ref": ["ministri-xv-1"]},
    {"m": "mc", "if": "!thur", "r": "The deacon and the subdeacon kneel on the top step at the priest’s right and left, an acolyte beside each; one acolyte rings the bell.", "ref": ["ministri-xv-1"]},
    {"m": "mc", "if": "full,thur", "r": "The deacon takes the thurible and incenses at each elevation.", "ref": ["ministri-xv-1"]},
    {"r": "He uncovers the chalice; taking it in both hands, he blesses it at benedixit, and says the words of consecration:", "ref": ["modus-x-3", "modus-x-4"]},
    {"w": "P", "la": "Símili modo postquam cenátum est, accípiens et hunc præclárum Cálicem in sanctas ac venerábiles manus suas: item tibi grátias agens, bene ✠ díxit, dedítque discípulis suis, dicens: Accípite, et bíbite ex eo omnes. HIC EST ENIM CALIX SÁNGUINIS MEI, NOVI ET ÆTÉRNI TESTAMÉNTI: MYSTÉRIUM FÍDEI: QUI PRO VOBIS ET PRO MULTIS EFFUNDÉTUR IN REMISSIÓNEM PECCATÓRUM.", "en": "In like manner, after he had supped, taking also this excellent chalice into his holy and venerable hands, and giving thanks to thee, he ✠ blessed it, and gave it to his disciples, saying: Take and drink ye all of this. FOR THIS IS THE CHALICE OF MY BLOOD, OF THE NEW AND ETERNAL TESTAMENT: THE MYSTERY OF FAITH: WHICH SHALL BE SHED FOR YOU AND FOR MANY UNTO THE REMISSION OF SINS."},
    {"r": "He sets the chalice down and adores; rising, he elevates it, sets it down, and says:", "ref": ["modus-x-4"]},
    {"w": "P", "la": "Hæc quotiescúmque fecéritis, in mei memóriam faciétis.", "en": "As often as ye shall do these things, ye shall do them in remembrance of me."},
    {"r": "He covers the chalice and adores again. Then, with arms extended:", "ref": ["modus-x-4", "modus-xi-1"]},
    {"r": "At Hostiam puram he makes three crosses over the offerings, then one over the Host and one over the chalice:", "ref": ["modus-xi-1"]},
    {"w": "P", "la": "Unde et mémores, Dómine, nos servi tui, sed et plebs tua sancta, eiúsdem Christi Fílii tui Dómini nostri tam beátæ passiónis, nec non et ab ínferis resurrectiónis, sed et in cælos gloriósæ ascensiónis: offérimus præcláræ maiestáti tuæ de tuis donis ac datis, hóstiam ✠ puram, hóstiam ✠ sanctam, hóstiam ✠ immaculátam, Panem ✠ sanctum vitæ ætérnæ, et Cálicem ✠ salútis perpétuæ.", "en": "Wherefore, O Lord, we thy servants, as also thy holy people, calling to mind the blessed passion of the same Christ thy Son our Lord, his resurrection from the dead, and his glorious ascension into heaven, offer unto thy most excellent majesty, of thine own gifts bestowed upon us, a pure ✠ victim, a holy ✠ victim, a spotless ✠ victim, the holy ✠ Bread of eternal life, and the Chalice ✠ of everlasting salvation."},
    {"r": "With hands extended:", "ref": ["modus-xi-2"]},
    {"w": "P", "la": "Supra quæ propítio ac seréno vultu respícere dignéris: et accépta habére, sícuti accépta habére dignátus es múnera púeri tui iusti Abel, et sacrifícium patriárchæ nostri Abrahæ: et quod tibi óbtulit summus sacérdos tuus Melchísedech, sanctum sacrifícium, immaculátam hóstiam.", "en": "Upon which vouchsafe to look with a propitious and serene countenance, and to accept them, as thou wert graciously pleased to accept the gifts of thy just servant Abel, and the sacrifice of our patriarch Abraham, and that which thy high priest Melchisedech offered to thee, a holy sacrifice, an unspotted victim."},
    {"r": "Bowing profoundly with arms crossed; rising at ut quotquot, he kisses the corporal; he blesses the Host and the chalice, and signs himself at benedictione caelesti:", "ref": ["modus-xi-2"]},
    {"w": "P", "la": "Súpplices te rogámus, omnípotens Deus: iube hæc perférri per manus sancti Angeli tui in sublíme altáre tuum, in conspéctu divínæ maiestátis tuæ: ut quotquot ex hac altáris participatióne sacrosánctum Fílii tui Cor ✠ pus et Sán ✠ guinem sumpsérimus, omni benedictióne cælésti et grátia repleámur. Per eúndem Christum Dóminum nostrum. Amen.", "en": "We most humbly beseech thee, almighty God, command these things to be carried by the hands of thy holy Angel to thine altar on high, in the sight of thy divine majesty; that as many of us as, by this participation at the altar, shall receive the most sacred ✠ Body and ✠ Blood of thy Son, may be filled with every heavenly blessing and grace. Through the same Christ our Lord. Amen."},
    {"r": "With hands joined; at N. et N. he pauses to pray in silence for the dead:", "ref": ["modus-xi-3"]},
    {"w": "P", "la": "Meménto étiam, Dómine, famulórum famularúmque tuárum N. et N., qui nos præcessérunt cum signo fídei, et dórmiunt in somno pacis. Ipsis, Dómine, et ómnibus in Christo quiescéntibus, locum refrigérii, lucis et pacis, ut indúlgeas, deprecámur. Per eúndem Christum Dóminum nostrum. Amen.", "en": "Be mindful also, O Lord, of thy servants and handmaids N. and N., who are gone before us with the sign of faith, and sleep in the sleep of peace. To these, O Lord, and to all who rest in Christ, grant, we beseech thee, a place of refreshment, light and peace. Through the same Christ our Lord. Amen."},
    {"r": "Striking his breast, he says the first three words aloud:", "ref": ["modus-xi-3"]},
    {"w": "P", "la": "Nobis quoque peccatóribus fámulis tuis, de multitúdine miseratiónum tuárum sperántibus, partem áliquam et societátem donáre dignéris, cum tuis sanctis Apóstolis et Martýribus: cum Ioánne, Stéphano, Matthía, Bárnaba, Ignátio, Alexándro, Marcellíno, Petro, Felicitáte, Perpétua, Agatha, Lúcia, Agnéte, Cæcília, Anastásia, et ómnibus Sanctis tuis: intra quorum nos consórtium, non æstimátor mériti, sed véniæ, quǽsumus, largítor admítte. Per Christum Dóminum nostrum.", "en": "To us sinners also, thy servants, hoping in the multitude of thy mercies, vouchsafe to grant some part and fellowship with thy holy Apostles and Martyrs: with John, Stephen, Matthias, Barnabas, Ignatius, Alexander, Marcellinus, Peter, Felicitas, Perpetua, Agatha, Lucy, Agnes, Cecilia, Anastasia, and all thy Saints: into whose company we beseech thee to admit us, not weighing our merits, but freely pardoning our offences. Through Christ our Lord."},
    {"r": "He blesses the offerings at sanctificas, vivificas, benedicis; he uncovers the chalice and genuflects; with the Host he makes three crosses over the chalice and two before it; he lays the Host down, covers the chalice, and genuflects:", "ref": ["modus-xi-4"]},
    {"w": "P", "la": "Per quem hæc ómnia, Dómine, semper bona creas, sancti ✠ fícas, vivi ✠ fícas, bene ✠ dícis, et præstas nobis. Per ip ✠ sum, et cum ip ✠ so, et in ip ✠ so, est tibi Deo Patri ✠ omnipoténti, in unitáte Spíritus ✠ Sancti, omnis honor et glória.", "en": "By whom, O Lord, thou dost always create, ✠ sanctify, ✠ quicken, ✠ bless and bestow upon us all these good things. Through ✠ him, and with ✠ him, and in ✠ him, is unto thee, God the Father ✠ almighty, in the unity of the Holy ✠ Ghost, all honour and glory."},
    {"w": "P", "la": "Per ómnia sǽcula sæculórum.", "en": "World without end."},
    {"w": "S", "la": "Amen.", "en": "Amen."}
  ]},
  pater: {la: "Pater noster", en: "The Lord’s Prayer", lines: [
    {"w": "P", "la": "Orémus. Præcéptis salutáribus móniti, et divína institutióne formáti, audémus dícere:", "en": "Let us pray. Admonished by saving precepts, and following the divine institution, we make bold to say:"},
    {"w": "P", "la": "Pater noster, qui es in cælis, sanctificétur nomen tuum: advéniat regnum tuum: fiat volúntas tua, sicut in cælo, et in terra. Panem nostrum quotidiánum da nobis hódie: et dimítte nobis débita nostra, sicut et nos dimíttimus debitóribus nostris. Et ne nos indúcas in tentatiónem.", "en": "Our Father, who art in heaven, hallowed be thy name; thy kingdom come; thy will be done on earth as it is in heaven. Give us this day our daily bread; and forgive us our trespasses, as we forgive them that trespass against us. And lead us not into temptation."},
    {"w": "S", "la": "Sed líbera nos a malo.", "en": "But deliver us from evil."},
    {"w": "P", "la": "Amen.", "en": "Amen."},
    {"w": "P", "la": "Líbera nos, quǽsumus, Dómine, ab ómnibus malis prætéritis, præséntibus et futúris: et intercedénte beáta et gloriósa semper Vírgine Dei Genetríce María, cum beátis Apóstolis tuis Petro et Paulo, atque Andréa, et ómnibus Sanctis, da propítius pacem in diébus nostris: ut, ope misericórdiæ tuæ adiúti, et a peccáto simus semper líberi et ab omni perturbatióne secúri. Per eúndem Dóminum nostrum Iesum Christum Fílium tuum, qui tecum vivit et regnat in unitáte Spíritus Sancti Deus,", "en": "Deliver us, we beseech thee, O Lord, from all evils, past, present and to come; and by the intercession of the blessed and glorious ever-virgin Mary, Mother of God, together with thy blessed Apostles Peter and Paul, and Andrew, and all the Saints, mercifully grant peace in our days; that, aided by the help of thy mercy, we may be always free from sin and secure from all disturbance. Through the same Jesus Christ thy Son our Lord, who liveth and reigneth with thee in the unity of the Holy Ghost, God,"},
    {"w": "P", "la": "Per ómnia sǽcula sæculórum.", "en": "World without end."},
    {"w": "S", "la": "Amen.", "en": "Amen."},
    {"w": "P", "la": "Pax ✠ Dómini sit ✠ semper vobís ✠ cum.", "en": "The peace ✠ of the Lord ✠ be always with ✠ you."},
    {"w": "S", "la": "Et cum spíritu tuo.", "en": "And with thy spirit."}
  ], adv: [
    {"r": "His hands are laid on the corporal; at Pater noster he raises and extends them:", "ref": ["modus-xii-1"]},
    {"w": "P", "la": "Orémus. Præcéptis salutáribus móniti, et divína institutióne formáti, audémus dícere:", "en": "Let us pray. Admonished by saving precepts, and following the divine institution, we make bold to say:"},
    {"w": "P", "la": "Pater noster, qui es in cælis, sanctificétur nomen tuum: advéniat regnum tuum: fiat volúntas tua, sicut in cælo, et in terra. Panem nostrum quotidiánum da nobis hódie: et dimítte nobis débita nostra, sicut et nos dimíttimus debitóribus nostris. Et ne nos indúcas in tentatiónem.", "en": "Our Father, who art in heaven, hallowed be thy name; thy kingdom come; thy will be done on earth as it is in heaven. Give us this day our daily bread; and forgive us our trespasses, as we forgive them that trespass against us. And lead us not into temptation."},
    {"m": "mc", "r": "The ministers answer in a low voice:", "ref": ["ministri-xvi-1"]},
    {"w": "S", "la": "Sed líbera nos a malo.", "en": "But deliver us from evil."},
    {"w": "P", "la": "Amen.", "en": "Amen."},
    {"m": "mc", "if": "thur", "r": "The subdeacon gives the paten to the deacon, who hands it to the priest, kissing his shoulder.", "ref": ["ministri-xvi-1"]},
    {"m": "mc", "if": "!thur", "r": "The deacon takes the paten from the altar and hands it to the priest, kissing his shoulder.", "ref": ["ministri-xvi-2"]},
    {"r": "With hands extended; he bows at Maria:", "ref": ["modus-xii-1"]},
    {"w": "P", "la": "Líbera nos, quǽsumus, Dómine, ab ómnibus malis prætéritis, præséntibus et futúris: et intercedénte beáta et gloriósa semper Vírgine Dei Genetríce María, cum beátis Apóstolis tuis Petro et Paulo, atque Andréa, et ómnibus Sanctis, da propítius pacem in diébus nostris: ut, ope misericórdiæ tuæ adiúti, et a peccáto simus semper líberi et ab omni perturbatióne secúri. Per eúndem Dóminum nostrum Iesum Christum Fílium tuum, qui tecum vivit et regnat in unitáte Spíritus Sancti Deus,", "en": "Deliver us, we beseech thee, O Lord, from all evils, past, present and to come; and by the intercession of the blessed and glorious ever-virgin Mary, Mother of God, together with thy blessed Apostles Peter and Paul, and Andrew, and all the Saints, mercifully grant peace in our days; that, aided by the help of thy mercy, we may be always free from sin and secure from all disturbance. Through the same Jesus Christ thy Son our Lord, who liveth and reigneth with thee in the unity of the Holy Ghost, God,"},
    {"r": "At da propitius pacem he signs himself with the paten and kisses it; he uncovers the chalice, genuflects, and breaks the Host over the chalice, keeping back a particle. Aloud:", "ref": ["modus-xii-2", "modus-xii-3"]},
    {"w": "P", "la": "Per ómnia sǽcula sæculórum.", "en": "World without end."},
    {"w": "S", "la": "Amen.", "en": "Amen."},
    {"r": "With the particle he makes three crosses within the chalice:", "ref": ["modus-xii-3"]},
    {"w": "P", "la": "Pax ✠ Dómini sit ✠ semper vobís ✠ cum.", "en": "The peace ✠ of the Lord ✠ be always with ✠ you."},
    {"w": "S", "la": "Et cum spíritu tuo.", "en": "And with thy spirit."}
  ]},
  rAg: {la: "", en: "", strip: 1, lines: [

  ], adv: [
    {"m": "ls", "r": "He says the Agnus Dei aloud, holding the Host over the chalice.", "ref": ["modus-xiii-1"]},
    {"m": "mc", "r": "The deacon goes to the Gospel corner and the subdeacon to the Epistle corner, each with an acolyte, and they say the Agnus Dei with the priest.", "ref": ["ministri-xvii-1"]}
  ]},
  agLow: {la: "Agnus Dei", en: "Agnus Dei", lines: [
    {"w": "P", "la": "Agnus Dei, qui tollis peccáta mundi: miserére nobis. Agnus Dei, qui tollis peccáta mundi: miserére nobis. Agnus Dei, qui tollis peccáta mundi: dona nobis pacem.", "en": "Lamb of God, who takest away the sins of the world, have mercy on us. Lamb of God, who takest away the sins of the world, have mercy on us. Lamb of God, who takest away the sins of the world, grant us peace.", "if": "!req"},
    {"if": "req", "w": "P", "la": "Agnus Dei, qui tollis peccáta mundi: dona eis réquiem. Agnus Dei, qui tollis peccáta mundi: dona eis réquiem. Agnus Dei, qui tollis peccáta mundi: dona eis réquiem sempitérnam.", "en": "Lamb of God, who takest away the sins of the world, grant them rest. Lamb of God, who takest away the sins of the world, grant them rest. Lamb of God, who takest away the sins of the world, grant them rest eternal."}
  ]},
  commSimple: {la: "Communio fidelium", en: "Communion of the faithful", lines: [
    {"r": "Communion of the faithful. When there are some to receive Communion, the server says the Confiteor:"},
    {"w": "S", "la": "Confíteor Deo omnipoténti, et beátæ Maríæ semper Vírgini, et beáto Domínico patri nostro, et ómnibus Sanctis, et tibi, pater, quia peccávi nimis cogitatióne, locutióne, ópere et omissióne, mea culpa: precor te oráre pro me.", "en": "I confess to almighty God, to blessed Mary ever a virgin, to blessed Dominic our father, to all the saints, and to thee, father, that I have sinned exceedingly in thought, word, deed and omission, through my fault: I beseech thee to pray for me."},
    {"r": "The priest, turned to the communicants, says:"},
    {"w": "P", "la": "Misereátur vestri omnípotens Deus, et dimíttat vobis ómnia peccáta vestra: líberet vos ab omni malo, salvet et confírmet in omni ópere bono, et perdúcat vos ad vitam ætérnam.", "en": "May almighty God have mercy on you and forgive you all your sins: may he deliver you from all evil, save and strengthen you in every good work, and bring you to life everlasting."},
    {"w": "S", "la": "Amen.", "en": "Amen."},
    {"w": "P", "la": "Absolutiónem et remissiónem ómnium peccatórum vestrórum tríbuat vobis omnípotens et miséricors Dóminus.", "en": "May the almighty and merciful Lord grant you pardon and remission of all your sins."},
    {"w": "S", "la": "Amen.", "en": "Amen."},
    {"r": "Holding up a Host over the pyx or paten, turned to the people, he says:"},
    {"w": "P", "la": "Ecce Agnus Dei, ecce qui tollit peccáta mundi.", "en": "Behold the Lamb of God, behold him who taketh away the sins of the world."},
    {"r": "And three times:"},
    {"w": "P", "la": "Dómine, non sum dignus, ut intres sub tectum meum: sed tantum dic verbo, et sanábitur ánima mea.", "en": "Lord, I am not worthy that thou shouldst enter under my roof; but only say the word, and my soul shall be healed."},
    {"r": "Giving Communion to each:"},
    {"w": "P", "la": "Corpus Dómini nostri Iesu Christi custódiat te in vitam ætérnam. Amen.", "en": "May the Body of our Lord Jesus Christ keep thee unto life everlasting. Amen."}
  ]},
  commConv: {la: "Communio Fratrum", en: "Communion of the friars", lines: [
    {"r": "The Communion of the friars. Those who are to communicate come in choir order towards the sanctuary, bow profoundly and kneel."},
    {"if": "!sac", "r": "The deacon brings the pyx, the candle-bearers going before, and sets it on the corporal; all prostrate in adoration while he brings it, the celebrant genuflecting."},
    {"if": "tab", "r": "The deacon takes the pyx from the tabernacle and sets it on the corporal."},
    {"r": "The ministers prostrate, the others stretched out in the venia, all say together:"},
    {"w": "S", "la": "Confíteor Deo omnipoténti, et beátæ Maríæ semper Vírgini, et beáto Domínico patri nostro, et ómnibus Sanctis, et tibi, pater, quia peccávi nimis cogitatióne, locutióne, ópere et omissióne, mea culpa: precor te oráre pro me.", "en": "I confess to almighty God, to blessed Mary ever a virgin, to blessed Dominic our father, to all the saints, and to thee, father, that I have sinned exceedingly in thought, word, deed and omission, through my fault: I beseech thee to pray for me."},
    {"r": "The priest, stepping aside from the middle so as not to turn his back to the Sacrament, says:"},
    {"w": "P", "la": "Misereátur vestri omnípotens Deus, et dimíttat vobis ómnia peccáta vestra: líberet vos ab omni malo, salvet et confírmet in omni ópere bono, et perdúcat vos ad vitam ætérnam.", "en": "May almighty God have mercy on you and forgive you all your sins: may he deliver you from all evil, save and strengthen you in every good work, and bring you to life everlasting."},
    {"w": "S", "la": "Amen.", "en": "Amen."},
    {"w": "P", "la": "Absolutiónem et remissiónem ómnium peccatórum vestrórum tríbuat vobis omnípotens et miséricors Dóminus.", "en": "May the almighty and merciful Lord grant you pardon and remission of all your sins."},
    {"w": "S", "la": "Amen.", "en": "Amen."},
    {"r": "All rise on their knees. The ministers communicate first, by rank, then the other friars, in their cappas, two by two; the deacon and subdeacon hold the communion cloth."},
    {"r": "Making the sign of the cross with the Host before each, the priest says:"},
    {"w": "P", "la": "Corpus Dómini nostri Iesu Christi custódiat te in vitam ætérnam. Amen.", "en": "May the Body of our Lord Jesus Christ keep thee unto life everlasting. Amen."},
    {"r": "They withdraw sideways, so as not to turn their backs to the Sacrament; the friars return to their stalls and give thanks in silence. Those who do not communicate lie prostrate meanwhile."},
    {"r": "The priest sets the pyx on the corporal and continues the Mass; the hosts that remain are reserved."}
  ]},
  communion: {la: "Communio", en: "Communion", lines: [
    {"w": "P", "la": "Hæc sacrosáncta commíxtio Córporis et Sánguinis Dómini nostri Iesu Christi fiat mihi et ómnibus suméntibus salus mentis et córporis, et ad vitam ætérnam promeréndam et capesséndam præparátio salutáris. Per eúndem Christum Dóminum nostrum. Amen.", "en": "May this most holy mingling of the Body and Blood of our Lord Jesus Christ be to me and to all who receive it health of mind and body, and a saving preparation for the meriting and the obtaining of eternal life. Through the same Christ our Lord. Amen."},
    {"w": "P", "la": "Pax tibi, et Ecclésiæ sanctæ Dei.", "en": "Peace be to thee and to the holy Church of God.", "if": "!req"},
    {"w": "P", "la": "Dómine Iesu Christe, Fili Dei vivi, qui ex voluntáte Patris, cooperánte Spíritu Sancto, per mortem tuam mundum vivificásti: líbera me per hoc sacrosánctum Corpus et Sánguinem tuum ab ómnibus iniquitátibus meis et univérsis malis: et fac me tuis semper inhærére mandátis, et a te numquam separári permíttas. Qui cum eódem Deo Patre et Spíritu Sancto vivis et regnas Deus, in sǽcula sæculórum. Amen.", "en": "O Lord Jesus Christ, Son of the living God, who by the will of the Father, the Holy Ghost cooperating, hast by thy death given life to the world: deliver me by this thy most sacred Body and Blood from all my iniquities and from all evils; make me always cleave to thy commandments, and never suffer me to be separated from thee. Who with the same God the Father and the Holy Ghost livest and reignest God, world without end. Amen."},
    {"w": "P", "la": "Corpus et Sanguis Dómini nostri Iesu Christi custódiant me in vitam ætérnam. Amen.", "en": "May the Body and Blood of our Lord Jesus Christ keep me unto life everlasting. Amen."},
    {"r": "Communion of the faithful."},
    {"w": "P", "la": "Ecce Agnus Dei, ecce qui tollit peccáta mundi.", "en": "Behold the Lamb of God, behold him who taketh away the sins of the world."},
    {"w": "P", "la": "Dómine, non sum dignus, ut intres sub tectum meum: sed tantum dic verbo, et sanábitur ánima mea.", "en": "Lord, I am not worthy that thou shouldst enter under my roof; but only say the word, and my soul shall be healed."},
    {"w": "P", "la": "Corpus Dómini nostri Iesu Christi custódiat te in vitam ætérnam. Amen.", "en": "May the Body of our Lord Jesus Christ keep thee unto life everlasting. Amen."},
    {"w": "P", "la": "Quod ore súmpsimus, Dómine, pura mente capiámus: ut de Córpore et Sánguine Dómini nostri Iesu Christi fiat nobis remédium sempitérnum. Amen.", "en": "What we have taken with our mouth, O Lord, may we receive with a pure mind; that from the Body and Blood of our Lord Jesus Christ there may come to us an everlasting remedy. Amen."}
  ], adv: [
    {"r": "Letting the particle fall into the chalice, he says secretly:", "ref": ["modus-xiii-1"]},
    {"w": "P", "la": "Hæc sacrosáncta commíxtio Córporis et Sánguinis Dómini nostri Iesu Christi fiat mihi et ómnibus suméntibus salus mentis et córporis, et ad vitam ætérnam promeréndam et capesséndam præparátio salutáris. Per eúndem Christum Dóminum nostrum. Amen.", "en": "May this most holy mingling of the Body and Blood of our Lord Jesus Christ be to me and to all who receive it health of mind and body, and a saving preparation for the meriting and the obtaining of eternal life. Through the same Christ our Lord. Amen."},
    {"m": "ls", "if": "!req", "r": "He kisses the lip of the chalice and gives the peace to the server, who holds the pall:", "ref": ["modus-xiii-1"]},
    {"m": "mc", "if": "!req", "r": "He kisses the lip of the chalice; the deacon holds out the Pax for him to kiss, and he says:", "ref": ["ministri-xvii-1"]},
    {"w": "P", "la": "Pax tibi, et Ecclésiæ sanctæ Dei.", "en": "Peace be to thee and to the holy Church of God.", "if": "!req"},
    {"m": "mc", "if": "!req", "r": "The deacon gives the Pax to the subdeacon, and he to the acolytes.", "ref": ["ministri-xvii-1"]},
    {"m": "mc", "if": "pope,!req", "r": "The deacon also takes the Pax to the Pope.", "ref": ["varia-iii-5"]},
    {"m": "mc", "if": "bp,!req", "r": "The deacon also takes the Pax to the Bishop.", "ref": ["varia-iii-5"]},
    {"m": "c", "if": "mo,sd,!sol,!req", "r": "The acolyte takes the Pax to him, and the brethren receive it after him in order.", "ref": ["ministri-xvii-2"]},
    {"m": "c", "if": "sd,!sol,!mo,!req", "r": "An acolyte takes the Pax to the cantors, and they give it to the brethren in order.", "ref": ["ministri-xvii-2"]},
    {"m": "c", "if": "sol,!req", "r": "The subdeacon himself, an acolyte going before, takes the Pax to the cantors and the brethren in the choir.", "ref": ["ministri-xvii-3"]},
    {"r": "With head bowed, he says with all devotion this one prayer, adding no other and not striking his breast:", "ref": ["modus-xiii-2"]},
    {"w": "P", "la": "Dómine Iesu Christe, Fili Dei vivi, qui ex voluntáte Patris, cooperánte Spíritu Sancto, per mortem tuam mundum vivificásti: líbera me per hoc sacrosánctum Corpus et Sánguinem tuum ab ómnibus iniquitátibus meis et univérsis malis: et fac me tuis semper inhærére mandátis, et a te numquam separári permíttas. Qui cum eódem Deo Patre et Spíritu Sancto vivis et regnas Deus, in sǽcula sæculórum. Amen.", "en": "O Lord Jesus Christ, Son of the living God, who by the will of the Father, the Holy Ghost cooperating, hast by thy death given life to the world: deliver me by this thy most sacred Body and Blood from all my iniquities and from all evils; make me always cleave to thy commandments, and never suffer me to be separated from thee. Who with the same God the Father and the Holy Ghost livest and reignest God, world without end. Amen."},
    {"r": "Holding the chalice in his right hand, he receives the Host, saying:", "ref": ["modus-xiii-2"]},
    {"w": "P", "la": "Corpus et Sanguis Dómini nostri Iesu Christi custódiant me in vitam ætérnam. Amen.", "en": "May the Body and Blood of our Lord Jesus Christ keep me unto life everlasting. Amen."},
    {"r": "He covers the chalice and rests a moment in meditation; then he genuflects and receives the Blood with the particle, saying nothing.", "ref": ["modus-xiii-2"]},
    {"r": "He gathers any particles on the corporal into the chalice with the paten, and consumes them.", "ref": ["modus-xiii-3"]},
    {"r": "Communion of the faithful."},
    {"w": "P", "la": "Ecce Agnus Dei, ecce qui tollit peccáta mundi.", "en": "Behold the Lamb of God, behold him who taketh away the sins of the world."},
    {"w": "P", "la": "Dómine, non sum dignus, ut intres sub tectum meum: sed tantum dic verbo, et sanábitur ánima mea.", "en": "Lord, I am not worthy that thou shouldst enter under my roof; but only say the word, and my soul shall be healed."},
    {"w": "P", "la": "Corpus Dómini nostri Iesu Christi custódiat te in vitam ætérnam. Amen.", "en": "May the Body of our Lord Jesus Christ keep thee unto life everlasting. Amen."},
    {"m": "l", "r": "The server pours wine for the first ablution and wine and water for the second, moves the Missal, and puts out the elevation candle.", "ref": ["varia-vi-8"]},
    {"m": "mc", "r": "The subdeacon pours the ablutions; the deacon moves the Missal and folds the corporal; the acolytes put out the elevation candles.", "ref": ["ministri-xviii-1"]},
    {"r": "He takes the first ablution, of wine, saying nothing; at the second, of wine and water poured over his fingers, he says:", "ref": ["modus-xiv-1"]},
    {"w": "P", "la": "Quod ore súmpsimus, Dómine, pura mente capiámus: ut de Córpore et Sánguine Dómini nostri Iesu Christi fiat nobis remédium sempitérnum. Amen.", "en": "What we have taken with our mouth, O Lord, may we receive with a pure mind; that from the Body and Blood of our Lord Jesus Christ there may come to us an everlasting remedy. Amen."},
    {"m": "ls", "r": "He wipes his fingers and the chalice and covers it; then he goes to the Missal at the Epistle corner and reads the Communion.", "ref": ["modus-xiv-1", "modus-xiv-2"]},
    {"m": "mc", "r": "The subdeacon purifies and covers the chalice; the priest goes to the Missal and reads the Communion.", "ref": ["ministri-xviii-1"]},
    {"if": "exp", "r": "He genuflects as he leaves the middle for the Communion.", "ref": ["varia-ii-4"]}
  ]},
  post: {la: "Postcommunio", en: "Postcommunion", lines: [
    {"w": "P", "la": "Dóminus vobíscum.", "en": "The Lord be with you."},
    {"w": "S", "la": "Et cum spíritu tuo.", "en": "And with thy spirit."},
    {"w": "P", "la": "Orémus.", "en": "Let us pray."}
  ], adv: [
    {"if": "!sac", "r": "Turning to the people as before:", "ref": ["modus-xiv-2"]},
    {"if": "tab", "r": "He turns as at the Collect, by his right, without turning his back to it:", "ref": ["varia-ii-9"]},
    {"if": "exp", "r": "He turns as at the Collect, from the Gospel side of the middle, genuflecting before and after:", "ref": ["varia-ii-5"]},
    {"m": "mc", "r": "The deacon lifts the hem of the chasuble.", "ref": ["ministri-xix-1"]},
    {"w": "P", "la": "Dóminus vobíscum.", "en": "The Lord be with you."},
    {"w": "S", "la": "Et cum spíritu tuo.", "en": "And with thy spirit."},
    {"r": "Turned back to the book, bowing to the cross:", "ref": ["modus-xiv-2"]},
    {"w": "P", "la": "Orémus.", "en": "Let us pray."},
    {"r": "He reads the Postcommunion with hands extended.", "ref": ["modus-xiv-2"]},
    {"m": "ls", "if": "sp", "r": "After the last Postcommunion he says Oremus with head bowed, and Humiliate capita vestra Deo; then the Prayer over the people.", "ref": ["modus-xiv-3"]},
    {"m": "mc", "if": "sp", "r": "After the last Postcommunion the priest says Oremus, bowing with the ministers; the deacon sings Humiliate capita vestra Deo; then the priest says the Prayer over the people.", "ref": ["ministri-xix-2"]},
    {"m": "mc", "r": "During the last prayers the subdeacon takes the chalice back to the sacristy.", "ref": ["ministri-xix-3"]}
  ]},
  postEnd: {la: "Dimissio", en: "Dismissal", lines: [
    {"w": "P", "la": "Dóminus vobíscum.", "en": "The Lord be with you."},
    {"w": "S", "la": "Et cum spíritu tuo.", "en": "And with thy spirit."}
  ], adv: [
    {"if": "!sac", "r": "At the end of the last prayer he comes to the middle and turns to the people:", "ref": ["modus-xiv-2", "modus-xv-1"]},
    {"if": "tab", "r": "At the end of the last prayer he comes to the middle and turns to the people as at the Collect, by his right:", "ref": ["varia-ii-9"]},
    {"if": "exp", "r": "At the end of the last prayer he genuflects at the middle and turns to the people from the Gospel side:", "ref": ["varia-ii-5"]},
    {"w": "P", "la": "Dóminus vobíscum.", "en": "The Lord be with you."},
    {"w": "S", "la": "Et cum spíritu tuo.", "en": "And with thy spirit."},
    {"m": "ls", "if": "!nogl,!req", "r": "Still facing the people:", "ref": ["modus-xv-1"]},
    {"m": "ls", "if": "nogl", "r": "Facing the altar:", "ref": ["modus-xv-1"]},
    {"m": "mc", "if": "!nogl,!req", "r": "The deacon, turning with the priest, sings it; then they turn back to the altar without going round:", "ref": ["ministri-xx-1"]},
    {"m": "mc", "if": "nogl", "r": "The deacon sings it facing the altar with the priest:", "ref": ["ministri-xx-1"]}
  ]},
  end: {la: "Finis Missæ", en: "The end of Mass", lines: [
    {"w": "P", "la": "Pláceat tibi, sancta Trínitas, obséquium servitútis meæ: et præsta, ut sacrifícium, quod óculis tuæ maiestátis indígnus óbtuli, tibi sit acceptábile, mihíque et ómnibus pro quibus illud óbtuli, sit, te miseránte, propitiábile. Per Christum Dóminum nostrum. Amen.", "en": "May the homage of my service be pleasing to thee, O holy Trinity; and grant that the sacrifice which I, unworthy, have offered in the sight of thy majesty may be acceptable to thee, and through thy mercy be a propitiation for me and for all those for whom I have offered it. Through Christ our Lord. Amen."},
    {"w": "P", "la": "Benedíctio Dei omnipoténtis, Pa ✠ tris, et Fílii, et Spíritus Sancti, descéndat super vos et máneat semper.", "en": "May the blessing of almighty God, the Father ✠, and the Son, and the Holy Ghost, descend upon you and remain for ever.", "if": "!req"},
    {"w": "S", "la": "Amen.", "en": "Amen.", "if": "!req"},
    {"w": "P", "la": "Dóminus vobíscum.", "en": "The Lord be with you."},
    {"w": "S", "la": "Et cum spíritu tuo.", "en": "And with thy spirit."},
    {"w": "P", "la": "Inítium sancti Evangélii secúndum Ioánnem.", "en": "The beginning of the holy Gospel according to John."},
    {"w": "S", "la": "Glória tibi, Dómine.", "en": "Glory be to thee, O Lord."},
    {"w": "P", "la": "In princípio erat Verbum, et Verbum erat apud Deum, et Deus erat Verbum. Hoc erat in princípio apud Deum. Omnia per ipsum facta sunt: et sine ipso factum est nihil, quod factum est: in ipso vita erat, et vita erat lux hóminum: et lux in ténebris lucet, et ténebræ eam non comprehendérunt. Fuit homo missus a Deo, cui nomen erat Ioánnes. Hic venit in testimónium, ut testimónium perhibéret de lúmine, ut omnes créderent per illum. Non erat ille lux, sed ut testimónium perhibéret de lúmine. Erat lux vera, quæ illúminat omnem hóminem veniéntem in hunc mundum. In mundo erat, et mundus per ipsum factus est, et mundus eum non cognóvit. In própria venit, et sui eum non recepérunt. Quotquot autem recepérunt eum, dedit eis potestátem fílios Dei fíeri, his, qui credunt in nómine eius: qui non ex sanguínibus, neque ex voluntáte carnis, neque ex voluntáte viri, sed ex Deo nati sunt. (Hic genuflectitur.) Et Verbum caro factum est, et habitávit in nobis: et vídimus glóriam eius, glóriam quasi Unigéniti a Patre, plenum grátiæ et veritátis.", "en": "In the beginning was the Word, and the Word was with God, and the Word was God. The same was in the beginning with God. All things were made by him: and without him was made nothing that was made. In him was life, and the life was the light of men: and the light shineth in darkness, and the darkness did not comprehend it. There was a man sent from God, whose name was John. This man came for a witness, to give testimony of the light, that all men might believe through him. He was not the light, but was to give testimony of the light. That was the true light, which enlighteneth every man that cometh into this world. He was in the world, and the world was made by him, and the world knew him not. He came unto his own, and his own received him not. But as many as received him, he gave them power to be made the sons of God, to them that believe in his name: who are born, not of blood, nor of the will of the flesh, nor of the will of man, but of God. (Here all kneel.) And the Word was made flesh, and dwelt among us: and we saw his glory, the glory as it were of the only-begotten of the Father, full of grace and truth."},
    {"w": "S", "la": "Deo grátias.", "en": "Thanks be to God."}
  ], adv: [
    {"r": "Turned back to the altar, bowing profoundly, he says secretly:", "ref": ["modus-xv-2"]},
    {"w": "P", "la": "Pláceat tibi, sancta Trínitas, obséquium servitútis meæ: et præsta, ut sacrifícium, quod óculis tuæ maiestátis indígnus óbtuli, tibi sit acceptábile, mihíque et ómnibus pro quibus illud óbtuli, sit, te miseránte, propitiábile. Per Christum Dóminum nostrum. Amen.", "en": "May the homage of my service be pleasing to thee, O holy Trinity; and grant that the sacrifice which I, unworthy, have offered in the sight of thy majesty may be acceptable to thee, and through thy mercy be a propitiation for me and for all those for whom I have offered it. Through Christ our Lord. Amen."},
    {"if": "!req,!prel", "r": "At Per Christum he kisses the altar; then, turning to the people, he blesses them with a single sign of the cross:", "ref": ["modus-xv-2"]},
    {"if": "!req,pope", "r": "At Per Christum he kisses the altar, and turns towards the Pope; kneeling as if asking leave to bless, he blesses the people on the side away from the Pope:", "ref": ["varia-iii-6"]},
    {"if": "!req,bp", "r": "At Per Christum he kisses the altar, and turns towards the Bishop; bowing as if asking leave to bless, he blesses the people on the side away from the Bishop:", "ref": ["varia-iii-6"]},
    {"if": "req", "r": "At Per Christum he kisses the altar.", "ref": ["modus-xv-2"]},
    {"m": "mc", "if": "!req", "r": "The ministers bow their heads.", "ref": ["ministri-xx-2"]},
    {"w": "P", "la": "Benedíctio Dei omnipoténtis, Pa ✠ tris, et Fílii, et Spíritus Sancti, descéndat super vos et máneat semper.", "en": "May the blessing of almighty God, the Father ✠, and the Son, and the Holy Ghost, descend upon you and remain for ever.", "if": "!req"},
    {"w": "S", "la": "Amen.", "en": "Amen.", "if": "!req"},
    {"if": "!sac", "r": "Completing the circle, he goes to the Gospel corner.", "ref": ["modus-xv-2"]},
    {"if": "tab", "r": "He turns back the way he came, bows his head before the tabernacle at the middle, and goes to the Gospel corner.", "ref": ["varia-ii-10"]},
    {"if": "exp", "r": "He returns to the middle, genuflects, and goes to the Gospel corner.", "ref": ["varia-ii-7"]},
    {"m": "mc", "r": "The acolytes hold their lighted candles; the deacon and subdeacon stand at the priest’s left for the last Gospel.", "ref": ["ministri-xx-2"]},
    {"r": "At the Gospel side he signs the altar with his thumb, and himself on the forehead, lips and breast; he genuflects at Et Verbum caro factum est:", "ref": ["modus-xv-3"]},
    {"w": "P", "la": "Dóminus vobíscum.", "en": "The Lord be with you."},
    {"w": "S", "la": "Et cum spíritu tuo.", "en": "And with thy spirit."},
    {"w": "P", "la": "Inítium sancti Evangélii secúndum Ioánnem.", "en": "The beginning of the holy Gospel according to John."},
    {"w": "S", "la": "Glória tibi, Dómine.", "en": "Glory be to thee, O Lord."},
    {"w": "P", "la": "In princípio erat Verbum, et Verbum erat apud Deum, et Deus erat Verbum. Hoc erat in princípio apud Deum. Omnia per ipsum facta sunt: et sine ipso factum est nihil, quod factum est: in ipso vita erat, et vita erat lux hóminum: et lux in ténebris lucet, et ténebræ eam non comprehendérunt. Fuit homo missus a Deo, cui nomen erat Ioánnes. Hic venit in testimónium, ut testimónium perhibéret de lúmine, ut omnes créderent per illum. Non erat ille lux, sed ut testimónium perhibéret de lúmine. Erat lux vera, quæ illúminat omnem hóminem veniéntem in hunc mundum. In mundo erat, et mundus per ipsum factus est, et mundus eum non cognóvit. In própria venit, et sui eum non recepérunt. Quotquot autem recepérunt eum, dedit eis potestátem fílios Dei fíeri, his, qui credunt in nómine eius: qui non ex sanguínibus, neque ex voluntáte carnis, neque ex voluntáte viri, sed ex Deo nati sunt. (Hic genuflectitur.) Et Verbum caro factum est, et habitávit in nobis: et vídimus glóriam eius, glóriam quasi Unigéniti a Patre, plenum grátiæ et veritátis.", "en": "In the beginning was the Word, and the Word was with God, and the Word was God. The same was in the beginning with God. All things were made by him: and without him was made nothing that was made. In him was life, and the life was the light of men: and the light shineth in darkness, and the darkness did not comprehend it. There was a man sent from God, whose name was John. This man came for a witness, to give testimony of the light, that all men might believe through him. He was not the light, but was to give testimony of the light. That was the true light, which enlighteneth every man that cometh into this world. He was in the world, and the world was made by him, and the world knew him not. He came unto his own, and his own received him not. But as many as received him, he gave them power to be made the sons of God, to them that believe in his name: who are born, not of blood, nor of the will of the flesh, nor of the will of man, but of God. (Here all kneel.) And the Word was made flesh, and dwelt among us: and we saw his glory, the glory as it were of the only-begotten of the Father, full of grace and truth."},
    {"w": "S", "la": "Deo grátias.", "en": "Thanks be to God."},
    {"if": "pope", "r": "He makes a fitting reverence to the Pope.", "ref": ["varia-iii-7"]},
    {"if": "bp", "r": "He makes a fitting reverence to the Bishop.", "ref": ["varia-iii-7"]},
    {"m": "ls", "if": "!sac", "r": "At the middle he folds the corporal, covers the chalice, bows to the cross, covers his head, and takes the chalice; below the lowest step he bows profoundly, and returns to the sacristy saying the Benedicite.", "ref": ["modus-xv-4"]},
    {"m": "ls", "if": "tab", "r": "At the middle he folds the corporal, covers the chalice, bows to the cross, covers his head, and takes the chalice; below the lowest step he genuflects, and returns to the sacristy saying the Benedicite.", "ref": ["modus-xv-4"]},
    {"m": "ls", "if": "exp", "r": "At the middle he folds the corporal, covers the chalice, and takes the chalice; below the lowest step he kneels on both knees, and returns to the sacristy saying the Benedicite.", "ref": ["modus-xv-4", "varia-ii-8"]},
    {"m": "l", "r": "In the sacristy the server, kneeling, asks pardon for any fault, helps the priest unvest, and says Benedictus Deus; the priest answers Pater, et Filius, et Spiritus Sanctus.", "ref": ["varia-vi-10", "varia-vi-11"]},
    {"m": "mc", "if": "!exp", "r": "Making the same reverence as at the entrance, all return to the sacristy in order.", "ref": ["ministri-xx-2"]},
    {"m": "mc", "if": "exp", "r": "Kneeling on both knees, all return to the sacristy in order.", "ref": ["varia-ii-8"]},
    {"m": "mc", "r": "The ministers unvest the priest, then one another; the acolytes cover the altar.", "ref": ["ministri-xx-2", "ministri-xx-3"]}
  ]},
  dismiss: {
    ite: [{"w": "P", "la": "Ite, missa est.", "en": "Go, the Mass is ended."}, {"w": "S", "la": "Deo grátias.", "en": "Thanks be to God."}],
    ben: [{"w": "P", "la": "Benedicámus Dómino.", "en": "Let us bless the Lord."}, {"w": "S", "la": "Deo grátias.", "en": "Thanks be to God."}],
    req: [{"w": "P", "la": "Requiéscant in pace.", "en": "May they rest in peace."}, {"w": "S", "la": "Amen.", "en": "Amen."}]
  }
};
