/* Shared by the Mass and Office pages: how the English is shown.
   'tap'  : Latin only; tap a passage to show (or hide) its English   (default)
   'both' : English with the Latin (beside it on wide screens)
   'en'   : English only where there is a translation */
(function () {
  var KEY = 'enMode';
  function get() {
    try {
      var v = localStorage.getItem(KEY);
      if (v === 'both' || v === 'en') return 'both';
    } catch (e) {}
    return 'tap';
  }
  function apply(m) {
    var b = document.body; if (!b) return;
    b.classList.remove('en-tap', 'en-both', 'en-only');
    b.classList.add(m === 'both' ? 'en-both' : m === 'en' ? 'en-only' : 'en-tap');
  }
  window.OPLang = {
    get: get,
    set: function (m) {
      try { localStorage.setItem(KEY, m); } catch (e) {}
      apply(m);
      document.dispatchEvent(new CustomEvent('oplang', {detail: m}));
    },
    apply: function () { apply(get()); }
  };
  // the EN switch at the top of the column: off = Latin, tap for English; on = Latin and English
  function wire() {
    apply(get());
    Array.prototype.forEach.call(document.querySelectorAll('.en-toggle'), function (t) {
      var mark = function () { var on = get() !== 'tap'; t.classList.toggle('on', on); t.setAttribute('aria-pressed', on); t.title = on ? 'Hide the English (tap a passage to show it)' : 'Show the English with the Latin'; };
      mark();
      t.addEventListener('click', function () { window.OPLang.set(get() === 'tap' ? 'both' : 'tap'); mark(); });
    });
  }
  if (document.readyState !== 'loading') wire(); else document.addEventListener('DOMContentLoaded', wire);

  // English on tap: the smallest passage that has a translation opens or closes
  var PAIR = '.o-lp, .o-pair, .r-cols, .m-pair, .o-sec';
  document.addEventListener('click', function (e) {
    if (!document.body.classList.contains('en-tap')) return;
    if (e.target.closest('a, button, summary, select, input, label, textarea, .no-tap')) return;
    var s = window.getSelection && String(window.getSelection());
    if (s) return;
    var p = e.target.closest(PAIR);
    while (p && !p.querySelector('.o-en, .o-tr, .en-text, .m-tr')) p = p.parentElement && p.parentElement.closest(PAIR);
    if (!p) return;
    p.classList.toggle('show-en');
  });

  // Report an error: a small button always at the foot of the screen
  var MAIL = 'jcampion@friars.providence.edu';
  function report() {
    if (document.getElementById('reportBtn')) return;
    var b = document.createElement('button');
    b.type = 'button'; b.id = 'reportBtn'; b.className = 'report-btn hide-print'; b.textContent = 'Report an error';
    var d = document.createElement('dialog');
    d.className = 'report-dlg'; d.setAttribute('aria-labelledby', 'reportTitle');
    d.innerHTML = '<h2 id="reportTitle">Report an error</h2>' +
      '<p>If you find a mistake in the text, the chant, the rubrics or the calendar, or something that does not work, please write to</p>' +
      '<p class="report-mail"><a id="reportMail"></a></p>' +
      '<p class="report-small">Please say which page and day, and what is wrong. A link to this page is added to the email for you.</p>' +
      '<div class="report-row"><a class="report-go" id="reportGo">Write an email</a><button type="button" id="reportCopy">Copy address</button><button type="button" id="reportClose">Close</button></div>';
    document.body.appendChild(b); document.body.appendChild(d);
    var mail = d.querySelector('#reportMail'); mail.textContent = MAIL; mail.href = 'mailto:' + MAIL;
    b.addEventListener('click', function () {
      var t = (document.querySelector('h1') || {}).textContent || document.title;
      d.querySelector('#reportGo').href = 'mailto:' + MAIL + '?subject=' + encodeURIComponent('Error on dominicanrite.com: ' + t.trim()) +
        '&body=' + encodeURIComponent('Page: ' + location.href + '\n\nWhat is wrong:\n\n');
      if (d.showModal) d.showModal(); else d.setAttribute('open', '');
    });
    d.querySelector('#reportClose').addEventListener('click', function () { d.close ? d.close() : d.removeAttribute('open'); });
    d.addEventListener('click', function (e) { if (e.target === d && d.close) d.close(); });
    d.querySelector('#reportCopy').addEventListener('click', function (e) {
      var c = e.target;
      if (navigator.clipboard) navigator.clipboard.writeText(MAIL).then(function () { c.textContent = 'Copied'; setTimeout(function () { c.textContent = 'Copy address'; }, 1500); });
    });
  }
  if (document.readyState !== 'loading') report(); else document.addEventListener('DOMContentLoaded', report);

  // the Options sheet (gear in the top bar)
  function sheetWire() {
    var g = document.getElementById('gear'), sh = document.getElementById('sheet'), bk = document.getElementById('sheetBack'), x = document.getElementById('sheetX');
    if (!g || !sh) return;
    if (!sh.querySelector('.side-foot')) {
      var f = document.createElement('p'); f.className = 'side-foot';
      f.innerHTML = 'A private project, not affiliated with the Order of Preachers. <a href="about.html">About the sources</a>';
      sh.appendChild(f);
    }
    function set(open) {
      sh.hidden = !open; if (bk) bk.hidden = !open; g.setAttribute('aria-expanded', open);
      document.body.classList.toggle('sheet-open', open);
      if (open) { sh.setAttribute('tabindex', '-1'); sh.focus(); }
      else g.focus();
    }
    g.addEventListener('click', function () { set(sh.hidden); });
    if (x) x.addEventListener('click', function () { set(false); });
    if (bk) bk.addEventListener('click', function () { set(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !sh.hidden) set(false); });
    // choosing a day closes the sheet, so the Mass or Hour is seen at once
    sh.addEventListener('change', function (e) { if (e.target.id === 'date' || e.target.id === 'selMass') setTimeout(function () { set(false); }, 120); });
    sh.addEventListener('click', function (e) { if (e.target.closest('.cal-day, .alt')) setTimeout(function () { set(false); }, 120); });
  }
  if (document.readyState !== 'loading') sheetWire(); else document.addEventListener('DOMContentLoaded', sheetWire);
})();

