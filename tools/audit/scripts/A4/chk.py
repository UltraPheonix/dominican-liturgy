import json,sys
sys.path.insert(0,'/tmp/A4')
import fixgen as F
OUT='/home/claude/dominican-liturgy/tools/audit/fixes/A4.json'
FX0=json.load(open(OUT))
FX=[]
def P(k,f,acc,pg,manual=None,why='punctuation as printed'):
    FX.append(F.make(k,f,acc,manual,src=pg,why=why))
def RAW(file,path,old,new,src,why): FX.append({"file":file,"path":path,"old":old,"new":new,"src":src,"why":why})
def EN(k,i,pairs,src,why):
    old=F.A.RD[k][i]['en']; new=old
    for o,n in pairs:
        assert new.count(o)==1,(k,o); new=new.replace(o,n)
    RAW('data/readings33.js',[k,i,'en'],old,new,src,why)
def SUB(file,path,pairs,src,why):
    """substring replacements on the current value at path"""
    cur={'data/orations.js':F.A.O,'data/readings33.js':F.A.RD,'data/masses.js':F.A.D}[file]
    for p in path: cur=cur[p]
    new=cur
    for o,n in pairs:
        assert new.count(o)==1,(path,o,new.count(o)); new=new.replace(o,n)
    RAW(file,path,cur,new,src,why)
def dump():
    json.dump(FX0+FX,open(OUT,'w'),ensure_ascii=False,indent=1); print(len(FX0),'+',len(FX))
exec(open(sys.argv[1]).read())
for e in FX: print(e["path"], "\n  NEW:", e["new"] if not isinstance(e["new"],str) else e["new"][-0:], "\n")
