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
    // hidden while the page is being scrolled, back when the reader stops (it covered the chant on phones)
    var rbT = null;
    window.addEventListener('scroll', function () {
      b.classList.add('rb-away'); clearTimeout(rbT);
      rbT = setTimeout(function () { b.classList.remove('rb-away'); }, 1500);
    }, {passive: true});
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
      f.innerHTML = 'For private devotion and reference, not an authoritative liturgical text. A private project, not affiliated with the Order of Preachers. <a href="about.html">About</a>';
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

  // Night mode: a moon button in the top bar; remembered per browser. The cappa bar is already dark.
  var TKEY = 'theme';
  function theme() { try { return localStorage.getItem(TKEY) === 'dark' ? 'dark' : 'light'; } catch (e) { return 'light'; } }
  function applyTheme(t) { document.documentElement.setAttribute('data-theme', t); }
  applyTheme(theme());
  function themeWire() {
    var tools = document.querySelector('.top-tools'), inn = document.querySelector('.top .top-in');
    if (!tools && inn) { tools = document.createElement('div'); tools.className = 'top-tools'; inn.appendChild(tools); }
    if (!tools || document.getElementById('themeBtn')) return;
    var b = document.createElement('button');
    b.type = 'button'; b.id = 'themeBtn'; b.className = 'theme-btn';
    var mark = function () { var d = theme() === 'dark'; b.setAttribute('aria-pressed', d); b.title = d ? 'Day mode' : 'Night mode'; b.setAttribute('aria-label', b.title);
      b.innerHTML = d ? '<svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.5" fill="currentColor"/><g stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></g></svg>'
        : '<svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z"/></svg>'; };
    mark();
    b.addEventListener('click', function () { var t = theme() === 'dark' ? 'light' : 'dark'; try { localStorage.setItem(TKEY, t); } catch (e) {} applyTheme(t); mark(); });
    tools.insertBefore(b, tools.firstChild);
  }
  if (document.readyState !== 'loading') themeWire(); else document.addEventListener('DOMContentLoaded', themeWire);

  // Tap the date at the head of the page: a month calendar opens under it (sets the Options date field, so each page handles it)
  function datePopWire() {
    var lab = document.getElementById('dayDate') || document.getElementById('dayMeta');
    var input = document.getElementById('date');
    if (!lab || !input || !window.OPCal || !lab.closest('.daybar')) return;
    lab.setAttribute('role', 'button'); lab.setAttribute('tabindex', '0'); lab.classList.add('day-pick');
    lab.title = 'Choose a day';
    var pop = document.createElement('div'); pop.className = 'date-pop'; pop.hidden = true; pop.setAttribute('role', 'dialog'); pop.setAttribute('aria-label', 'Choose a day');
    var calBox = document.createElement('div'); pop.appendChild(calBox);
    var todayB = document.createElement('button'); todayB.type = 'button'; todayB.className = 'date-today'; todayB.textContent = 'Today'; pop.appendChild(todayB);
    lab.closest('.daybar').appendChild(pop);
    var cal = null;
    function cur() { var v = input.value; if (/^\d{4}-\d\d-\d\d$/.test(v)) { var p = v.split('-').map(Number); return new Date(p[0], p[1] - 1, p[2]); } return new Date(); }
    function pick(d) {
      input.value = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
      input.dispatchEvent(new Event('change', {bubbles: true}));
      close();
    }
    function dot(d) {
      var P = window.ProprOP; if (!P || !P.massesOf) return '';
      try { var w = P.massesOf(d).win, c = w ? P.massColor(w, d) : ''; return c === 'black' ? '#7a7a7a' : ({white: '#ffffff', red: '#b3313d', green: '#5f8f5f', violet: '#6a3d8f', rose: '#d98aa6'}[c] || ''); } catch (e) { return ''; }
    }
    function open() {
      if (!cal) cal = window.OPCal(calBox, {date: cur(), onPick: pick, dot: dot}); else cal.set(cur());
      pop.hidden = false; lab.setAttribute('aria-expanded', 'true');
      var f = pop.querySelector('.cal-day.sel') || pop.querySelector('.cal-day'); if (f) f.focus();
    }
    function close() { pop.hidden = true; lab.setAttribute('aria-expanded', 'false'); }
    lab.addEventListener('click', function () { pop.hidden ? open() : close(); });
    lab.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pop.hidden ? open() : close(); } });
    todayB.addEventListener('click', function () { pick(new Date()); });
    document.addEventListener('click', function (e) { if (!pop.hidden && !pop.contains(e.target) && e.target !== lab && !lab.contains(e.target)) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !pop.hidden) { close(); lab.focus(); } });
  }
  if (document.readyState !== 'loading') datePopWire(); else document.addEventListener('DOMContentLoaded', datePopWire);
})();

/* One header and one language switch on every page (Mass, Office, Holy Week, Rubrics, Prayers, About) */
(function () {
  var NAV = [['./', 'Mass', /(^|\/)(index\.html)?$/], ['office.html', 'Office', /office\.html$/], ['holyweek.html', 'Holy Week', /holyweek\.html$/],
    ['rubrics.html', 'Rubrics', /rubrics\.html$/], ['prayers.html', 'Prayers', /prayers\.html$/], ['processions.html', 'Processions', /processions\.html$/], ['about.html', 'About', /about\.html$/]];
  function wire() {
    var nav = document.querySelector('.top .nav'), path = location.pathname;
    if (nav && !document.body.classList.contains('booklet')) {
      nav.innerHTML = '';
      NAV.forEach(function (n) {
        var a = document.createElement('a'); a.href = n[0]; a.textContent = n[1];
        if (n[2].test(path)) a.setAttribute('aria-current', 'page');
        nav.appendChild(a);
      });
    }
    var inn = document.querySelector('.top .top-in');
    if (inn && !inn.querySelector('.top-tools')) { var t = document.createElement('div'); t.className = 'top-tools'; inn.appendChild(t); }
    // the language switch: Latin (tap a passage for its English) / Latin + English, under the title of the page
    var old = document.querySelector('.top .en-toggle');
    var seg = document.querySelector('.seg[data-lang]');
    if (old && !seg) {
      seg = document.createElement('div'); seg.className = 'seg'; seg.setAttribute('data-lang', ''); seg.setAttribute('role', 'radiogroup'); seg.setAttribute('aria-label', 'Language');
      seg.innerHTML = '<button type="button" role="radio" data-v="tap">Latin</button><button type="button" role="radio" data-v="both">Latin + English</button>';
      var bar = document.createElement('div'); bar.className = 'pagebar hide-print'; bar.appendChild(seg);
      var slot = document.getElementById('hwbar') || document.getElementById('hours');
      if (slot && slot.id === 'hwbar') slot.insertBefore(seg, slot.firstChild);
      else if (slot) slot.parentNode.insertBefore(bar, slot);
      else { var db = document.querySelector('.daybar'); if (db) db.parentNode.insertBefore(bar, db.nextSibling); }
    }
    if (old) old.remove();
    if (!seg || !window.OPLang) return;
    var mark = function () { var v = window.OPLang.get(); Array.prototype.forEach.call(seg.children, function (b) { var on = b.getAttribute('data-v') === v; b.classList.toggle('on', on); b.setAttribute('aria-checked', on); }); };
    mark();
    if (!seg.hasAttribute('data-wired')) {
      seg.setAttribute('data-wired', '');
      seg.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; window.OPLang.set(b.getAttribute('data-v')); });
    }
    document.addEventListener('oplang', mark);
  }
  if (document.readyState !== 'loading') wire(); else document.addEventListener('DOMContentLoaded', wire);

  // a quiet line at the foot of every page (About, the disclaimer: not an authoritative liturgical text, not affiliated with the Order)
  function siteFoot() {
    if (document.querySelector('.site-foot') || /booklet\.html$/.test(location.pathname)) return;
    var f = document.createElement('footer'); f.className = 'site-foot hide-print';
    f.innerHTML = 'For private devotion and as a resource, not an authoritative liturgical text: if celebrating the Dominican rite, please consult the liturgical books. ' +
      'A private project, not affiliated with the Order of Preachers. ' +
      '<a href="about.html#disclaimer">About</a> · <a href="about.html#support">Books &amp; support the Order</a>';
    (document.querySelector('.content') || document.body).appendChild(f);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', siteFoot); else siteFoot();
})();
