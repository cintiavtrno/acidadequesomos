// ===== s2_nav.js — navegação (grade + A*), independente do desenho =====
// Nav.init({ blocked(x,y), X0,X1,YB,YF }) — o jogo fornece a colisão (ObjectSys.solids + paredes).
Sim.Nav = {
  G: 4,
  init(o) { Object.assign(this, o); },
  free(x, y) { return !this.blocked(x, y) && !this.blocked(x - 2, y) && !this.blocked(x + 2, y); },
  nearestFree(x, y) { if (this.free(x, y)) return [x, y]; for (let r = 2; r < 60; r += 2) for (let a = 0; a < 16; a++) { const px = x + Math.cos(a * Math.PI / 8) * r, py = y + Math.sin(a * Math.PI / 8) * r; if (this.free(px, py)) return [Math.round(px), Math.round(py)]; } return [x, y]; },
  los(a, b) { const n = Math.ceil(Math.hypot(b[0] - a[0], b[1] - a[1]) / 2); for (let t = 1; t < n; t++) { const x = a[0] + (b[0] - a[0]) * t / n, y = a[1] + (b[1] - a[1]) * t / n; if (!this.free(x, y)) return false; } return true; },
  path(x0, y0, x1, y1) {
    const G = this.G, ox = this.X0, oy = this.YB - 12, W = Math.ceil((this.X1 - this.X0) / G) + 1, H = Math.ceil((this.YF + 16 - oy) / G) + 1;
    const free = (i, j) => i >= 0 && j >= 0 && i < W && j < H && this.free(ox + i * G, oy + j * G);
    const cellOf = (x, y) => [Sim.clamp(Math.round((x - ox) / G), 0, W - 1), Sim.clamp(Math.round((y - oy) / G), 0, H - 1)];
    const near = c => { if (free(c[0], c[1])) return c; for (let r = 1; r < 14; r++) for (let dj = -r; dj <= r; dj++) for (let di = -r; di <= r; di++) if (Math.max(Math.abs(di), Math.abs(dj)) === r && free(c[0] + di, c[1] + dj)) return [c[0] + di, c[1] + dj]; return c; };
    const s = near(cellOf(x0, y0)), g = near(cellOf(x1, y1)), key = (i, j) => j * W + i;
    const gs = new Map([[key(...s), 0]]), from = new Map(), open = [[0, s[0], s[1]]], done = new Set(), hf = (i, j) => Math.hypot(i - g[0], j - g[1]);
    while (open.length) {
      let bi = 0; for (let q = 1; q < open.length; q++) if (open[q][0] < open[bi][0]) bi = q; const [, i, j] = open.splice(bi, 1)[0];
      const k = key(i, j); if (done.has(k)) continue; done.add(k); if (i === g[0] && j === g[1]) break;
      for (let di = -1; di <= 1; di++) for (let dj = -1; dj <= 1; dj++) {
        if (!di && !dj) continue; const ni = i + di, nj = j + dj; if (!free(ni, nj)) continue; if (di && dj && (!free(i + di, j) || !free(i, j + dj))) continue;
        const c = gs.get(k) + (di && dj ? 1.414 : 1), nk = key(ni, nj); if (!gs.has(nk) || c < gs.get(nk)) { gs.set(nk, c); from.set(nk, [i, j]); open.push([c + hf(ni, nj), ni, nj]); }
      }
    }
    if (!from.has(key(...g)) && (s[0] !== g[0] || s[1] !== g[1])) return null;       // sem caminho
    const pts = []; let cur = g; while (cur && !(cur[0] === s[0] && cur[1] === s[1])) { pts.unshift([ox + cur[0] * G, oy + cur[1] * G]); cur = from.get(key(...cur)); }
    pts.push([x1, y1]); const out = []; let f0 = [x0, y0], i = 0;
    while (i < pts.length) { let j = pts.length - 1; while (j > i && !this.los(f0, pts[j])) j--; out.push(pts[j]); f0 = pts[j]; i = j + 1; }
    return out;
  },
  // ponto de aproximação de um assento: ponto livre perto da cadeira, de onde o personagem desliza para sentar
  approach(seat) {
    const c = [[0, 10], [-13, 0], [13, 0], [0, -10], [-13, 8], [13, 8], [-13, -6], [13, -6], [0, 16]];
    for (const [dx, dy] of c) if (this.free(seat.x + dx, seat.y + dy) && this.path(this.EXIT_X, this.YF - 6, seat.x + dx, seat.y + dy)) return [seat.x + dx, seat.y + dy];
    return null;
  }
};
