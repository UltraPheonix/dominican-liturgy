import asyncio, sys
from playwright.async_api import async_playwright
# book.py choir|priest|cong HASH out.pdf
async def main():
    b_, h, out = sys.argv[1], sys.argv[2], sys.argv[3]
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1000,'height':900})
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)+' '+str(e.stack)[:600])); pg.on('console', lambda m: errs.append(m.text) if m.type in ('error',) else None)
        await pg.goto('http://localhost:8768/booklet.html?b=%s#%s'%(b_,h))
        try: await pg.wait_for_selector('body.b-ready', timeout=90000)
        except Exception as e: print('timeout', await pg.evaluate("(document.getElementById('bStatus')||{}).textContent"))
        print(await pg.evaluate("(document.getElementById('bStatus')||{}).textContent"))
        await pg.emulate_media(media='print')
        await pg.pdf(path=out, width='210mm', height='297mm', print_background=True, prefer_css_page_size=True)
        print('errors', errs[:8])
        await b.close()
asyncio.run(main())
