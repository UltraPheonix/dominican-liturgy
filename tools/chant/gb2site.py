"""gb2site.py ID NAME "book line" -> site/gabc/NAME.gabc from the GregoBase sqlite, with a header like the site's."""
import sqlite3, json, sys
i, name, book = int(sys.argv[1]), sys.argv[2], sys.argv[3]
c = sqlite3.connect('/home/claude/build/gb/gb.sqlite')
r = c.execute('select incipit, "office-part", mode, transcriber, gabc from gregobase_chants where id=?', (i,)).fetchone()
OP = {'an': 'Antiphona', 'hy': 'Hymnus', 're': 'Responsorium', 'rb': 'Responsorium breve', 'tr': 'Tractus', 'or': 'Ordinarium', 'va': 'Varia', 'al': 'Alleluia'}
g = json.loads(r[4])
open('/home/claude/build/site/gabc/%s.gabc' % name, 'w').write(
    'name:%s;\noffice-part:%s;\nmode:%s;\nbook:%s;\ntranscriber:%s (GregoBase %d);\n%%%%\n%s\n' % (r[0], OP.get(r[1], r[1] or ''), r[2] or '', book, r[3] or 'GregoBase', i, g.strip()))
print(name, r[0], r[2], g[:160].replace('\n', ' '))
