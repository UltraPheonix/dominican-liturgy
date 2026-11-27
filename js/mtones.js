/* The priest's and ministers' tones at Mass in the Order of Preachers: the prayers (Collect, Postcommunion)
   and the Epistle and Gospel. Source: J. Harrison O.P., How to Sing Plain Chant, chiefly for the use of
   Dominican Choirs (S. Dominic's Press, 1920), ch. VI: 2 "Prayers at Vespers, Lauds, and Mass" (pp. 66-67),
   5 "The Epistle" (pp. 73-77), 6 "The Gospel" (p. 77); written "in accordance with the Regulae Cantus" O.P.
   F clef on the third line: FA = h (the reciting note), MI = g, RE = f, SOL = i.
   Every function returns GABC (with its clef) for exsurge. Needs js/psalm.js (OPPsalm.analyse). */
(function () {
  'use strict';
  var root = typeof self !== 'undefined' ? self : globalThis;
  var FA = 'h', MI = 'g', RE = 'f', SOL = 'i';
  // monosyllables that lean on the next word and carry no accent
  var PROCLITIC = /^(in|ad|ab|a|e|ex|de|cum|per|pro|sub|præ|ob|et|ac|ut|nec|si|sed|aut|vel|ne|nam|qui|quæ|quod|quo|qua|sic|tam|jam|iam|non|te|me|se|tu|nos|vos)$/i;

  function plain(t) {
    return String(t || '').replace(/<[^>]+>/g, '').replace(/[()\[\]«»“”"]/g, '').replace(/\s+[-–—]\s+/g, ', ')
      .replace(/\s+/g, ' ').trim();
  }
  // syllables with accents: monosyllables other than proclitics count as accented (Harrison p. 74: "est", "sunt")
  function syls(text) {
    var s = root.OPPsalm.analyse(text);
    s.forEach(function (x) {
      var w = x.t.replace(/[^A-Za-zÀ-ÿæœǽÆŒǼ]/g, '');
      x.a = x.acc || (x.mono && !PROCLITIC.test(w));
    });
    return s;
  }
  function out(s, notes) {
    return s.map(function (x, i) { return x.t + '(' + notes[i] + ')' + (x.last ? ' ' : ''); }).join('').trim();
  }
  function accents(s) { var a = []; s.forEach(function (x, i) { if (x.a) a.push(i); }); return a; }
  // split at punctuation, keeping it: [{t, p}] where p is the last mark
  function pieces(text, re) {
    var o = [], m, r = new RegExp('[^' + re + ']+[' + re + ']*', 'g');
    while ((m = r.exec(text))) { var t = m[0].trim(); if (t) o.push({t: t, p: (/[.:;,?!]$/.exec(t) || [''])[0]}); }
    return o;
  }

  // ------------------------------------------------------------------ prayers (Harrison pp. 66-67)
  // Inflexion: descend after the last accent (FA ... MI MI)
  function inflexion(t) {
    var s = syls(t), n = s.map(function () { return FA; }), a = accents(s), L = a.length ? a[a.length - 1] : s.length - 1;
    for (var i = L + 1; i < s.length; i++) n[i] = MI;
    return out(s, n);
  }
  // Mediation: descend after the penultimate accent, rise again on the last accent
  function mediationPr(t) {
    var s = syls(t), n = s.map(function () { return FA; }), a = accents(s);
    if (a.length >= 2) for (var i = a[a.length - 2] + 1; i < a[a.length - 1]; i++) n[i] = MI;
    return out(s, n);
  }
  var TERM = 'per(h) óm(i)ni(h)a(h) sǽ(h)cu(g)la(g) sæ(g)cu(h)ló(hg)rum.(g)';
  function oration(text, o) {
    var t = plain(text);
    var body = t, concl = '';
    var cm = /\s((?:Per (?:eúndem |eumdem )?Dóminum|Per Christum|Qui (?:tecum|vivis|cum Patre|vivit|venturus))\b.*)$/.exec(t);
    if (cm) { body = t.slice(0, cm.index).trim(); concl = cm[1]; }
    // Orémus: Harrison p. 67 (sung apart, after Dóminus vobíscum, when o.noOremus)
    var g = o && o.noOremus ? '(f3) ' : '(f3) O(h)ré(gh)mus.(h) (::) ';
    // the body: the Mediation immediately before the Conclusion, an Inflexion before it, a Mediation before that ...
    var ms = pieces(body, ':;?');
    if (ms.length > 1 && ms[ms.length - 1].t.length < 12) { ms[ms.length - 2].t += ' ' + ms[ms.length - 1].t; ms.pop(); }
    ms.forEach(function (x, i) {
      var back = ms.length - 1 - i, med = back % 2 === 0;
      g += (med ? mediationPr(x.t) : inflexion(x.t)) + (back === 0 ? ' (:) ' : (med ? ' (:) ' : ' (;) '));
    });
    if (concl) {
      // the long conclusion: Inflexion at tuum / Patre, Mediation at Sancti Deus, the Termination
      var c = /^(.*?(?:tuum|Patre|Patri)[,:]?)\s+(.*?Deus,?)\s+(per ómnia sǽcula sæculórum\.?)$/i.exec(concl);
      var c2 = /^(.*?Deus,?)\s+(per ómnia sǽcula sæculórum\.?)$/i.exec(concl);
      if (c) g += inflexion(c[1]) + ' (;) ' + mediationPr(c[2]) + ' (:) ' + TERM;
      else if (c2) g += mediationPr(c2[1]) + ' (:) ' + TERM;
      else g += mediationPr(concl.replace(/\.$/, '')) + '.';   // Per Christum Dóminum nostrum (short conclusion)
      g += ' (::) <sp>R/</sp>. A(g)men.(h) (::)';
    }
    return g;
  }

  // ------------------------------------------------------------------ Epistle and Gospel (Harrison pp. 73-77)
  // Mediation (at a colon): unaccented syllables just before the penultimate accent on RE (accented ones on FA),
  // the penultimate accent on FA, then MI up to the final syllable, which is on FA
  function mediationL(t) {
    var s = syls(t), n = s.map(function () { return FA; }), a = accents(s), L = s.length - 1, i;
    if (a.length < 2) { for (i = 0; i < L; i++) n[i] = RE; return out(s, n); }   // Fratres: Caríssimi:
    var A1 = a[a.length - 2];
    for (i = A1 + 1; i < L; i++) n[i] = MI;
    for (i = A1 - 1; i >= 0 && !s[i].a; i--) n[i] = RE;
    return out(s, n);
  }
  // the penultimate accent of a termination, natural or adventitious
  function penult(s, A2) {
    for (var i = A2 - 2; i >= 0; i--) if (s[i].a) return i;
    return A2 >= 2 ? A2 - 2 : A2 - 1;
  }
  function lastAccent(s) {
    if (!s.length) return -1;
    var a = accents(s), A2 = a.length ? a[a.length - 1] : s.length - 1;
    if (A2 === s.length - 1 && s[A2].mono && s.length > 1) {                     // a monosyllable at the end
      for (var i = s.length - 2; i >= 0; i--) if (s[i].a && !s[i].mono) return i;
    }
    return A2;
  }
  // Epistle: from the penultimate accent the podatus FA-SOL, MI before the last accent, RE on it and after, MI last
  function termEp(t) {
    if (!syls(t).length) return '';
    var s = syls(t), n = s.map(function () { return FA; }), L = s.length - 1, A2 = lastAccent(s), A1 = penult(s, A2), i;
    if (A1 >= 0) n[A1] = FA + SOL;
    if (A2 - 1 > A1) n[A2 - 1] = MI;
    for (i = A2; i < L; i++) n[i] = RE;
    n[L] = MI;
    return out(s, n);
  }
  // Gospel: from FA to MI at the last accent and all the syllables after it
  function termEv(t) {
    if (!syls(t).length) return '';
    var s = syls(t), n = s.map(function () { return FA; }), A2 = lastAccent(s);
    for (var i = A2; i < s.length; i++) n[i] = MI;
    return out(s, n);
  }
  // questions: on MI, the last syllable FA (a final monosyllable MI-FA)
  function question(t) {
    var s = syls(t), n = s.map(function () { return MI; }), L = s.length - 1;
    n[L] = s[L].mono ? MI + FA : FA;
    return out(s, n);
  }
  // the conclusion: two phrases; in the first the syllables between its last two accents on RE; in the second
  // MI on the syllable before the last accent (both syllables after the accent of a dactyl)
  function conclusion(t) {
    var s = syls(t), n = s.map(function () { return FA; });
    // the short pause: the last comma, or else the word boundary nearest the middle
    var words = t.split(' '), cut = -1, acc = 0, k;
    for (k = words.length - 2; k >= 1; k--) if (/[,;:]$/.test(words[k])) { cut = k + 1; break; }
    if (cut < 0) { cut = Math.max(1, Math.round(words.length / 2)); }
    if (words.length < 3 || cut >= words.length) return termEp(t);
    var first = words.slice(0, cut).join(' '), second = words.slice(cut).join(' ');
    var s1 = syls(first), s2 = syls(second);
    var n1 = s1.map(function () { return FA; }), n2 = s2.map(function () { return FA; });
    var a1 = accents(s1);
    if (a1.length >= 2) for (k = a1[a1.length - 2] + 1; k < a1[a1.length - 1]; k++) n1[k] = RE;
    var A2 = lastAccent(s2);
    if (A2 >= 1) {
      n2[A2 - 1] = MI;
      // the syllable before the accent closes a dactyl (Dóminum nostrum): its two last syllables on MI
      if (s2[A2 - 1].last && A2 >= 3 && s2[A2 - 3].a && !s2[A2 - 3].mono && s2[A2 - 3].word === s2[A2 - 1].word) n2[A2 - 2] = MI;
    }
    return out(s1, n1) + ' (,) ' + out(s2, n2);
  }
  // a reading: sentences end in a termination (or a question), colons take a mediation, the last sentence the conclusion
  function reading(text, gospel) {
    var t = plain(text).replace(/\s*\d+\s*/g, ' ');
    var sents = pieces(t, '.?!'), g = '(f3) ';
    // a last word standing alone (Amen.) belongs to the sentence before it
    if (sents.length > 1 && sents[sents.length - 1].t.split(' ').length <= 1) { var z = sents.pop(); sents[sents.length - 1].t += ' ' + z.t; sents[sents.length - 1].p = z.p; }
    sents.forEach(function (S, si) {
      var lastS = si === sents.length - 1;
      var parts = pieces(S.t, ':;');
      parts.forEach(function (P, pi) {
        var lastP = pi === parts.length - 1;
        if (!lastP) { g += mediationL(P.t) + ' (;) '; return; }
        if (S.p === '?') g += question(P.t) + (lastS ? ' (::)' : ' (:) ');
        else if (lastS) g += conclusion(P.t) + ' (::)';
        else g += (gospel ? termEv(P.t) : termEp(P.t)) + ' (:) ';
      });
    });
    return g;
  }
  // the title of the Epistle: "... beáti Pauli Apóstoli: ad Romános." (Harrison's examples p. 73, 75)
  function epistleTitle(t) {
    t = plain(t);
    var m = /^(.*Apóstoli)\s+(ad\s.*)$/i.exec(t);
    if (m) return '(f3) ' + mediationL(m[1] + ':') + ' (;) ' + termEp(m[2]) + ' (::)';
    return '(f3) ' + termEp(t) + ' (::)';
  }
  // the announcement of the Gospel: Graduale O.P. (1950), Modus respondendi in Missa, p. 147* ("Ad Evangelium",
  // printed with Lucam: Lu(g)cam(g)); the other names take the same cadence, MI from their accent
  var EVN = {Matthæus: 'Mat(h)thǽ(g)um.(g)', Marcus: 'Mar(g)cum.(g)', Lucas: 'Lu(g)cam.(g)', Joannes: 'Io(h)án(g)nem.(g)', Ioannes: 'Io(h)án(g)nem.(g)'};
  function sequentia(book) {
    var n = EVN[book]; if (!n) return null;
    return '(f3) Se(h)quén(h)ti(h)a(h) san(h)cti(f) E(h)van(g)gé(g)li(g)i(h) (;) se(h)cún(h)dum(h) ' + n + ' (::) ' +
      '<sp>R/</sp>. Gló(h)ri(h)a(h) ti(h)bi(h) Dó(g)mi(g)ne.(g) (::)';
  }
  root.OPMassTones = {oration: oration, sequentia: sequentia, reading: reading, epistleTitle: epistleTitle,
    _: {mediationL: mediationL, termEp: termEp, termEv: termEv, question: question, conclusion: conclusion, inflexion: inflexion, mediationPr: mediationPr}};
})();

/* The same tones as the Processionarium O.P. (1913) prints them: Art. III "Modus cantandi Capitula, Orationes,
   Benedictiones, Lectiones, Epistolas, Evangelia", pp. 402-430 (pdf = printed + 16). F clef on the 3rd line:
   FA = h (the reciting note), MI = g, RE = f, SOL = i, LA = c. New functions only (the ones above, after Harrison,
   stay as they are for the pages that use them). Every function returns GABC beginning '(f3) '.
     orationProc(text, {tone: 'mass'|'hours', dv, oremus, noOremus, amen, flectamus, pointing})
         pointing: 'book' = take ";" (or † ‡) as flexio and ":" as elevatio, as a book prints them; otherwise they
         alternate back from the final elevatio. final: 'flex' = a prayer without conclusion that ends on a flexio
         (Triduum 1927 p. 205, Respice)
         'mass'  = II  "Orationes ad Vesperas, Laudes et Missam", pp. 404-406
         'hours' = III "Orationes ad Horas, et quotiescumque aliae Orationes quae non sunt de corpore Officii et
                        Missae", pp. 407-408 (blessings, processions, absolution, altar of repose)
     lessonProc(text, {title, pointing})  IV  Lessons and the prophecies at Mass, pp. 408-413 (end by n. 11)
     readingProc(text, gospel)        V   Epistle, pp. 414-419; VI Gospel, pp. 424-426 (same call shape as reading)
     epistleProc(text, {title}), gospelProc(text, {book, dv})
     epistleTitleProc(title)          p. 414 (mediation at "Apóstoli :") and p. 417 (Ad Romános.)
   Differences from Harrison (1920) found on the pages: Hebrew names keep the accent on the last syllable (p. 417 Amós,
   p. 419 Je-sú, p. 424 Je-sú, p. 425 Jacób, David, p. 418 Israél); a final monosyllable takes the cadence alone
   (p. 418 Dóminus est., p. 425 Non sum.); the run of accents before the penultimate accent of a mediation stays on FA
   and only the unaccented run before it goes to RE (p. 425 Ho-san-ná fí-li-o Da-víd :); long words at the end of
   a mediation take a secondary accent (p. 415, p. 424 E-van-gé-li-i); the final modulation rises RE-FA on the last
   accent before the pause (p. 419 enar-rá-bit, p. 426 spí-ri-tum bó-num). */
(function () {
  'use strict';
  var root = typeof self !== 'undefined' ? self : globalThis;
  var T = root.OPMassTones; if (!T) return;
  var FA = 'h', MI = 'g', RE = 'f', SOL = 'i', LA = 'c';
  // prepositions and conjunctions "quæ ex se accentum non habent" (p. 416); other monosyllables are accented
  // (p. 411 cor méum, non áliud; p. 418 Spem non habent, quem dévoret; p. 426 peténtibus se)
  var UNACC = /^(in|ad|ab|abs|a|e|ex|de|cum|per|pro|sub|super|præ|ob|post|et|ac|atque|ut|nec|neque|si|sed|aut|vel|ne|nam|seu|sive|dum)$/i;
  // Hebrew names, accented on the last syllable when the Missal prints no accent on them (pp. 409-425)
  var HEB = {jesus: 1, jesu: 1, jesum: 1, iesus: 1, iesu: 1, iesum: 1, israel: ['Is', 'ra', 'el'], david: 1, jacob: 1, iacob: 1,
    sion: 1, nathan: 1, jesse: 1, iesse: 1, aaron: ['A', 'a', 'ron'], edom: 1, bosra: 1, ephraim: ['E', 'phra', 'im'],
    emmanuel: ['Em', 'ma', 'nu', 'el'], acharon: 1, amos: 1, sichem: 1, gad: 1, isaac: ['I', 'sa', 'ac'], abraham: 1,
    joseph: 1, ioseph: 1, amen: 1, nephtali: 1, sinai: ['Si', 'na', 'i'], cedron: 1, ephrem: 1, juda: 1, iuda: 1, levi: 1,
    adam: 1, noe: ['No', 'e'], jerusalem: 1, ierusalem: 1, bethlehem: 1, nazareth: 1, sabaoth: 1, eloi: ['E', 'lo', 'i'],
    gabbatha: 1, golgotha: 1, cedar: 1, jordan: 1, iordan: 1, achaz: 1, sabbath: 1};
  // printed with an accent in the Missal but sung with the Hebrew final accent (Proc. p. 418 Jerúsa-lém, p. 425)
  var FINAL = {jerusalem: 1, ierusalem: 1};
  var ACUTE = /[áéíóúýǽÁÉÍÓÚÝǼ]/;
  function bare(w) { return w.replace(/[^A-Za-zÀ-ÿæœǽÆŒǼ]/g, ''); }
  function fold(w) { return bare(w).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ë/g, 'e'); }
  function plain(t) {
    return String(t || '').replace(/<[^>]+>/g, '').replace(/[{}()\[\]«»“”"‘’^*†✠]/g, '').replace(/\s+[-–—]\s+/g, ', ')
      .replace(/\s+/g, ' ').trim();
  }
  // syllables, word by word: {t, w (word index), a (accented), mono, heb, last (last of its word), wa (accent index in word), wn}
  function syls(text) {
    var words = String(text).trim().split(/\s+/).filter(function (w) { return /[A-Za-zÀ-ÿǼǽ]/.test(w); }), out = [];
    words.forEach(function (w, wi) {
      var f = fold(w), h = HEB[f], parts;
      if (Array.isArray(h) && !ACUTE.test(w)) {
        // split the written word at the given syllables, keeping its punctuation
        var lead = /^[^A-Za-zÀ-ÿæœǽÆŒǼ]*/.exec(w)[0], tail = /[^A-Za-zÀ-ÿæœǽÆŒǼ]*$/.exec(w)[0], core = w.slice(lead.length, w.length - tail.length), k = 0;
        parts = h.map(function (p) { var s = core.substr(k, p.length); k += p.length; return s; });
        parts[0] = lead + parts[0]; parts[parts.length - 1] += core.slice(k) + tail;
      } else {
        parts = [];
        // an accented vowel before another vowel is a syllable of its own (I-sa-í-æ, p. 417)
        root.OPPsalm.analyse(w).forEach(function (x) { x.t.replace(/([áéíóúý])([aeiouyæœ])/g, function (m0, v1, v2) { return /^[áé]u$/i.test(v1 + v2) ? m0 : v1 + '\u0001' + v2; }).split('\u0001').forEach(function (q) { parts.push(q); }); });
        // "ii" is two syllables: á-bi-i, i-is
        for (var k = 0; k < parts.length; k++) if (/^[iIíÍ]i/.test(parts[k].replace(/^[^A-Za-zÀ-ÿ]+/, ''))) {
          var q = parts[k], lead2 = /^[^A-Za-zÀ-ÿ]*/.exec(q)[0], body2 = q.slice(lead2.length);
          if (k > 0 && /[^aeiouyáéíóúýæœǽ]$/i.test(parts[k - 1])) {
            var c = parts[k - 1].slice(-1); parts[k - 1] = parts[k - 1].slice(0, -1);
            parts.splice(k, 1, c + body2.charAt(0), body2.slice(1));
          } else parts.splice(k, 1, lead2 + body2.charAt(0), body2.slice(1));
          k++;
        }
      }
      var n = parts.length, acc = -1;
      if (n === 1) acc = UNACC.test(bare(w)) ? -1 : 0;
      else {
        parts.forEach(function (p, i) { if (ACUTE.test(p)) acc = i; });
        if (h && (acc < 0 || FINAL[f])) acc = n - 1;   // Hebrew: the last syllable (Jerúsa-lém, pp. 415, 418, 425)
        if (acc < 0) acc = n === 2 ? 0 : n - 3;
      }
      parts.forEach(function (p, i) {
        out.push({t: p, w: wi, a: i === acc, mono: n === 1, heb: !!h && (!ACUTE.test(w) || !!FINAL[f]) && n > 1, h3: !!h && n === 3, first: i === 0, last: i === n - 1, wa: acc, wn: n, wi: i});
      });
    });
    return out;
  }
  function out(s, n) { return s.map(function (x, i) { return x.t + '(' + n[i] + ')' + (x.last ? ' ' : ''); }).join('').trim(); }
  function accs(s) { var a = []; s.forEach(function (x, i) { if (x.a) a.push(i); }); return a; }
  function fill(s, v) { return s.map(function () { return v; }); }
  // the last syllable is accented: a monosyllable (not a preposition) or a Hebrew name
  function finalAcc(s) { var L = s.length - 1; return L >= 0 && s[L].a && s[L].last && (s[L].mono || s[L].heb); }
  // members ending at the given marks: [{t, p}]
  function pieces(text, marks) {
    var o = [], m, r = new RegExp('[^' + marks + ']+[' + marks + ']*', 'g');
    while ((m = r.exec(text))) { var t = m[0].trim(); if (t && /[A-Za-zÀ-ÿǽ]/.test(t)) o.push({t: t, p: (/[.:;,?!]$/.exec(t) || [''])[0]}); else if (t && o.length) o[o.length - 1].t += t; }
    return o;
  }
  // a colon after the words that bring in direct speech ends the verse (p. 411, n. 6; p. 417, 4°)
  var SAYS = /\b(dicit|dixit|dixérunt|dixerunt|dicunt|dicens|dicéntes|dicentes|ait|aiunt|inquit|respóndit|respondit|respondérunt|respondens|respóndens|clamábant|clamavérunt|clamávit|loquútus|locútus|dícite|dicite|dicat|dicam|dico|dicébant|interrogávit|exclamávit|orávit|dicéntem|scriptum est|clamans|clamávit)\b[^:]*:$/i;
  function speech(member, next) { return !!next && SAYS.test(member) && /^[A-ZÀ-ÝÆŒǼ]/.test(next.replace(/^[^A-Za-zÀ-ÿǽ]+/, '')); }
  // split the conclusion from the body of a prayer
  var CONCL = /\s((?:Per (?:eúndem |eúmdem |eumdem |eundem )?(?:Dóminum|Dominum|Christum)|Qui (?:tecum|vivis|cum Patre|vivit|venturus|cum Deo))\b.*)$/;

  // ================================================================ Orations: tones II and III (pp. 404-408)
  // FLEXIO at ";": II the syllables after the last accent to MI (Fí-li-um tú-um(g) ;), III to RE (tri-stí-ti-a(f) ;)
  function flexO(t, III) {
    var s = syls(t), n = fill(s, FA), a = accs(s);
    if (!a.length || finalAcc(s)) return out(s, n);
    for (var i = a[a.length - 1] + 1; i < s.length; i++) n[i] = III ? RE : MI;
    return out(s, n);
  }
  // ELEVATIO at ":": two syllables before the last accent (three, if the third is the middle of a dactyl: pér-fru-i
  // læ-tí-ti-a) to MI (III: the last of them to RE), the accent and the rest back on FA (p. 405, p. 407)
  function elevO(t, III) {
    var s = syls(t), n = fill(s, FA), a = accs(s);
    if (!a.length) return out(s, n);
    var A = a[a.length - 1], k = 2;
    if (A >= 3) { var x = s[A - 3]; if (!x.first && !x.last && s[A - 3].wa === x.wi - 1 && x.wn - x.wa === 3) k = 3; }
    for (var i = Math.max(0, A - k); i < A; i++) n[i] = MI;
    if (III && A >= 1) n[A - 1] = RE;
    return out(s, n);
  }
  // the Missal prints the conclusions shortened; they are sung whole (p. 406). "ejúsdem" when the prayer names the Holy
  // Spirit (Missal, Rubr. gen.: "si in Oratione facta fuerit mentio Spiritus Sancti, terminatur in unitate ejusdem
  // Spiritus Sancti"), or when the Missal prints it; a conclusion printed with "in unitáte Spíritus" keeps what it prints
  function expandConcl(c, body) {
    c = c.replace(/\s*(\.\.\.|…)\s*/g, ' ').replace(/[.\s]+$/, '').trim();
    var named = /in unitáte/.exec(c);
    var sp = named ? (/ejúsdem/.test(c) ? 'ejúsdem ' : '') : (/Spírit\S* Sanct|Sanct\S* Spírit|Paráclit/.test(body) ? 'ejúsdem ' : '');
    var U = 'in unitáte ' + sp + 'Spíritus Sancti Deus: per ómnia sǽcula sæculórum.';
    if (/sæculórum|saeculorum/.test(c) || /\bDeus$/.test(c)) return c + '.';
    var m = /^Per (eúmdem |eúndem |eumdem |eundem )?(Dóminum|Dominum)?\b/.exec(c);
    if (m && !/^Per (eúmdem |eúndem )?Christum/.test(c)) return 'Per ' + (m[1] || '') + 'Dóminum nostrum Jesum Christum Fílium tuum; qui tecum vivit et regnat ' + U;
    if (/^Qui tecum vivit/.test(c)) return 'Qui tecum vivit et regnat ' + U;
    if (/^Qui vivis et regnas per ómnia/.test(c)) return 'Qui vivis et regnas per ómnia sǽcula sæculórum.';
    if (/^Qui vivis( et regnas)?( cum Deo Patre)?$/.test(c)) return 'Qui vivis et regnas cum Deo Patre; ' + U;
    if (/^Qui cum Patre/.test(c)) return 'Qui cum Patre et eódem Spíritu Sancto vivis et regnas Deus: per ómnia sǽcula sæculórum.';
    if (/^Per (eúmdem |eúndem )?Christum$/.test(c)) return c + ' Dóminum nostrum.';
    return c + '.';
  }
  // the inflexions alternate back from the end, which always has the elevatio (p. 405, 2°); with byMarks the book's
  // own pointing decides: ";" (or the flex sign †) a flexio, ":" an elevatio (as printed in Proc. pp. 20-21, Triduum 1927)
  function body(members, III, byMarks, endFlex) {
    var g = '';
    members.forEach(function (x, i) {
      var back = members.length - 1 - i, elev = byMarks ? ((back === 0 && !endFlex) || x.p !== ';') : (back % 2 === 0) !== !!endFlex;
      g += (elev ? elevO(x.t, III) : flexO(x.t, III)) + (elev ? ' (;) ' : ' (,) ');
    });
    return g;
  }
  function conclO(c, III) {
    var m, g = '';
    // short conclusions (p. 406, 4°; p. 408)
    if ((m = /^(.*?)\bChristum Dóminum nostrum\.?$/.exec(c))) {
      var pre = m[1].trim();
      if (pre) g += out(syls(pre), fill(syls(pre), FA)) + ' ';
      return g + (III ? 'Chris(h)tum(h) Dó(h)mi(h)num(h) nos(h)trum.(f)' : 'Chris(i)tum(h) Dó(h)mi(g)num(g) nos(h)trum.(h)');
    }
    if (/^Qui vivis et regnas per ómnia/.test(c)) return III ? 'Qui(h) vi(h)vis(h) et(h) reg(h)nas(h) per(h) óm(h)ni(h)a(h) sǽ(h)cu(h)la(h) sæ(h)cu(h)ló(h)rum.(f)'
      : 'Qui(h) vi(h)vis(h) et(h) reg(h)nas(h) per(h) óm(i)ni(h)a(h) sǽ(h)cu(h)la(h) sæ(g)cu(g)ló(h)rum.(h)';
    // long conclusions (p. 406, 3°; p. 408): [flexio] ; [elevatio] Deus : per ómnia sǽcula sæculórum.
    var TERM = III ? 'per(h) óm(h)ni(h)a(h) sǽ(h)cu(h)la(h) sæ(h)cu(h)ló(h)rum.(f)' : 'per(h) óm(i)ni(h)a(h) sǽ(h)cu(g)la(g) sæ(g)cu(h)ló(hg)rum.(g)';
    var k = c.search(/\s*:?\s*per ómnia sǽcula sæculórum\.?$/);
    if (k < 0 && /\bDeus\.?$/.test(c)) {    // written out up to "Deus." (the Per ómnia follows in the Preface tone)
      var ps0 = c.replace(/\.$/, '').split(/[;,]\s*(?=qui )/);
      return (ps0.length > 1 ? flexO(ps0[0] + ';', III) + ' (,) ' : '') + elevO(ps0[ps0.length - 1] + '.', III);
    }
    if (k < 0) {   // any other ending: recited, flexio/elevatio by its punctuation, the last member an elevatio
      return body(pieces(c, ':;'), III).replace(/ \(;\) $/, '.(::)').replace(/\(::\)$/, '').trim();
    }
    var head = c.slice(0, k).trim().replace(/[:,]$/, '');
    var ps = head.split(/;\s*/);
    if (ps.length > 1) g += flexO(ps[0] + ';', III) + ' (,) ';
    var last = ps[ps.length - 1] + ':';
    g += elevO(last, III) + ' (;) ';       // II sanc(g)ti(g) Dé(h)us(h) :  III sanc(g)ti(f) Dé(h)us(h) :
    return g + TERM;
  }
  function orationProc(text, o) {
    o = o || {};
    var III = o.tone === 'hours' || o.tone === 'III';
    var t = plain(String(text || '').replace(/\s*[†‡]/g, ';')).replace(/\s*\.\s*$/, '.');
    var b = t, c = '', cm = CONCL.exec(t);
    if (cm) { b = t.slice(0, cm.index).trim(); c = expandConcl(cm[1], b); }
    var g = '(f3) ';
    if (o.dv) g += III ? 'Dó(h)mi(h)nus(h) vo(h)bís(h)cum.(f) (::) <sp>R/</sp>. Et(g) cum(g) spí(g)ri(g)tu(g) tu(g)o.(h) (::) '
      : 'Dó(g)mi(h)nus(h) vo(gh)bís(hg)cum.(g) (::) <sp>R/</sp>. Et(g) cum(h) spí(h)ri(g)tu(g) tu(h)o.(h) (::) ';
    var orem = o.oremus != null ? !!o.oremus : !o.noOremus;
    if (orem) g += III ? 'O(h)ré(h)mus.(f) (::) ' : 'O(h)ré(gh)mus.(h) (::) ';
    if (o.flectamus) g += 'Flec(f)tá(h)mus(i) gé(i)nu(h)a.(h) (::) Le(f)vá(hi)te.(i) (::) ';
    // the body: commas take no inflexion; ; and : and a full stop inside the prayer divide it (p. 405, 2°)
    var ms = pieces(b, ':;.?!');
    if (ms.length > 1 && ms[ms.length - 1].t.split(' ').length < 3) { var z = ms.pop(); ms[ms.length - 1].t += ' ' + z.t; }
    g += body(ms, III, o.pointing === 'book', o.final === 'flex');
    if (c) {
      g += conclO(c, III) + ' (::)';
      if (o.amen !== false) g += ' <sp>R/</sp>. A(g)men.(h) (::)';
    } else g = g.replace(/ \([;,]\) $/, ' (::)');
    return g.replace(/\s+/g, ' ').trim();
  }

  // ================================================================ Lessons and prophecies: IV (pp. 408-413)
  // FLEX: the syllables after the last accent to RE; none after a monosyllable or Hebrew name (p. 409)
  function flexL(t) {
    var s = syls(t), n = fill(s, FA), a = accs(s);
    if (!a.length || finalAcc(s)) return out(s, n);
    for (var i = a[a.length - 1] + 1; i < s.length; i++) n[i] = RE;
    return out(s, n);
  }
  // MEDIATION: the two syllables before the last accent MI RE (one: RE), the accent and the rest FA; a final
  // monosyllable or Hebrew name: the last three syllables MI RE FA (pp. 409-410)
  function medL(t) {
    var s = syls(t), n = fill(s, FA), a = accs(s), L = s.length - 1;
    if (finalAcc(s)) { if (L >= 1) n[L - 1] = RE; if (L >= 2) n[L - 2] = MI; return out(s, n); }
    if (!a.length) return out(s, n);
    var A = a[a.length - 1];
    if (A >= 1) n[A - 1] = RE;
    if (A >= 2) n[A - 2] = MI;
    return out(s, n);
  }
  // TERMINATION (pp. 410-411): the unaccented syllable before the last accent RE (two, if it ends a dactyl), the accent
  // MI, the rest LA; an accented syllable before it stays FA; a final monosyllable or Hebrew name: RE before it, MI on it
  function termL(t) {
    var s = syls(t), n = fill(s, FA), a = accs(s), L = s.length - 1, i;
    if (!s.length) return '';
    if (finalAcc(s)) {
      n[L] = MI;
      if (L >= 1) { n[L - 1] = RE; if (L >= 3 && s[L - 1].last && s[L - 1].wn - s[L - 1].wa === 3) n[L - 2] = RE; }
      return out(s, n);
    }
    var A = a.length ? a[a.length - 1] : 0;
    n[A] = MI; for (i = A + 1; i <= L; i++) n[i] = LA;
    if (A >= 1 && !(s[A - 1].a && (s[A - 1].mono || s[A - 1].heb || s[A - 1].last))) {
      n[A - 1] = RE;
      var p = s[A - 1];
      if (p.last && p.wn - p.wa === 3 && A >= 2) n[A - 2] = RE;       // Grá-ti-a ple-na, Dó-mi-nus Dé-us
    }
    return out(s, n);
  }
  // the end of a lesson without Tu autem (n. 11, p. 413), and of a Gospel verse (p. 424): a semitone down on the last
  // accent and the syllables after it
  function semiL(t) {
    var s = syls(t), n = fill(s, FA), a = accs(s);
    if (!s.length) return '';
    var A = finalAcc(s) ? s.length - 1 : (a.length ? a[a.length - 1] : 0);
    for (var i = A; i < s.length; i++) n[i] = MI;
    return out(s, n);
  }
  // QUESTION (n. 9, p. 412): as the mediation, but the accent only to MI and the syllables after it FA; a final
  // monosyllable or Hebrew name MI-FA joined
  function questL(t) {
    var s = syls(t), n = fill(s, FA), a = accs(s), L = s.length - 1;
    if (finalAcc(s)) { n[L] = MI + FA; if (L >= 1) n[L - 1] = RE; if (L >= 2) n[L - 2] = MI; return out(s, n); }
    if (!a.length) return out(s, n);
    var A = a[a.length - 1];
    n[A] = MI;
    if (A >= 1) n[A - 1] = RE;
    if (A >= 2) n[A - 2] = MI;
    return out(s, n);
  }
  // verses: up to . ? ! or a colon that brings in direct speech; inside, the mediation before the end, a flex before
  // that, alternately (p. 409, 3°)
  function verses(t) {
    var ms = pieces(t, ':;.?!'), vs = [], cur = [];
    ms.forEach(function (m, i) {
      cur.push(m);
      var nx = ms[i + 1];
      if (/[.?!]/.test(m.p) || !nx || (m.p === ':' && speech(m.t, nx.t))) { vs.push(cur); cur = []; }
    });
    if (cur.length) vs.push(cur);
    // a last word standing alone (Amen.) belongs to the verse before it
    if (vs.length > 1 && vs[vs.length - 1].length === 1 && vs[vs.length - 1][0].t.split(' ').length <= 1) { var z = vs.pop(); var lv = vs[vs.length - 1]; lv[lv.length - 1].t += ' ' + z[0].t; lv[lv.length - 1].p = z[0].p; }
    return vs;
  }
  function lessonProc(text, o) {
    o = o || {};
    var g = '(f3) ';
    if (o.title) g += termL(plain(o.title)) + ' (:) ';
    var vs = verses(plain(String(text || '').replace(/\s*[†‡]/g, ';')).replace(/\s*\d+\s*/g, ' '));
    vs.forEach(function (v, vi) {
      var lastV = vi === vs.length - 1, q = v[v.length - 1].p === '?';
      v.forEach(function (m, mi) {
        var back = v.length - 1 - mi;
        if (o.pointing === 'book' && back > 0 && !q) { g += m.p === ';' ? flexL(m.t) + ' (,) ' : medL(m.t) + ' (;) '; return; }
        if (back === 0) {
          if (q) g += questL(m.t) + (lastV ? ' (::)' : ' (:) ');
          else if (lastV) g += semiL(m.t) + ' (::)';
          else g += termL(m.t) + ' (:) ';
        } else if (q) g += flexL(m.t) + ' (,) ';                        // in a question only the flex (n. 9)
        else if (back % 2 === 1) g += medL(m.t) + ' (;) ';
        else g += flexL(m.t) + ' (,) ';
      });
    });
    return g.trim();
  }

  // ================================================================ Epistle (V, pp. 414-419) and Gospel (VI, pp. 424-426)
  // accents for the end of a mediation: a long last word takes a secondary accent two syllables before its accent
  // (Hebrew of three syllables, Latin of four with a long penult or five with a short one; never a third, p. 415); a
  // preposition or conjunction before a last word of one accent takes one, if a syllable lies between (p. 416)
  function medAccents(s) {
    var L = s.length - 1; if (L < 1) return;
    var w = s[L].w, ws = [], i;
    for (i = 0; i <= L; i++) if (s[i].w === w) ws.push(i);
    var n = ws.length, wa = s[ws[0]].wa, sec = false;
    // a Hebrew name of three syllables: both its first and its last syllable (Néphta-lì, p. 415)
    if (s[ws[0]].h3) { s[ws[0]].a = true; s[ws[2]].a = true; return; }
    if (wa >= 2 && ((s[ws[0]].heb && n === 3) || (n - wa === 2 && n >= 4) || (n - wa === 3 && n >= 5))) { s[ws[0] + wa - 2].a = true; sec = true; }
    var p = ws[0] - 1;
    if (!sec && p >= 0 && s[p].mono && !s[p].a && wa >= 1) s[p].a = true;
  }
  // MEDIATION (p. 414): the penultimate accent FA, MI to the last syllable, which is FA; the accents just before the
  // penultimate stay FA, the unaccented syllables before them RE
  function medE(t) {
    var s = syls(t); medAccents(s);
    var n = fill(s, FA), a = accs(s), L = s.length - 1, i;
    // one accent only (Fratres :, Caríssimi :): RE up to the last syllable, which is FA (p. 416)
    if (a.length < 2) { for (i = 0; i < L; i++) n[i] = RE; return out(s, n); }
    var A1 = a[a.length - 2];
    for (i = A1 + 1; i < L; i++) n[i] = MI;
    i = A1 - 1;
    while (i >= 0 && s[i].a) i--;
    for (; i >= 0 && !s[i].a; i--) n[i] = RE;
    return out(s, n);
  }
  // the accent before the last one, or an adventitious one two syllables back (one, at the start)
  function prevAcc(s, A2) {
    for (var i = A2 - 1; i >= 0; i--) if (s[i].a) return i;
    return A2 >= 2 ? A2 - 2 : A2 - 1;
  }
  function lastAcc(s) { var a = accs(s); return finalAcc(s) ? s.length - 1 : (a.length ? a[a.length - 1] : 0); }
  // TERMINATION of the Epistle (p. 417): the penultimate accent FA-SOL, MI on the syllable before the last accent,
  // RE on the accent and after it, MI on the last syllable; a final monosyllable or Hebrew name: RE from the
  // penultimate accent to it, MI on it (p. 418 Dómi-nus est., In Isra-él.)
  function termE(t) {
    var s = syls(t); if (!s.length) return '';
    var n = fill(s, FA), L = s.length - 1, A2 = lastAcc(s), A1 = prevAcc(s, A2), i;
    if (A1 >= 0) n[A1] = FA + SOL;
    if (A2 === L && L > 0) { for (i = A1 + 1; i < L; i++) n[i] = RE; n[L] = MI; return out(s, n); }
    if (A2 - 1 > A1) n[A2 - 1] = MI;
    for (i = A2; i < L; i++) n[i] = RE;
    n[L] = MI;
    return out(s, n);
  }
  // QUESTION (p. 418, 5°): from the interrogative word on MI, the last syllable FA; a final monosyllable or Hebrew MI-FA
  var QW = /^(quis|quid|cur|quómodo|quomodo|quáre|quare|númquid|numquid|nonne|nónne|ubi|úbi|unde|únde|quando|quándo|quantum|quántum|quot|quare|utquid|ut quid|quem|quam|quæ|quo|qua|cujus|cuius|cui|quibus|qualis|quális|quómodo|an|quóusque|quousque|quámdiu|quamdiu|úsquequo|usquequo)$/i;
  function questE(t) {
    var s = syls(t), n = fill(s, FA), L = s.length - 1, st = 0, ws = t.split(' ');
    for (var k = 0; k < ws.length; k++) if (QW.test(bare(ws[k]).toLowerCase())) { st = k; break; }
    for (var i = 0; i <= L; i++) if (s[i].w >= st) n[i] = MI;
    n[L] = s[L].a && (s[L].mono || s[L].heb) ? MI + FA : FA;
    return out(s, n);
  }
  // the final modulation (p. 418, 6°; p. 426): two parts. The first: RE between its last two accents, the last accent
  // RE-FA joined, the rest FA; the second: MI on the syllable before its last accent (two after a dactyl), the accent
  // and the rest FA
  function finalE(t) {
    var words = t.split(' '), cut = -1, k;
    for (k = words.length - 2; k >= 1; k--) if (/[,;:]$/.test(words[k])) { if (words.length - 1 - k <= 4) cut = k + 1; break; }
    if (cut < 0) { cut = words.length - 2; if (cut >= 1 && syls(words[cut - 1]).length === 1 && !/[,;:]$/.test(words[cut - 1])) cut--; }
    if (cut < 1) return conclusion2(t);
    return part1(words.slice(0, cut).join(' ')) + ' (,) ' + conclusion2(words.slice(cut).join(' '));
  }
  function part1(t) {
    var s = syls(t), n = fill(s, FA), a = accs(s), i;
    if (!a.length) return out(s, n);
    var A2 = a[a.length - 1], A1 = a.length > 1 ? a[a.length - 2] : -1;
    for (i = A1 + 1; i < A2; i++) n[i] = RE;
    n[A2] = RE + FA;
    return out(s, n);
  }
  function conclusion2(t) {
    var s = syls(t), n = fill(s, FA), A2 = lastAcc(s);
    if (A2 >= 1) {
      n[A2 - 1] = MI;
      var p = s[A2 - 1];
      if (p.last && p.wn - p.wa === 3 && A2 >= 2) n[A2 - 2] = MI;   // after a dactyl: Dó-mi-num nos-trum, pe-tén-ti-bus se
    }
    return out(s, n);
  }
  function readingProc(text, gospel) {
    var t = plain(text).replace(/\s*\d+\s*/g, ' ').trim();
    var vs = verses(t), g = '(f3) ';
    vs.forEach(function (v, vi) {
      var lastV = vi === vs.length - 1, q = v[v.length - 1].p === '?';
      v.forEach(function (m, mi) {
        if (mi < v.length - 1) { g += medE(m.t) + ' (;) '; return; }
        if (q) g += questE(m.t) + (lastV ? ' (::)' : ' (:) ');
        else if (lastV) g += finalE(m.t) + ' (::)';
        else g += (gospel ? semiL(m.t) : termE(m.t)) + ' (:) ';
      });
    });
    return g.trim();
  }
  function epistleTitleProc(t) {
    t = plain(t);
    var m = /^(.*Apóstoli)\s+(ad\s.*)$/i.exec(t);
    if (m) return '(f3) ' + medE(m[1] + ':') + ' (;) ' + termE(m[2]) + ' (::)';
    return '(f3) ' + termE(t) + ' (::)';
  }
  function epistleProc(text, o) {
    o = o || {};
    var r = readingProc(text, false);
    return o.title ? epistleTitleProc(o.title).replace(/ \(::\)$/, ' (:) ') + r.replace(/^\(f3\) /, '') : r;
  }
  function gospelProc(text, o) {
    o = o || {};
    var r = readingProc(text, true), g = '';
    if (o.dv) g += '(f3) Dó(g)mi(h)nus(h) vo(gh)bís(hg)cum.(g) (::) <sp>R/</sp>. Et(g) cum(h) spí(h)ri(g)tu(g) tu(h)o.(h) (::) ';
    if (o.book && T.sequentia(o.book)) g += (g ? '' : '(f3) ') + T.sequentia(o.book).replace(/^\(f3\) /, '') + ' ';
    return g ? g + r.replace(/^\(f3\) /, '') : r;
  }
  T.orationProc = orationProc; T.lessonProc = lessonProc; T.readingProc = readingProc; T.epistleTitleProc = epistleTitleProc;
  T.epistleProc = epistleProc; T.gospelProc = gospelProc;
  T._proc = {syls: syls, flexO: flexO, elevO: elevO, flexL: flexL, medL: medL, termL: termL, semiL: semiL, questL: questL,
    medE: medE, termE: termE, questE: questE, finalE: finalE, part1: part1, conclusion2: conclusion2, verses: verses};
})();
