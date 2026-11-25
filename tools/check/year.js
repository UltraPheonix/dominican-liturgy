// Year check of the Mass (run in the page: python3 tools/check/year.py). One problem per line; empty = clean.
(async () => {
  const P = ProprOP, S = P.state(), D = P.D, out = [], y0 = +(window.__Y || 2026);
  const AL = /al\([^)]*\)\s*le\([^)]*\)\s*l[úu]\(/i;
  for (let d = new Date(y0, 10, 29, 12); d < new Date(y0 + 1, 10, 28, 12); d = P.addDays(d, 1)) {
    const r = P.massesOf(d), k = r.win; if (!k) continue;
    S.key = k; S.date = d;
    const parts = P.massParts(k), E = P.easter(d.getFullYear()), f = P.diffDays(d, E), lent = f >= -63 && f < 0, pasch = f >= 0 && f < 56;
    const tag = P.iso(d) + ' ' + k;
    if (lent && parts.al.length) out.push(tag + ': Alleluia in Septuagesima/Lent');
    if (lent && !parts.tr.length && (d.getDay() === 0 || [1, 3, 5].includes(d.getDay()) && f >= -46 || !P.isTemporal(k)) && !/^Quad6[hfs]|^Quad6t/.test(k)) out.push(tag + ': no Tract');
    if (!lent && parts.tr.length && !/^(Adv3|Pent0|Emb|S1102|S1113|C114|S0915)/.test(k) && !pasch) out.push(tag + ': Tract outside Lent');
    const pn = P.prefaceOf(k, d), pc = pn && P.prefaceChant(pn, k, d);
    if (d.getDay() === 0 && pc && pc.tone !== 'solemn') out.push(tag + ': Sunday Preface ' + pn + ' in the ferial tone');
    for (const p of ['in', 'of', 'co']) for (const c of parts[p] || []) {
      if (pasch) continue;
      let g; try { g = P.splitGabc(await P.loadGabc(c.id)).body; } catch (e) { out.push(tag + ': missing gabc ' + c.id); continue; }
      const s = P.seasonalGabc(g, p);
      if (AL.test(s) && !/^(Epi2|CorpusChristi|C62s|S0806|C75s)$/.test(k)) out.push(tag + ': Alleluia left in ' + p + ' ' + c.id);
    }
  }
  return out.join('\n');
})()
