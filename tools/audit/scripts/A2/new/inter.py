import sys,json; sys.path.insert(0,'/tmp/A2/new')
from add import add
PD=' Per Dóminum nostrum Iesum Christum, Fílium tuum; qui tecum vivit et regnat in unitáte Spíritus Sancti Deus: per ómnia sǽcula sæculórum.'
PDE=' Per Dóminum nostrum Iesum Christum, Fílium tuum; qui tecum vivit et regnat in unitáte eiúsdem Spíritus Sancti Deus: per ómnia sǽcula sæculórum.'
PE=' Per eúndem Dóminum nostrum Iesum Christum, Fílium tuum; qui tecum vivit et regnat in unitáte Spíritus Sancti Deus: per ómnia sǽcula sæculórum.'
QT=' Qui tecum vivit et regnat in unitáte eiúsdem Spíritus Sancti Deus: per ómnia sǽcula sæculórum.'
EPD=' through our Lord Jesus Christ, Your Son, who lives and reigns with You in the unity of the Holy Spirit, God, world without end.'
EPDE=' through our Lord Jesus Christ, Your Son, who lives and reigns with You in the unity of the same Holy Spirit, God, world without end.'
EPE=' through the same Lord Jesus Christ, Your Son, who lives and reigns with You in the unity of the Holy Spirit, God, world without end.'
EQT=' who lives and reigns with You in the unity of the same Holy Spirit, God, world without end.'
def it(after,chant,pre,la,en,src,en_src,**kw):
    d={"after":after,"chant":chant,"pre":pre,"la":la,"en":en,"src":src,"en_src":en_src}; d.update(kw); return d
OR='Orémus.'
INTER={
'Pasc6s':[
 it(0,False,OR,'Deus, qui in Abrahæ fámuli tui ópere, humáno géneri obediéntiæ exémpla præbuísti: concéde nobis, et nostræ voluntátis pravitátem frángere; et tuórum præceptórum rectitúdinem in ómnibus adimplére:'+PD,
   'O God, who in the deed of Abraham Your servant gave mankind an example of obedience, grant us both to break the perverseness of our own will and to fulfil in all things the uprightness of Your commandments:'+EPD,'M39 p. 240 (pdf 159L)','ai'),
 it(1,True,OR,'Deus, qui nobis per Prophetárum ora præcepísti temporália relínquere, atque ad ætérna festináre; da fámulis tuis: ut quæ a te jussa cognóvimus; implére cælésti inspiratióne valeámus:'+PD,
   'O God, who by the mouths of the Prophets have commanded us to forsake the things of time and to hasten to the things eternal, grant to Your servants that what we know to have been commanded by You we may be able to fulfil by heavenly inspiration:'+EPD,'M39 p. 241 (pdf 159R)','ai'),
 it(2,True,OR,'Deus, qui nos ad celebrándam hanc festivitátem utriúsque testaménti páginis ínstruis: da nobis intellígere misericórdiam tuam; ut ex perceptióne præséntium múnerum, firma sit exspectátio futurórum:'+PD,
   'O God, who by the pages of both Testaments instruct us to celebrate this festival, grant us to understand Your mercy, that by receiving present gifts we may have a firm expectation of those to come:'+EPD,'M39 p. 241 (pdf 159R)','ai'),
 it(3,False,OR,'Deus incommutábilis virtus, et lumen ætérnum; réspice propítius ad totíus Ecclésiæ mirábile sacraméntum: et da fámulis tuis, ut quod devóte ágimus; étiam rectitúdine vitæ teneámus:'+PD,
   'O God, unchangeable power and eternal light, look mercifully upon the wondrous sacrament of the whole Church, and grant to Your servants that what we devoutly perform we may also hold fast by uprightness of life:'+EPD,'M39 p. 242 (pdf 160L)','ai'),
 it(3,True,OR,'Concéde, quǽsumus omnípotens Deus: ut qui solemnitátem doni Sancti Spíritus cólimus; cæléstibus desidériis accénsi, fontem vitæ sitiámus:'+PDE,
   'Grant, we beseech You, almighty God, that we who keep the solemnity of the gift of the Holy Spirit, being kindled with heavenly desires, may thirst for the fountain of life:'+EPDE,'M39 p. 243 (pdf 160R)','ai',
   rubric='Finita hac Oratione, dicantur Litaniæ sicut in Sabbato Sancto, pag. 185.'),
],
'Quad6w':[
 it(0,True,'Dóminus vobíscum. Orémus. Flectámus génua. Leváte.','Deus, qui pro nobis Fílium tuum crucis patíbulum subíre voluísti, ut inimíci a nobis expélleres potestátem; concéde nobis fámulis tuis, ut resurrectiónis grátiam consequámur:'+PE,
   'O God, who would have Your Son suffer for us on the gibbet of the cross, to deliver us from the power of the enemy, grant to us Your servants that we may obtain the grace of His resurrection:'+EPE,'M39 p. 154 (pdf 111L)','dm',
   rubric='Secunda et tertia Oratio, pag. 63'),
],
'Pent0w':[
 it(0,True,'Dóminus vobíscum. Orémus.','Præsta, quǽsumus omnípotens et miséricors Deus; ut Spíritus Sanctus advéniens, templum nos glóriæ suæ dignánter inhabitándo perfíciat:'+PDE,
   'Grant, we beseech You, almighty and merciful God, that the Holy Spirit may come upon us, and by His indwelling make us worthy to be the temples of His glory:'+EPDE,'M39 p. 250 (pdf 164L)','dm'),
],
'Pent0s':[
 it(0,True,OR,'Illo nos igne, quǽsumus Dómine, Spíritus Sanctus inflámmet: quem Dóminus noster Jesus Christus misit in terram; et vóluit veheménter accéndi:'+QT,
   'Let the Holy Spirit, we beseech You, O Lord, inflame us with that fire which our Lord Jesus Christ cast upon the earth, and earnestly longed to be enkindled:'+EQT,'M39 p. 254 (pdf 166L)','dm'),
 it(1,True,OR,'Deus, qui ad animárum medélam, jejúnii devotióne castigári córpora præcepísti; concéde nobis propítius, et mente et córpore tibi semper esse devótos:'+PD,
   'O God, You have commanded our souls to be healed when our bodies are chastened by the service of fasting; mercifully grant that we may ever serve You in soul and body:'+EPD,'M39 p. 255 (pdf 166R)','dm'),
 it(2,True,OR,'Præsta, quǽsumus omnípotens Deus: ut salutáribus jejúniis erudíti; ab ómnibus étiam vítiis abstinéntes, propitiatiónem tuam facílius impetrémus:'+PD,
   'Grant to us, O Lord, we beseech You, that taught by these healthful fastings and abstaining from all harmful indulgences, we may the more easily obtain Your mercies:'+EPD,'M39 p. 255 (pdf 166R)','dm'),
 it(3,True,OR,'Præsta, quǽsumus omnípotens Deus, sic nos ab épulis carnálibus abstinére; ut a vítiis irruéntibus páriter jejunémus:'+PD,
   'Grant us, almighty God, we pray, so to abstain from food, that we may likewise fast from the vices that attack us:'+EPD,'M39 p. 256 (pdf 167L)','dm'),
 it(4,True,'Dóminus vobíscum. Orémus.','Deus, qui tribus púeris mitigásti flammas ígnium; concéde propítius, ut nos fámulos tuos non exúrat flamma vitiórum:'+PD,
   'O God, who tempered the flames of fire for the three young men, mercifully grant that we Your servants may not be consumed by the flames of vice:'+EPD,'M39 p. 256 (pdf 167L)','dm'),
],
}
WHY={
'Pasc6s':'the collects after the prophecies (M39 pp. 240-243) were missing; "Quinque sequentes Orationes sine Dominus vobiscum dicantur: sed dicatur statim Oremus" (p. 240). after = index of the lesson in readings33 Pasc6s; chant = said after the Tract that follows the lesson (Lesson IV: Deus incommutabilis before the Tract Sicut cervus, Concede after it, p. 242-243). English: AI translation of the Missal\'s Latin (the 1959 Missal has no prophecies; RULINGS 27 Nov 22:05)',
'Quad6w':'the collect after Lesson I and the Responsory Ne avertas (p. 154) was missing from orations.js; it is preceded by "Dóminus vobíscum. Orémus. Flectámus génua. Leváte." and followed by the rubric "Secunda et tertia Oratio, pag. 63" (the commemorations go after this collect). English: St Dominic Missal 1959 as in data/holyweek_text.js, conclusion expanded',
'Pent0w':'the collect after Lesson I and the Alleluia Spiritus Domini (p. 250; Rubr. gen. XIII.3, p. 53: "post quamlibet Lectionem in quarta Feria, et Sabbato Quatuor Temporum Pentecostes dicuntur Alleluia eo modo, quo ibidem signantur") was missing. English: St Dominic Missal 1959 (dm1959 text layer, DM pdf p. 508), conclusion expanded',
'Pent0s':'the collects after Lessons I-V, each after its Alleluia (pp. 254-256), were missing; "Quinque Orationes sequentes dicantur sine Dominus vobiscum... sed dicatur Oremus" (p. 254: the Collect Mentibus and the four after Lessons I-IV); the fifth (after Daniel) is preceded by "Dóminus vobíscum." (p. 256). English: St Dominic Missal 1959 (dm1959 text layer, DM pdf pp. 518-523; OCR slips "0 Lord", "serv;ice", "us,." fixed), conclusions expanded',
}
if __name__=='__main__':
    E=[]
    for k,v in INTER.items():
        E.append({"file":"data/orations.js","path":[k,"inter"],"op":"add","old":None,"new":v,"src":'; '.join(sorted(set(x['src'] for x in v))),"why":"new field \"inter\" (brief step 2): "+WHY[k]})
        for x in v: print(k,x['after'],x['chant'],'|',x['pre'],'|',x['la'],'\n   ',x['en'])
    add(E)
