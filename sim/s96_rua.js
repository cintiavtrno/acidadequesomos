// ===== s96_rua.js — a rua de 1996, dia da gravação (Etapa D) =====
// DOM-free. Mundo mínimo: Lia, atores com plano repetido (andar, ficar, tocar, filmar), colisão e navegação da rua.
// Os atores e suas marcações ficam em s96_elenco.js (dados). A trama de 1996 ainda não existe: não há diálogo, missão nem relógio de cena.
const Sim96 = {};
(function () {
  const clamp = Sim.clamp;
  const W = 1500, VH = 270, DIV = 110;
  const yw = x => 212 + Math.floor(Math.max(0, x) / DIV);
  const dirDe = (dx, dy) => Math.abs(dx) >= Math.abs(dy) * 0.55 ? (dx < 0 ? 'left' : 'right') : (dy < 0 ? 'up' : 'down');
  Sim96.W = W; Sim96.VH = VH; Sim96.yw = yw;

  class Ator {
    constructor(w, d) {
      this.w = w; this.id = d.id; this.who = d.who || d.id; this.nome = d.nome || d.id; this.papel = d.papel || ''; this.obs = d.obs || '';
      this.x = d.x; this.sy = d.sy; this.y = d.y != null ? d.y : yw(d.x) + d.sy; this.face = d.face || 'down'; this.anim = d.anim || 'idle'; this.at = w.rv() * 3;
      this.plano = d.plano || []; this.i = -1; this.espera = 0; this.estado = 'espera'; this.path = []; this.vm = d.vm || 1; this.camada = d.camada || 'sorted';
      this.clip = d.clip != null ? d.clip : null; this.vies = d.vies || 0; this.fixo = !!d.fixo; this.alpha = 1; this.passo = null; this.proximo(true);
    }
    setAnim(a) { if (this.anim !== a) { this.anim = a; this.at = 0; } }
    proximo(ini) {
      if (!this.plano.length) { this.espera = 1e9; this.estado = 'espera'; return; }
      this.i = (this.i + 1) % this.plano.length; const p = this.plano[this.i], rv = this.w.rv;
      if (p.vai || p.vaiAle) {
        let x, sy;
        if (p.vai) { x = p.vai[0]; sy = p.vai[1]; } else { x = rv.range(p.vaiAle.x[0], p.vaiAle.x[1]); sy = rv.range(p.vaiAle.sy[0], p.vaiAle.sy[1]); }
        let y = yw(x) + sy; const f = this.w.livre(x, y); x = f[0]; y = f[1]; const c = this.w.caminho(this.x, this.y, x, y);
        if (!c || !c.length) { this.x = x; this.y = y; this.estado = 'espera'; this.espera = 0.3; if (p.fim) this.face = p.fim; return; }
        this.path = c; this.estado = 'anda'; this.passo = p; this.setAnim(p.anim || 'walk');
      } else {
        this.estado = 'espera'; const a = p.anims ? rv.pick(p.anims) : p.anim; if (a) this.setAnim(a);
        if (p.face) this.face = p.face; if (p.faces) this.face = rv.pick(p.faces);
        this.espera = p.fica ? rv.range(p.fica[0], p.fica[1]) : 4;
        if (ini && p.ini != null) this.espera = p.ini;
      }
    }
    update(dt) {
      this.at += dt;
      if (this.estado === 'espera') { this.espera -= dt; if (this.espera <= 0) this.proximo(); return; }
      const alvo = this.path[0]; if (!alvo) { this.estado = 'espera'; this.espera = 0.2; if (this.passo && this.passo.fim) this.face = this.passo.fim; return; }
      const dx = alvo[0] - this.x, dy = alvo[1] - this.y, d = Math.hypot(dx, dy), v = this.w.vel(this.who) * this.vm * dt;
      if (d <= v) { this.x = alvo[0]; this.y = alvo[1]; this.path.shift(); if (!this.path.length) { this.estado = 'espera'; this.espera = 0.15; if (this.passo && this.passo.fim) this.face = this.passo.fim; this.proximoAnim(); } }
      else { this.x += dx / d * v; this.y += dy / d * v; this.face = dirDe(dx, dy); }
    }
    proximoAnim() { const p = this.passo; if (p && p.fimAnim) this.setAnim(p.fimAnim); }
  }

  Sim96.World = class {
    constructor(o) {
      this.scene = o.scene; this.rv = Sim.RNG(o.seed || 1996); this.atlas = o.atlas || {}; this.t = 0;
      this.solids = (this.scene.solids || []).map(s => ({ id: s.id, x0: s.x0, x1: s.x1, sy0: s.sy0, sy1: s.sy1 }));
      this.grade(); const self = this;
      Sim.Nav.init({ X0: 0, X1: W, YB: 205, YF: 264, EXIT_X: 0, blocked: (x, y) => self.blocked(x, y) });
      this.lia = { x: 110, y: yw(110) + 22, face: 'right' };
      this.atores = {}; this.lista = [];
      for (let d of (o.elenco.atores || [])) { if (d.predio) d = Object.assign({}, d, { y: this.scene.buildings[d.predio].base - 97 }); const a = new Ator(this, d); this.atores[a.id] = a; this.lista.push(a); }
    }
    vel(who) { const a = this.atlas[who + '_side']; return a ? a.speed_mps * 24 : 22; }
    grade() {
      const H = VH + 1; this.G1 = new Uint8Array(W * H);
      for (let yy = 0; yy < H; yy++) for (let xx = 0; xx < W; xx++) this.G1[yy * W + xx] = this.bloqueadoCru(xx, yy) ? 1 : 0;
    }
    bloqueadoCru(x, y) {
      if (x < 6 || x > W - 6) return true; if (y < yw(x) + 8 || y > VH - 3) return true;
      for (const s of this.solids) { const m = (s.x0 + s.x1) / 2, a = yw(m) + s.sy0, b = yw(m) + s.sy1; if (x >= s.x0 && x <= s.x1 && y >= a && y <= b) return true; }
      return false;
    }
    blocked(x, y) { x = Math.round(x); y = Math.round(y); if (x < 0 || x >= W || y < 0 || y > VH) return true; return this.G1[y * W + x] === 1; }
    livre(x, y) { if (Sim.Nav.free(x, y)) return [x, y]; const n = Sim.Nav.nearestFree(x, y); return n || [x, y]; }
    caminho(x0, y0, x1, y1) { const p = Sim.Nav.path(x0, y0, x1, y1); return p ? p.slice() : null; }
    update(dt) { this.t += dt; for (const a of this.lista) a.update(dt); }
  };
})();
