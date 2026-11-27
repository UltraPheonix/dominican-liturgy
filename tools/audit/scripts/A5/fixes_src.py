import sys; sys.path.insert(0,'/tmp/A5')
from fx import *
LC=' Per Dóminum nostrum Iesum Christum, Fílium tuum: qui tecum vivit et regnat in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum.'
EC='; through our Lord Jesus Christ, Your Son, who lives and reigns with You in the unity of the Holy Spirit, God, world without end.'
# ---------- C7s: chants and readings are those of the Missal's Martyr-Bishop Mass Laetabitur (pp. 5*-6*); the orations were those of the Martyr-non-Bishop Mass (pp. 9*-10*)
S='M39 pp. 5*-6* (pdf 370-371)'
orat_set('C7s','or','Lætétur Ecclésia tua, Deus, beáti N. Mártyris tui atque Pontíficis confísa suffrágiis: atque eius précibus gloriósis, et devóta permáneat; et secúra consístat:'+LC,
  'Helped by the prayers of blessed N., Your martyr and bishop, may Your Church be glad, O Lord; and through his glorious intercession may she abide in loyalty and stand unshaken'+EC,S,'wrong Mass: the Collect of the Martyr-non-Bishop Mass (p. 9*) stood here; the Missal prints Lætétur for this Mass (English: St Dominic Missal 1959, Ember Saturday of September, commemoration)')
orat_set('C7s','se','Súscipe Dómine múnera, quæ in eius tibi solemnitáte deférimus, cuius nos confídimus patrocínio liberári.'+LC,
  'Receive, O Lord, these offerings which we make on the feast of him through whose patronage we trust to be made free'+EC,S,'wrong Mass: Secret of p. 10* replaced by the Missal\'s Secret of this Mass, p. 6* (English: St Dominic Missal 1959, Holy Guardian Angels, commemoration of St Leger)')
orat_set('C7s','pc','Satiásti Dómine famíliam tuam munéribus sacris: eius, quǽsumus, semper interventióne nos réfove; cuius solémnia celebrámus:'+LC,
  'You have filled Your household, O Lord, with sacred gifts; ever refresh us, we beseech You, by the intercession of him whose feast we celebrate'+EC,S,'wrong Mass: Postcommunion of p. 10* replaced by the Missal\'s Postcommunion of this Mass, p. 6* (English as for C55s, him for her)')
orsrc('C7s','Missale O.P. (1939), pp. 5*-6* (In festo unius Martyris Pontificis extra tempus Paschale); English after the St Dominic Missal (1959)','orations now from the Mass whose chants and readings the page shows')
rd('C7s',1,'la',[('ei, dicéntes: Quia','ei, dicéntes, Quia'),('rogat ea quæ pacis','rogat ea, quæ pacis')],'M39 p. 6* (pdf 371)','punctuation as printed')
# ---------- Commune pp. 7*-11* (pdf 371-373), every edit checked on the scan
for k,n in [('C11s',371),('C15s',372),('C18s',373)]:
    auto_rd(k,n)
rd('C11s',0,'la',[('et ter Dómini','et Pater Dómini'),('sic éritis et consolatiónis.','sic éritis et consolatiónis: In Christo Jesu Dómino nostro.')],'M39 p. 7* (pdf 371)','word as printed (Pater); ending as printed')
rd('C15s',1,'la',[('fructum multum, quia','fructum multum: quia')],'M39 p. 8* (pdf 372)','punctuation as printed')
rd('C18s',0,'la',[('áffuit','ádfuit'),('claritátem ætérnam.','claritátem ætérnam, Dóminus Deus noster.')],'M39 p. 10* (pdf 373)','spelling as printed; ending as printed')
