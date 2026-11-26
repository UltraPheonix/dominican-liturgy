from en_common import *
ECOLL_DOC="O God, who gave blessed %s to Your people as a minister of eternal salvation, grant, we beseech You, that we may deserve to have him as our intercessor in heaven whom we had as the teacher of life on earth"
SE_OMN="Almighty and everlasting God, through the intercession of blessed {n}, Your {t}, make the gifts offered to Your majesty avail us unto everlasting salvation"
PC_SACR="Receiving the sacraments of our salvation, grant, we beseech You, almighty God, that the prayer of blessed {n}, Your {t}, may help us everywhere, in whose veneration we have offered these gifts to Your majesty"
F={};EN={}
F['Adv2']={'p':'4-5','or':'Excita Dómine corda nostra ad præparándas Unigéniti tui vias; ut per ejus advéntum, purificátis tibi méntibus servíre mereámur: Qui tecum.',
 'se':'Placáre, quǽsumus Dómine, humilitátis nostræ précibus, et hóstiis: et ubi nulla súppetunt suffrágia meritórum, tuis nobis succúrre præsídiis. Per Dóminum.',
 'pc':'Repléti cibo spiritális alimóniæ, súpplices te Dómine deprecámur: ut hujus participatióne mystérii dóceas nos terréna despícere; et amáre cæléstia: Per Dóminum.'}
F['Epi1']={'p':'','or':'Dómine Jesu Christe, qui Maríæ et Joseph súbditus, domésticam vitam ineffabílibus virtútibus consecrásti: fac nos, utriúsque auxílio, Famíliæ sanctæ tuæ exémplis ínstrui; et consórtium cónsequi sempitérnum: Qui vivis.',
 'se':'Placatiónis hóstiam offérimus tibi, Dómine, supplíciter deprecántes: ut, per intercessiónem Deíparæ Vírginis cum beáto Joseph, famílias nostras in pace et grátia tua fírmiter constítuas. Per eúmdem Dóminum.',
 'pc':'Quos cæléstibus réficis sacraméntis, fac, Dómine Jesu, sanctæ Famíliæ tuæ exémpla júgiter imitári; ut, in hora mortis nostræ, occurrénte gloriósa Vírgine Matre tua cum beáto Joseph, per te in ætérna tabernácula récipi mereámur: Qui vivis.'}
F['Jan1']={'p':'','or':'Deus, qui nobis nati Salvatóris diem celebráre concédis octávum: fac nos, quǽsumus, ejus perpétua Divinitáte muníri; cujus sumus carnáli commércio reparáti: Qui tecum vivit.',
 'se':'Præsta, quǽsumus Dómine, ut per hæc múnera, quæ Dómini nostri Jesu Christi arcánæ Nativitátis mystério gérimus, purificátæ mentis intelligéntiam consequámur. Per eúmdem Dóminum.',
 'pc':'Præsta, quǽsumus Dómine: ut quod Salvatóris nostri iteráta festivitáte percépimus; perpétuæ nobis redemptiónis cónferat medicínam: Per eúmdem Dóminum.'}
EN['Jan1']={'or':'O God, who grant us to keep the eighth day from the birth of our Saviour, make us, we beseech You, to be defended by His everlasting Godhead, by whose fellowship in our flesh we have been restored',
 'se':'Grant, we beseech You, O Lord, that through these gifts which we offer in the mystery of the hidden Nativity of our Lord Jesus Christ, we may obtain the understanding of a purified mind',
 'pc':'Grant, we beseech You, O Lord, that what we have received in the renewed feast of our Saviour may bring us the healing of everlasting redemption'}
F['Pent23']={'p':'','or':'Absólve, quǽsumus Dómine, tuórum delícta populórum: ut a peccatórum nostrórum néxibus, quæ pro nostra fragilitáte contráximus; tua benignitáte liberémur: Per Dóminum.',
 'se':'Pro nostræ servitútis augménto, sacrifícium tibi, Dómine, laudis offérimus: ut quod immé­ritis contulísti, propítius exsequáris. Per Dóminum.'.replace('­',''),
 'pc':'Quǽsumus omnípotens Deus: ut quos divína tríbuis participatióne gaudére; humánis non sinas subjacére perículis: Per Dóminum.'}
F['G502_3']={'p':'478-479 (In Vigilia SS. Petri et Pauli, 28 Jun.)','or':'Præsta, quǽsumus omnípotens Deus: ut nullis nos permíttas perturbatiónibus cóncuti; quos in Apostólicæ confessiónis petra solidásti: Per Dóminum.',
 'se':'Munus pópuli tui, quǽsumus Dómine, Apostólica intercessióne sanctífica, nosque a peccatórum nostrórum máculis emúnda. Per Dóminum.',
 'pc':'Quos cælésti, Dómine, aliménto satiásti; Apostólicis intercessiónibus ab omni adversitáte custódi: Per Dóminum.'}
EN['G502_3']={'or':'Grant, we beseech You, almighty God, that You suffer not to be shaken by any disturbances us whom You have set firm on the rock of the Apostolic confession',
 'se':'Sanctify, we beseech You, O Lord, the gift of Your people by the intercession of the Apostles, and cleanse us from the stains of our sins',
 'pc':'Guard from all adversity, by the intercession of the Apostles, O Lord, those whom You have filled with heavenly food'}
F['ChristusRex']={'p':'604-605 (Dominica ultima Octobris)','or':'Omnípotens sempitérne Deus, qui in dilécto Fílio tuo, universórum Rege, ómnia instauráre voluísti: concéde propítius ut cunctæ famíliæ Géntium, peccáti vúlnere disgregátæ; ejus suavíssimo subdántur império: Qui tecum.',
 'se':'Hóstiam tibi, Dómine, humánæ reconciliatiónis offérimus: præsta, quǽsumus; ut Quem sacrifíciis præséntibus immolámus, Ipse cunctis Géntibus unitátis et pacis dona concédat, Jesus Christus Fílius tuus Dóminus noster: Qui tecum.',
 'pc':'Immortalitátis alimóniam consecúti, quǽsumus, Dómine: ut, qui sub Christi Regis vexíllis militáre gloriámur, cum Ipso, in cælésti sede, júgiter regnáre possímus: Qui tecum.'}
F['G491']={'p':'470-471 (SS. Gervasius et Protasius, 19 Jun.)','or':'Deus, qui nos ánnua sanctórum Mártyrum tuórum Gervásii et Protásii solemnitáte lætíficas: concéde propítius, ut quorum gaudémus méritis; accendámur exémplis: Per Dóminum.',
 'se':'Múnera tibi, Dómine, dicáta sanctífica: et intercedéntibus sanctis Martýribus tuis Gervásio et Protásio, per éadem nos placátus inténde. Per Dóminum.',
 'pc':'Salutáris tui, Dómine, múnere satiáti, súpplices exorámus: ut cujus lætámur gustu; intercedéntibus sanctis Martýribus tuis Gervásio et Protásio, renovémur efféctu: Per Dóminum.'}
F['C7s']={'p':'9*-10* (Unius Martyris non Pontificis)','or':'Adésto Dómine supplicatiónibus nostris: ut qui ex iniquitáte nostra reos nos esse cognóscimus; beáti N. Mártyris tui intercessióne liberémur: Per Dóminum.',
 'se':'Munéribus nostris, quǽsumus Dómine, precibúsque suscéptis: intercedénte beáto N. Mártyre tuo, et cæléstibus nos munda mystériis, et cleménter exáudi. Per Dóminum.',
 'pc':'Quǽsumus omnípotens Deus: ut qui cæléstia aliménta percépimus; intercedénte beáto N. Mártyre tuo, per hæc contra ómnia advérsa muniámur: Per Dóminum.'}
EN['C7s']={'or':'Hearken, O Lord, to our supplications, that we who know ourselves to be guilty by our iniquity may be delivered by the intercession of blessed N., Your martyr',
 'se':'Having received our gifts and prayers, we beseech You, O Lord, that by the intercession of blessed N., Your martyr, You would both cleanse us by heavenly mysteries and mercifully hear us',
 'pc':'We beseech You, almighty God, that we who have received heavenly food may, by the intercession of blessed N., Your martyr, be thereby defended against all adversity'}
F['C11s']={'p':'4*-5* (Unius Martyris Pontificis, alia Missa)','or':'Da, quǽsumus omnípotens Deus: ut qui beáti N. Mártyris tui atque Pontíficis solémnia cólimus; ejus apud te intercessiónibus adjuvémur: Per Dóminum.',
 'se':'Hæc hóstia, quǽsumus Dómine, emúndet nostra delícta: et ad sacrifícium celebrándum, subditórum tibi córpora mentésque sanctíficet. Per Dóminum.',
 'pc':'Refécti participatióne múneris sacri, quǽsumus Dómine Deus noster: ut cujus exséquimur cultum; intercedénte beáto N. Mártyre tuo atque Pontífice, sentiámus efféctum: Per Dóminum.'}
EN['C11s']={'or':'Grant, we beseech You, almighty God, that we who keep the feast of blessed N., Your martyr and bishop, may be helped by his intercession with You',
 'se':'May this sacrifice, we beseech You, O Lord, cleanse us from our sins, and sanctify the bodies and minds of Your servants for the celebration of the sacrifice',
 'pc':'Refreshed by partaking of the sacred gift, we beseech You, O Lord our God, that, by the intercession of blessed N., Your martyr and bishop, we may feel the effect of the rite we perform'}
F['C18s']={'p':'10*-11* (Unius Martyris non Pontificis, alia Missa)','or':'Præsta, quǽsumus omnípotens Deus: ut qui beáti N. Mártyris tui natalítia cólimus; a cunctis malis imminéntibus ejus intercessióne liberémur: Per Dóminum.',
 'se':'Hóstias tibi, Dómine, beáti N. Mártyris tui dicátas méritis, benígnus assúme: et ad perpétuum nobis tríbue proveníre subsídium. Per Dóminum.',
 'pc':'Sumptis, Dómine, sacraméntis: quǽsumus, ut intercedénte beáto N. Mártyre tuo; supplicatiónes nostras placátus inténdas: Per Dóminum.'}
EN['C18s']={'or':'Grant, we beseech You, almighty God, that we who keep the birthday of blessed N., Your martyr, may by his intercession be delivered from all threatening evils',
 'se':'Graciously accept, O Lord, the sacrifices dedicated to You by the merits of blessed N., Your martyr, and grant that they may avail us for everlasting help',
 'pc':'Having received the sacraments, O Lord, we beseech You that, by the intercession of blessed N., Your martyr, You may graciously hearken to our supplications'}
F['C21s']={'p':'12*-13* (Plurimorum Martyrum)','or':'Præsta, quǽsumus omnípotens Deus: ut qui gloriósos Mártyres fortes in sua confessióne cognóvimus; pios apud te in nostra intercessióne sentiámus: Per Dóminum.',
 'se':'Benedíctio tua Dómine larga descéndat: quæ et múnera nostra, deprecántibus sanctis Martýribus tuis, tibi reddat accépta, et nobis sacraméntum redemptiónis effíciat. Per Dóminum.',
 'pc':'Cæléstibus refécti sacraméntis et gáudiis, súpplices te Dómine deprecámur: ut quorum gloriámur triúmphis; protegámur auxíliis: Per Dóminum.'}
EN['C21s']={'or':'Grant, we beseech You, almighty God, that we who have known the glorious martyrs to be steadfast in their confession may feel them to be loving intercessors for us with You',
 'se':'May Your blessing, O Lord, come down abundantly, that, Your holy martyrs pleading, it may make our gifts acceptable to You and make for us the sacrament of redemption',
 'pc':'Refreshed with heavenly sacraments and joys, we humbly pray You, O Lord, that we may be protected by the help of those in whose triumphs we glory'}
F['G491b']=None
F['C30s']={'p':'18*-19* (Confessoris Pontificis)','or':'Da, quǽsumus omnípotens Deus: ut beáti N. Confessóris tui atque Pontíficis veneránda solémnitas; et devotiónem nobis áugeat, et salútem: Per Dóminum.',
 'se':'Sancti tui, quǽsumus Dómine, nos ubíque lætíficent: ut dum eórum mérita recólimus, patrocínia sentiámus. Per Dóminum.',
 'pc':'Præsta, quǽsumus omnípotens Deus: ut de percéptis munéribus grátias exhibéntes; intercedénte beáto N. Confessóre tuo atque Pontífice, benefícia potióra sumámus: Per Dóminum.'}
EN['C30s']={'or':'Grant, we beseech You, almighty God, that the venerable feast of blessed N., Your confessor and bishop, may increase in us both devotion and salvation',
 'se':'May Your saints, we beseech You, O Lord, everywhere gladden us, that while we recall their merits we may feel their protection',
 'pc':'Grant, we beseech You, almighty God, that, giving thanks for the gifts received, we may, by the intercession of blessed N., Your confessor and bishop, receive still greater benefits'}
del F['G491b']
F['C32s']={'p':'19*-20* (Confessoris Pontificis, alia Missa)','or':'Exáudi, quǽsumus Dómine, preces nostras, quas in beáti N. Confessóris tui atque Pontíficis solemnitáte deférimus: ut qui tibi digne méruit famulári; ejus intercedéntibus méritis, ab ómnibus nos absólvas peccátis: Per Dóminum.',
 'se':'Accépta sit in conspéctu tuo Dómine nostra devótio: ut ejus nobis fiat supplicatióne salutáris, pro cujus solemnitáte defértur. Per Dóminum.',
 'pc':'Da, quǽsumus Dómine, fidélibus tuis, Sanctórum tuórum semper veneratióne lætári; et eórum perpétua supplicatióne muníri: Per Dóminum.'}
EN['C32s']={'or':'Hear, we beseech You, O Lord, the prayers which we offer on the feast of blessed N., Your confessor and bishop, that by the merits and intercession of him who was found worthy to serve You, You may absolve us from all our sins',
 'se':'May our devotion be acceptable in Your sight, O Lord, and may it become saving for us through the supplication of him on whose feast it is offered',
 'pc':'Grant, we beseech You, O Lord, to Your faithful ever to rejoice in the veneration of Your saints and to be defended by their unceasing intercession'}
F['C35s']={'p':'20*-21* (Doctoris)','or':'Deus, qui pópulo tuo ætérnæ salútis beátum N. minístrum tribuísti: præsta quǽsumus, ut quem doctórem vitæ habúimus in terris; intercessórem habére mereámur in cælis: Per Dóminum.',
 'se':'Omnípotens sempitérne Deus, múnera tuæ majestáti obláta, per intercessiónem beáti N. Confessóris tui atque Doctóris, ad perpétuam nobis fac proveníre salútem. Per Dóminum.',
 'pc':'Sacraménta salútis nostræ suscipiéntes, concéde, quǽsumus omnípotens Deus: ut beáti N. Confessóris tui atque Doctóris nos ubíque orátio ádjuvet; in cujus veneratióne hæc tuæ obtúlimus majestáti: Per Dóminum.'}
EN['C35s']={'or':ECOLL_DOC%'N.','se':SE_OMN.format(n='N.',t='confessor and doctor'),'pc':PC_SACR.format(n='N.',t='confessor and doctor')}
F['C42s']={'p':'23*-24* (Confessoris non Pontificis, alia Missa)','or':'Adésto Dómine supplicatiónibus nostris, quas in beáti N. Confessóris tui solemnitáte deférimus: ut qui nostræ justítiæ fidúciam non habémus; ejus, qui tibi plácuit, précibus adjuvémur: Per Dóminum.',
 'se':'Præsta nobis, quǽsumus omnípotens Deus, ut nostræ humilitátis oblátio, et pro tuórum tibi grata sit honóre Sanctórum, et nos córpore páriter et mente puríficet. Per Dóminum.',
 'pc':'Quǽsumus omnípotens Deus: ut qui cæléstia aliménta percépimus; intercedénte beáto N. Confessóre tuo, per hæc contra ómnia advérsa muniámur: Per Dóminum.'}
EN['C42s']={'or':'Hearken, O Lord, to the prayers which we offer on the feast of blessed N., Your confessor, that we who have no confidence in our own righteousness may be helped by the prayers of him who pleased You',
 'se':SE_PRAESTA,'pc':PC_QUAESUMUS.format(n='N.')}
F['C45s']={'p':'27*-28* (Virginis et Martyris)','or':'Indulgéntiam nobis, quǽsumus Dómine, beáta N. Virgo et Martyr implóret: quæ tibi grata semper éxstitit; et mérito castitátis, et tuæ professióne virtútis: Per Dóminum.',
 'se':'Súscipe Dómine múnera, quæ in beátæ N. Vírginis et Mártyris tuæ solemnitáte deférimus: cujus nos confídimus patrocínio liberári. Per Dóminum.',
 'pc':'Auxiliéntur nobis, Dómine, sumpta mystéria; et intercedénte beáta N. Vírgine et Mártyre tua, sempitérna protectióne confírment: Per Dóminum.'}
EN['C45s']={'or':'May blessed N., virgin and martyr, we beseech You, O Lord, implore pardon for us, she who was ever pleasing to You both by the merit of her chastity and by the confession of Your power',
 'se':'Receive, O Lord, the gifts we bring on the feast of blessed N., Your virgin and martyr, by whose patronage we trust to be delivered',
 'pc':'May the mysteries we have received help us, O Lord, and, through the intercession of blessed N., Your virgin and martyr, strengthen us with everlasting protection'}
F['C48s']={'p':'29*-30* (Virginis et Martyris, alia Missa)','or':'Omnípotens sempitérne Deus, qui infírma mundi éligis, ut fórtia quæque confúndas: concéde propítius, ut qui beátæ N. Vírginis et Mártyris tuæ solémnia cólimus; ejus apud te patrocínia sentiámus: Per Dóminum.',
 'se':'Hóstias, Dómine, quas tibi offérimus, propítius súscipe: et intercedénte beáta N. Vírgine et Mártyre tua, víncula peccatórum nostrórum absólve. Per Dóminum.',
 'pc':'Refécti cibo, potúque cælésti, Deus noster, te súpplices exorámus: ut in cujus hæc commemoratióne percépimus; ejus muniámur et précibus: Per Dóminum.'}
EN['C48s']={'or':'Almighty and everlasting God, who choose the weak things of the world to confound the strong, mercifully grant that we who keep the feast of blessed N., Your virgin and martyr, may feel the help of her patronage with You',
 'se':'Mercifully receive, O Lord, the sacrifices which we offer You, and, by the intercession of blessed N., Your virgin and martyr, loose the bonds of our sins',
 'pc':'Refreshed with heavenly food and drink, O our God, we humbly entreat You that we may also be defended by the prayers of her in whose commemoration we have received these gifts'}
F['C51s']={'p':'35*-36* (Unius Sanctæ nec Virginis nec Martyris)','or':'Tuórum corda fidélium Deus miserátor illústra: et beátæ N. précibus gloriósis, fac nos próspera mundi despícere; et cælésti semper consolatióne gaudére: Per Dóminum.',
 'se':'Múnera, Dómine, nostræ devotiónis offérimus: ut tibi grata, et nobis salutária, beátæ N. pia supplicatióne reddántur. Per Dóminum.',
 'pc':'Quǽsumus omnípotens Deus: ut quos salutáribus dignátus es erudíre mystériis; beátæ N. intercessióne gloriósa, cæléstibus refícias aliméntis: Per Dóminum.'}
EN['C51s']={'or':'O merciful God, enlighten the hearts of Your faithful, and by the glorious prayers of blessed N. make us despise the prosperity of the world and ever rejoice in heavenly consolation',
 'se':'We offer You, O Lord, the gifts of our devotion, that they may become pleasing to You and salutary to us through the devout supplication of blessed N.',
 'pc':'We beseech You, almighty God, that those whom You have deigned to instruct by the saving mysteries You may refresh with heavenly food through the glorious intercession of blessed N.'}
EN['G491']={'or':'O God, who gladden us by the yearly feast of Your holy martyrs Gervase and Protase, mercifully grant that we may be kindled by the example of those in whose merits we rejoice',
 'se':'Sanctify, O Lord, the gifts dedicated to You, and, Your holy martyrs Gervase and Protase interceding, look graciously upon us through them',
 'pc':'Filled with the gift of Your salvation, we humbly pray You, O Lord, that, Your holy martyrs Gervase and Protase interceding, we may be renewed by the effect of that which we rejoice to taste'}
F['Pent23']['p']='303-304 (Dominica XXI post Octavam Trinitatis)'
