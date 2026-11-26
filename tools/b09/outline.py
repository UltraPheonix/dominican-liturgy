"""Condensed outline of a page range of the 1909 Breviary: structure lines only (psalm verses skipped), accents restored.
usage: python3 outline.py v1 86 246 > outline.txt"""
import re, sys, gzip, os
sys.path.insert(0, os.path.dirname(__file__))
from latdict import fix_line
vol, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
pages = gzip.open(os.path.join(os.path.dirname(__file__), 'text', vol + '.txt.gz'), 'rt').read().split('\f### ')[1:]
START = re.compile(r'^(Ant|Antiphona|Capitulum|Hymnus|Oratio|Orémus|Oremus|Responsorium|R\. ?br|Lectio|Benedictio|Absolutio|Invitatorium|In Nocturno|Ad [A-Z]|AD [A-Z]|DOMINICA|FERIA|SABBATO|IN |T |¶|f\.|y\.|V\.|J\.|Gloria Patri|Glória Patri|Hic non|Kyrie|Pater noster|Credo|Psalmus|Canticum|Cánticum|Ps\.)')
skip = False
for pg in pages[a:b]:
    i, body = pg.split('\n', 1)
    print('== p%s' % i)
    for col in body.split('\n||\n'):
        for l in col.split('\n'):
            s = l.strip()
            if not s or re.match(r'^[\W\d]{0,4}$', s): continue
            if re.match(r'^(Psalmus|Canticum|Cánticum)', s): print(fix_line(s)); skip = True; continue
            if skip and not START.match(s): continue
            skip = False
            print(fix_line(s))
