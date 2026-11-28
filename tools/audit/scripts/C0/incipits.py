#!/usr/bin/env python3
"""Coordinator: give each Gospel's English the opening its Latin has ("In illo témpore: Dixit Jesus discípulis suis:" →
"At that time: Jesus said to his disciples:"). Joseph's ruling: the English follows the Missal's Latin.
Prints the proposed changes; with --write appends them to tools/audit/fixes/C0.json.
28 Nov: the first version used a generic lead-in pattern and cut real text (Luke 10:16-17a; "Going, preach, saying") and turned
"Then shall the kingdom" into "Shall the kingdom" (CHECK.md session 2); corrected by later C0 entries. Now only the lead-ins in
LEADS (each reviewed) are replaced, and "Then shall the kingdom of heaven be like" becomes "The kingdom of heaven shall be like"."""
import json, re, sys, os
R0 = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
def load(fn):
    s = open(os.path.join(R0, fn)).read(); i = re.search(r'(?:var\s+\w+|window\.\w+)\s*=\s*', s).end(); j = max(s.rfind('}'), s.rfind(']')) + 1
    return json.loads(s[i:j])
MAP = [  # Latin incipit (after "In illo témpore:") → English
 ('Dixit Jesus discípulis suis parábolam hanc', 'Jesus spoke this parable to his disciples'),
 ('Dixit Jesus discípulis suis', 'Jesus said to his disciples'),
 ('Dixit Jesus discípulis', 'Jesus said to the disciples'),
 ('Dixit Petrus ad Jesum', 'Peter said to Jesus'),
 ('Dixit Jesus turbis Judæórum', 'Jesus said to the multitudes of the Jews'),
 ('Dixit Jesus turbis parábolam hanc', 'Jesus spoke this parable to the multitudes'),
 ('Dixit Jesus turbis', 'Jesus said to the multitudes'),
 ('Dixit Jesus Pharisǽis', 'Jesus said to the Pharisees'),
 ('Dicébat Jesus turbis hanc similitúdinem', 'Jesus spoke this similitude to the multitudes'),
 ('Dicébat Jesus Scribis, et Pharisǽis', 'Jesus said to the Scribes and Pharisees'),
 ('Dicébat Jesus turbis Judæórum', 'Jesus said to the multitudes of the Jews'),
 ('Locútus est Jesus ad turbas, et ad discípulos suos, dicens', 'Jesus spoke to the multitudes and to his disciples, saying'),
 ('Locútus est Jesus turbis Judæórum, dicens', 'Jesus spoke to the multitudes of the Jews, saying'),
 ('Dixit Pilátus ad Jesum', 'Pilate said to Jesus'),
 ('Dixit Jesus Simóni Petro', 'Jesus said to Simon Peter'),
 ('Dixit Jesus Petro', 'Jesus said to Peter'),
]
LEADS = ['Then Peter answering, said to him: ', 'Another parable he proposed unto them, saying: ', 'Another parable he proposed to them, saying: ',
 'Then Jesus said to his disciples: ', 'He said to them: ', 'He spoke also this parable: ', 'Jesus answered, and said to him: ',
 'Again therefore Jesus said to them: ', 'Then Jesus spoke to the multitudes and to his disciples, Saying: ', 'Again therefore, Jesus spoke to them, saying: ',
 'Turning to his disciples, he said: ', 'Pilate therefore went into the hall again, and called Jesus, and said to him: ', 'He said to all: ', 'And he said to all: ',
 'This he said, signifying by what death he should glorify God. And when he had said this, he saith to him: ', 'When therefore they had dined, Jesus saith to Simon Peter: ']
_OLD_LEAD = re.compile(r"^([^:]{0,170}?\b(?:said|saith|saying|spoke|proposed|parable|similitude)\b(?:\s+(?:(?:to|unto)\s+)?(?:him|them|her|all|(?:his|the)\s+\w+(?:\s+of\s+the\s+Jews)?|[A-Z]\w+(?:\s+[A-Z]\w+)?))?(?:,\s*saying)?\s*,?\s*):\s*", re.I)
R = load('data/readings33.js'); out = []
for k, L in R.items():
    if not isinstance(L, list): continue
    for i, x in enumerate(L):
        la, en = x.get('la', ''), x.get('en', '')
        m = re.match(r'In illo témpore:\s*(.+?):\s*(.*)', la, re.S)
        if not m or not en.startswith('At that time:'): continue
        inc = next((e for l, e in MAP if m.group(1) == l), None)
        if not inc: continue
        body = en[len('At that time:'):].lstrip()
        if re.sub(r'^(Then|And)\s+', '', body).lower().startswith(inc.lower()) and not body.lower().startswith(inc.lower()):
            pass  # e.g. "Then Jesus said to his disciples:" → normalised below by LEAD
        elif body.lower().startswith(inc.lower()): continue
        for L0 in LEADS:
            if body.startswith(L0): body = body[len(L0):]; break
        body = re.sub(r'^Then shall the kingdom of heaven be like', 'The kingdom of heaven shall be like', body)
        body = body[:1].upper() + body[1:]
        new = f'At that time: {inc}: {body}'
        out.append({"file": "data/readings33.js", "path": [k, i, 'en'], "old": en, "new": new,
                    "src": "the Missal's Latin incipit: " + la[:60], "why": "Joseph's ruling (27 Nov): the English follows the Missal's Latin; Gospel incipit added (coordinator script C0/incipits.py)"})
for e in out: print(e['path'][0], '|', e['old'][:110].replace('\n', ' '), '\n   →', e['new'][:110], '\n')
print(len(out))
if '--write' in sys.argv:
    fn = os.path.join(R0, 'tools/audit/fixes/C0.json'); C = json.load(open(fn)); C += out
    json.dump(C, open(fn, 'w'), ensure_ascii=False, indent=1); print('written')
