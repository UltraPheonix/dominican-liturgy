"""Build data/memoriae.js: the prayers of the Kalendarium's Memoriae (Missale O.P. 1939, printed in the Mass of their day as
"De S. N." or as a Memoria of its own), for their commemoration at Mass. Latin: memoriae_la.json (memoriae.py +
memoriae_clean.py); English: the site's own where the prayer is already on the site, else translated for this site (AI).
Run: python3 tools/orat39/memoriae.py && python3 tools/orat39/memoriae_clean.py && python3 tools/orat39/memoriae_build.py"""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(H))
LA = json.load(open(H + '/memoriae_la.json', encoding='utf8')); MAP = json.load(open(H + '/memoriae_enmap.json', encoding='utf8'))
RAW = json.load(open(H + '/memoriae_raw.json', encoding='utf8'))
EN = {}
for f in ('memoriae_en1', 'memoriae_en2', 'memoriae_en3'):
    ns = {}; exec(open(H + '/%s.py' % f, encoding='utf8').read(), ns); EN.update(ns['EN'])
EC = {'Per Dóminum nostrum Iesum Christum, Fílium tuum: qui tecum vivit et regnat in unitáte eiúsdem': 'Through our Lord Jesus Christ, Your Son, who lives and reigns with You in the unity of the same Holy Spirit, God, world without end.',
      'Per Dóminum': 'Through our Lord Jesus Christ, Your Son, who lives and reigns with You in the unity of the Holy Spirit, God, world without end.',
      'Per eúndem': 'Through the same Jesus Christ, Your Son, our Lord, who lives and reigns with You in the unity of the Holy Spirit, God, world without end.',
      'Qui vivis': 'Who live and reign with God the Father, in the unity of the Holy Spirit, God, world without end.',
      'Qui tecum': 'Who lives and reigns with You in the unity of the Holy Spirit, God, world without end.',
      'Dóminum nostrum': 'our Lord Jesus Christ, Your Son: who lives and reigns with You in the unity of the Holy Spirit, God, world without end.'}
def en_concl(la):
    for k, v in EC.items():
        if k in la: return v
    return EC['Per Dóminum']
out = {}
for k, v in LA.items():
    md, title = k.split('|', 1)
    e = out.setdefault(k, {'md': md, 'la': title})
    for f, la in v.items():
        m = MAP.get(k + '|' + f, {})
        if 'en_full' in m: en = m['en_full']
        elif m.get('n') in EN: en = EN[m['n']].rstrip(' .;:,') + '; ' + en_concl(la)[0].lower() + en_concl(la)[1:]
        else: en = ''
        e[f] = [la, en]
    e['src'] = 'Missale O.P. (1939), in the Mass of %s/%s; English translated for this site (AI) where not already on the site' % (md[2:], md[:2])
# the octave of St John Baptist: "Et fiat Memoria Octavae S. Joannis Bapt. cum Orationibus ut in Festo, p. 474" (1 Jul.)
O = json.loads(open(R + '/data/orations.js', encoding='utf8').read().split('=', 1)[1].strip().rstrip(';'))
k = '0701|Octava S. Joannis Baptistæ'
out[k] = {'md': '0701', 'la': 'Octava S. Joannis Baptistæ', 'or': O['S0624']['or'], 'se': O['S0624']['se'], 'pc': O['S0624']['pc'],
          'src': 'Missale O.P. (1939), 1 Jul.: cum Orationibus ut in Festo (p. 474)'}
PD = 'Per Dóminum nostrum Iesum Christum, Fílium tuum: qui tecum vivit et regnat in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum.'
EPD = 'through our Lord Jesus Christ, Your Son, who lives and reigns with You in the unity of the Holy Spirit, God, world without end.'
# the commemoration of St Anastasia at the second Mass of Christmas, "Memoria de S. Anastasia" (Missal pp. 21-22)
out['1225|S. Anastasiæ Mart.'] = {'md': '1225', 'la': 'S. Anastasiæ Mart.',
  'or': ['Da, quǽsumus, omnípotens Deus: ut qui beátæ Anastásiæ Mártyris tuæ solémnia cólimus; eius apud te patrocínia sentiámus: ' + PD,
         'Grant, we beseech You, almighty God, that we who keep the feast of blessed Anastasia, Your Martyr, may feel her patronage with You; ' + EPD],
  'se': ['Accipe, quǽsumus Dómine, múnera dignánter obláta: et beátæ Anastásiæ Mártyris tuæ suffragántibus méritis, ad nostræ salútis auxílium proveníre concéde. ' + PD,
         'Receive, we beseech You, O Lord, the gifts we offer, and grant that, through the merits of blessed Anastasia, Your Martyr, they may avail for our salvation; ' + EPD],
  'pc': ['Satiásti, Dómine, famíliam tuam munéribus sacris: eius, quǽsumus, interventióne nos réfove; cuius solémnia celebrámus: ' + PD,
         'You have filled Your household, O Lord, with holy gifts; refresh us ever, we beseech You, by the intercession of her whose feast we keep; ' + EPD],
  'src': 'Missale O.P. (1939), Christmas, second Mass: Memoria de S. Anastasia (pp. 21-22); English translated for this site (AI)'}
# Ember Wednesday of Advent commemorated in the Mass of a feast: "Oratio sequens non est dicenda pro Memoria de Adventu in Missa
# festi ... sed dici debet Oratio subsequens, Festina" (Missal, Feria IV Quatuor Temporum Adventus)
out['Adv3w|Feria IV Quatuor Temporum Adventus'] = {'md': '1200', 'la': 'Feria IV Quatuor Temporum Adventus',
  'or': ['Festína, quǽsumus Dómine, ne tardáveris: et auxílium nobis supérnæ virtútis impénde; ut advéntus tui consolatiónibus sublevéntur, qui in tua pietáte confídunt: Qui vivis et regnas cum Deo Patre, in unitáte Spíritus Sancti, Deus, per ómnia sǽcula sæculórum.',
         'Make haste, we beseech You, O Lord, do not delay, and grant us the help of Your heavenly power; that they who trust in Your goodness may be relieved by the consolations of Your coming; who live and reign with God the Father, in the unity of the Holy Spirit, God, world without end.'],
  'se': O['Adv3w']['se'], 'pc': O['Adv3w']['pc'],
  'src': 'Missale O.P. (1939), Feria IV Quatuor Temporum Adventus: the Oratio Festina for its commemoration in the Mass of a feast'}
js = 'window.MEMORIAE = ' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n'
open(R + '/data/memoriae.js', 'w', encoding='utf8').write(js)
print(len(out), 'Memoriae;', sum(1 for v in out.values() for f in ('or', 'se', 'pc') if f in v and v[f][1]), 'prayers with English;', len(js), 'bytes')
