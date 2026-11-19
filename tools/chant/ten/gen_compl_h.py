# Maundy Thursday Compline (Triduum O.P. 1927, pp. 130-133) -> tools/hw39/Quad6h_compl.src
import psalms, json, subprocess
out = []; SPEC = []
def w(*l): out.extend(l)
def T(la, en): w('T: ' + la, ' = ' + en)
def R(la, en): w('R: ' + la, ' = ' + en)
def ps(n, pid, tla, ten, noInton=False):
    vs = psalms.psalm(n)
    SPEC.append(dict(id=pid, name=tla, tone='VIII', diff='G', solemn=False, noInton=noInton, verses=[la for la, en in vs],
                     src='Ecclesiasticum Officium O.P. Triduo ante Pascha (1927): tone and ending as the book gives them on the first verse',
                     tr='set to the Dominican psalm tone (Tonorum communium regulae)'))
    w('F: %s | %s' % (tla, ten), 'G: %s | Tonus VIII G' % pid, 'F: Textus et versio | Text and translation')
    for la, en in vs: T(la, en)
    w('F/', 'F/')
w('== Ad Completorium | Compline', 'S: Ecclesiasticum Officium O.P. Triduo ante Pascha (1927), pp. 130-133')
R('Chorus dicat Completorium, si competens hora fuerit: alioquin, facto aliquo temporis intervallo, hora idonea cantetur.',
  'The Choir says Compline, if the hour is suitable; otherwise, after some interval of time, it is sung at a suitable hour.')
R('Completorium voce mediocri dicatur, ita tamen quod sonus psalmodiæ clare distincteque resonet (quod etiam abhinc omnibus Horis in psalmodia et cantu usque ad Vesperas Sabbati fiat, exceptis Matutinis, quæ solemnius sunt dicendæ).',
  'Compline is said in a moderate voice, yet so that the sound of the psalmody rings out clearly and distinctly (which is also to be done from now on at all the Hours, in psalmody and chant, until Vespers of Saturday, except Matins, which are to be said more solemnly).')
R('Non dicitur *Jube, domne,* nec Benedictio *Noctem quiétam,* neque Lectio *Fratres, sóbrii estóte,* neque *Confíteor,* neque ℣. *Convérte nos,* neque ℣. *Deus, in adjutórium,* sed, dicto *Pater noster,* postquam versis vultibus ad Altare Fratres se signaverint, inchoëtur:',
  'There is not said *Jube, domne,* nor the Blessing *Noctem quiétam,* nor the Lesson *Fratres, sóbrii estóte,* nor the *Confíteor,* nor the ℣. *Convérte nos,* nor the ℣. *Deus, in adjutórium;* but when the *Pater noster* has been said, and the brethren, turned towards the altar, have signed themselves, there is begun:')
T('{Aña} Christus factus est. {Ps. 4} Cum invocárem.', '{Ant.} Christ became obedient… {Ps. 4}')
ps(4, 'op-ten-h-ps-4', 'Psalmus 4 Cum invocárem', 'Psalm 4')
ps(90, 'op-ten-h-ps-90', 'Psalmus 90 Qui hábitat', 'Psalm 90')
ps(133, 'op-ten-h-ps-133', 'Psalmus 133 Ecce nunc', 'Psalm 133')
R('Continuo sequitur Canticum Simeonis:', 'The Canticle of Simeon follows at once:')
ps('Canticum Simeonis', 'op-ten-h-ps-nunc', 'Canticum Simeonis (Luc. 2) Nunc dimíttis', 'Canticle of Simeon (Luke 2)', noInton=True)
T('{Aña} Christus factus est pro nobis obédiens usque ad mortem, mortem autem crucis.', '{Ant.} Christ became obedient for us unto death, even the death of the Cross.')
w('G: op-ten-h-c01 | Antiphona · VIII')
w('L: Oratio', ' = Prayer')
T('^Réspice, quǽsumus, Dómine, super hanc famíliam tuam, pro qua Dóminus noster Jesus Christus non dubitávit mánibus tradi nocéntium, et crucis subíre torméntum.',
  'Look down, we beseech thee, O Lord, upon this thy family, for which our Lord Jesus Christ did not hesitate to be delivered into the hands of the wicked, and to undergo the torment of the Cross.')
R('Non additur *Qui tecum,* neque *Amen,* neque *Benedicámus,* neque *Fidélium,* sed solum *Pater noster,* et *Credo.* Benedictio non datur, omittitur Ant. *Salve, Regína,* nec aspergitur Aqua benedicta.',
  '*Qui tecum,* *Amen,* *Benedicámus* and *Fidélium* are not added, but only the *Pater noster* and the *Credo.* The Blessing is not given, the Antiphon *Salve, Regína* is left out, and Holy Water is not sprinkled.')
open('/home/claude/dominican-liturgy/tools/hw39/Quad6h_compl.src', 'w').write('\n'.join(out) + '\n')
print(subprocess.run(['node', '/home/claude/build/ten/gen_ps.js'], input=json.dumps(SPEC, ensure_ascii=False), capture_output=True, text=True).stdout)
