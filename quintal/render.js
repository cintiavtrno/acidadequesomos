// ===== render.js — tela do quintal (3/4): camadas estáticas + objetos e personagens ordenados pelo y da base + copa da mangueira =====
(function (Q) {
  'use strict';
  const { sx, sy } = Q, W = 720, H = 270;
  const PAL = (typeof window !== 'undefined' && window.PAL) || {}, TI = PAL.TIMB, CA = PAL.CAL, ST = PAL.STONE, TE = PAL.TELHA, LF = PAL.LEAF, GL = PAL.GLASS, WD = PAL.WOOD, SR = PAL.STRAW, CL = PAL.CLAY, RD = PAL.RED, SK = PAL.SACK, IR = PAL.IRON;
  const rng = s => () => { s |= 0; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const shade = (c, f) => { const n = parseInt(c.slice(1), 16), r = Math.min(255, (n >> 16) * f) | 0, g = Math.min(255, (n >> 8 & 255) * f) | 0, b = Math.min(255, (n & 255) * f) | 0; return 'rgb(' + r + ',' + g + ',' + b + ')'; };
  const SPR = {}; for (const w of ['lia', 'aurea', 'raimundo', 'dandara', 'lucia', 'ze', 'nonato', 'bela', 'cicera', 'junior', 'tonho', 'zefa', 'nena', 'davi', 'rita', 'caio', 'bia', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6']) SPR[w] = [w, 'tq'];
  const COR = { zefa: '#d9534f', nena: '#e8e2d2', davi: '#3b3b44', rita: '#a3566b', caio: '#5a8f3d', bia: '#c0689a' };
  const RAMPA = { F07: IR, F08: SK, F09: TI, F10: ST, F11: CL, F12: TI, F13: TI, M01: TI, M09: TI, M14: TI, M22: CL, M25: TI, M26: TI, M27: SR, F15: ST, F05: TI, F06: TI };
  const KIDS = [ // [camisa 4 tons claro→escuro, short 3 tons]
    [[[246, 214, 120], [226, 178, 70], [186, 136, 44], [140, 98, 34]], [[96, 120, 90], [70, 92, 70], [48, 66, 52]]],
    [[[150, 200, 150], [104, 160, 108], [70, 120, 80], [48, 88, 60]], [[170, 120, 80], [130, 88, 58], [92, 62, 42]]],
    [[[240, 232, 214], [214, 204, 184], [176, 166, 148], [132, 124, 112]], [[74, 116, 196], [50, 86, 160], [36, 64, 122]]],
    [[[240, 170, 110], [222, 128, 70], [184, 92, 48], [140, 66, 40]], [[96, 96, 112], [70, 70, 86], [50, 50, 64]]],
    [[[190, 150, 210], [150, 108, 178], [112, 74, 142], [80, 52, 108]], [[200, 190, 160], [168, 156, 126], [130, 120, 96]]],
    [[[120, 196, 200], [76, 152, 162], [50, 112, 126], [36, 82, 96]], [[150, 70, 64], [116, 50, 48], [84, 36, 38]]],
  ];
  const J_SHIRT = [[238, 132, 112], [216, 90, 70], [180, 56, 44], [138, 42, 34]], J_SHORT = [[74, 116, 196], [50, 86, 160], [36, 64, 122]];
  const BRICKC = i => PAL.BRICK ? PAL.BRICK[[2, 3, 2, 4][i % 4]] : '#a34f3e';
  class Render {
    constructor(cv, sim, CharLib) {
      this.cv = cv; this.ctx = cv.getContext('2d'); this.sim = sim; this.CL = CharLib; this.D = sim.D; this.cam = 0; this.t = 0;
      this.ctx.imageSmoothingEnabled = false; this.fig = {};
      this.face = {}; for (const k in this.D.SEATS) { const s = this.D.SEATS[k]; this.face[s[2]] = this.face[s[2]] || sim.seatDir(k); }
      this.cat = (window.QCAT && window.QCAT.sprites) || {}; this.est = this.compoe(true); this.estN = this.compoe(false); this.copa = CharLib.img.q_copa;
    }
    kids() {
      const CLb = this.CL, a = CLb.atlas.junior_side, im = CLb.img.junior_side; if (!a || !im) return;
      for (let i = 1; i <= 6; i++) {
        const c = document.createElement('canvas'); c.width = im.width; c.height = im.height; const g = c.getContext('2d'); g.drawImage(im, 0, 0);
        const d = g.getImageData(0, 0, c.width, c.height), px = d.data, map = {}, v = KIDS[i - 1];
        J_SHIRT.forEach((k, j) => map[k.join()] = v[0][j]); J_SHORT.forEach((k, j) => map[k.join()] = v[1][j]);
        for (let o = 0; o < px.length; o += 4) { if (!px[o + 3]) continue; const m = map[px[o] + ',' + px[o + 1] + ',' + px[o + 2]]; if (m) { px[o] = m[0]; px[o + 1] = m[1]; px[o + 2] = m[2]; } }
        g.putImageData(d, 0, 0); CLb.atlas['m' + i + '_side'] = a; CLb.img['m' + i + '_side'] = c;
      }
    }
    P(X, Y, Z) { return [sx(X), sy(Y, Z)]; }
    compoe(tema) {
      const c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(this.CL.img.q_base, 0, 0);
      for (const k in this.cat) if (tema && this.cat[k].layer === 'parede') this.spr(g, k); return c;
    }
    spr(g, id) { const s = this.cat[id]; if (!s) return false; const im = this.CL.img['q_' + s.folha.replace('.png', '')], r = s.rect; g.drawImage(im, r[0], r[1], r[2], r[3], s.pos_px[0], s.pos_px[1], r[2], r[3]); return true; }
    buildStatic() {
      const c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d'), D = this.D, R = rng(11), P = (X, Y, Z) => this.P(X, Y, Z);
      const px = (x, y, w, h, col) => { g.fillStyle = col; g.fillRect(Math.round(x), Math.round(y), Math.round(w), Math.round(h)); };
      const rect = (X0, Y0, Z0, X1, Y1, Z1, col) => { const a = P(X0, Y0, Z1), b = P(X1, Y1, Z0); px(a[0], a[1], b[0] - a[0], b[1] - a[1], col); };
      // céu em faixas planas
      px(0, 0, W, 40, '#8fb9cc'); px(0, 40, W, 40, '#a6c8d4'); px(0, 80, W, 70, '#bfd8dc');
      // casa de Rita: parede, telhado de telha com fiadas e cumeeira, dano com lona azul
      const Rt = D.RITA, bx0 = sx(Rt.x0), bx1 = sx(Rt.x1), by = sy(Rt.y_beiral, Rt.z_beiral), cy = sy(Rt.y_cume, Rt.z_cume);
      rect(Rt.x0, Rt.y_beiral, 0, Rt.x1, Rt.y_beiral, Rt.z_beiral, CA[2]); px(bx0, by - 2, bx1 - bx0, 3, CA[1]);
      for (let y = cy, k = 0; y < by - 2; y += 3, k++) { px(bx0, y, bx1 - bx0, 3, TE[k % 2 ? 2 : 1]); px(bx0, y, bx1 - bx0, 1, TE[k % 2 ? 3 : 2]); for (let x = bx0 + (k % 2) * 3; x < bx1; x += 6) px(x, y + 1, 1, 2, TE[0]); }
      px(bx0, cy - 2, bx1 - bx0, 3, TE[3]); px(bx0, cy, bx1 - bx0, 1, TE[0]); px(bx0, by - 3, bx1 - bx0, 1, TE[0]);
      { const a = sx(Rt.dano_x0), b = sx(Rt.dano_x1); px(a, by - 24, b - a, 22, GL[2]); for (let i = 0; i < 5; i++) px(a + 2 + i * 7, by - 24, 2, 22, GL[1]); px(a, by - 24, b - a, 1, GL[4]); px(a + 1, by - 3, b - a - 2, 1, GL[0]); px(a + 6, by - 30, 6, 6, ST[4]); px(a + 6, by - 30, 6, 1, ST[1]); px(a + 6, by - 24, 6, 1, ST[1]); }
      // parede da casa de Zefa: reboco liso com variação em manchas largas, umidade ascendente e uma falha de reboco localizada
      rect(0, 0, 0, 11, 0, 4, CA[2]);
      for (let k = 0; k < 14; k++) { const x = R() * 260 + 24, y = 28 + R() * 70, w = 30 + R() * 60, h = 10 + R() * 22; g.fillStyle = k % 2 ? 'rgba(222,218,207,.33)' : 'rgba(176,153,140,.18)'; g.fillRect(x | 0, y | 0, w | 0, h | 0); }
      { const a = P(0, 0, 0.28), b = P(11, 0, 0); for (let x = a[0]; x < b[0]; x++) { const hh = 14 + 6 * Math.sin(x * 0.11) + 3 * Math.sin(x * 0.37); px(x, a[1] - hh, 1, hh, 'rgba(147,108,109,.20)'); } }
      { const a = P(9.9, 0, 1.1), b = P(11, 0, 0.28); px(a[0], a[1] + 14, b[0] - a[0], b[1] - a[1] - 14, BRICKC(0)); for (let i = 0; i < 18; i++) px(a[0] + (i % 6) * 5 + (((i / 6) | 0) % 2) * 2, a[1] + 14 + ((i / 6) | 0) * 4, 4, 3, BRICKC(1 + (i % 3))); px(a[0], a[1] + 12, b[0] - a[0], 2, CA[1]); }
      rect(0, 0, 0, 11, 0, 0.28, ST[2]); rect(0, 0, 0.26, 11, 0, 0.3, ST[3]); rect(0, 0, 3.86, 11, 0, 4, CA[4]); rect(0, 0, 3.8, 11, 0, 3.86, CA[1]);
      // muro de divisa
      rect(11, 0, 0, 28, 0, 2.4, CA[3]);
      for (let k = 0; k < 22; k++) { const x = sx(11) + R() * 380, y = sy(0, 2.3) + R() * 36, w = 20 + R() * 40, h = 8 + R() * 16; g.fillStyle = k % 2 ? 'rgba(203,196,174,.45)' : 'rgba(176,153,140,.25)'; g.fillRect(x | 0, y | 0, w | 0, h | 0); }
      rect(11, 0, 0, 28, 0, 0.22, CA[1]); rect(11, 0, 2.28, 28, 0, 2.4, ST[3]); rect(11, 0, 2.38, 28, 0, 2.4, ST[4]); rect(11, 0, 2.2, 28, 0, 2.28, CA[1]);
      g.fillStyle = CA[1]; g.fillRect(sx(0) - 7, sy(0, 2.4), 7, sy(8, 0) - sy(0, 2.4)); g.fillRect(sx(28), sy(0, 2.4), 7, sy(8, 0) - sy(0, 2.4)); px(sx(0) - 7, sy(0, 2.4), 7, 2, ST[3]); px(sx(28), sy(0, 2.4), 7, 2, ST[3]);
      // janela da cozinha: caixilho, vidro, duas folhas abertas de venezianas verdes, peitoril de pedra
      { const o = D.OPEN.janela; rect(o.x0 - .1, 0, o.z0 - .1, o.x1 + .1, 0, o.z1 + .1, TI[1]); rect(o.x0, 0, o.z0, o.x1, 0, o.z1, GL[3]); rect(o.x0, 0, o.z1 - .5, o.x1, 0, o.z1, GL[4]);
        rect(o.x0 + .58, 0, o.z0, o.x0 + .62, 0, o.z1, TI[2]); rect(o.x0, 0, o.z0 + .5, o.x1, 0, o.z0 + .54, TI[2]);
        for (const s2 of [-1, 1]) { const xa = s2 < 0 ? o.x0 - .32 : o.x1, xb = s2 < 0 ? o.x0 : o.x1 + .32; rect(xa, 0, o.z0, xb, 0, o.z1, WD[2]); for (let z = o.z0 + .08; z < o.z1; z += .12) rect(xa + .02, 0, z, xb - .02, 0, z + .03, WD[1]); rect(xa, 0, o.z0, xa + .03, 0, o.z1, WD[4]); }
        rect(o.x0 - .15, 0, o.z0 - .1, o.x1 + .15, 0, o.z0 - .04, ST[4]); rect(o.x0 - .15, 0, o.z0 - .13, o.x1 + .15, 0, o.z0 - .1, ST[1]); }
      // porta de serviço: batente, duas almofadas, maçaneta, soleira
      { const o = D.OPEN.servico; rect(o.x0 - .1, 0, 0, o.x1 + .1, 0, o.h + .1, TI[1]); rect(o.x0, 0, 0, o.x1, 0, o.h, WD[2]); rect(o.x0, 0, 0, o.x0 + .04, 0, o.h, WD[4]);
        rect(o.x0 + .14, 0, .18, o.x1 - .14, 0, 1.05, WD[1]); rect(o.x0 + .17, 0, .21, o.x1 - .17, 0, 1.02, WD[3]); rect(o.x0 + .14, 0, 1.2, o.x1 - .14, 0, o.h - .14, WD[1]); rect(o.x0 + .17, 0, 1.23, o.x1 - .17, 0, o.h - .17, WD[3]);
        rect(o.x1 - .26, 0, 1.0, o.x1 - .18, 0, 1.1, SR[2]); rect(o.x0 - .12, 0, 0, o.x1 + .12, 0, .06, ST[4]); }
      // portão de Rita (lado direito, de perfil)
      { const o = D.OPEN.portao; g.fillStyle = TI[2]; g.beginPath(); [P(28, o.y0, 0), P(28, o.y1, 0), P(28, o.y1, 1.8), P(28, o.y0, 1.8)].forEach((p, i) => i ? g.lineTo(p[0] + 4, p[1]) : g.moveTo(p[0] + 4, p[1])); g.fill(); g.fillStyle = TI[1]; g.fillRect(sx(28) + 3, sy(o.y0, 1.8), 1, sy(o.y1, 0) - sy(o.y0, 1.8)); }
      this.bandeira(g);
      // piso de cimento queimado: lajes grandes com tom próprio, juntas finas, desgaste em manchas largas e poucas trincas
      const f0 = P(0, 0, 0), f1 = P(28, 8, 0);
      for (let i = 0, X = 0; X < 28; X += 1.4, i++) for (let j = 0, Y = 0; Y < 8; Y += 1.0, j++) { const a = P(X, Y, 0), b = P(Math.min(28, X + 1.4), Math.min(8, Y + 1), 0), t = R(); g.fillStyle = t < .33 ? '#b8a48c' : t < .66 ? '#bda993' : '#b09c85'; g.fillRect(Math.round(a[0]), Math.round(a[1]), Math.round(b[0] - a[0]), Math.round(b[1] - a[1])); }
      for (let X = 1.4; X < 28; X += 1.4) { g.fillStyle = 'rgba(147,108,109,.35)'; g.fillRect(sx(X), f0[1], 1, f1[1] - f0[1]); }
      for (let Y = 1; Y < 8; Y++) { g.fillStyle = 'rgba(147,108,109,.30)'; g.fillRect(f0[0], sy(Y, 0), f1[0] - f0[0], 1); }
      for (let k = 0; k < 12; k++) { const x = f0[0] + R() * (f1[0] - f0[0]), y = f0[1] + R() * (f1[1] - f0[1]); g.fillStyle = k % 2 ? 'rgba(222,218,207,.18)' : 'rgba(80,42,59,.10)'; g.beginPath(); g.ellipse(x, y, 20 + R() * 36, 5 + R() * 9, 0, 0, 7); g.fill(); }
      g.strokeStyle = 'rgba(80,42,59,.35)'; g.lineWidth = 1; for (let k = 0; k < 5; k++) { let x = f0[0] + R() * (f1[0] - f0[0]), y = f0[1] + 12 + R() * (f1[1] - f0[1] - 20); g.beginPath(); g.moveTo(x | 0, y | 0); for (let i = 0; i < 4; i++) { x += 4 + R() * 6; y += (R() - .5) * 5; g.lineTo(x | 0, y | 0); } g.stroke(); }
      { const s2 = D.OPEN.soleira; g.fillStyle = 'rgba(80,42,59,.12)'; g.fillRect(sx(s2.x0), sy(4.5, 0), sx(s2.x1) - sx(s2.x0), sy(8, 0) - sy(4.5, 0)); }
      // sob o puxadinho e sombra da mangueira
      { const U = D.PUX, a = P(U.x0, U.y0, 0), b = P(U.x1, U.y1, 0); px(a[0], a[1], b[0] - a[0], b[1] - a[1], 'rgba(45,26,31,.30)'); px(a[0], a[1], b[0] - a[0], 8, 'rgba(45,26,31,.18)'); }
      { const m = D.MANGA, c2 = this.P(m.copa_c[0] + 0.3, m.copa_c[1] + 1.0, 0); for (let r = 0; r < 3; r++) { g.fillStyle = 'rgba(30,52,44,.17)'; g.beginPath(); g.ellipse(c2[0], c2[1], 70 - r * 13, 34 - r * 6, 0, 0, 7); g.fill(); } }
      px(0, sy(0, 2.4), sx(0) - 7, sy(8, 0) - sy(0, 2.4), CA[1]); px(sx(28) + 7, sy(0, 2.4), W - sx(28) - 7, sy(8, 0) - sy(0, 2.4), CA[1]);
      // calçada de pedra e soleira
      px(0, f1[1], W, H - f1[1], ST[2]); for (let r = 0, y = f1[1]; y < H; y += 7, r++) { px(0, y, W, 1, ST[1]); for (let x = (r % 2) * 14; x < W; x += 28) px(x, y, 1, 7, ST[1]); } px(0, f1[1], W, 1, ST[3]);
      { const s2 = D.OPEN.soleira; px(sx(s2.x0), f1[1] - 3, sx(s2.x1) - sx(s2.x0), 7, ST[4]); px(sx(s2.x0), f1[1] - 3, sx(s2.x1) - sx(s2.x0), 1, '#f2f1ee'); px(sx(s2.x0), f1[1] + 4, sx(s2.x1) - sx(s2.x0), 1, ST[2]); }
      // puxadinho: rufo, telhas em corte e viga frontal com mãos-francesas
      { const U = D.PUX, a = P(U.x0, 0, U.z_fundo), b = P(U.x1, 0, U.z_fundo); px(a[0], a[1], b[0] - a[0], 3, TE[1]); px(a[0], a[1], b[0] - a[0], 1, TE[3]); for (let i = a[0]; i < b[0]; i += 5) px(i, a[1] - 3, 3, 3, TE[2]);
        const c1 = P(U.x0, U.y1, U.z_frente), d1 = P(U.x1, U.y1, U.z_frente); px(c1[0], c1[1], d1[0] - c1[0], 5, TI[2]); px(c1[0], c1[1], d1[0] - c1[0], 1, TI[4]); px(c1[0], c1[1] + 5, d1[0] - c1[0], 1, TI[0]); }
      return c;
    }
    bandeira(g) {
      const b = this.D.BANDEIRA, a = this.P(b.x0, 0, b.z1), z = this.P(b.x1, 0, b.z0), x0 = Math.round(a[0]), y0 = Math.round(a[1]), w = Math.round(z[0] - a[0]), h = Math.round(z[1] - a[1]);
      const px = (x, y, ww, hh, col) => { g.fillStyle = col; g.fillRect(x, y, ww, hh); };
      px(x0 + 2, y0 + 3, w, h, 'rgba(45,26,31,.30)');                                          // sombra do pano
      px(x0 - 2, y0 - 3, w + 4, 3, TI[2]); px(x0 - 2, y0 - 3, w + 4, 1, TI[4]); px(x0 - 2, y0 + h, w + 4, 3, TI[2]); px(x0 - 2, y0 + h + 2, w + 4, 1, TI[0]);   // varetas
      px(x0 - 3, y0 - 4, 2, 5, TI[1]); px(x0 + w + 1, y0 - 4, 2, 5, TI[1]);
      px(x0 + w / 2 - 4, y0 - 7, 1, 4, TI[1]); px(x0 + w / 2 + 3, y0 - 7, 1, 4, TI[1]); px(x0 + w / 2 - 4, y0 - 8, 8, 1, TI[1]);   // cordão
      px(x0, y0, w, h, '#4d7f7b'); for (let x = x0 + 1; x < x0 + w; x += 3) px(x, y0, 1, h, 'rgba(255,255,255,.06)'); px(x0, y0, 2, h, 'rgba(30,52,44,.25)'); px(x0 + w - 2, y0, 2, h, 'rgba(30,52,44,.35)');
      px(x0 + 2, y0 + 2, w - 4, 1, SR[2]); px(x0 + 2, y0 + h - 3, w - 4, 1, SR[2]); px(x0 + 2, y0 + 2, 1, h - 4, SR[2]); px(x0 + w - 3, y0 + 2, 1, h - 4, SR[2]);
      px(x0 + 4, y0 + 4, w - 8, 1, RD[2]); px(x0 + 4, y0 + h - 5, w - 8, 1, RD[2]);
      for (let x = x0 + 1; x < x0 + w - 1; x += 2) { px(x, y0 + h, 1, 4, SR[3]); px(x, y0 + h + 3, 1, 1, SR[1]); }       // franja
      const cx = x0 + Math.round(w / 2), top = y0 + 12;
      const santo = (sx0, rb, skin) => {   // 13 × ~36 px
        const x = sx0 - 6;
        g.fillStyle = SR[3]; g.beginPath(); g.ellipse(sx0, top + 4, 7, 5, 0, 0, 7); g.fill(); g.fillStyle = '#4d7f7b'; g.beginPath(); g.ellipse(sx0, top + 5, 5, 4, 0, 0, 7); g.fill();   // auréola
        px(x + 3, top + 2, 7, 1, TI[0]); px(x + 3, top + 2, 7, 3, TI[0]); px(x + 3, top + 4, 7, 6, skin[0]); px(x + 9, top + 4, 1, 6, skin[1]); px(x + 4, top + 7, 1, 1, TI[0]); px(x + 8, top + 7, 1, 1, TI[0]); px(x + 5, top + 9, 3, 1, skin[1]);
        px(x + 5, top + 10, 3, 2, skin[1]);                                                                                        // pescoço
        for (let i = 0; i < 24; i++) { const half = 3 + Math.floor(i * 0.22); px(sx0 - half - 1, top + 12 + i, half * 2 + 2, 1, rb[1]); px(sx0 - half - 1, top + 12 + i, 2, 1, rb[2]); px(sx0 + half, top + 12 + i, 2, 1, rb[0]); if (i % 6 === 5) px(sx0 - half + 1, top + 12 + i, half * 2 - 1, 1, rb[0]); }
        px(sx0 - 4, top + 12, 8, 3, rb[2]); px(sx0 - 4, top + 24, 9, 1, SR[2]);                                                    // gola e cinto
        px(sx0 - 3, top + 36, 3, 2, skin[1]); px(sx0 + 1, top + 36, 3, 2, skin[1]);                                                // pés
      };
      santo(cx - 8, [RD[1], RD[2], RD[3]], ['#c08a62', '#8f5c40']); santo(cx + 8, ['#26385e', '#3f5f93', '#5b80b3'], ['#b27a54', '#80503a']);
      px(cx - 3, top + 24, 6, 3, '#c08a62'); px(cx - 3, top + 24, 6, 1, '#d9ab86');                                                   // mãos dadas
      px(cx - 1, y0 + 6, 2, 2, SR[3]); px(cx - 11, y0 + 8, 1, 1, SR[3]); px(cx + 10, y0 + 8, 1, 1, SR[3]);
      for (let i = 0; i < 6; i++) { px(x0 + 5 + i * Math.floor((w - 10) / 5), y0 + h - 9 + (i % 2), 3, 2, i % 2 ? LF[3] : RD[3]); }   // guirlanda embaixo
    }
    buildCopa() {
      const c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d'), R = rng(5), H_ = this.D.HULL;
      const path = () => { g.beginPath(); H_.forEach((p, i) => i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1])); g.closePath(); };
      path(); g.fillStyle = LF[1]; g.fill(); g.save(); path(); g.clip();
      const xs = H_.map(p => p[0]), ys = H_.map(p => p[1]), x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys), cl = [];
      for (let i = 0; i < 150; i++) cl.push([x0 + R() * (x1 - x0), y0 + R() * (y1 - y0), 6 + R() * 7]);
      cl.sort((a, b) => a[1] - b[1]);
      for (const [x, y, r] of cl) { const up = 1 - (y - y0) / (y1 - y0), lx = 1 - (x - x0) / (x1 - x0), lit = 0.5 * up + 0.5 * lx;
        g.fillStyle = LF[0]; g.beginPath(); g.ellipse(x, y + 2, r, r * .72, 0, 0, 7); g.fill();
        g.fillStyle = lit > .62 ? LF[3] : lit > .36 ? LF[2] : LF[1]; g.beginPath(); g.ellipse(x, y, r, r * .7, 0, 0, 7); g.fill();
        g.fillStyle = lit > .5 ? LF[4] : LF[3]; g.beginPath(); g.ellipse(x - r * .25, y - r * .28, r * .45, r * .26, 0, 0, 7); g.fill(); }
      for (let i = 0; i < 40; i++) { const x = x0 + R() * (x1 - x0), y = y0 + R() * (y1 - y0); g.fillStyle = LF[0]; g.fillRect(x | 0, y | 0, 3, 1); }
      for (let i = 0; i < 7; i++) { const x = x0 + 12 + R() * (x1 - x0 - 24), y = y0 + (y1 - y0) * (.45 + R() * .5); g.fillStyle = SR[2]; g.fillRect(x | 0, y | 0, 3, 4); g.fillStyle = SR[1]; g.fillRect(x | 0, (y | 0) + 3, 3, 1); g.fillStyle = SR[3]; g.fillRect(x | 0, y | 0, 1, 1); }
      g.restore(); path(); g.strokeStyle = LF[0]; g.lineWidth = 1; g.stroke();
      return c;
    }
    box(g, x, y, w, d, h, z, r, r2) {
      const a = this.P(x, y, z + h), b = this.P(x + w, y + d, z + h), f = this.P(x + w, y + d, z), x0 = Math.round(a[0]), x1 = Math.round(b[0]), yt = Math.round(a[1]), yb = Math.round(b[1]), yf = Math.round(f[1]);
      if (typeof r === 'string') r = [r2, r2, r2, r, r];                      // compatibilidade (cores soltas)
      g.fillStyle = r[2]; g.fillRect(x0, yb, x1 - x0, Math.max(1, yf - yb)); g.fillStyle = r[3]; g.fillRect(x0, yt, x1 - x0, Math.max(1, yb - yt));
      g.fillStyle = r[4]; g.fillRect(x0, yt, x1 - x0, 1); g.fillRect(x0, yb, 1, Math.max(0, yf - yb)); g.fillStyle = r[1]; g.fillRect(x1 - 1, yb, 1, Math.max(0, yf - yb)); g.fillRect(x0, yf - 1, x1 - x0, 1);
      g.fillStyle = r[2]; g.fillRect(x0, yb - 1, x1 - x0, 1); g.fillStyle = r[1]; g.fillRect(x0, yb, x1 - x0, 1);
      if (z === 0) { g.fillStyle = 'rgba(45,26,31,.22)'; g.fillRect(x0 + 1, yf, x1 - x0, 1); g.fillStyle = 'rgba(45,26,31,.10)'; g.fillRect(x0 + 2, yf + 1, x1 - x0 - 1, 1); }
    }
    obj(g, o) {
      const id = o.id; if (this.spr(g, this.sim.normal && id === 'M01' ? 'M01n' : id)) return;
      if (id === 'F14') { const a = this.P(o.x - 0.1, o.y, 0), r = Math.round; g.fillStyle = TI[0]; g.fillRect(r(a[0]) - 2, r(a[1]) - 2, 18, 4); g.fillStyle = TI[1]; g.fillRect(r(sx(22.25)), r(sy(2.6, 2.8)), 19, r(sy(2.8, 0) - sy(2.6, 2.8))); g.fillStyle = TI[2]; g.fillRect(r(sx(22.25)) + 3, r(sy(2.6, 2.8)), 3, r(sy(2.8, 0) - sy(2.6, 2.8))); g.fillStyle = TI[0]; g.fillRect(r(sx(22.25)) + 14, r(sy(2.6, 2.8)), 5, r(sy(2.8, 0) - sy(2.6, 2.8))); return; }
      if (/^M(0[2-7]|1[5-8]|20)$/.test(id) || /^M2[34]$/.test(id) || /^M1[0-3]$/.test(id) || id === 'M21' || id === 'M19' || id === 'M08') return this.assento(g, o);
      const rp = o.cat === 'D' ? LF : (RAMPA[id] || RAMPA[id.replace(/[ab]$/, '')] || TI);
      this.box(g, o.x, o.y, o.w, o.d, o.h, 0, rp);
      if (id === 'F08') { const a = this.P(o.x, o.y, o.h); g.fillStyle = '#2b2b2b'; for (let i = 0; i < 4; i++) g.fillRect(a[0] + 3 + (i % 2) * 9, a[1] + 1 + ((i / 2) | 0) * 3, 6, 2); g.fillStyle = '#7a8a9a'; g.fillRect(a[0] + 2, a[1] + 14, 18, 2); }
      if (id === 'F07') { const a = this.P(o.x, o.y, 0.5), t = this.t; g.fillStyle = IR[1]; g.fillRect(a[0] + 4, a[1] - 7, 24, 10); g.fillStyle = IR[3]; g.fillRect(a[0] + 5, a[1] - 9, 22, 3); g.fillStyle = IR[4]; g.fillRect(a[0] + 5, a[1] - 9, 22, 1); g.fillStyle = RD[1]; g.fillRect(a[0] + 4, a[1] + 8, 24, 3); g.fillStyle = (Math.sin(t * 9) > 0) ? '#e08a2a' : '#f0c24a'; g.fillRect(a[0] + 8, a[1] + 6, 4, 3); g.fillRect(a[0] + 17, a[1] + 5 + (Math.sin(t * 7) > 0 ? 0 : 1), 5, 4); }
      if (id === 'F10') { const a = this.P(o.x, o.y, o.h); g.fillStyle = GL[3]; g.fillRect(a[0] + 2, a[1] + 1, 20, 7); g.fillStyle = GL[4]; g.fillRect(a[0] + 2, a[1] + 1, 20, 1); g.fillStyle = IR[4]; g.fillRect(a[0] + 10, a[1] - 5, 2, 6); g.fillRect(a[0] + 10, a[1] - 5, 5, 1); if (Math.floor(this.t * 1.5) % 2) { g.fillStyle = GL[4]; g.fillRect(a[0] + 14, a[1] - 3, 1, 2); } }
      if (id === 'F12') { const a = this.P(o.x, o.y + o.d, 0.2); g.fillStyle = 'rgba(0,0,0,.15)'; for (let i = 0; i < 6; i++) g.fillRect(a[0] + 3 + i * 14, a[1] - 14, 1, 12); }
      if (id === 'M01') { const a = this.P(o.x, o.y, o.h), b = this.P(o.x + o.w, o.y + o.d, o.h); g.fillStyle = SK[3]; g.fillRect(a[0], a[1], b[0] - a[0], b[1] - a[1]); g.fillStyle = SR[2]; for (let x = a[0] + 2; x < b[0]; x += 4) g.fillRect(x, a[1] + 1, 2, 1); g.fillStyle = SK[1]; g.fillRect(a[0], a[1] + (b[1] - a[1]) - 1, b[0] - a[0], 1); g.fillStyle = SK[2]; g.fillRect(a[0], b[1], b[0] - a[0], 4); }
    }
    assento(g, o) {
      const f = this.face[o.id] || 'down', big = o.w > 1.2;
      if (o.h <= 0.5 || big) { this.box(g, o.x, o.y, o.w, o.d, o.h, 0, TI); return; }
      // cadeira: assento + encosto do lado oposto ao rosto de quem senta
      const seatH = 0.45; this.box(g, o.x + .02, o.y + .02, o.w - .04, o.d - .04, 0.06, seatH - 0.06, TI);
      g.fillStyle = TI[1]; for (const [px, py] of [[o.x + .04, o.y + o.d - .04], [o.x + o.w - .08, o.y + o.d - .04]]) { const a = this.P(px, py, seatH - 0.06), b = this.P(px, py, 0); g.fillRect(a[0], a[1], 2, b[1] - a[1]); }
      const encosto = (x0, y0, x1, y1) => this.box(g, x0, y0, x1 - x0, y1 - y0, 0.42, seatH, TI);
      if (f === 'down') encosto(o.x + .02, o.y, o.x + o.w - .02, o.y + .06); else if (f === 'up') encosto(o.x + .02, o.y + o.d - .06, o.x + o.w - .02, o.y + o.d);
      else if (f === 'right') encosto(o.x, o.y + .02, o.x + .06, o.y + o.d - .02); else encosto(o.x + o.w - .06, o.y + .02, o.x + o.w, o.y + o.d - .02);
    }
    item(g, s) {
      if (this.spr(g, s.id)) return;
      const n = s.nome.toLowerCase(), a = this.P(s.x, s.y, s.z + s.h), b = this.P(s.x + s.w, s.y + s.d, s.z + s.h), f = this.P(s.x + s.w, s.y + s.d, s.z), cx = (a[0] + b[0]) / 2, w = Math.max(2, b[0] - a[0]);
      const cor = /prato dos santos/.test(n) ? SK[4] : /pratinho|prato|pilha/.test(n) ? SK[3] : /pratinho/.test(n) ? CL[2] : /vela/.test(n) ? SR[4] : /flores|vasinho/.test(n) ? LF[3] : /caruru|vatap|travessa|caçarola|panela|tacho/.test(n) ? SR[2] : /arroz|farofa/.test(n) ? SR[3] : /bacia/.test(n) ? GL[4] : /jarra|balde|copo/.test(n) ? GL[4] : /cesto|bandeja|tábua|facas|colher|cuia/.test(n) ? TI[3] : SR[3];
      if (/toalha/.test(n)) return;
      if (/bacia|travessa|panela|caçarola|tacho|balde|cesto|bandeja|pratinho|prato|pilha|cocada/.test(n)) {
        const h = Math.max(2, f[1] - b[1] + (b[1] - a[1])); g.fillStyle = shade(cor, .78); g.fillRect(a[0], b[1] - 1, w, Math.max(2, f[1] - b[1] + 1)); g.fillStyle = cor; g.fillRect(a[0], a[1], w, Math.max(2, b[1] - a[1] + 1));
        if (/caruru|vatap|farofa|arroz|cocada/.test(n) || /bacia central|pratinho/.test(n)) { g.fillStyle = /vatap/.test(n) ? SR[2] : /caruru/.test(n) ? SR[1] : /farofa|arroz/.test(n) ? SR[3] : TI[2]; g.fillRect(a[0] + 1, a[1], Math.max(1, w - 2), Math.max(1, b[1] - a[1] - 0)); }
        if (/prato dos santos/.test(n)) { g.fillStyle = RD[2]; g.fillRect(cx - 1, a[1], 2, 1); }
      } else if (/vela/.test(n)) { g.fillStyle = cor; g.fillRect(cx - 1, a[1], 2, Math.max(2, f[1] - a[1])); g.fillStyle = (Math.sin(this.t * 10) > 0) ? SR[3] : SR[2]; g.fillRect(cx - 1, a[1] - 3, 2, 3); g.fillStyle = 'rgba(255,220,120,.25)'; g.fillRect(cx - 4, a[1] - 5, 8, 8); }
      else if (/flores|vasinho/.test(n)) { g.fillStyle = CL[1]; g.fillRect(cx - 2, f[1] - 4, 4, 4); g.fillStyle = LF[3]; g.fillRect(cx - 2, a[1] + 1, 4, f[1] - a[1] - 4); g.fillStyle = SK[4]; g.fillRect(cx - 3, a[1], 2, 2); g.fillRect(cx + 1, a[1] + 1, 2, 2); g.fillRect(cx - 1, a[1] - 1, 2, 2); }
      else if (/jarra|copos|copinhos|cuia|balde|colher|facas|conchas|peças/.test(n)) { g.fillStyle = shade(cor, .8); g.fillRect(a[0], a[1] + 1, w, Math.max(2, f[1] - a[1] - 1)); g.fillStyle = cor; g.fillRect(a[0], a[1], w, Math.max(1, b[1] - a[1])); }
      else { g.fillStyle = shade(cor, .8); g.fillRect(a[0], a[1], w, Math.max(1, f[1] - a[1])); g.fillStyle = cor; g.fillRect(a[0], a[1], w, Math.max(1, b[1] - a[1])); }
    }
    figura(g, e, px, py, alpha) {
      const h = this.D.CH[e.id][1] * 24 * (e.state === 'sentado' ? 0.72 : 1), col = COR[e.id] || '#888', moving = e.anim === 'walk', bob = moving ? Math.round(Math.sin(this.t * 9 + e.x) * 1) : 0;
      g.save(); g.globalAlpha = alpha; g.fillStyle = 'rgba(18,10,28,.34)'; g.fillRect(px - 5, py - 1, 10, 2); g.fillStyle = shade(col, .7); g.fillRect(px - 4, py - h * .42 + bob, 3, h * .42); g.fillRect(px + 1, py - h * .42 + bob, 3, h * .42);
      g.fillStyle = col; g.fillRect(px - 5, py - h * .78 + bob, 10, h * .4); g.fillStyle = '#6b4a35'; g.fillRect(px - 4, py - h + bob, 8, h * .22); g.fillStyle = shade(col, 1.2); g.fillRect(px - 5, py - h * .75 + bob, 2, h * .3); g.restore();
    }
    ent(g, e, alpha) {
      const sp = SPR[e.id], k = e.state === 'sentado' ? this.keySeat(e) : 0;
      let px = Math.round(sx(e.x)), py = Math.round(sy(e.y, e.state === 'sentado' && !e.chao ? 0.0 : 0)) + (e.state === 'sentado' && !e.chao ? 3 : 0);
      if (sp) {
        const a = this.CL.atlas[sp[0] + '_' + sp[1]]; if (!a) return this.figura(g, e, px, py, alpha);
        const dir = sp[1] === 'tq' ? (e.face || 'down') : (/left/.test(e.face) ? 'left' : /right/.test(e.face) ? 'right' : /up/.test(e.face) ? 'up' : 'down');
        g.save(); g.globalAlpha = alpha; if (sp[2]) { g.translate(px, py); g.scale(sp[2], sp[2]); this.CL.draw(g, { who: sp[0], persp: sp[1], x: 0, y: 0, anim: e.anim || 'idle', dir, t: this.t + e.x }); } else this.CL.draw(g, { who: sp[0], persp: sp[1], x: px, y: py, anim: e.anim || 'idle', dir, t: this.t + e.x });
        g.restore();
      } else this.figura(g, e, px, py, alpha);
    }
    keySeat(e) { if (e.chao) return e.y + 0.25; const o = this.sim.OB[this.D.SEATS[e.seat][2]]; return o.y + o.d + 0.01; }
    frame(dt, zoomW) {
      this.t += dt; const g = this.ctx, sim = this.sim, L = sim.lia, D = this.D;
      this.cam = Math.max(0, Math.min(W - 480, Math.round(sx(L.x) - 240)));
      g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = '#120d10'; g.fillRect(0, 0, 480, 270); g.save(); g.translate(-this.cam, 0); g.drawImage(this.sim.normal ? this.estN : this.est, 0, 0);
      const lista = [];
      for (const o of Object.values(sim.OB)) { if (/^F0[1-4]$/.test(o.id)) continue; lista.push([o.y + o.d, 0, o]); }
      for (const s of sim.IT) { if (s.id === 'E01') continue; if (sim.normal && (/^E/.test(s.id) || /^(F08|F09|F12|M01|M27)$/.test(s.sup))) continue; if (['E03', 'E04', 'E05', 'E06', 'E07', 'E08', 'E09', 'E02', 'E10', 'E11'].includes(s.id) && !sim.toalha) continue; if (s.id === 'M27') continue; if (s.sup === 'M27' && sim.fasen !== 'C' && sim.fasen !== 'D') continue; const so = sim.OB[s.sup]; lista.push([so ? so.y + so.d + 0.002 + s.y * 1e-4 : s.y + s.d + 0.002, 1, s]); }
      if (sim.toalha) this.toalha(g);
      for (const id in sim.npcs) { const n = sim.npcs[id]; if (n.vis) lista.push([n.state === 'sentado' ? this.keySeat(n) : n.y, 2, n]); }
      lista.push([L.state === 'sentada' ? this.keySeat({ seat: L.seat }) : L.y, 2, L]);
      lista.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
      const heads = []; this.perto = null; { let bd = 1.6; for (const id in sim.npcs) { const n = sim.npcs[id]; if (!n.vis) continue; const d = Math.hypot(n.x - L.x, n.y - L.y); if (d < bd) { bd = d; this.perto = n; } } }
      for (const [, k, o] of lista) {
        if (k === 0) { if (o.id === 'M27' && sim.fasen !== 'C' && sim.fasen !== 'D') continue; this.obj(g, o); }
        else if (k === 1) this.item(g, o);
        else { const al = o.alpha != null ? o.alpha : 1; if (o.id === 'lia') this.ent(g, { id: 'lia', x: o.x, y: o.y, face: o.face, anim: o.anim, state: o.state === 'sentada' ? 'sentado' : 'livre', seat: o.seat, chao: false, t: o.t }, 1); else this.ent(g, o, al);
          const h = this.D.CH[o.id][1] * 24 * (o.state === 'sentado' ? .72 : 1); heads.push([sx(o.x), sy(o.y, 0) - h]); }
      }
      // vapor do panelão e cheiro de dendê (partículas leves)
      for (let i = 0; i < 4; i++) { const ph = (this.t * .5 + i * .25) % 1, x = sx(3.75) + Math.sin(this.t * 2 + i * 2) * 3, y = sy(1.2, 0.95) - ph * 22; g.fillStyle = 'rgba(245,245,240,' + (0.35 * (1 - ph)).toFixed(2) + ')'; g.fillRect(x | 0, y | 0, 3, 2); }
      // copa: translúcida (recorte) só onde cobre cabeças
      const c = this.copaTmp || (this.copaTmp = document.createElement('canvas')); c.width = W; c.height = H; const cg = c.getContext('2d'); cg.drawImage(this.copa, 0, 0); cg.globalCompositeOperation = 'destination-out';
      for (const [hx, hy] of heads) if (hx > 490 && hx < 642 && hy < 118) { const gr = cg.createRadialGradient(hx, hy + 8, 6, hx, hy + 8, 22); gr.addColorStop(0, 'rgba(0,0,0,1)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); cg.fillStyle = gr; cg.fillRect(hx - 24, hy - 14, 48, 44); }
      g.drawImage(c, 0, 0); g.restore();
    }
    toalha(g) {
      if (this.spr(g, 'E01')) return;
      const T = this.D.TOALHA, a = this.P(T.x0, T.y0, 0), b = this.P(T.x1, T.y1, 0); g.fillStyle = 'rgba(60,35,20,.18)'; g.fillRect(a[0] + 1, b[1], b[0] - a[0], 2);
      g.fillStyle = RD[3]; g.fillRect(a[0], a[1], b[0] - a[0], b[1] - a[1]);
      for (let i = 0; i < 6; i++) for (let j = 0; j < 6; j++) if ((i + j) % 2) { g.fillStyle = 'rgba(242,241,238,.40)'; g.fillRect(a[0] + i * (b[0] - a[0]) / 6, a[1] + j * (b[1] - a[1]) / 6, (b[0] - a[0]) / 6, (b[1] - a[1]) / 6); }
      g.fillStyle = RD[1]; g.fillRect(a[0], a[1], b[0] - a[0], 1); g.fillRect(a[0], b[1] - 1, b[0] - a[0], 1); g.fillRect(a[0], a[1], 1, b[1] - a[1]); g.fillRect(b[0] - 1, a[1], 1, b[1] - a[1]);
    }
    nome(g, e, h) { const t = this.D.CH[e.id][0].replace(/ \(.*/, ''), x = Math.round(sx(e.x)), y = Math.round(sy(e.y, 0) - h) - 4; g.font = '7px sans-serif'; const w = g.measureText(t).width; g.fillStyle = 'rgba(20,12,16,.7)'; g.fillRect(x - w / 2 - 2, y - 7, w + 4, 9); g.fillStyle = '#f4e6cf'; g.fillText(t, x - w / 2, y); }
  }
  Q.Render = Render;
})(typeof window !== 'undefined' ? window.Quintal : null);
