// Generate tools/proc/gabc/tone_*.gabc: versicles and prayers of the processions, sung to the tones of the
// Processionarium O.P. (1913). Rules applied (all read from the book, see each file's header):
//  - Versicles: Regulae, Art. II § IV 3° (p. 395-396), "Subscripto modo dicantur Versiculi ... in Processionibus":
//    recitation on the tenor (F clef 3rd line: h), the syllables after the last accent fall a third (f), as in
//    "sacrá(h)ta(f)", "tu(h)os(f)"; with a closing alleluia (p. 396, "Dícite in natiónibus, allelúia") the words
//    before it stay on the tenor, a half bar, then al-le-lú(h) ia(f).
//  - Prayers: Art. III § III (pp. 407-408) "Modus cantandi Orationes ad Horas, et quotiescumque aliquae aliae
//    Orationes quae non sunt de corpore Officii et Missae cantandae fuerint": Orémus h h f; body on the tenor h;
//    at the flexa (‡ in the book) the syllables after the last accent fall to f (tristí(h)ti(f)a(f));
//    at the metrum (: in the book) the two syllables before the last accent (three when the third belongs to a
//    dactyl, p. 405 2°) go to g, the last of them to f, the accent and what follows back on h
//    (salú(h)te(g) gau(f)dé(h)re(h); pér(h)fru(g)i(g) læ(f)tí(h)ti(h)a(h)); conclusion with its flexa
//    (nos(h)trum(f), sæculó(h)rum(f)); ℟. A(g)men(h) (p. 401 VII 2°, p. 408).
const fs = require('fs');
global.window = {};
const P = require('/home/claude/dominican-liturgy/js/psalm.js');
const TEXTS = JSON.parse(fs.readFileSync('/tmp/gen/texts.json', 'utf8'));
const OUT = '/home/claude/dominican-liturgy/tools/proc/gabc/';

function syl(text) { return P.analyse(text); }
function lastAcc(s) { let a = -1; s.forEach((x, i) => { if (x.acc) a = i; }); return a < 0 ? Math.max(0, s.length - 2) : a; }
function render(s, notes) {
  return s.map((x, i) => x.t + '(' + notes[i] + ')' + (x.last ? ' ' : '')).join('').trim();
}
function recto(t) { const s = syl(t); return render(s, s.map(() => 'h')); }
function flex(t) {
  const s = syl(t), A = lastAcc(s);
  return render(s, s.map((x, i) => i > A ? 'f' : 'h'));
}
function metrum(t) {
  const s = syl(t), A = lastAcc(s);
  let k = 2;
  if (A >= 4 && !s[A - 3].acc && s[A - 4].acc && s[A - 4].word === s[A - 3].word && s[A - 3].word === s[A - 2].word) k = 3;
  return render(s, s.map((x, i) => i >= A ? 'h' : (i === A - 1 ? 'f' : (i >= A - k ? 'g' : 'h'))));
}
const AMEN = '<sp>R/</sp>. A(g)men.(h) (::)';
const OREMUS = 'O(h)ré(h)mus.(f) (::)';
// a versicle or response: [text] with the final flexa; ", allelúia" after a half bar (p. 396)
function vr(t) {
  inData(TEXTS.some(x => x.includes(t)) ? t : t.replace(/, allelúia\.$/, '.'));
  const m = /^(.*),\s*(allelúia\.?)$/.exec(t);
  if (m) return recto(m[1] + ',') + ' (;) ' + flex(m[2]) + ' (::)';
  return flex(t) + ' (::)';
}
// prayer: list of [text, 'f'|'m'|'c'] ; f = flexa (;), m = metrum (:), c = conclusion (flexa, ::)
function prayer(parts, oremus = true) {
  let g = '(f3) ' + (oremus ? OREMUS + ' ' : '');
  parts.forEach(([t, k]) => {
    if (k === 'f') g += flex(t) + ' (;) ';
    else if (k === 'm') g += metrum(t) + ' (:) ';
    else g += flex(t) + ' (::) ';
  });
  return g + AMEN;
}
function inData(t) { if (!TEXTS.some(x => x.includes(t))) { console.error('NOT IN proc_data:', t); process.exit(1); } }
function check(name, parts, full) {
  const joined = 'Orémus. ' + parts.map(p => p[0]).join(' ') + ' ℟. Amen.';
  if (joined !== full) { console.error('TEXT MISMATCH', name); process.exit(1); }
  inData(joined);
}
const VTONE = 'Versicle: Art. II § IV 3° (pp. 395-396: "Subscripto modo dicantur Versiculi ad Memorias et ante Laudes, et in Processionibus, et quotiescumque dicitur V. a Sacerdote"): tenor h, the syllables after the last accent of the versicle (marked with the flexa sign in the text) fall to f, as in the example Dignáre me laudáre te, Virgo sacráta. R. Da mihi virtútem contra hostes tuos; alleluia after a half bar as in the example Dícite in natiónibus, allelúia (p. 396). Proparoxytone endings: both syllables after the accent fall (the flexa as defined in Art. III § I, p. 402: geminatur nota re). F clef on the 3rd line as printed.';
const OTONE = 'Prayer: Art. III § III, pp. 407-408 ("Modus cantandi Orationes ad Horas, et quotiescumque aliquae aliae Orationes quae non sunt de corpore Officii et Missae cantandae fuerint"), applied after its printed example Concéde nos fámulos tuos (p. 407) and conclusions (p. 408): Orémus h h f; tenor h; at the flexa (the sign after the word in the text of this page) the syllables after the last accent fall to f; at the metrum (colon in the text of this page) the two syllables before the last accent (three if the third ends a dactyl, Art. III § II 2°, p. 405) on g, the last of them on f, the accent and the rest on h; R. Amen g h (p. 401, VII 2°; p. 408). The inflexions fall where this page marks them, not where the site text has its punctuation. F clef on the 3rd line as printed.';
function write(file, name, part, pageNote, tone, gabc) {
  const head = `name:${name};\noffice-part:${part};\nmode:;\nbook:Processionarium O.P. (Cormier), 1913, ${pageNote};\n` +
    `commentary:${tone.replace(/;/g, ',')};\ntranscriber:the tone of the Processionarium O.P. 1913 applied to this text for this site (the book prints no melody with this text);\n%%\n`;
  fs.writeFileSync(OUT + file + '.gabc', head + gabc + '\n');
  console.log(file, gabc.length);
}

// ---------------- Ascension, pp. 50-51
write('tone_asc_versus', 'Ascendit Deus (versus ad processionem)', 'Versiculus', 'p. 50 (text)', VTONE,
  '(f3) <sp>V/</sp>. ' + vr('Ascéndit Deus in jubilatióne, allelúia.') + ' <sp>R/</sp>. ' + vr('Et Dóminus in voce tubæ, allelúia.'));
let p = [['Deus, cujus Fílius in alta cælórum poténter ascéndens, captivitátem nostram sua duxit virtúte captívam:', 'f'],
         ['tríbue, quǽsumus, ut dona, quæ suis particípibus cóntulit, largiátur et nobis,', 'm'],
         ['Jesus Christus Fílius tuus Dóminus noster: Qui tecum vivit et regnat per ómnia sǽcula sæculórum.', 'c']];
check('asc', p, 'Orémus. Deus, cujus Fílius in alta cælórum poténter ascéndens, captivitátem nostram sua duxit virtúte captívam: tríbue, quǽsumus, ut dona, quæ suis particípibus cóntulit, largiátur et nobis, Jesus Christus Fílius tuus Dóminus noster: Qui tecum vivit et regnat per ómnia sǽcula sæculórum. ℟. Amen.');
write('tone_asc_oratio', 'Deus, cujus Filius (oratio ad processionem)', 'Oratio', 'pp. 50-51 (text, with its flexa after captívam, colon after nobis, flexa after sæculórum)', OTONE, prayer(p));

// ---------------- Purification, pp. 66-67, 72
p = [['Omnípotens sempitérne Deus, qui hodiérna die Unigénitum tuum ulnis sancti Simeónis in Templo sancto tuo suscipiéndum præsentásti:', 'f'],
     ['tuam súpplices deprecámur cleméntiam:', 'm'],
     ['ut has candélas, quas nos fámuli tui, in tui nóminis magnificéntiam suscipiéntes, gestáre cúpimus, luce accénsas, bene✠dícere et sancti✠ficáre, atque lúmine supérnæ benedictiónis accéndere dignéris:', 'f'],
     ['quátenus eas tibi Dómino Deo nostro offeréndo, digni, et sancto igne dulcíssimæ caritátis tuæ succénsi, in Templo sancto glóriæ tuæ repræsentári mereámur.', 'm'],
     ['Per eúndem Christum Dóminum nostrum.', 'c']];
check('omnip', p, 'Orémus. Omnípotens sempitérne Deus, qui hodiérna die Unigénitum tuum ulnis sancti Simeónis in Templo sancto tuo suscipiéndum præsentásti: tuam súpplices deprecámur cleméntiam: ut has candélas, quas nos fámuli tui, in tui nóminis magnificéntiam suscipiéntes, gestáre cúpimus, luce accénsas, bene✠dícere et sancti✠ficáre, atque lúmine supérnæ benedictiónis accéndere dignéris: quátenus eas tibi Dómino Deo nostro offeréndo, digni, et sancto igne dulcíssimæ caritátis tuæ succénsi, in Templo sancto glóriæ tuæ repræsentári mereámur. Per eúndem Christum Dóminum nostrum. ℟. Amen.');
write('tone_pur_omnipotens', 'Omnipotens sempiterne Deus (benedictio candelarum)', 'Oratio', 'p. 66 (rubric: "benedicat voce mediocri, eo modo quo dicuntur Orationes ad Horas") and p. 67 (text, with its flexa after præsentásti and dignéris, colons after cleméntiam and mereámur, flexa after nostrum)', OTONE, prayer(p));
write('tone_pur_versus', 'Post partum (versus ad processionem)', 'Versiculus', 'p. 72 (text)', VTONE,
  '(f3) <sp>V/</sp>. ' + vr('Post partum, Virgo, invioláta permansísti.') + ' <sp>R/</sp>. ' + vr('Dei Génitrix, intercéde pro nobis.'));
p = [['Erúdi, quǽsumus, Dómine, plebem tuam:', 'm'],
     ['et quæ extrínsecus ánnua tríbuis devotióne venerári,', 'f'],
     ['intérius ássequi grátiæ tuæ luce concéde.', 'm'],
     ['Per Christum Dóminum nostrum.', 'c']];
check('erudi', p, 'Orémus. Erúdi, quǽsumus, Dómine, plebem tuam: et quæ extrínsecus ánnua tríbuis devotióne venerári, intérius ássequi grátiæ tuæ luce concéde. Per Christum Dóminum nostrum. ℟. Amen.');
write('tone_pur_erudi', 'Erudi, quaesumus (oratio ad processionem)', 'Oratio', 'p. 72 (text, with its colon after tuam, flexa after venerári, colon after concéde, flexa after nostrum)', OTONE, prayer(p));

// ---------------- Salve Regina procession, pp. 90-91
const TP_R = (r) => ' <i>T. P.</i>(::) <sp>R/</sp>. ' + vr(r.replace(/\.$/, ', allelúia.'));
write('tone_salve_dignare', 'Dignare me (versus post Salve Regina)', 'Versiculus', 'p. 90 (text; the same versicle is the printed example of the tone, p. 395-396)', VTONE +
  ' In Paschaltide the Alleluia is added (p. 90: Temp. Pasch. additur Allelúia), sung as in the example on p. 396.',
  '(f3) <sp>V/</sp>. ' + vr('Dignáre me laudáre te, Virgo sacráta.') + ' <sp>R/</sp>. ' + vr('Da mihi virtútem contra hostes tuos.').replace(/ \(::\)$/, '') + TP_R('Da mihi virtútem contra hostes tuos.'));
p = [['Concéde nos fámulos tuos, quǽsumus, Dómine Deus, perpétua mentis et córporis salúte gaudére:', 'm'],
     ['et gloriósa beátæ Maríæ semper Vírginis intercessióne, a præsénti liberári tristítia,', 'f'],
     ['et ætérna pérfrui lætítia.', 'm'],
     ['Per Christum Dóminum nostrum.', 'c']];
check('concede', p, 'Orémus. Concéde nos fámulos tuos, quǽsumus, Dómine Deus, perpétua mentis et córporis salúte gaudére: et gloriósa beátæ Maríæ semper Vírginis intercessióne, a præsénti liberári tristítia, et ætérna pérfrui lætítia. Per Christum Dóminum nostrum. ℟. Amen.');
write('tone_salve_concede', 'Concede nos famulos tuos (oratio post Salve Regina)', 'Oratio', 'pp. 90-91 (text; the same prayer is the printed example of the tone, p. 407, and its conclusion p. 408)', OTONE, prayer(p));
write('tone_salve_dominice', 'Ora pro nobis, beate Pater Dominice (versus)', 'Versiculus', 'p. 91 (text)', VTONE +
  ' In Paschaltide the Alleluia is added (p. 91: Temp. Pasch. additur Allelúia), sung as in the example on p. 396.',
  '(f3) <sp>V/</sp>. ' + vr('Ora pro nobis, beáte Pater Domínice.') + ' <sp>R/</sp>. ' + vr('Ut digni efficiámur promissiónibus Christi.').replace(/ \(::\)$/, '') + TP_R('Ut digni efficiámur promissiónibus Christi.'));
p = [['Concéde, quǽsumus, omnípotens Deus:', 'm'],
     ['ut qui peccatórum nostrórum póndere prémimur,', 'f'],
     ['beáti Domínici Confessóris tui, Patris nostri, patrocínio sublevémur.', 'm'],
     ['Per Christum Dóminum nostrum.', 'c']];
check('dominici', p, 'Orémus. Concéde, quǽsumus, omnípotens Deus: ut qui peccatórum nostrórum póndere prémimur, beáti Domínici Confessóris tui, Patris nostri, patrocínio sublevémur. Per Christum Dóminum nostrum. ℟. Amen.');
write('tone_salve_dominici', 'Concede, quaesumus, omnipotens Deus (oratio de S. P. Dominico)', 'Oratio', 'p. 91 (text, with its colon after Deus, flexa after prémimur, colon after sublevémur, flexa after nostrum)', OTONE, prayer(p));

// ---------------- Litany of Loreto: after the Prose / Regina caeli, p. 95
write('tone_lor_genitrix', 'Ora pro nobis, sancta Dei Genitrix (versus)', 'Versiculus', 'p. 95 (text)', VTONE +
  ' In Paschaltide the Alleluia is added (p. 95: T. P. additur Allelúia), sung as in the example on p. 396.',
  '(f3) <sp>V/</sp>. ' + vr('Ora pro nobis, sancta Dei Génitrix.') + ' <sp>R/</sp>. ' + vr('Ut digni efficiámur promissiónibus Christi.').replace(/ \(::\)$/, '') + TP_R('Ut digni efficiámur promissiónibus Christi.'));
p = [['Grátiam tuam, quǽsumus, Dómine, méntibus nostris infúnde:', 'm'],
     ['ut qui, Angelo nuntiánte, Christi Fílii tui Incarnatiónem cognóvimus,', 'f'],
     ['per Passiónem ejus et Crucem ad resurrectiónis glóriam perducámur.', 'm'],
     ['Per eúndem Christum Dóminum nostrum.', 'c']];
check('gratiam', p, 'Orémus. Grátiam tuam, quǽsumus, Dómine, méntibus nostris infúnde: ut qui, Angelo nuntiánte, Christi Fílii tui Incarnatiónem cognóvimus, per Passiónem ejus et Crucem ad resurrectiónis glóriam perducámur. Per eúndem Christum Dóminum nostrum. ℟. Amen.');
write('tone_lor_gratiam', 'Gratiam tuam (oratio)', 'Oratio', 'p. 95 (text, with its colon after infúnde, flexa after cognóvimus, colon after perducámur, flexa after nostrum)', OTONE, prayer(p));
write('tone_lor_postpartum', 'Post partum (versus post Prosam vel Regina caeli)', 'Versiculus', 'p. 95 (text)', VTONE +
  ' In Paschaltide the Alleluia is added (p. 95: T. P. additur Allelúia), sung as in the example on p. 396.',
  '(f3) <sp>V/</sp>. ' + vr('Post partum, Virgo, invioláta permansísti.') + ' <sp>R/</sp>. ' + vr('Dei Génitrix, intercéde pro nobis.').replace(/ \(::\)$/, '') + TP_R('Dei Génitrix, intercéde pro nobis.'));
p = [['Prótege, Dómine, fámulos tuos subsídiis pacis:', 'm'],
     ['et beátæ Maríæ semper Vírginis patrocíniis confidéntes,', 'f'],
     ['a cunctis hóstibus redde secúros.', 'm'],
     ['Per Christum Dóminum nostrum.', 'c']];
check('protege', p, 'Orémus. Prótege, Dómine, fámulos tuos subsídiis pacis: et beátæ Maríæ semper Vírginis patrocíniis confidéntes, a cunctis hóstibus redde secúros. Per Christum Dóminum nostrum. ℟. Amen.');
write('tone_lor_protege', 'Protege, Domine (oratio)', 'Oratio', 'p. 95 (text, with its colon after pacis, flexa after confidéntes, colon after secúros, flexa after nostrum)', OTONE, prayer(p));
