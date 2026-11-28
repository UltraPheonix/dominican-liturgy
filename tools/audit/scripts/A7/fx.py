"""Append fix entries to tools/audit/fixes/A7.json. 'old' = the value in the simulated post-apply state (state.py ZZZ),
which already includes A7's own earlier entries; an existing identical entry (same path and new) is not added twice."""
import json, os, subprocess
ROOT = '/home/claude/dominican-liturgy'; FX = ROOT + '/tools/audit/fixes/A7.json'; ST = '/tmp/A7/state/'
def refresh(): subprocess.run(['python3', ROOT + '/tools/audit/scripts/A7/state.py', 'ZZZ'], capture_output=True)
def load(): return json.load(open(FX, encoding='utf8')) if os.path.exists(FX) else []
_cache = {}
def state(fn):
    b = os.path.basename(fn).replace('.js', '.json')
    if b not in _cache: _cache[b] = json.load(open(ST + b, encoding='utf8'))
    return _cache[b]
def get(fn, path):
    v = state(fn)
    for k in path: v = v[k]
    return v
def add(fn, path, new, src, why, op=None):
    E = load()
    for e in E:
        if e['path'] == path and e['file'] == fn and e['new'] == new: return False
    if op == 'add': old = None
    else:
        old = get(fn, path)
        if old == new: return False
    e = {'file': fn, 'path': path, 'old': old, 'new': new, 'src': src, 'why': why}
    if op: e['op'] = op
    E.append(e)
    json.dump(E, open(FX, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    return True
