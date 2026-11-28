#!/usr/bin/env python3
"""Apply the Mass-text audit fixes (tools/audit/fixes/*.json) to the live data files. Idempotent: safe to run
any number of times, and must be run again after any rebuild of data/orations.js, readings33.js, masses.js,
addiv.js or memoriae.js.

A fixes file is a JSON list of entries:
  {"file": "data/orations.js", "path": ["Adv1", "or", 0], "old": "<exact current value>", "new": "<corrected value>",
   "src": "M39 p. 1 (pdf 33)", "why": "punctuation as printed"}
"path" navigates the JSON object of the file (keys and list indices). "old" must equal the current value (else the
entry is reported as CONFLICT and skipped); if the value already equals "new" it is skipped as done.
Values may be strings or any JSON value.
To ADD something the data lacks (a missing reading, a missing key): give "op": "add" and "old": null. The last path element
is a new dict key, or a list index equal to the list's length (append). If the value is already there and equal to "new",
the entry is done; if something different is there, it is a CONFLICT. Usage: python3 tools/audit/apply_fixes.py [--dry]
"""
import json, glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dry = '--dry' in sys.argv

def load(fn):
    s = open(os.path.join(ROOT, fn), encoding='utf8').read()
    i = re.search(r'(?:var\s+\w+|window\.\w+)\s*=\s*', s).end()
    j = max(s.rfind('}'), s.rfind(']')) + 1
    return s, i, j, json.loads(s[i:j])

def dump(obj, orig):
    sep = (', ', ': ') if '": ' in orig[:5000] else (',', ':')
    return json.dumps(obj, ensure_ascii=False, separators=sep)

# Joseph, 27 Nov 22:35: every expanded conclusion is pointed "Fílium tuum; qui tecum" (the Missal's printed pointing,
# e.g. pp. 245, 247, 472-473). canon() applies it to every string, so entries written before or after the change agree.
CAPS = str.maketrans({'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ý': 'Y', 'Ǽ': 'Æ'})
def canon(v):
    if isinstance(v, str):
        v = v.replace('Fílium tuum: qui tecum', 'Fílium tuum; qui tecum').replace('Fílium tuum: Qui tecum', 'Fílium tuum; qui tecum')
        # the rest of the printed pointing of the full conclusion (M39 pp. 16, and e.g. "Sancti Deus : per omnia",
        # "cum Deo Patre; in unitate"): ':' before "per ómnia", ';' before "in unitáte" after "Deo Patre"
        v = re.sub(r'Spíritus Sancti,? Deus[,:]? per ómnia', 'Spíritus Sancti Deus: per ómnia', v)
        v = re.sub(r'Spíritus Sancti Deus per ómnia', 'Spíritus Sancti Deus: per ómnia', v)
        v = re.sub(r'cum Deo Patre,? in unitáte', 'cum Deo Patre; in unitáte', v)
        v = v.replace('Christum, Fílium tuum;', 'Christum Fílium tuum;')   # no comma, as printed (pp. 472-475, 516, 545)
        # the Missal prints no accent on a capital letter ("Angelus", "Anima", "Ideo"; CHECK.md)
        v = v.translate(CAPS)
        return v
    if isinstance(v, list): return [canon(x) for x in v]
    if isinstance(v, dict): return {k: canon(x) for k, x in v.items() if k != 'la_fixed'}   # la_fixed: dead OCR scratch field, removed 28 Nov
    return v

# Entries on the same path form a chain (an auditor correcting its own earlier entry). An earlier link is "superseded"
# when the current value already equals the "new" of a later link on that path.
ALL = []
for ff in sorted(glob.glob(os.path.join(ROOT, 'tools/audit/fixes/*.json'))):
    for e in json.load(open(ff, encoding='utf8')): ALL.append((ff, e))
LATER = {}
for n, (ff, e) in enumerate(ALL): LATER.setdefault((e['file'], json.dumps(e['path'])), []).append(n)

def replayed(n, stages=False):
    """Entry n's "new" with every later, deeper entry (path extends n's path) applied to it, in order.
    With stages=True, return the list of every intermediate state (so a value part-way through the chain matches)."""
    import copy
    e = ALL[n][1]; v = copy.deepcopy(e['new']); p = e['path']; out = [copy.deepcopy(v)]
    for m in range(n + 1, len(ALL)):
        f = ALL[m][1]
        if f['file'] != e['file'] or len(f['path']) <= len(p) or f['path'][:len(p)] != p: continue
        cur = v
        try:
            for k in f['path'][len(p):-1]: cur = cur[k]
            last = f['path'][-1]
            if f.get('op') == 'add':
                if isinstance(cur, list) and last == len(cur): cur.append(f['new'])
                elif isinstance(cur, dict) and last not in cur: cur[last] = f['new']
            elif canon(cur[last]) == canon(f['old']): cur[last] = f['new']
        except (KeyError, IndexError, TypeError): pass
        out.append(copy.deepcopy(v))
    return out if stages else v

files = {}
stats = {'applied': 0, 'done': 0, 'conflict': 0}
for n, (ff, e) in enumerate(ALL):
    if True:
        fn = e['file']
        if fn not in files: files[fn] = list(load(fn))
        s, i, j, obj = files[fn]
        cur = obj
        if e.get('op') == 'add':
            try:
                for k in e['path'][:-1]: cur = cur[k]
            except (KeyError, IndexError, TypeError):
                print('MISSING', os.path.basename(ff), fn, e['path']); stats['conflict'] += 1; continue
            last = e['path'][-1]
            have = (last in cur) if isinstance(cur, dict) else (isinstance(last, int) and last < len(cur))
            if have:
                if canon(cur[last]) == canon(e['new']) or any(canon(cur[last]) == canon(x) for x in replayed(n, True)) \
                   or any(canon(cur[last]) == canon(ALL[m][1]['new']) for m in LATER[(e['file'], json.dumps(e['path']))] if m > n):
                    stats['done'] += 1
                else: print('CONFLICT(add)', os.path.basename(ff), fn, e['path']); stats['conflict'] += 1
                continue
            e = dict(e, new=canon(e['new']))
            if isinstance(cur, list):
                if last != len(cur): print('CONFLICT(add index)', os.path.basename(ff), fn, e['path']); stats['conflict'] += 1; continue
                cur.append(e['new'])
            else: cur[last] = e['new']
            stats['applied'] += 1; continue
        try:
            for k in e['path'][:-1]: cur = cur[k]
            last = e['path'][-1]; val = cur[last]
        except (KeyError, IndexError, TypeError):
            print('MISSING', os.path.basename(ff), fn, e['path']); stats['conflict'] += 1; continue
        if canon(val) == canon(e['new']):
            if val != canon(val): cur[last] = canon(val); stats['applied'] += 1
            else: stats['done'] += 1
            continue
        if any(canon(val) == canon(ALL[m][1]['new']) for m in LATER[(fn, json.dumps(e['path']))] if m > n) \
           or any(canon(val) == canon(x) for x in replayed(n, True)):
            stats['done'] += 1; continue
        if canon(val) != canon(e['old']):
            print('CONFLICT', os.path.basename(ff), fn, e['path'], '\n  now:', str(val)[:160], '\n  old:', str(e['old'])[:160]); stats['conflict'] += 1; continue
        cur[last] = canon(e['new']); stats['applied'] += 1
for fn in ('data/orations.js', 'data/addiv.js', 'data/memoriae.js', 'data/readings33.js'):
    if fn not in files: files[fn] = list(load(fn))
for fn in list(files):
    s, i, j, obj = files[fn]; files[fn][3] = canon(obj)
for fn, (s, i, j, obj) in files.items():
    new = s[:i] + dump(obj, s[i:j]) + s[j:]
    if new != s and not dry:
        open(os.path.join(ROOT, fn), 'w', encoding='utf8').write(new)
print(stats, '(dry run)' if dry else '')
