# Builds data/ordo.js (basic lines and the full directions of the Missale O.P. 1939, Ritus) from the earlier ordo.js dumped to /tmp/ordo.json; kept for reference.
import json, re
O = json.load(open('/tmp/ordo.json'))
def r(t, m=None, ref=None, c=None, lv=None):
    d = {}
    if m: d['m'] = m
    if c: d['if'] = c
    d['r'] = t
    if ref: d['ref'] = ref if isinstance(ref, list) else [ref]
    return d
def L(sec, i, **kw):
    # a line of the earlier Order of Mass, kept for both modes; where the advanced text or forms differ, the basic ones are kept in rb / mb
    old = O[sec]['lines'][i]; d = dict(old)
    if 'r' in kw and kw['r'] != old.get('r'): d['rb'] = kw.get('rb', old['r'])
    if 'm' in kw and kw['m'] != old.get('m'): d['mb'] = old.get('m', '')
    kw.pop('rb', None); d.update(kw); return d
def B(sec, i, r=None, m=None):
    # a direction of the earlier Order of Mass shown only in the basic mode (corrected where it was wrong)
    d = dict(O[sec]['lines'][i]); d['lv'] = 'b'
    if r: d['r'] = r
    if m is not None:
        if m: d['m'] = m
        else: d.pop('m', None)
    return d
def t(w, la, en, m=None, c=None):
    d = {}
    if m: d['m'] = m
    if c: d['if'] = c
    d.update({'w': w, 'la': la, 'en': en}); return d
# conditional directions repeated wherever the priest turns to the people
def turn(m=None, first=False):
    if not first:
        return [r('The Sacrament is in the tabernacle: he turns to the people and back as at the Collect, by his right, without turning his back to it.', m, 'varia-ii-9', 'tab'),
                r('The Sacrament is exposed: he turns to the people and back as at the Collect, from the Gospel side of the middle, genuflecting before and after.', m, 'varia-ii-5', 'exp')]
    return [r('The Sacrament is in the tabernacle on this altar: so as not to turn his back to it, he goes to the middle, bows his head, steps a little towards the Gospel side and turns to the people by his right; he returns the same way, bowing again before the tabernacle.', m, 'varia-ii-9', 'tab'),
            r('The Sacrament is exposed: he genuflects at the middle, goes towards the Gospel corner and turns to the people there, his back towards the corner of the altar; he returns the same way, genuflecting again in the middle.', m, 'varia-ii-5', 'exp')]
def gx(m=None, where='passes the middle of the altar'):
    # the Sacrament exposed: a genuflexion each time the priest comes to, leaves or passes the middle (Missale O.P. 1939, Ritus, De his quae addenda sunt ... n. 4)
    return r('The Sacrament is exposed: he genuflects on one knee as he %s.' % where, m, 'varia-ii-4', 'exp')
N = {}
N['chalice'] = {'la': O['chalice']['la'], 'en': O['chalice']['en'], 'lines': [
  r('Coming to the altar, he bows profoundly at its middle (without bending the knee), goes up, sets the chalice towards the Gospel side, spreads the corporal, lays the paten with the host on it and the purificator beside it. He pours a little wine into the chalice; the server, holding out the water, says:', 'l', ['praeparatio-ii-8', 'praeparatio-ii-9'], '!sac'),
  r('Coming to the altar, he genuflects on one knee at its middle (the Sacrament being in the tabernacle), goes up, sets the chalice towards the Gospel side, spreads the corporal, lays the paten with the host on it and the purificator beside it. He pours a little wine into the chalice; the server, holding out the water, says:', 'l', ['praeparatio-ii-8', 'praeparatio-ii-9'], 'tab'),
  r('Coming to the altar, he kneels on both knees before the Sacrament exposed and, uncovering his head, adores; then he goes up, sets the chalice towards the Gospel side, spreads the corporal, lays the paten with the host on it and the purificator beside it. He pours a little wine into the chalice; the server, holding out the water, says:', 'l', ['praeparatio-ii-8', 'varia-ii-3'], 'exp'),
  L('chalice', 1),
  r('When the priest has read the Gospel at his seat, the subdeacon carries the Missal to the Gospel corner, washes his hands, puts on the veil, and brings the chalice, holding it by the knot with the paten and pall steadied above. In the sight of the seated priest and deacon he gives the paten with the host to the deacon, who shows it to the priest; he pours in wine, as much as the priest indicates, from the acolyte’s cruet, and offers the water to be blessed:', 'mc', 'ministri-vi-4'),
  L('chalice', 3),
  t('D', 'Dóminus.', 'The Lord.', 'mc'),
  r('The priest blesses the water:', None, 'praeparatio-ii-9', '!req'),
  L('chalice', 5, **{'if': '!req'}),
  L('chalice', 6, **{'if': '!req'}),
  r('In Masses for the Dead the water is not blessed.', None, 'varia-iv-1', 'req'),
  r('He lets fall into the chalice so little water that it can very easily be wholly changed into wine, wipes the chalice, sets the paten with the host on it, covers it with the pall and veil and puts it on the corporal; then he goes to the Missal at the Epistle corner and finds the Mass.', 'l', 'praeparatio-ii-9'),
  r('The subdeacon lets a little water fall into the middle of the chalice, takes back the paten with the host from the deacon, carries the chalice to the middle of the altar, covers it as before, and comes to sit.', 'mc', 'ministri-vi-4')]}
N['foot'] = {'la': O['foot']['la'], 'en': O['foot']['en'], 'lines': [
  r('Having found the Mass, he returns with hands joined to the middle of the altar, uncovers his head with both hands, arranges the capuce, and prays secretly:', 'l', 'praeparatio-ii-10'),
  r('When the choir has begun the Gloria Patri of the Introit (or its verse), the ministers go to the altar with heads covered by capuce and amice: the acolytes with lighted candles, the subdeacon with the book of the Gospels (or the prepared chalice, on days when it is not brought during the Gloria), the deacon with the Missal, last the priest. Below the lowest step, the deacon at the priest’s right, the subdeacon at his left and an acolyte on each side, all bow profoundly (or genuflect) and uncover; the priest says secretly:', 'mc', ['ministri-iii-1', 'ministri-iii-2']),
  r('Standing before the altar, the priest says in a low voice:', 's'),
  L('foot', 1),
  r('Before the Pope: the priest waits kneeling below the lowest step on the Gospel side, before the Pontiff; having received his blessing he rises and, turned somewhat towards the altar, begins Mass.', None, 'varia-iii-1', 'pope'),
  r('Before a Cardinal Legate, a Patriarch, an Archbishop or a Bishop in his own see or jurisdiction: the priest waits standing below the lowest step on the Gospel side; at the sign given he makes a profound reverence to the prelate and, turned to the altar, begins Mass.', None, 'varia-iii-1', 'bp'),
  r('He stands immediately below the top step before the middle of the altar, with hands joined before his breast, bows profoundly, and begins in a clear voice, signing himself from forehead to breast and from the left shoulder to the right:', 'ls', 'modus-i-1'),
  r('Rising, the priest signs himself from forehead to breast and shoulders and says in an audible voice:', 'mc', 'ministri-iii-2'),
  L('foot', 3), L('foot', 4), L('foot', 5),
  r('Bowing profoundly, with joined hands, in a moderate voice (he does not strike his breast at mea culpa):', None, 'modus-i-2'),
  r('The ministers bow profoundly with him, without bending the knee; the acolytes stand upright facing one another, holding their candlesticks.', 'mc', 'ministri-iii-2'),
  r('Celebrating solemnly before the Pope or one of the prelates named, in a church of his jurisdiction, the priest makes the Confession with the prelate, standing at his left, and says tibi Pater for vobis fratres and te Pater for vos fratres.', 'mc', 'varia-iii-2', 'prel'),
  L('foot', 7),
  r('The server, kneeling at the priest’s left, answers:', 'l', 'varia-vi-4'),
  L('foot', 8), L('foot', 9),
  r('He too says the Confiteor (with et tibi, pater), not striking his breast:', 'l', 'modus-i-2'),
  L('foot', 10), L('foot', 11), L('foot', 12),
  L('foot', 13, ref=['modus-i-3']),
  L('foot', 14), L('foot', 15),
  r('Standing fully erect, with hands joined before his breast:', None, 'modus-i-3'),
  L('foot', 16), L('foot', 17),
  r('The Confession made, he genuflects if it is the Pope, or bows profoundly to the other prelates.', 'mc', 'varia-iii-3', 'prel'),
  L('foot', 18, ref=['modus-i-4', 'ministri-iii-3']),
  L('foot', 19),
  L('foot', 20, ref=['modus-i-4']),
  r('Meanwhile the deacon puts the Missal at the Epistle corner and the subdeacon the book of the Gospels at the Gospel corner, propped at the back; the acolytes set their candles down on the sanctuary steps and put them out.', 'mc', 'ministri-iii-3'),
  r('The Sacrament is exposed: on coming to the altar all kneel on both knees.', 'smc', 'varia-ii-3', 'exp'),
  r('The Sacrament is exposed. As far as possible no Mass but a solemn Mass is said before it; when one is, each time the celebrant comes to, leaves or passes the middle of the altar, he and the ministers genuflect on one knee, and no one ever turns his back to the Sacrament.', None, ['varia-ii-1', 'varia-ii-4', 'varia-ii-6'], 'exp'),
  r('The Sacrament is exposed: the deacon kisses neither the priest’s hand nor his shoulder when he hands him anything (the chalice, the thurible, the paten).', 'mc', ['varia-ii-6', 'ministri-x-1', 'ministri-xvi-1'], 'exp'),
  r('The Sacrament is exposed: the server genuflects, instead of bowing, whenever he passes the middle of the altar.', 'l', 'varia-vi-6', 'exp'),
  r('On days other than Corpus Christi and its octave when the Sacrament is exposed, a solemn Mass of the Blessed Sacrament is celebrated, with the due commemorations; the conventual Mass of the Office of the day is also said (or one Mass is sung of the day, with a commemoration of the Sacrament).', 'mc', 'varia-ii-2', 'exp'),
  r('The Sacrament is in the tabernacle: the bows made at the middle of the altar on arriving and leaving become genuflexions.', 'smc', ['praeparatio-ii-8', 'modus-xv-4'], 'tab')]}
N['rAs'] = {'la': '', 'en': '', 'strip': 1, 'lines': [
  r('On Sundays, when the Hour before Mass is finished, the priest, deacon and subdeacon come to the sanctuary in albs with stoles and maniples (if there is to be a procession, the priest in a silk cope and the ministers in dalmatics), the acolytes going before. The deacon stands with the senior acolyte at the priest’s right, the subdeacon with the junior at his left; all bow profoundly (or genuflect) before the altar.', 'mc', 'ministri-ii-1'),
  r('The senior acolyte brings the water, the deacon hands the sprinkler, and as the cantors begin Asperges me the priest sprinkles the high altar (not too much), then the deacon, subdeacon and acolytes, the Master of the Order if present, the cantors on Doubles, and the brethren, beginning on the right; after the clerics the lay brothers, then the seculars in choir. The same order is kept for the peace and the incensing.', 'c', 'ministri-ii-2'),
  r('The priest sprinkles the altar, the ministers and the people.', 'm', 'ministri-ii-2'),
  r('The Master of the Order is sprinkled next after the ministers and acolytes, before the cantors and the brethren.', 'c', 'ministri-ii-2', 'mo'),
  r('When the antiphon is finished, standing before the sanctuary steps as at the beginning, he says Ostende nobis, Dominus vobiscum, Oremus and the prayer Exaudi nos; then the ministers return to the sacristy (and, if there is a procession, it follows, after which the priest exchanges the cope for the chasuble).', 'mc', ['ministri-ii-3', 'ministri-ii-4']),
]}
N['rIn'] = {'la': '', 'en': '', 'strip': 1, 'lines': [
  r('At the Epistle corner he begins the Introit in a clear and audible voice; at Gloria Patri he bows his head a little towards the cross (in Masses for the Dead there is no Gloria Patri, and the Requiem aeternam is repeated after the verse); then he repeats the Introit as far as the verse.', 'ls', ['modus-ii-1', 'varia-iv-1']),
  r('All come together at the book, opened by the deacon (who turns the pages and points out what is to be said), and standing at the priest’s right in order of rank say the Introit and the Kyrie with him; they do not kneel at Salve sancta parens.', 'mc', 'ministri-iii-4'),
  r('Then the deacon stands behind the priest and the subdeacon behind the deacon; the acolytes stand below the sanctuary steps (or in the first stalls of the choir), and never go up to the top step. During the Canon they stand at the deacon’s right and left, in the form of a cross.', 'mc', 'ministri-iii-5')]}
N['rKy'] = {'la': '', 'en': '', 'strip': 1, 'lines': [
  r('He says the Kyrie eleison alternately with the server.', 'l', ['modus-ii-1', 'varia-vi-4']),
  r('On Sundays, and on Doubles and above, the priest, deacon and subdeacon may sit at the Epistle side (the deacon at the priest’s left, the subdeacon at the deacon’s left, the acolytes on a lower bench). The acolytes spread a small cloth over their knees, and one of them takes it up at the last Kyrie eleison, beginning with the priest and kissing his hand.', 'mc', 'ministri-iii-6'),
  r('When the Gloria is not said (from Septuagesima to Easter), the subdeacon fetches the chalice from the sacristy during the Kyrie, as is done during the Gloria on other days.', 'mc', 'ministri-iv-2', 'nogl')]}
N['rGl'] = {'la': '', 'en': '', 'strip': 1, 'lines': [
  r('The last Kyrie said, he goes with hands joined to the middle of the altar. At Gloria he lays his hands extended on the altar; at in excelsis he raises them; at Deo he joins them and bows his head; then he returns to the Epistle corner and continues it at the book with hands joined. He bows his head at Adoramus te, Gratias agimus tibi, Jesu Christe, suscipe deprecationem nostram, and again at Jesu Christe.', 'l', 'modus-ii-2'),
  r('The last Kyrie sung, he goes to the middle of the altar and intones the Gloria, with the gestures of the Low Mass (hands laid on the altar at Gloria, raised at in excelsis, joined at Deo, with a bow); then he goes to the Epistle corner and continues it at the book, bowing at Adoramus te, Gratias agimus tibi, Jesu Christe and Suscipe deprecationem nostram.', 's', ['modus-ii-2', 'ministri-iv-1']),
  gx('ls', 'comes to the middle for the Gloria and again as he leaves it'),
  r('All rise, stand before the middle of the altar and bow profoundly; the priest goes up and intones the Gloria. Then all go together to the Epistle corner and continue it with him, standing at his right; when it is said, the priest and deacon stand until the community has finished it. The ministers pass behind, never between, those of higher rank.', 'mc', 'ministri-iv-1'),
  r('Meanwhile on Sundays and Doubles the subdeacon, an acolyte going before with the wine and water, goes to the sacristy, puts on a clean veil over his shoulders, and brings the prepared chalice raised before his breast; they bow profoundly in the middle; he sets the chalice on the veil spread on the Epistle corner, and the acolyte puts the cruets in the niche or on a bench.', 'mc', 'ministri-iv-2')]}
N['kyLow'] = O['kyLow']; N['glLow'] = O['glLow']
N['collect'] = {'la': O['collect']['la'], 'en': O['collect']['en'], 'lines': [
  r('In the same place, without kissing the altar, he turns to the people by his left (towards the Epistle corner), his hands raised no higher than the shoulders and extended so that they can be seen from behind, and says Dominus vobiscum, joining his hands; returning to the book by the same side, he bows his head a little towards the cross and says Oremus, opening his hands for the prayer. At Per Dominum nostrum he joins them and bows his head.', None, ['modus-iii-1', 'modus-iii-2'])] + turn(first=True) + [
  r('As the priest begins Dominus vobiscum, the deacon (not kneeling, unless a bishop celebrates) lightly raises the lower edge of the chasuble, and so goes with him to the book and points out the prayer; he does the same at the Offertory, the Orate fratres and the Postcommunion.', 'mc', 'ministri-v-1'),
  L('collect', 1), L('collect', 2), L('collect', 3),
  r('After Oremus he says Flectamus genua: taking the front of the chasuble in both hands and laying it on the altar, he kneels; the server answers Levate, and rising at once he says the prayer.', 'ls', 'modus-iii-3', 'flect'),
  r('After Oremus the deacon, kneeling with the lower ministers, sings Flectamus genua, and rising at once sings Levate; the priest does not kneel but goes on with the prayer.', 'mc', ['ministri-v-2', 'varia-i-2'], 'flect')]}
N['collectEnd'] = {'la': O['collectEnd']['la'], 'en': O['collectEnd']['en'], 'lines': [
  r('With his hands laid on the book, or resting on the altar, he reads the Epistle or Lesson; then, with hands joined, the Gradual, Alleluia or Tract, and Sequence.', 'l', 'modus-iv-1'),
  r('The server stays kneeling at the Gospel side (always on the side opposite the book) until the Epistle and the Alleluia with its verse, or the Tract or Sequence, are said.', 'l', ['varia-vi-4', 'varia-vi-5']),
  L('collectEnd', 1, m='s'),
  r('After the last prayer, with Per omnia saecula saeculorum and the choir’s Amen, the priest and deacon go down to the lowest step; all bow profoundly before the altar and go to sit.', 'mc', 'ministri-v-2'),
  r('During the last prayer the subdeacon, an acolyte going before, carries the book of Epistles against his breast to the lectern before the sanctuary steps (or, in some convents, on Sundays and Doubles, to the pulpit) and sings the Epistle facing the altar; the acolyte then puts the book back on the altar.', 'mc', 'ministri-vi-1'),
  r('The deacon and an acolyte seat the priest and lay a small cloth on his knees. The deacon washes his fingers, spreads the corporal in the middle of the altar and gives the Missal to the acolyte, who holds it before the seated priest. The priest reads the Epistle, then the Gradual, Alleluia or Tract and Sequence, verse by verse alternately with the deacon; then they rise, and the priest, standing, reads the Gospel at his seat, signing himself at its beginning and end.', 'mc', ['ministri-vi-2', 'ministri-vi-3'])]}
N['rGr'] = {'la': '', 'en': '', 'strip': 1, 'lines': [
  r('He genuflects at the verse of the Tract Adjuva nos, Deus salutaris noster.', 'ls', 'varia-i-1', 'adjuva'),
  r('All kneel at the verse of the Tract Adjuva nos, Deus salutaris noster.', 'mc', ['varia-i-1', 'varia-i-2'], 'adjuva'),
  r('He genuflects while he says the verse Veni Sancte Spiritus, as far as reple.', 'ls', 'varia-i-1', 'veni'),
  r('At the verse Veni Sancte Spiritus the priest and ministers rise and stand (they do not kneel) while it is sung as far as reple; they sit again when the choir rises.', 'mc', ['ministri-vii-1', 'varia-i-2'], 'veni'),
  r('Towards the end of the Alleluia, Tract, Responsory or Sequence the acolytes light their candles. The thurifer comes on Simple feasts and above, on Sundays, on Tuesdays of St Dominic, Wednesdays of St Thomas or another saint of the Order, Thursdays of Corpus Christi, Saturdays of Our Lady and the octave day of simple octaves; he stands in the sanctuary before the middle of the altar.', 'mc', 'ministri-vii-2', 'full'),
  r('On Totum Duplex feasts (on which alone the cross is carried at the Gospel), after the Epistle the acolytes go with the thurifer to the sacristy and return with the crossbearer between them; all but the crossbearer bow profoundly before the altar steps.', 'mc', 'ministri-vii-3', 'full'),
  r('The thurifer goes to the priest and offers the incense, saying Benedicite; the priest makes the sign of the cross over it, saying In nomine Patris, et Filii, et Spiritus Sancti. Amen.', 'mc', 'ministri-vii-3', 'full')]}
N['gospel'] = {'la': O['gospel']['la'], 'en': O['gospel']['en'], 'lines': [
  r('When the Alleluia or Tract is finished, the server carries the Missal to the Gospel corner; the priest goes there with joined hands, bowing to the cross at the middle of the altar, and says secretly:', 'ls', ['modus-iv-2', 'varia-vi-4'], '!req'),
  r('When the Tract or Sequence is finished, the server carries the Missal to the Gospel corner; the priest goes there with joined hands, bowing to the cross at the middle of the altar.', 'ls', ['modus-iv-2', 'varia-vi-4'], 'req'),
  gx('ls', 'passes the middle on his way to the Gospel corner'),
  L('gospel', 1, **{'if': '!req'}),
  r('In Masses for the Dead he does not say Dominus sit in corde meo.', 'ls', 'varia-iv-1', 'req'),
  r('The deacon rises, takes the book of the Gospels in both hands and, bowing a little before the priest, says:', 'mc', 'ministri-viii-1'),
  L('gospel', 3, m='mc'),
  r('The priest, rising, answers:', 'mc', 'ministri-viii-1'),
  L('gospel', 4, m='mc'),
  t('P', 'In nómine Patris, et Fílii, et Spíritus Sancti.', 'In the name of the Father, and of the Son, and of the Holy Ghost.', 'mc'),
  t('D', 'Amen.', 'Amen.', 'mc'),
  r('They go to the lectern at the Gospel side (in a slightly raised place, facing north; in some convents, on Sundays and Doubles, to the pulpit): first the thurifer, then the candle-bearers (with the crossbearer between them on Totum Duplex feasts), the subdeacon with the cushion, and last the deacon carrying the book against his breast. The subdeacon puts the cushion under the book and stands behind the deacon; the crossbearer and candle-bearers stand facing the deacon.', 'mc', ['ministri-viii-1', 'ministri-viii-2']),
  r('He lays his joined hands on the Missal and says:', 'ls', 'modus-v-1'),
  L('gospel', 6, m='ls'), L('gospel', 7, m='ls'),
  t('D', 'Dóminus vobíscum.', 'The Lord be with you.', 'mc'), t('S', 'Et cum spíritu tuo.', 'And with thy spirit.', 'mc'),
  r('At Sequentia he signs the beginning of the Gospel with his thumb, then his forehead, mouth and breast, and then his whole person:', 'ls', 'modus-v-1'),
  r('At Sequentia the deacon signs the beginning of the Gospel with his thumb, then his forehead, mouth and breast, and his whole person; the priest and subdeacon do the same, facing the altar. Taking the thurible from the subdeacon, he incenses the book three times, and sings the Gospel with hands joined.', 'mc', 'ministri-viii-3'),
  L('gospel', 8, m='ls'),
  t('D', 'Sequéntia sancti Evangélii secúndum N.', 'The continuation of the holy Gospel according to N.', 'mc'),
  L('gospel', 9),
  r('With his joined hands on the Missal he reads the whole Gospel. He bows his head at the names of Jesus and Mary, and genuflects towards the book where the Gospel requires it (Et procidentes adoraverunt eum at the Epiphany, and the like).', 'ls', ['modus-v-2', 'varia-i-1']),
  r('While the Gospel is sung the priest stands at the Epistle corner facing it, hands joined; all the brethren turn towards the Gospel wherever it is read, and sign themselves at its end. At the words at which one genuflects, the deacon genuflects towards the book, the priest and the others towards the altar; the acolytes holding the candlesticks do not.', 'mc', ['ministri-viii-4', 'varia-i-2'])]}
N['afterGospel'] = {'la': O['afterGospel']['la'], 'en': O['afterGospel']['en'], 'lines': [
  r('At the end of the Gospel he signs himself again; then, signing the Gospel with the cross, he kisses it, saying secretly (not after the Passion):', 'ls', 'modus-v-3', '!prel,!req'),
  r('The Gospel finished, the deacon hands the open book with the cushion to the subdeacon, and they return to the altar in the order they came. The priest, at the middle of the altar, kisses the book which the subdeacon brings, the deacon pointing out the Gospel with his finger (not after the Passion); signing it with his thumb, he says (the deacon answers Amen, and kisses it after him):', 'mc', ['ministri-viii-5', 'ministri-ix-1'], '!prel,!req'),
  r('In Masses for the Dead the book is not kissed and Per evangelica dicta is not said.', None, 'varia-iv-1', 'req'),
  r('A prelate is present: the book of the Gospels is carried to the Pope, or to the prelate, to be kissed (to the most dignified only, if there are several; to none, if they are equal), and the celebrant neither kisses the book nor says Per evangelica dicta.', None, 'varia-iii-4', 'prel'),
  L('afterGospel', 1, **{'if': '!prel,!req'}),
  L('afterGospel', 2)]}
N['rCr'] = {'la': '', 'en': '', 'strip': 1, 'lines': [
  r('At the middle of the altar, his hands laid extended on it, he says Credo; at in unum he raises them, at Deum he joins them and bows his head to the cross; then he returns to the Gospel corner and continues at the book with hands joined, bowing his head at Jesum Christum. At Et incarnatus est he comes to the middle and kneels; having said Homo factus est he rises and returns to the book; he bows at simul adoratur and signs himself at Et vitam venturi saeculi.', 'l', ['modus-vi-1', 'modus-vi-2']),
  r('He intones the Credo at the middle of the altar (hands laid on it, raised at in unum, joined at Deum, with a bow), and continues it at the book; at Et incarnatus est he comes to the middle and kneels, rising after Homo factus est; he bows at simul adoratur and signs himself at Et vitam venturi saeculi.', 's', ['modus-vi-1', 'modus-vi-2']),
  gx('ls', 'comes to the middle for the Credo, and at each going to and from the book'),
  r('The priest intones the Credo at the middle of the altar; the deacon and the other ministers stand at his left, one behind another towards the Gospel corner, and continue it in a low voice. When the choir reaches Et incarnatus est, the priest kneels before the middle of the altar, the deacon and subdeacon on the first step behind him, the acolytes on a lower step with the crossbearer between them and the thurifer behind; all face the altar. Then the acolytes and thurifer bow and go back to the sacristy (with the cross, if it was carried). All bow at simul adoratur.', 'mc', ['ministri-ix-2', 'ministri-ix-3'])]}
N['crLow'] = O['crLow']
N['offerDial'] = {'la': O['offerDial']['la'], 'en': O['offerDial']['en'], 'lines': [
  r('At the middle of the altar (he does not kiss it), turning to the people, he opens and joins his hands as at the first Dominus vobiscum, and returns by the same way; with hands opened and raised, bowing his head to the cross, he begins Oremus, joining them at the last syllable:', None, 'modus-vii-1')] + turn() + [
  L('offerDial', 1), L('offerDial', 2), L('offerDial', 3),
  r('He goes to the book and reads the Offertory with hands joined:', 'ls', 'modus-vii-2'),
  r('The priest says the Offertory at the book, and the ministers continue it with him, all standing at his left:', 'mc', 'ministri-x-1')]}
N['offertory'] = {'la': O['offertory']['la'], 'en': O['offertory']['en'], 'lines': [
  r('Having said the Offertory and drawn the book nearer, he returns to the middle of the altar, lifts the veil with the pall from the chalice with both hands and sets it aside on the Epistle side; laying his hands on the altar he says Quid retribuam, raising them, and joining them at Calicem salutaris:', 'ls', 'modus-vii-2'),
  L('offertory', 2, m='ls'),
  r('Returning to the middle of the altar, the priest says:', 'mc', 'ministri-x-1'),
  t('P', 'Quid retríbuam Dómino pro ómnibus quæ retríbuit mihi?', 'What shall I render to the Lord for all the things that he hath rendered unto me?', 'mc'),
  r('Meanwhile the subdeacon uncovers the chalice of veil and pall and gives it to the deacon, who offers it to the priest, holding it by the lower part of the foot and kissing his hand (not if the Sacrament is exposed), saying:', 'mc', 'ministri-x-1'),
  t('D', 'Immola Deo sacrifícium laudis, et redde Altíssimo vota tua.', 'Offer to God the sacrifice of praise, and pay thy vows to the Most High.', 'mc'),
  r('The priest, taking it, says:', 'mc', 'ministri-x-1'),
  t('P', 'Cálicem salutáris accípiam, et nomen Dómini invocábo.', 'I will take the chalice of salvation, and I will call upon the name of the Lord.', 'mc'),
  r('In Masses for the Dead the words Quid retribuam Domino pro omnibus, quae retribuit mihi? are not said.', None, 'varia-iv-1', 'req'),
  r('He takes the chalice, with the paten and host upon it, in both hands (the right at the middle of the chalice, the left at the foot), raises it above the corporal to the height of his breast, and with his eyes raised to God offers both together:', None, 'modus-vii-3'),
  L('offertory', 4),
  r('He sets the chalice down in the middle of the corporal; with his left hand he lifts the paten and, putting his right to it also, lets the host down before the foot of the chalice without touching it; he puts the paten at the right of the corporal, half under it over the purificator, and covers the chalice with the pall.', None, 'modus-vii-3'),
  r('The incensing: the thurifer holds the thurible at the right of the altar; the deacon offers incense in the spoon, the priest blesses it, the deacon puts it in and hands him the thurible, kissing his hand (not if the Sacrament is exposed). The priest makes the sign of the cross with the thurible over the chalice, bows, and incenses it three times, swinging low, never above the shoulder; then the tabernacle (or the cross) three times. Bowing with the deacon at the middle, he incenses the top of the altar towards the candlesticks with three swings to the Epistle corner, returns, and does the same to the Gospel corner; then the front of the altar, three swings from the Gospel corner to the middle and three to the Epistle corner. The deacon raises his chasuble meanwhile.', 'mc', ['ministri-xi-1', 'ministri-xi-2'], 'full'),
  r('If there are relics or images of the saints on the altar, after the tabernacle (or cross) he incenses those on the Gospel side with two swings, and then those on the Epistle side, before going on with the altar.', 'mc', 'ministri-xi-3', 'full'),
  r('The Sacrament is exposed: after incensing the chalice the priest, kneeling on both knees on the top step with the ministers, incenses the Sacrament, bowing profoundly before and after; standing, he incenses the altar, genuflecting each time he passes the middle. He is incensed standing below the top step at the Epistle corner, facing the people, and washes his hands there. No one turns his back to the Sacrament.', 'mc', 'varia-ii-6', 'exp,full'),
  r('Meanwhile the other ministers stand at the Epistle corner, the subdeacon next to the altar, the acolytes and thurifer at his left, one below another. The priest, having finished, stands at the end of the altar with hands joined, facing the deacon, who incenses him with three swings and gives the thurible back to the thurifer.', 'mc', 'ministri-xi-4', 'full'),
  gx(None, 'leaves the middle for the washing of the hands, and again on his return'),
  r('He goes to the Epistle corner, the server having spread the towel and made the water ready, and washes the first four fingers, saying, and no further:', 'ls', ['modus-vii-4', 'varia-vi-6']),
  r('The priest washes his hands, the subdeacon pouring the water, the deacon handing him the towel taken from the acolyte; he says:', 'mc', 'ministri-xii-1'),
  L('offertory', 8),
  r('Having dried his fingers, he returns with hands joined to the middle of the altar and begins In spiritu humilitatis bowing profoundly, standing erect at et placeat tibi. He does not turn the pages or touch anything with the fingers with which he is to handle the Body of the Lord.', None, 'modus-vii-4'),
  L('offertory', 10),
  r('Turned to the people (he does not kiss the altar), with hands raised and extended, he says Orate fratres in a moderate voice; joining his hands he continues secretly, and completes the circle towards the Gospel corner to return to the Missal. There is no response:', None, 'modus-vii-5'),
  r('He says only the two words Orate fratres in a moderate voice, so that the ministers can hear; the deacon raises the chasuble as before. In the season of flies the deacon keeps them away from the priest and the sacrifice with a fan.', 'mc', 'ministri-xii-2')] + [dict(x, r=x['r'].replace(' as at the Collect', ' as at the Collect (he does not complete the circle)')) for x in turn()] + [
  L('offertory', 12),
  r('With hands joined, as before:', None, 'modus-vii-5'),
  L('offertory', 14),
  r('With hands joined he says Oremus; then, his hands opened and extended, the Secret, joining them and bowing his head a little at Per Dominum; before each further commemoration he says Oremus again:', None, 'modus-vii-5')]}
N['offertoryEnd'] = O['offertoryEnd']
N['rPf'] = {'la': '', 'en': '', 'strip': 1, 'lines': [
  r('At the middle of the altar his hands are laid on it on either side for Per omnia saecula saeculorum and Dominus vobiscum; at Sursum corda he raises and extends them; at Gratias agamus he joins them, bows his head to the cross at Deo nostro, and opens them again for the Preface, joining them at supplici confessione dicentes.', None, ['modus-viii-1', 'modus-viii-2']),
  r('During the Preface the thurifer makes ready; after Gratias agamus Domino Deo nostro he bows before the altar and incenses the deacon, then the subdeacon and the acolytes, who stand, the deacon with one acolyte at the Gospel corner and the subdeacon with the other at the Epistle corner, almost facing one another, hands joined and heads a little bowed.', 'mc', 'ministri-xiii-1', 'full'),
  r('The Master of the Order is present: the thurifer incenses him first in the choir, before the brethren.', 'c', 'ministri-xiii-2', 'mo,full'),
  r('Then he goes into the choir with fresh, unblessed incense, and incenses the Master of the Order if present, then the brethren in both choirs, beginning with the seniors in the upper stalls, and then the lay brothers; he returns and stands in the middle behind the subdeacon.', 'c', 'ministri-xiii-2', 'full')]}
N['rSa'] = {'la': '', 'en': '', 'strip': 1, 'lines': [
  r('With hands joined he says the Sanctus, signing himself at Benedictus qui venit. At the Sanctus the server rings the bell a few times, then rises and lights the candle for the elevation.', 'ls', ['modus-viii-2', 'varia-vi-7']),
  r('At supplici confessione the deacon with one acolyte (who rings the bell a few times) goes to the Gospel corner and the subdeacon with the other to the Epistle corner; facing one another they say the Sanctus with the priest and sign themselves at Benedictus qui venit. The brethren in choir sign themselves at Benedictus without turning to the altar.', 'mc', 'ministri-xiv-1'),
  r('On Sundays, Simple feasts and above, solemn octaves, the octave day of simple octaves, and the Tuesdays of St Dominic, Thursdays of the Blessed Sacrament, Saturdays of Our Lady and days of saints of the Order, the subdeacon puts on the veil, receives the paten from the deacon, covered with the veil, and holds it raised behind the deacon until after the Pater noster, his left hand under his right arm; the acolytes light the candles for the elevation. On other days the subdeacon does not hold the paten.', 'mc', 'ministri-xiv-2'),
  r('The choir must not draw out the Sanctus, and the priest must go slowly enough that the elevation never comes before the chant has ended.', 'smc', 'ministri-xv-2'),
  r('With one acolyte only (on ferias, feasts of three lessons and within non-solemn octaves), he stands at the right beside the deacon during the Confiteor, the Sanctus and Agnus Dei, and at the genuflexion at the consecration.', 'mc', 'ministri-xx-4', 'one')]}
N['saLow'] = O['saLow']
C = 'canon'
N['canon'] = {'la': O[C]['la'], 'en': O[C]['en'], 'lines': [
  L(C, 0, ref=['modus-ix-1']), L(C, 1),
  r('At Papa the Pope’s own name is said (left out while the See is vacant); at Antistite the name of the Bishop of the diocese (left out if he is dead, or in Rome).', None, 'modus-ix-1'),
  L(C, 2, ref=['modus-ix-2'], r='Commemoration of the living, with hands joined before his breast; after tuarum, his eyes lowered, he remembers for a short while, in his mind only, those whom he wishes to commend to God:'), L(C, 3),
  L(C, 4, ref=['modus-ix-3']), L(C, 5),
  L(C, 6, ref=['modus-ix-3']), L(C, 7),
  r('At Quam oblationem, his left hand on the altar, with the first three fingers of the right he makes three crosses over the whole sacrifice, then one over the Host only at Corpus and one over the chalice only at Sanguis; he bows his head at Jesu Christi.', None, 'modus-ix-4'),
  L(C, 8),
  r('At Qui pridie he wipes the tips of his thumbs and forefingers on the corporal and takes up the Host; at elevatis oculis in caelum he raises his eyes and lowers them at once; at benedixit he signs the Host once. Then, not leaning on the altar but bending a little, secretly, attentively and without pause, he says the words of consecration:', None, ['modus-x-1', 'modus-x-2']),
  L(C, 9),
  L(C, 10, r='Kneeling, he adores the Host; rising, he elevates it as high as he conveniently can, so that those behind can see it, his eyes fixed on it, and lays it on the corporal; he adores it again kneeling. From now until the ablution he keeps thumb and forefinger joined, except to touch the Host.', ref=['modus-x-2']),
  r('Kneeling behind the priest, the server rings the bell at the elevation of the Body and of the Blood, and raises the chasuble.', 'l', 'varia-vi-7'),
  r('At the consecration the deacon (at the priest’s right) and the subdeacon with the paten (at his left) kneel on the top step, an acolyte beside each on a lower step, one ringing the bell, until after the elevation of the chalice. On days with incense the deacon takes the thurible and incenses continuously at the elevation of the Body and of the Blood, then gives it back to be taken to the sacristy.', 'mc', 'ministri-xv-1'),
  r('The bell is rung at the elevation of the Body and of the Blood.', 's', 'varia-vi-7'),
  r('At Simili modo he uncovers the chalice and shakes his fingers lightly over it; at accipiens he takes it in both hands, raises it a little at Item tibi gratias agens, blesses it at benedixit, and at Accipite, et bibite holds it slightly tilted; standing, with head bowed, he says the words of consecration of the Blood:', None, ['modus-x-3', 'modus-x-4']),
  L(C, 11),
  r('Having said the words, he sets the chalice down and adores the Blood kneeling; rising, he elevates the uncovered chalice (its foot not above his head) for the people to adore, and setting it down in its place says:', None, 'modus-x-4'),
  L(C, 12),
  L(C, 13, r='He covers the chalice with the pall and adores again kneeling. Then, his arms extended more than usual, though moderately (in the form of a cross):', ref=['modus-x-4', 'modus-xi-1']),
  r('At Hostiam puram, his left hand on the corporal, he makes three crosses over the whole sacrifice, one over the Host at Panem sanctum and one over the chalice at Calicem salutis.', None, 'modus-xi-1'),
  L(C, 14),
  r('With hands raised and extended in the usual way:', None, 'modus-xi-2'),
  L(C, 15),
  L(C, 16, r='Bowing profoundly, his hands crossed before his breast, the left arm under the right; at ut quotquot he begins to rise, so as to kiss the right side of the corporal at altaris participatione; standing, he blesses the Host at Corpus and the chalice at Sanguinem, and signs himself (not touching himself) at benedictione caelesti:', ref=['modus-xi-2']),
  L(C, 17),
  L(C, 18, r='Commemoration of the dead, with hands joined; at N. N., his eyes on the sacrifice, he calls to mind the dead in his mind only:', ref=['modus-xi-3']),
  L(C, 19),
  L(C, 20, r='Striking his breast lightly with the three last fingers of the right hand, he says the three words Nobis quoque peccatoribus aloud, and continues secretly with hands extended:', ref=['modus-xi-3']),
  L(C, 21),
  r('At sanctificas he signs the whole sacrifice three times; he uncovers the chalice and, after et praestas nobis, genuflects; with the Host he makes three crosses over the chalice at Per ipsum, a fourth before it at Deo Patri and a fifth low before its foot at Spiritus Sancti; he lays the Host down (without showing it to the people), covers the chalice and genuflects.', None, 'modus-xi-4'),
  L(C, 22), L(C, 23), L(C, 24)]}
P = 'pater'
N['pater'] = {'la': O[P]['la'], 'en': O[P]['en'], 'lines': [
  r('His hands are laid on the corporal on either side for Per omnia saecula saeculorum and Oremus; at Pater noster he raises and extends them.', None, 'modus-xii-1'),
  L(P, 0), L(P, 1),
  r('The deacon, with the other ministers, answers in a low voice:', 'mc', 'ministri-xvi-1'),
  L(P, 2), L(P, 3),
  r('He continues in a low voice with hands extended, bowing his head at Maria:', None, 'modus-xii-1'),
  r('After the Pater noster the subdeacon gives the paten to the deacon, who takes it with his bare hand and gives it to the priest before Da propitius pacem, kissing his shoulder (not if the Sacrament is exposed); the acolytes fold the veil and lay it on the Gospel corner.', 'mc', ['ministri-xvi-1', 'ministri-xvi-2']),
  L(P, 4),
  r('At da propitius pacem he signs himself with the paten, kisses it and lays it aside; at et ab omni perturbatione securi he uncovers the chalice and genuflects; holding the Host over the chalice he breaks it in two, beginning Per eumdem; at Qui tecum vivit he breaks off a particle, and holding the parts as if joined says aloud:', None, ['modus-xii-2', 'modus-xii-3']),
  L(P, 6), L(P, 7),
  L(P, 8, r='He makes the sign of the cross three times within the chalice with the particle:', ref=['modus-xii-3']),
  L(P, 9), L(P, 10)]}
N['rAg'] = {'la': '', 'en': '', 'strip': 1, 'lines': [
  r('He says the Agnus Dei aloud, holding the parts of the Host over the chalice.', 'ls', 'modus-xiii-1'),
  r('After Pax Domini the deacon with one acolyte goes to the Gospel corner and the subdeacon with the other to the Epistle corner, and facing one another they say the Agnus Dei with the priest.', 'mc', 'ministri-xvii-1')]}
N['agLow'] = O['agLow']
N['commSimple'] = O['commSimple']; N['commConv'] = O['commConv']
CM = 'communion'
N['communion'] = {'la': O[CM]['la'], 'en': O[CM]['en'], 'lines': [
  L(CM, 0, r='Then he says secretly, letting the particle fall into the chalice:', ref=['modus-xiii-1']), L(CM, 1),
  L(CM, 2, m='ls', ref=['modus-xiii-1', 'varia-iv-1']),
  r('In Masses for the Dead the chalice is not kissed and the peace is not given.', None, 'varia-iv-1', 'req'),
  r('He kisses the lip of the chalice; then the deacon holds out the paten, or the holy image called the Pax, for him to kiss, and he says in a low voice (not in Masses for the Dead, nor in the Triduum before Easter):', 'mc', 'ministri-xvii-1'),
  L(CM, 3),
  L(CM, 4, m='mc', r='The deacon gives the Pax to the subdeacon to kiss, and the subdeacon to the acolytes, who stand in the middle behind him.', ref=['ministri-xvii-1'], **{'if': '!req'}),
  r('On Sundays, and Doubles and above, one acolyte gives the Pax to the cantors (unless the Master of the Order is present), and a cantor to the brethren in order, after the Agnus Dei has been sung; on other days only the ministers receive it. On the great solemnities (Christmas, Easter, the Ascension, Pentecost, Corpus Christi, the Assumption, our holy Father Dominic, All Saints and the like) the subdeacon himself carries it to the choir.', 'c', ['ministri-xvii-2', 'ministri-xvii-3'], '!req'),
  r('The deacon also takes the instrument of peace to the prelate.', 'mc', 'varia-iii-5', 'prel,!req'),
  r('The Master of the Order is present: the acolyte takes the Pax to him (instead of to the cantors), and the brethren receive it after him in order.', 'c', 'ministri-xvii-2', 'mo,!req'),
  L(CM, 5, ref=['modus-xiii-2']), L(CM, 6),
  L(CM, 7, r='His head bowed, holding the chalice in his right hand, he receives the Host from his left, saying (then he covers the chalice, rests a little in meditation, genuflects, and receives the Blood with the particle, saying nothing):', ref=['modus-xiii-2']),
  L(CM, 8),
  r('After the first draught he gathers the particles from the corporal with the paten into the chalice, and consumes them.', None, 'modus-xiii-3'),
  L(CM, 9), L(CM, 10), L(CM, 11), L(CM, 12), L(CM, 13), L(CM, 14),
  r('The server ministers wine for the first ablution and wine and water for the second, carries the book to the Epistle side, and puts out the elevation candle.', 'l', 'varia-vi-8'),
  r('At the Epistle corner the subdeacon pours the wine, and then wine and water. Meanwhile the deacon carries the Missal to the Epistle corner, washes his fingers, folds the corporal and puts it in the burse; the subdeacon, having washed his fingers, takes the chalice, purifies it and covers it; the acolytes put out the elevation candles.', 'mc', 'ministri-xviii-1'),
  L(CM, 15, ref=['modus-xiv-1']),
  L(CM, 16),
  gx(None, 'leaves the middle to go to the Missal for the Communion'),
  L(CM, 17, r='He wipes his fingers and the chalice, covers it and sets it on the corporal; then, bowing to the cross, he goes to the Missal at the Epistle corner and reads the Communion with hands joined:', ref=['modus-xiv-1', 'modus-xiv-2'])]}
N['post'] = {'la': O['post']['la'], 'en': O['post']['en'], 'lines': [
  L('post', 0, ref=['modus-xiv-2'], r='Turning to the people as before the first Collect, he says Dominus vobiscum; at Oremus, his hands joined, he bows his head a little to the cross; then the Postcommunion with hands extended:')] + turn() + [
  r('The deacon raises the chasuble as before.', 'mc', 'ministri-xix-1'),
  L('post', 1), L('post', 2), L('post', 3),
  r('On a Lenten feria, after all the commemorations, the priest says Oremus with head bowed and adds Humiliate capita vestra Deo before the Prayer over the people.', 'ls', 'modus-xiv-3', 'sp'),
  r('On a Lenten feria, after all the commemorations, the priest says Oremus, bowing his head with the ministers, and the deacon sings Humiliate capita vestra Deo; the priest goes on with the Prayer over the people.', 'mc', 'ministri-xix-2', 'sp'),
  r('During the last prayers the subdeacon, an acolyte going before with the cruets, carries the chalice back to the sacristy (without the veil on his shoulders); on returning he takes the book of the Gospels and the other acolyte lights the candles. If there is only one prayer, or the sacristy is far off, he takes the chalice back only after Mass.', 'mc', 'ministri-xix-3')]}
N['postEnd'] = {'la': O['postEnd']['la'], 'en': O['postEnd']['en'], 'lines': [
  r('At Per Dominum nostrum of the last prayer he comes to the middle of the altar; turned to the people, his hands raised and extended, he says Dominus vobiscum, joining them at vobiscum:', None, ['modus-xiv-2', 'modus-xv-1'])] + turn() + [
  L('postEnd', 1), L('postEnd', 2),
  r('Ite missa est is said turned to the people; when the Gloria was not said, Benedicamus Domino is said instead, and Requiescant in pace in Masses for the Dead, both facing the altar.', 'ls', 'modus-xv-1'),
  L('postEnd', 3, r='When the priest turns to say Dominus vobiscum, the deacon turns too and sings Ite missa est (if the Gloria was said); otherwise he does not turn, but sings Benedicamus Domino (or Requiescant in pace) facing the altar with the priest. They stay turned to the community only while Ite missa est is sung, and turn back without going round.', ref=['ministri-xx-1'])]}
E = 'end'
N['end'] = {'la': O[E]['la'], 'en': O[E]['en'], 'lines': [
  L(E, 0, r='Turning back to the altar by the same way, he bows profoundly (even after Benedicamus Domino or Requiescant in pace) and says secretly with hands joined:', ref=['modus-xv-2']),
  L(E, 1),
  L(E, 2, r='At Per Christum he stands and kisses the altar; turned to the people he gives the blessing with the right hand fully extended, the left on his breast, signing them with a single cross:', ref=['modus-xv-2'], **{'if': '!req'}),
  r('At Per Christum he stands and kisses the altar. In Masses for the Dead no blessing is given.', None, ['modus-xv-2', 'varia-iv-1'], 'req'),
  r('Before the Pope (kneeling) or one of the prelates named (bowing his head), he turns as if asking leave to bless, and blesses those present on the side where the prelate is not.', None, 'varia-iii-6', 'prel,!req'),
  r('The ministers bow their heads at the blessing.', 'mc', 'ministri-xx-2', '!req'),
  L(E, 3), L(E, 4),
  r('Completing the circle, he goes to the Gospel corner.', None, 'modus-xv-2', '!sac,!req'),
  r('The Sacrament is in the tabernacle: he turns to bless as at the Dominus vobiscum, by his right, without turning his back to it; he does not complete the circle, but returns the same way to the middle, bows his head before the tabernacle, and goes to the Gospel corner.', None, 'varia-ii-10', 'tab,!req'),
  r('The Sacrament is exposed: he gives the blessing where he said Dominus vobiscum, from the Gospel side of the middle; he does not complete the circle, but returns to the middle, genuflects, and so goes to the Gospel corner.', None, 'varia-ii-7', 'exp,!req'),
  r('The senior acolyte gives the Missal to the deacon and the other the book of the Gospels to the subdeacon; they hold the lighted candles during the last Gospel; the deacon and subdeacon go up to the priest’s left at the Gospel corner to hear it.', 'mc', 'ministri-xx-2'),
  L(E, 5, r='At the Gospel side he signs the altar (or the book) with his thumb at Dominus vobiscum, and his forehead, lips and breast at Initium; he reads it with hands joined, facing the Gospel corner, and genuflects at Et Verbum caro factum est:', ref=['modus-xv-3']),
  L(E, 6), L(E, 7), L(E, 8), L(E, 9), L(E, 10), L(E, 11),
  r('At the end of the Gospel he returns to the middle, folds the corporal into the burse, sets the chalice in the middle with the veil and burse on it, bows to the cross, covers his head with capuce and amice, takes the chalice, and below the lowest step bows profoundly (genuflects if the Sacrament is in the tabernacle; kneels on both knees if it is exposed) and returns to the sacristy, saying the canticle Benedicite.', 'ls', ['modus-xv-4', 'varia-ii-8']),
  r('The server takes the book and puts out the candles in time to lead the priest back to the sacristy; there, prostrate at the priest’s feet, he asks pardon for any fault in his service, helps him unvest kissing his hand, and says Benedictus Deus; the priest answers Pater, et Filius, et Spiritus Sanctus, and he Amen.', 'l', ['varia-vi-10', 'varia-vi-11']),
  r('With a bow or genuflexion as at the entrance, all return to the sacristy in the order they came; the ministers first unvest the priest, then help one another. The acolytes cover the altar and put it in order; on Sundays they carry holy water through the cells and the offices.', 'mc', ['ministri-xx-2', 'ministri-xx-3']),
  r('The Gospel finished, he makes a fitting reverence to the prelate.', None, 'varia-iii-7', 'prel'),
  r('The Sacrament is exposed: the celebrant and ministers kneel on both knees before leaving the altar.', 'mc', 'varia-ii-8', 'exp')]}
N['dismiss'] = O['dismiss']
# m: l = Low, s = Sung, m = Solemn, c = Conventual; the old 'm' (Solemn) lines also hold at a Conventual Mass
for k, s in N.items():
    if k == 'dismiss': continue
    for l in s['lines']:
        if l.get('m') == 'm' and k in ('kyLow',): pass
        if 'm' in l and 'm' in l['m'] and 'c' not in l['m'] and k not in ('rAs',) : l['m'] += 'c'
# the basic mode: the earlier Order of Mass, as it was, with its errors corrected
FIX = {('foot', 21): None,
       ('chalice', 2): 'At a Solemn Mass, after the Epistle, the subdeacon brings the chalice and prepares it before the seated priest; presenting the water he says:',
       ('gospel', 2): 'The deacon takes the book of the Gospels and, bowing before the priest, asks his blessing:',
       ('gospel', 5): 'The deacon goes with the subdeacon, thurifer and acolytes to the lectern at the Gospel side.',
       ('afterGospel', 0): 'The priest (at a Solemn Mass, the subdeacon bringing him the book) kisses the Gospel, saying:',
       ('offertory', 0): 'At a Solemn Mass the deacon hands the chalice to the priest, saying Immola Deo sacrificium laudis, et redde Altissimo vota tua.',
       ('offertory', 6): 'At a Solemn Mass the chalice and the altar are now incensed, and the deacon incenses the priest; the ministers and the choir are incensed at the Preface.',
       ('canon', 10): 'He adores, elevates the Sacred Host, and adores again. The bell is rung at the elevation; at a Solemn Mass the deacon incenses the Host.',
       ('communion', 4): 'At a Solemn Mass the deacon holds out the paten (or the Pax) for the priest to kiss, and gives it to the subdeacon, who gives it to the acolytes and (on Sundays and Doubles) to the choir (not in Masses for the Dead).',
       ('postEnd', 3): 'The deacon sings the dismissal.'}
BASIC = {}
for k, sec in O.items():
    if k == 'dismiss': continue
    out = []
    for i, l in enumerate(sec['lines']):
        l = dict(l)
        if (k, i) in FIX:
            if FIX[(k, i)] is None: continue
            l['r'] = FIX[(k, i)]
        if 'm' in l and 'm' in l['m'] and 'c' not in l['m']: l['m'] += 'c'
        out.append(l)
    BASIC[k] = out
# serialise
def js(v): return json.dumps(v, ensure_ascii=False)
out = ['''/* Ordo Missæ secundum ritum Ordinis Prædicatorum (Missale O.P. 1939).
   Latin after the Missale O.P.; English after the St Dominic Missal (1959) and Divinum Officium.
   Each section is a list of lines: {r: rubric} or {w: speaker, la: Latin, en: English}.
   m limits a line to some forms of Mass: l = Low Mass, s = Sung Mass, m = Solemn Mass, c = Conventual Mass (default: all).
   if limits a line to a circumstance chosen on the Mass page: tab (the Sacrament in the tabernacle on this altar), exp (exposed),
   sac (either), pope, bp (a Cardinal Legate, Patriarch, Archbishop or Bishop in his jurisdiction), prel (either), mo (the Master of the Order), one (one server
   or acolyte), full (two acolytes, thurifer, crossbearer), req (a Mass for the Dead), flect (a day with Flectamus genua), sp (a day
   with a Prayer over the people), adjuva (a Tract with Adjuva nos), veni (Veni Sancte Spiritus), nogl (no Gloria); "!" negates, "," joins.
   ref: the paragraphs of the Missal's rubrics (rubrics.html, data/rubtext.js) behind a direction, opened from it on the Mass page.
   Sections marked strip are directions without a heading, set before a chant of the Proper or the Ordinary.
   Each section has two forms: lines, the basic Order of Mass with its few directions, and adv, the full directions of the Missal's
   Ritus (shown when "Full rubrics" is on); a section without adv is the same in both. */
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
open('/home/claude/dominican-liturgy/data/ordo.js', 'w').write(src)
# check refs
R = json.loads(open('/home/claude/dominican-liturgy/data/rubtext.js').read().split('window.RUBTEXT = ', 1)[1].rstrip().rstrip(';'))
bad = [x for s in N.values() if isinstance(s, dict) and 'lines' in s for l in s['lines'] for x in l.get('ref', []) if x not in R]
print('bad refs', bad)
