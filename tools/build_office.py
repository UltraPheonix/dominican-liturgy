"""Build site/data/office.js: the spoken Divine Office according to the Breviarium O.P. (Cormier, 1909).
Latin from the Breviary (OCR, corrected by hand); English our own (psalms and canticles are drawn by the page from
the Vulgate and the Douay-Rheims, verse by verse).  First stage: the Ordinary, Compline, Prime, Terce, Sext, None."""
import json

def T(la, en, **kw):
    d = {'la': la, 'en': en}; d.update(kw); return d
def V(la, en):  # versicle and response
    return T(la, en, t='v')
def A(la, en): return T(la, en, t='ant')
def CH(ref, la, en): return T(la, en, t='chap', ref=ref)
def R(la, en): return T(la, en, t='resp')
def OR(la, en, h='Oratio'): return T(la, en, t='or', h=h)
def RUB(en): return {'t': 'rub', 'la': en, 'en': en}
def H(la): return {'t': 'h', 'la': la}
def PS(ref, title=None, gloria=True):
    d = {'t': 'ps', 'ref': ref}
    if title: d['title'] = title
    if not gloria: d['gloria'] = False
    return d
def HY(name, la, en): return {'t': 'hymn', 'name': name, 'la': la, 'en': en}

ORD = {
 'Pater': T('Pater noster, qui es in cælis, sanctificétur nomen tuum. Advéniat regnum tuum. Fiat volúntas tua, sicut in cælo et in terra. Panem nostrum quotidiánum da nobis hódie. Et dimítte nobis débita nostra, sicut et nos dimíttimus debitóribus nostris. Et ne nos indúcas in tentatiónem. Sed líbera nos a malo. Amen.',
            'Our Father, who art in heaven, hallowed be thy name. Thy kingdom come. Thy will be done on earth as it is in heaven. Give us this day our daily bread. And forgive us our trespasses, as we forgive them that trespass against us. And lead us not into temptation. But deliver us from evil. Amen.'),
 'Ave': T('Ave María, grátia plena: Dóminus tecum: benedícta tu in muliéribus, et benedíctus fructus ventris tui, Jesus. Sancta María, Mater Dei, ora pro nobis peccatóribus, nunc et in hora mortis nostræ. Amen.',
          'Hail Mary, full of grace, the Lord is with thee: blessed art thou among women, and blessed is the fruit of thy womb, Jesus. Holy Mary, Mother of God, pray for us sinners, now and at the hour of our death. Amen.'),
 'Credo': T('Credo in Deum Patrem omnipoténtem, Creatórem cæli et terræ. Et in Jesum Christum, Fílium ejus únicum, Dóminum nostrum: qui concéptus est de Spíritu Sancto, natus ex María Vírgine, passus sub Póntio Piláto, crucifíxus, mórtuus, et sepúltus: descéndit ad ínferos; tértia die resurréxit a mórtuis; ascéndit ad cælos; sedet ad déxteram Dei Patris omnipoténtis: inde ventúrus est judicáre vivos et mórtuos. Credo in Spíritum Sanctum, sanctam Ecclésiam cathólicam, Sanctórum communiónem, remissiónem peccatórum, carnis resurrectiónem, vitam ætérnam. Amen.',
            'I believe in God the Father almighty, Creator of heaven and earth. And in Jesus Christ his only Son, our Lord: who was conceived by the Holy Ghost, born of the Virgin Mary, suffered under Pontius Pilate, was crucified, died, and was buried: he descended into hell; the third day he rose again from the dead; he ascended into heaven, and sitteth at the right hand of God the Father almighty: from thence he shall come to judge the living and the dead. I believe in the Holy Ghost, the holy catholic Church, the communion of Saints, the forgiveness of sins, the resurrection of the body, and life everlasting. Amen.'),
 'secreto': RUB('Pater noster and Ave María are said silently.'),
 'secretoCredo': RUB('Pater noster and Credo are said silently.'),
 'Domine labia': V('℣. Dómine, lábia mea apéries. ℟. Et os meum annuntiábit laudem tuam.', '℣. O Lord, thou wilt open my lips. ℟. And my mouth shall declare thy praise.'),
 'Deus in adjutorium': T('℣. Deus in adjutórium meum inténde. ℟. Dómine ad adjuvándum me festína. Glória Patri, et Fílio, et Spirítui Sancto. Sicut erat in princípio, et nunc, et semper, et in sǽcula sæculórum. Amen. Allelúia.',
                         '℣. O God, come to my assistance. ℟. O Lord, make haste to help me. Glory be to the Father, and to the Son, and to the Holy Ghost. As it was in the beginning, is now, and ever shall be, world without end. Amen. Alleluia.', t='v', alleluia=True),
 'Gloria Patri': T('Glória Patri, et Fílio, et Spirítui Sancto. Sicut erat in princípio, et nunc, et semper, et in sǽcula sæculórum. Amen.',
                   'Glory be to the Father, and to the Son, and to the Holy Ghost. As it was in the beginning, is now, and ever shall be, world without end. Amen.'),
 'Dominus vobiscum': V('℣. Dóminus vobíscum. ℟. Et cum spíritu tuo.', '℣. The Lord be with you. ℟. And with thy spirit.'),
 'Benedicamus': V('℣. Benedicámus Dómino. ℟. Deo grátias.', '℣. Let us bless the Lord. ℟. Thanks be to God.'),
 'Fidelium': V('℣. Fidélium ánimæ per misericórdiam Dei requiéscant in pace. ℟. Amen.', '℣. May the souls of the faithful departed, through the mercy of God, rest in peace. ℟. Amen.'),
 'Kyrie preces': V('Kýrie eléison. Christe eléison. Kýrie eléison. Pater noster [silently]… ℣. Et ne nos indúcas in tentatiónem. ℟. Sed líbera nos a malo.',
                   'Lord, have mercy. Christ, have mercy. Lord, have mercy. Our Father [silently]… ℣. And lead us not into temptation. ℟. But deliver us from evil.'),
 'Oremus': T('Orémus.', 'Let us pray.', t='v'),
}

# ---------------- Compline ----------------
TE_LUCIS = HY('Te lucis ante terminum',
 ['Te lucis ante términum,\nRerum Creátor, póscimus,\nUt sólita cleméntia\nSis præsul ad custódiam.',
  'Procul recédant sómnia,\nEt nóctium phantásmata:\nHostémque nostrum cómprime,\nNe polluántur córpora.',
  'Præsta, Pater omnípotens,\nPer Jesum Christum Dóminum,\nQui tecum in perpétuum\nRegnat cum Sancto Spíritu. Amen.'],
 ['Before the ending of the light,\nCreator of all things, we pray\nthat with thy wonted clemency\nthou be our guardian and our guide.',
  'Far off let dreams and fancies flee,\nand all the phantoms of the night;\nhold fast our enemy in check,\nlest any stain defile our flesh.',
  'Grant this, O Father almighty,\nthrough Jesus Christ our Lord,\nwho with thee and the Holy Ghost\nreigneth for evermore. Amen.'])
CHRISTE_QUI_LUX = HY('Christe qui lux es et dies',
 ['Christe, qui lux es et dies,\nNoctis tenébras détegis,\nLucísque lumen créderis,\nLumen beátum prǽdicans.',
  'Precámur, sancte Dómine,\nDefénde nos in hac nocte:\nSit nobis in te réquies,\nQuiétam noctem tríbue.',
  'Ne gravis somnus írruat,\nNec hostis nos subrípiat,\nNec caro illi conséntiens\nNos tibi reos státuat.',
  'Oculi somnum cápiant,\nCor ad te semper vígilet:\nDéxtera tua prótegat\nFámulos, qui te díligunt.',
  'Defénsor noster, áspice,\nInsidiántes réprime,\nGubérna tuos fámulos,\nQuos sánguine mercátus es.',
  'Meménto nostri, Dómine,\nIn gravi isto córpore:\nQui es defénsor ánimæ,\nAdésto nobis, Dómine.',
  'Præsta, Pater omnípotens,\nPer Jesum Christum Dóminum,\nQui tecum in perpétuum\nRegnat cum Sancto Spíritu. Amen.'],
 ['O Christ, who art the light and day,\nthou dost lay bare the shades of night;\nthou art believed the light of light,\nand dost proclaim the blessed light.',
  'We pray thee, holy Lord,\ndefend us in this night:\nlet our rest be in thee;\ngrant us a quiet night.',
  'Let no heavy sleep fall on us,\nnor the enemy steal upon us,\nnor the flesh, consenting to him,\nmake us guilty in thy sight.',
  'Let our eyes take their sleep,\nbut our heart ever watch for thee;\nlet thy right hand protect\nthy servants who love thee.',
  'Look down, O our defender,\ndrive back those who lie in wait;\ngovern thy servants,\nwhom thou hast bought with thy blood.',
  'Remember us, O Lord,\nin this heavy body:\nthou who art the defender of the soul,\nbe with us, O Lord.',
  'Grant this, O Father almighty,\nthrough Jesus Christ our Lord,\nwho with thee and the Holy Ghost\nreigneth for evermore. Amen.'])
JESU_NOSTRA = ['Jesu, nostra redémptio,\nAmor et desidérium,\nDeus Creátor ómnium,\nHomo in fine témporum.',
  'Quæ te vicit cleméntia,\nUt ferres nostra crímina,\nCrudélem mortem pátiens,\nUt nos a morte tólleres?',
  'Inférni claustra pénetrans,\nTuos captívos rédimens,\nVictor triúmpho nóbili\nAd dextram Patris résidens:',
  'Ipsa te cogat píetas,\nUt mala nostra súperes\nParcéndo, et voti cómpotes\nNos tuo vultu sáties.']
JESU_NOSTRA_EN = ['O Jesus, our redemption,\nour love and our desire,\nGod, Creator of all things,\nman at the end of time:',
  'what mercy overcame thee,\nthat thou shouldst bear our crimes,\nsuffering a cruel death\nto take us out of death?',
  'Piercing the bars of hell,\nredeeming thine own captives,\nvictor in noble triumph,\nthou sittest at the Father’s right hand.',
  'Let thy own goodness move thee\nto overcome our evils by sparing us,\nand, granting what we ask,\nto fill us with the sight of thy face.']
JESU_END = {
 'pascha': (['Quǽsumus, Auctor ómnium,\nIn hoc Pascháli gáudio,\nAb omni mortis ímpetu\nTuum defénde pópulum.',
             'Glória tibi, Dómine,\nQui surrexísti a mórtuis,\nCum Patre et Sancto Spíritu,\nIn sempitérna sǽcula. Amen.'],
            ['We pray thee, Author of all things,\nin this Paschal joy,\nfrom every assault of death\ndefend thy people.',
             'Glory be to thee, O Lord,\nwho didst rise from the dead,\nwith the Father and the Holy Ghost,\nfor ever and ever. Amen.']),
 'ascensio': (['Tu esto nostrum gáudium,\nQui es futúrus prǽmium:\nSit nostra in te glória,\nPer cuncta semper sǽcula.',
               'Glória tibi, Dómine,\nQui scandis supra sídera,\nCum Patre et Sancto Spíritu,\nIn sempitérna sǽcula. Amen.'],
              ['Be thou our joy,\nwho art to be our reward:\nlet our glory be in thee\nthrough all the ages for ever.',
               'Glory be to thee, O Lord,\nwho dost ascend above the stars,\nwith the Father and the Holy Ghost,\nfor ever and ever. Amen.']),
 'pentecostes': (['Dudum sacráta péctora\nTua replésti grátia:\nDimítte nunc peccámina,\nEt da quiéta témpora.',
                  'Sit laus Patri cum Fílio,\nSancto simul Paráclito:\nNobísque mittat Fílius\nCharísma Sancti Spíritus. Amen.'],
                 ['Long since thou didst fill\nhallowed hearts with thy grace:\nnow forgive our sins,\nand grant us peaceful times.',
                  'Praise be to the Father with the Son\nand with the Holy Paraclete:\nand may the Son send us\nthe gift of the Holy Ghost. Amen.']),
}
def jesu_nostra(season):
    la, en = JESU_END.get(season, JESU_END['pascha'])
    return HY('Jesu nostra redemptio', JESU_NOSTRA + la, JESU_NOSTRA_EN + en)

def compline(season):
    """season: annum (also Advent, Christmastide, Septuagesima, Ash Wednesday week), lent1 (to Lent III), lent3, passio, pascha, ascensio, pentecostes"""
    pas = season in ('pascha', 'ascensio', 'pentecostes')
    al = ', allelúia' if pas else ''; al_en = ', alleluia' if pas else ''
    out = [H('Ad Completorium'),
      V('℣. Jube, domne, benedícere. Benedíctio. Noctem quiétam et finem perféctum tríbuat nobis omnípotens et miséricors Dóminus. ℟. Amen.',
        '℣. Pray, sir, a blessing. The blessing. May the almighty and merciful Lord grant us a quiet night and a perfect end. ℟. Amen.'),
      T('Fratres: Sóbrii estóte, et vigiláte: quia adversárius vester diábolus tamquam leo rúgiens círcuit, quærens quem dévoret: cui resístite fortes in fide. Tu autem, Dómine, miserére nostri. ℟. Deo grátias.',
        'Brethren: Be sober and watch: because your adversary the devil, as a roaring lion, goeth about seeking whom he may devour: whom resist ye, strong in faith. But thou, O Lord, have mercy on us. ℟. Thanks be to God.', t='lect', ref='1 Petr. 5: 8-9'),
      V('℣. Adjutórium nostrum in nómine Dómini. ℟. Qui fecit cælum et terram.', '℣. Our help is in the name of the Lord. ℟. Who made heaven and earth.'),
      RUB('Pater noster is said silently. Then the Confiteor:'),
      T('Confíteor Deo omnipoténti, et beátæ Maríæ semper Vírgini, et beáto Domínico Patri nostro, et ómnibus Sanctis: quia peccávi nimis cogitatióne, locutióne, ópere et omissióne, mea culpa: precor beátam Maríam semper Vírginem, et beátum Domínicum Patrem nostrum, et omnes Sanctos oráre pro me.',
        'I confess to almighty God, and to blessed Mary ever Virgin, and to blessed Dominic our Father, and to all the Saints: that I have sinned exceedingly in thought, word, deed and omission, through my fault: I pray blessed Mary ever Virgin, and blessed Dominic our Father, and all the Saints to pray for me.', t='txt'),
      T('Misereátur mei omnípotens Deus, et dimíttat mihi ómnia peccáta mea: líberet me ab omni malo, salvet, et confírmet in omni ópere bono, et perdúcat me ad vitam ætérnam. Amen.',
        'May almighty God have mercy on me, and forgive me all my sins: deliver me from all evil, save and confirm me in every good work, and bring me to life everlasting. Amen.', t='txt'),
      RUB('In choir: the Prior says the Confiteor (“…et vobis, Fratres… precor vos oráre pro me”), the choir answers Misereátur tui… and says the Confiteor (“…et tibi, Pater…”), and the Prior gives the absolution Misereátur vestri….'),
      V('℣. Convérte nos, Deus, salutáris noster. ℟. Et avérte iram tuam a nobis.', '℣. Convert us, O God our Saviour. ℟. And turn away thy anger from us.'),
      {'ref': 'Deus in adjutorium'},
      PS('Psalmi 4'), PS('Psalmi 30: 2-6', 'Psalmus 30, 1-6'), PS('Psalmi 90'), PS('Psalmi 133'),
    ]
    out.append(A('Allelúia, allelúia, allelúia, allelúia.', 'Alleluia, alleluia, alleluia, alleluia.') if pas else
               A('Miserére mihi, Dómine, et exáudi oratiónem meam.', 'Have mercy on me, O Lord, and hear my prayer.'))
    out.append(CH('Jer. 14: 9', 'Tu in nobis es, Dómine, et nomen sanctum tuum invocátum est super nos: ne derelínquas nos, Dómine Deus noster. ℟. Deo grátias.',
                  'Thou, O Lord, art among us, and thy holy name is called upon us: forsake us not, O Lord our God. ℟. Thanks be to God.'))
    if season == 'lent1' or season == 'lent3':
        out.append(R('℟. In pace in idípsum * Dórmiam et requiéscam. ℣. Si dédero somnum óculis meis, et pálpebris meis dormitatiónem. * Dórmiam. Glória Patri. ℟. In pace.',
                     '℟. In peace in the selfsame * I will sleep and I will rest. ℣. If I shall give sleep to my eyes, or slumber to my eyelids. * I will sleep. Glory be to the Father. ℟. In peace.'))
        out.append(RUB('This responsory is said on Saturdays and Sundays, on doubles and in solemn octaves; on other days the responsory In manus tuas, as at other seasons.'))
    elif season == 'passio':
        out.append(R('℟. In manus tuas, Dómine, * Comméndo spíritum meum. ℣. Redemísti nos, Dómine, Deus veritátis. * Comméndo. ℟. In manus.',
                     '℟. Into thy hands, O Lord, * I commend my spirit. ℣. Thou hast redeemed us, O Lord, the God of truth. * I commend. ℟. Into thy hands.'))
        out.append(RUB('Glória Patri is omitted (but it is said on feasts of Saints).'))
    elif pas:
        out.append(R('℟. In manus tuas, Dómine, comméndo spíritum meum. * Allelúia, allelúia. ℣. Redemísti nos, Dómine, Deus veritátis. * Allelúia, allelúia. Glória Patri. ℟. In manus.',
                     '℟. Into thy hands, O Lord, I commend my spirit. * Alleluia, alleluia. ℣. Thou hast redeemed us, O Lord, the God of truth. * Alleluia, alleluia. Glory be to the Father. ℟. Into thy hands.'))
    else:
        out.append(R('℟. In manus tuas, Dómine, * Comméndo spíritum meum. ℣. Redemísti nos, Dómine, Deus veritátis. * Comméndo. Glória Patri. ℟. In manus.',
                     '℟. Into thy hands, O Lord, * I commend my spirit. ℣. Thou hast redeemed us, O Lord, the God of truth. * I commend. Glory be to the Father. ℟. Into thy hands.'))
    out.append(CHRISTE_QUI_LUX if season in ('lent1', 'lent3', 'passio') else jesu_nostra(season) if pas else TE_LUCIS)
    out.append(V('℣. Custódi nos, Dómine, ut pupíllam óculi%s. ℟. Sub umbra alárum tuárum prótege nos%s.' % (al, al),
                 '℣. Keep us, O Lord, as the apple of thy eye%s. ℟. Protect us under the shadow of thy wings%s.' % (al_en, al_en)))
    out.append(PS('Lucas 2: 29-32', 'Canticum Simeonis · Nunc dimittis'))
    NUNC = {
      'lent1': A('Evígila super nos, ætérne Salvátor, ne nos apprehéndat cállidus tentátor: quia tu factus es nobis sempitérnus adjútor.',
                 'Watch over us, eternal Saviour, lest the cunning tempter seize us: for thou art become our everlasting helper.'),
      'lent3': A('Média vita in morte sumus: quem quǽrimus adjutórem, nisi te, Dómine, qui pro peccátis nostris juste irásceris? * Sancte Deus, sancte fortis, sancte et miséricors Salvátor, amáræ morti ne tradas nos. ℣. Ne projícias nos in témpore senectútis: cum defécerit virtus nostra, ne derelínquas nos, Dómine. * Sancte Deus…',
                 'In the midst of life we are in death: whom shall we seek for a helper, but thee, O Lord, who for our sins art justly angered? * Holy God, holy and mighty, holy and merciful Saviour, deliver us not to bitter death. ℣. Cast us not off in the time of old age: when our strength shall fail, forsake us not, O Lord. * Holy God…'),
      'passio': A('O Rex glorióse inter Sanctos tuos, qui semper es laudábilis, et tamen ineffábilis: tu in nobis es, Dómine, et nomen sanctum tuum invocátum est super nos: ne derelínquas nos, Deus noster: ut in die judícii nos collocáre dignéris inter Sanctos et eléctos tuos, Rex benedícte.',
                  'O glorious King among thy Saints, who art ever to be praised and yet art beyond all speech: thou, O Lord, art among us, and thy holy name is called upon us: forsake us not, O our God: that on the day of judgement thou mayest vouchsafe to place us among thy Saints and thine elect, O blessed King.'),
      'pas': A('Allelúia, resurréxit Dóminus, allelúia: sicut dixit vobis, allelúia, allelúia.', 'Alleluia, the Lord is risen, alleluia: as he said unto you, alleluia, alleluia.'),
      'annum': A('Salva nos, Dómine, vigilántes, custódi nos dormiéntes: ut vigilémus cum Christo, et requiescámus in pace.',
                 'Save us, O Lord, while we wake, and guard us while we sleep: that we may watch with Christ, and rest in peace.'),
    }
    out.append(NUNC['pas'] if pas else NUNC.get(season, NUNC['annum']))
    out += [{'ref': 'Dominus vobiscum'}, {'ref': 'Oremus'},
      OR('Vísita, quǽsumus, Dómine, habitatiónem istam, et omnes insídias inimíci ab ea longe repélle: et Angeli tui sancti hábitent in ea, qui nos in pace custódiant, et benedíctio tua sit super nos semper. Per Dóminum nostrum Jesum Christum Fílium tuum, qui tecum vivit et regnat in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum. ℟. Amen.',
         'Visit, we beseech thee, O Lord, this dwelling, and drive far from it all the snares of the enemy: let thy holy Angels dwell herein to keep us in peace, and let thy blessing be always upon us. Through our Lord Jesus Christ thy Son, who liveth and reigneth with thee in the unity of the Holy Ghost, God, world without end. ℟. Amen.'),
      {'ref': 'Dominus vobiscum'}, {'ref': 'Benedicamus'},
      V('Benedíctio Dei omnipoténtis, Patris, et Fílii, ✠ et Spíritus Sancti descéndat super nos, et máneat semper. ℟. Amen.',
        'May the blessing of almighty God, the Father, the Son, ✠ and the Holy Ghost, come down upon us and remain for ever. ℟. Amen.')]
    if season != 'holyweds':
        out += [H('Salve Regina'),
          A('Salve, Regína, mater misericórdiæ: vita, dulcédo et spes nostra, salve. Ad te clamámus éxsules fílii Hevæ. Ad te suspirámus geméntes et flentes in hac lacrimárum valle. Eja ergo, advocáta nostra, illos tuos misericórdes óculos ad nos convérte; et Jesum, benedíctum fructum ventris tui, nobis post hoc exsílium osténde. O clemens, o pia, o dulcis Virgo María.%s' % (' Allelúia.' if pas else ''),
            'Hail, holy Queen, mother of mercy: our life, our sweetness and our hope, hail. To thee do we cry, poor banished children of Eve. To thee do we send up our sighs, mourning and weeping in this vale of tears. Turn then, most gracious advocate, thine eyes of mercy towards us; and after this our exile show unto us the blessed fruit of thy womb, Jesus. O clement, O loving, O sweet Virgin Mary.%s' % (' Alleluia.' if pas else '')),
          V('℣. Dignáre me laudáre te, Virgo sacráta%s. ℟. Da mihi virtútem contra hostes tuos%s.' % (al, al),
            '℣. Make me worthy to praise thee, holy Virgin%s. ℟. Give me strength against thine enemies%s.' % (al_en, al_en)),
          {'ref': 'Oremus'},
          OR('Concéde nos fámulos tuos, quǽsumus, Dómine Deus, perpétua mentis et córporis salúte gaudére: et gloriósa beátæ Maríæ semper Vírginis intercessióne, a præsénti liberári tristítia, et ætérna pérfrui lætítia. Per Christum Dóminum nostrum. ℟. Amen.',
             'Grant, we beseech thee, O Lord God, that we thy servants may rejoice in continual health of mind and body: and by the glorious intercession of blessed Mary ever Virgin, be delivered from present sorrow and enjoy everlasting gladness. Through Christ our Lord. ℟. Amen.'),
          H('O lumen Ecclesiae'),
          A('O lumen Ecclésiæ, doctor veritátis, rosa patiéntiæ, ebur castitátis, aquam sapiéntiæ propinásti grátis: prædicátor grátiæ, nos junge beátis.%s' % (' Allelúia.' if pas else ''),
            'O light of the Church, teacher of truth, rose of patience, ivory of chastity, freely thou didst pour forth the waters of wisdom: preacher of grace, unite us with the blessed.%s' % (' Alleluia.' if pas else '')),
          V('℣. Ora pro nobis, beáte Pater Domínice%s. ℟. Ut digni efficiámur promissiónibus Christi%s.' % (al, al),
            '℣. Pray for us, O blessed Father Dominic%s. ℟. That we may be made worthy of the promises of Christ%s.' % (al_en, al_en)),
          {'ref': 'Oremus'},
          OR('Concéde, quǽsumus, omnípotens Deus: ut qui peccatórum nostrórum póndere prémimur, beáti Domínici Confessóris tui, Patris nostri, patrocínio sublevémur. Per Christum Dóminum nostrum. ℟. Amen.',
             'Grant, we beseech thee, almighty God: that we who are weighed down by the burden of our sins may be raised up by the patronage of blessed Dominic thy Confessor, our Father. Through Christ our Lord. ℟. Amen.')]
    else:
        out.append(RUB('On Wednesday of Holy Week the Salve Regina and the antiphon of our holy Father Dominic are omitted.'))
    out += [{'ref': 'Fidelium'}, RUB('Pater noster and Credo are said silently.')]
    return out

# ---------------- Prime ----------------
JAM_LUCIS = HY('Jam lucis orto sidere',
 ['Jam lucis orto sídere,\nDeum precémur súpplices,\nUt in diúrnis áctibus\nNos servet a nocéntibus.',
  'Linguam refrénans témperet,\nNe litis horror ínsonet:\nVisum fovéndo cóntegat,\nNe vanitátes háuriat.',
  'Sint pura cordis íntima,\nAbsístat et vecórdia:\nCarnis terat supérbiam\nPotus cibíque párcitas.',
  'Ut cum dies abscésserit,\nNoctémque sors redúxerit,\nMundi per abstinéntiam\nIpsi canámus glóriam.',
  'Deo Patri sit glória,\nEjúsque soli Fílio,\nCum Spíritu Paráclito,\nEt nunc, et in perpétuum. Amen.'],
 ['Now that the star of light is risen,\nlet us humbly pray to God\nthat in the deeds of the day\nhe keep us from all harm.',
  'May he bridle and restrain the tongue,\nlest the noise of strife resound;\nmay he guard and veil our sight,\nlest it drink in vanities.',
  'May the heart within be pure,\nand folly depart from it;\nmay sparing food and drink\nwear down the pride of the flesh;',
  'that when the day has gone\nand its course brings back the night,\nkept clean by abstinence from the world,\nwe may sing his glory.',
  'To God the Father be glory,\nand to his only Son,\nwith the Spirit, the Paraclete,\nnow and for evermore. Amen.'])
QUICUMQUE = {'t': 'ps', 'ref': 'QUICUMQUE', 'title': 'Symbolum S. Athanasii'}
PRIME_ANT = {
 'adventus': {'sun': None, 'fer': A('Veni, et líbera nos, Deus noster.', 'Come and deliver us, O our God.')},
 'annum': {'sun': A('Glória tibi, Trínitas, æquális una Déitas, et ante ómnia sǽcula, et nunc, et in perpétuum.', 'Glory be to thee, O Trinity, one equal Godhead, before all ages, and now, and for evermore.'),
           'fer': A('Deus, exáudi oratiónem meam: áuribus pércipe verba oris mei.', 'O God, hear my prayer: give ear to the words of my mouth.')},
 'quadragesima': {'sun': None, 'fer': A('Vivo ego, dicit Dóminus: nolo mortem peccatóris, sed ut magis convertátur, et vivat.', 'As I live, saith the Lord: I desire not the death of the sinner, but rather that he be converted and live.')},
 'passio': {'sun': None, 'fer': A('Animæ impiórum fremébant advérsum me: et gravátum est cor meum super eos.', 'The souls of the wicked raged against me: and my heart was heavy because of them.')},
 'pascha': {'sun': A('Cognovérunt Dóminum, allelúia, in fractióne panis, allelúia.', 'They knew the Lord, alleluia, in the breaking of bread, alleluia.'),
            'fer': A('Cognovérunt Dóminum, allelúia, in fractióne panis, allelúia.', 'They knew the Lord, alleluia, in the breaking of bread, alleluia.')},
}
REGI = CH('1 Tim. 1: 17', 'Regi sæculórum immortáli et invisíbili, soli Deo honor et glória in sǽcula sæculórum. Amen. ℟. Deo grátias.',
          'To the King of ages, immortal and invisible, the only God, be honour and glory for ever and ever. Amen. ℟. Thanks be to God.')
PACEM = CH('Zach. 8: 19', 'Pacem et veritátem dilígite, ait Dóminus omnípotens. ℟. Deo grátias.', 'Love ye peace and truth, saith the Lord almighty. ℟. Thanks be to God.')
JESU_CHRISTE = R('℟. Jesu Christe, Fili Dei vivi, * Miserére nobis. Jesu Christe. ℣. Qui sedes ad déxteram Patris. * Miserére nobis. Glória Patri. ℟. Jesu Christe.',
                 '℟. Jesus Christ, Son of the living God, * have mercy on us. Jesus Christ. ℣. Who sittest at the right hand of the Father. * Have mercy on us. Glory be to the Father. ℟. Jesus Christ.')
EXSURGE = V('℣. Exsúrge, Dómine, ádjuva nos. ℟. Et líbera nos propter nomen tuum.', '℣. Arise, O Lord, help us. ℟. And deliver us for thy name’s sake.')
IN_HAC_HORA = OR('In hac hora hujus diéi tua nos, Dómine, reple misericórdia: ut per totum diem exsultántes, in tuis láudibus júgiter delectémur. Per Dóminum nostrum Jesum Christum Fílium tuum, qui tecum vivit et regnat in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum. ℟. Amen.',
                 'At this hour of the day, O Lord, fill us with thy mercy: that rejoicing all the day long we may ever delight in thy praises. Through our Lord Jesus Christ thy Son, who liveth and reigneth with thee in the unity of the Holy Ghost, God, world without end. ℟. Amen.')
DOMINE_DEUS = OR('Dómine Deus omnípotens, qui ad princípium hujus diéi nos perveníre fecísti: tua nos hódie salva virtúte; ut in hac die ad nullum declinémus peccátum, sed semper ad tuam justítiam faciéndam nostra procédant elóquia, dirigántur cogitatiónes et ópera. Per Dóminum nostrum Jesum Christum Fílium tuum, qui tecum vivit et regnat in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum. ℟. Amen.',
                 'O Lord God almighty, who hast brought us to the beginning of this day: save us today by thy power; that this day we may fall into no sin, but that all our words may go forth, and our thoughts and deeds be directed, to the doing of thy justice. Through our Lord Jesus Christ thy Son, who liveth and reigneth with thee in the unity of the Holy Ghost, God, world without end. ℟. Amen.')
PRECES_PRIME = [T('Kýrie eléison. Christe eléison. Kýrie eléison. Pater noster [silently]… ℣. Et ne nos indúcas in tentatiónem. ℟. Sed líbera nos a malo. ℣. Vivet ánima mea, et laudábit te. ℟. Et judícia tua adjuvábunt me. ℣. Errávi sicut ovis, quæ périit. ℟. Quære servum tuum, Dómine, quia mandáta tua non sum oblítus. Credo in Deum [silently]… ℣. Carnis resurrectiónem. ℟. Vitam ætérnam. Amen.',
                  'Lord, have mercy. Christ, have mercy. Lord, have mercy. Our Father [silently]… ℣. And lead us not into temptation. ℟. But deliver us from evil. ℣. My soul shall live and shall praise thee. ℟. And thy judgements shall help me. ℣. I have gone astray like a sheep that is lost. ℟. Seek thy servant, O Lord, for I have not forgotten thy commandments. I believe in God [silently]… ℣. The resurrection of the body. ℟. And life everlasting. Amen.', t='v', preces=True)]
CONFITEOR_PRIME = [
  T('Confíteor Deo omnipoténti, et beátæ Maríæ semper Vírgini, et beáto Domínico Patri nostro, et ómnibus Sanctis: quia peccávi nimis cogitatióne, locutióne, ópere et omissióne, mea culpa: precor beátam Maríam semper Vírginem, et beátum Domínicum Patrem nostrum, et omnes Sanctos oráre pro me.',
    'I confess to almighty God, and to blessed Mary ever Virgin, and to blessed Dominic our Father, and to all the Saints: that I have sinned exceedingly in thought, word, deed and omission, through my fault: I pray blessed Mary ever Virgin, and blessed Dominic our Father, and all the Saints to pray for me.', t='txt'),
  T('Misereátur mei omnípotens Deus, et dimíttat mihi ómnia peccáta mea: líberet me ab omni malo, salvet, et confírmet in omni ópere bono, et perdúcat me ad vitam ætérnam. Amen.',
    'May almighty God have mercy on me, and forgive me all my sins: deliver me from all evil, save and confirm me in every good work, and bring me to life everlasting. Amen.', t='txt')]

def prime(season, sunday, penit_sunday):
    out = [H('Ad Primam'), RUB('Pater noster, Ave María and Credo are said silently.'), {'ref': 'Deus in adjutorium'}, JAM_LUCIS]
    if penit_sunday:   # Sundays from Septuagesima to Palm Sunday
        out += [PS('Psalmi 21', gloria=True), PS('Psalmi 22'), PS('Psalmi 23'), PS('Psalmi 24'), PS('Psalmi 25'), PS('Psalmi 53'), PS('Psalmi 92', gloria=False)]
    else:
        out += [PS('Psalmi 53')]
    out += [PS('Psalmi 118: 1-16', 'Psalmus 118 · Beati immaculati'), PS('Psalmi 118: 17-32', 'Psalmus 118 · Retribue servo tuo')]
    if sunday: out.append(QUICUMQUE)
    a = PRIME_ANT.get(season, PRIME_ANT['annum'])['sun' if sunday else 'fer']
    out.append(a or {'t': 'proper', 'part': 'ant1', 'hour': 'laudes', 'la': 'Antíphona prima Laudum Dominicæ.', 'en': 'The first antiphon of Sunday Lauds.'})
    out.append(REGI if sunday else PACEM)
    if season != 'passio': out.append(JESU_CHRISTE)
    out.append(EXSURGE)
    if not sunday: out += PRECES_PRIME
    out += CONFITEOR_PRIME
    if not sunday: out.append(V('℣. Dignáre, Dómine, die isto. ℟. Sine peccáto nos custodíre.', '℣. Vouchsafe, O Lord, this day. ℟. To keep us without sin.'))
    out += [{'ref': 'Dominus vobiscum'}, {'ref': 'Oremus'}, IN_HAC_HORA if sunday else DOMINE_DEUS, {'ref': 'Dominus vobiscum'}, {'ref': 'Benedicamus'}]
    return out

# ---------------- Terce, Sext, None ----------------
HYMNS = {
 'tertia': HY('Nunc Sancte nobis Spiritus',
   ['Nunc, Sancte, nobis, Spíritus,\nUnum Patri cum Fílio,\nDignáre promptus íngeri\nNostro refúsus péctori.',
    'Os, lingua, mens, sensus, vigor\nConfessiónem pérsonent:\nFlamméscat igne cáritas,\nAccéndat ardor próximos.',
    'Præsta, Pater piíssime,\nPatríque compar Unice,\nCum Spíritu Paráclito,\nRegnans per omne sǽculum. Amen.'],
   ['Now, Holy Spirit, one with the Father and the Son,\nvouchsafe to come to us with speed,\npoured forth into our hearts.',
    'Let mouth, tongue, mind, sense and strength\nsound forth thy praise;\nlet love blaze up with fire,\nand its ardour kindle those about us.',
    'Grant this, most loving Father,\nand thou, the only Son, the Father’s equal,\nwith the Spirit, the Paraclete,\nreigning through every age. Amen.']),
 'sexta': HY('Rector potens, verax Deus',
   ['Rector potens, verax Deus,\nQui témperas rerum vices,\nSplendóre mane ínstruis,\nEt ígnibus merídiem:',
    'Exstíngue flammas lítium,\nAufer calórem nóxium,\nConfer salútem córporum,\nVerámque pacem córdium.',
    'Præsta, Pater piíssime,\nPatríque compar Unice,\nCum Spíritu Paráclito,\nRegnans per omne sǽculum. Amen.'],
   ['Mighty ruler, God of truth,\nwho orderest the changes of things,\nwho furnishest the morning with brightness\nand the noonday with fire:',
    'quench the flames of strife,\ntake away all harmful heat,\ngrant health of body\nand true peace of heart.',
    'Grant this, most loving Father,\nand thou, the only Son, the Father’s equal,\nwith the Spirit, the Paraclete,\nreigning through every age. Amen.']),
 'nona': HY('Rerum Deus tenax vigor',
   ['Rerum, Deus, tenax vigor,\nImmótus in te pérmanens,\nLucis diúrnæ témpora\nSuccéssibus detérminans:',
    'Largíre clarum véspere,\nQuo vita nusquam décidat:\nSed prǽmium mortis sacræ\nPerénnis instet glória.',
    'Præsta, Pater piíssime,\nPatríque compar Unice,\nCum Spíritu Paráclito,\nRegnans per omne sǽculum. Amen.'],
   ['O God, the unfailing strength of all things,\nwho abidest unmoved in thyself,\nand markest out the hours of the daylight\nin their due succession:',
    'grant us light at eventide,\nthat life may never fail us;\nbut that, as the reward of a holy death,\neverlasting glory may await us.',
    'Grant this, most loving Father,\nand thou, the only Son, the Father’s equal,\nwith the Spirit, the Paraclete,\nreigning through every age. Amen.']),
}
LITTLE_PS = {'tertia': [('Psalmi 118: 33-48', 'Legem pone'), ('Psalmi 118: 49-64', 'Memor esto'), ('Psalmi 118: 65-80', 'Bonitatem fecisti')],
             'sexta': [('Psalmi 118: 81-96', 'Defecit'), ('Psalmi 118: 97-112', 'Quomodo dilexi'), ('Psalmi 118: 113-128', 'Iniquos odio habui')],
             'nona': [('Psalmi 118: 129-144', 'Mirabilia'), ('Psalmi 118: 145-160', 'Clamavi'), ('Psalmi 118: 161-176', 'Principes')]}
# seasonal antiphon, chapter, short responsory, versicle; 'sun' / 'fer'
LITTLE = {
 'tertia': {
  'adventus': {'sun': {'ant': None},
               'fer': {'ant': A('Veni, Dómine, et noli tardáre: reláxa facínora plebis tuæ Israel.', 'Come, O Lord, and do not delay: loose the misdeeds of thy people Israel.')},
               'chap': CH('Jer. 23: 5', 'Ecce dies véniunt, dicit Dóminus, et suscitábo David germen justum: et regnábit rex, et sápiens erit: et fáciet judícium et justítiam in terra. ℟. Deo grátias.', 'Behold the days come, saith the Lord, and I will raise up to David a just branch: and a king shall reign, and shall be wise: and shall execute judgement and justice in the earth. ℟. Thanks be to God.'),
               'resp': R('℟. Veni ad liberándum nos, * Dómine Deus virtútum. Veni. ℣. Osténde fáciem tuam, et salvi érimus. * Dómine. Glória Patri. ℟. Veni.', '℟. Come to deliver us, * O Lord God of hosts. Come. ℣. Show thy face, and we shall be saved. * O Lord. Glory be to the Father. ℟. Come.'),
               'vers': V('℣. Timébunt gentes nomen tuum, Dómine. ℟. Et omnes reges terræ glóriam tuam.', '℣. The nations shall fear thy name, O Lord. ℟. And all the kings of the earth thy glory.')},
  'annum': {'sun': {'ant': A('Laus et perénnis glória Deo Patri, et Fílio, Sancto simul Paráclito, in sæcula sæculórum.', 'Praise and everlasting glory to God the Father, and to the Son, and likewise to the Holy Paraclete, for ever and ever.'),
                    'chap': CH('1 Joann. 4: 16', 'Deus cáritas est: et qui manet in caritáte, in Deo manet, et Deus in eo. ℟. Deo grátias.', 'God is charity: and he that abideth in charity abideth in God, and God in him. ℟. Thanks be to God.'),
                    'resp': R('℟. Inclína cor meum, Deus, * In testimónia tua. Inclína. ℣. Avérte óculos meos ne vídeant vanitátem: in via tua vivífica me. * In testimónia tua. Glória Patri. ℟. Inclína.', '℟. Incline my heart, O God, * unto thy testimonies. Incline. ℣. Turn away my eyes that they may not behold vanity: quicken me in thy way. * Unto thy testimonies. Glory be to the Father. ℟. Incline.')},
            'fer': {'ant': A('Deduc me, Dómine, in sémitam mandatórum tuórum.', 'Lead me, O Lord, into the path of thy commandments.'),
                    'chap': CH('Jer. 17: 14', 'Sana me, Dómine, et sanábor: salvum me fac, et salvus ero: quóniam laus mea tu es. ℟. Deo grátias.', 'Heal me, O Lord, and I shall be healed: save me, and I shall be saved: for thou art my praise. ℟. Thanks be to God.'),
                    'resp': R('℟. Sana ánimam meam, * Quia peccávi tibi. Sana. ℣. Ego dixi: Dómine, miserére mei. * Quia. Glória Patri. ℟. Sana.', '℟. Heal my soul, * for I have sinned against thee. Heal. ℣. I said: O Lord, be thou merciful to me. * For I have sinned. Glory be to the Father. ℟. Heal.')},
            'vers': V('℣. Adjútor meus esto, Dómine: ne derelínquas me. ℟. Neque despícias me, Deus salutáris meus.', '℣. Be thou my helper, O Lord: forsake me not. ℟. Do not despise me, O God my Saviour.')},
  'quadragesima': {'fer': {'ant': A('Advenérunt nobis dies pœniténtiæ, ad rediménda peccáta, et salvándas ánimas.', 'The days of penance are come upon us, to redeem our sins and to save our souls.'),
                           'chap': CH('Joel 2: 12-13', 'Convertímini ad me in toto corde vestro, in jejúnio, et fletu, et planctu: et scíndite corda vestra, et non vestiménta vestra, ait Dóminus omnípotens. ℟. Deo grátias.', 'Be converted to me with all your heart, in fasting, and in weeping, and in mourning: and rend your hearts, and not your garments, saith the Lord almighty. ℟. Thanks be to God.')},
                   'sun': {}},
  'passio': {'fer': {'ant': A('Judicásti, Dómine, causam ánimæ meæ: defénsor vitæ meæ, Dómine Deus meus.', 'Thou hast judged, O Lord, the cause of my soul: thou art the defender of my life, O Lord my God.')}, 'sun': {}},
  'pascha': {'sun': {}, 'fer': {},
             'ant': A('Pax vobis, ego sum, allelúia: nolíte timére, allelúia.', 'Peace be to you, it is I, alleluia: fear not, alleluia.'),
             'chap': CH('Rom. 6: 9-10', 'Christus resúrgens ex mórtuis jam non móritur, mors illi ultra non dominábitur. Quod enim mórtuus est peccáto, mórtuus est semel: quod autem vivit, vivit Deo. ℟. Deo grátias.', 'Christ rising again from the dead dieth now no more, death shall no more have dominion over him. For in that he died to sin, he died once: but in that he liveth, he liveth unto God. ℟. Thanks be to God.'),
             'vers': V('℣. Surréxit Dóminus vere, allelúia. ℟. Et appáruit Simóni, allelúia.', '℣. The Lord is risen indeed, alleluia. ℟. And hath appeared to Simon, alleluia.')},
 },
 'sexta': {
  'adventus': {'sun': {'ant': None},
               'fer': {'ant': A('Tuam, Dómine, éxcita poténtiam, et veni ad salvándum nos.', 'Stir up thy might, O Lord, and come to save us.')},
               'chap': CH('Jer. 23: 6', 'In diébus illis salvábitur Juda, et Israel habitábit confidénter: et hoc est nomen, quod vocábunt eum, Dóminus justus noster. ℟. Deo grátias.', 'In those days shall Juda be saved, and Israel shall dwell confidently: and this is the name that they shall call him, The Lord our just one. ℟. Thanks be to God.'),
               'resp': R('℟. Osténde nobis, Dómine, * Misericórdiam tuam. Osténde. ℣. Et salutáre tuum da nobis. * Misericórdiam tuam. Glória Patri. ℟. Osténde.', '℟. Show us, O Lord, * thy mercy. Show us. ℣. And grant us thy salvation. * Thy mercy. Glory be to the Father. ℟. Show us.'),
               'vers': V('℣. Meménto nostri, Dómine, in beneplácito pópuli tui. ℟. Vísita nos in salutári tuo.', '℣. Remember us, O Lord, in the favour of thy people. ℟. Visit us with thy salvation.')},
  'annum': {'sun': {'ant': A('Glória laudis résonet in ore ómnium Patri genitǽque Proli: Spirítui Sancto páriter resúltet laude perénni.', 'Let the glory of praise resound in the mouth of all to the Father and to the Son begotten; and to the Holy Spirit likewise let it ring out in praise unending.'),
                    'chap': CH('2 Cor. 13: 13', 'Grátia Dómini nostri Jesu Christi, et cáritas Dei, et communicátio Sancti Spíritus sit semper cum ómnibus vobis. Amen. ℟. Deo grátias.', 'The grace of our Lord Jesus Christ, and the charity of God, and the communication of the Holy Ghost be always with you all. Amen. ℟. Thanks be to God.'),
                    'resp': R('℟. In ætérnum, Dómine, * Pérmanet verbum tuum. In ætérnum. ℣. In cælo, et in sǽculum sǽculi véritas tua. * Pérmanet. Glória Patri. ℟. In ætérnum.', '℟. For ever, O Lord, * thy word standeth firm. For ever. ℣. In heaven, and from generation to generation, is thy truth. * Thy word. Glory be to the Father. ℟. For ever.')},
            'fer': {'ant': A('Ádjuva me, et salvus ero, Dómine.', 'Help me, and I shall be saved, O Lord.'),
                    'chap': CH('Gal. 6: 2', 'Alter altérius ónera portáte, et sic adimplébitis legem Christi. ℟. Deo grátias.', 'Bear ye one another’s burdens, and so you shall fulfil the law of Christ. ℟. Thanks be to God.')},
            'vers': V('℣. Dóminus regit me, et nihil mihi déerit. ℟. In loco páscuæ ibi me collocávit.', '℣. The Lord ruleth me, and I shall want nothing. ℟. He hath set me in a place of pasture.')},
  'quadragesima': {'fer': {'ant': A('Commendémus nosmetípsos in multa patiéntia, in jejúniis multis, per arma justítiæ.', 'Let us commend ourselves in much patience, in many fastings, by the armour of justice.'),
                           'chap': CH('Isai. 55: 7', 'Derelínquat ímpius viam suam, et vir iníquus cogitatiónes suas, et revertátur ad Dóminum, et miserébitur ejus: et ad Deum nostrum, quóniam multus est ad ignoscéndum. ℟. Deo grátias.', 'Let the wicked forsake his way, and the unjust man his thoughts, and let him return to the Lord, and he will have mercy on him: and to our God, for he is bountiful to forgive. ℟. Thanks be to God.')},
                   'sun': {}},
  'passio': {'fer': {'ant': A('Pópule meus, quid feci tibi, aut quid moléstus fui? Respónde mihi.', 'O my people, what have I done to thee, or in what have I grieved thee? Answer thou me.'),
                     'chap': CH('Isai. 50: 6-7', 'Fáciem meam non avérti ab increpántibus, et conspuéntibus in me: Dóminus Deus auxiliátor meus, ídeo non sum confúsus. ℟. Deo grátias.', 'I have not turned away my face from them that rebuked me and spit upon me: the Lord God is my helper, therefore am I not confounded. ℟. Thanks be to God.'),
                     'vers': V('℣. Ne perdas cum ímpiis, Deus, ánimam meam. ℟. Et cum viris sánguinum vitam meam.', '℣. Take not away my soul, O God, with the wicked. ℟. Nor my life with bloody men.')}, 'sun': {}},
  'pascha': {'sun': {}, 'fer': {},
             'ant': A('Ecce ego vobíscum sum, allelúia, ómnibus diébus, allelúia.', 'Behold I am with you, alleluia, all days, alleluia.'),
             'chap': CH('Col. 3: 1-2', 'Si consurrexístis cum Christo, quæ sursum sunt quǽrite, ubi Christus est in déxtera Dei sedens: quæ sursum sunt sápite, non quæ super terram. ℟. Deo grátias.', 'If you be risen with Christ, seek the things that are above, where Christ is sitting at the right hand of God: mind the things that are above, not the things that are upon the earth. ℟. Thanks be to God.'),
             'vers': V('℣. Surréxit Dóminus de sepúlcro, allelúia. ℟. Qui pro nobis pepéndit in ligno, allelúia.', '℣. The Lord is risen from the tomb, alleluia. ℟. Who for us hung upon the tree, alleluia.')},
 },
 'nona': {
  'adventus': {'sun': {'ant': None},
               'fer': {'ant': A('In tuo advéntu érue nos, Dómine.', 'At thy coming deliver us, O Lord.')},
               'chap': CH('Isai. 2: 2', 'Erit in novíssimis diébus præparátus mons domus Dómini in vértice móntium, et elevábitur super colles, et fluent ad eum omnes gentes. ℟. Deo grátias.', 'In the last days the mountain of the house of the Lord shall be prepared on the top of mountains, and it shall be exalted above the hills, and all nations shall flow unto it. ℟. Thanks be to God.'),
               'resp': R('℟. Super te, Jerúsalem, * Oriétur Dóminus. Super te. ℣. Et glória ejus in te vidébitur. * Oriétur. Glória Patri. ℟. Super te.', '℟. Upon thee, O Jerusalem, * shall the Lord arise. Upon thee. ℣. And his glory shall be seen upon thee. * Shall the Lord arise. Glory be to the Father. ℟. Upon thee.'),
               'vers': V('℣. Dómine Deus virtútum, convérte nos. ℟. Et osténde fáciem tuam, et salvi érimus.', '℣. O Lord God of hosts, convert us. ℟. And show thy face, and we shall be saved.')},
  'annum': {'sun': {'ant': A('Ex quo ómnia, per quem ómnia, in quo ómnia: ipsi glória in sǽcula.', 'Of whom are all things, by whom are all things, in whom are all things: to him be glory for ever.'),
                    'chap': CH('1 Joann. 5: 7', 'Tres sunt, qui testimónium dant in cælo: Pater, Verbum, et Spíritus Sanctus: et hi tres unum sunt. ℟. Deo grátias.', 'There are three who give testimony in heaven: the Father, the Word, and the Holy Ghost: and these three are one. ℟. Thanks be to God.')},
            'fer': {'ant': A('Áspice in me, Dómine, et miserére mei.', 'Look thou upon me, O Lord, and have mercy on me.'),
                    'chap': CH('1 Cor. 6: 20', 'Empti enim estis prétio magno: glorificáte, et portáte Deum in córpore vestro. ℟. Deo grátias.', 'For you are bought with a great price: glorify and bear God in your body. ℟. Thanks be to God.')},
            'vers': V('℣. Ab occúltis meis munda me, Dómine. ℟. Et ab aliénis parce servo tuo.', '℣. From my secret sins cleanse me, O Lord. ℟. And from those of others spare thy servant.')},
  'quadragesima': {'fer': {'ant': A('Per arma justítiæ virtútis Dei, commendémus nosmetípsos in multa patiéntia.', 'By the armour of justice, of the power of God, let us commend ourselves in much patience.'),
                           'chap': CH('Isai. 58: 7', 'Frange esuriénti panem tuum, et egénos, vagósque induc in domum tuam: cum víderis nudum, óperi eum, et carnem tuam ne despéxeris, ait Dóminus omnípotens. ℟. Deo grátias.', 'Deal thy bread to the hungry, and bring the needy and the harbourless into thy house: when thou shalt see one naked, cover him, and despise not thy own flesh, saith the Lord almighty. ℟. Thanks be to God.')},
                   'sun': {}},
  'passio': {'fer': {'ant': A('Numquid rédditur pro bono malum, quia fodérunt fóveam ánimæ meæ?', 'Shall evil be rendered for good, because they have dug a pit for my soul?'),
                     'chap': CH('Jer. 17: 18', 'Confundántur qui me persequúntur, et non confúndar ego: páveant illi, et non páveam ego: induc super eos diem afflictiónis, et dúplici contritióne cóntere eos, Dómine Deus noster. ℟. Deo grátias.', 'Let them be confounded that persecute me, and let not me be confounded: let them be afraid, and let not me be afraid: bring upon them the day of affliction, and with a double destruction destroy them, O Lord our God. ℟. Thanks be to God.'),
                     'resp': R('℟. Príncipes persecúti sunt me gratis, et a verbis tuis formidávit cor meum: * Lætábor ego super elóquia tua. ℣. Quasi qui invénit spólia multa. * Lætábor ego. ℟. Príncipes.', '℟. Princes have persecuted me without cause, and my heart hath been in awe of thy words: * I will rejoice at thy words. ℣. As one that hath found great spoil. * I will rejoice. ℟. Princes.'),
                     'vers': V('℣. Éripe me de inimícis meis, Deus meus. ℟. Et ab insurgéntibus in me líbera me.', '℣. Deliver me from my enemies, O my God. ℟. And defend me from them that rise up against me.')}, 'sun': {}},
  'pascha': {'sun': {}, 'fer': {},
             'ant': A('Ecce ego vobíscum sum, allelúia, ómnibus diébus, allelúia.', 'Behold I am with you, alleluia, all days, alleluia.'),
             'chap': CH('Col. 3: 1-2', 'Si consurrexístis cum Christo, quæ sursum sunt quǽrite, ubi Christus est in déxtera Dei sedens: quæ sursum sunt sápite, non quæ super terram. ℟. Deo grátias.', 'If you be risen with Christ, seek the things that are above, where Christ is sitting at the right hand of God: mind the things that are above, not the things that are upon the earth. ℟. Thanks be to God.'),
             'vers': V('℣. Surréxit Dóminus de sepúlcro, allelúia. ℟. Qui pro nobis pepéndit in ligno, allelúia.', '℣. The Lord is risen from the tomb, alleluia. ℟. Who for us hung upon the tree, alleluia.')},
 },
}

QUICUMQUE_TEXT = [
 ('Quicúmque vult salvus esse, * ante ómnia opus est, ut téneat cathólicam fidem:', 'Whosoever will be saved, * before all things it is necessary that he hold the catholic faith:'),
 ('Quam nisi quisque íntegram inviolatámque serváverit, * absque dúbio in ætérnum peribit.', 'which faith except every one do keep whole and undefiled, * without doubt he shall perish everlastingly.'),
 ('Fides autem cathólica hæc est: * ut unum Deum in Trinitáte, et Trinitátem in unitáte venerémur.', 'And the catholic faith is this: * that we worship one God in Trinity, and Trinity in unity;'),
 ('Neque confundéntes persónas, * neque substántiam separántes.', 'neither confounding the persons, * nor dividing the substance.'),
 ('Alia est enim persóna Patris, ália Fílii, * ália Spíritus Sancti:', 'For there is one person of the Father, another of the Son, * and another of the Holy Ghost;'),
 ('Sed Patris, et Fílii, et Spíritus Sancti una est divínitas, * æquális glória, coætérna majéstas.', 'but the Godhead of the Father, of the Son, and of the Holy Ghost is all one, * the glory equal, the majesty co-eternal.'),
 ('Qualis Pater, talis Fílius, * talis Spíritus Sanctus.', 'Such as the Father is, such is the Son, * and such is the Holy Ghost.'),
 ('Increátus Pater, increátus Fílius, * increátus Spíritus Sanctus.', 'The Father uncreate, the Son uncreate, * and the Holy Ghost uncreate.'),
 ('Imménsus Pater, imménsus Fílius, * imménsus Spíritus Sanctus.', 'The Father incomprehensible, the Son incomprehensible, * and the Holy Ghost incomprehensible.'),
 ('Ætérnus Pater, ætérnus Fílius, * ætérnus Spíritus Sanctus.', 'The Father eternal, the Son eternal, * and the Holy Ghost eternal.'),
 ('Et tamen non tres ætérni, * sed unus ætérnus.', 'And yet they are not three eternals, * but one eternal.'),
 ('Sicut non tres increáti, nec tres imménsi, * sed unus increátus, et unus imménsus.', 'As also there are not three uncreated, nor three incomprehensibles, * but one uncreated and one incomprehensible.'),
 ('Simíliter omnípotens Pater, omnípotens Fílius, * omnípotens Spíritus Sanctus.', 'So likewise the Father is almighty, the Son almighty, * and the Holy Ghost almighty;'),
 ('Et tamen non tres omnipoténtes, * sed unus omnípotens.', 'and yet they are not three almighties, * but one almighty.'),
 ('Ita Deus Pater, Deus Fílius, * Deus Spíritus Sanctus.', 'So the Father is God, the Son is God, * and the Holy Ghost is God;'),
 ('Et tamen non tres dii, * sed unus est Deus.', 'and yet they are not three gods, * but one God.'),
 ('Ita Dóminus Pater, Dóminus Fílius, * Dóminus Spíritus Sanctus.', 'So likewise the Father is Lord, the Son Lord, * and the Holy Ghost Lord;'),
 ('Et tamen non tres Dómini, * sed unus est Dóminus.', 'and yet not three lords, * but one Lord.'),
 ('Quia, sicut singillátim unamquámque persónam Deum ac Dóminum confitéri christiána veritáte compéllimur: * ita tres Deos aut Dóminos dícere cathólica religióne prohibémur.', 'For like as we are compelled by the Christian verity to acknowledge every person by himself to be God and Lord, * so are we forbidden by the catholic religion to say there be three gods or three lords.'),
 ('Pater a nullo est factus: * nec creátus, nec génitus.', 'The Father is made of none, * neither created, nor begotten.'),
 ('Fílius a Patre solo est: * non factus, nec creátus, sed génitus.', 'The Son is of the Father alone, * not made, nor created, but begotten.'),
 ('Spíritus Sanctus a Patre et Fílio: * non factus, nec creátus, nec génitus, sed procédens.', 'The Holy Ghost is of the Father and of the Son, * neither made, nor created, nor begotten, but proceeding.'),
 ('Unus ergo Pater, non tres Patres: unus Fílius, non tres Fílii: * unus Spíritus Sanctus, non tres Spíritus Sancti.', 'So there is one Father, not three fathers; one Son, not three sons; * one Holy Ghost, not three holy ghosts.'),
 ('Et in hac Trinitáte nihil prius aut postérius, nihil majus aut minus: * sed totæ tres persónæ coætérnæ sibi sunt et coæquáles.', 'And in this Trinity none is afore or after another, none is greater or less than another; * but the whole three persons are co-eternal together and co-equal.'),
 ('Ita ut per ómnia, sicut jam supra dictum est, * et únitas in Trinitáte, et Trínitas in unitáte veneránda sit.', 'So that in all things, as is aforesaid, * the unity in Trinity and the Trinity in unity is to be worshipped.'),
 ('Qui vult ergo salvus esse, * ita de Trinitáte séntiat.', 'He therefore that will be saved, * must thus think of the Trinity.'),
 ('Sed necessárium est ad ætérnam salútem, * ut Incarnatiónem quoque Dómini nostri Jesu Christi fidéliter credat.', 'Furthermore, it is necessary to everlasting salvation * that he also believe rightly the Incarnation of our Lord Jesus Christ.'),
 ('Est ergo fides recta, ut credámus et confiteámur, * quia Dóminus noster Jesus Christus, Dei Fílius, Deus et homo est.', 'For the right faith is, that we believe and confess * that our Lord Jesus Christ, the Son of God, is God and man;'),
 ('Deus est ex substántia Patris ante sǽcula génitus: * et homo est ex substántia matris in sǽculo natus.', 'God, of the substance of the Father, begotten before the worlds; * and man, of the substance of his mother, born in the world;'),
 ('Perféctus Deus, perféctus homo: * ex ánima rationáli et humána carne subsístens.', 'perfect God and perfect man, * of a reasonable soul and human flesh subsisting;'),
 ('Æquális Patri secúndum divinitátem: * minor Patre secúndum humanitátem.', 'equal to the Father as touching his Godhead, * and inferior to the Father as touching his manhood.'),
 ('Qui licet Deus sit et homo, * non duo tamen, sed unus est Christus.', 'Who, although he be God and man, * yet he is not two, but one Christ;'),
 ('Unus autem non conversióne divinitátis in carnem, * sed assumptióne humanitátis in Deum.', 'one, not by conversion of the Godhead into flesh, * but by taking of the manhood into God;'),
 ('Unus omníno, non confusióne substántiæ, * sed unitáte persónæ.', 'one altogether, not by confusion of substance, * but by unity of person.'),
 ('Nam sicut ánima rationális et caro unus est homo: * ita Deus et homo unus est Christus.', 'For as the reasonable soul and flesh is one man, * so God and man is one Christ;'),
 ('Qui passus est pro salúte nostra: descéndit ad ínferos: * tértia die resurréxit a mórtuis.', 'who suffered for our salvation, descended into hell, * rose again the third day from the dead.'),
 ('Ascéndit ad cælos, sedet ad déxteram Dei Patris omnipoténtis: * inde ventúrus est judicáre vivos et mórtuos.', 'He ascended into heaven, he sitteth on the right hand of God the Father almighty, * from whence he shall come to judge the living and the dead.'),
 ('Ad cujus advéntum omnes hómines resúrgere habent cum corpóribus suis: * et redditúri sunt de factis própriis ratiónem.', 'At whose coming all men shall rise again with their bodies, * and shall give account for their own works.'),
 ('Et qui bona egérunt, ibunt in vitam ætérnam: * qui vero mala, in ignem ætérnum.', 'And they that have done good shall go into life everlasting; * and they that have done evil into everlasting fire.'),
 ('Hæc est fides cathólica, * quam nisi quisque fidéliter firmitérque credíderit, salvus esse non póterit.', 'This is the catholic faith, * which except a man believe faithfully and firmly, he cannot be saved.')]
data = {'quicumque': QUICUMQUE_TEXT, 'ordinarium': ORD, 'compline': {s: compline(s) for s in ('annum', 'lent1', 'lent3', 'passio', 'pascha', 'ascensio', 'pentecostes', 'holyweds')},
        'prime': {'annum': None}, 'little': LITTLE, 'littleHymns': HYMNS, 'littlePsalms': LITTLE_PS, 'primeAnt': PRIME_ANT,
        'primeParts': {'jamLucis': JAM_LUCIS, 'regi': REGI, 'pacem': PACEM, 'jesuChriste': JESU_CHRISTE, 'exsurge': EXSURGE, 'inHacHora': IN_HAC_HORA, 'domineDeus': DOMINE_DEUS, 'preces': PRECES_PRIME, 'confiteor': CONFITEOR_PRIME}}
# Prime for every combination the page needs
data['prime'] = {}
for s in ('adventus', 'annum', 'quadragesima', 'passio', 'pascha'):
    for sun in (0, 1):
        data['prime']['%s_%d' % (s, sun)] = prime(s, sun, False)
data['prime']['penit_1'] = prime('annum', 1, True)
with open('site/data/office.js', 'w', encoding='utf8') as f:
    f.write('// Generated by build_office.py from the Breviarium O.P. (1909). Do not edit by hand.\n')
    f.write('var OFFICE = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
print('office.js', sum(len(v) for v in data['compline'].values()), 'Compline items')
