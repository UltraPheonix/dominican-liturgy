import json,re,os
ROOT='/home/claude/dominican-liturgy'
def load(fn):
    s=open(os.path.join(ROOT,fn),encoding='utf8').read()
    i=re.search(r'(?:var\s+\w+|window\.\w+)\s*=\s*', s).end()
    j=max(s.rfind('}'), s.rfind(']'))+1
    return json.loads(s[i:j])
