"""Build processions.html from tools/proc/proc_data.py (Processionarium O.P., 1913). The notation is shown as printed
(page images in art/proc/<page>.png, from the CMAA scan) until it is transcribed; nothing is inferred."""
import os, re, html, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(H)); sys.path.insert(0, H)
from proc_data import SECTIONS
E = html.escape
shell = open(R + '/prayers.html', encoding='utf8').read()
head = shell[:shell.index('<div class="content">')]
head = head.replace('Prayers of the Priest', 'Processions').replace('aria-current="page"', '')
tail = shell[shell.index('</main>'):]
def pair(la, en, cls=''):
    return '<div class="pr-pair%s"><p lang="la">%s</p><p class="pr-en" lang="en">%s</p></div>' % (cls, la, en)
def vr(s): return re.sub(r'(℣\.|℟\.|Ant\.)', r'<span class="r">\1</span>', E(s))
out = ['<div class="content"><div class="inner">', '  <main class="prose">', '    <h1>Processionarium</h1>',
       '    <p class="pr-src">From the <i>Processionarium juxta ritum Sacri Ordinis Praedicatorum</i> (Rome, 1913, ed. Cormier). The chant is shown as printed, '
       'page by page (scan by the Church Music Association of America); the texts are given beneath in Latin and English.</p>',
       '    <p class="ai-note">The English is an AI translation from the Latin, not yet checked by a human translator.</p>',
       '    <ol class="pr-toc">' + ''.join('<li><a href="#%s">%s <span class="pr-toc-en">%s</span></a></li>' % (s['id'], E(s['la']), E(s['en'])) for s in SECTIONS) + '</ol>']
for s in SECTIONS:
    out.append('    <h2 class="pr-ph" id="%s">%s<span class="pr-h-en">%s · pp. %s</span></h2>' % (s['id'], E(s['la']), E(s['en']), '%d–%d' % (s['pages'][0], s['pages'][-1]) if len(s['pages']) > 1 else s['pages'][0]))
    for it in s['items']:
        if it[0] == 'rub': out.append(pair(E(it[1]), E(it[2]), ' pr-rub'))
        elif it[0] == 'txt': out.append(pair(vr(it[1]), vr(it[2])))
        elif it[0] == 'h': out.append('<h3 class="pc-h">%s<span class="pr-h-en">%s</span></h3>' % (E(it[1]), E(it[2])))
        elif it[0] == 'scan':
            pg = it[1]
            out.append('<details class="pc-scan"><summary>The chant as printed · p. %s</summary>%s</details>' % (
                ', '.join(map(str, pg)), ''.join('<img src="art/proc/%d.png" loading="lazy" alt="Processionarium O.P. (1913), page %d" width="800">' % (p, p) for p in pg)))
        elif it[0] == 'lit':
            rows = []
            for la, rl, en, re_ in it[1]:
                if la == '*': rows.append('<div class="pc-row pc-rr"><p lang="la">%s</p><p class="pr-en" lang="en">%s</p></div>' % (E(rl), E(re_))); continue
                rows.append('<div class="pc-row"><p lang="la">%s <span class="pc-resp">%s</span></p><p class="pr-en" lang="en">%s <span class="pc-resp">%s</span></p></div>' % (E(la), E(rl), E(en), E(re_)))
            out.append('<div class="pc-lit">' + ''.join(rows) + '</div>')
out.append('  ')
page = head + '\n'.join(out) + tail
page = page.replace('href="processions.html"', 'href="processions.html" aria-current="page"', 1)
open(R + '/processions.html', 'w', encoding='utf8').write(page)
print('processions.html', len(page))
