/* Booklets for any day: Choir Book, Priest's Missal, Congregation Booklet (A4, printed from the browser).
   booklet.html?b=choir|priest|cong#<the Mass page's hash>
   Everything is laid out here into explicit A4 pages, so that page numbers (contents, footers) are known. */
(function () {
  'use strict';
  var MM = 96 / 25.4;
  var G = {pageW: 210 * MM, pageH: 297 * MM, top: 19 * MM, bot: 24 * MM, side: 21 * MM, gap: 7 * MM};
  G.bodyW = G.pageW - 2 * G.side; G.bodyH = G.pageH - G.top - G.bot; G.colW = (G.bodyW - G.gap) / 2;
  var CANON = {w: 120 * MM, h: 201 * MM};
  var GOLD = '#BD9E5E', DEEP = '#8A7140';
  var params = new URLSearchParams(location.search);
  var BOOK = {choir: 'choir', priest: 'priest', cong: 'cong', congregation: 'cong', missal: 'priest'}[params.get('b') || 'choir'] || 'choir';
  var BOOK_NAME = {choir: 'Choir Book', priest: 'Priest’s Missal', cong: 'Congregation Booklet'}[BOOK];
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  function el(tag, a, kids) {
    var n = document.createElement(tag);
    if (a) Object.keys(a).forEach(function (k) {
      if (a[k] == null || a[k] === false) return;
      if (k === 'text') n.textContent = a[k]; else if (k === 'html') n.innerHTML = a[k]; else n.setAttribute(k, a[k]);
    });
    (kids || []).forEach(function (c) { if (c == null) return; n.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return n;
  }

  // ------------------------------------------------------------------ units
  // A unit is one block that is never split: a heading, a picture, a paragraph, one line of chant.
  // keep: stays on the same page/column as the unit after it.
  var A, D, S, M, R, ORD, units = [], pending = [];
  function U(node, o) { o = o || {}; var u = {n: node, keep: !!o.keep, tight: !!o.tight, brk: o.brk || '', sect: o.sect || null, toc: o.toc || null, id: 'u' + units.length}; units.push(u); return u; }
  function section(kind) { U(el('div'), {brk: 'section', sect: kind}); }

  function diamond() { return el('div', {class: 'b-dia'}, [el('span')]); }
  function heading(title, sub, o) {
    o = o || {};
    var n = el('div', {class: 'b-head'}, [el('div', {class: 'b-title', text: title}), sub ? el('div', {class: 'b-sub', text: sub}) : null, diamond()]);
    return U(n, {keep: true, toc: o.toc || null});
  }
  function rubric(t, o) { var u = U(el('p', {class: 'b-rub' + (o && o.left ? ' left' : ''), text: t}), {keep: !(o && o.nokeep)}); if (o && o.nokeep) u.after = true; return u; }
  function posture(t) { return U(el('p', {class: 'b-post', text: t}), {keep: true}); }
  function art(file, o) {
    o = o || {};
    var arch = /_arch/.test(file);
    var n = el('div', {class: 'b-art ' + (arch ? 'arch' : 'sq') + (o.size ? ' ' + o.size : '')}, [el('div', {class: 'frame'}, [el('img', {src: 'art/' + file + '.jpg', alt: ''})])]);
    if (o.caption) n.appendChild(el('div', {class: 'b-cap', text: o.caption}));
    return U(n, {keep: true});
  }

  // text paragraphs: long ones are cut at sentences so that they can run on to the next column
  function sentences(t) { return t.match(/[^.:;!?]+[.:;!?]+[»”’)]*\s*|[^.:;!?]+$/g) || [t]; }
  function chunks(t, max) {
    if (t.length <= max) return [t];
    var ss = sentences(t), out = [], cur = '';
    ss.forEach(function (s) { if (cur && (cur + s).length > max) { out.push(cur.trim()); cur = ''; } cur += s; });
    if (cur.trim()) out.push(cur.trim());
    return out;
  }
  function mark(w) { return w ? el('span', {class: 'b-mk', text: w + ' '}) : null; }
  function para(t, o) {
    o = o || {};
    t = J(t);
    chunks(t, o.max || 420).forEach(function (c, i) {
      U(el('p', {class: 'b-p' + (o.cls ? ' ' + o.cls : '') + (i ? ' cont' : '')}, [i ? null : mark(o.mark), c]), {keep: o.keep && i === 0});
    });
  }
  // Latin | English side by side (congregation booklet)
  function pair(la, en, o) {
    o = o || {};
    la = J(la);
    var n = Math.max(1, Math.ceil(Math.max(la.length, en.length * 0.9) / 380));
    var a = splitN(la, n), b = splitN(en, n);
    for (var i = 0; i < n; i++) {
      U(el('div', {class: 'b-pair' + (i ? ' cont' : '') + (o.cls ? ' ' + o.cls : '')}, [
        el('p', {class: 'la'}, [i ? null : mark(o.mk), a[i] || '']),
        el('p', {class: 'en'}, [i ? null : mark(o.mkEn || o.mk), b[i] || ''])]), {keep: o.keep && i === 0});
    }
  }
  // the Missal's spelling: consonantal i as j (Jesu, ejus, adjuvándo)
  function J(t) {
    return String(t || '').replace(/\b([Ii])(?=[aeouáéóúæ])/g, function (m, c) { return c === 'I' ? 'J' : 'j'; })
      .replace(/([aeouáéóúæ])i(?=[aeouáéóú])/g, '$1j').replace(/\b(ad|con|in|sub|ab|ob)i(?=[uú])/gi, '$1j')
      .replace(/allelúja/g, 'allelúia').replace(/Allelúja/g, 'Allelúia');
  }
  function splitN(t, n) {
    if (n <= 1) return [t];
    var ss = sentences(t), total = t.length, out = [], cur = '', k = 1;
    ss.forEach(function (s) { cur += s; if (k < n && (t.indexOf(cur) >= 0) && out.join('').length + cur.length >= total * k / n) { out.push(cur.trim()); cur = ''; k++; } });
    out.push(cur.trim());
    while (out.length < n) out.push('');
    return out;
  }

  // ------------------------------------------------------------------ chant
  function chantCtx(o) {
    var w = o.width;
    return {font: "'EB Garamond', serif", size: o.size || 17, dropSize: o.drop || 50, dropFont: "'EB Garamond', serif", dropColor: GOLD,
      rubric: GOLD, lines: GOLD, glyph: o.glyph, width: w, noAnno: true, noDrop: !!o.noDrop};
  }
  // placeholder unit; the lines become units of their own after drawing
  function chant(id, o) {
    o = o || {};
    var box = el('div', {class: 'b-chant'});
    var u = U(box, {keep: false});
    u.chant = true;
    var w = o.width || colWidth();
    pending.push(A.loadGabc(id).then(function (t) {
      var g = A.splitGabc(t), body = g.body;
      if (o.fix) body = o.fix(body);
      if (o.part === 'in' && A.fullIntroit) body = A.fullIntroit(body, g.header, A.state && A.state().key);
      return A.renderInto(box, body, g.header, o.part || null, chantCtx({width: w, size: o.size, glyph: o.glyph, drop: o.drop, noDrop: o.noDrop})).then(function () {
        if (o.initial) initialImage(box, o.initial);
      });
    }).catch(function (e) { box.appendChild(el('p', {class: 'b-err', text: 'Chant ' + id + ' could not be drawn: ' + e.message})); }));
    return u;
  }
  function gabcInline(gabc, o) {
    o = o || {};
    var box = el('div', {class: 'b-chant'}), u = U(box); u.chant = true;
    var w = o.width || colWidth();
    pending.push(A.renderInto(box, gabc, {}, null, chantCtx({width: w, size: o.size, glyph: o.glyph, noDrop: true})));
    return u;
  }
  // a manuscript initial in place of the drawn initial letter
  function initialImage(box, file) {
    var svg = box.querySelector('svg'); if (!svg) return;
    var cap = svg.querySelector('text.dropCap');
    if (!cap) return;
    try {
      var b0 = cap.getBBox(), cx = parseFloat(cap.getAttribute('x')), s = Math.max(2 * cx - 6, b0.height);
      var b = {x: cx - s / 2, width: s, y: b0.y + b0.height - s, height: s};
      var img = document.createElementNS('http://www.w3.org/2000/svg', 'image');
      img.setAttribute('href', 'art/' + file + '.jpg'); img.setAttributeNS('http://www.w3.org/1999/xlink', 'href', 'art/' + file + '.jpg');
      img.setAttribute('x', b.x); img.setAttribute('y', b.y); img.setAttribute('width', s); img.setAttribute('height', s);
      img.setAttribute('preserveAspectRatio', 'xMidYMid slice');
      var r = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      ['x', 'y', 'width', 'height'].forEach(function (k) { r.setAttribute(k, img.getAttribute(k)); });
      r.setAttribute('fill', 'none'); r.setAttribute('stroke', GOLD); r.setAttribute('stroke-width', '1');
      cap.style.display = 'none';
      cap.parentNode.appendChild(img); cap.parentNode.appendChild(r);
      var vb = svg.getAttribute('viewBox').split(/\s+/).map(Number);
      if (b.y < vb[1]) { var d = vb[1] - b.y + 2; vb[1] -= d; vb[3] += d; svg.setAttribute('viewBox', vb.join(' ')); }
    } catch (e) {}
  }

  var curCols = 1;
  function colWidth() { return curCols === 2 ? G.colW : curCols === 'canon' ? CANON.w : G.bodyW; }

  // ------------------------------------------------------------------ texts of the day
  function iso(d) { return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function dateLine(d) { return DAYS[d.getDay()] + ', ' + d.getDate() + ' ' + MONTHS[d.getMonth()] + ' ' + d.getFullYear(); }
  function feastLatin() {
    var t = A.clean(M.title).replace(/^\d+ [A-Za-z.]+ — /, '').replace(/FestivitaS/g, 'Festivitas');
    return FIX[S.key] ? FIX[S.key][0] : t;
  }
  function feastEnglish() { return FIX[S.key] ? FIX[S.key][1] : (M.name_en || A.clean(M.en || '') || feastLatin()); }
  var FIX = {S1112: ['In Festivitate Omnium Sanctorum Ordinis Prædicatorum', 'Feast of All Saints of the Order of Preachers']};
  function rankLine() {
    var r = M.rank, cls = {I: 'I classis', II: 'II classis', III: 'III classis', IV: 'IV classis'}[r] || '';
    var form = {solemn: 'Missa solemnis', sung: 'Missa cantata', low: 'Missa lecta'}[S.ordo] || 'Missa solemnis';
    return (cls ? 'Festum ' + cls + ' · ' : '') + form;
  }
  function formEn() { return {solemn: 'Solemn Mass', sung: 'Sung Mass', low: 'Low Mass'}[S.ordo] || 'Solemn Mass'; }

  var BOOKS_LA = [
    [/^Ad Romanos/, 'Léctio Epístolæ beáti Pauli Apóstoli ad Romános.', 'A Lesson from the Epistle of blessed Paul the Apostle to the Romans.', 'Fratres:', 'Brethren:'],
    [/^Ad Corinthios/, 'Léctio Epístolæ beáti Pauli Apóstoli ad Corínthios.', 'A Lesson from the Epistle of blessed Paul the Apostle to the Corinthians.', 'Fratres:', 'Brethren:'],
    [/^Ad Galatas/, 'Léctio Epístolæ beáti Pauli Apóstoli ad Gálatas.', 'A Lesson from the Epistle of blessed Paul the Apostle to the Galatians.', 'Fratres:', 'Brethren:'],
    [/^Ad Ephesios/, 'Léctio Epístolæ beáti Pauli Apóstoli ad Ephésios.', 'A Lesson from the Epistle of blessed Paul the Apostle to the Ephesians.', 'Fratres:', 'Brethren:'],
    [/^Ad Philippenses/, 'Léctio Epístolæ beáti Pauli Apóstoli ad Philippénses.', 'A Lesson from the Epistle of blessed Paul the Apostle to the Philippians.', 'Fratres:', 'Brethren:'],
    [/^Ad Colossenses/, 'Léctio Epístolæ beáti Pauli Apóstoli ad Colossénses.', 'A Lesson from the Epistle of blessed Paul the Apostle to the Colossians.', 'Fratres:', 'Brethren:'],
    [/^Ad Thessalonicenses/, 'Léctio Epístolæ beáti Pauli Apóstoli ad Thessalonicénses.', 'A Lesson from the Epistle of blessed Paul the Apostle to the Thessalonians.', 'Fratres:', 'Brethren:'],
    [/^Ad Timotheum/, 'Léctio Epístolæ beáti Pauli Apóstoli ad Timótheum.', 'A Lesson from the Epistle of blessed Paul the Apostle to Timothy.', 'Caríssime:', 'Dearly beloved:'],
    [/^Ad Titum/, 'Léctio Epístolæ beáti Pauli Apóstoli ad Titum.', 'A Lesson from the Epistle of blessed Paul the Apostle to Titus.', 'Caríssime:', 'Dearly beloved:'],
    [/^Ad Hebr/, 'Léctio Epístolæ beáti Pauli Apóstoli ad Hebrǽos.', 'A Lesson from the Epistle of blessed Paul the Apostle to the Hebrews.', 'Fratres:', 'Brethren:'],
    [/^Jacobi/, 'Léctio Epístolæ beáti Jacóbi Apóstoli.', 'A Lesson from the Epistle of blessed James the Apostle.', 'Caríssimi:', 'Dearly beloved:'],
    [/^Petri/, 'Léctio Epístolæ beáti Petri Apóstoli.', 'A Lesson from the Epistle of blessed Peter the Apostle.', 'Caríssimi:', 'Dearly beloved:'],
    [/^Joannis/, 'Léctio Epístolæ beáti Joánnis Apóstoli.', 'A Lesson from the Epistle of blessed John the Apostle.', 'Caríssimi:', 'Dearly beloved:'],
    [/^Actus/, 'Léctio Actuum Apostolórum.', 'A Lesson from the Acts of the Apostles.', 'In diébus illis:', 'In those days:'],
    [/^Apocalypsis/, 'Léctio libri Apocalýpsis beáti Joánnis Apóstoli.', 'A Lesson from the Book of the Apocalypse of blessed John the Apostle.', 'In diébus illis:', 'In those days:'],
    [/^(Sapientia|Ecclesiasticus|Proverbia|Canticum)/, 'Léctio libri Sapiéntiæ.', 'A Lesson from the Book of Wisdom.', '', ''],
    [/^Isaias/, 'Léctio Isaíæ Prophétæ.', 'A Lesson from Isaias the Prophet.', 'In diébus illis:', 'In those days:'],
    [/^Jeremias/, 'Léctio Jeremíæ Prophétæ.', 'A Lesson from Jeremias the Prophet.', 'In diébus illis:', 'In those days:'],
    [/^Ezechiel/, 'Léctio Ezechiélis Prophétæ.', 'A Lesson from Ezechiel the Prophet.', 'In diébus illis:', 'In those days:'],
    [/^Daniel/, 'Léctio Daniélis Prophétæ.', 'A Lesson from Daniel the Prophet.', 'In diébus illis:', 'In those days:'],
    [/^Joel/, 'Léctio Joélis Prophétæ.', 'A Lesson from Joel the Prophet.', '', ''],
    [/^Osee/, 'Léctio Oséæ Prophétæ.', 'A Lesson from Osee the Prophet.', '', ''],
    [/^Malachias/, 'Léctio Malachíæ Prophétæ.', 'A Lesson from Malachias the Prophet.', '', ''],
    [/^Zacharias/, 'Léctio Zacharíæ Prophétæ.', 'A Lesson from Zacharias the Prophet.', '', ''],
    [/^Genesis/, 'Léctio libri Genesis.', 'A Lesson from the Book of Genesis.', 'In diébus illis:', 'In those days:'],
    [/^Exodus/, 'Léctio libri Exodi.', 'A Lesson from the Book of Exodus.', 'In diébus illis:', 'In those days:'],
    [/^Esther/, 'Léctio libri Esther.', 'A Lesson from the Book of Esther.', 'In diébus illis:', 'In those days:'],
    [/^Tobi/, 'Léctio libri Tobíæ.', 'A Lesson from the Book of Tobias.', 'In diébus illis:', 'In those days:'],
    [/^Judith/, 'Léctio libri Judith.', 'A Lesson from the Book of Judith.', 'In diébus illis:', 'In those days:'],
    [/^Regum/, 'Léctio libri Regum.', 'A Lesson from the Book of Kings.', 'In diébus illis:', 'In those days:'],
    [/^Machab/, 'Léctio libri Machabæórum.', 'A Lesson from the Book of Machabees.', 'In diébus illis:', 'In those days:']];
  var GOSPEL = {Matthæus: ['Matthǽum', 'Matthew'], Marcus: ['Marcum', 'Mark'], Lucas: ['Lucam', 'Luke'], Joannes: ['Joánnem', 'John']};
  function readingHead(r) {
    if (r.type === 'Gospel') {
      var g = GOSPEL[r.ref.split(' ')[0]] || ['', ''];
      return {la: 'Sequéntia sancti Evangélii secúndum ' + g[0] + '.', en: 'The continuation of the holy Gospel according to ' + g[1] + '.', open: 'In illo témpore:', openEn: 'At that time:'};
    }
    var b = BOOKS_LA.filter(function (x) { return x[0].test(r.ref); })[0];
    if (!b) return {la: 'Léctio.', en: 'A Lesson.', open: '', openEn: ''};
    return {la: b[1], en: b[2], open: b[3], openEn: b[4]};
  }
  function shortRef(ref) {
    var m = /^(.*?)\s*(\d+):\s*(.*)$/.exec(ref); if (!m) return ref;
    var b = m[1].replace(/^Ad Corinthios (\d)/, '$1 Cor.').replace(/^Ad Thessalonicenses (\d)/, '$1 Thess.').replace(/^Ad Timotheum (\d)/, '$1 Tim.')
      .replace(/^Petri (\d)/, '$1 Pet.').replace(/^Joannis (\d)/, '$1 John').replace(/^Ad Romanos/, 'Rom.').replace(/^Ad Galatas/, 'Gal.')
      .replace(/^Ad Ephesios/, 'Eph.').replace(/^Ad Philippenses/, 'Phil.').replace(/^Ad Colossenses/, 'Col.').replace(/^Ad Titum/, 'Tit.').replace(/^Ad Hebræos/, 'Heb.')
      .replace(/^Matthæus/, 'Matth.').replace(/^Marcus/, 'Mark').replace(/^Lucas/, 'Luke').replace(/^Joannes/, 'John');
    return b + ' ' + m[2] + ', ' + m[3];
  }
  var EVANGELIST = function () {
    var g = (S._gos || {}).ref || ''; var k = g.split(' ')[0];
    return {Matthæus: 'Matthǽum', Marcus: 'Marcum', Lucas: 'Lucam', Joannes: 'Joánnem'}[k] || null;
  };

  // the readings and the proper texts are loaded first, so that the layout is synchronous
  var TX = {};
  function preload(seq) {
    var jobs = [];
    seq.forEach(function (it) {
      if (it.t === 'read') {
        if (it.r.type === 'Gospel') S._gos = it.r;
        jobs.push((it.r.la ? Promise.resolve([it.r.la, it.r.en || '']) : Promise.all([A.readingText('la', it.r.ref), A.readingText('en', it.r.ref)])).then(function (v) { TX['r:' + it.r.ref] = v; }));
      }
      if (it.t === 'chant') jobs.push(A.chantLatin(it.c.id).then(function (t) { TX['c:' + it.c.id] = t; }));
    });
    return Promise.all(jobs);
  }
  function chantEn(id) { var t = D.trans[id]; return t ? t.t : ''; }
  function chantRef(id) { var t = D.trans[id]; return t && t.r ? t.r.replace(/,\s*[\d\-–, ]+$/, '') : ''; }
  function modeOf(id) { return null; }

  var PART_LA = {in: 'Officium', gr: 'Responsorium', al: 'Alleluia', tr: 'Tractus', se: 'Sequentia', of: 'Offertorium', co: 'Communio', pr: 'Ante Missam', ad: 'Ad adorationem Crucis', an: 'Ad Vesperas'};
  var PART_EN = {in: 'Introit', gr: 'Gradual', al: 'Alleluia', tr: 'Tract', se: 'Sequence', of: 'Offertory', co: 'Communion', pr: 'Before Mass', ad: 'Adoration of the Cross', an: 'Vespers'};
  var ORD_LA = {as: 'Asperges', ky: 'Kyrie', gl: 'Gloria', cr: 'Credo', sa: 'Sanctus', ag: 'Agnus Dei', it: 'Ite, missa est'};
  var PART_ART = {gr: 'catherine_arch', of: 'peter_martyr_arch', co: 'last_supper_arch', sa: 'sano_virgin_arch'};

  function ordSub(id) {
    var c = D.chants[id]; if (!c) return '';
    var m = /\b([IVX]+)\b/.exec(c.i), n = m ? m[1] : '';
    var extra = /\(([^)]+)\)/.exec(c.i);
    return (n ? 'Ordinarium ' + n : A.clean(c.i)) + (extra ? ' · ' + extra[1] : '') + (c.pg ? ' · p. ' + c.pg : '');
  }
  function ordName(id) { var c = D.chants[id]; return c ? A.clean(c.i) : ''; }
  function propSub(id, c) {
    var ref = chantRef(id), ch = D.chants[id], bits = [];
    if (ref) bits.push(ref);
    if (ch && ch.m) bits.push('Mode ' + ch.m);
    if (ch && ch.pg) bits.push('Grad. O.P. p. ' + ch.pg);
    return bits.join(' · ');
  }
  function incipit(id) { var c = D.chants[id]; return c ? A.clean(c.i).replace(/\.\.\..*$/, '').replace(/\s*\(.*$/, '') : ''; }

  // ================================================================== CHOIR BOOK
  var TOC = [];
  function tocEntry(label, it) { var e = {label: label, it: it}; TOC.push(e); return e; }
  function buildChoir(seq) {
    curCols = 1;
    var gloriaPatri = function (id) { return /Gl[oó]ria Patri/.test(TX['c:' + id] || ''); };
    var ini = {in: 'init_g_dominic', al: 'init_a_angel'};
    seq.forEach(function (it) {
      if (it.t === 'chant') {
        var p = it.p, id = it.c.id; if (!id) return;
        var head = heading(PART_LA[p] || p, propSub(id), {toc: tocEntry(PART_LA[p] + ' ', null)});
        head.toc.it = head; head.toc.label = [PART_LA[p] + ' ', el('i', {text: incipit(id)})];
        if (PART_ART[p]) art(PART_ART[p]);
        var file = ini[p], first = (TX['c:' + id] || '').trim().charAt(0).toUpperCase();
        var useIni = file && ((p === 'in' && first === 'G') || (p === 'al' && first === 'A'));
        chant(id, {part: p, initial: useIni ? file : null, drop: useIni ? 54 : 50});
        if (p === 'al' && !/Allel[uú]ia\.?\s*$/.test((TX['c:' + id] || '').trim())) rubric('After the verse the Allelúia is repeated.', {nokeep: true});
        if (p === 'of' && !A.paschal() && /T\.\s*P\./.test(TX['c:' + id] || '')) rubric('Outside Paschaltide, sung without the Allelúia.', {nokeep: true});
        return;
      }
      if (it.t === 'ord') {
        var oid = ORD[it.k]; if (!oid) return;
        var h = heading(ORD_LA[it.k], ordSub(oid)); h.toc = tocEntry(ordName(oid), h);
        if (it.k === 'gl') rubric('The celebrant intones Glória in excélsis Deo, the choir continues at Et in terra pax.');
        if (it.k === 'cr') { art('init_prophet', {size: 'small'}); rubric('The celebrant intones Credo in unum Deum, the choir continues at Patrem omnipoténtem.'); }
        if (it.k === 'sa') art('sano_virgin_arch');
        if (it.k === 'it') rubric(/Benedicamus/.test(ordName(oid)) ? 'The deacon sings Benedicámus Dómino, the choir answers Deo grátias.' : 'The deacon sings Ite, missa est, the choir answers Deo grátias.');
        chant(oid, {part: null, noDrop: it.k === 'it' || it.k === 'gl' || it.k === 'cr' ? false : false});
        return;
      }
      if (it.t === 'ordo' && it.k === 'collect') {
        heading('Ad Orationes', 'Modus respondendi · p. 146*');
        rubric('Before the Collect (I); after the Postcommunion (II, In fine).');
        chant(A.findKyriale('Ad Orationes I'), {noDrop: true});
        rubric('In fine'); chant(A.findKyriale('Ad Orationes II'), {noDrop: true});
        return;
      }
      if (it.t === 'ordo' && it.k === 'gospel') {
        heading('Ad Evangelium', 'Modus respondendi · p. 147*');
        var ev = EVANGELIST();
        chant(A.findKyriale('Ad Evangelium'), {noDrop: true, fix: function (b) {
          var r = {'Matthǽum': 'Mat(h)thǽ(g)um.(g)', 'Marcum': 'Mar(g)cum.(g)', 'Lucam': 'Lu(g)cam.(g)', 'Joánnem': 'Jo(h)án(g)nem.(g)'}[ev];
          return r ? b.replace('Lu(g)cam.(g)', r) : b;
        }});
        return;
      }
      if (it.t === 'pref') {
        var solemn = R.gloria && !R.requiem;
        heading('Ad Præfationem', (solemn ? 'In tono solemni' : 'In tono feriali') + ' · p. 147*');
        chant(A.findKyriale(solemn ? 'Ad Praefationem in tono solemni' : 'Ad Praefationem in tono feriali'), {noDrop: true});
        return;
      }
      if (it.t === 'ordo' && it.k === 'pater') {
        heading('Ad Pater noster · Ad Pax Domini', 'Modus respondendi · p. 148*');
        chant(A.findKyriale('Ad Pater noster'), {noDrop: true});
        chant(A.findKyriale('Ad Pax Domini'), {noDrop: true});
      }
    });
    creditsUnit();
  }
  // ================================================================== ORDO helpers (priest, congregation)
  var MODE = function () { return {low: 'l', sung: 's', solemn: 'm'}[S.ordo] || 'm'; };
  function ordoLines(k) {
    var O = window.ORDO, sec, lines;
    if (k === 'dismiss') { lines = O.dismiss[R.requiem ? 'req' : R.dismiss === 'ite' ? 'ite' : 'ben']; sec = {la: 'Dimissio', en: 'Dismissal'}; }
    else { sec = O[k]; if (!sec) return null; lines = sec.lines; }
    var md = MODE();
    lines = (lines || []).filter(function (l) { return !l.m || l.m.indexOf(md) >= 0; });
    return {la: sec.la, en: sec.en, lines: lines};
  }
  var WHO = {P: 'S.', S: 'M.', D: 'D.', C: ''};
  var WHO_EN = {P: 'P.', S: 'M.', D: 'D.', C: ''};
  function lineMark(l, en) {
    if (!l.w || /^(℟|℣|Ant\.)/.test(l.la || '')) return '';
    return (en ? WHO_EN : WHO)[l.w] || '';
  }

  // ================================================================== PRIEST'S MISSAL
  function buildPriest(seq) {
    curCols = 2;
    var mk = function (l) { return lineMark(l); };
    var ordoSec = function (k, title) {
      var s = ordoLines(k); if (!s) return;
      if (title !== false) heading(title || s.la, null);
      s.lines.forEach(function (l, i) {
        if (l.r) { rubric(l.r, {left: true}); return; }
        if (l.read) return;
        var ev = EVANGELIST();
        para(ev ? l.la.replace(/secúndum N\./, 'secúndum ' + ev + '.') : l.la, {mark: mk(l), cls: 'pr'});
      });
    };
    var sung = S.ordo !== 'low';
    seq.forEach(function (it) {
      if (it.t === 'ordo') {
        if (it.k === 'canon') { canonPages(); curCols = 2; return; }
        if (it.k === 'pater' && sung) {
          heading('Pater noster', null);
          // Missale O.P. 1939, Appendix: the ferial chant in feasts of three lessons, on ferias and in Masses for the Dead
          var pc = A.isTemporal(S.key) ? A.temporalClass(S.key, S.date) : A.feastClass(S.key), ptSol = !R.requiem && pc <= 3;
          rubric('The priest sings (' + (ptSol ? 'solemn' : 'ferial') + ' chant):', {left: true});
          chant(ptSol ? 'op-m39-pater-solemn' : 'op-m39-pater-ferial', {noDrop: true, glyph: 1 / 19, size: 14});
          var s = ordoLines('pater');
          var after = false;
          s.lines.forEach(function (l) {
            if (/^Líbera nos/.test(l.la || '')) after = true;
            if (!after) return;
            if (l.r) { rubric(l.r, {left: true}); return; }
            // the Pax chant (Appendix) begins with Per omnia ... Amen and ends with Et cum spiritu tuo
            if (/^Pax\s*✠?\s*Dómini/.test(l.la || '')) { chant('op-m39-pax', {noDrop: true, glyph: 1 / 19, size: 14}); return; }
            if (/^Per ómnia sǽcula sæculórum\.?\s*(℟\.\s*)?(Amen\.?)?$/.test(l.la || '') || /^(℟\.\s*)?Amen\.?$/.test(l.la || '') || /^(℟\.\s*)?Et cum spíritu tuo/.test(l.la || '')) return;
            para(l.la, {mark: mk(l), cls: 'pr'});
          });
          return;
        }
        if (it.k === 'collect') {
          heading('Oratio', null);
          var s2 = ordoLines('collect');
          s2.lines.forEach(function (l) { if (l.r) rubric(l.r, {left: true}); });
          if (sung) chant(A.findKyriale('Ad Orationes I'), {noDrop: true, glyph: 1 / 19, size: 14});
          else para('Dóminus vobíscum. ℟. Et cum spíritu tuo. Orémus.', {cls: 'pr'});
          return;
        }
        if (it.k === 'collectEnd' || it.k === 'offertoryEnd' || it.k === 'postEnd') { ordoSec(it.k, false); return; }
        if (it.k === 'post') { heading('Postcommunio', null); ordoSec('post', false); return; }
        ordoSec(it.k);
        return;
      }
      if (it.t === 'oratio') {
        if (it.k === 'sp') { heading('Oratio super populum', null); para('Orémus. ℣. Humiliáte cápita vestra Deo.', {cls: 'pr'}); }
        // sung in the solemn tone of the prayers (Harrison 1920); said at a Low Mass
        var og = null;
        try { og = sung && window.OPMassTones ? OPMassTones.oration(J(it.x[0])) : null; } catch (e) { console.warn('tone', e); }
        if (og) { gabcInline(og, {size: 14, glyph: 1 / 19}); return; }
        para(it.x[0], {cls: 'pr'}); para('℟. Amen.', {cls: 'pr'}); return;
      }
      if (it.t === 'chant') {
        var p = it.p, id = it.c.id; if (!id) return;
        heading(PART_LA[p] || p, chantRef(id));
        para(TX['c:' + id] || '', {cls: 'pr'});
        return;
      }
      if (it.t === 'ord') {
        var oid = ORD[it.k]; if (!oid) return;
        if (it.k === 'gl' || it.k === 'cr') {
          heading(ORD_LA[it.k], null);
          if (sung) { rubric('The celebrant intones:', {left: true}); intonation(oid); }
          var low = ordoLines(it.k + 'Low');
          if (low) low.lines.forEach(function (l) { if (!l.r) para(l.la, {cls: 'pr'}); });
          return;
        }
        if (it.k === 'sa' || it.k === 'ag' || it.k === 'ky') {
          var lw = ordoLines(it.k + 'Low'); if (!lw) return;
          heading(ORD_LA[it.k], null);
          lw.lines.forEach(function (l) { if (l.r) rubric(l.r, {left: true}); else para(l.la, {cls: 'pr', mark: mk(l)}); });
          return;
        }
        if (it.k === 'it') {
          heading(ordName(oid).replace(/\s+[IVX]+.*$/, ''), null);
          rubric('The deacon sings (at a Sung Mass the priest):', {left: true});
          chant(oid, {noDrop: true, glyph: 1 / 19, size: 14});
        }
        return;
      }
      if (it.t === 'read') { reading(it.r, false); return; }
      if (it.t === 'pref') { preface(); return; }
    });
    curCols = 2;
    creditsUnit();
  }
  function intonation(id) {
    pending.push(A.loadGabc(id).then(function (t) {
      var b = A.splitGabc(t).body, m = /^([\s\S]*?\((?:[a-m]\d)\)[\s\S]*?)(\(;\)|\(:\)|\(::\)|\(,\))/.exec(b);
      var clef = (/\(([cf][1-4])\)/.exec(b) || [, 'c4'])[1];
      // the intonation ends where the choir takes over: Et in terra pax / Patrem omnipotentem
      var cut = b.search(/\s(Et|Pa)\(/);
      var into = cut > 0 ? b.slice(0, cut) + ' (::)' : (m ? m[1] + '(::)' : b);
      return into;
    }).then(function (g) { return g; }));
    // drawn in order: a placeholder chant that reads the intonation when it is drawn
    var box = el('div', {class: 'b-chant'}), u = U(box); u.chant = true;
    var w = colWidth();
    pending.push(A.loadGabc(id).then(function (t) {
      var b = A.splitGabc(t).body, cut = b.search(/\s(Et|Pa)\(/);
      var g = cut > 0 ? b.slice(0, cut) + ' (::)' : b;
      return A.renderInto(box, g, {}, null, chantCtx({width: w, size: 14, glyph: 1 / 19, noDrop: true}));
    }));
  }
  function reading(r, cong) {
    var v = TX['r:' + r.ref] || ['', ''], h = readingHead(r), gos = r.type === 'Gospel';
    var laT = v[0] || '', enT = v[1] || '';
    var dupOpen = h.open && laT.replace(/[^A-Za-z ]/g, '').toLowerCase().indexOf(h.open.replace(/[^A-Za-z ]/g, '').toLowerCase().trim()) === 0;
    var la = (h.open && !dupOpen ? h.open + ' ' : '') + laT, en = (h.openEn ? h.openEn + ' ' : '') + enT;
    if (!cong) {
      heading(gos ? 'Evangelium' : (r.type === 'Lesson' ? 'Lectio' : 'Epistola'), shortRef(r.ref));
      // the Gospel's greeting and title are in the Order of Mass just before
      if (BOOK === 'priest' && S.ordo !== 'low' && window.OPMassTones && la) {
        // the Epistle and Gospel tones of the Order (Harrison 1920, ch. VI 5-6)
        var tg = null, rg = null;
        try { tg = gos ? null : OPMassTones.epistleTitle(J(h.la)); rg = OPMassTones.reading(J(la), gos); } catch (e) { console.warn('tone', e); }
        if (tg) gabcInline(tg, {size: 14, glyph: 1 / 19});
        if (rg) gabcInline(rg, {size: 14, glyph: 1 / 19}); else para(la, {cls: 'pr', max: 360});
      } else {
        if (!gos) para(h.la, {cls: 'pr i'});
        para(la, {cls: 'pr', max: 360});
      }
      para(gos ? '℟. Laus tibi, Christe.' : '℟. Deo grátias.', {cls: 'pr'});
      return;
    }
    heading(gos ? 'Gospel · Evangelium' : (r.type === 'Lesson' ? 'Lesson · Lectio' : 'Epistle · Epistola'), shortRef(r.ref));
    art(gos ? 'st_matthew_arch' : 'st_paul_arch', {size: 'small'});
    posture(gos ? 'All stand' : 'All sit');
    if (gos) pair('℣. Dóminus vobíscum. ℟. Et cum spíritu tuo. ℣. ' + h.la + ' ℟. Glória tibi, Dómine.', '℣. The Lord be with you. ℟. And with thy spirit. ℣. ' + h.en + ' ℟. Glory be to thee, O Lord.');
    else pair(h.la, h.en, {cls: 'i'});
    pair(la, en);
    pair(gos ? '℟. Laus tibi, Christe.' : '℟. Deo grátias.', gos ? '℟. Praise be to thee, O Christ.' : '℟. Thanks be to God.');
  }
  function preface() {
    var name = A.prefaceOf(S.key, S.date); if (!name) return;
    var P = A.prefaceText(name, S.key, S.date), solemn = R.gloria && !R.requiem;
    heading('Præfatio', P.name);
    if (BOOK === 'priest') {
      var PC = A.prefaceChant(name, S.key, S.date);
      if (S.ordo !== 'low' && PC) {
        if (name === 'Dominico') art('tiepolo_arch', {size: 'small'});
        chant(PC.id, {noDrop: true, glyph: 1 / 19, size: 14, fix: PC.fix});
        if (PC.adapted) rubric('No chant is printed in the Missal for this Preface; its text is here fitted to the solemn tone.', {left: true});
      } else {
        if (S.ordo !== 'low') chant(A.findKyriale(solemn ? 'Ad Praefationem in tono solemni' : 'Ad Praefationem in tono feriali'), {noDrop: true, glyph: 1 / 19, size: 14});
        para(P.la, {cls: 'pr', max: 360});
        if (S.ordo !== 'low') rubric('The Preface is sung to the ' + (solemn ? 'solemn' : 'ferial') + ' tone of the Missal (Appendix).', {left: true});
      }
      return;
    }
    posture('All stand');
    pair('℣. Dóminus vobíscum. ℟. Et cum spíritu tuo. ℣. Sursum corda. ℟. Habémus ad Dóminum. ℣. Grátias agámus Dómino Deo nostro. ℟. Dignum et justum est.',
      '℣. The Lord be with you. ℟. And with thy spirit. ℣. Lift up your hearts. ℟. We have lifted them up to the Lord. ℣. Let us give thanks to the Lord our God. ℟. It is meet and just.');
    pair(P.la, P.tr);
  }

  // the Canon: inside the illuminated border, one wide column
  function canonPages() {
    curCols = 'canon';
    U(el('div'), {brk: 'section', sect: 'canon'});
    U(el('div', {class: 'c-front'}, [el('div', {class: 'b-art arch big'}, [el('div', {class: 'frame'}, [el('img', {src: 'art/crucifixion_arch.jpg', alt: ''})])]),
      el('div', {class: 'c-cap', text: 'Per ipsum, et cum ipso, et in ipso'})]), {});
    U(el('div'), {brk: 'page'});
    U(el('div', {class: 'b-head canon'}, [el('div', {class: 'b-title', text: 'Canon Missæ'}), diamond()]), {keep: true});
    var s = ordoLines('canon'), first = true;
    s.lines.forEach(function (l) {
      if (l.r) { rubric(l.r, {left: true}); return; }
      var t = l.la || '';
      if (/^Qui prídie/.test(t)) art('last_supper_arch', {size: 'small'});
      var cons = /^(Hoc est enim Corpus meum|Hic est enim Calix Sánguinis mei|Hic est enim calix)/.exec(t);
      if (cons) {
        var lines = t.split(/(?<=\.)\s+(?=Hæc quotiescúmque)/);
        U(el('div', {class: 'c-cons'}, [diamond(), el('p', {text: lines[0]}), diamond()]), {});
        if (lines[1]) para(lines[1], {cls: 'cn'});
        return;
      }
      var short = t.length < 50;
      var p = el('p', {class: 'b-p cn' + (first ? ' te' : '') + (short ? ' short' : '')}, short ? [J(t)] : [el('span', {class: 'lettrine', text: t.charAt(0)}), J(t.slice(1))]);
      first = false;
      U(p, {});
    });
    U(el('div'), {brk: 'section', sect: BOOK === 'priest' ? 'two' : 'one'});
  }

  // ================================================================== CONGREGATION BOOKLET
  var POSTURE = {foot: 'All kneel', in: 'All stand', gr: 'All sit', al: 'All sit', of: 'All sit', sa: 'All kneel', co: 'All kneel', post: 'All stand', dismiss: 'All kneel for the blessing', end: 'All stand'};
  function buildCong(seq) {
    curCols = 1;
    var did = {};
    var pairLines = function (k) {
      var s = ordoLines(k); if (!s) return;
      s.lines.forEach(function (l) {
        if (l.r) { rubric(l.r); return; }
        if (l.read) return;
        pair(l.la, l.en, {mk: lineMark(l), mkEn: lineMark(l, true)});
      });
      return s;
    };
    seq.forEach(function (it, n) {
      if (it.t === 'ordo') {
        var k = it.k;
        if (k === 'foot') { heading('Prayers at the Foot of the Altar', null); art('init_last_supper', {size: 'small'}); posture('All kneel'); rubric('While the choir sings the Introit, the priest and ministers say the preparatory prayers at the foot of the altar. In the Dominican rite there is no Psalm 42; the confession is short.'); pairLines('foot'); return; }
        if (k === 'collect') { heading('Collect · Oratio', null); posture('All stand'); pair('℣. Dóminus vobíscum. ℟. Et cum spíritu tuo. Orémus.', '℣. The Lord be with you. ℟. And with thy spirit. Let us pray.'); return; }
        if (k === 'collectEnd' || k === 'offertoryEnd' || k === 'postEnd' || k === 'chalice' || k === 'gospel' || k === 'offerDial') {
          if (k === 'offerDial') pair('℣. Dóminus vobíscum. ℟. Et cum spíritu tuo. Orémus.', '℣. The Lord be with you. ℟. And with thy spirit. Let us pray.');
          return;
        }
        if (k === 'afterGospel') { rubric('The sermon may follow; all sit.'); return; }
        if (k === 'offertory') { heading('The Offertory', null); posture('All sit'); pairLines('offertory'); return; }
        if (k === 'canon') {
          heading('The Canon of the Mass', null); art('crucifixion_arch'); posture('All kneel'); rubric('The priest says the Canon in silence.');
          var s = ordoLines('canon');
          s.lines.forEach(function (l) { if (!l.r) pair(l.la, l.en, {cls: /^(Hoc est enim|Hic est enim)/.test(l.la) ? 'cons' : ''}); });
          return;
        }
        if (k === 'pater') { heading('Pater noster', null); pairLines('pater'); return; }
        if (k === 'communion') { heading('Communion of the Faithful', null); art('last_supper_arch', {size: 'small'}); posture('All kneel'); pairLines('communion'); return; }
        if (k === 'post') { heading('Postcommunion · Postcommunio', null); posture('All stand'); pair('℣. Dóminus vobíscum. ℟. Et cum spíritu tuo. Orémus.', '℣. The Lord be with you. ℟. And with thy spirit. Let us pray.'); return; }
        if (k === 'dismiss') { heading('Dismissal and Blessing', null); pairLines('dismiss'); return; }
        if (k === 'end') { heading('Last Gospel', 'John 1, 1-14'); art('st_john_arch', {size: 'small'}); posture('All stand; kneel at Et Verbum caro factum est'); pairLines('end'); return; }
        pairLines(k);
        return;
      }
      if (it.t === 'oratio') {
        if (it.k === 'se') { heading('Secret · Secreta', null); }
        if (it.k === 'sp') { heading('Prayer over the People · Oratio super populum', null); posture('All bow'); pair('Orémus. ℣. Humiliáte cápita vestra Deo.', 'Let us pray. ℣. Bow down your heads before God.'); }
        pair(it.x[0], it.x[1]); pair('℟. Amen.', '℟. Amen.');
        return;
      }
      if (it.t === 'chant') {
        var p = it.p, id = it.c.id; if (!id) return;
        if ((p === 'gr' || p === 'al' || p === 'tr') && did.grad) { pair(TX['c:' + id] || '', chantEn(id)); return; }
        var title = p === 'gr' || p === 'al' || p === 'tr' ? 'Gradual and Alleluia · Responsorium' : (PART_EN[p] + ' · ' + PART_LA[p]);
        if (p === 'gr' || p === 'al' || p === 'tr') did.grad = true;
        heading(p === 'co' ? 'Communion Antiphon · Communio' : title, chantRef(id));
        var a = {in: 'init_g_dominic', gr: 'catherine_arch', of: 'peter_martyr_arch'}[p];
        if (a) art(a, {size: 'small'});
        if (POSTURE[p]) posture(POSTURE[p]);
        pair(TX['c:' + id] || '', chantEn(id));
        return;
      }
      if (it.t === 'ord') {
        var low = ordoLines(it.k + 'Low');
        if (it.k === 'it') return;
        if (!low) return;
        var name = {ky: 'Kyrie', gl: 'Gloria', cr: 'Credo', sa: 'Sanctus', ag: 'Agnus Dei'}[it.k];
        heading(name, null);
        if (it.k === 'sa') { art('sano_virgin_arch', {size: 'small'}); posture('All kneel'); }
        if (it.k === 'cr') posture('All stand; kneel at Et incarnatus est');
        low.lines.forEach(function (l) { if (!l.r) pair(l.la, l.en); });
        return;
      }
      if (it.t === 'read') { reading(it.r, true); return; }
      if (it.t === 'pref') { preface(); return; }
    });
    creditsUnit();
  }

  // ================================================================== covers, credits
  function cover() {
    var d = S.date, name = feastEnglish(), la = feastLatin();
    var band = el('div', {class: 'c-band'}, [el('div', {class: 'c-date', text: dateLine(d)}), el('div', {class: 'c-feast', text: name}),
      el('div', {class: 'c-la', text: la}), el('div', {class: 'c-rank', text: rankLine()})]);
    var kids = [];
    if (BOOK === 'choir') {
      kids = [el('div', {class: 'c-top', text: 'Liber Chori'}), el('div', {class: 'c-sub', text: 'Propria et Ordinarium Missæ juxta ritum Sacri Ordinis Prædicatorum'}),
        el('div', {class: 'b-art sq cover'}, [el('div', {class: 'frame'}, [el('img', {src: 'art/leaf_dominic.jpg', alt: ''})])]), band];
      var toc = el('div', {class: 'c-toc', id: 'toc'});
      kids.push(toc);
      kids.push(el('div', {class: 'c-note', text: 'All chants from the Graduale juxta ritum Sacri Ordinis Prædicatorum (Rome, 1950)'}));
    } else if (BOOK === 'priest') {
      kids = [el('div', {class: 'c-top', text: 'Missale'}), el('div', {class: 'c-sub', text: 'Ordo et Proprium Missæ juxta ritum Sacri Ordinis Prædicatorum'}),
        el('div', {class: 'b-art sq cover'}, [el('div', {class: 'frame'}, [el('img', {src: 'art/init_g_dominic.jpg', alt: ''})])]), band,
        el('div', {class: 'c-toc', id: 'toc'})];
    } else {
      kids = [el('div', {class: 'c-top', text: 'Holy Mass'}), el('div', {class: 'c-sub', text: 'according to the Rite of the Order of Preachers'}),
        el('div', {class: 'b-art arch cover'}, [el('div', {class: 'frame'}, [el('img', {src: 'art/tiepolo_arch.jpg', alt: ''})])]), band,
        el('p', {class: 'c-intro', text: introText()})];
    }
    return el('div', {class: 'b-cover'}, kids);
  }
  function introText() {
    var bits = [];
    if (FIX[S.key] && S.key === 'S1112') return 'Today the Order of Preachers keeps in one feast all its saints and blessed: the friars, nuns, sisters and laity who followed St Dominic in preaching the Gospel for the salvation of souls. The Mass takes its chants from the feast of All Saints; the Collect, Epistle and Gospel are proper to the day, and the Preface is that of our Holy Father St Dominic.';
    bits.push('This booklet gives the whole ' + formEn().toLowerCase() + ' of ' + feastEnglish() + ' in Latin, with an English translation beside it.');
    var pn = A.prefaceOf(S.key, S.date); if (pn && window.PREFACES && PREFACES[pn]) bits.push('The Preface is ' + PREFACES[pn].en.replace(/^Preface/, 'the Preface') + '.');
    bits.push(R.gloria ? 'The Gloria is sung' + (R.credo ? ' and the Creed is said.' : '; there is no Creed.') : 'There is no Gloria' + (R.credo ? ', but the Creed is said.' : ' and no Creed.'));
    return bits.join(' ');
  }
  function creditsUnit() {
    var t = [
      ['Texts', 'Order of Mass and rubrics after the Missale juxta ritum Sacri Ordinis Prædicatorum (Rome, 1939); proper texts from the Graduale O.P. (1950) and the St Dominic Missal; Epistle and Gospel from the Vulgate, in English from the Douay-Rheims Bible. Other English translations are the editor’s.'],
      ['Chant', 'Graduale juxta ritum Sacri Ordinis Prædicatorum (Rome, 1950), GABC from GregoBase; the priest’s chants (Preface, Pater noster, Pax) transcribed from the Missale O.P., Appendix. Engraved with Exsurge.'],
      ['Art', 'All images public-domain works from the open-access collection of The Art Institute of Chicago (CC0): Neri da Rimini, antiphonary leaves with St Dominic and the angel in initials (c. 1300); G. B. Tiepolo, Virgin and Child with SS Dominic and Hyacinth; Lo Spagna, St Catherine of Siena; A. Vivarini, St Peter Martyr; Sano di Pietro, Virgin and Child with saints and angels; A. Dürer, The Last Supper; M. Raimondi, St Paul preaching; J. de Gheyn II, St Matthew; P. Farinati, St John; Giovanni di Paolo’s circle, Crucifixion; a French prayer-book leaf (c. 1500) for the Canon border.'],
      ['Edition', 'Set in EB Garamond. Colours of Providence College: Providence Black and Providence Gold. Generated by dominicanrite.com for ' + dateLine(S.date) + '.']];
    U(el('div', {class: 'b-credits'}, [el('div', {class: 'b-title', text: 'Credits & Sources'}), el('div', {class: 'cr-rule'})].concat(t.map(function (x) { return el('p', null, [el('b', {text: x[0] + '. '}), x[1]]); }))), {brk: 'bottom'});
  }

  // ================================================================== pagination
  function paginate(root, measure) {
    // the measuring area must have the width of the column each unit is laid in
    var pages = [], page = null, col = null, colsLeft = 0, h = 0, cap = 0, sect = BOOK === 'priest' ? 'two' : 'one';
    var geom = function () {
      if (sect === 'two') return {cols: 2, w: G.colW, h: G.bodyH};
      if (sect === 'canon') return {cols: 1, w: CANON.w, h: CANON.h};
      return {cols: 1, w: G.bodyW, h: G.bodyH};
    };
    var newPage = function () {
      var g = geom();
      page = el('div', {class: 'b-page ' + (sect === 'canon' ? 'canon' : 'std') + (sect === 'two' ? ' two' : '')});
      if (sect === 'canon') page.classList.add((pages.length + 2) % 2 ? 'odd' : 'even');
      var body = el('div', {class: 'b-body'}); page.appendChild(body);
      page._body = body; pages.push(page); root.appendChild(page);
      colsLeft = g.cols; newCol();
    };
    var newCol = function () {
      if (colsLeft <= 0) { newPage(); return; }
      colsLeft--;
      col = el('div', {class: 'b-col'}); page._body.appendChild(col); h = 0; cap = geom().h;
    };
    newPage();
    var i = 0;
    while (i < units.length) {
      var u = units[i];
      if (u.brk === 'section') { sect = u.sect || sect; if (h > 0 || colsLeft < geom().cols - 1 || page._body.childNodes.length > 1) { colsLeft = 0; newPage(); } else { page.remove(); pages.pop(); newPage(); } i++; continue; }
      if (u.brk === 'page') { colsLeft = 0; newPage(); i++; continue; }
      // the group of units that must stay together
      var j = i, gh = 0;
      while (true) { gh += units[j].h; if (!units[j].keep || j + 1 >= units.length || units[j + 1].brk) break; j++; }
      if (h > 0 && h + gh > cap) {
        // a group taller than a column only keeps its first two units together
        if (gh > cap) { var k = i, kh = 0; while (k <= j && kh + units[k].h <= cap - h) { kh += units[k].h; k++; } if (k - i < 2) newCol(); }
        else newCol();
      }
      if (u.brk === 'bottom') { var sp = cap - h - u.h; if (sp > 0) col.appendChild(el('div', {style: 'height:' + sp + 'px'})); }
      col.appendChild(u.n); u.page = pages.length; h += u.h;
      i++;
    }
    return pages;
  }
  function measureAll(area) {
    var widths = {one: G.bodyW, two: G.colW, canon: CANON.w}, sect = BOOK === 'priest' ? 'two' : 'one';
    units.forEach(function (u) {
      if (u.brk === 'section') { sect = u.sect; u.h = 0; return; }
      if (u.brk === 'page') { u.h = 0; return; }
      var box = el('div', {class: 'b-col ' + (sect === 'canon' ? 'in-canon' : '') + (sect === 'two' ? ' in-two' : ''), style: 'width:' + widths[sect] + 'px'});
      area.appendChild(box); box.appendChild(u.n);
      u.h = Math.ceil(u.n.getBoundingClientRect().height + parseFloat(getComputedStyle(u.n).marginTop) + parseFloat(getComputedStyle(u.n).marginBottom));
    });
  }
  // after drawing, every chant is cut into its lines, each a unit of its own
  function explodeChants() {
    var out = [];
    units.forEach(function (u, i) {
      if (!u.chant) { out.push(u); return; }
      var lines = Array.prototype.slice.call(u.n.querySelectorAll('.line'));
      if (!lines.length) { out.push(u); return; }
      lines.forEach(function (ln, k) {
        var w = el('div', {class: 'b-chant' + (k ? ' cont' : '')}); w.appendChild(ln);
        var nx = units[i + 1];
        out.push({n: w, keep: (k === 0 && lines.length > 1) || (k === lines.length - 1 && nx && nx.after), id: u.id + '_' + k, brk: ''});
      });
      // the last line keeps with a rubric that follows it
    });
    units = out;
  }

  // ================================================================== build
  function build(api) {
    A = api; D = api.D; S = api.state();
    if (!S.key) return;
    if (!S.ordo) S.ordo = params.get('ordo') || 'solemn';
    M = D.masses[S.key]; R = api.rubricsOf(S.key, S.date); ORD = api.ordinaryIds();
    document.title = BOOK_NAME + ' — ' + feastEnglish() + ' ' + iso(S.date);
    var root = document.getElementById('book');
    root.innerHTML = '';
    var bar = el('div', {class: 'b-bar'}, [
      el('span', {class: 'b-bar-t', text: BOOK_NAME + ' · ' + feastEnglish() + ' · ' + dateLine(S.date)}),
      el('span', {class: 'b-bar-s', id: 'bStatus', text: 'Laying out the pages…'}),
      el('a', {href: '?b=choir' + location.hash, text: 'Choir'}), el('a', {href: '?b=priest' + location.hash, text: 'Priest'}), el('a', {href: '?b=cong' + location.hash, text: 'Congregation'}),
      el('button', {type: 'button', id: 'bPrint', text: 'Print / Save as PDF'})]);
    document.body.insertBefore(bar, document.body.firstChild);
    document.getElementById('bPrint').addEventListener('click', function () { window.print(); });
    var seq = api.massSequence(M, S.parts);
    var fonts = ['16px "EB Garamond"', 'italic 16px "EB Garamond"', '500 16px "EB Garamond"', '600 16px "EB Garamond"', '16px Versiculum'];
    Promise.all(fonts.map(function (f) { return document.fonts.load(f); })).then(function () { return preload(seq); }).then(function () {
      if (BOOK === 'choir') buildChoir(seq); else if (BOOK === 'priest') buildPriest(seq); else buildCong(seq);
      var area = el('div', {class: 'b-measure'}); document.body.appendChild(area);
      // chants are drawn in the measuring area, at their column's width
      var sect = BOOK === 'priest' ? 'two' : 'one';
      units.forEach(function (u) {
        if (u.brk === 'section') sect = u.sect;
        if (u.chant) { var b = el('div', {class: 'b-col' + (sect === 'canon' ? ' in-canon' : '') + (sect === 'two' ? ' in-two' : '')}); b.style.width = ({one: G.bodyW, two: G.colW, canon: CANON.w})[sect] + 'px'; area.appendChild(b); b.appendChild(u.n); }
      });
      return Promise.all(pending).then(function () { return Promise.all(Array.prototype.map.call(document.images, function (im) { return im.complete ? 0 : new Promise(function (r) { im.onload = im.onerror = r; }); })); }).then(function () {
        explodeChants();
        measureAll(area);
        var cv = el('div', {class: 'b-page cover'}, [cover()]);
        root.appendChild(cv);
        var pages = paginate(root);
        area.remove();
        // footers and contents
        var foot = (BOOK === 'choir' ? 'Choir Book · ' : BOOK === 'priest' ? 'Missale · ' : '') + feastEnglish() + (BOOK === 'cong' ? ' · ' + S.date.getDate() + ' ' + MONTHS[S.date.getMonth()] + ' ' + S.date.getFullYear() : '');
        pages.forEach(function (p, i) { if (!p.classList.contains('canon')) p.appendChild(el('div', {class: 'b-foot'}, [foot, el('span', {class: 'dot', text: ' • '}), String(i + 2)])); });
        var toc = document.getElementById('toc');
        if (toc) {
          var rows = BOOK === 'choir' ? TOC : [];
          if (BOOK === 'priest') units.forEach(function (u) { if (u.n.classList && u.n.classList.contains('b-head')) rows.push({label: u.n.querySelector('.b-title').textContent, it: u}); });
          rows.forEach(function (r) {
            var pg = r.it && r.it.page ? r.it.page + 1 : '';
            toc.appendChild(el('div', {class: 'toc-row'}, [el('span', {class: 'toc-l'}, [].concat(r.label)), el('span', {class: 'toc-p', text: String(pg)})]));
          });
          if (BOOK === 'priest' && rows.length > 22) toc.classList.add('two');
        }
        document.getElementById('bStatus').textContent = (pages.length + 1) + ' pages · ready to print';
        document.body.classList.add('b-ready');
      });
    }).catch(function (e) { document.getElementById('bStatus').textContent = 'Error: ' + e.message; if (window.console) console.error(e); });
  }
  window.OPBook = {build: build, units: function () { return units; }};
})();
