const { make } = require('./harness.js');
const { Sim, w, solids } = make({ seed: +process.argv[2] || 1991 });
w.cena = 'street'; w.lia.x = 240; w.lia.y = 300;
const ev = []; w.bus.on('*', (e, d) => { if (!['fala', 'estado_npc', 'relacao', 'humor', 'memoria', 'estado_objeto'].includes(e)) ev.push(w.clock.label() + ' ' + e + ' ' + JSON.stringify(d).slice(0, 110)); });
w.step(330 * 1);
console.log(ev.join('\n')); console.log(JSON.stringify(w.stats), 'queue', w.service.queue);
for (const k in w.seats) console.log(k, w.seats[k].ap);
