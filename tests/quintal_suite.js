// Testes do quintal (Etapa 8) — Node: node tests/quintal_suite.js
// Alcance de assentos e pontos, bloqueio da toalha na fase C1, ninguém preso em nenhuma fase e falas por fase do caruru.
const Q = require(__dirname + '/../quintal/quintal.js'), D = require(__dirname + '/../quintal/qdata.json');
D.SPEED = { ze: 0.57, nonato: 1.1, junior: 1.7 };
let pass = 0, fail = 0; const ok = (n, c, x) => { c ? pass++ : fail++; console.log((c ? 'PASS ' : 'FAIL ') + n + (x !== undefined && x !== '' ? ' · ' + x : '')); };
const s = new Q.Sim(D); s.forcada = true;   // fase escolhida pelo teste, não pelo relógio

// 1. todos os assentos e pontos de uso são alcançáveis a partir da soleira (Lia e NPC)
const src = [4.5, 7.5], bad = [];
for (const [id, v] of Object.entries(D.SEATS)) for (const [nm, r, l] of [['Lia', 0.25, true], ['NPC', 0.30, false]]) if (!s.achar(s.base, src, v[3], r, l)) bad.push(id + '/' + nm);
for (const [k, v] of Object.entries(D.STAND)) { if (k === 'toalha_zefa' || k === 'telhado') continue; if (!s.achar(s.base, src, [v[0], v[1]], 0.25, true)) bad.push('stand ' + k); }
ok('assentos e pontos alcançáveis da soleira', bad.length === 0, bad.join(','));

// 2. fase C1: a toalha bloqueia o centro e a Lia ainda chega ao banner
s.fase('C1', true);
ok('C1: Lia chega ao banner', !!s.achar(s.c1, src, [10.1, 1.95], 0.25, true));
ok('C1: o centro da toalha não é andável', !s.walk(s.c1, D.TOALHA.cx, D.TOALHA.cy, 0.25, true));

// 3. transição entre fases com NPCs andando: ninguém preso, e quem deve estar em cena está
for (const f of ['A', 'B', 'C1', 'C', 'D', 'A']) {
  s.fase(f, false); for (let t = 0; t < 240; t += 0.1) s.update(0.1);
  const esperados = Object.keys(D.FASE[f]).filter(k => k !== 'lia' && s.npcs[k]).sort();
  const visiveis = Object.values(s.npcs).filter(n => n.vis).map(n => n.id).sort();
  const presos = Object.values(s.npcs).filter(n => n.vis && n.state === 'preso').map(n => n.id);
  ok('fase ' + f + ': ninguém preso', presos.length === 0, presos.join(','));
  ok('fase ' + f + ': quem deve estar em cena está (' + esperados.length + ')', JSON.stringify(visiveis) === JSON.stringify(esperados), 'faltam/sobram: ' + esperados.filter(x => !visiveis.includes(x)).concat(visiveis.filter(x => !esperados.includes(x))).join(','));
}

// 4. falas por fase: a Áurea (e a Zefa) falam do que acontece naquela fase do caruru
const fala = (id, fase) => { s.fase(fase, true); const n = s.npcs[id]; n.vis = true; s.lia.x = n.x; s.lia.y = n.y + 0.8; s.falar(id); const t = s.conversa && s.conversa.linhas[0].texto; s.fecharConversa(); return t; };
const fa = {}; for (const f of ['B', 'C1', 'C', 'D']) fa[f] = fala('aurea', f);
ok('Áurea: uma fala diferente em cada fase', new Set(Object.values(fa)).size === 4, JSON.stringify(Object.values(fa).map(x => (x || '').slice(7, 30))));
ok('Áurea (B) conta que deixou o balcão sem ninguém', /balcão sem ninguém/.test(fa.B || ''));
ok('Áurea (C1) fala das crianças na toalha', /crianças|toalha/.test(fa.C1 || ''));
ok('Áurea (D) fala da conversa sobre o Programa', /Programa/.test(fa.D || ''));
ok('Zefa muda de fala entre preparo e mesa', fala('zefa', 'A') !== fala('zefa', 'C'));

// 5. conversa investigativa: assuntos por fase, anotações, nada pré-pronto
const perto = id => { const n = s.npcs[id]; n.vis = true; s.lia.x = n.x; s.lia.y = n.y + 0.8; };
const fresco = f => { const t = new Q.Sim(D); t.forcada = true; t.fase(f, true); return t; };
const junto = (t, id) => { const n = t.npcs[id]; n.vis = true; t.lia.x = n.x; t.lia.y = n.y + 0.8; t.falar(id); };
{
  const t = fresco('D'); junto(t, 'zefa');
  ok('assunto de vínculo só aparece depois de olhar a bandeira', !t.topicosDe('zefa').some(x => x.id === 'pai'));
  t.fecharConversa(); t.examinar('banner'); junto(t, 'zefa');
  ok('depois de examinar a bandeira, a Zefa tem o assunto da bandeira', t.topicosDe('zefa').some(x => x.id === 'pai'));
  const antes = t.notas().length; t.conversaAcao('perguntar', 'pai');
  ok('perguntar rende anotação nova e ela entra no caderninho', t.notas().length === antes + 1 && !!t.kp.q_zefa_pai);
  t.conversaAcao('perguntar', 'pai'); ok('perguntar de novo a mesma coisa não repete a anotação', t.notas().length === antes + 1);
  ok('Dandara: o segundo assunto só vem depois do primeiro', (junto(t, 'dandara'), t.topicosDe('dandara').map(x => x.id).join() === 'lista'));
  t.conversaAcao('perguntar', 'lista'); ok('...e depois da lista aparece "quem ficou fora"', t.topicosDe('dandara').some(x => x.id === 'comodos'));
}
{ // ficar ouvindo também rende anotação, e muda com a fase
  const t = fresco('D'); junto(t, 'dandara'); t.conversaAcao('ouvir'); ok('ouvir Dandara na fase D rende anotação (prazo do Programa)', !!t.kp.q_prazo);
  const u = fresco('C'); junto(u, 'dandara'); u.conversaAcao('ouvir'); ok('na fase C ela só conta assinaturas (sem anotação)', !u.kp.q_prazo);
}
// só o que existe em cada fase: A tem poucas pessoas; D tem seis anotações só de conversa, sem examinar nada
{
  const t = fresco('D'); let g = 0; const ids = Object.keys(D.FASE.D).filter(k => k !== 'lia' && t.npcs[k]);
  for (let volta = 0; volta < 4; volta++) for (const id of ids) { junto(t, id); for (const tp of t.topicosDe(id)) { t.conversaAcao('perguntar', tp.id); g++; } t.conversaAcao('ouvir'); }
  ok('fase D: dá para chegar a 6 anotações só conversando (' + t.notas().length + ')', t.notas().length >= 6);
  const A = fresco('A'); let a = 0; for (const id of Object.keys(D.FASE.A).filter(k => k !== 'lia' && A.npcs[k])) { junto(A, id); for (const tp of A.topicosDe(id)) { A.conversaAcao('perguntar', tp.id); a++; } }
  ok('fase A (12h): já há anotações para fazer cedo (' + A.notas().length + ')', A.notas().length >= 2);
}
{ // totais: com quintal inteiro explorado passa muito de 6
  const t = fresco('D'); for (const k of Object.keys(D.STAND)) if (Q.TXT[k] && k !== 'toalha_zefa' && k !== 'telhado') t.examinar(k); ok('objetos do quintal rendem anotações (' + t.notas().length + ')', t.notas().length >= 4);
}
{ // fora do caruru não há anotação (1991: quintal comum e vazio)
  const t = fresco('N'); t.examinar('banner'); ok('fase N (sem caruru): nada é anotado', t.notas().length === 0 && t.topicosDe('zefa').length === 0);
}
{ // conversa segura a pessoa parada e fecha quando a Lia se afasta
  const t = fresco('B'); junto(t, 'zefa'); const p0 = [t.npcs.zefa.x, t.npcs.zefa.y]; for (let i = 0; i < 20; i++) t.update(0.1);
  ok('conversa aberta mantém a pessoa no lugar', t.conversa && t.npcs.zefa.x === p0[0] && t.npcs.zefa.y === p0[1]);
  t.lia.x += 5; t.update(0.1); ok('a conversa fecha quando a Lia se afasta', t.conversa === null);
}
{ // as falas pré-prontas continuam só no "Cumprimentar": existe sempre o caminho Perguntar para quem tem assunto
  const t = fresco('C'); junto(t, 'nonato'); ok('Nonato: aparece Perguntar (assunto próprio)', t.temAssunto('nonato') && t.topicosDe('nonato').length >= 1);
}

console.log('\n' + pass + ' ok · ' + fail + ' falhas'); process.exit(fail ? 1 : 0);
