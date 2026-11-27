# addrep.py "LINE" NEXTKEY : append a per-Mass line to A3.md and update Where I stopped
import sys,re
FN='/home/claude/dominican-liturgy/tools/audit/A3.md'
s=open(FN,encoding='utf8').read()
line=sys.argv[1]; nxt=sys.argv[2]; key=line.split(' |')[0]
s=re.sub(r'\*\*Where I stopped:\*\*.*', '**Where I stopped:** %s done (session 4); next %s.'%(key,nxt), s, count=1)
i=s.index('\n\n## "Qui tecum"')
s=s[:i]+'\n'+line+s[i:]
open(FN,'w',encoding='utf8').write(s)
print('ok')
