// Missão da sacola de pão: única, atravessa dias, marca "pega" e "entregue" — node tests/sacola.js
const H = require('./harness.js'); let ok = 0, bad = 0; const check = (n, c, x) => { console.log((c ? 'PASSOU ' : 'FALHOU ') + n + (x ? ' — ' + x : '')); c ? ok++ : bad++; };
const { w, Sim } = H.make({ rate: 3, seed: 3 }); const Sc = Sim.Sacola, G = Sc.H();
check('1. começa sem missão', Sc.S.estado === 'nada' && Sc.painel() === '');
Sc.esquece(w); check('2. Raimundo esquece a sacola: ela fica no balcão e a missão diz onde', Sc.S.estado === 'balcao' && /balcão da padaria, entre a vitrine de pães e a caixa/.test(Sc.painel()) && Sc.visivel());
check('3. só pega perto da sacola (frente do balcão, entre vitrine e caixa)', Sc.perto({ x: 172, y: 195 }) && !Sc.perto({ x: 330, y: 195 }) && !Sc.perto({ x: 172, y: 150 }));
check('4. entregar sem ter pego não vale', Sc.entrega(Object.assign({}, w, { casaPick: () => 'x' })) === false);
Sc.pegar(w); check('5. pegar marca como pega e some do balcão', Sc.S.estado === 'lia' && !Sc.visivel() && /✓ Sacola pega/.test(Sc.painel()));
check('6. entregar fora da casa não vale (só a casa tem casaPick)', Sc.entrega(w) === false);
const fake = Object.assign(Object.create(Object.getPrototypeOf(w)), w, { casaPick: () => 'ok' });
check('7. entregar na casa marca entregue e conclui', Sc.entrega(fake) === true && Sc.S.estado === 'entregue' && /cumprida/.test(Sc.painel()));
Sc.S.avisoRua = false; Sc.esquece(w); check('8. é missão de uma vez só: nunca volta depois de entregue', Sc.S.estado === 'entregue');
// atravessa dias: o estado "balcao" não é zerado quando o dia vira
{ const t = H.make({ rate: 3, seed: 4 }); const S2 = t.Sim.Sacola; S2.esquece(t.w); t.w.persist.dia = 3; S2.esquece(t.w); check('9. dias passam e a sacola continua no balcão (não zera nem repete o aviso)', S2.S.estado === 'balcao'); }
// em 1994 ela não aparece
{ const t = H.make({ rate: 3, seed: 5 }); t.Sim.Sacola.H().MUNDO_ANO = 1994; t.Sim.Sacola.esquece(t.w); check('10. em 1994 a missão não existe', t.Sim.Sacola.S.estado === 'nada' && t.Sim.Sacola.painel() === ''); }
// Raimundo atendido deixa a sacola na simulação do dia
{ let n = 0; for (let seed = 1; seed <= 6; seed++) { const t = H.make({ rate: 3, seed }); for (let i = 0; i < 20000 && t.w.clock.min < 12 * 60; i++) t.w.update(.2); if (t.Sim.Sacola.S.estado === 'balcao') n++; } check('11. no dia, ao ser atendido, Raimundo esquece a sacola', n > 0, n + '/6'); }
console.log(ok + ' passaram, ' + bad + ' falharam'); process.exit(bad ? 1 : 0);
