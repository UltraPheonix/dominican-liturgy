"""Year check of the Mass in headless Chrome (serve the repo on :8768 first)."""
import asyncio, os, sys
from playwright.async_api import async_playwright
JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'year.js')).read()
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await b.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('http://localhost:8768/index.html'); await pg.wait_for_timeout(2500)
        r = await pg.evaluate(JS); print(r or 'clean'); print('page errors:', errs[:5]); await b.close()
asyncio.run(main())
