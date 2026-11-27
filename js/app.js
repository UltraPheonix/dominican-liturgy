/* Propria Missae juxta ritum Ordinis Praedicatorum
 * A Dominican version of the Propers tool of bbloomf/jgabc (public domain), rendering the chants of
 * the Graduale O.P. (1950) with exsurge.  Data: data/masses.js (see /build).
 */
(function () {
  'use strict';
  var D = window.DOMINICAN;
  // Ordinarium X (Grad. O.P. pp. 152*-158*): its Gloria, Sanctus and Agnus are the Vatican Mass VIII melodies
  (function () {
    var add = [['opX-gloria', 'Gloria X', '153*'], ['opX-sanctus', 'Sanctus X', '157*'], ['opX-agnus', 'Agnus X', '158*']];
    if (!D || !D.kyriale) return;
    add.forEach(function (a) { if (!D.chants[a[0]]) { D.chants[a[0]] = {p: 'ky', i: a[1], pg: a[2]}; var at = D.kyriale.indexOf(8039); D.kyriale.splice(at < 0 ? D.kyriale.length : at, 0, a[0]); } });
  })();
  // Masses made from others: the last Sunday after the Octave of Trinity, and the resumed Sundays after the Epiphany
  (function () {
    var M = D.masses, ROM = ['', 'I', 'II', 'III', 'IV', 'V', 'VI'], O = window.ORATIONS || {};
    if (M.Pent23 && !M.Pent24) {
      M.Pent24 = Object.assign({}, M.Pent23, {title: 'Dominica ultima post Octavam Trinitatis', en: 'Last Sunday after the Octave of Trinity',
        readings: [{type: 'Epistle', ref: 'Ad Colossenses 1: 9-14'}, {type: 'Gospel', ref: 'Matthæus 24: 15-35'}]});
    }
    if (M.Pent2) { M.Pent2.title = 'Dominica infra Octavam Corporis Christi'; M.Pent2.en = 'Sunday within the Octave of Corpus Christi'; }
    if (M.Pent3) { M.Pent3.title = 'Dominica I post Octavam Trinitatis'; M.Pent3.en = '1st Sunday after the Octave of Trinity'; }
    [3, 4, 5, 6].forEach(function (n) {
      var e = M['Epi' + n];
      if (!e || !M.Pent23) return;
      M['Epi' + n + 'r'] = Object.assign({}, M.Pent23, {title: 'Dominica ' + ROM[n - 1] + ' quæ superfuit post Octavam Epiphaniæ',
        en: ['', '1st', '2nd', '3rd', '4th', '5th'][n - 1] + ' Sunday after the Octave of the Epiphany (resumed)', readings: e.readings});
      if (O['Epi' + n]) O['Epi' + n + 'r'] = O['Epi' + n];
    });
    if (!O.Pent24 && O.Pent23) O.Pent24 = O.Pent23;
    // list the Masses made here in the Proper of Time too, after the 23rd Sunday, so the Mass list (Options) can show them
    var tp = (D.sections || []).filter(function (s) { return s.id === 'tempore'; })[0];
    if (tp) {
      var add = ['Epi3r', 'Epi4r', 'Epi5r', 'Epi6r', 'Pent24'].filter(function (k) { return M[k] && tp.items.indexOf(k) < 0; });
      var at = tp.items.indexOf('Pent23');
      if (add.length) Array.prototype.splice.apply(tp.items, [at < 0 ? tp.items.length : at + 1, 0].concat(add));
    }
  })();
  var PARTS = ['pr', 'in', 'gr', 'al', 'tr', 'se', 'ad', 'of', 'co', 'an'];
  var PART_NAME = {in: 'Officium', gr: 'Responsorium', al: 'Alleluia', tr: 'Tractus', se: 'Sequentia', of: 'Offertorium', co: 'Communio', an: 'Ad Vesperas', pr: 'Ante Missam', ad: 'Ad adorationem Crucis'};
  var PART_EN = {in: 'Office', gr: 'Responsory', al: 'Alleluia', tr: 'Tract', se: 'Sequence', of: 'Offertory', co: 'Communion', an: 'Vespers', pr: 'Before Mass', ad: 'Adoration of the Cross'};
  var PART_ABBR = {in: 'Off.', gr: 'Resp.', al: 'Allel.', tr: 'Tract.', se: 'Seq.', of: 'Offert.', co: 'Comm.'};
  var ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII'];
  var CONF = {
    introit: null,
    graduale: null,
    proper: {cls: 'ok', text: 'Proper'},
    manual: {cls: 'info', text: 'Dominican Mass'},
    shared: {cls: 'info', text: 'Chants re-used'},
    common: {cls: 'info', text: 'From the Common'},
    dm: {cls: 'ok', text: 'St. Dominic Missal'},
    missal: {cls: 'ok', text: 'Missale O.P.'},
    guess: {cls: 'warn', text: 'Common: check Ordo'}
  };
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var el = function (tag, attrs, kids) {
    var e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'text') e.textContent = attrs[k];
      else if (k === 'html') e.innerHTML = attrs[k];
      else if (k.slice(0, 2) === 'on') e.addEventListener(k.slice(2), attrs[k]);
      else if (attrs[k] !== null && attrs[k] !== undefined && attrs[k] !== false) e.setAttribute(k, attrs[k]);
    });
    (kids || []).forEach(function (c) { if (c) e.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return e;
  };
  var SMALL = /^(et|in|de|a|ab|ad|ac|cum|e|ex|post|pro|sub|super|ante|per|of|the|and|to)$/i;
  var clean = function (s) {
    s = String(s || '').replace(/<[^>]+>/g, '');
    var letters = s.replace(/[^A-Za-zÀ-ÿÆæŒœ]/g, '');
    if (letters.length > 6 && letters.replace(/[^A-ZÀ-ÞÆŒ]/g, '').length / letters.length > 0.7) {
      s = s.toLowerCase().replace(/[a-zà-ÿæœ]+/g, function (w, i) {
        if (i > 0 && SMALL.test(w)) return w;
        return w.charAt(0).toUpperCase() + w.slice(1);
      }).replace(/\b(o\.p|b\.m\.v|s\.p\.n|ss|s|b|bb|n|d|c|e|v|m|mm|p)\./gi, function (x) { return x.toUpperCase(); });
    }
    return s;
  };

  // ---------------------------------------------------------------- state & URL
  // #<massKey>[&in=id,id&gr=id...]  (only parts the user changed are stored)
  var state = {key: null, parts: null, edited: {}, date: null, season: 'auto', ord: '', credo: '', asp: '', ordo: '', hwr: '1939', edit: false, comm: '', prel: '', sac: '', serv: '', rub: ''};

  var HWP = document.body && document.body.getAttribute('data-page') === 'hw';
  var BOOKP = document.body && document.body.getAttribute('data-page') === 'book';
  function readHash() {
    var h = decodeURIComponent(location.hash.slice(1));
    if (!h) return null;
    var bits = h.split('&'), out = {key: bits.shift(), over: {}, opts: {}};
    bits.forEach(function (b) {
      var kv = b.split('=');
      if (PARTS.indexOf(kv[0]) >= 0) out.over[kv[0]] = kv[1] ? kv[1].split(',').map(function (x) { return /^\d+$/.test(x) ? Number(x) : x; }) : [];
      else if (['d', 'season', 'ord', 'credo', 'asp', 'ordo', 'hw', 'conv', 'comm', 'prel', 'sac', 'serv', 'rub'].indexOf(kv[0]) >= 0) out.opts[kv[0]] = kv[1] || '';
    });
    return out;
  }
  function writeHash() {
    if (!state.key || !state.parts) return;
    var bits = [state.key], def = massParts(state.key);
    PARTS.forEach(function (p) {
      var a = (def[p] || []).map(function (c) { return c.id; }).join(',');
      var b = (state.parts[p] || []).map(function (c) { return c.id; }).join(',');
      if (a !== b) bits.push(p + '=' + b);
    });
    if (state.date) bits.push('d=' + iso(state.date));
    if (state.season !== 'auto') bits.push('season=' + state.season);
    if (state.ord) bits.push('ord=' + state.ord);
    if (state.credo) bits.push('credo=' + state.credo);
    if (state.asp) bits.push('asp=' + state.asp);
    if (state.ordo) bits.push('ordo=' + state.ordo);
    if (state.comm) bits.push('comm=' + state.comm);
    if (state.prel) bits.push('prel=' + state.prel);
    if (state.sac) bits.push('sac=' + state.sac);
    if (state.serv) bits.push('serv=' + state.serv);
    if (state.rub) bits.push('rub=' + state.rub);
    if (HWP || state.hwr !== '1939') bits.push('hw=' + state.hwr);
    history.replaceState(null, '', '#' + bits.join('&'));
  }

  // ---------------------------------------------------------------- chant files
  var gabcCache = {};
  function loadGabc(id) {
    if (!gabcCache[id]) {
      var path = /^r\d+$/.test(String(id)) ? 'gabc/r/' + String(id).slice(1) : 'gabc/' + id;
      gabcCache[id] = fetch(path + '.gabc').then(function (r) {
        if (!r.ok) throw new Error('gabc/' + id + '.gabc: ' + r.status);
        return r.text();
      });
    }
    return gabcCache[id];
  }
  // The Introit sung in full: antiphon, psalm verse, the whole Glória Patri in the Introit tone of its mode (Graduale O.P. pp. IX-XI,
  // data/introit_gp.js), then the antiphon again. In Passiontide and at Masses for the dead there is no Glória Patri: the antiphon is
  // repeated straight after the verse. The books print only "Glória Patri. E u o u a e"; GregoBase files differ in how they mark the verse.
  function fullIntroit(body, header, key) {
    var GP = window.INTROIT_GP; if (!GP || !body) return body;
    var clef = (/^\s*\(([cf]b?[1-4])\)/.exec(body) || [])[1]; if (!clef) return body;
    if (/repetitur|<i>[^<]*Ant\.?<\/i>/i.test(body)) return body;                   // the book already shows the repetition
    var vm = /(<sp>V\/<\/sp>\.?|\bV\/\.|<i>Ps\.<\/i>)/.exec(body), ant;
    var g = /\(::\)\s*(?:<eu>)?\s*Gl[oó]\([^)]*\)\s*ri\([^)]*\)\s*a[.,]?\(/.exec(body);
    if (vm) ant = body.slice(0, vm.index).replace(/\s*\(::\)\s*$/, '');
    else {                                                // no verse sign: the antiphon ends at the double bar before the verse's own
      var bars = [], re = /\(::\)/g, m; while ((m = re.exec(body)) && (!g || m.index <= g.index)) bars.push(m.index);
      if (bars.length < 2) return body; ant = body.slice(0, bars[bars.length - 2]);
    }
    ant = ant.replace(/^\s*\([cf]b?[1-4]\)\s*/, '').replace(/\s+$/, '');
    if (!/\(::\)\s*$/.test(ant)) ant += ' (::)';
    var verse = g ? body.slice(0, g.index) + '(::)' : body.replace(/\s+$/, '');
    if (!/\(::\)\s*$/.test(verse)) return body;
    var noGP = /^Quad[56]/.test(key || '') || /^\s*\([cf]b?[1-4]\)\s*R[eé]\(/.test(body) || /^(?:C114|S1102)/.test(key || '');
    var mode = parseInt(header && header.mode, 10), gp = GP[mode];
    if (!noGP && !gp) return body;
    // the Gloria Patri and the repeat continue on the same staff: a clef is drawn again only where it changes
    var gpClef = gp && (/^\s*\(([cf]b?[1-4])\)/.exec(gp) || [])[1];
    if (gpClef === clef) gp = gp.replace(/^\s*\([cf]b?[1-4]\)\s*/, '');
    // the repeat is written as in the Graduale: 'Ant.' and the incipit up to the asterisk (Joseph, 25 Nov.)
    // (the Dominican Graduale marks the end of the intonation with a double bar instead of an asterisk)
    var star = ant.search(/\*\s*\(/); if (star < 0) { star = ant.search(/\(::\)/); if (star === ant.search(/\(::\)\s*$/)) star = -1; }
    var inc = star > 0 ? ant.slice(0, star).replace(/\s+$/, '') + ' (::)' : ant;
    inc = inc.replace(/^(\s*)([^\s(]+)\(/, '$1<i>Ant.</i>() $2(');
    return verse + (noGP ? '' : ' ' + gp.replace(/\s+$/, '')) + (gpClef && gpClef !== clef && !noGP ? ' (' + clef + ') ' : ' ') + inc;
  }
  function splitGabc(text) {
    var i = text.indexOf('%%');
    var head = i >= 0 ? text.slice(0, i) : '', body = i >= 0 ? text.slice(i + 2) : text;
    var header = {};
    head.split(/\n/).forEach(function (l) {
      var m = /^\s*([\w-]+)\s*:\s*(.*?);?\s*$/.exec(l);
      if (m) header[m[1].toLowerCase()] = m[2];
    });
    return {header: header, body: body.replace(/^\s+/, '')};
  }

  // ---------------------------------------------------------------- exsurge
  // The chant context and the GABC adjustments are those of jgabc (util.js, propers.js).
  function makeContext(o) {
    o = o || {};
    var ctxt = new exsurge.ChantContext(exsurge.TextMeasuringStrategy.Canvas);
    ctxt.condenseLineAmount = 1;
    ctxt.lineBreaking = 'optimal';
    ctxt.setGlyphScaling(1 / 16);
    ctxt.textColor = 'currentColor';
    ctxt.staffLineColor = ctxt.neumeLineColor = ctxt.dividerLineColor = 'currentColor';
    ctxt.negativeFillColor = 'var(--paper, #fff)';
    ctxt.setFont(o.font || "'Crimson Text', serif", o.size || 19.2 / 0.9);
    ctxt.spaceBetweenSystems = 0;
    ctxt.textStyles.dropCap.size = o.dropSize || 64;
    if (o.dropFont) ctxt.textStyles.dropCap.font = o.dropFont;
    if (o.dropColor) ctxt.textStyles.dropCap.color = o.dropColor;
    ctxt.textStyles.annotation.size = 12.8;
    ctxt.minLyricWordSpacing *= 0.7;
    ctxt.accidentalSpaceMultiplier = 1.5;
    ctxt.specialCharProperties['font-family'] = "'Versiculum'";
    ctxt.specialCharProperties['font-variant'] = 'normal';
    ctxt.specialCharProperties['font-weight'] = '400';
    var defaultSpecialCharText = ctxt.specialCharText;
    ctxt.specialCharText = function (ch) { return defaultSpecialCharText(ch).toLowerCase(); };
    ctxt.setRubricColor(o.rubric || 'var(--rubric, #b3121f)');
    if (o.lines) ctxt.staffLineColor = o.lines;
    if (o.glyph) ctxt.setGlyphScaling(o.glyph);
    return ctxt;
  }
  // Outside Paschaltide the optional "T. P. Alleluia" at the end of a chant is not sung
  function stripTP(gabc) {
    var m = /<i>\s*T\.\s*P\.\s*<\/i>/.exec(gabc);
    if (!m) return gabc;
    var j = gabc.indexOf('(::)', m.index);
    // the Alleluia ends at the first double bar after it; if the T. P. marker itself carries the double bar
    // ("<i>T. P.</i>(::) Al(...)"), at the next one
    var k = j < 0 ? -1 : (/\w\(/.test(gabc.slice(m.index + m[0].length, j)) ? j : gabc.indexOf('(::)', j + 4));
    if (k < 0) return gabc.slice(0, m.index) + '(::)';
    return gabc.slice(0, m.index) + '(::)' + gabc.slice(k + 4);
  }
  // Seasonal form of a sung proper (XIII, 1-7):
  //  - "E. T. P." / "Extra T. P.": outside Paschaltide the printed alternative ending replaces the last words and the Alleluia;
  //  - outside Paschaltide the Alleluia that the Graduale adds for Paschaltide (often unmarked) is not sung in the Introit,
  //    Offertory and Communion, except where it belongs to the chant all year (KEEP_AL, checked in the Missale O.P. 1933);
  //  - from Septuagesima to Easter no Alleluia at all.
  var B = '(?:\\s*\\([,;:]\\d?\\))?';
  var AL = B + '\\s*(?:T\\.\\s?P\\.\\s*)?[Aa]l\\([^)]*\\)\\s*le\\([^)]*\\)\\s*l[úu]\\([^)]*\\)\\s*[ij]a[.,;:!]?\\([^)]*\\)' + B;
  function stripAlleluia(g) {
    var re = new RegExp('([^\\s()]+?)([,;:]?)(\\([^)]*\\)(?:\\s*\\([^)]*\\))*?)((?:' + AL + ')+)\\s*(\\(::\\)|$)?', 'g'), end = g.replace(/\s+$/, '').length;
    g = g.replace(re, function (m, syl, p, notes, run, bar, off) {
      if (bar === undefined && off + m.replace(/\s+$/, '').length < end) return syl + p + notes + ' (;) ';   // inside the chant
      return syl + (/[.!?]$/.test(syl) ? '' : '.') + notes + ' (::)';
    });
    return g.replace(new RegExp('\\(::\\)(?:' + AL + ')+\\s*(\\(::\\)|$)', 'g'), '(::)').replace(/\(;\)\s*(\([:;,]\d?\))/g, '$1').replace(/\s+\(;\)\s*$/, ' (::)').replace(/\(::\)(\s*\(::\))+/g, '(::)');
  }
  // "E. T. P." / "Extra T. P.": the ending sung outside Paschaltide replaces the last words and the Alleluia
  function etp(g, pasch) {
    var m = /<i>\s*(?:E\.?\s*T\.?\s*P\.?|Extra\s*T\.?\s*P\.?):?\s*<\/i>(?:\([^)]*\))?\s*/.exec(g); if (!m) return g;
    var head = g.slice(0, m.index).replace(/\s+$/, ''), tail = g.slice(m.index + m[0].length).replace(/^\*\s*(\([^)]*\))?\s*/, '');
    if (pasch) return head;
    var n = tail.split(/\s+/).filter(function (w) { return /[A-Za-zÀ-ÿæœ]\(/.test(w); }).length;
    var toks = stripAlleluia(head).replace(/\s*\(::\)\s*$/, '').split(/\s+/);
    while (n > 0 && toks.length) { var t = toks.pop(); if (/[A-Za-zÀ-ÿæœ]\(/.test(t)) n--; }
    while (toks.length && /^(\*?\([^)]*\)|\*)$/.test(toks[toks.length - 1])) toks.pop();
    return toks.join(' ') + ' ' + tail;
  }

  var KEEP_AL = {Epi2: 'of', C75s: 'in of co', S0806: 'co', CorpusChristi: 'in', C62s: 'in'};
  // a Kyriale Ite with "vel Benedicamus" (Ite II, V, VI): keep only the half that is sung today
  // Kyriale Ite II, V, VI carry their Benedicamus after the Ite (II and VI as "vel Benedicamus"): keep only the half sung today
  function dismissGabc(body, ben) {
    var m = /\(::z?\)\s*(?:<i>vel<\/i>\s*)?(B\{?e\}?\()/.exec(body);
    if (!m) return body;
    if (!ben) return body.slice(0, m.index) + '(::)';
    var clef = (/\(([cf]b?[1-4])\)/.exec(body) || [, 'c4'])[1];
    return '(' + clef + ') ' + body.slice(m.index + m[0].length - m[1].length).replace(/^B\{e\}/, 'Be').trim();
  }
  function seasonalGabc(gabc, part) {
    var key = state.key || '', pasch = paschal(), lent = !pasch && currentSeason() === 'lent';
    gabc = etp(gabc, pasch);
    if (pasch) return gabc;
    gabc = stripTP(gabc);
    if (!/^(in|of|co)$/.test(part || '')) return gabc;
    if (!lent && KEEP_AL[key] && KEEP_AL[key].split(' ').indexOf(part) >= 0) return gabc;
    return stripAlleluia(gabc);
  }
  // one clef at the head of the chant; repeated identical clefs and doubled double bars are dropped
  function tidyGabc(g) {
    var cur = null;
    g = g.replace(/\(([cf]b?[1-4])\)/g, function (m, c) { if (c === cur) return '()'; cur = c; return m; });
    return g.replace(/\(\)\s*(?=\()/g, '').replace(/\(::\)(\s*\(\))*(\s*\(::\))+/g, '(::)').replace(/\([:;,]\d?\)\s*\(::\)/g, '(::)');
  }
  function exsurgeGabc(gabc, part) {
    gabc = tidyGabc(seasonalGabc(gabc, part));
    return gabc
      // verbatim LaTeX the renderer cannot read: accented y, emphasised rubrics, braces
      .replace(/<v>\\'y<\/v>/g, 'ý').replace(/<v>\\'Y<\/v>/g, 'Ý').replace(/<v>([A-Za-z])<\/v>/g, '$1')
      .replace(/<v>\\emph\{([^}]*)\}<\/v>/g, '<i>$1</i>')
      .replace(/<i>\{([^}]*)\}<\/i>/g, '<i>$1</i>')
      .replace(/<i>(i+j)<\/i>\./g, '<i>$1.</i>')
      .replace(/<v>\\([VRA])bar<\/v>/g, function (m, b) { return b + '/.'; })
      .replace(/<sp>([VRA])\/<\/sp>\.?/g, function (m, b) { return b + '/.'; })
      .replace(/(\)\s+)([^()]*V\/\.\s*\d+\.?)(?=[ (])/g, '$1^$2^')
      .replace(/(\s*)((?:<(\w+)>[^()]*?<\/\3>)?(?:<(\w+)>[^()]*?<\/\4>|[^()<>])+)(?=\s+[^\s()]+\([^)])/g, function (match, ws, main) {
        return (main.match(/[|^]|^\s*$/) || (main.match(/[aeiouyáéíóúýæǽœë]/i) && !main.match(/<\w+>/))) ? match : (ws + '^' + main + '^');
      })
      .replace(/\\emph{([^(}]+)\}/g, '_$1_')
      .replace(/(v[A-Z]__[A-Z])([^_])/g, '$1_3$2')
      .replace(/([^)]\s+)([*†]|<i>(?:i+j|Repet)\.<\/i>)\(/g, '$1^$2^(')
      .replace(/\^?(<i>[^(|]*? [^(|]*?<\/i>)\^?([^(|]*)/g, '^$1^$2')
      .replace(/\*(\([:;,]+\))\s+(<i>i+j\.<\/i>)\(/g, '{*} $2$1 (')
      .replace(/(\s+)({?<i>(?:i+j|Repet)\.<\/i>}?)\(/g, '$1^$2^(')
      .replace(/\[([^\]\s-áéíóú]+)\](?=\()/g, '|$1 ')
      .replace(/\[([^\]\s-]+)-?\](?=\()/g, '|$1')
      .replace(/(<b>[^<]+)œ́/g, '$1œ</b>́<b>')
      .replace(/(?:{})?<i>\(([^)]+)\)<\/i>/g, '_{}$1_')
      .replace(/<\/?i>/g, '_')
      .replace(/(\)\s+(?:\([^)]*\))*)(\s*[^(^|]+)(?=\(\))/g, '$1^$2^')
      .replace(/\\hspace{[^}]*}/g, '')
      .replace(/(?:\(Z\)\s*)?<alt>(.*?\\emph.*?)<\/alt>/gi, '^_$1_^() (Z)\n')
      .replace(/<alt>.*?<\/alt>/gi, '')
      .replace(/\[[ou]ll:[01]?[{}][01]?\]/ig, '')
      .replace(/\s(<nlba>)?\^?\*\^?(?=\s*[^(])/g, ' $1*()')
      .replace(/(\))\s*\(\)/g, ')')
      .replace(/\^_([^_^]*)_\^/g, '^$1^');   // exsurge does not nest italics inside red text
  }

  var renderQueue = Promise.resolve(), glyphSeq = 0;
  function renderInto(container, body, header, part, o) {
    o = o || {};
    // one layout at a time keeps the page responsive and the order stable
    renderQueue = renderQueue.then(function () {
      return new Promise(function (resolve) {
        try {
          var ctxt = makeContext(o);
          var gabc = exsurgeGabc(body, part);
          var mappings = exsurge.Gabc.createMappingsFromSource(ctxt, gabc);
          var dropCap = o.noDrop ? false : header['initial-style'] !== '0';
          var score = new exsurge.ChantScore(ctxt, mappings, dropCap);
          if (dropCap && PART_ABBR[part] && !o.noAnno) {
            var mode = ROMAN[parseInt(header.mode, 10)] || '';
            score.annotation = mode ? new exsurge.Annotations(ctxt, '%' + PART_ABBR[part] + '%', '%' + mode + '%')
                                    : new exsurge.Annotations(ctxt, '%' + PART_ABBR[part] + '%');
          }
          var width = o.width || Math.min(container.clientWidth || 600, 720);
          ctxt.width = width;
          score.performLayoutAsync(ctxt, function () {
            try {
              score.layoutChantLines(ctxt, width);
              // one drawing per staff line, so that a long chant can run across pages
              var lines = score.createSvgNodeForEachLine(ctxt);
              if (lines && !lines.length && lines.nodeType) lines = [lines];
              container.innerHTML = '';
              // exsurge draws notes as references (<use>) to glyphs defined once, in the first line.
              // Printing does not follow such references reliably, so every reference is replaced by a
              // copy of the glyph itself: each line then carries its own notes, on screen and on paper.
              var glyphs = {};
              Array.prototype.forEach.call(lines, function (svg) {
                Array.prototype.forEach.call(svg.querySelectorAll('defs [id]'), function (n) { glyphs[n.getAttribute('id')] = n; });
              });
              Array.prototype.forEach.call(lines, function (svg) {
                Array.prototype.slice.call(svg.querySelectorAll('use')).forEach(function (u) {
                  var h = u.getAttribute('xlink:href') || u.getAttribute('href') || '';
                  var g = glyphs[h.replace(/^#/, '')];
                  if (!g) { u.parentNode.removeChild(u); return; }
                  var x = parseFloat(u.getAttribute('x')) || 0, y = parseFloat(u.getAttribute('y')) || 0;
                  var wrap = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                  wrap.setAttribute('transform', 'translate(' + x + ',' + y + ')');
                  if (u.getAttribute('class')) wrap.setAttribute('class', u.getAttribute('class'));
                  if (u.getAttribute('fill')) wrap.setAttribute('fill', u.getAttribute('fill'));
                  if (u.getAttribute('style')) wrap.setAttribute('style', u.getAttribute('style'));
                  var copy = g.cloneNode(true);
                  copy.removeAttribute('id');
                  wrap.appendChild(copy);
                  u.parentNode.replaceChild(wrap, u);
                });
              });
              Array.prototype.forEach.call(lines, function (svg) {
                var w = parseFloat(svg.getAttribute('width')), h = parseFloat(svg.getAttribute('height'));
                if (w && h && !svg.getAttribute('viewBox')) svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
                svg.removeAttribute('width'); svg.removeAttribute('height');
                container.appendChild(el('div', {class: 'line'}, [svg]));
                // fit the frame to what the line actually draws (exsurge places later lines above their frame)
                try {
                  var b = svg.getBBox(), vb = svg.getAttribute('viewBox').split(/\s+/).map(Number);
                  // a stray element can report an absurd size: never let the frame grow beyond twice the line
                  var hh = (b.height > 0 && b.height < vb[3] * 2) ? b.height + 6 : vb[3] + 6;
                  // (the later lines of a long chant drift ever higher above their frame, so b.y itself is not bounded)
                  if (isFinite(b.y) && b.height > 0 && b.height < vb[3] * 2) svg.setAttribute('viewBox', [vb[0], (b.y - 3).toFixed(2), vb[2], hh.toFixed(2)].join(' '));
                } catch (e) {}
              });
            } catch (e) { showError(container, e); }
            resolve();
          });
        } catch (e) { showError(container, e); resolve(); }
      });
    });
    return renderQueue;
  }
  function showError(container, e) {
    container.innerHTML = '';
    container.appendChild(el('p', {class: 'error', text: 'This chant could not be drawn (' + e.message + '). The GABC can still be edited below.'}));
    if (window.console) console.error(e);
  }

  // ---------------------------------------------------------------- selectors
  function fillMassSelect() {
    var sel = $('#selMass');
    sel.innerHTML = '';
    D.sections.forEach(function (s) {
      var og = el('optgroup', {label: s.title + ' — ' + s.en});
      s.items.forEach(function (k) { og.appendChild(el('option', {value: k, text: clean(D.masses[k].title)})); });
      sel.appendChild(og);
    });
  }
  function chantOptions(part, current) {
    var sel = el('select', {class: 'chant-select', 'aria-label': PART_EN[part] + ' chant'});
    sel.appendChild(el('option', {value: '', text: '(none)'}));
    var og = el('optgroup', {label: 'All ' + PART_NAME[part] + ' chants'});
    Object.keys(D.chants).filter(function (id) { return D.chants[id].p === part; })
      .sort(function (a, b) { return D.chants[a].i.localeCompare(D.chants[b].i); }).forEach(function (id) {
        var c = D.chants[id];
        og.appendChild(el('option', {value: id, text: clean(c.i) + (c.roman ? (/Franciscan/.test(c.i) ? ' — Franciscan Graduale' : ' — Roman Graduale') : ' — p. ' + c.pg), selected: String(current) === id ? 'selected' : null}));
      });
    sel.appendChild(og);
    return sel;
  }

  // ---------------------------------------------------------------- seasons
  function seasonOfDate(d) {
    var E = easter(d.getFullYear()), f = diffDays(d, E);
    if (f >= -63 && f < 0) return 'lent';
    if (f >= 0 && f < 56) return 'pasch';
    return 'annum';
  }
  function currentSeason() {
    if (state.season !== 'auto') return state.season;
    return seasonOfDate(state.date || new Date());
  }
  // the chants of a Mass for the season: Tract from Septuagesima, two Alleluias in Paschaltide
  function massParts(key) {
    var m = D.masses[key], parts = {};
    PARTS.forEach(function (p) { parts[p] = (m.parts[p] || []).slice(); });
    var temporal = isTemporal(key), se = m.season || {}, s = currentSeason();
    if (!temporal && s === 'lent' && se.lent && se.lent.tr) { parts.al = []; parts.tr = se.lent.tr.slice(); }
    if (!temporal && s === 'pasch' && se.pasch) {
      if (se.pasch.al) { parts.gr = []; parts.al = se.pasch.al.slice(); parts.tr = []; }
      ['in', 'of', 'co'].forEach(function (p) { if (se.pasch[p]) parts[p] = se.pasch[p].slice(); });
    }
    if (s !== 'lent' && !temporal) parts.tr = parts.al.length ? [] : parts.tr;
    if (s === 'lent') parts.al = [];   // from Septuagesima no Alleluia at all; the Tract (if any) takes its place (XIII, 7)
    if (s !== 'lent' && parts.al.length && parts.tr.length && !isEmber(key)) parts.tr = [];   // the Tract is only for Septuagesima-Lent (SCJ)
    if (s !== 'pasch' && !temporal && parts.al.length > 1 && !/Tempore Paschali/.test(m.title || '')) parts.al = parts.al.slice(0, 1);   // the second Alleluia is the Paschal one
    var d = state.date;
    if (ferialUseOfSunday(key, d)) {
      if (/^Pasc/.test(key)) {
        // a feria of Paschaltide: one verse, taken alternately from the Sunday's two (XIII, 1)
        if (parts.al.length > 1) parts.al = [parts.al[d.getDay() % 2 ? 0 : 1]];
      } else {
        parts.al = [];                                  // on ferias the Alleluia is omitted entirely (XIII, 6; XVII)
        if (/^(7a|6a|5a)$/.test(key)) parts.tr = [];    // nor is the Tract said (XIII, 7)
      }
    }
    // Tempore Ascensionis (Ascension to the Vigil of Pentecost) the second Alleluia is the one the Missal gives for it
    if (!temporal && s === 'pasch' && se.asc && se.asc.al && parts.al.length > 1 && d) {
      var fA = diffDays(d, easter(d.getFullYear()));
      if (fA >= 39 && fA <= 48) parts.al = [parts.al[0], se.asc.al[0]];
    }
    if (key === 'C79s' && d) {
      var md = (d.getMonth() + 1) * 100 + d.getDate(), fE = diffDays(d, easter(d.getFullYear()));
      if (md >= 1225 || md <= 202) { parts.of = [{id: 8151}]; parts.co = [{id: 7543}]; }       // a Nativitate usque ad Purificationem
      if (fE >= 39 && fE <= 48 && parts.al.length > 1) parts.al = [parts.al[0], {id: 5526}];  // tempore Ascensionis
    }
    if (isEmber(key) && !/^Pent0/.test(key)) parts.al = [];
    if (isVigil(key) && !/^(Dec24|Jan5a|AscVig)$/.test(key) && !(key === 'Dec24' && d && d.getDay() === 0)) parts.al = [];
    if (/Innocent/.test(titleText(key)) && d && d.getDay() !== 0) parts.al = [];
    return parts;
  }
  function isTemporal(key) { return D.sections[0].items.indexOf(key) >= 0; }

  // ---------------------------------------------------------------- liturgical colour and class
  var COLORS = {white: '#ffffff', red: '#b3313d', green: '#5f8f5f', violet: '#6a3d8f', rose: '#d98aa6', black: '#111111'};
  var COLOR_LA = {white: 'White', red: 'Red', green: 'Green', violet: 'Violet', rose: 'Rose', black: 'Black'};
  function massColor(key, d) {
    var dd = d || state.date, d0IsSunday = function () { return !dd || dd.getDay() === 0; };
    var m = D.masses[key], t = clean(m.title || '').replace(/^\d+ [A-Za-z.]+ — /, '') + ' ' + clean(m.en || '').replace(/^[A-Za-z]+ \d+ — /, '');
    if (/^(Adv3|Quad4)$/.test(key)) return 'rose';
    if (m.color) return m.color;
    if (/Vigilia|Vigil of/.test(t) && !/Pasch|Pentecost|Nativ/.test(t)) return 'violet';
    if (/^(Adv|7a|6a|5a|Quad|EmbWed|EmbFri|EmbSat|Litaniis|Dec24)/.test(key) && !/Quad6h|Quad5f/.test(key)) return key === 'Quad6f' ? 'black' : 'violet';
    if (/^(Pent0|Pasc6s)/.test(key)) return 'red';
    if (/^(Pent1|Epi1)$/.test(key) && d0IsSunday()) return 'white';
    if (/^(Epi[1-6]|Pent\d)/.test(key) && !/^Pent0/.test(key)) return 'green';
    if (/Defunct|C114s|Mass for the Dead/.test(key + t)) return 'black';
    if (/Passione|Spiritu Sancto|C68s|C75s/.test(key + t)) return 'red';
    if (/\bMm?\.|Mart|Apost|Evang|Protomart|Innocent|Pretiosiss|Sanguin/.test(t) && !/Conversio|Cathedra|Ioannis Ap\. et Evang/.test(t)) return 'red';
    return 'white';
  }
  // class of a day of the Proper of the Time (rubrics of 1960)
  function temporalClass(key, d) {
    if (key === 'Epi' && d && !(d.getMonth() === 0 && d.getDate() === 6)) return 4;
    if (key === 'Jan1' && d && !(d.getMonth() === 0 && d.getDate() === 1)) return 4;
    if (key === 'Nat2' && d && d.getDay() !== 0 && !(d.getMonth() === 0 && d.getDate() === 2)) return 4;
    if (/^Dec25/.test(key) && d) return d.getDate() === 25 ? 1 : 2;
    if (/^(Pasc1|Epi[1-6]|Pent\d+)$/.test(key) && d && d.getDay() !== 0) return 4;
    if (/^Adv[1-4]$/.test(key) && d && d.getDay() !== 0) return (d.getMonth() === 11 && d.getDate() >= 17) ? 2 : 3;
    if (/^(Adv[1-4]|Quad[1-6]|Pasc0|Pasc1|Pent0|Pent1|Pasc6s|Dec24|Dec25|Jan1|Epi|Asc|CorpusChristi|SCJ|ChristusRex|5aw)$/.test(key)) return 1;
    if (/^Quad6|^Pasc0|^Pent0/.test(key)) return 1;
    if (d && d.getDay() === 0) return 2;
    if (/^Adv/.test(key) && d && d.getMonth() === 11 && d.getDate() >= 17) return 2;
    if (/^(Adv3[wfs]|EmbWedSept|EmbFriSept|EmbSatSept|Quad1[wfs]|Pent0)/.test(key)) return 2;
    if (/^(7a|6a|5a)$/.test(key) && d && d.getDay() !== 0) return 4;   // ferias of Septuagesima to Quinquagesima week
    if (key === 'AscVig') return 2;
    if (/^(5a|Quad)/.test(key)) return 3;
    return 4;
  }
  // vigils of the II class (rubrics of 1960): St John the Baptist, Sts Peter and Paul, the Assumption
  var VIGIL_CLASS = {G494: 2, G502_3: 2, S0814: 2};
  function feastClass(key) { return VIGIL_CLASS[key] || {I: 1, II: 2, III: 3}[D.masses[key].rank] || 4; }
  // the Annunciation and St Joseph when impeded (rubrics of 1960, nn. 95-96): the Annunciation falling from Palm Sunday
  // to Low Sunday goes to the Monday after Low Sunday; St Joseph falling in Holy Week goes to the Saturday before Palm
  // Sunday; either falling on a Sunday of Lent goes to the Monday
  function feastDate(key, y) {
    var m = D.masses[key], d = new Date(y, m.month, m.day);
    if (key !== 'S0325' && key !== 'S0319') return d;
    var E = easter(y), f = diffDays(d, E);
    if (key === 'S0325' && f >= -7 && f <= 7) return addDays(E, 8);
    if (key === 'S0319' && f >= -7 && f <= -1) return addDays(E, -8);
    if (d.getDay() === 0) return addDays(d, 1);
    return d;
  }

  // ---------------------------------------------------------------- rubrics of the Mass
  // Missale O.P. (1939), Rubricae generales: IX (Gloria), XIII (Gradual, Alleluia, Tract, Sequence),
  // XIV (Credo), XVI (Ite missa est / Benedicamus Domino), XVII (Mass of a feria).
  var SUNDAY_MASS = /^(Adv[1-4]|Epi[1-6]|Pent\d+|Pasc[1-6]|7a|6a|5a|Nat1)$/;
  function ferialUseOfSunday(key, d) { return !!(d && d.getDay() !== 0 && SUNDAY_MASS.test(key)); }
  function isRequiem(key) { return /^(C114s|S1102|S1113)$/.test(key) || /Defunct/.test(D.masses[key].title || ''); }
  function titleText(key) { var m = D.masses[key]; return clean(m.title || '') + ' ' + (m.name_en || '') + ' ' + clean(m.en || ''); }
  function isVigil(key) { return /Vigili|Vigil of|pridie/i.test(titleText(key)) && !/^(Pasc6s|Quad6s)$/.test(key); }
  function isEmber(key) { return /^(Adv3[wfs]|Quad1[wfs]|EmbWedSept|EmbFriSept|EmbSatSept|EmbSatSeptS|Pent0[wfs])$/.test(key); }
  function inSeptLent(d) { var E = easter(d.getFullYear()); return d >= addDays(E, -63) && d < addDays(E, -1); }
  // Gloria and Credo by the rubrics of 1960 followed by the Ordo O.P.: Gloria on Sundays outside Advent and
  // Septuagesima–Lent, on feasts of the I, II and III class and in the octaves, never on ferias, vigils or Ember days
  // (save Pentecost); Credo on Sundays, I class days, and II class feasts of Our Lord, Our Lady, the Apostles and Evangelists.
  function rubricsOf(key, d) {
    var m = D.masses[key], t = titleText(key), sun = d ? d.getDay() === 0 : true, temporal = isTemporal(key);
    var sec = (D.sections.filter(function (s) { return s.items.indexOf(key) >= 0; })[0] || {}).id;
    if (isRequiem(key)) return {gloria: false, credo: false, dismiss: 'req', requiem: true};
    var md = d ? (d.getMonth() + 1) * 100 + d.getDate() : 0, g, c;
    if (temporal) {
      var penitential = /^(Adv|7a|6a|5a|Quad)/.test(key) || key === 'Dec24';
      var ferial = ferialUseOfSunday(key, d) || (key === 'Epi' && md !== 106) || (key === 'Jan1' && md && md !== 101) ||
                   (key === 'Nat2' && d && !sun && md !== 102);
      g = !penitential && !ferial && !isVigil(key) && !(isEmber(key) && !/^Pent0/.test(key)) && key !== 'Litaniis';
      if (/^(Quad6h|Quad6s|Pasc6s)$/.test(key)) g = true;
      if (key === 'Quad6f') g = false;
      c = sun || /^(Dec25_[12]|Pasc0[mtwhfs]?|Asc|Pasc6s|Pent0[mtwhfs]?|CorpusChristi|SCJ|ChristusRex)$/.test(key) ||
          (key === 'Dec25_3' && md === 1225) || (key === 'Jan1' && md === 101) || (key === 'Epi' && md === 106) || (key === 'Nat2' && (sun || md === 102));
      if (key === 'Nat2') { g = !!(sun || md === 102); }
      if (/^(Quad6f|Quad6s)$/.test(key)) c = false;
    } else if (sec === 'votivae') {
      g = /Mari|Dominic|Thom|Sacrament|Corporis|Sacerdot/.test(t) && !(d && inSeptLent(d));
      c = false;
    } else {
      var cls = feastClass(key);
      g = !isVigil(key);
      c = !isVigil(key) && (sun || cls === 1 || /Apost|App\.|Evang/.test(t) ||
          (cls === 2 && /\bDomini\b|Christi|Iesu|Jesu|Crucis|Transfigur|Baptism|Mari[aæe]|B\. ?M\. ?V|Virginis Mari|Our Lady/.test(t)));
    }
    // Missale O.P. 1939, Rubricae generales XVI, 1: "Ite Missa est dicitur quotiescumque dictum est Gloria in excelsis. Et dum
    // non dicitur, ejus loco dicitur Benedicamus Domino" (Maundy Thursday: Ite Missa est, p. 166)
    return {gloria: g, credo: c, dismiss: g ? 'ite' : 'ben'};
  }

  // ---------------------------------------------------------------- the ring of the liturgical year
  function liturgicalYear(d) {
    var y = d.getFullYear();
    var adv = function (yy) { var n = new Date(yy, 11, 25); return addDays(n, -((n.getDay() || 7) + 21)); };
    var start = d >= adv(y) ? adv(y) : adv(y - 1), Y = start.getFullYear() + 1, E = easter(Y);
    var end = adv(Y);
    var seg = [
      ['Advent', start, new Date(Y - 1, 11, 25), 'violet'],
      ['Christmas', new Date(Y - 1, 11, 25), new Date(Y, 0, 14), 'white'],
      ['Epiphany', new Date(Y, 0, 14), addDays(E, -63), 'green'],
      ['Septuagesima', addDays(E, -63), addDays(E, -46), 'violet'],
      ['Lent', addDays(E, -46), E, 'violet'],
      ['Eastertide', E, addDays(E, 49), 'white'],
      ['Pentecost', addDays(E, 49), addDays(E, 56), 'red'],
      ['After Pentecost', addDays(E, 56), end, 'green']
    ];
    return {start: start, end: end, seg: seg, total: diffDays(end, start)};
  }
  var SVGNS = 'http://www.w3.org/2000/svg';
  function sv(tag, attrs, text) {
    var e = document.createElementNS(SVGNS, tag);
    Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (text != null) e.textContent = text;
    return e;
  }
  var WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  // the day, in the side column
  function drawRing() {
    var d = state.date || new Date(), m = D.masses[state.key] || {};
    var today = diffDays(d, new Date()) === 0;
    var set = function (id, t) { var e = document.getElementById(id); if (e) e.textContent = t; };
    set('dayDate', WEEKDAYS[d.getDay()].slice(0, 3) + ' ' + d.getDate() + ' ' + MONTHS[d.getMonth()].slice(0, 3) + ' ' + d.getFullYear() + (today ? ' · Today' : ''));
    set('dayTitle', clean(m.title || '').replace(/^\d+ [A-Za-z.]+ — /, ''));
    set('daySub', m.name_en || clean(m.en || '').replace(/^[A-Z][a-z]{2} \d+ — /, ''));
    if (state.cal) state.cal.set(d);
  }
  function wrap(text, n) {
    var out = [], line = '';
    text.split(/\s+/).forEach(function (w) {
      if ((line + ' ' + w).trim().length > n && line) { out.push(line); line = w; } else line = (line + ' ' + w).trim();
    });
    if (line) out.push(line);
    return out;
  }
  function drawPills() {
    var m = D.masses[state.key], box = $('#pills');
    if (!box || !m) return;
    var col = massColor(state.key, state.date);
    box.innerHTML = '';
    var dot = el('span', {class: 'dot' + (col === 'white' ? ' white' : ''), 'aria-hidden': 'true'});
    dot.style.background = COLORS[col];
    var cls = m.rank || (isTemporal(state.key) ? ['', 'I', 'II', 'III', 'IV'][temporalClass(state.key, state.date)] : '');
    var bits = [COLOR_LA[col]];
    if (cls) bits.push(cls + ' class');
    if (!isTemporal(state.key)) bits.push({annum: 'Per annum', lent: 'Septuagesima–Lent', pasch: 'Paschaltide'}[currentSeason()]);
    box.appendChild(dot);
    box.appendChild(document.createTextNode(bits.join(' · ')));
  }

  // ---------------------------------------------------------------- the page
  function occursOn(key, d) { var r = massesOf(d); return r.temp.concat(r.feasts, r.beati).indexOf(key) >= 0; }
  function nextDateOf(key) {
    var d0 = new Date(); d0.setHours(12, 0, 0, 0);
    for (var i = 0; i < 400; i++) { var d = addDays(d0, i); if (occursOn(key, d)) return d; }
    return null;
  }
  function showMass(key, over) {
    var m = D.masses[key];
    if (!m) return;
    state.key = key;
    state.edited = {};
    // a Mass picked from the list is shown for the next day it is said (a Sunday Mass on its Sunday, with its Alleluia
    // and its Preface), not for whatever day happens to be selected
    if (!state.date || !occursOn(key, state.date)) {
      state.date = nextDateOf(key);
      if ($('#date')) $('#date').value = state.date ? iso(state.date) : '';
    }
    var def = massParts(key);
    state.parts = {};
    PARTS.forEach(function (p) {
      state.parts[p] = (over && over[p]) ? over[p].map(function (id) { return {id: id, chosen: true}; }) : def[p];
    });
    $('#selMass').value = key;
    drawRing(); drawPills(); drawMass(); writeHash();
    document.title = clean(m.title) + ' — Propria Missae O.P.';
  }

  var ORD_LABEL = {pf: 'Praefatio', as: 'Asperges', ky: 'Kyrie', gl: 'Gloria', cr: 'Credo', sa: 'Sanctus', ag: 'Agnus Dei', it: 'Ite, missa est'};
  // The Ordinary of the day. Kyriale O.P. (1950): I in festis totis duplicibus (I class); II in festis duplicibus et
  // Dominicis (II class, Sundays); III in festis simplicibus (III class); IV Tempore Paschali; V in Sabbatis de B. Virgine;
  // VI infra octavas simplices et in Missis votivis; VIII profestis diebus (ferias). Parts not in GregoBase's Kyriale
  // are taken from the nearest Mass that has them.
  var ORD_FALLBACK = {I: ['II'], II: ['I'], III: ['II'], IV: ['I'], V: ['II'], VI: ['V', 'II'], VIII: ['VI']};
  function easterOctave(d) { if (!d) return false; var f = diffDays(d, easter(d.getFullYear())); return f >= -1 && f <= 6; }
  function paschaltide(d) { if (!d) return false; var f = diffDays(d, easter(d.getFullYear())); return f >= 0 && f <= 55; }
  // a feast or votive Mass of Our Lady
  function isMarian(key) {
    var m = D.masses[key] || {}, t = titleText(key).replace(/^.*?—\s*/, '');
    if (key === 'C79s' || key === 'C82s') return true;
    if (/^S\.\s*Mari(æ|ae)\s+ad Nives/i.test(t)) return true;                  // Our Lady of the Snows
    if (/^B\.\s*Mari(æ|ae)\s+(Virg|V\.)/i.test(t)) return true;               // B. Mariæ Virg. Reginæ, …
    if (/^Ss\.\s*Nominis\s+B/i.test(t)) return true;                         // Holy Name of Mary
    if (/^(S|Ss|SS|B|Bb)\.\s/.test(t)) return false;                           // a saint or blessed (St Joseph, St Anne, Bl. Maria …)
    return /\bMari(a|ae|æ|e)(?![a-zæ])|B\. ?M\. ?V|Virginis Mari|Our Lady|Deipar|Rosarii|Immaculat|Beatae Virginis/i.test(t + ' ' + (m.name_en || ''));
  }
  // The Kyriale O.P. after the rubrics of 1960 (Fr. A. Thompson, "The Gloria and Credo in the post-1960 Dominican Rite"):
  // I class I (of Our Lady V); Sundays II; II class III (of Our Lady V); III class VI (of Our Lady, and her Saturdays, V);
  // ferias and days of penance "Profestis diebus" (VIII in the GregoBase numbering, p. 145*).
  function autoKyriale(key, d) {
    var temporal = isTemporal(key);
    var sec = (D.sections.filter(function (s) { return s.items.indexOf(key) >= 0; })[0] || {}).id;
    var R = rubricsOf(key, d), sunday = d && d.getDay() === 0;
    if (!R.gloria && !sunday) return 'VIII';
    if (isMarian(key)) return 'V';
    if (sec === 'votivae') return 'VI';
    var cls = temporal ? temporalClass(key, d) : feastClass(key);
    if (temporal && sunday && !/^(Pasc0|Pent0)$/.test(key)) return 'II';      // all Sundays but Easter and Pentecost
    if (cls === 1) return 'I';
    if (sunday) return 'II';
    if (cls === 2) return 'III';
    if (cls === 3) return 'VI';
    return R.gloria ? 'VI' : 'VIII';
  }
  // In Paschaltide the Easter Kyrie (IV) on feasts of the I and II class not of Our Lady, and on Sundays
  function paschalKyrie(key, d) {
    if (!paschaltide(d) || isMarian(key) || key === 'Quad6s') return false;
    var cls = isTemporal(key) ? temporalClass(key, d) : feastClass(key);
    return cls <= 2 || (d && d.getDay() === 0);
  }
  function ordinaryIds() {
    var o = {}, R = rubricsOf(state.key, state.date), d = state.date;
    if (state.key === 'Quad6f') return o;   // Good Friday: no Ordinary
    var find = function (name) { var r = null; D.kyriale.forEach(function (id) { if (D.chants[id].i === name) r = id; }); return r; };
    // Asperges before the principal Mass on Sundays; Vidi aquam from Easter to Pentecost
    var asp = state.asp;
    // (not on Palm Sunday: the blessing of palms takes its place)
    if (!asp && d && d.getDay() === 0 && !R.requiem && state.key !== 'Quad6') { var f = diffDays(d, easter(d.getFullYear())); asp = (f >= 0 && f <= 49) ? 'vidi' : 'asperges'; }
    if (asp && asp !== 'none') o.as = asp === 'vidi' ? D.front[1] : D.front[0];
    if (state.ord === 'none') { if (R.credo && state.credo && state.credo !== 'none') o.cr = find('Credo ' + state.credo); return o; }
    if (R.requiem) { o.ky = find('Kyrie (Requiem)'); o.sa = find('Sanctus VIII'); o.ag = find('Agnus VIII'); o.it = find('Requiescant'); o.req = true; return o; }
    var num = state.ord || autoKyriale(state.key, d);
    var part = function (kind) {
      var chain = [num].concat(ORD_FALLBACK[num] || []), hit = null;
      chain.forEach(function (n) {
        if (hit) return;
        D.kyriale.forEach(function (id) {
          var nm = D.chants[id].i, m = /^(Kyrie|Gloria|Sanctus|Agnus|Ite|Benedicamus)\s+([IVX]+)\b/.exec(nm);
          if (m && m[1] === kind && m[2] === n && !hit) hit = id;
        });
      });
      return hit;
    };
    o.ky = (num === 'VIII' && find('Kyrie VIII - Profestis diebus')) || part('Kyrie');
    if (!state.ord && paschalKyrie(state.key, d)) { o.ky = find('Kyrie IV') || o.ky; o.pk = true; }
    if (R.gloria) o.gl = part('Gloria');
    o.sa = part('Sanctus'); o.ag = part('Agnus');
    // Ite missa est when the Gloria is said (with two Alleluias in the Easter octave); otherwise Benedicamus Domino (XVI, 1)
    // Missale O.P. 1939, Appendix pp. 33-34 (Toni Ite, Missa est, etc.): the Benedicamus of Advent and Septuagesima-Lent
    // Sundays, the Vigil of Christmas and the Holy Innocents is the tone of Totis Duplicibus (Ite II); Saturdays of Our Lady
    // in Septuagesima, that of Ite V; semidoubles and simples in Septuagesima and votive Masses, that of Ite VI; ferias,
    // vigils, Ember days and feasts of three lessons, Benedicamus VIII (in profestis diebus)
    if (R.dismiss === 'ben') {
      var sec = (D.sections.filter(function (s) { return s.items.indexOf(state.key) >= 0; })[0] || {}).id, tempo = isTemporal(state.key);
      var bn = (tempo && d && d.getDay() === 0) || state.key === 'Dec24' || /Innocent/.test(titleText(state.key)) ? 'Ite II' :
        state.key === 'C79s' ? 'Ite V' : (sec === 'votivae' || (!tempo && !isVigil(state.key))) ? 'Ite VI' : null;
      o.it = (bn && find(bn)) || find('Benedicamus VIII');
    }
    else o.it = (easterOctave(d) || state.key === 'Quad6s') ? find('Ite IV') : (part('Ite') || find('Ite I'));
    // a Credo chosen under Options is sung even on a day whose rubrics do not require it
    if ((R.credo && state.credo !== 'none') || (state.credo && state.credo !== 'none')) o.cr = find('Credo ' + (state.credo || 'I'));
    o.num = num;
    return o;
  }

  // ---------------------------------------------------------------- the Preface of the day
  // Rubricae generales XV, 2: the Preface of the season is said also on feasts that have none of their own;
  // Sundays per annum the Preface of the Trinity; otherwise the Common Preface.
  function seasonPreface(d) {
    var y = d.getFullYear(), E = easter(y), f = diffDays(d, E), md = (d.getMonth() + 1) * 100 + d.getDate();
    if (md >= 1225 || md <= 105) return 'Nativitate';
    if (md >= 106 && md <= 113) return 'Epiphania';
    if (f >= -46 && f <= -15) return 'Quadragesima';
    if (f >= -14 && f <= -3) return 'Sancta Cruce';
    if (f >= -1 && f <= 38) return 'Paschalis';
    if (f >= 39 && f <= 47) return 'Ascensione';
    if (f >= 48 && f <= 55) return 'Spiritu Sancto';
    // within Octaves whose feast has its own Preface (the Prefaces' rubrics: "et dicatur per totam Octavam, etiam in festis
    // Sanctorum, nisi propriam habuerint"; on a resumed Sunday "Praefatio Octavae"), but never in the Mass of the Sunday
    if (d.getDay() === 0) return null;
    if (f >= 57 && f <= 59) return 'SS. Trinitate';                 // SS. Trinitatis, per Octavam usque ad quintam Feriam exclusive
    if (f >= 69 && f <= 75) return 'Corde Iesu';                    // SS. Cordis Jesu, per totam Octavam
    if (md >= 630 && md <= 706) return 'Apostolis';                 // SS. Petri et Pauli, Octava solemnis
    if (md >= 805 && md <= 811) return 'Dominico';                  // S. P. N. Dominici, Octava solemnis
    if (md >= 816 && md <= 822) return 'B. Maria Virgine';          // Assumptionis, Octava solemnis
    if (md >= 1209 && md <= 1215) return 'B. Maria Virgine';        // Conceptionis Immaculatae, Octava solemnis
    return null;
  }
  // Missale O.P. 1939: Transfiguration "Praefatio de Trinitate"; the Crown of Thorns has none of its own (so that of the
  // season); in all Masses of St Dominic his own; votive Masses with their own (Rubr. gen. XV, 2 and the Prefaces' rubrics)
  var PREF39 = {S0806: 'SS. Trinitate', S0424: '', S0524: 'Dominico', S0531: 'B. Maria Virgine', C68s: 'Sancta Cruce',
    C75s: 'Spiritu Sancto', C82s: 'B. Maria Virgine'};
  function prefaceOf(key, d) {
    var m = D.masses[key], temporal = isTemporal(key), R = rubricsOf(key, d);
    if (key === 'Quad6f' || !window.PREFACES) return null;
    if (R.requiem) return 'Defunctorum';
    var mp = PREF39.hasOwnProperty(key) ? PREF39[key] : m.pref;
    if (mp && PREFACES[mp]) return mp;
    if (key === 'SCJ') return 'Corde Iesu';
    if (key === 'ChristusRex') return 'D. N. Iesu Christo';
    if (key === 'S1004') return 'Francisco';   // Missale O.P. 1939, Appendix: in all Masses of St Francis
    if (key === 'C79s' || /in Sabbato/.test(m.title || '')) {
      // Saturday of Our Lady: from Christmas to the Purification the Mass Vultum tuum with the Preface of the Nativity
      var md = d ? (d.getMonth() + 1) * 100 + d.getDate() : 0;
      return (md >= 1225 || (md && md <= 202)) ? 'Nativitate' : 'B. Maria Virgine';
    }
    if (key === 'Pent1') return d && d.getDay() !== 0 && diffDays(d, easter(d.getFullYear())) > 59 ? 'Communis' : 'SS. Trinitate';
    var s = d ? seasonPreface(d) : keyPreface(key);
    if (s) return s;
    if (isSundayMass(key, d)) return 'SS. Trinitate';
    return 'Communis';
  }
  // a Sunday Mass sung on its Sunday (or opened without a date): never the ferial Preface or tone
  var SUNDAY_KEY = /^(Adv[1-4]|Nat[12]|Epi[1-6]r?|7a|6a|5a|Quad[1-6]|Pasc[0-6]|Pent\d+)$/;
  function isSundayMass(key, d) { return SUNDAY_KEY.test(key) && (!d || d.getDay() === 0); }
  function keyPreface(key) {
    if (/^Nat/.test(key)) return 'Nativitate';
    if (/^Quad[1-4]/.test(key)) return 'Quadragesima';
    if (/^Quad[56]/.test(key)) return 'Sancta Cruce';
    if (/^Pasc[0-5]/.test(key)) return 'Paschalis';
    if (/^Pasc6/.test(key)) return 'Ascensione';
    if (/^Pent0/.test(key)) return 'Spiritu Sancto';
    return null;
  }
  var BVM_WORD = [[/C82s/, 'Veneratióne sanctíssimi Rosárii', 'veneration of the most holy Rosary'], [/Annuntiat/, 'Annuntiatióne', 'Annunciation'], [/Visitat/, 'Visitatióne', 'Visitation'], [/Assumpt/, 'Assumptióne', 'Assumption'],
    [/Nativit/, 'Nativitáte', 'Nativity'], [/Pr(ae|æ)sentat/, 'Præsentatióne', 'Presentation'], [/Concept/, 'Conceptióne immaculáta', 'Immaculate Conception'],
    [/Dolor|Septem|Compassion/, 'Compassióne', 'Compassion'], [/Rosar|Cordis|Nominis|Regin|Lauret/, 'Solemnitáte', 'Solemnity'],
    [/Apparitio/, 'Conceptióne immaculáta', 'Immaculate Conception'], [/Sabbat|C79s/, 'Veneratióne', 'Veneration']];
  // the word of the Preface of Our Lady: by the feast, or within the Octaves of the Assumption and the Immaculate Conception
  function bvmWord(key, d) {
    var t = titleText(key) + ' ' + key, w = BVM_WORD.filter(function (x) { return x[0].test(t); })[0];
    if (w) return w;
    var md = d ? (d.getMonth() + 1) * 100 + d.getDate() : 0;
    if (md >= 816 && md <= 822) return BVM_WORD[3];
    if (md >= 1209 && md <= 1215) return BVM_WORD[6];
    return null;
  }
  function prefaceText(name, key, d) {
    var p = PREFACES[name], la = p.la, en = p.tr, t = titleText(key) + ' ' + key;
    if (name === 'B. Maria Virgine') {
      var w = bvmWord(key, d) || [null, 'Festivitáte', 'Feast'];
      la = la.replace('{Festivitáte}', w[1]); en = en.replace('{Feast}', w[2]);
    }
    if (name === 'S. Ioseph') { la = la.replace('{Festivitáte}', 'Festivitáte'); en = en.replace('{Feast}', 'Feast'); }
    if (name === 'Paschalis') {
      var f = d ? diffDays(d, easter(d.getFullYear())) : 10;
      var v = f === -1 ? ['in hac potíssimum nocte', 'on this night above all'] : (f >= 0 && f <= 6 ? ['in hac potíssimum die', 'on this day above all'] : ['in hoc potíssimum', 'at this time above all']);
      la = la.replace('{in hoc potíssimum}', v[0]); en = en.replace('{at this time above all}', v[1]);
    }
    if (name === 'Spiritu Sancto') {
      var g = d ? diffDays(d, easter(d.getFullYear())) : 0, oct = g >= 48 && g <= 55;
      la = la.replace(' {hodiérna die}', oct ? ' hodiérna die' : ''); en = en.replace(' {on this day}', oct ? ' on this day' : '');
    }
    return {name: p.name, en: p.en, la: la, tr: en};
  }
  // the Preface sung from the Missale O.P. (1939), Appendix: solemn tone on days of the I and II class, ferial tone
  // otherwise where the Appendix gives one (Lent, Holy Cross, Paschaltide, the Common); the Requiem Preface is ferial.
  // The Sacred Heart and St Thomas have no chant there: they are fitted to the solemn tone (tools/pdfomr/adapt_pref.py)
  var PREF_SLUG = {'Nativitate': 'nativitate', 'Epiphania': 'epiphania', 'Quadragesima': 'quadragesima', 'Sancta Cruce': 'cruce', 'Paschalis': 'paschalis',
    'Ascensione': 'ascensione', 'Spiritu Sancto': 'spiritu-sancto', 'SS. Trinitate': 'trinitate', 'D. N. Iesu Christo': 'christo-rege',
    'B. Maria Virgine': 'bmv', 'S. Ioseph': 'ioseph', 'Apostolis': 'apostolis', 'Dominico': 'dominico', 'Francisco': 'francisco', 'Communis': 'communis',
    'Defunctorum': 'defunctorum', 'Corde Iesu': 'corde-iesu', 'S. Thoma Aquinate': 'thoma'};
  var PREF_FERIAL = {'Quadragesima': 1, 'Sancta Cruce': 1, 'Paschalis': 1, 'Communis': 1, 'Defunctorum': 1};
  var BVM_SYL = {'Annuntiatióne': 'An-nun-ti-a-ti-ó-ne', 'Visitatióne': 'Vi-si-ta-ti-ó-ne', 'Assumptióne': 'As-sump-ti-ó-ne', 'Nativitáte': 'Na-ti-vi-tá-te',
    'Præsentatióne': 'Præ-sen-ta-ti-ó-ne', 'Conceptióne immaculáta': 'Con-cep-ti-ó-ne im-ma-cu-lá-ta', 'Transfixióne': 'Trans-fi-xi-ó-ne',
    'Solemnitáte': 'So-lem-ni-tá-te', 'Compassióne': 'Com-pas-si-ó-ne', 'Veneratióne': 'Ve-ne-ra-ti-ó-ne', 'Veneratióne sanctíssimi Rosárii': 'Ve-ne-ra-ti-ó-ne sanc-tís-si-mi Ro-sá-ri-i', 'Festivitáte': 'Fe-sti-vi-tá-te'};
  // Missale O.P. 1939, Appendix: the Prefaces "cum cantu solemni" on Sundays and in all feasts Simplex and above and
  // through their octaves; "cum cantu feriali" in profestis diebus and feasts of three lessons. The Pater noster the
  // same: "Cantus ferialis dicitur in festis trium Lectionum et in diebus ferialibus, et in Missis Defunctorum".
  // Ferias, vigils and Ember days (outside the octave of Pentecost) are profestis dies; so are Monday to Wednesday of
  // Holy Week (the Preface of the Cross, ferial "a Dominica Passionis usque ad Cenam Domini exclusive"). Votive Masses
  // are ferial unless sung pro causa publica (Rubr. gen. XV, 2). Feasts of three lessons are not yet told apart
  // from the 1960 classes (tools/RANKS_PLAN.md): every Mass of a Saint or Blessed counts as Simplex or above.
  function solemnDay(key, d) {
    if (isRequiem(key)) return false;
    if (isSundayMass(key, d)) return true;
    if (D.sections.some(function (x) { return x.id === 'votivae' && x.items.indexOf(key) >= 0; })) return false;
    if (isVigil(key) || (isEmber(key) && !/^Pent0/.test(key))) return false;
    if (!isTemporal(key)) return true;
    if (/^(Quad6[mtw]|5aw)$/.test(key)) return false;   // Ash Wednesday: "in capite Jejunii" ferial
    return temporalClass(key, d) === 1;
  }
  function prefaceChant(name, key, d) {
    var slug = PREF_SLUG[name]; if (!slug) return null;
    var tone = name === 'Defunctorum' ? 'ferial' : (!PREF_FERIAL[name] || solemnDay(key, d) ? 'solemn' : 'ferial');
    var f = d ? diffDays(d, easter(d.getFullYear())) : 10;
    if (name === 'Paschalis' && tone === 'solemn') slug = 'paschalis-die';
    var fix = function (b) {
      if (name === 'Paschalis' && tone === 'solemn') {
        if (f === -1) b = b.replace('di(h)e(h)', 'noc(h)te(h)');
        else if (!(f >= 0 && f <= 6)) b = b.replace('hac(h)', 'hoc(h)').replace(' di(h)e(h)', '');
      }
      if (name === 'Spiritu Sancto' && !(f >= 48 && f <= 55)) b = b.replace(/ho\(g\)di\(g\)ér\(g\)na\(g\) di\(g\)e\(g\) \(;\) /, '');
      if (name === 'B. Maria Virgine') {
        var w = bvmWord(key, d);
        var syl = BVM_SYL[w ? w[1] : 'Festivitáte'] || BVM_SYL['Festivitáte'];
        b = b.replace('Fe(h)sti(h)vi(h)tá(h)te(h)', syl.split(' ').map(function (wd) { return wd.split('-').map(function (s) { return s + '(h)'; }).join(''); }).join(' '));
      }
      return b;
    };
    return {id: 'op-m39-praef-' + slug + '-' + tone, tone: tone, adapted: name === 'Corde Iesu' || name === 'S. Thoma Aquinate', fix: fix};
  }
  function drawPreface(key, d, R) {
    var name = prefaceOf(key, d);
    if (!name) return null;
    var P = prefaceText(name, key, d), PC0 = prefaceChant(name, key, d), solemn = PC0 ? PC0.tone === 'solemn' : solemnDay(key, d);
    var dialogue = null;
    D.kyriale.forEach(function (id) { if (D.chants[id].i === (solemn ? 'Ad Praefationem in tono solemni' : 'Ad Praefationem in tono feriali')) dialogue = id; });
    var box = el('section', {class: 'part preface', 'data-part': 'pf'});
    box.appendChild(el('div', {class: 'part-head hide-print'}, [el('h2', {text: 'Praefatio'}), el('span', {class: 'incipit', text: P.name}),
      el('span', {class: 'mode', text: solemn ? 'tono solemni' : 'tono feriali'})]));
    box.appendChild(el('h2', {class: 'print-only', text: 'Praefatio · ' + P.name}));
    var PC = prefaceChant(name, key, d);
    if (PC && state.ordo !== 'low') {
      var cb = el('div', {class: 'chant'});
      box.appendChild(cb);
      loadGabc(PC.id).then(function (t) { var g = splitGabc(t); renderInto(cb, PC.fix(g.body), g.header, null); }, function (e) { showError(cb, e); });
      if (PC.adapted) box.appendChild(el('p', {class: 'rubric', text: 'No chant is printed in the Missale O.P. for this Preface: its text is fitted to the solemn tone.'}));
    } else if (dialogue && state.ordo !== 'low') {
      var cb2 = el('div', {class: 'chant'});
      box.appendChild(cb2);
      loadGabc(dialogue).then(function (t) { var g = splitGabc(t); renderInto(cb2, g.body, g.header, null); }, function (e) { showError(cb2, e); });
    }
    // when the Preface is sung the chant already carries the Latin: only the English is added
    var sungPf = !!((PC || dialogue) && state.ordo !== 'low');
    box.appendChild(el('div', {class: 'r-cols pf-text' + (sungPf ? ' pf-sung' : '')}, [sungPf ? null : el('p', {class: 'la', lang: 'la', text: P.la}), el('p', {class: 'en-text', lang: 'en', text: P.tr})]));
    if (!sungPf) box.appendChild(el('p', {class: 'pf-sanctus', text: 'Sanctus, Sanctus, Sanctus…'}));
    return box;
  }

  // readings that change with the season within one Mass
  function seasonalReadings(key, d) {
    if (key !== 'C79s' || !d) return null;
    var md = (d.getMonth() + 1) * 100 + d.getDate(), fE = diffDays(d, easter(d.getFullYear()));
    if (md >= 1225 || md <= 202) return [{type: 'Epistle', ref: 'Ad Titum 3: 4-7'}, {type: 'Gospel', ref: 'Lucas 2: 15-19'}];
    if (fE >= 0 && fE <= 55) return [{type: 'Lesson', ref: 'Ecclesiasticus 24: 14-16'}, {type: 'Gospel', ref: 'Joannes 19: 25-27'}];
    return null;
  }

  // the order of the Mass: Introit, Kyrie, Gloria; the lessons, each followed by its gradual; after the Epistle
  // the Gradual, Alleluia or Tract and Sequence; the Gospel; Credo; Offertory; Sanctus, Agnus Dei; Communion; dismissal
  function massSequence(m, parts) {
    var HT = window.HW_TEXT && HW_TEXT[state.hwr] && HW_TEXT[state.hwr][state.key];
    var HW0 = window.HOLYWEEK && HOLYWEEK[state.key], skip = (HW0 && HW0.skipChants) || [];
    var HW = state.hwr !== '1939' && window.HOLYWEEK && HOLYWEEK[state.key];
    var rs = seasonalReadings(state.key, state.date) || (HW && HW.readings) || m33Readings(state.key, m.readings) || [], pre = rs.filter(function (r) { return r.type !== 'Gospel'; }), gos = rs.filter(function (r) { return r.type === 'Gospel'; });
    var q = [], ch = function (p) { (parts[p] || []).forEach(function (c, i) { if (skip.indexOf(c.id) < 0) q.push({t: 'chant', p: p, i: i, c: c}); }); };
    var take = function (p, i) { var c = (parts[p] || [])[i]; if (c) q.push({t: 'chant', p: p, i: i, c: c}); };
    // with the Order of Mass (state.ordo: low, sung, solemn) its prayers and rubrics go between the chants;
    // at a Low Mass the Ordinary is said, not sung
    var O = window.ORDO && state.ordo && state.key !== 'Quad6f' ? state.ordo : '', R = O ? rubricsOf(state.key, state.date) : {};
    var od = function (k) { if (O) q.push({t: 'ordo', k: k}); };
    var orat = function (k) { var x = window.ORATIONS && ORATIONS[state.key]; if (x && x[k]) q.push({t: 'oratio', k: k, x: x[k], src: x.src}); };
    var STRIP = {ky: 'rKy', gl: 'rGl', cr: 'rCr', sa: 'rSa', ag: 'rAg'};
    var ord = function (k) {
      if (O && STRIP[k] && !(k === 'gl' && !R.gloria) && !(k === 'cr' && !R.credo)) q.push({t: 'ordo', k: STRIP[k]});
      if (O === 'low') { if (k === 'ky' || (k === 'gl' && R.gloria) || (k === 'cr' && R.credo) || k === 'sa' || (k === 'ag' && !m.noAgnus)) q.push({t: 'ordo', k: k + 'Low'}); }
      else q.push({t: 'ord', k: k});
    };
    if (HT) {
      // Holy Week: the rite transcribed exactly as the chosen book prints it; the Ordinary and the
      // Order of Mass go where the book's markers (X) say
      var X = function (x) {
        if (x === 'start') { if (O === 'low') od('chalice'); od('foot'); }
        else if (/^(ky|gl|cr|sa|ag)$/.test(x)) { if (!(x === 'ag' && m.noAgnus)) ord(x); }
        else if (x === 'gradualEnd') { if (O && O !== 'low') od('chalice'); }
        else if (x === 'offer') od('offerDial');
        else if (x === 'pref') q.push({t: 'pref'});
        else if (x === 'canon') { od('canon'); od('pater'); ord('ag'); od('communion'); }
        else if (x === 'dismiss') { if (O === 'low') od('dismiss'); else q.push({t: 'ord', k: 'it'}); }
        else if (x === 'endNoGospel') od('endNoGospel');
        else if (x === 'canonNoAg') { od('canon'); od('pater'); od('communion'); }
        else od(x);
      };
      HT.forEach(function (sec, n) {
        var chunk = [], started = false;
        var flush = function () {
          if (!chunk.length) return;
          q.push({t: 'hwtext', s: {la: sec.la, en: sec.en, src: sec.src, blocks: chunk, cont: started}, n: n});
          started = true; chunk = [];
        };
        sec.blocks.forEach(function (b) { if (b.t === 'X') { flush(); X(b.x); } else chunk.push(b); });
        flush();
      });
      return q;
    }
    if (state.hwr === '1939' && /^Quad6/.test(state.key)) {
      q.push({t: 'hwnote'});
      ['pr', 'in', 'gr', 'al', 'tr', 'se', 'ad', 'of', 'co', 'an'].forEach(function (p) { (parts[p] || []).forEach(function (c, i) { q.push({t: 'chant', p: p, i: i, c: c}); }); });
      return q;
    }
    var hw = function (at) { if (HW) HW.sections.forEach(function (s, i) { if (s.at === at) q.push({t: 'hw', s: s}); }); };
    hw('start'); ch('pr'); hw('afterPr');
    if (O === 'low' && !m.prophecies) od('chalice');
    if (!m.prophecies && !(HW && HW.noFoot)) od('foot');
    if (O && (parts['in'] || []).length) od('rIn');
    ch('in');
    if (!m.prophecies) { ord('ky'); ord('gl'); od('collect'); orat('or'); od('collectEnd'); }
    var gr = (parts.gr || []).length, tr = (parts.tr || []).length;
    if (m.prophecies) {
      // Holy Saturday, Vigil of Pentecost: prophecies, the last ones each followed by a tract; the Litany;
      // then the Mass begins with the Kyrie and Gloria
      var ptr = m.ptr != null ? m.ptr : tr, k = 0;
      pre.forEach(function (r, i) {
        if (i === m.prophecies) { ord('ky'); ord('gl'); od('collect'); orat('or'); od('collectEnd'); }
        q.push({t: 'read', r: r});
        if (i < m.prophecies && i >= m.prophecies - ptr) take('tr', k++);
        hw('lesson' + i);
        if (i === pre.length - 1) { ch('al'); for (var j = k; j < tr; j++) take('tr', j); }
      });
    } else {
      // each lesson is followed by its gradual, in order; the last one also by the Alleluia or Tract
      // m.grAt: the lesson after which each gradual (or hymn) is sung, where the Graduale lacks some of them
      var gi = 0, at = m.grAt || null, al = (parts.al || []).length, ai = 0;
      pre.forEach(function (r, i) {
        q.push({t: 'read', r: r});
        var last = i === pre.length - 1;
        if (at) { at.forEach(function (li, j) { if (li === i && j < gr) take('gr', j); }); if (last) gi = gr; }
        else if (!last && gi < gr) take('gr', gi++);
        // Ember Wednesday of Pentecost: an Alleluia after each lesson (XIII, 3)
        if (m.alEach && !last && ai < al - 1) take('al', ai++);
        hw('lesson' + i);
        if (last) {
          for (; gi < gr; gi++) take('gr', gi);
          for (; ai < al; ai++) take('al', ai);
          ch('tr');
        }
      });
      if (!pre.length) { ch('gr'); ch('al'); ch('tr'); }
    }
    if (O && !m.prophecies) od('rGr');
    ch('se');
    if (O && O !== 'low') od('chalice');
    state._gos = gos[0] || null;
    var passion = gos.some(function (r) { return r.passion; });
    if (gos.length && !passion) od('gospel');
    gos.forEach(function (r) { q.push({t: 'read', r: r}); });
    if (gos.length && !passion) od('afterGospel');
    hw('afterGospel');
    ch('ad');
    ord('cr'); od('offerDial'); ch('of'); od('offertory'); orat('se'); od('offertoryEnd'); od('rPf'); q.push({t: 'pref'}); ord('sa');
    od('canon'); od('pater');
    if (!m.noAgnus) ord('ag');
    od('communion');
    ch('co'); ch('an'); hw('afterCo'); od('post'); orat('pc'); orat('sp'); od('postEnd');
    if (O === 'low') od('dismiss'); else q.push({t: 'ord', k: 'it'});
    if (!(HW && HW.noLastGospel)) od('end'); else od('endNoGospel');
    hw('end');
    return q;
  }
  function rubricLine(R) {
    var pn = prefaceOf(state.key, state.date), P = pn ? PREFACES[pn] : null, num = state.ord && state.ord !== 'none' ? state.ord : autoKyriale(state.key, state.date);
    if (state.key === 'Quad6f') return 'Lessons and Tracts · the Passion · the Solemn Prayers · the Adoration of the Cross · the Mass of the Presanctified';
    if (R.requiem) return 'Mass for the Dead · Kyrie (Requiem) · without Gloria or Credo · Sequence Dies iræ · Preface for the Dead · Agnus Dei with dona eis requiem · Requiescant in pace';
    var kyr = num === 'VIII' ? 'VIII (Profestis diebus)' : num;
    if (!state.ord && paschalKyrie(state.key, state.date)) kyr += ', Kyrie IV';
    return (state.ord === 'none' ? '' : 'Kyriale: Missa ' + kyr + ' · ') + (R.gloria ? 'Gloria' : 'no Gloria') + ' · ' + (R.credo ? 'Credo' : 'no Credo') +
      (P ? ' · ' + P.en : '') + ' · ' + (R.dismiss === 'ite' ? 'Ite, missa est' : 'Benedicamus Domino');
  }

  // the bar under the title: form of Mass, language, print & share
  function markBar() {
    var f = $('#segForm'), l = $('#segLang');
    if (f) Array.prototype.forEach.call(f.children, function (b) { var on = (b.getAttribute('data-v') || '') === (state.ordo || ''); b.classList.toggle('on', on); b.setAttribute('aria-checked', on); });
    var ro = $('#rubopts');
    if (ro) {
      ro.hidden = !state.ordo;
      if ($('#selComm')) $('#selComm').value = commOf();
      if ($('#selPrel')) $('#selPrel').value = state.prel || '';
      if ($('#selSac')) $('#selSac').value = state.sac || '';
      if ($('#selServ')) $('#selServ').value = servOf();
      var fr = fullRub();
      if ($('#roAi')) $('#roAi').hidden = !fr;
      ['selPrel', 'selSac', 'selServ'].forEach(function (id) { var x = $('#' + id); if (x) x.parentNode.hidden = !fr || (id === 'selServ' && state.ordo === 'low'); });
      var sr = $('#segRub');
      if (sr) Array.prototype.forEach.call(sr.children, function (b) { var on = (b.getAttribute('data-v') || '') === (state.rub || ''); b.classList.toggle('on', on); b.setAttribute('aria-checked', on); });
    }
    if (l && window.OPLang) { var lv = OPLang.get(); Array.prototype.forEach.call(l.children, function (b) { var on = b.getAttribute('data-v') === lv; b.classList.toggle('on', on); b.setAttribute('aria-checked', on); }); }
  }
  // a strip of links to the parts of the Mass, kept in view while scrolling; the part on screen is marked
  var JUMP = {hw: 1, in: 1, ky: 1, gl: 1, oratio: 1, reading: 1, gr: 1, al: 1, tr: 1, se: 1, cr: 1, of: 1, pf: 1, sa: 1, ag: 1, co: 1, it: 1, as: 1};
  var jumpObs = null;
  function buildJump(main) {
    var nav = $('#jump'); if (!nav) return;
    nav.innerHTML = ''; if (jumpObs) jumpObs.disconnect();
    var secs = [];
    Array.prototype.forEach.call(main.children, function (sec, n) {
      var p = sec.getAttribute && sec.getAttribute('data-part');
      if (!p || !JUMP[p]) return;
      var h = sec.querySelector('.part-head h2, h3');
      var t = h ? (h.firstChild && h.firstChild.nodeType === 3 ? h.firstChild.nodeValue : h.textContent) : '';
      t = (t || '').trim();
      if (!t && p === 'oratio') t = {or: 'Oratio', se: 'Secreta', pc: 'Postcommunio', sp: 'Super populum'}[sec.getAttribute('data-k')] || '';
      if (!t) return;
      if (p === 'pf') t = 'Praefatio';
      sec.id = sec.id || 'p-' + n;
      secs.push(sec);
      nav.appendChild(el('a', {href: '#' + sec.id, 'data-for': sec.id, text: t, onclick: function (e) {
        e.preventDefault();
        var top = sec.getBoundingClientRect().top + window.scrollY - (nav.getBoundingClientRect().height + (($('.top') || {}).offsetHeight || 0)) - 6;
        window.scrollTo({top: top, behavior: 'smooth'});
      }}));
    });
    nav.hidden = secs.length < 3;
    var th = ($('.top') || {}).offsetHeight || 0;
    document.documentElement.style.setProperty('--toph', th + 'px');
    if (!('IntersectionObserver' in window)) return;
    jumpObs = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) {
        if (!e.isIntersecting) return;
        var a = nav.querySelector('a[data-for="' + e.target.id + '"]');
        if (!a) return;
        Array.prototype.forEach.call(nav.querySelectorAll('a.on'), function (x) { x.classList.remove('on'); });
        a.classList.add('on');
        var r = a.getBoundingClientRect(), nr = nav.getBoundingClientRect();
        if (r.left < nr.left || r.right > nr.right) nav.scrollTo({left: a.offsetLeft - 16, behavior: 'smooth'});
      });
    }, {rootMargin: '-' + (th + 60) + 'px 0px -65% 0px'});
    secs.forEach(function (s2) { jumpObs.observe(s2); });
  }

  function drawMass() {
    if (BOOKP) return;
    var m = D.masses[state.key], main = $('#mass'), mhead = $('#mhead') || main;
    main.innerHTML = ''; if (mhead !== main) mhead.innerHTML = '';
    markBar();
    if (!HWP && /^Quad6[mtwhfs]?$/.test(state.key)) {
      main.appendChild(el('header', {class: 'mass-head'}, [el('h1', {text: clean(m.title).replace(/^\d+ [A-Za-z.]+ — /, '')}), el('p', {class: 'en', text: m.name_en || clean(m.en || '')})]));
      main.appendChild(el('div', {class: 'hw-card'}, [
        el('p', {text: 'Holy Week has its own section, with the whole rite of each day as the Missal gives it, in the traditional (1939) and the reformed (1959) form.'}),
        el('a', {class: 'sbtn hw-go', href: 'holyweek.html#' + state.key, text: 'Open in Holy Week ›'})]));
      return;
    }
    var latin = clean(m.title).replace(/^\d+ [A-Za-z.]+ — /, '');
    var english = m.name_en || (isTemporal(state.key) ? clean(m.en || '') : '');
    mhead.appendChild(el('header', {class: 'mass-head'}, [
      el('h1', {text: latin}),
      english && english !== latin ? el('p', {class: 'en', text: english}) : null
    ]));
    var ord = ordinaryIds();
    var d0 = state.date || new Date();
    main.insertBefore(el('div', {class: 'choir-head print-only'}, [
      el('div', {class: 'c-cross', text: '✠'}),
      el('div', {class: 'ch-title', text: clean(m.title).replace(/^\d+ [A-Za-z.]+ — /, '')}),
      el('div', {class: 'ch-sub', text: WEEKDAYS[d0.getDay()] + ', ' + d0.getDate() + ' ' + MONTHS[d0.getMonth()] + ' ' + d0.getFullYear() + ' · Graduale juxta ritum Ordinis Praedicatorum'})
    ]), main.firstChild);
    var R = rubricsOf(state.key, state.date);
    mhead.appendChild(el('p', {class: 'rubric-line', text: rubricLine(R)}));
    if (!(HWP && window.HW_TEXT && HW_TEXT[state.hwr] && HW_TEXT[state.hwr][state.key])) main.appendChild(el('h2', {class: 'caps-head', id: 'chants', text: state.ordo ? 'Ordo et Proprium Missae' : 'Proprium Missae'}));
    if (ord.as) { if (state.ordo && window.ORDO && ORDO.rAs) { var asr = drawSection({la: '', en: '', lines: secLines(ORDO.rAs), k: 'rAs', strip: 1}, R); if (asr) main.appendChild(asr); } main.appendChild(drawOrdinary('as', ord.as)); }
    var readHead = false;
    massSequence(m, state.parts).forEach(function (it) {
      if (it.t === 'chant') main.appendChild(drawSlot(it.p, it.i, it.c));
      else if (it.t === 'pref') { var pf = drawPreface(state.key, state.date, R); if (pf) main.appendChild(pf); }
      else if (it.t === 'ord') { if (ord[it.k]) main.appendChild(drawOrdinary(it.k, ord[it.k])); }
      else if (it.t === 'oratio') main.appendChild(drawOratio(it));
      else if (it.t === 'hw') { var hws = drawSection(it.s, R); if (hws) main.appendChild(hws); }
      else if (it.t === 'hwtext') main.appendChild(drawHwText(it.s, it.n));
      else if (it.t === 'hwnote') main.appendChild(el('p', {class: 'hint rubric', text: 'This day of Holy Week is still being transcribed from the Missale O.P. (1939); its chants follow.'}));
      else if (it.t === 'ordo') { var os = drawOrdo(it.k, R); if (os) main.appendChild(os); }
      else {
        if (!readHead) { readHead = true; }
        main.appendChild(drawReading(it.r));
      }
    });
    if (false) {
      main.appendChild(el('p', {class: 'hint hide-print', id: 'ordinary'}, ['To add the Kyrie, Gloria, Credo, Sanctus and Agnus Dei, choose a Mass of the Kyriale under Options.']));
    }
    var src = {dm: 'Chants as assigned by the St. Dominic Missal (1959)', missal: 'Chants as given in the Missale O.P. (1939)',
      proper: 'Proper Mass of the Graduale O.P.', common: 'Common named by the Missale O.P. (1939)', guess: 'Common chosen from the saint\'s title: check the Ordo',
      shared: 'Chants re-used from elsewhere in the Graduale', g50: 'Mass as the Graduale O.P. gives it on the day', manual: 'Dominican Mass, checked against the Missale O.P.'}[m.conf];
    buildJump(main);
    main.appendChild(el('p', {class: 'source hide-print'}, [
      'Graduale O.P. (1950)' + (m.page ? ', p. ' + m.page : '') + (src ? ' · ' + src : '') + '. Readings and prayers: Missale O.P. (1933/1939)' + (isSung() ? '; reading tones: Harrison O.P. (1920)' : '') + '. ',
      el('a', {href: 'about.html', text: 'About the sources'})
    ]));
    if (!state.edit) return;
    var add = el('section', {class: 'add hide-print'});
    var partSel = el('select', {'aria-label': 'Part to add'});
    PARTS.forEach(function (p) { partSel.appendChild(el('option', {value: p, text: PART_EN[p]})); });
    add.appendChild(el('div', {class: 'row'}, [
      el('span', {text: 'Add a chant: '}), partSel,
      el('button', {type: 'button', class: 'btn small', text: 'Add', onclick: function () {
        state.parts[partSel.value].push({id: null, chosen: true}); drawMass(); writeHash();
      }})
    ]));
    if (m.extras && m.extras.length) {
      var list = el('ul', {class: 'extras'});
      m.extras.forEach(function (id) {
        var c = D.chants[id];
        if (!c) return;
        var p = PARTS.indexOf(c.p) >= 0 ? c.p : null;
        list.appendChild(el('li', null, [
          el('span', {text: (p ? PART_EN[p] : c.p.toUpperCase()) + ': ' + clean(c.i) + ' (p. ' + c.pg + ') '}),
          p ? el('button', {type: 'button', class: 'linkbtn', text: 'add', onclick: function () {
            state.parts[p].push({id: id, chosen: true}); drawMass(); writeHash();
          }}) : null
        ]));
      });
      add.appendChild(el('details', null, [el('summary', {text: 'Other chants printed on these pages of the Graduale (' + m.extras.length + ')'}), list]));
    }
    main.appendChild(add);
  }

  // a section of the Order of Mass: rubrics in red, the priest's and ministers' parts with their translation
  function drawOrdo(k, R) {
    var O = window.ORDO, sec, lines;
    if (k === 'dismiss') { sec = {la: R.requiem ? 'Requiescant in pace' : R.dismiss === 'ite' ? 'Ite, missa est' : 'Benedicamus Domino', en: 'Dismissal'}; lines = O.dismiss[R.requiem ? 'req' : R.dismiss === 'ite' ? 'ite' : 'ben']; }
    else if (k === 'endNoGospel') { sec = O.end; var el0 = secLines(O.end); lines = el0.slice(0, el0.findIndex(function (l) { return /^At the Gospel side/.test(l.r || ''); })); }
    else { sec = O[k]; if (!sec) return null; lines = secLines(sec); }
    // the Communion of the faithful: none, the simple rite, or (at a Conventual Mass) the Communion of the friars
    if (k === 'communion' && window.ORDO) {
      var c0 = lines.findIndex(function (l) { return /^Communion of the faithful/.test(l.r || ''); });
      var c1 = lines.findIndex(function (l) { return /custódiat te in vitam/.test(l.la || ''); });
      var cm = commOf(), rep = cm === 'none' ? [] : cm === 'friars' ? ORDO.commConv.lines : ORDO.commSimple.lines;
      if (c0 >= 0 && c1 > c0) lines = lines.slice(0, c0).concat(rep, lines.slice(c1 + 1));
    }
    if (R.requiem && k === 'communion') lines = lines.filter(function (l) { return !/^Pax tibi/.test(l.la || '') && !/^He kisses the lip of the chalice/.test(l.r || ''); });
    var HWk = window.HOLYWEEK && HOLYWEEK[state.key];
    if (k === 'dismiss' && HWk && HWk.alleluiaDismiss) lines = lines.map(function (l) { return {w: l.w, la: l.la.replace(/\.$/, ', allelúia, allelúia.'), en: l.en.replace(/\.$/, ', alleluia, alleluia.')}; });
    // at a private Mass of Palm Sunday the Gospel of the blessing is the last Gospel
    var HW = window.HOLYWEEK && HOLYWEEK[state.key];
    if (k === 'canon' && HW && HW.canon) {
      lines = lines.map(function (l) {
        var hit = l.la && Object.keys(HW.canon).filter(function (w) { return l.la.indexOf(w) === 0; })[0];
        return hit ? {w: 'P', la: HW.canon[hit][0], en: HW.canon[hit][1]} : l;
      });
    }
    if (k === 'end' && HW && HW.lastGospel && state.ordo === 'low') {
      lines = lines.map(function (l) {
        if (/^Inítium sancti Evangélii/.test(l.la || '')) return {w: 'P', la: 'Sequéntia sancti Evangélii secúndum Matthǽum.', en: 'The continuation of the holy Gospel according to Matthew.'};
        if (/^In princípio erat Verbum/.test(l.la || '')) return {read: HW.lastGospel};
        return l;
      });
    }
    if (isSung() && k === 'canon') {
      var n = lines.length;
      if (n > 1 && /^Per ómnia sǽcula sæculórum/.test(lines[n - 2].la || '') && /^Amen/.test(lines[n - 1].la || '')) lines = lines.slice(0, n - 2);
    }
    if (isSung() && k === 'pater') {
      // Missale O.P. 1939, Appendix: the ferial chant in feasts of three lessons, on ferias and in Masses for the Dead
      var sol = solemnDay(state.key, state.date) && !R.requiem, after = false, L2 = [];
      L2.push({r: 'The priest sings (' + (sol ? 'solemn' : 'ferial') + ' tone):'});
      L2.push({g: sol ? 'op-m39-pater-solemn' : 'op-m39-pater-ferial', nd: 1, en: 'World without end. ℟. Amen. Let us pray. Admonished by saving precepts, and following the divine instruction, we make bold to say: Our Father … And lead us not into temptation. ℟. But deliver us from evil.'});
      lines.forEach(function (l) {
        if (/^Líbera nos/.test(l.la || '')) after = true;
        if (!after) { if (l.r && /^His hands are laid on the corporal/.test(l.r)) L2.unshift(l); else if (l.r) L2.push(l); else if (/^Amen\.$/.test(l.la || '') && l.w === 'P') L2.push(l); return; }
        if (/^Pax\s*✠?\s*Dómini/.test(l.la || '')) { L2.push({g: 'op-m39-pax', nd: 1, en: 'World without end. ℟. Amen. The peace ✠ of the Lord be ✠ always with ✠ you. ℟. And with thy spirit.'}); return; }
        if (/^Per ómnia sǽcula sæculórum\.?$/.test(l.la || '') || /^Amen\.$/.test(l.la || '') || /^Et cum spíritu tuo/.test(l.la || '')) return;
        L2.push(l);
      });
      lines = L2;
    }
    return drawSection({la: sec.la, en: sec.en, lines: lines, k: k, strip: sec.strip}, R);
  }
  function drawSection(sec, R) {
    var mode = modeOf(), lines = sec.lines, k = sec.k;
    lines = lines.filter(function (l) { return showLine(l, R); });
    if (!lines.length) return null;
    var b0 = gospelBook();
    if (k === 'gospel' && b0 && EV_LA[b0]) lines = lines.map(function (l) { return /secúndum N\./.test(l.la || '') ? {w: l.w, la: l.la.replace('N.', EV_LA[b0] + '.'), en: l.en.replace(/according to N\./, 'according to ' + EV_EN[b0] + '.')} : l; });
    if (mode !== 'l' && /^(collect|offerDial|post|postEnd|gospel)$/.test(k || '')) lines = singLines(lines);
    if (R.requiem) lines = lines.filter(function (l) { return !/^(Benedíctio Dei omnipoténtis|Amen\.$)/.test(l.la || '') || k !== 'end'; });
    var box = el('section', {class: 'part ordo' + (sec.strip ? ' rubstrip' : ''), 'data-part': 'ordo'});
    if (!sec.strip) box.appendChild(el('div', {class: 'part-head'}, [el('h2', {text: sec.la}), el('span', {class: 'incipit', text: sec.en})]));
    lines.forEach(function (l, i) {
      if (l.r) { box.appendChild(rubLine(l)); return; }
      if (l.read) { box.appendChild(drawReading({type: l.type || 'Gospel', ref: l.read})); return; }
      if (l.g || l.gabc) {
        if (l.n) box.appendChild(el('p', {class: 'hw-chant-n', text: l.n}));
        box.appendChild(l.gabc ? gabcBox(l.gabc) : chantBox(l.g, l.nd ? {noDrop: true} : undefined));
        if (l.en) box.appendChild(el('p', {class: 'en-text tone-en', lang: 'en', text: l.en}));
        return;
      }   // a chant of the 1959 Holy Week (gabc/op59-*)
      var near = function (j) { return lines[j] && lines[j].w === 'S'; };
      var mark = l.w === 'C' || /^(℟|℣|Ant\.)/.test(l.la) ? '' : l.w === 'S' ? '℟. ' : (l.w === 'D' || near(i + 1) || near(i - 1)) && l.la.length < 140 ? '℣. ' : '';
      box.appendChild(el('div', {class: 'r-cols o-line'}, [
        el('p', {class: 'la', lang: 'la'}, [mark ? el('span', {class: 'o-mark', text: mark}) : null, l.la]),
        el('p', {class: 'en-text', lang: 'en'}, [mark ? el('span', {class: 'o-mark', text: mark}) : null, l.en])]));
    });
    return box;
  }
  // the Collect, Secret or Postcommunion of the day
  function flectamusDay(key, d) {
    return isTemporal(key) && /^(5a[whfs]|Quad[1-6][mtwhfs])$/.test(key) && !/^Quad6[hfs]$/.test(key) && !(d && d.getDay() === 0);
  }
  function chantBox(id, o) {
    var cb = el('div', {class: 'chant'});
    loadGabc(id).then(function (t) { var g = splitGabc(t); renderInto(cb, g.body, g.header, null, o); }, function (e) { showError(cb, e); });
    return cb;
  }
  // a chant made here (the tones of the prayers and readings), drawn without a large initial
  function gabcBox(gabc) {
    var cb = el('div', {class: 'chant tone'});
    renderInto(cb, gabc, {}, null, {noDrop: true});
    return cb;
  }
  var EV_LA = {Matthæus: 'Matthǽum', Marcus: 'Marcum', Lucas: 'Lucam', Joannes: 'Ioánnem', Ioannes: 'Ioánnem'};
  var EV_EN = {Matthæus: 'Matthew', Marcus: 'Mark', Lucas: 'Luke', Joannes: 'John', Ioannes: 'John'};
  function gospelBook() { var g = state._gos; return g && g.ref ? g.ref.split(' ')[0] : null; }
  function isSung() { return state.ordo === 'sung' || state.ordo === 'solemn' || state.ordo === 'conv'; }
  // the form of Mass as a letter of data/ordo.js (l Low, s Sung, m Solemn, c Conventual), and the circumstances chosen on the page
  function modeOf() { return {low: 'l', sung: 's', solemn: 'm', conv: 'c'}[state.ordo] || 'l'; }
  function commOf() { return state.comm || (state.ordo === 'conv' ? 'friars' : 'simple'); }
  function servOf() { return state.serv || (state.ordo === 'solemn' || state.ordo === 'conv' ? 'full' : 'one'); }
  function holds(cond, R) {
    if (!cond) return true;
    var inc = function (p, re) { return ((state.parts || {})[p] || []).some(function (c) { var x = D.chants[c.id]; return x && re.test(x.i || ''); }); };
    var or = window.ORATIONS && ORATIONS[state.key];
    var dr = dayRank(state.key, state.date), gl = !!(R && R.gloria), sd = dr.sun || dr.dup;
    var sept = !!(state.date && inSeptLent(state.date)), chgl = gl && sd, chky = !gl && sept;
    var fr = fullRub(), sac = fr ? state.sac : '', prel = fr ? state.prel : '';   // the circumstances are chosen only with the full rubrics
    var on = {tab: sac === 'tab', exp: sac === 'exp', sac: !!sac, pope: prel === 'pope', bp: prel === 'bp',
              prel: prel === 'pope' || prel === 'bp', mo: prel === 'mo', one: servOf() === 'one', full: servOf() === 'full', req: !!(R && R.requiem),
              flect: flectamusDay(state.key, state.date), sp: !!(or && or.sp), adjuva: inc('tr', /^Domine non secundum/), veni: inc('al', /^Veni Sancte Spiritus/), nogl: !gl,
              sun: dr.sun, dup: dr.dup, td: dr.td, sd: sd, thur: dr.thur, sol: dr.sol, sept: sept, chgl: chgl, chky: chky, chin: !chgl && !chky};
    return cond.split(',').every(function (c) { var neg = c.charAt(0) === '!', v = !!on[neg ? c.slice(1) : c]; return neg ? !v : v; });
  }
  // the full directions of the Missal (Ritus servandus), or the basic Order of Mass with its few directions
  function fullRub() { return state.rub === 'full'; }
  function rubPref() { try { return localStorage.getItem('rubrics') === 'full' ? 'full' : ''; } catch (e) { return ''; } }
  function secLines(sec) { return fullRub() && sec.adv ? sec.adv : sec.lines; }
  // the rank of the day, for the directions that depend on it (Missale O.P. 1939, Kalendarium, data/kalendar39.js); an approximation
  // until the full classification of days is built
  var KALRANK = null;
  function dayRank(key, d) {
    if (!KALRANK) { KALRANK = {}; var K = window.KAL39 || {}; Object.keys(K).forEach(function (md) { K[md].forEach(function (e) { if (e[2] && !KALRANK[e[2]]) KALRANK[e[2]] = e[1]; }); }); }
    var rank = KALRANK[key] || '', m = D.masses[key] || {}, t = titleText(key);
    if (isTemporal(key) && temporalClass(key, d) === 1 && /^(Dec25(_\d)?|Jan1|Epi|Pasc0|Asc|Pent0|CorpusChristi|SCJ|ChristusRex)$/.test(key)) rank = 'Totum Duplex';
    var sun = isSundayMass(key, d) || !!(d && d.getDay() === 0);
    var td = /Totum Duplex/.test(rank), dup = td || /^Duplex/.test(rank);
    var vot = D.sections.some(function (x) { return x.id === 'votivae' && x.items.indexOf(key) >= 0; }) && /Dominic|Thom|Sacrament|Corporis|Mari/.test(t);
    var thur = sun || dup || /Simplex|Semiduplex|Novem|Octava sol/.test(rank) || vot || (isTemporal(key) && temporalClass(key, d) <= 2);
    var sol = /^(Dec25(_\d)?|Pasc0|Asc|Pent0|CorpusChristi|S0815|S0804|S1101)$/.test(key);
    return {rank: rank, sun: sun, dup: dup, td: td, thur: thur, sol: sol};
  }
  function showLine(l, R) { return (!l.m || l.m.indexOf(modeOf()) >= 0) && holds(l['if'], R); }
  // a direction of the rubrics: the short form always shown; when it rests on paragraphs of the Missal, tapping it opens them (English)
  var COND_LABEL = {tab: 'Tabernacle', exp: 'Exposition', sac: 'Blessed Sacrament', pope: 'The Pope present', bp: 'Prelate present', prel: 'Prelate present', mo: 'Master of the Order', one: 'One acolyte', req: 'Requiem'};
  function rubLine(l) {
    var tag = (l['if'] || '').split(',').filter(function (c) { return COND_LABEL[c]; }).map(function (c) { return COND_LABEL[c]; })[0];
    var lead = tag ? el('span', {class: 'o-cond', text: tag}) : null;
    if (!l.ref || !fullRub()) return el('p', {class: 'o-rub' + (tag ? ' cond' : '')}, [lead, l.r]);
    var full = el('div', {class: 'rx-full'});
    var d = el('details', {class: 'o-rub rx' + (tag ? ' cond' : '')}, [el('summary', {}, [lead, l.r]), full]);
    d.addEventListener('toggle', function () {
      if (!d.open || full.firstChild) return;
      full.appendChild(el('p', {class: 'rx-wait', text: 'Opening the rubrics…'}));
      loadRubText().then(function (T) {
        full.innerHTML = '';
        l.ref.forEach(function (id) {
          var x = T[id]; if (!x) return;
          var tx = el('span'); tx.innerHTML = x[1]; full.appendChild(el('p', {class: 'rx-p'}, [el('span', {class: 'rx-h', text: x[0]}), ' ', tx]));
        });
        full.appendChild(el('p', {class: 'rx-ai', text: 'AI translation from the Latin of the Missal; not yet checked by a human translator.'}));
        full.appendChild(el('a', {class: 'rx-go', href: 'rubrics.html#' + l.ref[0], text: 'In the Rubrics of the Missal ›'}));
      }, function () { full.innerHTML = ''; full.appendChild(el('a', {class: 'rx-go', href: 'rubrics.html#' + l.ref[0], text: 'Open in the Rubrics of the Missal ›'})); });
    });
    return d;
  }
  var rubTextP = null;
  function loadRubText() {
    if (window.RUBTEXT) return Promise.resolve(window.RUBTEXT);
    if (!rubTextP) rubTextP = new Promise(function (ok, no) {
      var sc = document.createElement('script'); sc.src = 'data/rubtext.js';
      sc.onload = function () { window.RUBTEXT ? ok(window.RUBTEXT) : no(); }; sc.onerror = function () { rubTextP = null; no(); };
      document.head.appendChild(sc);
    });
    return rubTextP;
  }
  // at a Sung or Solemn Mass the greetings, Orémus and the announcement of the Gospel are sung:
  // Graduale O.P. (1950), Modus respondendi in Missa, pp. 146*-147* (Ad Orationes I; Ad Evangelium);
  // Orémus after Harrison (1920) p. 67; the Dóminus vobíscum of the Gospel "like those for the Prayers" (p. 77)
  function singLines(lines) {
    var o = [], nx = function (i, re) { return lines[i + 1] && re.test(lines[i + 1].la || ''); };
    for (var i = 0; i < lines.length; i++) {
      var l = lines[i], la = l.la || '';
      if (/^Dóminus vobíscum\.$/.test(la) && nx(i, /^Et cum spíritu tuo\.$/)) { o.push({g: '7339', nd: 1, en: 'The Lord be with you. ℟. And with thy spirit.'}); i++; continue; }
      if (/^Orémus\.$/.test(la)) { o.push({g: 'op-h-oremus', nd: 1, en: 'Let us pray.'}); continue; }
      if (/^Sequéntia sancti Evangélii/.test(la) && nx(i, /^Glória tibi/) && window.OPMassTones) {
        var b = gospelBook(), g = b && OPMassTones.sequentia(b);
        if (g) { o.push({gabc: g, en: 'The continuation of the holy Gospel according to ' + EV_EN[b] + '. ℟. Glory be to thee, O Lord.'}); i++; continue; }
      }
      o.push(l);
    }
    return o;
  }
  function drawOratio(it) {
    var name = {or: ['Oratio', 'Collect'], se: ['Secreta', 'Secret'], pc: ['Postcommunio', 'Postcommunion'], sp: ['Oratio super populum', 'Prayer over the People']}[it.k];
    var box = el('section', {class: 'part ordo oratio', 'data-part': 'oratio', 'data-k': it.k});
    // with the Order of Mass shown, the Collect and Postcommunion go under its heading (Oratio, Postcommunio)
    if (!(state.ordo && window.ORDO && (it.k === 'or' || it.k === 'pc'))) box.appendChild(el('div', {class: 'part-head'}, [el('h2', {text: name[0]}), el('span', {class: 'incipit', text: it.k === 'sp' && it.x[2] ? name[1] + ' · ' + it.x[2] : name[1]})]));
    else box.classList.add('cont');
    // Missale O.P. 1939 (Feria IV Cinerum): "Flectamus genua, et Levate, quotidie in Quadragesima in Missa de tempore:
    // exceptis Dominicis, et die Cenae, et Sabbato Paschae"; the deacon sings them after Oremus, before the Collect
    if (it.k === 'or' && flectamusDay(state.key, state.date)) {
      box.appendChild(el('div', {class: 'r-cols o-line'}, [el('p', {class: 'la', lang: 'la', text: 'Orémus. ℣. Flectámus génua. ℟. Leváte.'}), el('p', {class: 'en-text', lang: 'en', text: 'Let us pray. ℣. Let us kneel. ℟. Arise.'})]));
      if (isSung()) box.appendChild(chantBox('op-m39-flectamus', {noDrop: true}));
    }
    // Lenten ferias: after the Postcommunion the priest says Oremus and the deacon Humiliate capita vestra Deo
    if (it.k === 'sp' && isSung()) box.appendChild(chantBox('op-m39-humiliate', {noDrop: true}));
    if (it.k === 'sp') box.appendChild(el('div', {class: 'r-cols o-line'}, [el('p', {class: 'la', lang: 'la', text: 'Orémus. ℣. Humiliáte cápita vestra Deo.'}), el('p', {class: 'en-text', lang: 'en', text: 'Let us pray. ℣. Bow down your heads before God.'})]));
    // at a Sung or Solemn Mass the Collect, Postcommunion and Prayer over the People are sung in the tone of the
    // prayers (Harrison 1920, pp. 66-67; Orémus is sung just before); the Secret is said in a low voice
    var og = null;
    if (isSung() && it.k !== 'se' && window.OPMassTones) { try { og = OPMassTones.oration(it.x[0], {noOremus: true}); } catch (e) { console.warn('tone', e); } }
    if (og) {
      box.appendChild(gabcBox(og));
      var amen = og.indexOf('A(g)men') >= 0;
      box.appendChild(el('p', {class: 'en-text tone-en', lang: 'en', text: it.x[1] + (amen ? ' ℟. Amen.' : '')}));
      if (!amen) box.appendChild(el('div', {class: 'r-cols o-line'}, [el('p', {class: 'la', lang: 'la'}, [el('span', {class: 'o-mark', text: '℟. '}), 'Amen.'])]));
      return box;
    }
    if (it.k === 'se' && isSung()) {
      // said in a low voice as far as "Deus"; "Per omnia saecula saeculorum" is sung aloud at the beginning of the Preface
      var sl = it.x[0].replace(/,?\s*per ómnia sǽcula sæculórum\.?\s*$/i, ','), se = it.x[1].replace(/,?\s*world without end\.?\s*$/i, ',');
      box.appendChild(el('div', {class: 'r-cols o-line'}, [el('p', {class: 'la', lang: 'la', text: sl}), el('p', {class: 'en-text', lang: 'en', text: se}), ]));
      return box;
    }
    box.appendChild(el('div', {class: 'r-cols o-line'}, [el('p', {class: 'la', lang: 'la', text: it.x[0]}), el('p', {class: 'en-text', lang: 'en', text: it.x[1]})]));
    box.appendChild(el('div', {class: 'r-cols o-line'}, [el('p', {class: 'la', lang: 'la'}, [el('span', {class: 'o-mark', text: '℟. '}), 'Amen.'])]));
    return box;
  }
  // Holy Week transcribed as printed. Markup: {red}, *black inside a rubric*, ^initial
  function hwInline(s, rubric) {
    var out = [], re = rubric ? /\{([^}]*)\}|\*([^*]*)\*|\^(\S)/g : /\{([^}]*)\}|\^(\S)/g, last = 0, m;
    while ((m = re.exec(s))) {
      if (m.index > last) out.push(s.slice(last, m.index));
      if (m[1] != null) out.push(el('span', {class: 'r', text: m[1]}));
      else if (rubric && m[2] != null) out.push(el('span', {class: 'k', text: m[2]}));
      else out.push(el('span', {class: 'r ini', text: rubric ? m[3] : m[2]}));
      last = re.lastIndex;
    }
    if (last < s.length) out.push(s.slice(last));
    return out;
  }
  // Holy Week chant: drawn in place, as on the Mass pages, when it comes near the screen.
  // Everything needed is kept on data- attributes, so a copied node still draws.
  var hwIO = null;
  function hwGo(wrap) {
    if (wrap.getAttribute('data-done')) return; wrap.setAttribute('data-done', '1');
    var box = wrap.querySelector('.chant'), id = wrap.getAttribute('data-id');
    box.innerHTML = ''; box.appendChild(el('p', {class: 'loading', text: 'Loading…'}));
    loadGabc(id).then(function (text) { box.innerHTML = ''; var g = splitGabc(text); renderInto(box, g.body, g.header, wrap.getAttribute('data-p') || undefined); })
      .catch(function (e) { showError(box, e); });
  }
  function hwWatch(root) {
    var ws = (root || document).querySelectorAll('.hw-chant:not([data-done])');
    if (!('IntersectionObserver' in window)) { Array.prototype.forEach.call(ws, hwGo); return; }
    if (!hwIO) hwIO = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { hwIO.unobserve(e.target); hwGo(e.target); } }); }, {rootMargin: '600px 0px'});
    Array.prototype.forEach.call(ws, function (w) { hwIO.observe(w); });
  }
  function hwChant(b) {
    var c = b.t === 'G' ? {id: b.id} : (state.parts[b.p] || [])[b.i];
    if (!c || !c.id) return null;
    var wrap = el('div', {class: 'hw-chant', 'data-id': c.id, 'data-p': b.p || ''}, [b.n ? el('p', {class: 'hw-chant-n', text: b.n}) : null, el('div', {class: 'chant'})]);
    setTimeout(function () { hwWatch(); }, 0);
    return wrap;
  }
  function hwBlocks(blocks, into) {
    blocks.forEach(function (b) {
      if (b.t === 'C' || b.t === 'G') { var ch = hwChant(b); if (ch) into.appendChild(ch); return; }
      if (b.t === 'F') {
        var inner = el('div', {class: 'hw-fold-body'});
        hwBlocks(b.blocks, inner);
        into.appendChild(el('details', {class: 'hw-fold'}, [el('summary', null, [el('span', {class: 'la', text: b.la}), el('span', {class: 'en-text', text: b.en})]), inner]));
        return;
      }
      var R = b.t === 'R', cls = {H: 'hw-h', I: 'hw-i', L: 'hw-l', R: 'hw-r', T: 'hw-t'}[b.t];
      if (b.t === 'L') {
        var lab = function (s) { var p = s.split(' | '); return [p[0], p[1] ? el('span', {class: 'hw-ref', text: ' ' + p[1]}) : null]; };
        into.appendChild(el('div', {class: 'r-cols o-line hw-l'}, [el('p', {class: 'la', lang: 'la'}, lab(b.la)), el('p', {class: 'en-text', lang: 'en'}, lab(b.en || ''))]));
        return;
      }
      into.appendChild(el('div', {class: 'r-cols o-line ' + cls}, [
        el('p', {class: 'la', lang: 'la'}, hwInline(b.la, R)),
        el('p', {class: 'en-text', lang: 'en'}, hwInline(b.en || '', R))]));
    });
  }
  function drawHwText(sec, n) {
    var box = el('section', {class: 'part ordo hw' + (sec.cont ? ' hw-cont' : ''), 'data-part': 'hw'});
    if (!sec.cont) box.appendChild(el('div', {class: 'part-head'}, [el('h2', {text: sec.la}), el('span', {class: 'incipit', text: sec.en})]));
    if (!sec.cont && sec.src) box.appendChild(el('p', {class: 'meta hw-src', text: sec.src}));
    hwBlocks(sec.blocks, box);
    return box;
  }
  function findKyriale(name) { var r = null; D.kyriale.forEach(function (id) { if (D.chants[id].i === name) r = id; }); return r; }
  function drawOrdinary(k, id) {
    var slot = el('section', {class: 'part', 'data-part': k, id: k === 'ky' || k === 'as' ? 'ordinary' : null});
    var box = el('div', {class: 'chant'}), nm = D.chants[id] ? D.chants[id].i : '';
    var label = k === 'it' && (/^Benedicamus/.test(nm) || rubricsOf(state.key, state.date).dismiss === 'ben') ? 'Benedicamus Domino' : k === 'it' && /^Requiescant/.test(nm) ? 'Requiescant in pace' : ORD_LABEL[k];
    slot.appendChild(el('div', {class: 'part-head hide-print'}, [el('h2', {text: label}), el('span', {class: 'incipit', text: D.chants[id] ? clean(D.chants[id].i) : ''})]));
    slot.appendChild(el('h2', {class: 'print-only', text: label + (D.chants[id] ? ' · ' + clean(D.chants[id].i).replace(/^(Kyrie|Gloria|Credo|Sanctus|Agnus|Ite|Benedicamus)\s*/, '') : '')}));
    slot.appendChild(box);
    if (k === 'ag' && rubricsOf(state.key, state.date).requiem)
      slot.appendChild(el('p', {class: 'hint rubric', text: 'At a Mass for the Dead: “dona eis requiem” twice, and the third time “dona eis requiem sempiternam”.'}));
    if (k === 'ky' && id === findKyriale('Kyrie IV') && state.ord !== 'IV')
      slot.appendChild(el('p', {class: 'hint rubric', text: 'In Paschaltide the Easter Kyrie is sung on Sundays and on feasts of the I and II class.'}));
    box.appendChild(el('p', {class: 'loading', text: 'Loading…'}));
    loadGabc(id).then(function (t) { var g = splitGabc(t); renderInto(box, k === 'it' ? dismissGabc(g.body, rubricsOf(state.key, state.date).dismiss === 'ben') : g.body, g.header, null); }, function (e) { showError(box, e); });
    return slot;
  }

  // ---------------------------------------------------------------- readings
  var bibleCache = {};
  function bibleBook(lang, book) {
    var key = lang + '/' + book;
    if (!bibleCache[key]) bibleCache[key] = fetch('bible/' + lang + '/' + encodeURIComponent(book) + '.txt').then(function (r) {
      if (!r.ok) throw new Error(book); return r.text();
    }).then(function (t) {
      var v = {};
      t.split('\n').forEach(function (l) { var a = l.split('\t'); if (a.length >= 3) v[a[0] + ':' + a[1]] = a.slice(2).join(' '); });
      return v;
    });
    return bibleCache[key];
  }
  // 'Ad Romanos 13: 11-14' or '3 Regum 19: 3-8'; several sections separated by ';', verse lists by ','
  function parseRef(ref) {
    var m = /^(\d)?\s*([^\d:]+?)(?:\s+(\d))?\s+(\d+):\s*(.+)$/.exec(ref.trim());
    if (!m) return null;
    var book = m[2].trim() + (m[1] ? ' ' + m[1] : (m[3] ? ' ' + m[3] : '')), ch = +m[4], out = [];
    m[5].split(';').forEach(function (seg) {
      seg = seg.trim();
      var c = /^(\d+):\s*(.*)$/.exec(seg);
      if (c) { ch = +c[1]; seg = c[2]; }
      seg.split(',').forEach(function (r) {
        var x = /^(\d+)[a-c]?(?:\s*-\s*(?:(\d+):)?(\d+)[a-c]?)?$/.exec(r.trim());
        if (!x) return;
        var a = +x[1], ch2 = x[2] ? +x[2] : ch, b = x[3] ? +x[3] : a;
        out.push([ch, a, ch2, b]);
        ch = ch2;
      });
    });
    return {book: book, ranges: out};
  }
  function readingText(lang, ref) {
    var p = parseRef(ref);
    if (!p) return Promise.resolve('');
    return bibleBook(lang, p.book).then(function (v) {
      var words = [];
      p.ranges.forEach(function (r) {
        for (var c = r[0]; c <= r[2]; c++) {
          for (var n = (c === r[0] ? r[1] : 1); n <= (c === r[2] ? r[3] : 200); n++) {
            if (v[c + ':' + n] === undefined) { if (c < r[2]) break; else continue; }
            words.push(v[c + ':' + n]);
          }
        }
      });
      return words.join(' ');
    });
  }
  var READ_LA = {Lesson: 'Lectio', Epistle: 'Epistola', Gospel: 'Evangelium', Psalmus: 'Psalmus', Canticum: 'Canticum'};
  // the Missal's own text (title + opening formula) where tools/m33 read it from the 1933 Missal
  function m33Readings(key, rs) {
    // the 1933 Missal wins (checked in tools/m33); a part it does not give (scan unreadable) keeps the site's reference
    var M = window.READINGS33 && READINGS33[key]; rs = rs || [];
    if (!M) return rs;
    var g = function (r) { return r.type === 'Gospel'; }, ng = function (r) { return !g(r); };
    var pick = function (a) { return {type: a.type, ref: a.ref, title: a.title, title_en: a.title_en, la: a.la, en: a.en, p33: a.p33}; };
    var pre = M.filter(ng).length ? M.filter(ng).map(pick) : rs.filter(ng);
    var gos = M.filter(g).length ? M.filter(g).map(pick) : rs.filter(g);
    return pre.concat(gos);
  }
  function drawReading(r) {
    var la = el('p', {class: 'la'}), en = el('p', {class: 'en-text'});
    var box = el('section', {class: 'reading', 'data-part': 'reading'}, [
      el('h3', null, [READ_LA[r.type], el('span', {class: 'ref', text: r.ref}), r.roman ? el('span', {class: 'badge warn', title: 'Reference from the Roman Missal (jgabc); not read from the Dominican Missal', text: 'Roman ref.'}) : null]),
      el('div', {class: 'r-cols'}, [la, en])]);
    var psTitle = function (t) { return r.type === 'Psalmus' ? t.replace(/^(Ipsi David[^.]*|Canticum graduum|Psalmus David[^.]*|A Psalm for David[^.]*|A gradual canticle|A psalm of David[^.]*)\.\s*/i, '') : t; };
    if (r.la && isSung() && window.OPMassTones && /^(Lesson|Epistle|Gospel)$/.test(r.type) && !r.passion) {
      var gos = r.type === 'Gospel', tg = null, rg = null;
      try { tg = gos || !r.title ? null : OPMassTones.epistleTitle(r.title); rg = OPMassTones.reading(r.la, gos); } catch (e) { console.warn('tone', e); }
      if (rg) {
        box.querySelector('.r-cols').remove();
        if (tg) box.appendChild(gabcBox(tg));
        box.appendChild(gabcBox(rg));
        box.appendChild(el('p', {class: 'en-text tone-en', lang: 'en'}, [el('span', {class: 'r-title', text: gos ? '' : (r.title_en || '')}), r.en || '']));
        return box;
      }
    }
    if (r.la) {
      // the title heads each column (Latin over the Latin, English over the English); the source goes on the reference line
      la.appendChild(el('span', {class: 'r-title', text: r.title || ''})); la.appendChild(document.createTextNode(r.la));
      en.appendChild(el('span', {class: 'r-title', text: r.title_en || ''})); en.appendChild(document.createTextNode(r.en || ''));
      return box;
    }
    readingText('la', r.ref).then(function (t) { la.textContent = psTitle(t); }, function () { la.textContent = ''; });
    readingText('en', r.ref).then(function (t) { en.textContent = psTitle(t); }, function () { en.textContent = ''; });
    return box;
  }
  function drawReadings(m) {
    var box = el('section', {class: 'readings', id: 'readings'});
    var rs = m.readings || [];
    if (!rs.length) return box;
    box.appendChild(el('h2', {class: 'caps-head', text: 'Lectiones'}));
    rs.forEach(function (r) {
      var la = el('p', {class: 'la'}), en = el('p', {class: 'en-text'});
      box.appendChild(el('div', {class: 'reading'}, [
        el('h3', null, [READ_LA[r.type], el('span', {class: 'ref', text: r.ref}), r.roman ? el('span', {class: 'badge warn', title: 'Reference from the Roman Missal (jgabc); not read from the Dominican Missal', text: 'Roman ref.'}) : null]),
        el('div', {class: 'r-cols'}, [la, en])]));
      readingText('la', r.ref).then(function (t) { la.textContent = t; }, function () { la.textContent = ''; });
      readingText('en', r.ref).then(function (t) { en.textContent = t; }, function () { en.textContent = ''; });
    });
    return box;
  }

  function drawSlot(part, index, c) {
    var slot = el('section', {class: 'part', 'data-part': part});
    var sel = chantOptions(part, c.id);
    var chantBox = el('div', {class: 'chant', 'aria-live': 'polite'});
    var editor = el('textarea', {class: 'gabc hide-print', spellcheck: 'false', rows: '6', hidden: 'hidden', 'aria-label': 'GABC of this chant'});
    var info = el('span', {class: 'src'});
    var toggle = el('button', {type: 'button', class: 'linkbtn', text: 'Edit GABC', onclick: function () {
      editor.hidden = !editor.hidden; toggle.textContent = editor.hidden ? 'Edit GABC' : 'Hide GABC';
    }});
    var remove = el('button', {type: 'button', class: 'linkbtn', text: 'Remove', onclick: function () {
      state.parts[part].splice(index, 1); drawMass(); writeHash();
    }});
    var ch = D.chants[c.id] || {};
    var incipit = el('span', {class: 'incipit', text: clean(ch.i || '').replace(/\s*\(.*?\)\s*/g, ' ').replace(/\.\.\..*$/, '').replace(/(\s*all\.)+\s*$/i, '').replace(/\s+alleluia\s*$/i, '').trim()});
    var mode = el('span', {class: 'mode'});
    var partName = part === 'an' && state.key === 'Quad6s' ? 'Ad Laudes' : PART_NAME[part];
    var head = el('div', {class: 'part-head hide-print'}, [el('h2', {text: partName}), state.edit ? sel : incipit, mode]);
    if (c.roman) head.appendChild(/Franciscan/.test(ch.i || '') ?
      el('span', {class: 'badge warn', title: 'Not in the Graduale O.P.: the melody of the Franciscan Graduale (Graduale Seraphicum)', text: 'Franciscan melody'}) :
      el('span', {class: 'badge warn', title: 'Not in the Graduale O.P. on GregoBase: the melody of the Roman Graduale', text: 'Roman melody'}));
    if (state.edit) { head.appendChild(toggle); head.appendChild(remove); }
    slot.appendChild(head);
    slot.appendChild(el('h2', {class: 'print-only', text: partName}));
    slot.appendChild(chantBox);
    var trc = c.id && (D.trans[c.id] || D.trans[String(c.id)]);
    var trDiv = null;
    if (trc && trc.t) { slot.classList.add('m-pair'); trDiv = el('div', {class: 'm-tr hide-print'}, trimTPText(trc.t).split(/(℣\.|℟\.)/).map(function (x) { return /^[℣℟]\.$/.test(x) ? el('span', {class: 'r', text: x}) : x; }).concat([trSrc(trc)])); slot.appendChild(trDiv); }
    slot.appendChild(editor);
    if (state.edit) slot.appendChild(el('p', {class: 'meta hide-print'}, [info]));
    sel.addEventListener('change', function () {
      state.parts[part][index] = {id: sel.value ? (/^\d+$/.test(sel.value) ? Number(sel.value) : sel.value) : null, chosen: true};
      drawMass(); writeHash();
    });
    if (!c.id) { chantBox.appendChild(el('p', {class: 'empty', text: 'Choose a chant from the list.'})); return slot; }
    chantBox.appendChild(el('p', {class: 'loading', text: 'Loading…'}));
    loadGabc(c.id).then(function (text) {
      var g = splitGabc(text);
      if (!g.body.trim()) {
        chantBox.innerHTML = '';
        chantBox.appendChild(el('p', {class: 'empty', text: 'This chant (Graduale O.P. p. ' + D.chants[c.id].pg + ') has not been transcribed in GregoBase yet. Its GABC can be typed in the editor.'}));
        editor.hidden = false; toggle.textContent = 'Hide GABC';
      }
      var edited = state.edited[part + index];
      editor.value = edited != null ? edited : g.body;
      var h = g.header, meta = [];
      if (h.mode) mode.textContent = 'Mode ' + (ROMAN[parseInt(h.mode, 10)] || h.mode);
      if (h.mode) meta.push('Mode ' + h.mode);
      if (h.commentary) meta.push(h.commentary);
      meta.push('Graduale O.P. p. ' + D.chants[c.id].pg);
      if (h.transcriber) meta.push('transcribed by ' + h.transcriber);
      info.textContent = meta.join(' · ') + ' · ';
      info.appendChild(el('a', {href: 'https://gregobase.selapa.net/chant.php?id=' + c.id, target: '_blank', rel: 'noopener', text: 'GregoBase ' + c.id}));
      var shown = function () { return part === 'in' ? fullIntroit(editor.value, h, state.key) : editor.value; };
      // the English of the Introit follows the Latin as it is sung: Glory be, then the antiphon again
      if (part === 'in' && trDiv && !/Glory be/.test(trDiv.textContent)) {
        var lt = gabcText(shown()), ant0 = trimTPText(trc.t).split('℣.')[0].trim();
        var antE = ant0.split(/\s+/).slice(0, 6).join(' ').replace(/[,.;:]$/, '') + '…';
        if (/Gl[oó]ria Patri/.test(lt) && !/sine Gl[oó]ria Patri/.test(lt)) { trDiv.appendChild(document.createTextNode(' Glory be to the Father, and to the Son, and to the Holy Ghost. As it was in the beginning, is now, and ever shall be, world without end. Amen. ')); }
        if (/Ant\.|Gl[oó]ria Patri|repetitur/.test(lt) && ant0) { trDiv.appendChild(el('span', {class: 'r', text: 'Ant. '})); trDiv.appendChild(document.createTextNode(antE)); }
        var ts0 = trDiv.querySelector('.tr-src'); if (ts0) trDiv.appendChild(ts0);   // the source stays last
      }
      if (state.ordo === 'low' && !state.edit) {   // at Low Mass the priest reads the proper: the text only, without the notes
        chantBox.innerHTML = ''; chantBox.className = 'said'; mode.textContent = '';
        var tx = gabcText(seasonalGabc(shown(), part)).replace(/^(\S)(\S*)/, function (a, f, r) { return f + r.toLowerCase(); })
          .replace(/Ant\.\s*([A-ZÁÉÍÓÚÆŒ]+)\s*$/, function (a, w) { return 'Ant. ' + w.charAt(0) + w.slice(1).toLowerCase(); });
        var antw = tx.split('℣.')[0].trim().split(/\s+/).slice(0, 3).join(' ').replace(/[,.;:]$/, '');
        tx = tx.replace(/Ant\.\s*\S+\s*$/, 'Ant. ' + antw + '…');
        var lp = el('p', {class: 'la', lang: 'la'});
        // the book's own directions in the chant (sine Gloria Patri, repetitur…) stay red, as rubrics
        tx.split(/(℣\.|℟\.|Ant\.|sine Gl[oó]ria Patri,?\s*sed repetitur:?|sine Gl[oó]ria Patri\.?|(?:et )?repetitur:?|Ps\.)/).forEach(function (x) {
          if (!x) return;
          if (/^(℣\.|℟\.|Ant\.|Ps\.)$/.test(x)) lp.appendChild(el('span', {class: 'o-mark', text: x + ' '}));
          else if (/^(sine|(et )?repetitur)/.test(x)) lp.appendChild(el('span', {class: 'said-rub', text: x + ' '}));
          else lp.appendChild(document.createTextNode(x.replace(/^\s+/, '')));
        });
        chantBox.appendChild(lp);
        return;
      }
      renderInto(chantBox, shown(), h, part);
      var timer;
      editor.addEventListener('input', function () {
        state.edited[part + index] = editor.value;
        clearTimeout(timer);
        timer = setTimeout(function () { renderInto(chantBox, shown(), h, part); }, 400);
      });
    }).catch(function (e) { showError(chantBox, e); });
    return slot;
  }

  // ---------------------------------------------------------------- calendar
  function easter(y) { // Anonymous Gregorian algorithm
    var a = y % 19, b = Math.floor(y / 100), c = y % 100, d = Math.floor(b / 4), e = b % 4, f = Math.floor((b + 8) / 25),
        g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30, i = Math.floor(c / 4), k = c % 4,
        l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451),
        month = Math.floor((h + l - 7 * m + 114) / 31), day = ((h + l - 7 * m + 114) % 31) + 1;
    return new Date(y, month - 1, day);
  }
  var DAY = 864e5;
  function addDays(d, n) { var r = new Date(d); r.setDate(r.getDate() + n); return r; }
  function diffDays(a, b) { return Math.round((Date.UTC(a.getFullYear(), a.getMonth(), a.getDate()) - Date.UTC(b.getFullYear(), b.getMonth(), b.getDate())) / DAY); }
  var WD = ['', 'm', 't', 'w', 'h', 'f', 's'];

  // the Temporale key for a date (the Mass of the day, or of the preceding Sunday on a free feria)
  function temporaleKey(d) {
    var y = d.getFullYear(), dow = d.getDay();
    var E = easter(y), fromE = diffDays(d, E);
    var nat = new Date(y, 11, 25), adv1 = addDays(nat, -((nat.getDay() || 7) + 21));
    var candidates = [];
    if (d >= adv1 && d < nat) {
      var w = Math.floor(diffDays(d, adv1) / 7) + 1;
      if (w === 3 && dow === 3) candidates.push('Adv3w');
      if (w === 3 && dow === 5) candidates.push('Adv3f');
      if (w === 3 && dow === 6) candidates.push('Adv3s');
      if (d.getMonth() === 11 && d.getDate() === 24) candidates.push('Dec24');
      candidates.push('Adv' + Math.min(w, 4));
      return candidates;
    }
    var md = (d.getMonth() + 1) * 100 + d.getDate();
    if (md === 1225) return ['Dec25_3', 'Dec25_1', 'Dec25_2'];
    if (md > 1225) return dow === 0 ? ['Nat1'] : ['Dec25_3'];
    if (md === 101) return ['Jan1'];
    if (md >= 102 && md <= 105) {
      var sunIn = [2, 3, 4, 5].some(function (dd) { return new Date(y, 0, dd).getDay() === 0; });
      if (dow === 0 || (md === 102 && !sunIn)) return ['Nat2'];
      return ['Jan1', 'Nat2'];
    }
    if (md === 106) return ['Epi'];
    var sept = addDays(E, -63);
    if (md > 106 && d < sept) {
      var epi = new Date(y, 0, 6), epi1 = addDays(epi, 7 - epi.getDay());
      if (d < epi1) return ['Epi'];
      return ['Epi' + Math.min(Math.floor(diffDays(d, epi1) / 7) + 1, 6)];
    }
    if (fromE >= -63 && fromE < -46) return [['7a', '6a', '5a'][Math.floor((fromE + 63) / 7)]];
    if (fromE >= -46 && fromE < -42) return ['5a' + WD[dow]];
    if (fromE >= -42 && fromE < 0) {
      var q = Math.floor((fromE + 42) / 7) + 1;
      return D.masses['Quad' + q + WD[dow]] ? ['Quad' + q + WD[dow]] : ['Quad' + q];
    }
    if (fromE >= 0 && fromE < 7) return ['Pasc0' + WD[dow]];
    if (fromE === 39) return ['Asc'];
    if (fromE === 48) return ['Pasc6s'];
    if (fromE >= 7 && fromE < 49) {
      var p = Math.floor(fromE / 7);
      if (fromE === 36 || fromE === 37) return ['Pasc5', 'Litaniis'];
      if (fromE === 38) return ['AscVig', 'Litaniis'];
      // the Solemnity of St Joseph (Wednesday after Easter II) was replaced in 1955 by St Joseph the Worker: an option only
      if (p === 2 && dow === 3) return ['Pasc2', 'Pasc2w'];
      return ['Pasc' + p + WD[dow], 'Pasc' + p];
    }
    if (fromE >= 49 && fromE < 56) return ['Pent0' + WD[dow], 'Pent0'];
    if (fromE === 60) return ['CorpusChristi'];
    if (fromE === 68) return ['SCJ'];
    if (fromE >= 56) {
      var adv1n = addDays(new Date(y, 11, 25), -((new Date(y, 11, 25).getDay() || 7) + 21));
      var weeksLeft = Math.floor(diffDays(adv1n, d) / 7);
      var n = Math.floor((fromE - 49) / 7);
      var keys = [];
      // Christ the King: last Sunday of October
      var oct31 = new Date(y, 9, 31), ck = addDays(oct31, -oct31.getDay());
      if (diffDays(d, ck) === 0) keys.push('ChristusRex');
      // September Ember days: Wednesday, Friday, Saturday after the third Sunday of September
      var s1 = new Date(y, 8, 1), sun3 = addDays(s1, ((7 - s1.getDay()) % 7) + 14), ed = diffDays(d, sun3);
      if (ed === 3) keys.push('EmbWedSept'); if (ed === 5) keys.push('EmbFriSept'); if (ed === 6) keys.push('EmbSatSept');
      // the last Sunday (Dominica ultima post Octavam Trinitatis) has its own Mass; the Sundays between the
      // twenty-first after the Octave of Trinity and the last take the prayers and lessons of the Sundays left
      // over after the Epiphany, the chants of the twenty-first (Missale O.P. 1939)
      var dS = diffDays(adv1n, d) + dow;
      if (n === 1 || fromE < 63) keys.push('Pent1');
      else if (dS <= 7) keys.push('Pent24');
      else if (n >= 24) keys.push('Epi' + Math.max(3, Math.min(6, 8 - Math.round(dS / 7))) + 'r');
      else keys.push('Pent' + Math.min(n, 23));
      return keys;
    }
    return [];
  }

  function iso(d) { return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  function fromIso(v) { var p = v.split('-').map(Number); return new Date(p[0], p[1] - 1, p[2]); }

  // the Masses of a date, the one taking precedence first (classes of the rubrics of 1960)
  function massesOf(d) {
    var seen = {}, temp = temporaleKey(d).filter(function (k) { if (!D.masses[k] || seen[k]) return false; seen[k] = 1; return true; });
    var feasts = [];
    D.sections.forEach(function (s) {
      if (s.id !== 'sanctorum') return;
      s.items.forEach(function (k) {
        var m = D.masses[k];
        if (k === 'S0325' || k === 'S0319') { if (diffDays(d, feastDate(k, d.getFullYear())) === 0) feasts.push(k); return; }
        if (m.month === d.getMonth() && m.day === d.getDate()) {
          if (VIGIL_CLASS[k] && d.getDay() === 0) return;      // a vigil falling on Sunday is omitted
          feasts.push(k);
        }
      });
    });
    var beati = (D.sections.filter(function (s) { return s.id === 'beati'; })[0] || {items: []}).items
      .filter(function (k) { var m = D.masses[k]; return m.month === d.getMonth() && m.day === d.getDate(); });
    var tk = temp[0], tc = tk ? temporalClass(tk, d) : 9;
    feasts.sort(function (a, b) { return feastClass(a) - feastClass(b); });
    var fk = feasts[0], fc = fk ? feastClass(fk) : 9;
    // the higher class wins; at equal class a Sunday or privileged feria wins, otherwise the feast
    var lentFeria = tk && /^(5a.|Quad)/.test(tk) && d.getDay() !== 0;
    var win = !fk ? tk : (!tk ? fk : (fc >= 4 ? tk : (fc < tc ? fk : (tc < fc ? tk : (d.getDay() === 0 || tc <= 1 || lentFeria ? tk : fk)))));
    // a free Saturday outside Advent and Lent: the Mass of Our Lady on Saturday
    if (d.getDay() === 6 && win === tk && tc >= 4 && !/^(Adv|5a|Quad|7a|6a)/.test(tk || '') && D.masses.C79s) {
      temp = temp.concat(['C79s']); win = 'C79s';
    }
    return {win: win, temp: temp, feasts: feasts, beati: beati};
  }

  function onDate(d, keepMass) {
    state.date = d;
    $('#date').value = iso(d);
    var r = massesOf(d), box = $('#dateResults');
    box.innerHTML = '';
    var mk = function (k, label) {
      return el('button', {type: 'button', 'data-k': k, class: 'alt' + (k === r.win ? ' win' : ''), onclick: function () { showMass(k); markChips(k); }},
        [el('small', {text: label}), clean(D.masses[k].title).replace(/^\d+ [A-Za-z.]+ — /, '')]);
    };
    var all = r.temp.concat(r.feasts).concat(r.beati);
    if (all.length > 1) {
      r.temp.forEach(function (k, i) { box.appendChild(mk(k, i ? 'or' : 'Temporale')); });
      r.feasts.forEach(function (k) { box.appendChild(mk(k, D.masses[k].rank ? D.masses[k].rank + ' class' : 'Feast')); });
      r.beati.forEach(function (k) { box.appendChild(mk(k, 'Blessed (ad libitum)')); });
    }
    if (!keepMass && r.win) showMass(r.win);
    else { drawRing(); drawPills(); writeHash(); }
  }
  function markChips(k) {
    Array.prototype.forEach.call(document.querySelectorAll('#dateResults .alt'), function (b) { b.classList.toggle('win', b.getAttribute('data-k') === k); });
  }
  function shiftDay(n) { onDate(addDays(state.date || new Date(), n)); }

  function fillOrdinarySelects() {
    var nums = [];
    D.kyriale.forEach(function (id) { var m = /^(Kyrie|Gloria|Sanctus|Agnus)\s+([IVX]+)\b/.exec(D.chants[id].i); if (m && nums.indexOf(m[2]) < 0) nums.push(m[2]); });
    var so = $('#selOrd'); so.appendChild(el('option', {value: '', text: 'Automatic (by the rank of the day)'})); so.appendChild(el('option', {value: 'none', text: 'None'}));
    nums.forEach(function (n) { so.appendChild(el('option', {value: n, text: 'Missa ' + n})); });
    var sc = $('#selCredo'); sc.appendChild(el('option', {value: '', text: 'Automatic (Credo I when it is said)'})); sc.appendChild(el('option', {value: 'none', text: 'None'}));
    D.kyriale.forEach(function (id) { var m = /^Credo\s+([IVX]+)$/.exec(D.chants[id].i); if (m) sc.appendChild(el('option', {value: m[1], text: 'Credo ' + m[1]})); });
  }

  // exposed for testing and for the browser console
  // ---------------------------------------------------------------- the two PDFs
  // the words of a chant, from its GABC
  function gabcText(body) {
    return body
      .replace(/<sp>V\/<\/sp>\.?/g, '℣.').replace(/<sp>R\/<\/sp>\.?/g, '℟.').replace(/<sp>\*<\/sp>/g, '')
      .replace(/\([^)]*\)/g, '')
      .replace(/\[[^\]]*\]/g, '')
      .replace(/<\/?[a-z]+>/gi, '')
      .replace(/[{}*†_^|]/g, '')
      .replace(/\s+/g, ' ')
      .replace(/\s+([,.;:!?])/g, '$1')
      .replace(/Gl[oó]ri\s*-?\s*a\.?\s*E\s*u\s*o\s*u\s*a\s*e\.?/g, 'Gloria Patri.')
      .replace(/\s*E\s*u\s*o\s*u\s*a\s*e\.?\s*$/g, '')
      .trim();
  }
  function paschal() { return currentSeason() === 'pasch' || /^(Pasc|Asc|AscVig|Litaniis|Pent0)/.test(state.key || '') || (state.key && D.masses[state.key] && /Tempore Paschali/.test(D.masses[state.key].title || '')); }
  // where the English of a chant comes from, shown after it
  var TR_SRC = {douay: 'Douay-Rheims', dra: 'Douay-Rheims, adapted to the chant', own: 'AI translation'};
  function trSrc(t) { var k = t.s || 'own'; return el('span', {class: 'tr-src' + (k === 'own' ? ' tr-ai' : ''), text: TR_SRC[k] || TR_SRC.own}); }
  function trimTPText(t) {
    if (paschal()) return t.replace(/\(P\.T\.\s*([^)]*)\)/g, '$1');
    return t.replace(/\s*\(P\.T\.[^)]*\)/g, '').replace(/\s*T\.\s?P\.\s*Alleluia,?\s*alleluia!?/g, '').replace(/,\s*alleluia[!.]?\s*(?=(℣\.|Glory be|$))/gi, '. ').replace(/\.\s*\./g, '.').trim();
  }
  function chantLatin(id) {
    return loadGabc(id).then(function (t) {
      var b = splitGabc(t).body;
      b = seasonalGabc(b, (D.chants[id] || {}).p);
      return gabcText(b);
    }, function () { return ''; });
  }
  var PART_EN_FULL = {in: 'Office', gr: 'Responsory', al: 'Alleluia', tr: 'Tract', se: 'Sequence', of: 'Offertory', co: 'Communion', an: 'Vespers antiphon', pr: 'Before Mass', ad: 'Adoration of the Cross'};
  var READ_EN = {Lesson: 'Lesson', Epistle: 'Epistle', Gospel: 'Gospel'};
  function buildCongregation() {
    var m = D.masses[state.key], box = $('#cong'), d = state.date || new Date(), jobs = [];
    box.innerHTML = '';
    var col = massColor(state.key);
    var cls = m.rank || (isTemporal(state.key) ? ['', 'I', 'II', 'III', 'IV'][temporalClass(state.key, state.date)] : '');
    var title = clean(m.title).replace(/^\d+ [A-Za-z.]+ — /, '');
    var en = m.name_en || (isTemporal(state.key) ? clean(m.en || '') : '');
    box.appendChild(el('header', {class: 'c-head'}, [
      el('div', {class: 'c-cross', text: '✠'}),
      el('div', {class: 'c-kicker', text: 'Missa juxta ritum Sacri Ordinis Praedicatorum'}),
      el('h1', {text: title}),
      en && en !== title ? el('div', {class: 'c-en', text: en}) : null,
      el('div', {class: 'c-date', text: WEEKDAYS[d.getDay()] + ', ' + d.getDate() + ' ' + MONTHS[d.getMonth()] + ' ' + d.getFullYear() +
        (cls ? ' · ' + cls + ' class' : '') + ' · ' + COLOR_LA[col]})
    ]));
    var sec = function (labLa, labEn, ref, isReading) {
      var la = el('div', {class: 'c-la', lang: 'la'}), enb = el('div', {class: 'c-en-text', lang: 'en'});
      box.appendChild(el('section', {class: 'c-sec' + (isReading ? ' c-read' : '')}, [
        el('h2', null, [el('span', {class: 'c-lab', text: labLa}), el('span', {class: 'c-lab-en', text: labEn}), ref ? el('span', {class: 'c-ref', text: ref}) : null]),
        el('div', {class: 'c-cols'}, [la, enb])
      ]));
      return {la: la, en: enb};
    };
    var chantSec = function (p, c) {
      var tr = D.trans[c.id] || D.trans[String(c.id)];
      var o = sec(PART_NAME[p], PART_EN_FULL[p], tr && tr.r ? tr.r : '');
      if (tr) { o.en.textContent = trimTPText(tr.t); o.en.appendChild(trSrc(tr)); }
      else o.en.appendChild(el('span', {class: 'c-missing', text: '(No English translation of this chant is available yet.)'}));
      jobs.push(chantLatin(c.id).then(function (t) { o.la.textContent = t; }));
    };
    var readSec = function (r) {
      var o = sec(READ_LA[r.type], READ_EN[r.type], r.ref, true);
      if (r.la) { o.la.textContent = r.la; o.en.textContent = r.en || ''; return; }   // as printed in the Missale O.P. (1933)
      jobs.push(readingText('la', r.ref).then(function (t) { o.la.textContent = t; }, function () {}));
      jobs.push(readingText('en', r.ref).then(function (t) { o.en.textContent = t; }, function () {}));
    };
    var R = rubricsOf(state.key, state.date), O = ordinaryIds(), OT = window.ORDINARY || {};
    box.appendChild(el('p', {class: 'c-rubric', text: rubricLine(R)}));
    var ordSec = function (t) { if (!t) return; var o = sec(t.la_name, t.en_name, ''); o.la.textContent = t.la; o.en.textContent = t.tr || t.en; };
    if (O.as) ordSec(O.as === D.front[1] ? OT.vidi : OT.as);
    massSequence(m, state.parts).forEach(function (it) {
      if (it.t === 'ord') {
        if (!O[it.k]) return;
        if (it.k === 'ag') ordSec(R.requiem ? OT.agReq : OT.ag);
        else if (it.k === 'it') {
          var nm = (D.chants[O.it] || {}).i || '';
          ordSec(/Requiescant/.test(nm) ? OT.req : /Benedicamus/.test(nm) ? OT.ben : (easterOctave(d) || state.key === 'Quad6s') ? OT.itePasch : OT.ite);
        } else ordSec(OT[it.k]);
        return;
      }
      if (it.t === 'chant') { if (it.c.id) chantSec(it.p, it.c); }
      else if (it.t === 'read') readSec(it.r);
      else if (it.t === 'pref') {
        var pn = prefaceOf(state.key, state.date);
        if (pn) { var P = prefaceText(pn, state.key, state.date), o = sec('Praefatio', P.en, ''); o.la.textContent = P.la; o.en.textContent = P.tr; }
      }
    });
    box.appendChild(el('footer', {class: 'c-foot', text: 'Chants: Graduale O.P. (1950). Readings: Vulgate and Douay-Rheims. English of the chants: Douay-Rheims where the chant is the text of Scripture, otherwise an AI translation (marked).'}));
    return Promise.all(jobs);
  }
  function printAs(mode) {
    var go = function () {
      document.body.setAttribute('data-print', mode);
      var old = document.title;
      document.title = clean(D.masses[state.key].title).replace(/^\d+ [A-Za-z.]+ — /, '') + (mode === 'choir' ? ' — Choir' : ' — Congregation');
      setTimeout(function () { window.print(); document.title = old; }, 150);
    };
    if (mode === 'congregation') buildCongregation().then(go, go); else go();
  }
  window.addEventListener('afterprint', function () { document.body.removeAttribute('data-print'); });

  if ('serviceWorker' in navigator && location.protocol !== 'file:') {
    window.addEventListener('load', function () { navigator.serviceWorker.register('sw.js').catch(function () {}); });
  }
  window.ProprOP = {D: D, dismissGabc: dismissGabc, solemnDay: solemnDay, flectamusDay: flectamusDay, PART_NAME: PART_NAME, clean: clean, prefaceText: prefaceText, prefaceChant: prefaceChant, seasonalReadings: seasonalReadings, chantLatin: chantLatin, trimTPText: trimTPText, paschal: function () { return paschal(); }, stripTP: stripTP, seasonalGabc: seasonalGabc, prefaceChant: prefaceChant, findKyriale: findKyriale, iso: iso, diffDays: diffDays, addDays: addDays, exsurgeGabc: exsurgeGabc, prefaceOf: prefaceOf, autoKyriale: autoKyriale, isMarian: isMarian, paschalKyrie: paschalKyrie, ordinaryIds: ordinaryIds, rubricsOf: rubricsOf, massSequence: massSequence, buildCongregation: buildCongregation, printAs: printAs, gabcText: gabcText, renderInto: renderInto, loadGabc: loadGabc, splitGabc: splitGabc, temporaleKey: temporaleKey, showMass: showMass, massesOf: massesOf, massColor: massColor, massParts: massParts, readingText: readingText, m33Readings: m33Readings, fullIntroit: fullIntroit, state: function () { return state; }, easter: easter, titleText: titleText, feastClass: feastClass, temporalClass: temporalClass, isTemporal: isTemporal};

  function start() {
    if (!document.getElementById('selMass')) return;   // loaded as a library (e.g. by the Office page)
    fillMassSelect();
    fillOrdinarySelects();
    $('#selMass').addEventListener('change', function (e) { if (e.target.value) showMass(e.target.value); });
    $('#date').addEventListener('change', function (e) { if (e.target.value) onDate(fromIso(e.target.value)); });
    $('#prevDay').addEventListener('click', function () { shiftDay(-1); });
    $('#nextDay').addEventListener('click', function () { shiftDay(1); });
    if (window.matchMedia && matchMedia('(max-width: 960px)').matches) Array.prototype.forEach.call(document.querySelectorAll('.side .collapse'), function (x) { x.removeAttribute('open'); });
    if (window.OPCal && $('#cal')) {
      state.cal = OPCal($('#cal'), {
        date: new Date(),
        onPick: function (d) { onDate(d); },
        dot: function (d) { var w = massesOf(d).win, c = w ? massColor(w, d) : ''; return c === 'black' ? '#7a7a7a' : (c ? COLORS[c] : ''); }
      });
    }
    $('#selSeason').addEventListener('change', function (e) { state.season = e.target.value; showMass(state.key); });
    $('#selOrd').addEventListener('change', function (e) { state.ord = e.target.value; drawMass(); writeHash(); });
    $('#selCredo').addEventListener('change', function (e) { state.credo = e.target.value; drawMass(); writeHash(); });
    $('#selAsp').addEventListener('change', function (e) { state.asp = e.target.value; drawMass(); writeHash(); });
    $('#selOrdo').addEventListener('change', function (e) { state.ordo = e.target.value; drawMass(); writeHash(); });
    if ($('#segRub')) $('#segRub').addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      state.rub = b.getAttribute('data-v') || ''; try { localStorage.setItem('rubrics', state.rub); } catch (x) {}
      drawMass(); writeHash();
    });
    // the circumstances of the Mass (shown with the Order of Mass): Communion, a prelate, the Blessed Sacrament, the servers
    [['selComm', 'comm'], ['selPrel', 'prel'], ['selSac', 'sac'], ['selServ', 'serv']].forEach(function (x) {
      var sel = $('#' + x[0]); if (sel) sel.addEventListener('change', function (e) { state[x[1]] = e.target.value; drawMass(); writeHash(); });
    });
    if ($('#segForm')) $('#segForm').addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      state.ordo = b.getAttribute('data-v') || ''; $('#selOrdo').value = state.ordo; drawMass(); writeHash();
    });

    if ($('#btnPM')) {
      var pmb = $('#btnPM'), pml = $('#pmList');
      var pmClose = function () { pml.hidden = true; pmb.setAttribute('aria-expanded', 'false'); };
      pmb.addEventListener('click', function (e) { e.stopPropagation(); pml.hidden = !pml.hidden; pmb.setAttribute('aria-expanded', String(!pml.hidden)); });
      pml.addEventListener('click', function (e) { setTimeout(pmClose, e.target.id === 'btnShare' ? 1600 : 0); });
      document.addEventListener('click', function (e) { if (!e.target.closest('.pmenu')) pmClose(); });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') pmClose(); });
    }
    // the booklets (Choir Book, Priest's Missal, Congregation Booklet) open as A4 pages ready to print
    var openBook = function (b) { writeHash(); window.open('booklet.html?b=' + b + location.hash, '_blank'); };
    $('#btnChoir').addEventListener('click', function () { openBook('choir'); });
    $('#btnCong').addEventListener('click', function () { openBook('cong'); });
    if ($('#btnPriest')) $('#btnPriest').addEventListener('click', function () { openBook('priest'); });
    $('#chkEdit').addEventListener('change', function (e) { state.edit = e.target.checked; drawMass(); });
    $('#btnShare').addEventListener('click', function () {
      var url = location.href, b = $('#btnShare');
      if (navigator.share) navigator.share({title: document.title, url: url}).catch(function () {});
      else if (navigator.clipboard) navigator.clipboard.writeText(url).then(function () { b.textContent = 'Link copied'; setTimeout(function () { b.textContent = 'Share this Mass'; }, 1500); });
    });
    var resizeTimer, lastW = window.innerWidth;
    window.addEventListener('resize', function () {
      if (Math.abs(window.innerWidth - lastW) < 40) return;
      lastW = window.innerWidth;
      clearTimeout(resizeTimer); resizeTimer = setTimeout(function () { if (state.key) drawMass(); }, 300);
    });
    if (HWP) {
      var hh = readHash() || {key: 'Quad6', opts: {}}, KEYS = ['Quad6', 'Quad6m', 'Quad6t', 'Quad6w', 'Quad6h', 'Quad6f', 'Quad6s'];
      var stored = ''; try { stored = localStorage.getItem('hwRite') || ''; } catch (e) {}
      state.hwr = hh.opts.hw === '1959' || hh.opts.hw === '1939' ? hh.opts.hw : (stored || '1939');
      state.ordo = hh.opts.ordo || ''; state.comm = hh.opts.comm || (hh.opts.conv === '1' ? 'friars' : ''); state.prel = hh.opts.prel || ''; state.sac = hh.opts.sac || ''; state.serv = hh.opts.serv || ''; state.rub = hh.opts.rub || rubPref(); state.ord = hh.opts.ord || ''; $('#selOrdo').value = state.ordo; $('#selOrd').value = state.ord;
      var today = new Date(); today.setHours(0, 0, 0, 0);
      var Ey = easter(today.getFullYear()); if (diffDays(today, Ey) > 0) Ey = easter(today.getFullYear() + 1);
      var dayOf = function (k) { return addDays(Ey, KEYS.indexOf(k) - 7); };
      // the 1959 reform is post-1955: kept for reference, hidden unless asked for (Joseph, 26 Nov 2026)
      var b59 = document.querySelector('#hwRite [data-r="1959"]'), show59 = $('#hwShow59');
      if (state.hwr === '1959' && b59) b59.hidden = false;
      if (show59) show59.addEventListener('click', function () { if (b59) b59.hidden = !b59.hidden; if (b59 && b59.hidden && state.hwr === '1959') { state.hwr = '1939'; try { localStorage.setItem('hwRite', '1939'); } catch (er) {} drawMass(); writeHash(); mark(); } });
      var mark = function () {
        Array.prototype.forEach.call(document.querySelectorAll('#hwDays button'), function (b) { var on = b.getAttribute('data-k') === state.key; b.classList.toggle('on', on); b.setAttribute('aria-current', on ? 'page' : 'false'); });
        Array.prototype.forEach.call(document.querySelectorAll('#hwRite button'), function (b) { var on = b.getAttribute('data-r') === state.hwr; b.classList.toggle('on', on); b.setAttribute('aria-pressed', on); });
      };
      var openDay = function (k) { if (KEYS.indexOf(k) < 0) k = 'Quad6'; state.key = k; onDate(dayOf(k), true); showMass(k); mark(); window.scrollTo(0, 0); };
      $('#hwDays').addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) openDay(b.getAttribute('data-k')); });
      $('#hwRite').addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b) return;
        state.hwr = b.getAttribute('data-r'); try { localStorage.setItem('hwRite', state.hwr); } catch (er) {}
        drawMass(); writeHash(); mark();
      });
      openDay(hh.key);
      return;
    }
    var h = readHash();
    if (BOOKP) {
      var ob = (h && h.opts) || {};
      state.season = ob.season || 'auto'; state.ord = ob.ord || ''; state.credo = ob.credo || ''; state.asp = ob.asp || ''; state.ordo = ob.ordo || ''; state.comm = ob.comm || (ob.conv === '1' ? 'friars' : ''); state.prel = ob.prel || ''; state.sac = ob.sac || ''; state.serv = ob.serv || ''; state.rub = ob.rub || rubPref(); state.hwr = ob.hw === '1959' ? '1959' : '1939';
      var bd = ob.d ? fromIso(ob.d) : new Date(); bd.setHours(0, 0, 0, 0);
      if (h && D.masses[h.key]) state.key = h.key;
      onDate(bd, !!(h && D.masses[h.key]));
      if (h && D.masses[h.key]) showMass(h.key, h.over);
      if (window.OPBook) OPBook.build(window.ProprOP);
      return;
    }
    if (h && D.masses[h.key]) {
      var o = h.opts;
      state.season = o.season || 'auto'; state.ord = o.ord || ''; state.credo = o.credo || ''; state.asp = o.asp || ''; state.ordo = o.ordo || ''; state.comm = o.comm || (o.conv === '1' ? 'friars' : ''); state.prel = o.prel || ''; state.sac = o.sac || ''; state.serv = o.serv || ''; state.rub = o.rub || rubPref(); state.hwr = o.hw === '1959' ? '1959' : '1939';
      $('#selSeason').value = state.season; $('#selOrd').value = state.ord; $('#selCredo').value = state.credo; $('#selAsp').value = state.asp; $('#selOrdo').value = state.ordo; 
      state.key = h.key;
      onDate(o.d ? fromIso(o.d) : new Date(), true);
      showMass(h.key, h.over);
    } else onDate(new Date());
  }
  // the chant is measured with the page's fonts, so wait for them
  var fonts = ['16px "Crimson Text"', 'italic 16px "Crimson Text"', 'bold 16px "Crimson Text"', '16px Versiculum'];
  Promise.all(fonts.map(function (f) { return document.fonts ? document.fonts.load(f) : null; })).then(start, start);
})();
