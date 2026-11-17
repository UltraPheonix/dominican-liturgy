// Completeness report: every Mass must have its chants and readings.
const fs=require('fs');eval(fs.readFileSync(process.argv[2]||'site/data/masses.js','utf8').replace('var DOMINICAN','global.D'));
const req=(k,m)=>{const need=['in','of','co'];
  const pasch=/^(Pasc|Asc|AscVig|Litaniis|Pent0)/.test(k); const lent=/^(7a|6a|5a|Quad)/.test(k);
  if(/^Quad6f$/.test(k)) return ['tr'];
  if(!pasch) need.push('gr');
  if(lent) need.push('tr'); else need.push('al');
  return need;};
let bad=[],nr=0,total=0;const by={};
for(const s of D.sections){ for(const k of s.items){ total++; const m=D.masses[k]; const miss=(m.req||req(k,m)).filter(p=>!(m.parts[p]&&m.parts[p].length));
  const rd=m.readings||[]; const noR=!rd.some(r=>r.type=='Gospel')||!rd.some(r=>r.type!='Gospel');
  if(noR) nr++; if(miss.length||noR){bad.push([s.id,k,m.en.slice(0,40),miss.join(','),noR?'READINGS':'']); by[s.id]=(by[s.id]||0)+1;}}}
console.log('masses',total,'incomplete',bad.length,'no full readings',nr,JSON.stringify(by));
const show=+process.argv[3]||25; for(const b of bad.slice(0,show)) console.log(b.join(' | '));
