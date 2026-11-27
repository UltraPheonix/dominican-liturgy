import json,re
d=json.load(open('/home/claude/dominican-liturgy/tools/audit/fixes/A2.json'))
J=re.compile(r'[¿¤«»@]|\.,|,\.|\s[,.;:!?]|Arnen|  |\bPs\b')
for e in d:
    s=json.dumps(e['new'],ensure_ascii=False)
    for m in J.finditer(s): print('JUNK',e['path'],repr(s[max(0,m.start()-40):m.end()+30]))
print('checked',len(d))
