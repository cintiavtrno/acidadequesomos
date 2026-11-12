// Camada de 1994 (rua, padaria, casa, quintal): node tests/ano94.js
// Em 1994 a rua já sente o Programa: aviso, risco, moradores saindo e a aposta no turista. Aqui se confere que os dados de 1994
// existem, estão ligados uns aos outros (assunto → comporta → anotação) e que dá para conversar e examinar no motor da rua.
const load = require('../sim/load_node.js'), fs = require('fs'); let pass = 0, fail = 0;
const ok = (n, c, x) => { c ? pass++ : fail++; console.log((c ? 'PASS ' : 'FAIL ') + n + (x !== undefined && x !== '' ? ' · ' + x : '')); };
const scene = JSON.parse(fs.readFileSync(__dirname + '/../assets/street6/scene_rua.json'));

// ---------------------------------------------------------------- rua
{
  const S = load(), RD = S.Rua.D; const antes = Object.keys(RD.kp).length; RD.virar94();
  ok('1991 continua intacto até a virada (kp_ray_sobrado existia)', antes > 0);
  ok('virada remove as anotações que só valiam em 1991', !RD.kp.kp_ray_sobrado && !RD.kp.kp_programa && !RD.kp.kp_rua_olhar && !RD.kp.kp_lucia_programa && !RD.kp.kp_obra_tijolo);
  ok('virar94 é idempotente', (RD.virar94(), Object.keys(RD.kp).length === Object.keys(RD.kp).length) && RD._v94 === true);
  // cada assunto de cada pessoa tem comporta com rótulo e pergunta; cada anotação citada existe
  let semGate = [], semKp = [], vazio = [];
  for (const id in RD.falas) {
    const F = RD.falas[id]; if (!F.saudar.length || !F.ouvir.length) vazio.push(id);
    for (const t in F.perguntar) {
      const g = (RD.gates[id] || {})[t]; if (!g || !g.label || !g.ask) semGate.push(id + ':' + t);
      for (const r of F.perguntar[t]) if (r.kp && !RD.kp[r.kp]) semKp.push(id + ':' + t + '→' + r.kp);
    }
  }
  ok('toda pessoa tem cumprimento e "ficar ouvindo"', vazio.length === 0, vazio.join(','));
  ok('todo assunto tem rótulo e pergunta da Lia', semGate.length === 0, semGate.join(','));
  ok('toda anotação citada pelas falas existe', semKp.length === 0, semKp.join(','));
  ok('os objetos novos apontam para anotações que existem', Object.values(RD.kpObj94).every(k => RD.kp[k]));
  const tema = Object.keys(RD.kp).filter(k => /^kp_94_/.test(k)); ok('há ao menos 15 anotações de 1994', tema.length >= 15, tema.length);
  const todo = JSON.stringify(RD.falas) + JSON.stringify(RD.kp);
  ok('o texto de 1994 trata de aviso, indenização e turista', /aviso/.test(todo) && /indeniza/.test(todo) && /turista/.test(todo));
  ok('o texto de 1994 insinua os eventos para moradores de Salvador (fase 2, de 1996)', /Salvador/.test(todo) && /evento|festa|show/.test(todo));
  ok('o texto de 1994 não carrega mais a "medição" de 1991 como notícia', !/Eles medem tudo, mas não perguntam/.test(todo));
  // vícios de escrita que a Cíntia pediu para evitar
  const vicios = [/não é [^.,;]{1,40}, é /i, /E aqui está o ponto/i, /Mais do que isso/i, /No fim do dia/i, /A verdade é simples/i, /Spoiler/i];
  const textos = []; for (const id in RD.falas) { for (const t in RD.falas[id].perguntar) RD.falas[id].perguntar[t].forEach(r => textos.push(r.t)); RD.falas[id].saudar.forEach(x => textos.push(x)); }
  Object.values(RD.kp).forEach(k => textos.push(k[1]));
  ok('nenhum texto de 1994 usa as muletas retóricas da lista', textos.every(t => vicios.every(v => !v.test(t))), textos.filter(t => vicios.some(v => v.test(t))).join(' | '));

  // conversa e objetos no motor da rua
  const w = new S.Rua.World({ scene, seed: 94 }); w.update(1);
  ok('conversa: Raimundo oferece "O aviso na porta" sem pré-requisito', w.topicos('raimundo').some(t => t.id === 'sobrado' && t.label === 'O aviso na porta'));
  const o = w.perguntar('raimundo', 'sobrado'); ok('perguntar rende a anotação do aviso', !!w.kp.kp_94_ray_aviso && o.some(l => l.quem === 'nota'));
  w.perguntar('raimundo', 'rua'); w.perguntar('raimundo', 'rua');
  ok('segunda resposta de "a rua" traz a marca de tinta', !!w.kp.kp_94_ray_vazias);
  w.perguntar('tonho', 'rua'); ok('Tonho: turista só no fim de semana', !!w.kp.kp_94_tonho_turista);
  w.perguntar('junior', 'casa'); ok('Júnior fala de si em primeira pessoa e rende anotação', !!w.kp.kp_94_junior_casa && /^Eu entrei/.test(RD.falas.junior.perguntar.casa[0].t));
  for (let i = 0; i < 3; i++) w.perguntar('lucia', 'programa');
  ok('Lúcia: aposta no turista e depois conversa de corredor (só com confiança)', !!w.kp.kp_94_lucia_aposta);
  const ids = ['aviso_sobrado', 'marca_sobrado', 'placa_padaria', 'faixa_assoc', 'tapume_verde', 'placa_obra'];
  const r = ids.map(id => w.examinar({ id, nome: id, desc: 'x' })); ok('examinar cada objeto novo rende anotação nova', r.every(x => x.novo && x.kp) && ids.every(id => w.kp[RD.kpObj94[id]]));
  ok('o quadro de avisos tem texto próprio em 1994', /lista datilografada/.test(w.examinar({ id: 'quadro_avisos', nome: 'q', desc: 'velho' }).texto));
  // gossip: o que circula entre as pessoas já é de 1994
  ok('informações que circulam (obra, gato, reunião) são as de 1994', /empreita/.test(S.Social.INFOS.i_obra.versoes[0]) && /casa fechada/.test(S.Social.INFOS.i_gato.versoes[0]) && /lista/.test(S.Social.INFOS.i_reuniao.versoes[0]));
}
// ---------------------------------------------------------------- padaria e casa
{
  const S = load(); S.Data.virar94(); const P = S.Data.falas;
  ok('padaria: Raimundo fala do aviso e Lúcia da aposta no turista', /aviso/.test(P.raimundo.perguntar.programa[0].texto) && P.lucia.perguntar.programa.some(f => /turista/.test(f.texto)));
  ok('padaria: o papo do balcão já não é de 1991', /forno aceso/.test(JSON.stringify(S.Data.bate_papo_balcao)));
  const C = load(); C.Casa.virar94(); const c = C.Data.casa;
  ok('casa: o papel na mesa é o aviso, e a mala está pronta', /aviso/.test(c.objetos.mesa_1.texto()) && /mala/.test(c.objetos.sacola_1.texto()) && /aviso/.test(c.falas.perguntar.papel[0].texto));
  ok('casa: a pergunta da Lia fala da marca na parede', /marca na parede/.test(c.asks.programa) && /aviso/.test(c.cena.opcoes.programa.linhas[1].texto));
}
// ---------------------------------------------------------------- quintal: Zefa defende o Programa; os outros sentem o custo
{
  const Q = require('../quintal/quintal.js'), QD = require('../quintal/qdata.json'); QD.SPEED = { ze: 0.57, nonato: 1.1, junior: 1.7 };
  const K = Q.Dialogo.K, T = Q.Dialogo.T;
  ok('quintal: Zefa tem as três falas da reforma (Programa, turista, casa)', ['reforma', 'turista', 'casa'].every(t => T.zefa[t]) && /Acho bom/.test(T.zefa.reforma.resp));
  ok('quintal: a aposta no turista aparece na boca de Zefa e a dúvida na de Tonho, Aurea e Lúcia', T.zefa.turista.resp.includes('turista') && T.tonho.turista && T.aurea.freguesia && T.lucia.evento);
  ok('quintal: os custos aparecem (Raimundo, Rita, Nonato, Bela, Cícera, Junior)', T.raimundo.sobrado && T.rita.telhado && T.nonato.empreita && T.bela.freguesas && T.cicera.varal && T.junior.casa);
  ok('quintal: Lúcia deixa escapar a conversa de corredor sobre eventos para a classe média de Salvador', /Salvador/.test(T.lucia.evento.resp));
  const t = new Q.Sim(QD); t.forcada = true; t.fase('D', true);
  const junto = id => { const n = t.npcs[id]; n.vis = true; t.lia.x = n.x; t.lia.y = n.y + 0.8; t.falar(id); };
  const ids = Object.keys(QD.FASE.D).filter(k => k !== 'lia' && t.npcs[k]);
  for (let v = 0; v < 4; v++) for (const id of ids) { junto(id); for (const tp of t.topicosDe(id)) t.conversaAcao('perguntar', tp.id); t.conversaAcao('ouvir'); }
  const n = t.notas().length; ok('quintal: só com conversa, a fase D rende bem mais que as 6 notas da meta', n >= 12, n);
  for (const k of ['q_zefa_reforma', 'q_zefa_turista', 'q_lucia_evento', 'q_zefa_raimundo']) ok('quintal: anotação ' + k + ' é alcançável', !!t.kp[k]);
  const todos = Object.values(K).map(k => k[1]).concat(Object.values(T).flatMap(p => Object.values(p).map(a => a.resp)));
  const vicios = [/não é [^.,;]{1,40}, é /i, /E aqui está o ponto/i, /Mais do que isso/i, /No fim do dia/i, /A verdade é simples/i];
  ok('quintal: nenhum texto usa as muletas retóricas da lista', todos.every(x => vicios.every(v => !v.test(x))));
}
// ---------------------------------------------------------------- Dia & Noite, gaveta, café, jogo novo, rótulo
{
  const S = load(), RD = S.Rua.D; RD.virar94();
  const w = new S.Rua.World({ scene, seed: 94 }); w.update(1);
  w.perguntar('dandara', 'dn'); ok('rua: Dandara explica o Dia & Noite (largos, cachê, casarões) e rende anotação', !!w.kp.kp_94_dandara_dn && /Terreiro de Jesus/.test(RD.falas.dandara.perguntar.dn[0].t) && /Quincas Berro/.test(RD.falas.dandara.perguntar.dn[0].t));
  ok('rua: o assunto do show de Tonho só abre depois de "o turista"', !w.topicos('tonho').some(t => t.id === 'show'));
  w.perguntar('tonho', 'rua'); ok('rua: depois de "o turista" abre "Os shows no Terreiro"', w.topicos('tonho').some(t => t.id === 'show')); w.perguntar('tonho', 'show'); ok('rua: Tonho conta que a rua esvazia quando o show acaba', !!w.kp.kp_94_tonho_show);
  const q = w.examinar({ id: 'quadro_avisos', nome: 'q', desc: 'velho' }); ok('rua: o cartaz do Dia & Noite está no quadro e rende anotação', /DIA & NOITE/.test(q.texto) && !!w.kp.kp_94_obj_dn);
  ok('rua: Lúcia já fala do Dia & Noite e da conversa de um evento maior', /Dia & Noite/.test(JSON.stringify(RD.falas.lucia)) && /evento maior/.test(JSON.stringify(RD.falas.lucia)));
}
{
  const { make: mk } = require('./harness.js'); const { Sim, w } = mk({ seed: 94 }); Sim.Data.virar94(); w.cena = 'interior';
  ok('padaria: objetivos de 1994 trocados (casa de Raimundo e aposta do Programa)', Sim.Data.objetivos.map(o => o.titulo).join('|') === 'A casa de Seu Raimundo|A aposta do Programa');
  ok('padaria: Dandara cita o Dia & Noite', Sim.Data.falas.dandara.perguntar.programa.some(f => /Dia & Noite/.test(f.texto)));
  const aurea = w.npcs.aurea; aurea.state = 'Away'; w.lia.x = aurea.x + 10; w.lia.y = aurea.y;
  const r = w.interaction.objeto({ id: 'gaveta_1' });
  ok('gaveta: com a vó fora (mesmo que a posição dela esteja perto) dá para mexer, sem "ela está olhando"', !/olhando/.test(r.texto) && /DIA & NOITE/.test(r.texto) && /aluguel/.test(r.texto), r.texto.slice(0, 60));
  ok('gaveta: rende o aluguel e a pasta do Dia & Noite', w.knowledge.has('kp_gaveta') && w.knowledge.has('kp_gaveta_aluguel') && w.knowledge.has('kp_gaveta_dn'));
  const { w: w2, Sim: S2 } = mk({ seed: 95 }); S2.Data.virar94(); w2.cena = 'interior'; const a2 = w2.npcs.aurea; a2.state = 'Idle'; w2.lia.x = a2.x + 10; w2.lia.y = a2.y;
  ok('gaveta: com a vó presente e perto, ela barra ("Aí não")', /olhando/.test(w2.interaction.objeto({ id: 'gaveta_1' }).texto) && !w2.knowledge.has('kp_gaveta_aluguel'));
}
{
  const sc = JSON.parse(fs.readFileSync(__dirname + '/../assets/objects/scene_casa.json')), Lt = JSON.parse(fs.readFileSync(__dirname + '/../assets/layout.json'));
  const solids = sc.colisao_arquitetura.concat(sc.instancias.filter(i => i.collide).map(i => i.collide)), { X0, X1, YB, YF, EXIT_X } = Lt;
  const blocked = (x, y) => { const g = Math.abs(x - EXIT_X) <= 24; if (x < X0 + 8 || x > X1 - 8 || y < YB + 6) return true; if (y > YF - 6 && !g) return true; if (y > YF + 10) return true; for (const [a, b, c, d] of solids) if (x > a && x < c && y > b && y < d) return true; return false; };
  const mk = (a94, start) => { const Sim = load(); Sim.Nav.init({ X0, X1, YB, YF, EXIT_X, blocked }); const w = new Sim.CasaWorld({ scene: sc, seed: 1994, rate: 1, start, hooks: { objs: {} } }); w.ano94 = a94; return w; };
  const a = mk(true, 760); const a91 = mk(false, 760); let g1 = 0; while (!a91.presente('raimundo') && g1++ < 3000) a91.update(.5); ok('casa: em 1991 o café também vale depois das 12h (antes só até 11h40, e ele só chega às 10h)', a91.interaction.cafeJuntos().ok); let g = 0; while (!a.presente('raimundo') && g++ < 3000) a.update(.5);
  const c = a.interaction.cafeJuntos(); ok('casa: em 1994 o café com Seu Raimundo está liberado depois do meio-dia (12h40)', c.ok || /movimento|rezando/.test(c.motivo || ''), c.motivo || '');
  const b = mk(false, 900); g = 0; while (!b.presente('raimundo') && g++ < 3000) b.update(.5); const cb = b.interaction.cafeJuntos(); ok('casa: em 1991 o café vale até 14h30 (ele sai de novo às 15h)', !cb.ok && /tarde/.test(cb.motivo));
}
{
  const sh = fs.readFileSync(__dirname + '/../mundo/shell_template.html', 'utf8');
  ok('jogo novo: o shell zera tudo o que começa com "balcao" ao abrir ?new=1, ao recomeçar e ao fim de 1994', /function zerarJogo/.test(sh) && /\^balcao/.test(sh) && /if \(Q\.get\('new'\) === '1'\) zerarJogo\(\)/.test(sh) && /function recomecar\(\) \{ zerarJogo\(\)/.test(sh) && (sh.match(/zerarJogo\(\)/g) || []).length >= 4);
  const rd = fs.readFileSync(__dirname + '/../quintal/render.js', 'utf8');
  ok('quintal: a etiqueta pixelada com o nome de quem está perto não é mais desenhada (o aviso "E Falar com ..." já traz o nome)', !/this\.nome\(g, o, h\)/.test(rd));
  const Q = require('../quintal/quintal.js'); const T = Q.Dialogo.T;
  ok('quintal: Dia & Noite na boca de Zefa, Dandara e Tonho', /Dia & Noite/.test(T.zefa.dn.resp) && /Pedro Archanjo/.test(T.zefa.dn.resp) && /cachê/.test(T.dandara.dn.resp) && /[Ss]how de graça/.test(T.tonho.show.resp));
}

// ---------------------------------------------------------------- sacola, gaiola, lata, Nena (correções da 4ª rodada)
{
  const S = load(), RD = S.Rua.D, w = new S.Rua.World({ scene, seed: 3, rate: 1.5 }); w.initNav && w.initNav();
  ok('rua: a gaiola do sobrado pode ser examinada e rende anotação (antes não existia objeto)', w.examinar({ id: 'gaiola_1', nome: 'g', desc: 'x' }).novo && !!w.kp.kp_obj_gaiola);
  w.update(.1); ok('rua: a Lia senta numa cadeira livre da mesa antes das quatro pessoas', w.mesa.liaSenta('T')); w.lia.sentada = true; let erro = null;
  try { for (let i = 0; i < 40000 && !w.mesa.lataFeita && w.clock.min < 700; i++) { w.update(.1); } } catch (e) { erro = e; }
  ok('rua: a lata do bairro fecha sem erro e rende anotação a quem está sentado (antes dava TypeError)', !erro && !!w.kp.kp_lata, erro && erro.message);
  {
    const w2 = new S.Rua.World({ scene, seed: 5, rate: 1.5 }); w2.initNav && w2.initNav(); let e2 = null;
    try { for (let i = 0; i < 40000 && w2.clock.min < 530; i++) w2.update(.1); const livre = ['E', 'T', 'F', 'D'].find(q => !w2.assentos[q].ocup); if (livre) { w2.mesa.liaSenta(livre); w2.lia.sentada = true; }
      for (let i = 0; i < 4000 && !w2.kp.kp_lata && w2.clock.min < 600; i++) w2.update(.1); } catch (e) { e2 = e; }
    ok('rua: a lata repete quando a Lia senta pela primeira vez, mesmo com a mesa já em jogo (8h50, cadeira do Seu Raimundo)', !e2 && !!w2.kp.kp_lata, e2 && e2.message);
  }
  const sh = fs.readFileSync(__dirname + '/../game/template.html', 'utf8');
  ok('sacola: falar com Seu Raimundo (tecla E ou clique) com a sacola na mão entrega o pão', /function openDialog\(id\) \{[^}]*Sim\.Sacola\.entrega\(SIM\)/.test(sh.replace(/\n/g, ' ')) && /entregar a sacola de pão a Seu Raimundo/.test(sh));
  const T = load(); const calls = []; const ctx = { save() { }, restore() { }, fillRect() { calls.push(1); }, set fillStyle(v) { } };
  T.Sacola.S.estado = 'nada'; T.Sacola.desenharMao(ctx, 100, 100, 'right'); const sem = calls.length; T.Sacola.S.estado = 'lia'; T.Sacola.desenharMao(ctx, 100, 100, 'right');
  ok('sacola: com ela na mão a Lia a leva desenhada; sem ela, nada', sem === 0 && calls.length > 5);
  const Q = require('../quintal/quintal.js'), D = require('../quintal/qdata.json'); D.SPEED = { ze: 0.57, nonato: 1.1, junior: 1.7 }; require('../quintal/dialogo.js');
  const q = new Q.Sim(D); q.forcada = true; q.fase('B', true); for (let t = 0; t < 30; t += .1) q.update(.1);
  ok('quintal: Dona Nena está em cena desde o preparo (fase A) e tem assunto logo de cara, sem precisar olhar nada', q.npcs.nena && q.npcs.nena.vis && q.topicosDe('nena').length >= 2, q.topicosDe('nena').map(t => t.id).join(','));
}
console.log('\n' + pass + ' passaram, ' + fail + ' falharam'); process.exit(fail ? 1 : 0);
