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
