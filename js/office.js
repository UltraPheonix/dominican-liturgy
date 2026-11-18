/* Officium Divinum juxta ritum S. Ordinis Praedicatorum — the spoken Office (Latin and English).
   Data: data/office.js (OFFICE), built by tools/build_office.py from the Breviarium O.P. (Cormier, 1909).
   The day's celebration and its rank come from the Missal page's calendar (js/app.js, loaded as a library). */
(function () {
  'use strict';
  var O = window.OFFICE, D = window.DOMINICAN, P = window.ProprOP;
  var $ = function (s, e) { return (e || document).querySelector(s); };
  var el = function (tag, attrs, kids) {
    var e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (attrs[k] == null) return;
      if (k === 'text') e.textContent = attrs[k];
      else if (k === 'html') e.innerHTML = attrs[k];
      else if (k.slice(0, 2) === 'on') e.addEventListener(k.slice(2), attrs[k]);
      else e.setAttribute(k, attrs[k]);
    });
    (kids || []).forEach(function (c) { if (c) e.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return e;
  };
  var HOURS = [['matutinum', 'Ad Matutinum', 'Matins'], ['laudes', 'Ad Laudes', 'Lauds'], ['prima', 'Ad Primam', 'Prime'],
    ['tertia', 'Ad Tertiam', 'Terce'], ['sexta', 'Ad Sextam', 'Sext'], ['nona', 'Ad Nonam', 'None'],
    ['vesperae', 'Ad Vesperas', 'Vespers'], ['completorium', 'Ad Completorium', 'Compline']];
  var DOW = ['dominica', 'feria2', 'feria3', 'feria4', 'feria5', 'feria6', 'sabbato'];
  var DOWX = null; var DOW_LA = ['Dominica', 'Feria secunda', 'Feria tertia', 'Feria quarta', 'Feria quinta', 'Feria sexta', 'Sabbato'];
  var state = {date: null, hour: null};

  // ---------- Bible (Vulgate and Douay-Rheims), verse by verse ----------
  var bible = {};
  function book(lang, name) {
    var k = lang + '/' + name;
    if (!bible[k]) bible[k] = fetch('bible/' + lang + '/' + encodeURIComponent(name) + '.txt').then(function (r) { return r.text(); }).then(function (t) {
      var v = {};
      t.split('\n').forEach(function (l) { var p = l.split('\t'); if (p.length >= 3) v[p[0] + ':' + p[1]] = p.slice(2).join(' '); });
      return v;
    });
    return bible[k];
  }
  // "Psalmi 118: 1-16" or "Psalmi 4" or "Lucas 1: 68-79" → [[c,v]...]
  function verses(ref, v) {
    var m = ref.match(/^(.*?)\s+(\d+)(?::\s*(.+))?$/), out = [];
    if (!m) return out;
    var ch = +m[2];
    if (!m[3]) { for (var n = 1; n < 400; n++) if (v[ch + ':' + n] !== undefined) out.push([ch, n]); return out; }
    m[3].split(',').forEach(function (part) {
      var r = part.trim().match(/^(\d+)(?:-(\d+))?$/);
      if (!r) return;
      for (var n = +r[1]; n <= +(r[2] || r[1]); n++) if (v[ch + ':' + n] !== undefined) out.push([ch, n]);
    });
    return out;
  }
  function bookOf(ref) { return ref.replace(/\s+\d+(?::.*)?$/, ''); }

  // ---------- the calendar: the day's celebration ----------
  function easter(y) { return P.easter(y); }
  function days(a, b) { return Math.round((a - b) / 864e5); }
  function season(d) {
    var y = d.getFullYear(), e = easter(y), f = days(d, e), md = (d.getMonth() + 1) * 100 + d.getDate();
    var xmas = new Date(y, 11, 25), adv1 = new Date(y, 11, 25 - ((xmas.getDay() || 7) + 21));
    if (d >= adv1 && md < 1225) return 'adventus';
    if (md >= 1225 || md <= 113) return 'nativitas';
    if (f >= -63 && f < -46) return 'septuagesima';
    if (f >= -46 && f < -14) return 'quadragesima';
    if (f >= -14 && f < 0) return 'passio';
    if (f >= 0 && f <= 55) return 'pascha';
    return 'annum';
  }
  function dayInfo(d) {
    var r = P.massesOf(d), key = r.win, m = D.masses[key] || {};
    var temporal = P.isTemporal(key);
    var cls = temporal ? P.temporalClass(key, d) : P.feastClass(key);
    return {key: key, title: m.title || '', en: m.name_en || m.en || '', cls: cls, temporal: temporal, season: season(d),
      dow: d.getDay(), sunday: d.getDay() === 0, feast: !temporal && cls <= 3};
  }

  // ---------- assembling an hour ----------
  function ord(name) { return (O.ordinarium || {})[name]; }
  // replace Alleluia at the end of "Deus in adjutorium" from Septuagesima to Holy Week
  function adapt(it, info) {
    if (!it || !it.la) return it;
    var c = JSON.parse(JSON.stringify(it));
    var penit = /septuagesima|quadragesima|passio/.test(info.season);
    if (penit && c.alleluia) {
      c.la = c.la.replace(/\s*Allel[uú]ia\.?\s*$/, ' Laus tibi, Dómine, Rex ætérnæ glóriæ.');
      c.en = (c.en || '').replace(/\s*Alleluia\.?\s*$/, ' Praise be to thee, O Lord, King of eternal glory.');
    }
    if (info.season === 'pascha' && c.paschal) { c.la += ' Allelúia.'; c.en += ' Alleluia.'; }
    return c;
  }
  // seasons as the Psalter's rubrics divide them
  function offSeason(d) {
    var y = d.getFullYear(), e = easter(y), f = days(d, e), md = (d.getMonth() + 1) * 100 + d.getDate();
    var xmas = new Date(y, 11, 25), adv1 = new Date(y, 11, 25 - ((xmas.getDay() || 7) + 21));
    if (d >= adv1 && md < 1225) return 'adventus';
    if (md >= 1225 || md <= 113) return 'nativitas';
    if (f < -63) return 'annum';
    if (f < -46) return 'septuagesima';
    if (f < -42) return 'cineres';                 // Ash Wednesday to Saturday
    if (f < -14) return 'quadragesima';
    if (f < -3) return 'passio';
    if (f < 0) return 'triduum';
    if (f < 7) return 'octavaPaschae';
    if (f < 39) return 'pascha';
    if (f < 49) return 'ascensio';
    if (f < 56) return 'pentecostes';
    return 'annum';
  }
  function complineKey(d, s) {
    var f = days(d, easter(d.getFullYear()));
    if (f >= -43 && f < -21) return 'lent1';       // from the Saturday after Ash Wednesday to Lent III
    if (f >= -22 && f < -15) return 'lent3';
    if (f === -4) return 'holyweds';
    if (f >= -15 && f < -4) return 'passio';
    if (f >= 6 && f < 38) return 'pascha';
    if (f >= 38 && f < 48) return 'ascensio';
    if (f >= 48 && f < 55) return 'pentecostes';
    return 'annum';
  }
  var NOTE = function (en) { return {t: 'rub', la: en, en: en}; };
  function collectItem(info) {
    var c = (O.collects || {})[info.key];
    if (c) return {t: 'or', la: c.la, en: c.en || ''};
    return NOTE('The collect of the day (as at Lauds) follows here.');
  }
  function hourItems(hour, info) {
    var d = state.date || new Date(), s = offSeason(d), feast = info.feast && !info.sunday, sun = info.sunday || feast, out = [];
    var special = {triduum: 'The Office of the Sacred Triduum has its own form, which is not yet on this page.',
                   octavaPaschae: 'Within the octave of Easter the little hours and Compline have their own form; the ordinary Paschal form is shown meanwhile.'};
    if (hour === 'completorium') {
      if (s === 'triduum') return [NOTE(special.triduum)];
      var ck = complineKey(d, s);
      if (s === 'octavaPaschae') { out.push(NOTE(special.octavaPaschae)); ck = 'pascha'; }
      O.compline[ck].forEach(function (it) {
        if (ck === 'pentecostes' && it.t === 'ps' && it.ref === 'Psalmi 90' && days(d, easter(d.getFullYear())) >= 49) return;  // not in the octave of Pentecost
        out.push(it.ref && !it.t ? ord(it.ref) : it);
      });
      return out.map(function (it) { return adapt(it, info); });
    }
    if (s === 'triduum') return [NOTE(special.triduum)];
    var base = {adventus: 'adventus', nativitas: 'annum', annum: 'annum', septuagesima: 'annum', cineres: 'quadragesima', quadragesima: 'quadragesima',
                passio: 'passio', octavaPaschae: 'pascha', pascha: 'pascha', ascensio: 'pascha', pentecostes: 'pascha'}[s];
    if (feast) out.push(NOTE('On a feast the antiphons, chapter and short responsory are those of the feast (Proper or Common of the Saints), which are not yet on this page; the festal form of the Psalter is shown meanwhile.'));
    else if (s === 'nativitas' || s === 'ascensio' || s === 'pentecostes' || s === 'octavaPaschae')
      out.push(NOTE('This season has its own antiphons, chapters and responsories in the Proper of the Season; until they are added, those of the Psalter are shown.'));
    if (hour === 'prima') {
      var penitSun = sun && /septuagesima|cineres|quadragesima|passio/.test(s);
      var key = penitSun ? 'penit_1' : base + '_' + (sun ? 1 : 0);
      (O.prime[key] || O.prime['annum_' + (sun ? 1 : 0)]).forEach(function (it) {
        if (it.t === 'proper') { out.push(NOTE('Antiphon: the first antiphon of Lauds of the Sunday (Proper of the Season).')); return; }
        if (base === 'passio' && it.t === 'resp') return;          // ℟. Jesu Christe not said from Passion Sunday to Low Sunday
        if (it.t === 'ps' && it.ref === 'QUICUMQUE') { out.push({t: 'quicumque'}); return; }
        if (it.t === 'or' && /In hac hora|Dómine Deus omnípotens/.test(it.la)) { out.push(it); return; }
        out.push(it.ref && !it.t ? ord(it.ref) : it);
      });
      return out.map(function (it) { return adapt(it, info); });
    }
    // Terce, Sext, None
    var L = O.little[hour][base] || O.little[hour].annum, part = (sun ? L.sun : L.fer) || {};
    var pick = function (k) { return (part && part[k] !== undefined) ? part[k] : L[k]; };
    var names = {tertia: 'Ad Tertiam', sexta: 'Ad Sextam', nona: 'Ad Nonam'};
    out.push({t: 'h', la: names[hour]}, NOTE('Pater noster and Ave María are said silently.'), ord('Deus in adjutorium'), O.littleHymns[hour]);
    O.littlePsalms[hour].forEach(function (p) { out.push({t: 'ps', ref: p[0], title: 'Psalmus 118 · ' + p[1]}); });
    var ant = pick('ant');
    if (ant) out.push(ant);
    else out.push(NOTE('Antiphon: from Lauds of the Sunday (' + {tertia: 'the second', sexta: 'the third', nona: 'the fifth'}[hour] + ' antiphon), in the Proper of the Season.'));
    var ch = pick('chap'); if (ch) out.push(ch);
    var rs = pick('resp'); if (rs) out.push(rs); else if (base === 'quadragesima' || base === 'passio') out.push(NOTE('Responsory and versicle of the Sunday.'));
    var vs = pick('vers'); if (vs) out.push(vs);
    if (!sun && base !== 'pascha') {
      var sat = d.getDay() === 6;
      if (!(sat && hour === 'nona')) out.push(ord('Kyrie preces'));
    }
    out.push(ord('Dominus vobiscum'), ord('Oremus'), collectItem(info), ord('Dominus vobiscum'), ord('Benedicamus'));
    return out.map(function (it) { return adapt(it, info); });
  }

  // ---------- drawing ----------
  function pair(la, en, cls) {
    return el('div', {class: 'o-pair ' + (cls || '')}, [el('p', {class: 'o-la', html: mark(la)}), el('p', {class: 'o-en', html: mark(en || '')})]);
  }
  // red ℣. ℟. ✠ * and rubrics in [brackets]
  function mark(s) {
    return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/(℣\.|℟\.|✠|\*|†)/g, '<span class="r">$1</span>')
      .replace(/\[([^\]]+)\]/g, '<span class="rub">$1</span>');
  }
  function drawPsalm(box, it, info) {
    var head = el('h4', {class: 'o-ps-head'}, [it.title || ('Psalmus ' + it.ref.replace(/^Psalmi\s+/, '')), it.en_title ? el('span', {class: 'o-en-t', text: ' ' + it.en_title}) : null]);
    var body = el('div', {class: 'o-psalm'});
    box.appendChild(el('section', {class: 'o-item o-ps'}, [head, body]));
    var b = bookOf(it.ref);
    Promise.all([book('la', b), book('en', b)]).then(function (r) {
      var la = r[0], en = r[1], vs = verses(it.ref, la);
      // drop the psalm's title (verse 1 when it is a heading such as "Psalmus David")
      if (/^Psalmi/.test(b) && !/:/.test(it.ref) && vs.length && /^(In finem|Psalmus|Psalmi|Canticum|Intellectus|Oratio|Alleluja|Allel[uú]ia|David|Ipsi David|Huic David|Laus cantici|Pro|Ad|Titulus|Confessio|In|Hymnus)\b/.test(la[vs[0].join(':')] || '') && (la[vs[0].join(':')] || '').length < 160 && it.keepTitle !== true) {
        if (!/[a-z]\s*:\s/.test((la[vs[0].join(':')] || '').slice(0, 60)) || /Psalmus|psalmus|Canticum|Intellectus/.test(la[vs[0].join(':')])) vs.shift();
      }
      vs.forEach(function (cv) { body.appendChild(pair(la[cv.join(':')], en[cv.join(':')], 'o-verse')); });
      if (it.gloria !== false && !info.noGloria) body.appendChild(pair(ord('Gloria Patri').la, ord('Gloria Patri').en, 'o-verse o-gp'));
    });
  }
  function drawItem(box, it, info) {
    if (!it) return;
    switch (it.t) {
      case 'h': box.appendChild(el('h3', {class: 'o-h', text: it.la})); break;
      case 'rub': box.appendChild(el('p', {class: 'o-rubric', text: it.en || it.la})); break;
      case 'ps': drawPsalm(box, it, info); break;
      case 'quicumque':
        var qb = el('section', {class: 'o-item o-ps'}, [el('h4', {class: 'o-ps-head', text: 'Symbolum S. Athanasii · Quicumque'})]);
        (O.quicumque || []).forEach(function (v) { qb.appendChild(pair(v[0], v[1], 'o-verse')); });
        qb.appendChild(pair(ord('Gloria Patri').la, ord('Gloria Patri').en, 'o-verse o-gp'));
        box.appendChild(qb); break;
      case 'hymn':
        var hb = el('section', {class: 'o-item o-hymn'}, [el('h4', {text: 'Hymnus' + (it.name ? ' · ' + it.name : '')})]);
        (it.la || []).forEach(function (st, i) { hb.appendChild(pair(st, (it.en || [])[i] || '', 'o-stanza')); });
        box.appendChild(hb); break;
      default:
        var lab = {ant: 'Ant.', chap: 'Capitulum', or: 'Oratio', inv: 'Invitatorium', lect: 'Lectio', resp: '℟. br.'}[it.t];
        var sec = el('section', {class: 'o-item o-' + (it.t || 'txt')});
        if (lab && it.t !== 'ant') sec.appendChild(el('h4', {text: lab + (it.ref ? ' · ' + it.ref : '')}));
        sec.appendChild(pair((it.t === 'ant' ? '<b>Ant.</b> ' : '') + it.la, (it.t === 'ant' ? 'Ant. ' : '') + (it.en || '')));
        if (it.t === 'ant') sec.querySelector('.o-la').innerHTML = '<span class="r">Ant.</span> ' + mark(it.la);
        box.appendChild(sec);
    }
  }
  function drawHour(hour) {
    state.hour = hour;
    var info = dayInfo(state.date), box = $('#office');
    box.innerHTML = '';
    var h = HOURS.filter(function (x) { return x[0] === hour; })[0];
    box.appendChild(el('header', {class: 'o-head'}, [
      el('h2', {text: h[1]}), el('p', {class: 'o-sub', text: h[2] + ' · ' + DOW_LA[info.dow] + ' · ' + (info.title.replace(/^.*?—\s*/, '') || '')})]));
    hourItems(hour, info).forEach(function (it) { if (it && it.t === 'h' && it.la === h[1]) return; drawItem(box, it, info); });
    document.querySelectorAll('#hours button').forEach(function (b) { b.classList.toggle('on', b.dataset.h === hour); });
    history.replaceState(null, '', '#' + hour + '&d=' + iso(state.date));
  }
  function iso(d) { return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function fromIso(s) { var p = s.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function defaultHour() {
    var h = new Date().getHours();
    return h < 6 ? 'matutinum' : h < 8 ? 'laudes' : h < 9 ? 'prima' : h < 11 ? 'tertia' : h < 14 ? 'sexta' : h < 16 ? 'nona' : h < 20 ? 'vesperae' : 'completorium';
  }
  function setDate(d) {
    state.date = d;
    $('#date').value = iso(d);
    var info = dayInfo(d);
    $('#dayTitle').textContent = info.title.replace(/^.*?—\s*/, '') || DOW_LA[d.getDay()];
    $('#dayMeta').textContent = DOW_LA[d.getDay()] + ' · ' + d.toLocaleDateString('en-GB', {day: 'numeric', month: 'long', year: 'numeric'}) + ' · ' + (info.cls ? ['', 'I', 'II', 'III', 'IV'][info.cls] + ' class' : '');
    drawHour(state.hour || defaultHour());
  }
  function start() {
    var nav = $('#hours');
    HOURS.forEach(function (h) { nav.appendChild(el('button', {type: 'button', 'data-h': h[0], text: h[2], onclick: function () { drawHour(h[0]); }})); });
    $('#date').addEventListener('change', function (e) { if (e.target.value) setDate(fromIso(e.target.value)); });
    $('#prevDay').addEventListener('click', function () { var d = new Date(state.date); d.setDate(d.getDate() - 1); setDate(d); });
    $('#nextDay').addEventListener('click', function () { var d = new Date(state.date); d.setDate(d.getDate() + 1); setDate(d); });
    var m = location.hash.match(/^#(\w+)(?:&d=(\d{4}-\d\d-\d\d))?/);
    if (m && HOURS.some(function (h) { return h[0] === m[1]; })) state.hour = m[1];
    setDate(m && m[2] ? fromIso(m[2]) : new Date());
  }
  window.OfficeOP = {hourItems: hourItems, dayInfo: dayInfo, season: season, drawHour: drawHour};
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
