const load = require('../sim/load_node.js'), fs = require('fs');
const scene = JSON.parse(fs.readFileSync(__dirname + '/../assets/objects/scene_padaria.json'));
exports.make = function (o) {
  o = o || {}; const Sim = load();
  const solids = scene.colisao_arquitetura.concat(scene.instancias.filter(i => i.collide).map(i => i.collide));
  const X0 = 72, X1 = 408, YB = 132, YF = 236, EXIT_X = 240;
  Sim.Nav.init({ X0, X1, YB, YF, EXIT_X, solids, blocked(x, y) { const gap = Math.abs(x - EXIT_X) <= 24; if (x < X0 + 8 || x > X1 - 8 || y < YB + 6) return true; if (y > YF - 6 && !gap) return true; if (y > YF + 10) return true; for (const [a, b, c, d] of solids) if (x >= a && x <= c && y >= b && y <= d) return true; return false; } });
  const w = new Sim.World(Object.assign({ scene, seed: 1991, rate: 1 }, o));
  return { Sim, w, solids };
};
exports.scene = scene;
