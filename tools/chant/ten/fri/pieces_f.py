# the washing of the altars (Triduum O.P. 1927, pp. 83-111): chant pieces = runs of staves (pdf page, side, staff index)
def rng(a, b):
    """'43R.0'..'44R.3' -> list of (pg, side, i) using the staff counts below"""
    import pickle, os
    S = pickle.load(open(os.environ.get('TRI_CACHE','/home/claude/build/tri_staves.pkl'), 'rb'))
    keys = []
    for k in sorted(S):
        for i in range(len(S[k])): keys.append((k[0], k[1], i))
    import re
    def p(s): m = re.match(r'(\d+)([LR])\.(\d+)', s); return (int(m.group(1)), m.group(2), int(m.group(3)))
    i0, i1 = keys.index(p(a)), keys.index(p(b))
    return keys[i0:i1 + 1]
P = [('t01', 'Astitérunt', '69R.0', '69R.1', 'Astitérunt reges terræ, et príncipes convenérunt in unum, advérsus Dóminum, et advérsus Christum ejus.'),
 ('t02', 'Divisérunt sibi', '70R.0', '70R.1', 'Divisérunt sibi vestiménta mea, et super vestem meam misérunt sortem.'),
 ('t03', 'Insurrexérunt', '71R.0', '71R.1', 'Insurrexérunt in me testes iníqui, et mentíta est iníquitas sibi.'),
 ('v01', 'Divisérunt sibi', '71R.2', '71R.3', '℣. Divisérunt sibi vestiménta mea. ℟. Et super vestem meam misérunt sortem.'),
 ('l01', 'Lectio I', '71R.4', '72R.1', 'De lamentatióne Jeremíæ Prophétæ. Aleph. Quómodo obtéxit calígine in furóre suo Dóminus fíliam Sion: projécit de cælo in terram ínclytam Israël, et non est recordátus scabélli pedum suórum in die furóris sui. Beth. Præcipitávit Dóminus, nec pepércit, ómnia speciósa Jacob: destrúxit in furóre suo munitiónes vírginis Juda, et dejécit in terram: pólluit regnum et príncipes ejus. Ghimel. Confrégit in ira furóris sui omne cornu Israël: avértit retrórsum déxteram suam a fácie inimíci: et succéndit in Jacob quasi ignem flammæ devorántis in gyro. Jerúsalem, Jerúsalem, convértere ad Dóminum Deum tuum.'),
 ('r01', 'Omnes amíci mei', '72R.2', '73L.0', 'Omnes amíci mei dereliquérunt me, et prævaluérunt insidiántes mihi: trádidit me quem diligébam: et terribílibus óculis plaga crudéli percutiéntes, * Acéto potábant me. ℣. Et dedérunt in escam meam fel, et in siti mea. * Acéto.'),
 ('l02', 'Lectio II', '73L.1', '73R.5', 'Daleth. Teténdit arcum suum quasi inimícus, firmávit déxteram suam quasi hostis: et occídit omne quod pulchrum erat visu in tabernáculo fíliæ Sion: effúdit quasi ignem indignatiónem suam. He. Factus est Dóminus velut inimícus, præcipitávit Israël: præcipitávit ómnia mœ́nia ejus, dissipávit munitiónes ejus, et replévit in fília Juda humiliátum et humiliátam. Vau. Et dissipávit quasi hortum tentórium suum: demolítus est tabernáculum suum: oblivióni trádidit Dóminus in Sion festivitátem et sábbatum: et in oppróbrium, et in indignatiónem furóris sui, regem et sacerdótem. Jerúsalem, Jerúsalem.'),
 ('r02', 'Velum templi', '73R.6', '74L.3', 'Velum templi scissum est, et omnis terra trémuit: latro de cruce clamábat, dicens: * Meménto mei, Dómine, dum véneris in regnum tuum. ℣. Amen dico tibi: hódie mecum eris in paradíso. * Meménto mei.'),
 ('l03', 'Lectio III', '74L.4', '74R.6', 'Zain. Répulit Dóminus altáre suum: maledíxit sanctificatióni suæ: trádidit in manu inimíci muros túrrium ejus: vocem dedérunt in domo Dómini sicut in die solémni. Heth. Cogitávit Dóminus dissipáre murum fíliæ Sion: teténdit funículum suum, et non avértit manum suam a perditióne: luxítque antemurále, et murus páriter dissipátus est. Teth. Defíxæ sunt in terra portæ ejus: pérdidit, et contrívit vectes ejus: regem ejus et príncipes ejus in géntibus: non est lex, et prophétæ ejus non invenérunt visiónem a Dómino. Jerúsalem, Jerúsalem.'),
 ('r03', 'Vínea mea', '74R.7', '75L.4', 'Vínea mea elécta, ego te plantávi: * Quómodo convérsa es in amaritúdinem, ut me crucifígeres, et Barábbam dimítteres? ℣. Ego quidem plantávi te víneam meam eléctam omne semen verum. * Quómodo. ℟. Vínea mea.'),
 ('t04', 'Vim faciébant', '76L.0', '76L.0', 'Vim faciébant, qui quærébant ánimam meam.'),
 ('t05', 'Confundántur', '76R.0', '76R.1', 'Confundántur, et revereántur, qui quærunt ánimam meam, ut áuferant eam.'),
 ('t06', 'Aliéni', '77L.1', '77L.2', 'Aliéni insurrexérunt in me, et fortes quæsiérunt ánimam meam.'),
 ('v02', 'Ab insurgéntibus', '77L.3', '77L.4', '℣. Ab insurgéntibus in me. ℟. Líbera me, Dómine.'),
 ('r04', 'Tamquam ad latrónem', '77R.0', '78L.3', 'Tamquam ad latrónem exístis cum gládiis comprehéndere me: quotídie apud vos eram in templo docens, et non me tenuístis: et ecce flagellátum dúcitis * Ad crucifigéndum. ℣. Fílius quidem hóminis vadit, sicut scriptum est de illo: væ autem hómini illi, per quem tradétur. * Ad crucifigéndum.'),
 ('r05', 'Ténebræ factæ sunt', '78R.0', '78R.7', 'Ténebræ factæ sunt, dum crucifixíssent Jesum Judǽi: et circa horam nonam exclamávit Jesus voce magna: Deus meus, Deus meus, ut quid me dereliquísti? * Et inclináto cápite emísit spíritum. ℣. Cum ergo accepísset acétum, dixit: Consummátum est. * Et inclináto.'),
 ('r06', 'Barábbas latro', '79L.0', '79R.2', 'Barábbas latro dimíttitur, et ínnocens Christus occíditur: nam et Judas armis doctus scéleris, qui per pacem dídicit fácere bellum, * Osculándo trádidit Dóminum Jesum Christum. ℣. Ecce turba, et qui vocabátur Judas, venit: et dum appropinquáret ad Jesum. * Osculándo. ℟. Barábbas.'),
 ('t07', 'Ab insurgéntibus', '80L.0', '80L.1', 'Ab insurgéntibus in me líbera me, Dómine, quia occupavérunt ánimam meam.'),
 ('t08', 'Longe fecísti', '81L.0', '81L.1', 'Longe fecísti notos meos a me: tráditus sum, et non egrediébar.'),
 ('t09', 'Captábunt', '81R.0', '81R.1', 'Captábunt in ánimam justi, et sánguinem innocéntem condemnábunt.'),
 ('v03', 'Locúti sunt', '82L.0', '82L.1', '℣. Locúti sunt advérsum me lingua dolósa. ℟. Et sermónibus ódii circumdedérunt me.'),
 ('r07', 'Tradidérunt me', '82L.2', '82R.5', 'Tradidérunt me in manus impiórum, et inter iníquos projecérunt me, et non pepercérunt ánimæ meæ: congregáti sunt advérsum me fortes: * Et sicut gigántes stetérunt contra me. ℣. Astitérunt reges terræ, et príncipes convenérunt in unum. * Et sicut.'),
 ('r08', 'Jesum trádidit', '83L.0', '83R.0', 'Jesum trádidit ímpius summis princípibus sacerdótum, et senióribus pópuli: Petrus autem sequebátur a longe, * Ut vidéret finem. ℣. Et ingréssus est Petrus in átrium príncipis sacerdótum. * Ut vidéret.'),
 ('r09', 'Sicut ovis', '83R.1', '84L.3', 'Sicut ovis ad occisiónem ductus est: et dum male tractarétur, non apéruit os suum: tráditus est ad mortem, * Ut vivificáret pópulum suum. ℣. Ipse vulnerátus est propter iniquitátes nostras: attrítus est propter scélera nostra. * Ut vivificáret. ℟. Sicut ovis.'),
 ('u01', 'Próprio Fílio', '84R.0', '84R.1', 'Próprio Fílio suo non pepércit Deus, sed pro nobis ómnibus trádidit illum.'),
 ('u02', 'Anxiátus est', '85R.0', '85R.1', 'Anxiátus est in me spíritus meus, in me turbátum est cor meum.'),
 ('u03', 'Ait latro', '86L.0', '86L.2', 'Ait latro ad latrónem: Nos quidem digna factis recípimus, hic autem quid fecit? Meménto mei, Dómine, dum véneris in regnum tuum.'),
 ('u04', 'Dum conturbáta', '87L.0', '87L.1', 'Dum conturbáta fúerit ánima mea, Dómine, misericórdiæ memor eris.'),
 ('u05', 'Meménto mei', '87R.0', '87R.1', 'Meménto mei, Dómine, dum véneris in regnum tuum.'),
 ('u06', 'Posuérunt', '89L.1', '89L.2', 'Posuérunt super caput ejus causam ipsíus scriptam: Jesus Nazarénus, Rex Judæórum.'),
 ('k01', 'Kyrie', '89L.3', '89L.3', 'Kýrie, eléison.'),
 ('k04', 'Dómine, miserére', '89L.6', '89L.6', 'Dómine, miserére.'),
 ('k05', 'Christus Dóminus', '89R.0', '89R.0', 'Christus Dóminus factus est obédiens usque ad mortem.'),
 ('k06', 'Agno miti', '89R.1', '89R.1', 'Agno miti básia cui lupus dedit venenósa.'),
 ('k07', 'Christe', '89R.2', '89R.2', 'Christe, eléison.'),
 ('k08', 'Vita in ligno', '89R.3', '89R.4', 'Vita in ligno móritur: inférnus et mors lugens spoliátur.'),
 ('k10', 'Te qui vinciri', '89R.6', '90L.0', 'Te qui vincíri voluísti, nosque a mortis vínculis eripuísti.'),
 ('k19', 'Mortem autem crucis', '90R.2', '90R.2', 'Mortem autem crucis.'),
 ('p2', 'Ps 2', '69L.0', '69L.1', 'Astitérunt. Quare fremuérunt gentes: et pópuli meditáti sunt inánia?'),
 ('p21', 'Ps 21', '69R.2', '69R.4', 'Divisérunt sibi. Deus, Deus meus, réspice in me: quare me dereliquísti? longe a salúte mea verba delictórum meórum.'),
 ('p26', 'Ps 26', '70R.2', '71L.0', 'Insurrexérunt. Dóminus illuminátio mea, et salus mea, quem timébo?'),
 ('p37', 'Ps 37', '75L.5', '75L.6', 'Vim faciébant. Dómine, ne in furóre tuo árguas me, neque in ira tua corrípias me.'),
 ('p39', 'Ps 39', '76L.1', '76L.2', 'Confundántur. Exspéctans exspectávi Dóminum, et inténdit mihi.'),
 ('p53', 'Ps 53', '76R.2', '77L.0', 'Aliéni. Deus, in nómine tuo salvum me fac: et in virtúte tua iúdica me.'),
 ('p58', 'Ps 58', '79R.3', '79R.5', 'Ab insurgéntibus. Éripe me de inimícis meis, Deus meus: et ab insurgéntibus in me líbera me.'),
 ('p87', 'Ps 87', '80R.0', '80R.1', 'Longe fecísti. Dómine, Deus salútis meæ: in die clamávi, et nocte coram te.'),
 ('p93', 'Ps 93', '81L.2', '81L.3', 'Captábunt. Deus ultiónum Dóminus: Deus ultiónum líbere egit.'),
 ('p50', 'Ps 50', '84L.4', '84L.5', 'Próprio. Miserére mei, Deus, secúndum magnam misericórdiam tuam.'),
 ('p142', 'Ps 142', '85L.0', '85L.2', 'Anxiátus est. Dómine, exáudi oratiónem meam: áuribus pércipe obsecratiónem meam in veritáte tua: exáudi me in tua iustítia.'),
 ('p62', 'Ps 62', '85R.2', '85R.3', 'Ait latro. Deus, Deus meus, ad te de luce vígilo.'),
 ('phab', 'Cant Habacuc', '86L.3', '86L.4', 'Dum conturbáta. Dómine, audívi auditiónem tuam, et tímui.'),
 ('p148', 'Ps 148', '87L.2', '87L.3', 'Meménto. Laudáte Dóminum de cælis: laudáte eum in excélsis.'),
 ('pben', 'Benedictus', '87R.2', '87R.4', 'Posuérunt. Benedíctus Dóminus, Deus Israël: quia visitávit, et fecit redemptiónem plebis suæ:')]
PM = []
MODES = {}
