import sys; sys.path.insert(0,'/tmp/A5')
from fx import *
LC=' Per Dóminum nostrum Iesum Christum, Fílium tuum: qui tecum vivit et regnat in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum.'
EC='; through our Lord Jesus Christ, Your Son, who lives and reigns with You in the unity of the Holy Spirit, God, world without end.'
# ---------- C7s: chants and readings are those of the Missal's Martyr-Bishop Mass Laetabitur (pp. 5*-6*); the orations were those of the Martyr-non-Bishop Mass (pp. 9*-10*)
S='M39 pp. 5*-6* (pdf 370-371)'
orat_set('C7s','or','Lætétur Ecclésia tua, Deus, beáti N. Mártyris tui atque Pontíficis confísa suffrágiis: atque eius précibus gloriósis, et devóta permáneat; et secúra consístat:'+LC,
  'Helped by the prayers of blessed N., Your martyr and bishop, may Your Church be glad, O Lord; and through his glorious intercession may she abide in loyalty and stand unshaken'+EC,S,'wrong Mass: the Collect of the Martyr-non-Bishop Mass (p. 9*) stood here; the Missal prints Lætétur for this Mass (English: St Dominic Missal 1959, Ember Saturday of September, commemoration)')
orat_set('C7s','se','Súscipe Dómine múnera, quæ in eius tibi solemnitáte deférimus, cuius nos confídimus patrocínio liberári.'+LC,
  'Receive, O Lord, these offerings which we make on the feast of him through whose patronage we trust to be made free'+EC,S,'wrong Mass: Secret of p. 10* replaced by the Missal\'s Secret of this Mass, p. 6* (English: St Dominic Missal 1959, Holy Guardian Angels, commemoration of St Leger)')
orat_set('C7s','pc','Satiásti Dómine famíliam tuam munéribus sacris: eius, quǽsumus, semper interventióne nos réfove; cuius solémnia celebrámus:'+LC,
  'You have filled Your household, O Lord, with sacred gifts; ever refresh us, we beseech You, by the intercession of him whose feast we celebrate'+EC,S,'wrong Mass: Postcommunion of p. 10* replaced by the Missal\'s Postcommunion of this Mass, p. 6* (English as for C55s, him for her)')
orsrc('C7s','Missale O.P. (1939), pp. 5*-6* (In festo unius Martyris Pontificis extra tempus Paschale); English after the St Dominic Missal (1959)','orations now from the Mass whose chants and readings the page shows')
rd('C7s',1,'la',[('ei, dicéntes: Quia','ei, dicéntes, Quia'),('rogat ea quæ pacis','rogat ea, quæ pacis')],'M39 p. 6* (pdf 371)','punctuation as printed')
# ---------- Commune pp. 7*-11* (pdf 371-373), every edit checked on the scan
for k,n in [('C11s',371),('C15s',372),('C18s',373)]:
    auto_rd(k,n)
rd('C11s',0,'la',[('et ter Dómini','et Pater Dómini'),('sic éritis et consolatiónis.','sic éritis et consolatiónis: In Christo Jesu Dómino nostro.')],'M39 p. 7* (pdf 371)','word as printed (Pater); ending as printed')
rd('C15s',1,'la',[('fructum multum, quia','fructum multum: quia')],'M39 p. 8* (pdf 372)','punctuation as printed')
rd('C18s',0,'la',[('áffuit','ádfuit'),('claritátem ætérnam.','claritátem ætérnam, Dóminus Deus noster.')],'M39 p. 10* (pdf 373)','spelling as printed; ending as printed')
# ---------- C21s Plurimorum Martyrum, pp. 12*-14* (pdf 374-375), checked on the scan
rd('C21s',0,'la',[('laudavérunt páriter.','laudavérunt páriter, Dómine Deus noster.')],'M39 p. 13* (pdf 374)','ending as printed')
rd('C21s',1,'la',[('inícient','injícient'),('respondeátis: ego enim','respondeátis. Ego enim')],'M39 pp. 13*-14* (pdf 374-375)','word as printed (injícient); punctuation as printed')
# ---------- C25s Plurimorum Martyrum alia Missa, pp. 14*-15* (pdf 375)
rd('C25s',0,'la',[('judícium certum: sumet scutum inexpugnábile, æquitátem.','judícium certum. Sumet scutum inexpugnábile æquitátem.')],'M39 p. 14* (pdf 375)','punctuation as printed')
# ---------- C28s Plurimorum Martyrum T.P., pp. 15*-17* (pdf 375-376)
rd('C28s',0,'la',[('in cælo dicéntium: Allelúja: salus','in cælo dicéntium, Allelúja: salus'),('dixérunt: Allelúja.','dixérunt, Allelúja.'),('dicéntes: Amen: allelúja.','dicéntes, Amen, allelúja.'),('magnórum, dicéntium: Allelúja','magnórum, dicéntium, Allelúja'),('ad cœnam','ad cenam')],'M39 p. 16* (pdf 376)','punctuation and spelling (cenam) as printed')
rd('C28s',1,'la',[('fructum multum, quia','fructum multum: quia'),('non mánserit, mittétur','non mánserit: mittétur'),('mánserint, quodcúmque','mánserint: quodcúmque')],'M39 p. 16* (pdf 376)','punctuation as printed')
# ---------- C30s Confessoris Pontificis (first Mass, Sacerdotes), pp. 17*-18* (pdf 376-377)
rd('C30s',0,'la',[('deínde pro constítuet eum. Pópuli: hoc','deínde pro pópuli: hoc'),('seípsum offeréndo.','seípsum offeréndo, Jesus Christus Dóminus noster.')],'M39 p. 17* (pdf 376)','stray words "constítuet eum." (the Gospel\'s last words) removed; ending as printed')
rd('C30s',1,'la',[('super ómnia bona sua','super ómnia bona sua constítuet eum.')],'M39 p. 18* (pdf 377)','missing ending as printed')
title('C30s','Commune Confessoris Pontificis','M39 pp. 17*-18* (pdf 376-377)','this is the first Mass (Sacerdotes); the Missal\'s "alia Missa" is Statuit (C32s)')
cur('data/masses.js',['masses','C30s','en']); setv('data/masses.js',['masses','C30s','en'],'Common of a Confessor Bishop','M39 pp. 17*-18* (pdf 376-377)','English of the corrected title')
orsrc('C30s','Missale O.P. (1939), pp. 17*-18* (Confessoris Pontificis); English after the St Dominic Missal (1959), checked against the Latin','pages as printed')
def rdall(k,i,a,b,n,src,why):
    s=cur('data/readings33.js',[k,i,'la'])
    if s.count(a)!=n: raise Exception(f'{k}.rd{i}: "{a}" occurs {s.count(a)} times, expected {n}')
    setv('data/readings33.js',[k,i,'la'],s.replace(a,b),src,why)
# ---------- C32s Confessoris Pontificis alia Missa (Statuit), pp. 18*-20* (pdf 377-378)
rd('C32s',0,'la',[('géntium dedit illi, et testaméntum','géntium dedit illi: et testaméntum'),('misericórdiam suam: et invénit','misericórdiam suam, et invénit'),('testaméntum ætérnum, et dedit','testaméntum ætérnum: et dedit'),('sacerdótium magnum: et beatificávit','sacerdótium magnum, et beatificávit'),('in nómine ipsíus, et offérre','in nómine ipsíus: et offérre')],'M39 pp. 18*-19* (pdf 377)','punctuation as printed')
rd('C32s',1,'la',[('vocávit servos suos, et trádidit','vocávit servos suos et trádidit'),('própriam virtútem: et proféctus','própriam virtútem, et proféctus')],'M39 pp. 19*-20* (pdf 377-378)','punctuation as printed')
rdall('C32s',1,'et fidélis: quia super pauca fuísti fidélis, super multa te constítuam: intra','et fidélis, quia super pauca fuísti fidélis, super multa te constítuam, intra',2,'M39 pp. 19*-20* (pdf 377-378)','punctuation as printed')
title('C32s','Commune Confessoris Pontificis (alia Missa)','M39 p. 18* (pdf 377)','the Missal prints this Mass (Statuit) as "In eodem festo alia Missa"; the first Mass is Sacerdotes (C30s)')
cur('data/masses.js',['masses','C32s','en']); setv('data/masses.js',['masses','C32s','en'],'Common of a Confessor Bishop (another Mass)','M39 p. 18* (pdf 377)','English of the corrected title')
orsrc('C32s','Missale O.P. (1939), pp. 18*-20* (Confessoris Pontificis, alia Missa); English after the St Dominic Missal (1959), checked against the Latin','pages as printed')
# ---------- C35s Unius Doctoris, pp. 20*-21* (pdf 378)
rd('C35s',0,'la',[('vivos et mórtuos','vivos, et mórtuos'),('in illa die, justus judex','in illa die justus judex')],'M39 p. 20* (pdf 378)','punctuation as printed')
rd('C35s',1,'la',[('montem pósita: neque','montem pósita. Neque'),('lúceat ómnibus qui in domo','lúceat ómnibus, qui in domo'),('Nolíte putáre quóniam veni sólvere legem aut prophétas','Nolíte putáre, quóniam veni sólvere legem, aut prophétas'),('dico vobis, donec','dico vobis: donec')],'M39 p. 21* (pdf 378)','punctuation as printed')
# ---------- C42s Confessoris non Pontificis alia Missa (Os justi), pp. 23*-24* (pdf 379-380)
rd('C42s',1,'la',[('dóminum suum quando revertátur','dóminum suum, quando revertátur'),('cum vénerit et pulsáverit','cum vénerit, et pulsáverit')],'M39 p. 24* (pdf 380)','punctuation as printed')
# ---------- C45s Virginis et Martyris (Loquebar), pp. 26*-28* (pdf 381-382)
rd('C45s',0,'la',[('Dómine Deus meus, exaltásti','Dómine Deus meus exaltásti'),('defluénte deprecátus sum','defluénte deprecáta sum'),('laudem dicam tibi.','laudem dicam tibi, Dómine Deus noster.')],'M39 p. 27* (pdf 381)','word as printed (deprecáta); punctuation and ending as printed')
rd('C45s',1,'la',[('secus littus','secus litus')],'M39 p. 27* (pdf 381)','spelling as printed')
# ---------- C48s Virginis et Martyris alia Missa (Me exspectaverunt), pp. 28*-29* (pdf 382)
rd('C48s',0,'la',[('tribulatiónum quæ circumdedérunt','tribulatiónum, quæ circumdedérunt'),('non sum æstuátus','non sum æstuáta'),('sustinéntes te et líberas','sustinéntes te, et líberas'),('de mánibus géntium.','de mánibus géntium, Dómine Deus noster.')],'M39 p. 28* (pdf 382)','word as printed (æstuáta); punctuation and ending as printed')
rd('C48s',1,'la',[('lámpades suas exiérunt','lámpades suas, exiérunt'),('dormitavérunt omnes et dormiérunt','dormitavérunt omnes, et dormiérunt')],'M39 p. 29* (pdf 382)','punctuation as printed')
# ---------- C51s (Virg. non Mart., Gaudeamus, pp. 30*-31*, pdf 383): readings only; orations stay OPEN (wrong Mass)
rd('C51s',0,'la',[('sed et supportáre me','sed et supportáte me'),('uni viro, vírginem','uni viro vírginem')],'M39 p. 30* (pdf 383)','word as printed (supportáte); punctuation as printed')
rd('C51s',1,'la',[('lámpades suas exiérunt','lámpades suas, exiérunt'),('dormitavérunt omnes et dormiérunt','dormitavérunt omnes, et dormiérunt'),('Date nobis óleo vestro','Date nobis de óleo vestro')],'M39 pp. 30*-31* (pdf 383)','missing word "de" as printed; punctuation as printed')
# ---------- C55s (Virg. non Mart. alia Missa, Dilexisti, pp. 31*-33*, pdf 383-384): readings only; title stays OPEN
rd('C55s',0,'la',[('non peccávit: tribulatiónem','non peccávit. Tribulatiónem'),('innúpta, et virgo, cógitat','innúpta, et virgo cógitat'),('córpore, et spíritu.','córpore, et spíritu: In Christo Jesu Dómino nostro.')],'M39 pp. 31*-32* (pdf 383-384)','punctuation and ending as printed')
rd('C55s',1,'la',[('secus littus','secus litus')],'M39 p. 32* (pdf 384)','spelling as printed')
# ---------- C62s votive De SS. Corpore Christi, pp. 40*-42* (pdf 388-389); orations were Divinum Officium's (Tempora/Pent01-4)
S62='M39 pp. 41*-42* (pdf 388-389)'
orat('C62s','or',[('sub Sacraménto mirábili passiónis','sub Sacraménto mirábili, passiónis'),('ita nos Córporis et Sánguinis tui','ita nos córporis et sánguinis tui')],S62,'punctuation and words as printed (p. 41*)')
orat('C62s','se',[('Ecclésiæ tuæ, quǽsumus, Dómine, unitátis','Ecclésiæ tuæ, quǽsumus Dómine, unitátis')],S62,'punctuation as printed (p. 42*)')
orat('C62s','pc',[('Fac nos, quǽsumus, Dómine,','Fac nos, quǽsumus Dómine,'),('fruitióne repléri: quam pretiósi Corporis et Sanguinis tui temporalis','fruitióne repléri; quam pretiósi córporis et sánguinis tui temporális')],S62,'punctuation and words as printed (p. 42*); \';\' is the flexa (Proc. 1913 p. 405)')
orsrc('C62s','Missale O.P. (1939), pp. 40*-42* (De SS. Corpore Christi)','orations checked on the Missal; the src named Divinum Officium')
rd('C62s',0,'la',[('postquam cœnávit','postquam cenávit'),('in meo sánguine: hoc fácite quotiescúmque','in meo sánguine: hoc fácite, quotiescúmque'),('et cálicem bibétis, mortem','et cálicem bibétis: mortem'),('Itaque quicúmque','Itaque quicúmque manducáverit panem hunc, vel bíberit cálicem Dómini indígne: reus erit córporis, et sánguinis Dómini. Probet autem seípsum homo: et sic de pane illo edat, et de cálice bibat. Qui enim mandúcat, et bibit indígne, judícium sibi mandúcat, et bibit: non dijúdicans corpus Dómini.')],'M39 p. 41* (pdf 388)','reading cut at a page break: completed to v. 29 as printed (= W-E3 entry); spelling (cenávit) and punctuation as printed')
rdset('C62s',0,'ref','Ad Corinthios 1 11: 23-29','M39 p. 41* (pdf 388)','reference of the full reading (as masses.js already gives)')
rd('C62s',1,'la',[('Caro mea, vere est cibus: et sanguis meus, vere est potus: qui','Caro mea vere est cibus: et sanguis meus vere est potus. Qui')],'M39 pp. 41*-42* (pdf 388-389)','punctuation as printed')
# ---------- C64s votive De D.N.J.C. Summo et Aeterno Sacerdote, pp. 42*-44* (pdf 389-390)
rd('C64s',0,'la',[('ut póntifex fíeret: sed qui','ut póntifex fíeret, sed qui'),('locútus est ad eum.','locútus est ad eum: Fílius meus es tu; ego hódie génui te. Quemádmodum et in álio loco dicit: Tu es Sacérdos in ætérnum secúndum órdinem Melchísedech. Qui in diébus carnis suæ preces supplicationésque ad eum, qui possit illum salvum fácere a morte, cum clamóre válido et lácrymis ófferens, exaudítus est pro sua reveréntia. Et quidem, cum esset Fílius Dei, dídicit ex iis, quæ passus est, obediéntiam: et consummátus, factus est ómnibus obtemperántibus sibi, causa salútis ætérnæ, appellátus a Deo póntifex juxta órdinem Melchísedech. De quo nobis grandis sermo, et ininterpretábilis ad dicéndum.')],'M39 pp. 42*-43* (pdf 389)','reading cut at a page break: completed to v. 11 as printed; punctuation as printed')
rdset('C64s',0,'ref','Ad Hebræos 5: 1-11','M39 pp. 42*-43* (pdf 389)','reference of the full reading (as masses.js already gives)')
rd('C64s',1,'la',[('Et accépto cálice grátias','Et accépto cálice, grátias'),('generatióne vitis donec','generatióne vitis, donec'),('Et accépto pane grátias','Et accépto pane, grátias'),('postquam cœnávit','postquam cenávit')],'M39 p. 43* (pdf 389)','punctuation and spelling (cenávit) as printed')
# ---------- C68s De Quinque Stigmatibus, pp. 46*-47* (pdf 391): readings only; orations OPEN (they are De Pœnis's, 48*-50*)
rd('C68s',0,'la',[('Dicit Dóminus: Effúndam','Hæc dicit Dóminus: Effúndam'),('spíritum grátiæ, et precum','spíritum grátiæ et precum'),('planctus in Jerúsalem, Et dicétur','planctus in Jerúsalem. Et dicétur'),('et dispergéntur oves.','et dispergéntur oves. Ait Dóminus omnípotens.')],'M39 p. 46* (pdf 391)','opening word and ending as printed; punctuation as printed')
rd('C68s',1,'la',[('inclináto cápite trádidit','inclináto cápite, trádidit'),('Judǽi ergo (quóniam parascéve erat)','Judǽi ergo, (quóniam Parascéve erat)'),('córpora sábbato (erat enim magnus dies ille sábbati), rogavérunt','córpora sábbato, (erat enim magnus dies ille Sábbati) rogavérunt')],'M39 p. 47* (pdf 391)','punctuation as printed')
# ---------- C75s votive De Spiritu Sancto extra Septuagesimam, pp. 53*-54* (pdf 394-395); orations were Divinum Officium's (Pentecost)
S75='M39 pp. 53*-54* (pdf 394-395)'
orat('C75s','or',[('Deus, qui hodiérna die corda','Deus, qui corda'),('consolatióne gaudére. Per','consolatióne gaudére: Per')],S75,'the votive Collect has no "hodiérna die" (p. 53*; the Preface rubric p. 54* likewise says "omissis verbis hodiérna die"); punctuation as printed')
orat('C75s','se',[('Múnera, quǽsumus, Dómine,','Múnera, quǽsumus Dómine,')],S75,'punctuation as printed (p. 54*)')
orat('C75s','pc',[('mundet infúsio: et sui','mundet infúsio; et sui'),('fecúndet. Per','fecúndet: Per')],S75,'punctuation as printed (p. 54*); \';\' is the flexa (Proc. 1913 p. 405)')
orsrc('C75s','Missale O.P. (1939), pp. 53*-54* (De Spiritu Sancto, extra Septuagesimam)','orations checked on the Missal; the src named Divinum Officium')
rd('C75s',0,'la',[('Petrum, et Joánnem','Petrum et Joánnem')],'M39 p. 53* (pdf 394)','punctuation as printed')
rd('C75s',1,'la',[('loquar vobíscum: venit enim','loquar vobíscum. Venit enim')],'M39 p. 54* (pdf 395)','punctuation as printed')
# ---------- C79s votive B. M. V. III (a Purificatione usque ad Adventum), pp. 57*-59* (pdf 396-397); orations were Divinum Officium's (Commune/C11)
S79='M39 pp. 58*-59* (pdf 397)'
orat('C79s','or',[('quǽsumus, Dómine Deus,','quǽsumus Dómine Deus,'),('córporis sanitáte gaudére: et, gloriósa','córporis salúte gaudére: et gloriósa'),('liberári tristítia, et ætérna','liberári tristítia; et ætérna'),('pérfrui lætítia. Per','pérfrui lætítia: Per')],S79,'word as printed (salúte, not sanitáte) and punctuation as printed (p. 58*); \';\' is the flexa (Proc. 1913 p. 405)')
orat('C79s','pc',[('obtúlimus maiestáti. Per','obtúlimus maiestáti: Per')],S79,'punctuation as printed (p. 59*)')
orsrc('C79s','Missale O.P. (1939), pp. 57*-59* (De sancta Maria in Sabbato, III: a Purificatione usque ad Adventum)','orations checked on the Missal; the src named Divinum Officium')
rd('C79s',0,'la',[('Inítio, et ante','Ab inítio, et ante')],'M39 p. 58* (pdf 397)','first word "Ab" as printed')
rd('C79s',1,'la',[('múlier de turba dixit','múlier de turba, dixit')],'M39 p. 58* (pdf 397)','punctuation as printed')
# ---------- C82s Missa privilegiata votiva SS. Rosarii, pp. 59*-61* (pdf 397-398)
S82='M39 pp. 59*-61* (pdf 397-398)'
orat('C82s','or',[('tibi coæquálem atque','tibi coæquálem, atque'),('sanctificatiónis, Dóminum','sanctificatiónis Dóminum'),('præelegísti: præsta, quǽsumus,','præelegísti: præsta quǽsumus,')],S82,'punctuation as printed (p. 59*)')
orat('C82s','se',[('Annue, quǽsumus, miséricors','Annue, quǽsumus miséricors'),('placeámus: ut, dum','placeámus: ut dum')],S82,'punctuation as printed (pp. 60*-61*)')
rdset('C82s',0,'la','Ego flos campi, et lílium convállium. Sicut lílium inter spinas, sic amíca mea inter fílias. Favus distíllans lábia tua sponsa, mel et lac sub lingua tua: et odor vestimentórum tuórum sicut odor thuris. Hortus conclúsus, soror mea sponsa, hortus conclúsus, fons signátus. Emissiónes tuæ, paradísus malórum punicórum cum pomórum frúctibus. Ego quasi vitis fructificávi suavitátem odóris: et flores mei fructus honóris et honestátis. Ego mater pulchræ dilectiónis, et timóris, et agnitiónis, et sanctæ spei. In me grátia omnis viæ et veritátis, in me omnis spes vitæ et virtútis. Transíte ad me omnes qui concupíscitis me, et a generatiónibus meis implémini: Spíritus enim meus super mel dulcis, et heréditas mea super mel et favum.','M39 pp. 59*-60* (pdf 397-398)','the Missal\'s Lesson is "Cant. 2 et 4 Eccli. 24": it opens with Cant 2 and 4 ("Ego flos campi"), which were missing (the site began with the garbled "Og quasi vitis"), and ends at "super mel et favum" (the site added Eccli 24: 28-31 and read "mei" for "mel")')
rdset('C82s',0,'ref','Canticum 2: 1-2; 4: 11-13; Ecclesiasticus 24: 23-27','M39 p. 59* (pdf 397)','the Missal prints "Cant. 2 et 4 Eccli. 24"')
rd('C82s',1,'la',[('per civitátes, et castélla','per civitátes et castélla'),('spirítibus malígnis, et infirmitátibus','spirítibus malígnis et infirmitátibus'),('semináre semen suum. Et dum séminat, áliud cécidit secus viam, et conculcátum','semináre semen suum: et dum séminat, áliud cécidit secus viam: et conculcátum'),('Hæc dicens clamábat','Hæc dicens, clamábat')],'M39 p. 60* (pdf 398)','punctuation as printed')
# ---------- C85s Ad tollendum schisma, pp. 66*-68* (pdf 401-402)
rd('C85s',0,'la',[('immundítiæ omnis in avarítiam','immundítiæ omnis, in avarítiam'),('sicut est véritas in','sicut est véritas in Christo Jesu Dómino nostro.')],'M39 p. 67* (pdf 401)','reading cut at a page break: ending as printed (= W-E3 entry); punctuation as printed')
# ---------- C89s Pro eligendo summo Pontifice, pp. 68*-70* (pdf 402-403)
rd('C89s',0,'la',[('ófferat dona, et sacrifícia','ófferat dona et sacrifícia'),('preces, supplicationésque','preces supplicationésque')],'M39 p. 69* (pdf 402)','punctuation as printed')
rd('C89s',1,'la',[('Si dilígitis me, mandáta','Si dilígitis me: mandáta'),('nec scit eum: vos autem cognoscétis eum, quia apud','nec scit eum. Vos autem cognoscétis eum: quia apud'),('Adhuc módicum, et mundus','Adhuc módicum: et mundus')],'M39 pp. 69*-70* (pdf 402-403)','punctuation as printed')
# ---------- C93s Pro Fidei Propagatione, pp. 70*-72* (pdf 403-404); orations were Divinum Officium's (Commune/Propaganda)
S93='M39 pp. 71*-72* (pdf 403-404)'
orat('C93s','or',[('Dóminum nostrum. Qui tecum','Dóminum nostrum: Qui tecum')],S93,'punctuation as printed (p. 71*); conclusion "Qui tecum" as printed')
orat('C93s','se',[('Protéctor noster, áspice, Deus, et','Protéctor noster áspice Deus, et'),('sacrificétur, et offerátur','sacrificétur et offerátur')],S93,'punctuation as printed (p. 72*)')
orsrc('C93s','Missale O.P. (1939), pp. 70*-72* (Pro Fidei Propagatione)','orations checked on the Missal; the src named Divinum Officium')
rd('C93s',0,'la',[('Miserére nostri Deus','Miserére nostri, Deus'),('nos cognóvimus quóniam','nos cognóvimus, quóniam'),('præter te Dómine.','præter te, Dómine.'),('sciant omnes qui hábitant','sciant omnes, qui hábitant')],'M39 p. 71* (pdf 403)','punctuation as printed')
rd('C93s',1,'la',[('pro régibus, et ómnibus, qui in sublimitáte sunt, ut quiétam, et tranquíllam vitam agámus in omni pietáte, et castitáte: hoc enim','pro régibus et ómnibus qui in sublimitáte sunt, ut quiétam et tranquíllam vitam agámus, in omni pietáte, et castitáte; hoc enim'),('Dei et hóminum homo','Dei et hóminum, homo'),('prædicátor, et Apóstolus (veritátem dico, non méntior) doctor géntium in fide, et veritáte.','prædicátor et apóstolus (veritátem dico, non méntior), doctor géntium in fide et veritáte.')],'M39 p. 72* (pdf 404)','punctuation as printed')
# ---------- C104s Pro vitanda mortalitate, pp. 90*-91* (pdf 413)
rd('C104s',0,'la',[('super Jerúsalem ut dispérderet','super Jerúsalem, ut dispérderet'),('cóntine manum tuam: erat autem','cóntine manum tuam. Erat autem'),('ad Dóminum cum vidísset','ad Dóminum, cum vidísset'),('egi: isti qui oves','egi: isti, qui oves'),('præcéperat ei Dóminus. Altáre Dómino','præcéperat ei Dóminus: et ædificávit altáre Dómino')],'M39 p. 90* (pdf 413)','missing words "et ædificávit" (v. 25) as printed; punctuation as printed')
rd('C104s',1,'la',[('clamántia, et dicéntia: Quia','clamántia, et dicéntia, Quia'),('detinébant illum ne discéderet','detinébant illum, ne discéderet')],'M39 p. 91* (pdf 413)','punctuation as printed')
# ---------- C110s Pro Sponso et Sponsa, pp. 94*-96* (pdf 415-416)
rd('C110s',0,'la',[('caput est mulíeris, sicut Christus','caput est mulíeris: sicut Christus'),('Viri, dilígite','Viri dilígite'),('relínquet homo patrem, et matrem','relínquet homo patrem et matrem')],'M39 pp. 94*-95* (pdf 415)','punctuation as printed')
rd('C110s',1,'la',[('másculum, et féminam','másculum et féminam'),('dimíttet homo patrem, et matrem','dimíttet homo patrem et matrem')],'M39 p. 95* (pdf 415)','punctuation as printed')
# ---------- C76s De Spiritu Sancto infra Septuagesimam (Cum sanctificatus), p. 54* (pdf 395): "Cetera ut supra" = C75s's readings
rd('C76s',0,'la',[('Petrum, et Joánnem','Petrum et Joánnem')],'M39 p. 53* (pdf 394); p. 54* "Cetera ut supra"','punctuation as printed (same Lesson as C75s)')
rd('C76s',1,'la',[('loquar vobíscum: venit enim','loquar vobíscum. Venit enim')],'M39 p. 54* (pdf 395)','punctuation as printed (same Gospel as C75s)')
# ---------- C39s Confessoris non Pontificis (Justus ut palma), pp. 22*-23* (pdf 379): readings only; orations OPEN (wrong Mass)
rd('C39s',0,'la',[('justítia in fide, ad cognoscéndum','justítia in fide ad cognoscéndum'),('comprehéndam in quo','comprehéndam, in quo')],'M39 p. 22* (pdf 379)','punctuation as printed')
rd('C39s',1,'la',[('Confíteor tibi Pater','Confíteor tibi, Pater'),('a sapiéntibus, et prudéntibus','a sapiéntibus et prudéntibus')],'M39 pp. 22*-23* (pdf 379)','punctuation as printed')
# ---------- Beati: readings identical to a Commune reading, where the Beatus's Missal rubric (seen on the scan crops,
# img/mont*.png) sends the Mass to that Commune page: the same scan-checked correction is carried over.
import json as _json
_A=_json.load(open(ROOT+'tools/audit/fixes/A5.json')) if False else None
def _old_new(ck,i):
    return ORIG[('data/readings33.js',(ck,i,'la'))], CUR[('data/readings33.js',(ck,i,'la'))]
BEATI={
 'C42s':(['S1114b','S1201b','S1216b','S0124b','S0216b','S0217b','S0219b','S0301b','S0320b','S0322b','S0517b','S0612b','S0724b','S0728b','S0730b','S0818b','S0819b','S0906b_2','S0923b','S0926b','S0928b','S1010b','S1011b','S1021b'],'Os justi, ut in Comm. Conf. non Pont., pag. 23*'),
 'C51s':(['S0102b','S0323b','S0413b','S0512b','S0520b','S0723b','S1013b'],'Gaudeamus, ut in Comm. Virg. non Mart., pag. 30*'),
 'C32s':(['S1126b','S0530b','S0610b','S0707b','S0713b','S0803b'],'Statuit, ut in Comm. Conf. Pont., pag. 18*'),
 'C39s':(['S0116b','S0426b','S0823b'],'Justus ut palma, ut in Comm. Conf. non Pont., pag. 22*'),
 'C21s':(['S0529b','S0602b'],'extra T. P. Salus autem, ut in Comm. plurim. Mart., pag. 13*'),
 'C15s':(['S0410b'],'Tempore Paschali, Officium Protexisti, ut in Communi Mart. non Pont., pag. 11*'),
}
for ck,(keys,rub) in BEATI.items():
    for i in range(len(R[ck])):
        k0=('data/readings33.js',(ck,i,'la'))
        if k0 not in ORIG or ORIG[k0]==CUR[k0]: continue
        old,new=ORIG[k0],CUR[k0]
        for b in keys:
            for j,r in enumerate(R.get(b,[])):
                if r['la']==old:
                    rdset(b,j,'la',new,SRC.get(k0,'')+'; rubric on the Beatus\'s page: "Officium %s"'%rub,'same correction as %s (checked on the scan); the Missal sends this Mass to that Commune page'%ck)
