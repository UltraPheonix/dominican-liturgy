#!/usr/bin/env node
/* Good Friday 1939 (tools/hw39/Quad6f*.src): every sung oration, bidding and lesson set to the Dominican tones of the
   Processionarium O.P. (1913) through the engine in js/mtones.js (OPMassTones.orationProc / lessonProc).
   Writes gabc/op-hw-quad6f-NN.gabc and prints (or, with --write, inserts) the G: line that goes right before each
   T: block. The Latin words are the Missal's (read from the .src); the inflexion marks are the Triduum O.P. (1927),
   which prints these texts pointed for singing with the flex sign (here ‡) and colons (Proc. p. 405: "ad signum
   flexae (vel in Missali ad punctum cum virgula ;)"). --pointing=missal uses the Missal's own punctuation instead.

   node tools/hw39/gen_quad6f.js                 dry run: generate in memory, check words, print G: lines
   node tools/hw39/gen_quad6f.js --gabc          also write the gabc files
   node tools/hw39/gen_quad6f.js --gabc --write  also insert the G: lines into the .src (skips any already there)
   options: --pointing=missal|triduum (default triduum)  --questions (also the items still open, see Q below)
            --only=NN,NN  --compile (gregorio check of each written file, run from /tmp)
   Books: Missale O.P. 1939 /home/claude/dl/missal/M39.pdf (pp. 166-179); Triduum O.P. 1927 /tmp/dl/tri.pdf (pdf page =
   printed/2 + 3); Processionarium O.P. 1913 /home/claude/dl/proc/p.pdf (pdf = printed + 16). */
'use strict';
const fs = require('fs'), path = require('path'), cp = require('child_process');
const SITE = path.resolve(__dirname, '..', '..'), HW = __dirname;
globalThis.window = globalThis; globalThis.self = globalThis;
require(path.join(SITE, 'js/psalm.js')); require(path.join(SITE, 'js/mtones.js'));
const T = globalThis.OPMassTones;

const args = process.argv.slice(2), opt = k => args.some(a => a === '--' + k || a.startsWith('--' + k + '='));
const val = k => { const a = args.find(x => x.startsWith('--' + k + '=')); return a ? a.split('=')[1] : null; };
const POINTING = val('pointing') || 'triduum', ONLY = val('only') ? val('only').split(',').map(Number) : null;

const TONE_II = 'the Dominican tone for orations at Vespers, Lauds and Mass (Processionarium O.P. 1913, pp. 404-406)';
const TONE_III = 'the Dominican tone for orations at the Hours (Processionarium O.P. 1913, pp. 407-408)';
const TONE_IV = 'the Dominican tone for lessons and the prophecies at Mass (Processionarium O.P. 1913, pp. 408-413, ending by n. 11, p. 413)';
const STRIP_FLECT = /\s*:?\s*Orémus\.\s*Flectámus génua\.\s*Leváte\.\s*$/;

/* Each item: n, src file, find (start of its T: line), kind, opts for the engine, the Missal page, the Triduum page,
   the rubric that decides the tone (quoted from the Missal, with page), and the Triduum pointing (Missal words). */
const ITEMS = [
  {n: 1, file: 'Quad6f.src', find: '^HÆC dicit Dóminus', kind: 'lesson', name: 'Prophetia (Osee 6)', m: 166, tri: 179,
   tone: TONE_IV, rub: '"legatur ... a fratre ... Prophetia ex Osee Propheta sine ullo titulo" (Missal p. 166; the Prior meanwhile "legat submissa voce Prophetiam")',
   pt: 'Hæc dicit Dóminus. In tribulatióne sua : mane consúrgent ad me. Veníte, et revertámur ad Dóminum ‡ quia ipse cepit, et sanábit nos : percútiet, et curábit nos. Vivificábit nos post duos dies ‡ in die tértia suscitábit nos : et vivémus in conspéctu ejus, sciémus, sequemúrque ut cognoscámus Dóminum. Quasi dilúculum præparátus est egréssus ejus : et véniet quasi imber nobis temporáneus, et serótinus terræ. Quid fáciam tibi, Ephraim? Quid fáciam tibi, Juda? Misericórdia vestra quasi nubes matutína : et quasi ros mane pertránsiens. Propter hoc dolávi in prophétis : occídi eos in verbis oris mei. Et judícia tua quasi lux egrediéntur. Quia misericórdiam vólui, et non sacrifícium : et sciéntiam Dei plus quam holocáusta.'},
  {n: 2, file: 'Quad6f.src', find: '^DEUS, a quo et Judas', kind: 'oration', name: 'Oratio Deus, a quo et Judas', m: 166, tri: '181-182',
   tone: TONE_II, o: {tone: 'mass', oremus: false},
   rub: '"absque Dóminus vobíscum, et absque Flectámus génua, præmisso tantum Orémus, dicat Orationem" (Missal p. 166); Orémus is op13-quad6f-oremus',
   pt: 'Deus, a quo et Judas reátus sui pœnam, et confessiónis suæ latro prǽmium sumpsit, concéde nobis tuæ propitiatiónis efféctum : ut sicut in passióne sua Jesus Christus Dóminus noster divérsa utrísque íntulit stipéndia meritórum ‡ ita nobis, abláto vetustátis erróre, resurrectiónis suæ grátiam largiátur : Qui tecum vivit et regnat in unitáte Spíritus Sancti Deus : per ómnia sǽcula sæculórum.'},
  {n: 3, file: 'Quad6f.src', find: '^IN diébus illis : Dixit Dóminus ad Móysen', kind: 'lesson', name: 'Lectio (Exodus 12)', m: 167, tri: 182,
   tone: TONE_IV, rub: '"legatur sine titulo, et in tono Lectionis, sequens Lectio" (Missal p. 167)',
   pt: 'In diébus illis, dixit Dóminus ad Móysen, et Aaron : in terra Ægýpti. Mensis iste, vobis princípium ménsium : primus erit in ménsibus anni. Loquímini ad univérsum cœtum filiórum Israël : et dícite eis. Décima die mensis hujus : tollat unusquísque agnum per famílias et domos suas. Sin autem minor est númerus ut suffícere possit ad vescéndum agnum ‡ assúmet vicínum suum qui junctus est dómui suæ : juxta númerum animárum quæ suffícere possunt ad esum agni. Erit autem agnus absque mácula : másculus, annículus. Juxta quem ritum tollétis et hædum : et servábitis eum usque ad quartam décimam diem mensis hujus. Immolabítque eum univérsa multitúdo filiórum Israël ad vésperam ‡ et sument de sánguine ejus, ac ponent super utrúmque postem, et in superlimináribus domórum : in quibus cómedent illum. Et edent carnes nocte illa assas igni : et ázymos panes cum lactúcis agréstibus. Non comedétis ex eo crudum quid, nec coctum aqua : sed tantum assum igni. Caput cum pédibus ejus et intestínis vorábitis : nec remanébit quidquam ex eo usque mane. Si quid resíduum fúerit : igne comburétis. Sic autem comedétis illum. Renes vestros accingétis ‡ et calceaménta habébitis in pédibus, tenéntes báculos in mánibus : et comedétis festinánter. Est enim Phase : id est tránsitus Dómini.'},
];
// the nine solemn prayers, Missal pp. 171-174, Triduum pp. 190-194: "dicat sequentes Orationes, sine Dóminus vobíscum"
// (p. 171); the biddings: "In fine hujus Orationis non respondeatur Amen, sed statim Sacerdos subjungat Orémus, et
// Diaconus Flectámus génua. Leváte. Tunc Sacerdos prosequatur Orationem" (p. 171)
const SOLEMN = [
  ['^OREMUS, dilectíssimi nobis, pro Ecclésia', 171, 190, 'pro Ecclesia', 'Orémus, dilectíssimi nobis, pro Ecclésia sancta Dei : ut eam Deus et Dóminus noster pacificáre, adunáre, et custodíre dignétur toto orbe terrárum, subjíciens ei principátus et potestátes ‡ detque nobis, quiétam et tranquíllam vitam degéntibus, glorificáre Deum Patrem omnipoténtem :'],
  ['^OMNIPOTENS sempitérne Deus, qui glóriam', 171, 191, null, 'Omnípotens sempitérne Deus, qui glóriam tuam ómnibus in Christo Géntibus revelásti : custódi ópera misericórdiæ tuæ ‡ ut Ecclésia tua toto orbe diffúsa, stábili fide in confessióne tui nóminis persevéret : Per eúmdem Dóminum nostrum Jesum Christum Fílium tuum; qui tecum vivit et regnat in unitáte Spíritus Sancti Deus : per ómnia sǽcula sæculórum.'],
  ['^OREMUS et pro beatíssimo Papa', 172, 191, 'pro Papa', 'Orémus et pro beatíssimo Papa nostro N. ‡ ut Deus et Dóminus noster, qui elégit eum in órdine Episcopátus, salvum atque incólumem custódiat Ecclésiæ suæ sanctæ, ad regéndum pópulum sanctum Dei :'],
  ['^OMNIPOTENS sempitérne Deus, cujus judício', 172, 191, null, 'Omnípotens sempitérne Deus, cujus judício univérsa fundántur ‡ réspice propítius ad preces nostras : et eléctum nobis Antístitem tua pietáte consérva ‡ ut christiána plebs, quæ te gubernátur auctóre, sub tanto Pontífice, credulitátis suæ méritis augeátur : Per Dóminum nostrum.'],
  ['^OREMUS et pro ómnibus Epíscopis', 172, 191, 'pro ordinibus', 'Orémus et pro ómnibus Epíscopis, Presbýteris, Diacónibus, Subdiacónibus, Acólythis, Exorcístis, Lectóribus, Ostiáriis, Confessóribus, Virgínibus, Víduis, et pro omni pópulo sancto Dei :'],
  ['^OMNIPOTENS sempitérne Deus, cujus spíritu', 172, 191, null, 'Omnípotens sempitérne Deus, cujus spíritu totum corpus Ecclésiæ sanctificátur et régitur : exáudi nos pro univérsis Ordínibus supplicántes ‡ ut grátiæ tuæ múnere, ab ómnibus tibi grádibus fidéliter serviátur : Per Dóminum.'],
  ['^OREMUS et pro christianíssimo Imperatóre', 172, 192, 'pro Imperatore', 'Orémus et pro christianíssimo Imperatóre nostro N. ‡ ut Deus et Dóminus noster súbditas illi fáciat omnes bárbaras natiónes ad nostram perpétuam pacem :'],
  ['^OMNIPOTENS sempitérne Deus, in cujus manu', 172, 192, null, 'Omnípotens sempitérne Deus, in cujus manu sunt ómnium potestátes, et ómnium jura regnórum ‡ réspice ad Románum benígnus Impérium : ut gentes, quæ in sua feritáte confídunt ‡ poténtiæ tuæ déxtera comprimántur : Per Dóminum.'],
  ['^OREMUS et pro Catechúmenis', 172, 192, 'pro Catechumenis', 'Orémus et pro Catechúmenis nostris, ut Deus et Dóminus noster adapériat aures præcordiórum ipsórum, januámque misericórdiæ ‡ ut per lavácrum regeneratiónis accépta remissióne ómnium peccatórum, et ipsi inveniántur in Christo Jesu Dómino nostro :'],
  ['^OMNIPOTENS sempitérne Deus, qui Ecclésiam tuam nova', 172, 192, null, 'Omnípotens sempitérne Deus, qui Ecclésiam tuam nova semper prole fecúndas : auge fidem et intelléctum Catechúmenis nostris ‡ ut renáti fonte baptísmatis, adoptiónis tuæ fíliis aggregéntur : Per Dóminum.'],
  ['^OREMUS, dilectíssimi nobis, Deum Patrem', 172, 192, 'pro necessitatibus', 'Orémus, dilectíssimi nobis, Deum Patrem omnipoténtem : ut cunctis mundum purget erróribus, morbos áuferat, famem depéllat ‡ apériat cárceres, víncula dissólvat : peregrinántibus réditum, infirmántibus sanitátem ‡ navigántibus portum salútis indúlgeat :'],
  ['^OMNIPOTENS sempitérne Deus, mæstórum', 173, 192, null, 'Omnípotens sempitérne Deus, mæstórum consolátio, laborántium fortitúdo : pervéniant ad te preces de quacúmque tribulatióne clamántium ‡ ut omnes sibi in necessitátibus suis, misericórdiam tuam gáudeant adfuísse : Per Dóminum.'],
  ['^OREMUS et pro hæréticis', 173, 193, 'pro hæreticis', 'Orémus et pro hæréticis, et schismáticis, ut Deus et Dóminus noster éruat eos ab erróribus univérsis ‡ et ad Sanctam Matrem Ecclésiam Cathólicam atque Apostólicam revocáre dignétur :'],
  ['^OMNIPOTENS sempitérne Deus, qui salvas', 173, 193, null, 'Omnípotens sempitérne Deus, qui salvas omnes, et néminem vis períre ‡ réspice ad ánimas diabólica fraude decéptas : ut omni hærética pravitáte depósita, errántium corda resipíscant ‡ et ad veritátis tuæ rédeant unitátem : Per Dóminum.'],
  ['^OREMUS et pro pérfidis Judǽis', 173, 193, 'pro Judæis', 'Orémus et pro pérfidis Judǽis, ut Deus et Dóminus noster áuferat velámen de córdibus eórum ‡ ut et ipsi agnóscant Jesum Christum Dóminum nostrum :'],
  ['^OMNIPOTENS sempitérne Deus, qui étiam', 173, 193, null, 'Omnípotens sempitérne Deus, qui étiam Judáicam perfídiam a tua misericórdia non repéllis : exáudi preces nostras, quas pro illíus pópuli obcæcatióne deférimus ‡ ut ágnita veritátis tuæ luce, quæ Christus est, a suis ténebris eruántur : Per eúmdem Dóminum.'],
  ['^OREMUS et pro pagánis', 173, 193, 'pro paganis', 'Orémus et pro pagánis, ut Deus omnípotens áuferat iniquitátem a córdibus eórum ‡ ut relíctis idólis suis, convertántur ad Deum vivum et verum, et únicum Fílium ejus Jesum Christum Deum et Dóminum nostrum :'],
  ['^OMNIPOTENS sempitérne Deus, qui non mortem', 173, '193-194', null, 'Omnípotens sempitérne Deus, qui non mortem peccatórum, sed vitam semper inquíris ‡ súscipe propítius oratiónem nostram : et líbera eos ab idolórum cultúra ‡ et ággrega Ecclésiæ tuæ sanctæ, ad laudem et glóriam nóminis tui : Per Dóminum.'],
];
let k = 4, ord = 0;
SOLEMN.forEach(([find, m, tri, bid, pt]) => {
  const isBid = !!bid; if (isBid) ord++;
  ITEMS.push({n: k++, file: 'Quad6f_b.src', find, kind: 'oration', m, tri, tone: TONE_II, pt,
    name: isBid ? 'Oratio solemnis ' + ord + ' (' + bid + '), the bidding' : 'Oratio solemnis ' + ord + ' (Omnípotens sempitérne Deus)',
    o: isBid ? {tone: 'mass', oremus: false, amen: false} : {tone: 'mass', oremus: false},
    strip: isBid ? STRIP_FLECT : null,
    rub: isBid ? '"dicat sequentes Orationes, sine Dóminus vobíscum, hoc modo" and "In fine hujus Orationis non respondeatur Amen" (Missal p. 171); Orémus. Flectámus génua. Leváte. follow in op13-quad6f-flectamus (op13-quad6f-oremus for the 8th)'
      : '"Tunc Sacerdos prosequatur Orationem" (Missal p. 171)'});
});
ITEMS.push(
  {n: 22, file: 'Quad6f_c.src', find: '^RESPICE, quǽsumus Dómine', kind: 'oration', name: 'Oratio Réspice (after Super ómnia)', m: 177, tri: 205,
   tone: TONE_II, o: {tone: 'mass', oremus: false, amen: false, final: 'flex'}, q: 'Q2',
   rub: '"Antiphona finita ... dicat sequentem Orationem, sine Dóminus vobíscum et sine Orémus, Fratribus super formas prostratis" (Missal p. 177); Triduum p. 205 adds "sicut dicitur ad horas hujus diei" and ends it with the flex sign',
   pt: 'Réspice, quǽsumus Dómine, super hanc famíliam tuam ‡ pro qua Dóminus noster Jesus Christus non dubitávit mánibus tradi nocéntium : et Crucis subíre torméntum ‡'},
  {n: 23, file: 'Quad6f_d.src', find: '^LIBERA nos, quǽsumus', kind: 'oration', name: 'Oratio Líbera nos', m: '178-179', tri: 209,
   tone: TONE_II, o: {tone: 'mass', oremus: false, amen: false, noTerm: true}, q: 'Q3',
   rub: '"Subjungat Sacerdos submisse Amen. Et immediate prosequatur Orationem" (Missal p. 178); no tone printed; Per ómnia follows in op39-quad6f-peromnia (Suppl. p. 32)',
   pt: 'Líbera nos, quǽsumus, Dómine, ab ómnibus malis, prætéritis, præséntibus, et futúris : et intercedénte beáta et gloriósa semper Vírgine Dei Genitríce María, cum beátis Apóstolis tuis Petro et Paulo, atque Andréa, et ómnibus Sanctis, da propítius pacem in diébus nostris : ut ope misericórdiæ tuæ adjúti, et a peccáto simus semper líberi, et ab omni perturbatióne secúri. Per eúmdem Dóminum nostrum Jesum Christum Fílium tuum, qui tecum vivit et regnat in unitáte Spíritus Sancti Deus.'},
  {n: 24, file: 'Quad6f_d.src', find: 'Quod ore súmpsimus', kind: 'none', name: 'Quod ore súmpsimus', m: 179, tri: 210, q: 'Q4',
   rub: '"Peracta communione ... in medio altaris junctis manibus dicat" (Missal p. 179); the private ablution prayer of every Mass, no voice or tone given'},
);
const QUESTIONS = new Set(['Q3', 'Q4']);   // generated only with --questions until main answers

// ---------------------------------------------------------------- helpers
const words = (s, f) => s.replace(/[‡^{}℟.,;:?!()]/g, ' ').toLowerCase().split(/\s+/).filter(Boolean)
  .map((w, i) => f || i === 0 ? w.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/ǽ/g, 'æ') : w);
function srcLine(file, find) {
  const L = fs.readFileSync(path.join(HW, file), 'utf8').split('\n');
  const i = L.findIndex(l => l.startsWith('T: ' + find));
  if (i < 0) throw new Error(file + ': no T: line starting ' + find);
  return {lines: L, i, text: L[i].slice(3)};
}
function missalText(it, t) {
  t = t.replace(/^\^/, '').replace(/\s*\{℟\.\}\s*Amen\.\s*$/, '').trim();
  if (it.strip) t = t.replace(it.strip, '');
  return t.replace(/^([A-ZÆŒ]{2,})/, w => w.charAt(0) + w.slice(1).toLowerCase().replace('æ', 'æ'));
}
function compareWords(a, b) {
  const d = [];
  for (const f of [true, false]) {   // first the words, then their accents (the first word is in capitals in the Missal)
    const x = words(a, f), y = words(b, f);
    for (let i = 0; i < Math.max(x.length, y.length); i++) if (x[i] !== y[i]) { d.push((f ? 'word ' : 'accent ') + i + ': ' + x.slice(i, i + 3).join(' ') + ' | ' + y.slice(i, i + 3).join(' ')); break; }
    if (d.length) break;
  }
  return d;
}
function sing(it, text) {
  const t = text.replace(/\s*‡/g, ';'), o = Object.assign({}, it.o || {}, POINTING === 'triduum' ? {pointing: 'book'} : {});
  let g;
  if (it.o && it.o.final === 'flex' && POINTING === 'triduum') {
    // ends on the flexio, no conclusion (Triduum p. 205): the engine's own flexio/elevatio by the book's marks
    const P = T._proc, ms = t.match(/[^;:]+[;:]?/g).map(x => x.trim()).filter(Boolean);
    g = '(f3) ' + ms.map((m, i) => /;$/.test(m) ? P.flexO(m) + (i === ms.length - 1 ? ' (::)' : ' (,)') : P.elevO(m) + ' (;)').join(' ');
  } else if (it.kind === 'lesson') g = T.lessonProc(t, o);
  else g = T.orationProc(t, o);
  if (it.o && it.o.noTerm) g = g.replace(/ \(;\) per\(h\) óm\(i\).*$/, ' (::)');   // Per ómnia is a separate file
  return g;
}
function header(it, gid) {
  const pts = POINTING === 'triduum' ? 'inflexion marks (flex sign and colons) from Officium Hebdomadæ Sanctæ / Triduum O.P. (1927), p. ' + it.tri
    : 'punctuation of the Missal';
  return ['name:' + it.name + ';', 'office-part:' + (it.kind === 'lesson' ? 'Lectio' : 'Oratio') + ';',
    'book:Text Missale O.P. (1939), p. ' + it.m + '; ' + pts + ';',
    'commentary:Set to ' + it.tone + '. Rubric: ' + it.rub.replace(/;/g, ',') + ';',
    'transcriber:generated by tools/hw39/gen_quad6f.js with js/mtones.js OPMassTones (Good Friday task, 2026-11-27);', '%%'].join('\n');
}

// ---------------------------------------------------------------- run
const report = [];
for (const it of ITEMS) {
  if (ONLY && !ONLY.includes(it.n)) continue;
  const gid = 'op-hw-quad6f-' + String(it.n).padStart(2, '0');
  if (it.kind === 'none' || (QUESTIONS.has(it.q) && !opt('questions'))) { report.push(`#${it.n} ${it.name}: open (${it.q}), not generated`); continue; }
  const s = srcLine(it.file, it.find), mt = missalText(it, s.text);
  const text = POINTING === 'triduum' ? it.pt : mt;
  const diff = compareWords(mt, it.pt);
  const g = sing(it, text);
  const lab = it.name + ', ' + (it.kind === 'lesson' ? 'lesson tone' : 'oration tone') + ' (Processionarium O.P. 1913, pp. ' + (it.kind === 'lesson' ? '408-413' : '404-406') + ')';
  const G = 'G: ' + gid + ' | ' + lab;
  report.push(`#${it.n} ${it.file} -> ${gid}${diff.length ? '  WORD DIFF ' + diff.join('; ') : ''}\n   ${G}\n   ${g.slice(0, 160)}${g.length > 160 ? ' ...' : ''}`);
  if (opt('gabc')) {
    const f = path.join(SITE, 'gabc', gid + '.gabc');
    fs.writeFileSync(f, header(it, gid) + '\n' + g + '\n');
    if (opt('compile')) {
      try { cp.execSync('gregorio -o x.gtex ' + f, {cwd: '/tmp', stdio: 'pipe'}); report.push('   gregorio OK'); }
      catch (e) { report.push('   gregorio FAILED: ' + String(e.stderr || e.message).slice(0, 300)); }
    }
  }
  if (opt('write')) {
    // re-read right before the edit (another worker edits the same files) and insert only if absent
    const r = srcLine(it.file, it.find);
    if (r.lines.some(l => l.startsWith('G: ' + gid + ' '))) { report.push('   G: already in ' + it.file); continue; }
    r.lines.splice(r.i, 0, G);
    fs.writeFileSync(path.join(HW, it.file), r.lines.join('\n'));
    report.push('   inserted before line ' + (r.i + 1) + ' of ' + it.file);
  }
}
console.log('pointing: ' + POINTING + '\n' + report.join('\n'));
