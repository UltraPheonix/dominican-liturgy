"""Apply tools/m33/propers_fix.json (propers checked on the Missale O.P. 1933 page images) to data/masses.js.
Idempotent. Usage: python3 tools/m33/propers_apply.py [path/to/masses.js]"""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__))
def apply(data):
    fx = json.load(open(os.path.join(H, 'propers_fix.json'), encoding='utf8'))
    n = 0
    for cid, c in fx.get('_add_chants', {}).items(): data['chants'].setdefault(cid, c)
    for cid, t in fx.get('_trans', {}).items(): data.setdefault('trans', {})[cid] = t
    for k, v in fx.items():
        if k.startswith('_') or k not in data['masses']: continue
        parts = data['masses'][k].setdefault('parts', {})
        tag = v.get('p33', v.get('p39'))
        for p, ids in v.items():
            if p in ('p33', 'p39') or p.startswith('_'): continue
            if p == 'asc_al':   # the second Alleluia Tempore Ascensionis
                data['masses'][k].setdefault('season', {}).setdefault('asc', {})['al'] = [{'id': ids, 'm39': tag}]; n += 1; continue
            if p == 'pasch':   # Introit, Offertory, Communion tempore Paschali (Commune Martyrum tempore Paschali)
                for q, l in ids.items(): data['masses'][k].setdefault('season', {}).setdefault('pasch', {})[q] = [{'id': i, 'm39': tag} for i in l]
                n += 1; continue
            if p == 'lent_tr':   # Tract 'infra Septuagesimam' (the Alleluia is then dropped by the app)
                data['masses'][k].setdefault('season', {}).setdefault('lent', {})['tr'] = [{'id': i, 'm33': tag} for i in ids]; n += 1; continue
            if p == 'pasch_al':   # the two Alleluias of Paschaltide (gradual dropped)
                data['masses'][k].setdefault('season', {}).setdefault('pasch', {})['al'] = [{'id': i, 'm39': tag} for i in ids]; n += 1; continue
            if not ids: parts.pop(p, None); n += 1; continue
            parts[p] = [dict({'id': i, 'm33': tag}, **({'roman': True} if data['chants'].get(str(i), {}).get('roman') else {})) for i in ids]; n += 1
            for i in ids: assert str(i) in data['chants'], (k, p, i)
        if 'req' in data['masses'][k]: data['masses'][k]['req'] = [p for p in data['masses'][k]['req'] if p in parts]
    return n
if __name__ == '__main__':
    F = sys.argv[1] if len(sys.argv) > 1 else os.path.join(H, '../../data/masses.js')
    s = open(F, encoding='utf8').read(); head, js = s.split('var DOMINICAN = ', 1)
    data = json.loads(js.rstrip().rstrip(';'))
    print(apply(data), 'parts set from propers_fix.json')
    open(F, 'w', encoding='utf8').write(head + 'var DOMINICAN = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
