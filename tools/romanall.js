// All of jgabc's Masses (Temporale, Saints, Commons, votive): chant IDs and the names of the chants.
const fs=require('fs'),vm=require('vm');const J=process.env.JGABC||'/home/claude/src/jgabc';
const c={module:{exports:{}},console};vm.createContext(c);
vm.runInContext(fs.readFileSync(J+'/propersdata.js','utf8')+';this.P=proprium;',c);
const name=id=>{try{const s=fs.readFileSync(J+'/gabc/'+id+'.gabc','utf8');const m=s.match(/^name:\s*([^;\n]*)/m);return m?m[1].trim():null}catch(e){return null}};
const F={in:'inID',gr:'grID',al:'alID',tr:'trID',se:'seID',of:'ofID',co:'coID'};const out={};
for(const [k,p] of Object.entries(c.P)){const o={};for(const [q,f] of Object.entries(F)){let v=p[f];if(v==null)continue;if(!Array.isArray(v))v=[v];
 v=v.filter(x=>typeof x==='number'||/^\d+$/.test(x)).map(Number).filter(x=>fs.existsSync(J+'/gabc/'+x+'.gabc'));if(v.length)o[q]=v.map(x=>({id:x,name:name(x)}));}
 if(Object.keys(o).length) out[k]=o;}
fs.writeFileSync('sources_roman_proprium.json',JSON.stringify(out));console.log(Object.keys(out).length,'masses');
