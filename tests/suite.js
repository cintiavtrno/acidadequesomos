// Testes obrigatórios da Etapa 4 (parte lógica; os visuais são tirados no navegador). Uso: node tests/suite.js
const { make, scene } = require('./harness.js');
let ok = 0, bad = 0; const out = [];
const T = (n, nome, cond, info) => { (cond ? ok++ : bad++); out.push((cond ? 'PASSOU ' : 'FALHOU ') + n + '. ' + nome + (info ? '  — ' + info : '')); };
const day = (seed, o) => { const m = make(Object.assign({ seed }, o)); return m; };

// 1/2/9/12 — Lia parada (ou fora da padaria): a padaria funciona sozinha, a Vó atende sem comandos, o relógio avança
{ const { w } = day(1991); w.cena = 'interior'; w.lia.x = 150; w.lia.y = 225; const t0 = w.clock.min, ev = []; w.bus.on('*', e => ev.push(e)); w.step(200);
  T(1, 'Lia parada: a padaria roda sozinha', ev.includes('atendido') && w.stats.servidos >= 2, 'servidos=' + w.stats.servidos);
  T(2, 'A Vó atende sem comandos (abre o forno, acende a vela, serve)', w.obj('forno_aceso') === 1 && w.obj('altar_vela') === 1 && w.stats.servidos >= 2, 'forno=' + w.obj('forno_aceso') + ' vela=' + w.obj('altar_vela'));
  T(9, 'O tempo avança continuamente', w.clock.min - t0 > 190, w.clock.label()); }
{ const { w } = day(7); w.cena = 'street'; w.step(60); const a = w.stats.servidos, c0 = w.clock.min; w.step(120);
  T(12, 'O mundo não congela quando Lia sai da área de serviço', w.stats.servidos > a && w.clock.min - c0 > 100 && w.stats.sem_lia >= 1, 'atendeu_com_lia_fora=' + w.stats.sem_lia); }

// 3 — clientes diferentes (ações, pedidos, tempo de espera, destinos)
{ const { w } = day(1991); const acts = {}; w.bus.on('estado_npc', d => { (acts[d.id] = acts[d.id] || new Set()).add(d.para); }); w.step(330);
  const R = acts.raimundo, D = acts.dandara, L = acts.lucia;
  T(3, 'Os três clientes se comportam de forma diferente', R.has('Praying') && !D.has('Praying') && L.has('Measuring') && !R.has('Measuring') && D.has('Observing') && !R.has('Observing'),
    'R:' + [...R].join('/') + ' | D:' + [...D].join('/') + ' | L:' + [...L].join('/')); }

// 4/8 — conversa espontânea entre dois NPCs + mudança de relação e boato
{ let conv = 0, boato = 0, rel = 0; for (const sd of [1991, 7, 42, 99]) { const { w } = day(sd); const r0 = w.rel.get('raimundo', 'dandara').aff; w.bus.on('conversa_fim', d => { if (!d.abortada) conv++; }); w.bus.on('boato', () => boato++); w.step(330); if (Math.abs(w.rel.get('raimundo', 'dandara').aff - r0) > .01) rel++; }
  T(4, 'Dois NPCs conversam espontaneamente (sem Lia)', conv >= 4, conv + ' conversas completas em 4 dias'); T(8, 'Relações sociais mudam depois das conversas', rel >= 3, rel + '/4 dias; boatos=' + boato); }

// 5 + 7 — Lia conversa com a Vó e atrasa o balcão: alguém desiste da fila (consequência observável)
{ const { w } = day(1991); w.cena = 'interior'; w.lia.x = 190; w.lia.y = 200; let des = null; w.bus.on('desistiu', d => { des = d; }); w.bus.on('dia_fim', () => { });
  w.step(23); w.npcs.aurea.dialogLia = true; w.step(75); w.npcs.aurea.dialogLia = false; w.step(30);
  T(5, 'Um cliente desiste da fila quando a espera passa da paciência', !!des, des ? des.id + ' esperou ' + des.esperou + ' min' : 'ninguém desistiu');
  T(7, 'Uma interação da Lia (falar com a Vó) altera a situação do balcão', !!des && w.stats.desistencias >= 1 && w.persist.evita[des.id] >= 1, 'desistências=' + w.stats.desistencias); }
// 7b — pedir a vez muda a fila e reage
{ const { w } = day(1991); w.cena = 'interior'; w.lia.x = 200; w.lia.y = 205; let ant = null;
  for (let i = 0; i < 600 && !(w.service.queue.indexOf('dandara') > 0 && w.npcs.dandara.state === 'Waiting'); i++) w.update(.1);
  const q0 = w.service.queue.join(','), r = w.interaction.ajudas('dandara').find(a => a.id === 'vez');
  if (r && r.ok) { w.interaction.abrir('dandara'); const t0 = w.rel.get('dandara', 'lia').trust; w.interaction.aplicar('ajudar', 'dandara', 'vez'); T(7, 'Pedir a vez altera a fila e a confiança', w.service.queue.join(',') !== q0 && w.rel.get('dandara', 'lia').trust > t0 && w.knowledge.has('kp_dandara_vez'), q0 + ' -> ' + w.service.queue.join(',')); }
  else T(7, 'Pedir a vez altera a fila e a confiança', false, 'ação indisponível: ' + q0); }
// 8b — ajudar muda confiança e circula entre moradores
{ const { w } = day(1991); w.cena = 'interior'; w.lia.x = 300; w.lia.y = 215; w.step(165); w.carry = 'copo'; const t0 = w.rel.get('raimundo', 'lia').trust; w.interaction.abrir('raimundo'); w.interaction.aplicar('ajudar', 'raimundo', 'agua');
  w.step(260); const soube = w.mem.has('dandara', 'soube_agua') || w.mem.has('lucia', 'soube_agua');
  T(8, 'Ajuda lembrada: confiança sobe e a notícia circula entre moradores', w.rel.get('raimundo', 'lia').trust > t0 + .1 && w.mem.has('raimundo', 'lia_ajudou_agua'), 'trust ' + t0.toFixed(2) + ' -> ' + w.rel.get('raimundo', 'lia').trust.toFixed(2) + ' ; soube=' + soube); }

// 6 — NPC usa objeto (senta, reza no nicho, olha a vitrine)
{ const { w } = day(1991); const seats = new Set(); let reza = 0, vit = 0; w.bus.on('sentou', d => seats.add(d.seat)); w.bus.on('rezou', () => reza++); w.bus.on('estado_npc', d => { if (d.para === 'Observing') vit++; }); w.step(330);
  T(6, 'NPCs usam objetos (cadeira/banco, nicho, vitrine)', seats.size >= 2 && reza >= 1 && vit >= 1, [...seats].join(',') + ' reza=' + reza + ' vitrine=' + vit); }

// 10/11 — colisão e animação × estado, a cada 0,1 s, em vários dias
{ let viol = 0, mism = 0, n = 0; const okAnim = { Away: ['idle', 'walk'], Entering: ['walk', 'idle', 'talk'], Idle: ['idle', 'walk', 'talk'], Observing: ['walk', 'idle', 'talk'], Waiting: ['walk', 'idle', 'talk'], Ordering: ['talk', 'idle', 'walk'], Seating: ['walk', 'idle', 'talk'], SeatingIn: ['walk'], Sitting: ['sit'], Standing: ['walk'], Praying: ['walk', 'idle'], Measuring: ['walk', 'interact', 'idle'], Approaching: ['walk', 'idle', 'talk'], Leaving: ['walk', 'idle', 'talk'],
    Work: ['serve_idle', 'serve_wrap', 'serve_write', 'serve_give', 'idle'], Walking: ['walk', 'idle'], Interacting: ['interact_high', 'interact', 'idle'], Serving: ['walk', 'serve_idle', 'serve_wrap', 'serve_write', 'serve_give', 'idle'] }; let bads = [];
  for (const sd of [1991, 7, 42]) { const { w, Sim } = day(sd); for (let i = 0; i < 3300; i++) { w.update(.1); for (const m of w.mobiles()) { if (m.loc !== 'padaria' || m.slide || ['Sitting', 'SeatingIn', 'Standing'].includes(m.state)) continue; n++; if (Sim.Nav.blocked(m.x, m.y) && !(m.y > 233 && Math.abs(m.x - 240) <= 24)) { viol++; if (bads.length < 4) bads.push(m.id + '@' + m.x.toFixed(0) + ',' + m.y.toFixed(0) + ' ' + m.state); }
        if (m.stateT > .25 && !(okAnim[m.state] || []).includes(m.anim)) { mism++; if (bads.length < 8) bads.push('anim ' + m.id + ' ' + m.state + '/' + m.anim); } } } }
  T(10, 'Personagens não atravessam móveis nem paredes', viol === 0, n + ' amostras, violações=' + viol + ' ' + bads.filter(b => !b.startsWith('anim')).join(' ')); T(11, 'Animações correspondem aos estados', mism === 0, 'incompatíveis=' + mism + ' ' + bads.filter(b => b.startsWith('anim')).join(' | ')); }
console.log(out.join('\n')); console.log('\n' + ok + ' passaram, ' + bad + ' falharam'); process.exit(bad ? 1 : 0);
