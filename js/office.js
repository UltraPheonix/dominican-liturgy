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
  var state = {date: null, hour: null, lang: 'both', priest: false};

  try { state.lang = localStorage.getItem('officeLang') || 'both'; state.priest = localStorage.getItem('officePriest') === '1'; } catch (e) {}

  function pad(n) { return (n < 10 ? '0' : '') + n; }
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

  function drawRow(row, day) {
    var la = cell(row[0], day), en = cell(row[1], day), lang = state.lang, html = '';
    var same = en.lines.join('\n') === la.lines.join('\n');
    if (la.head || en.head) {
      html += '<h3 class="o-h">' + esc(lang === 'en' ? (en.head || la.head) : (la.head || en.head)) +
        (lang === 'both' && en.head && la.head && en.head !== la.head ? ' <span class="o-h-en">' + esc(en.head) + '</span>' : '') + '</h3>';
    }
    if (lang === 'la' || !en.lines.length || same) {
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
    $('#date').value = key;
    drawHours();
    if (range && (key < range.from || key > range.to)) {
      main.innerHTML = '<p class="o-msg">The Office is ready for every day from ' + range.from + ' to ' + range.to + '. This date is outside that range for now.</p>';
      $('#dayTitle').textContent = ''; $('#dayMeta').textContent = d.toDateString();
      return;
    }
    main.innerHTML = '<p class="o-msg">…</p>';
    Promise.all([getJSON(BASE + key.slice(0, 4) + '/' + key.slice(5) + '.json'), common ? null : getJSON(BASE + 'common.json')])
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
        $('#dayMeta').textContent = (t[1] ? t[1] + ' · ' : '') + d.toLocaleDateString('en-GB', {weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'});
        var rows = rowsOf(day, hour);
        main.innerHTML = '<header class="o-head"><h2>' + esc(h[1]) + '</h2><p class="o-sub">' + esc(h[2]) + ' · ' + esc(t[0]) + '</p></header>' +
          rows.map(function (row) { return drawRow(row, day); }).join('') +
          '<p class="o-src">Text from Divinum Officium, <i>Ordo Praedicatorum – 1962</i> (MIT licence), following the Breviarium S.O.P. (1962). English is Divinum Officium’s; where a Dominican text has no English yet, the Latin stands alone.</p>';
        document.title = h[2] + ' — ' + t[0];
      })
      .catch(function () {
        main.innerHTML = '<p class="o-msg">The Office for this day could not be loaded. If you are offline, open the day once while online to keep it.</p>';
      });
  }

  function drawHours() {
    $('#hours').innerHTML = HOURS.map(function (h) {
      var on = h[0] === state.hour;
      return '<button type="button" role="tab" data-h="' + h[0] + '" aria-selected="' + on + '"' + (on ? ' class="on"' : '') + '>' + h[2] + '</button>';
    }).join('');
    var lb = $('#langs');
    if (lb) Array.prototype.forEach.call(lb.querySelectorAll('button'), function (b) {
      var on = b.getAttribute('data-l') === state.lang;
      b.classList.toggle('on', on); b.setAttribute('aria-pressed', on);
    });
    var pr = $('#priest');
    if (pr) pr.checked = state.priest;
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
    if (pr) pr.addEventListener('change', function () {
      state.priest = this.checked;
      try { localStorage.setItem('officePriest', state.priest ? '1' : '0'); } catch (er) {}
      draw();
    });
    $('#prevDay').addEventListener('click', function () { state.date = addDays(state.date, -1); go(); });
    $('#nextDay').addEventListener('click', function () { state.date = addDays(state.date, 1); go(); });
    $('#date').addEventListener('change', function () { var d = parseIso(this.value); if (d) { state.date = d; go(); } });
    window.addEventListener('hashchange', function () { readHash(); draw(); });
    getJSON(BASE + 'range.json').then(function (r) { range = r; }).catch(function () {}).then(function () { setHash(); draw(); });
  }

  window.OfficeOP = {iso: iso, state: function () { return state; }, cell: cell};
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
