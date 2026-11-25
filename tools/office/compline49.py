"""Compline as in the Completorii Libellus O.P. (Suarez, Rome 1949; media.churchmusicassociation.org/dominican/
completorium-1949-suarez.pdf, pp. 1-8, 18-21, 118-122): rewrites the shared Compline blocks of data/office/common.json,
which came from Divinum Officium's 1962 Dominican data. Run from the repo root: python3 tools/office/compline49.py"""
import json
P = 'data/office/common.json'
cm = json.load(open(P, encoding='utf-8'))
N = '<n>{}</n>'
CONF = ('<c>C</c>onfíteor Deo omnipoténti, et beátæ Maríæ semper Vírgini, et beáto Domínico Patri nostro, et ómnibus Sanctis, '
        'et {to}: quia peccávi nimis cogitatióne, locutióne, ópere et omissióne, mea culpa: precor {pr} oráre pro me.')
CONF_EN = ('<c>I</c> confess to almighty God, to blessed Mary ever Virgin, to blessed Dominic our Father, to all the Saints, '
           'and to {to}, that I have sinned exceedingly in thought, word, deed and omission, through my fault: I beseech {pr} to pray for me.')
ADJ = '\n'.join([
    '<r>℣.</r> Adjutórium nostrum in nómine Dómini.', '<r>℟.</r> Qui fecit cælum et terram.',
    N.format('All bow profoundly, or prostrate as the season requires, and say the <k>Pater noster</k> silently; then the Hebdomadarian:'),
    CONF.format(to='vobis, fratres', pr='vos'),
    N.format('Chorus:'),
    '<c>M</c>isereátur tui omnípotens Deus, et dimíttat tibi ómnia peccáta tua: líberet te ab omni malo, salvet, et confírmet in omni ópere bono, et perdúcat te ad vitam ætérnam.',
    N.format('Hebdomadarius:') + ' Amen.', N.format('Chorus:'),
    CONF.format(to='tibi, Pater', pr='te'),
    N.format('Hebdomadarius:'),
    '<c>M</c>isereátur vestri omnípotens Deus, et dimíttat vobis ómnia peccáta vestra: líberet vos ab omni malo, salvet, et confírmet in omni ópere bono, et perdúcat vos ad vitam ætérnam.',
    '<r>℟.</r> Amen.',
    N.format('All stand and turn to the altar:'),
    '<r>℣.</r> Convérte nos, Deus, salutáris noster.', '<r>℟.</r> Et avérte iram tuam a nobis.'])
ADJ_EN = '\n'.join([
    '<r>℣.</r> Our help is in the name of the Lord.', '<r>℟.</r> Who made heaven and earth.',
    N.format('The Our Father is said silently; then the Hebdomadarian:'),
    CONF_EN.format(to='you, brethren', pr='you'),
    N.format('Choir:'),
    '<c>M</c>ay almighty God have mercy upon thee, forgive thee all thy sins, deliver thee from all evil, save and confirm thee in every good work, and bring thee to life everlasting.',
    N.format('Hebdomadarian:') + ' Amen.', N.format('Choir:'),
    CONF_EN.format(to='thee, Father', pr='thee'),
    N.format('Hebdomadarian:'),
    '<c>M</c>ay almighty God have mercy upon you, forgive you all your sins, deliver you from all evil, save and confirm you in every good work, and bring you to life everlasting.',
    '<r>℟.</r> Amen.', N.format('All stand and turn to the altar:'),
    '<r>℣.</r> Convert us, O God our Saviour.', '<r>℟.</r> And turn away thy anger from us.'])
CAP = ('<h>Capitulum</h>\n<r>Jerem. 14</r>\n<c>T</c>u in nobis es, Dómine, et nomen sanctum tuum invocátum est super nos: '
       'ne derelínquas nos, Dómine, Deus noster.\n<r>℟.</r> Deo grátias.')
CAP_EN = ('<h>Chapter</h>\n<r>Jer. 14</r>\n<c>T</c>hou, O Lord, art among us, and thy holy name is called upon by us: forsake us not, '
          'O Lord our God.\n<r>℟.</r> Thanks be to God.')
RESP_NOTE = N.format('On a Double or Totum Duplex it is sung by two Friars standing in the middle of the choir; otherwise by the Friar appointed, in his stall.')
RESP = ('\n\n<h>Responsorium</h>\n' + RESP_NOTE + '\n<r>℟.br.</r> In manus tuas, Dómine, * Comméndo spíritum meum.\nIn manus.\n'
        '<r>℣.</r> Redemísti me, Dómine, Deus veritátis. * Comméndo.\n<r>℣.</r> Glória Patri, et Fílio, et Spirítui Sancto. In manus.')
RESP_P = ('\n\n<h>Responsorium</h>\n' + RESP_NOTE + '\n<r>℟.br.</r> In manus tuas, Dómine, comméndo spíritum meum, * Allelúia, allelúia.\nIn manus.\n'
          '<r>℣.</r> Redemísti me, Dómine, Deus veritátis. * Allelúia, allelúia.\n<r>℣.</r> Glória Patri, et Fílio, et Spirítui Sancto. In manus.')
RESP_EN = ('\n\n<h>Responsory</h>\n<r>℟.</r> Into thy hands, O Lord, * I commend my spirit. Into thy hands.\n'
           '<r>℣.</r> Thou hast redeemed us, O Lord, God of truth. * I commend.\n<r>℣.</r> Glory be to the Father, and to the Son, and to the Holy Ghost. Into thy hands.')
RESP_P_EN = ('\n\n<h>Responsory</h>\n<r>℟.</r> Into thy hands, O Lord, I commend my spirit, * Alleluia, alleluia. Into thy hands.\n'
             '<r>℣.</r> Thou hast redeemed us, O Lord, God of truth. * Alleluia, alleluia.\n<r>℣.</r> Glory be to the Father, and to the Son, and to the Holy Ghost. Into thy hands.')
VISITA = ('<c>V</c>ísita, quǽsumus, Dómine, habitatiónem istam, et omnes insídias inimíci ab ea longe repélle: et Ángeli tui sancti '
          'habitántes in ea nos in pace custódiant, et benedíctio tua sit super nos semper.\nPer Dóminum nostrum Jesum Christum Fílium tuum, '
          'qui tecum vivit et regnat in unitáte Spíritus Sancti Deus: per ómnia sǽcula sæculórum.\n<r>℟.</r> Amen.')
def oratio(v1, r1): return '<h>Oratio</h>\n<r>℣.</r> ' + v1 + '\n<r>℟.</r> ' + r1 + '\n<c>O</c>rémus.\n' + VISITA
BEN = ('<r>Benedictio.</r> ' + N.format('Given by the Prior, without chant (not on Maundy Thursday and Good Friday):') +
       ' Benedíctio Dei omnipoténtis Patris, et Fílii, ✠ et Spíritus Sancti descéndat super vos, et máneat semper.\n<r>℟.</r> Amen.\n' +
       N.format('In the absence of the Prior, the Subprior or the Hebdomadarian gives it, saying not super vos but super nos.'))
def concl(v1, r1): return '<h>Conclusio</h>\n<r>℣.</r> ' + v1 + '\n<r>℟.</r> ' + r1 + '\n<r>℣.</r> Benedicámus Dómino.\n<r>℟.</r> Deo grátias.\n' + BEN
def proc(tp):
    a = ' Allelúia.' if tp else ''
    return '\n'.join([
        '<h>Ad processionem in fine Completorii</h>',
        N.format('After the blessing the Salve Regina is begun by two cantors (on Doubles and Totum Duplex) or by one; at its beginning all '
                 'prostrate, or kneel in Paschaltide, until "Salve Regina" has been sung; then the procession goes into the church and the '
                 'Hebdomadarian sprinkles the brethren with holy water.'),
        '<r>Ant.</r> Salve, Regína, mater misericórdiæ: Vita, dulcédo et spes nostra, salve. Ad te clamámus éxsules fílii Hevæ. Ad te '
        'suspirámus, geméntes et flentes in hac lacrimárum valle. Eia ergo, advocáta nostra, illos tuos misericórdes óculos ad nos convérte. '
        'Et Jesum, benedíctum fructum ventris tui, nobis post hoc exsílium osténde. O clemens, O pia, O dulcis Virgo María.' + a,
        '<r>℣.</r> Dignáre me laudáre te, Virgo sacráta.' + a, '<r>℟.</r> Da mihi virtútem contra hostes tuos.' + a,
        '<c>O</c>rémus.',
        '<c>C</c>oncéde nos fámulos tuos, quǽsumus, Dómine Deus, perpétua mentis et córporis salúte gaudére: et gloriósa beátæ Maríæ semper '
        'Vírginis intercessióne a præsénti liberári tristítia, et ætérna pérfrui lætítia: Per Christum Dóminum nostrum.\n<r>℟.</r> Amen.',
        '', '<r>Ant.</r> O lumen Ecclésiæ, Doctor veritátis, Rosa patiéntiæ, Ebur castitátis, Aquam sapiéntiæ propinásti gratis: '
        'Prædicátor grátiæ, nos junge beátis.' + a,
        '<r>℣.</r> Ora pro nobis, beáte Pater Domínice.' + a, '<r>℟.</r> Ut digni efficiámur promissiónibus Christi.' + a,
        '<c>O</c>rémus.',
        '<c>C</c>oncéde, quǽsumus, omnípotens Deus: ut, qui peccatórum nostrórum póndere prémimur, beáti Domínici Confessóris tui, Patris '
        'nostri, patrocínio sublevémur: Per Christum Dóminum nostrum.\n<r>℟.</r> Amen.',
        '', '<r>℣.</r> Fidélium ánimæ per misericórdiam Dei requiéscant in pace.', '<r>℟.</r> Amen.',
        N.format('Then Pater noster and Credo in Deum, said silently.')])
def proc_en(tp):
    a = ' Alleluia.' if tp else ''
    return '\n'.join([
        '<h>Procession at the end of Compline</h>',
        '<r>Ant.</r> Hail, holy Queen, Mother of mercy, our life, our sweetness and our hope. To thee do we cry, poor banished children of Eve; '
        'to thee do we send up our sighs, mourning and weeping in this valley of tears. Turn then, most gracious advocate, thine eyes of mercy '
        'toward us; and after this our exile show unto us the blessed fruit of thy womb, Jesus. O clement, O loving, O sweet Virgin Mary.' + a,
        '<r>℣.</r> Make me worthy to praise thee, holy Virgin.' + a, '<r>℟.</r> Give me strength against thine enemies.' + a,
        '<c>L</c>et us pray.',
        '<c>G</c>rant, we beseech thee, O Lord God, that we thy servants may enjoy perpetual health of mind and body; and by the glorious '
        'intercession of blessed Mary ever Virgin, be delivered from present sorrow and enjoy eternal gladness. Through Christ our Lord.\n<r>℟.</r> Amen.',
        '', '<r>Ant.</r> O light of the Church, teacher of truth, rose of patience, ivory of chastity, freely thou didst pour forth the waters '
        'of wisdom: preacher of grace, unite us with the blessed.' + a,
        '<r>℣.</r> Pray for us, blessed Father Dominic.' + a, '<r>℟.</r> That we may be made worthy of the promises of Christ.' + a,
        '<c>L</c>et us pray.',
        '<c>G</c>rant, we beseech thee, almighty God, that we who are weighed down by the burden of our sins may be raised up by the patronage '
        'of blessed Dominic, thy Confessor, our Father. Through Christ our Lord.\n<r>℟.</r> Amen.',
        '', '<r>℣.</r> May the souls of the faithful, through the mercy of God, rest in peace.', '<r>℟.</r> Amen.'])
FIX = {
    '36189bfff7': ('<h>Incipit</h>\n' + N.format('The Friar appointed, in his stall, bowing to the Hebdomadarian:') +
                   '\n<r>℣.</r> Jube, domne, benedícere.\n<r>Benedictio.</r> Noctem quiétam et finem perféctum tríbuat nobis omnípotens et '
                   'miséricors Dóminus.\n<r>℟.</r> Amen.'),
    'bd62e26baf': ('<h>Start</h>\n<r>℣.</r> Pray, father, a blessing.\n<r>Benediction.</r> May the almighty and merciful Lord grant us a '
                   'quiet night and a perfect end.\n<r>℟.</r> Amen.'),
    '15ad8f25a1': ('<h>Lectio</h>\n<r>1 Petri 5</r>\n<c>F</c>ratres: Sóbrii estóte, et vigiláte: quia adversárius vester diábolus tamquam '
                   'leo rúgiens círcuit, quærens quem dévoret: cui resístite fortes in fide. Tu autem, Dómine, miserére nostri.\n<r>℟.</r> Deo grátias.'),
    'a0e021ed94': ('<h>Lesson</h>\n<r>1 Peter 5</r>\n<c>B</c>rethren: Be sober and watch: because your adversary the devil, as a roaring lion, '
                   'goeth about seeking whom he may devour. Whom resist ye, strong in faith. But thou, O Lord, have mercy upon us.\n<r>℟.</r> Thanks be to God.'),
    'd4cc46ba42': ADJ, '0516270dcd': ADJ, '90fd4abbec': ADJ_EN,
    'a167c9b1db': CAP + RESP, '95b92ddc86': CAP + RESP_P, '0f1b4d67c2': CAP, '12da9bdbf9': CAP_EN, '42f8ab9150': CAP_EN + RESP_EN,
    '9fbf8d309e': CAP_EN + RESP_P_EN,
    '690c2baea0': oratio('Dómine, exáudi oratiónem meam.', 'Et clamor meus ad te véniat.'),
    '0aa74f544e': oratio('Dóminus vobíscum.', 'Et cum spíritu tuo.'),
    'e5045c9ece': concl('Dómine, exáudi oratiónem meam.', 'Et clamor meus ad te véniat.'),
    'f58ba516a6': concl('Dóminus vobíscum.', 'Et cum spíritu tuo.'),
    '7f9023f752': ('<h>Conclusion</h>\n<r>℣.</r> O Lord, hear my prayer.\n<r>℟.</r> And let my cry come unto thee.\n<r>℣.</r> Let us bless the Lord.\n'
                   '<r>℟.</r> Thanks be to God.\n<r>Benediction.</r> May the blessing of almighty God, the Father, the Son, ✠ and the Holy Ghost, '
                   'come down upon you and remain for ever.\n<r>℟.</r> Amen.'),
    '8369a9dc5b': ('<h>Conclusion</h>\n<r>℣.</r> The Lord be with you.\n<r>℟.</r> And with thy spirit.\n<r>℣.</r> Let us bless the Lord.\n'
                   '<r>℟.</r> Thanks be to God.\n<r>Benediction.</r> May the blessing of almighty God, the Father, the Son, ✠ and the Holy Ghost, '
                   'come down upon you and remain for ever.\n<r>℟.</r> Amen.'),
    '54ef816215': proc(False), 'dd930c0583': proc(True), 'e2702ea181': proc_en(False), '8065596881': proc_en(True),
}
for k, v in FIX.items():
    assert k in cm, k
    cm[k] = v
for k in ('0b433afcc1',):     # Nunc dimittis antiphon: the book's punctuation
    cm[k] = cm[k].replace('custódi nos dormiéntes; ut', 'custódi nos dormiéntes: ut')
json.dump(cm, open(P, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(FIX), 'Compline blocks rewritten')
