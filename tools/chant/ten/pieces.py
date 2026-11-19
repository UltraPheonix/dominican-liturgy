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
P = [('t01', 'Zelus domus tuæ', '3R.0', '4L.0', 'Zelus domus tuæ comédit me, et oppróbria exprobrántium tibi cecidérunt super me.'),
 ('t02', 'Avertántur retrórsum', '4L.3', '4L.4', 'Avertántur retrórsum, et erubéscant, qui cógitant mihi mala.'),
 ('t03', 'Deus meus, éripe me', '5L.0', '5L.0', 'Deus meus, éripe me de manu peccatóris.'),
 ('v01', 'Exsúrge, Dómine', '5L.1', '5L.2', '℣. Exsúrge, Dómine. ℟. Et júdica causam meam.'),
 ('l01', 'Lectio I', '5R.0', '6L.3', 'Incipit lamentátio Jeremíæ Prophétæ. Aleph. Quómodo sedet sola cívitas plena pópulo: facta est quasi vídua dómina géntium: princeps provinciárum facta est sub tribúto. Beth. Plorans plorávit in nocte, et lácrimæ ejus in maxíllis ejus: non est qui consolétur eam ex ómnibus caris ejus: omnes amíci ejus sprevérunt eam, et facti sunt ei inimíci. Ghimel. Migrávit Judas propter afflictiónem, et multitúdinem servitútis: habitávit inter gentes, nec invénit réquiem: omnes persecutóres ejus apprehendérunt eam inter angústias. Jerúsalem, Jerúsalem, convértere ad Dóminum Deum tuum.'),
 ('l02', 'Lectio II', '6R.3', '7L.6', 'Daleth. Viæ Sion lugent eo quod non sint qui véniant ad solemnitátem: omnes portæ ejus destrúctæ: sacerdótes ejus geméntes: vírgines ejus squálidæ, et ipsa oppréssa amaritúdine. He. Facti sunt hostes ejus in cápite, inimíci ejus locupletáti sunt: quia Dóminus locútus est super eam propter multitúdinem iniquitátum ejus: párvuli ejus ducti sunt in captivitátem, ante fáciem tribulántis. Vau. Et egréssus est a fília Sion omnis decor ejus: facti sunt príncipes ejus velut aríetes non inveniéntes páscua: et abiérunt absque fortitúdine ante fáciem subsequéntis. Jerúsalem, Jerúsalem.'),
 ('l03', 'Lectio III', '7R.7', '8R.3', 'Zain. Recordáta est Jerúsalem diérum afflictiónis suæ, et prævaricatiónis ómnium desiderabílium suórum, quæ habúerat a diébus antíquis, cum cáderet pópulus ejus in manu hostíli, et non esset auxiliátor: vidérunt eam hostes, et derisérunt sábbata ejus. Heth. Peccátum peccávit Jerúsalem, proptérea instábilis facta est: omnes, qui glorificábant eam, sprevérunt illam, quia vidérunt ignomíniam ejus: ipsa autem gemens convérsa est retrórsum. Teth. Sordes ejus in pédibus ejus, nec recordáta est finis sui: depósita est veheménter, non habens consolatórem: vide, Dómine, afflictiónem meam, quóniam eréctus est inimícus. Jerúsalem, Jerúsalem.'),
 ('t04', 'Liberávit Dóminus', '10L.0', '10L.1', 'Liberávit Dóminus páuperem a poténte: et ínopem, cui non erat adjútor.'),
 ('t05', 'Cogitavérunt ímpii', '10R.0', '10R.1', 'Cogitavérunt ímpii, et locúti sunt nequítiam: iniquitátem in excélso locúti sunt.'),
 ('t06', 'Exsúrge, Dómine', '11R.0', '11R.0', 'Exsúrge, Dómine, et júdica causam meam.'),
 ('v02', 'Deus meus', '11R.1', '11R.2', '℣. Deus meus, éripe me de manu peccatóris. ℟. Et de manu contra legem agéntis et iníqui.'),
 ('t07', 'Dixi iníquis', '14L.2', '14L.3', 'Dixi iníquis: Nolíte loqui advérsus Deum iniquitátem.'),
 ('t08', 'Terra trémuit', '14R.2', '14R.3', 'Terra trémuit et quiévit, dum resúrgeret in judícium Deus.'),
 ('t09', 'In die tribulatiónis', '15R.0', '15R.1', 'In die tribulatiónis meæ Deum exquisívi mánibus meis.'),
 ('v03', 'Homo pacis meæ', '15R.2', '15R.3', '℣. Homo pacis meæ, in quo sperávi. ℟. Ampliávit advérsum me supplantatiónem.')]
P += [('u01', 'Justificéris', '18L.0', '18L.1', 'Justificéris, Dómine, in sermónibus tuis, et vincas cum judicáris.'),
 ('u02', 'Dóminus tamquam ovis', '19L.0', '19L.1', 'Dóminus tamquam ovis ad víctimam ductus est, et non apéruit os suum.'),
 ('u03', 'Contrítum est', '19R.0', '19R.1', 'Contrítum est cor meum in médio mei: contremuérunt ómnia ossa mea.'),
 ('u04', 'Exhortátus es', '20L.0', '20R.0', 'Exhortátus es in virtúte tua, et in refectióne sancta tua, Dómine.'),
 ('u05', 'Oblátus est', '20R.3', '21L.0', 'Oblátus est, quia ipse vóluit: et peccáta nostra ipse portávit.'),
 ('b01', 'Benedictus', '21L.1', '22L.6', 'Benedíctus Dóminus Deus Israël: quia visitávit, et fecit redemptiónem plebis suæ: Et eréxit cornu salútis nobis: in domo David, púeri sui. Sicut locútus est per os sanctórum, qui a sǽculo sunt, prophetárum ejus: Salútem ex inimícis nostris, et de manu ómnium, qui odérunt nos: Ad faciéndam misericórdiam cum pátribus nostris: et memorári testaménti sui sancti. Jusjurándum, quod jurávit ad Ábraham patrem nostrum, datúrum se nobis: Ut sine timóre, de manu inimicórum nostrórum liberáti, serviámus illi. In sanctitáte, et justítia coram ipso, ómnibus diébus nostris. Et tu, puer, Prophéta Altíssimi vocáberis: præíbis enim ante fáciem Dómini paráre vias ejus: Ad dandam sciéntiam salútis plebi ejus: in remissiónem peccatórum eórum: Per víscera misericórdiæ Dei nostri: in quibus visitávit nos, óriens ex alto: Illumináre his, qui in ténebris, et in umbra mortis sedent: ad dirigéndos pedes nostros in viam pacis.'),
 ('u06', 'Tráditor autem', '22L.7', '22R.0', 'Tráditor autem dedit eis signum, dicens: Quem osculátus fúero, ipse est, tenéte eum.'),
 ('k01', 'Kyrie (Fratres)', '22R.1', '22R.1', 'Kýrie, eléison.'),
 ('k02', 'Kyrie (Chorus)', '22R.2', '22R.2', 'Kýrie, eléison.'),
 ('k03', 'Kyrie (Fratres)', '22R.3', '22R.3', 'Kýrie, eléison.'),
 ('k04', 'Dómine, miserére', '22R.4', '22R.4', 'Dómine, miserére.'),
 ('k05', 'Christus Dóminus', '22R.5', '22R.5', 'Christus Dóminus factus est obédiens usque ad mortem.'),
 ('k06', 'Qui passúrus', '22R.6', '22R.6', 'Qui passúrus advenísti propter nos.'),
 ('k07', 'Christe (Chorus)', '23L.0', '23L.0', 'Christe, eléison.'),
 ('k08', 'Qui expánsis', '23L.1', '23L.2', 'Qui expánsis in cruce mánibus, traxísti ómnia ad te sǽcula.'),
 ('k09', 'Christe (Chorus)', '23L.3', '23L.3', 'Christe, eléison.'),
 ('k10', 'Qui prophétice', '23L.4', '23L.4', 'Qui prophétice prompsísti: Ero mors tua, o mors.'),
 ('k11', 'Christe (Chorus)', '23L.5', '23L.5', 'Christe, eléison.'),
 ('k12', 'Dómine, miserére', '23L.6', '23L.6', 'Dómine, miserére.'),
 ('k13', 'Christus Dóminus', '23R.0', '23R.0', 'Christus Dóminus factus est obédiens usque ad mortem.'),
 ('k14', 'Kyrie (Fratres)', '23R.1', '23R.1', 'Kýrie, eléison.'),
 ('k15', 'Kyrie (Chorus)', '23R.2', '23R.2', 'Kýrie, eléison.'),
 ('k16', 'Kyrie (Fratres)', '23R.3', '23R.3', 'Kýrie, eléison.'),
 ('k17', 'Dómine, miserére', '23R.4', '23R.4', 'Dómine, miserére.'),
 ('k18', 'Christus Dóminus', '23R.5', '23R.5', 'Christus Dóminus factus est obédiens usque ad mortem.'),
 ('k19', 'Mortem autem crucis', '23R.6', '23R.6', 'Mortem autem crucis.')]
PM = []
MODES = {}
