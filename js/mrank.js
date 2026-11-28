/* Missal ranking engine: which Mass is said on a date, by the Dominican rite before 1955.
 * Missal only (the Breviary has its own engine, kept by the Office pages).
 *
 * Sources: Missale O.P. 1939 (M39), Rubricae generales I-VIII (tools/orat39/m39lin.txt 6300-6955), its Kalendarium with
 * the supplements approved before 1955 (data/kalendar39.js), and the rubrics printed in the Proper. The Missal refers the
 * table of occurrence to the Breviary, which we do not have for 1923-1954; the order of precedence below was therefore
 * read from the Ordo O.P. of 1944 (Prov. Poloniae, tools/ordo44), day by day. Each rule cites what it rests on.
 *
 * Usage: OPMissalRank(KAL39, masses).day(date) -> {office, masses, win, commems, ...}; in node:
 *   require('./js/mrank.js')(KAL39, masses)
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory;
  else root.OPMissalRank = factory;
})(typeof window !== 'undefined' ? window : this, function (KAL, MASSES) {
  'use strict';
  MASSES = MASSES || {};
  var DAY = 864e5;
  function addDays(d, n) { var r = new Date(d.getFullYear(), d.getMonth(), d.getDate()); r.setDate(r.getDate() + n); return r; }
  function diffDays(a, b) { return Math.round((Date.UTC(a.getFullYear(), a.getMonth(), a.getDate()) - Date.UTC(b.getFullYear(), b.getMonth(), b.getDate())) / DAY); }
  function iso(d) { return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  function mmdd(d) { return String(d.getMonth() + 1).padStart(2, '0') + String(d.getDate()).padStart(2, '0'); }
  function easter(y) { // Anonymous Gregorian algorithm
    var a = y % 19, b = Math.floor(y / 100), c = y % 100, d = Math.floor(b / 4), e = b % 4, f = Math.floor((b + 8) / 25),
        g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30, i = Math.floor(c / 4), k = c % 4,
        l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451),
        month = Math.floor((h + l - 7 * m + 114) / 31), day = ((h + l - 7 * m + 114) % 31) + 1;
    return new Date(y, month - 1, day);
  }
  function adv1(y) { var n = new Date(y, 11, 25); return addDays(n, -((n.getDay() || 7) + 21)); }
  function leap(y) { return (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0; }
  var WD = ['', 'm', 't', 'w', 'h', 'f', 's'];
  function has(k) { return !!(k && MASSES[k]); }

  // ------------------------------------------------------------------ precedence values (higher wins)
  // From the Ordo O.P. 1944: minor Sundays yield to Totum Duplex I and II classis (Raymund 23 Jan, Visitation 2 Jul,
  // Gorcum 9 Jul, Transfiguration 6 Aug, Rosary 1 Oct) and beat the rest (Carmel 16 Jul commemorated); Sundays of the
  // II class yield to the I class only (Catherine de' Ricci, Totum Duplex II classis, moved from Sexagesima to 14 Feb);
  // Sundays of the I class to nothing (St Joseph moved from Laetare to 20 Mar). Major ferias (Advent, Lent, Ember days,
  // Rogations) and common vigils yield in the Office to Simplex and above (B. Constantius, Semiduplex, 26 Feb; Damasus,
  // Simplex, 11 Dec), not to Tres Lectiones (Rubr. IV.2 lists Totum Duplex, Duplex, Semiduplex, Simplex). Days within
  // the octaves of the Epiphany and Corpus Christi yield to the I class only (St Antony, Duplex, 13 Jun 1944:
  // De oct. 4-o; Rubr. IV.2 "Octavas privilegiatas Epiphaniae et SS. Corporis Christi"); days within the octaves of
  // Christmas, the Ascension and the Sacred Heart yield to Semiduplex and above (Thomas of Canterbury 29 Dec, Peter
  // Celestine 19 May, B. Columba 20 May, B. Hosanna 20 Jun), and beat Tres Lectiones (Gervase and Protase, 19 Jun);
  // days within solemn octaves yield even to Simplex (Damasus within the octave of the Immaculate Conception).
  var RANK_PV = {'Totum Duplex I classis': 90, 'Totum Duplex II classis': 80, 'Totum Duplex': 60, 'Duplex': 50,
    'Semiduplex': 40, 'Simplex': 30, 'Tres Lectiones': 20, 'Octava solemnissima': 79, 'Octava solemnis': 79, 'Memoria': 5};
  // Breviarium S.O.P. 1924 (Theissling), Rubricae generales (tools/b24): § II (Sundays of the I class yield to no feast, of
  // the II class to Totum Duplex I classis only; privileged ferias to none, the others only beat Tres Lectiones; the Vigils of
  // Christmas and Pentecost to none, of the Epiphany to the I and II class and feasts of the Lord); § XXIX.3 (minor Sundays
  // yield to the I and II class and to feasts of the Lord of nine lessons, not to octave days); § XXIX.10 (the octaves of
  // Easter and Pentecost beat every feast; within those of the Epiphany and Corpus Christi only the I class wins, and on their
  // octave day only the I class of the universal Church; within the octave of Christmas, the Ascension and all solemn
  // octaves only Tres Lectiones and days within simple octaves lose, on their octave day every feast below the II class)
  var PV = {feriaMajor: 21.6, feriaAdv: 21, vigil: 21.5, bvmSat: 22, inOctSimplex: 22, inOctSolemn: 25, inOctPrivLow: 25, inOctPriv: 87,
    sundayMinor: 79.5, sundayII: 88, sundayI: 96, octDay: 79, octDayPriv: 89.5, orderI: 89, lordOnSunday: 79.7, vigEpi: 78};
  // Offices of the Saints with a proper Homily or proper Responsories (Breviarium S.O.P. 1924, Proprium Sanctorum, read by
  // tools/b24/homily.py): on these days the Homily of an impeded Sunday is not read, nor its Mass resumed (§ VII.2)
  var NOT_VACANT = {}; '0102 0103 0104 0115 0117 0118 0121 0122 0123 0125 0126 0130 0201 0202 0205 0211 0212 0213 0222 0223 0307 0308 0312 0318 0319 0322 0324 0325 0327 0401 0404 0405 0411 0414 0425 0429 0503 0510 0520 0601 0611 0614 0618 0624 0628 0629 0630 0701 0702 0705 0706 0709 0710 0712 0722 0725 0729 0801 0804 0806 0807 0808 0810 0811 0815 0816 0817 0822 0824 0825 0827 0828 0829 0830 0902 0908 0912 0914 0915 0917 0919 0921 0924 0925 0929 0930 1002 1004 1006 1010 1014 1015 1018 1024 1028 1101 1102 1103 1106 1108 1109 1111 1112 1117 1118 1119 1121 1122 1123 1125 1130 1203 1206 1207 1208 1210 1215 1221 1226 1227 1228 1229 1231'.split(' ').forEach(function (k) { NOT_VACANT[k] = 1; });
  function rankShort(r) {
    return {'Totum Duplex I classis': 'Totum Duplex, I class', 'Totum Duplex II classis': 'Totum Duplex, II class'}[r] || r;
  }

  // ------------------------------------------------------------------ the Proper of the Time
  // the site key of the Mass of the Time for a date (the Mass of the day, or of the preceding Sunday on a free feria)
  function temporaleKey(d) {
    var y = d.getFullYear(), dow = d.getDay();
    var E = easter(y), fromE = diffDays(d, E);
    var nat = new Date(y, 11, 25), a1 = adv1(y);
    var c = [];
    if (d >= a1 && d < nat) {
      var w = Math.floor(diffDays(d, a1) / 7) + 1;
      if (w === 3 && dow === 3) c.push('Adv3w');
      if (w === 3 && dow === 5) c.push('Adv3f');
      if (w === 3 && dow === 6) c.push('Adv3s');
      if (d.getMonth() === 11 && d.getDate() === 24) c.push('Dec24');
      c.push('Adv' + Math.min(w, 4));
      return c;
    }
    var md = (d.getMonth() + 1) * 100 + d.getDate();
    if (md === 1225) return ['Dec25_3', 'Dec25_1', 'Dec25_2'];
    if (md > 1225) return dow === 0 ? ['Nat1'] : ['Dec25_3'];
    if (md === 101) return ['Jan1'];
    if (md >= 102 && md <= 105) {
      var sunIn = [2, 3, 4, 5].some(function (dd) { return new Date(y, 0, dd).getDay() === 0; });
      if (dow === 0 || (md === 102 && !sunIn)) return ['Nat2'];
      return md === 105 ? ['Jan5a', 'Jan1'] : ['Jan1', 'Nat2'];
    }
    if (md === 106) return ['Epi'];
    var sept = addDays(E, -63);
    if (md > 106 && d < sept) {
      var epi = new Date(y, 0, 6), epi1 = addDays(epi, 7 - epi.getDay());
      if (d < epi1) return ['Epi'];
      return ['Epi' + Math.min(Math.floor(diffDays(d, epi1) / 7) + 1, 6)];
    }
    if (fromE >= -63 && fromE < -46) return [['7a', '6a', '5a'][Math.floor((fromE + 63) / 7)]];
    if (fromE >= -46 && fromE < -42) return ['5a' + WD[dow]];
    if (fromE >= -42 && fromE < 0) {
      var q = Math.floor((fromE + 42) / 7) + 1;
      // Friday in Passion Week: the feria (Quad5fe); its feast, the Compassion of Our Lady, is Quad5f
      if (q === 5 && dow === 5 && MASSES.Quad5fe) return ['Quad5fe'];
      return MASSES['Quad' + q + WD[dow]] || !Object.keys(MASSES).length ? ['Quad' + q + WD[dow]] : ['Quad' + q];
    }
    if (fromE >= 0 && fromE < 7) return ['Pasc0' + WD[dow]];
    if (fromE === 39) return ['Asc'];
    if (fromE === 48) return ['Pasc6s'];
    if (fromE >= 7 && fromE < 49) {
      var p = Math.floor(fromE / 7);
      if (fromE === 36 || fromE === 37) return ['Pasc5', 'Litaniis'];
      if (fromE === 38) return ['AscVig', 'Litaniis'];
      if (fromE > 39) return dow === 0 || fromE > 46 ? ['Pasc6'] : ['Asc'];
      if (p === 2 && dow === 3) return ['Pasc2', 'Pasc2w'];
      return [dow === 0 ? 'Pasc' + p : 'Pasc' + p];
    }
    if (fromE >= 49 && fromE < 56) return ['Pent0' + WD[dow]];
    if (fromE === 56) return ['Pent1'];
    if (fromE === 60) return ['CorpusChristi'];
    if (fromE === 68) return ['SCJ'];
    if (fromE >= 56) {
      var a1n = adv1(y), n = Math.floor((fromE - 49) / 7), keys = [];
      // the September Ember days: Wednesday, Friday and Saturday after the Exaltation of the Holy Cross (Missale O.P. 1939,
      // Quatuor Tempora, p. [8]; Brev. 1924 likewise)
      var x14 = new Date(y, 8, 14), ew = addDays(x14, ((3 - x14.getDay() + 7) % 7) || 7), ed = diffDays(d, ew);
      if (ed === 0) keys.push('EmbWedSept'); if (ed === 2) keys.push('EmbFriSept'); if (ed === 3) keys.push('EmbSatSept');
      // the last Sunday has its own Mass; the Sundays between the twenty-first after the Octave of Trinity and the last
      // take the prayers and lessons of the Sundays left over after the Epiphany (Missale O.P. 1939)
      var dS = diffDays(a1n, d) + dow;
      if (n === 1 || fromE < 63) keys.push(fromE < 60 ? 'Pent1' : 'CorpusChristi');
      else if (dS <= 7) keys.push('Pent24');
      else if (n >= 24) keys.push('Epi' + Math.max(3, Math.min(6, 8 - Math.round(dS / 7))) + 'r');
      else keys.push('Pent' + Math.min(n, 23));
      return keys;
    }
    return [];
  }

  // the day of the Proper of the Time: what it is and how it stands in occurrence
  function temporal(d) {
    var y = d.getFullYear(), dow = d.getDay(), E = easter(y), fromE = diffDays(d, E), md = mmdd(d);
    var keys = temporaleKey(d), key = keys[0], t = {keys: keys, key: key, dow: dow, pv: 0, kind: 'feria', ownMass: false,
      major: false, season: '', fromE: fromE};
    var a1 = adv1(y), nat = new Date(y, 11, 25), sept = addDays(E, -63), ash = addDays(E, -46);
    if (d >= a1 && d < nat) t.season = 'adv';
    else if (md >= '1225' || md <= '0113') t.season = 'nat';
    else if (d < sept) t.season = 'epi';
    else if (d < ash) t.season = 'sept';
    else if (fromE < -14) t.season = 'quad';
    else if (fromE < 0) t.season = 'pass';
    else if (fromE < 56) t.season = 'pasch';
    else t.season = 'pent';
    var sunday = dow === 0;
    if (sunday) {
      t.kind = 'sunday'; t.pv = PV.sundayMinor;
      // Sundays of the I and II class (Ordo 1944: Dom. I Adventus, I-IV Quadragesimae, in Passione, in Ramis,
      // in Albis "1. cl."; II-IV Adventus, Septuagesima, Sexagesima, Quinquagesima "2. cl.")
      if (/^(Adv1|Quad[1-6]|Pasc1)$/.test(key)) t.pv = PV.sundayI;
      else if (/^(Adv[2-4]|7a|6a|5a)$/.test(key)) t.pv = PV.sundayII;
      if (/^(Pasc0|Pent0)/.test(key)) { t.pv = 100; t.kind = 'feast'; }
      if (key === 'Pasc1') t.octday = 'Pasc0';
    }
    // privileged days of the Time
    if (/^(Pasc0|Pent0)$/.test(key) || /^(Quad6[hfs]|Epi)$/.test(key) && !(key === 'Epi' && md !== '0106') || /^Dec25/.test(key) && md === '1225') { t.pv = 100; t.kind = 'feast'; }
    if (/^(Pasc0|Pent0)[mt]$/.test(key)) { t.pv = 98; t.kind = 'octave'; }
    if (/^(Pasc0|Pent0)[whfs]$/.test(key)) { t.pv = 97; t.kind = 'octave'; }
    if (key === '5aw' || /^Quad6[mtw]$/.test(key)) { t.pv = 99; t.ownMass = true; }
    if (key === 'Dec24') { t.pv = 95; t.kind = 'vigil'; t.ownMass = true; }
    if (key === 'Pasc6s') { t.pv = 95; t.kind = 'vigil'; t.ownMass = true; }
    if (key === 'Jan5a') { t.pv = PV.vigEpi; t.kind = 'vigil'; t.ownMass = true; }
    // Lent ferias from Thursday after Ash Wednesday, Passiontide ferias before Palm Sunday, Ember days, Rogations,
    // the Vigil of the Ascension ("feria major", Rubr. IV.2): major ferias with a Mass of their own
    if (!sunday && (t.season === 'quad' || t.season === 'pass') && fromE > -46 && fromE < -7) { t.pv = PV.feriaMajor; t.major = true; t.ownMass = true; t.lent = true; }
    if (/^(Adv3[wfs]|Quad1[wfs]|EmbWedSept|EmbFriSept|EmbSatSept)$/.test(key)) { t.pv = PV.feriaMajor; t.major = true; t.ownMass = true; t.ember = true; }
    if (keys.indexOf('Litaniis') >= 0) { t.pv = PV.feriaMajor; t.major = true; t.ownMass = true; t.rogation = true; }
    if (key === 'AscVig') { t.vigil = true; }
    // 25 April, the Greater Litanies (Rubr. IV.4: if it is Easter Sunday, on the Tuesday after Easter)
    if ((md === '0425' && fromE !== 0) || (fromE === 2 && mmdd(E) === '0425')) { t.rogation = true; t.litMaj = true; if (t.pv < PV.feriaMajor) t.pv = PV.feriaMajor; }
    // Advent ferias: major, but the Mass is that of the Sunday (Ordo 1944, 19 Dec.: Missa de Dom. praec.)
    if (!sunday && t.season === 'adv' && !t.ember && key !== 'Dec24') { t.pv = PV.feriaAdv; t.major = true; }
    // the temporal feasts and their octaves
    var tf = null;
    // the Circumcision beats every feast, even of the I class (§ XXIX.10)
    if (md === '0101') tf = {key: 'Jan1', rank: 'Totum Duplex II classis', title: 'Circumcisio Domini', pv: 100};
    if (key === 'Nat2' && (sunday || md === '0102')) tf = {key: 'Nat2', rank: 'Totum Duplex I classis', title: 'SS. Nominis Jesu'};
    if (md === '0106') tf = {key: 'Epi', rank: 'Totum Duplex I classis', title: 'Epiphania Domini', pv: 100};
    if (fromE === 39) tf = {key: 'Asc', rank: 'Totum Duplex I classis', title: 'Ascensio Domini', pv: 92};
    if (fromE === 56) tf = {key: 'Pent1', rank: 'Totum Duplex I classis', title: 'Festum SS. Trinitatis', pv: 91};
    if (fromE === 60) tf = {key: 'CorpusChristi', rank: 'Totum Duplex I classis', title: 'Festum SS. Corporis Christi', pv: 92};
    if (fromE === 68) tf = {key: 'SCJ', rank: 'Totum Duplex I classis', title: 'Festum SS. Cordis Jesu', pv: 92};
    // Missale O.P. 1939, Festa mobilia (p. 14)
    if (fromE === -52) tf = {key: 'S0430', rank: 'Totum Duplex', title: 'Translatio S. Catharinae Senensis Virg. O. P.', note: 'Mass as on 30 April, with Credo (Missal p. [Translatio])'};
    if (fromE === -9) tf = {key: MASSES.Quad5fe ? 'Quad5f' : 'S0915', rank: 'Totum Duplex', title: 'Compassio B. Mariae V.'};
    if (fromE === 17) tf = {key: 'Pasc2w', rank: 'Totum Duplex I classis', title: 'Solemnitas S. Joseph Sponsi B. Mariae V.'};
    if (fromE === 69) tf = {key: 'PurCordisBMV', rank: 'Totum Duplex', title: 'Purissimi Cordis B. Mariae V.', missing: 'Missal pp. 316-317'};
    var oct31 = new Date(y, 9, 31), ck = addDays(oct31, -oct31.getDay());
    if (diffDays(d, ck) === 0) tf = {key: 'ChristusRex', rank: 'Totum Duplex I classis', title: 'D. N. Jesu Christi Regis'};
    var o1 = new Date(y, 9, 1), ros = addDays(o1, (7 - o1.getDay()) % 7);
    if (diffDays(d, ros) === 0) tf = {key: 'S1007', rank: 'Totum Duplex I classis', title: 'SS. Rosarii B. Mariae V.'};
    // the Holy Family: the Sunday within the octave of the Epiphany, or the Saturday within it when the Epiphany is a
    // Sunday (Missal p. 39: "Si Epiphania in Dominica evenerit, sequens Missa dicatur Sabbato infra Octavam")
    var ep = new Date(y, 0, 6), hf = ep.getDay() === 0 ? new Date(y, 0, 12) : addDays(ep, 7 - ep.getDay());
    if (diffDays(d, hf) === 0) tf = {key: 'Epi1', rank: 'Totum Duplex', title: 'Sanctae Familiae Jesu, Mariae, Joseph', pv: 89};
    if (tf) { t.feast = tf; }
    return t;
  }

  // the octaves of the Time and their grades
  function temporalOctaves(d) {
    var y = d.getFullYear(), E = easter(y), out = [];
    // the octave day has a Mass of its own where the Missal prints one (In Octava Epiphaniae, pp. 38-39)
    var OWN = {Epi: 'EpiOct'};
    var add = function (start, key, title, within, octday) {
      var n = diffDays(d, start);
      if (n >= 1 && n <= 6) out.push({key: key, title: title, day: n, pv: within, of: key});
      if (n === 7 && octday) out.push({key: OWN[key] && MASSES[OWN[key]] ? OWN[key] : key, title: 'Dies octava: ' + title, day: 7, pv: octday, of: key, octday: true});
    };
    add(new Date(y - (d.getMonth() === 0 ? 1 : 0), 11, 25), 'Dec25_3', 'Nativitas Domini', PV.inOctPrivLow, 0);
    add(new Date(y, 0, 6), 'Epi', 'Epiphania Domini', PV.inOctPriv, PV.octDayPriv);
    add(addDays(E, 39), 'Asc', 'Ascensio Domini', PV.inOctPrivLow, PV.octDay);
    add(addDays(E, 56), 'Pent1', 'SS. Trinitas', PV.inOctSolemn, PV.octDay);
    add(addDays(E, 60), 'CorpusChristi', 'SS. Corpus Christi', PV.inOctPriv, PV.octDayPriv);
    add(addDays(E, 68), 'SCJ', 'SS. Cor Jesu', PV.inOctPrivLow, PV.octDay);
    add(addDays(E, 17), 'Pasc2w', 'Solemnitas S. Joseph', PV.inOctSolemn, PV.octDay);
    var o1 = new Date(y, 9, 1), ros = addDays(o1, (7 - o1.getDay()) % 7);
    add(ros, 'S1007', 'SS. Rosarium B. M. V.', PV.inOctSolemn, PV.octDay);
    return out;
  }

  // ------------------------------------------------------------------ the Proper of the Saints
  // entries of the Kalendarium for a date; in a leap year the feasts of 24-28 February are kept a day later and the
  // Vigil of St Matthias on the 24th (the bissextile day)
  function kalOf(d) {
    var y = d.getFullYear(), m = d.getMonth(), dd = d.getDate(), md = mmdd(d);
    if (leap(y) && m === 1) {
      if (dd === 24) return (KAL['0223'] || []).filter(function (e) { return /Vigilia/.test(e[1]); });
      if (dd === 23) return (KAL['0223'] || []).filter(function (e) { return !/Vigilia/.test(e[1]); });
      if (dd >= 25) md = '02' + String(dd - 1);
    }
    return (KAL[md] || []).filter(function (e) { return !/^Pro Italia/.test(e[0]); });
  }
  // the date of a fixed feast's octave start, for 'Octava ...' entries
  function octaveBase(d, title) {
    for (var k = 7; k >= 7; k--) {
      var b = addDays(d, -k), es = kalOf(b);
      for (var i = 0; i < es.length; i++) if (/oct=/.test(es[i][3] || '')) return {date: b, e: es[i]};
    }
    return null;
  }
  // sanctoral octaves running on d (days 1-6)
  function sanctoralOctaves(d) {
    var out = [];
    for (var n = 1; n <= 6; n++) {
      var b = addDays(d, -n);
      kalOf(b).forEach(function (e) {
        var m = /oct=(solemnis|simplex)\b/.exec(e[3] || '');
        if (m) out.push({key: e[2], title: e[0], day: n, pv: m[1] === 'solemnis' ? PV.inOctSolemn : PV.inOctSimplex, of: e[2], grade: m[1]});
      });
    }
    return out;
  }

  function cand(o) { return o; }
  // the common vigils with a Mass in the Missale O.P. 1939 (by the date of the Kalendarium)
  var VIGIL_MASS = {'1129': 1, '1207': 1, '0623': 1, '0628': 1, '0809': 1, '0814': 1, '0920': 1, '1027': 1, '1031': 1};
  var LORD = /\bDomini\b|D\. ?N\. ?J\. ?C|Salvatoris|S\. Crucis|Sanguinis|Jesu\b/;
  // the candidates of a date before transfers: {kind, key, title, rank, pv, ...}
  function candidates(d) {
    var t = temporal(d), out = [];
    // the Sunday within a privileged octave of the second order is of the Sunday, with a commemoration of the octave
    // (Ordo 1944, 11 Jun.: Dom. infra oct. Corp. Christi. De ea. m. oct.)
    if (t.kind === 'sunday' && temporalOctaves(d).some(function (o) { return o.pv === PV.inOctPriv; })) t.pv = PV.inOctPriv + 1;
    out.push(cand({kind: 'temporal', key: t.key, title: '', rank: '', pv: t.pv, t: t}));
    if (t.feast) out.push(cand({kind: 'tfeast', key: t.feast.key, title: t.feast.title, rank: t.feast.rank,
      pv: t.feast.pv || RANK_PV[t.feast.rank], note: t.feast.note, missing: t.feast.missing}));
    temporalOctaves(d).forEach(function (o) { out.push(cand({kind: o.octday ? 'octday' : 'octave', key: o.key, title: o.title, rank: o.octday ? 'Octava' : '', pv: o.pv, day: o.day, of: o.of})); });
    sanctoralOctaves(d).forEach(function (o) { out.push(cand({kind: 'octave', key: o.key, title: o.title, rank: '', pv: o.pv, day: o.day, of: o.of, grade: o.grade})); });
    var tkeys = t.keys.concat(t.feast ? [t.feast.key] : []);
    kalOf(d).forEach(function (e, i) {
      // the feasts of the Time listed in the Kalendarium (Christmas, Circumcision, Epiphany) come from the Time
      if (e[2] && (tkeys.indexOf(e[2]) >= 0 || /^Dec25/.test(e[2]))) return;
      if (/^Octava /.test(e[0]) && out.some(function (c) { return c.kind === 'octday'; })) return;
      var rank = e[1], c = {kind: 'feast', key: e[2], title: e[0], rank: rank, pv: RANK_PV[rank] || 0, md: mmdd(d), order: i, note: e[3]};
      // the Kalendarium marks as Vigils also fast days that have no Mass of their own (St Matthias, St James, St Bartholomew,
      // St Thomas: the Missal prints none, and the Ordo 1944 says nothing of them in the Mass on 24 Jul., 23 Aug., 20 Dec.);
      // only the vigils with a Mass in the Missal enter the occurrence (Rubr. IV.2 "Vigiliis communibus quae propriam Missam habent")
      if (rank === 'Vigilia') { if (!VIGIL_MASS[mmdd(d)]) return; c.kind = 'vigil'; c.pv = PV.vigil; }
      else if (rank === 'Novem Lectiones') { c.kind = 'anniv'; c.pv = -1; }
      else if (rank === 'Memoria') { c.kind = 'memoria'; c.pv = -1; }
      else if (/^Octava/.test(rank) || /^Octava /.test(e[0])) {
        var b = octaveBase(d); c.kind = 'octday'; c.key = c.key || (b && b.e[2]); c.of = b && b.e[2];
      }
      // All Souls excludes every feast (§ XXIX.8)
      if (/^Commemoratio Omnium Fidelium/.test(e[0])) { c.kind = 'feast'; c.pv = 94; c.allSouls = true; }
      // the Order's feasts of the I class yield to those of the universal Church (§ XXVIII.1) and to the octave day of
      // the Epiphany and of Corpus Christi (§ XXIX.10)
      if (rank === 'Totum Duplex I classis' && /O\. ?P\.|S\. P\. N\.|Ordinis|Patrocinium S\. Thom/.test(e[0])) c.pv = PV.orderI;
      // a feast of the Lord of nine lessons takes a minor Sunday (§ XXIX.3), except within the privileged octaves
      if (t.kind === 'sunday' && t.pv === PV.sundayMinor && c.kind === 'feast' && c.pv >= 30 && c.pv < 80 && LORD.test(e[0])) c.pv = PV.lordOnSunday;
      out.push(c);
    });
    return out;
  }

  // ------------------------------------------------------------------ the year, with transfers
  var cache = {};
  function isSunday(d) { return d.getDay() === 0; }
  function computeRange(y) {
    if (cache[y]) return cache[y];
    var start = new Date(y - 1, 10, 15), end = new Date(y, 11, 31), res = {}, queue = [];
    for (var d = start; d <= end; d = addDays(d, 1)) {
      var cs = candidates(d), t = cs[0].t;
      // vigils falling on a Sunday are anticipated on the Saturday (Missal, 27 Jun.: "Si hodie sit Sabbatum, Missa dicitur
      // de Vigilia anticipata"; 14 Aug.: "Si sequens Vigilia Assumptionis anticipetur Sabbato")
      cs = cs.filter(function (c) { return !(c.kind === 'vigil' && isSunday(d)); });
      if (d.getDay() === 6) candidates(addDays(d, 1)).forEach(function (c) { if (c.kind === 'vigil') { c.anticipated = true; cs.push(c); } });
      // All Souls on a Sunday goes to the Monday
      cs = cs.filter(function (c) { if (c.allSouls && isSunday(d)) { queue.push({c: c, from: iso(d), keepPv: true}); return false; } return true; });
      // the Mass of the Sunday within the octave of Christmas, when the Sunday is 25-28 December, is said on the 30th
      // (Missal p. 28: "ejus Officium transferatur in diem 30 Decembris")
      if (mmdd(d) === '1230') {
        var y0 = d.getFullYear(), s = [25, 26, 27, 28].filter(function (x) { return new Date(y0, 11, x).getDay() === 0; });
        if (s.length) cs.push({kind: 'temporal', key: 'Nat1', title: 'Dominica infra Octavam Nativitatis', rank: '', pv: 71, t: t, resumed: true});
      }
      // transferred feasts waiting for a free day: a day without a feast of the I or II class or a privileged day, and
      // not a Sunday (St Joseph to Monday 20 Mar. 1944; St Vincent Ferrer from Holy Wednesday to 17 Apr.; Catherine de'
      // Ricci from Sexagesima to 14 Feb.)
      var top = Math.max.apply(null, cs.map(function (c) { return c.pv; }));
      // "in proximiorem insequentem diem, quae libera sit ab alio Festo Toto Duplici I et II classis, a Dominica occurrenti,
      // a Vigilia privilegiata, et ab aliis Officiis, quae hujusmodi Festa respective excludant" (Brev. 1924, § XXIX.4)
      queue.sort(function (a, b) { return b.c.pv - a.c.pv; });
      if (queue.length && !isSunday(d) && top < 80 && !(t.kind === 'vigil') && queue[0].c.pv > top) {
        var q = queue.shift(); q.c.transferredFrom = q.from; cs.push(q.c);
      }
      cs.sort(function (a, b) { return b.pv - a.pv || (a.kind === 'temporal' ? -1 : 0) || (a.order || 0) - (b.order || 0); });
      var win = cs[0];
      // Totum Duplex I and II classis impeded: transferred (Rubr. VII.4 and the Ordo); lesser feasts commemorated
      cs.slice(1).forEach(function (c) {
        // a Totum Duplex I or II classis impeded is transferred, and is not commemorated on the day it leaves (Ordo 1944,
        // 13 Feb. Sexagesima, 19 Mar. Laetare, 5 Apr. Holy Wednesday: "2-a et 3-a Or. ut in Missali" / "Dom. I. Quadrag.")
        if ((c.kind === 'feast') && c.pv >= 80 && !c.transferredFrom) { c.transferring = true; queue.push({c: c, from: iso(d)}); }
        if (c.transferredFrom && c !== win) queue.unshift({c: c, from: c.transferredFrom});
      });
      res[iso(d)] = {date: new Date(d), cands: cs, win: win, t: t};
    }
    markResumptions(res);
    cache[y] = res;
    return res;
  }
  // the Homily of an impeded Sunday is read within its week on the least solemn vacant day (the earlier, if equal): Tota
  // Duplicia communia and below without a proper Homily or Responsories, all octaves, and ferias without a Homily of their
  // own (Brev. 1924, § VII.2); on that day the Missal resumes the Sunday's Mass (Rubr. III.3-4). Not resumed: the Sunday
  // before the Ascension impeded by a feast of the I or II class or of the Lord (§ VII.6), the Vigil of Christmas on a
  // Sunday (§ VII.1), the Sundays of 25-28 December (30 Dec., p. 28) and of 1-6 January (§ XXIX.3).
  function solemnityForHomily(o, d) {
    var w = o.win, t = o.t;
    // a free Saturday has the Office of Our Lady, given up only when the Homily can be read on no other day (§ XXI.1)
    if (w.kind === 'temporal') return t.kind === 'feria' && !t.ownMass && !o.cands.some(function (c) { return c.kind === 'vigil'; }) && t.pv < 85 ? (d.getDay() === 6 && bvmSaturday(o, d) ? 10 : 0) : null;
    if (w.kind === 'octave') return 1;
    if (w.kind === 'octday') return w.pv >= 79 ? 6.5 : 2;
    if (w.kind === 'feast') {
      if (w.pv >= 80 || NOT_VACANT[w.md]) return null;   // a vigil under a feast does not prevent it (Ordo 1944, 9 Aug.)
      return {'Tres Lectiones': 2, 'Simplex': 3, 'Semiduplex': 4, 'Duplex': 5, 'Totum Duplex': 6}[w.rank];
    }
    return null;
  }
  function markResumptions(res) {
    Object.keys(res).forEach(function (k) {
      var o = res[k], d = o.date, t = o.t;
      if (!isSunday(d) || t.kind !== 'sunday' || o.win.kind === 'temporal' || t.pv >= PV.sundayI) return;
      var md = mmdd(d);
      if (/^(Nat1|Nat2|Epi1|Pent1|Dec24|Adv4)$/.test(t.key) && (md === '1224' || t.key !== 'Adv4')) return;
      if ((md >= '1225' && md <= '1228') || (md >= '0101' && md <= '0106')) return;
      if (t.key === 'Pasc5') return;
      if (o.win.kind === 'tfeast' && o.win.key === t.key) return;
      var best = null;
      for (var j = 1; j < 7; j++) {
        var z = res[iso(addDays(d, j))];
        if (!z) break;
        var sc = solemnityForHomily(z, z.date);
        // Saturday only when no other day of the week is vacant (§ XXI.1: then no Office of Our Lady)
        if (sc != null && (best == null || sc < best.sc)) best = {o: z, sc: sc};
      }
      if (best) best.o.resume = {key: t.key, from: k};
    });
  }

  // ------------------------------------------------------------------ the day
  function officeOf(d) { var r = computeRange(d.getFullYear()); return r[iso(d)]; }

  function weekStart(d) { return addDays(d, -d.getDay()); }
  // is d a free feria (no feast of three lessons or above, no octave, no feria or vigil with its own Mass)?
  function freeFeria(o) {
    var w = o.win, t = o.t;
    if (o.resume) return false;
    if (w.kind !== 'temporal' || t.kind !== 'feria') return false;
    if (t.ownMass || t.pv > PV.feriaMajor || o.cands.some(function (c) { return c.kind === 'vigil'; })) return false;
    return !o.cands.some(function (c) { return c !== w && c.pv >= 20 && c.kind !== 'temporal'; });
  }
  function bvmSaturday(o, d) {
    // the Office of Our Lady on Saturday: on a free Saturday outside Advent and Lent, Ember days, vigils and octaves
    // (Ordo 1944, 9 Sept.: Offic. B.M.V. in Sabbato over St Gorgonius, Tres Lectiones; every Saturday with a Simplex
    // or higher feast has the feast with a commemoration of Our Lady)
    // (Brev. 1924, § XXI.1: every Saturday except in Lent, on Ember days, within octaves and on octave days, on Simplex feasts
    // and above, on vigils with a Mass of their own, and when the Sunday Homily can be read on no other day)
    if (d.getDay() !== 6 || o.resume) return false;
    var t = o.t;
    if (t.season === 'quad' || t.season === 'pass' || t.ember || /^(5a|Quad|Pasc0|Pent0)/.test(t.key) || t.key === 'Pasc6s' || t.key === 'Dec24') return false;
    if (o.cands.some(function (c) { return c.kind === 'vigil' || ((c.kind === 'octave' || c.kind === 'octday') && c.pv >= 20); })) return false;
    return o.win.pv < 30;
  }
  // the week's Mass for the dead (Rubr. VI.2): the first day of the week not impeded by a feast of three lessons or
  // above, an octave, a feria or vigil with its own Mass, or a resumed Sunday; not in the weeks of All Souls, Easter,
  // Pentecost, Holy Week, Christmas or of the Order's four Anniversaries
  var annivCache = {};
  function anniversaries(y) {
    if (annivCache[y]) return annivCache[y];
    var out = {}, r = computeRange(y);
    Object.keys(KAL).forEach(function (md) {
      KAL[md].forEach(function (e) {
        if (e[1] !== 'Novem Lectiones') return;
        // sung on their day unless it is a Sunday, a holy day, a privileged feria, vigil or octave, or a feast of the I
        // or II class; then on the next day not so impeded (Rubr. VI.2)
        var d = new Date(y, +md.slice(0, 2) - 1, +md.slice(2));
        for (var k = 0; k < 10; k++) {
          var o = r[iso(d)];
          if (!o) break;
          if (!isSunday(d) && o.win.pv < 80 && !(o.t.pv >= 85)) break;
          d = addDays(d, 1);
        }
        out[iso(d)] = {key: e[2], title: e[0], md: md};
      });
    });
    annivCache[y] = out;
    return out;
  }
  // the weeks without the Mass for the dead (Rubr. VI.2: All Souls, Easter, Pentecost, Holy Week, Christmas, the Anniversaries)
  function requiemExempt(ws) {
    for (var k = 0; k < 7; k++) {
      var x = addDays(ws, k), E = easter(x.getFullYear()), f = diffDays(x, E), md = mmdd(x);
      if (anniversaries(x.getFullYear())[iso(x)]) return true;
      if ((f >= -7 && f <= 6) || (f >= 49 && f <= 55) || md === '1102' || md === '1225') return true;
    }
    return false;
  }
  function requiemDay(d) {
    var ws = weekStart(d);
    if (requiemExempt(ws)) return null;
    for (var j = 1; j < 7; j++) {
      var z = addDays(ws, j), o = officeOf(z);
      if (o && freeFeria(o) && !bvmSaturday(o, z)) return iso(z);
    }
    return null;
  }
  // Rubr. VI.2: "Quod si Missa de Requiem ob continuas Festivitates vel dies supra relatos infra hebdomadam celebrari non
  // possit, tunc alia hebdomadae die, minus solemni, in Missa conventuali ... additur Oratio Omnipotens pro Vivis et
  // Defunctis post Orationes a Rubricis praescriptas": the least solemn weekday (the lowest rank; the first if equal)
  function omnipotensDay(d) {
    var ws = weekStart(d);
    if (requiemExempt(ws) || requiemDay(d)) return null;
    var best = null, bp = Infinity;
    for (var j = 1; j < 7; j++) {
      var z = addDays(ws, j), o = officeOf(z);
      if (o && o.win && o.win.pv < bp) { bp = o.win.pv; best = iso(z); }
    }
    return best;
  }

  function label(c) {
    if (!c) return '';
    if (c.kind === 'temporal') return '';
    return c.title;
  }

  function day(d) {
    d = new Date(d.getFullYear(), d.getMonth(), d.getDate());
    var o = officeOf(d), t = o.t, win = o.win, cs = o.cands, masses = [], notes = [];
    var add = function (key, lab, extra) {
      if (key && masses.some(function (m) { return m.key === key; })) return;
      var m = {key: key || null, label: lab, missing: !has(key)};
      for (var k in extra || {}) m[k] = extra[k];
      masses.push(m);
    };
    var office = {kind: win.kind, key: win.key, title: win.title, rank: win.rank, pv: win.pv, transferredFrom: win.transferredFrom || null};
    var feria = t; // the day of the Time
    var tKey = t.key;
    var bvm = bvmSaturday(o, d);
    if (bvm) office = {kind: 'bvmSat', key: 'C79s', title: 'Officium B. Mariae V. in Sabbato', rank: '', pv: PV.bvmSat};
    var vigil = cs.filter(function (c) { return c.kind === 'vigil'; })[0];
    var vigKey = vigil && (vigil.key || null);
    // two conventual Masses (Rubr. IV.2-4): Lent ferias, Ember days, common vigils with a Mass, Rogations
    var twoMass = (t.lent || t.ember || t.rogation || vigil) && (win.kind === 'feast' || win.kind === 'tfeast' || win.kind === 'octday');
    var onVigil = vigil && !t.lent && !t.ember && !t.rogation;
    var priv = win.kind === 'feast' || win.kind === 'tfeast' ? win.rank : '';
    var feriaKey = t.rogation ? (t.keys.indexOf('AscVig') >= 0 ? 'AscVig' : 'Litaniis') : (onVigil ? vigKey : tKey);
    var feriaLab = t.rogation ? 'the Rogations' : (onVigil ? 'the vigil' : 'the feria');
    if (office.kind === 'bvmSat') {
      add('C79s', 'Saturday of Our Lady');
      add(tKey, 'Mass of the Sunday (private Masses)');
    } else if (twoMass) {
      if (/I classis/.test(priv) && onVigil) {
        // "In Totis Duplicibus tamen I classis nihil umquam fit de Vigilia non privilegiata"
        add(win.key, 'Feast');
      } else if (/classis/.test(priv)) {
        add(win.key, 'In choir: the feast');
        add(feriaKey, 'Outside choir: ' + feriaLab, {title: onVigil ? vigil.title : ''});
      } else {
        add(feriaKey, 'In choir: ' + feriaLab, {title: onVigil ? vigil.title : ''});
        add(win.key, 'Outside choir: the feast');
      }
    } else if (win.kind === 'octave' && (t.lent || t.ember || t.rogation || vigil)) {
      // "De die item infra Octavam non privilegiatam ... non dicitur Missa conventualis, sed fit tantum Memoria in
      // Missa de Feria vel Vigilia"
      add(feriaKey, 'Mass of ' + feriaLab + ', with a commemoration of the octave (Rubr. IV.2)', {title: onVigil ? vigil.title : ''});
    } else if (win.kind === 'vigil') {
      add(win.key, 'Vigil', {title: win.title});
    } else if (win.kind === 'temporal') {
      if (cs.some(function (c) { return c.resumed && c === win; })) add(win.key, 'Sunday within the octave');
      else if (t.kind === 'feria' && !t.ownMass) {
        var rq = requiemDay(d) === iso(d);
        if (rq && has('C114s')) add('C114s', 'Conventual Mass for the dead (the week\'s first free feria)');
        if (vigil) add(vigKey, 'Vigil', {title: vigil.title});
        add(tKey, t.season === 'adv' ? 'Mass of the Sunday' : 'Mass of the preceding Sunday');
        // the votive Masses of the ferias (Rubr. V.1)
        if (!rq && !vigil && t.season !== 'adv') {
          if (d.getDay() === 4) { add('C62s', 'Votive: the Blessed Sacrament'); add('C64s', 'Votive: Christ the High Priest'); }
        }
      } else {
        add(t.ember || t.rogation || t.lent ? feriaKey : tKey, '');
        if (vigil && t.major) notes.push('The vigil is commemorated (Rubr. IV.3)');
      }
    } else if (win.kind === 'octave') {
      add(win.key, 'Within the octave');
    } else {
      add(win.key, win.kind === 'octday' ? 'Octave day' : '');
    }
    // All Souls: three Masses (Rubr. VI.1)
    if (win.allSouls) { add('S1102_2', 'Second Mass'); add('S1102_3', 'Third Mass'); }
    // Christmas: three Masses
    if (win.kind === 'temporal' && /^Dec25/.test(tKey)) { add('Dec25_1', 'At midnight'); add('Dec25_2', 'At dawn'); }
    // Rogation days and 25 April with a feast of the I or II class: the Mass of the Rogations too (Rubr. IV.4)
    if (t.rogation && !twoMass && /classis/.test(priv)) add('Litaniis', 'Rogations (with the procession)');
    // the Order's four Anniversaries: sung besides the conventual Mass of the day, or alone on a free feria, where the one
    // conventual Mass for the dead suffices (Rubr. VI.2; Ordo 1944, 5 Sept.: Missa conv. unica de Anniversario)
    var a = anniversaries(d.getFullYear())[iso(d)];
    if (a && a.key) {
      // the label says which conventual Mass it is; the Anniversary's own title (Kalendarium) goes in title (qc_ui C10)
      if (freeFeria(o) && !bvm) masses = masses.filter(function (m) { return m.key !== 'C114s'; }), masses.unshift({key: a.key, label: 'The one conventual Mass', title: a.title, anniv: true, missing: !has(a.key)});
      else add(a.key, 'Second conventual Mass (sung)', {anniv: true, title: a.title});
    }
    // the Mass of an impeded Sunday resumed on this day (Rubr. III.3-4): on ferias, within octaves and on feasts and octave
    // days of three lessons one conventual Mass, of the Sunday; on other feasts two, the Sunday's in choir
    if (o.resume && has(o.resume.key)) {
      var rk = o.resume.key, single = win.kind === 'temporal' || win.kind === 'octave' || win.rank === 'Tres Lectiones' || (win.kind === 'octday' && win.pv < 79);
      var rest = masses.filter(function (m) { return m.key !== rk && !m.anniv; }), an = masses.filter(function (m) { return m.anniv; });
      masses = [];
      if (single) {
        add(rk, 'Mass of the Sunday (resumed, Rubr. III.3)');
        rest.forEach(function (m) { if (m.key !== 'C114s') add(m.key, 'Private Masses may be of the day', {title: m.title}); });
      } else {
        add(rk, 'In choir: the Sunday (resumed, Rubr. III.4)');
        rest.forEach(function (m) { add(m.key, 'Outside choir: ' + (m.label ? m.label.replace(/^(In|Outside) choir: /, '') : 'the feast'), {title: m.title}); });
      }
      an.forEach(function (m) { masses.push(m); });
      twoMass = !single;
    }

    // what is commemorated (in the order of the Rubrics: Sunday, privileged feria, octave, feasts, memoriae)
    var commems = [];
    var pushC = function (c, kind) {
      if (!c || c === win || (c.transferring && c.kind === 'feast')) return;
      if (commems.some(function (x) { return x.title === c.title && x.key === c.key; })) return;
      commems.push({key: c.key || null, title: c.title || '', rank: c.rank || '', kind: kind || c.kind, pv: c.pv || 0});
    };
    if (win.kind !== 'temporal' && t.kind === 'sunday') pushC({key: t.key, title: 'Dominica', rank: ''}, 'sunday');
    if (win.kind !== 'temporal' && t.major) pushC({key: tKey, title: 'Feria', rank: ''}, 'feria');
    if (vigil && win !== vigil && !(/I classis/.test(priv))) pushC(vigil, 'vigil');
    cs.forEach(function (c) { if ((c.kind === 'octave' || c.kind === 'octday') && c !== win && c.pv >= 20) pushC(c, 'octave'); });
    cs.forEach(function (c) { if ((c.kind === 'feast' || c.kind === 'tfeast') && c !== win && c.pv >= 20) pushC(c, 'feast'); });
    // Our Lady on a Saturday whose Office of her is impeded (Brev. 1924, § XXI.3): not on Doubles and above, within
    // solemnissima and solemn octaves and on their octave days, from 2 to 13 January, nor on All Souls; after the feasts,
    // before the Memoriae (Ordo 1944, 15 Jul.: "2-a Or. festi, 3-a Concede. (B.V.)"; 29 Jul.: "2-a Or. Concede. (B.M.V.),
    // 3-a SS. Felicis")
    var md = mmdd(d);
    if (d.getDay() === 6 && !bvm && win.pv < 50 && t.pv < 50 && !win.allSouls && !(md >= '0102' && md <= '0113') &&
        !cs.some(function (c) { return c.kind === 'octday' || (c.kind === 'octave' && c.pv >= PV.inOctSolemn); }))
      pushC({key: null, title: 'S. Maria in Sabbato', rank: ''}, 'bvm');
    cs.forEach(function (c) { if (c.kind === 'memoria') pushC(c, 'memoria'); });
    // at the conventual and sung Mass of a feast of the I class nothing is made of common Totum Duplex feasts and below,
    // nor of non-privileged octaves; of the II class nothing of Tres Lectiones and below (Rubr. VIII.2)
    // VIII.2 speaks of feasts ("in Festis I classis ... in Festis II classis"): ferias, Sundays, vigils and days within
    // octaves are not restricted (Ordo 1944: Ash Wed. "2-a Orat. B. Petri Dam."; 12 Mar. "2-a Or. S. Gregorii"; 4 Apr.
    // "m. S. Isidori"; 13-14 Apr., 31 May-3 Jun. "m. B. ..."), save the feasts of the Lord of the Time and Easter and
    // Pentecost Monday and Tuesday ("nihil fit"). "I classis" must not match "II classis" (14 Feb., 17 Apr.).
    var winFeast = win.kind === 'feast' || win.kind === 'tfeast' ||
      (win.kind === 'temporal' && /^(Dec25(_\d)?|Jan1|Epi|Pasc0[mt]?|Asc|Pent0[mt]?|Pent1|CorpusChristi|SCJ|ChristusRex)$/.test(win.key || ''));
    var I = winFeast && (/(^|[^I])I classis/.test(win.rank || '') || win.pv >= 90), II = winFeast && /II classis/.test(win.rank || '');
    commems.forEach(function (c) {
      var pv = RANK_PV[c.rank] || (c.kind === 'memoria' ? 5 : 0);
      // the Sunday and a major feria are always commemorated, even on a feast of the I class (Missal, after the First Sunday of Advent, scan p. 34: "semper fit
      // Memoria de Feria majori Adventus, Quadragesimae, Quatuor Temporum et Rogationum"; Ordo 1944, 8 Dec.: "In Missa m. fer.")
      if (c.kind === 'feria' || c.kind === 'sunday') { if (twoMass && c.kind === 'feria') c.privateOnly = true; return; }
      if (I && ((c.kind === 'feast' && pv <= 60) || c.kind === 'memoria' || (c.kind === 'octave' && !/^(Epi|CorpusChristi|Asc|SCJ|Dec25)/.test(c.key || '')))) c.privateOnly = true;
      if (II && (pv <= 20 || c.kind === 'memoria')) c.privateOnly = true;
      // within the octaves of Easter and Pentecost the Ordo makes no Memoria (Simplex) at the conventual Mass (Ordo 1944,
      // 14 Apr. "m. B. Petri" without SS. Tiburtius etc.; 2 Jun. "m. BB. Sadoc" without SS. Marcellinus and Peter)
      if (c.kind === 'memoria' && win.kind === 'temporal' && /^(Pasc0[whfs]|Pent0[whfs])$/.test(win.key || '')) c.privateOnly = true;
      // on the days of two conventual Masses the Mass of the feast is said without the feria or vigil, which private
      // Masses commemorate (Rubr. IV.2; Ordo 1944, 27 Mar.: "2-a Missa conv. extra Chorum de festo sine mem.")
      if (twoMass && (c.kind === 'feria' || c.kind === 'vigil')) c.privateOnly = true;
    });
    var winKey = masses.length ? masses[0].key : tKey;
    return {date: iso(d), temporal: {key: tKey, keys: t.keys, kind: t.kind, season: t.season, pv: t.pv}, office: office,
      masses: masses, win: winKey, commems: commems, notes: notes, twoMasses: !!twoMass};
  }

  return {day: day, temporaleKey: temporaleKey, easter: easter, temporal: temporal, rankShort: rankShort, omnipotensDay: omnipotensDay,
    _office: officeOf, _cache: cache};
});
