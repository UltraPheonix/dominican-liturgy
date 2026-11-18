/* Chant rendering for the Office page: GABC → exsurge → SVG, one staff line per <div class="line">.
   The context and the GABC adjustments follow the Mass page (js/app.js), which follows jgabc. */
(function () {
  'use strict';
  var ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII'];

  function makeContext() {
    var ctxt = new exsurge.ChantContext(exsurge.TextMeasuringStrategy.Canvas);
    ctxt.condenseLineAmount = 1;
    ctxt.lineBreaking = 'optimal';
    ctxt.setGlyphScaling(1 / 16);
    ctxt.textColor = 'currentColor';
    ctxt.staffLineColor = ctxt.neumeLineColor = ctxt.dividerLineColor = 'currentColor';
    ctxt.negativeFillColor = 'var(--paper, #fff)';
    ctxt.setFont("'Crimson Text', serif", 19.2 / 0.9);
    ctxt.spaceBetweenSystems = 0;
    ctxt.textStyles.dropCap.size = 56;
    ctxt.textStyles.annotation.size = 12.8;
    ctxt.minLyricWordSpacing *= 0.7;
    ctxt.accidentalSpaceMultiplier = 1.5;
    ctxt.specialCharProperties['font-family'] = "'Versiculum'";
    ctxt.specialCharProperties['font-variant'] = 'normal';
    ctxt.specialCharProperties['font-weight'] = '400';
    var defaultSpecialCharText = ctxt.specialCharText;
    ctxt.specialCharText = function (ch) { return defaultSpecialCharText(ch).toLowerCase(); };
    ctxt.setRubricColor('var(--rubric, #b3121f)');
    return ctxt;
  }

  // the optional Paschal Alleluia ("T. P.") is left out outside Paschaltide
  function stripTP(gabc) {
    var m = /<i>\s*T\.\s*P\.\s*<\/i>/.exec(gabc);
    if (!m) return gabc;
    var j = gabc.indexOf('(::)', m.index);
    var k = j < 0 ? -1 : (/\w\(/.test(gabc.slice(m.index + m[0].length, j)) ? j : gabc.indexOf('(::)', j + 4));
    if (k < 0) return gabc.slice(0, m.index) + '(::)';
    return gabc.slice(0, m.index) + '(::)' + gabc.slice(k + 4);
  }

  function prepare(gabc, keepTP) {
    if (!keepTP) gabc = stripTP(gabc);
    // the Roman books print the psalm ending (E u o u a e) after the antiphon: the psalm tone is shown with the psalm itself
    gabc = gabc.replace(/\s*E\([^)]*\)\s*u\([^)]*\)\s*o\([^)]*\)\s*u\([^)]*\)\s*a\([^)]*\)\s*e\.?\([^)]*\)(\s*\([:;,]*\))?/g, '');
    return gabc
      .replace(/<v>\\'y<\/v>/g, 'ý').replace(/<v>\\'Y<\/v>/g, 'Ý').replace(/<v>([A-Za-z])<\/v>/g, '$1')
      .replace(/<v>\\emph\{([^}]*)\}<\/v>/g, '<i>$1</i>')
      .replace(/<i>\{([^}]*)\}<\/i>/g, '<i>$1</i>')
      .replace(/<i>(i+j)<\/i>\./g, '<i>$1.</i>')
      .replace(/<v>\\([VRA])bar<\/v>/g, function (m, b) { return b + '/.'; })
      .replace(/<sp>([VRA])\/<\/sp>\.?/g, function (m, b) { return b + '/.'; })
      .replace(/<sp>\*<\/sp>/g, '*')
      .replace(/<v>[^<]*<\/v>/g, '')
      .replace(/([^)]\s+)([*†]|<i>(?:i+j|Repet)\.<\/i>)\(/g, '$1^$2^(')
      .replace(/\^?(<i>[^(|]*? [^(|]*?<\/i>)\^?([^(|]*)/g, '^$1^$2')
      .replace(/(\s+)({?<i>(?:i+j|Repet)\.<\/i>}?)\(/g, '$1^$2^(')
      .replace(/\[[ou]ll:[01]?[{}][01]?\]/ig, '')
      .replace(/<alt>.*?<\/alt>/gi, '')
      .replace(/<\/?i>/g, '_')
      .replace(/\\hspace{[^}]*}/g, '')
      .replace(/\s(<nlba>)?\^?\*\^?(?=\s*[^(])/g, ' $1*()')
      .replace(/(\))\s*\(\)/g, ')')
      .replace(/<\/?(?:nlba|eu|clear|pr)>/g, '')
      .replace(/\^_([^_^]*)_\^/g, '^$1^');
  }

  function showError(container, e) {
    container.innerHTML = '';
    var p = document.createElement('p');
    p.className = 'o-msg';
    p.textContent = 'This chant could not be drawn.';
    container.appendChild(p);
    if (window.console) console.warn(e);
  }

  // fit each drawn line to its frame and inline the glyph references (printing ignores <use>)
  function finish(container, lines) {
    if (lines && !lines.length && lines.nodeType) lines = [lines];
    container.innerHTML = '';
    var glyphs = {};
    Array.prototype.forEach.call(lines, function (svg) {
      Array.prototype.forEach.call(svg.querySelectorAll('defs [id]'), function (n) { glyphs[n.getAttribute('id')] = n; });
    });
    Array.prototype.forEach.call(lines, function (svg) {
      Array.prototype.slice.call(svg.querySelectorAll('use')).forEach(function (u) {
        var g = glyphs[(u.getAttribute('xlink:href') || u.getAttribute('href') || '').replace(/^#/, '')];
        if (!g) { u.parentNode.removeChild(u); return; }
        var wrap = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        wrap.setAttribute('transform', 'translate(' + (parseFloat(u.getAttribute('x')) || 0) + ',' + (parseFloat(u.getAttribute('y')) || 0) + ')');
        ['class', 'fill', 'style'].forEach(function (a) { if (u.getAttribute(a)) wrap.setAttribute(a, u.getAttribute(a)); });
        var copy = g.cloneNode(true);
        copy.removeAttribute('id');
        wrap.appendChild(copy);
        u.parentNode.replaceChild(wrap, u);
      });
    });
    Array.prototype.forEach.call(lines, function (svg) {
      var w = parseFloat(svg.getAttribute('width')), h = parseFloat(svg.getAttribute('height'));
      if (w && h && !svg.getAttribute('viewBox')) svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
      svg.removeAttribute('width'); svg.removeAttribute('height');
      var div = document.createElement('div');
      div.className = 'line';
      div.appendChild(svg);
      container.appendChild(div);
      // the staff stops at the last sign instead of running empty to the margin
      try {
        Array.prototype.forEach.call(svg.querySelectorAll('.chantLine'), function (ln) {
          var right = 0;
          Array.prototype.forEach.call(ln.querySelectorAll(':scope > .ChantNotationElement'), function (el) {
            var m = /translate\(([-\d.e]+)/.exec(el.getAttribute('transform') || ''), tx = m ? parseFloat(m[1]) : 0;
            var nb = el.querySelector('.Notations') || el, bb = nb.getBBox();
            if (bb.width) right = Math.max(right, tx + bb.x + bb.width);
          });
          if (right > 0) Array.prototype.forEach.call(ln.querySelectorAll('.staffLine'), function (sl) {
            if (parseFloat(sl.getAttribute('x2')) > right + 1) sl.setAttribute('x2', right.toFixed(2));
          });
        });
      } catch (e) {}
      try {
        var b = svg.getBBox(), vb = svg.getAttribute('viewBox').split(/\s+/).map(Number);
        var hh = (b.height > 0 && b.height < vb[3] * 2) ? b.height + 6 : vb[3] + 6;
        if (isFinite(b.y) && Math.abs(b.y) < vb[3] * 2) svg.setAttribute('viewBox', [vb[0], (b.y - 3).toFixed(2), vb[2], hh.toFixed(2)].join(' '));
      } catch (e) {}
    });
  }

  var queue = Promise.resolve();
  // opts: {mode: '8', label: 'Ant.', keepTP: bool, dropCap: bool}
  function render(container, gabc, opts) {
    opts = opts || {};
    queue = queue.then(function () {
      return new Promise(function (resolve) {
        if (!container.isConnected) { resolve(); return; }
        try {
          var ctxt = makeContext();
          var mappings = exsurge.Gabc.createMappingsFromSource(ctxt, prepare(gabc, opts.keepTP));
          var dropCap = opts.dropCap !== false;
          var score = new exsurge.ChantScore(ctxt, mappings, dropCap);
          if (dropCap && opts.label) {
            var mode = ROMAN[parseInt(opts.mode, 10)] || '';
            score.annotation = mode ? new exsurge.Annotations(ctxt, '%' + opts.label + '%', '%' + mode + '%')
                                    : new exsurge.Annotations(ctxt, '%' + opts.label + '%');
          }
          var width = Math.min(container.clientWidth || 600, 720);
          ctxt.width = width;
          score.performLayoutAsync(ctxt, function () {
            try {
              score.layoutChantLines(ctxt, width);
              finish(container, score.createSvgNodeForEachLine(ctxt));
            } catch (e) { showError(container, e); }
            resolve();
          });
        } catch (e) { showError(container, e); resolve(); }
      });
    });
    return queue;
  }

  // the key under which a text is looked up in data/chant/office.json (same as build/gb/build_chant.py)
  function key(s) {
    return String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
      .replace(/æ/g, 'ae').replace(/œ/g, 'oe').replace(/j/g, 'i').replace(/[^a-z]/g, '');
  }

  window.OPChant = {render: render, prepare: prepare, key: key};
})();
