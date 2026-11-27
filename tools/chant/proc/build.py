"""Build gabc/op-proc-*.gabc from the per-staff transcriptions here (a line ending '+' continues the word on the next staff)."""
import sys,os
H=os.path.dirname(os.path.abspath(__file__)); G=os.path.join(H,'..','..','..','gabc')
def build(src,out,head):
    ls=[l.rstrip() for l in open(os.path.join(H,src)) if l.strip() and not l.startswith('#')]
    body=''
    for l in ls:
        if l.endswith('+'): body+=l[:-1]
        else: body+=l+' '
    open(os.path.join(G,out),'w').write(head+'%%\n'+body.strip()+'\n')
P='book:Processionarium O.P. (1913), %s;\ntranscriber:transcribed from the page images (Mass chat, 2026-11-26);\n'
build('cum.txt','op13-cumappropinquaret.gabc','name:Cum appropinquaret;\noffice-part:Antiphona;\nmode:7;\n'+P%'pp. 24-26')
build('coll.txt','op13-collegerunt.gabc','name:Collegerunt;\noffice-part:Antiphona;\nmode:2;\n'+P%'p. 27')
build('unus.txt','op13-unusautem.gabc','name:Unus autem;\noffice-part:Versus;\nmode:2;\n'+P%'p. 28')
build('ave.txt','op13-averex.gabc','name:Ave Rex noster;\noffice-part:Antiphona;\nmode:2;\n'+P%'pp. 29-30')
build('glor.txt','op13-glorialaus.gabc','name:Gloria laus;\noffice-part:Hymnus;\nmode:1;\n'+P%'p. 30')
for n,w in [(1,'Israel es tu Rex'),(2,'Coetus in excelsis'),(3,'Plebs hebraea')]:
    build('glor_v%d.txt'%n,'op13-glorialaus-v%d.gabc'%n,'name:'+w+';\noffice-part:Versus;\nmode:1;\n'+P%'p. 31')
build('ingr.txt','op13-ingrediente.gabc','name:Ingrediente Domino;\noffice-part:Responsorium;\nmode:2;\n'+P%'p. 32')
build('deore.txt','op13-deoreleonis.gabc','name:De ore leonis;\noffice-part:Versus;\n'+P%'p. 33')
