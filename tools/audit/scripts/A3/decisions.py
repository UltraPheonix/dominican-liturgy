# per change id: 'skip' or override string (replacement Missal segment, accented)
D={}
SUB={}     # fid -> [(old, new)] applied after build
EXTRA=[]   # raw fix entries
NOTES={}   # key -> list of report notes
def skip(*ids):
    for i in ids: D[i]='skip'
# ---- S1101-S1102_3
skip('S1102.r0#0','S1102_3.pc#0')
SUB['S1102_2.r0']=[('cógitans. (nisi','cógitans. (Nisi'),('mórtuis). et quia','mórtuis). Et quia')]
SUB['S1102.r1']=[('Amen, Amen dico','Amen, amen dico')]
EXTRA.append({"file":"data/readings33.js","path":["S1102",1,"en"],"old":"At that time: Amen, amen I say unto you, that the hour cometh,","new":"At that time: Jesus said to the multitudes of the Jews: Amen, amen I say unto you, that the hour cometh,","src":"M39 p. 610 (pdf 344)","why":"English lacked the opening clause of the Latin (Dixit Jesus turbis Judaeorum)","_prefix":True})
NOTES['S1102_2']=['CHANT gr: Missal p. 610-611 prints Graduale Requiem with V. Animae eorum (not In memoria) for the 2nd Mass -> propose gr [6001] (G50 115*). Note G28 p. 106* rubric assigns In memoria to the day of All Souls: coordinator to decide.']
NOTES['S1102_3']=['CHANT gr: Missal p. 612 prints Graduale Requiem with V. Animae eorum for the 3rd Mass -> propose gr [6001] (G50 115*); same G28 rubric caveat.']
