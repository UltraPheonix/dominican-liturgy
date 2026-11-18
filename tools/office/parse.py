"""Turn the Divinum Officium engine's HTML into a compact structure.

Each hour becomes {"head": [...], "rows": [[latin, english], ...]} where every
cell is a short markup string:  <r>red</r>  <h>section heading</h>
<c>initial</c>  <n>verse number</n>  <k>black</k>, lines separated by \n.
"""
import html
import re

HOURS = ['Matutinum', 'Laudes', 'Prima', 'Tertia', 'Sexta', 'Nona', 'Vespera', 'Completorium']


def clean_cell(s):
    s = re.sub(r"<DIV ALIGN='right'>.*?</DIV>", '', s, flags=re.S)
    s = re.sub(r"<A ID='[^']*'></A>", '', s)
    s = re.sub(r"<FONT SIZE='-1' >.*?</FONT>", '', s, flags=re.S)       # engine comments {..}
    s = s.replace('\n', '')
    s = re.sub(r'<br\s*/?>', '\n', s, flags=re.I)
    s = re.sub(r"<span style='color:red; font-size:1.25em'>(.*?)</span>", r'\1', s)
    s = re.sub(r"<span class='nigra'>(.*?)</span>", r'<k>\1</k>', s)
    # nested FONT: do innermost first, several passes
    for _ in range(4):
        s = re.sub(r"<FONT SIZE='\+1' COLOR=\"red\">((?:(?!<FONT).)*?)</FONT>", r'<h>\1</h>', s, flags=re.S)
        s = re.sub(r"<FONT SIZE='\+2' COLOR=\"red\">((?:(?!<FONT).)*?)</FONT>", r'<c>\1</c>', s, flags=re.S)
        s = re.sub(r"<FONT SIZE='1' COLOR=\"red\">((?:(?!<FONT).)*?)</FONT>", r'<n>\1</n>', s, flags=re.S)
        s = re.sub(r"<FONT COLOR=\"red\">((?:(?!<FONT).)*?)</FONT>", r'<r>\1</r>', s, flags=re.S)
        s = re.sub(r"<FONT[^>]*>((?:(?!<FONT).)*?)</FONT>", r'\1', s, flags=re.S)
    s = re.sub(r'</?(?:B|I|SPAN|span|A)[^>]*>', '', s)
    s = re.sub(r'<(?!/?[rhcnk]>)[^>]+>', '', s)
    s = html.unescape(s)
    s = re.sub(r'<(r|h|c|n|k)>\s*</\1>', '', s)
    s = re.sub(r'[ \t]+', ' ', s)
    lines = [l.strip() for l in s.split('\n')]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    out = []
    for l in lines:          # collapse runs of blank lines
        if not l and out and not out[-1]:
            continue
        out.append(l)
    return '\n'.join(out)


def parse(text):
    i = text.find('<P ALIGN=CENTER>')
    head = []
    if i >= 0:
        j = text.find('</P>', i)
        h = text[i:j]
        h = re.sub(r'<br\s*/?>', '\n', h)
        h = html.unescape(re.sub(r'<[^>]+>', '', h))
        head = [x.strip() for x in h.split('\n') if x.strip()]
    rows = []
    for tr in re.findall(r'<TR>(.*?)</TR>', text, re.S):
        tds = re.findall(r'<TD[^>]*>(.*?)</TD>', tr, re.S)
        if not tds:
            continue
        cells = [clean_cell(t) for t in tds]
        if len(cells) == 1:
            cells.append('')
        rows.append(cells[:2])
    return {'head': head, 'rows': rows}


if __name__ == '__main__':
    import sys
    import json
    r = parse(open(sys.argv[1], encoding='utf-8').read())
    print(json.dumps(r, ensure_ascii=False, indent=1)[:6000])
