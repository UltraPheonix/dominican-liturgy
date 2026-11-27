"""The Masses for the Dead as the Missale O.P. (1939) gives them, pp. 114*-121*: idempotent; run after any rebuild of
data/masses.js, data/orations.js or data/readings33.js:  python3 tools/requiem/build.py
- C114s = 'In Missis quotidianis Defunctorum' (the weekly conventual Mass for the dead): Lesson Apoc. 14, Gospel Jn 6:51-55,
  three prayers: (1) Pro defunctis Episcopis seu Sacerdotibus "Deus, qui inter apostolicos" (said first when it is not
  specified for whom the Mass is offered), (2) Pro defunctis fratribus, propinquis et benefactoribus (ADDIV set defFr),
  (3) Pro vivis et defunctis (ADDIV d38); Responsorium Requiem with V. Animae and Tract Absolve (pro pluribus);
  for one only: Si ambulem, Sicut cervus (extras).
- C114o = 'In die obitus seu depositionis defuncti' (pp. 114*-116*): Lesson 1 Thess. 4:13-18, Responsorium Si ambulem,
  Tract Sicut cervus, Gospel Jn 11:21-27, prayers Deus, cui proprium est.
- The anniversary is S1113 (pp. 116*-118*)."""
import json, os
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def load(path, var):
    s = open(R + path, encoding='utf8').read(); i = s.index(var) + len(var); j = s.rstrip().rstrip(';').rindex('}') + 1
    return s[:i], json.loads(s[i:j]), s[j:]
LC = 'Per Dóminum nostrum Iesum Christum, Fílium tuum: qui tecum vivit et regnat in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum.'
EC = 'through our Lord Jesus Christ, Your Son, who lives and reigns with You in the unity of the Holy Spirit, God, world without end.'
SRC = 'Missale O.P. (1939), pp. 118*-121* (In Missis quotidianis Defunctorum)'
P1 = {
 'or': ('Deus, qui inter apostólicos Sacerdótes, fámulos tuos Pontificáli vel Sacerdotáli fecísti dignitáte vigére; præsta, quǽsumus, ut eórum quoque perpétuo aggregéntur consórtio:',
        'O God, who raised Your servants to the dignity of bishops (or priests) in the apostolic priesthood; grant, we beseech You, that they may be joined in fellowship with Your apostles forever;'),
 'se': ('Súscipe Dómine, quǽsumus, pro animábus famulórum tuórum Pontíficum vel Sacerdótum, quas offérimus, hóstias: ut quibus in hoc sǽculo Pontificále seu Sacerdotále donásti méritum, in cælésti regno Sanctórum tuórum iúbeas iungi consórtio.',
        'Receive, we beseech You, O Lord, the sacrifice which we offer up on behalf of Your servants who were bishops (or priests), so that those whom You raised up to episcopal (or priestly) rank in this world may, by Your command, be joined to Your saints in the kingdom of heaven;'),
 'pc': ('Prosit, quǽsumus Dómine, animábus famulórum tuórum Pontíficum seu Sacerdótum misericórdiæ tuæ imploráta cleméntia; ut eius, in quo speravérunt, et credidérunt, ætérnum cápiant, te miseránte, consórtium:',
        'We beseech You, O Lord, that Your clemency, which we implore, may benefit the souls of Your servants who were bishops (or priests), that by Your mercy they may obtain eternal fellowship with Him in whom they hoped and believed;'),
}
FR = {'n': 'defFr', 'la': 'Pro defunctis fratribus, propinquis et benefactoribus', 'en': 'For our deceased brethren, relatives and benefactors',
 'or': ('Deus, véniæ largítor, et humánæ salútis auctor, quǽsumus cleméntiam tuam: ut nostræ congregatiónis fratres, soróres, familiáres, et benefactóres, qui ex hoc sǽculo transiérunt; beáta María semper Vírgine intercedénte cum ómnibus Sanctis tuis, ad perpétuæ beatitúdinis consórtium perveníre concédas:',
        'O God, the giver of pardon and the author of human salvation, we beseech Your clemency, that by the intercession of the blessed Mary ever Virgin, and of all Your saints, You would grant that the brethren, sisters, relatives and benefactors of our Order who have passed out of this life may partake of everlasting bliss;'),
 'se': ('Deus, cuius misericórdiæ non est númerus, súscipe propítius preces humilitátis nostræ: et animábus fratrum, sorórum, familiárium, et benefactórum nostrórum, quibus tui nóminis dedísti confessiónem, per hæc sacraménta salútis nostræ, cunctórum remissiónem tríbue peccatórum.',
        'O God, of whose mercy there is no end, favorably receive our humble prayers, and by means of this sacrament of our salvation grant to the souls of our brethren, sisters, relatives and benefactors, who by Your grace confessed Your holy name, remission of all their sins;'),
 'pc': ('Præsta, quǽsumus, omnípotens et miséricors Deus: ut ánimæ fratrum, sorórum, familiárium, et benefactórum nostrórum, pro quibus hoc sacrifícium laudis tuæ obtúlimus maiestáti; per huius virtútem sacraménti a peccátis ómnibus expiátæ, lucis perpétuæ, te miseránte, recípiant beatitúdinem:',
        'Grant, we beseech You, almighty and merciful God, that the souls of our brethren, sisters, relatives and benefactors, for whom we offer up to Your majesty this sacrifice of praise, may, by virtue of this sacrament, be cleansed from all sin, and by Your mercy receive the happiness of eternal light;'),
}
# ---- orations
h, O, t = load('/data/orations.js', 'window.ORATIONS = ')
if 'C114o' not in O: O['C114o'] = O['C114s']            # the old C114s were the prayers of the day of death
O['C114o']['src'] = 'Missale O.P. (1939), pp. 114*-116* (In die obitus seu depositionis defuncti); English after the St Dominic Missal (1959), checked against the Latin'
# the weekly conventual Mass for the dead (Rubr. VI.2) is for the brethren, familiars and benefactors: Rubr. XII.6 "prima
# Oratio erit Deus, veniae largitor, secunda Deus, qui nos Patrem, tertia non mutabitur" (Omnipotens ... qui vivorum)
O['C114s'] = {'src': SRC + '; prayers by Rubr. gen. XII.6 (the weekly Mass for the brethren, familiars and benefactors): Deus, veniae largitor; Deus, qui nos patrem (Orationes diversae n. 8, p. 124*); Omnipotens ... qui vivorum. English after the St Dominic Missal (1959)',
              'or': [FR['or'][0] + ' ' + LC, FR['or'][1] + ' ' + EC], 'se': [FR['se'][0] + ' ' + LC, FR['se'][1] + ' ' + EC], 'pc': [FR['pc'][0] + ' ' + LC, FR['pc'][1] + ' ' + EC]}
open(R + '/data/orations.js', 'w', encoding='utf8').write(h + json.dumps(O, ensure_ascii=False) + t)
# ---- the 2nd prayer as a set of the Orationes ad diversa (the 3rd is d38, Pro vivis et defunctis alia)
h, A, t = load('/data/addiv.js', 'window.ADDIV = ')
def part(la, en): return {'la': la, 'lc': LC, 'en': en.rstrip(';'), 'ec': EC[0].upper() + EC[1:], 's': 'ai'}
PM = {'or': ('Deus, qui nos patrem et matrem honoráre præcepísti: miserére cleménter animábus paréntum nostrórum: eorúmque peccáta dimítte; nosque eos in ætérnæ claritátis gáudio fac vidére:',
             'O God, You have commanded us to honor our father and mother; in Your loving kindness have mercy on the souls of our parents; forgive them their sins, and bring us to see them in the joy of eternal light;'),
      'se': ('Súscipe sacrifícium Dómine, quod tibi pro animábus paréntum nostrórum offérimus: eísque gáudium sempitérnum in regióne vivórum concéde; nosque cum illis felicitáti Sanctórum coniúnge.',
             'Receive, O Lord, the sacrifice which we offer to You for the souls of our parents; grant them everlasting joy in the land of the living, and in their company let us share in the happiness of the saints;'),
      'pc': ('Cæléstis participátio sacraménti, quǽsumus Dómine, animábus paréntum nostrórum réquiem et lucem obtíneat perpétuam; nosque cum illis grátia tua corónet ætérna:',
             'We beseech You, O Lord, that this heavenly sacrament of which we have partaken may obtain for the souls of our parents rest and light everlasting; and may Your grace crown us with them for evermore;')}
A['sets']['defPM'] = {'n': 0, 'la': 'Pro patre et matre simul', 'en': 'For our fathers and mothers', 'or': part(*PM['or']), 'se': part(*PM['se']), 'pc': part(*PM['pc']),
                      'inc': 'Deus, qui nos patrem', 'src': 'Missale O.P. (1939), Orationes diversae pro Defunctis n. 8, p. 124*; English after the St Dominic Missal (1959), in the plural'}
# the 2nd prayers of the Order's four Anniversaries (Rubr. XII.7; Ordo 1944, 4 Feb., 12 Jul., 5 Sept., 10 Nov.): in February
# Deus, qui nos patrem (defPM), in July Deus, cujus miseratione (defMis, Orationes diversae pro Defunctis n. 9, p. 124*),
# in September and November Deus, veniae largitor in the Order's form (defFr, In Missis quotidianis, Secunda Oratio, p. 119*)
A['sets']['defFr'] = {'n': 0, 'la': FR['la'], 'en': FR['en'], 'or': part(*FR['or']), 'se': part(*FR['se']), 'pc': part(*FR['pc']),
                      'inc': 'Deus, véniæ largítor', 'src': 'Missale O.P. (1939), In Missis quotidianis Defunctorum, Secunda Oratio, p. 119* (the Secret and Postcommunion as at the weekly Mass)'}
MIS = {'or': ('Deus, cuius miseratióne ánimæ fidélium requiéscunt: fámulis et famulábus tuis ómnibus, hic et ubíque in Christo quiescéntibus, da propítius véniam peccatórum; ut a cunctis reátibus absolúti, tecum sine fine læténtur:',
              'O God, by whose mercy the souls of the faithful find rest, mercifully grant to all Your servants and handmaids who rest in Christ, here and everywhere, the pardon of their sins, that, set free from all guilt, they may rejoice with You without end;'),
       'se': ('Pro animábus famulórum famularúmque tuárum, et ómnium catholicórum hic et ubíque in Christo dormiéntium, hóstiam Dómine súscipe benígnus oblátam: ut hoc sacrifício singulári, vínculis horréndæ mortis exútæ, vitam mereántur ætérnam.',
              'For the souls of Your servants and handmaids, and of all Catholics who sleep in Christ here and everywhere, receive graciously, O Lord, the sacrifice we offer, that, loosed by this singular sacrifice from the bonds of dreadful death, they may deserve eternal life;'),
       'pc': ('Deus, fidélium lumen animárum, adésto supplicatiónibus nostris: et da fámulis et famulábus tuis, quorum córpora hic et ubíque in Christo requiéscunt; refrigérii sedem, quiétis beatitúdinem, et lúminis claritátem:',
              'O God, the light of faithful souls, be present to our supplications, and grant to Your servants and handmaids, whose bodies rest here and everywhere in Christ, a place of refreshment, the happiness of rest and the brightness of light;')}
A['sets']['defMis'] = {'n': 0, 'la': 'Pro his, qui in cœmeterio requiescunt', 'en': 'For those who rest in the cemetery', 'or': part(*MIS['or']), 'se': part(*MIS['se']), 'pc': part(*MIS['pc']),
                       'inc': 'Deus, cuius miseratióne', 'src': 'Missale O.P. (1939), Orationes diversae pro Defunctis n. 9, p. 124* (Latin read from the scan); English: AI translation'}
open(R + '/data/addiv.js', 'w', encoding='utf8').write(h + json.dumps(A, ensure_ascii=False, separators=(',', ':')) + t)
# ---- readings
h, RD, t = load('/data/readings33.js', 'var READINGS33 = ')
if not any(r['ref'].startswith('Joannes 11') for r in RD.get('C114o', [])):
    RD['C114o'] = [r for r in RD.get('C114s', []) if r['ref'].startswith('Joannes 11')]
thes = {'type': 'Lesson', 'ref': 'Ad Thessalonicenses 1 4: 13-18', 'title': 'Léctio Epístolæ beáti Pauli Apóstoli ad Thessalonicénses.',
        'title_en': 'Lesson from the Epistle of blessed Paul the Apostle to the Thessalonians.',
        'la': 'Fratres: Nólumus vos ignoráre de dormiéntibus, ut non contristémini sicut et céteri, qui spem non habent. Si enim crédimus quod Jesus mórtuus est, et resurréxit: ita et Deus eos, qui dormiérunt per Jesum, addúcet cum eo. Hoc enim vobis dícimus in verbo Dómini, quia nos, qui vívimus, qui resídui sumus in advéntum Dómini, non præveniémus eos, qui dormiérunt. Quóniam ipse Dóminus in jussu, et in voce Archángeli, et in tuba Dei descéndet de cælo: et mórtui, qui in Christo sunt, resúrgent primi. Deínde nos, qui vívimus, qui relínquimur, simul rapiémur cum illis in núbibus óbviam Christo in áera, et sic semper cum Dómino érimus. Itaque consolámini ínvicem in verbis istis.',
        'en': 'Brethren: We will not have you ignorant concerning them that are asleep, that you be not sorrowful, even as others who have no hope. For if we believe that Jesus died, and rose again; even so them who have slept through Jesus, will God bring with him. For this we say unto you in the word of the Lord, that we who are alive, who remain unto the coming of the Lord, shall not prevent them who have slept. For the Lord himself shall come down from heaven with commandment, and with the voice of an archangel, and with the trumpet of God: and the dead who are in Christ, shall rise first. Then we who are alive, who are left, shall be taken up together with them in the clouds to meet Christ, into the air, and so shall we be always with the Lord. Wherefore, comfort ye one another with these words.',
        'p33': None, 'src': 'Missale O.P. 1939, p. 114*; Vulgate and Douay-Rheims verses'}
RD['C114o'] = [thes] + [r for r in RD['C114o'] if r['type'] == 'Gospel']
RD['C114s'] = [dict(r, src='Missale O.P. 1939, pp. 119*-120* (In Missis quotidianis Defunctorum)') for r in RD['S1102_3']]
open(R + '/data/readings33.js', 'w', encoding='utf8').write(h + json.dumps(RD, ensure_ascii=False, separators=(',', ':')) + t)
# ---- masses
h, D, t = load('/data/masses.js', 'var DOMINICAN = ')
M = D['masses']; q = M['C114s']
# one name everywhere (qc_ui W7): the weekly conventual Mass for the brethren, relatives and benefactors (Rubr. VI.2, XII.6)
q['title'] = 'Missa pro Defunctis (conventualis)'; q['en'] = 'Conventual Requiem for the brethren, relatives and benefactors'
q['page'] = '114*-121*'; q['conf'] = 'missal'
q['note'] = ('Missale O.P. (1939), pp. 118*-121*: In Missis quotidianis Defunctorum. For several (and at the conventual Mass): '
             'Responsorium Requiem with V. Animae eorum and Tract Absolve; for one only: Si ambulem and Sicut cervus. '
             'The Sequence is said at sung and conventual Masses; at others it is at the priest\'s choice.')
q['readings'] = [{'type': 'Lesson', 'ref': 'Apocalypsis 14: 13', 'm39': True}, {'type': 'Gospel', 'ref': 'Joannes 6: 51-55', 'm39': True}]
o = json.loads(json.dumps(q))
o.update({'title': 'Missa pro Defunctis in die obitus seu depositionis', 'en': 'Mass for the Dead on the day of death or burial',
          'page': '114*-116*', 'note': 'Missale O.P. (1939), pp. 114*-116*. On the third, seventh and thirtieth day the same Mass with other prayers (p. 116*).',
          'readings': [{'type': 'Lesson', 'ref': 'Ad Thessalonicenses 1 4: 13-18', 'm39': True}, {'type': 'Gospel', 'ref': 'Joannes 11: 21-27', 'm39': True}],
          'extras': [6001, 'op-g28-requiem-gr-inmemoria', 6367]})
o['parts'] = dict(o['parts']); o['parts']['gr'] = [{'id': 6258}]; o['parts']['tr'] = [{'id': 7107}]
o.pop('jgabc', None); o.pop('introit', None)
M['C114o'] = o
for s in D['sections']:
    if 'C114s' in s['items'] and 'C114o' not in s['items']: s['items'].insert(s['items'].index('C114s') + 1, 'C114o')
open(R + '/data/masses.js', 'w', encoding='utf8').write(h + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + t)
print('ok')
