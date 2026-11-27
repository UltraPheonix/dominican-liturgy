from fx6 import *
from fx6 import _sub
LC=' Per Dóminum nostrum Iesum Christum, Fílium tuum: qui tecum vivit et regnat in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum.'
# ===== 1. Requiem Masses, M39 pp. 114*-124* (pdf 425-430)
# C114o, In die obitus, pp. 114*-116*: orations OK (pdf 425-426); 1 Thess 4 OK; John 11 punctuation
rd('C114o',1,'la',[('nunc scio quia quæcúmque','nunc scio, quia quæcúmque'),('resurréctio, et vita','resurréctio et vita'),('crédidi quia tu','crédidi, quia tu'),('Christus, Fílius Dei','Christus Fílius Dei')],'M39 p. 115* (pdf 425)','punctuation as printed')
# ===== 2. Beati with a different Gospel named in their rubric
L10="In illo témpore: Designávit Dóminus et álios septuagínta duos, et misit illos binos ante fáciem suam in omnem civitátem, et locum, quo erat ipse ventúrus. Et dicébat illis: Messis quidem multa, operárii autem pauci. Rogáte ergo dóminum messis, ut mittat operários in messem suam. Ite: ecce ego mitto vos sicut agnos inter lupos. Nolíte portáre sácculum, neque peram, neque calceaménta, et néminem per viam salutavéritis. In quamcúmque domum intravéritis, primum dícite: Pax huic dómui: et si ibi fúerit fílius pacis, requiéscet super illum pax vestra: sin autem, ad vos revertétur. In eádem autem domo manéte, edéntes, et bibéntes quæ apud illos sunt: dignus est enim operárius mercéde sua. Nolíte transíre de domo in domum. Et in quamcúmque civitátem intravéritis, et suscéperint vos, manducáte quæ apponúntur vobis: et curáte infírmos, qui in illa sunt, et dícite illis: Appropinquávit in vos regnum Dei."
def gospel_from(k,srck,la,src,why):
    s=R[srck][1]
    for f in ('ref','title','title_en','p33'):
        if R[k][1].get(f)!=s.get(f): rdset(k,1,f,s[f],src,why)
    rdset(k,1,'la',la if la else s['la'],src,why)
    rdset(k,1,'en',s['en'],src,why+' (English: Douay, as on '+srck+')')
    if M[k]['readings'][1]['ref']!=s['ref']:
        cur('data/masses.js',['masses',k,'readings',1,'ref']); setv('data/masses.js',['masses',k,'readings',1,'ref'],s['ref'],src,why)
gospel_from('S1103b','S1112',None,'M39 p. 614 (pdf 346) rubric; Gospel M39 p. 26* (pdf 381)','wrong Gospel: the rubric reads "Officium Os justi, ut in Comm. Conf. non Pont., pag. 23*, cum Evangelio Ecce nos reliquimus, ut in Communi Abbatum, pag. 26*"; Matt 19: 27-29 as printed on p. 26* (= S1112, checked word by word on the scan)')
gospel_from('S0225b','S0719',L10,'M39 p. 388 (pdf 233) rubric; Gospel M39 p. 25* (pdf 380)','wrong Gospel: the rubric reads "Officium Os justi, ut in Comm. Conf. non Pont., pag. 23*, cum Evangelio Designavit, pag. 25*"; Luke 10: 1-9 as printed on p. 25*')
for k in ('S0119b','S0428b','S0717b'):
    gospel_from(k,'S0719',L10,'M39 p. 25* (pdf 380)','Luke 10: 1-9 as printed on p. 25* (the rubric\'s "Evangelio Designavit, pag. 25*"): missing words "et" (Dóminus et álios) / "quo" (quo erat), punctuation, stray final "In"; ref and English to v. 9')
# ----- Beati sent to "Gaudeamus, ut in Communi nec Virg. nec Mart., pag. 36*": Lesson Prov 31 (36*-37*), Gospel Matt 13 (38*)
import copy as _c
def setread(k,i,obj,src,why):
    for f in ('type','ref','title','title_en','la','en','p33'):
        if f in obj and R[k][i].get(f)!=obj[f]: rdset(k,i,f,obj[f],src,why)
    mr=M[k]['readings']
    cur('data/masses.js',['masses',k,'readings',i])
    nv=dict(mr[i]); nv['type']=obj['type']; nv['ref']=obj['ref']; nv.pop('roman',None)
    if nv!=mr[i]: setv('data/masses.js',['masses',k,'readings',i],nv,src,why)
PROV=_c.deepcopy(R['S1119'][0]); PROV['la']=PROV['la'].replace('vir ejus, et laudávit','vir ejus et laudávit')
assert PROV['la']!=R['S1119'][0]['la']
MT13=_c.deepcopy(R['C55s'][1])
MT13['la']=_sub(MT13['la'],[('quem qui ínvenit','quem qui invénit'),('exíbunt ángeli','Exíbunt Angeli'),('fletus, et stridor','fletus et stridor')],'MT13')
for k,pgs in (('S0103b','p. 351 (pdf 214)'),('S0228b','p. 389 (pdf 233)'),('S0808b','p. 522 (pdf 300)')):
    why='wrong readings: the rubric (M39 %s) reads "Officium Gaudeamus, ut in Communi nec Virg. nec Mart., pag. 36*"; the site had the Virg. non Mart. readings (2 Cor 10 / Matt 25, p. 30*)'%pgs
    setread(k,0,PROV,'M39 pp. 36*-37* (pdf 386)',why+'; Lesson Prov 31: 10-31 as printed on pp. 36*-37* ("vir ejus et laudávit"; text = S1119, checked on the scan)')
    setread(k,1,MT13,'M39 p. 38* (pdf 387)',why+'; Gospel Matt 13: 44-52 as printed on p. 38* (invénit; Exíbunt Angeli; "fletus et stridor"; "nova et vétera")')

# ----- S0605b: the Missal prints the whole Mass Os justi on pp. 460-461 (pdf 269); readings = Comm. Os justi, no proper
rd('S0605b',0,'la',[('pecúnia et thesáuris','pecúnia, et thesáuris')],'M39 p. 461 (pdf 269)','punctuation as printed')
rd('S0605b',1,'la',[('dóminum suum quando','dóminum suum, quando'),('cum vénerit et pulsáverit','cum vénerit, et pulsáverit')],'M39 pp. 460-461 (pdf 269)','punctuation as printed')
# ----- S0609b: "Officium Gaudeamus, ut in Comm. Virg. non Mart., pag. 30*, praeter ea, quae sequuntur" (p. 462): own Introit and orations only; readings = p. 30* (C51s, scan-checked by A5)
for i in (0,1):
    if R['S0609b'][i]['la']!=R['C51s'][i]['la']: rdset('S0609b',i,'la',R['C51s'][i]['la'],'M39 p. 462 (pdf 270) rubric; readings M39 pp. 30*-31* (pdf 383)','readings of the Comm. Virg. non Mart., p. 30*, as printed (A5\'s C51s correction carried over): '+('supportáte, "uni viro vírginem"' if i==0 else 'commas "lámpades suas, exiérunt", "dormitavérunt omnes, et"'))
# ----- S0904b: rubric p. 550 "Officium Gaudeamus, ut in Communi unius Virg. non Mart., p. 30*"; pp. 550-551 print only the orations (seen on the scan): readings of p. 30* (C51s)
for i in (0,1):
    for f in ('ref','title','title_en','la','en','p33'):
        if R['S0904b'][i].get(f)!=R['C51s'][i].get(f): rdset('S0904b',i,f,R['C51s'][i][f],'M39 p. 550 (pdf 314) rubric; readings M39 pp. 30*-31* (pdf 383)','wrong readings (1 Thess 2 / John 21 are not in the 1939 Missal for this Beata): the rubric reads "Officium Gaudeamus, ut in Communi unius Virg. non Mart., p. 30*" and pp. 550-551 print only the orations; readings of p. 30* (C51s, scan-checked by A5)')
cur('data/masses.js',['masses','S0904b','readings'])
setv('data/masses.js',['masses','S0904b','readings'],[{'type':'Epistle','ref':R['C51s'][0]['ref']},{'type':'Gospel','ref':R['C51s'][1]['ref']}],'M39 p. 550 (pdf 314)','refs of the readings of p. 30*')
# ----- Beati whose rubric crop failed in A5: rubric read here (text layer, each Beatus's own entry has no readings), readings = the Commune's (scan-checked by A5)
BEATI={ # key: (commune key, rubric page/pdf, rubric words, gospel override)
 'S0303b':('C42s','p. 394 (pdf 236)','Officium Os justi, ut in Communi Conf. non Pontif. pag. 23*',None),
 'S0503b':('C51s','p. 534 (pdf 306)','Officium Gaudeamus, ut in Comm. Virg. non Mart., pag. 30*',None),
 'S0620b':('C51s','p. 469 (pdf 274)','Officium Gaudeamus, ut in Communi Virg. non Mart., pag. 30*',None),
 'S0622b':('C32s','p. 470 (pdf 274)','Officium Statuit, ut in Communi Conf. Pontificis, pag. 18*',None),
 'S0905b':('C30s','p. 550 (pdf 314)','Officium Sacerdotes, ut in Communi Conf. Pont., pag. 17*',None),
 'S1116b':('C51s','p. 624 (pdf 351)','Officium Gaudeamus, ut in Communi Virg. non Mart., pag. 30*',None),
 'S0427b':('C51s','p. 420 (pdf 249)','Officium Gaudeamus, ut in Communi Virg. non Mart. pag. 30*, cum Orationibus sequentibus',None),
 'S0528b':('C51s','p. 454 (pdf 266)','Officium Gaudeamus, ut in Communi Virg. non Mart., pag. 30*',None),
 'S1030b':('C51s','p. 600 (pdf 339)','Officium Gaudeamus, ut in Comm. Virg. non Mart., pag. 30*',None),
 'S0514b':('C42s','p. 442 (pdf 260)','Officium Os justi, ut in Communi Conf. non Pont., pag. 23*',None),
 'S1026b':('C42s','p. 597 (pdf 337)','Officium Os justi, ut in Communi Conf. non Pont., pag. 23*',None),
 'S0811b':('C42s','p. 522 (pdf 300)','Officium Os justi, ut in Communi Conf. non Pont., pag. 23*, cum Evangelio Designavit, pag. 25*','Lucas 10: 1-9'),
 'S1012b':('C42s','p. 579 (pdf 327)','Officium Os justi, de Communi Confessoris non Pontificis, pag. 23*, cum Evangelio Designavit Dominus, pag. 25*','Lucas 10: 1-9'),
}
for k,(c,pg,rub,gos) in BEATI.items():
    why='the rubric (M39 %s) reads "%s"; the Beatus\'s own entry prints only the orations; readings of the Commune (%s)'%(pg,rub,c)
    src='M39 %s'%pg
    refs=[R[c][0]['ref'],gos or R[c][1]['ref']]
    if R.get(k):
        for i in (0,1):
            for f in ('type','ref','title','title_en','la','en','p33'):
                if R[k][i].get(f)!=R[c][i].get(f): rdset(k,i,f,R[c][i][f],src,why+(', scan-checked by A5' if True else ''))
    mr=M[k]['readings']; new=[{'type':R[c][0]['type'] if R[c][0]['type']!='Lesson' else 'Lesson','ref':refs[0]},{'type':'Gospel','ref':refs[1]}]
    if [ (x['type'],x['ref']) for x in mr]!=[(x['type'],x['ref']) for x in new]:
        cur('data/masses.js',['masses',k,'readings']); setv('data/masses.js',['masses',k,'readings'],new,src,why+('' if R.get(k) else '; this key has no readings33 entry, so the page takes the text from the Bible by these refs'))
# ===== 3. Wrong orations
import copy as _cp
EC='; through our Lord Jesus Christ, Your Son, who lives and reigns with You in the unity of the Holy Spirit, God, world without end.'
LCe=' Per eúmdem Dóminum nostrum Iesum Christum Fílium tuum, qui tecum vivit et regnat in unitáte Spíritus Sancti, Deus, per ómnia sǽcula sæculórum.'
ECe='; through the same Jesus Christ, Your Son, our Lord, who lives and reigns with You in the unity of the Holy Spirit, God, world without end.'
QT=' Qui tecum vivit et regnat in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum.'
EQT='; who lives and reigns with You in the unity of the Holy Spirit, God, world without end.'
import subprocess as _sp, re as _re, json as _js
_BS=_sp.run(['git','-C',ROOT,'show','d0394fd:data/orations.js'],capture_output=True,text=True).stdout
_BO=_js.loads(_BS[_re.search(r'window\.\w+\s*=\s*',_BS).end():_BS.rfind('}')+1])
import fx6 as _fx
def setobj(k,new,src,why):
    cur('data/orations.js',[k]); setv('data/orations.js',[k],new,src,why)
    _fx.ORIG[('data/orations.js',(k,))]=_BO[k]   # pre-fix value (git d0394fd); the fix is already applied in the data
# C39s Justus ut palma (22*-23*, pdf 379): the Divinum Officium "Os justi" prayers stood here
setobj('C39s',{'src':'Missale O.P. (1939), pp. 22*-23* (Confessoris non Pontificis, Justus ut palma); English: St Dominic Missal (1959), Common No. 13',
 'or':['Deus, qui nos beáti N. Confessóris tui ánnua solemnitáte lætíficas: concéde propítius, ut cuius natalítia cólimus; étiam actiónes imitémur:'+LC,
       'O God, year by year You gladden us by the solemnity of blessed N. Your confessor; mercifully grant that as we hallow his feast, we may follow in his ways'+EC],
 'se':['Laudis tibi Dómine hóstias immolámus in tuórum commemoratióne Sanctórum: quibus nos et præséntibus éxui malis confídimus, et futúris.'+LC,
       'We offer You, O Lord, victims of praise in memory of Your saints; and trust thereby to be freed from all ills both present and to come'+EC],
 'pc':['Refécti cibo potúque cælésti, Deus noster, te súpplices exorámus: ut in cuius hæc commemoratióne percépimus; eius muniámur et précibus:'+LC,
       'Refreshed with this heavenly food and drink, our God, we humbly pray, that he in whose memory we have received this sacrament, may help us by his prayers'+EC],
 'en_src':{'or':'dm','se':'dm','pc':'dm'}},
 'M39 pp. 22*-23* (pdf 379)','wrong orations (Divinum Officium "Os justi" set: Adesto / Praesta / Quaesumus); the Missal\'s Mass Justus ut palma prints Collect Deus, qui nos (22*), Secret Laudis tibi, Postcommunion Refecti cibo (23*), seen on the scan; conclusion Per Dominum as printed (Rubr. gen. XI.2, p. 52: "Si Oratio dirigatur ad Patrem, concluditur Per Dominum nostrum"). English verbatim from the St Dominic Missal 1959, Common No. 13 (tools/orat39/dm1959 rows, OCR slips only: "victims of", "this")')
# C51s Virg. non Mart. (Gaudeamus, 30*-31*, pdf 383): the nec Virg. nec Mart. orations (36*-38*) stood here; the Missal's are those of C55s (text layer of 30*-31* = C55s word for word)
n51=_cp.deepcopy(O['C51s'])
for p in ('or','se','pc'): n51[p]=_cp.deepcopy(O['C55s'][p])
n51['src']='Missale O.P. (1939), pp. 30*-31* (Unius Virginis non Martyris); English after the St Dominic Missal (1959), checked against the Latin'
setobj('C51s',n51,'M39 pp. 30*-31* (pdf 383)','wrong orations: Tuorum corda / Munera / Quaesumus are the nec Virg. nec Mart. Mass (pp. 36*-38*); p. 30*-31* prints Exaudi nos / Accepta tibi sit / Satiasti (= C55s, A5 scan-checked; the text layer of pdf 383 agrees word for word)')
# C68s De Quinque Stigmatibus (46*-47*, pdf 391-392): the orations were those of De Poenis seu Passione (48*)
setobj('C68s',{'src':'Missale O.P. (1939), pp. 46*-47* (De Quinque Stigmatibus D. N. J. C.); English: AI translation of the Missal\'s Latin (no St Dominic Missal text)',
 'or':['Deus, qui unigéniti Fílii tui passióne, et copiósa per quinque vúlnera sui sánguinis effusióne, humánam natúram peccáto pérditam reparásti: tríbue nobis, quǽsumus, ut qui illíus passiónis glóriam, et ab eo suscépta vúlnera venerámur in terris; eiúsdem pretiosíssimi sánguinis fructum cónsequi mereámur in cælis:'+LCe,
       'O God, who by the passion of Your only-begotten Son, and by the plentiful shedding of His blood through five wounds, restored human nature lost by sin: grant us, we beseech You, that we who venerate on earth the glory of His passion and the wounds He received, may deserve to obtain in heaven the fruit of that same most precious blood'+ECe],
 'se':['Oblátum tibi, Dómine, sacrifícium, intercedénte unigéniti Fílii tui, mediántibus quinque vulnéribus, passióne, vivíficet nos semper, et múniat.'+QT,
       'May the sacrifice offered to You, O Lord, by the intercession of the passion of Your only-begotten Son, through His five wounds, ever give us life and protect us'+EQT],
 'pc':['Refécti vitálibus alimóniis, quǽsumus Dómine Deus noster: ut qui Stígmata Dómini nostri Iesu Christi venerándo cólimus; hæc in nostris córdibus impréssa, móribus et vita teneámus:'+LCe,
       'Refreshed with life-giving nourishment, we beseech You, O Lord our God, that we who honour with veneration the Stigmata of our Lord Jesus Christ, may hold them impressed on our hearts, in our conduct and our life'+ECe],
 'en_src':{'or':'ai','se':'ai','pc':'ai'}},
 'M39 pp. 46*-47* (pdf 391)','wrong orations (those of De Poenis seu Passione, 48*); Latin read on the scan of 46*-47*. Conclusions as printed: Collect and Postcommunion "Per eúmdem" (Rubr. gen. XI.2, p. 52: "si in principio Orationis fiat mentio Filii, terminatur Per eumdem Dominum nostrum"), Secret "Qui tecum vivit et regnat" (printed; XI.2: "si in fine Orationis fiat ejus mentio, terminatur per Qui tecum vivit"). English: AI translation (Joseph\'s ruling, 27 Nov), labelled by en_src')
# C75s: the Collect's English still had "on this day" (A5 removed "hodierna die" from the Latin, p. 53*)
orat('C75s','or',[('O God, You Who on this day have taught','O God, You Who have taught')],'M39 p. 53* (pdf 395)','English matched to the votive Latin (no "hodierna die", p. 53*)',i=1)
# C76s De Spiritu Sancto infra Septuagesimam (54*): "Cetera ut supra, excepto quod nullum allelúia dicitur" -> orations of C75s
n76=_cp.deepcopy(O['C75s'])
n76['or'][1]=n76['or'][1].replace('O God, You Who on this day have taught','O God, You Who have taught')
n76['src']='Missale O.P. (1939), p. 54* (De Spiritu Sancto infra Septuagesimam: "Cetera ut supra"); orations as pp. 53*-54*'
setobj('C76s',n76,'M39 p. 54* (pdf 395)','wrong orations (Lent IV Wednesday\'s, Divinum Officium Quad4-3); the Missal p. 54* prints only the Officium Cum sanctificatus and the Tract Caeli distillaverunt, then "Cetera ut supra, excepto quod nullum allelúia dicitur" (seen on the scan): the orations are C75s\'s (Deus qui corda / Munera / Sancti Spiritus), conclusion "in unitáte ejúsdem" as printed on p. 54* ("Per Dóminum... in unitáte ejúsdem"; Rubr. gen. XI.2, p. 52)')
# ===== 4. Tracts: all seven Masses already carry the Missal's Tract in season.lent.tr (A5 looked only at parts.tr); verified on the scan
# C104s: stray Alleluia 6408 "Adjuva nos" (G50 p. 108*, the next Mass) in parts.al; p. 90* prints Alleluia Salvabo (5286) and the Paschal second Alleluia Confiteantur (5433) only
al=cur('data/masses.js',['masses','C104s','parts','al'])
setv('data/masses.js',['masses','C104s','parts','al'],[x for x in al if x['id']!=6408],'M39 pp. 90*-91* (pdf 413); G50 pp. 105*, 108*','stray Alleluia "Adjuva nos" (6408, G50 p. 108*, Mass pro remissione peccatorum) removed: the Missal prints for this Mass only "Allelúia, allelúia. V. Zach. 8 Salvábo pópulum meum" and "Temp. Pasch. secundum Allelúia. V. Ps. 106 Confiteántur" (p. 90*); "Adjuva nos" is here only a verse of the Tract (p. 91*)')
# ===== 5. data/memoriae.js against the scan (Rubr. gen. XI.1-2, p. 52); each change seen on the scan crop
mem('1007|SS. Sergii, Bacchi, Marcelli et Apuleji MM.','pc',[('protegámur: Per','protegámur. Per')],'M39 p. 571 (pdf 330)','punctuation as printed ("protegámur. Per Dóminum.")')
mem('0103|Octava S. Joannis Ap. et Ev.','or',[('illústra: ut, beáti','illústra: ut beáti'),('doctrínis, ad dona','doctrínis; ad dona')],'M39 (pdf 214)','punctuation as printed (flexa ";" after doctrínis)')
mem('0531|S. Angelæ Mericiæ Virg.','or',[('mereámur ætérnis: Per','mereámur ætérnis. Per')],'M39 (pdf 266)','punctuation as printed ("ætérnis. (Per Dóminum.)")')
mem('0531|S. Petronillæ Virg.','se',[('honóre Sanctórum, quorum','honóre Sanctórum: quorum')],'M39 (pdf 267)','punctuation as printed')
mem('0531|S. Petronillæ Virg.','pc',[('Satiásti Dómine famíliam','Satiásti, Dómine, famíliam')],'M39 (pdf 267)','punctuation as printed')
mem('0512|SS. Nerei, Achillei et Pancratii MM.','se',[('semper implóret. Per','semper implóret: Per')],'M39 (pdf 259)','punctuation as printed ("implóret: Per Dóminum.")')
mem('0702|SS. Processi et Martiniani MM.','pc',[('Córporis sacri et pretiósi','Córporis sacri, et pretiósi')],'M39 (pdf 282)','punctuation as printed; conclusion "Per eúmdem" as printed')
mem('0720|S. Margaritæ Virg. et Mart.','or',[('professióne virtútis: Per','professióne virtútis. Per')],'M39 (pdf 289)','punctuation as printed ("virtútis. Per Dóminum.")')
mem('0720|S. Margaritæ Virg. et Mart.','pc',[('protectióne confírment: Per','protectióne confírment. Per')],'M39 (pdf 289)','punctuation as printed ("confírment. Per Dóminum.")')
mem('0803|Inventio Corporis S. Stephani Protomartyris','or',[('exoráre Dóminum nostrum','exoráre: Dóminum nostrum')],'M39 (pdf 296)','punctuation as printed: "pro persecutóribus exoráre: Dóminum nostrum Jesum Christum Fílium tuum. Qui tecum." (the conclusion is "Qui tecum" because the Son is named at the end, Rubr. gen. XI.2, p. 52: "si in fine Orationis fiat ejus mentio, terminatur per Qui tecum vivit"; the Missal prints "Fílium tuum. Qui tecum" here; the pointing of the conclusion is left to apply_fixes.py canon())')
mem('0817|Octava S. Laurentii','or',[('quǽsumus, omnípotens Deus: vitiórum nostrorum','quǽsumus omnípotens Deus, vitiórum nostrórum'),('superáre. Per','superáre: Per')],'M39 (pdf 305)','punctuation (and the accent nostrórum) as printed: "Da nobis, quǽsumus omnípotens Deus, vitiórum nostrórum flammas exstínguere; ... superáre: Per Dóminum."')
mem('0817|Octava S. Laurentii','se',[('Accipe, quǽsumus, Dómine,','Accipe, quǽsumus Dómine,'),('et, beáti Lauréntii','et beáti Lauréntii')],'M39 (pdf 305)','punctuation as printed')
mem('0817|Octava S. Laurentii','pc',[('súpplices te, Dómine, deprecámur: ut, quod','súpplices te Dómine deprecámur: ut quod'),('offício, intercedénte','offício; intercedénte'),('augméntum. Per','augméntum: Per')],'M39 (pdf 305)','punctuation as printed (flexa ";" after offício; ":" before Per, text layer and scan)')
mem('1225|S. Anastasiæ Mart.','or',[('Da, quǽsumus, omnípotens Deus','Da, quǽsumus omnípotens Deus')],'M39 p. 22 (pdf 44)','punctuation as printed')
mem('1225|S. Anastasiæ Mart.','pc',[('Satiásti, Dómine, famíliam','Satiásti Dómine famíliam')],'M39 (pdf 45)','punctuation as printed (here without commas, unlike p. 31*)')
mem('Adv3w|Feria IV Quatuor Temporum Adventus','se',[('Acépta tibi','Accépta tibi'),('quǽsumus, Dómine, nostra ieiúnia: quæ','quǽsumus Dómine, nostra ieiúnia, quæ'),('ad sempiterna promíssa','ad sempitérna promíssa')],'M39 (pdf 38)','misspelling "Acépta" -> "Accépta"; accent sempitérna; punctuation as printed')
mem('0531|S. Angelæ Mericiæ Virg.','pc',[('et mente: Per','et mente. Per')],'M39 (pdf 267)','punctuation as printed ("et mente. (Per Dóminum.)")')
K='0701|Octava S. Joannis Baptistæ'
mem(K,'or',[('spirituálium grátiam','spiritálium grátiam'),('salútis ætérnæ. Per','salútis ætérnæ: Per')],'M39 p. 474 (pdf 276)','1 July (pdf 280): "Et fiat Memoria Octavae S. Joannis Bapt. cum Orationibus ut in Festo, p. 474"; word "spiritálium" as printed (not spirituálium); ":" before Per as printed')
mem(K,'se',[('cumulámus: illíus','cumulámus, illíus'),('cécinit ad futúrum et adésse monstravit, Dóminum','cécinit adfutúrum, et adésse monstrávit: Dóminum')],'M39 pp. 474-475 (pdf 276)','words and punctuation as printed: "cécinit adfutúrum, et adésse monstrávit: Dóminum nostrum Jesum Christum Fílium tuum; qui tecum." (Qui tecum: Rubr. gen. XI.2, p. 52, the Son named at the end)')
mem(K,'pc',[('lætítiam: per quem','lætítiam; per quem'),('auctórem, Dóminum','auctórem: Dóminum')],'M39 p. 475 (pdf 276)','punctuation as printed: "lætítiam; per quem ... auctórem: Dóminum nostrum Jesum Christum Fílium tuum; qui tecum."')
mem('Adv3w|Feria IV Quatuor Temporum Adventus','pc',[('Salutáris tui, Dómine, munere satiáti','Salutáris tui Dómine múnere satiáti'),('ut, cuius lætámur gustu, renovémur efféctu. Per','ut cuius lætámur gustu; renovémur efféctu: Per')],'M39 (pdf 38)','punctuation (flexa ";" after gustu, ":" before Per) and accent múnere as printed')
# ----- S0529b, S0602b (Joseph 27 Nov: switch readings by season, as the rubric says): Paschaltide "Officium Sancti tui, ut in Comm. plurim. Mart., pag. 15*", otherwise "Salus autem ..., p. 13*"
for k,pg in (('S0529b','p. 454 (pdf 266)'),('S0602b','p. 459 (pdf 268)')):
    for i in (0,1):
        for f in ('type','ref','title','title_en','la','en','p33'):
            if R[k][i].get(f)!=R['C21s'][i].get(f): rdset(k,i,f,R['C21s'][i][f],'M39 '+pg+'; readings M39 p. 13* (pdf 374)','extra T.P. readings = Comm. plurimorum Mart. Salus autem, p. 13* (C21s, scan-corrected by A5)')
    mr=M[k]['readings']; new=[{'type':R['C21s'][0]['type'],'ref':R['C21s'][0]['ref']},{'type':'Gospel','ref':R['C21s'][1]['ref']}]
    if [(x['type'],x['ref']) for x in mr]!=[(x['type'],x['ref']) for x in new]:
        cur('data/masses.js',['masses',k,'readings']); setv('data/masses.js',['masses',k,'readings'],new,'M39 '+pg,'refs of the readings actually given (Salus autem, p. 13*: Sap 10 / Luke 21); the old ref Hebr 11 is the Roman Missal\'s')
    sp=cur('data/masses.js',['masses',k,'season','pasch'])
    nsp=dict(sp); nsp['readings']=[{f:R['C28s'][i][f] for f in ('type','ref','title','title_en','la','en','p33') if f in R['C28s'][i]} for i in (0,1)]
    setv('data/masses.js',['masses',k,'season','pasch'],nsp,'M39 '+pg+'; readings M39 pp. 15*-17* (pdf 375-376)','rubric: "Temp. Pasch. Officium Sancti tui, ut in Comm. plurim. Mart., pag. 15*; Extra Temp. Pasch. Officium Salus autem ..., p. 13*": the Paschaltide readings (Apoc 19, John 15 = C28s, scan-corrected by A5) in season.pasch.readings; js/app.js seasonalReadings() must read them (see report)')
# the coordinator applied the earlier form of these three (with the conclusion's pointing as printed); per the coordinator (27 Nov), the conclusion's pointing is left to canon(): chain back
import fx6 as _f6
_LIVE=load('data/memoriae.js')
for _k,_p in (('0803|Inventio Corporis S. Stephani Protomartyris','or'),('0701|Octava S. Joannis Baptistæ','se'),('0701|Octava S. Joannis Baptistæ','pc')):
    _key=('data/memoriae.js',(_k,_p,0))
    if _LIVE[_k][_p][0]!=_f6.CUR[_key] and _LIVE[_k][_p][0]!=_f6.ORIG[_key]:
        _f6.CHAIN[_key]=(_LIVE[_k][_p][0],'conclusion pointing handed back to apply_fixes.py canon() (coordinator, 27 Nov): body punctuation as printed only')
