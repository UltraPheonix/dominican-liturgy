"""Orations read from the Missale O.P. 1939 for Masses that had none: patched into data/orations.js (idempotent).
Also: Masses not of the pre-1955 rite are taken out of the lists (they stay in data, unused)."""
import json, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
PER = 'Per eúndem Dóminum nostrum Iesum Christum Fílium tuum: qui tecum vivit et regnat in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum.'
PER_EN = 'Through the same Jesus Christ, thy Son our Lord, Who liveth and reigneth with thee, in the unity of the Holy Ghost, God, world without end.'
ADD = {
 'C82s': {'src': 'Missale O.P. (1939), pp. 59*-60*, Missa privilegiata votiva SS. Rosarii B. Mariae V.; English our own',
  'or': ['Omnípotens et miséricors Deus, qui ab ætérno Unigénitum tibi coæquálem atque consubstantiálem Fílium secúndum carnem prædestinásti in Spíritu sanctificatiónis, Dóminum nostrum Iesum Christum; et sanctíssimam Vírginem Maríam tibi acceptíssimam in matrem eídem a sǽculo præelegísti: præsta, quǽsumus, ut amborum méritis, per sacra quíndecim mystéria sacratíssimi Rosárii complétis, ita in præsénti simus illis addícti; quaténus étiam in cæléstis vitæ glória fructus eórum in nobis iúgiter sentiámus: Per eúndem Dóminum nostrum Iesum Christum Fílium tuum: qui tecum vivit et regnat in unitáte eiúsdem Spíritus Sancti Deus, per ómnia sǽcula sæculórum.',
         'Almighty and merciful God, who from eternity didst predestine according to the flesh, in the Spirit of sanctification, thine only-begotten Son, coequal and consubstantial with thee, our Lord Jesus Christ, and didst choose from of old the most holy Virgin Mary, most acceptable to thee, to be his Mother: grant, we beseech thee, that by the merits of both, through the fifteen sacred mysteries of the most holy Rosary fulfilled, we may be so devoted to them in this present life that in the glory of the life of heaven we may also feel their fruit in us for ever. Through the same Jesus Christ, thy Son our Lord, Who liveth and reigneth with thee, in the unity of the same Holy Ghost, God, world without end.'],
  'se': ['Annue, quǽsumus, miséricors Deus, précibus nostris: ut quicúmque intra Rosárii Dei Genitrícis Maríæ, eius soli Fílio dicáti, ámbitum virtútis continémur, plena tibi atque perfécta córporis et ánimæ devotióne placeámus: ut, dum hæc præséntia vota réddimus, ad ætérna prǽmia, te adiuvánte, veníre mereámur. ' + PER,
         'Grant, we beseech thee, merciful God, to our prayers, that all of us who are held within the virtuous circle of the Rosary of Mary, Mother of God, dedicated to her only Son, may please thee with full and perfect devotion of body and soul; that, while we pay these present vows, we may with thy help come to the eternal rewards. ' + PER_EN],
  'pc': ['Veneránda sacratíssimi Rosárii mystéria in honórem Dei Genitrícis semper Vírginis Maríæ ab Ecclésia tua fidéli dicáta celebrántes, omnípotens Deus, benígno favóre proséquere: ut ómnibus in te sperántibus auxílii tui munus osténdas; et mysteriórum virtus, et votórum obtineátur efféctus: ' + PER,
         'Almighty God, as we celebrate the venerable mysteries of the most holy Rosary, dedicated by thy faithful Church to the honour of Mary, Mother of God and ever Virgin, follow us with thy kind favour: that thou mayest show the gift of thy help to all who hope in thee, and that the power of the mysteries and the effect of our prayers may be obtained. ' + PER_EN]},
}
TITLE = {'C82s': ('Missa votiva SS. Rosarii B. Mariæ V. (Salve radix sancta)', 'Votive Mass of the Most Holy Rosary')}
# not of the rite before 1955: St Joseph the Worker (1955), St Pius X (feast 1955), Blesseds beatified after 1955, and a duplicate of St Francis
DROP = ['S0501', 'S0903', 'G587', 'S1119b', 'S1209b', 'S0110b', 'S0401b', 'S0508b', 'S0516b', 'S0521b', 'S0620bx', 'S0704b', 'S0708b',
        'S0718b', 'S0727b', 'S0812b', 'S0813b', 'S0902b', 'S0906b', 'S0907b', 'S1006b', 'S1014b', 'S1019b', 'S1030bx']
def run():
    p = R + '/data/orations.js'; s = open(p, encoding='utf8').read(); head = s[:s.index('{')]
    O = json.loads(s[s.index('{'):].rstrip().rstrip(';')); O.update(ADD)
    open(p, 'w', encoding='utf8').write(head + json.dumps(O, ensure_ascii=False) + ';\n')
    F = R + '/data/masses.js'; s = open(F, encoding='utf8').read(); h, js = s.split('var DOMINICAN = ', 1); D = json.loads(js.rstrip().rstrip(';'))
    for k, (la, en) in TITLE.items(): D['masses'][k]['title'] = la; D['masses'][k]['en'] = en; D['masses'][k]['name_en'] = en
    for sec in D['sections']: sec['items'] = [k for k in sec['items'] if k not in DROP]
    open(F, 'w', encoding='utf8').write(h + 'var DOMINICAN = ' + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + ';\n')
    print(len(ADD), 'Masses given orations;', len(DROP), 'post-1955 Masses taken out of the lists')
if __name__ == '__main__': run()
