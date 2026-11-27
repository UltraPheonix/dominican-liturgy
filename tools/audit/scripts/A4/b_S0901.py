# ---- S0901 St Giles (3 LL.) p. 548: "Officium Os justi, ut in Communi Abbatis, pag. 25*"; Common pp. 25*-26* (pdf 380-381)
RD=F.A.RD
L0=dict(RD['S0207'][0]); G0=dict(RD['S0207'][1])
G0['la']=G0['la'].replace('secúti sumus te: quid ergo','secúti sumus te: Quid ergo'); assert 'Quid ergo' in G0['la']
G0['en']=RD['S0519'][1]['en']
W='M39 p. 548 (pdf 313): "S. ÆGIDII Abbatis (3 LL.) Officium Os justi, ut in Communi Abbatis, pag. 25*"; the Common p. 25* prints Lectio Eccli. 45 "Diléctus Deo" and p. 26* the Gospel Matth. 19 "Dixit Petrus ad Jesum: Ecce nos relíquimus" (masses.js already gives these refs). The site had Eccli 31 "Beátus vir" + Luc 12 "Sint lumbi" (Common of a Confessor not Bishop, pp. 22*-24*)'
RAW('data/readings33.js',['S0901',0],RD['S0901'][0],L0,'M39 p. 25* (pdf 380)',W+'; Latin as printed (= S0207); English Douay-Rheims Eccli 45:1-6 without "Moses was" and v. 6b, which the Missal omits')
RAW('data/readings33.js',['S0901',1],RD['S0901'][1],G0,'M39 p. 26* (pdf 381)',W+'; Latin as printed ("te : Quid ergo"); English Douay-Rheims Matth 19:27-29 with the Missal\'s incipit "Peter said to Jesus" (as S0519)')
