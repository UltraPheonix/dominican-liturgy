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
})();
