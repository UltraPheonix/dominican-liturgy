/* Propria Missae juxta ritum Ordinis Praedicatorum
 * A Dominican version of the Propers tool of bbloomf/jgabc (public domain), rendering the chants of
 * the Graduale O.P. (1950) with exsurge.  Data: data/masses.js (see /build).
 */
(function () {
  'use strict';
  var D = window.DOMINICAN;
  var PARTS = ['in', 'gr', 'al', 'tr', 'se', 'of', 'co'];
  var PART_NAME = {in: 'Introitus', gr: 'Graduale', al: 'Alleluia', tr: 'Tractus', se: 'Sequentia', of: 'Offertorium', co: 'Communio'};
  var PART_EN = {in: 'Introit', gr: 'Gradual', al: 'Alleluia', tr: 'Tract', se: 'Sequence', of: 'Offertory', co: 'Communion'};
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
  var clean = function (s) { return String(s || '').replace(/<[^>]+>/g, ''); };

  // ---------------------------------------------------------------- state & URL
  // #<massKey>[&in=id,id&gr=id...]  (only parts the user changed are stored)
  var state = {key: null, parts: null, edited: {}, date: null, season: 'auto', ord: '', credo: '', asp: ''};

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

  var renderQueue = Promise.resolve();
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
              var svg = score.createSvgNode(ctxt);
              svg.removeAttribute('width'); svg.removeAttribute('height');
              container.innerHTML = '';
              container.appendChild(svg);
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
    return parts;
  }
  function isTemporal(key) { return D.sections[0].items.indexOf(key) >= 0; }

  // ---------------------------------------------------------------- liturgical colour and class
  var COLORS = {white: '#ffffff', red: '#b3313d', green: '#5f8f5f', violet: '#6a3d8f', rose: '#d98aa6', black: '#111111'};
  var COLOR_LA = {white: 'White', red: 'Red', green: 'Green', violet: 'Violet', rose: 'Rose', black: 'Black'};
  function massColor(key) {
    var m = D.masses[key], t = clean(m.title || '').replace(/^\d+ [A-Za-z.]+ — /, '') + ' ' + clean(m.en || '').replace(/^[A-Za-z]+ \d+ — /, '');
    if (/^(Adv3|Quad4)$/.test(key)) return 'rose';
    if (/^(Adv|7a|6a|5a|Quad|EmbWed|EmbFri|EmbSat|Litaniis|Dec24)/.test(key) && !/Quad6h|Quad5f/.test(key)) return key === 'Quad6f' ? 'black' : 'violet';
    if (/^(Pent0|Pasc6s)/.test(key)) return 'red';
    if (/^(Epi[1-6]|Pent\d)/.test(key) && !/^Pent0/.test(key)) return 'green';
    if (/Defunct|C114s|Mass for the Dead/.test(key + t)) return 'black';
    if (/Passione|Spiritu Sancto|C68s|C75s/.test(key + t)) return 'red';
    if (/\bMm?\.|Mart|Apost|Evang|Protomart|Innocent|Pretiosiss|Sanguin/.test(t) && !/Conversio|Cathedra|Ioannis Ap\. et Evang/.test(t)) return 'red';
    return 'white';
  }
  // class of a day of the Proper of the Time (rubrics of 1960)
  function temporalClass(key, d) {
    if (key === 'Epi' && d && !(d.getMonth() === 0 && d.getDate() === 6)) return 4;
    if (/^Dec25/.test(key) && d && d.getDate() !== 25) return 2;
    if (/^(Adv[1-4]|Quad[1-6]|Pasc0|Pasc1|Pent0|Dec24|Dec25|Jan1|Epi|Asc|CorpusChristi|SCJ|ChristusRex|5aw)$/.test(key)) return 1;
    if (/^Quad6|^Pasc0|^Pent0/.test(key)) return 1;
    if (d && d.getDay() === 0) return 2;
    if (/^Adv/.test(key) && d && d.getMonth() === 11 && d.getDate() >= 17) return 2;
    if (/^(Adv3[wfs]|EmbWedSept|EmbFriSept|EmbSatSept|Quad1[wfs]|Pent0)/.test(key)) return 2;
    if (/^(5a|Quad)/.test(key)) return 3;
    return 4;
  }
  function feastClass(key) { return {I: 1, II: 2, III: 3}[D.masses[key].rank] || 4; }

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

  var ORD_LABEL = {as: 'Asperges', ky: 'Kyrie', gl: 'Gloria', cr: 'Credo', sa: 'Sanctus', ag: 'Agnus Dei', it: 'Ite, missa est'};
  function ordinaryIds() {
    var o = {};
    if (state.asp) o.as = state.asp === 'vidi' ? D.front[1] : D.front[0];
    if (state.ord) {
      D.kyriale.forEach(function (id) {
        var n = D.chants[id].i, m = /^(Kyrie|Gloria|Sanctus|Agnus|Ite|Benedicamus)\s+([IVX]+)\b/.exec(n);
        if (!m || m[2] !== state.ord) return;
        var k = {Kyrie: 'ky', Gloria: 'gl', Sanctus: 'sa', Agnus: 'ag', Ite: 'it', Benedicamus: 'it'}[m[1]];
        if (!o[k] || m[1] === 'Ite') o[k] = id;
      });
    }
    if (state.credo) D.kyriale.forEach(function (id) { if (D.chants[id].i === 'Credo ' + state.credo) o.cr = id; });
    return o;
  }

  function drawMass() {
    var m = D.masses[state.key], main = $('#mass');
    main.innerHTML = '';
    var badge = CONF[m.conf];
    main.appendChild(el('header', {class: 'mass-head'}, [
      el('h1', {text: clean(m.title).replace(/^\d+ [A-Za-z.]+ — /, '')}),
      el('p', {class: 'en'}, [
        m.en ? clean(m.en) : '',
        m.page ? el('span', {text: ' · Graduale O.P. p. ' + m.page}) : null,
        badge ? el('span', {class: 'badge ' + badge.cls, text: badge.text}) : null
      ]),
      m.note ? el('p', {class: 'note hide-print', text: m.note}) : null
    ]));
    var ord = ordinaryIds();
    main.appendChild(el('h2', {class: 'caps-head', id: 'chants', text: 'Proprium Missae'}));
    var ordSlot = function (k) { if (ord[k]) main.appendChild(drawOrdinary(k, ord[k])); };
    ordSlot('as');
    PARTS.forEach(function (p) {
      if (p === 'of') {
        main.appendChild(drawReadings(m));
        ordSlot('cr');
      }
      (state.parts[p] || []).forEach(function (c, i) { main.appendChild(drawSlot(p, i, c)); });
      if (p === 'in') { ordSlot('ky'); ordSlot('gl'); }
      if (p === 'of') { ordSlot('sa'); ordSlot('ag'); }
    });
    ordSlot('it');
    if (!state.ord && !state.asp && !state.credo) {
      main.appendChild(el('p', {class: 'note hide-print', id: 'ordinary'}, ['The Ordinary (Kyrie, Gloria, Credo, Sanctus, Agnus Dei) can be added from the Kyriale menu.']));
    }
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
    slot.appendChild(el('div', {class: 'part-head'}, [el('h2', {text: ORD_LABEL[k] + (D.chants[id] ? ' · ' + clean(D.chants[id].i).replace(/^(Kyrie|Gloria|Sanctus|Agnus|Ite|Credo|Benedicamus)\s*/, '') : '')})]));
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
    var m = /^(\d)?\s*([^\d:]+?)\s+(\d+):\s*(.+)$/.exec(ref.trim());
    if (!m) return null;
    var book = m[2].trim() + (m[1] ? ' ' + m[1] : ''), ch = +m[3], out = [];
    m[4].split(';').forEach(function (seg) {
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
  function drawReadings(m) {
    var box = el('section', {class: 'readings', id: 'readings'});
    var rs = m.readings || [];
    if (!rs.length) return box;
    box.appendChild(el('h2', {class: 'caps-head', text: 'Lectiones'}));
    rs.forEach(function (r) {
      var la = el('p', {class: 'la'}), en = el('p', {class: 'en-text'});
      box.appendChild(el('div', {class: 'reading'}, [
        el('h3', null, [READ_LA[r.type], el('span', {class: 'ref', text: r.ref}), r.roman ? el('span', {class: 'badge warn', title: 'Reference from the Roman Missal (jgabc); not read from the Dominican Missal', text: 'Roman ref.'}) : null]),
        la, en]));
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
    slot.appendChild(el('div', {class: 'part-head hide-print'}, [
      el('h2', {text: PART_NAME[part]}), sel,
      c.roman ? el('span', {class: 'badge warn', title: 'Not found in the Graduale O.P. on GregoBase: the melody of the Roman Graduale is shown', text: 'Roman melody'}) : null,
      c.inferred ? el('span', {class: 'badge info', title: 'Not printed with this Mass; the Graduale uses it again from p. ' + (D.chants[c.id] || {}).pg, text: 're-used'}) : null,
      toggle, remove
    ]));
    slot.appendChild(el('h2', {class: 'print-only', text: PART_NAME[part]}));
    slot.appendChild(chantBox);
    slot.appendChild(editor);
    slot.appendChild(el('p', {class: 'meta hide-print'}, [info]));
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
    if (md >= 102 && md <= 105) return dow === 0 ? ['Nat2'] : (md === 105 ? ['Jan5a', 'Nat2'] : ['Nat2']);
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
      return ['Quad' + q + WD[dow], 'Quad' + q];
    }
    if (fromE >= 0 && fromE < 7) return ['Pasc0' + WD[dow]];
    if (fromE === 39) return ['Asc'];
    if (fromE === 48) return ['Pasc6s'];
    if (fromE >= 7 && fromE < 49) {
      var p = Math.floor(fromE / 7);
      return (fromE >= 35 && fromE <= 37) ? ['Litaniis', 'Pasc5'] : (fromE === 38 ? ['AscVig', 'Pasc5'] : ['Pasc' + p + WD[dow], 'Pasc' + p]);
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
    var win = !fk ? tk : (!tk ? fk : (fc < tc ? fk : (tc < fc ? tk : (d.getDay() === 0 || tc <= 2 || lentFeria ? tk : fk))));
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
    var so = $('#selOrd'); so.appendChild(el('option', {value: '', text: 'None'}));
    nums.forEach(function (n) { so.appendChild(el('option', {value: n, text: 'Missa ' + n})); });
    var sc = $('#selCredo'); sc.appendChild(el('option', {value: '', text: 'None'}));
    D.kyriale.forEach(function (id) { var m = /^Credo\s+([IVX]+)$/.exec(D.chants[id].i); if (m) sc.appendChild(el('option', {value: m[1], text: 'Credo ' + m[1]})); });
  }

  // exposed for testing and for the browser console
  window.ProprOP = {renderInto: renderInto, loadGabc: loadGabc, splitGabc: splitGabc, temporaleKey: temporaleKey, showMass: showMass, massesOf: massesOf, massColor: massColor, massParts: massParts};

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
    $('#btnPrint').addEventListener('click', function () { window.print(); });
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
