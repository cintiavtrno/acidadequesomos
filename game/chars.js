// ===== chars.js — sistema de personagens reutilizável (O balcão da vó · Etapa 2) =====
// Cada personagem × câmera tem uma folha (PNG) + atlas (JSON). Células 40×52, âncora = pés (20,46).
// Folhas: <quem>_side (rua, 4 direções) e <quem>_tq (interior 3/4, 8 direções). Nunca se misturam perspectivas.
const CharLib = {
  atlas: {}, img: {},
  init(atlases, images) { this.atlas = atlases; this.img = images; },
  key(who, persp) { return who + '_' + persp; },
  row(who, persp, anim, dir) {
    const a = this.atlas[this.key(who, persp)]; if (!a) return null;
    return a.rows[anim + '/' + dir] || a.rows[anim + '/down'] || null;
  },
  // direção de tela (8 dir.) a partir de um vetor de movimento; 'down' = de frente para a câmera
  dir8(dx, dy) {
    if (!dx && !dy) return null;
    const v = dy < 0 ? 'up' : dy > 0 ? 'down' : '', h = dx < 0 ? 'left' : dx > 0 ? 'right' : '';
    return v && h ? v + '_' + h : (v || h);
  },
  dir4(dx, dy) { if (dx) return dx < 0 ? 'left' : 'right'; if (dy) return dy < 0 ? 'up' : 'down'; return null; },
  speedPx(who) { return this.atlas[this.key(who, 'tq')].speed_mps * 24; },     // px/s horizontal; 1 m = 24 px
  frameOf(info, t) { const k = Math.floor(t * info.fps); return info.loop ? k % info.n : Math.min(info.n - 1, k); },
  duration(who, persp, anim, dir) { const i = this.row(who, persp, anim, dir); return i ? i.n / i.fps : 0; },
  // c = { who, persp, x, y, anim, dir, t }  (x,y = ponto entre os pés, em coordenadas de tela já deslocadas)
  draw(ctx, c, opt) {
    opt = opt || {};
    const a = this.atlas[this.key(c.who, c.persp)], img = this.img[this.key(c.who, c.persp)]; if (!a || !img) return;
    const info = this.row(c.who, c.persp, c.anim, c.dir) || this.row(c.who, c.persp, 'idle', 'down'); if (!info) return;
    const k = this.frameOf(info, c.t), P = a.pad, [W, H] = a.cell, px = Math.round(c.x), py = Math.round(c.y);
    if (opt.shadow !== false) {
      ctx.fillStyle = 'rgba(18,10,28,0.34)';
      const w = c.who === 'lia' ? 4 : 5;
      ctx.fillRect(px - w, py - 1, w * 2, 1); ctx.fillRect(px - w - 1, py, w * 2 + 2, 1); ctx.fillRect(px - w + 1, py + 1, w * 2 - 2, 1);
    }
    ctx.save();
    if (opt.alpha != null) ctx.globalAlpha = opt.alpha;
    if (opt.clipBelowY != null) { ctx.beginPath(); ctx.rect(0, 0, 4096, opt.clipBelowY); ctx.clip(); }
    ctx.drawImage(img, P + k * (W + P), P + info.row * (H + P), W, H, px - a.anchor[0], py - a.anchor[1], W, H);
    ctx.restore();
  }
};
