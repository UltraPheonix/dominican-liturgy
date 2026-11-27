"""Build data/ordo.js: the Order of Mass of the Missale O.P. (1939) with two sets of directions.
lines: the basic Order of Mass, with only the rubrics printed in the Ordo Missae of the Missal;
adv: the full directions of the Missal's Ritus servandus, step by step, for Low, Sung, Solemn and Conventual Mass, with the
circumstances chosen on the Mass page (a prelate, the Blessed Sacrament, the servers, the rank of the day).
The texts of the prayers (Latin and English) are in tools/rubrics/ordo_texts.json.
Usage: python3 tools/rubrics/ordo_directions.py"""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(H, '..', '..')
O = json.load(open(os.path.join(H, 'ordo_texts.json')))
# the basic mode: only the rubrics printed in the Ordo Missae of the Missal itself (Missale O.P. 1939, pp. 191-193 and the Canon,
# pp. 205-210), with the prayers; nothing from the Ritus servandus
def T(sec, prefix, **kw):
    for l in O[sec]['lines']:
        if 'la' in l and l['la'].startswith(prefix):
            d = dict(l); d.update(kw); return d
    raise KeyError((sec, prefix))
def R0(t, m=None, c=None):
    d = {}
    if m: d['m'] = m
    if c: d['if'] = c
    d['r'] = t; return d
NR = '!req'
BASIC = {
 'chalice': [T('chalice', 'Benedícite', **{'if': NR}), T('chalice', 'In nómine', **{'if': NR}), T('chalice', 'Amen', **{'if': NR})],
 'foot': [
  T('foot', 'Actiónes nostras'),
  R0('The priest, when he is about to celebrate, comes to the middle of the altar, makes a profound bow, and standing signs himself with the sign of the cross, saying in a clear and audible voice:'),
  T('foot', 'In nómine Patris'),
  R0('Then in the same voice:'),
  T('foot', 'Confitémini'), T('foot', 'Quóniam in sǽculum'),
  R0('Then, bowing profoundly, he says:'),
  T('foot', 'Confíteor Deo omnipoténti, et beátæ Maríæ semper Vírgini, et beáto Domínico patri nostro, et ómnibus Sanctis, et vobis'),
  T('foot', 'Misereátur tui'), T('foot', 'Amen.'),
  R0('Then the server repeats the Confession, and where the priest said vobis, fratres and vos, he says tibi, pater and te.', 'l'),   # one server at Low Mass (qc_ui W15)
  R0('Then the ministers repeat the Confession, and where the priest said vobis, fratres and vos, they say tibi, pater and te.', 'smc'),
  T('foot', 'Confíteor Deo omnipoténti, et beátæ Maríæ semper Vírgini, et beáto Domínico patri nostro, et ómnibus Sanctis, et tibi'),
  R0('This said, the priest says:'),
  T('foot', 'Misereátur vestri'), dict(O['foot']['lines'][12]),
  T('foot', 'Absolutiónem'), dict(O['foot']['lines'][15]),
  R0('The Confession and absolution made, the priest stands erect and says:'),
  T('foot', 'Adiutórium'), T('foot', 'Qui fecit'),
  R0('And going up to the altar, bowing profoundly again, he says the prayer:'),
  T('foot', 'Aufer a nobis'),
  R0('This prayer said, he kisses the altar, first signing it in the middle with his right thumb; and standing erect he signs himself, and going to the book with hands joined before his breast, begins the Office, or Introit, of the Mass.')],
 'rKy': [R0('The Introit finished, he says alternately with the server:', 'l'), R0('The Introit finished, he says alternately with the ministers:', 'smc')],
 'rGl': [R0('Then, going to the middle of the altar, he says the Gloria (if it is to be said), bowing his head at Deo, at Adoramus te, at Gratias agimus tibi, at Jesu Christe, at suscipe deprecationem nostram, and again at Jesu Christe.')],
 'collect': [T('collect', 'Dóminus vobíscum'), T('collect', 'Et cum spíritu'), T('collect', 'Orémus')],
 'collectEnd': [],
 'gospel': [
  R0('Then, having said the Collect, the Epistle and the Responsory with the Alleluia or Tract, he goes to the Gospel corner, bowing his head at the middle of the altar, and says:', None, NR),
  R0('Then, having said the Collect, the Epistle and the Responsory with the Tract, he goes to the Gospel corner, bowing his head at the middle of the altar.', None, 'req'),
  T('gospel', 'Dóminus sit in corde meo', **{'if': NR}),
  T('gospel', 'Iube, domne'), T('gospel', 'Dóminus sit in corde tuo'),
  R0('And standing before the book, with his hands joined upon it, he says:'),
  T('gospel', 'Dóminus vobíscum'), T('gospel', 'Et cum spíritu'),
  R0('And saying Sequentia (or Initium) sancti Evangelii, he signs the Gospel with his right thumb, and himself on the forehead, mouth and breast; then with his right hand he signs himself with a larger sign of the cross, from forehead to breast and shoulders. The server answers Gloria tibi Domine:', 'l'),
  R0('And saying Sequentia (or Initium) sancti Evangelii, he signs the Gospel with his right thumb, and himself on the forehead, mouth and breast; then with his right hand he signs himself with a larger sign of the cross, from forehead to breast and shoulders. The ministers answer Gloria tibi Domine:', 'smc'),
  T('gospel', 'Sequéntia sancti'), T('gospel', 'Glória tibi'),
  R0('Then he continues the Gospel with hands joined, as before.')],
 'afterGospel': [
  R0('When it is finished, he signs himself again with the larger sign of the cross; and at once signing the Gospel with the cross with his thumb, he kisses it, saying:', None, NR),
  T('afterGospel', 'Per evangélica', **{'if': NR})],
 'rCr': [R0('Then at the middle of the altar, extending, raising and joining his hands, he says (if it is to be said) Credo in unum Deum, and going to the book continues it with hands joined. At Deum he bows his head to the cross, and does the same at Jesum Christum and at simul adoratur; at Et incarnatus est he kneels on both knees; at the end, at Et vitam venturi saeculi, he signs himself with the sign of the cross from forehead to breast and shoulders.')],
 'offerDial': [
  R0('Then, turned to the people, he says:'),
  T('offerDial', 'Dóminus vobíscum'), T('offerDial', 'Et cum spíritu'),
  R0('Then he says Oremus, and the Offertory.'),
  T('offerDial', 'Orémus')],
 'offertory': [
  R0('The Offertory said, raising and joining his hands, he says Quid retribuam; and taking the chalice, with the host laid on the paten, in both hands and raising it above the corporal before his breast, he says Calicem salutaris:', None, NR),
  T('offertory', 'Quid retríbuam', **{'if': NR}),
  R0('Then, offering, he says:'),
  T('offertory', 'Súscipe, sancta'),
  R0('This said, setting the chalice down on the corporal, he lifts the paten from the chalice, lays the host before its foot, and covers the chalice with the pall. Then, going to the Epistle corner for the washing of the fingers, he says (and no further):'),
  T('offertory', 'Lavábo'),
  R0('After the washing of the fingers, the priest, coming to the middle of the altar with hands joined before his breast, bows profoundly, saying:'),
  T('offertory', 'In spíritu'),
  R0('This said, standing erect and turning to the people, extending and joining his hands, he says in a moderate voice Orate fratres, these two words only, continuing the rest secretly:'),
  T('offertory', 'Oráte, fratres'),
  R0('With hands joined he adds:'),
  T('offertory', 'Dómine, exáudi'),
  R0('and Oremus. Then, with hands extended, he says the Secret prayer or prayers; when they are finished, at the conclusion, he says in a clear and audible voice Per omnia saecula saeculorum, with the Preface proper to the Mass.')],
 'canon': [l for l in O['canon']['lines'] if 'la' in l],
 'pater': [l for l in O['pater']['lines'] if 'la' in l],
 'agLow': [dict(O['agLow']['lines'][0], **{'if': NR}),
           {'if': 'req', 'w': 'P', 'la': 'Agnus Dei, qui tollis peccáta mundi: dona eis réquiem. Agnus Dei, qui tollis peccáta mundi: dona eis réquiem. Agnus Dei, qui tollis peccáta mundi: dona eis réquiem sempitérnam.', 'en': 'Lamb of God, who takest away the sins of the world, grant them rest. Lamb of God, who takest away the sins of the world, grant them rest. Lamb of God, who takest away the sins of the world, grant them rest eternal.'}],
 'communion': [T('communion', 'Hæc sacrosáncta'), T('communion', 'Pax tibi', **{'if': NR}), T('communion', 'Dómine Iesu Christe'), T('communion', 'Corpus et Sanguis'),
   R0('Communion of the faithful.'), T('communion', 'Ecce Agnus Dei'), T('communion', 'Dómine, non sum dignus'), T('communion', 'Corpus Dómini nostri'),
   T('communion', 'Quod ore')],
 'post': [l for l in O['post']['lines'] if 'la' in l],
 'postEnd': [l for l in O['postEnd']['lines'] if 'la' in l],
 'end': [T('end', 'Pláceat'), T('end', 'Benedíctio Dei', **{'if': NR}), dict(O['end']['lines'][4], **{'if': NR})] + [l for l in O['end']['lines'][5:] if 'la' in l],
 'offertoryEnd': [l for l in O['offertoryEnd']['lines'] if 'la' in l],
}
CV = O['commConv']['lines']
def cvx(prefix):
    return dict([l for l in CV if 'la' in l and l['la'].startswith(prefix)][0])
BASIC['commConv'] = [
  R0('The Communion of the friars. Those who are to communicate come in choir order towards the sanctuary, bow profoundly and kneel.'),
  R0('The deacon brings the pyx, the candle-bearers going before, and sets it on the corporal; all prostrate in adoration while he brings it, the celebrant genuflecting.', None, '!sac'),
  R0('The deacon takes the pyx from the tabernacle and sets it on the corporal.', None, 'tab'),
  R0('The ministers prostrate, the others stretched out in the venia, all say together:'),
  cvx('Confíteor'),
  R0('The priest, stepping aside from the middle so as not to turn his back to the Sacrament, says:'),
  cvx('Misereátur'), dict(CV[4]), cvx('Absolutiónem'), dict(CV[6]),
  R0('All rise on their knees. The ministers communicate first, by rank, then the other friars, in their cappas, two by two; the deacon and subdeacon hold the communion cloth.'),
  R0('Making the sign of the cross with the Host before each, the priest says:'),
  cvx('Corpus Dómini'),
  R0('They withdraw sideways, so as not to turn their backs to the Sacrament; the friars return to their stalls and give thanks in silence. Those who do not communicate lie prostrate meanwhile.'),
  R0('The priest sets the pyx on the corporal and continues the Mass; the hosts that remain are reserved.')]
for k in ('kyLow', 'glLow', 'crLow', 'saLow', 'commSimple'):
    BASIC[k] = [dict(l) for l in O[k]['lines']]
for k in BASIC:
    for l in BASIC[k]:
        if 'm' in l and 'm' in l['m'] and 'c' not in l['m']: l['m'] += 'c'
# ---------------------------------------------------------------------------------------------------------------------
# The full directions: the Ritus servandus of the Missale O.P. (1939), step by step, one action to a line.
# r(text, forms, refs, condition); forms: l Low, s Sung, m Solemn, c Conventual (None = all); refs: paragraphs of rubrics.html
LS, MC, NR = 'ls', 'mc', '!req'
def r(t, m=None, ref=None, c=None):
    d = {}
    if m: d['m'] = m
    if c: d['if'] = c
    d['r'] = t
    if ref: d['ref'] = ref if isinstance(ref, list) else [ref]
    return d
def t(w, la, en, m=None, c=None):
    d = {}
    if m: d['m'] = m
    if c: d['if'] = c
    d.update({'w': w, 'la': la, 'en': en}); return d
def X(sec, prefix, m=None, c=None, nth=0):
    hits = [l for l in O[sec]['lines'] if 'la' in l and l['la'].startswith(prefix)]
    d = dict(hits[nth]); d.pop('m', None)
    if m: d['m'] = m
    if c: d['if'] = c
    return d
def gx(where, m=None):
    return r('The Sacrament is exposed: he genuflects as he %s.' % where, m, 'varia-ii-4', 'exp')
# turning to the people at the Dominus vobiscum (and Orate fratres, the blessing): the altar without the Sacrament, the tabernacle, exposition
def turn_out(lead=''):
    return [r(lead + 'Without kissing the altar, he turns to the people by his left, hands raised and extended:', None, 'modus-iii-1', '!sac'),
            r(lead + 'He goes to the middle, bows his head, steps a little towards the Gospel side, and turns to the people by his right, so as not to turn his back to the tabernacle:', None, 'varia-ii-9', 'tab'),
            r(lead + 'He genuflects at the middle, steps towards the Gospel corner, and turns to the people there, his back to the corner of the altar:', None, 'varia-ii-5', 'exp')]
def turn_back(after):
    return [r('He turns back by the same way and, ' + after, None, 'modus-iii-2', '!sac'),
            r('He turns back by the same way, bowing again before the tabernacle, and, ' + after, None, 'varia-ii-9', 'tab'),
            r('He returns the same way, genuflecting at the middle, and, ' + after, None, 'varia-ii-5', 'exp')]
A = {}
A['chalice'] = [
  r('Coming to the altar, he bows profoundly at the middle, goes up, and sets the chalice towards the Gospel side.', 'l', 'praeparatio-ii-8', '!sac'),
  r('Coming to the altar, he genuflects at the middle (the Sacrament is in the tabernacle), goes up, and sets the chalice towards the Gospel side.', 'l', 'praeparatio-ii-8', 'tab'),
  r('Coming to the altar, he kneels on both knees before the Sacrament exposed, then goes up and sets the chalice towards the Gospel side.', 'l', ['praeparatio-ii-8', 'varia-ii-3'], 'exp'),
  r('He spreads the corporal in the middle, lays the paten with the host on it, and the purificator at its right.', 'l', 'praeparatio-ii-8'),
  r('He pours a little wine into the chalice. Holding out the water, the server says:', 'l', 'praeparatio-ii-9', NR),
  r('He pours a little wine into the chalice, and adds a very little water.', 'l', 'praeparatio-ii-9', 'req'),
  r('The chalice is prepared while the Gradual is sung. Holding out the water, the server says:', 's', None, NR),
  r('After reading the Gospel at his seat, the priest sits again. The subdeacon, wearing the veil, brings the chalice and prepares it before him.', MC, 'ministri-vi-4'),
  r('He hands the paten with the host to the deacon, who shows it to the priest, and pours in as much wine as the priest indicates.', MC, 'ministri-vi-4'),
  r('Holding out the water, the subdeacon says:', MC, 'ministri-vi-4', NR),
  X('chalice', 'Benedícite', c=NR),
  t('D', 'Dóminus.', 'The Lord.', MC, NR),
  r('The priest blesses the water:', None, 'praeparatio-ii-9', NR),
  X('chalice', 'In nómine', c=NR), X('chalice', 'Amen', c=NR),
  r('He adds so little water that it can very easily be changed into wine, and wipes the chalice.', 'l', 'praeparatio-ii-9', NR),
  r('He sets the paten with the host on the chalice, covers it with the pall and veil, and places it on the corporal.', 'l', 'praeparatio-ii-9'),
  r('He opens the Missal at the Epistle corner and finds the Mass.', 'l', 'praeparatio-ii-9'),
  r('The subdeacon adds a little water, takes back the paten, carries the chalice to the middle of the altar, covers it, and returns to his seat.', MC, 'ministri-vi-4')]
A['foot'] = [
  r('He returns to the middle of the altar, uncovers his head, and says secretly:', 'l', 'praeparatio-ii-10'),
  r('When the choir begins the Gloria Patri of the Introit, the ministers go to the altar: the acolytes with their candles, the subdeacon with the Gospel book, the deacon with the Missal, and last the priest.', MC, 'ministri-iii-1', '!chin,!req'),
  r('When the choir begins the Gloria Patri of the Introit, the ministers go to the altar: the acolytes with their candles, the subdeacon carrying the prepared chalice, the deacon with the Missal, and last the priest.', MC, 'ministri-iii-1', 'chin,!req'),
  # Requiem: no Gloria Patri (Ritus, De his quae omittuntur in Missa pro Defunctis), so the verse Te decet (Ministri III.3: "vel Versu, si Gloria Patri non dicitur") (qc_ui W3)
  r('When the choir begins the verse Te decet of the Introit (there is no Gloria Patri), the ministers go to the altar: the acolytes with their candles, the subdeacon with the Gospel book, the deacon with the Missal, and last the priest.', MC, 'ministri-iii-1', '!chin,req'),
  r('When the choir begins the verse Te decet of the Introit (there is no Gloria Patri), the ministers go to the altar: the acolytes with their candles, the subdeacon carrying the prepared chalice, the deacon with the Missal, and last the priest.', MC, 'ministri-iii-1', 'chin,req'),
  r('Below the lowest step they stand in line, the deacon at the priest’s right, the subdeacon at his left, an acolyte at each end. All bow profoundly and uncover their heads.', MC, 'ministri-iii-2', '!sac'),
  r('Below the lowest step they stand in line, the deacon at the priest’s right, the subdeacon at his left, an acolyte at each end. All genuflect and uncover their heads.', MC, ['ministri-iii-2', 'praeparatio-ii-8'], 'tab'),
  r('Below the lowest step they stand in line, the deacon at the priest’s right, the subdeacon at his left, an acolyte at each end. All kneel on both knees and uncover their heads.', MC, ['ministri-iii-2', 'varia-ii-3'], 'exp'),
  r('Rising, the priest says secretly:', MC, 'ministri-iii-2'),
  r('Before beginning, the priest says secretly:', 's'),
  X('foot', 'Actiónes nostras'),
  r('The Sacrament is exposed: whenever the priest comes to the middle of the altar, leaves it or passes it, he genuflects (the server or ministers with him); no one ever turns his back to the Sacrament.', None, ['varia-ii-4', 'varia-ii-6'], 'exp'),
  r('The Sacrament is exposed: the server genuflects whenever he passes the middle.', 'l', 'varia-vi-6', 'exp'),
  r('The Sacrament is exposed: the deacon kisses neither the priest’s hand nor his shoulder when he hands him anything.', MC, 'varia-ii-6', 'exp'),
  r('The Pope is present: the priest first kneels below the lowest step on the Gospel side, facing the Pope, and waits for his blessing; then he rises and, turned partly towards the altar, begins.', None, 'varia-iii-1', 'pope'),
  r('The Bishop is present: the priest first stands below the lowest step on the Gospel side; at the Bishop’s sign he bows profoundly to him, then turns to the altar and begins.', None, 'varia-iii-1', 'bp'),
  r('Standing just below the top step, he bows profoundly and signs himself, saying aloud:', LS, 'modus-i-1'),
  r('He signs himself, saying aloud:', MC, 'ministri-iii-2'),
  X('foot', 'In nómine Patris'), X('foot', 'Confitémini'), X('foot', 'Quóniam in sǽculum'),
  r('Bowing profoundly, with hands joined, he says in a moderate voice (he does not strike his breast):', None, 'modus-i-2'),
  r('The ministers bow with him, without bending the knee; the acolytes stand upright, facing each other.', MC, 'ministri-iii-2'),
  r('He makes the Confession with the Pope, standing at his left, and says tibi, Pater and te, Pater instead of vobis, fratres and vos, fratres.', MC, 'varia-iii-2', 'pope'),
  r('He makes the Confession with the Bishop, standing at his left, and says tibi, Pater and te, Pater instead of vobis, fratres and vos, fratres.', MC, 'varia-iii-2', 'bp'),
  X('foot', 'Confíteor Deo omnipoténti, et beátæ Maríæ semper Vírgini, et beáto Domínico patri nostro, et ómnibus Sanctis, et vobis'),
  r('The server, kneeling at his left, answers:', 'l', 'varia-vi-4'),
  X('foot', 'Misereátur tui'), X('foot', 'Amen.'),
  r('Then the Confiteor is said to the priest, with tibi, pater and te, pater:', None, 'modus-i-2'),
  X('foot', 'Confíteor Deo omnipoténti, et beátæ Maríæ semper Vírgini, et beáto Domínico patri nostro, et ómnibus Sanctis, et tibi'),
  X('foot', 'Misereátur vestri'), dict(O['foot']['lines'][12]),
  r('Without making the sign of the cross:', None, 'modus-i-3'),
  X('foot', 'Absolutiónem'), dict(O['foot']['lines'][15]),
  r('Standing erect, with hands joined:', None, 'modus-i-3'),
  X('foot', 'Adiutórium'), X('foot', 'Qui fecit'),
  r('He genuflects to the Pope.', MC, 'varia-iii-3', 'pope'),
  r('He bows profoundly to the Bishop.', MC, 'varia-iii-3', 'bp'),
  r('He goes up to the altar and, bowing profoundly towards its middle, says secretly:', None, ['modus-i-4', 'ministri-iii-3']),
  X('foot', 'Aufer a nobis'),
  r('At Per Christum he makes a cross on the altar with his thumb and kisses it, his hands laid on the altar.', None, 'modus-i-4'),
  r('Standing, he signs himself, saying secretly In nomine Patris, et Filii, et Spiritus Sancti. Amen, and goes with hands joined to the Missal at the Epistle corner.', None, 'modus-i-4'),
  r('Meanwhile the deacon places the Missal at the Epistle corner and the subdeacon the Gospel book at the Gospel corner; the acolytes set their candles down on the steps and put them out.', MC, 'ministri-iii-3')]
A['rAs'] = [
  r('On Sundays, when the Hour before Mass is finished, the priest (in alb, stole and maniple, or in a cope if there is to be a procession) comes to the sanctuary with the ministers and acolytes; all bow profoundly before the altar.', MC, 'ministri-ii-1'),
  r('As the cantors begin Asperges me, the priest sprinkles the altar, then the deacon, subdeacon and acolytes.', MC, 'ministri-ii-2'),
  r('The Master of the Order is present: he is sprinkled next.', 'c', 'ministri-ii-2', 'mo'),
  r('Then the cantors, and the brethren, beginning with the right choir; then the lay brothers, and the seculars in choir.', 'c', 'ministri-ii-2', 'dup'),
  r('Then the brethren, beginning with the right choir; then the lay brothers, and the seculars in choir.', 'c', 'ministri-ii-2', '!dup'),
  r('Then the people.', 'm', 'ministri-ii-2'),
  r('When the antiphon is finished, standing before the steps, the priest says the versicles and the prayer; then all return to the sacristy.', MC, 'ministri-ii-3')]
A['rIn'] = [
  r('At the Epistle corner he reads the Introit aloud, bowing towards the cross at Gloria Patri, and repeats the antiphon.', LS, 'modus-ii-1', NR),
  r('At the Epistle corner he reads the Introit aloud and repeats the antiphon.', LS, ['modus-ii-1', 'varia-iv-1'], 'req'),
  r('The ministers stand at the priest’s right in order, and say the Introit and the Kyrie with him; the deacon turns the pages.', MC, 'ministri-iii-4'),
  r('Then the deacon stands behind the priest and the subdeacon behind the deacon; the acolytes stand below the steps.', MC, 'ministri-iii-5')]
A['rKy'] = [
  r('He says the Kyrie alternately with the server.', 'l', 'modus-ii-1'),
  r('They may sit at the Epistle side, the deacon at the priest’s left and the subdeacon at the deacon’s left; an acolyte spreads a cloth over their knees.', MC, 'ministri-iii-6', 'sd'),
  r('At the last Kyrie an acolyte takes up the cloth, beginning with the priest and kissing his hand.', MC, 'ministri-iii-6', 'sd'),
  r('During the Kyrie the subdeacon, wearing the veil, brings the chalice from the sacristy and sets it on the Epistle corner.', MC, 'ministri-iv-2', 'chky')]
A['rGl'] = [
  gx('comes to the middle, and again as he leaves it', LS),
  r('He goes to the middle. At Gloria he lays his hands on the altar; at in excelsis he raises them; at Deo he joins them and bows.', 'l', 'modus-ii-2'),
  r('He continues at the Epistle corner with hands joined, bowing at Adoramus te, Gratias agimus tibi, Jesu Christe and Suscipe deprecationem nostram.', 'l', 'modus-ii-2'),
  r('He intones the Gloria at the middle of the altar, with the same gestures, and continues it at the Epistle corner, bowing at the same words.', 's', ['modus-ii-2', 'ministri-iv-1']),
  r('All rise and bow before the middle; the priest goes up and intones the Gloria. They continue it with him at the Epistle corner, standing at his right.', MC, 'ministri-iv-1'),
  r('When they have said it, the priest and deacon stand until the choir has finished.', MC, 'ministri-iv-1'),
  r('Meanwhile the subdeacon goes with an acolyte to the sacristy and brings the chalice, wearing the veil; he sets it on the Epistle corner.', MC, 'ministri-iv-2', 'chgl')]
A['collect'] = turn_out() + [
  r('The deacon lifts the hem of the chasuble and goes with him.', MC, 'ministri-v-1'),
  X('collect', 'Dóminus vobíscum'), X('collect', 'Et cum spíritu')] + turn_back('at the book, bowing towards the cross, says:') + [
  X('collect', 'Orémus'),
  r('He kneels for Flectamus genua, laying the front of the chasuble on the altar; the server answers Levate, and he rises.', LS, 'modus-iii-3', 'flect'),
  r('The deacon, kneeling with the lower ministers, sings Flectamus genua, and rising sings Levate; the priest does not kneel.', MC, ['ministri-v-2', 'varia-i-2'], 'flect'),
  r('He reads the Collect with hands extended, joining them and bowing at Per Dominum nostrum.', None, 'modus-iii-2')]
A['collectEnd'] = [
  r('With his hands on the book or on the altar he reads the Epistle; then, with hands joined, the Gradual and what follows.', 'l', 'modus-iv-1'),
  r('The server kneels on the Gospel side until the end of the Alleluia or Tract.', 'l', ['varia-vi-4', 'varia-vi-5']),
  r('The Epistle is read and the Gradual sung.', 's'),
  r('After the last prayer the priest and deacon go down to the lowest step; all bow and go to sit.', MC, 'ministri-v-2'),
  r('The subdeacon, an acolyte going before, sings the Epistle at the lectern before the steps, facing the altar.', MC, 'ministri-vi-1'),
  r('Seated, the priest reads the Epistle, and the Gradual and Alleluia verse by verse with the deacon; then he stands and reads the Gospel at his seat.', MC, ['ministri-vi-2', 'ministri-vi-3']),
  r('Meanwhile the deacon spreads the corporal on the altar.', MC, 'ministri-vi-3')]
A['rGr'] = [
  r('He genuflects at the verse Adjuva nos, Deus salutaris noster.', LS, 'varia-i-1', 'adjuva'),
  r('All genuflect at the verse Adjuva nos, Deus salutaris noster.', MC, ['varia-i-1', 'varia-i-2'], 'adjuva'),
  r('He genuflects while he says the verse Veni Sancte Spiritus, as far as reple.', LS, 'varia-i-1', 'veni'),
  r('At the verse Veni Sancte Spiritus the priest and ministers stand, bowing profoundly, as far as reple; they sit again when the choir rises.', MC, ['ministri-vii-1', 'varia-i-2'], 'veni'),
  r('Towards the end of the chant the acolytes light their candles, and the thurifer comes.', MC, 'ministri-vii-2', 'full,thur'),
  r('Towards the end of the chant the acolytes light their candles.', MC, 'ministri-vii-2', '!thur'),
  r('The acolytes go with the thurifer to the sacristy and bring back the processional cross.', MC, 'ministri-vii-3', 'full,td'),
  r('The thurifer offers incense to the priest, saying Benedicite; the priest blesses it, saying In nomine Patris, et Filii, et Spiritus Sancti.', MC, 'ministri-vii-3', 'full,thur')]
A['gospel'] = [
  r('The server carries the Missal to the Gospel corner. The priest follows, bowing to the cross as he passes the middle, and says secretly:', LS, ['modus-iv-2', 'varia-vi-4'], '!req,!exp'),
  r('The server carries the Missal to the Gospel corner. The priest follows, genuflecting as he passes the middle, and says secretly:', LS, ['modus-iv-2', 'varia-ii-4'], '!req,exp'),
  r('The server carries the Missal to the Gospel corner, and the priest follows, bowing to the cross as he passes the middle.', LS, 'modus-iv-2', 'req'),
  X('gospel', 'Dóminus sit in corde meo', LS, NR),
  r('The deacon takes the Gospel book and, bowing to the priest, says:', MC, 'ministri-viii-1'),
  X('gospel', 'Iube, domne', MC),
  r('The priest stands and answers:', MC, 'ministri-viii-1'),
  X('gospel', 'Dóminus sit in corde tuo', MC),
  t('P', 'In nómine Patris, et Fílii, et Spíritus Sancti.', 'In the name of the Father, and of the Son, and of the Holy Ghost.', MC),
  t('D', 'Amen.', 'Amen.', MC),
  r('They go to the lectern at the Gospel side: the thurifer, the acolytes with the cross between them, the subdeacon with the cushion, and the deacon carrying the book.', MC, ['ministri-viii-1', 'ministri-viii-2'], 'full,td'),
  r('They go to the lectern at the Gospel side: the thurifer, the acolytes, the subdeacon with the cushion, and the deacon carrying the book.', MC, ['ministri-viii-1', 'ministri-viii-2'], 'full,thur,!td'),
  r('They go to the lectern at the Gospel side: the acolytes, the subdeacon with the cushion, and the deacon carrying the book.', MC, ['ministri-viii-1', 'ministri-viii-2'], '!full'),
  r('They go to the lectern at the Gospel side: the acolytes, the subdeacon with the cushion, and the deacon carrying the book.', MC, ['ministri-viii-1', 'ministri-viii-2'], 'full,!thur'),
  r('With his hands joined on the book:', LS, 'modus-v-1'),
  X('gospel', 'Dóminus vobíscum', LS), X('gospel', 'Et cum spíritu', LS),
  t('D', 'Dóminus vobíscum.', 'The Lord be with you.', MC), t('S', 'Et cum spíritu tuo.', 'And with thy spirit.', MC),
  r('At Sequentia he signs the book with his thumb, then his forehead, lips and breast:', LS, 'modus-v-1'),
  r('At Sequentia the deacon signs the book and himself; the priest and subdeacon sign themselves, facing the altar:', MC, 'ministri-viii-3'),
  X('gospel', 'Sequéntia sancti', LS),
  t('D', 'Sequéntia sancti Evangélii secúndum N.', 'The continuation of the holy Gospel according to N.', MC),
  X('gospel', 'Glória tibi'),
  r('The deacon incenses the book three times.', MC, 'ministri-viii-3', 'full,thur'),
  r('He reads the Gospel with hands joined on the book, bowing at the names of Jesus and Mary.', LS, 'modus-v-2'),
  r('The deacon sings the Gospel with hands joined. The priest stands at the Epistle corner facing it; all the brethren turn towards it.', MC, ['ministri-viii-3', 'ministri-viii-4'])]
A['afterGospel'] = [
  r('At the end he signs himself, then kisses the Gospel, saying:', LS, 'modus-v-3', '!prel,!req'),
  r('The ministers return to the altar. The subdeacon brings the book to the priest, the deacon pointing to the Gospel; the priest kisses it, saying:', MC, ['ministri-viii-5', 'ministri-ix-1'], '!prel,!req'),
  r('The ministers return to the altar.', MC, 'ministri-viii-5', 'prel'),
  r('The Gospel book is taken to the Pope to kiss.', None, 'varia-iii-4', 'pope,!req'),
  r('The Gospel book is taken to the Bishop to kiss.', None, 'varia-iii-4', 'bp,!req'),
  X('afterGospel', 'Per evangélica', c='!prel,!req'),
  t('D', 'Amen.', 'Amen.', MC, '!prel,!req'),
  r('The deacon kisses the book after him.', MC, 'ministri-ix-1', '!prel,!req'),
  r('The sermon may follow.', LS, None, 'sun')]
A['rCr'] = [
  gx('comes to the middle for the Credo, and as he goes to and from the book', LS),
  r('At the middle, his hands laid on the altar, he says Credo; at in unum he raises them, at Deum he joins them and bows.', 'l', 'modus-vi-1'),
  r('He continues at the Gospel corner, bowing at Jesum Christum. At Et incarnatus est he comes to the middle and kneels, rising after Homo factus est.', 'l', ['modus-vi-1', 'modus-vi-2']),
  r('He bows at simul adoratur and signs himself at Et vitam venturi saeculi.', 'l', 'modus-vi-2'),
  r('He intones the Credo at the middle of the altar, with the same gestures, and continues it at the Gospel corner; at Et incarnatus est he kneels at the middle.', 's', ['modus-vi-1', 'modus-vi-2']),
  r('The priest intones the Credo at the middle; the ministers stand at his left, one behind the other, and continue it with him in a low voice.', MC, 'ministri-ix-2'),
  r('At Et incarnatus est, as the choir sings it, the priest kneels at the middle, the deacon and subdeacon on the step behind him, the acolytes lower down.', MC, 'ministri-ix-2'),
  r('All bow at simul adoratur.', MC, 'ministri-ix-3'),
  r('Then the acolytes and thurifer take the cross back to the sacristy.', MC, 'ministri-ix-3', 'full,td')]
A['offerDial'] = [r(x['r'].replace('he turns', 'at the middle he turns').replace('Without kissing the altar, at the middle', 'At the middle, without kissing the altar,'), x.get('m'), x.get('ref'), x.get('if')) for x in turn_out()] + [
  X('offerDial', 'Dóminus vobíscum'), X('offerDial', 'Et cum spíritu')] + turn_back('bowing to the cross, says:') + [
  X('offerDial', 'Orémus'),
  r('At the book he reads the Offertory.', LS, 'modus-vii-2'),
  r('At the book he says the Offertory with the ministers.', MC, 'ministri-x-1')]
A['offertory'] = [
  r('At the middle he uncovers the chalice and sets the veil aside; laying his hands on the altar, he says:', LS, 'modus-vii-2', NR),
  r('At the middle he uncovers the chalice and sets the veil aside.', LS, 'modus-vii-2', 'req'),
  X('offertory', 'Quid retríbuam', LS, NR),
  r('At the middle the priest says:', MC, 'ministri-x-1', NR),
  t('P', 'Quid retríbuam Dómino pro ómnibus quæ retríbuit mihi?', 'What shall I render to the Lord for all the things that he hath rendered unto me?', MC, NR),
  r('The subdeacon uncovers the chalice; the deacon hands it to the priest, holding it by the foot and kissing his hand, and says:', MC, 'ministri-x-1', NR),
  t('D', 'Immola Deo sacrifícium laudis, et redde Altíssimo vota tua.', 'Offer to God the sacrifice of praise, and pay thy vows to the Most High.', MC, NR),
  r('Taking it, the priest says:', MC, 'ministri-x-1', NR),
  t('P', 'Cálicem salutáris accípiam, et nomen Dómini invocábo.', 'I will take the chalice of salvation, and I will call upon the name of the Lord.', MC, NR),
  r('The subdeacon uncovers the chalice and the deacon hands it to the priest.', MC, 'ministri-x-1', 'req'),
  r('Raising the chalice, with the paten and host on it, to the height of his breast, he offers them:', None, 'modus-vii-3'),
  X('offertory', 'Súscipe, sancta'),
  r('He sets the chalice down, slides the host onto the corporal before it, puts the paten partly under the corporal, and covers the chalice with the pall.', None, 'modus-vii-3'),
  r('The deacon presents incense; the priest blesses it and takes the thurible from him.', MC, 'ministri-xi-1', 'full,thur'),
  r('He incenses the chalice (a sign of the cross and three swings), then the tabernacle or the cross, then the top of the altar on either side, then its front.', MC, ['ministri-xi-1', 'ministri-xi-2'], 'full,thur,!exp'),
  r('He incenses the chalice; then, kneeling on both knees on the top step with the ministers, he incenses the Sacrament, bowing profoundly before and after; then, standing, the altar, genuflecting as he passes the middle.', MC, ['varia-ii-6', 'ministri-xi-2'], 'full,thur,exp'),
  r('Standing at the Epistle corner, the priest is incensed by the deacon.', MC, 'ministri-xi-4', 'full,thur,!exp'),
  r('He goes down to the Epistle corner below the top step and, facing the people, is incensed by the deacon.', MC, 'varia-ii-6', 'full,thur,exp'),
  gx('leaves the middle for the washing of the hands, and again on his return', LS),
  r('At the Epistle corner he washes his fingers, saying:', LS, ['modus-vii-4', 'varia-vi-6']),
  r('At the Epistle corner the subdeacon pours the water and the deacon hands the towel; the priest says:', MC, 'ministri-xii-1'),
  X('offertory', 'Lavábo'),
  r('He returns to the middle and, bowing profoundly, says:', None, 'modus-vii-4'),
  X('offertory', 'In spíritu'),
  r('Without kissing the altar he turns to the people, says Orate fratres aloud and the rest secretly, and turns back completing the circle:', None, 'modus-vii-5', '!sac'),
  r('He steps towards the Gospel side and turns to the people by his right, so as not to turn his back to the tabernacle; he says Orate fratres aloud and the rest secretly, and returns the same way:', None, 'varia-ii-10', 'tab'),
  r('He genuflects, steps towards the Gospel corner and turns to the people; he says Orate fratres aloud and the rest secretly, and returns the same way, genuflecting:', None, 'varia-ii-7', 'exp'),
  X('offertory', 'Oráte, fratres'),
  r('Facing the altar, with hands joined:', None, 'modus-vii-5'),
  X('offertory', 'Dómine, exáudi'),
  r('Then Oremus, and the Secret in a low voice.', None, 'modus-vii-5')]
A['rPf'] = [
  r('His hands lie on the altar for Per omnia saecula saeculorum and Dominus vobiscum; at Sursum corda he raises them; at Gratias agamus he joins them and bows; he opens them for the Preface and joins them at supplici confessione dicentes.', None, ['modus-viii-1', 'modus-viii-2']),
  r('After Gratias agamus the thurifer incenses the deacon, the subdeacon and the acolytes, who stand facing one another at the two corners.', MC, 'ministri-xiii-1', 'full,thur'),
  r('The Master of the Order is present: the thurifer then incenses him.', 'c', 'ministri-xiii-2', 'mo,full,thur'),
  r('Then the thurifer incenses the brethren in both choirs, seniors first, and the lay brothers, and returns to stand behind the subdeacon.', 'c', 'ministri-xiii-2', 'full,thur')]
A['rSa'] = [
  r('With hands joined he says the Sanctus, signing himself at Benedictus qui venit. The server rings the bell a few times and lights the elevation candle.', LS, ['modus-viii-2', 'varia-vi-7']),
  r('At supplici confessione the deacon goes to the Gospel corner and the subdeacon to the Epistle corner, each with an acolyte; facing one another they say the Sanctus with the priest, signing themselves at Benedictus. An acolyte rings the bell.', MC, 'ministri-xiv-1'),
  r('The subdeacon takes the veil, receives the paten from the deacon, and holds it raised behind the deacon until after the Pater noster; the acolytes light the elevation candles.', MC, 'ministri-xiv-2', 'thur'),
  r('The choir does not draw out the Sanctus, and the priest goes slowly enough that the elevation never comes before it ends.', 'smc', 'ministri-xv-2'),
  r('With only one acolyte, he stands at the deacon’s right during the Sanctus and the consecration.', MC, 'ministri-xx-4', 'one')]
C = 'canon'
A['canon'] = [
  r('Bowing profoundly, with hands joined, he begins secretly. At uti he stands erect; at benedicas he makes three crosses over the offerings; at In primis he joins his hands.', None, 'modus-ix-1'),
  X(C, 'Te ígitur'),
  r('At Papa he names the Pope; at Antistite the Bishop of the diocese.', None, 'modus-ix-1'),
  r('With hands joined; after tuarum he pauses to remember in silence those he wishes to commend to God:', None, 'modus-ix-2'),
  X(C, 'Meménto, Dómine'),
  r('With hands extended; he bows at the names of Mary and Jesus:', None, 'modus-ix-3'),
  X(C, 'Communicántes'),
  r('With hands extended as for the prayers (not over the offerings):', None, 'modus-ix-3'),
  X(C, 'Hanc ígitur'),
  r('He makes three crosses over the offerings, then one over the Host and one over the chalice; he bows at Jesu Christi:', None, 'modus-ix-4'),
  X(C, 'Quam oblatiónem'),
  r('He wipes his fingers on the corporal and takes the Host; he raises his eyes at elevatis oculis and blesses the Host at benedixit. Bending a little, he says the words of consecration secretly and without pause:', None, ['modus-x-1', 'modus-x-2']),
  X(C, 'Qui prídie'),
  r('He kneels and adores; rising, he elevates the Host so that it can be seen, lays it on the corporal, and adores again. From now on he keeps thumb and forefinger joined.', None, 'modus-x-2'),
  r('Kneeling behind the priest, the server rings the bell at each elevation and raises the chasuble.', 'l', 'varia-vi-7'),
  r('The bell is rung at each elevation.', 's', 'varia-vi-7'),
  r('The deacon and the subdeacon (with the paten) kneel on the top step at the priest’s right and left, an acolyte beside each; one acolyte rings the bell.', MC, 'ministri-xv-1', 'thur'),
  r('The deacon and the subdeacon kneel on the top step at the priest’s right and left, an acolyte beside each; one acolyte rings the bell.', MC, 'ministri-xv-1', '!thur'),
  r('The deacon takes the thurible and incenses at each elevation.', MC, 'ministri-xv-1', 'full,thur'),
  r('He uncovers the chalice; taking it in both hands, he blesses it at benedixit, and says the words of consecration:', None, ['modus-x-3', 'modus-x-4']),
  X(C, 'Símili modo'),
  r('He sets the chalice down and adores; rising, he elevates it, sets it down, and says:', None, 'modus-x-4'),
  X(C, 'Hæc quotiescúmque'),
  r('He covers the chalice and adores again. Then, with arms extended:', None, ['modus-x-4', 'modus-xi-1']),
  r('At Hostiam puram he makes three crosses over the offerings, then one over the Host and one over the chalice:', None, 'modus-xi-1'),
  X(C, 'Unde et mémores'),
  r('With hands extended:', None, 'modus-xi-2'),
  X(C, 'Supra quæ'),
  r('Bowing profoundly with arms crossed; rising at ut quotquot, he kisses the corporal; he blesses the Host and the chalice, and signs himself at benedictione caelesti:', None, 'modus-xi-2'),
  X(C, 'Súpplices'),
  r('With hands joined; at N. et N. he pauses to pray in silence for the dead:', None, 'modus-xi-3'),
  X(C, 'Meménto étiam'),
  r('Striking his breast, he says the first three words aloud:', None, 'modus-xi-3'),
  X(C, 'Nobis quoque'),
  r('He blesses the offerings at sanctificas, vivificas, benedicis; he uncovers the chalice and genuflects; with the Host he makes three crosses over the chalice and two before it; he lays the Host down, covers the chalice, and genuflects:', None, 'modus-xi-4'),
  X(C, 'Per quem'), X(C, 'Per ómnia'), X(C, 'Amen')]
P = 'pater'
A['pater'] = [
  r('His hands are laid on the corporal; at Pater noster he raises and extends them:', None, 'modus-xii-1'),
  X(P, 'Orémus. Præcéptis'), X(P, 'Pater noster'),
  r('The ministers answer in a low voice:', MC, 'ministri-xvi-1'),
  X(P, 'Sed líbera'), X(P, 'Amen'),
  r('The subdeacon gives the paten to the deacon, who hands it to the priest, kissing his shoulder.', MC, 'ministri-xvi-1', 'thur'),
  r('The deacon takes the paten from the altar and hands it to the priest, kissing his shoulder.', MC, 'ministri-xvi-2', '!thur'),
  r('With hands extended; he bows at Maria:', None, 'modus-xii-1'),
  X(P, 'Líbera nos'),
  r('At da propitius pacem he signs himself with the paten and kisses it; he uncovers the chalice, genuflects, and breaks the Host over the chalice, keeping back a particle. Aloud:', None, ['modus-xii-2', 'modus-xii-3']),
  X(P, 'Per ómnia'), X(P, 'Amen', nth=1),
  r('With the particle he makes three crosses within the chalice:', None, 'modus-xii-3'),
  X(P, 'Pax'), X(P, 'Et cum')]
A['rAg'] = [
  r('He says the Agnus Dei aloud, holding the Host over the chalice.', LS, 'modus-xiii-1'),
  r('The deacon goes to the Gospel corner and the subdeacon to the Epistle corner, each with an acolyte, and they say the Agnus Dei with the priest.', MC, 'ministri-xvii-1')]
CM = 'communion'
A['communion'] = [
  r('Letting the particle fall into the chalice, he says secretly:', None, 'modus-xiii-1'),
  X(CM, 'Hæc sacrosáncta'),
  r('He kisses the lip of the chalice and gives the peace to the server, who holds the pall:', LS, 'modus-xiii-1', NR),
  r('He kisses the lip of the chalice; the deacon holds out the Pax for him to kiss, and he says:', MC, 'ministri-xvii-1', NR),
  X(CM, 'Pax tibi', c=NR),
  r('The deacon gives the Pax to the subdeacon, and he to the acolytes.', MC, 'ministri-xvii-1', NR),
  r('The deacon also takes the Pax to the Pope.', MC, 'varia-iii-5', 'pope,!req'),
  r('The deacon also takes the Pax to the Bishop.', MC, 'varia-iii-5', 'bp,!req'),
  r('The Master of the Order is present: the acolyte takes the Pax to him, and the brethren receive it after him in order.', 'c', 'ministri-xvii-2', 'mo,sd,!sol,!req'),
  r('An acolyte takes the Pax to the cantors, and they give it to the brethren in order.', 'c', 'ministri-xvii-2', 'sd,!sol,!mo,!req'),
  r('The subdeacon himself, an acolyte going before, takes the Pax to the cantors and the brethren in the choir.', 'c', 'ministri-xvii-3', 'sol,!req'),
  r('With head bowed, he says with all devotion this one prayer, adding no other and not striking his breast:', None, 'modus-xiii-2'),
  X(CM, 'Dómine Iesu Christe'),
  r('Holding the chalice in his right hand, he receives the Host, saying:', None, 'modus-xiii-2'),
  X(CM, 'Corpus et Sanguis'),
  r('He covers the chalice and rests a moment in meditation; then he genuflects and receives the Blood with the particle, saying nothing.', None, 'modus-xiii-2'),
  r('He gathers any particles on the corporal into the chalice with the paten, and consumes them.', None, 'modus-xiii-3'),
  r('Communion of the faithful.'),
  X(CM, 'Ecce Agnus'), X(CM, 'Dómine, non sum'), X(CM, 'Corpus Dómini nostri'),
  r('The server pours wine for the first ablution and wine and water for the second, moves the Missal, and puts out the elevation candle.', 'l', 'varia-vi-8'),
  r('The subdeacon pours the ablutions; the deacon moves the Missal and folds the corporal; the acolytes put out the elevation candles.', MC, 'ministri-xviii-1'),
  r('He takes the first ablution, of wine, saying nothing; at the second, of wine and water poured over his fingers, he says:', None, 'modus-xiv-1'),
  X(CM, 'Quod ore'),
  r('He wipes his fingers and the chalice and covers it; then he goes to the Missal at the Epistle corner and reads the Communion.', LS, ['modus-xiv-1', 'modus-xiv-2']),
  r('The subdeacon purifies and covers the chalice; the priest goes to the Missal and reads the Communion.', MC, 'ministri-xviii-1'),
  gx('leaves the middle for the Communion')]
A['post'] = [r('Turning to the people as before:', None, 'modus-xiv-2', '!sac'),
  r('The Sacrament is in the tabernacle: he turns as at the Collect, by his right, without turning his back to it:', None, 'varia-ii-9', 'tab'),
  r('The Sacrament is exposed: he turns as at the Collect, from the Gospel side of the middle, genuflecting before and after:', None, 'varia-ii-5', 'exp'),
  r('The deacon lifts the hem of the chasuble.', MC, 'ministri-xix-1'),
  X('post', 'Dóminus vobíscum'), X('post', 'Et cum spíritu'),
  r('Turned back to the book, bowing to the cross:', None, 'modus-xiv-2'),
  X('post', 'Orémus'),
  r('He reads the Postcommunion with hands extended.', None, 'modus-xiv-2'),
  r('After the last Postcommunion he says Oremus with head bowed, and Humiliate capita vestra Deo; then the Prayer over the people.', LS, 'modus-xiv-3', 'sp'),
  r('After the last Postcommunion the priest says Oremus, bowing with the ministers; the deacon sings Humiliate capita vestra Deo; then the priest says the Prayer over the people.', MC, 'ministri-xix-2', 'sp'),
  r('During the last prayers the subdeacon takes the chalice back to the sacristy.', MC, 'ministri-xix-3')]
A['postEnd'] = [
  r('At the end of the last prayer he comes to the middle and turns to the people:', None, ['modus-xiv-2', 'modus-xv-1'], '!sac'),
  r('At the end of the last prayer he comes to the middle and turns to the people as at the Collect, by his right:', None, 'varia-ii-9', 'tab'),
  r('At the end of the last prayer he genuflects at the middle and turns to the people from the Gospel side:', None, 'varia-ii-5', 'exp'),
  X('postEnd', 'Dóminus vobíscum'), X('postEnd', 'Et cum spíritu'),
  r('Still facing the people:', LS, 'modus-xv-1', '!nogl,!req'),
  r('Facing the altar:', LS, 'modus-xv-1', 'nogl'),
  r('The deacon, turning with the priest, sings it; then they turn back to the altar without going round:', MC, 'ministri-xx-1', '!nogl,!req'),
  r('The deacon sings it facing the altar with the priest:', MC, 'ministri-xx-1', 'nogl')]
E = 'end'
A['end'] = [
  r('Turned back to the altar, bowing profoundly, he says secretly:', None, 'modus-xv-2'),
  X(E, 'Pláceat'),
  r('At Per Christum he kisses the altar; then, turning to the people, he blesses them with a single sign of the cross:', None, 'modus-xv-2', '!req,!prel'),
  r('At Per Christum he kisses the altar, and turns towards the Pope; kneeling as if asking leave to bless, he blesses the people on the side away from the Pope:', None, 'varia-iii-6', '!req,pope'),
  r('At Per Christum he kisses the altar, and turns towards the Bishop; bowing as if asking leave to bless, he blesses the people on the side away from the Bishop:', None, 'varia-iii-6', '!req,bp'),
  r('At Per Christum he kisses the altar.', None, 'modus-xv-2', 'req'),
  r('The ministers bow their heads.', MC, 'ministri-xx-2', NR),
  X(E, 'Benedíctio', c=NR), dict(O[E]['lines'][4], **{'if': NR}),
  r('Completing the circle, he goes to the Gospel corner.', None, 'modus-xv-2', '!sac'),
  r('He turns back the way he came, bows his head before the tabernacle at the middle, and goes to the Gospel corner.', None, 'varia-ii-10', 'tab'),
  r('He returns to the middle, genuflects, and goes to the Gospel corner.', None, 'varia-ii-7', 'exp'),
  r('The acolytes hold their lighted candles; the deacon and subdeacon stand at the priest’s left for the last Gospel.', MC, 'ministri-xx-2'),
  r('At the Gospel side he signs the altar with his thumb, and himself on the forehead, lips and breast; he genuflects at Et Verbum caro factum est:', None, 'modus-xv-3'),
  X(E, 'Dóminus vobíscum'), X(E, 'Et cum spíritu'), X(E, 'Inítium'), X(E, 'Glória tibi'), X(E, 'In princípio'), X(E, 'Deo grátias'),
  r('He makes a fitting reverence to the Pope.', None, 'varia-iii-7', 'pope'),
  r('He makes a fitting reverence to the Bishop.', None, 'varia-iii-7', 'bp'),
  r('At the middle he folds the corporal, covers the chalice, bows to the cross, covers his head, and takes the chalice; below the lowest step he bows profoundly, and returns to the sacristy saying the Benedicite.', LS, 'modus-xv-4', '!sac'),
  r('At the middle he folds the corporal, covers the chalice, bows to the cross, covers his head, and takes the chalice; below the lowest step he genuflects, and returns to the sacristy saying the Benedicite.', LS, 'modus-xv-4', 'tab'),
  r('At the middle he folds the corporal, covers the chalice, and takes the chalice; below the lowest step he kneels on both knees, and returns to the sacristy saying the Benedicite.', LS, ['modus-xv-4', 'varia-ii-8'], 'exp'),
  r('In the sacristy the server, kneeling, asks pardon for any fault, helps the priest unvest, and says Benedictus Deus; the priest answers Pater, et Filius, et Spiritus Sanctus.', 'l', ['varia-vi-10', 'varia-vi-11']),
  r('Making the same reverence as at the entrance, all return to the sacristy in order.', MC, 'ministri-xx-2', '!exp'),
  r('Kneeling on both knees, all return to the sacristy in order.', MC, 'varia-ii-8', 'exp'),
  r('The ministers unvest the priest, then one another; the acolytes cover the altar.', MC, ['ministri-xx-2', 'ministri-xx-3'])]
A['agLow'] = BASIC['agLow']; A['offertoryEnd'] = BASIC['offertoryEnd']; A['commConv'] = BASIC['commConv']
import re as _re
_PFX = _re.compile(r'^(The Sacrament is exposed|The Sacrament is in the tabernacle|The Pope is present|The Bishop is present|The Master of the Order is present): ')
for _k, _ls in A.items():
    for _l in _ls:
        if 'r' in _l and _l.get('if') and _re.search(r'(^|,)(tab|exp|pope|bp|mo)(,|$)', _l['if']):
            _t = _PFX.sub('', _l['r']); _l['r'] = _t[:1].upper() + _t[1:]
STRIPS = {'rAs', 'rIn', 'rKy', 'rGl', 'rGr', 'rCr', 'rPf', 'rSa', 'rAg'}
N = {}
for k, sec in O.items():
    if k == 'dismiss': N[k] = sec; continue
    N[k] = {'la': sec['la'], 'en': sec['en'], 'lines': A.get(k, sec['lines'])}
for k in STRIPS:
    N[k] = {'la': '', 'en': '', 'strip': 1, 'lines': A[k]}
for k in BASIC:
    N.setdefault(k, {'la': '', 'en': '', 'strip': 1, 'lines': []})
# keep the order of the Mass in the file
ORDER = ['chalice', 'foot', 'rAs', 'rIn', 'rKy', 'rGl', 'kyLow', 'glLow', 'collect', 'collectEnd', 'rGr', 'gospel', 'afterGospel', 'rCr', 'crLow',
         'offerDial', 'offertory', 'offertoryEnd', 'rPf', 'rSa', 'saLow', 'canon', 'pater', 'rAg', 'agLow', 'commSimple', 'commConv',
         'communion', 'post', 'postEnd', 'end', 'dismiss']
N = {k: N[k] for k in ORDER}
# serialise
def js(v): return json.dumps(v, ensure_ascii=False)
out = ['''/* Ordo Missæ secundum ritum Ordinis Prædicatorum (Missale O.P. 1939).
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
window.ORDO = {''']
keys = list(N.keys())
for j, k in enumerate(keys):
    s = N[k]
    if k == 'dismiss':
        out.append('  dismiss: {\n' + ',\n'.join('    %s: [%s]' % (kk, ', '.join(js(x) for x in vv)) for kk, vv in s.items()) + '\n  }')
        continue
    clean = [{kk: vv for kk, vv in l.items() if kk not in ('rb', 'mb', 'lv')} for l in s['lines']]
    basic = BASIC.get(k, [])
    head = '  %s: {la: %s, en: %s%s, lines: [\n' % (k, js(s['la']), js(s['en']), ', strip: 1' if s.get('strip') else '')
    body = head + ',\n'.join('    ' + js(l) for l in basic) + '\n  ]'
    if clean != basic: body += ', adv: [\n' + ',\n'.join('    ' + js(l) for l in clean) + '\n  ]'
    out.append(body + '}' + (',' if j < len(keys) - 1 else ''))
src = '\n'.join(out[:1]) + '\n' + ',\n'.join(o.rstrip(',') for o in out[1:]) + '\n};\n'
open(os.path.join(ROOT, 'data', 'ordo.js'), 'w').write(src)
# check refs
R = json.loads(open(os.path.join(ROOT, 'data', 'rubtext.js')).read().split('window.RUBTEXT = ', 1)[1].rstrip().rstrip(';'))
bad = [x for s in N.values() if isinstance(s, dict) and 'lines' in s for l in s['lines'] for x in l.get('ref', []) if x not in R]
print('bad refs', bad)
