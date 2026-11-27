import sys, asyncio
from playwright.sync_api import sync_playwright
urls = sys.argv[1:]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    for u in urls:
        ctx = b.new_context(); pg = ctx.new_page(); errs = []
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://localhost:8765/holyweek.html'); pg.evaluate("localStorage.setItem('hwRite','1939')")
        pg.goto(u); pg.wait_for_timeout(2500)
        # scroll through to trigger lazy chant
        h = pg.evaluate('document.body.scrollHeight')
        for y in range(0, h, 1500): pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(120)
        pg.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)"); pg.wait_for_timeout(500)
        h = pg.evaluate('document.body.scrollHeight')
        for y in range(0, h, 1500): pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(120)
        pg.wait_for_timeout(1500)
        txt = pg.evaluate('document.body.innerText')
        svgs = pg.evaluate("document.querySelectorAll('.hw-chant svg, .chant svg').length")
        print(u, 'errors:', len(errs), errs[:3], 'could-not:', txt.count('could not be drawn'), 'svgs:', svgs)
        ctx.close()
    b.close()
