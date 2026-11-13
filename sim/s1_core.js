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
  constructor(o) { o = o || {}; this.min = o.start != null ? o.start : 420; this.rate = o.rate || 1; this.openAt = o.openAt || 420; this.closeAt = o.closeAt || 780; this.day = o.day || 1; this.paused = false; this.ended = false; this.tReal = 0; this.hold = o.hold != null ? o.hold : null; this.mult = 1; }
  // hold = minuto em que o relógio para (a noite permanece); mult = fator de ritmo (cai quando o jogador fica parado). O relógio não decide o fim do dia.
  tick(dt) { if (this.paused || this.ended) return 0; if (this.hold != null && this.min >= this.hold) return 0; this.tReal += dt; let d = dt * this.rate * (this.mult == null ? 1 : this.mult); if (this.hold != null && this.min + d > this.hold) d = this.hold - this.min; this.min += d; return d; }
  get hh() { return Math.floor(this.min / 60); }
  get mm() { return Math.floor(this.min % 60); }
  label() { return String(this.hh).padStart(2, '0') + ':' + String(this.mm).padStart(2, '0'); }
  isOpen() { return this.min >= this.openAt && this.min < this.closeAt; }
  periodo() { const h = this.hh; return h < 9 ? 'manhã cedo' : h < 11 ? 'manhã' : h < 13 ? 'fim de manhã' : 'tarde'; }
  at(hhmm) { const [h, m] = hhmm.split(':').map(Number); return h * 60 + m; }
};

// Missão da sacola de pão do Seu Raimundo. É única: acontece uma vez só, em 1991, e atravessa quantos dias forem precisos.
// estados: nada → balcao (sacola em cima do balcão) → lia (Lia pegou) → entregue (fim, nunca mais volta). Guardado no localStorage.
Sim.Sacola = {
  KEY: 'balcao_sacola', LOCAL: { x: 172, y: 194 },   // onde Lia fica para pegar: de frente para a sacola, entre a vitrine e a caixa
  H() { try { const P = window.parent; if (P && P !== window && P.MUNDO_BRIDGE) return P; } catch (e) { } return typeof window !== 'undefined' ? window : globalThis; },
  ano() { const H = this.H(); return (H && H.MUNDO_ANO) || 1991; },
  get S() {
    const H = this.H(); if (H.__sacola) return H.__sacola;
    const S = H.__sacola = { estado: 'nada' };
    try { const v = typeof localStorage !== 'undefined' && localStorage.getItem(this.KEY); if (v) { const e = JSON.parse(v).estado; if (['balcao', 'lia', 'entregue'].includes(e)) S.estado = e; } } catch (e) { }
    return S;
  },
  salvar() { try { if (typeof localStorage !== 'undefined') localStorage.setItem(this.KEY, JSON.stringify({ estado: this.S.estado })); } catch (e) { } },
  limpar() { try { if (typeof localStorage !== 'undefined') localStorage.removeItem(this.KEY); } catch (e) { } const H = this.H(); if (H) H.__sacola = null; },
  esquece(w) {
    if (this.ano() === 1994) return;
    const S = this.S; if (S.estado !== 'nada') return; S.estado = 'balcao'; S.avisoRua = false; this.salvar(); if (w.bus) w.bus.emit('sacola_aviso', {});
    const v = w.npcs && w.npcs.aurea; if (v && w.dialogue) w.dialogue.speak(v, 'Ih, o Raimundo deixou a sacola de pão em cima do balcão, entre a vitrine e a caixa. Lia, leva lá no sobrado amarelo, aqui do lado.');
  },
  desenharMao(ctx, x, y, face) {                  // a sacola na mão da Lia enquanto ela a leva (padaria, casa e rua)
    if (this.ano() === 1994 || this.S.estado !== 'lia') return;
    const f = String(face || ''), e = f === 'l' || f.indexOf('left') >= 0, d = f === 'r' || f.indexOf('right') >= 0, bx = Math.round(x + (e ? -8 : d ? 8 : 7)), by = Math.round(y - 11);
    ctx.save(); ctx.fillStyle = 'rgba(0,0,0,.22)'; ctx.fillRect(bx - 4, by + 7, 8, 1);
    ctx.fillStyle = '#f0c36a'; ctx.fillRect(bx - 2, by - 3, 2, 4); ctx.fillRect(bx, by - 2, 2, 3);                   // pães pontudos
    ctx.fillStyle = '#b8895a'; ctx.fillRect(bx - 3, by, 7, 7); ctx.fillStyle = '#d4a574'; ctx.fillRect(bx - 3, by, 7, 1); ctx.fillStyle = '#8f6540'; ctx.fillRect(bx - 3, by + 6, 7, 1);
    ctx.fillStyle = '#6b8f71'; ctx.fillRect(bx - 1, by + 2, 3, 2); ctx.fillStyle = '#7a5530'; ctx.fillRect(bx - 3, by - 2, 1, 2); ctx.fillRect(bx + 3, by - 2, 1, 2); ctx.fillRect(bx - 3, by - 3, 7, 1);   // alças
    ctx.restore();
  },
  perto(p) { return Math.hypot(p.x - this.LOCAL.x, (p.y - this.LOCAL.y) * 1.5) < 34; },
  visivel() { return this.ano() !== 1994 && this.S.estado === 'balcao'; },
  painel() {                                     // HTML do painel de objetivos (padaria, casa e rua)
    if (this.ano() === 1994) return ''; const e = this.S.estado; if (e === 'nada') return '';
    const ok = e === 'entregue', l = (f, t) => '<div class="d">' + (f ? '✓ ' : '◦ ') + t + '</div>';
    const peg = e === 'lia' || ok;
    return '<div class="t">' + (ok ? '✓ ' : '◦ ') + 'Levar o pão do Seu Raimundo' + (ok ? ' · cumprida' : '') + '</div>'
      + l(peg, peg ? 'Sacola pega.' : 'Pegar a sacola de pano: está em cima do balcão da padaria, entre a vitrine de pães e a caixa registradora.')
      + l(ok, ok ? 'Entregue ao Seu Raimundo.' : 'Levar ao sobrado amarelo, ao lado da padaria (porta da rua, à esquerda). Ele chega em casa por volta das 10h.')
      + '<div style="margin-bottom:.4em"></div>';
  },
  pegar(w) {
    const S = this.S; if (S.estado !== 'balcao') return false; S.estado = 'lia'; this.salvar();
    const v = w.npcs && w.npcs.aurea; if (v && w.dialogue) w.dialogue.speak(v, 'Isso, minha filha. O sobrado amarelo é aqui do lado, pela esquerda. Ele agradece com café.');
    if (w.bus) w.bus.emit('sacola_pegou', {}); return true;
  },
  entrega(w) {                                   // chamado na casa, perto de Raimundo
    const S = this.S; if (S.estado !== 'lia' || !w.casaPick) return false; S.estado = 'entregue'; this.salvar();
    const R = w.npcs.raimundo; try { w.dialogue.speak(R, 'O pão! Cabeça de quem tem muita coisa pra lembrar. Fica pra um café, minha filha?'); } catch (e) { }
    w.rel.change('raimundo', 'lia', { aff: .08, trust: .1 }, 'sacola'); w.knowledge.award('kp_c_sacola_pao', { via: 'entregou' }); if (w.bus) w.bus.emit('sacola_entregue', {}); return true;
  },
};
;Sim.saudarHora = (txt, min) => typeof txt !== 'string' ? txt : (min >= 1080 ? txt.replace(/\bBom dia\b/g, 'Boa noite') : min >= 720 ? txt.replace(/\bBom dia\b/g, 'Boa tarde') : txt);   // a saudação acompanha a hora do relógio
