// acontecimentos da rua em 1991: papel dos técnicos (dia 3), chuva (dias 2 e 4), reunião da associação (dia 4)
const load = require('../sim/load_node.js'), fs = require('fs'), path = require('path');
const scene = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'assets/street6/scene_rua.json')));
let ok = 0, bad = 0; const t = (n, c, x) => { if (c) { ok++; console.log('PASS', n); } else { bad++; console.log('FAIL', n, x || ''); } };
const RATE = 0.5;
function mundo(dia, seed) {
  const S = load(), w = new S.Rua.World({ scene, seed, rate: RATE, integrado: true, dia, persist: {}, hooks: {} }); w.initNav && w.initNav();
  const upd = w.update.bind(w); w.update = dt => { for (const k of ['raimundo:casa', 'raimundo:padaria', 'dandara:padaria', 'lucia:padaria']) w.lib[k] = true; upd(dt); };
  w.lia.x = 5; return w;
}
const ate = (w, min, f) => { while (w.clock.min < min) { w.update(.1); if (f) f(); } };
for (const seed of [1, 2, 3]) {
  const w = mundo(2, seed); let chuvaVista = false, abrigados = 0;
  ate(w, 1140, () => { if (w.evAtivo('chuva')) { chuvaVista = true; for (const id of ['ze', 'nonato', 'junior']) if (w.npcs[id] && w.npcs[id].state === 'Away') abrigados++; } });
  t('dia 2 seed ' + seed + ': chuva acontece e termina', chuvaVista && !w.evAtivo('chuva') && w.aco.chuva && w.aco.chuva.acabou);
  const presos = Object.keys(w.npcs).filter(id => w.npcs[id].state === 'Walking' && !w.npcs[id].path.length);
  t('dia 2 seed ' + seed + ': ninguém fica travado', presos.length === 0, presos.join());
}
{
  const w = mundo(1, 1); ate(w, 1140);
  t('dia 1: não chove e não há papel no quadro', !w.aco.chuva && !w.aco.papel);
}
{
  const w = mundo(3, 1); ate(w, 530); const a = w.aco.papel; ate(w, 560);
  t('dia 3: papel dos técnicos aparece às 9h', !a && w.aco.papel);
  t('dia 3: não chove', !w.aco.chuva);
}
{
  const w = mundo(4, 2); let reun = false; ate(w, 1135, () => { if (w.evAtivo('reuniao')) reun = true; });
  t('dia 4: reunião acontece às 18h, cartaz e giz no cenário', reun && w.aco.cartaz && Object.keys(w.aco.giz).length > 0);
  const d = w.npcs.dandara;
  t('dia 4: Dandara termina dentro da associação ou longe da rua', d.state === 'Away' || d.state === 'Entering' || d.state === 'Idle');
}

{ // atividades: ajudar Cícera com a roupa (chuva) e segurar a trena de Lúcia (dia 3+)
  const w = mundo(2, 1); let c = null, tops = null;
  ate(w, 1140, () => { if (!c && w.evAtivo('varal')) { const n = w.npcs.cicera; w.lia.x = n.x - 14; w.lia.y = n.y + 1; c = w.abrirConversa('cicera'); if (c) { tops = w.topicos('cicera'); } } });
  t('chuva: Dona Cícera oferece "Ajudar com a roupa"', !!tops && JSON.stringify(tops).includes('roupa'), JSON.stringify(tops).slice(0, 200));
  if (tops) { const o = w.perguntar('cicera', 'roupa'); t('ajudar com a roupa marca a vivência e dá confiança', w.tem('ajudou_roupa') && (w.trust.cicera || 0) > .1, JSON.stringify(o).slice(0, 160)); }
  const w2 = mundo(1, 1); w2.clock.min = 1000; t('fora da chuva o tópico não existe', !JSON.stringify(w2.topicos('cicera') || []).includes('roupa'));
}
{
  const w = mundo(3, 1); let achou = false;
  ate(w, 1100, () => { if (!achou && w.evAtivo('medindo')) { const n = w.npcs.lucia; w.lia.x = n.x - 14; w.lia.y = n.y + 1; if (w.abrirConversa('lucia') && JSON.stringify(w.topicos('lucia')).includes('trena')) { achou = true; w.perguntar('lucia', 'trena'); } } });
  t('dia 3: enquanto mede, Lúcia deixa segurar a trena', achou && w.tem('segurou_trena'));
}
console.log('\n' + ok + ' passaram, ' + bad + ' falharam'); process.exit(bad ? 1 : 0);
