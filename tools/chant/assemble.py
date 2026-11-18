# Items (decode.py) -> chant pieces with GABC.
import json, re, sys, unicodedata
L='abcdefghijklm'
VOW='aeiouyæœáéíóúýǽëAEIOUYÆŒÁÉÍÓÚÝǼË'
ONSET={'bl','br','cl','cr','dr','fl','fr','gl','gr','pl','pr','tr','ch','ph','th','gn','st','sc','sp','ct','pt','mn','ps','qu','gu'}
def base(c): return unicodedata.normalize('NFD',c)[0].lower()
def isv(w,i):
    c=w[i]
    if c not in VOW: return False
    b=base(c)
    if b in 'iu':
        prev=base(w[i-1]) if i>0 else ''
        nxt=w[i+1] if i+1<len(w) else ''
        if b=='u' and prev in ('q','g') and nxt and nxt in VOW: return False     # qu, gu+vowel
        if b=='i' and nxt and nxt in VOW and (i==0 or (prev and w[i-1] in VOW)): return False   # consonantal i
    return True
def syllabify(w):
    """Split a Latin word (letters only, possibly with punctuation) into syllables."""
    idx=[i for i in range(len(w)) if isv(w,i)]
    # diphthongs ae oe au: merge
    nuc=[]
    for i in idx:
        if nuc and nuc[-1][-1]==i-1 and base(w[i-1])+base(w[i]) in ('ae','oe','au'): nuc[-1].append(i)
        else: nuc.append([i])
    if len(nuc)<=1: return [w]
    cuts=[]
    for a,b in zip(nuc,nuc[1:]):
        s,e=a[-1]+1,b[0]        # consonants w[s:e]
        cons=''.join(base(c) for c in w[s:e] if c.isalpha())
        n=e-s
        if n==0: cuts.append(e)
        elif n==1: cuts.append(s)
        else:
            if cons[-2:] in ONSET: cuts.append(e-2)
            else: cuts.append(e-1)
    out=[]; st=0
    for c in cuts: out.append(w[st:c]); st=c
    out.append(w[st:]); return [x for x in out if x]
def tokens(lyr):
    """Lyric chars -> list of (text, x, word_end, italic)."""
    toks=[]; cur=None; last=None
    for c in lyr:
        ch=c['c']
        gap=last is not None and c['x']-last>2.2
        if ch.isspace() or gap:
            if cur: toks.append(cur); cur=None
            if ch.isspace(): last=c['x1']; continue
        if cur is None: cur={'t':'','x':c['x'],'xs':[],'x1s':[],'it':'Italic' in c['font']}
        cur['t']+=ch; cur['xs'].append(c['x']); cur['x1s'].append(c['x1']); last=c['x1']
    if cur: toks.append(cur)
    syl=[]
    for t in toks:
        txt=t['t']; xs=t['xs']; x1s=t['x1s']; cont=txt.endswith('-')
        if t['it'] or not any(ch.isalpha() for ch in txt):
            syl.append({'t':txt,'x':xs[0],'end':True,'rub':True}); continue
        # fragments at hyphens
        frags=[]; st=0
        for i,ch in enumerate(txt):
            if ch=='-':
                if i>st: frags.append((st,i))
                st=i+1
        if st<len(txt): frags.append((st,len(txt)))
        for fi,(a,b) in enumerate(frags):
            word=txt[a:b]
            # leading/trailing punctuation stays with the syllable
            m=re.match(r'^([^A-Za-zÀ-ÿĀ-žǼǽ]*)(.*?)([^A-Za-zÀ-ÿĀ-žǼǽ]*)$',word)
            pre,core,post=m.groups()
            parts=syllabify(core) if core else ['']
            pos=a+len(pre)
            for pi,pt in enumerate(parts):
                text=(pre if pi==0 else '')+pt+(post if pi==len(parts)-1 else '')
                xi=xs[min(pos,len(xs)-1)] if pi>0 else xs[a]
                # anchor: the centre of the syllable's vowel
                vi=next((k for k,ch in enumerate(pt) if ch in VOW),0)
                k=min(pos+vi,len(xs)-1); va=(xs[k]+x1s[k])/2
                syl.append({'t':text,'x':xi,'va':va,'end':(fi==len(frags)-1 and pi==len(parts)-1 and not cont),'ws':(fi==0 and pi==0) or False})
                pos+=len(pt)
    return syl
def notestr(n):
    p=n['p']+3
    if p<0 or p>12: p=max(0,min(12,p))
    c=L[p]
    if n['s']=='rh': return c.upper()
    if n['s']=='q': return c+'w'
    if n['s']=='small': return c+'~'
    if n['s']=='hollow': c+='r'
    elif n.get('v'): c+='v'
    if n.get('acc'): c+="'"
    return c
def system_gabc(s, prevclef):
    els=[e for e in s['els'] if e['k']!='acc']
    for a in [e for e in s['els'] if e['k']=='acc']:
        ns=[e for e in els if e['k']=='n']
        if ns:
            n=min(ns,key=lambda e:abs(e['x']-a['x'])); n['acc']=1
    # drop the custos (a small note ending the line)
    while els and els[-1]['k']=='n' and els[-1]['s']=='small': els.pop()
    size=s['size']; syl=tokens(s['lyr'])
    out=[]; clef=None
    # group consecutive notes into neumes
    groups=[]
    for e in els:
        if e['k']=='clef':
            if clef is None: clef=e['c']
            continue
        if e['k']=='n':
            if groups and groups[-1]['k']=='g' and e['x']-groups[-1]['lx']<0.13*size:
                groups[-1]['n'].append(e); groups[-1]['lx']=e['x']; continue
            if groups and groups[-1]['k']=='flat': fl=groups.pop()['p']
            else: fl=None
            groups.append({'k':'g','x':e['x'],'lx':e['x'],'n':[e],'flat':fl})
        elif e['k']=='flat': groups.append({'k':'flat','x':e['x'],'p':e['p']})
        elif e['k']=='bar': groups.append({'k':'bar','x':e['x'],'b':e['b']})
    # assign neumes to syllables
    tol=0.05*size
    lyr_syl=[x for x in syl if not x.get('rub')]
    for i,x in enumerate(lyr_syl):
        x['ws']=(i==0) or lyr_syl[i-1]['end']
    for g in groups:
        if g['k']!='g': continue
        cand=[i for i,x in enumerate(lyr_syl) if x['va']-tol<=g['x']]
        g['s']=cand[-1] if cand else 0
    seq=[]   # [(syllable index or None, gabc piece)]
    used=set(g['s'] for g in groups if g['k']=='g')
    # merge syllables without notes into the previous one
    merged={}
    texts={i:x['t'] for i,x in enumerate(lyr_syl)}
    ends={i:x['end'] for i,x in enumerate(lyr_syl)}
    n=len(lyr_syl)
    for i in range(n):
        if i in used: continue
        # a syllable without notes joins its neighbour in the same word (the next one if it starts the word)
        if (lyr_syl[i]['ws'] or i==0) and i+1<n and not lyr_syl[i]['end'] and (i+1) in used:
            j=i+1
            texts[j]=texts[i]+texts[j]; texts[i]=None; merged[i]=j
            if lyr_syl[j]['ws']: pass
            lyr_syl[j]['ws']=lyr_syl[i]['ws']
        elif i>0:
            j=i-1
            seen=set()
            while j in merged and j not in seen: seen.add(j); j=merged[j]
            texts[j]+=texts[i]; ends[j]=ends[i]; texts[i]=None; merged[i]=j
    # a merged-forward syllable keeps the next one's notes: resolve groups
    gabc=''; cur=None; buf=''
    def flush():
        nonlocal gabc,cur,buf
        if cur is not None:
            t=texts.get(cur) or ''
            gabc+=t+'('+buf+')'+(' ' if ends.get(cur,True) else '')
        cur=None; buf=''
    # rubric tokens (*, italic) are placed by x among the groups
    rubs=[x for x in syl if x.get('rub')]
    seqs=[(g['x'],'g',g) for g in groups]+[(r['x'],'r',r) for r in rubs]
    seqs.sort(key=lambda t:(t[0],0 if t[1]=='r' else 1))
    for x,k,g in seqs:
        if k=='r':
            flush(); t=g['t']
            gabc+=(t if t=='*' else '<i>'+t+'</i>')+'() ' ; continue
        if g['k']=='bar':
            flush(); gabc+='('+g['b']+') ' if not gabc.endswith('() ') else ''
            if gabc.endswith('() '): gabc=gabc[:-3]+'('+g['b']+') '
            continue
        if g['k']=='flat': continue
        si=g['s']; seen=set()
        while si in merged and si not in seen: seen.add(si); si=merged[si]
        if si!=cur: flush(); cur=si
        elif buf: buf+='/'
        if g.get('flat') is not None: buf+=L[g['flat']+3]+'x'
        buf+=''.join(notestr(n) for n in g['n'])
    flush()
    cont=bool(lyr_syl) and not lyr_syl[-1]['end']
    return clef, gabc.strip(), cont
def plain(g): return re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',re.sub(r'\([^)]*\)','',g))).strip()
def assemble(items, book):
    pieces=[]; cur=None; ctx=[]
    for it in items:
        if it['k']=='text':
            if it['y']<40: continue           # running head and page number
            if cur: pieces.append(cur); cur=None
            ctx.append(it['text']); ctx=ctx[-6:]; continue
        clef,g,cont=system_gabc(it, cur and cur['clef'])
        if cur is None:
            cur={'book':book,'page':it['page'],'ctx':list(ctx),'lab':it['lab'],'clef':clef,'gabc':'('+(clef or 'c4')+') '+g,'cont':cont}
            ctx=[]
        else:
            sep='' if cur['cont'] else ' '
            if clef and clef!=cur['clef']: cur['gabc']+=' ('+clef+')'; cur['clef']=clef; sep=' ' if not cur['cont'] else ''
            cur['gabc']+=sep+g; cur['cont']=cont
    if cur: pieces.append(cur)
    for p in pieces: p['text']=plain(p['gabc'])
    return pieces
if __name__=='__main__':
    book=sys.argv[1]
    items=json.load(open(f'items_{book}.json'))
    P=assemble(items,book)
    json.dump(P,open(f'pieces_{book}.json','w'),ensure_ascii=False,indent=0)
    for p in P[:int(sys.argv[2]) if len(sys.argv)>2 else 8]: print(p['page'],p['lab'],p['ctx'][-2:],'\n ',p['gabc'][:600])
