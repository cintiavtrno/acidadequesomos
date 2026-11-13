// ===== s5_dialogue.js — DialogueSystem (falas contextuais) + conversas espontâneas entre NPCs =====
Sim.dir8 = function (dx, dy) {
  if (Math.abs(dx) < .01 && Math.abs(dy) < .01) return null;
  const ax = Math.abs(dx), ay = Math.abs(dy), h = dx < 0 ? 'left' : 'right', v = dy < 0 ? 'up' : 'down';
  return ax > 2 * ay ? h : ay > 2 * ax ? v : v + '_' + h;
};
Sim.Dialogue = class {
  constructor(w) { this.w = w; this.used = {}; }
  ctx(id, extra) {
    const w = this.w, n = w.npcs[id];
    return Object.assign({ id, loc: n ? n.zona() : null, estado: n ? n.estadoFala() : null, nivel: id === 'aurea' || n ? w.rel.nivel(id, 'lia') : 0, humor: n ? n.mood : 'normal', hora: w.clock.min }, extra || {});
  }
  match(q, c) {
    const w = this.w;
    if (q.loc && !([].concat(q.loc).includes(c.loc))) return false;
    if (q.estado && q.estado !== c.estado) return false;
    if (q.conf && (c.nivel < q.conf[0] || c.nivel > q.conf[1])) return false;
    if (q.humor && !q.humor.includes(c.humor)) return false;
    if (q.mem && !w.mem.has(c.id, q.mem)) return false;
    if (q.semMem && w.mem.has(c.id, q.semMem)) return false;
    if (q.hora && (c.hora < q.hora[0] || c.hora > q.hora[1])) return false;
    if (q.presente && !w.presente(q.presente)) return false;
    if (q.flag && !w.flags[q.flag]) return false;
    return true;
  }
  // escolhe a fala mais específica; entre iguais, a menos recente (evita repetição); registra o uso
  pick(list, c) {
    if (!list || !list.length) return null;
    const ok = list.filter(f => this.match(f.quando, c)); if (!ok.length) return null;
    const spec = Math.max(...ok.map(f => Object.keys(f.quando).length)), top = ok.filter(f => Object.keys(f.quando).length === spec);
    top.sort((a, b) => (this.used[a.id] || -1e9) - (this.used[b.id] || -1e9) || this.w.rng() - .5);
    const f = top[0]; this.used[f.id] = this.w.bus.t; return f;
  }
  line(id, kind, c, topic) { const bank = Sim.Data.falas[id]; if (!bank) return null; const L = topic ? (bank[kind] || {})[topic] : bank[kind]; return this.pick(L, c || this.ctx(id)); }
  speak(npc, text, ttl) { text = Sim.saudarHora(text, this.w.clock.min); npc.say = { text, ttl: ttl || 1.8 + text.length * .05 }; this.w.bus.emit('fala', { quem: npc.id, texto: text }); }
  usedRecently(id, secs) { return this.used[id] != null && this.w.bus.t - this.used[id] < secs; }
};

// Conversas entre NPCs: roteiros de Sim.Data.conversas. Acontecem na fila, nas mesas ou quando alguém procura o outro.
Sim.Conversations = class {
  constructor(w) { this.w = w; this.act = []; this.cool = {}; this.timer = 4; this.lastPair = {}; }
  active(id) { return this.act.find(c => c.a === id || c.b === id) || null; }
  eligible(n) { return n && n.id !== 'aurea' && n.loc === 'padaria' && ['Waiting', 'Sitting', 'Observing'].includes(n.state) && n.stateT > 1.2 && !n.slide && !this.active(n.id) && !n.dialogLia; }
  near(a, b) { const d = Sim.dist(a, b); return d < (a.state === 'Sitting' && b.state === 'Sitting' ? 92 : 66); }
  update(dt) {
    const w = this.w;
    for (const c of this.act.slice()) this.step(c, dt);
    this.timer -= dt; if (this.timer > 0) return; this.timer = 3 + w.rng() * 3;
    const ids = Object.keys(w.npcs).filter(i => this.eligible(w.npcs[i]));
    for (let i = 0; i < ids.length; i++) for (let j = i + 1; j < ids.length; j++) {
      const A = w.npcs[ids[i]], B = w.npcs[ids[j]]; if (!this.near(A, B)) continue;
      const key = [A.id, B.id].sort().join('+'); if ((this.cool[key] || -1e9) > w.bus.t - 45) continue;
      const aff = (w.rel.get(A.id, B.id).aff + w.rel.get(B.id, A.id).aff) / 2, soc = (A.needs.social + B.needs.social) / 2;
      const chance = Sim.clamp(.35 + soc * .5 + aff * .3 + (A.state === 'Waiting' && B.state === 'Waiting' ? .25 : 0), .1, .95);
      if (!w.rng.chance(chance)) { this.cool[key] = w.bus.t - 30; continue; }
      const s = this.script(A, B); if (s) { this.start(A, B, s); return; }
    }
  }
  script(A, B) {
    const w = this.w, ok = Sim.Data.conversas.filter(s => s.par.includes(A.id) && s.par.includes(B.id) && !this.cool[s.id] && w.rel.get(A.id, B.id).aff >= s.min_aff - 0.5 && (!s.cond || s.cond(w)));
    ok.sort((x, y) => (x.cond ? 0 : 1) - (y.cond ? 0 : 1)); return ok[0] || null;     // roteiros condicionados à situação têm prioridade
  }
  start(A, B, s) {
    const w = this.w, c = { a: A.id, b: B.id, s, i: 0, t: 0, wait: .4 };
    this.act.push(c); A.chat = c; B.chat = c; this.cool[s.id] = w.bus.t; this.cool[[A.id, B.id].sort().join('+')] = w.bus.t;
    w.bus.emit('conversa_inicio', { a: A.id, b: B.id, id: s.id, tema: s.tema }); this.face(A, B); this.face(B, A);
  }
  face(A, B) { if (A.state === 'Sitting') return; const d = Sim.dir8(B.x - A.x, B.y - A.y); if (d && !A.path.length) A.face = d; }
  step(c, dt) {
    const w = this.w, A = w.npcs[c.a], B = w.npcs[c.b];
    if (!this.eligibleIn(A) || !this.eligibleIn(B) || !this.near(A, B) || A.dialogLia || B.dialogLia) return this.end(c, true);
    c.wait -= dt; if (c.wait > 0) return;
    if (c.i >= c.s.falas.length) return this.end(c, false);
    const [quem, texto] = c.s.falas[c.i++], N = w.npcs[quem]; w.dialogue.speak(N, texto); c.wait = N.say.ttl + .5;
    this.face(w.npcs[quem === c.a ? c.b : c.a], N); this.face(N, w.npcs[quem === c.a ? c.b : c.a]);
    w.bus.emit('conversa_fala', { quem, texto, id: c.s.id, perto_lia: w.liaPerto(N, 90) });
    if (c.s.ouvido && w.liaPerto(N, 90) && w.cena === 'interior') c.ouviu = true;
  }
  eligibleIn(n) { return n && n.loc === 'padaria' && ['Waiting', 'Sitting', 'Observing', 'Ordering', 'Idle', 'Approaching'].includes(n.state); }
  end(c, abort) {
    const w = this.w, A = w.npcs[c.a], B = w.npcs[c.b]; this.act.splice(this.act.indexOf(c), 1);
    if (A) A.chat = null; if (B) B.chat = null;
    w.bus.emit('conversa_fim', { a: c.a, b: c.b, id: c.s.id, abortada: abort });
    if (abort) return;
    const e = c.s.efeito || {};
    for (const [x, y] of [[c.a, c.b], [c.b, c.a]]) w.rel.change(x, y, { aff: e.aff || 0, tens: e.tens || 0 }, 'conversa:' + c.s.id);
    if (A) A.needs.social = Math.max(0, A.needs.social - .25); if (B) B.needs.social = Math.max(0, B.needs.social - .25);
    w.mem.gossip(c.a, c.b, w.rng);
    if (e.cede) w.service.cedeVez(e.cede[0], e.cede[1], true);
    if (c.ouviu) w.knowledge.award(c.s.ouvido, { via: 'ouvida' });
    if (c.s.id === 'dl_tensao') { w.mem.remember('dandara', 'tensao_lucia', { publico: true }); w.mem.remember('lucia', 'tensao_dandara'); w.setMood('dandara', 'irritada', 60); }
  }
};
