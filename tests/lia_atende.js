// Lia atende no balcão (PROPOSTA): pega um cliente da fila, ele é servido em ~4,6 s, estoque e caixa mudam, sem duplicar atendimento com a Vó.
const H = require('./harness.js'); let ok = 0, bad = 0; const check = (n, c, x) => { console.log((c ? 'PASSOU ' : 'FALHOU ') + n + (x ? ' — ' + x : '')); c ? ok++ : bad++; };
const { w } = H.make({ rate: 3 }); const S = w.service; let n = null, t = 0;
while (t < 600 && !n) { w.update(.1); t += .1; n = S.podeLia(); }
check('1. aparece cliente esperando na fila', !!n, n && n.id + ' em ' + w.clock.label());
const caixa0 = S.caixa, pao0 = S.stock.pao, fiado0 = JSON.stringify(w.persist.fiado);
const c = S.liaAtende(); check('2. Lia começa a atender', c && S.jobLia && c.state === 'Ordering');
let g = 0; while (S.jobLia && g++ < 200) w.update(.1);
check('3. termina em ≤ 5 s', g <= 50, (g / 10) + ' s');
check('4. cliente atendido, saiu da fila, contado como "pela Lia"', c.ses.served && !S.queue.includes(c.id) && w.stats.pela_lia === 1);
check('5. estoque e caixa/fiado mudam', S.stock.pao < pao0 && (S.caixa > caixa0 || JSON.stringify(w.persist.fiado) !== fiado0));
// cancelar devolve à fila
let m = null; t = 0; while (t < 900 && !m) { w.update(.1); t += .1; m = S.podeLia(); }
if (m) { S.liaAtende(); w.update(.3); S.cancelaLia(); check('6. cancelar devolve o cliente à fila', !S.jobLia && m.state === 'Waiting' && S.queue.includes(m.id)); } else check('6. (sem segundo cliente a tempo)', true);
// Vó e Lia nunca atendem a mesma pessoa
let dup = 0; for (let i = 0; i < 4000; i++) { w.update(.1); if (S.job && S.jobLia && S.job.cust === S.jobLia.cust) dup++; if (i % 40 === 0 && !S.jobLia) S.liaAtende(); }
check('7. nunca atendem o mesmo cliente ao mesmo tempo', dup === 0);
console.log(ok + ' passaram, ' + bad + ' falharam'); process.exit(bad ? 1 : 0);
