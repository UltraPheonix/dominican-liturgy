# rep.py KEY "Missal page" "result" : set KEY's row in tools/audit/A1.md and the "Where I stopped" session-4 line
import sys,re,json
FN='/home/claude/dominican-liturgy/tools/audit/A1.md'
k,pg,res=sys.argv[1:4]
s=open(FN,encoding='utf8').read()
row='| %s | %s | %s |'%(k,pg,res)
s2,n=re.subn(r"^\| %s \|.*$"%re.escape(k),lambda m:row,s,count=1,flags=re.M)
assert n==1,n
n_fix=len(json.load(open('/home/claude/dominican-liturgy/tools/audit/fixes/A1.json')))
line='- Session 4 (28 Nov): audited Quad2m to %s on the scan; next is the Mass after %s in groups.json "A1". Fix entries in tools/audit/fixes/A1.json: %d (session-4 entries marked "s4": true; scripts tools/audit/scripts/A1/s4_*).'%(k,k,n_fix)
if '- Session 4 (28 Nov)' in s2: s2=re.sub(r'^- Session 4 \(28 Nov\).*$',lambda m:line,s2,flags=re.M)
else: s2=s2.replace('## Where I stopped\n','## Where I stopped\n'+line+'\n',1)
open(FN,'w',encoding='utf8').write(s2); print('ok',n_fix)
