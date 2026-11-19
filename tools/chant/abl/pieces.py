# the washing of the altars (Triduum O.P. 1927, pp. 83-111): chant pieces = runs of staves (pdf page, side, staff index)
def rng(a, b):
    """'43R.0'..'44R.3' -> list of (pg, side, i) using the staff counts below"""
    import pickle
    S = pickle.load(open('/home/claude/build/tri_staves.pkl', 'rb'))
    keys = []
    for k in sorted(S):
        for i in range(len(S[k])): keys.append((k[0], k[1], i))
    import re
    def p(s): m = re.match(r'(\d+)([LR])\.(\d+)', s); return (int(m.group(1)), m.group(2), int(m.group(3)))
    i0, i1 = keys.index(p(a)), keys.index(p(b))
    return keys[i0:i1 + 1]
P = [
 ('r01', 'In monte Olivéti', '43R.0', '43R.5', 'In monte Olivéti orávit ad Patrem: Pater, si fíeri potest, tránseat a me calix iste: Spíritus quidem promptus est, caro autem infírma: * Fiat volúntas tua. ℣. Verúmtamen non sicut ego volo, sed sicut tu vis. * Fiat.'),
 ('r02', 'Tristis est ánima mea', '44L.0', '44R.3', 'Tristis est ánima mea usque ad mortem: sustinéte hic, et vigiláte mecum: nunc vidébitis turbam, quæ circúmdabit me: * Vos fugam capiétis, et ego vadam immolári pro vobis. ℣. Ecce appropínquat hora, et Fílius hóminis tradétur in manus peccatórum. * Vos fugam.'),
 ('r03', 'Ecce vídimus eum', '44R.4', '45L.4', 'Ecce vídimus eum non habéntem spéciem, neque decórem: aspéctus ejus in eo non est. Hic peccáta nostra portávit, et pro nobis dolet: ipse autem vulnerátus est propter iniquitátes nostras: * Cujus livóre sanáti sumus. ℣. Vere languóres nostros ipse tulit, et dolóres nostros ipse portávit. * Cujus.'),
 ('r04', 'Amícus meus', '45L.5', '45R.5', 'Amícus meus ósculi me trádidit signo. Quem osculátus fúero, ipse est, tenéte eum. Hoc malum fecit signum, qui per ósculum adimplévit homicídium. * Infélix prætermísit prétium sánguinis, et in fine láqueo se suspéndit. ℣. Fílius quidem hóminis vadit, sicut scriptum est de illo: væ autem hómini illi, per quem tradétur. * Infélix.'),
 ('r05', 'Unus ex vobis', '45R.6', '46L.3', 'Unus ex vobis tradet me hódie: væ illi, per quem tradar ego: * Mélius illi erat, si natus non fuísset. ℣. Qui intíngit mecum manum in parópside, hic me traditúrus est in manus peccatórum. * Mélius.'),
 ('r06', 'Eram quasi agnus', '46L.4', '46R.4', 'Eram quasi agnus ínnocens: ductus sum ad immolándum, et nesciébam: consílium fecérunt inimíci mei advérsum me, dicéntes: * Veníte, mittámus lignum in panem ejus, et eradámus eum de terra vivéntium. ℣. Omnes inimíci mei advérsum me cogitábant mala mihi: verbum iníquum mandavérunt advérsum me, dicéntes. * Veníte.'),
 ('r07', 'Una hora', '46R.5', '47L.3', 'Una hora non potuístis vigiláre mecum, qui exhortabámini mori pro me? * Vel Judam non vidétis, quómodo non dormit, sed festínat trádere me Judǽis? ℣. Dormíte jam, et requiéscite: ecce appropínquat, qui me tradet. * Vel Judam.'),
 ('r08', 'Senióres pópuli', '47L.4', '47R.0', 'Senióres pópuli consílium fecérunt, * Ut Jesum dolo tenérent, et occíderent: cum gládiis, et fústibus exiérunt tamquam ad latrónem. ℣. Collegérunt ergo Pontífices et Pharisǽi concílium. * Ut Jesum.'),
 ('r09', 'Revelábunt cæli', '47R.1', '48L.0', 'Revelábunt cæli iniquitátem Judæ, et terra advérsus eum consúrget: et maniféstum erit peccátum illíus in die furóris Dómini: * Cum eis, qui dixérunt Dómino Deo: Recéde a nobis, sciéntiam viárum tuárum nólumus. ℣. In diem perditiónis servábitur, et ad diem ultiónis ducétur. * Cum eis.'),
 ('r10', 'Circumdedérunt me', '48L.1', '48R.0', 'Circumdedérunt me viri mendáces: sine causa flagéllis cecidérunt me: * Sed tu, Dómine, defénsor víndica me. ℣. Quóniam tribulátio próxima est, et non est qui ádjuvet. * Sed.'),
 ('a01', 'Tuam Crucem', '48R.1', '48R.3', 'Tuam Crucem adorámus, Dómine, tuam gloriósam recólimus Passiónem: miserére nostri, qui passus es pro nobis.'),
 ('a02', 'Sit nomen Dómini', '49L.0', '49L.0', 'Sit nomen Dómini benedíctum in sǽcula.'),
 ('a03', 'Suscépit nos Dóminus', '49L.1', '49L.2', 'Suscépit nos Dóminus in sinum et cor suum, recordátus misericórdiæ suæ.'),
 ('a04', 'Speciósa facta est', '49L.3', '49R.3', 'Speciósa facta est, et suávis in delíciis virginitátis sancta Dei Génitrix: quam vidéntes fíliæ Sion vernántem in flóribus rosárum, et líliis convállium, beatíssimam prædicavérunt, et Regínæ laudavérunt eam.'),
 ('a05', 'Tota pulchra es', '49R.4', '49R.5', 'Tota pulchra es, María, et mácula originális non est in te.'),
 ('a06', 'Sancta Dei Génitrix', '50L.0', '50L.1', 'Sancta Dei Génitrix, Virgo semper María, intercéde pro nobis ad Dóminum Deum nostrum.'),
 ('a07', 'Archángeli Michaélis', '50L.2', '50R.0', 'Archángeli Michaélis interventióne suffúlti, te, Dómine, deprecámur, ut quos honóre proséquimur, contingámus et mente.'),
 ('a08', 'Inter natos mulíerum', '50R.1', '50R.2', 'Inter natos mulíerum non surréxit major Joánne Baptísta.'),
 ('a09', 'Ecce fidélis servus', '50R.3', '51L.0', 'Ecce fidélis servus et prudens, quem constítuit Dóminus super famíliam suam.'),
 ('a10', 'Petre, amas me', '51L.1', '51L.2', 'Petre, amas me? pasce oves meas. Tu scis, Dómine, quia amo te.'),
 ('a11', 'Sancte Paule Apóstole', '51L.3', '51R.1', 'Sancte Paule Apóstole, prædicátor veritátis et Doctor Géntium, intercéde pro nobis ad Deum, qui te elégit.'),
 ('a12', 'Pie Pater Domínice', '51R.2', '51R.4', 'Pie Pater Domínice, tuórum memor óperum, sta coram summo Júdice pro tuo cœtu páuperum.'),
 ('a13', 'Petrus novus íncola', '52L.0', '52L.1', 'Petrus novus íncola cælos laureátus ascéndit, auréola tríplici dotátus.'),
 ('a14', 'Exaltávit Dóminus', '52L.2', '52L.4', 'Exaltávit Dóminus húmiles servos suos, et suscépit eos in tabernácula sancta, recordátus misericórdiæ suæ.'),
 ('a15', 'Pius instar facis', '52R.0', '52R.1', 'Pius instar facis sǽculum illúminat, ut in viam pacis pedes nostros dírigat.'),
 ('a16', 'Beátus Antonínus', '52R.2', '52R.3', 'Beátus Antonínus, ad præsulátum quasi ad cruciátum raptus, doctrína et móribus gregem suum pavit.'),
 ('a17', 'O Thoma, laus et glória', '53L.0', '53L.2', 'O Thoma, laus et glória Prædicatórum Ordinis, nos transfer ad cæléstia, proféssor sacri Nóminis.'),
 ('a18', 'Adsit nobis propítius', '53L.3', '53R.1', 'Adsit nobis propítius in hujus vitæ véspere ad Christum nos Vincéntius tuto ferens itínere.'),
 ('a19', 'Tuum, Dómine', '53R.2', '53R.3', 'Tuum, Dómine, fac sentiámus auxílium, qui beáti Hyacínthi depóscimus patrocínium.'),
 ('a20', 'Piis Raymúndi précibus', '54L.0', '54L.2', 'Piis Raymúndi précibus educ nos, Dómine, de domo servitútis peccáti in libertátem glóriæ filiórum tuórum.'),
 ('a21', 'Quasi meridiánus fulgor', '54L.3', '54R.0', 'Quasi meridiánus fulgor consúrget tibi ad vésperam: et cum te consúmptum putáveris, oriéris ut Lúcifer.'),
 ('a22', 'Ad sedes regni', '54R.1', '54R.2', 'Ad sedes regni fáciat transíre supérni Virgo fovens méritis nos Catharína suis.'),
 ('a23', 'Rosa soror nostra', '54R.3', '55L.0', 'Rosa soror nostra bene sit nobis propter te, et vivat ánima nostra ob grátiam tui.'),
 ('a24', 'Tuam laudántes glóriam', '55L.1', '55L.3', 'Tuam laudántes glóriam Agnes beáta réspice: cæléstis Agni grátiam benígna nobis óbtine.'),
 ('a25', 'Exsultávit ánima mea', '55R.0', '55R.3', 'Exsultávit ánima mea in Deo meo: quia índuit me vestiménto salútis, et induménto justítiæ, quasi sponsam ornátam monílibus suis.'),
 ('a26', 'Sanctos suos', '55R.4', '56L.0', 'Sanctos suos magnificávit Dóminus in salutári suo: ecce enim ex hoc beátos illos dicent omnes generatiónes.'),
 ('a27', 'Intercéde súpplicans', '56L.1', '56L.2', 'Intercéde súpplicans assídue pro nobis Jesu Dómino María Magdaléna.'),
 ('a28', 'Estóte fortes in bello', '56L.3', '56R.1', 'Estóte fortes in bello, et pugnáte cum antíquo serpénte, et accipiétis regnum ætérnum, dicit Dóminus.'),
 ('a29', 'Qui me conféssus fúerit', '56R.2', '56R.3', 'Qui me conféssus fúerit coram homínibus, confitébor et ego eum coram Patre meo.'),
 ('a30', 'Justórum ánimæ', '57L.0', '57L.1', 'Justórum autem ánimæ in manu Dei sunt, et non tanget illos torméntum malítiæ.'),
 ('a31', 'Similábo eum', '57L.2', '57L.3', 'Similábo eum viro sapiénti, qui ædificávit domum suam supra petram.'),
 ('a32', 'Veni, elécta mea', '57R.0', '57R.1', 'Veni, elécta mea, et ponam in te thronum meum: quia concupívit Rex spéciem tuam.'),
]

PM = [
 ('m01', 'r01', '6L.4', '6R.2', 'In monte Olivéti orávit ad Patrem: Pater, si fíeri potest, tránseat a me calix iste: Spíritus quidem promptus est, caro autem infírma: * Fiat volúntas tua. ℣. Verúmtamen non sicut ego volo, sed sicut tu vis. * Fiat.'),
 ('m02', 'r02', '7L.7', '7R.6', 'Tristis est ánima mea usque ad mortem: sustinéte hic, et vigiláte mecum: nunc vidébitis turbam, quæ circúmdabit me: * Vos fugam capiétis, et ego vadam immolári pro vobis. ℣. Ecce appropínquat hora, et Fílius hóminis tradétur in manus peccatórum. * Vos fugam.'),
 ('m03', 'r03', '8R.4', '9L.4', 'Ecce vídimus eum non habéntem spéciem, neque decórem: aspéctus ejus in eo non est. Hic peccáta nostra portávit, et pro nobis dolet: ipse autem vulnerátus est propter iniquitátes nostras: * Cujus livóre sanáti sumus. ℣. Vere languóres nostros ipse tulit, et dolóres nostros ipse portávit. * Cujus. ℟. Ecce.'),
 ('m04', 'r04', '12L.0', '12R.2', 'Amícus meus ósculi me trádidit signo. Quem osculátus fúero, ipse est, tenéte eum. Hoc malum fecit signum, qui per ósculum adimplévit homicídium. * Infélix prætermísit prétium sánguinis, et in fine láqueo se suspéndit. ℣. Fílius quidem hóminis vadit, sicut scriptum est de illo: væ autem hómini illi, per quem tradétur. * Infélix.'),
 ('m05', 'r05', '12R.3', '13L.3', 'Unus ex vobis tradet me hódie: væ illi, per quem tradar ego: * Mélius illi erat, si natus non fuísset. ℣. Qui intíngit mecum manum in parópside, hic me traditúrus est in manus peccatórum. * Mélius.'),
 ('m06', 'r06', '13L.4', '13R.7', 'Eram quasi agnus ínnocens: ductus sum ad immolándum, et nesciébam: consílium fecérunt inimíci mei advérsum me, dicéntes: * Veníte, mittámus lignum in panem ejus, et eradámus eum de terra vivéntium. ℣. Omnes inimíci mei advérsum me cogitábant mala mihi: verbum iníquum mandavérunt advérsum me, dicéntes. * Veníte. ℟. Eram.'),
 ('m07', 'r07', '16L.0', '16L.6', 'Una hora non potuístis vigiláre mecum, qui exhortabámini mori pro me? * Vel Judam non vidétis, quómodo non dormit, sed festínat trádere me Judǽis? ℣. Dormíte jam, et requiéscite: ecce appropínquat, qui me tradet. * Vel Judam.'),
 ('m08', 'r08', '16R.0', '16R.4', 'Senióres pópuli consílium fecérunt, * Ut Jesum dolo tenérent, et occíderent: cum gládiis, et fústibus exiérunt tamquam ad latrónem. ℣. Collegérunt ergo Pontífices et Pharisǽi concílium. * Ut Jesum.'),
 ('m09', 'r09', '17L.0', '17R.3', 'Revelábunt cæli iniquitátem Judæ, et terra advérsus eum consúrget: et maniféstum erit peccátum illíus in die furóris Dómini: * Cum eis, qui dixérunt Dómino Deo: Recéde a nobis, sciéntiam viárum tuárum nólumus. ℣. In diem perditiónis servábitur, et ad diem ultiónis ducétur. * Cum eis. ℟. Revelábunt.'),
]
