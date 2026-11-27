# append/replace entries in tools/audit/fixes/A2.json (same file+path => replaced)
import json,sys,re
OUT='/home/claude/dominican-liturgy/tools/audit/fixes/A2.json'
JUNK=re.compile(r'[¿¤«»@]|\.,|,\.|\s[,.;:]|[a-z]\s?-\s[a-z]|  ')
def check(v):
    s=json.dumps(v,ensure_ascii=False)
    for m in JUNK.finditer(s):
        raise SystemExit('JUNK %r in %s'%(m.group(0),s[max(0,m.start()-40):m.end()+40]))
def add(entries):
    cur=json.load(open(OUT))
    for e in entries:
        check(e['new'])
        cur=[c for c in cur if not (c['file']==e['file'] and c['path']==e['path'])]
        cur.append(e)
    json.dump(cur,open(OUT,'w'),ensure_ascii=False,indent=1)
    print('total',len(cur))
