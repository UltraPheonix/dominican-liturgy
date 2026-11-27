// Generate tools/proc/gabc/ex_*.gabc: the versicles and prayers of "In Processionibus extraordinariis",
// Processionarium O.P. (Cormier, Rome 1913), pp. 131-134 (pdf 147-150). Run: node tools/proc/gen_ex.js [--print]
// The book prints these texts without notes; each is set to the tone the book itself prints for it:
//  - Versicles: Regulae, Art. II § IV 3° (pp. 395-396), "Subscripto modo dicantur Versiculi ad Memorias et ante Laudes,
//    et in Processionibus, et quotiescumque dicitur V. a Sacerdote": tenor h (F clef on the 3rd line, as printed),
//    the syllables after the last accent fall to f (Di-gná-re me lau-dá-re te Vir-go sa-crá(h)-ta(f));
//    the place of the fall is marked in the text of pp. 131-134 by the flexa sign (here †).
//  - Prayers: Art. III § III (pp. 407-408), "Modus cantandi Orationes ad Horas, et quotiescumque aliquae aliae
//    Orationes quae non sunt de corpore Officii et Missae cantandae fuerint": Orémus h h f; tenor h; at the flexa sign
//    the syllables after the last accent fall to f (tristí(h)ti(f)a(f)); at the colon (metrum) the two syllables before
//    the last accent (three when they end a dactyl: Art. III § II 2°, p. 405) on g, the last of them on f, the accent
//    and the rest on h (salú(h)te(g) gau(f)dé(h)re(h); pér(h)fru(g)i(g) læ(f)tí(h)ti(h)a(h)); conclusion Per Christum
//    Dóminum nos(h)trum(f) (p. 408); R/. A(g)men(h) (p. 401 VII 2°; p. 408).
// The logic is copied from tools/proc/gen_tones.js (the established processions generator); that file is not changed.
// Every text below was read word by word from the scan, with the book's flexa signs (†) and colons; the site text
// items (proc_data.py, block "# extraordinariae (W-A2)") are checked against them.
'use strict';
const fs = require('fs'), path = require('path'), cp = require('child_process');
const H = __dirname, R = path.dirname(path.dirname(H));
global.window = {};
const P = require(R + '/js/psalm.js');
const OUT = H + '/gabc/';

// ---- versicles ending on a monosyllable, which the book marks with ':' instead of the flexa sign (pp. 132-134).
// The tone of p. 395 3° gives no example of such an ending. MONO selects the reading (decision of the coordinator):
//   'recto' : the whole line on the tenor, no fall;   'fall' : the last syllable (the monosyllable) alone falls to f.
const MONO = process.env.EX_MONO || 'pending';

const ANALYSE = t => P.analyse(t);
function lastAcc(s) { let a = -1; s.forEach((x, i) => { if (x.acc) a = i; }); return a < 0 ? Math.max(0, s.length - 2) : a; }
// a placeholder word Zq<n> stands for an alternative printed in the book in parentheses (vel Dux, vel Princeps):
// shown in italics, without notes (it replaces the word before it when sung, on the same tenor)
let ALT = [];
function render(s, notes) {
  return s.map((x, i) => {
    const m = /^Zq(\d)$/.exec(x.t);
    if (m) return ALT[+m[1]].split(' ').map(w => '<i>' + w + '</i>()').join(' ') + ' ';
    return x.t + '(' + notes[i] + ')' + (x.last ? ' ' : '');
  }).join('').trim();
}
function prep(t) { ALT = []; return t.replace(/\(([^)]*)\)/g, (m0, a) => { ALT.push(a); return 'Zq' + (ALT.length - 1); }); }
function recto(t) { const s = ANALYSE(prep(t)); return render(s, s.map(() => 'h')); }
function flex(t) { const s = ANALYSE(prep(t)), A = lastAcc(s); return render(s, s.map((x, i) => i > A ? 'f' : 'h')); }
function metrum(t) {
  const s = ANALYSE(prep(t)), A = lastAcc(s);
  let k = 2;
  if (A >= 4 && !s[A - 3].acc && s[A - 4].acc && s[A - 4].word === s[A - 3].word && s[A - 3].word === s[A - 2].word) k = 3;
  return render(s, s.map((x, i) => i >= A ? 'h' : (i === A - 1 ? 'f' : (i >= A - k ? 'g' : 'h'))));
}
// in a versicle the fall is on the syllables after the last accent of the word that carries the flexa sign; a word of
// one syllable at the very end has none (the flexa is then not printed: see MONO)
function vflex(t) {
  const s = P.analyse(prep(t)).map(x => Object.assign({}, x));
  // P.analyse moves the accent back for a final monosyllable (psalm rule): the versicle needs the word's own accent
  let A = -1; s.forEach((x, i) => { if (x.acc && !(i === s.length - 1 && x.mono)) A = i; });
  const w = s[s.length - 1].word, ws = s.map((x, i) => i).filter(i => s[i].word === w);
  const own = ws.find(i => s[i].acc); if (own !== undefined) A = own; else if (ws.length === 2) A = ws[0];
  return render(s, s.map((x, i) => i > A ? 'f' : 'h'));
}
function versLine(t) {
  // t: a versicle or response with internal flexa signs (†) and its end mark: '.' (the book's flexa sign) or ':'
  const end = t.slice(-1), body = t.slice(0, -1).trim();
  const parts = body.split(/\s*†\s*/);
  const g = parts.map((p, i) => {
    if (i < parts.length - 1) return vflex(p) + ' (;)';
    if (end === '.') return vflex(p + '.');
    if (end === ':') {
      if (MONO === 'recto') return recto(p + '.');
      if (MONO === 'fall') { const s = ANALYSE(p + '.'); return render(s, s.map((x, j) => j === s.length - 1 ? 'f' : 'h')); }
      throw new Error('MONO not decided: ' + t);
    }
    throw new Error('end mark ' + t);
  });
  return g.join(' ') + ' (::)';
}
function vr(v, r) { return '<sp>V/</sp>. ' + versLine(v) + ' <sp>R/</sp>. ' + versLine(r); }
// a prayer: segments ending in ':' (metrum) or '†' (flexa); the last segment, without mark, is the conclusion (flexa)
function prayer(src, o) {
  o = o || {};
  const segs = []; let m; const re = /[^:†]+[:†]?/g;
  while ((m = re.exec(src))) if (m[0].trim()) segs.push(m[0].trim());
  let g = o.oremus ? 'O(h)ré(h)mus.(f) (::) ' : '';
  segs.forEach((p, i) => {
    const mark = p.slice(-1), txt = p.replace(/\s*†$/, '').trim();
    const lastSeg = i === segs.length - 1;
    if (mark === '†') g += flex(txt) + ' (;) ';
    else if (mark === ':') g += metrum(txt) + (lastSeg ? ' (:)' : ' (:) ');
    else g += flex(txt) + ' (::) <sp>R/</sp>. A(g)men.(h) (::)';
  });
  return g.trim();
}
// The site text keeps the flexa sign where the book prints it inside a text ('†'); at the end of a versicle the
// book's flexa sign is written as a full stop; ':' as printed.

const VTONE = 'Versicle: Art. II § IV 3° (pp. 395-396: "Subscripto modo dicantur Versiculi ad Memorias et ante Laudes, et in Processionibus, et quotiescumque dicitur V. a Sacerdote"): tenor h, the syllables after the last accent of the versicle fall to f, as in the printed example Dignáre me laudáre te, Virgo sacráta. R. Da mihi virtútem contra hostes tuos (pp. 395-396). Proparoxytone endings: both syllables after the accent fall (geminatur nota re, p. 402). The fall is where pp. 131-134 print the flexa sign. F clef on the 3rd line as printed.';
const OTONE = 'Prayer: Art. III § III, pp. 407-408 ("Modus cantandi Orationes ad Horas, et quotiescumque aliquae aliae Orationes quae non sunt de corpore Officii et Missae cantandae fuerint"), applied after its printed example Concéde nos fámulos tuos (p. 407) and conclusions (p. 408): Orémus h h f, tenor h, at the flexa sign of the text the syllables after the last accent fall to f, at the colon (metrum) the two syllables before the last accent (three if they end a dactyl, Art. III § II 2°, p. 405) on g, the last of them on f, the accent and the rest on h, R. Amen g h (p. 401, VII 2°, p. 408). The inflexions fall where the book marks them on pp. 132-134. F clef on the 3rd line as printed.';
const MONONOTE = {
  recto: ' This line ends on a monosyllable and the book prints a colon, not the flexa sign, after it: sung on the tenor throughout without a fall (reading chosen by the site; the tone of p. 395 gives no example of this ending).',
  fall: ' This line ends on a monosyllable and the book prints a colon, not the flexa sign, after it: only the monosyllable falls to f (reading chosen by the site; the tone of p. 395 gives no example of this ending).',
};
function write(file, name, part, pageNote, tone, gabc) {
  const head = `name:${name};\noffice-part:${part};\nmode:;\nbook:Processionarium O.P. (Cormier), 1913, ${pageNote};\n` +
    `commentary:${tone.replace(/;/g, ',')};\ntranscriber:the tone printed in the Processionarium O.P. 1913 applied to this text for this site (the book prints this text without notes);\n%%\n`;
  fs.writeFileSync(OUT + file + '.gabc', head + gabc + '\n');
  console.log(file, gabc.length);
}

// ------------------------------------------------------------------ the texts, read from pp. 131-134
const VERSUS = [  // p. 131, after the Pater noster ("Et postea subjungat:"); every line ends with the flexa sign
  ['Et ne nos indúcas in tentatiónem.', 'Sed líbera nos a malo.'],
  ['Ora pro nobis, sancta Dei Génitrix.', 'Ut digni efficiámur promissiónibus Christi.'],
  ['Dómine, non secúndum peccáta nostra fácias nobis.', 'Neque secúndum iniquitátes nostras retríbuas nobis.'],
];
const CONCEDE = 'Concéde nos fámulos tuos, quǽsumus, Dómine Deus, perpétua mentis et córporis salúte gaudére: et gloriósa beátæ Maríæ semper Vírginis intercessióne a præsénti liberári tristítia † et ætérna pérfrui lætítia:';
const PARCE = 'Parce, Dómine, parce pópulo tuo: ut dignis flagellatiónibus castigátus † in tua miseratióne respíret:';
const PCD = ' Per Christum Dóminum nostrum.';
const OCC = [
  {id: 'ecclesia', name: 'Si fuerit tribulatio Ecclesiae', page: 'p. 132', la: 'Si fúerit tribulátio Ecclésiæ', v: 'Ádjuva nos, Deus salutáris noster.', r: 'Et propter glóriam nóminis tui, Dómine, líbera nos:',
   o: 'Ecclésiæ tuæ, quǽsumus, Dómine, preces placátus admítte: ut destrúctis adversitátibus et erróribus univérsis † secúra tibi sérviat libertáte:' + PCD},
  {id: 'pace', name: 'Pro pace', page: 'p. 132', la: 'Si Procéssio fiat pro pace', v: 'Fiat pax in virtúte tua.', r: 'Et abundántia in túrribus tuis.',
   o: 'Deus, a quo sancta desidéria, recta consília et justa sunt ópera † da servis tuis illam, quam mundus dare non potest, pacem: ut et corda nostra mandátis tuis dédita † et hóstium subláta formídine, témpora sint tua protectióne tranquílla:' + PCD},
  {id: 'pluvia', name: 'Pro petenda pluvia', page: 'p. 133', la: 'Si Procéssio fiat pro peténda plúvia', v: 'Óperi, Dómine, cælum núbibus.', r: 'Et para terræ plúviam.',
   o: 'Deus, in quo vívimus, et movémur, et sumus † plúviam nobis tríbue congruéntem: ut præséntibus auxíliis sufficiénter adjúti † sempitérna fiduciálius appetámus:' + PCD},
  {id: 'serenitate', name: 'Pro serenitate', page: 'p. 133', la: 'Si Procéssio fiat pro serenitáte', v: 'Adduxísti, Dómine, Spíritum tuum super terram.', r: 'Et prohíbitæ sunt plúviæ de cælo.',
   o: 'Ad te, Dómine, clamántes exáudi † et áëris serenitátem nobis tríbue supplicántibus: ut qui juste pro peccátis nostris afflígimur † misericórdia tua præveniénte, tuam cleméntiam sentiámus:' + PCD},
  {id: 'pestilentia', name: 'Tempore pestilentiae', page: 'p. 133', la: 'Si Procéssio fiat témpore pestiléntiæ', v: 'Exsúrge, Dómine, ádjuva nos:', r: 'Et líbera nos propter nomen tuum.',
   o: 'Deus, qui non mortem, sed pœniténtiam desíderas peccatórum † pópulum tuum, quǽsumus, ad te convérte propítius: ut dum tibi devótus exístit † iracúndiæ tuæ ab eo flagélla amóveas:' + PCD},
  {id: 'turcas', name: 'Contra Turcas et Haereticos', page: 'pp. 133-134', la: 'Si Procéssio fiat contra Turcas et Hæréticos', v: 'Mitte nobis Dómine auxílium de Sancto.', r: 'Et de Sion tuére nos:',
   o: 'Omnípotens sempitérne Deus, in cujus manu sunt ómnium potestátes et ómnium jura regnórum: réspice in auxílium Christianórum † ut gentes Turcárum atque Hæreticórum, quæ in sua feritáte confídunt, déxteræ tuæ poténtia conterántur:' + PCD},
  {id: 'papa', name: 'Pro summo Pontifice', page: 'p. 134', la: 'Si Procéssio fiat pro summo Pontífice', v: 'Orémus pro Dómino Papa.', r: 'Dóminus consérvet eum, et vivíficet eum, et beátum fáciat eum in terra † et non tradat eum in ánimam inimicórum ejus.',
   o: 'Deus, ómnium fidélium pastor et rector † fámulum tuum N. quem Pastórem Ecclésiæ tuæ præésse voluísti, propítius réspice: da ei, quǽsumus, verbo et exémplo quibus præest profícere † ut ad vitam una cum grege sibi crédito pervéniat sempitérnam:' + PCD},
  {id: 'rege', name: 'Pro Rege, Duce, vel Principe', page: 'p. 134', la: 'Si Procéssio fiat pro Rege, Duce, vel Príncipe', v: 'Salvum fac servum tuum.', r: 'Deus meus, sperántem in te:',
   o: 'Quǽsumus, omnípotens Deus: ut fámulus tuus N. Rex (vel Dux, vel Princeps) noster, qui tua miseratióne suscépit Regni (vel Ducátus, vel Principátus) gubernácula † virtútum étiam ómnium percípiat increménta: quibus decénter ornátus, et vitiórum monstra devitáre † et ad te, qui via, véritas et vita es, gratiósus váleat perveníre:' + PCD},
];

// the site text items, as they must stand in proc_data.py
const TXT = {
  versus: VERSUS.map(([v, r]) => '℣. ' + v + ' ℟. ' + r).join(' '),
  orationes: 'Orémus. ' + CONCEDE + ' Orátio. ' + PARCE,
};
OCC.forEach(o => { TXT[o.id] = '℣. ' + o.v + ' ℟. ' + o.r + ' Orátio. ' + o.o + ' ℟. Amen.'; });
if (process.argv.includes('--print')) { Object.entries(TXT).forEach(([k, v]) => console.log(k + '\t' + v)); process.exit(0); }

// check: every text set here stands, word for word, in a txt item of the section (the existing V/R item of p. 131
// is written there with '.' ends, as here)
const items = JSON.parse(cp.execFileSync('python3', ['-c',
  'import sys, json; sys.path.insert(0, sys.argv[1]); import proc_data as d; print(json.dumps([x for x in d.S["extraordinariae"]["items"] if x[0] == "txt"]))', H]).toString());
Object.entries(TXT).forEach(([k, v]) => { if (!items.some(x => x[1] === v)) { console.error('NOT IN proc_data (extraordinariae):', k, '\n  ', v); process.exitCode = 1; } });
if (process.exitCode) process.exit(1);

// ------------------------------------------------------------------ the files
write('ex_versus', 'In Processionibus extraordinariis: Et ne nos inducas; Ora pro nobis; Domine, non secundum (versus)', 'Versiculus',
  'p. 131 (text, each line ending with the flexa sign)', VTONE,
  '(f3) ' + VERSUS.map(([v, r]) => vr(v, r)).join(' '));
write('ex_orationes', 'In Processionibus extraordinariis: Oremus. Concede nos; Parce, Domine (orationes)', 'Oratio',
  'p. 132 (text: "Deinde, absque Dominus vobiscum, dicat sequentes Orationes praemisso Oremus", with the flexa sign after Orémus, tristítia and castigátus, and colons after gaudére, lætítia, tuo and respíret; neither prayer has its own conclusion: the rubric "Demum subjungat aliquam ex infra positis Orationibus ... eam terminando Per Christum Dominum nostrum" puts the one conclusion after the prayer of the occasion)', OTONE,
  '(f3) ' + prayer(CONCEDE, {oremus: true}) + ' ' + prayer(PARCE));
OCC.forEach(o => {
  const mono = /:$/.test(o.v) || /:$/.test(o.r);
  write('ex_' + o.id, 'In Processionibus extraordinariis: ' + o.name + ' (versus et oratio)', 'Versiculus, Oratio',
    o.page + ' (text, with the flexa signs and colons as printed; the prayer ends the series begun with Orémus. Concéde nos, p. 132, and is concluded Per Christum Dóminum nostrum as that rubric prescribes' +
    (['turcas', 'papa', 'rege'].includes(o.id) ? ', the book abbreviating it "Per Christum..."' : '') + ')',
    'V. and R.: ' + VTONE + (mono ? MONONOTE[MONO] : '') + ' Prayer (said without Orémus, which went before Concéde nos): ' + OTONE +
    (o.id === 'papa' ? ' In the R. the book prints a flexa sign also after "in terra": the fall is made there too, with a half bar.' : '') +
    (o.id === 'rege' ? ' The alternatives the book prints in parentheses (vel Dux, vel Princeps; vel Ducátus, vel Principátus) are shown in italics without notes: the one used is sung on the tenor in place of Rex, Regni.' : ''),
    '(f3) ' + vr(o.v, o.r) + ' ' + prayer(o.o));
});
