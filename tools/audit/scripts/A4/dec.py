import json,sys
sys.path.insert(0,'/tmp/A4')
import fixgen as F
FX=[]; NOTES={}
def P(k,f,acc,pg,manual=None,why='punctuation as printed'):
    FX.append(F.make(k,f,acc,manual,src=pg,why=why))
def RAW(file,path,old,new,src,why): FX.append({"file":file,"path":path,"old":old,"new":new,"src":src,"why":why})
def N(k,s): NOTES.setdefault(k,[]).append(s)
def EN(k,i,pairs,src,why):
    old=F.A.RD[k][i]['en']; new=old
    for o,n in pairs:
        assert new.count(o)==1,(k,o); new=new.replace(o,n)
    RAW('data/readings33.js',[k,i,'en'],old,new,src,why)
# ---- batch 1
P('S0518','r0',[0],'M39 p. 446 (pdf 262)')
P('S0518','r1',[0,1,3,4,5],'M39 p. 446-447 (pdf 262)')
P('S0519','r0',[0,1,2,3,4],'M39 p. 447-448 (pdf 262-263)')
P('S0519','r1',[1],'M39 p. 448 (pdf 263)')
P('S0522','r0',[0,1,2,3,4],'M39 p. 449 (pdf 263)')
P('S0522','r1',[0,1,2,5,6],'M39 p. 450 (pdf 264)')
P('S0525','r0',[0,1],'M39 p. 450-451 (pdf 264)',manual={0:'Pater',1:': In Christo Jesu Dómino nostro'},why='word cut ("ter" for "Pater") and ending ": In Christo Jesu Domino nostro" missing, as printed')
EN('S0525',0,[('so shall you be also of the consolation.','so shall you be also of the consolation, in Christ Jesus our Lord.')],'M39 p. 451 (pdf 264)','English ending to match the Latin as printed')
N('S0525','CHANT: Missal p. 450 Tempore Paschali: "Officium Protexisti, de Comm. Mart. Pont., pag. 8*, cum Orationibus ut in Missa sequenti. Dicitur Alleluia, semel ante et post unicum V. Justus": pasch al should be [5678 Justus] only (site [5678, 5767 Surrexit Pastor]); then no Ascension verse either. READINGS OPEN: in Paschaltide the whole Common Mass p. 8* is said, so the readings are Stabunt justi (Sap. 5) and Ego sum vitis (Jo. 15); the site always gives Urban\'s 2 Cor 1 / Matth 25.')
N('S0524','READINGS: Missal p. 450 "Omnia fiant ut in Missa ejus, quae dicitur Feria iij" = votive Mass of St Dominic pp. 64*-66*: Epistle 2 Tim 4 Carissime: Testificor; Gospel Matth 5 Vos estis sal terrae. Site has no READINGS33 entry and masses.js gives Roman refs Eccli 31:8-11 / Luc 12:35-40 (roman:true): WRONG. Fix: give S0524 the Epistle/Gospel of S0804 (same texts, checked below) or of the votive Mass; masses.js refs corrected by fix.')
# ---- batch 2
for k in ('S0526','G481'):
    P(k,'r0',[0,1],'M39 p. 452-453 (pdf 265)',manual=[('comparatióne illíus aréna','comparatióne illíus, aréna'),('amicítiæ Dei, propter disciplínæ dona commendáti.','amicítiæ Dei.')],why='punctuation as printed; the lesson ends "amicitiae Dei." (the words "propter disciplinae dona commendati" are not printed)')
    EN(k,0,[('become the friends of God, being commended for the gift of discipline.','become the friends of God.')],'M39 p. 453 (pdf 265)','English cut to the Latin as printed')
N('G481','CHANT: duplicate of S0526 (Philip Neri); pasch al should be [6501 De excelso, 5437 Concaluit] as in S0526 (M39 p. 453), G481 has [6501] only.')
RAW('data/masses.js',['masses','S0527','title'],F.A.M['S0527']['title'],F.A.M['S0527']['title'].replace('Venerablis','Venerabilis'),'M39 p. 454 (pdf 266)','misspelling')
#P('S0527','r0',[0,1,2,3],'M39 p. 20* (pdf 378), Comm. Doct. (Missal p. 454: "ut in Comm. Doct., pag. 20*")')
#P('S0527','r1',[0,1,3,4,5],'M39 pp. 20*-21* (pdf 378)')
N('S0531','CHANT OPEN: the 1956 leaf (pdf 366-367, pp. 3-4) prints a proper Mass: Officium Gaudeamus ... sub honore beatae Mariae Virginis Reginae, V. Effundit cor meum; Gr. Ipse habet in vestimento (Apoc 19) V. Regina adstat; Alleluia Salve, Regina misericordiae (T.P. 2nd Surrexit Dominus et occurrens; Asc. Ascendens); Off. Regali ex progenie; Co. Regina mundi dignissima. The site has in 4289 Gaudeamus...assumptione, gr 6822 In me gratia, al 7208 Salve Mater, of 7216 Ave Regina caelorum, co 5623 Valde mirabilis: none is the printed chant. No GregoBase/G28/G50 source exists for these 1954 texts (searched). Needs a decision (label "not in the Graduale O.P." or set texts to a tone). READINGS OPEN: no READINGS33 entry; refs Eccli 24:5 / Luc 1:26-33 fetch a Bible text, not the Missal lesson (Eccli 24: Ego ex ore Altissimi ... vitam aeternam habebunt) / Gospel Luc 1:26-33 as printed.')
N('S0603','CHANT: Missal p. 459-460 "Temp. Pasch. Officium Sancti tui, ut in Communi plurimorum Martyrum, pag. 15*. Post Trinitatem Officium Intret, pag. 14*": the Intret Mass has a single Alleluia verse Te Martyrum (p. 15*): al should be [4992] (site [4992, 5648 Sancti et justi]). Pasch set OK.')
def dump():
    json.dump(FX,open('/home/claude/dominican-liturgy/tools/audit/fixes/A4.json','w'),ensure_ascii=False,indent=1)
    json.dump(NOTES,open('/tmp/A4/notes.json','w'),ensure_ascii=False,indent=1)
M_=F.A.M
RAW('data/masses.js',['masses','S0524','readings'],M_['S0524']['readings'],[{'type':'Epistle','ref':'Ad Timotheum 2 4: 1-8'},{'type':'Gospel','ref':'Matthæus 5: 13-19'}],'M39 p. 450 (pdf 264) -> Missa de S. Dominico, pp. 64*-66* (pdf 399-400)','Missal assigns the votive Mass of St Dominic: Epistle 2 Tim 4 Carissime: Testificor; Gospel Matth 5 Vos estis sal terrae (the Roman refs Eccli 31 / Luc 12 were wrong)')
