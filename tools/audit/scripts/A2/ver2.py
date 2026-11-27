R='data/readings33.js'; O='data/orations.js'; MS='data/masses.js'
SC='punctuation, capitals and words as printed (checked on scan)'
VER={}; EXTRA=[]
def v(k,f,src,why=SC): VER['%s|%s.%s'%(k,k,f)]=(src,why)
def x(path,src,why,file=R,**kw):
    d={'file':file,'path':path,'src':src,'why':why}; d.update(kw); EXTRA.append(d)
import sys; sys.path.insert(0,'/tmp/A2/new')
from douay import dr
# ---- Pent2
v('Pent2','or.0','M39 p. 261 (pdf 169R)')
v('Pent2','pc.0','M39 p. 263 (pdf 170R)')
v('Pent2','0.la','M39 p. 262 (pdf 170L)')
x(['Pent2','se',0],'M39 p. 262 (pdf 170L)',SC+' ("puríficet, et"; cæléstis; "actiónem. Per")',file=O,subs=[('puríficet: et','puríficet, et'),('cœléstis','cæléstis'),('actiónem: Per','actiónem. Per')])
x(['Pent2',1,'la'],'M39 p. 262 (pdf 170L)','the Gospel was cut at "dixit servo suo." (v. 21); completed as printed through "gustábit cenam meam." (Lk 14:16-24); cenam/cenæ as printed; capitals "Rogo"',
  new='In illo témpore: Dixit Jesus Pharisǽis parábolam hanc: Homo quidam fecit cenam magnam, et vocávit multos. Et misit servum suum hora cenæ dícere invitátis ut venírent quia jam paráta sunt ómnia. Et cœpérunt simul omnes excusáre. Primus dixit ei: Villam emi, et necésse hábeo exíre, et vidére illam: Rogo te, habe me excusátum. Et alter dixit: Juga boum emi quinque, et eo probáre illa: Rogo te, habe me excusátum. Et álius dixit: Uxórem duxi, et ídeo non possum veníre. Et revérsus servus, nuntiávit hæc dómino suo. Tunc irátus paterfamílias, dixit servo suo: Exi cito in platéas, et vicos civitátis: et páuperes, ac débiles, et cæcos, et claudos íntroduc huc. Et ait servus: Dómine, factum est ut imperásti, et adhuc locus est. Et ait dóminus servo: Exi in vias, et sepes: et compélle intráre, ut impleátur domus mea. Dico autem vobis, quod nemo virórum illórum, qui vocáti sunt, gustábit cenam meam.')
x(['Pent2',1,'ref'],'M39 p. 262 (pdf 170L)','the Gospel printed is Lk 14:16-24',new='Lucas 14: 16-24')
x(['masses','Pent2','readings',1,'ref'],'M39 p. 262 (pdf 170L)','the Gospel printed is Lk 14:16-24',file=MS,new='Lucas 14: 16-24')
x(['Pent2',1,'en'],'M39 p. 262 (pdf 170L)','English completed to v. 24 (Douay, bible/en Lucas 14:16-24 verse by verse); incipit to match "Dixit Jesus Pharisǽis parábolam hanc"',
  new='At that time: Jesus spoke this parable to the Pharisees: '+dr('Lucas',14,16,24,[('But he said to him: A certain man','A certain man')]))
x(['Pent2',0,'en'],'M39 p. 262 (pdf 170L)','English had "brethren", which the Latin ("Caríssimi: Nolíte mirári") does not have',subs=[('Wonder not, brethren, if','Wonder not, if')])
x(['masses','Pent2','parts','se'],'M39 p. 262 (pdf 170L): "Sequentia Lauda Sion, pag. 260"','the Missal prescribes the Sequence Lauda Sion in this Mass (Sunday within the Octave of Corpus Christi); masses.js had none. Same chant id as CorpusChristi.se (4211)',file=MS,op='add',new=[{'id':4211}])
x(['masses','Pent2','title'],'M39 p. 261 (pdf 169R): "Dominica infra Oct. Corporis Christi"','wrong word: "in Octavam" for "infra Octavam" (calendar style kept)',file=MS,subs=[('Dominica in Octavam','Dominica infra Octavam')])
# ---- SCJ (inserted leaf, M39 pp. 7-9 of the supplement = pdf 362R-363R)
v('SCJ','or.0','M39 suppl. p. 7 (pdf 362R)')
v('SCJ','se.0','M39 suppl. p. 9 (pdf 363R)')
v('SCJ','pc.0','M39 suppl. p. 9 (pdf 363R)')
x(['SCJ',0,'la'],'M39 suppl. p. 7 (pdf 362R)',SC,subs=[('divítias Christi, et illumináre','divítias Christi: et illumináre'),('in Deo, qui ómnia','in Deo qui ómnia'),('principátibus, et potestátibus','principátibus et potestátibus'),('sapiéntia Dei, secúndum','sapiéntia Dei: secúndum'),('sæculórum, quam fecit','sæculórum quam fecit'),('Dómino nostro: in quo','Dómino nostro, in quo'),('fidúciam, et accéssum','fidúciam et accéssum'),('in terra nominátur, ut','in terra nominátur: ut'),('interiórem hóminem, Christum','interiórem hóminem: Christum'),('radicáti, et fundáti, ut possítis comprehéndere cum','radicáti et fundáti: ut possítis comprehéndere, cum')])
x(['SCJ',1,'la'],'M39 suppl. p. 8 (pdf 363L)','punctuation as printed (no parentheses; "Parascéve erat, ut"); restores "ália" (íterum ália Scriptúra) and the garbled "Para parascéve erat)"',
  new='In illo témpore: Judǽi, quóniam Parascéve erat, ut non remanérent in cruce córpora sábbato, erat enim magnus dies ille sábbati, rogavérunt Pilátum ut frangeréntur eórum crura et tolleréntur. Venérunt ergo mílites, et primi quidem fregérunt crura et altérius qui crucifíxus est cum eo. Ad Jesum autem cum veníssent, ut vidérunt eum jam mórtuum, non fregérunt ejus crura: sed unus mílitum láncea latus ejus apéruit, et contínuo exívit sanguis et aqua. Et qui vidit testimónium perhíbuit: et verum est testimónium ejus. Et ille scit quia vera dicit, ut et vos credátis. Facta sunt enim hæc ut Scriptúra implerétur: Os non comminuétis ex eo. Et íterum ália Scriptúra dicit: Vidébunt in quem transfixérunt.')
# ---- Pent3
for f,p in [('or.0','M39 p. 265 (pdf 171R)'),('se.0','M39 p. 266 (pdf 172L)'),('pc.0','M39 p. 266 (pdf 172L)'),('0.la','M39 p. 265 (pdf 171R)'),('1.la','M39 p. 265 (pdf 171R)')]: v('Pent3',f,p)
x(['masses','Pent3','title'],'M39 p. 265 (pdf 171R): "Dominica infra Octavam SS. Cordis Jesu"','wrong word: "in Octavam" for "infra Octavam"',file=MS,subs=[('Dominica in Octavam','Dominica infra Octavam')])
# ---- PurCordisBMV
v('PurCordisBMV','0.la','M39 p. 317 (pdf 197R)')
v('PurCordisBMV','1.la','M39 p. 317 (pdf 197R)')
# ---- Pent4
for f,p in [('se.0','M39 p. 267 (pdf 172R)'),('pc.0','M39 p. 268 (pdf 173L)'),('0.la','M39 pp. 266-267 (pdf 172L-R)'),('1.la','M39 p. 267 (pdf 172R)')]: v('Pent4',f,p)
x(['Pent4','or',0],'M39 p. 266 (pdf 172L)',SC+' ("quǽsumus Dómine:")',file=O,subs=[('Da nobis, quǽsumus, Dómine:','Da nobis, quǽsumus Dómine:')])
x(['Pent4',0,'en'],'M39 p. 267 (pdf 172R)','English lacked the ending the Latin has ("In Christo Jesu Dómino nostro"), added as elsewhere on the site',subs=[('the redemption of our body.','the redemption of our body: in Christ Jesus our Lord.')])
# ---- Pent5
for f,p in [('or.0','M39 p. 268 (pdf 173L)'),('se.0','M39 p. 269 (pdf 173R)'),('pc.0','M39 p. 269 (pdf 173R)'),('0.la','M39 p. 268 (pdf 173L)'),('1.la','M39 p. 269 (pdf 173R)')]: v('Pent5',f,p)
x(['Pent5',0,'en'],'M39 p. 268 (pdf 173L)','English ran on into 1 Pet 3:15b, which the Latin (ends "sanctificáte in córdibus vestris") does not have',subs=[('in your hearts, being ready always to satisfy every one that asketh you a reason of that hope which is in you.','in your hearts.')])
x(['Pent5',1,'en'],'M39 p. 269 (pdf 173R)','English lacked "Dixit Jesus discípulis suis" and had "I tell you, that", which the Latin ("Nisi abundáverit") does not have',subs=[('At that time: I tell you, that unless','At that time: Jesus said to his disciples: Unless')])
# ---- Pent6
for f,p in [('or.0','M39 p. 269 (pdf 173R)'),('se.0','M39 p. 270 (pdf 174L)'),('pc.0','M39 p. 271 (pdf 174R)'),('0.la','M39 pp. 269-270 (pdf 173R-174L)'),('1.la','M39 p. 270 (pdf 174L)')]: v('Pent6',f,p)
x(['Pent6',0,'en'],'M39 p. 269 (pdf 173R)','English had "Know you not that" and a question, which the Latin ("Quicúmque baptizáti sumus … baptizáti sumus.") does not have',subs=[('Brethren: Know you not that all we, who are baptized in Christ Jesus, are baptized in his death?','Brethren: All we, who are baptized in Christ Jesus, are baptized in his death.')])
x(['Pent6',1,'en'],'M39 p. 270 (pdf 174L)','English had "Again", which the Latin ("Cum turba multa esset") does not have',subs=[('At that time: Again, when there was','At that time: When there was')])
# ---- Pent7
for f,p in [('or.0','M39 p. 271 (pdf 174R)'),('se.0','M39 p. 272 (pdf 175L)'),('pc.0','M39 p. 272 (pdf 175L)'),('0.la','M39 p. 271 (pdf 174R)'),('1.la','M39 p. 271 (pdf 174R)')]: v('Pent7',f,p)
x(['Pent7',1,'en'],'M39 p. 271 (pdf 174R)','English lacked "Dixit Jesus discípulis suis"',subs=[('At that time: Beware of','At that time: Jesus said to his disciples: Beware of')])
# ---- Pent8
for f,p in [('or.0','M39 p. 272 (pdf 175L)'),('se.0','M39 pp. 272-273 (pdf 175L-R)'),('pc.0','M39 p. 273 (pdf 175R)'),('0.la','M39 p. 272 (pdf 175L)'),('1.la','M39 pp. 272-273 (pdf 175L-R)')]: v('Pent8',f,p)
x(['Pent8',0,'en'],'M39 p. 272 (pdf 175L)','English had "Therefore" and ran on into Rom 8:17b, which the Latin (ends "coherédes autem Christi") does not have',subs=[('Therefore, brethren, we are debtors','Brethren: We are debtors'),('joint heirs with Christ: yet so, if we suffer with him, that we may be also glorified with him.','joint heirs with Christ.')])
x(['Pent8',1,'en'],'M39 p. 272 (pdf 175L)','English lacked "Jesus … parábolam hanc"',subs=[('At that time: He said also to his disciples:','At that time: Jesus spoke this parable to his disciples:')])
# ---- Pent9
for f,p in [('pc.0','M39 p. 275 (pdf 176R)'),('0.la','M39 p. 274 (pdf 176L)'),('1.la','M39 p. 274 (pdf 176L)')]: v('Pent9',f,p)
x(['Pent9','or',0],'M39 p. 273 (pdf 175R)',SC,file=O,subs=[('supplicántium: et, ut','supplicántium: et ut'),('fac eos quæ','fac eos, quæ'),('postuláre. Per','postuláre: Per')])
x(['Pent9','se',0],'M39 p. 274 (pdf 176L)',SC,file=O,subs=[('Concéde nobis, quǽsumus, Dómine,','Concéde nobis, quǽsumus Dómine,'),('mystéria: quia, quóties','mystéria: quia quóties')])
x(['Pent9',0,'en'],'M39 p. 274 (pdf 176L)','English had 1 Cor 10:6a, which the Latin (begins "Non simus concupiscéntes") does not have',subs=[('Brethren: These things were done in a figure of us, that we should not covet','Brethren: We should not covet')])
x(['Pent9',1,'en'],'M39 p. 274 (pdf 176L)','English ran on into Lk 19:47b, which the Latin (ends "docens quotídie in templo") does not have; incipit names Jesus and Jerusalem as the Latin does',subs=[(' And the chief priests and the scribes and the rulers of the people sought to destroy him:',''),('At that time: When he drew near,','At that time: When Jesus drew near to Jerusalem,')])
# ---- Pent10
for f,p in [('or.0','M39 p. 275 (pdf 176R)'),('se.0','M39 p. 276 (pdf 177L)'),('pc.0','M39 p. 276 (pdf 177L)'),('0.la','M39 p. 275 (pdf 176R)'),('1.la','M39 pp. 275-276 (pdf 176R-177L)')]: v('Pent10',f,p)
x(['Pent10',0,'ref'],'M39 p. 275 (pdf 176R)','the Epistle begins "Fratres: Scitis quóniam" (1 Cor 12:2), as masses.js already has',new='Ad Corinthios 1 12: 2-11')
x(['Pent10',0,'en'],'M39 p. 275 (pdf 176R)','English had 1 Cor 12:1, which the Latin (begins at v. 2) does not have',subs=[('Now concerning spiritual things, my brethren, I would not have you ignorant. You know that','Brethren: You know that')])
x(['Pent10',1,'en'],'M39 p. 275 (pdf 176R)','English to name Jesus as the Latin does ("Dixit Jesus ad quosdam")',subs=[('and despised others, he spoke also this parable:','and despised others, Jesus spoke also this parable:')])
# ---- Pent11
for f,p in [('or.0','M39 p. 276 (pdf 177L)'),('se.0','M39 p. 277 (pdf 177R)'),('pc.0','M39 p. 277 (pdf 177R)'),('0.la','M39 pp. 276-277 (pdf 177L-R)'),('1.la','M39 p. 277 (pdf 177R)')]: v('Pent11',f,p)
x(['Pent11',0,'en'],'M39 pp. 276-277 (pdf 177L-R)','English repeated "brethren" and ran on into 1 Cor 15:10b, which the Latin (ends "vácua non fuit") does not have',subs=[('Brethren: I make known unto you, brethren, the gospel','Brethren: I make known unto you the gospel'),('hath not been void, but I have laboured more abundantly than all they: yet not I, but the grace of God with me.','hath not been void.')])
x(['Pent11',1,'en'],'M39 p. 277 (pdf 177R)','English had "Again" and lacked the subject ("Exiens Jesus")',subs=[('At that time: Again going out of the coasts of Tyre, he came','At that time: Jesus going out of the coasts of Tyre, came')])
# ---- Pent12
for f,p in [('or.0','M39 p. 278 (pdf 178L)'),('se.0','M39 p. 279 (pdf 178R)'),('pc.0','M39 p. 279 (pdf 178R)'),('0.la','M39 p. 278 (pdf 178L)'),('1.la','M39 pp. 278-279 (pdf 178L-R)')]: v('Pent12',f,p)
# ---- Pent13
for f,p in [('or.0','M39 p. 279 (pdf 178R)'),('se.0','M39 p. 280 (pdf 179L)'),('pc.0','M39 p. 280 (pdf 179L)'),('0.la','M39 pp. 279-280 (pdf 178R-179L)'),('1.la','M39 p. 280 (pdf 179L)')]: v('Pent13',f,p)
# ---- Pent14
for f,p in [('or.0','M39 p. 281 (pdf 179R)'),('se.0','M39 p. 282 (pdf 180L)'),('pc.0','M39 p. 282 (pdf 180L)'),('0.la','M39 p. 281 (pdf 179R)'),('1.la','M39 pp. 281-282 (pdf 179R-180L)')]: v('Pent14',f,p)
x(['Pent14',0,'en'],'M39 p. 281 (pdf 179R)','English had "I say then", which the Latin ("Fratres: Spíritu ambuláte") does not have',subs=[('Brethren: I say then, walk in the spirit','Brethren: Walk in the spirit')])
# ---- Pent15
for f,p in [('or.0','M39 p. 282 (pdf 180L)'),('se.0','M39 p. 283 (pdf 180R)'),('pc.0','M39 p. 283 (pdf 180R)'),('0.la','M39 pp. 282-283 (pdf 180L-R)'),('1.la','M39 p. 283 (pdf 180R)')]: v('Pent15',f,p)
# ---- Pent16
for f,p in [('or.0','M39 p. 284 (pdf 181L)'),('se.0','M39 p. 285 (pdf 181R)'),('pc.0','M39 p. 285 (pdf 181R)'),('0.la','M39 p. 284 (pdf 181L)'),('1.la','M39 pp. 284-285 (pdf 181L-R)')]: v('Pent16',f,p)
x(['Pent16',0,'en'],'M39 p. 284 (pdf 181L)','English had "Wherefore", which the Latin ("Fratres: Obsecro vos") does not have',subs=[('Brethren: Wherefore I pray you','Brethren: I pray you')])
# ---- Pent17
for f,p in [('or.0','M39 p. 285 (pdf 181R)'),('se.0','M39 p. 286 (pdf 182L)'),('pc.0','M39 p. 286 (pdf 182L)'),('0.la','M39 pp. 285-286 (pdf 181R-182L)'),('1.la','M39 p. 286 (pdf 182L)')]: v('Pent17',f,p)
x(['Pent17',0,'en'],'M39 p. 285 (pdf 181R)','English had "therefore", which the Latin ("Obsecro vos ego vinctus") does not have',subs=[('Brethren: I therefore, a prisoner in the Lord,','Brethren: I, a prisoner in the Lord,')])
# ---- EmbWedSept
for f,p in [('or.0','M39 p. 287 (pdf 182R)'),('se.0','M39 p. 289 (pdf 183R)'),('pc.0','M39 p. 289 (pdf 183R)'),('0.la','M39 p. 287 (pdf 182R)'),('1.la','M39 pp. 287-288 (pdf 182R-183L)'),('2.la','M39 pp. 288-289 (pdf 183L-R)')]: v('EmbWedSept',f,p)
x(['EmbWedSept',1,'title'],'M39 p. 287 (pdf 182R): "Léctio Libri Esdræ. 2 Esd. 8"','heading as printed',new='Léctio libri Esdræ.')
x(['EmbWedSept',1,'title_en'],'M39 p. 287 (pdf 182R)','English heading to match the Latin',new='Lesson from the Book of Esdras.')
x(['EmbWedSept',1,'en'],'M39 p. 287 (pdf 182R)','English began with Neh 7:72b ("The seventh month came …"), which the Latin (begins "Congregátus est omnis pópulus") does not have',subs=[('In those days: The seventh month came: and the children of Israel were in their cities. And all the people','In those days: All the people')])
x(['EmbWedSept',0,'en'],'M39 p. 287 (pdf 182R)','English had "saith the Lord", which the Missal\'s Latin ("Ecce dies véniunt: et comprehéndet") does not have',subs=[('Behold the days come, saith the Lord, when','Behold the days come, when')])
x(['EmbWedSept','inter'],'M39 p. 287 (pdf 182R)','new field "inter": the collect after Lesson I and the Responsory Beata gens, preceded by "Dóminus vobíscum. Orémus"; the Missal prints "Secunda Oratio" A cunctis after it (the commemorations follow this collect) and "Oratio sequens non est dicenda pro memoria Q. T. in Missa festi … sed dici debet Oratio subsequens Præsta". English: St Dominic Missal 1959 (DM pdf p. 592), conclusion expanded',file=O,op='add',
  new=[{'after':0,'chant':True,'pre':'Dóminus vobíscum. Orémus.','la':'Præsta, quǽsumus Dómine, famíliæ tuæ supplicánti: ut dum a cibis corporálibus se ábstinet; a vítiis quoque mente jejúnet: Per Dóminum nostrum Iesum Christum Fílium tuum; qui tecum vivit et regnat in unitáte Spíritus Sancti Deus: per ómnia sǽcula sæculórum.','en':'Grant to Your suppliant flock, O Lord, we pray, that while denying meats to the body, they may also fast from the vices of the soul: through our Lord Jesus Christ, Your Son, who lives and reigns with You in the unity of the Holy Spirit, God, world without end.','src':'M39 p. 287 (pdf 182R)','en_src':'dm','rubric':'Secunda Oratio A cunctis; Tertia Oratio ad libitum (p. 287)'}])
