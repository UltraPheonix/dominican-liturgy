import asyncio,sys
from playwright.async_api import async_playwright
dates=sys.argv[1:]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        ctx=await b.new_context(); errs=[]
        await ctx.add_init_script("try{localStorage.setItem('officeRite','1909')}catch(e){}")
        for d in dates:
            for h in ('Laudes','Vespera','Matutinum'):
                pg=await ctx.new_page()
                pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None); pg.on('pageerror',lambda e: errs.append(str(e)))
                await pg.goto('http://localhost:8768/office.html#%s&d=%s'%(h,d)); await pg.wait_for_timeout(2500)
                txt=await pg.inner_text('body'); i=txt.find('Oratio de Sancto')
                if h=='Laudes': print(d,'|',txt[i:i+300].replace('\n',' ') if i>=0 else 'NO SAINT PRAYER')
                await pg.close()
        print('ERRORS',errs[:8]); await b.close()
asyncio.run(main())
