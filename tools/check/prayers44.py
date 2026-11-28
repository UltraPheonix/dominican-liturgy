"""The 2nd/3rd prayers the Mass page prescribes, day by day (step 2, Ordo 1944 sections A-H).
usage: python3 tools/check/prayers44.py START END [PORT] > out.json   (local server; dates YYYY-MM-DD)
Each line: date, the Mass shown (the conventual Mass of the day), the office and its commemorations, the prayers prescribed."""
import sys, json, datetime
from playwright.sync_api import sync_playwright
a, b = [datetime.date.fromisoformat(x) for x in sys.argv[1:3]]
port = sys.argv[3] if len(sys.argv) > 3 else '8768'
with sync_playwright() as p:
    br = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox']); pg = br.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://localhost:%s/index.html?t=1' % port); pg.wait_for_timeout(3000)
    d = a; out = []
    while d <= b:
        errs.clear()
        pg.evaluate("(v) => { const i = document.querySelector('#date'); i.value = v; i.dispatchEvent(new Event('change')); }", d.isoformat())
        pg.wait_for_timeout(500)
        r = pg.evaluate("() => window.OPTest ? {key: OPTest.key(), ids: OPTest.prescribed(), names: OPTest.names(), day: OPTest.day()} : null")
        r = r or {}; r['date'] = d.isoformat(); r['errors'] = errs[:]
        out.append(r); print(json.dumps(r, ensure_ascii=False), flush=True)
        d += datetime.timedelta(days=1)
    br.close()
