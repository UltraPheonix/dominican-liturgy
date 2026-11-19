import asyncio, sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page()
        await pg.goto('http://localhost:8768/booklet.html?b=%s#%s'%(sys.argv[1],sys.argv[2]))
        await pg.wait_for_selector('body.b-ready', timeout=90000)
        print(await pg.evaluate(sys.argv[3]))
        await b.close()
asyncio.run(main())
