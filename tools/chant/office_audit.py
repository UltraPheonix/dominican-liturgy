"""Office chant table audit (2026-11-25).
Every melody in data/chant/office.json must be Dominican and must carry the text it is used for:
 1. where the Antiphonarium O.P. 1933 (GregoBase source 11) has the same text, its melody is used (written to data/chant/op/<id>.gabc);
 2. melodies from Roman books (Liber Usualis = source 3/48, RC-*) without a Dominican equivalent are dropped (the text is then
    said/sung to the tone, not to a Roman melody);
 3. OMR transcriptions (Ta*, OP33-*) whose words differ from the text (truncated, other verse) are dropped.
Writes tools/chant/office_audit.txt (what changed). Run: python3 tools/chant/office_audit.py"""
import json, re, sqlite3, unicodedata, os, difflib
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
MAP = os.path.join(R, 'data/chant/office.json'); OP = os.path.join(R, 'data/chant/op')
M = json.load(open(MAP))
c = sqlite3.connect('file:%s?mode=ro' % os.path.join(R, 'tools/gregobase/gb.sqlite'), uri=True)
def norm(t):
    t = t.split('%%')[-1]
    t = re.sub(r'<i>.*?</i>', '', t); t = re.sub(r'<[^>]*>', '', t); t = re.sub(r'\([^)]*\)', '', t)
    t = ''.join(ch for ch in unicodedata.normalize('NFD', t.lower()) if unicodedata.category(ch) != 'Mn')
    t = t.replace('æ', 'ae').replace('œ', 'oe').replace('j', 'i').replace('y', 'i')
    t = re.sub(r'e\s*u\s*o\s*u\s*a\s*e\.?\s*$', '', t.strip())
    return re.sub(r'[^a-z]', '', t)
src = {}
for cid, s in c.execute('select chant_id, source from gregobase_chant_sources'): src.setdefault(cid, set()).add(s)
OPSRC = {11, 12, 13, 14, 20, 21, 35, 36}
G11 = {}
for gid, g, part, mode in c.execute("select g.id, g.gabc, g.\"office-part\", g.mode from gregobase_chants g join gregobase_chant_sources s on s.chant_id=g.id where s.source=11"):
    try: g = json.loads(g)
    except Exception: continue
    G11.setdefault(norm(g), []).append((gid, g, part, mode))
def find11(kk):
    for t, v in G11.items():
        if t.startswith(kk) and len(t) - len(kk) < 40: return v[0]
    return None
log = []; n = {'gb11': 0, 'drop-roman': 0, 'drop-text': 0}
for k, v in list(M.items()):
    f = v[0]; kk = re.sub(r'^(hy|rb|re|vs|an)', '', k).replace('y', 'i').replace('j', 'i')
    roman = (f.isdigit() and not (src.get(int(f), set()) & OPSRC)) or f.startswith('RC-')
    path = os.path.join(OP, f + '.gabc'); t = norm(open(path, encoding='utf8').read()) if os.path.exists(path) else ''
    omr = not f.isdigit() and not f.startswith('RC-') and not f.startswith('C49')
    if omr:   # an OMR transcription: its words must be the text's (not cut short, not another verse)
        ok = bool(t) and (t.startswith(kk) or (len(t) >= 25 and kk.startswith(t)) or difflib.SequenceMatcher(None, t[:len(kk)], kk).ratio() >= 0.9 and len(t) >= len(kk) - 2)
    else:     # a Dominican book (GregoBase): its own words are the Dominican text, even where the Office text (Roman) differs
        ok = bool(t)
    if roman or not ok or omr:   # the Antiphonarium 1933 (GregoBase) wins over an OMR transcription of the same piece
        hit = find11(kk)
        if omr and ok and not hit: continue
        if hit:
            gid, g, part, mode = hit
            out = os.path.join(OP, '%d.gabc' % gid)
            if not os.path.exists(out): open(out, 'w', encoding='utf8').write(re.sub(r'<i>\s*Ant\.\s*</i>\(\)\s*', '', g).replace('(c3) () ', '(c3) ').replace('(c4) () ', '(c4) ').strip() + '\n')
            M[k] = [str(gid), str(mode or v[1]), v[2], v[3], '']; n['gb11'] += 1; log.append('1933  %-50s %s -> %s' % (k[:50], f, gid)); continue
        del M[k]; n['drop-roman' if roman else 'drop-text'] += 1
        log.append('drop  %-50s %s (%s)' % (k[:50], f, 'Roman book' if roman else 'words differ: ' + t[:50]))
json.dump(M, open(MAP, 'w'), ensure_ascii=False, separators=(',', ':'))
open(os.path.join(R, 'tools/chant/office_audit.txt'), 'w').write('\n'.join(log) + '\n')
print(n, len(M))
