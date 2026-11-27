import sqlite3,re,sys,unicodedata
c=sqlite3.connect('/home/claude/dominican-liturgy/tools/gregobase/gb.sqlite')
DOM=('11','12','13','14','20','21','35','36')
def text(g):
    g=re.sub(r'\([^)]*\)','',g or ''); g=re.sub(r'<[^>]*>','',g); g=re.sub(r'\{|\}|\[[^\]]*\]','',g)
    return re.sub(r'\s+',' ',g).strip()
def search(pat,part=None):
    q="select c.id,c.incipit,c.\"office-part\",s.source,s.page,c.gabc from gregobase_chants c join gregobase_chant_sources s on s.chant_id=c.id"
    out=[]
    for cid,inc,op,src,pg,g in c.execute(q):
        if str(src) not in DOM: continue
        if part and op!=part: continue
        if re.search(pat,(inc or '')+' ',re.I): out.append((cid,inc,op,src,pg,text(g)))
    return out
if __name__=='__main__':
    for r in search(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else None): print(r[:5],'|',r[5][:300])
