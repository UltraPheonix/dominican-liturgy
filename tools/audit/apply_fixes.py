#!/usr/bin/env python3
"""Apply the Mass-text audit fixes (tools/audit/fixes/*.json) to the live data files. Idempotent: safe to run
any number of times, and must be run again after any rebuild of data/orations.js, readings33.js, masses.js,
addiv.js or memoriae.js.

A fixes file is a JSON list of entries:
  {"file": "data/orations.js", "path": ["Adv1", "or", 0], "old": "<exact current value>", "new": "<corrected value>",
   "src": "M39 p. 1 (pdf 33)", "why": "punctuation as printed"}
"path" navigates the JSON object of the file (keys and list indices). "old" must equal the current value (else the
entry is reported as CONFLICT and skipped); if the value already equals "new" it is skipped as done.
Values may be strings or any JSON value. Usage: python3 tools/audit/apply_fixes.py [--dry]
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

files = {}
stats = {'applied': 0, 'done': 0, 'conflict': 0}
for ff in sorted(glob.glob(os.path.join(ROOT, 'tools/audit/fixes/*.json'))):
    for e in json.load(open(ff, encoding='utf8')):
        fn = e['file']
        if fn not in files: files[fn] = list(load(fn))
        s, i, j, obj = files[fn]
        cur = obj
        try:
            for k in e['path'][:-1]: cur = cur[k]
            last = e['path'][-1]; val = cur[last]
        except (KeyError, IndexError, TypeError):
            print('MISSING', os.path.basename(ff), fn, e['path']); stats['conflict'] += 1; continue
        if val == e['new']: stats['done'] += 1; continue
        if val != e['old']:
            print('CONFLICT', os.path.basename(ff), fn, e['path'], '\n  now:', str(val)[:160], '\n  old:', str(e['old'])[:160]); stats['conflict'] += 1; continue
        cur[last] = e['new']; stats['applied'] += 1
for fn, (s, i, j, obj) in files.items():
    new = s[:i] + dump(obj, s[i:j]) + s[j:]
    if new != s and not dry:
        open(os.path.join(ROOT, fn), 'w', encoding='utf8').write(new)
print(stats, '(dry run)' if dry else '')
