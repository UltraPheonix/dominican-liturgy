/* Psalm tones of the Order of Preachers and the fitting of the words to them, after the
   "Tonorum communium iuxta ritum Ordinis Prædicatorum regulæ" (Rome, 1965), art. I–II.

   A cadence is written as GABC note groups separated by spaces:
     'x   a melodic accent (falls on a Latin accent)
     xr   a "superveniens" (hollow) note, sung only by the extra syllable of a dactyl
     the groups before the first accent are preparatory notes, one syllable each;
     the groups after an accent (and its superveniens) are sung one syllable each.
*/
(function () {
  'use strict';
  var window = typeof self !== 'undefined' ? self : (typeof globalThis !== 'undefined' ? globalThis : {});

  var TONES = {
    'I':   {clef: 'c4', inton: 'f gh', tenor: 'h', flex: "'h gr g", med: "'ixi hr h 'g hr h", sol: "hg gixi h 'hg gh", solAnt: 'h',
            term: {D: "g f 'gh gr gFED", g: "g f 'gh gr g", a: "g f 'g hr h"}, def: 'D'},
    'II':  {clef: 'f3', inton: 'e f', tenor: 'h', flex: "'h fr f", med: "'i hr h", sol: "hg hi i 'hi hr h", solInton: 'e f eh',
            term: {D: "g 'e fr f"}, def: 'D'},
    'III': {clef: 'c4', inton: 'g hj', tenor: 'j', flex: "'j hr h", med: "'k jr j 'i jr j", sol: "'jk jr j 'ih hj", solAnt: 'j',
            term: {a: "h 'j jr ih", a2: "ji hi 'h gr gh"}, def: 'a'},
    'IV':  {clef: 'c4', inton: 'h gh', tenor: 'h', flex: "'h gr g", med: "g h 'i hr h", sol: "hg gi i 'hi hr h",
            term: {E: "g h ih 'gf e"}, ant: {E: 'g'}, def: 'E'},
    'IVA': {clef: 'c3', inton: 'i hi', tenor: 'i', flex: "'i hr h", med: "h i 'j ir i", sol: "ih hj j 'ij ir i",
            term: {A: "h i j 'h fr f"}, def: 'A'},
    'V':   {clef: 'c3', inton: 'd f', tenor: 'h', flex: "'h fr f", med: "'i hr h",
            term: {a: "'i gr g 'h fr f"}, def: 'a'},
    'VI':  {clef: 'c4', inton: 'f gh', tenor: 'h', flex: "'h gr g", med: "'ixi hr h 'g hr h", sol: "hg gixi h 'hg gh", solAnt: 'h',
            term: {F: "f gh 'g fr f"}, def: 'F'},
    'VII': {clef: 'c3', inton: 'h hi', tenor: 'i', flex: "'i hr h", med: "'k jr j 'i jr j", sol: "'ik jr j 'ji ij", solAnt: 'j',
            term: {a: "'j ir i 'h hr gf", d: "'j ir i 'h hr gi"}, def: 'd'},
    'VIII':{clef: 'c4', inton: 'g h', tenor: 'j', flex: "'j hr h", med: "'k jr j", sol: "ih ij j 'ij ir i", solClef: 'c3', solTenor: 'i', solInton: 'f g fi',
            term: {G: "i j 'h gr g", c: "h j 'k jr j"}, def: 'G'},
    'PER': {clef: 'c4', inton: 'ixhi', tenor: 'h', flex: "'h gr g", med: "i h 'g fr f",
            inton2: 'ixhi', tenor2: 'g', term: {'': "d 'f fr ed"}, def: ''}
  };
  var ROMAN = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII', 8: 'VIII'};

  // ---------------------------------------------------------------- syllables and accents
  var VOW = 'aeiouyæœáéíóúýǽëAEIOUYÆŒÁÉÍÓÚÝǼË';
  var ACUTE = /[áéíóúýǽÁÉÍÓÚÝǼ]/;
  function base(c) { return c.normalize('NFD').charAt(0).toLowerCase(); }
  function isV(w, i) {
    var c = w.charAt(i);
    if (VOW.indexOf(c) < 0) return false;
    var b = base(c), prev = i > 0 ? base(w.charAt(i - 1)) : '', nxt = w.charAt(i + 1);
    if (b === 'u' && (prev === 'q' || prev === 'g') && nxt && VOW.indexOf(nxt) >= 0 && i >= 1) return false;
    // consonantal i after a prefix: ad-iútor, con-iúnx, in-iústus, ab-iéctus, ob-iécit, sub-iéctus, re-iécit
    if (b === 'i' && nxt && VOW.indexOf(nxt) >= 0 && /^(ad|con|in|ob|sub|ab|re)$/i.test(w.slice(0, i).normalize('NFD').replace(/[\u0300-\u036f]/g, ''))) return false;
    var pv = i > 0 && VOW.indexOf(w.charAt(i - 1)) >= 0 && !(prev === 'u' && i >= 2 && /[qg]/.test(base(w.charAt(i - 2))));
    if (b === 'i' && nxt && VOW.indexOf(nxt) >= 0 && (i === 0 || pv)) return false;
    return true;
  }
  var ONSET = {bl: 1, br: 1, cl: 1, cr: 1, dr: 1, fl: 1, fr: 1, gl: 1, gr: 1, pl: 1, pr: 1, tr: 1, ch: 1, ph: 1, th: 1,
               gn: 1, st: 1, sc: 1, sp: 1, ct: 1, pt: 1, mn: 1, ps: 1, qu: 1, gu: 1};
  // split a word (letters, possibly with punctuation around) into syllables
  function syllabify(w) {
    var idx = [], i;
    for (i = 0; i < w.length; i++) if (isV(w, i)) idx.push(i);
    var nuc = [];
    idx.forEach(function (i) {
      var last = nuc[nuc.length - 1];
      if (last && last[last.length - 1] === i - 1 && w.charAt(i) !== 'ë' &&
          /^(ae|oe|au)$/.test(base(w.charAt(i - 1)) + base(w.charAt(i)))) last.push(i);
      else nuc.push([i]);
    });
    if (nuc.length <= 1) return [w];
    var cuts = [];
    for (i = 0; i + 1 < nuc.length; i++) {
      var s = nuc[i][nuc[i].length - 1] + 1, e = nuc[i + 1][0], n = e - s;
      var cons = '';
      for (var k = s; k < e; k++) if (/[A-Za-z]/.test(base(w.charAt(k)))) cons += base(w.charAt(k));
      if (n === 0) cuts.push(e);
      else if (n === 1) cuts.push(s);
      else cuts.push(ONSET[cons.slice(-2)] ? e - 2 : e - 1);
    }
    var out = [], st = 0;
    cuts.forEach(function (c) { out.push(w.slice(st, c)); st = c; });
    out.push(w.slice(st));
    return out.filter(function (x) { return x; });
  }
  // words -> syllables with accents: [{t, word, first, last, acc (tonic), sec (secondary)}]
  function analyse(text) {
    var words = text.trim().split(/\s+/).filter(function (w) { return /[A-Za-zÀ-ÿǼǽ]/.test(w); });
    var syl = [];
    words.forEach(function (w, wi) {
      var parts = syllabify(w), n = parts.length, acc = -1;
      parts.forEach(function (p, i) { if (ACUTE.test(p)) acc = i; });
      if (acc < 0 && n === 2) acc = 0;
      else if (acc < 0 && n >= 3) acc = n - 3;      // unmarked long words are Hebrew names: Ísrael
      parts.forEach(function (p, i) {
        syl.push({t: p, word: wi, first: i === 0, last: i === n - 1, acc: i === acc, mono: n === 1,
                  // secondary accents (art. I § IV a, b)
                  sec: (acc >= 2 && i === acc - 2) || (acc >= 0 && n - acc === 3 && i === n - 1)});
      });
    });
    // a monosyllable at the end has no accent; the accent falls back (§ IV c)
    var L = syl.length;
    if (L >= 2 && syl[L - 1].mono) {
      if (syl[L - 2].mono) syl[L - 2].acc = true;                       // mandávit dé te
      else {
        var w = syl[L - 2].word, ws = syl.filter(function (s) { return s.word === w; });
        var a = ws.findIndex(function (s) { return s.acc; });
        if (a >= 0 && ws.length - a === 3) { ws[a].acc = false; ws[ws.length - 1].acc = true; }  // génuí te
      }
    }
    return syl;
  }

  // ---------------------------------------------------------------- cadences
  function parseCadence(str, ant) {
    var toks = str.trim().split(/\s+/).map(function (t) {
      return {n: t.replace(/^'/, '').replace(/r$/, ''), acc: t.charAt(0) === "'", sup: /^[a-m]r$/.test(t)};
    });
    var c = {prep: [], accs: []}, cur = null;
    toks.forEach(function (t) {
      if (t.acc) { cur = {n: t.n, sup: null, after: []}; c.accs.push(cur); }
      else if (!cur) c.prep.push(t.n);
      else if (t.sup && !cur.after.length && cur.sup === null) cur.sup = t.n;
      else cur.after.push(t.n);
    });
    c.ant = ant || null;
    return c;
  }
  // fit syllables to a cadence; returns notes per syllable (array, same length) and roles
  function fit(syl, cad, tenor) {
    var L = syl.length, notes = new Array(L), roles = new Array(L), k = cad.accs.length;
    // the melodic accents fall on the last k accents of the text
    var pos = [], i;
    var accIdx = [];
    for (i = 0; i < L - 1; i++) if (syl[i].acc) accIdx.push(i);
    if (!accIdx.length) accIdx.push(Math.max(0, L - 2));
    pos[k - 1] = accIdx[accIdx.length - 1];
    if (k === 2) {
      var need = cad.accs[0].after.length, a2 = pos[1], cand = [];
      for (i = a2 - 1; i >= 0; i--) if (syl[i].acc || syl[i].sec) cand.push(i);
      var pick = cand.filter(function (j) { var g = a2 - j - 1; return g >= need && g <= need + 1; })[0];
      // no accent at the right distance: the syllable there takes an adventitious accent
      if (pick === undefined) pick = Math.max(0, a2 - need - 1);
      pos[0] = pick;
    }
    var end = L;
    for (var a = k - 1; a >= 0; a--) {
      var A = cad.accs[a], p = pos[a], segEnd = end, n = segEnd - p - 1;
      // syllables after the accent: the superveniens takes the extra ones
      var after = A.after.slice(), j = p + 1, extra = n - after.length;
      if (cad.ant && a === k - 1 && n === 2 && after.length === 1) {
        // superveniens anticipata (IV E): the accent takes the hollow note, the next syllable the clivis
        notes[p] = cad.ant; roles[p] = 'acc'; notes[p + 1] = A.n; roles[p + 1] = 'sup'; notes[p + 2] = after[0]; roles[p + 2] = 'fin';
        end = p; continue;
      }
      notes[p] = A.n; roles[p] = 'acc';
      for (; extra > 0 && j < segEnd; extra--, j++) { notes[j] = A.sup || after[0] || A.n; roles[j] = 'sup'; }
      var m = Math.max(0, after.length - (segEnd - j));
      for (var q = m; q < after.length && j < segEnd; q++, j++) { notes[j] = after[q]; roles[j] = 'fin'; }
      end = p;
    }
    // preparatory notes
    for (i = cad.prep.length - 1, j = end - 1; i >= 0 && j >= 0; i--, j--) { notes[j] = cad.prep[i]; roles[j] = 'prep'; }
    for (; j >= 0; j--) { notes[j] = tenor; roles[j] = 'ten'; }
    return {notes: notes, roles: roles};
  }

  // ---------------------------------------------------------------- a verse
  // automatic flex when the first half is long and has a natural pause (the 1962 text carries no †)
  function flexAt(half) {
    var syl = analyse(half);
    if (syl.length < 20) return -1;
    var re = /[,;:](?=\s)/g, m, best = -1, words = 0, total = half.split(/\s+/).length;
    while ((m = re.exec(half))) {
      var before = half.slice(0, m.index + 1);
      var nb = analyse(before).length;
      if (nb >= 7 && syl.length - nb >= 7) best = m.index + 1;
    }
    return best;
  }

  function toneOf(mode, diff) {
    var r = ROMAN[mode] || mode;
    if (r === 'IV' && diff === 'A') r = 'IVA';
    var T = TONES[r];
    if (!T) return null;
    var d = (diff && T.term[diff] !== undefined) ? diff : T.def;
    return {name: r, T: T, diff: d};
  }

  // point one verse: returns [{half: 1|2, t, note, role}] for each syllable, with markers
  function pointVerse(text, tone, opts) {
    opts = opts || {};
    var T = tone.T, parts = text.split(/\s*\*\s*/), out = [];
    var h1 = parts[0] || '', h2 = parts.slice(1).join(' ');
    if (!h2) { h2 = h1; h1 = ''; }
    function run(half, cad, ten, inton, mark) {
      if (!half) return;
      var syl = analyse(half), f = fit(syl, cad, ten);
      if (inton) {
        var it = inton.split(' ');
        for (var i = 0; i < it.length && i < syl.length && f.roles[i] === 'ten'; i++) { f.notes[i] = it[i]; f.roles[i] = 'int'; }
      }
      syl.forEach(function (s, i) { out.push({t: s.t, first: s.first, last: s.last, note: f.notes[i], role: f.roles[i]}); });
      if (mark) out.push({mark: mark});
    }
    var fl = opts.noFlex || opts.solemn ? -1 : flexAt(h1);
    if (opts.inton && /^\s*Magn[ií]ficat\s*$/i.test(h1.replace(/[^A-Za-zÀ-ÿ ]/g, ''))) {
      // the first verse of the Magnificat: the intonation only, without a mediation
      var ms = analyse(h1), it0 = (T.solInton && opts.solemn ? T.solInton : T.inton).split(' ');
      if (opts.solemn && T.solClef) out.solClef = T.solClef;
      ms.forEach(function (x, i) { out.push({t: x.t, first: x.first, last: x.last, note: it0[i] || (opts.solemn && T.solTenor) || T.tenor, role: i < it0.length ? 'int' : 'ten'}); });
      out.push({mark: '*'});
    } else if (opts.solemn && T.sol) {
      // the solemn mediation of the Gospel canticles: its own staff where the clef differs (VIII)
      run(h1, parseCadence(T.sol, T.solAnt), T.solTenor || T.tenor, opts.inton ? (T.solInton || T.inton) : null, '*');
      if (T.solClef) out.solClef = T.solClef;
    } else if (fl > 0) {
      run(h1.slice(0, fl), parseCadence(T.flex), T.tenor, opts.inton ? T.inton : null, '†');
      run(h1.slice(fl).trim(), parseCadence(T.med), T.tenor, null, '*');
    } else run(h1, parseCadence(T.med), T.tenor, opts.inton ? T.inton : null, '*');
    run(h2, parseCadence(T.term[tone.diff], T.ant && T.ant[tone.diff]), T.tenor2 || T.tenor, T.inton2 || null, null);
    return out;
  }

  // GABC of a pointed verse (the first verse, notated)
  function verseGabc(pv, tone) {
    var g = '(' + (pv.solClef || tone.T.clef) + ') ', word = '';
    pv.forEach(function (s) {
      if (s.mark) { g += s.mark === '*' ? '*(:) ' + (pv.solClef ? '(' + tone.T.clef + ') ' : '') : '†(,) '; return; }
      var t = s.t.replace(/[()]/g, '');
      g += t + '(' + s.note + ')' + (s.last ? ' ' : '');
    });
    return g.trim() + ' (::)';
  }
  // pointed text: accents bold, preparatory syllables italic
  function verseHtml(pv, esc) {
    var h = '';
    pv.forEach(function (s) {
      if (s.mark) { h += ' <span class="r">' + s.mark + '</span>'; return; }
      var t = esc(s.t);
      if (s.role === 'acc') t = '<b>' + t + '</b>';
      else if (s.role === 'prep') t = '<i>' + t + '</i>';
      h += (s.first && h ? ' ' : '') + t;
    });
    return h;
  }

  // ---------------------------------------------------------------- choosing the ending (art. II, usus differentiarum)
  var LET = 'abcdefghijklm';
  // absolute pitch (diatonic step number, C = 0) of a GABC letter under a clef
  function pitch(clef, ch) {
    var line = parseInt(clef.charAt(1), 10), pos = LET.indexOf(ch.toLowerCase());
    var clefPos = 1 + 2 * line;                      // d=line1 → index 3
    var base = clef.charAt(0) === 'c' ? 7 : 3;       // c' = 7, f = 3 (steps above c)
    return base + (pos - clefPos);
  }
  var NAMES = ['ut', 're', 'mi', 'fa', 'sol', 'la', 'si'];
  function noteNames(gabc) {
    var m = /\(([cf][1-4])\)/.exec(gabc), clef = m ? m[1] : 'c4', out = [];
    gabc.replace(/\(([^)]*)\)/g, function (a, inner) {
      if (/^[cf][1-4]$/.test(inner)) { clef = inner; return a; }
      inner.replace(/([a-mA-M])(?![x#y])/g, function (x, c) { out.push(pitch(clef, c)); return x; });
      return a;
    });
    return out;
  }
  function chooseDiff(mode, gabc) {
    var n = noteNames(gabc || ''), f = n[0], nm = function (p) { return NAMES[((p % 7) + 7) % 7]; };
    var r = ROMAN[mode] || mode;
    if (f === undefined) return null;
    if (r === 'I') {
      if (nm(f) === 'ut') return 'D';
      if (nm(f) === 're') return 'g';
      if (nm(f) === 'la') return 'a';
      if (nm(f) === 'fa') {
        var nx = n.slice(1, 4).map(nm);
        if (nx[0] === 'mi' && nx[1] === 're') return 'a';
        if (nx[0] === 'la' || (nx[0] === 'sol' && nx[1] === 'la')) return 'a';
        if (nx.indexOf('ut') >= 0 && nx.indexOf('la') > nx.indexOf('ut')) return 'g';
        return 'D';
      }
      return 'D';
    }
    if (r === 'III') return (nm(f) === 'mi' && f < 7) ? 'a2' : 'a';
    if (r === 'IV') { var last = n[n.length - 1]; return nm(last) === 'la' ? 'A' : 'E'; }
    if (r === 'VII') {
      var s = n[1];
      return (nm(f) === 'sol' && s !== undefined && s > f && ['la', 'si', 'ut'].indexOf(nm(s)) >= 0) ? 'a' : 'd';
    }
    if (r === 'VIII') return (nm(f) === 'ut' && f >= 7) ? 'c' : 'G';
    return null;
  }

  window.OPPsalm = {TONES: TONES, toneOf: toneOf, analyse: analyse, syllabify: syllabify, fit: fit, parseCadence: parseCadence,
                    pointVerse: pointVerse, verseGabc: verseGabc, verseHtml: verseHtml, chooseDiff: chooseDiff, noteNames: noteNames};
  if (typeof module !== 'undefined') module.exports = window.OPPsalm;
})();
