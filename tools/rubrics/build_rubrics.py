"""Build rubrics.html (Rubricae generales Missarum, Missale O.P. 1939, Latin and English) from rubrics_data.py.
Usage: python3 tools/rubrics/build_rubrics.py"""
import html, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
from rubrics_data import PROLOGUE, TITLES, COLOURS
ROOT = os.path.join(H, '..', '..')
E = html.escape

def slug(n): return 'tit-' + n.lower()

# the words of prayers and chants named in the rubrics (said or not said), set in bold in both columns
INC = ['Gloria in excelsis Deo', 'Gloria in excelsis', 'Gloria Patri', 'Gloria tibi Domine', 'Te Deum laudamus', 'Kyrie eleison',
  'Christe eleison', 'Credo', 'Oremus', 'Dominus vobiscum', 'Et cum spiritu tuo', 'Domine exaudi orationem meam: et clamor meus ad te veniat',
  'Domine exaudi orationem meam', 'Orate fratres', 'Per omnia saecula saeculorum', 'Per Dominum nostrum', 'Qui vivis et regnas cum Deo Patre',
  'Per eumdem Dominum nostrum', 'Per eumdem Dominum', 'Qui tecum vivit', 'in unitate ejusdem Spiritus Sancti', 'Ite Missa est', 'Ite missa est',
  'Benedicamus Domino', 'Deo gratias', 'Requiescant in pace', 'Amen', 'Placeat', 'In principio erat Verbum', 'In principio',
  'Initium sancti Evangelii', 'Cum natus esset Jesus', 'Sequentia sancti Evangelii secundum', 'Memento', 'Communicantes', 'Hanc igitur',
  'Cum sanctificatus fuero', 'Omnipotens sempiterne Deus, qui vivorum', 'Omnipotens', 'Deus qui de beatae Mariae', 'Deus qui caritatis',
  'Deus, qui caritatis', 'Deus qui salutis', 'Deus qui pro nobis Filium', 'A cunctis', 'Deus, qui inter summos', 'Deus, qui inter apostolicos',
  'Deus, qui inter Apostolicos', 'Deus, cui proprium', 'Quaesumus Domine, ut animae', 'Deus, veniae largitor', 'Inclina, Domine',
  'Quaesumus, Domine, pro tua', 'Fidelium Deus', 'Animabus, quaesumus', 'Propitiare, quaesumus', 'Deus, qui nos Patrem',
  'Deus Indulgentiarum', 'Deus, cujus miseratione', 'pontificali', 'sacerdotali', 'Gloria']
INC_RE = re.compile('(?<![\\w>])(' + '|'.join(re.escape(x) for x in sorted(INC, key=len, reverse=True)) + ')(?![\\w<])')
def mark(t): return INC_RE.sub(r'<b class="rb-inc">\1</b>', E(t))

def pair(la, en):
    return ('<div class="rb-pair"><p class="rb-la" lang="la">%s</p><p class="rb-en" lang="en">%s</p></div>' % (mark(la), mark(en)))

import glob, importlib
# the other rubrics of the Missal (Ritus servandus etc.): one module per part, tools/rubrics/ritus_*.py, each defining a tuple
# (id, Latin title, English title, [(number, Latin heading, English heading, [(Latin, English), ...]), ...]); ORDER = Missal order
ORDER_BEFORE = ['ritus_defectibus', 'ritus_praeparatio', 'ritus_modus', 'ritus_varia', 'ritus_ministri', 'ritus_communio']
ORDER_AFTER = ['ritus_vestes']
def load(names):
    out = []
    for n in names:
        if os.path.exists(os.path.join(H, n + '.py')):
            m = importlib.import_module(n); out += [v for k, v in vars(m).items() if k.isupper() and isinstance(v, tuple)]
    return out
def part_html(P, toc, body):
    pid, la, en, chs = P
    sub = []
    for num, hla, hen, paras in chs:
        cid = pid + '-' + (num or 'p').lower()
        if hla: sub.append('<li><a href="#%s"><span class="rb-n">%s</span> %s <span class="rb-toc-en">%s</span></a></li>' % (cid, num, E(hla), E(hen)))
        body.append('<section class="rb-sec" id="%s">%s%s</section>' % (cid, ('<h3 class="rb-h3"><span class="rb-n">%s</span> %s<span class="rb-h-en">%s</span></h3>' % (num, E(hla), E(hen))) if hla else '', ''.join(pair(a, b) for a, b in paras)))
    toc.append('<li class="rb-part"><a href="#%s">%s <span class="rb-toc-en">%s</span></a>%s</li>' % (pid, E(la), E(en), ('<ol>' + ''.join(sub) + '</ol>') if sub else ''))
body = []
toc = []
for P in load(ORDER_BEFORE):
    body.append('<h2 class="rb-ph" id="%s">%s<span class="rb-h-en">%s</span></h2>' % (P[0], E(P[1]), E(P[2])))
    part_html(P, toc, body)
gen_toc = []
body.append('<h2 class="rb-ph" id="generales">Rubricae generales Missarum<span class="rb-h-en">General rubrics of the Mass</span></h2>')
body.append('<section class="rb-sec" id="prooemium">' + pair(*PROLOGUE) + '</section>')
for n, la, en, paras in TITLES:
    gen_toc.append('<li><a href="#%s"><span class="rb-n">%s</span> %s <span class="rb-toc-en">%s</span></a></li>' % (slug(n), n, E(la), E(en)))
    body.append('<section class="rb-sec" id="%s"><h2><span class="rb-n">%s</span> %s<span class="rb-h-en">%s</span></h2>%s</section>'
                % (slug(n), n, E(la), E(en), ''.join(pair(a, b) for a, b in paras)))
la, en, paras = COLOURS
gen_toc.append('<li><a href="#colores">%s <span class="rb-toc-en">%s</span></a></li>' % (E(la), E(en)))
toc.append('<li class="rb-part"><a href="#generales">Rubricae generales Missarum <span class="rb-toc-en">General rubrics of the Mass</span></a><ol>' + ''.join(gen_toc) + '</ol></li>')
body.append('<section class="rb-sec" id="colores"><h2>%s<span class="rb-h-en">%s</span></h2>%s</section>'
            % (E(la), E(en), ''.join(pair(a, b) for a, b in paras)))
for P in load(ORDER_AFTER):
    body.append('<h2 class="rb-ph" id="%s">%s<span class="rb-h-en">%s</span></h2>' % (P[0], E(P[1]), E(P[2])))
    part_html(P, toc, body)

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
    .rb .rb-sec, .rb .rb-ph { scroll-margin-top: 70px; }
    .rb h2.rb-ph { font-size: 26px; margin: 56px 0 8px; border-top: 1px solid var(--line); padding-top: 22px; }
    .rb h3.rb-h3 { font-family: var(--caps); font-weight: 500; letter-spacing: .05em; font-size: 19px; color: var(--rubric); margin: 30px 0 10px; }
    .rb .rb-toc .rb-part { margin: 0 0 14px; } .rb .rb-toc .rb-part > a { font-family: var(--caps); color: var(--rubric); }
    .rb .rb-toc ol { list-style: none; padding-left: 1em; margin: 4px 0 0; }
    .rb .rb-pair { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; margin: 0 0 14px; }
    .rb .rb-pair p { margin: 0; line-height: 1.5; text-align: justify; hyphens: auto; }
    .rb .rb-en { color: var(--muted); font-style: italic; }
    .rb .rb-inc { font-weight: 600; color: var(--ink); }
    .rb .rb-en .rb-inc { font-style: normal; }
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
    <h1>Rubricae Missalis</h1>
    <p class="rb-src">All the rubrics of the <i>Missale juxta ritum Sacri Ordinis Praedicatorum</i> (Rome, 1939), in the order of the Missal:
      the defects in celebrating Mass, the preparation, the rite of Low Mass, the ceremonial of the ministers at the solemn and conventual
      Mass, Holy Communion, the general rubrics and the colours,
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
