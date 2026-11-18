// Dump every chantable piece of the Office (antiphons, hymn first lines, responsories) with where it occurs.
const fs=require('fs');const B='data/office/';const common=JSON.parse(fs.readFileSync(B+'common.json'));
const sh={};function ex(t){return t.split('\n').map(l=>{if(l[0]!='§')return l;const k=l.slice(1),s=k.slice(0,2);sh[s]=sh[s]||JSON.parse(fs.readFileSync(B+'psalter/'+s+'.json'));return sh[s][k]||''}).join('\n')}
const out={};
for(const y of fs.readdirSync(B).filter(x=>/^\d{4}$/.test(x)))for(const f of fs.readdirSync(B+y)){
  const day=JSON.parse(fs.readFileSync(B+y+'/'+f));
  for(const [h,rows] of Object.entries(day.h))rows.forEach(r=>{
    const lines=ex(day.b[r[0]]||common[r[0]]||'').split('\n');
    let head='';
    lines.forEach((l,i)=>{
      if(/^<h>/.test(l)){head=l.replace(/<[^>]+>/g,'');return;}
      let kind=null,t=null;
      if(/^<r>Ant\.<\/r>/.test(l)){kind='an';t=l.replace(/^<r>Ant\.<\/r>\s*/,'');}
      else if(/Hymnus/.test(head)&&/^<c>/.test(l)&&!/^<r>/.test(lines[i-1]||'x')){kind='hy';t=lines.slice(i,i+4).join(' ');}
      else if(/^<r>℟\.br\.<\/r>/.test(l)){kind='rb';t=l.replace(/^<r>℟\.br\.<\/r>\s*/,'');}
      if(!kind)return;
      t=t.replace(/<[^>]+>/g,'');const k=kind+'|'+t;
      (out[k]=out[k]||{kind,t,n:0,where:[]}).n++; if(out[k].where.length<3)out[k].where.push(y+'-'+f.slice(0,5)+' '+h);
    });
  });
}
fs.writeFileSync('/home/claude/build/gb/office_texts.json',JSON.stringify(Object.values(out)));
const c={};Object.values(out).forEach(o=>c[o.kind]=(c[o.kind]||0)+1);console.log(c);
