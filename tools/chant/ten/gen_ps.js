// psalms set to the Dominican tones (js/psalm.js) -> gabc files. stdin: [{id, name, tone, diff, solemn, src, verses:[...]}]
const P = require('/home/claude/dominican-liturgy/js/psalm.js'), fs = require('fs');
const spec = JSON.parse(fs.readFileSync(0, 'utf8'));
for (const s of spec) {
  const tone = P.toneOf(s.tone, s.diff);
  let clef = null, body = [];
  s.verses.forEach((v, i) => {
    v = v.replace(/\s*✠\s*/g, ' ').replace(/\s+/g, ' ').trim();
    const pv = P.pointVerse(v, tone, {inton: i === 0 || s.solemn, solemn: !!s.solemn});
    let g = P.verseGabc(pv, tone);
    const m = /^\(([cf]b?[1-4])\)\s*/.exec(g); if (m) { if (!clef) clef = m[1]; g = g.slice(m[0].length); }
    body.push(g);
  });
  const hdr = `name:${s.name};\noffice-part:Psalmus;\nmode:${tone.name}${tone.diff ? ' ' + tone.diff : ''};\nbook:${s.src};\ntranscriber:${s.tr} for dominicanrite.com;\ninitial-style:0;\n%%\n`;
  fs.writeFileSync(`/home/claude/dominican-liturgy/gabc/${s.id}.gabc`, hdr + `(${clef}) ` + body.join(' (Z)\n') + '\n');
}
console.log('ok', spec.length);
