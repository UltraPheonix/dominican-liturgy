import json,sys,re
o=json.load(open('new_or.json'))
for k in sys.argv[1:]:
    print('##',k)
    for kind in ('or','se','pc'):
        print(kind, re.sub(r'(Per Dóminum|Per eúndem|Qui vivis|Qui tecum).*$', r'\1…', o[k][kind][0]))
