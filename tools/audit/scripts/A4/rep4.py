import sys,re
fn='/home/claude/dominican-liturgy/tools/audit/A4.md'
s=open(fn).read()
lines=open(sys.argv[1]).read().rstrip('\n')
nxt=sys.argv[2]
H='\n### Session 4 Masses (from S0901, groups.json order; Rubr. gen. re-read in full, m39lin @@PAGE 24-33, M39 pp. 47-57)\n'
if H not in s: s=s.replace('\n## Site-wide item',H+'\n## Site-wide item',1)
s=s.replace('\n## Site-wide item','\n'+lines+'\n\n## Site-wide item',1)
s=re.sub(r'\*\*Where I stopped:[^\n]*',f'**Where I stopped: session 4, last Mass done {sys.argv[3]}; next Mass not started: {nxt}.** (apply_fixes.py handles chained entries; merge_chains.py is no longer needed.)',s,1)
open(fn,'w').write(s)
