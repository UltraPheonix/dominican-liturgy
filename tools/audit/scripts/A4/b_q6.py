# ---- Q6 ruling (Joseph, RULINGS.md): where the Missal's Latin departs from the Vulgate the English follows the Latin, labelled AI translation.
# Eccli 31:8: the Missal prints "Beátus vir" (Vulgate "Beatus dives"); the Douay "Blessed is the rich man" contradicts it.
PG={'S0604':'M39 p. 23* (pdf 379), Os justi alia Missa','S0613':'M39 p. 23* (pdf 379), Os justi alia Missa','S0715':'M39 p. 23* (pdf 379), Os justi alia Missa','S0718':'M39 p. 23* (pdf 379), Os justi alia Missa','S0807':'M39 p. 520 (pdf 299)','S0816':'M39 p. 530 (pdf 304)','S0831':'M39 p. 547 (pdf 312)','S0902':'M39 p. 549 (pdf 313)'}
for k,pg in PG.items():
    assert F.A.RD[k][0]['la'].startswith('Beátus vir, qui invéntus')
    EN(k,0,[('Blessed is the rich man that','Blessed is the man that')],pg,'the Missal prints "Beátus vir" (Vulgate Eccli 31:8 "Beatus dives"): the English follows the Missal\'s Latin (Joseph\'s ruling on Q6)')
    FX.append({"file":"data/readings33.js","op":"add","path":[k,0,'en_src'],"old":None,"new":'ai',"src":pg,"why":'label: the English is adapted to the Missal\'s Latin "Beátus vir", not Douay-Rheims verbatim (Joseph\'s ruling on Q6: labelled AI translation)'})
