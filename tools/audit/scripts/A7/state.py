#!/usr/bin/env python3
"""state.py [UPTO] : simulate apply_fixes.py in memory over the fixes files that sort before UPTO (default 'A7.json'),
and dump the resulting data objects (canon()'d) to /tmp/A7/state/<name>.json. Writes nothing under the repo."""
import sys, os, json, glob, io, contextlib
ROOT = '/home/claude/dominican-liturgy'
upto = sys.argv[1] if len(sys.argv) > 1 else 'A7.json'
src = open(ROOT + '/tools/audit/apply_fixes.py', encoding='utf8').read()
src = src.replace("sorted(glob.glob(os.path.join(ROOT, 'tools/audit/fixes/*.json')))",
                  "[f for f in sorted(glob.glob(os.path.join(ROOT, 'tools/audit/fixes/*.json'))) if os.path.basename(f) < UPTO]")
src = src.replace("open(os.path.join(ROOT, fn), 'w', encoding='utf8').write(new)", "pass")
g = {'__file__': ROOT + '/tools/audit/apply_fixes.py', '__name__': 'sim', 'UPTO': upto}
sys.argv = ['x', '--dry']
buf = io.StringIO()
with contextlib.redirect_stdout(buf): exec(compile(src, 'apply_fixes_sim', 'exec'), g)
print(buf.getvalue()[-300:])
for fn, (s, i, j, obj) in g['files'].items():
    json.dump(obj, open('/tmp/A7/state/' + os.path.basename(fn).replace('.js', '.json'), 'w'), ensure_ascii=False)
print('dumped', list(g['files']))
