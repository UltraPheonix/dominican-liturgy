import asyncio, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page()
        await pg.goto('http://localhost:8765/index.html')
        await pg.wait_for_function("window.ProprOP && window.DOMINICAN",timeout=40000)
        res=await pg.evaluate("""()=>{const out={};for(let t=new Date(2026,0,1);t.getFullYear()==2026;t.setDate(t.getDate()+1)){const r=ProprOP.massesOf(new Date(t));out[t.getFullYear()+'-'+String(t.getMonth()+1).padStart(2,'0')+'-'+String(t.getDate()).padStart(2,'0')]=r.win}return out}""")
        json.dump(res,open('wins2026.json','w'),indent=0); print(len(res))
        await b.close()
asyncio.run(main())
