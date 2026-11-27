"""Build prayers.html: the prayers of the Missale O.P. (1939) at the vesting, and before and after Mass, Latin and English.
Usage: python3 tools/prayers/build_prayers.py"""
import html, os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
from prayers_data import PARTS
from prayers_published import SOURCES, PUB
ROOT = os.path.join(H, '..', '..')
E = html.escape
import re
DAY = re.compile(r'^(Die Dominica|Feria [IV]+|Sabbato|Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday)\. ')
def txt(t):
    m = DAY.match(t); lead = ''
    if m: lead = '<span class="pr-day">%s</span> ' % E(m.group(1)); t = t[m.end():]
    return lead + E(t).replace('\n', '<br>')
toc, body = [], []
for pid, la, en, rub, items in PARTS:
    sub = []
    body.append('<h2 class="pr-ph" id="%s">%s<span class="pr-h-en">%s</span></h2>' % (pid, E(la), E(en)))
    if rub: body.append('<div class="pr-pair pr-rub"><p lang="la">%s</p><p class="pr-en" lang="en">%s</p></div>' % (E(rub[0]), E(rub[1])))
    for i, (hla, hen, r, paras) in enumerate(items):
        iid = '%s-%d' % (pid, i + 1)
        sub.append('<li><a href="#%s">%s <span class="pr-toc-en">%s</span></a></li>' % (iid, E(hla), E(hen)))
        s = ['<section class="pr-sec" id="%s"><h3>%s<span class="pr-h-en">%s</span></h3>' % (iid, E(hla), E(hen))]
        if r: s.append('<div class="pr-pair pr-rub"><p lang="la">%s</p><p class="pr-en" lang="en">%s</p></div>' % (E(r[0]), E(r[1])))
        pub = PUB.get(hla)
        if pub:
            assert len(pub[1]) == len(paras), hla
            paras = [(a, b) for (a, _), b in zip(paras, pub[1])]
            s.append('<p class="pr-srcline">English: %s.</p>' % E(SOURCES[pub[0]]))
        else:
            s.append('<p class="pr-srcline ai">English: AI translation (Claude), not yet checked by a human translator.</p>')
        verse = any('\n' in a for a, b in paras)
        for a, b in paras:
            s.append('<div class="pr-pair%s"><p class="pr-la" lang="la">%s</p><p class="pr-en" lang="en">%s</p></div>' % (' pr-verse' if verse else '', txt(a), txt(b)))
        s.append('</section>'); body.append(''.join(s))
    toc.append('<li class="pr-part"><a href="#%s">%s <span class="pr-toc-en">%s</span></a><ol>%s</ol></li>' % (pid, E(la), E(en), ''.join(sub)))
page = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dominican Rite — Prayers of the Priest</title>
<script>try{if(localStorage.getItem('theme')==='dark')document.documentElement.setAttribute('data-theme','dark')}catch(e){}</script>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Cormorant+SC:wght@500;600&display=swap">
  <link rel="stylesheet" href="style.css">
  <link rel="manifest" href="manifest.webmanifest">
  <link rel="icon" href="icon.svg" type="image/svg+xml">
  <meta name="theme-color" content="#111111">
</head>
<body class="pr">
<header class="top hide-print">
  <div class="top-in">
    <a class="brand" href="./" aria-label="Dominican Rite, today's Mass"><svg width="26" height="26" viewBox="0 0 40 40" aria-hidden="true"><rect x="17" y="3" width="6" height="34" fill="currentColor"/><rect x="3" y="17" width="34" height="6" fill="currentColor"/><circle cx="20" cy="4" r="3.6" fill="currentColor"/><circle cx="20" cy="36" r="3.6" fill="currentColor"/><circle cx="4" cy="20" r="3.6" fill="currentColor"/><circle cx="36" cy="20" r="3.6" fill="currentColor"/></svg>
      <span class="t1">Dominican Rite</span></a>
    <nav class="nav" aria-label="Main"><a href="./">Mass</a><a href="office.html">Office</a><a href="holyweek.html">Holy Week</a><a href="rubrics.html">Rubrics</a><a href="prayers.html" aria-current="page">Prayers</a><a href="about.html">About</a></nav>
  </div>
</header>
<div class="content"><div class="inner">
  <main class="prose">
    <h1>Orationes Sacerdotis</h1>
    <p class="pr-src">The prayers of the priest from the <i>Missale juxta ritum Sacri Ordinis Praedicatorum</i> (Rome, 1939), pp. 57&ndash;64:
      at the washing of the hands and the vesting, and before and after Mass, with English translations.</p>
    <p class="ai-note">Where a published English translation exists it is given, with its source; words in [square brackets] are ours, supplying what a version made for the laity leaves out. The rest is <b>AI translation</b> (made with Claude), marked as such and not yet checked by a human translator. The Latin is the text of the Missal; where the two differ, follow the Latin.
      The rubrics of the vesting are in the <a href="rubrics.html#praeparatio">Rubrics</a>.</p>
    <ol class="pr-toc">%s</ol>
    %s
  </main>
</div></div>
<script src="js/ui.js"></script>
</body>
</html>
''' % (''.join(toc), '\n    '.join(body))
open(os.path.join(ROOT, 'prayers.html'), 'w', encoding='utf8').write(page)
print('prayers.html', len(page))
