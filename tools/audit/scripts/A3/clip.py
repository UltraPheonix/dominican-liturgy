# python3 clip.py PDFPAGE(1-based) x0 y0 x1 y1 out [zoom]  (coords in pt, page 854x679)
import fitz,sys
D=fitz.open('/home/claude/dl/missal/M39.pdf'); a=sys.argv
pg=D[int(a[1])-1]; z=float(a[7]) if len(a)>7 else 4
pg.get_pixmap(matrix=fitz.Matrix(z,z),clip=fitz.Rect(*map(float,a[2:6]))).save(a[6])
