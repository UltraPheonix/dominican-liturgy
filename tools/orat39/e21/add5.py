import json,sys
sys.path.insert(0,'.')
from en_common import *
X=json.load(open('extra_final.json')); E=json.load(open('en_final.json'))
PL={'or':'Deus, qui nos concédis sanctórum Mártyrum tuórum N. et N. natalítia cólere; da nobis in ætérna beatitúdine de eórum societáte gaudére: Per Dóminum.',
 'se':'Múnera tibi, Dómine, nostræ devotiónis offérimus: quæ et pro tuórum tibi grata sint honóre Sanctórum, et nobis salutária, te miseránte, reddántur. Per Dóminum.',
 'pc':'Præsta nobis, quǽsumus Dómine, intercedéntibus sanctis Martýribus tuis N. et N.; ut quæ ore contígimus, pura mente capiámus: Per Dóminum.'}
EPL={'or':'O God, who grant us to keep the birthday of Your holy martyrs N. and N., grant us to rejoice in their company in everlasting bliss',
 'se':'We offer You, O Lord, the gifts of our devotion, that they may be pleasing to You for the honor of Your saints and, by Your mercy, become salutary to us',
 'pc':'Grant us, we beseech You, O Lord, by the intercession of Your holy martyrs N. and N., that what we have touched with our lips we may receive with a pure mind'}
new={
'C15s':{'p':'8*-9* (Unius Martyris Pontificis, tempore Paschali)','or':'Da, quǽsumus omnípotens Deus: ut qui beáti N. Mártyris tui atque Pontíficis solémnia cólimus; ejus apud te intercessiónibus adjuvémur: Per Dóminum.',
 'se':'Hæc hóstia, quǽsumus Dómine, emúndet nostra delícta: et ad sacrifícium celebrándum, subditórum tibi córpora mentésque sanctíficet. Per Dóminum.',
 'pc':'Refécti participatióne múneris sacri, quǽsumus Dómine Deus noster: ut cujus exséquimur cultum; intercedénte beáto N. Mártyre tuo atque Pontífice, sentiámus efféctum: Per Dóminum.'},
'C25s':dict(PL,p='14*-15* (Plurimorum Martyrum, alia Missa)'),
'C28s':dict(PL,p='16*-17* (Plurimorum Martyrum, tempore Paschali)'),
'C55s':{'p':'32*-33* (Unius Virginis non Martyris, alia Missa)','or':'Exáudi nos Deus salutáris noster: ut sicut de beátæ N. Vírginis tuæ festivitáte gaudémus; ita piæ devotiónis erudiámur afféctu: Per Dóminum.',
 'se':'Accépta tibi sit, Dómine, sacrátæ plebis oblátio pro tuórum honóre Sanctórum, quorum se méritis de tribulatióne percepísse cognóscit auxílium. Per Dóminum.',
 'pc':'Satiásti Dómine famíliam tuam munéribus sacris: ejus, quǽsumus, semper interventióne nos réfove; cujus solémnia celebrámus: Per Dóminum.'},
}
en={'C15s':{'or':'Grant, we beseech You, almighty God, that we who keep the feast of blessed N., Your martyr and bishop, may be helped by his intercession with You',
 'se':'May this sacrifice, we beseech You, O Lord, cleanse us from our sins, and sanctify the bodies and minds of Your servants for the celebration of the sacrifice',
 'pc':'Refreshed by partaking of the sacred gift, we beseech You, O Lord our God, that, by the intercession of blessed N., Your martyr and bishop, we may feel the effect of the rite we perform'},
 'C25s':EPL,'C28s':EPL,
 'C55s':{'or':'Hear us, O God our Saviour, that as we rejoice in the feast of blessed N., Your virgin, so we may be taught the spirit of loving devotion','se':SE_ACCEPTA,'pc':PC_SATIASTI.replace('of her','of her')}}
X.update(new); E.update(en)
json.dump(X,open('extra_final.json','w'),ensure_ascii=False,indent=1)
json.dump(E,open('en_final.json','w'),ensure_ascii=False,indent=1)
