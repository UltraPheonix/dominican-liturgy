# ---- G555 = Graduale-page copy of the Immaculate Heart Mass (S0822; Missal leaf of 1945, pp. 4-6, pdf 361-362)
import copy
O=F.A.O; RD=F.A.RD; M=F.A.M
LEAF='M39 leaf "Immaculati Cordis B. M. V." pp. 4-6 (pdf 361-362)'
W='G555 is the Graduale-page copy of the Immaculate Heart Mass (same five chants as S0822: Adeamus, Exsultabit cor meum, Magnificat, Exsultavit spiritus meus, Dixit Jesus). Joseph (27 Nov 22:25, G385/G505): keep such copies and fix their readings to the Missal'
for p in ('or','se','pc'):
    RAW('data/orations.js',['G555',p],O['G555'][p],O['S0822'][p],LEAF,W+'; the prayer came from DO (src Sancti/08-22); now the leaf\'s text as on S0822 (Collect "in unitáte ejúsdem Spíritus Sancti", Rubr. gen. XI.2 p. 52; "propítius, ut ... recoléntes;"; Secret "qui Cor"; Postcommunion "solémnia ... égimus;")')
RAW('data/orations.js',['G555','src'],O['G555']['src'],O['S0822']['src'],LEAF,W)
RAW('data/masses.js',['masses','G555','readings'],M['G555']['readings'],M['S0822']['readings'],LEAF,W+'; the site had the Nativity of Our Lady\'s readings (Prov 8, Matth 1); the leaf prints Eccli 24:23-31 "Ego quasi vitis" and Jo 19:25-27 "Stabant juxta crucem"')
FX.append({"file":"data/readings33.js","op":"add","path":['G555'],"old":None,"new":copy.deepcopy(RD['S0822']),"src":LEAF,"why":W+'; the readings as printed on the leaf (= S0822, checked in session 3)'})
SUB('data/masses.js',['masses','G555','title'],[('Erucvtavit','Eructavit')],'G28/G50 incipit','OCR slip in the title')
SUB('data/masses.js',['masses','G555','en'],[('Erucvtavit','Eructavit')],'G28/G50 incipit','OCR slip in the title')
