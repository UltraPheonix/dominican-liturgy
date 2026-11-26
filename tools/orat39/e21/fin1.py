from en_common import *
# final Latin read from M39 page images (task 2: DO-sourced orations replaced by the Missal's text)
F = {}
EN = {}
F['S0117']={'p':'356','or':'Intercéssio nos, quǽsumus Dómine, beáti Antónii Abbátis comméndet: ut quod nostris méritis non valémus; ejus patrocínio assequámur: Per Dóminum.',
 'se':'Sacris altáribus, Dómine, hóstias superpósitas sanctus Antónius Abbas, quǽsumus, in salútem nobis proveníre depóscat. Per Dóminum.',
 'pc':'Prótegat nos, Dómine, cum tui perceptióne sacraménti, beátus Antónius Abbas, pro nobis intercedéndo: ut et conversatiónis ejus experiámur insígnia; et intercessiónis ipsíus percipiámus suffrágia: Per Dóminum.'}
F['S0127']={'p':'','or':'Ecclésiam tuam, quǽsumus Dómine, grátia cæléstis amplíficet; quam beáti Joánnis Chrysóstomi Confessóris tui atque Pontíficis, illustráre voluísti gloriósis méritis et doctrínis: Per Dóminum.',
 'se':'Passiónis Fílii tui, Dómine, memóriam recenséntes depóscimus: ut quod tibi in beáti Joánnis Chrysóstomi Pontíficis tui solemnitáte deférimus, sacrifícium sit accéptum. Per eúmdem.',
 'pc':'Hæc nos, quǽsumus Dómine, commúnio sancta lætíficet: qua beáti Joánnis Chrysóstomi Pontíficis tui suffrágiis, virtútes roboréntur intérius; et actus extérius piæ operatiónis excréscant: Per Dóminum.'}
EN['S0127']={'or':'May heavenly grace, we beseech You, O Lord, increase Your Church, which You have willed to enlighten by the glorious merits and teaching of blessed John Chrysostom, Your confessor and bishop',
 'se':'Recalling the memory of the Passion of Your Son, O Lord, we ask that the sacrifice which we offer You on the feast of blessed John Chrysostom, Your bishop, may be acceptable',
 'pc':'May this holy communion, we beseech You, O Lord, gladden us, that by the prayers of blessed John Chrysostom, Your bishop, our virtues may be strengthened within and the works of devout service may increase without'}
F['S0128']={'p':'','or':'Deus, qui in tuæ caritátis exémplum, ad fidélium redemptiónem sanctum Petrum Ecclésiam tuam nova prole fecundáre divínitus docuísti: ipsíus nobis intercessióne concéde, a peccáti servitúte solútis; in cælésti pátria perpétua libertáte gaudére: Qui vivis.',
 'se':'Præsta nobis, quǽsumus omnípotens Deus, ut nostræ humilitátis oblátio, et pro tuórum tibi grata sit honóre Sanctórum, et nos córpore páriter et mente puríficet. Per Dóminum.',
 'pc':'Quǽsumus omnípotens Deus: ut qui cæléstia aliménta percépimus; intercedénte beáto Petro Confessóre tuo, per hæc contra ómnia advérsa muniámur: Per Dóminum.'}
SE_OMN='Almighty and everlasting God, through the intercession of blessed {n}, Your {t}, make the gifts offered to Your majesty avail us unto everlasting salvation'
PC_SACR='Receiving the sacraments of our salvation, grant, we beseech You, almighty God, that the prayer of blessed {n}, Your {t}, may help us everywhere, in whose veneration we have offered these gifts to Your majesty'
def DOC(name_gen, la_t, n, t):
    return ('Omnípotens sempitérne Deus, múnera tuæ majestáti obláta, per intercessiónem beáti %s %s, ad perpétuam nobis fac proveníre salútem. Per Dóminum.'%(name_gen,la_t),
            'Sacraménta salútis nostræ suscipiéntes, concéde, quǽsumus omnípotens Deus: ut beáti %s %s nos ubíque orátio ádjuvet; in cujus veneratióne hæc tuæ obtúlimus majestáti: Per Dóminum.'%(name_gen,la_t),
            SE_OMN.format(n=n,t=t), PC_SACR.format(n=n,t=t))
se,pc,ese,epc=DOC('Francísci','Pontíficis tui atque Doctóris','Francis','bishop and doctor')
F['S0129']={'p':'','or':'Deus, qui ad animárum salútem beátum Francíscum Confessórem tuum atque Pontíficem, ómnibus ómnia factum esse voluísti: concéde propítius, ut caritátis tuæ dulcédine perfúsi; ejus dirigéntibus mónitis, ac suffragántibus méritis, ætérna gáudia consequámur: Per Dóminum.','se':se,'pc':pc}
EN['S0129']={'se':ese,'pc':epc}
F['S0131']={'p':'','or':'Deus, qui sanctum Joánnem Confessórem tuum adolescéntium patrem et magístrum excitásti; ac per eum, auxiliatríce Vírgine María, novas in Ecclésia tua famílias floréscere voluísti: concéde, quǽsumus, ut eódem caritátis igne succénsi; ánimas quǽrere, tibíque soli servíre valeámus: Per Dóminum.',
 'se':'Súscipe, Dómine, oblatiónem mundam salutáris Hóstiæ et præsta, ut, te in ómnibus et super ómnia diligéntes, in glóriæ tuæ laudem vívere mereámur. Per Dóminum.',
 'pc':'Córporis et Sánguinis tui, Dómine, mystério satiátis, concéde, quǽsumus; ut, intercedénte sancto Joánne Confessóre, in gratiárum semper actióne maneámus: Qui vivis.'}
F['S0202']={'p':'','or':'Omnípotens sempitérne Deus, majestátem tuam súpplices exorámus: ut sicut unigénitus Fílius tuus hodiérna die cum nostræ carnis substántia in templo est præsentátus; ita nos fácias purificátis tibi méntibus præsentári: Per eúmdem Dóminum.',
 'se':'Exáudi Dómine preces nostras: et ut digna sint múnera, quæ óculis tuæ majestátis offérimus, subsídium nobis, per intercessiónem beátæ Maríæ Vírginis, perpétuæ tuæ pietátis impénde. Per Dóminum.',
 'pc':'Quǽsumus Dómine Deus noster: ut sacrosáncta mystéria, quæ pro reparatiónis nostræ munímine contulísti; intercedénte beáta María semper Vírgine, et præsens nobis remédium esse fácias, et futúrum: Per Dóminum.'}
F['S0204']={'p':'','or':'Deus, qui in Ecclésia tua nova semper instáuras exémpla virtútum: da pópulo tuo, beáti Andréæ Confessóris tui atque Pontíficis ita sequi vestígia; ut assequátur et prǽmia: Per Dóminum.',
 'se':'Accépta sit in conspéctu tuo Dómine nostra devótio: ut ejus nobis fiat supplicatióne salutáris, pro cujus solemnitáte defértur. Per Dóminum.',
 'pc':'Da, quǽsumus Dómine, fidélibus tuis, Sanctórum tuórum semper veneratióne lætári; et eórum perpétua supplicatióne muníri: Per Dóminum.'}
F['S0208']={'p':'','or':'Deus, qui per sanctum Joánnem Ordinem sanctíssimæ Trinitátis, ad rediméndum de potestáte Saracenórum captívos, cǽlitus institúere dignátus es: præsta quǽsumus, ut ejus suffragántibus méritis; a captivitáte córporis et ánimæ, te adjuvánte, liberémur: Per Dóminum.',
 'se':'Præsta nobis, quǽsumus omnípotens Deus, ut nostræ humilitátis oblátio, et pro tuórum tibi grata sit honóre Sanctórum, et nos córpore páriter et mente puríficet. Per Dóminum.',
 'pc':'Quǽsumus omnípotens Deus: ut qui cæléstia aliménta percépimus; intercedénte beáto Joánne Confessóre tuo, per hæc contra ómnia advérsa muniámur: Per Dóminum.'}
F['S0209']={'p':'','or':'Deus qui beátum Cyríllum Confessórem tuum atque Pontíficem divínæ maternitátis beatíssimæ Vírginis Maríæ assertórem invíctum effecísti: concéde, ipso intercedénte, ut qui vere eam Genitrícem Dei crédimus; matérna ejúsdem protectióne salvémur: Per eúmdem Dóminum.',
 'se':'Múnera nostra, omnípotens Deus, benígnus réspice: et intercedénte beáto Cyríllo præsta, ut Unigénitum tuum Jesum Christum Dóminum nostrum in tua tecum glória coætérnum, in córdibus nostris digne suscípere mereámur: Qui tecum vivit et regnat.',
 'pc':'Divínis Dómine, refécti mystériis, Te súpplices deprecámur: ut exémplis et méritis beáti Cyrílli Pontíficis adjúti; sanctíssimæ Genitríci Unigéniti tui digne famulári valeámus: Qui tecum vivit.'}
se,pc,ese,epc=DOC('Petri','Confessóris tui atque Doctóris','Peter','confessor and doctor')
F['S0223']={'p':'','or':'Concéde nos, quǽsumus omnípotens Deus, beáti Petri Confessóris tui atque Pontíficis mónita et exémpla sectári; ut per terréstrium rerum contémptum, ætérna gáudia consequámur: Per Dóminum.','se':se,'pc':pc}
EN['S0223']={'se':ese,'pc':epc}
COLL_DOC='Deus, qui pópulo tuo ætérnæ salútis beátum %s minístrum tribuísti: præsta quǽsumus, ut quem doctórem vitæ habúimus in terris; intercessórem habére mereámur in cælis: Per Dóminum.'
ECOLL_DOC='O God, who gave blessed %s to Your people as a minister of eternal salvation, grant, we beseech You, that we may deserve to have him as our intercessor in heaven whom we had as the teacher of life on earth'
se,pc,ese,epc=DOC('Isidóri','Pontíficis tui atque Doctóris','Isidore','bishop and doctor')
F['S0404']={'p':'','or':COLL_DOC%'Isidórum','se':se,'pc':pc}; EN['S0404']={'or':ECOLL_DOC%'Isidore','se':ese,'pc':epc}
se,pc,ese,epc=DOC('Ansélmi','Pontíficis tui atque Doctóris','Anselm','bishop and doctor')
F['S0421']={'p':'','or':COLL_DOC%'Ansélmum','se':se,'pc':pc}; EN['S0421']={'or':ECOLL_DOC%'Anselm','se':ese,'pc':epc}
NOTES=['S0421 Collect: the Missal prints "pópulo tuæ ætérnæ salútis" (misprint); printed as "pópulo tuo".']
se,pc,ese,epc=DOC('Hilárii','Confessóris tui atque Doctóris','Hilary','confessor and doctor')
F['S0114']={'p':'20*-21* (Commune Doctorum, as the Missal directs on 14 Jan., p. 353)','or':COLL_DOC%'Hilárium','se':se,'pc':pc}; EN['S0114']={'or':ECOLL_DOC%'Hilary','se':ese,'pc':epc}
se,pc,ese,epc=DOC('Athanásii','Confessóris tui atque Pontíficis','Athanasius','confessor and bishop')
F['S0502']={'p':'','or':COLL_DOC%'Athanásium','se':se,'pc':pc}; EN['S0502']={'or':ECOLL_DOC%'Athanasius','se':ese,'pc':epc}
F['S0510']={'p':'','or':'Sancti Antoníni, Dómine, Confessóris tui atque Pontíficis méritis adjuvémur: ut sicut te in illo mirábilem prædicámus; ita in nos misericórdem fuísse gloriémur: Per Dóminum.',
 'se':'Sacrifícium nostrum, Dómine, beátus Antonínus sacérdos majestátis tuæ óculis reddat accéptum: qui se tibi, dum vixit, sanctam et placéntem hóstiam immolávit. Per Dóminum.',
 'pc':'Vitáli cibo recreáti, grátias tibi Dómine ágimus: et rogámus, ut quod ad glóriam súmpsimus sancti tui Præsulis Antoníni; ejus précibus sit nobis contra hostíles ímpetus auxílium: Per Dóminum.'}
EN['S0510']={'or':'May we be helped, O Lord, by the merits of saint Antoninus, Your confessor and bishop, that, as we proclaim You wonderful in him, so we may glory that You have been merciful to us',
 'se':'May blessed Antoninus the priest, O Lord, make our sacrifice acceptable in the eyes of Your majesty, he who while he lived offered himself to You as a holy and pleasing victim',
 'pc':'Refreshed with life-giving food, we give You thanks, O Lord, and ask that what we have received for the glory of Your holy bishop Antoninus may by his prayers be our help against the assaults of the enemy'}
se,pc,ese,epc=DOC('Bedæ','Confessóris tui atque Doctóris','Bede','confessor and doctor')
F['S0527']={'p':'','or':'Deus, qui Ecclésiam tuam beáti Bedæ Confessóris tui atque Doctóris eruditióne claríficas: concéde propítius fámulis tuis; ejus semper illustrári sapiéntia et méritis adjuvári: Per Dóminum.','se':se,'pc':pc}
EN['S0527']={'se':ese,'pc':epc}
F['S0606']={'p':'','or':'Deus, qui beátum Norbértum Confessórem tuum atque Pontíficem, verbi tui præcónem exímium effecísti; et per eum Ecclésiam tuam nova prole fecundásti: præsta quǽsumus, ut ejúsdem suffragántibus méritis, quod ore simul et ópere dócuit; te adjuvánte exercére valeámus: Per Dóminum.',
 'se':'Sancti tui, quǽsumus Dómine, nos ubíque lætíficent: ut dum eórum mérita recólimus, patrocínia sentiámus. Per Dóminum.',
 'pc':'Præsta, quǽsumus omnípotens Deus: ut de percéptis munéribus grátias exhibéntes; intercedénte beáto Norbérto Confessóre tuo atque Pontífice, benefícia potióra sumámus: Per Dóminum.'}
F['S0611']={'p':'','or':'Quǽsumus omnípotens Deus: ut beátus Bárnabas Apóstolus, tuum pro nobis implóret auxílium; ut a nostris reátibus absolúti, a cunctis étiam perículis eruámur: Per Dóminum.',
 'se':'Sacrándum tibi, Dómine, munus offérimus: quo beáti Bárnabæ Apóstoli tui solémnia recoléntes, purificatiónem quoque nostris méntibus implorámus. Per Dóminum.',
 'pc':'Percéptis Dómine sacraméntis, supplíciter exorámus: ut intercedénte beáto Bárnaba Apóstolo tuo, quæ pro illíus veneránda gérimus passióne; nobis profíciant ad medélam: Per Dóminum.'}
EN['S0611']={'or':'We beseech You, almighty God, that blessed Barnabas the Apostle may implore Your help for us, that, being freed from our sins, we may also be delivered from all dangers',
 'se':'We offer You, O Lord, the gift to be consecrated, by which, keeping the feast of blessed Barnabas Your Apostle, we implore also the cleansing of our minds',
 'pc':'Having received the sacraments, O Lord, we humbly entreat You that, by the intercession of blessed Barnabas Your Apostle, what we do in veneration of his passion may avail for our healing'}
F['S0613']={'p':'','or':'Ecclésiam tuam, Deus, beáti Antónii Confessóris tui solémnitas votíva lætíficet: ut spirituálibus semper muniátur auxíliis; et gáudiis pérfrui mereátur ætérnis: Per Dóminum.',
 'se':'Præsens oblátio fiat, Dómine, pópulo tuo salutáris, pro quo dignátus es Patri tuo te vivéntem hóstiam immoláre: Qui cum eódem Deo Patre et Spíritu Sancto vivis et regnas Deus, per ómnia sǽcula sæculórum.',
 'pc':'Divínis, Dómine, munéribus satiáti: quǽsumus, ut beáti Antónii Confessóris tui méritis gloriósis; salutáris víctimæ desiderátum sentiámus efféctum: Per Dóminum.'}
EN['S0613']={'or':'May the devout feast of blessed Anthony, Your confessor, gladden Your Church, O God, that she may ever be defended by spiritual help and deserve to enjoy everlasting joys',
 'se':'May this present offering, O Lord, be saving for Your people, for whom You deigned to offer Yourself to Your Father as a living victim; who with the same God the Father and the Holy Spirit live and reign, God, world without end',
 'pc':'Filled with divine gifts, we beseech You, O Lord, that by the glorious merits of blessed Anthony, Your confessor, we may feel the longed-for effect of the saving Victim'}
se,pc,ese,epc=DOC('Ephræm','Confessóris tui atque Doctóris','Ephrem','confessor and doctor')
F['S0618']={'p':'','or':'Deus, qui Ecclésiam tuam beáti Ephræm Confessóris tui et Doctóris mira eruditióne et præcláris vitæ méritis illustráre voluísti: te súpplices exorámus; ut, ipso intercedénte, eam advérsus erróris et pravitátis insídias perénni tua virtúte deféndas. Per Dóminum.','se':se,'pc':pc}
EN['S0618']={'se':ese,'pc':epc}
F['S0712']={'p':'','or':'Intercéssio nos, quǽsumus Dómine, beáti Joánnis Abbátis comméndet: ut quod nostris méritis non valémus; ejus patrocínio assequámur: Per Dóminum.',
 'se':'Præsta nobis, quǽsumus omnípotens Deus, ut nostræ humilitátis oblátio, et pro tuórum tibi grata sit honóre Sanctórum, et nos córpore páriter et mente puríficet. Per Dóminum.',
 'pc':'Prótegat nos, Dómine, cum tui perceptióne sacraménti, beátus Joánnes Abbas, pro nobis intercedéndo: ut et conversatiónis ejus experiámur insígnia; et intercessiónis ipsíus percipiámus suffrágia: Per Dóminum.'}
F['S0714']={'p':'','or':COLL_DOC%'Bonaventúram',
 'se':'Sancti Bonaventúræ Confessóris tui atque Pontíficis nobis, Dómine, pia non desit orátio: quæ et múnera nostra concíliet, et tuam nobis indulgéntiam semper obtíneat. Per Dóminum.',
 'pc':'Ut nobis, Dómine, tua sacrifícia dent salútem; beátus Bonaventúra Conféssor tuus et Póntifex, quǽsumus, precátor accédat. Per Dóminum.'}
F['S0715']={'p':'','or':'Deus, qui hodiérna die beátum Henrícum Confessórem tuum e terréni cúlmine impérii ad regnum ætérnum transtulísti; te súpplices exorámus: ut sicut illum, grátiæ tuæ ubertáte prævéntum, illécebras sǽculi superáre fecísti; ita nos fácias, ejus imitatióne, mundi hujus blandiménta vitáre, et ad te puris méntibus perveníre: Per Dóminum.',
 'se':'Laudis tibi Dómine hóstias immolámus in tuórum commemoratióne Sanctórum: quibus nos et præséntibus éxui malis confídimus, et futúris: Per Dóminum.',
 'pc':'Refécti cibo potúque cælésti, Deus noster, te súpplices exorámus: ut in cujus hæc commemoratióne percépimus; ejus muniámur et précibus: Per Dóminum.'}
EN['S0715']={'se':SE_LAUDIS,'pc':PC_REFECTI}
F['S0816']={'p':'','or':'Deus, qui præ ómnibus sanctis tuis beátum Jóachim Genitrícis Fílii tui patrem esse voluísti: concéde quǽsumus, ut cujus festa venerámur; ejus quoque perpétuo patrocínia sentiámus: Per eúmdem.',
 'se':'Súscipe clementíssime Deus sacrifícium in honórem sancti Patriárchæ Jóachim, patris Maríæ Vírginis, majestáti tuæ oblátum: ut ipso cum cónjuge sua et beatíssima prole intercedénte, perféctam cónsequi mereámur remissiónem peccatórum, et glóriam sempitérnam. Per Dóminum.',
 'pc':'Quǽsumus omnípotens Deus, ut per hæc sacraménta, quæ súmpsimus: intercedéntibus méritis et précibus beáti Jóachim, patris Genitrícis dilécti Fílii tui Dómini nostri Jesu Christi; tuæ grátiæ in præsénti, et ætérnæ glóriæ in futúro partícipes esse mereámur: Per eúmdem.'}
se,pc,ese,epc=DOC('Bernárdi','Confessóris tui atque Doctóris','Bernard','confessor and doctor')
F['S0820']={'p':'','or':COLL_DOC%'Bernárdum','se':se,'pc':pc}; EN['S0820']={'or':ECOLL_DOC%'Bernard','se':ese,'pc':epc}
F['S0828']={'p':'','or':'Adésto supplicatiónibus nostris omnípotens Deus: et quibus fidúciam sperándæ pietátis indúlges; intercedénte beáto Augustíno Confessóre tuo atque Pontífice, consuétæ misericórdiæ tríbue benígnus efféctum: Per Dóminum.',
 'se':'Sancti Confessóris tui atque Pontíficis Augustíni nobis, Dómine, pia non desit orátio: quæ et múnera nostra concíliet, et tuam nobis indulgéntiam semper obtíneat. Per Dóminum.',
 'pc':'Ut nobis, Dómine, tua sacrifícia dent salútem; beátus Conféssor tuus Augustínus, et Póntifex, quǽsumus, precátor accédat: Per Dóminum.'}
EN['S0828']={'or':'Hearken to our supplications, almighty God, and, blessed Augustine, Your confessor and bishop, interceding, graciously grant the effect of Your wonted mercy to those to whom You give confidence to hope for Your loving-kindness',
 'se':'May the loving prayer of Your holy confessor and bishop Augustine not fail us, O Lord, that it may make our gifts acceptable and ever obtain for us Your pardon',
 'pc':'That Your sacrifices may give us salvation, O Lord, may blessed Augustine, Your confessor and bishop, we beseech You, come forward as our advocate'}
F['S0929']={'p':'','or':'Deus, qui miro órdine Angelórum ministéria hominúmque dispénsas; concéde propítius: ut a quibus tibi ministrántibus in cælo semper assístitur; ab his in terra vita nostra muniátur: Per Dóminum.',
 'se':'Hóstias tibi, Dómine, laudis offérimus, supplíciter deprecántes: ut eásdem, Angélico pro nobis interveniénte suffrágio, et placátus accípias, et ad salútem nostram proveníre concédas. Per Dóminum.',
 'pc':'Beáti Archángeli tui Michaélis intercessióne suffúlti, súpplices te, Dómine, deprecámur: ut quod ore proséquimur; contingámus et mente: Per Dóminum.'}
F['S0822']={'p':'supplement (Immaculati Cordis B.M.V., 22 Aug.), pp. 4-6','or':'Omnípotens sempitérne Deus, qui in Corde beátæ Maríæ Vírginis dignum Spíritus Sancti habitáculum præparásti: concéde propítius, ut ejúsdem immaculáti Cordis festivitátem devóta mente recoléntes; secúndum cor tuum vívere valeámus: Per Dóminum ejúsdem.',
 'se':'Majestáti tuæ, Dómine, Agnum immaculátum offeréntes, quǽsumus, ut corda nostra ignis ille divínus accéndat, qui Cor beátæ Maríæ Vírginis ineffabíliter inflammávit: Per eúmdem Dóminum.',
 'pc':'Divínis refécti munéribus te, Dómine, supplíciter exorámus: ut beátæ Maríæ Vírginis intercessióne, cujus immaculáti Cordis solémnia venerándo égimus; a præséntibus perículis liberáti, ætérnæ vitæ gáudia consequámur: Per Dóminum.'}
EN['S0822']={'or':'Almighty and everlasting God, who in the Heart of the blessed Virgin Mary prepared a dwelling worthy of the Holy Spirit, mercifully grant that, keeping with devout minds the feast of her Immaculate Heart, we may be able to live according to Your heart',
 'se':'Offering to Your majesty, O Lord, the spotless Lamb, we beseech You that our hearts may be kindled by that divine fire which ineffably inflamed the Heart of the blessed Virgin Mary',
 'pc':'Refreshed with divine gifts, we humbly entreat You, O Lord, that by the intercession of the blessed Virgin Mary, whose Immaculate Heart we have venerated in this feast, we may be freed from present dangers and attain the joys of eternal life'}
CMP={'p':'314-315 (In Compassione B.M.V.)','or':'Intervéniat pro nobis, quǽsumus Dómine Jesu Christe, nunc et in hora mortis nostræ apud tuam cleméntiam beáta Virgo María Mater tua: cujus sacratíssimam ánimam in hora benedíctæ passiónis tuæ dolóris gládius pertransívit; et in gloriósa resurrectióne tua ingens gáudium lætificávit: Qui vivis.',
 'se':'Offérimus tibi preces et hóstias, Dómine Jesu Christe, humíliter supplicántes: ut qui transfixiónem dulcíssimi spíritus beátæ Maríæ Matris tuæ précibus recensémus; suo suorúmque sub cruce Sanctórum consórtium multiplicáto piíssimo intervéntu, méritis mortis tuæ, méritum cum Beátis habeámus: Qui vivis et regnas.',
 'pc':'Sacrifícia, quæ súmpsimus, Dómine Jesu Christe, transfixiónem Matris tuæ et Vírginis devóte celebrántes; nobis ímpetrent apud cleméntiam tuam omnis boni salutáris efféctum: Qui vivis et regnas.'}
ECMP={'or':'May the blessed Virgin Mary, Your Mother, intercede for us with Your mercy, we beseech You, O Lord Jesus Christ, now and at the hour of our death, she whose most holy soul was pierced by the sword of sorrow in the hour of Your blessed passion, and gladdened with great joy in Your glorious resurrection',
 'se':'We offer You prayers and sacrifices, O Lord Jesus Christ, humbly beseeching You that we who by our prayers recall the piercing of the most sweet spirit of blessed Mary Your Mother may, by the manifold and most loving intercession of her and of the Saints with her beneath the Cross, have through the merits of Your death a share with the Blessed',
 'pc':'May the sacrifices which we have received, O Lord Jesus Christ, as we devoutly celebrate the piercing of Your Mother and Virgin, obtain for us from Your mercy the effect of every saving good'}
F['Quad5f']=dict(CMP); EN['Quad5f']=ECMP
F['S0915']=dict(CMP,p='314-315 (In Compassione B.M.V.; "Missa dicitur ut in Compassione", 15 Sept., p. 559)'); EN['S0915']=ECMP
F['S1006']={'p':'','or':'Sancti Brunónis Confessóris tui, quǽsumus Dómine, intercessiónibus adjuvémur: ut qui majestátem tuam gráviter delinquéndo offéndimus; ejus méritis et précibus, nostrórum delictórum véniam consequámur: Per Dóminum.',
 'se':'Laudis tibi Dómine hóstias immolámus in tuórum commemoratióne Sanctórum: quibus nos et præséntibus éxui malis confídimus, et futúris. Per Dóminum.',
 'pc':'Quǽsumus omnípotens Deus: ut qui cæléstia aliménta percépimus; intercedénte beáto Brunóne Confessóre tuo, per hæc contra ómnia advérsa muniámur: Per Dóminum.'}
EN['S1006']={'se':SE_LAUDIS,'pc':PC_QUAESUMUS.format(n='Bruno')}
F['S1019']={'p':'','or':'Deus, qui beátum Petrum Confessórem tuum admirábilis pœniténtiæ, et altíssimæ contemplatiónis múnere illustráre dignátus es: da nobis, quǽsumus; ut ejus suffragántibus méritis, carne mortificáti facílius cæléstia capiámus: Per Dóminum.',
 'se':'Præsta nobis, quǽsumus omnípotens Deus, ut nostræ humilitátis oblátio, et pro tuórum tibi grata sit honóre Sanctórum, et nos córpore páriter et mente puríficet. Per Dóminum.',
 'pc':'Quǽsumus omnípotens Deus: ut qui cæléstia aliménta percépimus; intercedénte beáto Petro Confessóre tuo, per hæc contra ómnia advérsa muniámur: Per Dóminum.'}
EN['S1019']={'se':SE_PRAESTA,'pc':PC_QUAESUMUS.format(n='Peter')}
F['S1102']={'p':'623 (Ad primam Missam)','or':'Fidélium, Deus, ómnium cónditor et redémptor: animábus famulórum, famularúmque tuárum remissiónem cunctórum tríbue peccatórum; ut indulgéntiam, quam semper optavérunt, piis supplicatiónibus consequántur: Qui vivis.',
 'se':'Hóstias, quǽsumus, Dómine, quas tibi pro animábus famulórum, famularúmque tuárum offérimus, propitiátus inténde; ut quibus fídei christiánæ méritum contulísti, dones et prǽmium. Per Dóminum.',
 'pc':'Animábus, quǽsumus, Dómine, famulórum famularúmque tuárum, orátio profíciat supplicántium: ut eas et a peccátis ómnibus éxuas; et tuæ redemptiónis fácias esse partícipes: Qui vivis.'}
EN['S1102']={'or':'O God, the creator and redeemer of all the faithful, grant to the souls of Your servants and handmaids the remission of all their sins, that by loving prayers they may obtain the pardon they have always desired',
 'se':'Look graciously, we beseech You, O Lord, on the sacrifices which we offer You for the souls of Your servants and handmaids, that to those on whom You bestowed the merit of Christian faith You may give also its reward',
 'pc':'May the prayer of Your suppliants, we beseech You, O Lord, profit the souls of Your servants and handmaids, that You may free them from all their sins and make them partakers of Your redemption'}
F['S1102_2']={'p':'624-625 (Ad secundam Missam)','or':'Deus, indulgentiárum Dómine; da animábus famulórum famularúmque tuárum, refrigérii sedem, quiétis beatitúdinem, et lúminis claritátem: Per Dóminum.',
 'se':'Propitiáre, Dómine, supplicatiónibus nostris, pro animábus famulórum famularúmque tuárum, pro quibus tibi offérimus sacrifícium laudis; ut eas Sanctórum tuórum consórtio sociáre dignéris. Per Dóminum.',
 'pc':'Præsta, quǽsumus, Dómine, ut ánimæ famulórum famularúmque tuárum, his purgátæ sacrifíciis; indulgéntiam páriter, et réquiem cápiant sempitérnam: Per Dóminum.'}
EN['S1102_2']={'or':'O God, the Lord of mercies, grant to the souls of Your servants and handmaids a place of refreshment, the happiness of rest and the brightness of light',
 'se':'Be appeased, O Lord, by our supplications for the souls of Your servants and handmaids, for whom we offer You the sacrifice of praise, that You may deign to join them to the fellowship of Your Saints',
 'pc':'Grant, we beseech You, O Lord, that the souls of Your servants and handmaids, being cleansed by this sacrifice, may obtain both pardon and everlasting rest'}
F['S1102_3']={'p':'625-626 (Ad tertiam Missam)','or':'Deus, véniæ largítor, et humánæ salútis auctor, quǽsumus cleméntiam tuam: ut ánimas famulórum famularúmque tuárum, quæ ex hoc sǽculo transiérunt; beáta María semper Vírgine intercedénte cum ómnibus Sanctis tuis, ad perpétuæ beatitúdinis consórtium perveníre concédas: Per Dóminum.',
 'se':'Deus, cujus misericórdiæ non est númerus, súscipe propítius preces humilitátis nostræ: et animábus ómnium fidélium defunctórum, quibus tui nóminis dedísti confessiónem, per hæc sacraménta salútis nostræ, cunctórum remissiónem tríbue peccatórum. Per Dóminum.',
 'pc':'Præsta, quǽsumus, omnípotens et miséricors Deus: ut ánimæ famulórum famularúmque tuárum, pro quibus hoc sacrifícium laudis tuæ obtúlimus majestáti; per hujus virtútem sacraménti, a peccátis ómnibus expiátæ, lucis perpétuæ, te miseránte, recípiant beatitúdinem: Per Dóminum.'}
EN['S1102_3']={'or':'O God, the giver of pardon and author of man\'s salvation, we beseech Your mercy that, blessed Mary ever Virgin interceding with all Your Saints, You would grant the souls of Your servants and handmaids who have passed out of this world to come to the fellowship of everlasting bliss',
 'se':'O God, whose mercy is without measure, mercifully receive the prayers of our lowliness, and through these sacraments of our salvation grant the remission of all sins to the souls of all the faithful departed, to whom You gave the confession of Your name',
 'pc':'Grant, we beseech You, almighty and merciful God, that the souls of Your servants and handmaids, for whom we have offered this sacrifice of praise to Your majesty, may by the power of this sacrament be cleansed from all their sins and, by Your mercy, receive the happiness of everlasting light'}
F['S1104']={'p':'','or':'Ecclésiam tuam, Dómine, sancti Cároli Confessóris tui atque Pontíficis contínua protectióne custódi: ut sicut illum pastorális sollicitúdo gloriósum effécit; ita nos ejus intercéssio in tuo semper fáciat amóre fervéntes: Per Dóminum.',
 'se':'Da miséricors Deus, ut hæc salutáris oblátio, intercedénte beáto Cárolo Confessóre tuo atque Pontífice, et a própriis nos reátibus indesinénter expédiat, et ab ómnibus tueátur advérsis. Per Dóminum.',
 'pc':'Præsta, quǽsumus Dómine Deus noster: ut quorum festivitáte votíva sunt sacraménta; eórum intercessióne salutária nobis reddántur: Per Dóminum.'}
EN['S1104']={'or':'Guard Your Church, O Lord, by the continual protection of saint Charles, Your confessor and bishop, that, as his pastoral care made him glorious, so his intercession may make us ever fervent in Your love',
 'se':'Grant, O merciful God, that this saving offering, by the intercession of blessed Charles, Your confessor and bishop, may ever free us from our own sins and defend us against all adversities',
 'pc':'Grant, we beseech You, O Lord our God, that the sacraments which are offered on the feast of Your saints may by their intercession become saving for us'}
F['S1111']={'p':'','or':'Deus, qui cónspicis quia ex nulla nostra virtúte subsístimus; concéde propítius, ut intercessióne beáti Martíni Confessóris tui atque Pontíficis, contra ómnia advérsa muniámur: Per Dóminum.',
 'se':'Da miséricors Deus, ut hæc salutáris oblátio, et a própriis nos reátibus indesinénter expédiat, et ab ómnibus tueátur advérsis. Per Dóminum.',
 'pc':'Præsta, quǽsumus Dómine Deus noster: ut quorum festivitáte votíva sunt sacraménta; eórum intercessióne salutária nobis reddántur: Per Dóminum.'}
EN['S1111']={'or':'O God, who see that we do not stand by any strength of our own, mercifully grant that by the intercession of blessed Martin, Your confessor and bishop, we may be defended against all adversities',
 'se':'Grant, O merciful God, that this saving offering may ever free us from our own sins and defend us against all adversities',
 'pc':'Grant, we beseech You, O Lord our God, that the sacraments which are offered on the feast of Your saints may by their intercession become saving for us'}
F['S1117']={'p':'','or':'Da, quǽsumus omnípotens Deus: ut beáti Gregórii Confessóris tui atque Pontíficis veneránda solémnitas; et devotiónem nobis áugeat, et salútem: Per Dóminum.',
 'se':'Sancti tui, quǽsumus Dómine, nos ubíque lætíficent: ut dum eórum mérita recólimus, patrocínia sentiámus. Per Dóminum.',
 'pc':'Præsta, quǽsumus omnípotens Deus: ut de percéptis munéribus grátias exhibéntes; intercedénte beáto Gregório Confessóre tuo atque Pontífice, benefícia potióra sumámus: Per Dóminum.'}
EN['S1117']={'or':'Grant, we beseech You, almighty God, that the venerable feast of blessed Gregory, Your confessor and bishop, may increase in us both devotion and salvation',
 'se':'May Your saints, we beseech You, O Lord, everywhere gladden us, that while we recall their merits we may feel their protection',
 'pc':'Grant, we beseech You, almighty God, that, giving thanks for the gifts received, we may, by the intercession of blessed Gregory, Your confessor and bishop, receive still greater benefits'}
EN['S0606']={'se':EN['S1117']['se'],'pc':'Grant, we beseech You, almighty God, that, giving thanks for the gifts received, we may, by the intercession of blessed Norbert, Your confessor and bishop, receive still greater benefits'}
F['S1120']={'p':'','or':'Deus, qui beátum Felícem Confessórem tuum ex erémo ad munus rediméndi captívos cǽlitus vocáre dignátus es: præsta quǽsumus, ut per grátiam tuam ex peccatórum nostrórum captivitáte, ejus intercessióne, liberáti; ad cæléstem pátriam perducámur: Per Dóminum.',
 'se':'Laudis tibi Dómine hóstias immolámus in tuórum commemoratióne Sanctórum: quibus nos et præséntibus éxui malis confídimus, et futúris. Per Dóminum.',
 'pc':'Refécti cibo potúque cælésti, Deus noster, te súpplices exorámus: ut in cujus hæc commemoratióne percépimus; ejus muniámur et précibus: Per Dóminum.'}
EN['S1120']={'se':SE_LAUDIS,'pc':PC_REFECTI}
se,pc,ese,epc=DOC('Joánnis','Confessóris tui atque Doctóris','John','confessor and doctor')
F['S1124']={'p':'','or':'Deus, qui sanctum Joánnem Confessórem tuum atque Doctórem perféctæ sui abnegatiónis, et crucis amatórem exímium effecísti: concéde, ut ejus imitatióni júgiter inhæréntes; glóriam assequámur ætérnam: Per Dóminum.','se':se,'pc':pc}
EN['S1124']={'se':ese,'pc':epc}
F['S1125']={'p':'','or':'Deus, qui dedísti legem Móysi in summitáte montis Sínai, et in eódem loco per sanctos Angelos tuos corpus beátæ Catharínæ Vírginis et Mártyris tuæ mirabíliter collocásti: præsta quǽsumus, ut ejus méritis et intercessióne; ad montem, qui Christus est, perveníre valeámus: Qui tecum vivit.',
 'se':'Hóstia, quǽsumus Dómine, quam tibi sanctæ Catharínæ Vírginis et Mártyris tuæ natalítia recenséntes offérimus, et víncula nostræ pravitátis absólvat, et tuæ nobis misericórdiæ dona concíliet. Per Dóminum.',
 'pc':'Quǽsumus Dómine salutáribus repléti mystériis: ut cujus solémnia celebrámus; ejus oratiónibus adjuvémur: Per Dóminum.'}
EN['S1125']={'or':'O God, who gave the law to Moses on the summit of Mount Sinai, and in that same place wonderfully laid the body of blessed Catherine, Your virgin and martyr, by Your holy Angels, grant, we beseech You, that by her merits and intercession we may be able to come to the mountain which is Christ',
 'se':'May the sacrifice, O Lord, which we offer You keeping the birthday of saint Catherine, Your virgin and martyr, both loose the bonds of our wickedness and win for us the gifts of Your mercy',
 'pc':'Filled with saving mysteries, we beseech You, O Lord, that we may be helped by the prayers of her whose feast we celebrate'}
F['S1204']={'p':'','or':'Deus, qui beátum Petrum Chrysólogum Doctórem egrégium divínitus præmonstrátum, ad regéndam et instruéndam Ecclésiam tuam éligi voluísti: præsta quǽsumus, ut quem Doctórem vitæ habúimus in terris; intercessórem habére mereámur in cælis: Per Dóminum.',
 'se':'Sancti Petri Chrysólogi Pontíficis tui atque Doctóris nobis, Dómine, pia non desit orátio: quæ et múnera nostra concíliet, et tuam nobis indulgéntiam semper obtíneat. Per Dóminum.',
 'pc':'Ut nobis, Dómine, tua sacrifícia dent salútem; beátus Petrus Chrysólogus Póntifex tuus et Doctor egrégius, quǽsumus, precátor accédat: Per Dóminum.'}
EN['S1204']={'or':'O God, who willed that blessed Peter Chrysologus, the excellent Doctor divinely foreshown, should be chosen to rule and instruct Your Church, grant, we beseech You, that we may deserve to have him as our intercessor in heaven whom we had as the teacher of life on earth',
 'se':'May the loving prayer of saint Peter Chrysologus, Your bishop and doctor, not fail us, O Lord, that it may make our gifts acceptable and ever obtain for us Your pardon',
 'pc':'That Your sacrifices may give us salvation, O Lord, may blessed Peter Chrysologus, Your bishop and excellent doctor, we beseech You, come forward as our advocate'}
F['S1213']={'p':'','or':'Exáudi nos Deus salutáris noster: ut sicut de beátæ Lúciæ Vírginis et Mártyris tuæ festivitáte gaudémus; ita piæ devotiónis erudiámur afféctu: Per Dóminum.',
 'se':'Accépta tibi sit, Dómine, sacrátæ plebis oblátio pro tuórum honóre Sanctórum, quorum se méritis de tribulatióne percepísse cognóscit auxílium. Per Dóminum.',
 'pc':'Satiásti Dómine famíliam tuam munéribus sacris: ejus, quǽsumus, semper interventióne nos réfove; cujus solémnia celebrámus: Per Dóminum.'}
EN['S1213']={'or':'Hear us, O God our Saviour, that as we rejoice in the feast of blessed Lucy, Your virgin and martyr, so we may be taught the spirit of loving devotion','se':SE_ACCEPTA,'pc':PC_SATIASTI}
F['S1226']={'p':'','or':'Da nobis, quǽsumus Dómine, imitári quod cólimus, ut discámus et inimícos dilígere: quia ejus natalítia celebrámus; qui novit étiam pro persecutóribus exoráre Dóminum nostrum Jesum Christum Fílium tuum: Qui tecum vivit et regnat in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum.',
 'se':'Súscipe Dómine múnera pro tuórum commemoratióne Sanctórum: ut sicut illos pássio gloriósos effécit, ita nos devótio reddat innócuos. Per Dóminum.',
 'pc':'Auxiliéntur nobis, Dómine, sumpta mystéria; et intercedénte beáto Stéphano Mártyre tuo, sempitérna protectióne confírment: Per Dóminum.'}
EN['S1226']={'or':'Grant us, we beseech You, O Lord, to imitate what we venerate, that we may learn to love even our enemies, since we keep the birthday of him who knew how to pray even for his persecutors to our Lord Jesus Christ Your Son; who lives and reigns with You in the unity of the Holy Spirit, God, world without end',
 'se':'Receive, O Lord, these gifts in commemoration of Your saints, that, as their passion made them glorious, so our devotion may make us blameless',
 'pc':'May the mysteries we have received help us, O Lord, and, by the intercession of blessed Stephen Your martyr, strengthen us with everlasting protection'}
EN['S0117']={'or':'May the intercession of blessed Anthony the Abbot, we beseech You, O Lord, commend us to You, that what we cannot obtain by our own merits we may obtain by his patronage',
 'se':'May saint Anthony the Abbot, we beseech You, O Lord, ask that the sacrifices laid upon Your holy altars may avail for our salvation',
 'pc':'May blessed Anthony the Abbot, interceding for us, protect us, O Lord, together with the reception of Your sacrament, that we may both experience the excellence of his way of life and receive the help of his intercession'}
EN.setdefault('S0128',{}).update({'se':SE_PRAESTA,'pc':PC_QUAESUMUS.format(n='Peter')})
EN.setdefault('S0204',{}).update({'se':'May our devotion be acceptable in Your sight, O Lord, and may it become saving for us through the supplication of him on whose feast it is offered',
 'pc':'Grant, we beseech You, O Lord, to Your faithful ever to rejoice in the veneration of Your saints and to be defended by their unceasing intercession'})
EN.setdefault('S0208',{}).update({'se':SE_PRAESTA,'pc':PC_QUAESUMUS.format(n='John')})
EN['S0712']={'or':'May the intercession of blessed John the Abbot, we beseech You, O Lord, commend us to You, that what we cannot obtain by our own merits we may obtain by his patronage',
 'se':SE_PRAESTA,
 'pc':'May blessed John the Abbot, interceding for us, protect us, O Lord, together with the reception of Your sacrament, that we may both experience the excellence of his way of life and receive the help of his intercession'}
EN['S0714']={'or':ECOLL_DOC%'Bonaventure',
 'se':'May the loving prayer of saint Bonaventure, Your confessor and bishop, not fail us, O Lord, that it may make our gifts acceptable and ever obtain for us Your pardon',
 'pc':'That Your sacrifices may give us salvation, O Lord, may blessed Bonaventure, Your confessor and bishop, we beseech You, come forward as our advocate'}
EN.setdefault('S1124',{}).update({'or':'O God, who made saint John, Your confessor and doctor, an outstanding lover of perfect self-denial and of the Cross, grant that, ever cleaving to his example, we may attain everlasting glory'})
