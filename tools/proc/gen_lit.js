/* Generates the fully-set litanies, versicles and prayers of processions.html (tools/proc/gabc/*.gabc) from the
   Processionarium O.P. (Cormier, Rome 1913). Run: node tools/proc/gen_lit.js
   Every formula below is the one the book prints (page given); each invocation is set to it as the book itself sets
   its printed examples. Nothing here comes from a Roman book.
   The texts of the litanies are taken from tools/proc/proc_data.py (LIT_LAUR, LIT_SANCT), so text and chant agree. */
'use strict';
const fs = require('fs'), path = require('path'), cp = require('child_process');
const H = __dirname, R = path.dirname(path.dirname(H));
const P = require(R + '/js/psalm.js');
const DATA = JSON.parse(cp.execFileSync('python3', ['-c',
  'import sys, json; sys.path.insert(0, sys.argv[1]); import proc_data as d; print(json.dumps({"laur": d.LIT_LAUR, "sanct": d.LIT_SANCT}))', H]).toString());

const ACUTE = /[áéíóúýǽÁÉÍÓÚÝǼ]/;
// syllables of a text: a word may carry '|' to give its syllables where the general rule would split wrongly
// (Ray|mún|de: "ay" is one vowel there). Accent: the acute; a word of two syllables on its first; a monosyllable none.
function syls(text, needAcc) {
  const out = [], words = text.trim().split(/\s+/).filter(w => /[A-Za-zÀ-ÿǼǽœŒ]/.test(w));
  words.forEach((w, wi) => {
    const parts = w.indexOf('|') >= 0 ? w.split('|') : P.syllabify(w);
    let acc = -1;
    parts.forEach((p, i) => { if (ACUTE.test(p)) acc = i; });
    if (acc < 0 && parts.length === 2) acc = 0;
    if (acc < 0 && parts.length >= 3 && needAcc && wi === words.length - 1) throw new Error('unmarked accent: ' + w + ' in ' + text);
    parts.forEach((p, i) => out.push({t: p, word: wi, first: i === 0, last: i === parts.length - 1, acc: i === acc, mono: parts.length === 1}));
  });
  return out;
}
function lastAcc(s) { for (let i = s.length - 1; i >= 0; i--) if (s[i].acc) return i; throw new Error('no accent: ' + s.map(x => x.t).join('')); }
function out(s, n) { return s.map((x, i) => x.t + '(' + n[i] + ')' + (x.last ? ' ' : '')).join('').trim(); }
const clean = t => t.replace(/\s+/g, ' ').trim();

// ------------------------------------------------------------------ the litany formulas
const F = {
  // Litaniae Lauretanae p. 92, Sancta Maria ... Virgo fidelis (c4): the recitation on F, the last accent on G,
  // a second syllable after it on G, the last syllable on A (the book lines Ma-ter Chri-sti, Vir-go pó-tens, Ma-ter
  // pu-rís-si-ma, Ma-ter Cre-a-tó-ris up under the notes so).
  laurA(t) { const s = syls(t, 1), L = lastAcc(s), n = s.map(() => 'f'); const post = s.length - 1 - L;
    if (post < 1 || post > 2) throw new Error('laurA ' + t); n[L] = 'g'; if (post === 2) n[L + 1] = 'g'; n[s.length - 1] = 'h'; return out(s, n); },
  // p. 92-93, Speculum justitiae ... Auxilium Christianorum (c4): recitation on A (la, gabc h), the last accent on B flat, all after it on G
  // (Spé-cu-lum ju-stí-ti-æ, Vas spi-ri-tu-á-le, Fœ-de-ris ar-ca, Re-fú-gi-um pec-ca-tó-rum).
  laurB(t) { const s = syls(t, 1), L = lastAcc(s), n = s.map(() => 'h'); if (L === s.length - 1) throw new Error('laurB ' + t);
    n[L] = 'ixi'; for (let i = L + 1; i < s.length; i++) n[i] = 'g'; return out(s, n); },
  // p. 93, Regina Angelorum ... (c4): recitation on C (do), the two syllables before the last accent on A and B, the accent and
  // all after it on C (Re-gí-na An-ge-ló-rum, Re-gí-na Már-ty-rum, Re-gí-na San-ctó-rum óm-ni-um).
  laurC(t) { const s = syls(t, 1), L = lastAcc(s), n = s.map(() => 'j'); if (L < 2) throw new Error('laurC ' + t);
    n[L - 2] = 'h'; n[L - 1] = 'i'; return out(s, n); },
  // Litaniae Sanctorum p. 126, Sancta Maria / Sancta Dei Genitrix / Sancta Virgo virginum (c4): recitation on G, the
  // last accent on A, all after it on G; the same notes for the plural on p. 127 (Om-nes sanc-ti An-ge-li et Ar-chán-ge-li)
  sanct(t) { const s = syls(t, 1), L = lastAcc(s), n = s.map(() => 'g'); n[L] = 'h'; if (L === s.length - 1) throw new Error('sanct ' + t); return out(s, n); },
  // p. 126, Sancte Michael / Gabriel / Raphael (c4): all on G, the last syllable on A
  michael(t) { const s = syls(t), n = s.map(() => 'g'); n[s.length - 1] = 'h'; return out(s, n); },
  // p. 126, Pater de caelis Deus (c4): recitation on G, De- of Deus on A
  trinity(t) { const s = syls(t, 1), L = lastAcc(s), n = s.map(() => 'g'); n[L] = 'h'; return out(s, n); },
  // p. 128, A damnatione perpetua (c3): recitation on C, the two syllables before the last accent on B and A, the accent and
  // all after it on C (A dam-na-ti-ó-ne per-pé-tu-a, as the book lines it up)
  libera(t) { const s = syls(t, 1), L = lastAcc(s), n = s.map(() => 'h'); if (L < 2) throw new Error('libera ' + t);
    n[L - 2] = 'g'; n[L - 1] = 'f'; return out(s, n); },
  // p. 129, Peccatores (c3): Pec(C) ca(B) tó(D) res(D): recitation on C, the syllable before the last accent on B,
  // the accent and all after it on D
  rogamus(t) { const s = syls(t, 1), L = lastAcc(s), n = s.map(() => 'h'); if (L < 1) throw new Error('rogamus ' + t);
    n[L - 1] = 'g'; for (let i = L; i < s.length; i++) n[i] = 'i'; return out(s, n); },
};
const RESP = {
  laurA: '<sp>R/</sp>. o(f)ra(e) pro(d) no(e)bis.(f)',                 // p. 92
  laurB: '<sp>R/</sp>. o(g)ra(f) pro(g) no(h)bis.(h)',                 // p. 92-93
  laurC: '<sp>R/</sp>. o(h)ra(g) pro(f) no(g)bis.(h)',                 // p. 93
  ora: '<sp>R/</sp>. O(g)ra(e) pro(f) no(g)bis.(g)',                   // p. 126
  orate: '<sp>R/</sp>. O(g)rá(g)te(e) pro(f) no(g)bis.(g)',            // p. 127
  miserere: 'mi(g)se(g)ré(e)re(f) no(g)bis.(g)',                       // p. 126
  libera: '<sp>R/</sp>. Lí(g)be(h)ra(f) nos,(e) Dó(f)mi(e)ne.(d)',     // p. 128
  rogamus: '<sp>R/</sp>. te(h) ro(g)gá(f)mus,(e) au(f)di(h) nos.(h)',   // p. 129
};
const FIX = {'Raymúnde,': 'Ray|mún|de,', 'Nicoláe,': 'Ni|co|lá|e,', 'Hierónyme,': 'Hie|ró|ny|me,'};
const fix = t => t.split(' ').map(w => FIX[w] || w).join(' ');

function file(name, head, body) {
  const g = Object.entries(head).map(([k, v]) => k + ':' + String(v).replace(/;/g, ',') + ';').join('\n') + '\n%%\n' + body + '\n';
  fs.writeFileSync(H + '/gabc/' + name + '.gabc', g);
  return name;
}
const BOOK = (p, part) => 'Processionarium O.P. (Cormier), 1913, ' + p + (part ? ' (' + part + ')' : '');
const TR = 'set for this site from the scan of the Processionarium O.P. 1913';

// ------------------------------------------------------------------ Litaniae Lauretanae (pp. 91-94)
const laur = DATA.laur.filter(r => r[0] !== '*');
const iA = laur.findIndex(r => r[0].startsWith('Sancta María')), iB = laur.findIndex(r => r[0].startsWith('Spéculum')),
      iC = laur.findIndex(r => r[0].startsWith('Regína Angel')), iZ = laur.findIndex(r => r[0].startsWith('Agnus'));
function block(rows, fn, resp, sep) { return rows.map(r => F[fn](fix(r[0])) + ' (::) ' + resp + ' (::)').join(sep || ' '); }
file('lor_invocation_maria', {name: 'Litaniae Lauretanae B. M. V.: Sancta Maria ... Virgo fidelis, ora pro nobis', 'office-part': 'Litaniae', mode: '6',
  book: BOOK('p. 92'), transcriber: TR,
  commentary: 'set to the formula printed on p. 92 (Sancta Maria, ora pro nobis), every invocation as the book lines its syllables up under those notes: recitation on F, the last accent on G, a following syllable on G, the last syllable on A'},
  '(c4) ' + block(laur.slice(iA, iB), 'laurA', RESP.laurA));
file('lor_invocation_speculum', {name: 'Litaniae Lauretanae B. M. V.: Speculum justitiae ... Auxilium Christianorum, ora pro nobis', 'office-part': 'Litaniae', mode: '6',
  book: BOOK('pp. 92-93'), transcriber: TR,
  commentary: 'set to the formula printed on pp. 92-93 (Speculum justitiae, ora pro nobis), every invocation as the book lines its syllables up under those notes: recitation on A (la, h), the last accent on B flat, the syllables after it on G'},
  '(c4) ' + block(laur.slice(iB, iC), 'laurB', RESP.laurB));
const regina = laur.slice(iC, iZ);
file('lor_invocation_regina', {name: 'Litaniae Lauretanae B. M. V.: Regina Angelorum ... Regina in caelum assumpta, ora pro nobis', 'office-part': 'Litaniae', mode: '6',
  book: BOOK('p. 93'), transcriber: TR,
  commentary: 'set to the formula printed on p. 93 (Regina Angelorum, ora pro nobis), every invocation as the book lines its syllables up under those notes: recitation on C (do, on the 4th line), the two syllables before the last accent on A and B, the accent and what follows on C. Regina in caelum assumpta (added 1950) is typed on a slip pasted into the scanned copy, not printed in 1913; it is set to the same formula and labelled'},
  '(c4) ' + regina.map((r, i) => (r[0].startsWith('Regína in') ? '<i>Added after 1913, typed into the scanned copy:</i>() ' : '') + F.laurC(r[0]) + ' (::) ' + RESP.laurC + ' (::)').join(' '));

// ------------------------------------------------------------------ Litaniae Sanctorum (pp. 126-130)
const S = DATA.sanct, idx = p => S.findIndex(p);
const sTr = S.slice(idx(r => r[0].startsWith('Pater de')), idx(r => r[0].startsWith('Sancta María')));
file('lit_miserere', {name: 'Litaniae Sanctorum: Pater de caelis Deus ... Sancta Trinitas unus Deus, miserere nobis', 'office-part': 'Litaniae', mode: '',
  book: BOOK('p. 126', 'Litaniae Sanctorum'), transcriber: TR,
  commentary: 'p. 126 notates Pater de caelis Deus, miserere nobis and gives the other three as text under it, with R/. Pater., etc.: the choir repeats the whole invocation. Each is set to the formula printed on p. 126 (recitation on G, De- of Deus on A), and the repetition written out'},
  '(c4) ' + sTr.map(r => { const a = F.trinity(r[0]) + ' (;) ' + RESP.miserere; return a + ' (::) <sp>R/</sp>. ' + a + ' (::)'; }).join(' '));
const iM = idx(r => r[0].startsWith('Sancta María')), iMi = idx(r => r[0].startsWith('Sancte Míchaël')), iAng = idx(r => r[0].startsWith('Omnes sancti Ángeli'));
file('lit_ora', {name: 'Litaniae Sanctorum: Sancta Maria, Sancta Dei Genitrix, Sancta Virgo virginum, ora pro nobis', 'office-part': 'Litaniae', mode: '',
  book: BOOK('p. 126', 'Litaniae Sanctorum'), transcriber: TR,
  commentary: 'the three invocations are printed under the one formula on p. 126 and set to it as the book lines them up (Sanc-ta Ma-rí-a: the accent on A; Gé-ni-trix, Vír-gi-num: the accent on A, the two syllables after it on G)'},
  '(c4) ' + block(S.slice(iM, iMi), 'sanct', RESP.ora));
file('lit_ora_michael', {name: 'Litaniae Sanctorum: Sancte Michael, Gabriel, Raphael, ora pro nobis', 'office-part': 'Litaniae', mode: '',
  book: BOOK('p. 126', 'Litaniae Sanctorum'), transcriber: TR,
  commentary: 'the three invocations are printed under the one formula on p. 126 (Sancte Mícha-el: all on G, the last syllable on A)'},
  '(c4) ' + block(S.slice(iMi, iAng), 'michael', RESP.ora));
const iJB = idx(r => r[0].startsWith('Sancte Joánnes Bapt')), iDom = idx(r => r[0] === '*'), iProp = idx(r => r[0].startsWith('Propítius'));
const saintLine = r => F.sanct(fix(r[0])) + ' (::) ' + (r[1].startsWith('oráte') ? RESP.orate : RESP.ora) + ' (::)';
file('lit_orate', {name: 'Litaniae Sanctorum: Omnes sancti Angeli et Archangeli; Omnes sancti beatorum Spirituum ordines, orate pro nobis', 'office-part': 'Litaniae', mode: '',
  book: BOOK('p. 127', 'Litaniae Sanctorum'), transcriber: TR,
  commentary: 'Omnes sancti Angeli et Archangeli, orate pro nobis is notated on p. 127; Omnes sancti beatorum Spirituum ordines, given as text, is set to that formula (recitation on G, the last accent on A, the syllables after it on G)'},
  '(c4) ' + S.slice(iAng, iJB).map(saintLine).join(' '));
file('lit_sancti', {name: 'Litaniae Sanctorum: Sancte Joannes Baptista ... Sancte Antonine', 'office-part': 'Litaniae', mode: '',
  book: BOOK('p. 127', 'Litaniae Sanctorum'), transcriber: TR,
  commentary: 'given as text on p. 127 (ora., orate. for ora pro nobis, orate pro nobis); each invocation set to the formula printed on p. 126 for Sancta Maria (singular) and on p. 127 for Omnes sancti Angeli (plural), which have the same notes for the invocation: recitation on G, the last accent on A, the syllables after it on G. Sancte Joseph is set to this general formula (Jó-seph), not to the Michael formula; the book does not say'},
  '(c4) ' + S.slice(iJB, iDom).map(saintLine).join(' '));
file('lit_sancti_dominice', {name: 'Litaniae Sanctorum: Sancte Pater Dominice ... Omnes Sancti', 'office-part': 'Litaniae', mode: '',
  book: BOOK('pp. 127-128', 'Litaniae Sanctorum'), transcriber: TR,
  commentary: 'given as text on pp. 127-128, after the rubric Vox exaltetur (the voice is raised: the book gives no other notes); each invocation set to the formula printed on p. 126 (singular) and p. 127 (plural): recitation on G, the last accent on A, the syllables after it on G'},
  '(c4) ' + S.slice(iDom + 1, iProp).map(saintLine).join(' '));
const iLib = idx(r => r[0].startsWith('A damnatióne')), iPec = idx(r => r[0].startsWith('Peccatóres')), iAg = idx(r => r[0].startsWith('Agnus'));
file('lit_libera', {name: 'Litaniae Sanctorum: A damnatione perpetua ... In die judicii, libera nos, Domine', 'office-part': 'Litaniae', mode: '',
  book: BOOK('pp. 128-129', 'Litaniae Sanctorum'), transcriber: TR,
  commentary: 'A damnatione perpetua is notated on p. 128; the others, given as text (libera.), are set to the formula printed there, as the book sets its example (A dam-na-ti-ó-ne per-pé-tu-a): recitation on C, the two syllables before the last accent on B and A, the accent and the syllables after it on C'},
  '(c3) ' + block(S.slice(iLib, iPec), 'libera', RESP.libera));
file('lit_rogamus', {name: 'Litaniae Sanctorum: Peccatores ... Fili Dei, te rogamus, audi nos', 'office-part': 'Litaniae', mode: '',
  book: BOOK('pp. 129-130', 'Litaniae Sanctorum'), transcriber: TR,
  commentary: 'Peccatores, te rogamus, audi nos is notated on p. 129; the others, given as text (te rogamus.), are set to the formula printed there, as the book sets its example (Pec-ca-tó-res): recitation on C (do, c3 clef), the syllable before the last accent on B, the accent and the syllables after it on D. Ut omnes errantes, added after 1913, is typed below p. 129 in the scanned copy; it is set to the same formula and labelled'},
  '(c3) ' + S.slice(iPec, iAg).filter(r => r[0] !== '*').map(r => (r[0].startsWith('Ut omnes errántes') ? '<i>Added after 1913, typed into the scanned copy:</i>() ' : '') +
    F.rogamus(fix(r[0])) + ' (::) ' + RESP.rogamus + ' (::)').join(' '));

// The versicles and prayers (Rogations p. 125, Loreto p. 95, and the rest) are made by gen_tones.js (tone_*.gabc),
// the extraordinary processions (pp. 131-134, ex_*.gabc) by their own generator. This file makes only the litanies.
console.log('done');
