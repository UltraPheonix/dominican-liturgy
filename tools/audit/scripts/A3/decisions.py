# per change id: 'skip' or override string (replacement Missal segment, accented)
D={}
SUB={}     # fid -> [(old, new)] applied after build
EXTRA=[]   # raw fix entries
NOTES={}   # key -> list of report notes
def skip(*ids):
    for i in ids: D[i]='skip'
# ---- S1101-S1102_3
skip('S1102.r0#0','S1102_3.pc#0')
SUB['S1102_2.r0']=[('cógitans. (nisi','cógitans. (Nisi'),('mórtuis). et quia','mórtuis). Et quia')]
SUB['S1102.r1']=[('Amen, Amen dico','Amen, amen dico')]
EXTRA.append({"file":"data/readings33.js","path":["S1102",1,"en"],"old":"At that time: Amen, amen I say unto you, that the hour cometh,","new":"At that time: Jesus said to the multitudes of the Jews: Amen, amen I say unto you, that the hour cometh,","src":"M39 p. 610 (pdf 344)","why":"English lacked the opening clause of the Latin (Dixit Jesus turbis Judaeorum)","_prefix":True})
NOTES['S1102_2']=['CHANT gr: Missal p. 610-611 prints Graduale Requiem with V. Animae eorum (not In memoria) for the 2nd Mass -> propose gr [6001] (G50 115*). Note G28 p. 106* rubric assigns In memoria to the day of All Souls: coordinator to decide.']
NOTES['S1102_3']=['CHANT gr: Missal p. 612 prints Graduale Requiem with V. Animae eorum for the 3rd Mass -> propose gr [6001] (G50 115*); same G28 rubric caveat.']
# ---- S1112 (p. 618-620, pdf 348-349): collect already in fixes; pc + epistle checked on scan pdf 349
SUB['S1112.r0']=[('famam: Ut seductóres','famam: ut seductóres')]
# ---- S1104 (pp. 614-616, pdf 346-347): lesson/gospel punctuation checked on scan; garbles skipped
skip('S1104.r1#7')
# ---- S1106 (p. 616-617, pdf 347; Common Plur. Mart. 'Intret' p. 14*-15*, pdf 375)
SUB['S1106.r0']=[('judícium certum. sumet','judícium certum. Sumet')]
EXTRA_S1106=1
# ---- S1109 (p. 617 -> Common Dedication pp. 2*-3*, pdf 369); Secret 'Extra ecclesiam dedicatam' (rubric p. 3*)
# ---- S1111 (pp. 618-619, pdf 348): lesson punct as S1104
# ---- S1115 (pp. 622-623, pdf 350); lesson ends 'amicitiae Dei.' (site had '... propter disciplinae dona commendati')
SUB['S1115.r1']=[('montem pósita. neque','montem pósita. Neque')]
SUB['S1115.r0']=[('amicítiæ Dei, propter disciplínæ dona commendáti.','amicítiæ Dei.')]
# ---- S1117 (pp. 624-625, pdf 351): no comma after iracundiae on the scan
skip('S1117.r0#0')
# ---- S1118 = S1109 (Common Dedication p. 2*-3*)
# ---- S1119 (pp. 625-626, pdf 351-352)
SUB['S1119.r0']=[('suæ A frigóribus','suæ a frigóribus')]
# ---- S1120 (pp. 626-628, pdf 352-353): Epistle lacked its ending
D['S1120.r0#1']=': In Christo Jesu Dómino nostro'
# ---- S1124 S1123 (p. 630, pdf 354)
# ---- S1124 (pp. 630-631, pdf 354; Comm. Doct. p. 20*-21*, pdf 378)
skip('S1124.r1#2')
SUB['S1124.r1']=[('montem pósita. neque','montem pósita. Neque')]
# ---- S1125 (pp. 632-633, pdf 355)
# ---- G369 Vigil of St Andrew (pp. 320-322, pdf 199-200); Lesson replaced by hand (fx_G369r0)
D['G369.se#1']='tui solémnia'
skip('G369.M[1129|S. Saturnini Ep. et Mart.].se#0')
SUB['G369.pc']=[('Andréa Apostolo','Andréa Apóstolo')]
# ---- S1130 (pp. 322-324, pdf 200-201)
skip('S1130.r1#3')
# ---- S1202 (pp. 324-326, pdf 201-202)
SUB['S1202.r1']=[('quem qui ínvenit homo','quem qui invénit homo')]
D['S1202.r1#1']='litus'
# ---- S1203 (pp. 326-327, pdf 202)
D['S1203.r0#0']='Ergo'
skip('S1203.r0#1')
# ---- S1204 (pp. 326-327, pdf 202; Comm. Doct. p. 20*)
skip('S1204.se#F','S1204.r1#2')
SUB['S1204.r1']=[('montem pósita. neque','montem pósita. Neque')]
# ---- S1206 (pp. 328-329, pdf 203); orations by hand
skip('S1206.r0#0')
# ---- S1207 (pp. 329-331, pdf 203-204)
SUB['S1207.r1']=[('montem pósita. neque','montem pósita. Neque')]
# ---- S1207v (pp. 331-332, pdf 204-205)
skip('S1207v.r0#0')
# ---- S1208 (pp. 333-334, pdf 205-206)
SUB['S1208.or']=[('eiúsdem Filii tui','eiúsdem Fílii tui')]
# ---- S1210 (pp. 334-336, pdf 206-207); Lesson by hand
skip('S1210.r1#5')
# ---- S1213 (pp. 336-337, pdf 207)
D['S1213.r0#0']='supportáte'
D['S1213.r1#0']='litus'
SUB['S1213.r1']=[('quem qui ínvenit homo','quem qui invénit homo')]
# ---- S1221 (pp. 338-339, pdf 208)
# ---- S1226 (pp. 340-342, pdf 209-210)
skip('S1226.or#1','S1226.or#F')
# ---- S1227 (pp. 342-344, pdf 210-211)
skip('S1227.se#0')
D['S1227.r0#2']=', Dóminus Deus noster'
D['S1227.r1#0']='cena'
# ---- S1228 (pp. 344-345, pdf 211)
D['S1228.r1#0']='tibi.'
# ---- S1229 (pp. 346-348, pdf 212-213)
# ---- S1231 (pp. 348-349, pdf 213)
# ---- session 3
# S0115 (p. 352-354, pdf 215-216): Maurus memoria prints no conclusion (middle oration, XI.1 p. 52): keep ':' before the expanded one
skip('S0115.M[0115|S. Mauri Abbatis].or#F','S0115.M[0115|S. Mauri Abbatis].pc#F')
# S0129 pc: text-layer garbles ('nostra', 'm'); scan has 'nostrae', 'majestati :'
skip('S0129.pc#0','S0129.pc#1','S0129.pc#F')
# S0131 pc: garble at 'maneamus : Qui vivis.'
skip('S0131.pc#0','S0131.pc#F')
skip('S0203.r0#1')
# S0207 readings replaced whole (Abbot Mass p. 25*): skip reading ops
skip('S0207.r0#0','S0207.r1#0','S0207.r1#1','S0207.r1#2')
skip('S0208.r0#0')
skip('S0208.r1#0')
skip(*['S0212.or#%d'%i for i in range(6)],'S0212.or#F',*['S0212.se#%d'%i for i in range(5)],'S0212.se#F',*['S0212.pc#%d'%i for i in range(8)],'S0212.pc#F')
skip('S0214.r0#0','S0214.r1#0')
skip('S0304.r0#0','S0304.r1#0')
# ---- session 4
SUB['S0318.r1']=[('suum. súfficit','suum. Súfficit')]
skip('S0324.pc#1','S0324.pc#2','S0324.pc#F')
skip('S0325.r1#5')
SUB['S0325.r0']=[('Butýrum et mei cómedet','Butýrum et mel cómedet')]
# S0327: STOP received; ops not yet seen on the scan are skipped (open item)
skip('S0327.pc#F','S0327.r1#0','S0327.r1#3','S0327.r1#4','S0327.r1#5','S0327.r1#6')
# ---- session 5 (28 Nov): capitals as printed (S1228, S0202, checked on the scan)
skip('S0202.se#0')
SUB['S0202.r0']=[('sicut anni antíqui.','sicut anni antíqui. Dicit Dóminus omnípotens.')]
# ---- S0402 (pp. 406-408, pdf 242-243)
D['S0402.pc#1']='sacraménta cæléstia'
SUB['S0402.or']=[('præmia','prǽmia')]
skip('S0402.or#0')
# ---- S0404 (p. 408, pdf 243; Comm. Doctoris pp. 20*-21*, pdf 378)
skip('S0404.r1#2')
# ---- S0405 (pp. 408-410, pdf 243-244): Collect printed 'Dóminum nostrum Jesum Christum...' (site expansion kept, tit. XI.2)
skip('S0405.or#0','S0405.or#F')
# ---- S0411 (p. 410-411, pdf 244 -> Comm. Doct. p. 20*): N. = Leo
skip('S0411.or#0','S0411.r1#0')
# ---- S0420 (pp. 413-415, pdf 245-246): Gospel commas 'arbor, ita', 'véniant, et' and '.' are on the scan (text layer garbled)
skip('S0420.pc#0','S0420.r1#2','S0420.r1#3','S0420.r1#4')
# ---- S0423 (p. 416, pdf 247 -> Comm. Mart. non Pont. T.P. 'Protexisti' pp. 11*-12*, pdf 373-374): Lesson replaced (see EXTRA in fx)
skip('S0423.r0#0','S0423.r0#C0')
# ---- S0424 (pp. 416-418, pdf 247-248)
skip('S0424.r0#4','S0424.r0#5')
SUB['S0424.r0']=[('veni: coronáberis','veni, coronáberis.')]
D['S0424.r1#1']=''
# ---- S0425 (pp. 418-419, pdf 248)
skip('S0425.r1#5')
# ---- S0430 (pp. 423-425, pdf 250-251): Gospel cut at 'Aliam' -> replaced as S0420 (EXTRA in fx)
skip('S0430.or#0')
# ---- S0503 (pp. 428-430, pdf 253-254): red rubric 'Hic genuflectitur :' not inserted into the reading text
skip('S0503.r0#2')
skip('S0504.r1#0')
# ---- S0508 (31 May, pp. 454-457, pdf 266-267): drop-cap garbles
skip('S0508.r0#0','S0508.r0#2')
# ---- S0508_2 (pp. 436-437, pdf 257): Gospel cut restored (Mt 18:8b-9a)
D['S0508_2.r1#3']='íngredi débilem, vel claudum, quam duas manus, vel duos pedes habéntem mitti in ignem ætérnum. Et si óculus tuus scandalízat te, érue eum, et prójice abs te: Bonum tibi est cum uno óculo in vitam intráre, quam duos óculos'
skip('S0509.r0#0')  # scan has 'illum : Et ipse'
skip('S0510.pc#0')
# ---- S0515 (p. 444, pdf 261 -> Os justi pp. 23*-24*): 'christiánam' lower case on the scan; se/pc replaced (EXTRA)
skip('S0515.or#C0','S0515.r0#0')
skip('S0516.r0#C0','S0516.r0#C1')  # Lesson replaced (EXTRA)
