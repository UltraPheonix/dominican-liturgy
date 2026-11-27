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
