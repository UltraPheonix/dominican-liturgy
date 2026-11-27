import sys,json,re
sys.path.insert(0,'/tmp/A2/new')
from draft import text
V='/tmp/A2/vig.txt'
def norm(s):
    s=re.sub(r'\s+([:;,.?!])',r'\1',s)
    s=re.sub(r'\s+',' ',s).strip()
    return s
def fix(s,subs):
    for a,b in subs:
        assert a in s,(a,s[:80]); s=s.replace(a,b)
    assert '¤' not in s and '@@' not in s, s
    return s
gen=fix(norm(text(V,148,233)),[('IN diébus','In diébus'),('visiónis; atque','visiónis: atque'),('Ígitur','Igitur'),
    ('gládium, @@PAGE¤ 158 240 In Vigilia Pentecostes ut','gládium, ut'),('httore¤','líttore')])
deu=fix(norm(text(V,251,293)),[('IN diébus','In diébus'),('a it:','ait:'),('com plevit¤:','complévit:'),('fcbderis¤','fœderis'),('ccetu¤','cœtu'),('Israel','Israël')])
isa=fix(norm(text(V,321,356)),[('ejus Praed¤. — 16 Pentecostes 241 in','ejus in'),('Israel','Israël')])
bar=fix(norm(text(V,379,472)),[('AUDI','Audi'),('intelléctus: @@PAGE¤ 159 242 In Vigilia Pentecostes ut','intelléctus: ut'),('qu«','quæ'),('e s t:','est:'),('Ádsumus','Adsumus'),('Israel','Israël')])
act=fix(norm(text(V,535,568)),[('IN diébus','In diébus'),('discípulos: dixítque ad eos: Pentecostes Si','discípulos: dixítque ad eos: Si'),('a it:','ait:')])
gos=fix(norm(text(V,587,614)),[('IN illo','In illo'),('Et @@PAGE¤ 160 244 In Vigilia Pentecostes ego','Et ego'),('e a:','ea:')])
def dr(*parts): return ' '.join(parts)
from douay import dr
EN={}
EN['gen']=dr('Genesis',22,1,19,[('After these things, God tempted','In those days: God tempted')])
EN['deu']=dr('Deuteronomium',31,22,30,[('Moses therefore wrote','In those days: Moses wrote'),('finished it: He commanded','finished it: he commanded'),('the Lord. saying','the Lord, saying'),('stiff neck, While','stiff neck. While'),('even to the end,','even to the end.')])
EN['isa']=dr('Isaias',4,1,6,[('And in that day seven','In that day seven')])
EN['bar']=dr('Baruch',3,9,38)
EN['act']=dr('Actus Apostolorum',19,1,8,[('And it came to pass, while','In those days: It came to pass, while')])
EN['gos']='At that time: Jesus said to his disciples: '+dr('Joannes',14,15,21)
R=[
 {"type":"Lesson","ref":"Genesis 22: 1-19","title":"Lectio prima.","title_en":"The First Lesson.","la":gen,"en":EN['gen'],"p33":316},
 {"type":"Lesson","ref":"Deuteronomium 31: 22-30","title":"Lectio secunda.","title_en":"The Second Lesson.","la":deu,"en":EN['deu'],"p33":317},
 {"type":"Lesson","ref":"Isaias 4: 1-6","title":"Lectio tertia.","title_en":"The Third Lesson.","la":isa,"en":EN['isa'],"p33":318},
 {"type":"Lesson","ref":"Baruch 3: 9-38","title":"Lectio quarta.","title_en":"The Fourth Lesson.","la":bar,"en":EN['bar'],"p33":318},
 {"type":"Epistle","ref":"Actus Apostolorum 19: 1-8","title":"Léctio Actuum Apostolórum.","title_en":"Lesson from the Acts of the Apostles.","la":act,"en":EN['act'],"p33":319},
 {"type":"Gospel","ref":"Joannes 14: 15-21","title":"Sequéntia sancti Evangélii secúndum Joánnem.","title_en":"Continuation of the holy Gospel according to John.","la":gos,"en":EN['gos'],"p33":320},
]
json.dump(R,open('/tmp/A2/new/pasc6s_readings.json','w'),ensure_ascii=False,indent=1)
for r in R: print('##',r['title'],r['ref'],'\n',r['la'],'\n')
