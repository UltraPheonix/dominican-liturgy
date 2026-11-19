import asyncio, sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1000,'height':600})
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type in ('error','warning') else None)
        await pg.goto('http://localhost:8767/index.html'); await pg.wait_for_timeout(500)
        for f in sys.argv[1:]:
            g=open(f).read().split('%%')[-1]
            await pg.evaluate('l=>draw(l)',['%%\n'+g]); await pg.wait_for_timeout(2500)
            el=await pg.query_selector('#c0'); bb=await el.bounding_box()
            await el.screenshot(path=f.replace('.gabc','_r.png'))
            print(f.split('/')[-1], 'height', bb and round(bb['height']), errs[-3:]); errs.clear()
        await b.close()
asyncio.run(main())
