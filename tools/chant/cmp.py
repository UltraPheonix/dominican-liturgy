"""cmp.py name : render /tmp/rt/<name>.gabc and stack it under the scan crop /tmp/rt/<name>.png -> /tmp/rt/<name>_cmp.png"""
import asyncio, sys
from PIL import Image
from playwright.async_api import async_playwright
n=sys.argv[1]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1000,'height':600})
        await pg.goto('http://localhost:8767/index.html'); await pg.wait_for_timeout(500)
        await pg.evaluate('l=>draw(l)',[open('/tmp/rt/%s.gabc'%n).read()]); await pg.wait_for_timeout(2500)
        el=await pg.query_selector('#c0'); await el.screenshot(path='/tmp/rt/r.png')
        a=Image.open('/tmp/rt/%s.png'%n).convert('L'); r=Image.open('/tmp/rt/r.png').convert('L')
        W=max(a.width,r.width); o=Image.new('L',(W,a.height+r.height+10),255); o.paste(a,(0,0)); o.paste(r,(0,a.height+10)); o.save('/tmp/rt/%s_cmp.png'%n)
        await b.close()
asyncio.run(main())
