# Index the Dominican chants of GregoBase: gb_op.json  {id: {inc, part, mode, src, page, gabc, text}}
import sqlite3, json, re, unicodedata
db=sqlite3.connect('gb.sqlite')
DOM={11:'AOP1933',12:'MOP1936',13:'COP1949',14:'GOP1950',20:'POP1913',21:'HSOP1965',35:'AOP1862a',36:'AOP1862b'}
def gtext(g):
    g=re.sub(r'^.*?%%\s*','',g,flags=re.S) if '%%' in g else g
    t=re.sub(r'\([^)]*\)','',g)
    t=re.sub(r'<[^>]+>','',t); t=re.sub(r'\{|\}','',t)
    return re.sub(r'\s+',' ',t).strip()
out={}
for cid,inc,part,mode,mvar,gabc,src,page,ver,comm in db.execute('''select c.id,c.incipit,c."office-part",c.mode,c.mode_var,c.gabc,cs.source,cs.page,c.version,c.commentary from gregobase_chants c join gregobase_chant_sources cs on cs.chant_id=c.id where cs.source in (%s)'''%','.join(map(str,DOM))):
    try: g=json.loads(gabc) if gabc and gabc.startswith('"') else gabc
    except Exception: g=gabc
    if isinstance(g,list): g='\n'.join(x if isinstance(x,str) else '' for x in g)
    if not g: continue
    e=out.setdefault(str(cid),{'inc':inc,'part':part,'mode':mode,'mvar':mvar,'ver':ver,'comm':comm,'src':[],'gabc':g,'text':gtext(g)})
    e['src'].append([DOM[src],page])
json.dump(out,open('gb_op.json','w'),ensure_ascii=False)
import collections
print(len(out), collections.Counter(e['part'] for e in out.values()))
print(list(out.values())[0]['gabc'][:300]); print(list(out.values())[0]['text'])
