// Teste da trama de 1996 (Node): falas alcançáveis, missões em qualquer ordem, ligações com 1991/1994, fim, e regras de texto.
const fs = require('fs'), B = __dirname + '/../';
eval(fs.readFileSync(B + 'sim/s1_core.js', 'utf8') + ';global.Sim=Sim;');
eval(fs.readFileSync(B + 'sim/s2_nav.js', 'utf8'));
eval(fs.readFileSync(B + 'sim/s96_rua.js', 'utf8') + ';global.Sim96=Sim96;');
eval(fs.readFileSync(B + 'sim/s96_elenco.js', 'utf8'));
eval(fs.readFileSync(B + 'sim/s96_trama.js', 'utf8'));
let falhas = 0; const ok = (c, m) => { if (!c) { falhas++; console.log('FALHOU:', m); } };
const T = Sim96.Trama, mk = (storage, o) => T.criar(Object.assign({ storage }, o || {}));
const mem = (init) => { const m = Object.assign({}, init || {}); return { getItem: k => m[k] == null ? null : m[k], setItem: (k, v) => { m[k] = v; }, _m: m }; };
const fala = (G, q, id) => G.perguntar(q, id);

// 1) quem fala existe no elenco e nos sprites
const ids = new Set(Sim96.Elenco.atores.map(a => a.id)), objs = Sim96.Elenco.objetos.map(o => o.id);
for (const [aid, q] of Object.entries(T.QUEM)) { ok(ids.has(aid), 'ator ausente no elenco: ' + aid); ok(T.FALAS[q], 'sem fala: ' + q); }
for (const o of Sim96.Elenco.objetos) if (o.fala) ok(T.FALAS[o.fala], 'objeto fala sem texto: ' + o.id);
for (const q of Object.keys(T.FALAS)) ok(T.NOMES[q] && T.COR[q], 'sem nome/cor: ' + q);
for (const [id, k] of Object.entries(T.KP)) ok(T.FIOS.some(f => f[0] === k[2]), 'fio inválido ' + id);
for (const f of Object.values(T.FALAS)) for (const t of f.topicos) for (const k of (t.da || [])) ok(T.KP[k], 'anotação inexistente ' + k);
for (const m of Object.values(T.OBJ)) if (m.kp) ok(T.KP[m.kp], 'anotação de objeto inexistente ' + m.kp);

// 2) todas as 20 anotações são alcançáveis jogando do zero (sem memória de 1991/1994)
function jogarTudo(G) {
  const seq = [['aurea', 'encomenda'], ['aurea', 'cesta'], ['assist_a', 'entrega'], ['aurea', 'como_foi'], ['aurea', 'padaria'], ['dandara', 'clipe'], ['rita', 'tinta']];
  G.exam('base_monitor');
  for (const [q, t] of seq) fala(G, q, t);
  for (const [q, t] of [['dandara', 'camera'], ['dandara', 'fase2'], ['tonho', 'venda'], ['tonho', 'plateia'], ['bela', 'freguesas'], ['ze', 'barbearia'], ['dandara', 'evento'], ['dandara', 'associacao'], ['zefa', 'rua'], ['cicera', 'esquinas'], ['nonato', 'empreita'], ['assist_a', 'locacao'], ['assist_b', 'silencio'], ['raimundo', 'clipe'], ['raimundo', 'mesa']]) fala(G, q, t);
  G.exam('quadro_avisos'); G.exam('mesa_domino');
}
{
  const G = mk(mem()); const t0 = G.diario();
  ok(t0.notas.length === 0 && G.missoes().every(m => !m.feito), 'estado inicial sujo');
  // ordem: 'camera' não aparece antes de ver monitor e Rita; 'evento' não antes de 3 vizinhos
  ok(!G.topicos('dandara').some(t => t.id === 'camera'), 'camera cedo demais');
  ok(!G.topicos('dandara').some(t => t.id === 'fase2'), 'fase2 cedo demais sem memória');
  ok(!G.topicos('aurea').some(t => t.id === 'fechar'), 'fechar cedo demais');
  jogarTudo(G);
  const d = G.diario();
  ok(d.notas.length === d.total, 'nem todas as anotações foram alcançadas: ' + d.notas.length + '/' + d.total);
  ok(G.missoes().every(m => m.feito), 'missões não concluídas: ' + JSON.stringify(G.missoes().map(m => [m.id, m.passo])));
  ok(G.podeFechar() && G.topicos('aurea').some(t => t.id === 'fechar'), 'não pode fechar o dia');
  ok(!G.fim(), 'fim antes da hora'); fala(G, 'aurea', 'fechar'); ok(G.fim(), 'fim não registrado');
  ok(d.ligacoes.every(l => !l.antiga), 'ligações antigas sem memória de 1991/1994');
  ok(d.ligacoes.length >= 2, 'faltam hipóteses de hoje');
}
// 3) com memória de 1991/1994 (rua + quintal), as ligações e falas extras aparecem
{
  const S = mem({ balcao_rua_v1: JSON.stringify({ kp: { kp_94_lucia_evento: 1, kp_94_programa: 1, kp_94_tonho_turista: 1, kp_94_ray_aviso: 1, kp_94_bela_freguesas: 1, kp_rua_olhar: 1 } }), balcao_quintal_kp: JSON.stringify({ kp: { q_zefa_casa: 1, q_rita_telhado: 1, q_aurea_freguesia: 1 } }) });
  const G = mk(S);
  ok(G.topicos('dandara').some(t => t.id === 'fase2'), 'memória de 1994 não abriu "O Programa agora"');
  jogarTudo(G); const d = G.diario();
  ok(d.ligacoes.filter(l => l.antiga).length >= 6, 'poucas ligações com 1991/1994: ' + d.ligacoes.filter(l => l.antiga).length);
  const r = G.perguntar('tonho', 'venda'); ok(r.linhas.length === 0 || r.linhas.length === 1, 'repetição devia dar uma fala');
  const G2 = mk(mem({ balcao_rua_v1: JSON.stringify({ kp: { kp_94_lucia_evento: 1 } }) })); const l1 = G2.perguntar('tonho', 'venda').linhas.length;
  const G3 = mk(mem({ balcao_rua_v1: JSON.stringify({ kp: { kp_94_tonho_turista: 1 } }) })); const l2 = G3.perguntar('tonho', 'venda').linhas.length;
  ok(l2 === l1 + 1, 'fala extra de Tonho com memória de 1994 (' + l1 + ' vs ' + l2 + ')');
}
// 4) ?mem=tudo e recomeço
{ const G = mk(mem(), { mem: 'tudo' }); ok(G.topicos('dandara').some(t => t.id === 'fase2'), 'mem=tudo não funciona'); jogarTudo(G); ok(G.diario().ligacoes.filter(l => l.antiga).length >= 9, 'mem=tudo: poucas ligações'); G.zerar(); ok(G.diario().notas.length === 0, 'zerar'); }
// 5) persistência
{ const S = mem(); const G = mk(S); fala(G, 'dandara', 'clipe'); const G2 = mk(S); ok(G2.tem('kp_96_gravacao') && G2.flag('m2inicio'), 'progresso não persistiu'); const G3 = mk(S, { novo: true }); ok(!G3.tem('kp_96_gravacao'), 'novo=1 manteve progresso'); }
// 6) missões em qualquer ordem: M3 antes de M2 funciona
{
  const G = mk(mem()); for (const q of [['tonho', 'venda'], ['bela', 'freguesas'], ['ze', 'barbearia']]) fala(G, q[0], q[1]);
  fala(G, 'dandara', 'clipe'); ok(G.topicos('dandara').every(t => t.id !== 'evento'), 'evento antes de fase2');
  G.exam('base_monitor'); fala(G, 'rita', 'tinta'); fala(G, 'dandara', 'camera'); fala(G, 'dandara', 'fase2');
  ok(G.topicos('dandara').some(t => t.id === 'evento'), 'evento não abriu com 3 vizinhos já ouvidos'); fala(G, 'dandara', 'evento'); ok(G.flag('m3') && G.flag('m2'), 'M2 e M3 não fecharam');
}
// 7) texto: tamanho, vícios e termos proibidos
const textos = []; for (const f of Object.values(T.FALAS)) { for (const s of f.saudar) textos.push(s); textos.push(f.rep); for (const t of f.topicos) { textos.push(t.label); for (const l of t.lin) textos.push(l[1]); } }
for (const k of Object.values(T.KP)) textos.push(k[0], k[1]); for (const l of T.LIGACOES) textos.push(l.t); for (const o of Object.values(T.OBJ)) textos.push(o.desc);
const todo = textos.join('\n');
ok(!/2000|Michael|Jackson|Spike|Governador|Secretário/i.test(todo), 'termo fora do escopo no texto (2000, pessoa real, cargos inventados)');
ok(!/não é [^.]{1,60}, é /i.test(todo), 'padrão "não é X, é Y" no texto');
for (const s of textos) ok(s.length <= 260, 'fala longa demais (' + s.length + '): ' + s.slice(0, 50));
for (const l of Object.values(T.FALAS).flatMap(f => f.topicos).flatMap(t => t.lin)) ok(l[1].split(/\s+/).length <= 45, 'linha com mais de 45 palavras: ' + l[1].slice(0, 40));
console.log(falhas ? falhas + ' falha(s)' : 'trama 1996: ok (' + Object.keys(T.KP).length + ' anotações, ' + Object.keys(T.FALAS).length + ' falantes, ' + T.LIGACOES.length + ' ligações)'); process.exit(falhas ? 1 : 0);
