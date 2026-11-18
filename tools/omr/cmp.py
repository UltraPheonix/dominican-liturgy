"""cmp.py KEY... : stack each scan crop (/tmp/om/c_<key>.png) over the rendering of its GABC from cand33.json -> /tmp/om/cmp.png"""
import asyncio, json, sys
from PIL import Image
from playwright.async_api import async_playwright
C=json.load(open('/home/claude/build/omr/cand33.json'))
keys=sys.argv[1:]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1500,'height':400})
        await pg.goto('http://localhost:8766/index.html'); await pg.wait_for_timeout(500)
        await pg.evaluate('l=>draw(l)',[C[k]['gabc'] for k in keys]); await pg.wait_for_timeout(1500)
        ims=[]
        for i,k in enumerate(keys):
            el=await pg.query_selector('#c%d'%i); await el.screenshot(path='/tmp/om/r%d.png'%i)
            a=Image.open('/tmp/om/c_%s.png'%k[:40]).convert('L'); a=a.resize((int(a.width*0.85),int(a.height*0.85)))
            r=Image.open('/tmp/om/r%d.png'%i).convert('L')
            ims+= [a,r]
        W=max(i.width for i in ims); H=sum(i.height for i in ims)+10*len(ims)
        o=Image.new('L',(W,H),255); y=0
        for im in ims: o.paste(im,(0,y)); y+=im.height+10
        o.save('/tmp/om/cmp.png'); await b.close()
asyncio.run(main())
