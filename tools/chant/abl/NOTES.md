# Washing of the altars (Triduum O.P. 1927, pp. 82-111) -> gabc/op-abl-r01..r10, a01..a32
- Staves read with tools/pdfomr/m39app.py on /home/claude/dl/tri/tri.pdf (musicasacra officium-hedomadae-sanctae-1927-paredes.pdf),
  cache /home/claude/build/tri_staves.pkl (tri_read.py PG0 PG1). build.py: OCR syllables positioned at blank gaps of the lyric line,
  aligned to the right text (pieces.py), notes by x; obliques (porrectus) thinned; fix.json = hand corrections after proofing.
- Responsories r01-r09 are printed twice (Tenebrae pp. 6-17 = pieces.PM m01-m09): both read, every disagreement looked at on the scan.
- Antiphons in GregoBase (Antiphonarium O.P. 1933): notes taken from there, transposed to the 1927 clef (assemble.py GB); others proofed
  on the scan (full.py/half.py/zz.py crops). Clefs from the clef grid (c3/c4/f3).
- Text + rubrics + versicles + orations: tools/hw39/Quad6h_abl.src (INC before Quad6h_mand). Versicle "etc." completed.
