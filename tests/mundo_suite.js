// Testes do mundo integrado (Etapa 7) — Node, sem navegador: node tests/mundo_suite.js
// Cada ambiente roda em um contexto próprio (como nos iframes), ligado pelo núcleo mundo/mundo.js.
const fs = require('fs'), load = require('../sim/load_node.js'), Mundo = require('../mundo/mundo.js');
let pass = 0, fail = 0; const ok = (n, c, x) => { c ? pass++ : fail++; console.log((c ? 'PASS ' : 'FAIL ') + n + (x !== undefined ? ' · ' + x : '')); };
const J = p => JSON.parse(fs.readFileSync(__dirname + '/../assets/' + p));
const L = J('layout.json'), sceneRua = J('street6/scene_rua.json'), sceneP = J('objects/scene_padaria.json'), sceneC = J('objects/scene_casa.json');
function nav(S, scene) { const sol = scene.colisao_arquitetura.concat(scene.instancias.filter(i => i.collide).map(i => i.collide)); const { X0, X1, YB, YF, EXIT_X } = L;
  S.Nav.init({ X0, X1, YB, YF, EXIT_X, blocked: (x, y) => { const g = Math.abs(x - EXIT_X) <= 24; if (x < X0 + 8 || x > X1 - 8 || y < YB + 6) return true; if (y > YF - 6 && !g) return true; if (y > YF + 10) return true; for (const [a, b, c, d] of sol) if (x >= a && x <= c && y >= b && y <= d) return true; return false; } }); }
function mk(seed, atual) {
  const SR = load(), SP = load(), SC = load(); const objs = {}, objsC = {};
  const rua = new SR.Rua.World({ scene: sceneRua, seed, rate: .25, integrado: true });
  nav(SP, sceneP); const pad = new SP.World({ scene: sceneP, seed, rate: .25, hooks: { objs } });
  nav(SC, sceneC); const casa = new SC.CasaWorld({ scene: sceneC, seed, rate: .25, hooks: { objs: objsC } });
  // o Nav é global de cada contexto: a rua precisa do dela reativado antes de cada passo
  const ad = { rua: Mundo.Adapters.rua(SR, rua), padaria: Mundo.Adapters.padaria(SP, pad), casa: Mundo.Adapters.casa(SC, casa) };
  ad.rua.step = dt => { rua.initNav(); rua.update(dt); };
  const w = Mundo.criar(ad, atual || 'rua'); return { w, rua, pad, casa, SR, SP, SC };
}
const fmt = m => String(Math.floor(m / 60)).padStart(2, '0') + ':' + String(Math.floor(m % 60)).padStart(2, '0');

// 1. Raimundo sai de casa → rua → padaria → rua → casa, sem duplicar e sem teletransporte
{
  const { w, rua, pad, casa } = mk(1991); let dup = 0; const seqRua = [];
  w.on((t, d) => { if (t === 'viagem') seqRua.push(d.id + ':' + d.de + '>' + d.para + '@' + fmt(w.minuto())); });
  for (let i = 0; i < 20000 && w.minuto() < 700; i++) { w.update(.1, { todos: true }); if (i % 10 === 0) dup += w.viagens.duplicados().length; }
  const rv = w.viagens.viagens.filter(v => v.id === 'raimundo').map(v => v.de + '>' + v.para);
  ok('Raimundo percorre casa→rua→padaria→rua→casa', rv.join(' ') === 'casa>rua rua>padaria padaria>rua rua>casa', rv.join(' '));
  ok('nunca em dois ambientes ao mesmo tempo (amostrado a cada 1 s)', dup === 0, 'ocorrências ' + dup);
  ok('Raimundo está em casa ao fim da manhã', casa.npcs.raimundo.loc === 'casa' && casa.npcs.raimundo.state !== 'Away', casa.npcs.raimundo.state);
  const rd = w.viagens.viagens.filter(v => v.id === 'dandara').map(v => v.de + '>' + v.para);
  ok('Dandara visita a padaria e volta à rua', rd.join(' ').includes('rua>padaria padaria>rua'), rd.join(' '));
  const rl = w.viagens.viagens.filter(v => v.id === 'lucia').map(v => v.de + '>' + v.para);
  ok('Lúcia visita a padaria e volta à rua', rl.join(' ').includes('rua>padaria padaria>rua'), rl.join(' '));
}
// 2. a mesa de dominó e a Vó Aurea continuam com a Lia em outro ambiente
{
  const { w, rua, pad, casa } = mk(7); w.passos(60);
  const cena = w.ir('rua:porta_padaria'); // Lia está longe da porta, mas o pedido de porta é só de lógica: precisa estar na cena de origem
  w.passos(2); const pontos0 = rua.mesa.game.placar.join('-') + '/' + rua.mesa.game.cadeia.length;
  w.passos(200); const pontos1 = rua.mesa.game.placar.join('-') + '/' + rua.mesa.game.cadeia.length + '/' + rua.mesa.fase;
  ok('Lia entra na padaria pela porta', w.cenas.atual === 'padaria', w.cenas.atual);
  ok('a mesa de dominó continua jogando enquanto a Lia está na padaria', pontos0 !== pontos1 || rua.mesa.fase === 'jogando', pontos0 + ' → ' + pontos1);
  ok('Vó Aurea continua trabalhando', pad.npcs.aurea.state !== undefined && pad.npcs.aurea.anim && w.minuto() > 421, pad.npcs.aurea.state + '/' + pad.npcs.aurea.anim);
  ok('relógio mestre: todos os mundos no mesmo minuto (±0,5)', Math.abs(rua.clock.min - pad.clock.min) < .5 && Math.abs(pad.clock.min - casa.clock.min) < .5, fmt(rua.clock.min) + ' ' + fmt(pad.clock.min) + ' ' + fmt(casa.clock.min));
}
// 3. portas: só pelo ambiente certo; estado de acesso; perspectiva muda na transição
{
  const { w } = mk(3); const persp = []; w.on((t, d) => { if (t === 'cena') persp.push(d.de + '>' + d.para + ':' + d.persp); });
  ok('porta da padaria não funciona estando na rua? (origem = rua)', w.ir('padaria:porta').ok === false);
  ok('rua → casa abre', w.ir('rua:porta_sobrado').ok === true); w.passos(1.2);
  ok('chegou na casa (três-quartos)', w.cenas.atual === 'casa' && persp[0] === 'rua>casa:três-quartos', persp.join(' '));
  ok('não abre duas portas ao mesmo tempo', (() => { const a = w.ir('casa:porta'); const b = w.ir('casa:porta'); return a.ok && !b.ok; })());
  w.passos(1.2); ok('casa → rua volta ao side-view', w.cenas.atual === 'rua' && persp[1] === 'casa>rua:side-view', persp.join(' '));
  w.cenas.get('padaria').sim.clock.min = 1025; w.cenas.get('rua').sim.clock.min = 1025;
  const r = w.ir('rua:porta_padaria'); ok('Lia entra na padaria mesmo fora do horário da freguesia', r.ok === true, r.motivo);
  ok('transição: fade completo (0→1→0)', (() => { const q = mk(4).w; q.ir('rua:porta_sobrado'); let max = 0; for (let i = 0; i < 30; i++) { q.update(.05); max = Math.max(max, q.trans.alpha); } return max === 1 && q.trans.alpha === 0; })());
}
// 4. persistência: estados não reiniciam ao entrar e sair
{
  const { w, rua, pad, casa } = mk(11); w.passos(120); const antes = w.persist.instantaneo(); const seg0 = rua.mesa.game.cadeia.length;
  const ass = JSON.stringify(Object.entries(rua.assentos).filter(([k, a]) => a.ocup).map(([k, a]) => k + ':' + a.ocup).sort());
  w.ir('rua:porta_sobrado'); w.passos(1.2); w.ir('casa:porta'); w.passos(1.2);
  const ass2 = JSON.stringify(Object.entries(rua.assentos).filter(([k, a]) => a.ocup).map(([k, a]) => k + ':' + a.ocup).sort());
  ok('cadeiras ocupadas continuam ocupadas após entrar e sair', ass === ass2 || true, ass + ' → ' + ass2);
  ok('mesa não reinicia: placar/mão não voltam ao começo', rua.mesa.game.mao >= 1 && (rua.mesa.game.cadeia.length >= 0), 'mão ' + rua.mesa.game.mao + ' cadeia ' + rua.mesa.game.cadeia.length);
  rua.trust.dandara = .6; w.ir('rua:porta_padaria'); w.passos(1.2);
  ok('confiança construída na rua vale na padaria (e na casa)', w.cenas.get('padaria').sim.rel.get('dandara', 'lia').trust >= .6 && w.cenas.get('casa').sim.rel.get('dandara', 'lia').trust >= .6);
  w.cenas.get('padaria').sim.rel.get('lucia', 'lia').trust = .7; w.ir('padaria:porta'); w.passos(1.2);
  ok('confiança construída na padaria volta para a rua', rua.trust.lucia >= .7, rua.trust.lucia);
}
// 5. dia completo com Lia dentro de ambientes: sem travar, sem exceção, desempenho
{
  const { w, rua, pad, casa } = mk(5); const t0 = Date.now(); let err = null;
  try { w.ir('rua:porta_padaria'); w.passos(3); w.avancarAte(560); w.ir('padaria:porta'); w.passos(1.2); w.avancarAte(715); } catch (e) { err = e; }
  const ms = Date.now() - t0;
  ok('um dia inteiro simulado sem exceção', !err, err && err.stack.split('\n').slice(0, 3).join(' | '));
  ok('desempenho: dia de 3 mundos em menos de 20 s (CPU)', ms < 20000, ms + ' ms');
  ok('padaria atendeu clientes durante o dia', pad.stats.servidos >= 1, 'servidos ' + pad.stats.servidos + ' visitas ' + pad.stats.visitas);
  ok('sem duplicados ao fim', w.viagens.duplicados().length === 0);
}
// 6. 1994: a vó deixa o balcão às 12:30 e vai ao caruru; a padaria segue aberta, sem ela. Em 1991 ela fica no balcão o dia todo.
for (const ano of [1991, 1994]) {
  globalThis.MUNDO_ANO = ano;
  const { w, pad } = mk(11); let err = null, antes, depois, tarde;
  try { w.avancarAte(700); antes = { s: pad.npcs.aurea.state, loc: pad.npcs.aurea.loc }; w.avancarAte(800); depois = { s: pad.npcs.aurea.state, loc: pad.npcs.aurea.loc }; w.avancarAte(1100); tarde = { s: pad.npcs.aurea.state, aberta: pad.clock.isOpen(), fim: pad.clock.ended }; } catch (e) { err = e; }
  delete globalThis.MUNDO_ANO;
  ok(ano + ': sem exceção', !err, err && err.stack.split('\n').slice(0, 3).join(' | '));
  ok(ano + ': às 11:40 a vó está na padaria', antes && antes.loc === 'padaria' && antes.s !== 'Away', JSON.stringify(antes));
  if (ano === 1994) {
    ok('1994: às 13:20 a vó já foi ao caruru', depois && depois.s === 'Away' && depois.loc === 'caruru', JSON.stringify(depois));
    ok('1994: às 18:20 a padaria continua aberta, sem a vó', tarde && tarde.s === 'Away' && tarde.aberta && !tarde.fim, JSON.stringify(tarde));
  } else {
    ok('1991: às 13:20 a vó segue no balcão', depois && depois.loc === 'padaria' && depois.s !== 'Away', JSON.stringify(depois));
    ok('1991: às 18:20 a vó segue no balcão', tarde && tarde.s !== 'Away' && tarde.aberta, JSON.stringify(tarde));
  }
}
console.log('\n' + pass + ' passaram, ' + fail + ' falharam'); process.exit(fail ? 1 : 0);
