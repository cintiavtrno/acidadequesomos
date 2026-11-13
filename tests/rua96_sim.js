// Teste do motor da rua de 1996 (Node): alvos de rota livres, atores andando sem entrar em colisão, músicos e equipe se movem na horizontal.
const fs = require('fs'), B = __dirname + '/../';
eval(fs.readFileSync(B + 'sim/s1_core.js', 'utf8') + ';global.Sim=Sim;');
eval(fs.readFileSync(B + 'sim/s2_nav.js', 'utf8'));
eval(fs.readFileSync(B + 'sim/s96_rua.js', 'utf8') + ';global.Sim96=Sim96;');
eval(fs.readFileSync(B + 'sim/s96_elenco.js', 'utf8'));
const scene = JSON.parse(fs.readFileSync(B + 'assets/street96/scene_rua96.json', 'utf8'));
const atlas = {}; for (const f of fs.readdirSync(B + 'assets/chars')) if (f.endsWith('_side.json')) atlas[f.replace('.json', '')] = JSON.parse(fs.readFileSync(B + 'assets/chars/' + f, 'utf8'));
let falhas = 0; const ok = (c, m) => { if (!c) { falhas++; console.log('FALHOU:', m); } };
const w = new Sim96.World({ scene, atlas, elenco: Sim96.Elenco, seed: 7 });
for (const a of w.lista) {
  ok(atlas[a.who + '_side'], 'sprite ausente: ' + a.who);
  for (const p of a.plano) if (p.vai) { const y = Sim96.yw(p.vai[0]) + p.vai[1]; ok(!w.blocked(p.vai[0], y), a.id + ' alvo bloqueado ' + p.vai); }
}
const x0 = {}; w.lista.forEach(a => x0[a.id] = [a.x, a.x]);
for (let t = 0; t < 240 * 20; t++) { w.update(1 / 20); for (const a of w.lista) { x0[a.id][0] = Math.min(x0[a.id][0], a.x); x0[a.id][1] = Math.max(x0[a.id][1], a.x); ok(isFinite(a.x) && isFinite(a.y), 'NaN em ' + a.id); } }
for (const id of ['perc1', 'perc2', 'perc4', 'cantor', 'cam_ombro', 'carga', 'diretor']) ok(x0[id][1] - x0[id][0] > 20, id + ' não se moveu na horizontal');
for (const a of w.lista) if (a.camada === 'sorted' && !a.fixo) ok(!w.blocked(a.x, a.y) || a.estado === 'anda', a.id + ' parado dentro de colisão');
console.log(falhas ? falhas + ' falha(s)' : 'rua96: ok (' + w.lista.length + ' atores)'); process.exit(falhas ? 1 : 0);
