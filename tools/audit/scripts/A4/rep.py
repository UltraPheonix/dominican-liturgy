import sys
fn='/home/claude/dominican-liturgy/tools/audit/A4.md'
done,nxt=sys.argv[1],sys.argv[2]; text=sys.stdin.read().rstrip('\n')+'\n'
s=open(fn).read()
import re
s=re.sub(r'\*\*Where I stopped: .*?\*\*',f'**Where I stopped: {done} done; next Mass not started: {nxt}.**',s,count=1)
s=s.replace("\n## Site-wide item","\n"+text+"\n## Site-wide item",1)
s=s.replace("\n\n\n","\n\n")
open(fn,'w').write(s)
