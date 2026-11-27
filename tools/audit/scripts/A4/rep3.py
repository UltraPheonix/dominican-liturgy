import sys,re
fn='/home/claude/dominican-liturgy/tools/audit/A4.md'
s=open(fn).read()
lines=open(sys.argv[1]).read().rstrip('\n')
nxt=sys.argv[2]
H='\n### Session 3 Masses (from S0802, groups.json order)\n'
if H not in s: s=s.replace('\n## Site-wide item',H+'\n## Site-wide item',1)
s=s.replace('\n## Site-wide item','\n'+lines+'\n\n## Site-wide item',1)
s=re.sub(r'\*\*Where I stopped:[^\n]*\*\*',f'**Where I stopped: session 3, last Mass done {sys.argv[3]}; next Mass not started: {nxt}.**',s,1)
open(fn,'w').write(s)
