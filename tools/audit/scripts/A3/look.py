# python3 look.py IDX(0-based fitz page = @@PAGE) "phrase" [up_pt] [down_pt] [out] -> crop of the column around phrase
import fitz,sys,warnings
D=fitz.open('/home/claude/dl/missal/M39.pdf')
a=sys.argv; ph=a[2]
for k in (int(a[1]),int(a[1])-1,int(a[1])+1,int(a[1])-2,int(a[1])+2):
    pg=D[k]; rs=pg.search_for(ph)
    if rs: break
up=float(a[3]) if len(a)>3 else 40; dn=float(a[4]) if len(a)>4 else 60
out=a[5] if len(a)>5 else '/tmp/A3/look.png'
if not rs: print('NOT FOUND'); sys.exit()
r=rs[0]; W=pg.rect.width
x0,x1=(0,W/2+5) if r.x0<W/2 else (W/2-5,W)
pg.get_pixmap(matrix=fitz.Matrix(3,3),clip=fitz.Rect(x0,max(0,r.y0-up),x1,min(pg.rect.height,r.y1+dn))).save(out)
print('fitz',k,len(rs),'hits; first',r)
