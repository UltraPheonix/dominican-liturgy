import sys; sys.path.insert(0,'/tmp/A5')
from lib import *
def c(k,i,needle,w=40,field='la'):
    s=R[k][i][field] if isinstance(i,int) else O[k][i][0]
    j=s.find(needle)
    print(k,i,repr(s[max(0,j-w):j+len(needle)+w]) if j>=0 else 'NOTFOUND '+needle)
def tail(k,i,n=120): print(k,i,'...',R[k][i]['la'][-n:])
def head(k,i,n=120): print(k,i,R[k][i]['title'],'|',R[k][i]['la'][:n])
