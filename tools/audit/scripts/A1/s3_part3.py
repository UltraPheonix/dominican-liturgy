# ---- inter: collects said between the lessons (new field, op add)
CON={'PD':' Per Dóminum nostrum Jesum Christum Fílium tuum; qui tecum vivit et regnat in unitáte Spíritus Sancti Deus: per ómnia sǽcula sæculórum.',
     'PE':' Per eúmdem Dóminum nostrum Jesum Christum Fílium tuum; qui tecum vivit et regnat in unitáte Spíritus Sancti Deus: per ómnia sǽcula sæculórum.',
     'QT':' Qui tecum vivit et regnat in unitáte Spíritus Sancti Deus: per ómnia sǽcula sæculórum.',
     'QV':' Qui vivis et regnas cum Deo Patre; in unitáte Spíritus Sancti Deus: per ómnia sǽcula sæculórum.'}
def it(after,pre,body,c,en,ens,src,**kw):
    d={'after':after,'pre':pre,'la':body+CON[c],'en':en,'src':src,'en_src':ens}; d.update(kw); return d
DM='St Dominic Missal (1959) p. %s, verbatim (OCR checked on the page image)'
N23='The Missal prints the Secunda and Tertia Oratio after this collect (%s): the 2nd and 3rd prayers of the day are said here, not after the first Collect'
INTER={
 'Adv3w':('M39 pp. 6-7 (pdf 37)',[
   it(0,'Dóminus vobíscum. Orémus.','Festína, quǽsumus Dómine, ne tardáveris: et auxílium nobis supérnæ virtútis impénde; ut advéntus tui consolatiónibus sublevéntur, qui in tua pietáte confídunt:','QV',
      'Hasten, we pray You, come soon, and yield the power of Your help from on high; that they who trust in Your love may be helped by the consolation of Your coming: who live and reign.','dm',
      'M39 p. 7 (pdf 37), after the Gradual Tóllite portas: "Hic dicitur Dóminus vobíscum. Orémus"; conclusion printed "Qui vivis et regnas."; English '+DM%'11 (pdf p. 34)',
      note=N23%'p. 7: Deus, qui de beátæ Maríæ (Per eúmdem); Deus, qui caritátis (Per Dóminum ... in unitáte ejúsdem)',
      rubric='The first Collect (Præsta) is said after the Kyrie with "Orémus" only ("Orémus sine Dóminus vobíscum", p. 6).')]),
 'Adv3s':('M39 pp. 10-13 (pdf 39-40)',[
   it(0,'Orémus.','Concéde, quǽsumus omnípotens Deus: ut qui sub peccáti jugo ex vetústa servitúte deprímimur; exspectáta unigéniti Fílii tui nova nativitáte, liberémur:','QT',
      'Grant, we beseech You, almighty God, that we who are bowed down by our old bondage under the yoke of sin, may be set free by that new birth of Your Only-begotten Son which we await: who lives and reigns with You.','dm',
      'M39 p. 11 (pdf 39); printed "Qui tecum."; English '+DM%'16 (pdf p. 39)',
      rubric='"Post Kýrie eléison quinque sequéntes Oratiónes dicántur sine Dóminus vobíscum. Nec dicátur Flectámus génua sed Orémus" (p. 10).'),
   it(1,'Orémus.','Indígnos nos, quǽsumus Dómine, fámulos tuos, quos actiónis própriæ culpa contrístat; unigéniti Fílii tui advéntu lætífica:','QT',
      'We beseech You, O Lord, that Your unworthy servants who are saddened by the guilt of their misdeeds, may be made glad by the coming of Your Only-begotten Son: who lives and reigns with You.','dm',
      'M39 p. 11 (pdf 39); printed "Qui tecum."; first word in capitals, accent supplied; English '+DM%'17 (pdf p. 40)'),
   it(2,'Orémus.','Præsta, quǽsumus omnípotens Deus: ut Fílii tui ventúra solémnitas, et præséntis nobis vitæ remédia cónferat; et prǽmia ætérna concédat:','PE',
      'Grant, we beseech You, almighty God, that the approaching feast of Your Son, may bestow on us remedies for this present life, and afford us rewards in the life to come: through the same Lord.','dm',
      'M39 p. 12 (pdf 40); printed "Per eúmdem."; English '+DM%'18 (pdf p. 41)'),
   it(3,'Orémus.','Preces pópuli tui, quǽsumus Dómine, cleménter exáudi: ut qui juste pro peccátis nostris afflígimur; pietátis tuæ visitatióne consolémur:','QV',
      'We beseech You, O Lord, mercifully to hear the prayers of Your people, that we who are justly afflicted for our sins may be comforted by the coming of Your loving kindness: who live and reign.','dm',
      'M39 pp. 12-13 (pdf 40); printed "Qui vivis."; English '+DM%'20 (pdf p. 43)'),
   it(4,'Dóminus vobíscum. Orémus.','Deus, qui tribus púeris mitigásti flammam ígnium; concéde propítius, ut nos fámulos tuos non exúrat flamma vitiórum:','PD',
      'O God, who for the three young men tempered the flame of fire, mercifully grant that the flame of vices may not burn us, Your servants: through our Lord.','ai',
      'M39 p. 13 (pdf 40), after the Hymn Benedíctus es: "Postea Dóminus vobíscum. Orémus"; printed "Per Dóminum."; English: AI translation (the St Dominic Missal 1959, p. 22, has "flammas", plural; the M39 prints "flammam")',
      note=N23%'p. 13: Deus, qui de beátæ Maríæ (Per eúmdem); Deus, qui caritátis')]),
 'Quad1w':('M39 pp. 69-70 (pdf 68-69)',[
   it(0,'Dóminus vobíscum. Orémus. Flectámus génua. Leváte.','Devotiónem pópuli tui, quǽsumus Dómine, benígnus inténde: ut qui per abstinéntiam macerántur in córpore; per fructum boni óperis reficiántur in mente:','PD',
      'Look down in mercy, O Lord, we beseech You, on the devotion of Your people; that as they mortify their bodies by abstinence, they may be refreshed in mind by the fruit of good deeds: through our Lord.','dm',
      'M39 p. 70 (pdf 69); printed "Per Dóminum."; first word in capitals, accent supplied; English '+DM%'124 (pdf p. 147)',
      note=N23%'p. 70: "Secunda et tertia Oratio, pag. 63"',
      rubric='The first Collect (Preces nostras): "Post Kýrie eléison non dicátur Dóminus vobíscum, sed Orémus. Flectámus génua. Leváte" (p. 68).')]),
 'Quad1s':('M39 pp. 74-77 (pdf 71-73)',[
   it(0,'Orémus. Flectámus génua. Leváte.','Deus, qui nos in tantis perículis constitútos, pro humána scis fragilitáte non posse subsístere; da nobis salútem mentis et córporis: ut ea, quæ pro peccátis nostris pátimur; te adjuvánte vincámus:','PD',
      'O God, You know that in such dangers our human weakness cannot stand firm; grant us health of mind and body, that, by Your help, we may overcome what we suffer for our sins: through our Lord.','dm',
      'M39 p. 76 (pdf 72); printed "Per Dóminum."; English '+DM%'138 (pdf p. 161)',
      rubric='"Post Kýrie eléison, quinque sequéntes Oratiónes dicántur sine Dóminus vobíscum. Sed ante unamquámque Oratiónem, nisi áliter notétur, dicátur Orémus. Flectámus génua. Leváte" (p. 74).'),
   it(1,'Orémus. Flectámus génua. Leváte.','Protéctor noster áspice Deus: ut qui malórum nostrórum póndere prémimur; percépta misericórdia, líbera tibi mente famulémur:','PD',
      'Look down upon us, O God, our protector, and grant that we who are burdened by the weight of our sins, may receive Your mercy and serve You with a free mind: through our Lord.','dm',
      'M39 p. 76 (pdf 72); printed "Per Dóminum."; first word in capitals, accent supplied; English '+DM%'139 (pdf p. 162)'),
   it(2,'Orémus. Flectámus génua. Leváte.','Adésto, quǽsumus Dómine, supplicatiónibus nostris: ut esse, te largiénte, mereámur et inter próspera húmiles; et inter advérsa secúri:','PD',
      'Be near to our cries, O Lord, we beseech You, that by Your bounty we may deserve to be humble in every success and steadfast in every trial: through our Lord.','dm',
      'M39 p. 76 (pdf 72); printed "Per Dóminum."; first word in capitals, accent supplied; English '+DM%'140 (pdf p. 163)'),
   it(3,'Orémus. Flectámus génua. Leváte.','Preces pópuli tui, quǽsumus Dómine, cleménter exáudi: ut qui juste pro peccátis nostris afflígimur; pro tui nóminis glória misericórditer liberémur:','PD',
      'Graciously hear, O Lord, the prayers of Your people, that we who are justly afflicted for our sins may, to the glory of Your name, be mercifully delivered: through our Lord.','dm',
      'M39 p. 76 (pdf 72); printed "Per Dóminum."; English '+DM%'141 (pdf p. 164)'),
   it(4,'Dóminus vobíscum. Orémus.','Deus, qui tribus púeris mitigásti flammas ígnium; concéde propítius, ut nos fámulos tuos non exúrat flamma vitiórum:','PD',
      'O God, who tempered the flames of fire for the three young men, mercifully grant that we Your servants may not be consumed by the flames of vice: through our Lord.','dm',
      'M39 p. 77 (pdf 73), after the Hymn Benedíctus es; printed "Per Dóminum."; English '+DM%'141 (pdf p. 164)',
      rubric='"Non dicátur Flectámus génua" (p. 77).', note=N23%'p. 77: "Secunda et tertia Oratio, pag. 63"')]),
}
for k,(pg,lst) in INTER.items():
    assert 'inter' not in O[k]
    for x in lst: assert x['after']<len(R[k]) and R[k][x['after']]['type']=='Lesson',(k,x['after'])
    add(OR,[k,'inter'],lst,pg,'NEW FIELD "inter": the collects the Missal prints between the lessons (Ember day), each after the lesson whose 0-based index in readings33[%s] is "after"; Latin read from the scan crops, conclusions expanded by type as printed (Rubr. gen. XI.2, M39 p. 52: "Si Oratio dirigatur ad Patrem, concluditur Per Dominum nostrum; et si ad Filium, Qui vivis et regnas cum Deo Patre; si in principio Orationis fiat mentio Filii, terminatur Per eumdem Dominum nostrum; si in fine Orationis fiat ejus mentio, terminatur per Qui tecum vivit"); "pre" = what the Missal prints before it; "rubric"/"note" = the Missal\'s rubrics there'%k)
