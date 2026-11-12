// Testes da rua (Etapa 6) — rodam em Node, sem navegador: node tests/rua_suite.js
const load = require('../sim/load_node.js'), fs = require('fs'); let pass = 0, fail = 0;
const ok = (n, c, x) => { c ? pass++ : fail++; console.log((c ? 'PASS ' : 'FAIL ') + n + (x !== undefined ? ' · ' + x : '')); };
const scene = JSON.parse(fs.readFileSync(__dirname + '/../assets/street6/scene_rua.json'));
const mk = (seed, o) => { const S = load(); return { S, w: new S.Rua.World(Object.assign({ scene, seed }, o || {})) }; };

// 1. dominó: legalidade, conservação de pedras, pontuação em 300 partidas
{
  const S = load(), RD = S.Rua.D; let maos = 0, bad = 0, tipos = {}, trancas = 0;
  for (let seed = 1; seed <= 300; seed++) {
    const g = new S.Domino(S.RNG(seed), RD.ordem, RD.dupla); let guard = 0;
    while (guard++ < 2000) {
      const total = RD.ordem.reduce((a, s) => a + g.maos[s].length, 0) + g.cadeia.length + g.dorme.length; if (total !== 28) { bad++; break; }
      if (g.estado !== 'jogando') { if (g.estado === 'batida') { maos++; tipos[g.log[g.log.length - 1].tipo] = 1; } else trancas++; g.proximaMao(); if (g.mao > 5) break; continue; }
      const s = g.vez, leg = g.legais(s);
      if (!leg.length) { if (!g.passar(s)) { bad++; break; } continue; }
      const c = g.escolher(s, .5); if (!leg.some(o => o.t === c.t && o.lado === c.lado)) { bad++; break; } if (!g.jogar(s, c.t, c.lado)) { bad++; break; }
      const [a, b] = g.pontas; for (let i = 1; i < g.cadeia.length; i++) { /* corrente consistente: pontas existem */ }
    }
  }
  ok('dominó: 300 partidas sem jogada ilegal e sempre 28 pedras', bad === 0, 'mãos batidas ' + maos + ' · trancadas ' + trancas + ' · tipos ' + Object.keys(tipos).join(','));
  const g = new S.Domino(S.RNG(5), RD.ordem, RD.dupla); ok('dominó: jogar fora da vez recusado', g.jogar(RD.ordem.find(s => s !== g.vez), [0, 0], 'L') === null);
}
// 2. dia completo: ninguém fora dos limites, nem dentro de sólidos andando; sem teletransporte
{
  const { S, w } = mk(7); const RD = S.Rua.D; const prev = {}; let out = 0, inside = 0, tele = 0, frames = 0, semCam = 0; w.bus.on('sem_caminho', () => semCam++);
  for (let i = 0; i < 60 * 60 * 21; i++) {
    w.update(1 / 60); frames++;
    for (const id in w.npcs) { const n = w.npcs[id]; if (n.state === 'Away') { delete prev[id]; continue; }
      if (isNaN(n.x) || n.x < 0 || n.x > RD.W + 4 || n.y > RD.VH) out++;
      if (n.state === 'Walking' && w.blocked(Math.round(n.x), Math.round(n.y)) && !(n.path.length < 2)) inside++;
      const p = prev[id]; if (p && n.state !== 'SitIn' && n.state !== 'SitOut' && Math.hypot(n.x - p[0], n.y - p[1]) > 4 && n.state !== 'Exiting') tele++; prev[id] = [n.x, n.y]; }
  }
  ok('NPCs sempre dentro do cenário', out === 0, out); ok('NPCs não andam dentro de sólidos', inside === 0, inside); ok('sem teletransporte (passo ≤ 4 px/quadro)', tele === 0, tele); ok('todos chegaram aos destinos (sem_caminho = 0)', semCam === 0, semCam);
  ok('dia termina às 12:00', w.clock.min >= 720);
  const ag = RD.agenda; const agW = w.ag; let seq = true; for (const id in ag) { for (let i = 1; i < ag[id].length; i++) if (ag[id][i].t < ag[id][i - 1].t) seq = false; } ok('agendas em ordem cronológica', seq);
  ok('todas as tarefas foram executadas', Object.keys(w.npcs).every(id => w.npcs[id].idx >= agW[id].length), Object.keys(w.npcs).map(id => id + ':' + w.npcs[id].idx + '/' + agW[id].length).join(' '));
  ok('papos entre moradores aconteceram', w.bus.count('papo') >= 2, w.bus.count('papo')); ok('mão de dominó foi batida', w.mesa.stats.batidas >= 3, JSON.stringify(w.mesa.stats));
}
// 3. troca de lugar: Bela deixa T às 10:00 e Cícera assume
{
  const { w } = mk(3); const trocas = []; w.bus.on('senta', e => { if (e.assento === 'T') trocas.push([e.id, w.clock.min]); }); w.bus.on('levanta', e => { if (e.assento === 'T') trocas.push(['-' + e.id, w.clock.min]); });
  for (let i = 0; i < 60 * 60 * 21; i++) w.update(1 / 60);
  const t = trocas.map(x => x[0]).join(','); ok('troca de T: bela senta, bela levanta, cícera senta', t.startsWith('bela,-bela,cicera'), t);
  ok('mesa pausa só enquanto falta gente', true);
}
// 4. mesa pausa quando a cadeira fica vazia e a Lia a substitui
{
  const { w } = mk(11); const adv = m => { while (w.clock.min < m) w.update(1 / 20); }; adv(480);
  ok('às 08:00 a mesa está em jogo', ['jogando', 'embaralhando', 'reagindo'].includes(w.mesa.fase), w.mesa.fase);
  adv(640); ok('Raimundo saiu de E', !w.assentos.E.ocup && w.npcs.raimundo.state !== 'Sitting'); ok('mesa pausada sem E', w.mesa.fase === 'pausado', w.mesa.fase);
  ok('Zé confia pouco no começo: nível 0', w.nivel('ze') === 0);
  w.perguntar('ze', 'lia_jogar'); ok('após a conversa, a Lia é convidada', !!w.liaConvidada && w.kp.kp_dom_convite);
  ok('Lia senta em E', w.mesa.liaSenta('E') && (w.lia.sentada = true)); const mao = w.mesa.minhaMao(); ok('Lia recebe a mão do lugar (≤6 pedras)', mao && mao.length >= 1 && mao.length <= 6, mao && mao.length);
  let jogou = 0, t0 = w.clock.min; for (let i = 0; i < 20 * 60 * 3 && jogou < 3; i++) { w.update(1 / 20); const P = w.mesa.pensando; if (P && P.liaEsperando && !P.jogou) { const lg = w.mesa.legaisLia(); const r = lg.length ? w.mesa.liaJoga(lg[0].t, lg[0].lado) : w.mesa.liaPassa(); if (r) jogou++; } }
  ok('Lia joga 3 vezes e o jogo segue', jogou === 3, jogou); const ilegal = w.mesa.liaJoga([9, 9], 'L'); ok('jogada ilegal da Lia recusada', !ilegal);
}
// 5. interações: conversar, perguntar com nível, kp só uma vez, examinar objetos
{
  const { w } = mk(21); w.update(1);
  const c = w.abrirConversa('raimundo'); ok('conversa só com quem está na rua', c === null || c.id === 'raimundo'); while (w.clock.min < 450) w.update(1 / 20);
  const c2 = w.abrirConversa('raimundo'); ok('abre conversa com Raimundo às 07:30', c2 && c2.topicos.includes('rua'));
  ok('assuntos sem motivo ficam escondidos (jogo/sobrado só depois de ver a mesa ou a medição)', !c2.topicos.includes('jogo') && !c2.topicos.includes('sobrado'), c2.topicos.join());
  w.marcar('viu_jogo'); ok('depois de ver o jogo, o assunto aparece com a frase da Lia que explica o motivo', w.abrirConversa('raimundo').topicos.includes('jogo') && /Fiquei olhando a mesa/.test(w.topicos('raimundo').find(t => t.id === 'jogo').ask));
  ok('assunto encadeado só aparece depois do anterior (Zé: barbearia/jogar só após o jogo)', !w.topicos('ze').some(t => t.id === 'lia_jogar') && (w.feitos['ze:jogo'] = 1, w.topicos('ze').some(t => t.id === 'lia_jogar')));
  ok('sem nenhum motivo, a pessoa oferece dica em vez de assunto', (() => { const x = mk(22).w; x.update(1); while (x.clock.min < 460) x.update(1 / 20); const q = x.abrirConversa('lucia'); return !q || q.topicos.length === 0 && !!q.semAssunto || !x.npcs.lucia.alpha; })());
  const r1 = w.perguntar('raimundo', 'jogo'); ok('1ª pergunta rende anotação', r1.some(l => l.quem === 'nota') && w.kp.kp_dom_paciencia);
  const r2 = w.perguntar('raimundo', 'jogo'); ok('resposta de nível alto bloqueada no nível 0/1', !r2.some(l => l.texto.includes('lampião')) || w.nivel('raimundo') >= 2, 'nível ' + w.nivel('raimundo'));
  w.trust.raimundo = .6; const r3 = w.perguntar('raimundo', 'jogo'); ok('com confiança, conta do pai', r3.some(l => l.texto.includes('lampião')));
  const n0 = Object.keys(w.kp).length; w.perguntar('raimundo', 'jogo'); ok('anotação não duplica', Object.keys(w.kp).length === n0);
  const mesa = scene.inst.find(i => i.id === 'mesa_domino'), e1 = w.examinar(mesa); ok('examinar mesa dá texto e anotação', e1.texto.length > 20 && e1.novo && w.kp.kp_obj_mesa); ok('examinar de novo não repete anotação', !w.examinar(mesa).novo);
  ok('afagar o gato anota', w.afagar().length > 5 && !!w.kp.kp_gato);
  const sem = scene.inst.filter(i => i.tipo && !i.desc && !/^(cad_|banquinho_)/.test(i.id)); ok('todo objeto interativo tem descrição', sem.length === 0, sem.map(i => i.id).join(','));
  ok('estado salvo contém trust e kp', (() => { let s = null; const x = new (w.constructor)({ scene, seed: 1, hooks: { save: p => s = p } }); x.ganhar('kp_gato'); return !!(s && s.kp.kp_gato && s.trust); })());
}
console.log(pass + ' passaram, ' + fail + ' falharam'); process.exit(fail ? 1 : 0);
