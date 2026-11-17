/* Propria Missae juxta ritum Ordinis Praedicatorum
 * A Dominican version of the Propers tool of bbloomf/jgabc (public domain), rendering the chants of
 * the Graduale O.P. (1950) with exsurge.  Data: data/masses.js (see /build).
 */
(function () {
  'use strict';
  var D = window.DOMINICAN;
  var PARTS = ['pr', 'in', 'gr', 'al', 'tr', 'se', 'ad', 'of', 'co', 'an'];
  var PART_NAME = {in: 'Introitus', gr: 'Graduale', al: 'Alleluia', tr: 'Tractus', se: 'Sequentia', of: 'Offertorium', co: 'Communio', an: 'Ad Vesperas', pr: 'Ante Missam', ad: 'Ad adorationem Crucis'};
  var PART_EN = {in: 'Introit', gr: 'Gradual', al: 'Alleluia', tr: 'Tract', se: 'Sequence', of: 'Offertory', co: 'Communion', an: 'Vespers', pr: 'Before Mass', ad: 'Adoration of the Cross'};
  var PART_ABBR = {in: 'Intr.', gr: 'Resp.', al: 'Allel.', tr: 'Tract.', se: 'Seq.', of: 'Offert.', co: 'Comm.'};
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
  var state = {key: null, parts: null, edited: {}, date: null, season: 'auto', ord: '', credo: '', asp: '', edit: false};

  function readHash() {
    var h = decodeURIComponent(location.hash.slice(1));
    if (!h) return null;
    var bits = h.split('&'), out = {key: bits.shift(), over: {}, opts: {}};
    bits.forEach(function (b) {
      var kv = b.split('=');
      if (PARTS.indexOf(kv[0]) >= 0) out.over[kv[0]] = kv[1] ? kv[1].split(',').map(function (x) { return /^\d+$/.test(x) ? Number(x) : x; }) : [];
      else if (['d', 'season', 'ord', 'credo', 'asp'].indexOf(kv[0]) >= 0) out.opts[kv[0]] = kv[1] || '';
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
  function makeContext() {
    var ctxt = new exsurge.ChantContext(exsurge.TextMeasuringStrategy.Canvas);
    ctxt.condenseLineAmount = 1;
    ctxt.lineBreaking = 'optimal';
    ctxt.setGlyphScaling(1 / 16);
    ctxt.textColor = 'currentColor';
    ctxt.staffLineColor = ctxt.neumeLineColor = ctxt.dividerLineColor = 'currentColor';
    ctxt.negativeFillColor = 'var(--paper, #fff)';
    ctxt.setFont("'Crimson Text', serif", 19.2 / 0.9);
    ctxt.spaceBetweenSystems = 0;
    ctxt.textStyles.dropCap.size = 64;
    ctxt.textStyles.annotation.size = 12.8;
    ctxt.minLyricWordSpacing *= 0.7;
    ctxt.accidentalSpaceMultiplier = 1.5;
    ctxt.specialCharProperties['font-family'] = "'Versiculum'";
    ctxt.specialCharProperties['font-variant'] = 'normal';
    ctxt.specialCharProperties['font-weight'] = '400';
    var defaultSpecialCharText = ctxt.specialCharText;
    ctxt.specialCharText = function (ch) { return defaultSpecialCharText(ch).toLowerCase(); };
    ctxt.setRubricColor('var(--rubric, #b3121f)');
    return ctxt;
  }
  // Outside Paschaltide the optional "T. P. Alleluia" at the end of a chant is not sung
  function stripTP(gabc) {
    var m = /<i>\s*T\.\s*P\.\s*<\/i>/.exec(gabc);
    if (!m) return gabc;
    var j = gabc.indexOf('(::)', m.index);
    var k = j < 0 ? -1 : gabc.indexOf('(::)', j + 4);
    if (k < 0) return gabc.slice(0, m.index) + '(::)';
    return gabc.slice(0, m.index) + '(::)' + gabc.slice(k + 4);
  }
  function exsurgeGabc(gabc) {
    if (currentSeason() !== 'pasch' && !/^(Pasc|Asc|AscVig|Litaniis|Pent0)/.test(state.key || '')) gabc = stripTP(gabc);
    return gabc
      .replace(/<v>\\([VRA])bar<\/v>/g, function (m, b) { return b + '/.'; })
      .replace(/<sp>([VRA])\/<\/sp>\.?/g, function (m, b) { return b + '/.'; })
      .replace(/(\)\s+)([^()]*V\/\.\s*\d+\.?)(?=[ (])/g, '$1^$2^')
      .replace(/(\s*)((?:<(\w+)>[^()]*?<\/\3>)?(?:<(\w+)>[^()]*?<\/\4>|[^()<>])+)(?=\s+[^\s()]+\([^)])/g, function (match, ws, main) {
        return (main.match(/[|^]|^\s*$/) || (main.match(/[aeiouyáéíóúýæǽœë]/i) && !main.match(/<\w+>/))) ? match : (ws + '^' + main + '^');
      })
      .replace(/\\emph{([^(}]+)\}/g, '_$1_')
      .replace(/(v[A-Z]__[A-Z])([^_])/g, '$1_3$2')
      .replace(/([^)]\s+)([*†]|<i>i+j\.<\/i>)\(/g, '$1^$2^(')
      .replace(/\^?(<i>[^(|]*? [^(|]*?<\/i>)\^?([^(|]*)/g, '^$1^$2')
      .replace(/\*(\([:;,]+\))\s+(<i>i+j\.<\/i>)\(/g, '{*} $2$1 (')
      .replace(/(\s+)({?<i>i+j\.<\/i>}?)\(/g, '$1^$2^(')
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
      .replace(/(\))\s*\(\)/g, ')');
  }

  var renderQueue = Promise.resolve(), glyphSeq = 0;
  function renderInto(container, body, header, part) {
    // one layout at a time keeps the page responsive and the order stable
    renderQueue = renderQueue.then(function () {
      return new Promise(function (resolve) {
        try {
          var ctxt = makeContext();
          var gabc = exsurgeGabc(body);
          var mappings = exsurge.Gabc.createMappingsFromSource(ctxt, gabc);
          var dropCap = header['initial-style'] !== '0';
          var score = new exsurge.ChantScore(ctxt, mappings, dropCap);
          if (dropCap && PART_ABBR[part]) {
            var mode = ROMAN[parseInt(header.mode, 10)] || '';
            score.annotation = mode ? new exsurge.Annotations(ctxt, '%' + PART_ABBR[part] + '%', '%' + mode + '%')
                                    : new exsurge.Annotations(ctxt, '%' + PART_ABBR[part] + '%');
          }
          var width = Math.min(container.clientWidth || 600, 720);
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
                  if (isFinite(b.y) && Math.abs(b.y) < vb[3] * 2) svg.setAttribute('viewBox', [vb[0], (b.y - 3).toFixed(2), vb[2], hh.toFixed(2)].join(' '));
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
        og.appendChild(el('option', {value: id, text: clean(c.i) + (c.roman ? ' — Roman Graduale' : ' — p. ' + c.pg), selected: String(current) === id ? 'selected' : null}));
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
    if (s === 'lent' && !temporal && parts.tr.length) parts.al = [];   // from Septuagesima the Tract replaces the Alleluia (XIII, 7)
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
    if (key === 'C79s' && d) {
      var md = (d.getMonth() + 1) * 100 + d.getDate(), fE = diffDays(d, easter(d.getFullYear()));
      if (md >= 1225 || md <= 202) { parts.of = [{id: 8151}]; parts.co = [{id: 7543}]; }       // a Nativitate usque ad Purificationem
      if (fE >= 39 && fE <= 48 && parts.al.length > 1) parts.al = [parts.al[0], {id: 5526}];  // tempore Ascensionis
    }
    if (isEmber(key) && !/^Pent0/.test(key)) parts.al = [];
    if (isVigil(key) && !/^(Dec24|Jan5a)$/.test(key) && !(key === 'Dec24' && d && d.getDay() === 0)) parts.al = [];
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
    if (/^Dec25/.test(key) && d && d.getDate() !== 25) return 2;
    if (/^(Pasc1|Epi[1-6]|Pent\d+)$/.test(key) && d && d.getDay() !== 0) return 4;
    if (/^Adv[1-4]$/.test(key) && d && d.getDay() !== 0) return (d.getMonth() === 11 && d.getDate() >= 17) ? 2 : 3;
    if (/^(Adv[1-4]|Quad[1-6]|Pasc0|Pasc1|Pent0|Pent1|Pasc6s|Dec24|Dec25|Jan1|Epi|Asc|CorpusChristi|SCJ|ChristusRex|5aw)$/.test(key)) return 1;
    if (/^Quad6|^Pasc0|^Pent0/.test(key)) return 1;
    if (d && d.getDay() === 0) return 2;
    if (/^Adv/.test(key) && d && d.getMonth() === 11 && d.getDate() >= 17) return 2;
    if (/^(Adv3[wfs]|EmbWedSept|EmbFriSept|EmbSatSept|Quad1[wfs]|Pent0)/.test(key)) return 2;
    if (/^(5a|Quad)/.test(key)) return 3;
    return 4;
  }
  function feastClass(key) { return {I: 1, II: 2, III: 3}[D.masses[key].rank] || 4; }

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
  function drawRing() {
    var d = state.date || new Date(), m = D.masses[state.key], L = liturgicalYear(d);
    var size = 420, c = size / 2, r = c - 48, sw = 26;
    var svg = sv('svg', {viewBox: '0 0 ' + size + ' ' + size, role: 'img',
      'aria-label': 'The liturgical year, with ' + WEEKDAYS[d.getDay()] + ' ' + d.getDate() + ' ' + MONTHS[d.getMonth()] + ' marked'});
    var pt = function (a, rad) { return [c + rad * Math.cos(a * Math.PI / 180), c + rad * Math.sin(a * Math.PI / 180)]; };
    var ang = function (day) { return -90 + 360 * day / L.total; };
    L.seg.forEach(function (sg) {
      var a0 = ang(diffDays(sg[1], L.start)) + 0.5, a1 = ang(diffDays(sg[2], L.start)) - 0.5;
      if (a1 <= a0) return;
      var p0 = pt(a0, r), p1 = pt(a1, r), large = a1 - a0 > 180 ? 1 : 0;
      var dpath = 'M ' + p0[0].toFixed(1) + ' ' + p0[1].toFixed(1) + ' A ' + r + ' ' + r + ' 0 ' + large + ' 1 ' + p1[0].toFixed(1) + ' ' + p1[1].toFixed(1);
      if (sg[3] === 'white') svg.appendChild(sv('path', {d: dpath, fill: 'none', stroke: '#c9c9c9', 'stroke-width': sw + 2}));
      svg.appendChild(sv('path', {d: dpath, fill: 'none', stroke: COLORS[sg[3]], 'stroke-width': sw}));
      var am = (a0 + a1) / 2, lp = pt(am, r + sw / 2 + 14), rot = (am > -90 && am < 90) ? am + 90 : am - 90;
      if (a1 - a0 > 24) svg.appendChild(sv('text', {x: lp[0].toFixed(1), y: lp[1].toFixed(1), 'text-anchor': 'middle', 'dominant-baseline': 'middle',
        'font-size': 10.5, 'letter-spacing': 2, fill: '#575757', 'font-family': 'Cormorant SC, serif', transform: 'rotate(' + rot.toFixed(1) + ' ' + lp[0].toFixed(1) + ' ' + lp[1].toFixed(1) + ')'}, sg[0].toUpperCase()));
    });
    var at = ang(diffDays(d, L.start)), t = pt(at, r), p = pt(at, r + sw / 2 + 30), q = pt(at, r + sw / 2 + 2);
    svg.appendChild(sv('line', {x1: p[0], y1: p[1], x2: q[0], y2: q[1], stroke: '#0d0d0d', 'stroke-width': 3}));
    svg.appendChild(sv('circle', {cx: t[0], cy: t[1], r: 8, fill: '#ffffff', stroke: '#0d0d0d', 'stroke-width': 3}));
    var today = diffDays(d, new Date()) === 0;
    var title = clean(m ? m.title : '').replace(/^\d+ [A-Za-z.]+ — /, '');
    var lines = wrap(title, 26).slice(0, 3);
    var y0 = c - 74;
    svg.appendChild(sv('text', {x: c, y: y0, 'text-anchor': 'middle', 'font-size': 13, 'letter-spacing': 3, fill: '#575757', 'font-family': 'Cormorant SC, serif'},
      WEEKDAYS[d.getDay()].toUpperCase() + (today ? ' · TODAY' : '')));
    svg.appendChild(sv('text', {x: c, y: y0 + 62, 'text-anchor': 'middle', 'font-size': 76, fill: '#0d0d0d', 'font-family': 'Cormorant Garamond, serif', 'font-weight': 600, style: 'font-variant-numeric: lining-nums'}, String(d.getDate())));
    svg.appendChild(sv('text', {x: c, y: y0 + 100, 'text-anchor': 'middle', 'font-size': 22, 'font-style': 'italic', fill: '#575757', 'font-family': 'Cormorant Garamond, serif'}, MONTHS[d.getMonth()] + ' ' + d.getFullYear()));
    lines.forEach(function (ln, i) {
      svg.appendChild(sv('text', {x: c, y: y0 + 134 + i * 22, 'text-anchor': 'middle', 'font-size': 20, fill: '#9c1b26', 'font-family': 'Cormorant Garamond, serif', 'font-weight': 600}, ln));
    });
    var box = $('#ring');
    box.innerHTML = '';
    box.appendChild(svg);
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
    var m = D.masses[state.key], box = $('#pills'), col = massColor(state.key);
    box.innerHTML = '';
    var dot = el('span', {class: 'dot' + (col === 'white' ? ' white' : ''), 'aria-hidden': 'true'});
    dot.style.background = COLORS[col];
    box.appendChild(el('span', {class: 'pill'}, [dot, COLOR_LA[col]]));
    var cls = m.rank || (isTemporal(state.key) ? ['', 'I', 'II', 'III', 'IV'][temporalClass(state.key, state.date)] : '');
    if (cls) box.appendChild(el('span', {class: 'pill', text: cls + ' class'}));
    var se = {annum: 'Per annum', lent: 'Septuagesima–Lent', pasch: 'Paschaltide'}[currentSeason()];
    if (!isTemporal(state.key)) box.appendChild(el('span', {class: 'pill', text: se}));
  }

  // ---------------------------------------------------------------- the page
  function showMass(key, over) {
    var m = D.masses[key];
    if (!m) return;
    state.key = key;
    state.edited = {};
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
  var ORD_FALLBACK = {I: ['II'], II: ['I'], III: ['II'], IV: ['I'], V: ['II'], VI: ['V', 'II'], VIII: []};
  function easterOctave(d) { if (!d) return false; var f = diffDays(d, easter(d.getFullYear())); return f >= -1 && f <= 6; }
  function paschaltide(d) { if (!d) return false; var f = diffDays(d, easter(d.getFullYear())); return f >= 0 && f <= 55; }
  function autoKyriale(key, d) {
    var temporal = isTemporal(key), t = titleText(key);
    var sec = (D.sections.filter(function (s) { return s.items.indexOf(key) >= 0; })[0] || {}).id;
    var R = rubricsOf(key, d);
    var sunday = d && d.getDay() === 0;
    if (!R.gloria && !sunday && (temporal || isVigil(key))) return 'VIII';     // ferias, vigils, Ember days of Advent and Lent
    if (key === 'C79s' || (sec === 'votivae' && /Mari/.test(t))) return 'V';
    if (sec === 'votivae') return 'VI';
    if (paschaltide(d) && !/^(Quad6s)$/.test(key)) return 'IV';
    if (temporal && sunday && (SUNDAY_MASS.test(key) || /^(Quad[1-6]|Adv[1-4]|Pent1?\d*)$/.test(key)) && key !== 'Pent1') return 'II';   // in Dominicis
    var cls = temporal ? temporalClass(key, d) : feastClass(key);
    if (cls === 1) return 'I';
    if (cls === 2 || (d && d.getDay() === 0)) return 'II';
    return 'III';
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
    if (R.requiem) { o.ky = find('Kyrie (Requiem)'); o.it = find('Requiescant'); return o; }
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
    if (R.gloria) o.gl = part('Gloria');
    o.sa = part('Sanctus'); o.ag = part('Agnus');
    // Ite missa est when the Gloria is said (with two Alleluias in the Easter octave); otherwise Benedicamus Domino
    if (R.gloria) o.it = (easterOctave(d) || state.key === 'Quad6s') ? find('Ite IV') : (part('Ite') || find('Ite I'));
    else o.it = part('Benedicamus') || find('Benedicamus VIII');
    if (R.credo && state.credo !== 'none') o.cr = find('Credo ' + (state.credo || 'I'));
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
    return null;
  }
  function prefaceOf(key, d) {
    var m = D.masses[key], temporal = isTemporal(key), R = rubricsOf(key, d);
    if (key === 'Quad6f' || !window.PREFACES) return null;
    if (R.requiem) return 'Defunctorum';
    if (m.pref && PREFACES[m.pref]) return m.pref;
    if (key === 'SCJ') return 'Corde Iesu';
    if (key === 'ChristusRex') return 'D. N. Iesu Christo';
    if (key === 'C79s' || /in Sabbato/.test(m.title || '')) {
      // Saturday of Our Lady: from Christmas to the Purification the Mass Vultum tuum with the Preface of the Nativity
      var md = d ? (d.getMonth() + 1) * 100 + d.getDate() : 0;
      return (md >= 1225 || (md && md <= 202)) ? 'Nativitate' : 'B. Maria Virgine';
    }
    if (key === 'Pent1') return d && d.getDay() !== 0 ? 'Communis' : 'SS. Trinitate';
    var s = d ? seasonPreface(d) : null;
    if (s) return s;
    if (d && d.getDay() === 0 && temporal) return 'SS. Trinitate';
    return 'Communis';
  }
  var BVM_WORD = [[/Annuntiat/, 'Annuntiatióne', 'Annunciation'], [/Visitat/, 'Visitatióne', 'Visitation'], [/Assumpt/, 'Assumptióne', 'Assumption'],
    [/Nativit/, 'Nativitáte', 'Nativity'], [/Pr(ae|æ)sentat/, 'Præsentatióne', 'Presentation'], [/Concept/, 'Conceptióne immaculáta', 'Immaculate Conception'],
    [/Dolor|Septem|Compassion/, 'Transfixióne', 'Transfixion'], [/Rosar/, 'Solemnitáte', 'Solemnity'], [/Sabbat|C79s/, 'Veneratióne', 'Veneration']];
  function prefaceText(name, key, d) {
    var p = PREFACES[name], la = p.la, en = p.tr, t = titleText(key) + ' ' + key;
    if (name === 'B. Maria Virgine') {
      var w = BVM_WORD.filter(function (x) { return x[0].test(t); })[0] || [null, 'Festivitáte', 'Feast'];
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
  function drawPreface(key, d, R) {
    var name = prefaceOf(key, d);
    if (!name) return null;
    var P = prefaceText(name, key, d), solemn = R.gloria && !R.requiem;
    var dialogue = null;
    D.kyriale.forEach(function (id) { if (D.chants[id].i === (solemn ? 'Ad Praefationem in tono solemni' : 'Ad Praefationem in tono feriali')) dialogue = id; });
    var box = el('section', {class: 'part preface', 'data-part': 'pf'});
    box.appendChild(el('div', {class: 'part-head'}, [el('h2', {text: 'Praefatio'}), el('span', {class: 'incipit', text: P.name}),
      el('span', {class: 'mode', text: solemn ? 'tono solemni' : 'tono feriali'})]));
    box.appendChild(el('h2', {class: 'print-only', text: 'Praefatio · ' + P.name}));
    if (dialogue) {
      var cb = el('div', {class: 'chant'});
      box.appendChild(cb);
      loadGabc(dialogue).then(function (t) { var g = splitGabc(t); renderInto(cb, g.body, g.header, null); }, function (e) { showError(cb, e); });
    }
    box.appendChild(el('div', {class: 'r-cols pf-text'}, [el('p', {class: 'la', lang: 'la', text: P.la}), el('p', {class: 'en-text', lang: 'en', text: P.tr})]));
    box.appendChild(el('p', {class: 'pf-sanctus', text: 'Sanctus, Sanctus, Sanctus…'}));
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
    var rs = seasonalReadings(state.key, state.date) || m.readings || [], pre = rs.filter(function (r) { return r.type !== 'Gospel'; }), gos = rs.filter(function (r) { return r.type === 'Gospel'; });
    var q = [], ch = function (p) { (parts[p] || []).forEach(function (c, i) { q.push({t: 'chant', p: p, i: i, c: c}); }); };
    var take = function (p, i) { var c = (parts[p] || [])[i]; if (c) q.push({t: 'chant', p: p, i: i, c: c}); };
    ch('pr'); ch('in');
    if (!m.prophecies) { q.push({t: 'ord', k: 'ky'}); q.push({t: 'ord', k: 'gl'}); }
    var gr = (parts.gr || []).length, tr = (parts.tr || []).length;
    if (m.prophecies) {
      // Holy Saturday, Vigil of Pentecost: prophecies, the last ones each followed by a tract; the Litany;
      // then the Mass begins with the Kyrie and Gloria
      var ptr = m.ptr != null ? m.ptr : tr, k = 0;
      pre.forEach(function (r, i) {
        if (i === m.prophecies) { q.push({t: 'ord', k: 'ky'}); q.push({t: 'ord', k: 'gl'}); }
        q.push({t: 'read', r: r});
        if (i < m.prophecies && i >= m.prophecies - ptr) take('tr', k++);
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
        if (last) {
          for (; gi < gr; gi++) take('gr', gi);
          for (; ai < al; ai++) take('al', ai);
          ch('tr');
        }
      });
      if (!pre.length) { ch('gr'); ch('al'); ch('tr'); }
    }
    ch('se');
    gos.forEach(function (r) { q.push({t: 'read', r: r}); });
    ch('ad');
    q.push({t: 'ord', k: 'cr'}); ch('of'); q.push({t: 'pref'}); q.push({t: 'ord', k: 'sa'});
    if (!m.noAgnus) q.push({t: 'ord', k: 'ag'});
    ch('co'); ch('an'); q.push({t: 'ord', k: 'it'});
    return q;
  }
  function rubricLine(R) {
    var pn = prefaceOf(state.key, state.date), P = pn ? PREFACES[pn] : null, num = state.ord && state.ord !== 'none' ? state.ord : autoKyriale(state.key, state.date);
    if (state.key === 'Quad6f') return 'Lessons and Tracts · the Passion · the Solemn Prayers · the Adoration of the Cross · the Mass of the Presanctified';
    if (R.requiem) return 'Mass for the Dead · without Gloria or Credo · Sequence Dies iræ · Preface for the Dead · Requiescant in pace';
    return (state.ord === 'none' ? '' : 'Kyriale: Missa ' + num + ' · ') + (R.gloria ? 'Gloria' : 'no Gloria') + ' · ' + (R.credo ? 'Credo' : 'no Credo') +
      (P ? ' · ' + P.en : '') + ' · ' + (R.dismiss === 'ite' ? 'Ite, missa est' : 'Benedicamus Domino');
  }

  function drawMass() {
    var m = D.masses[state.key], main = $('#mass');
    main.innerHTML = '';
    var latin = clean(m.title).replace(/^\d+ [A-Za-z.]+ — /, '');
    var english = m.name_en || (isTemporal(state.key) ? clean(m.en || '') : '');
    main.appendChild(el('header', {class: 'mass-head'}, [
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
    main.appendChild(el('p', {class: 'rubric-line', text: rubricLine(R)}));
    main.appendChild(el('h2', {class: 'caps-head', id: 'chants', text: 'Proprium Missae'}));
    if (ord.as) main.appendChild(drawOrdinary('as', ord.as));
    var readHead = false;
    massSequence(m, state.parts).forEach(function (it) {
      if (it.t === 'chant') main.appendChild(drawSlot(it.p, it.i, it.c));
      else if (it.t === 'pref') { var pf = drawPreface(state.key, state.date, R); if (pf) main.appendChild(pf); }
      else if (it.t === 'ord') { if (ord[it.k]) main.appendChild(drawOrdinary(it.k, ord[it.k])); }
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
      shared: 'Chants re-used from elsewhere in the Graduale', manual: 'Dominican Mass, checked against the Missale O.P.'}[m.conf];
    main.appendChild(el('p', {class: 'source hide-print'}, [
      'Graduale O.P. (1950)' + (m.page ? ', p. ' + m.page : '') + (src ? ' · ' + src : '') + '. ',
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

  function drawOrdinary(k, id) {
    var slot = el('section', {class: 'part', 'data-part': k, id: k === 'ky' || k === 'as' ? 'ordinary' : null});
    var box = el('div', {class: 'chant'});
    slot.appendChild(el('div', {class: 'part-head hide-print'}, [el('h2', {text: ORD_LABEL[k]}), el('span', {class: 'incipit', text: D.chants[id] ? clean(D.chants[id].i) : ''})]));
    slot.appendChild(el('h2', {class: 'print-only', text: ORD_LABEL[k] + (D.chants[id] ? ' · ' + clean(D.chants[id].i).replace(/^(Kyrie|Gloria|Credo|Sanctus|Agnus|Ite|Benedicamus)\s*/, '') : '')}));
    slot.appendChild(box);
    box.appendChild(el('p', {class: 'loading', text: 'Loading…'}));
    loadGabc(id).then(function (t) { var g = splitGabc(t); renderInto(box, g.body, g.header, null); }, function (e) { showError(box, e); });
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
  var READ_LA = {Lesson: 'Lectio', Epistle: 'Epistola', Gospel: 'Evangelium'};
  function drawReading(r) {
    var la = el('p', {class: 'la'}), en = el('p', {class: 'en-text'});
    var box = el('section', {class: 'reading', 'data-part': 'reading'}, [
      el('h3', null, [READ_LA[r.type], el('span', {class: 'ref', text: r.ref}), r.roman ? el('span', {class: 'badge warn', title: 'Reference from the Roman Missal (jgabc); not read from the Dominican Missal', text: 'Roman ref.'}) : null]),
      el('div', {class: 'r-cols'}, [la, en])]);
    readingText('la', r.ref).then(function (t) { la.textContent = t; }, function () { la.textContent = ''; });
    readingText('en', r.ref).then(function (t) { en.textContent = t; }, function () { en.textContent = ''; });
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
    var head = el('div', {class: 'part-head hide-print'}, [el('h2', {text: PART_NAME[part]}), state.edit ? sel : incipit, mode]);
    if (c.roman) head.appendChild(el('span', {class: 'badge warn', title: 'Not in the Graduale O.P. on GregoBase: the melody of the Roman Graduale', text: 'Roman melody'}));
    if (state.edit) { head.appendChild(toggle); head.appendChild(remove); }
    slot.appendChild(head);
    slot.appendChild(el('h2', {class: 'print-only', text: PART_NAME[part]}));
    slot.appendChild(chantBox);
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
      renderInto(chantBox, editor.value, h, part);
      var timer;
      editor.addEventListener('input', function () {
        state.edited[part + index] = editor.value;
        clearTimeout(timer);
        timer = setTimeout(function () { renderInto(chantBox, editor.value, h, part); }, 400);
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
      if (n === 1 || fromE < 63) keys.push('Pent1');
      else keys.push(weeksLeft === 0 ? 'Pent23' : 'Pent' + Math.min(n, 23));
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
      s.items.forEach(function (k) { var m = D.masses[k]; if (m.month === d.getMonth() && m.day === d.getDate()) feasts.push(k); });
    });
    var beati = (D.sections.filter(function (s) { return s.id === 'beati'; })[0] || {items: []}).items
      .filter(function (k) { var m = D.masses[k]; return m.month === d.getMonth() && m.day === d.getDate(); });
    var tk = temp[0], tc = tk ? temporalClass(tk, d) : 9;
    feasts.sort(function (a, b) { return feastClass(a) - feastClass(b); });
    var fk = feasts[0], fc = fk ? feastClass(fk) : 9;
    // the higher class wins; at equal class a Sunday or privileged feria wins, otherwise the feast
    var lentFeria = tk && /^(5a|Quad)/.test(tk) && d.getDay() !== 0;
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
      return el('button', {type: 'button', class: 'chip' + (k === r.win ? ' win' : ''), onclick: function () { showMass(k); markChips(k); }},
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
    Array.prototype.forEach.call(document.querySelectorAll('#dateResults .chip'), function (b) { b.classList.remove('win'); });
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
  function paschal() { return currentSeason() === 'pasch' || /^(Pasc|Asc|AscVig|Litaniis|Pent0)/.test(state.key || ''); }
  function trimTPText(t) {
    if (paschal()) return t;
    return t.replace(/\s*T\.\s?P\.\s*Alleluia,?\s*alleluia!?/g, '').replace(/,?\s*alleluia[!.]?\s*(?=(℣\.|Glory be|$))/gi, '. ').replace(/\.\s*\./g, '.').trim();
  }
  function chantLatin(id) {
    return loadGabc(id).then(function (t) {
      var b = splitGabc(t).body;
      if (!paschal()) b = stripTP(b);
      return gabcText(b);
    }, function () { return ''; });
  }
  var PART_EN_FULL = {in: 'Introit', gr: 'Gradual', al: 'Alleluia', tr: 'Tract', se: 'Sequence', of: 'Offertory', co: 'Communion', an: 'Vespers antiphon', pr: 'Before Mass', ad: 'Adoration of the Cross'};
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
      if (tr) o.en.textContent = trimTPText(tr.t);
      else o.en.appendChild(el('span', {class: 'c-missing', text: '(No English translation of this chant is available yet.)'}));
      jobs.push(chantLatin(c.id).then(function (t) { o.la.textContent = t; }));
    };
    var readSec = function (r) {
      var o = sec(READ_LA[r.type], READ_EN[r.type], r.ref, true);
      jobs.push(readingText('la', r.ref).then(function (t) { o.la.textContent = t; }, function () {}));
      jobs.push(readingText('en', r.ref).then(function (t) { o.en.textContent = t; }, function () {}));
    };
    var R = rubricsOf(state.key, state.date);
    box.appendChild(el('p', {class: 'c-rubric', text: rubricLine(R)}));
    massSequence(m, state.parts).forEach(function (it) {
      if (it.t === 'chant') { if (it.c.id) chantSec(it.p, it.c); }
      else if (it.t === 'read') readSec(it.r);
      else if (it.t === 'pref') {
        var pn = prefaceOf(state.key, state.date);
        if (pn) { var P = prefaceText(pn, state.key, state.date), o = sec('Praefatio', P.en, ''); o.la.textContent = P.la; o.en.textContent = P.tr; }
      }
    });
    box.appendChild(el('footer', {class: 'c-foot', text: 'Chants: Graduale O.P. (1950). Readings: Vulgate and Douay-Rheims. English of the chants: St. Dominic Missal (1959).'}));
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
  window.ProprOP = {prefaceOf: prefaceOf, autoKyriale: autoKyriale, ordinaryIds: ordinaryIds, rubricsOf: rubricsOf, massSequence: massSequence, buildCongregation: buildCongregation, printAs: printAs, gabcText: gabcText, renderInto: renderInto, loadGabc: loadGabc, splitGabc: splitGabc, temporaleKey: temporaleKey, showMass: showMass, massesOf: massesOf, massColor: massColor, massParts: massParts};

  function start() {
    fillMassSelect();
    fillOrdinarySelects();
    $('#selMass').addEventListener('change', function (e) { if (e.target.value) showMass(e.target.value); });
    $('#date').addEventListener('change', function (e) { if (e.target.value) onDate(fromIso(e.target.value)); });
    $('#prevDay').addEventListener('click', function () { shiftDay(-1); });
    $('#nextDay').addEventListener('click', function () { shiftDay(1); });
    $('#navToday').addEventListener('click', function () { onDate(new Date()); });
    $('#navCalendar').addEventListener('click', function () { var i = $('#date'); i.focus(); if (i.showPicker) try { i.showPicker(); } catch (e) {} });
    $('#navMasses').addEventListener('click', function () { var s = $('#selMass'); s.focus(); if (s.showPicker) try { s.showPicker(); } catch (e) {} });
    $('#selSeason').addEventListener('change', function (e) { state.season = e.target.value; showMass(state.key); });
    $('#selOrd').addEventListener('change', function (e) { state.ord = e.target.value; drawMass(); writeHash(); });
    $('#selCredo').addEventListener('change', function (e) { state.credo = e.target.value; drawMass(); writeHash(); });
    $('#selAsp').addEventListener('change', function (e) { state.asp = e.target.value; drawMass(); writeHash(); });
    $('#btnChoir').addEventListener('click', function () { printAs('choir'); });
    $('#btnCong').addEventListener('click', function () { printAs('congregation'); });
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
    var h = readHash();
    if (h && D.masses[h.key]) {
      var o = h.opts;
      state.season = o.season || 'auto'; state.ord = o.ord || ''; state.credo = o.credo || ''; state.asp = o.asp || '';
      $('#selSeason').value = state.season; $('#selOrd').value = state.ord; $('#selCredo').value = state.credo; $('#selAsp').value = state.asp;
      state.key = h.key;
      onDate(o.d ? fromIso(o.d) : new Date(), true);
      showMass(h.key, h.over);
    } else onDate(new Date());
  }
  // the chant is measured with the page's fonts, so wait for them
  var fonts = ['16px "Crimson Text"', 'italic 16px "Crimson Text"', 'bold 16px "Crimson Text"', '16px Versiculum'];
  Promise.all(fonts.map(function (f) { return document.fonts ? document.fonts.load(f) : null; })).then(start, start);
})();
