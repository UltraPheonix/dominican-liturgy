CENA=[(a,b,0) for a,b in [('cœnam','cenam'),('cœnávit','cenávit'),('cœnáculum','cenáculum'),('cœna ','cena '),('cœna,','cena,'),('cœnæ','cenæ'),('Cœnántibus','Cenántibus')]]
OV={
'Quad5s|Quad5s.1.la':[('moritúrus.)','moritúrus).')],
'Quad6|Quad6.0.la':[('nom¿ en: Hic genuflectitur¿:','nomen:')],
'Quad6|Quad6.1.la':[('Sciens autem jesus','Sciens autem Jesus'),('C Cenantibus¿','Cenántibus'),
  ('scandalizabor¿. C Ait illi Jesus: Arnen','scandalizábor. Ait illi Jesus: Amen'),('cum felle mistum','cum felle mixtum'),
  ('C Cxeunte¿','Exeúnte'),('plus quam','plusquam'),('p residis¿','prǽsidis')],
'Quad6m|Quad6m.1.la':CENA,
'Quad6t|Quad6t.1.la':CENA+[('ul¿','ut'),('petíssent','petiíssent'),('convitiabántur','conviciabántur')],
'Quad6w|Quad6w.2.la':CENA+[('hæc vidéntes. T ecce','hæc vidéntes. Et ecce')],
'Quad6h|Quad6h.0.la':CENA,
'Quad6h|Quad6h.1.la':CENA,
}
OV['Quad6|Quad6.1.la']=OV['Quad6|Quad6.1.la']+[('et omne concílium, quærébant','et omne concílium quærébant'),('Caíph','Cáiph')]
OV['Quad6m|Quad6m.pc.0']=[('delectémur et fructu','delectémur, et fructu')]
OV['Quad6m|Quad6m.0.la']=[('confúsus: ídeo','confúsus: Ídeo')]
OV['Quad6m|Quad6m.1.la']=OV['Quad6m|Quad6m.1.la']+[('nardi pístici pretiósi','nardi pístici, pretiósi'),('Sínite illam ut','Sínite illam, ut')]
OV['Quad6t|Quad6t.se.0']=[('quǽsumus, Dómine, propénsius','quǽsumus Dómine, propénsius')]
OV['Quad6t|Quad6t.0.la']=[('Dómine, demonstrásti','Dómine demonstrásti')]
OV['Quad6t|Quad6t.1.la']=OV['Quad6t|Quad6t.1.la']+[('Sínite, videámus si','Sínite, videámus, si'),('Jesus autem emíssa voce magna exspirávit.,.','Jesus autem, emíssa voce magna, exspirávit.'),('mirabátur si jam','mirabátur, si jam')]
OV['Quad6w|Quad6w.se.0']=[('Dómini nostri, mystério','Dómini nostri mystério')]
OV['Quad6w|Quad6w.2.la']=OV['Quad6w|Quad6w.2.la']+[
 ('regno )Dei.','regno Dei.'),('opportunitátem ut tráderet','opportunitátem, ut tráderet'),('in civitátem occúrret','in civitátem, occúrret'),
 ('Et accépto cálice grátias','Et accépto cálice, grátias'),('Dico enim vobis quod non bibam de generatióne vitis donec','Dico enim vobis, quod non bibam de generatióne vitis, donec'),
 ('Et accépto pane grátias','Et accépto pane, grátias'),('expetívit vos ut cribráret','expetívit vos, ut cribráret'),('rogávi pro te ut non','rogávi pro te, ut non'),
 ('tollat: simíliter','tollat simíliter'),('sudor ejus sicut','sudor ejus, sicut'),('appropinquávit Jesu ut','appropinquávit Jesu, ut'),
 ('qui vénerant ad se príncipes','qui vénerant ad se, príncipes'),('dixit illis: Oráte ne','dixit illis: Oráte, ne'),
 ('Et viri qui tenébant','Et viri, qui tenébant'),('S T v es Rex','Tu es Rex'),('At ille respóndens ait: Tu dicis','At ille respóndens, ait: Tu dicis'),
 ('Fílius hóminis sedens a dextris','Fílius hóminis, sedens a dextris'),('per diem festum unum','per diem festum, unum'),('et homicídium missus','et homicídium, missus'),
 ('Pater dimítte illis','Pater, dimítte illis'),('Respóndens autem alter increpábat','Respóndens autem alter, increpábat'),
 ('voce magna Jesus ait','voce magna Jesus, ait'),('exspirávit.,.','exspirávit.'),
 ('justus: hic non consénserat consílio, et áctibus eórum ab','justus: (hic non consénserat consílio, et áctibus eórum) ab')]
OV['Quad6w|Quad6w.2.la']=OV['Quad6w|Quad6w.2.la']+[('in agónia','in agonía'),('At illi instábant vócibus','At illi instábant, vócibus')]
OV['Quad6h|Quad6h.or.0']=[('Christus, Dóminus noster divérsa','Christus Dóminus noster divérsa')]
OV['Quad6h|Quad6h.0.la']=OV['Quad6h|Quad6h.0.la']+[('hoc fácite quotiescúmque bibétis','hoc fácite, quotiescúmque bibétis'),('reus erit Córporis et Sánguinis','reus erit Córporis, et Sánguinis')]
OV['Quad6|Quad6.1.la']=OV['Quad6|Quad6.1.la']+[('spíritum., et genuflectitur¿. Et ecce','spíritum. Et ecce'),('cum. eo','cum eo')]
OV['Quad6t|Quad6t.1.la']=OV['Quad6t|Quad6t.1.la']+[('exspirávit.,.','exspirávit.')]
