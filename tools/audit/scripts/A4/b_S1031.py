# ---- S1031 Holy Relics (t. d.) pp. 601-602 (pdf 339-340);  S1031v Vigil of All Saints pp. 603-604 (pdf 340-341)
import json as _j
_G=[e for e in _j.load(open(OUT)) if e['path']==['S0927',1,'la']][-1]['new']
SUB('data/readings33.js',['S1031',0,'la'],[('Viri misericórdiæ sunt, quorum pietátes non defuérunt: cum sémine','Hi viri misericórdiæ sunt, quorum pietátes non defuérunt: Cum sémine'),('nepótes eórum, et in testaméntis','nepótes eórum: Et in testaméntis'),('manent: semen eórum','manent: Semen eórum')],'M39 p. 601 (pdf 339)','the first word "Hi" was missing ("Hi viri misericórdiæ sunt", as in S0626); as printed: ": Cum sémine"; "eórum : Et in testaméntis"; ": Semen eórum"')
for k,pg in (('S1031','M39 p. 602 (pdf 340)'),('S1031v','M39 pp. 603-604 (pdf 340-341)')):
    RAW('data/readings33.js',[k,1,'la'],F.A.RD[k][1]['la'],_G,pg,'as printed (the same Luc 6:17-23 text and points as S0927, p. 570): "Beáti páuperes : quia ... esurítis : quia ... fletis : quia"; "tamquam malum, propter"')
    EN(k,1,[(' For according to these things did their fathers to the prophets.','')],pg,'the Latin ends "merces vestra multa est in cælo." (no v. 23b)')
P('S1031v','r0',[0,1,2,3],'M39 p. 603 (pdf 340)',why='as printed: "sanctórum : Et cantábant"; "in Sánguine tuo"; "natióne : Et fecísti"; "Angelórum"')
