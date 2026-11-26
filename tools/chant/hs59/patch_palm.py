"""Palm Sunday, 1959 view (data/holyweek.js): the distribution and procession chants of the Cantus Gregoriani ad Ordinem
Hebdomadae Sanctae O.P. instauratum (Romae 1959), pp. 5-18, with its rubrics (Latin) and our English. Idempotent."""
import json, os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..','data','holyweek.js')
s=open(P).read()
if 'op59-pueri1' in s: print('already'); raise SystemExit
L=s.split('\n')
def js(d): return '        '+json.dumps(d,ensure_ascii=False)+','
R=lambda la,en=None: {'r': la+(' — '+en if en else '')}
def T(la,en): return {'w':'C','la':la,'en':en}
def G(id,n): return {'g':id,'n':n}
rep='Et repetitur antiphona Púeri Hebræórum.'
REP_EN='And the antiphon Púeri Hebræórum is repeated.'
dist=[
 {'r':'The palms are sprinkled with holy water and distributed by the celebrant, first to the clergy and then to the people.'},
 {'r':'Ramorum benedictióne finíta, cantor, ramum celebránti ófferens, íncipit antíphonam Púeri Hebræórum, tolléntes, et omnes ipsam et álteram, scílicet Púeri Hebræórum vestiménta, a cantóre páriter incipiéndam, prosequúntur, dum ínterim rami a sacrísta distribuúntur. Dum rami distribuúntur, stat chorus contra chorum. Si antíphonæ non suffíciant, cum vérsibus psalmi 23, et respective psalmi 46 et Glória Patri in fine, cantári possunt, ut infra. — When the blessing of the palms is finished, the cantor, offering a palm to the celebrant, begins the antiphon Púeri Hebræórum, tolléntes, and all continue it and the other, Púeri Hebræórum vestiménta, also begun by the cantor, while the palms are distributed by the sacristan; the choir stands side facing side. If the antiphons are not enough, they may be sung with the verses of Psalm 23 and of Psalm 46 respectively, and the Glória Patri at the end, as follows. (Cantus Gregoriani … Hebdomadae Sanctae O.P. instauratum, Rome 1959, pp. 5–8.)'},
 G('op59-pueri1','Antiphona 1 · I b'),
 T('Púeri Hebræórum, tolléntes ramos olivárum, obviavérunt Dómino, clamántes et dicéntes: Hosánna in excélsis.','The Hebrew children, taking up olive branches, met the Lord, crying out and saying: Hosanna in the highest.'),
 G('op59-ps23','Psalmus 23, 1-2 et 7-10'),
 T('Dómini est terra et plenitúdo eius, * orbis terrárum et univérsi qui hábitant in eo.','The earth is the Lord’s and the fulness thereof: * the world, and all they that dwell therein.'),
 T('Quia ipse super mária fundávit eum, * et super flúmina præparávit eum.','For he hath founded it upon the seas; * and hath prepared it upon the rivers.'),
 {'r':rep+' — '+REP_EN},
 T('Attóllite portas, príncipes, vestras, † et elevámini, portæ æternáles, * et introíbit rex glóriæ.','Lift up your gates, O ye princes, and be ye lifted up, O eternal gates: * and the King of Glory shall enter in.'),
 T('Quis est iste rex glóriæ? * Dóminus fortis et potens, Dóminus potens in prœ́lio.','Who is this King of Glory? * the Lord who is strong and mighty: the Lord mighty in battle.'),
 {'r':rep+' — '+REP_EN},
 T('Attóllite portas, príncipes, vestras, † et elevámini, portæ æternáles, * et introíbit rex glóriæ.','Lift up your gates, O ye princes, and be ye lifted up, O eternal gates: * and the King of Glory shall enter in.'),
 T('Quis est iste rex glóriæ? * Dóminus virtútum ipse est rex glóriæ.','Who is this King of Glory? * the Lord of hosts, he is the King of Glory.'),
 {'r':rep+' — '+REP_EN},
 T('Glória Patri, et Fílio, * et Spirítui Sancto.','Glory be to the Father, and to the Son, * and to the Holy Ghost.'),
 T('Sicut erat in princípio et nunc et semper, * et in sǽcula sæculórum. Amen.','As it was in the beginning, is now and ever shall be, * world without end. Amen.'),
 {'r':rep+' — '+REP_EN},
 G('op59-pueri2','Antiphona 2 · I b'),
 T('Púeri Hebræórum vestiménta prosternébant in via, et clamábant dicéntes: Hosánna Fílio David: benedíctus qui venit in nómine Dómini.','The Hebrew children spread their garments in the way, and cried out, saying: Hosanna to the Son of David; blessed is he who comes in the name of the Lord.'),
 G('op59-ps46','Psalmus 46'),
 T('Omnes gentes, pláudite mánibus: * iubiláte Deo in voce exsultatiónis.','O clap your hands, all ye nations: * shout unto God with the voice of joy.'),
 T('Quóniam Dóminus excélsus, terríbilis, * rex magnus super omnem terram.','For the Lord is high, terrible: * a great king over all the earth.'),
 {'r':rep+' — '+REP_EN},
 T('Subiécit pópulos nobis * et gentes sub pédibus nostris.','He hath subdued the people under us; * and the nations under our feet.'),
 T('Elégit nobis hereditátem suam: * spéciem Iacob, quam diléxit.','He hath chosen for us his inheritance, * the beauty of Jacob which he hath loved.'),
 {'r':rep+' — '+REP_EN},
 T('Ascéndit Deus in iúbilo, * et Dóminus in voce tubæ.','God is ascended with jubilee, * and the Lord with the sound of trumpet.'),
 T('Psállite Deo nostro, psállite: * psállite regi nostro, psállite.','Sing praises to our God, sing ye: * sing praises to our king, sing ye.'),
 {'r':rep+' — '+REP_EN},
 T('Quóniam rex omnis terræ Deus: * psállite sapiénter.','For God is the king of all the earth: * sing ye wisely.'),
 T('Regnábit Deus super gentes: * Deus sedet super sedem sanctam suam.','God shall reign over the nations: * God sitteth on his holy throne.'),
 {'r':rep+' — '+REP_EN},
 T('Príncipes populórum congregáti sunt cum Deo Abraham, * quóniam dii fortes terræ veheménter eleváti sunt.','The princes of the people are gathered together with the God of Abraham: * for the strong gods of the earth are exceedingly exalted.'),
 {'r':rep+' — '+REP_EN},
 T('Glória Patri, et Fílio, * et Spirítui Sancto.','Glory be to the Father, and to the Son, * and to the Holy Ghost.'),
 T('Sicut erat in princípio et nunc et semper, * et in sǽcula sæculórum. Amen.','As it was in the beginning, is now and ever shall be, * world without end. Amen.'),
 {'r':rep+' — '+REP_EN},
 {'r':'Quæ si non suffíciant, repetántur quoúsque distribútio ramórum finiátur; si autem finiátur prius, cláuditur cum Glória Patri, et repétitur antíphona. — If these are not enough, they are repeated until the distribution of the palms is finished; if it is finished sooner, they end with the Glória Patri and the antiphon is repeated.'},
]
ocr='Et repetitur antiphona Omnes colláudant. — And the antiphon Omnes colláudant is repeated.'
proc=[
 {'r':'Then follows the procession. Cantóribus inchoántibus antíphonam Occúrrunt, procéssio egréditur. Progrediénte processióne cantántur antíphonæ, hymni et psalmi qui infra indicántur, omnes vel áliqui, pro opportunitáte. — As the cantors begin the antiphon Occúrrunt, the procession goes out. As it goes, the antiphons, hymns and psalms given below are sung, all or some of them, as is convenient. (Cantus Gregoriani … 1959, pp. 9–18; the St Dominic Missal prints here the older chants Cum appropinquáret and Collegérunt.)'},
 G('op59-occurrunt','Antiphona 1 · VIII'),
 T('Occúrrunt turbæ cum flóribus et palmis Redemptóri óbviam, et victóri triumphánti digna dant obséquia: Fílium Dei ore gentes prædicant, et in laudem Christi voces tonant per núbila: Hosánna.','The crowds go out with flowers and palms to meet the Redeemer, and pay fitting homage to the triumphant victor: the nations proclaim the Son of God, and their voices thunder through the clouds in praise of Christ: Hosanna.'),
 G('op59-cumangelis','Antiphona 2 · VII'),
 T('Cum ángelis et púeris fidéles inveniámur, triumphatóri mortis clamántes: Hosánna in excélsis.','With the angels and the children may we be found faithful, crying out to the conqueror of death: Hosanna in the highest.'),
 G('op59-turbamulta','Antiphona 3 · IV'),
 T('Turba multa, quæ convénerat ad diem festum, clamábat Dómino: Benedíctus qui venit in nómine Dómini: Hosánna in excélsis.','A great crowd that had come together for the feast cried out to the Lord: Blessed is he who comes in the name of the Lord: Hosanna in the highest.'),
 G('op59-coeperunt','Antiphona 4 · I'),
 T('Cœpérunt omnes turbæ descendéntium gaudéntes laudáre Deum voce magna super ómnibus quas víderant virtútibus, dicéntes: Benedíctus, qui venit Rex in nómine Dómini; pax in cælo, et glória in excélsis.','The whole multitude of those coming down began with joy to praise God with a loud voice for all the mighty works they had seen, saying: Blessed is the King who comes in the name of the Lord; peace in heaven, and glory in the highest.'),
 {'r':'Hymnus ad Christum Regem. Pópulus, si fíeri potest, post unumquémque versum hymni, versum Glória, laus cum choro repetit. — Hymn to Christ the King. The people, if possible, repeat the verse Glória, laus with the choir after each verse of the hymn.'},
 {'r':'Cantores: — The cantors:'},
 G('op13-glorialaus','Glória, laus · I (the same melody as in the Processionarium O.P. 1913)'),
 T('Glória, laus et honor tibi sit, Rex Christe, Redémptor, cui pueríle decus prompsit Hosánna pium.','Glory, praise and honour be to thee, Christ, King and Redeemer, to whom the glory of children sang a loving Hosanna.'),
 {'r':'Chorus cum pópulo: Glória, laus. Cantores: — The choir with the people: Glória, laus. The cantors:'},
 G('op59-glorialaus-v1','℣. 1'),
 T('Israël es tu Rex, Davídis et ínclita proles, nómine qui in Dómini, Rex benedícte, venis.','Thou art the King of Israel, David’s glorious offspring, the blessed King who comes in the name of the Lord.'),
 {'r':'Chorus cum pópulo: Glória, laus. Cantores: — The choir with the people: Glória, laus. The cantors:'},
 G('op59-glorialaus-v2','℣. 2'),
 T('Cœtus in excélsis te laudat cǽlicus omnis, et mortális homo et cuncta creáta simul.','The whole company on high praises thee, and mortal man, and all creation together.'),
 {'r':'Chorus cum pópulo: Glória, laus. Cantores: — The choir with the people: Glória, laus. The cantors:'},
 G('op59-glorialaus-v3','℣. 3'),
 T('Plebs Hebrǽa tibi cum palmis óbvia venit; cum prece, voto, hymnis ádsumus, ecce, tibi.','The Hebrew people came to meet thee with palms; behold, we are here before thee with prayer, vow and hymns.'),
 {'r':'Chorus cum pópulo: Glória, laus. — The choir with the people: Glória, laus.'},
 G('op59-omnescoll','Antiphona 5 · VIII a'),
 T('Omnes colláudant nomen tuum, et dicunt: Benedíctus qui venit in nómine Dómini: Hosánna in excélsis.','All praise thy name and say: Blessed is he who comes in the name of the Lord: Hosanna in the highest.'),
 {'r':'Hæc antíphona post psalmum 147 vel post binos versus eiúsdem psalmi repéti potest. — This antiphon may be repeated after Psalm 147, or after every two verses of it.'},
 G('op59-ps147','Psalmus 147'),
 T('Lauda, Ierúsalem, Dóminum: * lauda Deum tuum, Sion.','Praise the Lord, O Jerusalem: * praise thy God, O Sion.'),
 T('2. Quóniam confortávit seras portárum tuárum: * benedíxit fíliis tuis in te.','Because he hath strengthened the bolts of thy gates, * he hath blessed thy children within thee.'),
 T('3. Qui pósuit fines tuos pacem: * et ádipe fruménti sátiat te.','Who hath placed peace in thy borders: * and filleth thee with the fat of corn.'),
 T('4. Qui emíttit elóquium suum terræ: * velóciter currit sermo eius.','Who sendeth forth his speech to the earth: * his word runneth swiftly.'),
 T('5. Qui dat nivem sicut lanam: * nébulam sicut cínerem spargit.','Who giveth snow like wool: * scattereth mists like ashes.'),
 T('6. Mittit crystállum suam sicut buccéllas: * ante fáciem frígoris eius quis sustinébit?','He sendeth his crystal like morsels: * who shall stand before the face of his cold?'),
 T('7. Emíttet verbum suum et liquefáciet ea: * flabit spíritus eius et fluent aquæ.','He shall send out his word, and shall melt them: * his wind shall blow, and the waters shall run.'),
 T('8. Qui annúntiat verbum suum Iacob: * iustítias et iudícia sua Israël.','Who declareth his word to Jacob: * his justices and his judgments to Israel.'),
 T('9. Non fecit táliter omni natióni: * et iudícia sua non manifestávit eis.','He hath not done in like manner to every nation: * and his judgments he hath not made manifest to them.'),
 T('10. Glória Patri, et Fílio, * et Spirítui Sancto.','Glory be to the Father, and to the Son, * and to the Holy Ghost.'),
 T('11. Sicut erat in princípio et nunc et semper, * et in sǽcula sæculórum. Amen.','As it was in the beginning, is now and ever shall be, * world without end. Amen.'),
 {'r':ocr},
 G('op59-fulgentibus','Antiphona 6 · VIII'),
 T('Fulgéntibus palmis prostérnimur adveniénti Dómino: huic omnes occurrámus cum hymnis et cánticis, glorificántes et dicéntes: Benedíctus Dóminus.','With shining palms we bow down before the Lord as he comes: let us all go out to meet him with hymns and songs, glorifying him and saying: Blessed be the Lord.'),
 {'r':'Nihil impédit quóminus cantétur a fidélibus hymnus Christus vincit, vel álius cantus in honórem Christi Regis. — Nothing prevents the faithful from singing the hymn Christus vincit, or another song in honour of Christ the King.'},
 {'r':'Antiphona 7. Antíphona Ave, Rex, si fíeri potest, cantátur ante óstium apértum ecclésiæ, et in eius inceptióne ab ómnibus fit adorátio crucis, ut séquitur. Cruciferárius et ceroferárii, stantes ante óstium apértum ecclésiæ, vultus vertunt ad altáre, imágine tamen Crucifíxi versa ad convéntum et pópulum. Cantóres genua flecténdo incípiunt Ave, et tunc omnes (præter cruciferárium et ceroferários) versis vúltibus ad crucem genua flectunt et antíphonam prosequúntur. Ad verba quem prophétæ omnes se érigunt, et stant versi ad crucem usque ad finem antíphonæ. — The antiphon Ave, Rex is sung, if possible, before the open door of the church, and at its beginning all adore the cross: the cross-bearer and candle-bearers, standing before the open door, face the altar, the image of the Crucified being turned towards the community and the people. The cantors, kneeling, begin Ave, and then all (except the cross-bearer and candle-bearers) kneel facing the cross and continue the antiphon. At the words quem prophétæ all rise and stand facing the cross until the end of the antiphon.'},
 G('op13-averex','Antiphona 7 · II (as in the Processionarium O.P. 1913)'),
 T('Ave, Rex noster, Fili David, Redémptor mundi, (Omnes surgunt) quem prophétæ prædixérunt Salvatórem dómui Israël esse ventúrum. Te enim ad salutárem víctimam Pater misit in mundum, quem exspectábant omnes Sancti ab orígine mundi. Et nunc: Hosánna Fílio David: Benedíctus qui venit in nómine Dómini: Hosánna in excélsis.','Hail, our King, Son of David, Redeemer of the world, (all rise) whom the prophets foretold as the Saviour who was to come to the house of Israel. For the Father sent thee into the world as the saving victim, thou whom all the Saints awaited from the beginning of the world. And now: Hosanna to the Son of David: blessed is he who comes in the name of the Lord: Hosanna in the highest.'),
 {'r':'Antíphona prædícta finíta, cantóribus incipiéntibus responsórium Ingrediénte, procéssio ecclésiam ingréditur, et omnes responsórium prosequúntur. Finíto responsório cantóres cantant versum Cumque audíssent. — When this antiphon is finished, the cantors begin the responsory Ingrediénte, the procession enters the church, and all continue the responsory. When it is finished the cantors sing the verse Cumque audíssent.'},
 G('op13-ingrediente','Responsorium · II (as in the Processionarium O.P. 1913)'),
 T('℟. Ingrediénte Dómino in sanctam civitátem, Hebræórum púeri resurrectiónem vitæ pronuntiántes, * Cum ramis palmárum: Hosánna, clamábant, in excélsis. ℣. Cumque audíssent quia venit Iesus Ierosólymam, exiérunt óbviam ei. * Cum ramis.','℟. As the Lord entered the holy city, the Hebrew children, proclaiming the resurrection of life, * with branches of palms cried out: Hosanna in the highest. ℣. When they had heard that Jesus was coming to Jerusalem, they went out to meet him. * With branches.'),
 {'r':'Cum convéntus chorum intrat, sínguli vadunt ad sedes suas, et qui aquam portávit ad sacrístiam revértitur. Ceroferárii sistunt ante gradus altáris hinc et inde. Cruciferárius, si crucem altáris in processióne detúlerit, eam statim suo loco repónit, ubi usque post Completórium discoopérta remánet; secus eam depónit iuxta credéntiam, ubi erat prius. Celebrans, cum ad altáre advénit, facta eídem débita reveréntia, cum minístris sacris ascéndit et se vertit ad pópulum. Finíto responsório cum versu et resumptióne, ceroferárii, cantóre eis deferénte, vel ipsi cantóres, dicunt: — As the community enters the choir, each goes to his seat, and the one who carried the water returns to the sacristy. The candle-bearers stand before the altar steps on either side. The cross-bearer, if he carried the altar cross in the procession, puts it back at once in its place, where it remains uncovered until after Compline; otherwise he puts it by the credence, where it was before. The celebrant, coming to the altar and making the due reverence, goes up with the sacred ministers and turns to the people. When the responsory with its verse and repetition is finished, the candle-bearers (the cantor bringing it to them), or the cantors themselves, say:'},
 G('op13-deoreleonis','℣. De ore leónis (tone of the Processionarium O.P. 1913, p. 33)'),
 {'w':'P','la':'De ore leónis líbera me, Dómine.','en':'From the lion’s mouth deliver me, O Lord.'},
 {'w':'S','la':'Et a córnibus unicórnium humilitátem meam.','en':'And my lowliness from the horns of the unicorns.'},
 {'r':'Deinde, diácono librum tenénte, célebrans, mánibus iunctis, absque Dóminus vobíscum, præmísso Orémus, dicit oratiónem ad compléndam processiónem eo tono quo dícitur ad Horas. — Then, the deacon holding the book, the celebrant with joined hands, without Dóminus vobíscum but first saying Orémus, says the prayer to end the procession in the tone used at the Hours.'},
]
i16=next(i for i,l in enumerate(L) if 'The palms are sprinkled with holy water' in l)
i25=next(i for i,l in enumerate(L) if 'Then follows the procession' in l)
i39=next(i for i,l in enumerate(L) if 'qui humáno géneri ad imitándum' in l and i>i25)
# keep the Oration line (i39) and its Amen (i39+1); replace the procession lines i25..i39-1
L=L[:i25]+[js(d) for d in proc]+L[i39:]
L=L[:i16]+[js(d) for d in dist]+L[i16+1:]
open(P,'w').write('\n'.join(L))
print('ok')
