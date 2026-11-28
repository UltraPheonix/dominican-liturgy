# Writes tools/audit/A2.md from rows.py (ROWS, STOP, QUESTIONS, NOTES)
import json
d={}; exec(open('/tmp/A2/rows.py').read(),d)
G=json.load(open('/home/claude/dominican-liturgy/tools/audit/groups.json'))['A2']
n=len(json.load(open('/home/claude/dominican-liturgy/tools/audit/fixes/A2.json')))
L=['# Audit A2 (Missale O.P. 1939)','',
'**Where I stopped:** '+d['STOP'],'',
'Fixes: tools/audit/fixes/A2.json (%d entries, every one seen on the scan). Scripts: tools/audit/scripts/A2/ (copy to /tmp/A2 to run; '
'`runp.py` makes props.json, `build.py` applies ov/*.py, `show.py KEY` diffs, `mass.py KEY` shows the Mass, `r.sh`/`z.py` render the scan, '
'`fin4.py` (safe merge) merges ver3.py (session 4) into the fixes file, `rep.py` writes this report from rows.py).'%n,'',
'Chants: checked = each id\'s incipit/verse is the one the Missal prints for this Mass (no notes read).','',
'| KEY | M39 pages | Result |','|---|---|---|']
for k in G:
    if k in d['ROWS']:
        p,r=d['ROWS'][k]; L.append('| %s | %s | %s |'%(k,p,r))
    else: L.append('| %s | | NOT STARTED on the scan (proposal in proposals_report.txt) |'%k)
L+=['','## Open items','']+['- '+x for x in d.get('OPEN',[])]
L+=['','## QUESTIONS FOR JOSEPH','']+['%d. %s'%(i+1,q) for i,q in enumerate(d['QUESTIONS'])]
L+=['','## Notes','']+['- '+x for x in d['NOTES']]
open('/home/claude/dominican-liturgy/tools/audit/A2.md','w').write('\n'.join(L)+'\n')
print('report written', n, 'fixes')
