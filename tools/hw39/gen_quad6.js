// Holy Week 1939, Palm Sunday to Wednesday (worker W-B2): the celebrant's and ministers' sung texts set to the
// Dominican tones printed in the Processionarium O.P. (1913), Regulae cantus, Art. III, via Lead B's tone engine
// (js/mtones.js, OPMassTones.*Proc). Text: exactly the Missale O.P. (1939) words as transcribed in tools/hw39/*.src.
//
//   node tools/hw39/gen_quad6.js [quad6|quad6m|quad6t|quad6w ...] [--write] [--insert]
//     (no flag)  dry run: print each item, its tone, the G: line and where it goes
//     --write    write gabc/op-hw-<day>-<n>.gabc (header cites book, page, rubric and tone)
//     --insert   insert the G: lines into the .src (the file is re-read right before each insertion; an item
//                whose G: line is already there is skipped; only G: lines are added, nothing else is changed)
//
// Tones (Processionarium O.P. 1913, pdf page = printed + 16):
//   II  "Modus cantandi Orationes ad Vesperas, Laudes et Missam", pp. 404-406       -> orationProc tone 'mass'
//   III "Modus cantandi Orationes ad Horas, et quotiescumque aliquae aliae Orationes quae non sunt de corpore
//        Officii et Missae cantandae fuerint", pp. 407-408                          -> orationProc tone 'hours'
//   IV  "Modus cantandi Benedictiones et Lectiones ... Prophetias in Missa", pp. 408-413  -> lessonProc
//   V   "Modus legendi Epistolam", pp. 414-420                                      -> epistleProc
//   VI  "Modus legendi Evangelium", pp. 424-430                                     -> gospelProc
// Orations: Missale O.P. 1939, Rubr. gen. XI.1 (p. 52): "Quotiescumque autem dicuntur plures Orationes, prima
// tantum, et ultima cum sua peroratione, seu conclusione terminantur; et ante primam, et secundam Orationem tantum
// dicitur Oremus : et ante primam dicitur etiam Dominus vobiscum, nisi aliter notetur". The abbreviated conclusions
// are written out here in the words of the Ordo Missae (Missale p. 30: "Per eumdem Dominum nostrum Jesum Christum
// Filium tuum, qui tecum vivit et regnat in unitate Spiritus Sancti Deus, per omnia saecula saeculorum"), pointed
// as the Processionarium p. 406 sings them ("Fílium tuum ; qui tecum ... Spíritus sancti Deus : per ómnia").
'use strict';
const fs = require('fs'), path = require('path');
const SITE = path.resolve(__dirname, '..', '..');
globalThis.window = globalThis;
require(path.join(SITE, 'js/psalm.js'));
require(path.join(SITE, 'js/mtones.js'));
const T = globalThis.OPMassTones;

const PROC = 'Processionarium O.P. (1913)';
const TONE = {
  II: {tone: 'mass', name: 'the Dominican tone of the Orations at Vespers, Lauds and Mass', pp: 'pp. 404-406'},
  III: {tone: 'hours', name: 'the Dominican tone of the Orations at the Hours', pp: 'pp. 407-408'},
  IV: {name: 'the Dominican tone of the Lessons and Prophecies at Mass', pp: 'pp. 408-413'},
  V: {name: 'the Dominican Epistle tone', pp: 'pp. 414-420'},
  VI: {name: 'the Dominican Gospel tone', pp: 'pp. 424-430'}
};

// the first word of a block, printed in capitals without accents in the Missal
const CAPS = {OMNIPOTENS: 'Omnípotens', PER: 'Per', FRATRES: 'Fratres', IN: 'In', DA: 'Da', ANTE: 'Ante',
  PRǼBEANT: 'Prǽbeant', ADJUVA: 'Ádjuva', SANCTIFICATIONIBUS: 'Sanctificatiónibus', TUA: 'Tua', PRÆSTA: 'Præsta',
  HÆC: 'Hæc', DEUS: 'Deus', LARGIRE: 'Largíre', RESPICE: 'Réspice', 'A CUNCTIS': 'A cunctis', DIVINA: 'Divína',
  MUNDET: 'Mundet'};

// conclusions written out (Rubr. gen. XI.2, p. 52: "si in Oratione facta fuerit mentio Spiritus Sancti, terminatur
// in unitate ejusdem Spiritus Sancti")
function conclusion(c, body) {
  const ej = /Spírit|Spirit/.test(body) ? 'ejúsdem ' : '';
  const U = 'in unitáte ' + ej + 'Spíritus Sancti Deus: per ómnia sǽcula sæculórum.';
  c = c.trim().replace(/\.$/, '');
  if (/^Per Dóminum( nostrum)?$/.test(c)) return 'Per Dóminum nostrum Jesum Christum Fílium tuum; qui tecum vivit et regnat ' + U;
  if (/^Per eúmdem( Dóminum( nostrum)?)?$/.test(c)) return 'Per eúmdem Dóminum nostrum Jesum Christum Fílium tuum; qui tecum vivit et regnat ' + U;
  if (/^Qui tecum vivit$/.test(c)) return 'Qui tecum vivit et regnat ' + U;
  if (/^Per eúmdem Christum Dóminum nostrum$/.test(c)) return c + '.';   // short conclusion, printed in full
  throw new Error('conclusion not known: ' + c);
}
const CONCL = /\s*:?\s*\b(Per Dóminum( nostrum)?|Per eúmdem( Dóminum( nostrum)?)?|Qui tecum vivit|Per eúmdem Christum Dóminum nostrum)\.?\s*(\{℟\.\}\s*Amen\.)?$/;

// the Latin of a T: line as sung: markup out, capitals of the first word in their accented form; j kept here
// (the engine's Hebrew list knows Jesus/Jesu), turned into i only in the gabc (site style, tools/hw39/build.py)
function clean(s) {
  s = s.replace(/^\^/, '');
  s = s.replace(/\{Hic genuflectitur :\}\s*UT IN NOMINE JESU OMNE GENU FLECTATUR/, 'ut in nómine Jesu omne genu flectátur');
  s = s.replace(/\s*\{✠\}\s*/g, '');          // bene ✠ dícas: one word, the cross is the priest's sign, not sung
  s = s.replace(/\{✠ ([A-Z])\}/g, '$1').replace(/\{([A-ZÆ])\}/g, '$1');
  s = s.replace(/\s*\{c\. [^}]*\}\s*$/, '');
  s = s.replace(/\s*\{℟\.\}\s*Amen\.$/, '');   // the printed ℟. Amen: the engine sings it (p. 406, p. 408)    // chapter reference after a title
  const m = /^(A CUNCTIS|[A-ZÆǼ]+)\b/.exec(s);
  if (m && m[1].length > 1 && m[1] === m[1].toUpperCase()) {
    if (!CAPS[m[1]]) throw new Error('capitals not known: ' + m[1]);
    s = CAPS[m[1]] + s.slice(m[1].length);
  }
  if (/[{}^]/.test(s)) throw new Error('markup left: ' + s.slice(0, 80));
  return s.trim();
}
const toI = g => g.replace(/j/g, 'i').replace(/J/g, 'I');

// ---------------------------------------------------------------------------------------------- the items
// find: the T: line whose Latin is sung (a regexp on the line); title: the T: line of the announcement (readings);
// before: the line before which the G: line goes (default: the title line, else the found line); conc: 'keep'
// (default: the conclusion printed or abbreviated is written out), 'drop' (2nd of three prayers: no conclusion)
const DAYS = {
  quad6: {name: 'Dominica in Ramis Palmarum', items: [
    {n: 1, file: 'Quad6', find: /^T: \^OMNIPOTENS sempitérne Redémptor/, tone: 'III', opts: {dv: false, oremus: false, pointing: 'book'}, special: 'palmBlessing',
      what: 'Benedictio ramorum: Omnípotens sempitérne Redémptor', page: 'pp. 137-138',
      rubric: 'Missale p. 137: "Prior ... ramos arborum ... benedicat eo modo, quo dicuntur Orationes ad Horas." Proc. p. 20: "benedicat eo tono, quo dicuntur Orationes ad Horas"; Proc. pp. 20-21 print this prayer pointed for the tone (the flexa sign where the Missal has a semicolon, and at voluísti ‡ where it has a full stop), ending "per ómnia sǽcula sæculórum ‡. ℟. Amen."',
      label: 'Omnípotens sempitérne Redémptor · in the tone of the Orations at the Hours (Processionarium O.P. 1913, pp. 20-21, 407-408)'},
    {n: 2, file: 'Quad6', find: /^T: \^IN illo témpore : Cum appropinquásset/, tone: 'VI', opts: {},
      what: 'Evangelium Cum appropinquásset (Matth. 21), the body (Dóminus vobíscum and Sequéntia: op13-palm-evangelium-dv, Proc. p. 23)', page: 'p. 139',
      rubric: 'Missale p. 139: "Distributis ramis, Diaconus, benedictione accepta a Priore, legat Evangelium Cum appropinquásset in loco, ubi profestis diebus Evangelium consuevit legi"; Proc. pp. 22-23: "Diaconus, benedictione accepta, cantet Evangelium Cum appropinquásset. in loco ubi profestis diebus Evangelium cantari consuevit."',
      label: 'In illo témpore: Cum appropinquásset · in the Gospel tone (Processionarium O.P. 1913, pp. 23-24, 424-430)'},
    {n: 3, file: 'Quad6_proc', find: /^T: \^OMNIPOTENS sempitérne Deus, qui humáno/, before: /^T: Orémus\.$/, tone: 'III', opts: {dv: false, oremus: true, pointing: 'book'},
      what: 'Oratio at the end of the procession: Orémus. Omnípotens sempitérne Deus, qui humáno géneri', page: 'p. 141 (Proc. p. 33)',
      rubric: 'Proc. p. 33 (Missale p. 141): "Deinde Prior absque Dóminus vobíscum, præmisso Orémus, dicat Orationem eo modo quo dicitur ad Horas"; Proc. p. 33 prints it pointed: "Orémus ‡ ... fecísti ‡ concéde propítius : ut ... documénta ‡ et Resurrectiónis consórtia mereámur : Per eúmdem Christum Dóminum nostrum ‡ ℟. Amen."',
      label: 'Orémus · Omnípotens sempitérne Deus · in the tone of the Orations at the Hours (Processionarium O.P. 1913, pp. 33, 407-408)'},
    {n: 4, file: 'Quad6', find: /^T: \^OMNIPOTENS sempitérne Deus, qui humáno/, tone: 'II', opts: {dv: true, oremus: true},
      what: 'Missa: Oratio (Collect), with Dóminus vobíscum and Orémus', page: 'p. 139',
      rubric: 'Missale p. 139: "Hæc Oratio sola dicatur." Rubr. gen. XI.1, p. 52: "ante primam dicitur etiam Dominus vobiscum"; Proc. p. 404: "Modus cantandi Orationes ad Vesperas, Laudes et Missam".',
      label: 'Dóminus vobíscum · Orémus · Oratio · in the Mass tone of the Orations (Processionarium O.P. 1913, pp. 404-406)'},
    {n: 5, file: 'Quad6', find: /^T: \^FRATRES : Hoc enim sentíte/, title: /^T: \{L\}éctio Epístolæ beáti Pauli Apóstoli ad Philippénses/, tone: 'V', opts: {},
      what: 'Epistola Phil. 2, with its title', page: 'pp. 139-140',
      rubric: 'Proc. p. 414, V: "Modus legendi Epistolam in his quæ infra ponuntur et in similibus" (the example begins "Léctio Epístolæ beáti Pauli apóstoli :"). The Missal\'s rubric inside the text ("Hic genuflectitur") is not sung.',
      label: 'Léctio Epístolæ beáti Pauli Apóstoli ad Philippénses · in the Epistle tone (Processionarium O.P. 1913, pp. 414-420)'},
    {n: 6, file: 'Quad6', find: /^T: \^PER hujus, Dómine, operatiónem/, tone: 'II', opts: {dv: false, oremus: false},
      what: 'Missa: Postcommunio (Dóminus vobíscum and Orémus are sung in the Order of Mass, X: post)', page: 'p. 146',
      rubric: 'Proc. p. 404, II: "Modus cantandi Orationes ad Vesperas, Laudes et Missam". One Postcommunion only (the Collect: "Hæc Oratio sola dicatur").',
      label: 'Postcommunio · in the Mass tone of the Orations (Processionarium O.P. 1913, pp. 404-406)'}
  ]},
  quad6m: {name: 'Feria II Hebdomadæ Sanctæ', items: [
    {n: 1, file: 'Quad6m', kind: 'dv', before: /^G: op-m39-flectamus/, tone: 'II', opts: {dv: true, oremus: true},
      what: 'Dóminus vobíscum. Orémus. before Flectámus génua (Flectámus already notated: op-m39-flectamus)', page: 'p. 146',
      rubric: 'Missale p. 146 prints "Dóminus vobíscum. Orémus. Flectámus génua. Leváte."; Proc. pp. 404-405: "Ante Orationem: Dóminus vobíscum ... Orémus. In Missis de Feria, a Feria IV Cinerum usque ad Cenam Domini exclusive, dicto Orémus, additur: Flectámus génua. Leváte."',
      label: 'Dóminus vobíscum · Orémus (Processionarium O.P. 1913, pp. 404-405)', shared: ['Quad6t']},
    {n: 2, file: 'Quad6m', find: /^T: \^DA, quǽsumus omnípotens Deus/, tone: 'II', opts: {dv: false, oremus: false},
      what: 'Oratio (Collect)', page: 'p. 146', rubric: 'Proc. p. 404, II (Orationes ad Missam); first of three prayers: with its conclusion (Rubr. gen. XI.1, p. 52).',
      label: 'Oratio · in the Mass tone of the Orations (Processionarium O.P. 1913, pp. 404-406)'},
    {n: 3, file: 'lent_or', find: /^T: \^DEUS, qui caritátis dona/, tone: 'II', opts: {dv: false, oremus: true, amen: false}, conc: 'drop',
      what: 'Secunda Oratio Deus, qui caritátis (Mon-Wed: lent_or.src is shared)', page: 'p. 63',
      rubric: 'Missale p. 146: "Secunda et tertia Oratio, pag. 63"; Rubr. gen. XI.1, p. 52: Orémus before the second; only the first and the last keep their conclusion.',
      label: 'Orémus · Secunda Oratio · in the Mass tone of the Orations (Processionarium O.P. 1913, pp. 404-406)'},
    {n: 4, file: 'lent_or', find: /^T: \^A CUNCTIS nos, quǽsumus Dómine/, tone: 'II', opts: {dv: false, oremus: false},
      what: 'Tertia Oratio A cunctis, with the conclusion (lent_or.src, shared Mon-Wed)', page: 'p. 63',
      rubric: 'Rubr. gen. XI.1, p. 52: the last prayer keeps its conclusion; no Orémus before the third.',
      label: 'Tertia Oratio · in the Mass tone of the Orations (Processionarium O.P. 1913, pp. 404-406)'},
    {n: 5, file: 'Quad6m', find: /^T: \^IN diébus illis : Dixit Isaías : Dóminus Deus apéruit/, title: /^T: \{L\}éctio Isaíæ Prophétæ\. \{c\. 50\}/, tone: 'V', opts: {},
      what: 'Lectio Is. 50 in the place of the Epistle, with its title', page: 'p. 147',
      rubric: 'In the place of the Epistle (after the Collects, before the Gradual), sung by the Subdeacon: Proc. p. 414, V "Modus legendi Epistolam in his quæ infra ponuntur et in similibus" (tools/handoff/hw_tones.md §4).',
      label: 'Léctio Isaíæ Prophétæ · in the Epistle tone (Processionarium O.P. 1913, pp. 414-420)'},
    {n: 6, file: 'Quad6m', find: /^T: \^ANTE sex dies Paschæ/, title: /^T: \{✠ S\}equéntia sancti Evangélii secúndum Joánnem/, tone: 'VI', opts: {book: 'Joannes', dv: true},
      what: 'Evangelium Joann. 12, with Dóminus vobíscum and Sequéntia', page: 'p. 147',
      rubric: 'Proc. p. 424, VI: "Modus legendi Evangelium in his quæ infra ponuntur et in similibus"; Initia: "Dóminus vobíscum ... Sequéntia sancti Evangélii ... ℟. Glória tibi, Dómine."',
      label: 'Dóminus vobíscum · Sequéntia sancti Evangélii secúndum Joánnem · in the Gospel tone (Processionarium O.P. 1913, pp. 424-430)'},
    {n: 7, file: 'Quad6m', find: /^T: \^PRǼBEANT nobis, Dómine/, tone: 'II', opts: {dv: false, oremus: false},
      what: 'Postcommunio (Dóminus vobíscum and Orémus: Order of Mass, X: post)', page: 'p. 148',
      rubric: 'Proc. p. 404, II; first of three: with its conclusion (Rubr. gen. XI.1, p. 52).',
      label: 'Postcommunio · in the Mass tone of the Orations (Processionarium O.P. 1913, pp. 404-406)'},
    {n: 8, file: 'lent_pc', find: /^T: \^DIVINA libántes mystéria/, tone: 'II', opts: {dv: false, oremus: true, amen: false}, conc: 'drop',
      what: 'Secunda Postcommunio Divína libántes (lent_pc.src, shared Mon-Wed)', page: 'p. 65',
      rubric: 'Missale p. 148: "Secunda et tertia Postcommunio, pag. 65"; Rubr. gen. XI.1, p. 52: Orémus before the second; no conclusion on it.',
      label: 'Orémus · Secunda Postcommunio · in the Mass tone of the Orations (Processionarium O.P. 1913, pp. 404-406)'},
    {n: 9, file: 'lent_pc', find: /^T: \^MUNDET et múniat nos/, tone: 'II', opts: {dv: false, oremus: false},
      what: 'Tertia Postcommunio Mundet et múniat, with the conclusion (lent_pc.src, shared Mon-Wed)', page: 'p. 65',
      rubric: 'Rubr. gen. XI.1, p. 52: the last prayer keeps its conclusion.',
      label: 'Tertia Postcommunio · in the Mass tone of the Orations (Processionarium O.P. 1913, pp. 404-406)'},
    {n: 10, file: 'Quad6m', kind: 'existing', id: 'op13-quad6f-oremus', before: /^G: op-m39-humiliate/,
      what: 'Orémus before Humiliáte (existing gabc, Proc. p. 405)', page: 'p. 148',
      label: 'Orémus (Processionarium O.P. 1913, p. 405)'},
    {n: 11, file: 'Quad6m', find: /^T: \^ADJUVA nos Deus salutáris noster/, tone: 'II', opts: {dv: false, oremus: false},
      what: 'Oratio super populum (after Orémus. Humiliáte cápita vestra Deo.)', page: 'p. 148',
      rubric: 'Proc. p. 405: "Ante ultimam Postcommunionem, in prædictis Missis, dicatur: Humiliáte cápita vestra Deo."; tone II.',
      label: 'Oratio super populum · in the Mass tone of the Orations (Processionarium O.P. 1913, pp. 404-406)'}
  ]},
  quad6t: {name: 'Feria III Hebdomadæ Sanctæ', items: [
    {n: 0, file: 'Quad6t', kind: 'existing', id: 'op-hw-quad6m-1', before: /^G: op-m39-flectamus/,
      what: 'Dóminus vobíscum. Orémus. (the Monday file op-hw-quad6m-1)', page: 'p. 148', label: 'Dóminus vobíscum · Orémus (Processionarium O.P. 1913, pp. 404-405)'},
    {n: 1, file: 'Quad6t', find: /^T: \^OMNIPOTENS sempitérne Deus : da nobis/, tone: 'II', opts: {dv: false, oremus: false},
      what: 'Oratio (Collect)', page: 'p. 148', rubric: 'Proc. p. 404, II; first of three prayers (Rubr. gen. XI.1, p. 52).',
      label: 'Oratio · in the Mass tone of the Orations (Processionarium O.P. 1913, pp. 404-406)'},
    {n: 2, file: 'Quad6t', find: /^T: \^IN diébus illis : Dixit Jeremías/, title: /^T: \{L\}éctio Jeremíæ Prophétæ/, tone: 'V', opts: {},
      what: 'Lectio Jer. 11 in the place of the Epistle, with its title', page: 'pp. 148-149',
      rubric: 'In the place of the Epistle: Proc. p. 414, V (hw_tones.md §4).',
      label: 'Léctio Jeremíæ Prophétæ · in the Epistle tone (Processionarium O.P. 1913, pp. 414-420)'},
    {n: 3, file: 'Quad6t', find: /^T: \^SANCTIFICATIONIBUS tuis/, tone: 'II', opts: {dv: false, oremus: false},
      what: 'Postcommunio', page: 'p. 153', rubric: 'Proc. p. 404, II; first of three.',
      label: 'Postcommunio · in the Mass tone of the Orations (Processionarium O.P. 1913, pp. 404-406)'},
    {n: 4, file: 'Quad6t', kind: 'existing', id: 'op13-quad6f-oremus', before: /^G: op-m39-humiliate/,
      what: 'Orémus before Humiliáte (existing gabc)', page: 'p. 153', label: 'Orémus (Processionarium O.P. 1913, p. 405)'},
    {n: 5, file: 'Quad6t', find: /^T: \^TUA nos misericórdia, Deus/, tone: 'II', opts: {dv: false, oremus: false},
      what: 'Oratio super populum', page: 'p. 153', rubric: 'Proc. p. 405 (Humiliáte "ante ultimam Postcommunionem"); tone II.',
      label: 'Oratio super populum · in the Mass tone of the Orations (Processionarium O.P. 1913, pp. 404-406)'}
  ]},
  quad6w: {name: 'Feria IV Hebdomadæ Sanctæ', items: [
    {n: 0, file: 'Quad6w', kind: 'existing', id: 'op13-quad6f-oremus', before: /^G: op-m39-flectamus/, nth: 0,
      what: 'Orémus before the first Flectámus (no Dóminus vobíscum: rubric)', page: 'p. 154',
      rubric: 'Missale p. 154: "Post Kyrie eléison, non dicatur Dóminus vobíscum, sed Orémus. Flectámus génua. Leváte."',
      label: 'Orémus (Processionarium O.P. 1913, p. 405)'},
    {n: 1, file: 'Quad6w', find: /^T: \^PRÆSTA, quǽsumus omnípotens Deus/, tone: 'II', opts: {dv: false, oremus: false},
      what: 'Oratio I Præsta (alone: the 2nd and 3rd prayers come after the second Collect)', page: 'p. 154',
      rubric: 'Proc. p. 404, II. The Missal prints "Secunda et tertia Oratio" only after the second Collect: this one keeps its conclusion.',
      label: 'Oratio · in the Mass tone of the Orations (Processionarium O.P. 1913, pp. 404-406)'},
    {n: 2, file: 'Quad6w', find: /^T: \^HÆC dicit Dóminus Deus : Dícite fíliæ Sion/, title: /^T: \{L\}éctio Isaíæ Prophétæ\. \{c\. 62 et 63\}/, tone: 'IV', opts: {},
      what: 'Lectio I Is. 62-63 (a prophecy before the Epistle), with its title', page: 'p. 154',
      rubric: 'Proc. p. 408, IV: "Modus cantandi ... Prophetias in Missa"; it ends without Tu autem: n. 11, p. 413 ("Quando Lectio non terminatur per Tu autem neque per Hæc dicit, tunc finis cantatur flectendo ad ipsum accentum ultimum uno semitonio").',
      label: 'Léctio Isaíæ Prophétæ · in the tone of the Prophecies at Mass (Processionarium O.P. 1913, pp. 408-413)'},
    {n: 3, file: 'Quad6w', kind: 'existing', id: 'op-hw-quad6m-1', before: /^G: op-m39-flectamus/, nth: 1,
      what: 'Dóminus vobíscum. Orémus. before the second Flectámus', page: 'p. 154', label: 'Dóminus vobíscum · Orémus (Processionarium O.P. 1913, pp. 404-405)'},
    {n: 4, file: 'Quad6w', find: /^T: \^DEUS, qui pro nobis Fílium tuum/, tone: 'II', opts: {dv: false, oremus: false},
      what: 'Oratio II Deus, qui pro nobis (first of three with lent_or)', page: 'p. 154', rubric: 'Proc. p. 404, II; Rubr. gen. XI.1.',
      label: 'Oratio · in the Mass tone of the Orations (Processionarium O.P. 1913, pp. 404-406)'},
    {n: 5, file: 'Quad6w', find: /^T: \^IN diébus illis : Dixit Isaías : Dómine, quis crédidit/, title: /^T: \{L\}éctio Isaíæ Prophétæ\. \{c\. 53\}/, tone: 'V', opts: {},
      what: 'Lectio II Is. 53 in the place of the Epistle, with its title', page: 'pp. 154-155',
      rubric: 'In the place of the Epistle: Proc. p. 414, V (hw_tones.md §4).',
      label: 'Léctio Isaíæ Prophétæ · in the Epistle tone (Processionarium O.P. 1913, pp. 414-420)'},
    {n: 6, file: 'Quad6w', find: /^T: \^LARGIRE sénsibus nostris/, tone: 'II', opts: {dv: false, oremus: false},
      what: 'Postcommunio', page: 'p. 160', rubric: 'Proc. p. 404, II; first of three.',
      label: 'Postcommunio · in the Mass tone of the Orations (Processionarium O.P. 1913, pp. 404-406)'},
    {n: 7, file: 'Quad6w', kind: 'existing', id: 'op13-quad6f-oremus', before: /^G: op-m39-humiliate/,
      what: 'Orémus before Humiliáte (existing gabc)', page: 'p. 160', label: 'Orémus (Processionarium O.P. 1913, p. 405)'},
    {n: 8, file: 'Quad6w', find: /^T: \^RESPICE, quǽsumus Dómine, super hanc/, tone: 'II', opts: {dv: false, oremus: false},
      what: 'Oratio super populum', page: 'p. 160', rubric: 'Proc. p. 405; tone II.',
      label: 'Oratio super populum · in the Mass tone of the Orations (Processionarium O.P. 1913, pp. 404-406)'}
  ]}
};

// -------------------------------------------------------------------------------------------------- run
const args = process.argv.slice(2), WRITE = args.includes('--write'), INSERT = args.includes('--insert');
const days = args.filter(a => !a.startsWith('--'));
const srcPath = f => path.join(__dirname, f + '.src');
const lines = f => fs.readFileSync(srcPath(f), 'utf8').split('\n');

function prepare(it) {
  const L = lines(it.file);
  if (it.kind === 'dv') return {gabc: T.orationProc('', Object.assign({tone: TONE[it.tone].tone}, it.opts)), text: 'Dóminus vobíscum. Orémus.'};
  const k = L.findIndex(l => it.find.test(l));
  if (k < 0) throw new Error(it.file + ': not found ' + it.find);
  if (L.slice(k + 1).some(l => it.find.test(l))) throw new Error(it.file + ': not unique ' + it.find);
  let la = clean(L[k].slice(3)), title = null, g;
  if (it.title) { const t = L.find(l => it.title.test(l)); if (!t) throw new Error('title not found'); title = clean(t.slice(3)); }
  if (it.special === 'palmBlessing') {
    // Proc. pp. 20-21 print this prayer pointed for tone III: the flexa sign where the Missal has ";", and also at
    // "voluísti ‡" (Missal: "voluísti."); the prayer ends in its own conclusion, pointed "... per ómnia sǽcula
    // sæculórum ‡. ℟. Amen." (no colon at Deus): the last member takes the flexa (tone III, p. 408: sæculó(h)rum(f))
    const k2 = la.indexOf('Salvátor mundi,');
    if (k2 < 0 || !/voluísti\. Sed/.test(la)) throw new Error('palm blessing text changed');
    const bodyTxt = la.slice(0, k2).trim().replace('voluísti. Sed', 'voluísti † sed'), fin = la.slice(k2).trim().replace(/\.$/, '');
    g = T.orationProc(bodyTxt, Object.assign({tone: 'hours'}, it.opts)).replace(/ \(::\)$/, ' (;)');
    g += ' ' + T._proc.flexO(fin + '.', true) + ' (::) <sp>R/</sp>. A(g)men.(h) (::)';
    // the sung text keeps the Missal's words and stop ("voluísti. Sed"); only the notes follow the Proc. pointing
    const g2 = g.replace(/sti;\(f\) \(,\) sed\(h\)/, 'sti.(f) (,) Sed(h)');
    if (g2 === g) throw new Error('voluísti flexa not found');
    return {gabc: g2.replace(/\s+/g, ' '), text: la};
  }
  if (it.tone === 'II' || it.tone === 'III') {
    la = la.replace(/\s*\(Per Dóminum[^)]*\)\s*$/, '');            // the parenthesised conclusion of a 2nd prayer
    const m = CONCL.exec(la);
    if (it.conc === 'drop') { if (m) la = la.slice(0, m.index); la = la.replace(/[\s:;,.]*$/, '.'); }
    else {
      if (!m) throw new Error('no conclusion: ' + la.slice(-60));
      const body = la.slice(0, m.index).replace(/\s*$/, '');
      la = body + ' ' + conclusion(m[1], body);
    }
    g = T.orationProc(la, Object.assign({tone: TONE[it.tone].tone}, it.opts));
  } else if (it.tone === 'IV') g = T.lessonProc(la, {title});
  else if (it.tone === 'V') g = T.epistleProc(la, {title});
  else if (it.tone === 'VI') g = T.gospelProc(la, it.opts);
  return {gabc: g, text: (title ? title + ' ' : '') + la};
}

function header(day, it, text) {
  const tn = TONE[it.tone];
  return [
    'name:' + it.what.replace(/;/g, ',') + ';',
    'office-part:' + ({II: 'Oratio', III: 'Oratio', IV: 'Lectio', V: 'Epistola', VI: 'Evangelium'})[it.tone] + ';',
    'occasion:' + DAYS[day].name + ' (Missale O.P. 1939, ' + it.page + ');',
    'book:set to ' + tn.name + ', ' + PROC + ', ' + tn.pp + ' (pdf = printed + 16); text from the Missale O.P. (1939), ' + it.page + ';',
    'commentary:' + (it.rubric || '').replace(/;/g, ',') + ';',
    'transcriber:generated by tools/hw39/gen_quad6.js with OPMassTones (js/mtones.js), Holy Week task W-B2, 2026-11-27;',
    '%%'
  ].join('\n');
}

function insertG(it, gline) {
  const L = lines(it.file);                      // re-read right before the edit (another worker edits these files)
  if (L.some(l => l.split('|')[0].trim() === gline.split('|')[0].trim() && (it.nth == null))) return 'present';
  let idx = -1;
  if (it.before) {
    const hits = L.map((l, i) => it.before.test(l) ? i : -1).filter(i => i >= 0);
    idx = hits[it.nth || 0];
  } else if (it.title) idx = L.findIndex(l => it.title.test(l));
  else idx = L.findIndex(l => it.find.test(l));
  if (idx == null || idx < 0) throw new Error(it.file + ': insertion point not found');
  if (L[idx - 1] && L[idx - 1].split('|')[0].trim() === gline.split('|')[0].trim()) return 'present';
  L.splice(idx, 0, gline);
  fs.writeFileSync(srcPath(it.file), L.join('\n'));
  return 'inserted before line ' + (idx + 1);
}

for (const day of (days.length ? days : Object.keys(DAYS))) {
  for (const it of DAYS[day].items) {
    const id = it.kind === 'existing' ? it.id : 'op-hw-' + day + '-' + it.n;
    const gline = 'G: ' + id + '|' + it.label;
    let note = '';
    if (it.kind !== 'existing') {
      if (!T.orationProc) throw new Error('OPMassTones.*Proc not loaded');
      const r = prepare(it);
      const file = path.join(SITE, 'gabc', id + '.gabc');
      if (WRITE) fs.writeFileSync(file, header(day, it, r.text) + '\n' + toI(r.gabc) + '\n');
      note = (WRITE ? 'wrote ' : 'would write ') + 'gabc/' + id + '.gabc (' + r.gabc.length + ' chars)';
      if (!WRITE && process.env.SHOW) console.log(toI(r.gabc));
    }
    if (INSERT) note += '; ' + it.file + '.src: ' + insertG(it, gline);
    console.log('[' + day + ' ' + it.n + '] ' + it.what + ' | tone ' + (it.tone || '-') + ' | ' + note + '\n    ' + it.file + '.src  ' + gline);
  }
}
