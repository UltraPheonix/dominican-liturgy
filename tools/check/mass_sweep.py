import asyncio
from playwright.async_api import async_playwright
KEYS = ['Adv1','Dec25_3','Epi','Quad1w','Quad4w','Pasc0','Pent0','CorpusChristi','Pent3','S0804','S1004','S1102','C114s','C82s']
FORMS = ['low','sung','solemn','conv']
CASES = [(k,f,rub,x) for k in KEYS for f in FORMS for rub in ['', 'full'] for x in ([''] if not rub else ['', '&sac=tab&prel=bp', '&sac=exp&prel=pope&serv=one'])]
JS = """()=>{const rs=[...document.querySelectorAll('#mass .o-rub')].map(e=>(e.querySelector('summary')||e).textContent.trim());
 const dup=rs.filter((t,i)=>rs.indexOf(t)!==i);
 const heads=[...document.querySelectorAll('#mass .part-head h2')].map(e=>e.textContent);
 const empty=[...document.querySelectorAll('#mass section.ordo')].filter(s=>!s.querySelector('.o-line,.o-rub,.chant,.reading,.tone')).length;
 return {n:rs.length, dup:[...new Set(dup)], empty, hasCanon:heads.includes('Canon Missæ'), last:heads.slice(-2)}}"""
async def worker(b, q, out):
    pg = await b.new_page(viewport={'width': 1000, 'height': 1000})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    while q:
        k, f, rub, x = q.pop()
        n0 = len(errs)
        await pg.goto('http://localhost:8768/index.html?n=%d#%s&ordo=%s&rub=%s%s' % (len(q), k, f, rub, x), wait_until='domcontentloaded')
        await pg.wait_for_timeout(1800)
        r = await pg.evaluate(JS)
        if [d for d in r['dup'] if not d.startswith(('Tabernacle','Exposition'))] or r['empty'] or not r['hasCanon'] or len(errs) > n0 or r['n'] == 0:
            out.append((k, f, rub, x, r, errs[n0:]))
async def m():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        q = list(CASES); out = []
        await asyncio.gather(*[worker(b, q, out) for _ in range(6)])
        for o in sorted(out, key=str): print(o)
        print('cases', len(CASES), 'flagged', len(out)); await b.close()
asyncio.run(m())
