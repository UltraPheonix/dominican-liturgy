import json,sys
from PIL import Image, ImageDraw, ImageFont
G=json.load(open(sys.argv[1])); want=sys.argv[2]; out=sys.argv[3]; only=sys.argv[4] if len(sys.argv)>4 else None
items=[(k,v) for k,v in G.items() if k.startswith(want) and (not only or v['ch'] in only)]
items.sort(key=lambda kv:kv[1]['ch'])
S=0.25; W,H=260,330; cols=8
img=Image.new('L',(cols*W,((len(items)+cols-1)//cols)*H),255); dr=ImageDraw.Draw(img)
fnt=ImageFont.load_default(size=22)
for i,(k,v) in enumerate(items):
    ox,oy=(i%cols)*W+60,(i//cols)*H+260
    for y in (5,173,341,509): dr.line([(ox-50,oy-y*S),(ox+200,oy-y*S)],fill=200)
    for p in v['polys']:
        if len(p)>2: dr.polygon([(ox+x*S,oy-y*S) for x,y in p],fill=0)
    dr.text(((i%cols)*W+5,(i//cols)*H+5),f"{v['ch']} {ord(v['ch'])}",fill=0,font=fnt)
img.save(out)
