"""Map tools/m39/kalendar39.txt to the site's Mass keys (data/masses.js) -> /tmp/x/krows.json + report."""
import json,re,unicodedata,subprocess
subprocess.run(['node','-e',"""var vm=require('vm'),fs=require('fs');var c={window:{}};vm.createContext(c);vm.runInContext(fs.readFileSync('data/masses.js','utf8')+';window.D=DOMINICAN;',c);var D=c.window.D;
var o={};Object.keys(D.masses).forEach(k=>{var m=D.masses[k];o[k]={t:m.title,mo:m.month,d:m.day,r:m.rank,op:m.op}});fs.writeFileSync('/tmp/x/sitem.json',JSON.stringify(o))"""],check=True)
S=json.load(open('/tmp/x/sitem.json'))
def norm(s): return unicodedata.normalize('NFD',s or '').encode('ascii','ignore').decode().lower().replace('ae','e').replace('j','i').replace('y','i')
STOP=set('s ss b bb et conf ep mart virg vid op o p eccl doct papae papa apostoli pres presb abbatis mm sociorum soc in de a ab ad i ii v iii confessoris martyris virginis episcopi'.split())
def words(s): return [w for w in re.findall(r'[a-z]+',norm(s)) if w not in STOP and len(w)>2]
byday={}
for k,m in S.items():
    if m.get('mo') is not None and m.get('d'): byday.setdefault('%02d%02d'%(m['mo']+1,m['d']),[]).append(k)
rows=[];used=set()
for l in open('tools/m39/kalendar39.txt'):
    if l.startswith('#') or not l.strip(): continue
    f=l.rstrip('\n').split('|'); d,t,r=f[0],f[1],f[2]; note=f[3] if len(f)>3 else ''
    best=None;bs=0
    a=set(words(t))
    for k in S:
        b=set(words(S[k]['t']))
        sc=sum(1 for x in a if any(x[:5]==y[:5] for y in b))/max(1,len(a))
        same=k in byday.get(d,[])
        sc=sc+(0.3 if same else 0)-(0 if same else 0.25)
        if sc>bs: bs,best=sc,k
    ok=bs>=0.6 and r not in ('Memoria','Vigilia') or bs>=0.9
    rows.append([d,t,r,note,best if ok else None])
    if ok: used.add(best)
json.dump(rows,open('/tmp/x/krows.json','w'),ensure_ascii=False)
if __name__=='__main__':
    for x in rows:
        if x[4] is None and x[2] not in ('Memoria','Vigilia'): print('NOMASS',x[0],x[1],'|',x[2],'| site:',[(k,S[k]['t'][:40]) for k in byday.get(x[0],[])])
    print('---- site Masses with a date, not in the 1939 calendar:')
    for k,m in sorted(S.items()):
        if m.get('mo') is not None and m.get('d') and k not in used: print(k,'|',m['t'],'|',m.get('r'))
