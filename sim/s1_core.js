// ===== s1_core.js — base da simulação (O balcão da vó · Etapa 4) =====
// DOM-free: roda no navegador e em Node (testes). Tudo vive no objeto global Sim.
// Módulos: core (RNG, EventSystem, WorldClock) · nav · data · social (relações + memória) · dialogue · npc (estados, decisão, rotina) · service · events · objectives · world.
const Sim = { v: '4.0', cfg: { speedPx: { lia: 30, aurea: 20, raimundo: 15.7, dandara: 26, lucia: 29 } } };

// gerador pseudo-aleatório com semente (mulberry32): a mesma semente repete o mesmo dia
Sim.RNG = function (seed) {
  let s = (seed >>> 0) || 1;
  const r = () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  r.pick = a => a[Math.floor(r() * a.length)];
  r.range = (a, b) => a + (b - a) * r();
  r.chance = p => r() < p;
  return r;
};
Sim.clamp = (v, a, b) => Math.max(a, Math.min(b, v));
Sim.dist = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);

// EventSystem — barramento simples: tudo que é notável no mundo vira um evento com nome e dados.
// A interface, o diário (Caderninho) e os testes só escutam; a simulação não sabe nada deles.
Sim.EventSystem = class {
  constructor() { this.h = {}; this.log = []; this.t = 0; this.n = {}; }
  on(ev, fn) { (this.h[ev] = this.h[ev] || []).push(fn); return this; }
  emit(ev, d) { d = d || {}; this.n[ev] = (this.n[ev] || 0) + 1; this.log.push({ t: this.t, ev, d }); if (this.log.length > 600) this.log.shift(); (this.h[ev] || []).forEach(f => f(d)); (this.h['*'] || []).forEach(f => f(ev, d)); }
  count(ev) { return this.n[ev] || 0; }
};

// WorldClock — relógio do mundo em minutos de jogo. O mundo anda mesmo que a câmera esteja em outro lugar.
// rate = minutos de jogo por segundo real (padrão 1). Horário de funcionamento e fim do dia vêm daqui.
Sim.WorldClock = class {
  constructor(o) { o = o || {}; this.min = o.start != null ? o.start : 420; this.rate = o.rate || 1; this.openAt = o.openAt || 420; this.closeAt = o.closeAt || 780; this.day = o.day || 1; this.paused = false; this.ended = false; this.tReal = 0; }
  tick(dt) { if (this.paused || this.ended) return 0; this.tReal += dt; const d = dt * this.rate; this.min += d; return d; }
  get hh() { return Math.floor(this.min / 60); }
  get mm() { return Math.floor(this.min % 60); }
  label() { return String(this.hh).padStart(2, '0') + ':' + String(this.mm).padStart(2, '0'); }
  isOpen() { return this.min >= this.openAt && this.min < this.closeAt; }
  periodo() { const h = this.hh; return h < 9 ? 'manhã cedo' : h < 11 ? 'manhã' : h < 13 ? 'fim de manhã' : 'tarde'; }
  at(hhmm) { const [h, m] = hhmm.split(':').map(Number); return h * 60 + m; }
};
