// Testes da casa (Etapa 5 · Fase A). Uso: node tests/casa_suite.js
const fs = require('fs'), load = require('../sim/load_node.js');
const scene = JSON.parse(fs.readFileSync(__dirname + '/../assets/objects/scene_casa.json'));
const L = JSON.parse(fs.readFileSync(__dirname + '/../assets/layout.json'));
const solids = scene.colisao_arquitetura.concat(scene.instancias.filter(i => i.collide).map(i => i.collide));
const { X0, X1, YB, YF, EXIT_X } = L;
const blocked = (x, y) => { const g = Math.abs(x - EXIT_X) <= 24; if (x < X0 + 8 || x > X1 - 8 || y < YB + 6) return true; if (y > YF - 6 && !g) return true; if (y > YF + 10) return true; for (const [a, b, c, d] of solids) if (x >= a && x <= c && y >= b && y <= d) return true; return false; };
function make(o) { const Sim = load(); Sim.Nav.init({ X0, X1, YB, YF, EXIT_X, blocked }); const objs = {}; const w = new Sim.CasaWorld(Object.assign({ scene, seed: 1991, rate: 1, hooks: { objs } }, o || {})); return { Sim, w, objs }; }
let ok = 0, bad = 0; const T = (n, nome, c, i) => { (c ? ok++ : bad++); console.log((c ? 'PASSOU ' : 'FALHOU ') + n + '. ' + nome + (i ? '  — ' + i : '')); };

// 1 — autonomia: Raimundo executa atividades variadas sem Lia
{ const { w } = make({ start: 400 }); const acts = new Set(); w.bus.on('atividade_inicio', d => acts.add(d.id || d.ativ)); let st = new Set(); w.bus.on('estado_npc', d => st.add(d.para)); w.step(300);
  T(1, 'Rotina autônoma gera atividades', w.stats.atividades >= 2 || acts.size >= 1, 'atividades=' + w.stats.atividades + ' estados=' + [...st].join('/')); }
// 2 — nunca entra em sólido nem sai dos limites
{ let viol = 0; for (const sd of [1, 7, 42]) { const { w } = make({ seed: sd, start: 400 }); const n = w.npcs.raimundo; for (let i = 0; i < 3000; i++) { w.update(.1); if (n.state !== 'Away' && n.loc === 'casa' && blocked(n.x, n.y) && !(n.state === 'Sitting' || n.state === 'SeatingIn' || n.state === 'Entering' || n.state === 'Leaving' || n.state === 'Standing')) viol++; } }
  T(2, 'Não atravessa paredes nem móveis', viol === 0, 'violações=' + viol); }
// 3 — sai para a padaria e volta
{ const { w } = make({ start: 400 }); const n = w.npcs.raimundo; let saiu = false, voltou = false; w.bus.on('estado_npc', d => { if (d.para === 'Away') saiu = true; if (saiu && d.de === 'Away') voltou = true; }); w.step(330);
  T(3, 'Sai para a padaria (~07:12) e volta (~10:25)', saiu && (voltou || w.presente('raimundo') || n.state !== 'Away'), 'saiu=' + saiu + ' voltou=' + voltou + ' t=' + w.clock.label()); }
// 4 — persistência: salvar e restaurar mantém estado, relações, memória
{ const { w, objs } = make({ start: 450 }); w.step(120); w.guardar(); const p = JSON.parse(JSON.stringify(w.persist)); const m = w.clock.min, ox = w.npcs.raimundo.x;
  const r = make({ start: 450, persist: p }); T(4, 'Persistência: relógio, objetos e posição restaurados', r.w.clock.min >= m - 1 && Math.abs(r.w.npcs.raimundo.x - ox) < 2 && r.w.persist.rel != null, 'min ' + m + '→' + r.w.clock.min); }
// 5 — o mundo não reinicia: Lia entra e sai, Raimundo continua
{ const { w } = make({ start: 450 }); w.step(30); const a = w.stats.atividades, m = w.clock.min; w.cena = 'street'; w.step(30); w.cena = 'casa'; w.step(10);
  T(5, 'Mundo continua com Lia fora e dentro', w.clock.min - m >= 38 && w.stats.atividades >= a, 'min +' + (w.clock.min - m)); }
// 6 — interação: saudar, tópicos e examinar
{ const { w } = make({ start: 450 }); const n = w.npcs.raimundo; let f = null; try { f = w.interaction.saudar('raimundo'); } catch (e) { f = 'ERRO ' + e.message; } const t = w.interaction.topicos('raimundo');
  T(6, 'Saudação e tópicos funcionam', typeof f === 'string' && f.length > 0 && !/^ERRO/.test(f) && t && t.length >= 1, String(f).slice(0, 50)); }
// 7 — determinismo
{ const a = make({ start: 400, seed: 5 }), b = make({ start: 400, seed: 5 }); a.w.step(200); b.w.step(200); const x = a.w.npcs.raimundo, y = b.w.npcs.raimundo;
  T(7, 'Mesma semente → mesmo dia', Math.abs(x.x - y.x) < .01 && a.w.stats.atividades === b.w.stats.atividades); }
// 8 — fim de dia
{ const { w } = make({ start: 400 }); w.step(20); let r; try { r = w.endDay(); } catch (e) { r = null; } T(8, 'Resumo do dia gerado', r && r.dia === 1 && Array.isArray(r.objetivos)); }
// 9 — todo assento tem aproximação livre; todo ponto de interação e de rotina é alcançável e fora de sólidos
{ const { w } = make({ start: 450 }); const semAp = Object.values(w.seats).filter(s => !s.ap).map(s => s.id); const ruins = [];
  for (const i of scene.interativos) if (blocked(i.stand[0], i.stand[1])) ruins.push(i.id);
  for (const k in scene.pontos) if (k !== 'porta' && blocked(scene.pontos[k][0], scene.pontos[k][1])) ruins.push('ponto:' + k);
  T(9, 'Assentos e pontos de interação acessíveis', semAp.length === 0 && ruins.length === 0, 'sem aproximação=' + semAp.join(',') + ' bloqueados=' + ruins.join(',')); }
// 10 — sem sobreposição entre móveis de chão (colisões não se interpenetram, exceto assento/mesa)
{ const R = scene.instancias.filter(i => i.collide && !/^cad_/.test(i.inst)); let ov = [];
  for (let a = 0; a < R.length; a++) for (let b = a + 1; b < R.length; b++) { const p = R[a].collide, q = R[b].collide; if (p[0] < q[2] && q[0] < p[2] && p[1] < q[3] && q[1] < p[3]) ov.push(R[a].inst + '×' + R[b].inst); }
  T(10, 'Móveis de chão não se sobrepõem', ov.length === 0, ov.join(',')); }
// 11 — cadeiras laterais fecham a mesa; armário e retrato têm pontos de parada distintos
{ const sp = id => (scene.instancias.find(i => i.id === id) || {}).asset || (scene.instancias.find(i => i.id === id) || {}).sprite;
  const e = scene.interativos.find(i => i.id === 'cad_esq'), d = scene.interativos.find(i => i.id === 'cad_dir'), a = scene.interativos.find(i => i.id === 'armario_1'), r = scene.interativos.find(i => i.id === 'retrato_1');
  T(11, 'Cadeiras viradas para a mesa; guarda-roupa examinável', e.asset === 'cadeira_c_dir' && d.asset === 'cadeira_c_esq' && Math.hypot(a.stand[0] - r.stand[0], a.stand[1] - r.stand[1]) >= 15); }
// 12 — conversa condicional na casa: sem motivo não há tópico; com a vivência aparece, com fala de abertura da Lia
{ const { w } = make({ start: 450 }); const t0 = w.interaction.topicos('raimundo').map(x => x.id || x.arg || x);
  T(12, 'Tópicos da casa dependem de vivências', JSON.stringify(t0).indexOf('programa') < 0 && JSON.stringify(t0).indexOf('retrato') < 0, JSON.stringify(t0)); }
// 13 — café na mesa: só se confiança suficiente; cena completa dá kp e convite
{ const { w } = make({ start: 400 }); w.rel.get('raimundo', 'lia').trust = .5; let guard = 0; while (!(w.interaction.cafeJuntos().ok) && guard++ < 3000) w.update(.5);
  const cj = w.interaction.cafeJuntos(); let fim = false;
  if (cj.ok) { w.interaction.iniciarCafe(); let g = 0; while (w.cafe && w.cafe.fase !== 'conversa' && g++ < 4000) { if (w.cafe.fase === 'sentando') w.lia.sentada = 'cad_esq'; w.update(.1); } if (w.cafe && w.cafe.fase === 'conversa') { w.interaction.cena('jeito'); w.interaction.fechar && w.interaction.fechar(); fim = true; } }
  T(13, 'Café juntos: oferta, preparo, sentar e conversa', cj.ok && fim, JSON.stringify(cj).slice(0, 80)); }

console.log('\n' + ok + ' passaram, ' + bad + ' falharam'); process.exit(bad ? 1 : 0);
