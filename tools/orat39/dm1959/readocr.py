# read back the crop OCR: keep only the words inside the kept text objects (drops margin notes), in reading order
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from dmpaths import *
import csv, json, glob, re
def words_of(stem):
    meta = json.load(open(stem + '.json')); r = meta['rect']; sc = 72 / meta['dpi']; pad = meta['pad']
    rows = []
    with open(stem + '.tsv', newline='') as f:
        for d in csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE):
            if d['level'] != '5' or not d['text'].strip(): continue
            L, T, Wd, H = (int(d[k]) for k in ('left', 'top', 'width', 'height'))
            cx = r[0] + (L - pad + Wd / 2) * sc
            rows.append({'t': d['text'], 'conf': float(d['conf']), 'key': (int(d['block_num']), int(d['par_num']), int(d['line_num']), int(d['word_num'])), 'cx': cx, 'top': r[1] + (T - pad) * sc, 'bot': r[1] + (T - pad + H) * sc})
    rows.sort(key=lambda w: w['key'])
    lines = {}
    for w in rows: lines.setdefault(w['key'][:3], []).append(w)
    for ws in lines.values():
        cy = (min(w['top'] for w in ws) + max(w['bot'] for w in ws)) / 2
        for w in ws:
            w['y'] = cy
            w['in'] = any(g[0] - 4 <= w['cx'] <= g[2] + 4 and abs(cy - (g[1] + g[3]) / 2) <= 5 for g in meta['g'])
    return rows
def lines_of(stem):
    ws = [w for w in words_of(stem) if w['in']]
    out = []; last = None
    for w in ws:
        k = w['key'][:3]
        if k != last: out.append([]); last = k
        out[-1].append(w)
    return out
def text_of(i, side):
    lines = []
    for stem in sorted(glob.glob(W_(f'crops/{i:04d}_{side}_*.tsv'))):
        if os.path.exists(stem[:-4] + '.json'): lines += lines_of(stem[:-4])
    return lines
if __name__ == '__main__':
    for i in map(int, sys.argv[1:]):
        for side in 'el':
            print(i, side, ' / '.join(' '.join(w['t'] for w in l) for l in text_of(i, side)))
