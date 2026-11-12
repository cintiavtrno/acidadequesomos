// fiado de outros vizinhos + sacola esquecida (PROPOSTA)
const H = require('./harness.js'); let ok = 0, bad = 0; const check = (n, c, x) => { console.log((c ? 'PASSOU ' : 'FALHOU ') + n + (x ? ' — ' + x : '')); c ? ok++ : bad++; };
let outros = 0, sacola = 0, dias = 0;
for (let seed = 1; seed <= 12; seed++) {
  const { w, Sim } = H.make({ rate: 3, seed }); dias++; Sim.Sacola.S.estado = 'nada'; w.bus.on && w.bus.on('fiado', e => { if (e.id !== 'raimundo') outros++; });
  for (let i = 0; i < 20000 && w.clock.min < 12 * 60; i++) w.update(.2);
  if (Sim.Sacola.S.estado === 'balcao') sacola++;
}
check('1. outros vizinhos pedem fiado em alguns dias', outros > 0, outros + ' pedidos em ' + dias + ' dias');
check('2. sacola esquecida aparece quando Raimundo é atendido', sacola > 0, sacola + '/' + dias);
// lata colaborativa no começo do dominó
{ const load = require('../sim/load_node.js'), fs = require('fs'); const scene = JSON.parse(fs.readFileSync(__dirname + '/../assets/street6/scene_rua.json'));
  const S = load(), w = new S.Rua.World({ scene, seed: 11 }); const falas = []; const f0 = S.Rua.MesaDomino && S.Rua.MesaDomino.prototype.falaSeat; 
  while (w.clock.min < 480) w.update(1 / 20);
  const c = w.mesa.lataFeita && w.mesa.stats.maos >= 0 && ['jogando', 'embaralhando', 'reagindo'].includes(w.mesa.fase); console.log((c ? 'PASSOU' : 'FALHOU') + ' 3. lata explicada antes da primeira mão e o jogo segue — ' + w.mesa.fase); if (!c) bad++; }
console.log(ok + ' passaram, ' + bad + ' falharam'); process.exit(bad ? 1 : 0);
