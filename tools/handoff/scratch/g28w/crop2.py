# crop2.py PNM X0 X1 LLEFT LRIGHT OUT [SEGW] [SC]  (L* = 4 line ys at x0 and at x1)
import sys, subprocess
pnm,x0,x1,LA,LB,out=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4],sys.argv[5],sys.argv[6]
segw=int(sys.argv[7]) if len(sys.argv)>7 else 1000
sc=sys.argv[8] if len(sys.argv)>8 else '1.15'
A=[float(v) for v in LA.split(',')]; B=[float(v) for v in LB.split(',')]
xs=x0;i=0
while xs<x1:
    xe=min(x1,xs+segw); t=((xs+xe)/2-x0)/max(1,(x1-x0))
    L=','.join('%d'%round(a+(b-a)*t) for a,b in zip(A,B))
    r=subprocess.run(['python3','/tmp/g28w/crop.py',pnm,str(xs),str(xe),L,'%s%d'%(out,i),str(segw),sc],capture_output=True,text=True)
    print(i,xs,xe,L,r.stdout.strip(),r.stderr[-300:])
    subprocess.run(['mv','%s%d_0.png'%(out,i),'%s_%d.png'%(out,i)])
    xs=xe;i+=1
