/* The Divine Office of the Dominican Rite (Breviarium S.O.P., 1962).
   The text of each day is generated ahead of time from Divinum Officium's
   "Ordo Praedicatorum - 1962" data (MIT licence) and checked against the
   1962 Breviary; this file only fetches and displays it. */
(function () {
  'use strict';
  var BASE = 'data/office/';
  var HOURS = [
    ['Matutinum', 'Ad Matutinum', 'Matins'], ['Laudes', 'Ad Laudes', 'Lauds'], ['Prima', 'Ad Primam', 'Prime'],
    ['Tertia', 'Ad Tertiam', 'Terce'], ['Sexta', 'Ad Sextam', 'Sext'], ['Nona', 'Ad Nonam', 'None'],
    ['Vespera', 'Ad Vesperas', 'Vespers'], ['Completorium', 'Ad Completorium', 'Compline']
  ];
  var $ = function (s) { return document.querySelector(s); };
  var cache = {}, common = null, shards = {}, range = null;
  var state = {date: null, hour: null, lang: 'both', priest: false, chant: false};
  var chantMap = null;

  try {
    state.lang = localStorage.getItem('officeLang') || 'both';
    state.priest = localStorage.getItem('officePriest') === '1';
    state.chant = localStorage.getItem('officeChant') === '1';
  } catch (e) {}

  function pad(n) { return (n < 10 ? '0' : '') + n; }
  var WD = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], MO = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  function shortDate(d) {
    var t = new Date(); t.setHours(0, 0, 0, 0);
    return WD[d.getDay()] + ' ' + d.getDate() + ' ' + MO[d.getMonth()] + ' ' + d.getFullYear() + (+d === +t ? ' · Today' : '');
  }
  function iso(d) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
  function parseIso(s) { var m = /^(\d{4})-(\d\d)-(\d\d)$/.exec(s || ''); return m ? new Date(+m[1], +m[2] - 1, +m[3]) : null; }
  function addDays(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function getJSON(url) {
    if (!cache[url]) {
      cache[url] = fetch(url).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
      cache[url].catch(function () { delete cache[url]; });
    }
    return cache[url];
  }

  // a sensible default hour for the time of day
  function hourNow() {
    var h = new Date().getHours();
    return h < 5 ? 'Matutinum' : h < 8 ? 'Laudes' : h < 9 ? 'Prima' : h < 11 ? 'Tertia' : h < 14 ? 'Sexta'
      : h < 16 ? 'Nona' : h < 20 ? 'Vespera' : 'Completorium';
  }

  // ---------- markup ----------
  var TAGS = {r: '<span class="r">', c: '<span class="r ini">', n: '<span class="r vn">', k: '<span class="k">', h: '<span class="r">'};
  function fmt(line) {
    var s = esc(line).replace(/&lt;(\/?)([rcnkh])&gt;/g, function (m, close, t) { return close ? '</span>' : TAGS[t]; });
    return s.replace(/([✠✙])/g, '<span class="r">$1</span>').replace(/ \* /g, ' <span class="r">*</span> ')
      .replace(/ † /g, ' <span class="r">†</span> ').replace(/ \+ /g, ' <span class="r">✠</span> ');
  }
  function blockText(id, day) { return (day.b && day.b[id]) || (common && common[id]) || ''; }
  function expand(text) {
    return text.split('\n').map(function (l) {
      if (l.charAt(0) !== '§') return l;
      var k = l.slice(1), sh = shards[k.slice(0, 2)] || {};
      return sh[k] || '';
    }).join('\n').split('\n');
  }
  // the hour's rows, said with or without a priest
  function rowsOf(day, hour) {
    var rows = day.h[hour] || [], p = state.priest && day.p && day.p[hour];
    if (!p) return rows;
    if (p.all) return p.all;
    return rows.map(function (row, i) { return p.i[i] || row; });
  }
  function neededShards(day) {
    var need = {};
    Object.keys(day.h).forEach(function (h) {
      rowsOf(day, h).forEach(function (row) {
        row.forEach(function (id) {
          blockText(id, day).replace(/^§(\d\d)\./gm, function (m, s) { need[s] = 1; return m; });
        });
      });
    });
    return Object.keys(need);
  }

  // a cell: its heading (the first <h> line) and its body lines
  function cell(id, day) {
    var lines = id ? expand(blockText(id, day)) : [], head = '';
    if (lines.length && /^<h>/.test(lines[0])) head = lines.shift().replace(/<\/?h>/g, '').trim();
    while (lines.length && !lines[0].trim()) lines.shift();
    return {head: head, lines: lines};
  }

  function lineClass(l) {
    if (/^<n>\d+:\d+/.test(l)) return 'o-l vs';
    if (/^<r>[^<]*<\/r>$/.test(l)) return 'o-l rub';
    return 'o-l';
  }
  function drawLine(l) {
    if (!l.trim()) return '<div class="o-gap"></div>';
    return '<div class="' + lineClass(l) + '">' + fmt(l) + '</div>';
  }

  // ---------- chant ----------
  function plain(l) { return l.replace(/<[^>]+>/g, ''); }
  // the chantable pieces of a Latin cell: antiphons, the hymn, the short responsory (as build/gb/build_chant.py)
  function chantSegs(lines, head) {
    var segs = [], K = window.OPChant ? OPChant.key : null;
    if (!K || !chantMap) return segs;
    var hymnAt = -1;
    for (var i = 0; i < lines.length; i++) {
      var l = lines[i];
      if (/^<r>Ant\.<\/r>/.test(l)) segs.push({s: i, e: i + 1, kind: 'an', key: K(plain(l).slice(4))});
      else if (/^<[rh]>Hymnus<\/[rh]>$/.test(l.trim())) hymnAt = i + 1;
      else if (/^<r>℟\.br\.<\/r>/.test(l)) {
        var e = i + 1;
        while (e < lines.length && lines[e].trim()) e++;
        segs.push({s: i, e: e, kind: 'rb', key: 'rb' + K(plain(l).slice(5))});
        i = e - 1;
      }
      if (hymnAt < 0 && i === 0 && /Hymnus$/.test(head || '')) hymnAt = 0;
      if (hymnAt >= 0 && i >= hymnAt - 1) {
        var j = hymnAt;
        while (j < lines.length && !lines[j].trim()) j++;
        if (j < lines.length) {
          var end = j, hk = 'hy' + K(plain(lines[j])), whole = chantMap[hk] && chantMap[hk][3];
          if (whole) {
            while (end < lines.length && !/^Amen\.?$/.test(plain(lines[end]).trim()) && !/^<r>℣\.<\/r>/.test(lines[end])) end++;
            if (end < lines.length && /^Amen/.test(plain(lines[end]).trim())) end++;
          } else {
            // only the first stanza is notated: the others are sung to it and stay as text
            while (end < lines.length && lines[end].trim()) end++;
          }
          segs.push({s: j, e: end, kind: 'hy', key: hk});
          i = end - 1;
        }
        hymnAt = -1;
      }
    }
    return segs.filter(function (g) { return chantMap[g.key]; });
  }
  var LABEL = {an: 'Ant.', hy: 'Hymn.', rb: 'R. br.'};
  function chantDiv(g) {
    var m = chantMap[g.key];
    return '<div class="chant o-chant" data-id="' + esc(m[0]) + '" data-mode="' + esc(m[1]) + '" data-tp="' + m[2] + '" data-kind="' + g.kind + '"></div>';
  }
  function drawChants(main) {
    Array.prototype.forEach.call(main.querySelectorAll('.o-chant[data-id]'), function (box) {
      getText('data/chant/op/' + box.getAttribute('data-id') + '.gabc').then(function (g) {
        var kind = box.getAttribute('data-kind'), tp = box.getAttribute('data-tp') === '1';
        OPChant.render(box, g, {mode: box.getAttribute('data-mode'), label: LABEL[kind], keepTP: tp, dropCap: kind !== 'rb'});
      }).catch(function () { box.textContent = ''; });
    });
  }
  // psalms: the tone of the antiphon, its first verse notated, the others pointed
  function drawPsalms(main) {
    if (!window.OPPsalm) return;
    var groups = {};
    Array.prototype.forEach.call(main.querySelectorAll('.o-pv[data-ps]'), function (el) {
      (groups[el.getAttribute('data-ps')] = groups[el.getAttribute('data-ps')] || []).push(el);
    });
    Object.keys(groups).forEach(function (k) {
      var m = chantMap[k];
      if (!m) return;
      getText('data/chant/op/' + m[0] + '.gabc').then(function (g) {
        var mode = parseInt(m[1], 10);
        if (!(mode >= 1 && mode <= 8)) return;
        var tone = OPPsalm.toneOf(mode, OPPsalm.chooseDiff(mode, g));
        if (!tone) return;
        groups[k].forEach(function (el) {
          var cant = el.getAttribute('data-cant') === '1', first = el.getAttribute('data-first') === '1';
          var pv = OPPsalm.pointVerse(el.getAttribute('data-t'), tone, {inton: first || cant});
          var num = el.getAttribute('data-num') || '';
          if (first) {
            var row = el.classList.contains('o-la') ? el.parentNode : el;
            var lab = document.createElement('div');
            lab.className = 'o-tone';
            lab.textContent = 'Tonus ' + tone.name.replace('IVA', 'IV') + (tone.diff ? ' ' + tone.diff : '');
            var box = document.createElement('div');
            box.className = 'chant o-chant';
            row.parentNode.insertBefore(lab, row);
            row.parentNode.insertBefore(box, row);
            OPChant.render(box, OPPsalm.verseGabc(pv, tone), {dropCap: false, keepTP: true});
          }
          // the first verse is read from the notes above; the others are pointed
          el.innerHTML = first ? num : (num ? num + ' ' : '') + OPPsalm.verseHtml(pv, esc);
          el.classList.add('o-pointed');
        });
      }).catch(function () {});
    });
  }
  var textCache = {};
  function getText(url) {
    if (!textCache[url]) {
      textCache[url] = fetch(url).then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); });
      textCache[url].catch(function () { delete textCache[url]; });
    }
    return textCache[url];
  }

  // a psalm or canticle verse (or its doxology)
  function isVerse(l) { return /^<n>\d+:\d+[a-z]?<\/n>/.test(l) || /^<r>[℣℟]\.<\/r>\s*(Glória Patri|Sicut erat)/.test(l); }
  function verseAttrs(l, ps, la) {
    var t = plain(l.replace(/^<n>[^<]*<\/n>\s*/, '').replace(/^<r>[℣℟]\.<\/r>\s*/, '')).trim();
    var num = (/^(<n>[^<]*<\/n>|<r>[℣℟]\.<\/r>)\s*/.exec(l) || ['', ''])[1];
    var a = ' data-ps="' + esc(ps.ant) + '" data-t="' + esc(t) + '" data-num="' + esc(num) + '"';
    if (ps.first) { a += ' data-first="1"'; ps.first = false; }
    if (ps.cant) a += ' data-cant="1"';
    return a;
  }

  function drawRow(row, day, ps) {
    ps = ps || {};
    var la = cell(row[0], day), en = cell(row[1], day), lang = state.lang, html = '';
    var same = en.lines.join('\n') === la.lines.join('\n');
    if (la.head || en.head) {
      html += '<h3 class="o-h">' + esc(lang === 'en' ? (en.head || la.head) : (la.head || en.head)) +
        (lang === 'both' && en.head && la.head && en.head !== la.head ? ' <span class="o-h-en">' + esc(en.head) + '</span>' : '') + '</h3>';
    }
    var segs = state.chant && lang !== 'en' ? chantSegs(la.lines, la.head) : [];
    ps.cant = /Benedictus|Magnificat/.test(la.head || '');
    var psalmCell = state.chant && lang !== 'en' && chantMap && (segs.length || ps.ant) && la.lines.some(isVerse);
    var at = {};
    segs.forEach(function (g) { at[g.s] = g; });
    var paired = lang === 'both' && !same && en.lines.length && la.lines.length === en.lines.length;
    if ((segs.length || psalmCell) && (lang === 'la' || paired || !en.lines.length || same)) {
      // chant in place of the Latin text; in "both", the English follows each chant as a translation
      var out = '';
      for (var i = 0; i < la.lines.length; i++) {
        var g = at[i];
        if (g) {
          if (g.kind === 'an') { ps.ant = g.key; ps.first = true; }
          out += chantDiv(g);
          if (paired) out += '<div class="o-tr">' + en.lines.slice(g.s, g.e).filter(function (x) { return x.trim(); }).map(fmt).join('<br>') + '</div>';
          i = g.e - 1;
          continue;
        }
        var l = la.lines[i], va = ps.ant && isVerse(l) ? verseAttrs(l, ps, la) : '';
        if (paired) {
          var e2 = en.lines[i];
          out += (!l.trim() && !e2.trim()) ? '<div class="o-gap"></div>' :
            '<div class="o-lp ' + lineClass(l) + '"><div class="o-la' + (va ? ' o-pv"' + va : '"') + '>' + fmt(l) + '</div><div class="o-en">' + fmt(e2) + '</div></div>';
        } else if (va) out += '<div class="' + lineClass(l) + ' o-pv"' + va + '>' + fmt(l) + '</div>';
        else out += drawLine(l);
      }
      html += '<div class="' + (paired ? 'o-lines' : 'o-col') + '">' + out + '</div>';
    } else if (segs.length) {
      // Latin and English of different lengths: chant in the Latin column
      var col = '';
      for (var k = 0; k < la.lines.length; k++) {
        if (at[k]) { col += chantDiv(at[k]); k = at[k].e - 1; } else col += drawLine(la.lines[k]);
      }
      html += '<div class="o-pair"><div class="o-la">' + col + '</div><div class="o-en">' + en.lines.map(drawLine).join('') + '</div></div>';
    } else if (lang === 'la' || !en.lines.length || same) {
      html += '<div class="o-col">' + la.lines.map(drawLine).join('') + '</div>';
    } else if (lang === 'en') {
      html += '<div class="o-col">' + en.lines.map(drawLine).join('') + '</div>';
    } else if (la.lines.length === en.lines.length) {
      // line by line, so that each verse sits beside its translation
      html += '<div class="o-lines">' + la.lines.map(function (l, i) {
        var e = en.lines[i];
        if (!l.trim() && !e.trim()) return '<div class="o-gap"></div>';
        return '<div class="o-lp ' + lineClass(l) + '"><div class="o-la">' + fmt(l) + '</div><div class="o-en">' + fmt(e) + '</div></div>';
      }).join('') + '</div>';
    } else {
      html += '<div class="o-pair"><div class="o-la">' + la.lines.map(drawLine).join('') +
        '</div><div class="o-en">' + en.lines.map(drawLine).join('') + '</div></div>';
    }
    return '<section class="o-sec">' + html + '</section>';
  }

  function titleOf(day, hour) {
    var t = (hour === 'Vespera' || hour === 'Completorium') && day.tv && day.tv.length ? day.tv : day.t;
    return (t && t[0]) || '';
  }

  function draw() {
    var main = $('#office'), d = state.date, key = iso(d);
    if (state.cal) state.cal.set(d);
    $('#date').value = key;
    drawHours();
    if (range && (key < range.from || key > range.to)) {
      main.innerHTML = '<p class="o-msg">The Office is ready for every day from ' + range.from + ' to ' + range.to + '. This date is outside that range for now.</p>';
      $('#dayTitle').textContent = ''; $('#dayRank').textContent = ''; $('#dayMeta').textContent = shortDate(d);
      return;
    }
    main.innerHTML = '<p class="o-msg">…</p>';
    Promise.all([getJSON(BASE + key.slice(0, 4) + '/' + key.slice(5) + '.json'), common ? null : getJSON(BASE + 'common.json'),
      state.chant && !chantMap ? getJSON('data/chant/office.json').then(function (m) { chantMap = m; }).catch(function () {}) : null])
      .then(function (r) {
        var day = r[0];
        if (r[1]) common = r[1];
        return Promise.all(neededShards(day).filter(function (s) { return !shards[s]; }).map(function (s) {
          return getJSON(BASE + 'psalter/' + s + '.json').then(function (j) { shards[s] = j; });
        })).then(function () { return day; });
      })
      .then(function (day) {
        if (iso(state.date) !== key) return;
        var hour = state.hour, h = HOURS.filter(function (x) { return x[0] === hour; })[0];
        var full = titleOf(day, hour), t = full.split(' ~ ');
        $('#dayTitle').textContent = t[0];
        $('#dayRank').textContent = t[1] || '';
        $('#dayMeta').textContent = shortDate(d);
        var rows = rowsOf(day, hour);
        main.innerHTML = '<header class="o-head"><h1>' + esc(h[1]) + '</h1><p class="o-sub">' + esc(h[2]) + '</p></header>' +
          (function () { var ps = {}; return rows.map(function (row) { return drawRow(row, day, ps); }).join(''); })() +
          '<p class="o-src">Text from Divinum Officium, <i>Ordo Praedicatorum – 1962</i> (MIT licence), following the Breviarium S.O.P. (1962). English is Divinum Officium’s; where a Dominican text has no English yet, the Latin stands alone.</p>';
        document.title = h[2] + ' — ' + t[0];
        if (state.chant) { drawChants(main); drawPsalms(main); }
      })
      .catch(function () {
        main.innerHTML = '<p class="o-msg">The Office for this day could not be loaded. If you are offline, open the day once while online to keep it.</p>';
      });
  }

  function drawHours() {
    $('#hours').innerHTML = HOURS.map(function (h) {
      var on = h[0] === state.hour;
      return '<button type="button" role="tab" data-h="' + h[0] + '" aria-selected="' + on + '" class="sbtn' + (on ? ' on' : '') + '">' + h[2] + '</button>';
    }).join('');
    var lb = $('#langs');
    if (lb) Array.prototype.forEach.call(lb.querySelectorAll('button'), function (b) {
      var on = b.getAttribute('data-l') === state.lang;
      b.classList.toggle('on', on); b.setAttribute('aria-pressed', on);
    });
    var pr = $('#priest');
    if (pr) pr.checked = state.priest;
    var ch = $('#chant');
    if (ch) ch.checked = state.chant;
  }

  function setHash() {
    var h = '#' + state.hour + '&d=' + iso(state.date);
    if (location.hash !== h) history.replaceState(null, '', h);
  }
  function go() { setHash(); draw(); window.scrollTo(0, 0); }

  function readHash() {
    var m = /^#(\w+)(?:&d=(\d{4}-\d\d-\d\d))?/.exec(location.hash);
    state.hour = m && HOURS.some(function (h) { return h[0] === m[1]; }) ? m[1] : hourNow();
    state.date = (m && parseIso(m[2])) || new Date(new Date().setHours(0, 0, 0, 0));
  }

  function start() {
    if (!$('#office')) return;
    readHash();
    $('#hours').addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      state.hour = b.getAttribute('data-h'); go();
    });
    var lb = $('#langs');
    if (lb) lb.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      state.lang = b.getAttribute('data-l');
      try { localStorage.setItem('officeLang', state.lang); } catch (er) {}
      draw();
    });
    var pr = $('#priest');
    var ch = $('#chant');
    if (ch) ch.addEventListener('change', function () {
      state.chant = this.checked;
      try { localStorage.setItem('officeChant', state.chant ? '1' : '0'); } catch (er) {}
      draw();
    });
    if (pr) pr.addEventListener('change', function () {
      state.priest = this.checked;
      try { localStorage.setItem('officePriest', state.priest ? '1' : '0'); } catch (er) {}
      draw();
    });
    if (window.matchMedia && matchMedia('(max-width: 960px)').matches) Array.prototype.forEach.call(document.querySelectorAll('.side .collapse'), function (x) { x.removeAttribute('open'); });
    if (window.OPCal && $('#cal')) state.cal = OPCal($('#cal'), {date: state.date, onPick: function (d) { state.date = d; go(); }});
    $('#prevDay').addEventListener('click', function () { state.date = addDays(state.date, -1); go(); });
    $('#nextDay').addEventListener('click', function () { state.date = addDays(state.date, 1); go(); });
    $('#date').addEventListener('change', function () { var d = parseIso(this.value); if (d) { state.date = d; go(); } });
    window.addEventListener('hashchange', function () { readHash(); draw(); });
    getJSON(BASE + 'range.json').then(function (r) { range = r; }).catch(function () {}).then(function () { setHash(); draw(); });
  }

  window.OfficeOP = {iso: iso, state: function () { return state; }, cell: cell};
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
