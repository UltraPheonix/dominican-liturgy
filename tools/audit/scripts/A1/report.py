import json
N=json.load(open('/tmp/A1/notes.json'))
G=json.load(open('/home/claude/dominican-liturgy/tools/audit/groups.json'))['A1']
F=json.load(open('/home/claude/dominican-liturgy/tools/audit/fixes/A1.json'))
done=[k for k in G if k in N['mass']]
L=['# Audit A1 (Temporale Adv1 to Quad5f)','',
'## Where I stopped','- '+N['stopped'],
'- Fix entries in tools/audit/fixes/A1.json: %d. `apply_fixes.py --dry`: 0 CONFLICT / MISSING.'%len(F),'',
'## Method (all Masses)',
]+['- '+x for x in N['method']]+['','## Results per Mass','| Mass | Missal page | Result |','|---|---|---|']
for k in G:
    if k in N['mass']:
        p,r=N['mass'][k]; L.append('| %s | %s | %s |'%(k,p,r))
    else: L.append('| %s | | not yet checked |'%k)
L+=['','## OPEN ITEMS (not fixable by a fixes entry, or outside this pass)']+['- '+x for x in N['open']]
L+=['','## QUESTIONS FOR JOSEPH']+['%d. %s'%(i+1,x) for i,x in enumerate(N['questions'])]
L+=['','## Leads found by the first script pass, not yet checked on the scan (Masses after the stop)']+['- '+x for x in N['leads']]
L+=['(from the first pass; items of Masses already done above are settled)','']+open('/tmp/A1/oldleads.md').read().replace('### ','#### ').splitlines()
L+=['','## Scripts (tools/audit/scripts/A1/; working copies in /tmp/A1)']+['- '+x for x in N['scripts']]
open('/home/claude/dominican-liturgy/tools/audit/A1.md','w').write('\n'.join(L)+'\n')
import shutil,glob
for f in glob.glob('/tmp/A1/*.py')+['/tmp/A1/dec.json','/tmp/A1/notes.json','/tmp/A1/headtail.txt']:
    shutil.copy(f,'/home/claude/dominican-liturgy/tools/audit/scripts/A1/')
for f in glob.glob('/tmp/A1/case_*.json'): shutil.copy(f,'/home/claude/dominican-liturgy/tools/audit/scripts/A1/')
print('report', len(done),'masses')
