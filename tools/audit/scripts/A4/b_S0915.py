# ---- S0915 Seven Sorrows (II cl.) p. 558: "Missa dicitur ut in Compassione B. M. V., Feria VI post Dom. Passionis, pag. 313, præter sequentia: Oratio Deus, in cujus passióne"; Compassion pp. 313-315 (pdf 195-196)
import copy
O=F.A.O; RD=F.A.RD
NEWOR=['Deus, in cuius passióne, secúndum Simeónis prophetíam, dulcíssimam ánimam gloriósæ Vírginis et Matris Maríæ dolóris gládius pertransívit: concéde propítius, ut qui dolóres eius venerándo recólimus; passiónis tuæ efféctum felícem consequámur: Qui vivis et regnas cum Deo Patre; in unitáte Spíritus Sancti Deus: per ómnia sǽcula sæculórum.',
 'O God, at whose passion, according to the prophecy of holy Simeon, a sword of grief pierced the most sweet soul of the glorious Mary, virgin and mother; grant, in Your mercy, that we who honor the memory of her sorrows, may gain the happy fruit of Your sufferings: who live and reign with God the Father, in the unity of the Holy Spirit, God, world without end.']
RAW('data/orations.js',['S0915','or'],O['S0915']['or'],NEWOR,'M39 p. 558 (pdf 318)','the Missal p. 558: "Missa dicitur ut in Compassione ... præter sequentia: Oratio Deus, in cujus passióne, secúndum Simeónis prophetíam ... consequámur : Qui vivis et regnas." The site had the Compassion Collect "Intervéniat" (p. 313). Qui vivis: addressed to the Son (Rubr. gen. XI.2 p. 52). English: the St Dominic Missal 1959 verbatim (tools/orat39/dm_prayers.json, key 0915), with the site\'s full conclusion')
SUB('data/orations.js',['S0915','se',0],[('cum Beátis habeámus: Qui vivis','cum Beátis habeámus. Qui vivis')],'M39 p. 315 (pdf 196)','as printed: "habeámus. Qui vivis et regnas"')
LA=RD['Quad5f'][0]['la']
for o,n in [('Deo excélso præ','Deo excélso, præ'),('cælum et terram, quia','cælum et terram: quia'),('tribulatiónem géneris','tribulatiónes géneris')]:
    assert LA.count(o)==1; LA=LA.replace(o,n)
EN0=('The Lord hath blessed thee by his power, because by thee he hath brought our enemies to nought. Blessed art thou, O daughter, by the Lord the most high God, above all women upon the earth. '
     'Blessed be the Lord who made heaven and earth: because he hath so magnified thy name this day, that thy praise shall not depart out of the mouth of men who shall be mindful of the power of the Lord for ever, for that thou hast not spared thy life, by reason of the distress and tribulation of thy people, but hast prevented our ruin in the presence of our God.')
L0={"type":"Lesson","ref":"Judith 13: 22-25","title":"Léctio libri Judith.","title_en":"Lesson from the Book of Judith.","la":LA,"en":EN0}
GLA=RD['Quad5f'][1]['la']
for o,n in [('Jesu mater ejus, et soror matris ejus','Jesu Mater ejus, et soror Matris ejus'),('Jesus matrem, et','Jesus Matrem, et'),('dicit matri suæ','dicit Matri suæ')]:
    assert GLA.count(o)==1; GLA=GLA.replace(o,n)
G0=copy.deepcopy(RD['Quad5f'][1]); G0['la']=GLA; G0.pop('p33',None)
FX.append({"file":"data/readings33.js","op":"add","path":['S0915'],"old":None,"new":[L0,G0],"src":'M39 pp. 313-314 (pdf 195-196)',"why":'"Missa dicitur ut in Compassione" (p. 558): readings33 had no S0915 entry (the app showed a Bible text). Latin as printed on pp. 313-314 ("excélso, præ"; "terram : quia"; "tribulatiónes"; "Mater ... Matris ... Matrem ... Matri"); English Douay-Rheims cut to the Missal\'s Latin (Judith 13:22-25 without "They all adored the Lord, and said to her", "And Ozias ... said to her", and "who hath directed thee to the cutting off the head of the prince of our enemies")'})
