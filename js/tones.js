/* The common tones of the Office of the Order of Preachers: opening of the Hours, versicles, chapter,
   prayers and their conclusions, Benedicamus Domino.
   Sources: Antiphonarium S.O.P. (1933), Toni communes I and VI; Regulae tonorum communium O.P. (1965), art. III.
   Every function returns GABC for exsurge. */
(function () {
  'use strict';
  var P = window.OPPsalm;

  // ---------------------------------------------------------------- fixed melodies
  var FIXED = {
    // Antiphonarium 1933, Toni communes I: Modus inchoandi Horas
    deus: "(c3) De(f)us,(f) in(f) ad(f)ju(f)tó(g)ri(f)um(f) me(f)um(f) in(f)tén(e)de.(f) (::) " +
          "<sp>R/</sp>. Dó(f)mi(f)ne,(f) ad(f) ad(f)ju(f)ván(f)dum(f) me(f) fe(f)stí(e)na.(f) (::) " +
          "Gló(f)ri(f)a(f) Pa(f)tri,(f) et(f) Fí(f)li(e)o,(e) (,) et(e) Spi(e)rí(e)tu(e)i(e) Sanc(e)to.(f) (:) " +
          "Si(f)cut(f) e(f)rat(f) in(f) prin(f)cí(f)pi(f)o,(f) et(f) nunc(f) et(f) sem(f)per,(e) (,) et(e) in(e) sǽ(f)cu(f)la(f) sæ(f)cu(f)ló(f)rum.(f) A(f)men.(e) (::)",
    alleluia: "Al(f)le(fg)lú(gf)ia.(e) (::)",
    laus: "(c3) Laus(h) ti(h)bi,(h) Dó(h)mi(g)ne,(g) (,) rex(g) æ(g)tér(h)næ(h) gló(h)ri(g)æ.(g) (::)",
    converte: "(c3) Con(h)vér(h)te(h) nos,(h) De(h)us,(h) sa(h)lu(h)tá(h)ris(h) no(g)ster.(h) (::) " +
              "<sp>R/</sp>. Et(h) a(h)vér(h)te(h) i(h)ram(h) tu(h)am(h) a(h) no(g)bis.(h) (::)",
    // Regulae 1965, art. III § III: before the prayer
    dvSol: "(f3) Dó(g)mi(h)nus(h) vo(gh)bís(hg)cum.(g.) (::) <sp>R/</sp>. Et(g) cum(h) spí(h)ri(g)tu(g) tu(h)o.(h.) (::)",
    dvSim: "(f3) Dó(h)mi(h)nus(h) vo(h)bís(h)cum.(f.) (::) <sp>R/</sp>. Et(g) cum(g) spí(h)ri(h)tu(h) tu(h)o.(h.) (::)",
    deSol: "(f3) Dó(g)mi(h)ne,(h) ex(h)áu(h)di(h) o(h)ra(h)ti(h)ó(g)nem(h) me(hg)am.(g.) (::) " +
           "<sp>R/</sp>. Et(g) cla(h)mor(h) me(h)us(h) ad(g) te(g) vé(h)ni(h)at.(h.) (::)",
    deSim: "(f3) Dó(h)mi(h)ne,(h) ex(h)áu(h)di(h) o(h)ra(h)ti(h)ó(h)nem(h) me(h)am.(f.) (::) " +
           "<sp>R/</sp>. Et(h) cla(h)mor(h) me(h)us(h) ad(h) te(h) vé(f)ni(g)at.(g.) (::)",
    oremusSol: "(f3) O(h)ré(gh)mus.(h.) (::)",
    oremusSim: "(f3) O(h)ré(h)mus.(f.) (::)",
    amen: "<sp>R/</sp>. A(g)men.(h.) (::)",
    // Antiphonarium 1933, Toni communes VI: at the end of the Hours
    // Matins (Fr Thompson's Antiphonale, Toni communes: Modus incohandi Officii lectionum)
    labia: "(f3) Dó(h)mi(h)ne,(h) lá(h)bi(h)a(h) me(h)a(h) a(h)pé(g)ri(g)es.(h) (::) <sp>R/</sp>. Et(h) os(h) me(h)um(h) an(h)nun(h)ti(h)á(h)bit(h) lau(h)dem(h) tu(g)am.(h) (::)",
    // Regulae 1965, art. III § IV: asking the blessing
    iube: "(f3) <sp>V/</sp>. Ju(g)be,(g) dom(h)ne,(h) be(h)ne(g)dí(f)ce(e)re.(e.) (::)",
    // Completorium O.P. 1949, pp. 2: the short lesson of Compline and the Adjutorium, as notated in the book
    lectioCompl: "(c3) Fra(h)tres:(h) Só(h)bri(h)i(h) es(h)tó(h)te(h) et(h) vi(h)gi(h)lá(h)te:(g) (,) qui(h)a(h) ad(h)ver(h)sá(h)ri(h)us(h) ve(h)ster(h) " +
      "di(h)á(h)bo(h)lus(h) (,) tam(h)quam(h) le(h)o(h) rú(h)gi(h)ens(h) (,) cír(h)cu(h)it,(h) quæ(h)rens(g) quem(f) dé(h)vo(h)ret:(h) (,) " +
      "cu(h)i(h) re(h)sí(h)sti(h)te(h) for(h)tes(h) in(f) fi(g)de.(c) (:) Tu(h) au(h)tem,(h) Dó(h)mi(f)ne,(f) (,) mi(h)se(h)ré(h)re(f) no(g)stri.(c) (::) " +
      "<sp>R/</sp>. De(g)o(g) grá(g)ti(g)as.(h) (::)",
    adjutorium: "(c3) <sp>V/</sp>. Ad(h)ju(h)tó(h)ri(h)um(h) no(h)strum(h) in(h) nó(h)mi(h)ne(h) Dó(h)mi(g)ni.(g) (::) " +
      "<sp>R/</sp>. Qui(h) fe(h)cit(h) cæ(h)lum(h) et(h) ter(h)ram.(g) (::)",
    benFin: "(c3) Be(f)ne(f)di(f)cá(f)mus(f) Dó(f)mi(e)no.(e) (::) <sp>R/</sp>. De(e)o(e) grá(e)ti(e)as.(f) (::)"
  };
  // Benedicamus at Lauds and Vespers (Antiphonarium 1933, Toni communes VI), GregoBase transcriptions
  var BEN = {I: '4206', BVM: '4227', II: '7984', domMaior: '7985', III: '7986', domMinor: '7986', simplex: '7993', feria: '7994'};

  // ---------------------------------------------------------------- recitation on a tone
  function plain(s) { return String(s).replace(/<[^>]+>/g, '').replace(/[✠✙]/g, '').replace(/\s+/g, ' ').trim(); }
  // words of a text fitted to a cadence on a tenor: GABC (without clef)
  function recite(text, cad, tenor, opts) {
    opts = opts || {};
    text = plain(text);
    if (!text) return '';
    var syl = P.analyse(text), f;
    if (cad) f = P.fit(syl, P.parseCadence(cad), tenor);
    else f = {notes: syl.map(function () { return tenor; })};
    if (opts.tail) {                                   // fixed notes on the last syllables (e.g. a melisma)
      var t = opts.tail.split(' ');
      for (var i = 0; i < t.length && i < syl.length; i++) f.notes[syl.length - t.length + i] = t[i];
    }
    var out = '';
    syl.forEach(function (s, i) { out += s.t.replace(/[()]/g, '') + '(' + f.notes[i] + ')' + (s.last ? ' ' : ''); });
    return out.trim();
  }
  // split a text into members at colons and semicolons (and question marks)
  function members(text) {
    var t = plain(text), out = [], re = /[^:;?]+[:;?]?/g, m;
    while ((m = re.exec(t))) if (m[0].trim()) out.push(m[0].trim());
    return out;
  }
  var FLEX = "'h fr f", ELEV = "g f 'h hr h";
  // chapter: alternate flexio and elevatio, the last being a flexio
  function chapter(text) {
    var ms = members(text), g = '(f3) ';
    ms.forEach(function (m, i) {
      var fromEnd = ms.length - 1 - i, cad = fromEnd % 2 === 0 ? FLEX : ELEV;
      g += recite(m, cad, 'h') + (fromEnd === 0 ? ' (::) ' : (cad === FLEX ? ' (;) ' : ' (:) '));
    });
    return g + '<sp>R/</sp>. De(g)o(g) grá(g)ti(g)as.(h.) (::)';
  }
  // the body of a prayer: alternate flexio and elevatio, the last being an elevatio
  function prayerBody(text) {
    var ms = members(text), g = '';
    ms.forEach(function (m, i) {
      var fromEnd = ms.length - 1 - i, cad = fromEnd % 2 === 0 ? ELEV : FLEX;
      g += recite(m, cad, 'h') + (cad === FLEX ? ' (;) ' : ' (:) ');
    });
    return g;
  }
  // conclusions of prayers (Regulae art. III § III, 3)
  function conclusion(text, solemn) {
    var t = plain(text), g = '';
    var finalCad = solemn ? "h 'hg g" : "h 'h g";
    var m = /^(.*?(?:Fílium tuum|Deo Patre))[,:]?\s*(.*?(?:Spíritus Sancti,? Deus),?)\s*(per ómnia sǽcula sæculórum\.?)$/i.exec(t);
    if (m) {
      g += recite(m[1], FLEX, 'h') + ' (;) ';
      g += recite(m[2], ELEV, 'h') + ' (:) ';
      g += recite(m[3], finalCad, 'h');
    } else if (/sæculórum\.?$/.test(t)) {
      g += recite(t, finalCad, 'h');
    } else {
      g += recite(t, "i h g 'hg g", 'h');               // Per Christum Dóminum nostrum
    }
    return g + ' (::) ' + FIXED.amen;
  }
  // the blessing before a lesson: two clauses of one accent each (Regulae art. III § IV, 1)
  function blessing(text) {
    var syl = P.analyse(plain(text)), half = Math.floor(syl.length / 2), cut = 0, best = 99;
    syl.forEach(function (s, i) { if (s.last && i < syl.length - 2 && Math.abs(i + 1 - half) < best) { best = Math.abs(i + 1 - half); cut = i + 1; } });
    var words = plain(text).split(/\s+/), wc = syl.slice(0, cut).filter(function (s) { return s.last; }).length;
    return '(f3) ' + recite(words.slice(0, wc).join(' '), "'h fr f", 'h') + ' (;) ' + recite(words.slice(wc).join(' '), "'h fr f", 'h') + ' (::) ' + FIXED.amen;
  }
  function versicle(v, r, solemn) {
    var tail = solemn ? 'g. hGFE/fg/hg.' : null;
    var cad = solemn ? null : "'h fr f";
    var g = '(f3) <sp>V/</sp>. ' + recite(v, cad, 'h', {tail: tail}) + ' (::)';
    if (r) g += ' <sp>R/</sp>. ' + recite(r, cad, 'h', {tail: tail}) + ' (::)';
    return g;
  }

  // ---------------------------------------------------------------- segments of a Latin cell
  var SKIP_VS = /^(Deus ✠? ?in ad[ij]utórium|Dómine, exáudi|Benedicámus|Fidélium|Glória Patri|Dóminus vobíscum|[IJ]ube,? domne|Tu autem|Ad[ij]utórium nostrum|Convérte nos|Benedícat|Divínum auxílium)/;
  function isV(l) { return /^<r>℣\.<\/r>/.test(l); }
  function isR(l) { return /^<r>℟\.<\/r>/.test(l); }
  function body(l) { return plain(l.replace(/^<r>[^<]*<\/r>\s*/, '')); }

  // ctx: {hour, solemn (Lauds/Vespers), priest, title, rank (1..4), sunday, bvm, paschal, seasonLaus}
  function segments(lines, head, ctx) {
    var segs = [], n = lines.length, i, j;
    var inComm = false;
    for (i = 0; i < n; i++) {
      var l = lines[i], t = body(l);
      if (/^<r>Commemoratio/.test(l)) { inComm = true; continue; }
      // opening of the Hour
      if (isV(l) && /^Deus ?✠? ?in ad[ij]utórium/.test(t)) {
        j = i + 1;
        while (j < n && !/^(Allelúia|Laus tibi)/.test(plain(lines[j]))) j++;
        if (j >= n) continue;
        var laus = /^Laus/.test(plain(lines[j]));
        segs.push({s: i, e: j + 1, kind: 'inc', gabc: FIXED.deus + ' ' + (laus ? FIXED.laus.replace(/^\(c3\) /, '') : FIXED.alleluia)});
        i = j; continue;
      }
      if (isV(l) && /^Dómine, lábia/.test(t) && i + 1 < n && isR(lines[i + 1])) {
        segs.push({s: i, e: i + 2, kind: 'inc', gabc: FIXED.labia}); i++; continue;
      }
      if (isV(l) && /^[IJ]ube,? domne/.test(t) && i + 2 < n && /^<r>Benedictio\.<\/r>/.test(lines[i + 1]) && isR(lines[i + 2])) {
        segs.push({s: i, e: i + 3, kind: 'bl', gabc: FIXED.iube + ' ' + blessing(body(lines[i + 1])).replace(/^\(f3\) /, '')}); i += 2; continue;
      }
      if (isV(l) && /^(Tu autem|Et ne nos indúcas)/.test(t) && i + 1 < n && isR(lines[i + 1])) {
        segs.push({s: i, e: i + 2, kind: 'vs', gabc: versicle(t, body(lines[i + 1]), false)}); i++; continue;
      }
      if (/^Te Deum laudámus/.test(plain(l))) {
        j = i;
        while (j + 1 < n && plain(lines[j + 1])) j++;
        segs.push({s: i, e: j + 1, kind: 'td', file: 'Ta1-5'}); i = j; continue;
      }
      if (/^Fratres: Sóbrii estóte/.test(plain(l)) && i + 1 < n && isR(lines[i + 1]) && /Deo grátias/.test(plain(lines[i + 1]))) {
        segs.push({s: i, e: i + 2, kind: 'cap', gabc: FIXED.lectioCompl}); i++; continue;
      }
      if (isV(l) && /^Ad[ij]utórium nostrum/.test(t) && ctx.hour === 'Completorium' && i + 1 < n && isR(lines[i + 1])) {
        segs.push({s: i, e: i + 2, kind: 'inc', gabc: FIXED.adjutorium}); i++; continue;
      }
      if (isV(l) && /^Convérte nos/.test(t) && i + 1 < n && isR(lines[i + 1])) {
        segs.push({s: i, e: i + 2, kind: 'inc', gabc: FIXED.converte}); i++; continue;
      }
      // Dominus vobiscum / Domine exaudi, Oremus, the prayer, its conclusion, Amen
      if (isV(l) && /^(Dóminus vobíscum|Dómine, exáudi)/.test(t) && i + 1 < n && isR(lines[i + 1])) {
        var dv = /^Dóminus/.test(t), sol = ctx.solemn;
        var pre = dv ? (sol ? FIXED.dvSol : FIXED.dvSim) : (sol ? FIXED.deSol : FIXED.deSim);
        // is a prayer coming?
        j = i + 2;
        if (j < n && /Orémus/.test(plain(lines[j]))) {
          var k = j + 1, bodyTxt = [], concl = null;
          while (k < n && !isR(lines[k]) && plain(lines[k])) {
            var pl = plain(lines[k]);
            if (/^(Per |Qui vivis|Qui tecum|Qui cum Patre|Qui vivit)/.test(pl) && /sæculórum|nostrum\.?$/.test(pl)) concl = pl;
            else bodyTxt.push(pl);
            k++;
          }
          if (k < n && isR(lines[k]) && /Amen/.test(plain(lines[k]))) {
            var g = pre + ' ' + (sol ? FIXED.oremusSol : FIXED.oremusSim).replace(/^\(f3\) /, '') + ' ' +
              prayerBody(bodyTxt.join(' ')) + (concl ? conclusion(concl, sol) : FIXED.amen);
            segs.push({s: i, e: k + 1, kind: 'or', gabc: g}); i = k; continue;
          }
        }
        segs.push({s: i, e: i + 2, kind: 'vs', gabc: pre}); i++; continue;
      }
      // a prayer without a preceding versicle (commemorations): Oremus ... Amen
      if (/^(<c>O<\/c>)?rémus\.?$|^Orémus\.?$/.test(plain(l)) || plain(l) === 'Orémus.') {
        var k2 = i + 1, bt = [], cc = null;
        while (k2 < n && !isR(lines[k2]) && plain(lines[k2])) {
          var p2 = plain(lines[k2]);
          if (/^(Per |Qui vivis|Qui tecum|Qui cum Patre|Qui vivit)/.test(p2) && /sæculórum|nostrum\.?$/.test(p2)) cc = p2; else bt.push(p2);
          k2++;
        }
        if (k2 < n && isR(lines[k2]) && /Amen/.test(plain(lines[k2])) && bt.length) {
          var sol2 = ctx.solemn;
          segs.push({s: i, e: k2 + 1, kind: 'or', gabc: (sol2 ? FIXED.oremusSol : FIXED.oremusSim) + ' ' + prayerBody(bt.join(' ')) + (cc ? conclusion(cc, sol2) : FIXED.amen)});
          i = k2; continue;
        }
      }
      // Benedicamus Domino
      if (isV(l) && /^Benedicámus Dómino\.?$/.test(t) && i + 1 < n && isR(lines[i + 1])) {
        var bq = benedicamus(ctx);
        if (bq) { segs.push({s: i, e: i + 2, kind: 'ben', ben: bq}); i++; continue; }
      }
      // the chapter (and the short lesson's ending)
      if (/Capitulum/.test(head || '') && /^<r>[^<]*\d+:\d+[^<]*<\/r>$/.test(l.trim()) && i + 2 < n && isR(lines[i + 2]) && /Deo grátias/.test(plain(lines[i + 2]))) {
        segs.push({s: i + 1, e: i + 3, kind: 'cap', gabc: chapter(lines[i + 1])}); i += 2; continue;
      }
      // versicle and response
      if (isV(l) && i + 1 < n && isR(lines[i + 1]) && !SKIP_VS.test(t) && !/^Dómine,? ad ad[ij]uvándum/.test(body(lines[i + 1]))) {
        var solV = !inComm && !(head === 'Incipit');
        segs.push({s: i, e: i + 2, kind: 'vs', gabc: versicle(t, body(lines[i + 1]), solV)}); i++; continue;
      }
      if (isV(l) && /^Fidélium ánimæ/.test(t) && i + 1 < n && isR(lines[i + 1])) {
        segs.push({s: i, e: i + 2, kind: 'vs', gabc: versicle(t, body(lines[i + 1]), false)}); i++; continue;
      }
    }
    return segs;
  }
  function benedicamus(ctx) {
    if (!ctx.solemn) return {gabc: FIXED.benFin};
    if (ctx.paschal) return null;                       // the Paschal forms are not yet transcribed: text
    var r = ctx.rank;
    if (r === 1) return {id: ctx.bvm ? BEN.BVM : BEN.I};
    if (ctx.sunday) return {id: r === 1 ? BEN.domMaior : BEN.domMinor};
    if (r === 2) return {id: BEN.II};
    if (r === 3) return {id: ctx.bvmSat ? BEN.simplex : BEN.III};
    return {id: BEN.feria};
  }

  window.OPTones = {segments: segments, FIXED: FIXED, BEN: BEN, recite: recite, chapter: chapter, versicle: versicle, conclusion: conclusion};
})();
