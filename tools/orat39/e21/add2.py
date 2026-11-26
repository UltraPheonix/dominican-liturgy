import json,sys
sys.path.insert(0,'.')
from en_common import *
X=json.load(open('extra_final.json')); E=json.load(open('en_final.json'))
new={
'S0504':{'p':'430-431','or':'Deus mœréntium consolátor, et in te sperántium salus; qui beátæ Mónicæ pias lácrymas in conversióne fílii sui Augustíni misericórditer suscepísti: da nobis utriúsque intervéntu, peccáta nostra deploráre; et grátiæ tuæ indulgéntiam inveníre: Per Dóminum.',
 'se':'Accépta tibi sit, Dómine, sacrátæ plebis oblátio pro tuórum honóre Sanctórum, quorum se méritis de tribulatióne percepísse cognóscit auxílium. Per Dóminum.',
 'pc':'Satiásti Dómine famíliam tuam munéribus sacris: ejus, quǽsumus, semper interventióne nos réfove; cujus solémnia celebrámus: Per Dóminum.'},
'S0703':{'p':'476-478 (28 Junii)','or':'Deus, qui beáto Irenǽo Mártyri tuo atque Pontífici tribuísti, ut et veritáte doctrínæ expugnáret hǽreses, et pacem Ecclésiæ felíciter confirmáret: da, quǽsumus, plebi tuæ in sancta religióne constántiam; et pacem tuam nostris concéde tempóribus. Per Dóminum.',
 'se':'Deus, qui credéntes in te pópulos nullis sinis cóncuti terróribus: dignáre preces et hóstias dicátæ tibi plebis suscípere, ut pax a tua pietáte concéssa, christianórum fines ab omni hoste fáciat esse secúros. Per Dóminum.',
 'pc':'Deus auctor pacis et amátor, quem nosse, vívere, cui servíre, regnáre est: prótege ab ómnibus impugnatiónibus súpplices tuos; ut, qui in defensióne tua confídimus, beáti Irenǽi Mártyris tui atque Pontíficis intercessióne, nullíus hostilitátis arma timeámus. Per Dóminum.'},
'S0729':{'p':'508-509','or':'Exáudi nos Deus salutáris noster: ut sicut de beátæ Marthæ Vírginis tuæ festivitáte gaudémus; ita piæ devotiónis erudiámur afféctu: Per Dóminum.',
 'se':'Accépta tibi sit, Dómine, sacrátæ plebis oblátio pro tuórum honóre Sanctórum, quorum se méritis de tribulatióne percepísse cognóscit auxílium. Per Dóminum.',
 'pc':'Satiásti Dómine famíliam tuam munéribus sacris: ejus, quǽsumus, semper interventióne nos réfove; cujus solémnia celebrámus: Per Dóminum.'},
'S0812':{'p':'525-526','or':'Fámulos tuos, quǽsumus Dómine, beátæ Vírginis tuæ Claræ votíva natalítia recenséntes; cæléstium gaudiórum sua fácias interventióne partícipes, et tui Unigéniti coherédes: Qui tecum vivit.',
 'se':'Accépta tibi sit, Dómine, sacrátæ plebis oblátio pro tuórum honóre Sanctórum, quorum se méritis de tribulatióne percepísse cognóscit auxílium. Per Dóminum.',
 'pc':'Satiásti Dómine famíliam tuam munéribus sacris: ejus, quǽsumus, semper interventióne nos réfove; cujus solémnia celebrámus: Per Dóminum.'},
'S1202':{'p':'325-326','or':'Indulgéntiam nobis, quǽsumus Dómine, beáta Bibiána Virgo et Martyr implóret: quæ tibi grata semper éxstitit; et mérito castitátis, et tuæ professióne virtútis: Per Dóminum.',
 'se':'Súscipe Dómine múnera, quæ in beátæ Bibiánæ Vírginis et Mártyris tuæ solemnitáte deférimus: cujus nos confídimus patrocínio liberári. Per Dóminum.',
 'pc':'Auxiliéntur nobis, Dómine, sumpta mystéria; et intercedénte beáta Bibiána Vírgine et Mártyre tua, sempitérna protectióne confírment: Per Dóminum.'},
'S0508':{'p':'455-457 (31 Maii)','or':'Dómine Jesu Christe, noster apud Patrem mediátor, qui beatíssimam Vírginem matrem tuam, matrem quoque nostram et apud te mediatrícem constitúere dignátus es: concéde propítius, ut quisquis ad te benefícia petitúrus accésserit; cuncta se per eam impetrásse lætétur: Qui vivis et regnas cum eódem Deo Patre.',
 'se':'Matris tuæ ac Mediatrícis nostræ précibus, Dómine, quǽsumus, hæc hostiárum oblátio nosmetípsos, tua grátia largiénte, tibi perfíciat munus ætérnum: Qui vivis.',
 'pc':'Subvéniat nobis, Dómine, beátæ Maríæ matris tuæ ac nostræ Mediatrícis orátio: ut per hæc sacrosáncta commércia, tua grátia largiénte; ad redemptiónis ætérnæ proficiámus augméntum: Qui vivis.'},
'S0910':{'p':'457-459 (1 Junii)','or':'Deus, qui nos beatórum Alphónsi et sociórum ejus triúmpho lætíficas; da nobis, quǽsumus, eórum méritis et intercessióne, eámdem in fide constántiam, et in ópere efficáciam: Per Dóminum.',
 'se':'Hóstias tibi Dómine offérimus in tuórum solemnitáte Beatórum, humíliter deprecántes, ut sicut illos pássio gloriósos effécit, ita et nos devótio reddat accéptos. Per Dóminum.',
 'pc':'Præsta, quǽsumus omnípotens Deus, ut qui beatórum Mártyrum tuórum memóriam recólimus: eórum quoque fidem et fortitúdinem æmulémur; hostiúmque nostrórum adversitátibus superátis, ætérni tui nóminis confessióne lætémur: Per Dóminum.'},
'S0111b':{'p':'384-385','or':'Deus, qui beátum Bernárdum a sǽculi vítiis revocátum, in viam perfectiónis traduxísti: ejus méritis et précibus concéde; ut nos peccáta nostra defléntes, ad te puris méntibus convertámur: Per Dóminum.',
 'se':'Súscipe, quǽsumus Dómine, munus oblátum: et nobis cleménter indúlge, ut beáti Bernárdi exémpla æmulántes, usque in finem in tuo constánter simus amóre fervéntes. Per Dóminum.',
 'pc':'Cæléstis convívii pasti delíciis, supplíciter te Dómine deprecámur: ut beáti Bernárdi, cujus hódie memóriam fácimus, intercessióne; salutárium bonórum ubertáte repléri mereámur: Per Dóminum.'},
}
en={
'S0504':{'or':'O God, the consoler of the sorrowful and the salvation of those who hope in You, who mercifully accepted the loving tears of blessed Monica for the conversion of her son Augustine; grant us, through the intercession of them both, to bewail our sins and to find the pardon of Your grace','se':SE_ACCEPTA,'pc':PC_SATIASTI},
'S0703':{'or':'O God, who granted to blessed Irenaeus, Your martyr and bishop, both to overcome heresies by the truth of his teaching and happily to establish peace in the Church; give, we beseech You, to Your people constancy in holy religion, and grant Your peace in our times',
 'se':'O God, who do not let the peoples who believe in You be shaken by any terrors, deign to receive the prayers and offerings of the people dedicated to You, that the peace granted by Your goodness may make the borders of Christians safe from every enemy',
 'pc':'O God, the author and lover of peace, to know whom is to live, to serve whom is to reign, protect Your suppliants from all assaults, that we who trust in Your defence may, through the intercession of blessed Irenaeus, Your martyr and bishop, fear the arms of no enemy'},
'S0729':{'or':'Hear us, O God our Saviour, that as we rejoice in the feast of blessed Martha, Your virgin, so we may be taught the spirit of loving devotion','se':SE_ACCEPTA,'pc':PC_SATIASTI},
'S0812':{'or':'We beseech You, O Lord, that Your servants who keep the feast of the birthday of blessed Clare, Your virgin, may by her intercession be made partakers of heavenly joys and co-heirs of Your only-begotten Son','se':SE_ACCEPTA,'pc':PC_SATIASTI},
'S1202':{'or':'May blessed Bibiana, virgin and martyr, we beseech You, O Lord, implore pardon for us, she who was ever pleasing to You both by the merit of her chastity and by the confession of Your power',
 'se':'Receive, O Lord, the gifts we bring on the feast of blessed Bibiana, Your virgin and martyr, by whose patronage we trust to be delivered',
 'pc':'May the mysteries we have received help us, O Lord, and, through the intercession of blessed Bibiana, Your virgin and martyr, strengthen us with everlasting protection'},
'S0508':{'or':'O Lord Jesus Christ, our mediator with the Father, who have deigned to appoint the most blessed Virgin, Your Mother, to be our mother also and our mediatrix with You; mercifully grant that whoever comes to You seeking favors may rejoice to have obtained them all through her',
 'se':'By the prayers of Your Mother and our Mediatrix, we beseech You, O Lord, may the offering of this sacrifice, by the gift of Your grace, make of ourselves an everlasting offering to You',
 'pc':'May the prayer of blessed Mary, Your Mother and our Mediatrix, help us, O Lord, that through these most holy mysteries, by the gift of Your grace, we may advance towards the increase of eternal redemption'},
'S0910':{'or':'O God, who gladden us by the triumph of the blessed Alphonsus and his companions; grant us, we beseech You, by their merits and intercession, the same constancy in faith and fruitfulness in work',
 'se':'We offer You sacrifices, O Lord, on the feast of Your blessed ones, humbly beseeching You that, as their passion made them glorious, so our devotion may make us acceptable',
 'pc':'Grant, we beseech You, almighty God, that we who keep the memory of Your blessed martyrs may also imitate their faith and fortitude, and, having overcome the attacks of our enemies, may rejoice in the confession of Your eternal name'},
'S0111b':{'or':'O God, who called blessed Bernard back from the vices of the world and led him into the way of perfection; grant by his merits and prayers that we, bewailing our sins, may turn to You with pure minds',
 'se':'Receive, we beseech You, O Lord, the gift we offer, and mercifully grant that, following the example of blessed Bernard, we may be steadfastly fervent in Your love to the end',
 'pc':'Fed with the delights of the heavenly banquet, we humbly pray You, O Lord, that through the intercession of blessed Bernard, whose memory we keep today, we may deserve to be filled with the abundance of saving gifts'},
}
X.update(new); E.update(en)
json.dump(X,open('extra_final.json','w'),ensure_ascii=False,indent=1)
json.dump(E,open('en_final.json','w'),ensure_ascii=False,indent=1)
print('ok',len(X))
