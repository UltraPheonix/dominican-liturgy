import json,re,unicodedata
ROOT='/home/claude/dominican-liturgy/'
def load(fn):
    s=open(ROOT+fn).read(); i=re.search(r'(?:var\s+\w+|window\.\w+)\s*=\s*',s).end(); j=max(s.rfind('}'),s.rfind(']'))+1
    return json.loads(s[i:j])
D=load('data/masses.js'); M=D['masses']; CH=D['chants']
O=load('data/orations.js'); R=load('data/readings33.js')
A5=json.load(open(ROOT+'tools/audit/groups.json'))['A5']
def chinc(cid):
    c=CH.get(str(cid),{}); return c.get('i','?')
