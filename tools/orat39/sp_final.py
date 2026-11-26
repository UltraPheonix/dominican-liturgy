"""Oratio super populum of the Lenten ferias (Ash Wednesday - Wednesday of Holy Week), read from the
Missale O.P. 1939 page images (pdf 62-113; printed page = 2*pdf-66 (+1 right half)). Ember Saturday of Lent:
"Oratio super populum hac die non dicitur" (p. 79). English: our own, after the Latin.
Writes the 'sp' field into data/orations.js: [Latin (i-spelling, conclusion written out), English, page]."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', '..', 'data', 'orations.js')
PD = 'Per Dóminum nostrum Iesum Christum, Fílium tuum: qui tecum vivit et regnat in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum.'
QT = 'Qui tecum vivit et regnat in unitáte Spíritus Sancti Deus per ómnia sǽcula sæculórum.'
EPD = 'through our Lord Jesus Christ, Your Son, who lives and reigns with You in the unity of the Holy Spirit, God, world without end.'
EQT = 'who lives and reigns with You in the unity of the Holy Spirit, God, world without end.'
SP = [
('5aw', 58, 'Inclinántes se, Dómine, majestáti tuæ propitiátus inténde: ut qui divíno múnere sunt refécti; cæléstibus semper nutriántur auxíliis',
 'Look graciously, O Lord, upon those who bow down before Your majesty, that they who have been refreshed by Your divine gift may ever be nourished by heavenly help'),
('5ah', 59, 'Parce Dómine, parce pópulo tuo: ut dignis flagellatiónibus castigátus; in tua miseratióne respíret',
 'Spare, O Lord, spare Your people, that, chastised by deserved scourges, they may find relief in Your mercy'),
('5af', 61, 'Tuére Dómine pópulum tuum, et ab ómnibus peccátis cleménter emúnda: quia nulla ei nocébit advérsitas; si nulla ei dominétur iníquitas',
 'Protect Your people, O Lord, and mercifully cleanse them from all their sins; for no adversity shall harm them if no wickedness has dominion over them'),
('5as', 63, 'Fidéles tui, Deus, per tua dona firméntur: ut éadem et percipiéndo requírant; et quæréndo sine fine percípiant',
 'May Your faithful, O God, be strengthened by Your gifts, that by receiving them they may seek them still, and seeking them may receive them for ever'),
('Quad1m', 67, 'Absólve, quǽsumus Dómine, nostrórum víncula peccatórum; et quidquid pro eis merémur propitiátus avérte',
 'Loose, we beseech You, O Lord, the bonds of our sins, and graciously turn away whatever we deserve for them'),
('Quad1t', 69, 'Ascéndant ad te, Dómine, preces nostræ; et ab Ecclésia tua cunctam repélle nequítiam',
 'May our prayers ascend to You, O Lord, and drive away all wickedness from Your Church'),
('Quad1w', 71, 'Mentes nostras, quǽsumus Dómine, lúmine tuæ claritátis illústra; ut vidére possímus quæ agénda sunt, et quæ recta sunt ágere valeámus',
 'Enlighten our minds, we beseech You, O Lord, with the light of Your brightness, that we may see what we ought to do and be able to do what is right'),
('Quad1h', 73, 'Da, quǽsumus Dómine, pópulis christiánis, et quæ profiténtur agnóscere; et cæléste munus dilígere, quod frequéntant',
 'Grant, we beseech You, O Lord, to Christian peoples both to understand what they profess and to love the heavenly gift which they so often receive'),
('Quad1f', 75, 'Exáudi nos miséricors Deus; et méntibus nostris grátiæ tuæ lumen osténde',
 'Hear us, O merciful God, and show to our minds the light of Your grace'),
('Quad2m', 82, 'Adésto supplicatiónibus nostris omnípotens Deus: et quibus fidúciam sperándæ pietátis indúlges; consuétæ misericórdiæ tríbue benígnus efféctum',
 'Hearken to our supplications, almighty God, and graciously grant the effect of Your wonted mercy to those to whom You give confidence to hope for Your loving-kindness'),
('Quad2t', 84, 'Propitiáre Dómine supplicatiónibus nostris: et animárum nostrárum medére languóribus; ut, remissióne percépta, in tua semper benedictióne lætémur',
 'Be appeased, O Lord, by our supplications, and heal the sickness of our souls, that, having received forgiveness, we may ever rejoice in Your blessing'),
('Quad2w', 86, 'Deus innocéntiæ restitútor et amátor, dírige ad te tuórum corda servórum: ut spíritus tui fervóre concépto, et in fide inveniántur stábiles; et in ópere effícaces',
 'O God, restorer and lover of innocence, direct to Yourself the hearts of Your servants, that, kindled with the fervor of Your Spirit, they may be found steadfast in faith and effective in work'),
('Quad2h', 87, 'Adésto Dómine fámulis tuis, et perpétuam benignitátem largíre poscéntibus: ut iis, qui te auctóre et gubernatóre gloriántur, et congregáta restáures; et restauráta consérves',
 'Be present, O Lord, to Your servants, and bestow Your unfailing kindness on those who ask it, that for those who glory in You as their maker and ruler You may restore what You have gathered and keep what You have restored'),
('Quad2f', 90, 'Da, quǽsumus Dómine, pópulo tuo salútem mentis et córporis: ut bonis opéribus inhæréndo; tuæ semper virtútis mereátur protectióne deféndi',
 'Grant, we beseech You, O Lord, to Your people health of mind and body, that, cleaving to good works, they may ever deserve to be defended by the protection of Your power'),
('Quad2s', 93, 'Famíliam tuam, quǽsumus Dómine, contínua pietáte custódi: ut quæ in sola spe grátiæ cæléstis innítitur; cælésti étiam protectióne muniátur',
 'Guard Your household, we beseech You, O Lord, with unceasing kindness, that, as it leans on the hope of heavenly grace alone, it may also be defended by heavenly protection'),
('Quad3m', 97, 'Subvéniat nobis, Dómine, misericórdia tua: ut ab imminéntibus peccatórum nostrórum perículis, te mereámur protegénte éripi; te liberánte salvári',
 'May Your mercy, O Lord, come to our help, that with You as our protector we may deserve to be rescued from the threatening dangers of our sins, and with You as our deliverer to be saved'),
('Quad3t', 98, 'Tua nos, Dómine, protectióne defénde; et ab omni semper iniquitáte custódi',
 'Defend us, O Lord, by Your protection, and keep us ever from all iniquity'),
('Quad3w', 100, 'Concéde, quǽsumus omnípotens Deus: ut qui protectiónis tuæ grátiam quǽrimus; liberáti a malis ómnibus, secúra tibi mente serviámus',
 'Grant, we beseech You, almighty God, that we who seek the grace of Your protection may be freed from all evils and serve You with a secure mind'),
('Quad3h', 102, 'Subjéctum tibi pópulum, quǽsumus Dómine, propitiátio cæléstis amplíficet; et tuis semper fáciat servíre mandátis',
 'May Your heavenly mercy, we beseech You, O Lord, increase the people subject to You, and make them ever obedient to Your commandments'),
('Quad3f', 105, 'Præsta, quǽsumus omnípotens Deus: ut qui in tua protectióne confídimus; cuncta nobis adversántia, te adjuvánte, vincámus',
 'Grant, we beseech You, almighty God, that we who trust in Your protection may, by Your help, overcome all that is against us'),
('Quad3s', 108, 'Prætende Dómine fidélibus tuis déxteram cæléstis auxílii: ut te toto corde perquírant; et quæ digne póstulant, cónsequi mereántur',
 'Stretch forth, O Lord, to Your faithful the right hand of heavenly help, that they may seek You with their whole heart and deserve to obtain what they worthily ask'),
('Quad4m', 112, 'Deprecatiónem nostram, quǽsumus Dómine, benígnus exáudi: et quibus supplicándi præstas afféctum; tríbue defensiónis auxílium',
 'Graciously hear our prayer, we beseech You, O Lord, and to those to whom You give the desire to pray grant the help of Your defence'),
('Quad4t', 114, 'Miserére Dómine pópulo tuo; et contínuis tribulatiónibus laborántem, propítius respiráre concéde',
 'Have mercy, O Lord, on Your people, and graciously grant them relief, toiling as they are under continual tribulations'),
('Quad4w', 117, 'Páteant aures misericórdiæ tuæ, Dómine, précibus supplicántium: et ut peténtibus desideráta concédas; fac eos quæ tibi sunt plácita postuláre',
 'Let the ears of Your mercy, O Lord, be open to the prayers of Your suppliants, and that You may grant their desires to those who ask, make them ask such things as please You'),
('Quad4h', 119, 'Pópuli tui Deus institútor et rector: peccáta, quibus impugnátur, expélle; ut semper tibi plácitus, et tuo munímine sit secúrus',
 'O God, founder and ruler of Your people, drive away the sins by which they are assailed, that they may ever be pleasing to You and secure under Your protection'),
('Quad4f', 122, 'Da nobis, quǽsumus omnípotens Deus: ut qui infirmitátis nostræ cónscii, de tua virtúte confídimus; sub tua semper pietáte gaudeámus',
 'Grant us, we beseech You, almighty God, that we who, conscious of our weakness, trust in Your strength, may ever rejoice under Your loving care'),
('Quad4s', 124, 'Deus, qui sperántibus in te miseréri pótius éligis, quam irásci: da nobis digne flere mala, quæ fécimus; ut tuæ consolatiónis grátiam inveníre mereámur',
 'O God, who choose rather to show mercy than to be angry with those who hope in You, grant us worthily to weep for the evils we have done, that we may deserve to find the grace of Your consolation'),
('Quad5m', 127, 'Da, quǽsumus Dómine, pópulo tuo salútem mentis et córporis: ut bonis opéribus inhæréndo; tua semper mereátur protectióne deféndi',
 'Grant, we beseech You, O Lord, to Your people health of mind and body, that, cleaving to good works, they may ever deserve to be defended by Your protection'),
('Quad5t', 129, 'Da nobis, quǽsumus Dómine, perseverántem in tua voluntáte famulátum; ut in diébus nostris et mérito, et número, pópulus tibi sérviens augeátur',
 'Grant us, we beseech You, O Lord, persevering service in Your will, that in our days the people serving You may grow both in merit and in number'),
('Quad5w', 131, 'Adésto supplicatiónibus nostris omnípotens Deus: et quibus fidúciam sperándæ pietátis indúlges; consuétæ misericórdiæ tríbue benígnus efféctum',
 'Hearken to our supplications, almighty God, and graciously grant the effect of Your wonted mercy to those to whom You give confidence to hope for Your loving-kindness'),
('Quad5h', 133, 'Esto, quǽsumus, Dómine, propítius plebi tuæ: ut quæ tibi non placent respuéntes; tuórum pótius repleántur delectatiónibus mandatórum',
 'Be gracious, we beseech You, O Lord, to Your people, that, rejecting what displeases You, they may rather be filled with delight in Your commandments'),
('Quad5f', 135, 'Concéde, quǽsumus omnípotens Deus: ut qui protectiónis tuæ grátiam quǽrimus; liberáti a malis ómnibus, secúra tibi mente serviámus',
 'Grant, we beseech You, almighty God, that we who seek the grace of Your protection may be freed from all evils and serve You with a secure mind'),
('Quad5s', 137, 'Tueátur, quǽsumus Dómine, déxtera tua pópulum deprecántem: et purificátum dignánter erúdiat; ut consolatióne præsénti ad futúra bona profíciat',
 'May Your right hand, we beseech You, O Lord, protect the people who pray to You, purify them and graciously instruct them, that by present consolation they may advance towards the good things to come'),
('Quad6m', 148, 'Ádjuva nos Deus salutáris noster; et ad benefícia recolénda, quibus nos instauráre dignátus es, tríbue veníre gaudéntes',
 'Help us, O God our Saviour, and grant that we may come with joy to the remembrance of the benefits by which You have deigned to renew us'),
('Quad6t', 153, 'Tua nos misericórdia, Deus, et ab omni subreptióne vetustátis expúrget; et capáces sanctæ novitátis effíciat',
 'May Your mercy, O God, cleanse us from all the deceits of our old nature and make us capable of holy newness of life'),
('Quad6w', 160, 'Réspice, quǽsumus Dómine, super hanc famíliam tuam: pro qua Dóminus noster Jesus Christus non dubitávit mánibus tradi nocéntium; et Crucis subíre torméntum',
 'Look down, we beseech You, O Lord, upon this Your family, for which our Lord Jesus Christ did not hesitate to be delivered into the hands of the wicked and to undergo the torment of the Cross'),
]
s = open(SITE, encoding='utf8').read(); PFX = 'window.ORATIONS = '
O = json.loads(s[len(PFX):].rstrip().rstrip(';'))
for k, p, la, en in SP:
    qt = k == 'Quad6w'
    la = la.replace('j', 'i').replace('J', 'I') + (': ' + QT if qt else ': ' + PD)
    en = en + '; ' + (EQT if qt else EPD)
    O.setdefault(k, {})['sp'] = [la, en, 'Missale O.P. (1939), p. %d' % p]
open(SITE, 'w', encoding='utf8').write(PFX + json.dumps(O, ensure_ascii=False) + ';\n')
print(len(SP), 'Orationes super populum written')
