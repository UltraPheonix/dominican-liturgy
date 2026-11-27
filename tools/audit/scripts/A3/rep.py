# rep.py KEY "page" "result"  -> appends a row to the A3.md table; updates the 'Where I stopped' line
import sys,re
FN='/home/claude/dominican-liturgy/tools/audit/A3.md'
key,page,res=sys.argv[1:4]
s=open(FN,encoding='utf8').read()
lines=s.split('\n')
i=lines.index('---|---|---')
j=i+1
while j<len(lines) and lines[j].strip() and '|' in lines[j]: j+=1
row='%s | %s | %s'%(key,page,res)
lines=[l for l in lines if not l.startswith(key+' | ')] if False else lines
lines.insert(j,row)
s='\n'.join(lines)
nxt=sys.argv[4] if len(sys.argv)>4 else ''
s=re.sub(r'^\*\*Where I stopped:\*\*.*$', '**Where I stopped:** %s done (session 3); next %s.'%(key,nxt), s, count=1, flags=re.M)
open(FN,'w',encoding='utf8').write(s)
print('ok')
