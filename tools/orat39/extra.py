"""Orations for Masses whose prayers the segmenter could not take whole (incomplete, "ut in Commune", "ut in festo ...",
supplements). The Latin in extra_final.json was read from the Missale O.P. 1939 page images (accented as printed);
here only the short conclusions are written out, the same way build_or.py does for the main 103.
English: en_extra in en_final.json style (body only). Output: extra_or.json in new_or.json format."""
import json, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
import importlib.util
spec = importlib.util.spec_from_file_location('b', 'build_or.py'); src = open('build_or.py').read()
# reuse the conclusion constants only (do not run build_or's main)
NS = {}
exec(src.split('def fix_spaced')[0].split('from spellchecker')[0] + '\n' + '\n'.join(l for l in src.split('\n') if re.match(r'^(PD|PDS|PE|QV|QT|EPD|EPDS|EPE|EQV|EQT) = ', l)), NS)
X = json.load(open('extra_final.json'))
E = json.load(open('en_final.json'))
def concl(t):
    t = t.strip().replace('eúmdem', 'eúndem')
    m = re.search(r'(Per Dóminum|Per eúndem|Qui vivis|Qui vivit|Qui tecum|qui tecum)[^.]*\.$', t)
    if not m: raise SystemExit('no conclusion: ' + t[-60:])
    s = m.group(1); body = t[:m.start()]
    if s == 'Per Dóminum': c, e = NS['PD'], NS['EPD']
    elif s == 'Per eúndem': c, e = NS['PE'], NS['EPE']
    elif s == 'Qui vivis': c, e = NS['QV'], NS['EQV']
    else: c, e = NS['QT'], NS['EQT']
    if s == 'Qui vivit': return body + 'Qui vivit et regnat cum Deo Patre in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum.', 'Who lives and reigns with God the Father in the unity of the Holy Spirit, God, world without end.'
    if s == 'qui tecum': return body + 'qui tecum vivit et regnat in unitáte Spíritus Sancti Deus per ómnia sǽcula sæculórum.', e
    return body + c, e
out = {}
for k, d in X.items():
    out[k] = {'page': d['p']}
    for kind in ('or', 'se', 'pc'):
        la, ec = concl(d[kind])
        b0 = E[k][kind].rstrip(' .;:,') if k in E and kind in E[k] else ''
        en = (b0 + '; ' + ec[0].lower() + ec[1:]) if b0 else ''
        out[k][kind] = [la, en]
json.dump(out, open('extra_or.json', 'w'), ensure_ascii=False, indent=0)
print(len(out), 'Masses;', sum(1 for v in out.values() for kind in ('or', 'se', 'pc') if not v[kind][1]), 'prayers without English')
