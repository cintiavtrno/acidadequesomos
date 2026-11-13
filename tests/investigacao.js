// Revisão de gameplay das 29 pistas de 1991: três perfis de jogador simulados em Node.
//   node tests/investigacao.js [sementes=4] [--relatorio]
// Os perfis não conhecem o gabarito: escolhem alvos ao acaso, com o tempo gasto em cada ação.
// Limite do modelo: a Lia é posta ao lado do alvo (sem andar), então o tempo de caminhada não entra; o navegador valida o resto.
const load = require('../sim/load_node.js'), fs = require('fs');
const scene = JSON.parse(fs.readFileSync(__dirname + '/../assets/street6/scene_rua.json'));
const NSEM = +(process.argv[2] || 4), REL = process.argv.includes('--relatorio');
let pass = 0, fail = 0; const ok = (n, c, x) => { c ? pass++ : fail++; console.log((c ? 'PASS ' : 'FAIL ') + n + (x !== undefined ? ' · ' + x : '')); };

const RATE = +process.env.RATE || +(/ANO === 1994 \? 0\.5 : ([\d.]+)/.exec(fs.readFileSync(__dirname + '/../mundo/shell_template.html', 'utf8')) || [0, 1.5])[1];   // min de jogo por segundo real
const sec = x => x * RATE;   // segundos reais de jogador -> minutos de jogo
const S0 = load(), RD0 = S0.Rua.D, KS = Object.keys(RD0.kp), META = RD0.kpMeta;
const CENTRAIS = KS.filter(k => META[k].cat === 'central');
const FIOS = { medicao: ['kp_lucia_medir', 'kp_ray_sobrado', 'kp_obj_quadro'], programa: ['kp_programa', 'kp_lucia_programa', 'kp_obj_quadro'], associacao: ['kp_associacao', 'kp_obj_quadro'], olhares: ['kp_rua_olhar'] };
const OBJS = ['mesa_domino', 'quadro_avisos', 'orelhao_1', 'poste_1', 'cavalete_pao', 'bike_1', 'lixeira_1', 'obra_1', 'caixote_1', 'gaiola_1'];
const IDS = Object.keys(RD0.pessoas);

function rngFn(seed) { let a = seed >>> 0 || 1; return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

function jogar(perfil, seed) {
  const S = load(), RD = S.Rua.D, w = new S.Rua.World({ scene, seed, rate: RATE, integrado: true }); w.initNav && w.initNav();   // integrado: agenda do dia todo (7h–19h), como no jogo
  const upd = w.update.bind(w); w.update = dt => { for (const k of ['raimundo:casa', 'raimundo:padaria', 'dandara:padaria', 'lucia:padaria']) w.lib[k] = true; upd(dt); };   // os outros ambientes liberam as pessoas na hora marcada
  const R = rngFn(seed * 7919 + perfil.length), pick = a => a[Math.floor(R() * a.length)];
  const log = { repetidas: 0, semAssunto: 0, semAssuntoSemDica: 0, reservas: 0, conversas: 0 };
  const vis = id => { const n = w.npcs[id]; return n && n.state !== 'Away' && n.alpha > .6; };
  const visiveis = () => IDS.filter(vis);
  const passo = (alvo, minutos) => {   // fica ao lado do alvo enquanto o tempo corre
    const fim = w.clock.min + minutos;
    while (w.clock.min < fim && w.clock.min < 1135) { if (alvo) { w.lia.x = alvo.x - 14; w.lia.y = alvo.y + 1; w.lia.seat = w.lia.seat; } w.update(.1); }
  };
  const falar = (id, modo) => {
    passo(null, sec(8));   // caminhada até a pessoa
    const n = w.npcs[id]; if (!vis(id)) return; w.lia.x = n.x - 14; w.lia.y = n.y + 1; passo(n, sec(1));
    const c = w.abrirConversa(id); if (!c) return; log.conversas++;
    if (modo === 'so_cumprimentar') { passo(n, sec(6)); return; }
    if (R() < .15 && modo === 'livre') { w.escutar(id); passo(n, sec(8)); return; }
    const tops = w.topicos(id);
    if (!tops.length) { log.semAssunto++; if (!w.pendencia(id)) log.semAssuntoSemDica++; passo(n, sec(6)); return; }
    const novos = tops.filter(t => !t.feito); const t = modo === 'livre' ? pick(tops) : (novos[0] || tops[0]);
    const antes = Object.keys(w.kp).length, out = w.perguntar(id, t.id);
    if (process.env.DEBUG === id) console.log(Math.floor(w.clock.min/60)+':'+String(Math.floor(w.clock.min%60)).padStart(2,'0'), id, t.id, 'nivel', w.nivel(id), 'trust', w.trust[id].toFixed(2), '->', out.map(l => (l.texto||'').slice(0,40)).join(' | '));
    if (out.some(l => l.quem === id && RD.repete.includes(l.texto))) log.repetidas++;
    if (out.some(l => l.nota && l.texto === RD.reservaGen) || out.some(l => l.quem === id && Object.values(RD.reserva[id] || {}).includes(l.texto))) log.reservas++;
    passo(n, sec(10));
  };
  const examinar = o => { const it = scene.inst.find(i => i.id === o) || { id: o, nome: o }; w.examinar(Object.assign({ desc: 'x', nome: o }, it)); };
  const gato = () => { passo(null, sec(8)); passo(w.gato, sec(3)); w.afagar && w.afagar(); };

  const T0 = 7 * 60, TF = 18 * 60 + 50;
  if (perfil === 'livre') {   // explora sem guia: alvo ao acaso, 3 min por ação
    while (w.clock.min < TF) {
      const r = R();
      if (r < .6) { const v = visiveis(); if (v.length) { falar(pick(v), 'livre'); continue; } }
      else if (r < .85) { passo(null, sec(8)); examinar(pick(OBJS)); passo(null, sec(4)); continue; }
      else if (r < .93) { gato(); continue; }
      else if (r < .98) { const mesa = { x: RD.mesa.x + 14, y: S.Rua.D.yw(RD.mesa.x) + 15 }; passo(null, sec(8)); passo(mesa, sec(12)); continue; }
      else { const livre = RD.ordem.find(s => !w.assentos[s].ocup); if (livre && (w.nivel('ze') >= 1 || w.liaConvidada)) { w.mesa.liaSenta(livre); w.lia.sentada = true; passo(null, sec(30)); w.mesa.liaLevanta(); continue; } }
      passo(null, sec(2));
    }
  } else if (perfil === 'conversador') {   // vai à pessoa que está na rua e foi menos ouvida; uma pergunta por visita; não examina objetos nem afaga o gato
    const visitas = {};
    while (w.clock.min < TF) {
      const v = visiveis(); if (!v.length) { passo(null, sec(5)); continue; }
      v.sort((a, b) => (visitas[a] || 0) - (visitas[b] || 0) || (R() - .5));
      const id = v[0]; visitas[id] = (visitas[id] || 0) + 1; falar(id, 'ordenado');
    }
  } else if (perfil === 'observador') {   // examina tudo, observa o que acontece, conversa só com três pessoas
    for (const o of OBJS) { passo(null, sec(8)); examinar(o); }
    gato();
    const escolhidos = []; while (escolhidos.length < 3) { const x = pick(IDS); if (!escolhidos.includes(x)) escolhidos.push(x); }
    let k = 0;
    while (w.clock.min < TF) {
      const mesa = { x: RD.mesa.x + 14, y: S.Rua.D.yw(RD.mesa.x) + 15 };
      if (k % 4 === 0) { passo(null, sec(8)); passo(mesa, sec(15)); }   // fica olhando a mesa de vez em quando
      else { const id = escolhidos[k % 3]; if (vis(id)) { falar(id, k % 2 ? 'so_cumprimentar' : 'ordenado'); } else passo(null, sec(5)); }
      k++; passo(null, sec(15));
    }
  }
  return { kp: Object.keys(w.kp), log, w, viv: Object.keys(w.viv), por: Object.fromEntries(Object.entries(w.kp).map(([k, v]) => [k, v.por])) };
}

const perfis = ['livre', 'conversador', 'observador'], res = {};
for (const p of perfis) { res[p] = []; for (let s = 1; s <= NSEM; s++) res[p].push(jogar(p, 100 + s)); }

const resumo = {};
for (const p of perfis) {
  const rs = res[p], n = rs.length, mediaKp = rs.reduce((a, r) => a + r.kp.length, 0) / n;
  const cent = rs.map(r => CENTRAIS.filter(k => r.kp.includes(k)).length), mediaC = cent.reduce((a, b) => a + b, 0) / n;
  const fios = rs.map(r => Object.keys(FIOS).filter(f => FIOS[f].some(k => r.kp.includes(k))).length);
  const freq = {}; for (const k of KS) freq[k] = rs.filter(r => r.kp.includes(k)).length / n;
  const soma = f => rs.reduce((a, r) => a + r.log[f], 0) / n;
  resumo[p] = { mediaKp, mediaC, minC: Math.min(...cent), fios, freq, repetidas: soma('repetidas'), semAssunto: soma('semAssunto'), semAssuntoSemDica: soma('semAssuntoSemDica'), reservas: soma('reservas'), conversas: soma('conversas') };
  console.log(`\n[${p}] sementes ${n} · pistas ${mediaKp.toFixed(1)}/29 · centrais ${mediaC.toFixed(1)}/${CENTRAIS.length} (mín ${Math.min(...cent)}) · fios da história (de 4): ${fios.join(',')} · conversas ${soma('conversas').toFixed(0)} · sem assunto ${soma('semAssunto').toFixed(1)} (sem dica ${soma('semAssuntoSemDica').toFixed(1)}) · repetições ${soma('repetidas').toFixed(1)} · reservas ${soma('reservas').toFixed(1)}`);
  const perdidas = KS.filter(k => freq[k] < .5).map(k => k.replace('kp_', '') + ' ' + Math.round(freq[k] * 100) + '%');
  console.log('   achadas em menos da metade das partidas: ' + (perdidas.join(', ') || 'nenhuma'));
}
if (REL) fs.writeFileSync('/tmp/investigacao_resumo.json', JSON.stringify(resumo, null, 1));

// critérios de experiência (pisos observados com folga; os perfis são grosseiros, então os números absolutos são conservadores)
for (const p of perfis) {
  const R = resumo[p], f3 = R.fios.filter(f => f >= 3).length / R.fios.length;
  ok(`${p}: em pelo menos 85% das partidas entende três ou quatro dos quatro fios da história principal (medição, Programa, associação, olhares), e nunca menos de dois`, f3 >= .85 && Math.min(...R.fios) >= 2, Math.round(f3 * 100) + '% · ' + R.fios.join(','));
}
ok('conversador: em média pelo menos 4 das 7 pistas centrais', resumo.conversador.mediaC >= 4, resumo.conversador.mediaC.toFixed(1));
ok('livre: em média pelo menos 2,5 das 7 pistas centrais (explora ao acaso, sem guia)', resumo.livre.mediaC >= 2.5, resumo.livre.mediaC.toFixed(1));
ok('observador (só objetos + 3 pessoas): ao menos a pista do quadro, que conta o Programa e a reunião', res.observador.every(r => r.kp.includes('kp_obj_quadro')));
ok('nenhum perfil fica sem assunto e sem dica ao mesmo tempo', perfis.every(p => resumo[p].semAssuntoSemDica === 0), perfis.map(p => resumo[p].semAssuntoSemDica).join(','));
ok('repetir pergunta não rende confiança: depois de ouvir as duas respostas de Seu Zé sobre o jogo, perguntar de novo não muda o nível de confiança', (() => {
  const S = load(), w = new S.Rua.World({ scene, seed: 9, rate: 1.5 }); w.initNav && w.initNav();
  w.marcar('viu_jogo'); w.perguntar('ze', 'jogo'); w.perguntar('ze', 'jogo'); const t2 = w.trust.ze; for (let i = 0; i < 6; i++) w.perguntar('ze', 'jogo'); return Math.abs(w.trust.ze - t2) < 1e-9;
})());
ok('a conversa certa leva ao assunto trancado: Raimundo conta "a mesa do pai" depois de três assuntos diferentes, sem repetir nenhum', (() => {
  const S = load(), w = new S.Rua.World({ scene, seed: 9, rate: 1.5 }); w.initNav && w.initNav();
  w.trust.raimundo = .3; w.marcar('viu_jogo'); w.marcar('viu_medicao'); w.perguntar('raimundo', 'rua'); w.perguntar('raimundo', 'jogo'); w.perguntar('raimundo', 'sobrado'); w.perguntar('raimundo', 'jogo'); return !!w.kp.kp_dom_pai;
})());
ok('a pista trancada dá sinal natural: Raimundo, ainda cerimonioso, responde que o assunto tem mais história', (() => {
  const S = load(), w = new S.Rua.World({ scene, seed: 9, rate: 1.5 }); w.initNav && w.initNav();
  w.trust.raimundo = .3; w.marcar('viu_jogo'); w.perguntar('raimundo', 'jogo'); const o = w.perguntar('raimundo', 'jogo'); return o.some(l => l.quem === 'raimundo' && /história/.test(l.texto)) && !w.kp.kp_dom_pai;
})());
ok('quem só viu o aviso do Programa no quadro já consegue perguntar à Lúcia e a Seu Raimundo, com pergunta que cabe no que viu', (() => {
  const S = load(), w = new S.Rua.World({ scene, seed: 9, rate: 1.5 }); w.initNav && w.initNav();
  w.examinar({ id: 'quadro_avisos', nome: 'q', desc: 'x' }); w.update(.1); const a = w.perguntar('lucia', 'medir'), b = w.perguntar('raimundo', 'sobrado');
  return !!w.kp.kp_lucia_medir && !!w.kp.kp_ray_sobrado && /ouvi dizer/i.test(a[0].texto) && /ouvi dizer/i.test(b[0].texto);
})());
ok('o diário registra quem deu a informação e as hipóteses; curiosidade some quando a anotação é feita', (() => {
  const S = load(), w = new S.Rua.World({ scene, seed: 9, rate: 1.5 }); w.initNav && w.initNav();
  w.marcar('viu_medicao'); let d = w.diario(); const tinha = d.acontecimentos.some(c => c.id === 'c_medicao');
  w.perguntar('lucia', 'medir'); w.perguntar('bela', 'rua'); d = w.diario(); const n = d.notas.find(x => x.id === 'kp_lucia_medir');
  return tinha && !d.acontecimentos.some(c => c.id === 'c_medicao') && n.por && n.por.quem === 'lucia' && d.hipoteses.length === 1;
})());

console.log(`\n${pass} passaram, ${fail} falharam`); process.exit(fail ? 1 : 0);
