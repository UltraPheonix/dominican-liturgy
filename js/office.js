/* The Divine Office of the Dominican Rite (Breviarium S.O.P., 1962).
   The text of each day is generated ahead of time from Divinum Officium's
   "Ordo Praedicatorum - 1962" data (MIT licence) and checked against the
   1962 Breviary; this file only fetches and displays it. */
(function () {
  'use strict';
  var BASE = 'data/office/';
  var HOURS = [
    ['Matutinum', 'Ad Matutinum', 'Matins'], ['Laudes', 'Ad Laudes', 'Lauds'], ['Prima', 'Ad Primam', 'Prime'],
    ['Tertia', 'Ad Tertiam', 'Terce'], ['Sexta', 'Ad Sextam', 'Sext'], ['Nona', 'Ad Nonam', 'None'],
    ['Vespera', 'Ad Vesperas', 'Vespers'], ['Completorium', 'Ad Completorium', 'Compline']
  ];
  var $ = function (s) { return document.querySelector(s); };
  var cache = {}, common = null, shards = {}, range = null;
  var state = {date: null, hour: null, lang: 'both', priest: false, chant: false};
  var chantMap = null;

  try {
    state.lang = 'both';
    state.priest = localStorage.getItem('officePriest') === '1';
    state.chant = localStorage.getItem('officeChant') === '1';
  } catch (e) {}

  function pad(n) { return (n < 10 ? '0' : '') + n; }
  var WD = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], MO = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  function shortDate(d) {
    var t = new Date(); t.setHours(0, 0, 0, 0);
    return WD[d.getDay()] + ' ' + d.getDate() + ' ' + MO[d.getMonth()] + ' ' + d.getFullYear() + (+d === +t ? ' · Today' : '');
  }
  function iso(d) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
  function parseIso(s) { var m = /^(\d{4})-(\d\d)-(\d\d)$/.exec(s || ''); return m ? new Date(+m[1], +m[2] - 1, +m[3]) : null; }
  function addDays(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function getJSON(url) {
    if (!cache[url]) {
      cache[url] = fetch(url).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
      cache[url].catch(function () { delete cache[url]; });
    }
    return cache[url];
  }

  // a sensible default hour for the time of day
  function hourNow() {
    var h = new Date().getHours();
    return h < 5 ? 'Matutinum' : h < 8 ? 'Laudes' : h < 9 ? 'Prima' : h < 11 ? 'Tertia' : h < 14 ? 'Sexta'
      : h < 16 ? 'Nona' : h < 20 ? 'Vespera' : 'Completorium';
  }

  // ---------- markup ----------
  var TAGS = {r: '<span class="r">', c: '<span class="r ini">', n: '<span class="r vn">', k: '<span class="k">', h: '<span class="r">'};
  function fmt(line) {
    if (window.OPNames) line = OPNames.en(OPNames.la(line));
    var s = esc(line).replace(/&lt;(\/?)([rcnkh])&gt;/g, function (m, close, t) { return close ? '</span>' : TAGS[t]; });
    return s.replace(/([✠✙])/g, '<span class="r">$1</span>').replace(/ \* /g, ' <span class="r">*</span> ')
      .replace(/ † /g, ' <span class="r">†</span> ').replace(/ \+ /g, ' <span class="r">✠</span> ');
  }
  function blockText(id, day) { if (id === '@preces-la') return PRECES.la; if (id === '@preces-en') return PRECES.en;
    var mx = /^@x:([^:]+):(\w+)$/.exec(id); if (mx) return xform(blockText(mx[1], day), mx[2]); return complineSeason(maryText(lentText(teLucisText((day.b && day.b[id]) || (common && common[id]) || '', day), day), day)); }
  // Compline in Christmastide (Completorium O.P. 1949 pp. 38-39 and the Antiphonarium 1933): In manus with Alleluia daily
  // to the Octave of the Epiphany; at the Nunc dimittis 'Alleluia. Verbum caro' to the Epiphany, then 'Alleluia. Omnes de Saba'.
  // C49 pp. 20-21: the Hebdomadarius (a priest) says Dominus vobiscum before the prayer and the Benedicamus
  function dvPriest(t) {
    return t.replace(/Dómine, exáudi oratiónem meam\.\n<r>℟\.<\/r> Et clamor meus ad te véniat\.\n(?=<c>O<\/c>rémus\.\n<c>V<\/c>ísita|<r>℣\.<\/r> Benedicámus)/, 'Dóminus vobíscum.\n<r>℟.</r> Et cum spíritu tuo.\n')
            .replace(/Lord, hear my prayer\.\n<r>℟\.<\/r> And let my cry come unto thee\.\n(?=<c>L<\/c>et us pray\.\n<c>V<\/c>isit|<r>℣\.<\/r> Let us bless)/, 'The Lord be with you.\n<r>℟.</r> And with thy spirit.\n');
  }
  var DOX = {
    natus: ['Glória tibi, Dómine,\nQui natus es de Vírgine,\nCum Patre et Sancto Spíritu,\nIn sempitérna sǽcula.', 'Glory to thee, O Lord,\nWho wast born of the Virgin,\nWith the Father and the Holy Spirit,\nUnto everlasting ages.'],
    epi: ['Glória tibi, Dómine,\nQui apparuísti hódie,\nCum Patre et Sancto Spíritu,\nIn sempitérna sǽcula.', 'Glory to thee, O Lord,\nWho hast appeared this day,\nWith the Father and the Holy Spirit,\nUnto everlasting ages.'],
    hf: ['Jesu, tuis obédiens\nQui factus es paréntibus,\nCum Patre summo ac Spíritu\nSemper tibi sit glória.', 'O Jesu, who wast subject to\nThy parents, glory be to thee,\nWith the most high Father and the Spirit,\nFor evermore.'],
    scj: ['Glória tibi, Dómine,\nQui Corde fundis grátiam,\nCum Patre et Sancto Spíritu,\nIn sempitérna sǽcula.', 'Glory to thee, O Lord,\nWho pourest forth grace from thy Heart,\nWith the Father and the Holy Spirit,\nUnto everlasting ages.'],
    maria: ['María, Mater grátiæ,\nMater misericórdiæ,\nTu nos ab hoste prótege,\nEt hora mortis súscipe.', 'Mary, Mother of grace,\nMother of mercy,\nShield us from the enemy,\nAnd receive us at the hour of death.']
  };
  var DOXOF = {nat: ['natus'], hn: ['natus'], hn2: ['natus'], cc: ['natus'], epi: ['epi'], hf: ['hf'], scj: ['scj'], bvma: ['maria', 'natus'], bvmb: ['maria', 'natus']};
  // Te lucis: the doxology of the feast or season in place of Praesta, Pater (C49 pp. 38-45, 70-79)
  function teLucisText(t, day) {
    if (!/e lucis ante términum|efore the ending of the day/.test(t) || !day) return t;
    var k = teLucisTune(makeToneCtx(day, 'Completorium'), state.date), ds = k && DOXOF[k];
    if (!ds) return t;
    var en = /efore the ending/.test(t) ? 1 : 0;
    var rep = ds.map(function (d) { var x = DOX[d][en]; return '<h>' + x.charAt(0) + '</h>' + x.slice(1); }).join('\n\n') + '\nAmen.';
    return t.replace(/<h>P<\/h>ræsta, Pater omnípotens,[\s\S]*?Amen\./, rep).replace(/<h>O<\/h> Father, that we ask be done,[\s\S]*?Amen\./, rep);
  }
  // Lent and Passiontide (C49 pp. 46-48): from the Saturday after Ash Wednesday to the Saturday before Passion Sunday,
  // R. In pace on Saturdays, Sundays and feasts, R. In manus on other days; from then to Wednesday in Holy Week,
  // R. In manus without Gloria Patri when of the season, with it on saints' feasts
  function lentResp(day) {
    var d = state.date; if (!d) return null;
    var E = easterOf(d.getFullYear()), f = Math.round((new Date(d.getFullYear(), d.getMonth(), d.getDate()) - E) / 864e5);
    if (f < -43 || f > -4) return null;
    var title = makeToneCtx(day, 'Completorium').title, feast = !/^(Feria|Dominica|Sabbato|Hebdomada)/.test(title);
    if (f <= -16) return (d.getDay() === 6 || d.getDay() === 0 || feast) ? 'pace' : 'manus';
    return feast ? 'manus' : 'manusPass';
  }
  var RESP = {
    head: ['\n\n<h>Responsorium</h>\n<n>On a Double or Totum Duplex it is sung by two Friars standing in the middle of the choir; otherwise by the Friar appointed, in his stall.</n>\n', '\n\n<h>Responsory</h>\n'],
    pace: ['<n>It is begun by the Friar who sings its verse; the choir sits for the verse.</n>\n<r>℟.br.</r> In pace in idípsum * Dórmiam et requiéscam.\n<r>℣.</r> Si dédero somnum óculis meis, et pálpebris meis dormitatiónem. * Dórmiam.\n<r>℣.</r> Glória Patri, et Fílio, et Spirítui Sancto.\n<r>℟.</r> In pace in idípsum dórmiam et requiéscam.',
           '<r>℟.</r> In peace in the selfsame * I will sleep and I will rest.\n<r>℣.</r> If I shall give sleep to mine eyes, or slumber to mine eyelids. * I will sleep.\n<r>℣.</r> Glory be to the Father, and to the Son, and to the Holy Ghost.\n<r>℟.</r> In peace in the selfsame I will sleep and I will rest.'],
    manus: ['<r>℟.br.</r> In manus tuas, Dómine, * Comméndo spíritum meum.\nIn manus.\n<r>℣.</r> Redemísti me, Dómine, Deus veritátis. * Comméndo.\n<r>℣.</r> Glória Patri, et Fílio, et Spirítui Sancto. In manus.',
            '<r>℟.</r> Into thy hands, O Lord, * I commend my spirit. Into thy hands.\n<r>℣.</r> Thou hast redeemed us, O Lord, God of truth. * I commend.\n<r>℣.</r> Glory be to the Father, and to the Son, and to the Holy Ghost. Into thy hands.'],
    manusPass: ['<r>℟.br.</r> In manus tuas, Dómine, * Comméndo spíritum meum.\nIn manus.\n<r>℣.</r> Redemísti me, Dómine, Deus veritátis. * Comméndo spíritum meum.\n<r>℟.</r> In manus tuas, Dómine, comméndo spíritum meum.',
                '<r>℟.</r> Into thy hands, O Lord, * I commend my spirit. Into thy hands.\n<r>℣.</r> Thou hast redeemed us, O Lord, God of truth. * I commend my spirit.\n<r>℟.</r> Into thy hands, O Lord, I commend my spirit.']
  };
  function lentText(t, day) {
    if (!/(Capitulum|Chapter)<\/h>\n<r>Jer(em)?\. 14<\/r>/.test(t) || /Responsor/.test(t)) return t;
    var k = lentResp(day); if (!k) return t;
    var en = /Chapter/.test(t) ? 1 : 0;
    return t + RESP.head[en] + RESP[k][en];
  }
  // feasts of Our Lady (C49 pp. 74-80, 81, 86-94, 101-105): the psalms of Sunday under Virgo Maria (or a proper antiphon),
  // at the Nunc dimittis Corde et animo, or Sub tuum on the feasts that the book names
  var MARY = {
    vm: ['Virgo María, non est tibi símilis nata in mundo inter mulíeres, florens ut rosa, fragrans sicut lílium: ora pro nobis, sancta Dei Génitrix.',
         'O Virgin Mary, none like thee hath been born in the world among women, blooming as the rose, fragrant as the lily: pray for us, holy Mother of God.'],
    sdg: ['Sancta Dei Génitrix, Virgo semper María, intercéde pro nobis ad Dóminum Deum nostrum.', 'Holy Mother of God, Mary ever Virgin, intercede for us with the Lord our God.'],
    ev: ['Ecce Virgo concípiet, et páriet Fílium, et vocábitur nomen ejus Emmánuel.', 'Behold, a Virgin shall conceive, and bear a Son, and his name shall be called Emmanuel.'],
    st: ['Sub tuum præsídium confúgimus, sancta Dei Génitrix: nostras deprecatiónes ne despícias in necessitátibus, sed a perículis cunctis líbera nos semper, Virgo benedícta.',
         'We fly to thy patronage, O holy Mother of God: despise not our petitions in our necessities, but deliver us always from all dangers, O blessed Virgin.'],
    ea: ['Ecce ancílla Dómini: fiat mihi secúndum verbum tuum.', 'Behold the handmaid of the Lord: be it done unto me according to thy word.']
  };
  function maryAnts(day) {
    var d = state.date; if (!d || !day) return null;
    var title = makeToneCtx(day, 'Completorium').title; if (!BVM.test(title) && !/Purificatione|Annuntiatione/.test(title)) return null;
    var md = (d.getMonth() + 1) * 100 + d.getDate(), f = Math.round((new Date(d.getFullYear(), d.getMonth(), d.getDate()) - easterOf(d.getFullYear())) / 864e5);
    if (/Purificatione/.test(title) || md === 202 || md === 201) return {ps: 'sdg'};
    if (/Annuntiatione/.test(title) || md === 325 || md === 324) return {ps: 'ev', nd: 'ea'};
    var sub = /Assumpt|Nominis Mari|Septem Dolor|Mediatric/.test(title) || [814, 815, 911, 912, 914, 915, 530, 531].indexOf(md) >= 0 || f === -10 || f === -9;
    return {ps: 'vm', nd: sub ? 'st' : null};
  }
  function maryText(t, day) {
    if (!/<r>Ant\.<\/r> (Miserére|Have mercy)|<r>Ant\.<\/r> (Corde et ánimo|With heart and soul)/.test(t)) return t;
    var m = maryAnts(day); if (!m) return t;
    var en = /Have mercy|With heart and soul|<h>Psalms|Psalm \d/.test(t) ? 1 : 0;
    var nw = {vm: 2, sdg: 1, ev: 2, st: 2, ea: 1}[m.ps], star = function (x) { var w = x.split(' '); return w.slice(0, nw).join(' ') + ' * ' + w.slice(nw).join(' '); };
    t = t.replace(/<r>Ant\.<\/r> (Miserére \* mihi|Have mercy \* on me)[^\n]*/, '<r>Ant.</r> ' + star(MARY[m.ps][en]))
         .replace(/<r>Ant\.<\/r> (Miserére mihi|Have mercy on me)[^\n]*/, '<r>Ant.</r> ' + MARY[m.ps][en]);
    if (m.nd) t = t.replace(/<r>Ant\.<\/r> (Corde et ánimo|With heart and soul)[^\n]*/g, '<r>Ant.</r> ' + MARY[m.nd][en]);
    return t;
  }
  function complineSeason(t) {
    t = dvPriest(t).replace('florens un rosa', 'florens ut rosa');
    var d = state.date; if (!d || !t || !/In manus tuas|Into thy hands|Salva nos, \*|Protect us, \*/.test(t)) return t;
    var md = (d.getMonth() + 1) * 100 + d.getDate(); if (!(md >= 1225 || md <= 113)) return t;
    t = t.replace('In manus tuas, Dómine, * Comméndo spíritum meum.\nIn manus.\n<r>℣.</r> Redemísti me, Dómine, Deus veritátis. * Comméndo.',
                  'In manus tuas, Dómine, comméndo spíritum meum, * Allelúia, allelúia.\nIn manus.\n<r>℣.</r> Redemísti me, Dómine, Deus veritátis. * Allelúia, allelúia.')
      .replace('Into thy hands, O Lord, * I commend my spirit. Into thy hands.\n<r>℣.</r> Thou hast redeemed us, O Lord, God of truth. * I commend.',
               'Into thy hands, O Lord, I commend my spirit, * Alleluia, alleluia. Into thy hands.\n<r>℣.</r> Thou hast redeemed us, O Lord, God of truth. * Alleluia, alleluia.');
    var epi = md >= 106 && md <= 113;
    var la = epi ? ['Allelúia. Omnes de Saba vénient, * allelúia: aurum et thus deferéntes, allelúia, allelúia.', 'Allelúia. Omnes de Saba vénient, allelúia: aurum et thus deferéntes, allelúia, allelúia.']
                 : ['Allelúia. * Verbum caro factum est, allelúia: et habitávit in nobis, allelúia, allelúia.', 'Allelúia. Verbum caro factum est, allelúia: et habitávit in nobis, allelúia, allelúia.'];
    var en = epi ? ['Alleluia. All they from Saba shall come, * alleluia, bringing gold and frankincense, alleluia, alleluia.', 'Alleluia. All they from Saba shall come, alleluia, bringing gold and frankincense, alleluia, alleluia.']
                 : ['Alleluia. * The Word was made flesh, alleluia, and dwelt among us, alleluia, alleluia.', 'Alleluia. The Word was made flesh, alleluia, and dwelt among us, alleluia, alleluia.'];
    return t.replace(/(<r>Ant\.<\/r> )Salva nos, \* Dómine[^\n]*/, '$1' + la[0]).replace(/(<r>Ant\.<\/r> )Salva nos, Dómine[^\n]*/, '$1' + la[1])
      .replace(/(<r>Ant\.<\/r> )Protect us, \* Lord[^\n]*/, '$1' + en[0]).replace(/(<r>Ant\.<\/r> )Protect us, Lord[^\n]*/, '$1' + en[1]);
  }
  function expand(text) {
    return text.split('\n').map(function (l) {
      if (l.charAt(0) !== '§') return l;
      var k = l.slice(1), sh = shards[k.slice(0, 2)] || {};
      return sh[k] || '';
    }).join('\n').split('\n');
  }
  // the hour's rows, said with or without a priest
  // Holy Saturday (C49 pp. 58-60): Compline as usual to the psalms, under the one antiphon Allelúia; after Ecce nunc the
  // Nunc dimittis at once with its antiphon of four Alleluias; Dominus vobiscum and the prayer Spiritum nobis
  var HOLYSAT = [['36189bfff7', 'bd62e26baf'], ['15ad8f25a1', 'a0e021ed94'], ['d4cc46ba42', '90fd4abbec'], ['35d01ad901', 'c9e02f1e9a'],
                 ['@x:e83ddd5568:hs', '@x:c1162e3e14:hs'], ['96b66025d7', 'e6f33d5910'], ['@x:ce328a6ba1:hs', '@x:7f9d6b930f:hs'],
                 ['@x:dff7e0c6b0:hs', '@x:0a624972d8:hs'], ['@x:690c2baea0:sn', '@x:c55577a1eb:sn'], ['e5045c9ece', '7f9023f752'], ['dd930c0583', '8065596881']];
  var SPIRITUM = ['<c>S</c>píritum nobis, Dómine, tuæ caritátis infúnde: ut quos sacraméntis Paschálibus satiásti, tua fácias pietáte concórdes.\nPer Dóminum nostrum Jesum Christum Fílium tuum, qui tecum vivit et regnat in unitáte ejúsdem Spíritus Sancti Deus: per ómnia sǽcula sæculórum.',
                  '<c>P</c>our forth upon us, O Lord, the Spirit of thy love: that those whom thou hast fed with the paschal sacraments may by thy loving-kindness be made of one mind.\n<h>T</h>hrough Jesus Christ, thy Son our Lord, Who liveth and reigneth with thee, in the unity of the same Holy Ghost, God, world without end.'];
  var AL4 = ['Allelúia, allelúia, allelúia, allelúia.', 'Alleluia, alleluia, alleluia, alleluia.'];
  function xform(t, how) {
    if (how === 'hs') {
      t = t.replace(/<r>Ant\.<\/r> Allelúia, \* allelúia, allelúia\./, '<r>Ant.</r> Allelúia.').replace(/<r>Ant\.<\/r> Alleluia, \* alleluia, alleluia\./, '<r>Ant.</r> Alleluia.')
           .replace(/\n<r>Ant\.<\/r> Allel[uú]ia, allel[uú]ia, allel[uú]ia\.$/, '');
      if (/Nunc dimittis/.test(t)) {
        var en = /Canticle/.test(t) ? 1 : 0;
        t = t.replace(/\n<r>Ant\.<\/r> [^\n]*\n(<r>Cantic)/, en ? '\n<n>After the last psalm the Nunc dimittis follows at once.</n>\n$1' : '\n<n>Post Psalmum Ecce nunc sequitur immediate Canticum.</n>\n$1').replace(/<r>Ant\.<\/r> [^\n]*$/, '<r>Ant.</r> ' + AL4[en]);
      }
    }
    if (how === 'al4') t = t.replace(/(<r>Ant\.<\/r> )Allelúia, (\* )?allelúia, allelúia\./g, function (m, a, st) { return a + 'Allelúia, ' + (st || '') + 'allelúia, allelúia, allelúia.'; })
                            .replace(/(<r>Ant\.<\/r> )Alleluia, (\* )?alleluia, alleluia\./g, function (m, a, st) { return a + 'Alleluia, ' + (st || '') + 'alleluia, alleluia, alleluia.'; });
    if (how === 'tri133' || how === 'tri133en') t = t.replace(/\n<r>Ant\.<\/r> Christus[^\n]*$/, how === 'tri133en' ? '\n<n>After Ecce nunc the Nunc dimittis follows at once.</n>' : '\n<n>Finito Psalmo Ecce nunc, immediate sequitur Canticum.</n>');
    if (how === 'tri1' || how === 'tri1en') t = t.replace(/<r>Special Completorium<\/r>\n\n/, how === 'tri1en' ?
        '<h>Psalms</h>\n<n>Jube domne, the blessing, the lesson, Adjutorium, Confiteor, Converte nos and Deus in adjutorium are omitted. When the Friars, bowing profoundly, have said the Pater noster silently, at a sign from the Prior all stand, turn to the altar and sign themselves; the antiphon is begun at once, and the psalms of Sunday are said in a moderate voice, without Gloria Patri.</n>\n' :
        '<h>Psalmi</h>\n<n>Non dicitur Jube, domne, neque Lectio, Adjutorium, Confiteor, Convérte nos aut Deus, in adjutorium. Fratribus profunde inclinatis et Pater noster submissa voce dicto, ad signum Prioris omnes erecti versis vultibus ad altare se signant; statim inchoatur Antiphona, et dicuntur Psalmi de Dominica voce mediocri, sine Glória Patri.</n>\n');
    if (/^tri(Thu|Fri)(en)?$/.test(how)) {
      var fri = /Fri/.test(how), E2 = /en$/.test(how);
      var before = (fri ? (E2 ? '<n>All prostrate again and say the Pater noster silently; then both choirs say alternately, without chant:</n>\n<r>Psalm 50</r>\n§05.78bd93ec68\n' : '<n>Iterum prosternunt se et dicunt secreto Pater noster; deinde ab utroque Choro alternatim sine cantu:</n>\n<r>Psalmus 50</r>\n§05.53ee802b60\n') : '') +
                   (E2 ? '<n>At once, with nothing before it, the Hebdomadarian says the prayer:</n>\n' : '<n>Sine intervallo, absque Dóminus vobíscum et absque Orémus, dicit Hebdomadarius Orationem:</n>\n');
      var after = E2 ? '<n>Amen is not answered; Dominus vobiscum, Benedicamus Domino and the blessing are omitted; the Salve Regina is not sung and there is no sprinkling with holy water. Bowing profoundly, the Friars say the Pater noster and the Credo silently, and at a sign from the Prior all rise.</n>'
                     : '<n>Non respondetur Amen, nec dicitur Dóminus vobíscum, neque Benedicámus Dómino; benedictio non datur, omittitur Antiphona Salve, Regína, nec fit aquæ benedictæ aspersio; sed Fratres profunde inclinati dicunt Pater noster et Credo in Deum, factoque signo a Priore surgunt omnes.</n>';
      t = t.replace(/\n(<c>[RL]<\/c>)/, '\n' + before + '$1').replace(/torméntum:/, 'torméntum.').replace(/\n<n>Non dicitur <k>Qui tecum[\s\S]*$/, '\n' + after);
      if (E2) t = t.replace(/(\n<c>L<\/c>ook down[^\n]*)(\n<n>[\s\S]*)?$/, '$1\n' + after);
    }
    if (how === 'fer4' || how === 'fer4en') t = how === 'fer4en'
      ? '<n>Wednesday in Holy Week (C49 p. 55): there are no prostrations and no preces; holy water is sprinkled during the psalms or the Nunc dimittis. The blessing is given, but the Salve Regina is not sung: at once Fidelium animae is said, and the Friars, bowing profoundly, say the Pater noster and the Credo.</n>'
      : '<n>Feria IV Majoris Hebdomadæ (C49 p. 55): absque prostrationibus et absque Precibus; dum cantantur Psalmi vel Canticum, aqua benedicta aspergitur. Benedictio datur; non cantatur Antiphona Salve, Regína, sed statim subditur Fidélium ánimæ; quo dicto Fratres profunde inclinati dicunt Pater noster et Credo in Deum.</n>';
    if (how === 'sn') {
      var e = /Prayer/.test(t) ? 1 : 0;
      t = t.replace(/<r>℣\.<\/r> [^\n]*\n<r>℟\.<\/r> [^\n]*\n/, e ? '<r>℣.</r> The Lord be with you.\n<r>℟.</r> And with thy spirit.\n' : '<r>℣.</r> Dóminus vobíscum.\n<r>℟.</r> Et cum spíritu tuo.\n')
           .replace(/(<c>[OL]<\/c>(rémus|et us pray)\.\n)[\s\S]*(\n<r>℟\.<\/r> Amen\.)/, '$1' + SPIRITUM[e] + '$3');
    }
    return t;
  }
  function rowsOf(day, hour) {
    var fE = state.date ? Math.round((new Date(state.date.getFullYear(), state.date.getMonth(), state.date.getDate()) - easterOf(state.date.getFullYear())) / 864e5) : 99;
    if (hour === 'Completorium' && fE === -1 && common) return HOLYSAT;
    var rows = day.h[hour] || [], p = state.priest && day.p && day.p[hour];
    // the last days of Holy Week (pp. 55-58)
    if (hour === 'Completorium' && (fE === -3 || fE === -2)) rows = rows.map(function (r, i) {
      var t = blockText(r[0], day), d = fE === -2 ? 'Fri' : 'Thu';
      if (/Special Completorium/.test(t)) return ['@x:' + r[0] + ':tri1', '@x:' + r[1] + ':tri1en'];
      if (/Psalmus 133/.test(t)) return ['@x:' + r[0] + ':tri133', '@x:' + r[1] + ':tri133en'];
      if (/Canticum Simeonis/.test(t)) return ['@x:' + r[0] + ':tri' + d, '@x:' + r[1] + ':tri' + d + 'en'];
      if (/Hodie post Completorium/.test(t)) return null;
      return r;
    }).filter(Boolean);
    if (hour === 'Completorium' && fE === -4) rows = rows.map(function (r) {
      return /^<h>Ad processionem/.test(blockText(r[0], day)) ? ['@x:' + r[0] + ':fer4', '@x:' + r[1] + ':fer4en'] : r;
    });
    // Easter Sunday to Friday (pp. 61-62): the psalms under four Alleluias; to Tuesday, the prayer Spiritum nobis
    if (hour === 'Completorium' && fE >= 0 && fE <= 5) rows = rows.map(function (r) {
      var t = blockText(r[0], day);
      if (/<r>Ant\.<\/r> Allelúia, (\* )?allelúia, allelúia\./.test(t)) return ['@x:' + r[0] + ':al4', '@x:' + r[1] + ':al4'];
      if (fE <= 2 && /<h>Oratio<\/h>/.test(t) && /ísita, quǽsumus/.test(t)) return ['@x:' + r[0] + ':sn', '@x:' + r[1] + ':sn'];
      return r;
    });
    if (p) rows = p.all ? p.all : rows.map(function (row, i) { return p.i[i] || row; });
    if (hour === 'Completorium' && complinePreces(day)) {
      var at = -1;
      rows.forEach(function (r, i) { if (at < 0 && /^<h>Oratio/.test(blockText(r[0], day))) at = i; });
      if (at > 0) rows = rows.slice(0, at).concat([['@preces-la', '@preces-en']], rows.slice(at));
    }
    return rows;
  }
  // Preces at Compline (Completorium O.P. 1949 pp. 19-20): on ferias and simple days, not on Sundays, feasts or within the
  // octaves of Christmas, Easter and Pentecost. Until the pre-1955 calendar is in, "simple" = a feria or a day of the IV class.
  function complinePreces(day) {
    var t = titleOf(day, 'Completorium'), d = state.date; if (!d) return false;
    var md = (d.getMonth() + 1) * 100 + d.getDate(), f = Math.round((d - easterOf(d.getFullYear())) / 864e5);
    if (md >= 1224 || md <= 101 || (f >= -1 && f <= 7) || (f >= 48 && f <= 56) || (f >= -4 && f <= -2)) return false;
    if (/^Dominica/.test(t) || /Sabbato/.test(t) && d.getDay() === 6 && /Dominica/.test(t)) return false;
    return (/^(Feria|Sabbato)/.test(t) && !/Sanct(æ|ae) Mari(æ|ae)/.test(t)) || /(^|[^I])IV\. classis/.test(t);
  }
  var PRECES = {
    la: '<h>Preces</h>\n<n>After the antiphon of the Nunc dimittis:</n>\n<r>Cantor:</r> Kýrie, eléison. <r>Chorus:</r> Christe, eléison. Kýrie, eléison.\n' +
      '<n>All bow, or prostrate according to the season; the Pater noster is said silently; then the Hebdomadarian, rising a little, aloud:</n>\n' +
      '<r>℣.</r> Et ne nos indúcas in tentatiónem.\n<r>℟.</r> Sed líbera nos a malo.\n<r>℣.</r> In pace in idípsum.\n<r>℟.</r> Dórmiam et requiéscam.\n' +
      '<n>Then the Credo is said silently; the Hebdomadarian, standing upright and turned to the altar, aloud:</n>\n' +
      '<r>℣.</r> Carnis resurrectiónem.\n<r>℟.</r> Vitam ætérnam. Amen.\n<r>℣.</r> Dignáre, Dómine, nocte ista.\n<r>℟.</r> Sine peccáto nos custodíre.',
    en: '<h>Preces</h>\n<n>After the antiphon of the Nunc dimittis:</n>\n<r>Cantor:</r> Lord, have mercy. <r>Choir:</r> Christ, have mercy. Lord, have mercy.\n' +
      '<n>All bow, or prostrate according to the season; the Our Father is said silently; then the Hebdomadarian, rising a little, aloud:</n>\n' +
      '<r>℣.</r> And lead us not into temptation.\n<r>℟.</r> But deliver us from evil.\n<r>℣.</r> In peace, in the selfsame.\n<r>℟.</r> I will sleep and I will rest.\n' +
      '<n>Then the Creed is said silently; the Hebdomadarian, standing upright and turned to the altar, aloud:</n>\n' +
      '<r>℣.</r> The resurrection of the body.\n<r>℟.</r> And life everlasting. Amen.\n<r>℣.</r> Vouchsafe, O Lord, this night.\n<r>℟.</r> To keep us without sin.'
  };
  function neededShards(day) {
    var need = {};
    Object.keys(day.h).forEach(function (h) {
      rowsOf(day, h).forEach(function (row) {
        row.forEach(function (id) {
          blockText(id, day).replace(/^§(\d\d)\./gm, function (m, s) { need[s] = 1; return m; });
        });
      });
    });
    return Object.keys(need);
  }

  // a cell: its heading (the first <h> line) and its body lines
  function cell(id, day) {
    var lines = id ? expand(blockText(id, day)) : [], head = '';
    if (lines.length && /^<h>/.test(lines[0])) head = lines.shift().replace(/<\/?h>/g, '').trim();
    while (lines.length && !lines[0].trim()) lines.shift();
    return {head: head, lines: lines};
  }

  function lineClass(l) {
    if (/^<n>\d+:\d+/.test(l)) return 'o-l vs';
    if (/^<r>[^<]*<\/r>$/.test(l)) return 'o-l rub';
    return 'o-l';
  }
  function drawLine(l) {
    if (!l.trim()) return '<div class="o-gap"></div>';
    return '<div class="' + lineClass(l) + '">' + fmt(l) + '</div>';
  }

  // ---------- chant ----------
  function plain(l) { return l.replace(/<[^>]+>/g, ''); }
  // the chantable pieces of a Latin cell: antiphons, the hymn, the short responsory (as build/gb/build_chant.py)
  function chantSegs(lines, head) {
    var segs = [], K = window.OPChant ? OPChant.key : null;
    if (!K || !chantMap) return segs;
    var hymnAt = -1;
    for (var i = 0; i < lines.length; i++) {
      var l = lines[i];
      if (/^<r>Ant\.<\/r>/.test(l)) segs.push({s: i, e: i + 1, kind: 'an', key: K(plain(l).slice(4))});
      else if (/^<[rh]>Hymnus<\/[rh]>$/.test(l.trim())) hymnAt = i + 1;
      else if (/^<r>℟\.<\/r>/.test(l) && /^\* /.test(lines[i + 1] || '')) {
        var e3 = i + 1;
        while (e3 < lines.length && lines[e3].trim()) e3++;
        segs.push({s: i, e: e3, kind: 're', key: 're' + K(plain(l).slice(2))});
        i = e3 - 1;
      }
      else if (/^<r>℟\.br\.<\/r>/.test(l)) {
        var e = i + 1;
        while (e < lines.length && lines[e].trim()) e++;
        segs.push({s: i, e: e, kind: 'rb', key: 'rb' + K(plain(l).slice(5))});
        i = e - 1;
      }
      if (hymnAt < 0 && i === 0 && /Hymnus$/.test(head || '')) hymnAt = 0;
      if (hymnAt >= 0 && i >= hymnAt - 1) {
        var j = hymnAt;
        while (j < lines.length && !lines[j].trim()) j++;
        if (j < lines.length) {
          var end = j, hk = 'hy' + K(plain(lines[j])), whole = chantMap[hk] && chantMap[hk][3];
          if (whole) {
            while (end < lines.length && !/^Amen\.?$/.test(plain(lines[end]).trim()) && !/^<r>℣\.<\/r>/.test(lines[end])) end++;
            if (end < lines.length && /^Amen/.test(plain(lines[end]).trim())) end++;
          } else {
            // only the first stanza is notated: the others are sung to it and stay as text
            while (end < lines.length && lines[end].trim()) end++;
          }
          segs.push({s: j, e: end, kind: 'hy', key: hk});
          i = end - 1;
        }
        hymnAt = -1;
      }
    }
    segs = segs.filter(function (g) { return chantMap[g.key]; });
    if (toneCtx && toneCtx.hour === 'Completorium') segs.forEach(function (g) {
      var tl = g.key === 'hytelucisanteterminum' && teLucisTune(toneCtx, state.date);
      if (tl) { g.file = 'C49-telucis-' + tl; g.mode = TLMODE[tl] || ''; }
      if (g.key === 'rbinmanustuasdominecommendospiritummeum' && lentResp(curDay) === 'manusPass') { g.file = 'C49-inmanus-pass'; g.mode = '4'; g.kind = 'rb'; }
      if (g.kind === 'an' && g.key === 'alleluiaalleluiaalleluia') { g.file = '6913'; g.mode = '8'; }   // C49 p. 63 (Antiphonarium 1933)
      if (g.key === 'hyiesunostraredemptio') {   // Paschaltide hymn: stanzas 5-6 by period (C49 pp. 64-66)
        var E = easterOf(state.date.getFullYear()), f = Math.round((state.date - E) / 864e5);
        g.file = '5793-' + (f < 39 ? 'res' : f < 49 ? 'asc' : 'pent'); g.mode = '4';
      }
    });
    if (window.OPTones && toneCtx) {
      OPTones.segments(lines, head, toneCtx).forEach(function (t) {
        if (!segs.some(function (g) { return t.s < g.e && g.s < t.e; })) segs.push(t);
      });
      segs.sort(function (a, b) { return a.s - b.s; });
    }
    return segs;
  }
  var toneCtx = null, curDay = null;
  function makeToneCtx(day, hour) {
    var title = titleOf(day, hour), m = /\b(I{1,3}|IV)\. classis/.exec(title);
    var rank = m ? {I: 1, II: 2, III: 3, IV: 4}[m[1]] : 4;
    return {hour: hour, title: title, solemn: hour === 'Laudes' || hour === 'Vespera', priest: state.priest, rank: rank,
            sunday: /^Dominica/.test(title), bvm: /Mari[æa]|B\. ?M\. ?V|Beatæ Vírginis/i.test(title),
            bvmSat: /Sancta Maria Sabbato|Sanctæ Mariæ in Sabbato/i.test(title)};
  }

  // Te lucis at Compline: the tune by rank and season (Completorium O.P. 1949, pp. 9-17). The old ranks are read from the title
  // when it gives them (Totum Duplex...); until the pre-1955 calendar is in, the 1960 class stands in for them.
  // Seasons with a tune of their own (Christmastide, Lent to the Octave of the Sacred Heart) keep the default melody for now.
  function easterOf(y) {
    var a = y % 19, b = Math.floor(y / 100), c = y % 100, d = Math.floor(b / 4), e = b % 4, f = Math.floor((b + 8) / 25),
      g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30, i = Math.floor(c / 4), k = c % 4, l = (32 + 2 * e + 2 * i - h - k) % 7,
      m = Math.floor((a + 11 * h + 22 * l) / 451), mo = Math.floor((h + l - 7 * m + 114) / 31), da = ((h + l - 7 * m + 114) % 31) + 1;
    return new Date(y, mo - 1, da, 12);
  }
  var BVM = /B(eat(æ|ae)|\.)\s*Mari(æ|ae)|Mari(æ|ae) Virgin|Sanct(æ|ae) Mari(æ|ae) (in )?Sabbato|Immaculat|Septem Dolor/;
  var TLMODE = {adv: '4', sab: '8', dom: '8', fer: '8', i: '7', tdii: '4', td: '7', d: '3', sd: '8', nat: '4', epi: '4', hn: '4', hf: '2', tri: '1', cc: '8', scj: '1', bvma: '1', bvmb: '2'};
  function teLucisTune(ctx, date) {
    var t = ctx.title || '', y = date.getFullYear(), md = (date.getMonth() + 1) * 100 + date.getDate(), wd = date.getDay();
    var E = (function () { var a = y % 19, b = Math.floor(y / 100), c = y % 100, d = Math.floor(b / 4), e = b % 4, f = Math.floor((b + 8) / 25),
      g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30, i = Math.floor(c / 4), k = c % 4, l = (32 + 2 * e + 2 * i - h - k) % 7,
      m = Math.floor((a + 11 * h + 22 * l) / 451), mo = Math.floor((h + l - 7 * m + 114) / 31), da = ((h + l - 7 * m + 114) % 31) + 1;
      return new Date(y, mo - 1, da); })();
    var dd = function (n) { var x = new Date(E); x.setDate(x.getDate() + n); return x; }, ash = dd(-46), scjOct = dd(68 + 8);
    var dec25 = new Date(y, 11, 25), adv1 = new Date(dec25); adv1.setDate(25 - (dec25.getDay() || 7) - 21);
    var advent = /Advent/.test(t) || (date >= adv1 && md < 1225), perAnnum = (md >= 113 && date < ash) || (date >= scjOct && date < adv1);
    var tempore = /^(Dominica|Feria|Sabbato|Hebdomada)/.test(t) && !/Sanct(æ|ae) Mari(æ|ae) Sabbato/.test(t);
    var old = /Totum Duplex|Duplex|Semiduplex|Simplex/.exec(t);
    // feasts with a tune of their own (C49 pp. 40-45, 70-76): the melody of the feast's hymn, with its doxology
    var f = Math.round((new Date(y, date.getMonth(), date.getDate()) - E) / 864e5);
    var hn = (function () { for (var k = 2; k <= 5; k++) if (new Date(y, 0, k).getDay() === 0) return k; return 2; })();
    var hf = (function () { for (var k = 7; k <= 12; k++) if (new Date(y, 0, k).getDay() === 0) return k; return 12; })();
    if (/Nominis Jesu/.test(t) || md === 100 + hn || md === 100 + hn - 1) return 'hn';
    if (/Famili(æ|ae)/.test(t) || md === 100 + hf || md === 100 + hf - 1) return 'hf';
    if (f >= 55 && f <= 58) return 'tri';                      // both Compline of Trinity Sunday, and Monday and Tuesday after
    if (f >= 59 && f <= 66) return 'cc';                       // Corpus Christi and its octave
    if (f >= 67 && f <= 75) return 'scj';                      // the Sacred Heart and its octave
    // Christmastide (pp. 36-39: the Christmas tune with 'Gloria tibi, Domine, qui natus es de Virgine') from the eve;
    // Epiphany and its octave (pp. 42-44: the same tune, 'qui apparuisti hodie'), from the eve
    if (md >= 1224 || md <= 104) return 'nat';
    if (md >= 105 && md <= 113) return 'epi';
    // feasts of Our Lady (pp. 74-80): I and II class and an octave day, one tune; Totum Duplex, within an octave
    // and her Saturday office, the other; both with the stanza 'Maria, Mater gratiae'
    if (BVM.test(t)) return /(^|[^I])I{1,2}\. classis/.test(t) ? 'bvma' : 'bvmb';
    if (tempore && !old) return advent ? (wd === 6 || wd === 0 ? 'adv' : 'fer') : perAnnum ? (wd === 6 ? 'sab' : wd === 0 ? 'dom' : 'fer') : null;
    if (/(^|[^I])I\. classis/.test(t)) return 'i';
    {
      if (old) return old[0] === 'Totum Duplex' ? (/II\. classis|Apostol/.test(t) ? 'tdii' : 'td') : old[0] === 'Duplex' ? 'd' : 'sd';
      return ctx.rank === 2 ? 'tdii' : ctx.rank === 3 ? 'd' : 'sd';
    }
  }
  var LABEL = {an: 'Ant.', hy: 'Hymn.', rb: 'R. br.', re: 'R.'};
  function chantDiv(g) {
    if (g.file) return '<div class="chant o-chant" data-id="' + esc(g.file) + '" data-mode="' + esc(g.mode || '') + '" data-tp="1" data-kind="' + (g.kind || 'hy') + '"></div>';
    if (g.gabc || g.ben) {
      if (g.ben === null) return '';
      if (g.ben && g.ben.id) return '<div class="chant o-chant" data-id="' + g.ben.id + '" data-mode="" data-tp="0" data-kind="ben"></div>';
      return '<div class="chant o-chant" data-g="' + esc((g.ben && g.ben.gabc) || g.gabc) + '" data-kind="' + g.kind + '"></div>';
    }
    var m = chantMap[g.key];
    return '<div class="chant o-chant" data-id="' + esc(m[0]) + '" data-mode="' + esc(m[1]) + '" data-tp="' + m[2] + '" data-kind="' + g.kind + '"></div>' +
      (m[5] === 'R' ? '<p class="o-note">Roman melody (Antiphonale Romanum, 1912): the Dominican one is not yet transcribed here.</p>' : '');
  }
  function drawChants(main) {
    Array.prototype.forEach.call(main.querySelectorAll('.o-chant[data-g]'), function (box) {
      OPChant.render(box, box.getAttribute('data-g'), {dropCap: false, keepTP: true});
    });
    Array.prototype.forEach.call(main.querySelectorAll('.o-chant[data-id]'), function (box) {
      getText('data/chant/op/' + box.getAttribute('data-id') + '.gabc').then(function (g) {
        var kind = box.getAttribute('data-kind'), tp = box.getAttribute('data-tp') === '1';
        OPChant.render(box, g, {mode: box.getAttribute('data-mode'), label: LABEL[kind], keepTP: tp, dropCap: kind !== 'rb' && kind !== 'ben'});
      }).catch(function () { box.textContent = ''; });
    });
  }
  // psalms: the tone of the antiphon, its first verse notated, the others pointed
  function drawPsalms(main) {
    if (!window.OPPsalm) return;
    var groups = {};
    Array.prototype.forEach.call(main.querySelectorAll('.o-pv[data-ps]'), function (el) {
      (groups[el.getAttribute('data-ps')] = groups[el.getAttribute('data-ps')] || []).push(el);
    });
    Object.keys(groups).forEach(function (k) {
      var m = chantMap[k];
      if (!m) return;
      getText('data/chant/op/' + m[0] + '.gabc').then(function (g) {
        var mode = parseInt(m[1], 10);
        if (!(mode >= 1 && mode <= 8)) return;
        var tone = OPPsalm.toneOf(mode, m[4] || OPPsalm.chooseDiff(mode, g));
        if (!tone) return;
        groups[k].forEach(function (el) {
          var cant = el.getAttribute('data-cant') === '1', first = el.getAttribute('data-first') === '1';
          var pv = OPPsalm.pointVerse(el.getAttribute('data-t'), tone, {inton: first || cant, solemn: cant});
          var num = el.getAttribute('data-num') || '';
          if (first) {
            // the first verse is sung from the notes, its translation beneath, as with the antiphon
            var row = el.classList.contains('o-la') ? el.parentNode : el;
            var tname = 'Tonus ' + tone.name.replace('IVA', 'IV') + (tone.diff ? ' ' + tone.diff : '');
            var prev = row.previousElementSibling, ph = prev && (prev.querySelector('.o-la') || prev);
            if (ph && /^(Psalmus|Canticum)/.test(ph.textContent.trim()) && !ph.querySelector('.o-tone')) {
              ph.insertAdjacentHTML('beforeend', ' <span class="o-tone">' + tname + '</span>');
            } else {
              var lab = document.createElement('div');
              lab.className = 'o-tone o-tone-b';
              lab.textContent = tname;
              row.parentNode.insertBefore(lab, row);
            }
            var box = document.createElement('div');
            box.className = 'chant o-chant';
            row.parentNode.insertBefore(box, row);
            var en = row.querySelector('.o-en');
            if (en && en !== el) {
              var tr = document.createElement('div');
              tr.className = 'o-tr';
              tr.innerHTML = en.innerHTML;
              row.parentNode.insertBefore(tr, row);
            }
            row.style.display = 'none';
            OPChant.render(box, OPPsalm.verseGabc(pv, tone), {dropCap: false, keepTP: true});
            return;
          }
          el.innerHTML = (num ? fmt(num) + ' ' : '') + OPPsalm.verseHtml(pv, esc);
          el.classList.add('o-pointed');
        });
      }).catch(function () {});
    });
  }
  var textCache = {};
  function getText(url) {
    if (!textCache[url]) {
      textCache[url] = fetch(url).then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); });
      textCache[url].catch(function () { delete textCache[url]; });
    }
    return textCache[url];
  }

  // a psalm or canticle verse (or its doxology)
  function isVerse(l) { return /^<n>\d+:\d+[a-z]?<\/n>/.test(l) || /^<r>[℣℟]\.<\/r>\s*(Glória Patri|Sicut erat)/.test(l); }
  function verseAttrs(l, ps, la) {
    var t = plain(l.replace(/^<n>[^<]*<\/n>\s*/, '').replace(/^<r>[℣℟]\.<\/r>\s*/, '')).trim();
    var num = (/^(<n>[^<]*<\/n>|<r>[℣℟]\.<\/r>)\s*/.exec(l) || ['', ''])[1];
    var a = ' data-ps="' + esc(ps.ant) + '" data-t="' + esc(t) + '" data-num="' + esc(num) + '"';
    if (ps.first) { a += ' data-first="1"'; ps.first = false; }
    if (ps.cant) a += ' data-cant="1"';
    return a;
  }

  function drawRow(row, day, ps) {
    ps = ps || {};
    curDay = day;
    var la = cell(row[0], day), en = cell(row[1], day), lang = state.lang, html = '';
    var same = en.lines.join('\n') === la.lines.join('\n');
    if (la.head || en.head) {
      html += '<h3 class="o-h">' + esc(lang === 'en' ? (en.head || la.head) : (la.head || en.head)) +
        (lang === 'both' && en.head && la.head && en.head !== la.head ? ' <span class="o-h-en">' + esc(en.head) + '</span>' : '') + '</h3>';
    }
    var segs = state.chant && lang !== 'en' ? chantSegs(la.lines, la.head) : [];
    ps.cant = /Benedictus|Magnificat/.test(la.head || '');
    var psalmCell = state.chant && lang !== 'en' && chantMap && (segs.length || ps.ant) && la.lines.some(isVerse);
    var at = {};
    segs.forEach(function (g) { at[g.s] = g; });
    var paired = lang === 'both' && !same && en.lines.length && la.lines.length === en.lines.length;
    if ((segs.length || psalmCell) && (lang === 'la' || paired || !en.lines.length || same)) {
      // chant in place of the Latin text; in "both", the English follows each chant as a translation
      var out = '';
      for (var i = 0; i < la.lines.length; i++) {
        var g = at[i];
        if (g) {
          if (g.kind === 'an') { ps.ant = g.key; ps.first = true; }
          out += chantDiv(g);
          if (paired) out += '<div class="o-tr">' + en.lines.slice(g.s, g.e).filter(function (x) { return x.trim(); }).map(fmt).join('<br>') + '</div>';
          i = g.e - 1;
          continue;
        }
        var l = la.lines[i];
        if (/^<r>Ant\.<\/r>/.test(l)) ps.ant = null;      // an antiphon without its chant: its psalm stays read
        var va = ps.ant && isVerse(l) ? verseAttrs(l, ps, la) : '';
        if (paired) {
          var e2 = en.lines[i];
          out += (!l.trim() && !e2.trim()) ? '<div class="o-gap"></div>' :
            '<div class="o-lp ' + lineClass(l) + '"><div class="o-la' + (va ? ' o-pv"' + va : '"') + '>' + fmt(l) + '</div><div class="o-en">' + fmt(e2) + '</div></div>';
        } else if (va) out += '<div class="' + lineClass(l) + ' o-pv"' + va + '>' + fmt(l) + '</div>';
        else out += drawLine(l);
      }
      html += '<div class="' + (paired ? 'o-lines' : 'o-col') + '">' + out + '</div>';
    } else if (segs.length) {
      // Latin and English of different lengths: chant in the Latin column
      var col = '';
      for (var k = 0; k < la.lines.length; k++) {
        if (at[k]) { col += chantDiv(at[k]); k = at[k].e - 1; } else col += drawLine(la.lines[k]);
      }
      html += '<div class="o-pair"><div class="o-la">' + col + '</div><div class="o-en">' + en.lines.map(drawLine).join('') + '</div></div>';
    } else if (lang === 'la' || !en.lines.length || same) {
      html += '<div class="o-col">' + la.lines.map(drawLine).join('') + '</div>';
    } else if (lang === 'en') {
      html += '<div class="o-col">' + en.lines.map(drawLine).join('') + '</div>';
    } else if (la.lines.length === en.lines.length) {
      // line by line, so that each verse sits beside its translation
      html += '<div class="o-lines">' + la.lines.map(function (l, i) {
        var e = en.lines[i];
        if (!l.trim() && !e.trim()) return '<div class="o-gap"></div>';
        return '<div class="o-lp ' + lineClass(l) + '"><div class="o-la">' + fmt(l) + '</div><div class="o-en">' + fmt(e) + '</div></div>';
      }).join('') + '</div>';
    } else {
      html += '<div class="o-pair"><div class="o-la">' + la.lines.map(drawLine).join('') +
        '</div><div class="o-en">' + en.lines.map(drawLine).join('') + '</div></div>';
    }
    return '<section class="o-sec">' + html + '</section>';
  }

  function titleOf(day, hour) {
    var t = (hour === 'Vespera' || hour === 'Completorium') && day.tv && day.tv.length ? day.tv : day.t;
    t = (t && t[0]) || '';
    return window.OPNames ? OPNames.la(t) : t;
  }

  function draw() {
    var main = $('#office'), d = state.date, key = iso(d);
    if (state.cal) state.cal.set(d);
    $('#date').value = key;
    drawHours();
    if (range && (key < range.from || key > range.to)) {
      main.innerHTML = '<p class="o-msg">The Office is ready for every day from ' + range.from + ' to ' + range.to + '. This date is outside that range for now.</p>';
      $('#dayTitle').textContent = ''; $('#dayRank').textContent = ''; $('#dayMeta').textContent = shortDate(d);
      return;
    }
    main.innerHTML = '<p class="o-msg">…</p>';
    Promise.all([getJSON(BASE + key.slice(0, 4) + '/' + key.slice(5) + '.json'), common ? null : getJSON(BASE + 'common.json'),
      state.chant && !chantMap ? getJSON('data/chant/office.json').then(function (m) { chantMap = m; }).catch(function () {}) : null])
      .then(function (r) {
        var day = r[0];
        if (r[1]) common = r[1];
        return Promise.all(neededShards(day).filter(function (s) { return !shards[s]; }).map(function (s) {
          return getJSON(BASE + 'psalter/' + s + '.json').then(function (j) { shards[s] = j; });
        })).then(function () { return day; });
      })
      .then(function (day) {
        if (iso(state.date) !== key) return;
        var hour = state.hour, h = HOURS.filter(function (x) { return x[0] === hour; })[0];
        var full = titleOf(day, hour), t = full.split(' ~ ');
        $('#dayTitle').textContent = t[0];
        $('#dayRank').textContent = t[1] || '';
        $('#dayMeta').textContent = shortDate(d);
        var rows = rowsOf(day, hour);
        main.innerHTML = '<header class="o-head"><h1>' + esc(h[1]) + '</h1><p class="o-sub">' + esc(h[2]) + '</p></header>' +
          (function () { var ps = {}; toneCtx = state.chant ? makeToneCtx(day, hour) : null; return rows.map(function (row) { return drawRow(row, day, ps); }).join(''); })() +
          '<p class="o-src">Text from Divinum Officium, <i>Ordo Praedicatorum – 1962</i> (MIT licence), following the Breviarium S.O.P. (1962). English is Divinum Officium’s; where a Dominican text has no English yet, the Latin stands alone.</p>';
        document.title = h[2] + ' — ' + t[0];
        if (state.chant) { drawChants(main); drawPsalms(main); }
      })
      .catch(function () {
        main.innerHTML = '<p class="o-msg">The Office for this day could not be loaded. If you are offline, open the day once while online to keep it.</p>';
      });
  }

  function drawHours() {
    $('#hours').innerHTML = HOURS.map(function (h) {
      var on = h[0] === state.hour;
      return '<button type="button" role="tab" data-h="' + h[0] + '" aria-selected="' + on + '" class="sbtn' + (on ? ' on' : '') + '">' + h[2] + '</button>';
    }).join('');
    var lb = $('#langs');
    if (lb) Array.prototype.forEach.call(lb.querySelectorAll('button'), function (b) {
      var on = b.getAttribute('data-l') === (window.OPLang ? OPLang.get() : 'tap');
      b.classList.toggle('on', on); b.setAttribute('aria-pressed', on);
    });
    var pr = $('#priest');
    if (pr) pr.checked = state.priest;
    var ch = $('#chant');
    if (ch) ch.checked = state.chant;
  }

  function setHash() {
    var h = '#' + state.hour + '&d=' + iso(state.date);
    if (location.hash !== h) history.replaceState(null, '', h);
  }
  function go() { setHash(); draw(); window.scrollTo(0, 0); }

  function readHash() {
    var m = /^#(\w+)(?:&d=(\d{4}-\d\d-\d\d))?/.exec(location.hash);
    state.hour = m && HOURS.some(function (h) { return h[0] === m[1]; }) ? m[1] : hourNow();
    state.date = (m && parseIso(m[2])) || new Date(new Date().setHours(0, 0, 0, 0));
  }

  function start() {
    if (!$('#office')) return;
    readHash();
    $('#hours').addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      state.hour = b.getAttribute('data-h'); go();
    });
    var lb = $('#langs');
    if (lb) lb.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      var m = b.getAttribute('data-l');
      if (window.OPLang) OPLang.set(m);
      state.lang = m === 'en' ? 'en' : 'both';
      draw();
    });
    var pr = $('#priest');
    var ch = $('#chant');
    if (ch) ch.addEventListener('change', function () {
      state.chant = this.checked;
      try { localStorage.setItem('officeChant', state.chant ? '1' : '0'); } catch (er) {}
      draw();
    });
    if (pr) pr.addEventListener('change', function () {
      state.priest = this.checked;
      try { localStorage.setItem('officePriest', state.priest ? '1' : '0'); } catch (er) {}
      draw();
    });
    if (window.matchMedia && matchMedia('(max-width: 960px)').matches) Array.prototype.forEach.call(document.querySelectorAll('.side .collapse'), function (x) { x.removeAttribute('open'); });
    if (window.OPCal && $('#cal')) state.cal = OPCal($('#cal'), {date: state.date, onPick: function (d) { state.date = d; go(); }});
    $('#prevDay').addEventListener('click', function () { state.date = addDays(state.date, -1); go(); });
    $('#nextDay').addEventListener('click', function () { state.date = addDays(state.date, 1); go(); });
    $('#date').addEventListener('change', function () { var d = parseIso(this.value); if (d) { state.date = d; go(); } });
    window.addEventListener('hashchange', function () { readHash(); draw(); });
    getJSON(BASE + 'range.json').then(function (r) { range = r; }).catch(function () {}).then(function () { setHash(); draw(); });
  }

  window.OfficeOP = {iso: iso, state: function () { return state; }, cell: cell};
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
