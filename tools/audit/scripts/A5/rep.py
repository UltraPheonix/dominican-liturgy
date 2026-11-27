# usage: python3 rep.py KEY "line"  -> replaces the line starting "| KEY |" or inserts before "| C114s, C114o, S1113"
import sys
p='/home/claude/dominican-liturgy/tools/audit/A5.md'; s=open(p).read()
k,line=sys.argv[1],sys.argv[2]
tag='| %s |'%k
if tag in s:
    i=s.index(tag); j=s.index('\n',i); s=s[:i]+line+s[j:]
else:
    i=s.index('| C114s, C114o, S1113'); s=s[:i]+line+'\n'+s[i:]
open(p,'w').write(s)
