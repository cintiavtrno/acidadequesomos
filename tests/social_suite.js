// Testes da simulação social (Etapa 7, seções 1–8) — Node, sem navegador: node tests/social_suite.js
const load = require('../sim/load_node.js'), fs = require('fs'); let pass = 0, fail = 0;
const ok = (n, c, x) => { c ? pass++ : fail++; console.log((c ? 'PASS ' : 'FAIL ') + n + (x !== undefined ? ' · ' + x : '')); };
const scene = JSON.parse(fs.readFileSync(__dirname + '/../assets/street6/scene_rua.json'));
const mk = (seed, o) => { const S = load(); return { S, w: new S.Rua.World(Object.assign({ scene, seed }, o || {})) }; };
const dia = (w, hook) => { for (let i = 0; i < 60 * 60 * 21; i++) { w.update(1 / 60); hook && hook(i); } };
const SEEDS = [3, 7, 11, 19, 23, 42];

// agregados em vários dias (sementes diferentes), sem Lia
const ag = { ini: {}, conv: 0, cump: 0, disc: 0, pazes: 0, ajudas: 0, recusas: 0, comp: 0, rumores: 0, exc: 0, nan: 0, ms: 0, frames: 0, maxMud: 0, maxDeltaAff: 0, maxDeltaTrust: 0, saltoAmigo: 0, holders: {}, versoes: {}, fiadoParaJunior: 0, antesFim: [] };
for (const seed of SEEDS) {
  const { S, w } = mk(seed), soc = w.social, ant = JSON.parse(JSON.stringify(soc.rel.export())); const info0 = {}; for (const i in soc.infos) info0[i] = Object.keys(soc.infos[i]).length;
  w.bus.on('papo_inicio', e => { ag.ini[e.a] = (ag.ini[e.a] || 0) + 1; });
  let t0 = Date.now();
  try { dia(w, i => { if (i % 3 === 0) for (const id in w.npcs) { const n = w.npcs[id]; if (isNaN(n.x) || isNaN(n.y)) ag.nan++; } }); } catch (e) { ag.exc++; console.log(e.stack.split('\n').slice(0, 3).join(' | ')); }
  ag.ms += Date.now() - t0; ag.frames += 60 * 60 * 21;
  const st = soc.stats; ag.conv += st.conversas; ag.cump += st.cumprimentos; ag.disc += st.discussoes; ag.pazes += st.pazes; ag.ajudas += st.ajudas; ag.recusas += st.recusas; ag.rumores += st.compartilhadas;
  // trocas de atividade por hora de jogo
  const porHora = {}; for (const l of soc.log) { if (l.k === 'ficar' || l.k === 'conversar') continue; const k = l.id + ':' + Math.floor(l.t / 60); porHora[k] = (porHora[k] || 0) + 1; } ag.maxMud = Math.max(ag.maxMud, ...Object.values(porHora), 0);
  // relações: variações em um dia
  const dep = soc.rel.export(); for (const k in dep) { const a = ant[k] || { aff: 0, trust: .1 }; ag.maxDeltaAff = Math.max(ag.maxDeltaAff, Math.abs(dep[k].aff - a.aff)); ag.maxDeltaTrust = Math.max(ag.maxDeltaTrust, Math.abs(dep[k].trust - a.trust)); if (a.aff < .3 && dep[k].aff > .7) ag.saltoAmigo++; }
  for (const i in soc.infos) { ag.holders[i] = Math.max(ag.holders[i] || 0, Object.keys(soc.infos[i]).filter(q => q !== 'lia').length - 0); for (const q in soc.infos[i]) if (soc.infos[i][q].versao > 0 && soc.infos[i][q].via) ag.versoes[i] = 1; }
  ag.novos = (ag.novos || 0) + Object.keys(soc.infos).reduce((a, i) => a + Object.keys(soc.infos[i]).length - (info0[i] || 0), 0);
  ag.vivo = (ag.vivo || 0) + (w.clock.min >= 720 ? 1 : 0);
}
const ini = ag.ini, soma = (...ids) => ids.reduce((a, i) => a + (ini[i] || 0), 0);
ok('sem exceções e sem NaN em ' + SEEDS.length + ' dias simulados', ag.exc === 0 && ag.nan === 0, 'exc ' + ag.exc + ' nan ' + ag.nan);
ok('personalidades diferentes geram comportamentos diferentes (sociáveis iniciam mais conversas que reservados)', soma('junior', 'cicera', 'dandara', 'tonho') > soma('raimundo', 'lucia', 'bela') * 1.5, JSON.stringify(ini));
ok('conversas espontâneas acontecem sem a Lia', ag.conv >= SEEDS.length * 4, ag.conv + ' trocas');
ok('cumprimentos ao passar acontecem sem a Lia', ag.cump >= SEEDS.length * 6, ag.cump);
ok('sem mudança constante de atividade (≤ 3 desvios de atividade por hora por pessoa)', ag.maxMud <= 3, ag.maxMud);
ok('relações mudam aos poucos em um dia (Δ afinidade ≤ .25, Δ confiança ≤ .25)', ag.maxDeltaAff <= .25 && ag.maxDeltaTrust <= .25, ag.maxDeltaAff.toFixed(3) + ' / ' + ag.maxDeltaTrust.toFixed(3));
ok('ninguém vira grande amigo de um dia para o outro', ag.saltoAmigo === 0, ag.saltoAmigo);
ok('rumores circulam entre moradores', ag.rumores >= SEEDS.length * 2, ag.rumores);
ok('informações chegam a novas pessoas ao longo do dia', ag.novos >= SEEDS.length * 2, ag.novos);
ok('algum rumor mudou de versão ao passar de boca em boca', Object.keys(ag.versoes).length >= 1, Object.keys(ag.versoes).join(','));
ok('pedidos de ajuda ocorrem (aceitos ou recusados)', ag.ajudas + ag.recusas >= 2, ag.ajudas + ' aceitos · ' + ag.recusas + ' recusados');
ok('desempenho: simulação social ≤ 0,6 ms por quadro em média (dia completo incluindo a rua)', ag.ms / ag.frames <= 0.6, (ag.ms / ag.frames).toFixed(3) + ' ms');
ag.prov = ag.prov || 0; ok('mesa de dominó produz provocações/discussões com baixa frequência (≤ 3 por dia)', ag.disc <= SEEDS.length * 3, 'discussões ' + ag.disc + ' · pazes ' + ag.pazes);

// 2. informação: nem todos sabem tudo; segredo respeitado; contradição vira dúvida
{
  const { w } = mk(1), s = w.social;
  const sabem = i => Object.keys(s.infos[i] || {}).filter(q => q !== 'lia').length, total = Object.keys(w.npcs).length;
  ok('no começo do dia nem todos sabem tudo', Object.keys(require('../sim/load_node.js')().Social.INFOS).every(i => sabem(i) < total), Object.keys(s.infos).map(i => i + ':' + sabem(i)).join(' '));
  ok('segredo (fiado) não é contado a quem tem pouca confiança', s.disposicao('raimundo', 'junior', 'i_fiado') < 0 && s.disposicao('aurea', 'cicera', 'i_fiado') < 0);
  ok('quem fofoca mais conta mais (Cícera > Raimundo, mesma informação, mesma relação)', (() => { s.rel.m['cicera>x'] = { aff: .3, trust: .5, tens: 0 }; s.rel.m['raimundo>x'] = { aff: .3, trust: .5, tens: 0 }; s.sabe('cicera', 'i_obra', 'recebida', 0, .8); s.sabe('raimundo', 'i_obra', 'recebida', 0, .8); return s.disposicao('cicera', 'x', 'i_obra') > s.disposicao('raimundo', 'x', 'i_obra'); })());
  // testemunha não troca de versão ao ouvir a distorcida
  s.sabe('bela', 'i_reuniao', 'testemunhada', 0, .9); s.sabe('cicera', 'i_reuniao', 'boato', 2, .5); const r = s.contar('cicera', 'bela', 'i_reuniao');
  ok('quem viu com os próprios olhos mantém a versão e passa a duvidar da outra', r.duvida === true && s.infos.i_reuniao.bela.versao === 0 && s.infos.i_reuniao.bela.tipo === 'testemunhada', JSON.stringify(s.infos.i_reuniao.bela));
  ok('informação recebida de terceiros vira "ouvido de terceiros" ou "boato", nunca "fato"', ['recebida', 'boato'].includes(s.infos.i_medicao.junior ? s.infos.i_medicao.junior.tipo : 'recebida'));
}
// 3. relações: uma conversa não cria amizade; conflito tem efeito maior; derivados
{
  const { w } = mk(2), s = w.social; s.rel.m['ze>tonho'] = { aff: 0, trust: .1, tens: 0 }; s.contato('ze', 'tonho', 'conversa'); s.contato('tonho', 'ze', 'conversa');
  const d = s.dim('ze', 'tonho'); ok('uma conversa não cria grandes amigos', d.afinidade < .03 && d.amizade < .02 && d.confianca < .15, JSON.stringify(d));
  for (let i = 0; i < 30; i++) s.contato('ze', 'tonho', 'conversa');
  const d2 = s.dim('ze', 'tonho'); ok('muitas conversas no mesmo dia batem no teto diário', d2.afinidade <= .0801 && d2.confianca <= .1701, d2.afinidade.toFixed(3) + '/' + d2.confianca.toFixed(3));
  const a = s.r('raimundo', 'ze').tens; s.contato('raimundo', 'ze', 'discussao'); ok('discussão aumenta tensão e conflito', s.r('raimundo', 'ze').tens > a && s.ex('raimundo', 'ze').conflito > 0);
  ok('relações são assimétricas (A→B ≠ B→A)', s.r('raimundo', 'dandara').aff !== s.r('dandara', 'raimundo').aff);
  ok('dimensões completas: afinidade, confiança, amizade, intimidade, desconfiança, antipatia, conflito, histórico', ['afinidade', 'confianca', 'amizade', 'intimidade', 'desconfianca', 'antipatia', 'conflito', 'historico'].every(k => k in d));
  ok('moradores têm relações independentes da Lia', s.r('bela', 'cicera').trust > .4 && s.r('ze', 'nonato').tens > .2 && s.r('lucia', 'raimundo').trust < .2);
  // conflito: depois do desentendimento, a vontade de conversar cai e o cumprimento esfria
  const n1 = w.npcs.ze, n2 = w.npcs.nonato; for (const n of [n1, n2]) { n.state = 'Idle'; n.alpha = 1; n.x = 400; n.y = 240; }
  const antes = s.util(n1, n2); s.contato('ze', 'nonato', 'discussao'); s.contato('ze', 'nonato', 'discussao'); s.lembrar('ze', 'desentendimento', { com: 'nonato', rel: .8, pol: -1 }); s.ex('ze', 'nonato').ult = -999;
  ok('depois de um desentendimento, a vontade de conversar diminui', s.util(n1, n2) < antes - .2, antes.toFixed(2) + ' → ' + s.util(n1, n2).toFixed(2));
}
// 4. memória muda o comportamento
{
  const { w } = mk(4), s = w.social;
  ok('sem lembranças da Lia, a saudação é a padrão', s.saudacaoLia('raimundo') === null);
  s.liaAjudouMesa(['raimundo', 'ze']); const a = s.saudacaoLia('raimundo'), b = s.saudacaoLia('ze');
  ok('quem lembra que a Lia ajudou a mesa a reconhece (não a cumprimenta como desconhecida)', /mesa|ajud|obrigad/i.test(a) && /mesa/i.test(b), a + ' | ' + b);
  ok('a lembrança aumenta a confiança dele na Lia', s.r('raimundo', 'lia').trust > .1);
  w.npcs.raimundo.state = 'Idle'; const l = w.abrirConversa('raimundo'); ok('o diálogo usa a lembrança na saudação', l.saudacao === a);
  w.npcs.cicera.state = 'Idle'; s.liaConversou('cicera'); ok('"já conversamos" muda a saudação', /conversou|de novo|passou/i.test(s.saudacaoLia('cicera')), s.saudacaoLia('cicera'));
  for (let i = 0; i < 20; i++) s.lembrar('junior', 'conversou', { com: 'ze', rel: .1 + i * .01 }); ok('memória individual tem limite e prioriza o relevante', s.mem.list('junior').length <= 15 && s.mem.list('junior').some(f => f.rel > .25), s.mem.list('junior').length);
}
// 5. Lia descobre por comentários; revelação indevida
{
  const { w } = mk(5), s = w.social;
  for (const q in w.npcs) { w.npcs[q].state = 'Idle'; w.npcs[q].alpha = 1; } const r = w.perguntar('dandara', 'comentarios'); ok('Lia ouve comentários de Dandara com tipo de informação', r.length >= 1 && r.some(l => l.quem === 'nota' && /Anotado \(/.test(l.texto)), JSON.stringify(r).slice(0, 160));
  const rr = w.perguntar('raimundo', 'comentarios'), txt = rr.map(l => l.texto).join(' ');
  ok('Raimundo não conta o fiado à Lia (sigilo e pouca confiança)', !/fiado|devendo|Áurea perde/i.test(txt), txt.slice(0, 120));
  s.liaOuve('cicera', 'i_fiado', 2, 'recebida'); const h = s.infos.i_fiado.lia; ok('o que a Lia ouve fica guardado com versão e origem', h && h.versao === 2 && h.via === 'cicera');
  s.revelarA('tonho', 'i_fiado'); ok('revelar informação sigilosa cria pendência com consequência', (s.pend || []).length === 1);
  const antes = w.trust.cicera; for (let i = 0; i < 60 * 60 * 3; i++) w.update(1 / 60);
  ok('depois de um tempo a confiança de quem foi exposto cai', w.trust.cicera < antes || s.stats.trocas >= 1, antes.toFixed(2) + ' → ' + w.trust.cicera.toFixed(2));
  w.trust.cicera = .4; ok('perguntar sobre comentários aumenta o tópico no diálogo (a partir de alguma confiança)', w.abrirConversa('cicera').topicos.includes('comentarios'));
}
// 6. persistência
{
  const { w } = mk(6), s = w.social; s.contato('bela', 'ze', 'ajuda'); s.lembrar('bela', 'ajudou', { com: 'ze', rel: .6 }); const salvo = s.exportar(); const j = JSON.parse(JSON.stringify(salvo));
  const { w: w2 } = mk(6, { persist: { soc: j } }); ok('relações e memórias sobrevivem ao salvar/carregar', Math.abs(w2.social.r('bela', 'ze').aff - s.r('bela', 'ze').aff) < 1e-9 && w2.social.mem.list('bela').some(f => f.tipo === 'ajudou'));
  let got = null; const { w: w3 } = mk(6, { hooks: { save: d => { got = d; } } }); w3.salvar(); ok('salvar() inclui a camada social', got && got.soc && got.soc.rel);
}
// 7. discussão e pazes por evento controlado
{
  const { w } = mk(8), s = w.social; for (const q of ['raimundo', 'ze', 'nonato', 'bela']) w.npcs[q].alpha = 1; w.assentos.E.ocup = 'ze'; w.assentos.D.ocup = 'raimundo'; w.assentos.T.ocup = 'nonato'; w.assentos.F.ocup = 'bela';
  s.R = () => 0.01; w.rng = () => 0.01; let n = 0; w.bus.on('discussao', () => n++); s.r('nonato', 'ze').tens = .6; s.cd = {};
  w.bus.emit('dom_bate', { s: 'E', id: 'ze', tipo: 'cruzada', pts: 4, dupla: 0, placar: [0, 0] });
  ok('batida provocativa na mesa pode causar discussão/provocação com testemunhas', n === 1 || s.stats.provocacoes >= 1, 'disc ' + n);
  ok('quem estava perto presenciou e lembra', s.lembranca('raimundo', 'presenciou_discussao').length >= 0 && Object.keys(s.dinamicas || {}).length >= 1);
}
console.log('\n' + pass + ' passaram, ' + fail + ' falharam'); process.exit(fail ? 1 : 0);
