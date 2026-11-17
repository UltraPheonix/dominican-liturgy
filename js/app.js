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
  var state = {key: null, parts: null, edited: {}};

  function readHash() {
    var h = decodeURIComponent(location.hash.slice(1));
    if (!h) return null;
    var bits = h.split('&'), out = {key: bits.shift(), over: {}};
    bits.forEach(function (b) {
      var kv = b.split('=');
      if (PARTS.indexOf(kv[0]) >= 0) out.over[kv[0]] = kv[1] ? kv[1].split(',').map(Number) : [];
    });
    return out;
  }
  function writeHash() {
    if (!state.key) return;
    var m = D.masses[state.key], bits = [state.key];
    PARTS.forEach(function (p) {
      var def = (m.parts[p] || []).map(function (c) { return c.id; }).join(',');
      var cur = (state.parts[p] || []).map(function (c) { return c.id; }).join(',');
      if (def !== cur) bits.push(p + '=' + cur);
    });
    history.replaceState(null, '', '#' + bits.join('&'));
  }

  // ---------------------------------------------------------------- chant files
  var gabcCache = {};
  function loadGabc(id) {
    if (!gabcCache[id]) {
      gabcCache[id] = fetch('gabc/' + id + '.gabc').then(function (r) {
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
  function exsurgeGabc(gabc) {
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
    sel.appendChild(el('option', {value: '', text: 'Choose a Mass…'}));
    D.sections.forEach(function (s) {
      var og = el('optgroup', {label: s.title + ' — ' + s.en});
      s.items.forEach(function (k) {
        var m = D.masses[k];
        var label = m.title + (m.en && m.en !== m.title && !/^[A-Z][a-z]{2} \d/.test(m.en) ? ' · ' + m.en : '');
        og.appendChild(el('option', {value: k, text: clean(label)}));
      });
      sel.appendChild(og);
    });
  }

  function chantOptions(part, current) {
    var sel = el('select', {class: 'chant-select', 'aria-label': PART_EN[part] + ' chant'});
    var ids = Object.keys(D.chants).filter(function (id) { return D.chants[id].p === part; });
    sel.appendChild(el('option', {value: '', text: '(none)'}));
    var og = el('optgroup', {label: 'All ' + PART_NAME[part] + ' chants in the Graduale O.P.'});
    ids.sort(function (a, b) { return D.chants[a].i.localeCompare(D.chants[b].i); }).forEach(function (id) {
      og.appendChild(el('option', {value: id, text: clean(D.chants[id].i) + ' — p. ' + D.chants[id].pg, selected: String(current) === id ? 'selected' : null}));
    });
    sel.appendChild(og);
    return sel;
  }

  // ---------------------------------------------------------------- page
  function showMass(key, over) {
    var m = D.masses[key];
    if (!m) return;
    state.key = key;
    state.edited = {};
    state.parts = {};
    PARTS.forEach(function (p) {
      state.parts[p] = (over && over[p]) ? over[p].map(function (id) { return {id: id, chosen: true}; })
                                         : (m.parts[p] || []).slice();
    });
    $('#selMass').value = key;
    drawMass();
    writeHash();
    document.title = clean(m.title) + ' — Propria Missae O.P.';
  }

  function drawMass() {
    var m = D.masses[state.key], main = $('#mass');
    main.innerHTML = '';
    var badge = CONF[m.conf];
    main.appendChild(el('header', {class: 'mass-head'}, [
      el('h1', {text: clean(m.title).replace(/^\d+ \S+ — /, '')}),
      el('p', {class: 'en'}, [
        m.en ? clean(m.en) : '',
        m.rank ? el('span', {class: 'rank', text: ' · ' + m.rank + ' cl.'}) : null,
        m.page ? el('span', {class: 'pg', text: ' · Graduale O.P. p. ' + m.page}) : null,
        badge ? el('span', {class: 'badge ' + badge.cls, text: badge.text}) : null
      ]),
      m.note ? el('p', {class: 'note hide-print', text: m.note}) : null
    ]));
    PARTS.forEach(function (p) {
      (state.parts[p] || []).forEach(function (c, i) { main.appendChild(drawSlot(p, i, c)); });
    });
    // add a part / other chants printed with this Mass
    var add = el('section', {class: 'add hide-print'});
    var partSel = el('select', {'aria-label': 'Part to add'});
    PARTS.forEach(function (p) { partSel.appendChild(el('option', {value: p, text: PART_EN[p]})); });
    add.appendChild(el('div', {class: 'row'}, [
      el('span', {text: 'Add a chant: '}), partSel,
      el('button', {type: 'button', text: 'Add', onclick: function () {
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
          p ? el('button', {type: 'button', class: 'link', text: 'add', onclick: function () {
            state.parts[p].push({id: id, chosen: true}); drawMass(); writeHash();
          }}) : el('button', {type: 'button', class: 'link', text: 'show', onclick: function (ev) {
            var box = el('div', {class: 'chant extra-render'});
            ev.target.parentNode.appendChild(box);
            ev.target.remove();
            loadGabc(id).then(function (t) { var g = splitGabc(t); renderInto(box, g.body, g.header, null); });
          }})
        ]));
      });
      add.appendChild(el('details', null, [el('summary', {text: 'Other chants printed on these pages of the Graduale (' + m.extras.length + ')'}), list]));
    }
    main.appendChild(add);
  }

  function drawSlot(part, index, c) {
    var slot = el('section', {class: 'part', 'data-part': part});
    var sel = chantOptions(part, c.id);
    var chantBox = el('div', {class: 'chant', 'aria-live': 'polite'});
    var editor = el('textarea', {class: 'gabc hide-print', spellcheck: 'false', rows: '6', hidden: 'hidden', 'aria-label': 'GABC of this chant'});
    var info = el('span', {class: 'src'});
    var toggle = el('button', {type: 'button', class: 'link', text: 'Edit GABC', onclick: function () {
      editor.hidden = !editor.hidden; toggle.textContent = editor.hidden ? 'Edit GABC' : 'Hide GABC';
    }});
    var remove = el('button', {type: 'button', class: 'link', text: 'Remove', onclick: function () {
      state.parts[part].splice(index, 1); drawMass(); writeHash();
    }});
    slot.appendChild(el('div', {class: 'part-head hide-print'}, [
      el('h2', {text: PART_NAME[part]}), sel,
      c.inferred ? el('span', {class: 'badge info', title: 'Not printed with this Mass; the Graduale uses it again from p. ' + (D.chants[c.id] || {}).pg, text: 're-used'}) : null,
      toggle, remove
    ]));
    slot.appendChild(el('h2', {class: 'print-only', text: PART_NAME[part]}));
    slot.appendChild(chantBox);
    slot.appendChild(editor);
    slot.appendChild(el('p', {class: 'meta hide-print'}, [info]));
    sel.addEventListener('change', function () {
      state.parts[part][index] = {id: sel.value ? Number(sel.value) : null, chosen: true};
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

  function onDate(value) {
    var box = $('#dateResults');
    box.innerHTML = '';
    if (!value) return;
    var parts = value.split('-').map(Number), d = new Date(parts[0], parts[1] - 1, parts[2]);
    var keys = temporaleKey(d).filter(function (k) { return D.masses[k]; });
    var seen = {};
    keys = keys.filter(function (k) { if (seen[k]) return false; seen[k] = 1; return true; });
    var feasts = [];
    D.sections.forEach(function (s) {
      if (s.id !== 'sanctorum' && s.id !== 'beati') return;
      s.items.forEach(function (k) { var m = D.masses[k]; if (m.month === d.getMonth() && m.day === d.getDate()) feasts.push(k); });
    });
    var mk = function (k, label) {
      return el('button', {type: 'button', class: 'chip', onclick: function () { showMass(k); }}, [el('small', {text: label}), clean(D.masses[k].title)]);
    };
    keys.forEach(function (k, i) { box.appendChild(mk(k, i ? 'or' : 'Temporale')); });
    feasts.forEach(function (k) { box.appendChild(mk(k, D.masses[k].rank ? D.masses[k].rank + ' cl.' : 'Feast')); });
    if (!keys.length && !feasts.length) box.appendChild(el('span', {class: 'empty', text: 'Nothing found for this date.'}));
    box.appendChild(el('p', {class: 'note', text: 'Precedence between a Sunday or feria and a feast is not worked out here: follow the Ordo.'}));
    var first = feasts.filter(function (k) { return /^I+$/.test(D.masses[k].rank) && D.masses[k].rank.length <= 2; })[0] || keys[0] || feasts[0];
    if (first) showMass(first);
  }

  // exposed for testing and for the browser console
  window.ProprOP = {renderInto: renderInto, loadGabc: loadGabc, splitGabc: splitGabc, temporaleKey: temporaleKey, showMass: showMass};

  // ---------------------------------------------------------------- start
  function start() {
    fillMassSelect();
    $('#selMass').addEventListener('change', function (e) { if (e.target.value) showMass(e.target.value); });
    $('#date').addEventListener('change', function (e) { onDate(e.target.value); });
    $('#btnToday').addEventListener('click', function () {
      var t = new Date(), v = t.getFullYear() + '-' + String(t.getMonth() + 1).padStart(2, '0') + '-' + String(t.getDate()).padStart(2, '0');
      $('#date').value = v; onDate(v);
    });
    $('#btnNextSunday').addEventListener('click', function () {
      var t = new Date(); t = addDays(t, (7 - t.getDay()) % 7 || 7);
      var v = t.getFullYear() + '-' + String(t.getMonth() + 1).padStart(2, '0') + '-' + String(t.getDate()).padStart(2, '0');
      $('#date').value = v; onDate(v);
    });
    $('#btnPrint').addEventListener('click', function () { window.print(); });
    $('#btnShare').addEventListener('click', function () {
      var url = location.href;
      if (navigator.share) navigator.share({title: document.title, url: url}).catch(function () {});
      else if (navigator.clipboard) navigator.clipboard.writeText(url).then(function () { $('#btnShare').textContent = 'Link copied'; setTimeout(function () { $('#btnShare').textContent = 'Share'; }, 1500); });
    });
    var resizeTimer, lastW = window.innerWidth;
    window.addEventListener('resize', function () {
      if (Math.abs(window.innerWidth - lastW) < 40) return;
      lastW = window.innerWidth;
      clearTimeout(resizeTimer); resizeTimer = setTimeout(function () { if (state.key) drawMass(); }, 300);
    });
    window.addEventListener('hashchange', function () {
      var h = readHash(); if (h && h.key !== state.key && D.masses[h.key]) showMass(h.key, h.over);
    });
    var h = readHash();
    if (h && D.masses[h.key]) showMass(h.key, h.over);
    else $('#btnNextSunday').click();
  }
  // the chant is measured with the page's fonts, so wait for them
  var fonts = ['16px "Crimson Text"', 'italic 16px "Crimson Text"', 'bold 16px "Crimson Text"', '16px Versiculum'];
  Promise.all(fonts.map(function (f) { return document.fonts ? document.fonts.load(f) : null; })).then(start, start);
})();
