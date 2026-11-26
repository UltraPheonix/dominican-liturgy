"""Proprium de Tempore of the 1909 Dominican Breviary -> tempora1909.json.  Stage 1: Advent (vol. 1 pdf 246-283), short
parts only (invitatory, Lauds antiphons of Sundays 'ad Laudes et per Horas', Benedictus/Magnificat antiphons, prayers,
responsory of First Vespers, the O antiphons, the Lauds antiphons of the six ferias before the Vigil). Lessons and Matins
responsories: next stage.  Keys: 'adv<week>-<weekday 0..6>'. Prayers end with their short conclusion as printed."""
import json, os
O = {}
def day(k, **kw): O.setdefault(k, {}).update(kw)
EXC1 = 'Excita, quǽsumus, Dómine, poténtiam tuam, et veni: ut ab imminéntibus peccatórum nostrórum perículis, te mereámur protegénte éripi, te liberánte salvári. Qui vivis.'
EXC2 = 'Excita, Dómine, corda nostra ad præparándas Unigéniti tui vias: ut per ejus advéntum purificátis tibi méntibus servíre mereámur. Qui tecum vivit.'
AUR3 = 'Aurem tuam, quǽsumus, Dómine, précibus nostris accómmoda: et mentis nostræ ténebras grátia tuæ visitatiónis illústra. Qui vivis.'
EXC4 = 'Excita, quǽsumus, Dómine, poténtiam tuam, et veni, et magna nobis virtúte succúrre: ut per auxílium grátiæ tuæ, quod nostra peccáta præpédiunt, indulgéntia tuæ propitiatiónis accéleret. Qui vivis.'
WEEK_OR = {1: EXC1, 2: EXC2, 3: AUR3, 4: EXC4}
REGEM = 'Regem ventúrum Dóminum, * Veníte, adorémus.'; PROPE = 'Prope est jam Dóminus: * Veníte, adorémus.'
# First Vespers of the Sundays (Saturday evening): responsory, Magnificat antiphon (prayer = the Sunday's)
VR1 = {1: ['Missus est Gábriel Ángelus ad Maríam Vírginem desponsátam Joseph, núntians ei verbum: et expavéscit Virgo de lúmine. Ne tímeas, María, invenísti grátiam apud Dóminum: ecce concípies, et páries,', 'Et vocábitur Altíssimi Fílius.',
           'Dabit ei Dóminus Deus sedem David patris ejus, et regnábit in domo Jacob in ætérnum.'],
       2: ['Ecce Dóminus véniet, et omnes Sancti ejus cum eo: et erit in die illa lux magna: et exíbunt de Jerúsalem sicut aqua munda: et regnábit Dóminus in ætérnum', 'Super omnes gentes.',
           'Ecce Dóminus cum virtúte véniet: et regnum in manu ejus, et potéstas, et impérium.'],
       3: ['Qui ventúrus est véniet, et non tardábit: et jam non erit timor in fínibus nostris:', 'Quóniam ipse est Salvátor noster.',
           'Depónet omnes iniquitátes nostras, et projíciet in profúndum maris ómnia peccáta nostra.'],
       4: ['Non auferétur sceptrum de Juda, et dux de fémore ejus, donec véniat qui mitténdus est:', 'Et ipse erit exspectátio géntium.',
           'Pulchrióres sunt óculi ejus vino, et dentes ejus lacte candidióres.']}
MAGN1 = {1: 'Ecce nomen Dómini venit de longínquo, et cláritas ejus replet orbem terrárum.',
         2: 'Veni, Dómine, visitáre nos in pace, ut lætémur coram te corde perfécto.',
         3: 'Ante me non est formátus Deus, et post me non erit: quia mihi curvábitur omne genu, et confitébitur omnis lingua.',
         4: None}   # O antiphon of the day
for w in (1, 2, 3, 4):
    day('adv%d-0' % w, oratio=WEEK_OR[w])
    day('adv%d-6' % (w - 1) if w > 1 else 'pre-adv', vesp_r=VR1[w], magn=MAGN1[w], oratio_vesp=WEEK_OR[w])
day('adv1-0', invit='Ecce venit Rex: * Occurrámus óbviam Salvatóri nostro.',
    laudes=['In illa die stillábunt montes dulcédinem, et colles fluent lac et mel, allelúja.', 'Jucundáre, fília Sion, et exsúlta satis, fília Jerúsalem, allelúja.',
            'Ecce Dóminus véniet, et omnes Sancti ejus cum eo: et erit in die illa lux magna, allelúja.', 'Omnes sitiéntes, veníte ad aquas: quǽrite Dóminum, dum inveníri potest, allelúja.',
            'Ecce véniet Prophéta magnus, et ipse renovábit Jerúsalem, allelúja.'],
    bened='Spíritus Sanctus in te descéndet, María: ne tímeas, habébis in útero Fílium Dei, allelúja.',
    magn='Ne tímeas, María, invenísti grátiam apud Dóminum: ecce concípies, et páries fílium, allelúja.')
day('adv2-0', invit='Rex noster advéniet Christus: * Quem Joánnes prædicávit Agnum esse ventúrum.',
    laudes=['Ecce in núbibus cæli Dóminus véniet cum potestáte magna, allelúja.', 'Urbs fortitúdinis nostræ Sion, Salvátor ponétur in ea murus et antemurále: aperíte portas, quia nobíscum Deus, allelúja.',
            'Ecce apparébit Dóminus, et non mentiétur: si moram fécerit, exspécta eum, quia véniet, et non tardábit, allelúja.',
            'Montes et colles cantábunt coram Deo laudem, et ómnia ligna silvárum plaudent mánibus: quóniam véniet dominátor Dóminus in regnum ætérnum, allelúja, allelúja.',
            'Ecce Dóminus noster cum virtúte véniet, et illuminábit óculos servórum suórum, allelúja.'],
    bened='Joánnes autem, cum audísset in vínculis ópera Christi, mittens duos ex discípulis suis, ait illi: Tu es qui ventúrus es, an álium exspectámus?',
    magn='Ite, dícite Joánni: Cæci vident, et surdi áudiunt: claudi curántur, leprósi mundántur.')
day('adv3-0', invit='Súrgite, vigilémus, veníte, adorémus: * Quia nescítis horam quando véniet Dóminus.',
    laudes=['Véniet Dóminus, et non tardábit, et illuminábit abscóndita tenebrárum, et manifestábit se ad omnes gentes, allelúja.', 'Jerúsalem, gaude gáudio magno, quia véniet tibi Salvátor, allelúja.',
            'Dabo in Sion salútem, et in Jerúsalem glóriam meam, allelúja.', 'Montes et omnes colles humiliabúntur: et erunt prava in dirécta, et áspera in vias planas: veni, Dómine, et noli tardáre, allelúja.',
            'Juste et pie vivámus, exspectántes beátam spem, et advéntum Dómini.'],
    bened='Super sólium David, et super regnum ejus sedébit in ætérnum, allelúja.',
    magn='Beáta es, María, quæ credidísti: perficiéntur in te quæ dicta sunt tibi a Dómino, allelúja.')
day('adv4-0', invit='Ecce jam venit plenitúdo témporis, in quo misit Deus Fílium suum natum de Vírgine, factum sub lege: * Veníte, adorémus.',
    laudes=['Cánite tuba in Sion, quia prope est dies Dómini: ecce véniet ad salvándum nos, allelúja, allelúja.', 'Ecce véniet desiderátus cunctis géntibus: et replébitur glória domus Dómini, allelúja.',
            'Erunt prava in dirécta, et áspera in vias planas: veni, Dómine, et noli tardáre, allelúja.',
            'Dóminus véniet, occúrrite illi, dicéntes: Magnum princípium, et regni ejus non erit finis: Deus, fortis, dominátor, princeps pacis, allelúja, allelúja.',
            'Omnípotens sermo tuus, Dómine, a regálibus sédibus véniet, allelúja.'],
    bened='Ave, María, grátia plena: Dóminus tecum: benedícta tu in muliéribus, allelúja.')
FER = {1: [('Ángelus Dómini nuntiávit Maríæ, et concépit de Spíritu Sancto, allelúja.', 'Jerúsalem, réspice ad oriéntem, et vide, allelúja.'),
           ('Leva, Jerúsalem, óculos, et vide poténtiam Regis: ecce Salvátor venit sólvere te a vínculo.', 'Quǽrite Dóminum, dum inveníri potest: invocáte eum, dum prope est, allelúja.'),
           ('De Sion exíbit lex, et verbum Dómini de Jerúsalem.', 'Véniet fórtior me post me, cujus non sum dignus sólvere corrígiam calceamentórum ejus.'),
           ('Benedícta tu in muliéribus, et benedíctus fructus ventris tui.', 'Exspectábo Dóminum Salvatórem meum, et præstolábor eum, dum prope est, allelúja.'),
           ('Ecce véniet Deus et homo de domo David sedére in throno, allelúja.', 'Ex Ægýpto vocávi Fílium meum: véniet ut salvet pópulum suum.'),
           ('Sion, noli timére: ecce Deus tuus véniet, allelúja.', None)],
       2: [('De cælo véniet dominátor Dóminus, et in manu ejus honor et impérium.', 'Ecce véniet Rex, Dóminus terræ, et ipse áuferet jugum captivitátis nostræ.'),
           ('Super te, Jerúsalem, oriétur Dóminus, et glória ejus in te vidébitur.', 'Vox clamántis in desérto: Paráte viam Dómini, rectas fácite sémitas Dei nostri.'),
           ('Ecce ego mitto Ángelum meum, qui præparábit viam meam ante fáciem tuam.', 'Sion, renovaberis, et vidébis justum tuum, qui ventúrus est in te.'),
           ('Tu es qui ventúrus es, Dómine, quem exspectámus, ut salvum fácias pópulum tuum.', 'Qui post me venit, ante me factus est: cujus non sum dignus calceaménta sólvere.'),
           ('Dícite: Pusillánimes, confortámini: ecce Dóminus Deus noster véniet.', 'Cantáte Dómino cánticum novum: laus ejus ab extrémis terræ.'),
           ('Levábit Dóminus signum in natiónibus, et congregábit dispérsos Israël.', None)],
       3: [('Egrediétur virga de radíce Jesse, et replébitur omnis terra glória Dómini: et vidébit omnis caro salutáre Dei.', 'Eleváre, eleváre, consúrge, Jerúsalem: solve víncula colli tui, captíva fília Sion.'),
           ('Tu, Béthlehem, terra Juda, non eris mínima: ex te enim exiet dux, qui regat pópulum meum Israël.', 'Erúmpant montes jucunditátem, et colles justítiam: quia lux mundi Dóminus cum poténtia véniet.'),
           ('Missus est Gábriel Ángelus ad Maríam Vírginem desponsátam Joseph.', 'Quómodo fiet istud, Ángele Dei, quia virum in concipiéndo non pértuli? Audi, María Virgo Christi: Spíritus Sanctus supervéniet in te, et virtus Altíssimi obumbrábit tibi.'),
           ('Vigiláte ánimo: in próximo est Dóminus Deus noster.', 'Lætámini cum Jerúsalem, et exsultáte in ea, omnes qui dilígitis eam, in ætérnum.'),
           ('Ex quo facta est vox salutatiónis tuæ in áuribus meis, exsultávit in gáudio infans in útero meo, allelúja.', 'Beáta es, María, quæ credidísti: perficiéntur in te quæ dicta sunt tibi a Dómino, allelúja.'),
           ('Omnis vallis implébitur, et omnis mons et collis humiliábitur: et vidébit omnis caro salutáre Dei.', None)],
       4: [('Dicit Dóminus: Pœniténtiam ágite: appropinquávit enim regnum cælórum, allelúja.', None),
           ('Consúrge, consúrge, indúere fortitúdinem, bráchium Dómini.', None),
           ('Ponent Dómino glóriam, et laudem ejus in ínsulis nuntiábunt: quia ecce véniet, et non tardábit.', None),
           ('Consolámini, consolámini, pópule meus, dicit Dóminus Deus vester.', None),
           ('Dies Dómini sicut fur in nocte, ita véniet: et vos estóte paráti, quia qua hora non putátis, Fílius hóminis véniet.', None),
           (None, None)]}
for w, l in FER.items():
    for i, (b, m) in enumerate(l):
        k = 'adv%d-%d' % (w, i + 1)
        if b: day(k, bened=b)
        if m: day(k, magn=m)
        day(k, invit=REGEM)
for i in (3, 5, 6):   # Ember days: own invitatory and own prayer at Lauds (at the other Hours the Sunday's)
    day('adv3-%d' % i, invit=PROPE)
day('adv3-3', oratio_laudes='Festína, quǽsumus, Dómine, ne tardáveris: et auxílium nobis supérnæ virtútis impénde: ut advéntus tui consolatiónibus sublevéntur, qui in tua pietáte confídunt. Qui vivis.')
day('adv3-5', oratio_laudes='Excita, quǽsumus, Dómine, poténtiam tuam, et veni: ut hi, qui in tua pietáte confídunt, ab omni cítius adversitáte liberéntur. Qui vivis.')
day('adv3-6', oratio_laudes='Deus, qui cónspicis, quia ex nostra pravitáte afflígimur: concéde propítius, ut ex tua visitatióne consolémur. Qui vivis.')
# O antiphons at the Magnificat from 17 December (in place of the ferial/Sunday one), no preces or prostrations at Vespers
OANT = {17: 'O Sapiéntia, quæ ex ore Altíssimi prodiísti, attíngens a fine usque ad finem fórtiter, suavitérque dispónens ómnia: veni ad docéndum nos viam prudéntiæ.',
        18: 'O Adonái, et Dux domus Israël, qui Móysi in igne flammæ rubi apparuísti, et ei in Sina legem dedísti: veni ad rediméndum nos in bráchio exténto.',
        19: 'O Radix Jesse, qui stas in signum populórum, super quem continébunt reges os suum, quem gentes deprecabúntur: veni ad liberándum nos, jam noli tardáre.',
        20: 'O Clavis David, et sceptrum domus Israël, qui áperis, et nemo claudit; claudis, et nemo áperit: veni, et educ vinctum de domo cárceris, sedéntem in ténebris et umbra mortis.',
        21: 'O Óriens, splendor lucis ætérnæ, et sol justítiæ: veni, et illúmina sedéntes in ténebris et umbra mortis.',
        22: 'O Rex géntium, et desiderátus eárum, lapísque anguláris, qui facis utráque unum: veni, et salva hóminem, quem de limo formásti.',
        23: 'O Emmánuel, Rex et légifer noster, exspectátio géntium, et Salvátor eárum: veni ad salvándum nos, Dómine Deus noster.'}
# Lauds antiphons of the six ferias before the Vigil of Christmas (with the ferial psalms), by weekday 1..6
SIX = {1: ['Ecce véniet Dóminus, princeps regum terræ: beáti qui paráti sunt occúrrere illi.', 'Cum vénerit Fílius hóminis, putas, invéniet fidem super terram?',
           'Ecce jam venit plenitúdo témporis, in quo misit Deus Fílium suum in terras.', 'Hauriétis aquas in gáudio de fóntibus Salvatóris.', 'Egrediétur Dóminus de loco sancto suo: véniet ut salvet pópulum suum.'],
       2: ['Roráte, cæli, désuper, et nubes pluant justum: aperiátur terra, et gérminet Salvatórem.', 'Emítte Agnum, Dómine, dominatórem terræ, de petra desérti ad montem fíliæ Sion.',
           'Ut cognoscámus, Dómine, in terra viam tuam, in ómnibus géntibus salutáre tuum.', 'Da mercédem, Dómine, sustinéntibus te, ut prophétæ tui fidéles inveniántur.',
           'Lex per Móysen data est: grátia et véritas per Jesum Christum facta est.'],
       3: ['Prophétæ prædicavérunt nasci Salvatórem de Vírgine María.', 'Spíritus Dómini super me: evangelizáre paupéribus misit me.',
           'Annuntiáte pópulis, et dícite: Ecce Deus Salvátor noster véniet.', 'Ecce véniet Dóminus, ut sédeat cum princípibus, et sólium glóriæ téneat.',
           'Propter Sion non tacébo, donec egrediátur ut splendor justus ejus.'],
       4: ['De Sion véniet Dóminus omnípotens, ut salvum fáciat pópulum suum.', 'Convértere, Dómine, aliquántulum, et ne tardes veníre ad servos tuos.',
           'De Sion véniet, qui regnatúrus est, Dóminus, Emmánuel magnum nomen ejus.', 'Ecce Deus meus, et honorábo eum: Deus patris mei, et exaltábo eum.',
           'Deus légifer noster, Dóminus rex noster, ipse véniet, et salvábit nos.'],
       5: ['Constántes estóte: vidébitis auxílium Dómini super vos.', 'Ad te, Dómine, levávi ánimam meam: veni, et éripe me, Dómine: ad te confúgi.',
           'Veni, Dómine, et noli tardáre: reláxa facínora plebis tuæ Israël.', 'Deus a Líbano véniet, et splendor ejus sicut lumen erit.',
           'Ego autem ad Dóminum aspíciam, et exspectábo Deum Salvatórem meum.'],
       6: ['Intuémini quam sit gloriósus iste, qui ingréditur ad salvándos pópulos.', 'Consúrge, consúrge, indúere fortitúdinem, bráchium Dómini.',
           'Eleváre, eleváre, consúrge, Jerúsalem: solve víncula colli tui, captíva fília Sion.',
           'Exspectétur sicut plúvia elóquium Dómini: descéndat super nos sicut ros Deus noster.', 'Parátus esto, Israël, in occúrsum Dómini, quóniam venit.']}
json.dump({'days': O, 'OANT': OANT, 'SIX': SIX, 'PRIME_RV_ADV': 'Qui ventúrus es in mundum.', 'WEEK_OR': WEEK_OR, '_doc': __doc__},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tempora1909.json'), 'w'), ensure_ascii=False, indent=1)
print(len(O), 'days')
