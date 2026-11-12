// carrega os módulos da simulação em Node (testes sem navegador)
const vm = require('vm'), fs = require('fs'), path = require('path');
const files = fs.readdirSync(__dirname).filter(f => /^s\d+_.*\.js$/.test(f)).sort((a, b) => parseInt(a.slice(1)) - parseInt(b.slice(1)));
module.exports = function () { const src = files.map(f => fs.readFileSync(path.join(__dirname, f), 'utf8')).join('\n'); const c = vm.createContext({ console, Math, JSON, Object, Array }); vm.runInContext(src + ';this.Sim=Sim', c); return c.Sim; };
module.exports.files = files;
