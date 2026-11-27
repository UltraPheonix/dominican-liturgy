# ---- S0802 St Alphonsus pp. 513-515 (pdf 295-296); S0804 St Dominic pp. 516-518 (pdf 297-298); S0805 p. 518 + p. 1*
P('S0802','r1',[0,1,2,3,4,5,6,7],'M39 p. 514 (pdf 296)',why='as printed (the same Gospel as S0731): "duos, et misit"; "civitátem, et locum"; "messis, ut"; ": Et si"; ": Sin autem"; "edéntes, et"; ": Dignus"; ": Et curáte"')
EN('S0802',0,[('Dearly beloved: Thou therefore, my son, be strong','Dearly beloved: Be strong')],'M39 p. 514 (pdf 296)','the English added "Thou therefore, my son," (2 Tim 2:1a), which the Missal\'s Latin "Caríssime: Confortáre" does not have')
SUB('data/readings33.js',['S0804',0,'la'],[('est vivos et mórtuos','est vivos, et mórtuos'),(': árgue,',': Argue,'),('opus fac evangelístæ','opus fac Evangelístæ'),('in illa die, justus judex: non solum','in illa die justus judex: Non solum')],'M39 p. 516 (pdf 297)','as printed: "vivos, et"; "Argue"; "Evangelístæ"; "in illa die justus judex : Non solum"')
EN('S0804',0,[(' Make haste to come to me quickly.','')],'M39 p. 516 (pdf 297)','the English added v. 9 "Make haste to come to me quickly."; the Latin ends "advéntum ejus." (as S0614)')
P('S0804','r1',[0,1,2,4,5,6,7,8],'M39 pp. 517-518 (pdf 297-298)',why='as printed (the same Gospel as S0714/S0527): "pósita."; "Neque"; "ómnibus, qui"; "putáre, quóniam"; "legem, aut"; ": Non veni"; "dico vobis :"; ": Qui autem"')
import copy
def cp2(k,i,src):
    r=copy.deepcopy(RD[k][i]); r['p33']=None; r['src']=src+'; text as for '+k+' (checked on the scan; same page)'
    for x in ('do','do_sim','la_fixed'): r.pop(x,None)
    return r
RD=F.A.RD
NEW716=[e['new'] for e in FX0 if e.get('op')=='add' and e['path']==['S0716']][0]
FX.append({"file":"data/readings33.js","op":"add","path":['S0805'],"old":None,"new":copy.deepcopy(NEW716),"src":'M39 p. 518 "Officium Gaudeámus, ut in Festis B. Mariæ Virg., pag. 1*"; p. 1* (pdf 368)',"why":'no READINGS33 entry: the app showed a Bible text (and masses.js marks the Lesson ref "roman"). The Missal\'s Lesson Eccli 24 "Ab inítio" and Gospel Luc 11 "Loquénte Jesu" of p. 1*, as added for S0716'})
FX.append({"file":"data/masses.js","op":"add","path":['masses','S0805','parts','in',0,'m39text'],"old":None,"new":'Gaudeámus omnes in Dómino, diem festum celebrántes sub honóre beátæ Maríæ Vírginis, de cujus solemnitáte gaudent Angeli, et colláudant Fílium Dei. ℣. Ps. 44 Eructávit cor meum verbum bonum: dico ego ópera mea regi. Glória Patri.',"src":'M39 p. 518; p. 1* (pdf 368)',"why":'Joseph (27 Nov): print the Missal\'s text with the name; the site\'s 4289 sings "de cujus Nativitáte" (G50 p. 566), but p. 1* prints "de cujus solemnitáte"; no Dominican source prints the melody with this text. app.js must show this text, unnotated'})
