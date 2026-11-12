// ===== s4_social.js — NPCRelationshipSystem e NPCMemorySystem =====
// Relações: par direcional "a>b" com afinidade (-1..1), confiança (0..1) e tensão (0..1). "x>lia" = o que x sente por Lia.
Sim.Relations = class {
  constructor(bus, init) { this.bus = bus; this.m = {}; this.hist = []; for (const k in init) this.m[k] = Object.assign({ aff: 0, trust: .1, tens: 0 }, init[k]); }
  get(a, b) { const k = a + '>' + b; return this.m[k] || (this.m[k] = { aff: 0, trust: .1, tens: 0 }); }
  nivel(a, b) { const t = this.get(a, b || 'lia').trust; return t < .25 ? 0 : t < .5 ? 1 : t < .75 ? 2 : 3; }
  change(a, b, d, why) {
    const r = this.get(a, b), antes = this.nivel(a, b);
    if (d.aff) r.aff = Sim.clamp(r.aff + d.aff, -1, 1); if (d.trust) r.trust = Sim.clamp(r.trust + d.trust, 0, 1); if (d.tens) r.tens = Sim.clamp(r.tens + d.tens, 0, 1);
    this.hist.push({ t: this.bus.t, a, b, d, why });
    this.bus.emit('relacao', { a, b, d, why, aff: r.aff, trust: r.trust, nivel: this.nivel(a, b), subiu: this.nivel(a, b) > antes, desceu: this.nivel(a, b) < antes });
  }
  export() { return JSON.parse(JSON.stringify(this.m)); }
  import(o) { for (const k in o) this.m[k] = o[k]; }
};

// Memória: fatos importantes por pessoa. Fatos "públicos" circulam em conversas (boato), alterando relações.
Sim.Memory = class {
  constructor(bus) { this.bus = bus; this.m = {}; }
  list(n) { return this.m[n] || (this.m[n] = []); }
  has(n, id) { return this.list(n).some(f => f.id === id); }
  get(n, id) { return this.list(n).find(f => f.id === id) || null; }
  remember(n, id, o) { if (this.has(n, id)) return false; const f = Object.assign({ id, t: this.bus.t, publico: false, via: null }, o || {}); this.list(n).push(f); this.bus.emit('memoria', { quem: n, fato: f }); return true; }
  // quando duas pessoas conversam, cada uma pode contar à outra os fatos públicos que sabe
  gossip(a, b, rng) {
    let n = 0;
    for (const [x, y] of [[a, b], [b, a]]) for (const f of this.list(x)) {
      if (!f.publico || f.via === y || this.has(y, f.alias || ('soube_' + f.id.replace(/^lia_/, ''))) || !rng.chance(.75)) continue;
      const nid = f.alias || ('soube_' + f.id.replace(/^lia_/, ''));
      this.remember(y, nid, { publico: false, via: x, de: f.id }); n++;
      this.bus.emit('boato', { de: x, para: y, fato: f.id, novo: nid });
    }
    return n;
  }
  export() { return JSON.parse(JSON.stringify(this.m)); }
  import(o) { this.m = o; }
};
