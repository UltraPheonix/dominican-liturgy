# ---- G566 Holy Name of Mary (Totum Duplex) pp. 556-557 (pdf 317): readings33 had none (the app showed a Bible text)
import copy,sys; sys.path.insert(0,'/tmp/A4'); import dr
RD=F.A.RD
L0=copy.deepcopy(RD['S0814'][0]); L0['la']=L0['la'].replace('pulcræ','pulchræ'); assert 'pulchræ' in L0['la']; L0.pop('p33',None)
GLA=('In illo témpore: Missus est Angelus Gábriel a Deo in civitátem Galilǽæ, cui nomen Názareth, ad vírginem desponsátam viro, cui nomen erat Joseph, de domo David, et nomen vírginis María. '
 'Et ingréssus Angelus ad eam, dixit: Ave grátia plena: Dóminus tecum: Benedícta tu in muliéribus. Quæ cum audísset, turbáta est in sermóne ejus, et cogitábat qualis esset ista salutátio. '
 'Et ait Angelus ei: Ne tímeas María, invenísti enim grátiam apud Deum: Ecce concípies in útero, et páries fílium, et vocábis nomen ejus Jesum. Hic erit magnus, et fílius Altíssimi vocábitur, et dabit illi Dóminus Deus sedem David patris ejus: Et regnábit in domo Jacob in ætérnum, et regni ejus non erit finis. '
 'Dixit autem María ad Angelum: Quómodo fiet istud, quóniam virum non cognósco? Et respóndens Angelus, dixit ei: Spíritus Sanctus supervéniet in te, et virtus Altíssimi obumbrábit tibi. Ideóque et quod nascétur ex te Sanctum, vocábitur Fílius Dei. '
 'Et ecce Elísabeth cognáta tua, et ipsa concépit fílium in senectúte sua: Et hic mensis sextus est illi, quæ vocátur stérilis: quia non erit impossíbile apud Deum omne verbum. Dixit autem María: Ecce ancílla Dómini, fiat mihi secúndum verbum tuum.')
en=dr.v('Lucas',1,26,38)
o='And in the sixth month, the angel Gabriel'; assert en.startswith(o); en='At that time: The angel Gabriel'+en[len(o):]
o=' And the angel departed from her.'; assert en.endswith(o); en=en[:-len(o)].replace('Nazareth, To a virgin','Nazareth, to a virgin')
G0={"type":"Gospel","ref":"Lucas 1: 26-38","title":"Sequéntia sancti Evangélii secúndum Lucam.","title_en":"Continuation of the holy Gospel according to Luke.","la":GLA,"en":en}
FX.append({"file":"data/readings33.js","op":"add","path":['G566'],"old":None,"new":[L0,G0],"src":'M39 p. 556 (pdf 317)',"why":'the Missal prints the Lesson Eccli 24 "Ego quasi vitis" and the Gospel Luc 1 "Missus est Angelus Gábriel" (masses.js has these refs, but readings33 had no G566 entry, so the app showed a Bible text). Lesson as printed (= S0814, but this page prints "pulchræ"); Gospel transcribed from the scan; English Douay-Rheims (Lesson as S0814; Gospel Luke 1:26-38 without "And in the sixth month" and v. 38b, which the Missal omits)'})
