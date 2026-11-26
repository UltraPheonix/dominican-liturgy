"""Build rubrics.html (Rubricae generales Missarum, Missale O.P. 1939, Latin and English) from rubrics_data.py.
Usage: python3 tools/rubrics/build_rubrics.py"""
import html, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
from rubrics_data import PROLOGUE, TITLES, COLOURS
ROOT = os.path.join(H, '..', '..')
E = html.escape

def slug(n): return 'tit-' + n.lower()

def pair(la, en):
    return ('<div class="rb-pair"><p class="rb-la" lang="la">%s</p><p class="rb-en" lang="en">%s</p></div>' % (E(la), E(en)))

body = []
toc = []
body.append('<section class="rb-sec" id="prooemium">' + pair(*PROLOGUE) + '</section>')
for n, la, en, paras in TITLES:
    toc.append('<li><a href="#%s"><span class="rb-n">%s</span> %s <span class="rb-toc-en">%s</span></a></li>' % (slug(n), n, E(la), E(en)))
    body.append('<section class="rb-sec" id="%s"><h2><span class="rb-n">%s</span> %s<span class="rb-h-en">%s</span></h2>%s</section>'
                % (slug(n), n, E(la), E(en), ''.join(pair(a, b) for a, b in paras)))
la, en, paras = COLOURS
toc.append('<li><a href="#colores">%s <span class="rb-toc-en">%s</span></a></li>' % (E(la), E(en)))
body.append('<section class="rb-sec" id="colores"><h2>%s<span class="rb-h-en">%s</span></h2>%s</section>'
            % (E(la), E(en), ''.join(pair(a, b) for a, b in paras)))

page = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dominican Rite — Rubrics of the Mass</title>
<script>try{if(localStorage.getItem('theme')==='dark')document.documentElement.setAttribute('data-theme','dark')}catch(e){}</script>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Cormorant+SC:wght@500;600&display=swap">
  <link rel="stylesheet" href="style.css">
  <link rel="manifest" href="manifest.webmanifest">
  <link rel="icon" href="icon.svg" type="image/svg+xml">
  <meta name="theme-color" content="#111111">
  <style>
    .rb main { max-width: 1040px; }
    .rb .rb-src { color: var(--muted); font-style: italic; max-width: 760px; }
    .rb .rb-toc { columns: 2 320px; padding-left: 0; list-style: none; margin: 18px 0 30px; }
    .rb .rb-toc li { break-inside: avoid; margin: 0 0 6px; }
    .rb .rb-toc a { text-decoration: none; color: inherit; }
    .rb .rb-toc a:hover { color: var(--rubric); }
    .rb .rb-toc-en { display: block; color: var(--muted); font-style: italic; font-size: .9em; padding-left: 2.2em; }
    .rb .rb-n { display: inline-block; min-width: 2.2em; color: var(--rubric); font-family: var(--caps); }
    .rb h2 { font-family: var(--caps); font-weight: 500; letter-spacing: .06em; font-size: 21px; color: var(--rubric); margin: 40px 0 12px; }
    .rb .rb-h-en { display: block; font-family: inherit; letter-spacing: 0; color: var(--muted); font-style: italic; font-size: 17px; }
    .rb .rb-sec { scroll-margin-top: 70px; }
    .rb .rb-pair { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; margin: 0 0 14px; }
    .rb .rb-pair p { margin: 0; line-height: 1.5; text-align: justify; hyphens: auto; }
    .rb .rb-en { color: var(--muted); font-style: italic; }
    @media (max-width: 760px) { .rb .rb-pair { grid-template-columns: 1fr; gap: 4px; } .rb .rb-en { font-size: .92em; } }
    @media print { .rb .rb-toc { display: none; } .rb .rb-pair { break-inside: avoid; } }
  </style>
</head>
<body class="rb">
<header class="top hide-print">
  <div class="top-in">
    <a class="brand" href="./" aria-label="Dominican Rite, today's Mass"><svg width="26" height="26" viewBox="0 0 40 40" aria-hidden="true"><rect x="17" y="3" width="6" height="34" fill="currentColor"/><rect x="3" y="17" width="34" height="6" fill="currentColor"/><circle cx="20" cy="4" r="3.6" fill="currentColor"/><circle cx="20" cy="36" r="3.6" fill="currentColor"/><circle cx="4" cy="20" r="3.6" fill="currentColor"/><circle cx="36" cy="20" r="3.6" fill="currentColor"/></svg>
      <span class="t1">Dominican Rite</span></a>
    <nav class="nav" aria-label="Main"><a href="./">Mass</a><a href="office.html">Office</a><a href="holyweek.html">Holy Week</a><a href="rubrics.html" aria-current="page">Rubrics</a><a href="about.html">About</a></nav>
  </div>
</header>
<div class="content"><div class="inner">
  <main class="prose">
    <h1>Rubricae generales Missarum</h1>
    <p class="rb-src">The general rubrics of the Mass from the <i>Missale juxta ritum Sacri Ordinis Praedicatorum</i> (Rome, 1939),
      with an English translation of our own. The Latin follows the Missal as printed, including the changes made to it up to
      1939; the later supplements and the reforms of 1955 and after are not included.</p>
    <ol class="rb-toc">%s</ol>
    %s
  </main>
</div></div>
<script src="js/ui.js"></script>
</body>
</html>
''' % (''.join(toc), '\n    '.join(body))
open(os.path.join(ROOT, 'rubrics.html'), 'w', encoding='utf8').write(page)
print('rubrics.html', len(page))
