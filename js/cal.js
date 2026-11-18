/* A month calendar for the side column, shared by the Mass and Office pages.
   OPCal(box, {date, onPick(date), dot(date) -> CSS colour or ''}) ; returns {set(date)} */
(function () {
  'use strict';
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var DAYS = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
  function same(a, b) { return a && b && a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate(); }

  window.OPCal = function (box, opts) {
    var sel = opts.date || new Date(), view = new Date(sel.getFullYear(), sel.getMonth(), 1);

    function draw() {
      var y = view.getFullYear(), m = view.getMonth(), first = new Date(y, m, 1), today = new Date();
      var start = new Date(y, m, 1 - first.getDay());
      var h = '<div class="cal-head"><button type="button" class="cal-nav" data-m="-1" aria-label="Previous month">‹</button>' +
        '<span class="cal-title">' + MONTHS[m] + ' ' + y + '</span>' +
        '<button type="button" class="cal-nav" data-m="1" aria-label="Next month">›</button></div>' +
        '<div class="cal-grid" role="grid">' + DAYS.map(function (d) { return '<span class="cal-dow" aria-hidden="true">' + d + '</span>'; }).join('');
      for (var i = 0; i < 42; i++) {
        var d = new Date(start.getFullYear(), start.getMonth(), start.getDate() + i);
        if (i === 35 && d.getMonth() !== m) break;
        var cls = 'cal-day' + (d.getMonth() !== m ? ' out' : '') + (same(d, today) ? ' today' : '') + (same(d, sel) ? ' sel' : '');
        var dot = opts.dot ? opts.dot(d) : '';
        h += '<button type="button" class="' + cls + '" data-d="' + d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate() + '"' +
          ' aria-label="' + d.toDateString() + '"' + (same(d, sel) ? ' aria-current="date"' : '') + '>' + d.getDate() +
          (dot ? '<i class="cal-dot" style="background:' + dot + '"></i>' : '') + '</button>';
      }
      box.innerHTML = h + '</div>';
    }
    box.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      if (b.hasAttribute('data-m')) { view = new Date(view.getFullYear(), view.getMonth() + (+b.getAttribute('data-m')), 1); draw(); return; }
      var p = b.getAttribute('data-d').split('-').map(Number);
      sel = new Date(p[0], p[1] - 1, p[2]);
      view = new Date(p[0], p[1] - 1, 1);
      draw();
      if (opts.onPick) opts.onPick(sel);
    });
    draw();
    return {
      set: function (d) { sel = d; view = new Date(d.getFullYear(), d.getMonth(), 1); draw(); },
      redraw: draw
    };
  };
})();

/* Dominican numbering of the Sundays: after the Octave of Trinity, of the Epiphany and of Easter
   (Missale O.P. 1939: Dominica II post Octavam Trinitatis = the Roman 4th after Pentecost, etc.) */
(function () {
  'use strict';
  var R = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI', 'XXII', 'XXIII', 'XXIV', 'XXV', 'XXVI'];
  function num(s) { if (/^\d+$/.test(s)) return +s; var i = R.indexOf(s.toUpperCase()); return i > 0 ? i : 0; }
  function ord(n) { var s = ['th', 'st', 'nd', 'rd'], v = n % 100; return n + (s[(v - 20) % 10] || s[v] || s[0]); }
  var SEASON = {pentecosten: [2, 'post Octavam Trinitatis'], epiphaniam: [1, 'post Octavam Epiphaniæ'], pascha: [1, 'post Octavam Paschæ']};
  function la(t) {
    if (!t) return t;
    return String(t)
      .replace(/(Dominica\s+)?([IVXL]+|\d+)(\s+et\s+[Uu]ltima)?\s+[Pp]ost\s+(Pentecosten|Epiphaniam|Pascha)\b/g, function (m, dom, n, ult, s) {
        var S = SEASON[s.toLowerCase()], k = num(n) - S[0];
        if (ult && S[0] === 2) return (dom || '') + 'ultima ' + S[1];
        if (s.toLowerCase() === 'pentecosten' && k === 0) return 'Dominica infra Octavam Corporis Christi';
        if (k < 1) return m;
        return (dom || '') + R[k] + ' ' + S[1];
      });
  }
  function en(t) {
    if (!t) return t;
    return String(t).replace(/(\d+)(?:st|nd|rd|th)( Sunday)? after (Pentecost|Epiphany|Easter)/g, function (m, n, sun, s) {
      var k = +n - (s === 'Pentecost' ? 2 : 1);
      if (s === 'Pentecost' && k === 0) return 'Sunday within the Octave of Corpus Christi';
      if (k < 1) return m;
      return ord(k) + (sun || '') + ' after the Octave of ' + {Pentecost: 'Trinity', Epiphany: 'the Epiphany', Easter: 'Easter'}[s];
    });
  }
  window.OPNames = {la: la, en: en};
  // the Masses carry their titles in the Roman numbering of the sources
  if (window.DOMINICAN && window.DOMINICAN.masses) {
    Object.keys(window.DOMINICAN.masses).forEach(function (k) {
      var m = window.DOMINICAN.masses[k];
      m.title = la(m.title); if (m.en) m.en = en(m.en); if (m.name_en) m.name_en = en(m.name_en);
    });
  }
})();
