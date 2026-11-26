"""Build gabc/op59-*.gabc from these per-staff transcriptions of the Cantus Gregoriani ad Ordinem Hebdomadae Sanctae
O.P. instauratum (Romae 1959) = media.churchmusicassociation.org/dominican/hebdomada-sancta-1959.pdf ('+' = word goes on)."""
import os
H=os.path.dirname(os.path.abspath(__file__)); G=os.path.join(H,'..','..','..','gabc')
SRC='book:Cantus Gregoriani ad Ordinem Hebdomadae Sanctae O.P. instauratum (Romae 1959), %s;\ntranscriber:transcribed from the page images (Mass chat, 2026-11-26);\n'
def build(src,out,name,part,mode,pages):
    body=''
    for l in open(os.path.join(H,src)):
        l=l.rstrip()
        if not l or l.startswith('#'): continue
        body+= l[:-1] if l.endswith('+') else l+' '
    head='name:%s;\noffice-part:%s;\n'%(name,part)+('mode:%s;\n'%mode if mode else '')+SRC%pages
    open(os.path.join(G,'op59-'+out+'.gabc'),'w').write(head+'%%\n'+body.strip()+'\n')
build('pueri1.txt','pueri1','Pueri Hebraeorum, tollentes','Antiphona','1','pp. 5-6')
build('ps23.txt','ps23','Domini est terra (Ps 23)','Psalmus','1','p. 6')
build('pueri2.txt','pueri2','Pueri Hebraeorum, vestimenta','Antiphona','1','p. 7')
build('ps46.txt','ps46','Omnes gentes (Ps 46)','Psalmus','1','p. 7')
build('occurrunt.txt','occurrunt','Occurrunt turbae','Antiphona','8','p. 9')
build('cumangelis.txt','cumangelis','Cum angelis et pueris','Antiphona','7','pp. 9-10')
build('turbamulta.txt','turbamulta','Turba multa','Antiphona','4','p. 10')
build('coeperunt.txt','coeperunt','Coeperunt omnes turbae','Antiphona','1','pp. 10-11')
for n in (1,2,3): build('glv%d.txt'%n,'glorialaus-v%d'%n,'Gloria laus, versus %d'%n,'Versus','1','p. 12')
build('omnescoll.txt','omnescoll','Omnes collaudant','Antiphona','8','p. 13')
build('ps147.txt','ps147','Lauda Ierusalem (Ps 147)','Psalmus','8','p. 13')
build('fulgentibus.txt','fulgentibus','Fulgentibus palmis','Antiphona','8','p. 14')
