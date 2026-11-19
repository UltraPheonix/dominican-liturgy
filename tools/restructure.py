import re, os
os.chdir('/home/claude/build/site')
GEAR='<button type="button" class="gear" id="gear" aria-controls="sheet" aria-expanded="false" title="Options"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M19.4 13a7.5 7.5 0 0 0 0-2l2.1-1.6-2-3.5-2.5 1a7.6 7.6 0 0 0-1.7-1L15 3h-4l-.4 2.9a7.6 7.6 0 0 0-1.7 1l-2.5-1-2 3.5L6.6 11a7.5 7.5 0 0 0 0 2l-2.2 1.6 2 3.5 2.5-1a7.6 7.6 0 0 0 1.7 1L11 21h4l.4-2.9a7.6 7.6 0 0 0 1.7-1l2.5 1 2-3.5zM13 15.5A3.5 3.5 0 1 1 13 8.5a3.5 3.5 0 0 1 0 7z" transform="translate(-1 0)"/></svg><span>Options</span></button>'
def top(brand, nav, gear=True):
    return ('<header class="top hide-print">\n  <div class="top-in">\n    '+brand+'\n    '+nav+'\n    <div class="top-tools">\n      <button type="button" class="en-toggle" aria-pressed="false" title="Show the English with the Latin">EN</button>\n'
            +('      '+GEAR+'\n' if gear else '')+'    </div>\n  </div>\n</header>\n')
def sheet(body, label='Options'):
    return ('<div class="sheet-back" id="sheetBack" hidden></div>\n<aside class="sheet hide-print" id="sheet" aria-label="'+label+'" hidden>\n  <div class="sheet-head"><span>'+label+'</span><button type="button" class="sheet-x" id="sheetX" aria-label="Close">×</button></div>\n'
            + body + '\n</aside>\n')
def grab(s, a, b):
    i=s.index(a); j=s.index(b, i)+len(b); return s[i:j]
def brandnav(s):
    brand=grab(s,'<a class="brand"','</a>')
    brand=brand.replace('<span><span class="t1">Dominican Rite</span><span class="t2">Missale · Breviarium</span></span>','<span class="t1">Dominican Rite</span>')
    return brand, grab(s,'<nav class="nav"','</nav>')
def field(s, fid):
    if fid in ('selSeason','selAsp','selOrdo'): return grab(s, '<div class="field"><label for="%s">'%fid, '</select></div>')
    return grab(s, '<div class="field"><label for="%s">'%fid, '</div>')
def sec(title, inner):
    return '  <section class="sh-sec"><h3>%s</h3>\n%s\n  </section>' % (title, inner)
EDIT='<label class="switch"><input type="checkbox" id="chkEdit"> Edit the chants (GABC)</label>'
TOOLS='<div class="tools hide-print"><button type="button" class="tbtn" id="btnShare">Share</button><button type="button" class="tbtn" id="btnChoir">Choir PDF</button><button type="button" class="tbtn" id="btnCong">Congregation PDF</button></div>\n'
def finish(s, a, b, head, pre):
    rest=s[b:].replace('<div class="inner">\n','<div class="inner">\n      '+pre,1)
    rest=rest.replace('    </div>\n  </div>\n</div>\n','    </div>\n  </div>\n',1)
    return s[:a]+head+rest
for page in ('index.html','holyweek.html'):
    s=open(page).read(); a=s.index('<div class="frame">'); b=s.index('<div class="content">'); side=s[a:b]
    brand,nav=brandnav(side); hw = page=='holyweek.html'
    F={f:field(side,f) for f in ['selMass','date','selSeason','selOrd','selCredo','selAsp','selOrdo']}
    if not hw:
        body='\n'.join([sec('Day', F['date']+'\n'+F['selMass']+'\n<div id="dateResults" class="alts"></div>\n<div id="cal" class="sh-cal"></div>'),
          sec('Chants', F['selSeason']+'\n'+F['selOrd']+'\n'+F['selCredo']+'\n'+F['selAsp']), sec('Show', F['selOrdo']), sec('Advanced', EDIT)])
        pre=('<div class="daybar hide-print"><button type="button" class="day-step" id="prevDay" aria-label="Previous day">‹</button><span class="day-d" id="dayDate"></span><button type="button" class="day-step" id="nextDay" aria-label="Next day">›</button><span class="day-meta" id="pills"></span></div>\n      '+TOOLS)
    else:
        hid='<div hidden>'+F['selMass']+F['date']+F['selSeason']+F['selCredo']+F['selAsp']+'<div id="dateResults"></div><div id="cal"></div><span id="dayDate"></span><span id="pills"></span><button id="prevDay"></button><button id="nextDay"></button></div>'
        body='\n'.join([sec('Show', F['selOrdo']), sec('Chants', F['selOrd']), sec('Advanced', EDIT), hid])
        pre='<div class="hw-pick hide-print">'+grab(side,'<div class="hw-rite"','</div>')+'\n      '+grab(side,'<nav class="hw-days"','</nav>')+'</div>\n      '+TOOLS
    open(page,'w').write(finish(s,a,b,top(brand,nav)+sheet(body),pre))
s=open('office.html').read(); a=s.index('<div class="frame">'); b=s.index('<div class="content">'); side=s[a:b]; brand,nav=brandnav(side)
body='\n'.join([sec('Show','<label class="switch"><input type="checkbox" id="chant"> Chant (Antiphonarium O.P.)</label>\n<label class="switch"><input type="checkbox" id="priest"> A priest or deacon presides</label>'),
                sec('Day','<input type="date" id="date" class="sh-date" aria-label="Date">\n<div id="cal" class="sh-cal"></div>')])
pre=('<div class="daybar hide-print"><button type="button" class="day-step" id="prevDay" aria-label="Previous day">‹</button><span class="day-d" id="dayMeta"></span><button type="button" class="day-step" id="nextDay" aria-label="Next day">›</button></div>\n'
     '      <div class="day-t"><h2 class="day-title" id="dayTitle"></h2><p class="day-sub" id="dayRank"></p></div>\n      <div id="hours" class="hours hide-print" role="tablist" aria-label="Hours"></div>\n')
open('office.html','w').write(finish(s,a,b,top(brand,nav)+sheet(body),pre))
s=open('about.html').read(); a=s.index('<div class="frame">'); b=s.index('<div class="content">'); side=s[a:b]; brand,nav=brandnav(side)
open('about.html','w').write(finish(s,a,b,top(brand,nav,False),''))
