"""Every day of a liturgical year on the Mass page: which Mass the page gives, what it shows, and what is missing.
usage: python3 tools/check/day_audit.py START END > /tmp/days.json   (dates YYYY-MM-DD; local server on :8768)"""
import sys, json, datetime
from playwright.sync_api import sync_playwright
a, b = [datetime.date.fromisoformat(x) for x in sys.argv[1:3]]
GET = r"""() => {
  const secs = [...document.querySelectorAll('main .part[data-part], main section[data-part]')];
  const parts = secs.map(s => ({p: s.dataset.part, k: s.dataset.k || '', inc: ((s.querySelector('.incipit, .c-sel option:checked, select option:checked')||{}).textContent||'').trim().slice(0,40),
      empty: !!s.querySelector('.empty'), loading: !!s.querySelector('.loading'), noen: !!s.querySelector('.c-missing'), extra: s.classList.contains('o-extra')}));
  const reads = [...document.querySelectorAll('main .reading, main [data-part=reading]')].map(r => ({la: ((r.querySelector('.la, [lang=la]')||{}).textContent||'').length, en: ((r.querySelector('.en-text, [lang=en]')||{}).textContent||'').length}));
  return {hash: location.hash, title: ((document.querySelector('main h1, .m-title')||{}).textContent||'').trim().slice(0,90),
          alts: [...document.querySelectorAll('#dateResults .alt')].map(x => x.dataset.k), parts, reads,
          text: (document.querySelector('main')||{innerText:''}).innerText.slice(0, 20000)};
}"""
out = []
with sync_playwright() as p:
    br = p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg = br.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://localhost:8768/index.html?audit=1'); pg.wait_for_timeout(2500)
    d = a
    while d <= b:
        errs.clear()
        pg.evaluate("(v) => { const i = document.querySelector('#date'); i.value = v; i.dispatchEvent(new Event('change')); }", d.isoformat())
        pg.wait_for_timeout(900)
        for _ in range(10):
            if not pg.evaluate("document.querySelectorAll('main .loading').length"): break
            pg.wait_for_timeout(400)
        r = pg.evaluate(GET); r['date'] = d.isoformat(); r['errors'] = list(errs)
        has = lambda s: s in r['text']
        r['gloria'] = has('Glória in excélsis') or has('Gloria in excelsis'); r['credo'] = has('Credo in unum'); r['req'] = has('Requiem')
        del r['text']; out.append(r)
        sys.stderr.write(d.isoformat() + ' ' + r['hash'][:40] + '\n')
        d += datetime.timedelta(days=1)
    br.close()
json.dump(out, sys.stdout, ensure_ascii=False)
