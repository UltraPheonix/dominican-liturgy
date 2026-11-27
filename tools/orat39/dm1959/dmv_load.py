import json,re
def loadjs(p, var):
    s=open(p,encoding='utf8').read()
    i=s.index('{'); j=s.rindex('}')
    return json.loads(s[i:j+1])
