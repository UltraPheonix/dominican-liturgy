"""Render every chant and check that all of its words appear (catches truncated or garbled renders)."""
import asyncio, json, sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 900, 'height': 900})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('http://localhost:8765/index.html#Pent23')
        await pg.wait_for_function("window.ProprOP && document.querySelectorAll('.chant svg').length>=4", timeout=60000)
        res = await pg.evaluate("""async (ONLY) => {
          const ids = new Set(ONLY.length ? ONLY : Object.keys(DOMINICAN.chants));
          if (!ONLY.length) JSON.stringify(DOMINICAN.kyriale||{}).replace(/"(\\d{3,6}(?:_\\w+)?)"/g, (m, x) => { ids.add(x); return m; });
          const norm = s => s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase().replace(/æ/g,'ae').replace(/œ/g,'oe').replace(/[^a-z]/g,'');
          const lyr = g => g.replace(/\\([^)]*\\)/g,' ').replace(/<[^>]+>/g,'').replace(/[\\^_|{}]/g,'');
          const bad = []; let n = 0;
          const box = document.createElement('div'); box.style.width='700px'; document.body.appendChild(box);
          for (const id of ids) {
            let t; try { t = await ProprOP.loadGabc(id); } catch(e) { continue; }
            const g = ProprOP.splitGabc(t); if (!g.body.trim()) continue; n++;
            try {
              await ProprOP.renderInto(box, g.body, g.header, (DOMINICAN.chants[id]||{}).p);
              const shown = Array.from(box.querySelectorAll('svg text')).map(x => x.textContent).join(' ');
              const want = norm(lyr(ProprOP.exsurgeGabc ? ProprOP.exsurgeGabc(g.body) : g.body)), got = norm(shown);
              const raw = /[_^]|<\\/?[a-z]+>/.test(shown);
              if (got.length < want.length * 0.93 || raw) bad.push([id, want.length, got.length, raw ? shown.match(/.{0,20}[_^<].{0,20}/)[0] : shown.slice(-60)]);
            } catch (e) { bad.push([id, 'error', String(e).slice(0, 100)]); }
          }
          return {n, bad};
        }""", sys.argv[1:])
        print(res['n'], 'chants;', len(res['bad']), 'with missing or raw text')
        json.dump(res['bad'], open('/tmp/chant_text_bad.json', 'w'), ensure_ascii=False, indent=0)
        for x in res['bad'][:60]: print(json.dumps(x, ensure_ascii=False))
        print('page errors', errs[:5])
        await b.close()
asyncio.run(main())
