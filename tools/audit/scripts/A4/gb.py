import sqlite3,re,json,sys
c=sqlite3.connect('/home/claude/dominican-liturgy/tools/gregobase/gb.sqlite')
def text(gabc):
    g=gabc.split('%%')[-1] if '%%' in gabc else gabc
    g=re.sub(r'\([^)]*\)','',g); g=re.sub(r'<[^>]+>','',g); g=re.sub(r'\{|\}','',g)
    return re.sub(r'\s+',' ',g).strip()
def info(i):
    r=c.execute('select id,incipit,"office-part",gabc,version from gregobase_chants where id=?',(i,)).fetchone()
    if not r: return None
    src=c.execute('select source,page from gregobase_chant_sources where chant_id=?',(i,)).fetchall()
    g=r[3]
    try: g=json.loads(g)
    except Exception: pass
    return dict(id=r[0],inc=r[1],part=r[2],src=src,text=text(g if isinstance(g,str) else str(g)),ver=r[4])
def search(pat,part=None,srcs=(11,12,13,14,20,21,35,36)):
    out=[]
    for r in c.execute('select id,incipit,"office-part",gabc from gregobase_chants'):
        g=r[3]
        try: g=json.loads(g)
        except Exception: pass
        t=text(g if isinstance(g,str) else str(g))
        if re.search(pat,t,re.I) and (part is None or r[2]==part):
            src=c.execute('select source,page from gregobase_chant_sources where chant_id=?',(r[0],)).fetchall()
            if srcs is None or any(s[0] in srcs for s in src): out.append((r[0],r[2],src,t[:120]))
    return out
if __name__=='__main__':
    for a in sys.argv[1:]:
        if a.isdigit(): x=info(int(a)); print(x['id'],x['part'],x['src'],x['text'][:300]) if x else print(a,'NONE')
        else:
            for r in search(a): print(r)
