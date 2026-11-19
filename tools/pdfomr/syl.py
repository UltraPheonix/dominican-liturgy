import re, unicodedata
V='aeiouyáéíóúýæœǽàèìòùäëïöüAEIOUYÁÉÍÓÚÆŒǼ'
def base(c): return unicodedata.normalize('NFD',c)[0].lower()
def isv(w,i):
    c=w[i]
    if c not in V: return False
    # u after q/g(u+vowel) consonantal
    if base(c)=='u' and i>0 and base(w[i-1]) in 'q' : return False
    if base(c)=='u' and i>0 and base(w[i-1])=='g' and i>1 and base(w[i-2])=='n' and i+1<len(w) and w[i+1] in V: return False
    # i initial before vowel (iam, ius) consonantal; j
    if base(c)=='i' and i==0 and len(w)>1 and w[1] in V: return False
    if base(c)=='i' and i>0 and w[i-1] in V and i+1<len(w) and w[i+1] in V: return False
    return True
def syllables(w):
    """returns list of start indices of syllables in word w"""
    n=len(w); vs=[]
    i=0
    while i<n:
        if isv(w,i):
            j=i+1
            # diphthongs ae oe au (not with diaeresis)
            if j<n and isv(w,j) and (base(w[i])+base(w[j])) in ('ae','oe','au','ei') and not (base(w[i])+base(w[j])=='ei'):
                j+=1
            vs.append((i,j)); i=j
        else: i+=1
    if len(vs)<=1: return [0]
    starts=[0]
    for k in range(1,len(vs)):
        a=vs[k-1][1]; b=vs[k][0]   # consonants between
        starts.append(a)   # liturgical hyphenation: the whole consonant group goes with the next vowel
    return starts
if __name__=='__main__':
    for w in ['Præcéptis','salutáribus','móniti','divína','institutióne','formáti','audémus','dícere','sanctificétur','Advéniat','quotidiánum','dimíttimus','tentatiónem','ómnia','sǽcula','sæculórum','Ecclésiæ','quǽsumus','sanguinem','lingua']:
        st=syllables(w); print(w, '-'.join(w[a:b] for a,b in zip(st, st[1:]+[len(w)])))
