"""Compact the engine output into the site's Office data.

site/data/office/psalter/<k>.json : runs of psalm verses shared by every day
                                    ({"id": text}), sharded by id
site/data/office/YYYY-MM.json     : {"days": {"YYYY-MM-DD": {"t": head,
                                    "h": {hour: [[la, en], ...]}}},
                                    "b": {block id: text}}
Cells are block ids; a block's text may hold lines "§<psalm-run id>".
"""
import glob
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from parse import parse, HOURS

SRC = '/home/claude/dl/do_out'
OUT = '/home/claude/build/site/data/office'
VERSE = re.compile(r'^<n>\d+:\d+[a-z]?</n>')
NSHARD = 64


def hid(s, n=10):
    return hashlib.blake2b(s.encode('utf-8'), digest_size=8).hexdigest()[:n]


def load_tr():
    base = os.path.dirname(__file__)
    todo = {str(x['id']): x['la'] for x in json.load(open(f'{base}/tr_todo.json', encoding='utf-8'))}
    out = {}
    for f in sorted(glob.glob(f'{base}/tr/*.json')):
        for k, v in json.load(open(f, encoding='utf-8')).items():
            if k in todo:
                out[todo[k]] = v
    return out


TR = None
MARK = re.compile(r'^(℣\.|℟\.br\.|℟\.|Ant\.|\*)\s*')


def apply_tr(cell):
    """Put our English in place of Latin lines left untranslated in the English column."""
    global TR
    if TR is None:
        TR = load_tr()
    out = []
    for line in cell.split('\n'):
        t = re.sub(r'<[^>]+>', '', line).strip()
        en = TR.get(t)
        if not en:
            out.append(line)
            continue
        m = MARK.match(en)
        mark, rest = (m.group(1), en[m.end():]) if m else ('', en)
        if mark and mark != '*':
            new = f'<r>{mark}</r> {rest}'
        elif mark == '*':
            new = f'* {rest}'
        elif line.startswith('<c>') and rest:
            new = f'<c>{rest[0]}</c>{rest[1:]}'
        else:
            new = rest
        out.append(new)
    return '\n'.join(out)


LATIN_FIX = [
    ('Confiteor Deo omnipotenti, et beáte Maríae semper Vírgini, et beáto Domínico Patri nostro, et omnibus Sanctis: quia peccavi nimis cogitatione, locutione, opere et omissione, me cupla:',
     'Confíteor Deo omnipoténti, et beátæ Maríæ semper Vírgini, et beáto Domínico Patri nostro, et ómnibus Sanctis: quia peccávi nimis cogitatióne, locutióne, ópere et omissióne, mea culpa:'),
]


def tidy(cell):
    for a, b in LATIN_FIX:
        cell = cell.replace(a, b)
    cell = cell.replace(' <n>‡</n>', '').replace('<n>‡</n> ', '').replace('<n>‡</n>', '')
    return cell


def addrun(lines, runs):
    t = '\n'.join(lines)
    ch = int(re.match(r'^<n>(\d+)', lines[0]).group(1))
    k = '%02d.%s' % (min(ch // 10, 99), hid(t))
    runs[k] = t
    return k


def split_runs(cell, runs):
    out, cur = [], []
    for line in cell.split('\n'):
        if VERSE.match(line):
            cur.append(line)
            continue
        if cur:
            out.append('§' + addrun(cur, runs))
            cur = []
        out.append(line)
    if cur:
        out.append('§' + addrun(cur, runs))
    return '\n'.join(out)


def main(years_or_months):
    os.makedirs(OUT + '/psalter', exist_ok=True)
    runs = {}
    for f in glob.glob(OUT + '/psalter/[0-9][0-9].json'):
        runs.update(json.load(open(f, encoding='utf-8')))
    alldays = {}
    for ym in years_or_months:
        y = ym[:4]
        for f in sorted(glob.glob(f'{SRC}/{y}/{ym}*.Laudes.html')):
            d = os.path.basename(f)[:10]
            day = {'h': {}}
            for h in HOURS:
                p = f'{SRC}/{y}/{d}.{h}.html'
                if not os.path.exists(p) or os.path.getsize(p) < 500:
                    day = None
                    break
                r = parse(open(p, encoding='utf-8').read())
                if h == 'Laudes':
                    day['t'] = r['head']
                if h == 'Vespera':
                    day['tv'] = r['head']
                day['h'][h] = [[split_runs(tidy(c) if i == 0 else apply_tr(tidy(c)), runs) for i, c in enumerate(row)] for row in r['rows']]
                pp = f'{SRC}/{y}/{d}.{h}.P.html'
                if os.path.exists(pp) and os.path.getsize(pp) > 500:
                    rp = [[split_runs(tidy(c) if i == 0 else apply_tr(tidy(c)), runs) for i, c in enumerate(row)] for row in parse(open(pp, encoding='utf-8').read())['rows']]
                    if rp != day['h'][h]:
                        day.setdefault('p', {})[h] = rp
            if day:
                alldays[d] = day
    # blocks used on several days go to common.json
    use = {}
    for d, day in alldays.items():
        seen = set()
        for rows in list(day['h'].values()) + list(day.get('p', {}).values()):
            for row in rows:
                for c in row:
                    seen.add(c)
        for c in seen:
            use[c] = use.get(c, 0) + 1
    common_path = OUT + '/common.json'
    common = json.load(open(common_path, encoding='utf-8')) if os.path.exists(common_path) else {}
    for c, n in use.items():
        if n >= 20:
            common[hid(c)] = c
    for d, day in alldays.items():
        own = {}
        hours = {}
        for h, rows in day['h'].items():
            out = []
            for row in rows:
                ids = []
                for c in row:
                    k = hid(c)
                    if k not in common:
                        own[k] = c
                    ids.append(k)
                out.append(ids)
            hours[h] = out
        prs = {}
        for h, rows in day.get('p', {}).items():
            base = day['h'][h]
            if len(rows) == len(base):
                diff = {}
                for i, row in enumerate(rows):
                    if row != base[i]:
                        ids = []
                        for c in row:
                            k = hid(c)
                            if k not in common:
                                own[k] = c
                            ids.append(k)
                        diff[str(i)] = ids
                prs[h] = {'i': diff}
            else:
                allr = []
                for row in rows:
                    ids = []
                    for c in row:
                        k = hid(c)
                        if k not in common:
                            own[k] = c
                        ids.append(k)
                    allr.append(ids)
                prs[h] = {'all': allr}
        os.makedirs(f'{OUT}/{d[:4]}', exist_ok=True)
        rec = {'t': day.get('t', []), 'tv': day.get('tv', []), 'h': hours, 'p': prs, 'b': own}
        with open(f'{OUT}/{d[:4]}/{d[5:]}.json', 'w', encoding='utf-8') as fh:
            json.dump(rec, fh, ensure_ascii=False, separators=(',', ':'))
    with open(common_path, 'w', encoding='utf-8') as fh:
        json.dump(common, fh, ensure_ascii=False, separators=(',', ':'))
    shards = {}
    for k, v in runs.items():
        shards.setdefault(k[:2], {})[k] = v
    for s_, dct in shards.items():
        with open(f'{OUT}/psalter/{s_}.json', 'w', encoding='utf-8') as fh:
            json.dump(dct, fh, ensure_ascii=False, separators=(',', ':'))
    dates = sorted(set(os.path.basename(p)[:5] and p[-15:-5] for p in glob.glob(OUT + '/[0-9][0-9][0-9][0-9]/*.json')))
    dd = sorted(p.split('/')[-2] + '-' + p.split('/')[-1][:5] for p in glob.glob(OUT + '/[0-9][0-9][0-9][0-9]/*.json'))
    json.dump({'from': dd[0], 'to': dd[-1]}, open(OUT + '/range.json', 'w'))
    tot = sum(os.path.getsize(f) for f in glob.glob(OUT + '/psalter/*.json'))
    sizes = [os.path.getsize(f'{OUT}/{d[:4]}/{d[5:]}.json') for d in alldays]
    print(len(alldays), 'days; day files avg', sum(sizes) // max(1, len(sizes)) // 1024, 'KB max', max(sizes) // 1024,
          'KB; common', len(common), os.path.getsize(common_path) // 1024, 'KB; psalm runs', len(runs), tot // 1024, 'KB')


if __name__ == '__main__':
    main(sys.argv[1:])
