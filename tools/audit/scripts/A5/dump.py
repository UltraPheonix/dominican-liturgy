import sys; sys.path.insert(0,'/tmp/A5')
from lib import *
for k in sys.argv[1:]:
  m=M.get(k,{})
  print('=====',k,m.get('title'),'| page',m.get('page'),'| conf',m.get('conf'),'| intr',m.get('introit'))
  for p,v in (m.get('parts') or {}).items():
    print('  ',p,[(x.get('id'),chinc(x.get('id')), {kk:vv for kk,vv in x.items() if kk!='id'}) for x in v])
  if m.get('extras'): print('   extras',m['extras'])
  if k in O:
    print('  src',O[k].get('src'))
    for p in O[k]:
      if p=='src': continue
      print('  ',p,'|',O[k][p][0] if isinstance(O[k][p],list) else O[k][p])
  for it in R.get(k,[]):
    print('  RD',it['ref'],'|',it['title'],'|',it['la'])
