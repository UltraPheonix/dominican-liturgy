# ---- S0921 St Matthew (Totum Duplex II cl.) pp. 565-566 (pdf 321-322)
CL='Per Dóminum nostrum Iesum Christum Fílium tuum; qui tecum vivit et regnat in unitáte Spíritus Sancti Deus: per ómnia sǽcula sæculórum.'
ECL='through our Lord Jesus Christ, Your Son, who lives and reigns with You in the unity of the Holy Spirit, God, world without end.'
O=F.A.O['S0921']
NEW={'or':['Beáti Apóstoli et Evangelístæ Matthǽi, Dómine, précibus adiuvémur: ut quod possibílitas nostra non óbtinet; eius nobis intercessióne donétur: '+CL,
           'May the prayers of the blessed apostle and evangelist, Matthew, help us, O Lord; that what is not in our power to attain, may be given to us at his intercession: '+ECL],
     'se':['Supplicatiónibus beáti Matthǽi Apóstoli et Evangelístæ, quǽsumus Dómine, Ecclésiæ tuæ commendétur oblátio, cuius magníficis prædicatiónibus erudítur. '+CL,
           'Let the offering of Your Church, we pray You, O Lord, be commended to You by the prayers of blessed Matthew, Your apostle and evangelist, by whose glorious preaching she is instructed: '+ECL],
     'pc':['Percéptis, Dómine, sacraméntis, beáto Matthǽo Apóstolo tuo et Evangelísta interveniénte, deprecámur: ut quæ pro eius celebráta sunt glória; nobis profíciant ad medélam: '+CL,
           'Having taken Your sacraments, O Lord, we beseech You by the intercession of blessed Matthew, Your apostle and evangelist, that what we celebrate to his honor may avail to our healing: '+ECL]}
PG={'or':'M39 p. 565 (pdf 321)','se':'M39 p. 566 (pdf 322)','pc':'M39 p. 566 (pdf 322)'}
EN={'or':'English: St Dominic Missal 1959 p. 1133 verbatim (tools/orat39/dm_prayers.json 0921)','se':'English: St Dominic Missal 1959 p. 1134 verbatim (dm_prayers.json 0921)','pc':'English: St Dominic Missal 1959, which for St Matthew prints "Postcommunion, p. 997" (the same prayer for St Paul, 30 June): its English with the name and title of St Matthew'}
for p in ('or','se','pc'):
    assert len(O[p])==2
    RAW('data/orations.js',['S0921',p],O[p],NEW[p],PG[p],'WRONG PRAYER: the site had the prayer of the Vigil of St Matthew (p. 564, "quam prævenímus" / "cuius natalítia prævenímus"); the feast\'s own prayer is printed here, Per Dóminum (addressed to the Father, Rubr. gen. XI.2 p. 52: "Si Oratio dirigatur ad Patrem, concluditur Per Dominum nostrum"). '+EN[p])
P('S0921','r0',[0,2,3,4],'M39 pp. 565-566 (pdf 321-322)',why='as printed: "quátuor : Fácies autem"; "désuper : Duæ pennæ"; "córpora eórum : Et unumquódque"; "ambulábat : Ubi erat"')
P('S0921','r1',[0,1,2,3,4],'M39 p. 566 (pdf 322)',why='as printed: "factum est discumbénte"; "peccatóres veniéntes"; "publicánis et peccatóribus"; "Magíster"; "quid est, Misericórdiam"')
