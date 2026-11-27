// node tools/ordo44/engine_dump.js 1944 > /tmp/e44.json : the Missal ranking engine for every day of a year
global.window = {};
require('../../data/kalendar39.js');
var fs = require('fs');
eval(fs.readFileSync(__dirname + '/../../data/masses.js', 'utf8').replace('var DOMINICAN', 'global.DOMINICAN'));
// the Masses app.js adds at load: the last Sunday and the Sundays left over after the Epiphany
var M = DOMINICAN.masses; M.Pent24 = M.Pent23; [3, 4, 5, 6].forEach(function (n) { M['Epi' + n + 'r'] = M.Pent23; });
var R = require('../../js/mrank.js')(window.KAL39, DOMINICAN.masses);
var y = +process.argv[2], out = [];
for (var d = new Date(y, 0, 1); d.getFullYear() === y; d.setDate(d.getDate() + 1)) {
  var r = R.day(d); r.mtitle = (DOMINICAN.masses[r.win] || {}).title || ''; out.push(r);
}
console.log(JSON.stringify(out, null, 0));
