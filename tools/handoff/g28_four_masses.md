# Graduale O.P. 1928 (Paredes): four missing feasts (handoff)

Source: /home/claude/dl/grad351/x/graduale_juxta_ritum_1928_paredes.djvu (1 djvu page = 2 printed pages).
Text layer: /tmp/g28pages.json. Helper scripts (outside the repo, in /tmp/g28w/): crop.py, crop2.py (interpolates tilted staves),
staffs.py (finds staff-line ys at two x positions), bars.py (vertical strokes).

## Where the feasts are printed, and their actual 1928 incipits
- SS. Angelorum Custodum (2 Oct): pp. 567-571, djvu 297 (right half) to 299.
  Off. "Angelis suis Deus mandavit de te" (mode I), Ps. "Qui habitat";
  Resp. "Laudate Dominum Deum nostrum ... V. Vivit autem ipse Dominus, quoniam custodivit me Angelus ejus" (mode III);
  Alleluia V. "Immittet Angelus Domini in circuitu timentium eum" (no mode numeral printed);
  Offert. "Angeli sunt administratorii Spiritus" (VIII); Comm. "Super muros tuos Jerusalem" (VIII). No Tempore Paschali or Septuagesima rubric is printed.
  (These differ from the 1950 OCR audit: 1928 has no "Benedicite Dominum" or "Angelis suis Deus mandavit" Responsorium.)
- S. Teresiae, Virginis (15 Oct): pp. 586-588, djvu 307 (both halves) and 308 (left).
  Off. "Dedit ei Dominus" (VI), Ps. "Cantate Domino"; Resp. "Danti mihi sapientiam ... V. Colluctata est" (V);
  Alleluia V. "Declaratio sermonum tuorum" (VIII); Offert. "Factus est in corde meo" (VI); Comm. "Misericordias Domini in aeternum cantabo" (I).
- S. Raphaelis Archangeli (24 Oct): pp. 589-590, djvu 308 (right) and 309 (left).
  Printed: "Officium Benedicite, pag. 433." Resp. "Laudate Dominum de caelis ... V. Laudate eum omnes Angeli ejus" (V) is printed in full.
  "Alleluia, V. In conspectu, pag. 470. Offertorium Stetit Angelus, pag. 436." The Communio "Angeli, Archangeli, Principatus ... benedicite in aeternum" is also printed in full on p. 590.
- S. Albertus Magnus (15 Nov): the 1928 book itself (p. 601, djvu 315 right) has only
  "B. Alberti Magni, Ep. et Conf. Ord. Praed. Missa Statuit, de Communi unius Confessoris et Pontificis, pag. 32*."
  The scan also contains a bound-in supplement leaf (djvu 314 right and 315 left, page "2", signed "Ex Secretaria S. R. C., die 9 Junii 1933").
  It reads "Missa In medio, in Festo unius Doctoris, pag. 35*, praeter sequentia", and prints Resp. "Ecce sacerdos magnus ... V. Inventus est justus"
  and "Alleluia. V. Vere magnus est in caelis Albertus ille fidelis qui fecit quod decuit". It is a 1933 supplement, not the 1928 text proper.

## Done (written in tools/g28/; each compiled with gregorio; first pass only, no second pass yet)
angeli_in, angeli_gr, angeli_al, angeli_of, angeli_co, teresia_in, teresia_gr: complete.
teresia_al: DRAFT, read up to "Decla-ra-ti-" (first staff of p. 588). The jubilus grouping still needs checking.
Notes: the liquescents (epiphonus/cephalicus, small second note) are written as ~:
Al(dc~), lu(cd~), cir(gh~), An(fg~) in angeli_of, in(gd~).
Uncertain items: angeli_co "i(h/ihih)": the last h is smudged and could be g. angeli_co "Jerúsalem": the accent mark is damaged in the print.
angeli_in "De(iyhj/ji/jkjk)": the natural sign is read as printed.
Mid-staff bars of 1.3 to 1.7 staff gaps are written (;). Bars of the full staff height are (:). Double bars are (::), including the "choir entry" double bars inside verses.
corrections.json was NOT touched.

## Left to do
1. Teresa Alleluia (p. 588, staves 2-3: djvu 308, staves with lines at y 894 and 1216), Offertorium "Factus est" (staves 4-6, y 1648/1996/2336),
   Communio "Misericordias" (staves 7-8, y 2748/3083). Crops already exist as /tmp/g28w/U1..U8_*.png (made with crop2.py, x 470-2460).
2. Raphael Resp. "Laudate Dominum de caelis": djvu 308 right, bottom staff (y about 3074), then djvu 309 left staves 1-3.
   Optionally raphael_co ("Angeli, Archangeli") on djvu 309 left, staves 4-7.
3. Albert: albertus_gr and albertus_al from the 1933 supplement (djvu 314 right, staves at y 1378-3054; djvu 315 left, y 569-1261).
   Header should say "Supplementum S.R.C. 1933 bound in the 1928 copy".
4. Second full pass over all files, then a gregorio compile (cd /tmp && gregorio -o x.gtex FILE).

## How to resume
- Render a page: ddjvu -format=pnm -page=N FILE /tmp/_pN.pnm
- Find the staves: python3 /tmp/g28w/staffs.py /tmp/_pN.pnm XA XB. Use XA=700, XB=2250 for the left page and 3300, 4700 for the right page.
- Crop a staff: python3 /tmp/g28w/crop2.py PNM X0 X1 "L@XA" "L@XB" OUTPREFIX 1000. It writes OUTPREFIX_k.png with a gabc-position grid and blob letters.
  The grid letters are gabc staff positions whatever the clef. Check the clef: the Teresa Resp. and Alleluia are c3.
