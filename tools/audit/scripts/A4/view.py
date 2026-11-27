import sys,subprocess,os
from PIL import Image
# usage: view.py PDFPAGE [L|R|LT|LB|RT|RB|Q1..Q8] [dpi]
pdf=int(sys.argv[1]); part=sys.argv[2] if len(sys.argv)>2 else 'L'; dpi=int(sys.argv[3]) if len(sys.argv)>3 else 160
fn=f'/tmp/A4/v/p{pdf}_{dpi}.png'
if not os.path.exists(fn):
    subprocess.run(['pdftoppm','-r',str(dpi),'-f',str(pdf),'-l',str(pdf),'-png','-singlefile','/home/claude/dl/missal/M39.pdf',fn[:-4]],check=True)
im=Image.open(fn); W,H=im.size
side=part[0]; x0,x1=(0,W//2+20) if side=='L' else (W//2-20,W)
y0,y1=0,H
if len(part)>1:
    v=part[1:]
    if v=='T': y1=H//2+40
    elif v=='B': y0=H//2-40
    elif v in '123': n=int(v); y0=max(0,(n-1)*H//3-30); y1=min(H,n*H//3+30)
out=f'/tmp/A4/v/c{pdf}{part}.png'; im.crop((x0,y0,x1,y1)).save(out); print(out, im.size)
