# ---- S0909 St Gorgonius (3 LL.) p. 554: "Officium Lætábitur, ut in Comm. Mart. non Pont., pag. 9*"; Common pp. 9*-10* (pdf 372-373)
RD=F.A.RD; M=F.A.M
L0=dict(RD['S0122'][0]); L0['la']=L0['la'].replace('potábit illum: et firmábitur','potábit illum: Et firmábitur'); assert 'illum: Et firm' in L0['la']
G0=dict(RD['S0122'][1]); G0['la']=RD['S0810'][1]['la']
W='M39 p. 554 (pdf 316): "S. GORGONII Mart. (3 LL.) Officium Lætábitur, ut in Comm. Mart. non Pont., pag. 9*"; the Common (pp. 9*-10*) prints Lectio Eccli. 14 et 15 "Beátus vir, qui in sapiéntia morábitur" and the Gospel Jo 12 "Amen, amen dico vobis, nisi granum fruménti". The site had Jac 1:12-18 + Luc 14:26-33 (readings33) and 2 Tim 2-3 (masses.js), neither printed for this Mass'
RAW('data/readings33.js',['S0909',0],RD['S0909'][0],L0,'M39 p. 9* (pdf 372)',W+'; Latin as printed (= S0122, with ": Et firmábitur"); English Douay as S0122')
RAW('data/readings33.js',['S0909',1],RD['S0909'][1],G0,'M39 pp. 9*-10* (pdf 372-373)',W+'; Latin as printed (= S0810: ": Et qui odit", ": Et ubi sum"); English Douay as S0122')
RAW('data/masses.js',['masses','S0909','readings'],M['S0909']['readings'],[{'type':'Lesson','ref':'Ecclesiasticus 14: 22, 15: 3-4, 6','m39':True},{'type':'Gospel','ref':'Joannes 12: 24-26','m39':True}],'M39 pp. 9*-10* (pdf 372-373)',W)
