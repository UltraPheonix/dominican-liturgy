import sys; sys.path.insert(0,'/tmp/A1')
from s3lib import *
RD='data/readings33.js'; OR='data/orations.js'
FORM={'cj':'Rom 6: 23 "in Christ Jesus our Lord"','alm':'2 Cor 6: 18 "saith the Lord Almighty"','log':'Exod 8: 10 "the Lord our God"','hdd':'Amos 1: 3 "Thus saith the Lord:"','jc':'Rom 7: 25 "by Jesus Christ our Lord"'}
def dsrc(ref,extra=''):
    return 'English: Douay-Rheims, bible/en '+ref+(' ; '+extra if extra else '')
# ---- 1. Quad2 Epistle (1 Thess 4: 1-7) and Quad1s Epistle (1 Thess 5: 14-23): exact Douay
B='Ad Thessalonicenses 1'
v=[V(B,4,n) for n in range(1,8)]
assert v[0].startswith('For the rest therefore, brethren, we pray')
v[0]='Brethren: We pray'+v[0][len('For the rest therefore, brethren, we pray'):]
assert v[6].endswith('unto sanctification.'); v[6]=v[6][:-1]+': in Christ Jesus our Lord.'
q2=' '.join(v)
v=[V(B,5,n) for n in range(14,24)]
assert v[0].startswith('And we beseech you, brethren, rebuke'); v[0]='Brethren: We beseech you, rebuke'+v[0][len('And we beseech you, brethren, rebuke'):]
q1s=' '.join(v)
PG={'Quad2':'M39 p. 79 (pdf 73)','Quad1s':'M39 p. 78 (pdf 72)'}
EP={'Quad2':(1,q2,'1 Thess 4: 1-7','opening "For the rest therefore, brethren, we pray" -> "Brethren: We pray" (Missal "Fratres: Rogámus"); AI translation (Missal departs from the Vulgate): ": in Christ Jesus our Lord." for the Missal\'s "In Christo Jesu Dómino nostro" (wording after '+FORM['cj']+')'),
    'Quad1s':(6,q1s,'1 Thess 5: 14-23','opening "And we beseech you, brethren," -> "Brethren: We beseech you," (Missal "Fratres: Rogámus vos")')}
for k,(n,en,ref,note) in EP.items():
    fix(RD,[k,n,'en'],en,PG[k]+'; bible/en '+ref,'English replaced by the exact Douay-Rheims text, verse by verse ('+note+'); the earlier text was written from memory')
    fix(RD,[k,n,'src'],cur(RD,[k,n,'src']).split('; English:')[0]+'; '+dsrc(ref,note),PG[k],'source note: English now from bible/en')
# ---- 2. Adv3 Epistle: "our Lord"
edit(RD,['Adv3',0,'en'],[('minds in Christ Jesus.','minds in Christ Jesus our Lord.')],'M39 p. 5 (pdf 36); bible/en Phil 4: 7','English lacked "our Lord" of the Missal\'s ending "In Christo Jesu Dómino nostro" (Douay wording of the same Latin, '+FORM['cj']+')')
# ---- 3. Adv3s lessons (Missal formulas; extra Douay clauses not in the Latin)
I='Isaias'
l0=V(I,19,20); assert l0.startswith('It shall be for a sign'); l0='They shall cry'+l0[l0.index('For they shall cry')+len('For they shall cry'):]
l0='In those days: '+l0+' '+V(I,19,21)+' '+V(I,19,22)
assert l0.endswith('and heal them.'); l0=l0[:-1]+', the Lord our God.'
fix(RD,['Adv3s',0,'en'],l0,'M39 p. 11 (pdf 39); bible/en Isa 19: 20-22','English to the Latin: the Missal begins at v. 20b "Clamábunt" (Douay "It shall be for a sign ... For" dropped) and ends "sanábit eos Dóminus Deus noster" ("the Lord our God": Douay wording of the same Latin, '+FORM['log']+')')
l1=VV(I,35,1,6)+' '+V(I,35,7)
cut=' In the dens where dragons dwell before, shall rise up the verdure of the reed and the bulrush.'; assert l1.endswith(cut); l1=l1[:-len(cut)]
l1='Thus saith the Lord: '+l1+' Saith the Lord Almighty.'
fix(RD,['Adv3s',1,'en'],l1,'M39 p. 11 (pdf 39); bible/en Isa 35: 1-7','English to the Latin: Missal "Hæc dicit Dóminus:" ('+FORM['hdd']+') and "Ait Dóminus omnípotens." ('+FORM['alm']+'); v. 7b "In the dens ..." is not in the Missal')
l2=VV(I,40,9,11); c2=', and he himself shall carry them that are with young.'; assert l2.endswith(c2); l2='Thus saith the Lord: '+l2[:-len(c2)]+', the Lord our God.'
fix(RD,['Adv3s',2,'en'],l2,'M39 pp. 11-12 (pdf 39-40); bible/en Isa 40: 9-11','English to the Latin: Missal "Hæc dicit Dóminus:" ('+FORM['hdd']+'); it ends "in sinu suo levábit, Dóminus Deus noster" for the Vulgate "fœtas ipse portábit" ("the Lord our God": '+FORM['log']+')')
# Daniel (Adv3s rd4, Quad1s rd4): the Missal puts vv. 47-48 inside v. 50
D='Daniel'
v49=V(D,3,49); v50=V(D,3,50); v47=V(D,3,47); v48=V(D,3,48); v51=V(D,3,51)
assert v49.startswith('But the angel'); a49='The angel'+v49[len('But the angel'):]
s50='And made the midst of the furnace like the blowing of a wind bringing dew, '; assert v50.startswith(s50)
assert v48.endswith('near the furnace.')
dan='In those days: '+a49+' '+s50[:-2]+'. '+v47+' '+v48[:-1]+', the king’s servants that heated it. A'+v50[len(s50)+1:]+' '+v51
for k,pg in [('Adv3s','M39 pp. 12-13 (pdf 40)'),('Quad1s','M39 pp. 76-77 (pdf 72)')]:
    e=cur(RD,[k,4,'en'])
    fix(RD,[k,4,'en'],dan,pg+'; bible/en Dan 3: 47-51','English of the Latin added in session 2 ("Flamma autem effundebátur ... qui eam incendébant", which the Missal puts inside v. 50): Douay vv. 47-48 in the Missal\'s order; "the king’s servants that heated it" (Missal "minístros regis, qui eam incendébant", not in the Vulgate v. 48) is an AI translation (wording after Douay v. 46); opening "But the angel" -> "The angel"')
    fix(RD,[k,4,'ref'],'Daniel 3: 47-51',pg,'reference: the reading now includes vv. 47-48 (masses.js has 3: 47-51; the Missal prints only "c. 3")')
# ---- 4. Dec25_2
k='Dec25_2'
is61=VV(I,61,1,3)+' '+V(I,62,11)+' '+V(I,62,12)
c=' But thou shalt be called: A city sought after, and not forsaken.'; assert is61.endswith(c); is61=is61[:-len(c)]
assert is61.endswith('the redeemed of the Lord.'); is61='Thus saith the Lord: '+is61[:-1]+' our God.'
fix(RD,[k,0,'en'],is61,'M39 p. 21 (pdf 44); bible/en Isa 61: 1-3; 62: 11-12','English to the Latin: Missal "Hæc dicit Dóminus:" ('+FORM['hdd']+'); ends "redémpti a Dómino Deo nostro" (Douay v. 12b "But thou shalt be called ..." is not in the Missal)')
t=VV('Ad Titum',3,4,7); a='But when the goodness and kindness of God our Saviour appeared:'; assert t.startswith(a)
t='Dearly beloved: The goodness and kindness of God our Saviour appeared:'+t[len(a):]
assert t.endswith('life everlasting.'); t=t[:-1]+': in Christ Jesus our Lord.'
fix(RD,[k,1,'en'],t,'M39 p. 21 (pdf 44); bible/en Titus 3: 4-7','English to the Latin: v. 4 was missing ("Appáruit benígnitas ... Dei"; opening "But when" dropped as in the Missal) and the ending "In Christo Jesu Dómino nostro" ('+FORM['cj']+')')
g=VV('Lucas',2,15,20); a='And it came to pass, after the angels departed from them into heaven, the shepherds said'; assert g.startswith(a)
g='At that time: The shepherds said'+g[len(a):]
fix(RD,[k,2,'en'],g,'M39 p. 22 (pdf 45); bible/en Luke 2: 15-20','English to the Latin: the Missal begins "Pastóres loquebántur ad ínvicem" (Douay "And it came to pass, after the angels departed from them into heaven," not in the Latin)')
# ---- 5. Nat1 Gospel
g=VV('Lucas',2,33,40); a='And his father and mother were wondering'; assert g.startswith(a)
g='At that time: Joseph and Mary the mother of Jesus were wondering'+g[len(a):]
fix(RD,['Nat1',1,'en'],g,'M39 p. 26 (pdf 47); bible/en Luke 2: 33-40','English to the Latin: the Missal reads "Erat Joseph, et María mater Jesu mirántes" for the Vulgate "pater ejus et mater"; "Joseph and Mary the mother of Jesus" is an AI translation of these words, the rest Douay')
# ---- 6. Epi5 Epistle
edit(RD,['Epi5',0,'en'],[('to God and the Father by him.','to God and the Father by Jesus Christ our Lord.')],'M39 p. 45 (pdf 56); bible/en Col 3: 17','English to the Latin: the Missal ends "per Jesum Christum Dóminum nostrum" for the Vulgate "per ipsum" (Douay wording of the same Latin, '+FORM['jc']+')')
# ---- 7. Quad1f
e=cur(RD,['Quad1f',0,'en']); assert e.endswith('he shall save his soul alive.')
fix(RD,['Quad1f',0,'en'],e+' '+V('Ezechiel',18,28)+' Saith the Lord Almighty.','M39 p. 74 (pdf 70); bible/en Ezek 18: 28','English completed: v. 28 (Douay) and the Missal\'s "Ait Dóminus omnípotens." ('+FORM['alm']+')')
j=VV('Joannes',5,1,15); a='After these things was a festival day'; assert j.startswith(a)
j='At that time: There was a festival day'+j[len(a):]
fix(RD,['Quad1f',1,'en'],j,'M39 pp. 74-75 (pdf 70-71); bible/en John 5: 1-15','English completed to v. 15 (it stopped at v. 7) from Douay; opening: the Missal begins "Erat dies festus" (Douay "After these things", Vulgate "Post hæc", not in the Missal; "There was" supplied)')
# ---- labels (RULINGS 27 Nov 23:00: where the Missal's Latin departs from the Vulgate the English follows the Latin, labelled "AI translation")
def label(k,n,txt,pg):
    r=cur(RD,[k,n])
    if 'src' in r: fix(RD,[k,n,'src'],r['src'].rstrip('. ')+'; '+txt,pg,'English source label')
    else: add(RD,[k,n,'src'],txt,pg,'English source label (new key)')
AI='AI translation (Missal departs from the Vulgate): '
label('Adv3',0,'English: Douay-Rheims (bible/en Phil 4: 4-7); '+AI+'"our Lord" (Missal "Dómino nostro")','M39 p. 5 (pdf 36)')
label('Adv3s',0,'English: Douay-Rheims (bible/en Isa 19: 20b-22); '+AI+'", the Lord our God" (Missal "Dóminus Deus noster")','M39 p. 11 (pdf 39)')
label('Adv3s',1,'English: Douay-Rheims (bible/en Isa 35: 1-7a); '+AI+'"Thus saith the Lord:" and "Saith the Lord Almighty." (Missal "Hæc dicit Dóminus", "Ait Dóminus omnípotens")','M39 p. 11 (pdf 39)')
label('Adv3s',2,'English: Douay-Rheims (bible/en Isa 40: 9-11); '+AI+'"Thus saith the Lord:" and ", the Lord our God." (Missal "Hæc dicit Dóminus", "Dóminus Deus noster" for the Vulgate "fœtas ipse portábit")','M39 pp. 11-12 (pdf 39-40)')
for k,pg in [('Adv3s','M39 pp. 12-13 (pdf 40)'),('Quad1s','M39 pp. 76-77 (pdf 72)')]:
    label(k,4,'English: Douay-Rheims (bible/en Dan 3: 47-51, in the Missal\'s order 49, 50a, 47, 48, 50b, 51); '+AI+'"the king’s servants that heated it" (Missal "minístros regis, qui eam incendébant")',pg)
label('Dec25_2',0,'English: Douay-Rheims (bible/en Isa 61: 1-3; 62: 11-12a); '+AI+'"Thus saith the Lord:" and "our God" (Missal "Hæc dicit Dóminus", "a Dómino Deo nostro")','M39 p. 21 (pdf 44)')
label('Dec25_2',1,'English: Douay-Rheims (bible/en Titus 3: 4-7); '+AI+'"in Christ Jesus our Lord" (Missal "In Christo Jesu Dómino nostro")','M39 p. 21 (pdf 44)')
label('Nat1',1,'English: Douay-Rheims (bible/en Luke 2: 33-40); '+AI+'"Joseph and Mary the mother of Jesus" (Missal "Joseph, et María mater Jesu")','M39 p. 26 (pdf 47)')
label('Epi5',0,'English: Douay-Rheims (bible/en Col 3: 12-17); '+AI+'"by Jesus Christ our Lord" (Missal "per Jesum Christum Dóminum nostrum")','M39 p. 45 (pdf 56)')
label('Quad1f',0,'English: Douay-Rheims (bible/en Ezek 18: 20-28); '+AI+'"Saith the Lord Almighty." (Missal "Ait Dóminus omnípotens")','M39 p. 74 (pdf 70)')
label('Quad1f',1,'English: Douay-Rheims (bible/en John 5: 1-15); opening "There was" supplied for the Missal\'s "Erat dies festus" (Douay "After these things was")','M39 pp. 74-75 (pdf 70-71)')
