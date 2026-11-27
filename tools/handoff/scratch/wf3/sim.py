# simulate the Mass page for every day of a year: serves repo files through playwright routes (read-only)
import json, sys, os, mimetypes, re
from playwright.sync_api import sync_playwright
ROOT = '/home/claude/dominican-liturgy'
year = int(sys.argv[1]); out = sys.argv[2]
def handle(route):
    url = route.request.url
    p = url.split('http://site.local/', 1)[1].split('#')[0].split('?')[0] or 'index.html'
    fp = os.path.join(ROOT, p)
    if not os.path.isfile(fp): return route.fulfill(status=404, body='')
    body = open(fp, 'rb').read()
    if p == 'js/app.js':
        s = body.decode('utf8')
        s = s.replace('window.ProprOP = {', 'window.ProprOP = {prescribed: prescribed, setName: setName, memoriasOf: memoriasOf, dayRankLabel: dayRankLabel, seasonPrayers: seasonPrayers, ', 1)
        body = s.encode('utf8')
    ct = mimetypes.guess_type(fp)[0] or 'application/octet-stream'
    route.fulfill(status=200, body=body, headers={'content-type': ct})
JS = r'''(y) => {
  const P = window.ProprOP, st = P.state(), D = P.D, res = [];
  for (let d = new Date(y, 0, 1, 12); d.getFullYear() === y; d.setDate(d.getDate() + 1)) {
    const dd = new Date(d), r = P.massesOf(dd), row = {date: P.iso(dd), office: r.day.office, temporal: r.day.temporal, commems: r.day.commems,
      twoMasses: r.day.twoMasses, notes: r.day.notes, head: P.dayRankLabel(r.day), missing: r.missing, masses: []};
    r.alts.forEach((a, i) => {
      const k = a.key; let o = {key: k, label: a.label || '', title: (D.masses[k] || {}).title || ''};
      try {
        st.date = dd; st.o2 = ''; st.o3 = ''; st.key = k;
        const R = P.rubricsOf(k, dd);
        o.gloria = R.gloria; o.credo = R.credo; o.dismiss = R.dismiss; o.requiem = !!R.requiem;
        o.pref = P.prefaceOf(k, dd); o.kyr = R.requiem ? 'Req' : P.autoKyriale(k, dd); o.pk = P.paschalKyrie(k, dd);
        o.color = P.massColor(k, dd);
        o.pr = P.prescribed(D.masses[k]); o.prn = o.pr.map(x => x === 'lib' ? '(ad lib.)' : P.setName(x));
      } catch (e) { o.err = String(e); }
      row.masses.push(o);
    });
    res.push(row);
  }
  return res;
}'''
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = b.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route('http://site.local/**', handle)
    pg.route(re.compile(r'^https?://(?!site\.local).*'), lambda r: r.abort())
    pg.goto('http://site.local/index.html#Jan1&d=%d-01-01' % year)
    pg.wait_for_function('!!(window.ProprOP && window.ProprOP.massesOf)', timeout=60000)
    pg.wait_for_timeout(1500)
    data = pg.evaluate(JS, year)
    json.dump(data, open(out, 'w'), ensure_ascii=False, indent=0)
    print('days', len(data), 'pageerrors', errs[:5])
    b.close()
