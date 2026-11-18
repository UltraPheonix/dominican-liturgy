import json, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
S=4; X0=-80; Y0=-360; W=260; H=300   # 1px = 4 font units
def raster(polys):
    img=Image.new('1',(W,H),0); dr=ImageDraw.Draw(img)
    for p in polys:
        if len(p)>2: dr.polygon([((x-X0)/S,(H-1)-(y-Y0)/S) for x,y in p],fill=1)
    return np.array(img,dtype=bool)
def bb(p): xs=[a for a,b in p]; ys=[b for a,b in p]; return min(xs),min(ys),max(xs),max(ys)
def comps(polys):
    keep=[p for p in polys if len(p)>2 and not (bb(p)[3]-bb(p)[1]<=12)]
    a=raster(keep)
    o=ndimage.binary_opening(a,structure=np.ones((7,7)))   # 28 units
    lab,n=ndimage.label(o); out=[]
    for i,sl in enumerate(ndimage.find_objects(lab)):
        ys,xs=sl; m=(lab[sl]==i+1)
        x0=xs.start*S+X0; x1=xs.stop*S+X0; y1=(H-ys.start)*S+Y0; y0=(H-ys.stop)*S+Y0
        out.append({'x0':x0,'x1':x1,'y0':y0,'y1':y1,'fill':round(float(m.mean()),2),
                    'lt':float(np.mean(np.where(m[:, :3].any(1))[0])) if m[:, :3].any() else None})
    # thin tall strokes (stems, bars) from the raw raster
    thin=a & ~ndimage.binary_dilation(o,structure=np.ones((3,3)))
    tl,tn=ndimage.label(thin); strokes=[]
    for i,sl in enumerate(ndimage.find_objects(tl)):
        ys,xs=sl; h=(ys.stop-ys.start)*S; w=(xs.stop-xs.start)*S
        if h>=60: strokes.append({'x0':xs.start*S+X0,'x1':xs.stop*S+X0,'y0':(H-ys.stop)*S+Y0,'y1':(H-ys.start)*S+Y0})
    holes=0
    for p in keep:
        for q in keep:
            if p is not q:
                a1=bb(p); a2=bb(q)
                if a2[0]>a1[0] and a2[2]<a1[2] and a2[1]>a1[1] and a2[3]<a1[3] and a2[2]-a2[0]>30: holes+=1
    return out, strokes, holes
if __name__=='__main__':
    import sys
    G=json.load(open('glyphs_all.json'))
    for k,v in sorted(G.items(), key=lambda kv: kv[1]['ch']):
        if not k.startswith(sys.argv[1]): continue
        c,s,h=comps(v['polys'])
        print(repr(v['ch']), ' '.join(f"[{d['x0']},{d['y0']}-{d['x1']},{d['y1']} f{d['fill']}]" for d in c), 'S:'+' '.join(f"{d['x0']},{d['y0']}-{d['y1']}" for d in s), 'H' if h else '')
