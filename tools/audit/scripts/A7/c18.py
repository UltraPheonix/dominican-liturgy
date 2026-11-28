from clus import *; from fx import add, get
s = 'M39 p. 16* (pdf 376), Comm. plur. Mart. T.P. (Sancti tui)'
la0 = canon_entry('C28s', 0, [('Allelúja: salus, et glória', 'Allelúja: Salus, et glória'), ('justificatiónes sunt sanctórum', 'justificatiónes sunt Sanctórum')], s,
                  "as printed: 'Allelúia : Salus, et glória', 'justificatiónes sunt Sanctórum' (capitals seen on the scan; i/j left)")
en0 = get(RF, ['C28s', 0, 'en']); tail = ' And he saith to me: These words of God are true.'
assert en0.endswith(tail); en0 = en0[:-len(tail)]
add(RF, ['C28s', 0, 'en'], en0, s, "English cut to the Missal's Latin, which ends 'Agni vocáti sunt.' (Apoc. 19: 9a): 'And he saith to me: These words of God are true.' (9b) dropped")
la1 = canon_entry('C28s', 1, [('pálmites: qui manet', 'pálmites: Qui manet')], s, "'vos pálmites : Qui manet' as printed (seen on the scan)")
en1 = get(RF, ['C28s', 1, 'en'])
MF = 'data/masses.js'
for k in ('S0529b', 'S0602b'):
    b = ['masses', k, 'season', 'pasch', 'readings']
    add(MF, b + [0, 'la'], la0, s, "Commune copy (Apoc. 19: 1-9, p. 16*; rubric 'Temp. Pasch. Officium Sancti tui, ut in Comm. plurim. Mart., pag. 15*'): 'Allelúia : Salus', 'Sanctórum' as printed (seen on the scan)")
    add(MF, b + [0, 'en'], en0, s, "English cut to the Missal's Latin (ends 'Agni vocáti sunt.'); 'And he saith to me: These words of God are true.' dropped (CHECK.md #118)")
    add(MF, b + [1, 'la'], la1, s, "Commune copy (Joan. 15: 5-11, p. 16*): 'vos pálmites : Qui manet' as printed (seen on the scan)")
    add(MF, b + [1, 'en'], en1, s, "English as the Commune text (C28s), with the incipit 'Jesus said to his disciples' that the Latin has")
print('ok')
