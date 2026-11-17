const fs=require('fs'),vm=require('vm');
const ctx={module:{exports:{}},console};vm.createContext(ctx);
vm.runInContext(fs.readFileSync((process.env.JGABC||'../../jgabc')+'/propersdata.js','utf8')+';this.sundayKeys=sundayKeys;this.proprium=proprium;this.saintKeys=saintKeys;this.commonsKeys=commonsKeys;this.otherKeys=otherKeys;',ctx);
const name=id=>{try{const s=fs.readFileSync((process.env.JGABC||'../../jgabc')+'/gabc/'+id+'.gabc','utf8');const m=s.match(/^name:\s*([^;\n]*)/m);return m?m[1].trim():null}catch(e){return null}};
const parts={in:'inID',gr:'grID',al:'alID',tr:'trID',se:'seID',of:'ofID',co:'coID'};
const out=[];
for(const k of ctx.sundayKeys){ if(!k.key) continue; const p=ctx.proprium[k.key]; if(!p){out.push({key:k.key,title:k.title,en:k.en,parts:{}});continue}
 const o={key:k.key,title:k.title.trim(),en:k.en.trim(),parts:{}};
 for(const [c,f] of Object.entries(parts)){ let v=p[f]; if(v==null) continue; if(!Array.isArray(v)) v=[v]; o.parts[c]=v.map(x=>name(x)).filter(Boolean);} out.push(o);}
fs.writeFileSync('sources/roman_temporale.json',JSON.stringify(out,null,0));
console.log(out.length); console.log(out.slice(0,6).map(o=>o.key+' '+JSON.stringify(o.parts)).join('\n'));
