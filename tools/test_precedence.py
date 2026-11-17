import asyncio, json, re, unicodedata
from playwright.async_api import async_playwright
def w(s):
    s=''.join(c for c in unicodedata.normalize('NFD',s.lower()) if not unicodedata.combining(c)).replace('j','i').replace('æ','ae')
    return set(x[:6] for x in re.findall(r'[a-z]{4,}',s))-{'sancti','sancta','beati','missa','feria','domini','dominica'}
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1300,'height':1000})
        errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
        await pg.goto('http://localhost:8765/index.html')
        await pg.wait_for_function("window.ProprOP && document.querySelectorAll('.chant svg').length>=4",timeout=40000)
        res=await pg.evaluate("""async()=>{const O=await (await fetch('ordo_test.json')).json();return O.map(([d,n,c])=>{const p=d.split('-').map(Number);const r=ProprOP.massesOf(new Date(p[0],p[1]-1,p[2]));const m=DOMINICAN.masses[r.win]||{};return [d,n,c,r.win,(m.title||'')+' '+(m.en||'')]})}""")
        ok=0; bad=[]
        for d,n,c,k,t in res:
            feria = n.startswith('Feria') or 'Dominica' in n or 'Hebdomad' in n or 'Quadrag' in n or 'Advent' in n
            good = bool(w(n)&w(t)) or (feria and k and not k.startswith('S'))
            ok+=good
            if not good: bad.append((d,n[:40],c,k,t[:50]))
        print('precedence matches the 2026 Ordo on',ok,'of',len(res),'days')
        for x in bad[:25]: print(' ',x)
        await pg.screenshot(path='/home/claude/build/shot_new_desktop.png')
        print('errors:',errs[:5])
        await b.close()
asyncio.run(main())
