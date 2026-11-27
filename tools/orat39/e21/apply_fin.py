import json,re,sys,difflib,unicodedata
sys.path.insert(0,'.')
exec(open(sys.argv[1] if len(sys.argv)>1 else '/tmp/fin.py').read())
ANCH={'Adv2':8911,'Epi1':12090,'Jan1':11388,'Pent23':38103,'G502_3':54239,'ChristusRex':65905,'G491':53524,'C7s':70768,'C11s':70536,'C18s':70875,'C21s':71139,'C30s':71528,'C32s':71656,'C35s':71812,'C42s':72124,'C45s':72423,'C48s':72565,'C51s':73383,'Quad5f':38983,'S0114':42658,'S0117':42845,'S0127':43854,'S0128':43917,'S0129':44066,'S0131':44172,'S0202':44466,'S0204':44802,'S0208':45006,'S0209':45043,'S0223':45770,'S0404':47712,'S0421':48406,'S0502':49475,'S0510':50615,'S0527':51970,'S0606':52724,'S0611':52920,'S0613':53142,'S0618':53454,'S0712':55748,'S0714':55892,'S0715':56024,'S0816':59149,'S0820':59590,'S0822':69110,'S0828':60246,'S0915':38983,'S0929':62923,'S1006':63877,'S1019':64897,'S1102':66261,'S1102_2':66456,'S1102_3':66577,'S1104':66737,'S1111':67095,'S1117':67637,'S1120':67890,'S1124':68302,'S1125':68362,'S1204':40247,'S1213':41084,'S1226':41454}
L=open('m39lin.txt').read().split('\n')
def pdfof(line):
    p=0
    for l in L[:line]:
        if l.startswith('@@PAGE'): p=int(l.split()[1])
    return p
sys.path.insert(0,'/tmp'); 
import importlib.util
spec=importlib.util.spec_from_file_location('po','/tmp/pageof.py'); po=importlib.util.module_from_spec(spec); spec.loader.exec_module(po)
def F_(s):
    s=s.replace('æ','ae').replace('œ','oe').replace('ǽ','ae')
    s=''.join(c for c in unicodedata.normalize('NFD',s) if not unicodedata.combining(c))
    return re.sub(r'[^a-z]','',s.lower().replace('j','i'))
o=open('../../data/orations.js').read(); O=json.loads(o[o.index('{'):].rstrip().rstrip(';'))
X=json.load(open('extra_final.json')); E=json.load(open('en_final.json'))
CUT=re.compile(r'[;,]?\s*(through (our|the same)|who live|who lives|world without end|Who live|Who lives|Through)')
for k,v in F.items():
    v=dict(v)
    if not v['p']:
        p0=pdfof(ANCH[k]); r=po.find(v['or'],[p0,p0+1,p0-1,p0+2]); r2=po.find(v['pc'],[p0,p0+1,p0+2,p0+3])
        a=po.label(*r) if r else '?'; b=po.label(*r2) if r2 else a
        v['p']=a if a==b else a+'-'+b
    X[k]=v
    en=dict(EN.get(k,{}))
    for kind in ('or','se','pc'):
        if kind in en: continue
        old=O.get(k,{}).get(kind)
        assert old, (k,kind,'no old english')
        r=difflib.SequenceMatcher(None,F_(old[0])[:200],F_(v[kind])[:200]).ratio()
        if r<0.9: print('CHECK',k,kind,round(r,2),'|',old[1][:150])
        m=CUT.search(old[1]); en[kind]=old[1][:m.start()] if m else old[1]
    E[k]=en
    print(k,v['p'])
json.dump(X,open('extra_final.json','w'),ensure_ascii=False,indent=1)
json.dump(E,open('en_final.json','w'),ensure_ascii=False,indent=1)
