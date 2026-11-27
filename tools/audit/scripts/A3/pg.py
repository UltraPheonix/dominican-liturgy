# render pdf page (1-based) column halves: python3 pg.py N [zoom]  -> /tmp/A3/pN_L.png, pN_R.png (split top/bottom too)
import fitz,sys
D=fitz.open('/home/claude/dl/missal/M39.pdf')
n=int(sys.argv[1]); z=float(sys.argv[2]) if len(sys.argv)>2 else 2.2
pg=D[n-1]; r=pg.rect
for side,(x0,x1) in (('L',(0,r.width/2+8)),('R',(r.width/2-8,r.width))):
    for part,(y0,y1) in (('a',(0,r.height*0.52)),('b',(r.height*0.48,r.height))):
        pix=pg.get_pixmap(matrix=fitz.Matrix(z,z),clip=fitz.Rect(x0,y0,x1,y1))
        pix.save('/tmp/A3/p%d_%s%s.png'%(n,side,part))
print(r)
