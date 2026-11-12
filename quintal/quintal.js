// ===== quintal.js — Etapa 8.6: o quintal do caruru (1994) jogável =====
// Parte DOM-free (Quintal.Sim): mundo em METROS (X 0–28, Y 0–8 de profundidade, Z altura), colisão por grade de 0,1 m, A* com custo de conforto,
// Lia + 16 NPCs + 6 meninos, fases A/B/C1/C/D, assentos, interação. Parte de tela (Quintal.Render): projeção 3/4 do jogo (sx=24+24X, sy=124+16Y−24Z).
// Os dados vêm de qdata.json (gerado do projeto espacial aprovado: quintal_data.py + quintal_pos.py). Nada é redesenhado aqui.
(function (root) {
  'use strict';
  const Q = {}, PX = 24, PY = 16, OX = 24, OY = 124, R = 0.1;
  const sx = X => OX + PX * X, sy = (Y, Z) => OY + PY * Y - PX * (Z || 0);
  Q.sx = sx; Q.sy = sy;
  const dist = (a, b, c, d) => Math.hypot(a - c, b - d);

  // ---------------------------------------------------------------- Sim
  class Sim {
    constructor(D, o) {
      o = o || {}; this.D = D; this.t = 0; this.clock = { min: o.start != null ? o.start : 420, rate: o.rate || 0.25, hh: 0, mm: 0, isOpen: () => true };
      this.NX = Math.round(D.W / R); this.NY = Math.round(D.D / R);
      this.OB = {}; for (const a of D.OBJ) this.OB[a[0]] = { id: a[0], nome: a[1], cat: a[2], x: a[3], y: a[4], w: a[5], d: a[6], h: a[7], col: a[8], int: a[9] };
      this.IT = D.ITENS.map(a => ({ id: a[0], nome: a[1], zona: a[2], sup: a[3], x: a[4], y: a[5], w: a[6], d: a[7], h: a[8], z: a[9], uso: a[15], estado: a[14] }));
      this.base = this.grid(false); this.c1 = this.grid(true);
      this.toalha = false; this.fasen = null; this.ocup = {};
      this.lia = { id: 'lia', x: 4.5, y: 7.5, face: 'up', anim: 'idle', state: 'livre', path: [], seat: null, t: 0, vis: true, v: [0, 0] };
      this.npcs = {}; for (const id in D.CH) if (id !== 'lia') this.npcs[id] = { id, x: 0, y: 0, face: 'down', anim: 'idle', state: 'fora', path: [], seat: null, t: 0, vis: false, goal: null, via: null, alvo: null, r: D.CH[id][2] };
      this.log = []; this.liaPresente = !(typeof window !== 'undefined' && window.MUNDO_ATIVO); this.forcada = false; this.fase(this.faseDoRelogio(), true);
    }
    // grade de distância (m) ao obstáculo mais próximo; bordas do piso bloqueiam, exceto soleira e portão
    grid(c1) {
      const { NX, NY } = this, D = this.D, B = new Uint8Array(NX * NY), W = D.W, DD = D.D;
      const blk = (x0, y0, x1, y1) => { for (let j = Math.max(0, Math.floor(y0 / R)); j < Math.min(NY, Math.ceil(y1 / R)); j++) for (let i = Math.max(0, Math.floor(x0 / R)); i < Math.min(NX, Math.ceil(x1 / R)); i++) B[j * NX + i] = 1; };
      for (const o of Object.values(this.OB)) if (o.col && !/^F0[1-4]$/.test(o.id)) blk(o.x, o.y, o.x + o.w, o.y + o.d);
      const T = D.TOALHA, b = T.buffer; if (c1) blk(T.x0 - b, T.y0 - b, T.x1 + b, T.y1 + b);
      const K = 12, dist = new Float32Array(NX * NY).fill(K * R), idx = [];
      for (let j = 0; j < NY; j++) for (let i = 0; i < NX; i++) if (B[j * NX + i]) idx.push([i, j]);
      const sol = D.OPEN.soleira, por = D.OPEN.portao;
      const wallDist = (x, y) => Math.min(x, y, (y >= por.y0 && y <= por.y1) ? 9 : W - x, (x >= sol.x0 && x <= sol.x1) ? 9 : DD - y);
      for (let j = 0; j < NY; j++) for (let i = 0; i < NX; i++) {
        const x = (i + .5) * R, y = (j + .5) * R; let m = wallDist(x, y);
        if (m > K * R) m = K * R;
        for (let jj = Math.max(0, j - K); jj <= Math.min(NY - 1, j + K); jj++) for (let ii = Math.max(0, i - K); ii <= Math.min(NX - 1, i + K); ii++) if (B[jj * NX + ii]) { const d = Math.hypot(ii - i, jj - j) * R; if (d < m) m = d; }
        dist[j * NX + i] = B[j * NX + i] ? 0 : m;
      }
      return dist;
    }
    cell(x, y) { return [Math.min(this.NX - 1, Math.max(0, Math.floor(x / R))), Math.min(this.NY - 1, Math.max(0, Math.floor(y / R)))]; }
    gridDo(e) { return (this.toalha && e.id !== 'zefa' && !this.livre(e)) ? this.c1 : this.base; }
    livre(e) { return false; }
    inRest(x, y) { const r = this.D.RESTRITA; return x >= r.x0 && x <= r.x1 && y >= r.y0 && y <= r.y1; }
    walk(g, x, y, r, lia) { if (x < 0.02 || y < 0.02 || x > this.D.W + 0.3 || y > this.D.D + 0.3) return false; const [i, j] = this.cell(x, y); if (g[j * this.NX + i] <= r) return false; if (lia && this.inRest(x, y)) return false; return true; }
    los(g, a, b, r, lia) { const n = Math.ceil(dist(a[0], a[1], b[0], b[1]) / 0.05); for (let k = 0; k <= n; k++) { const t = k / n; if (!this.walk(g, a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, r - 0.03, lia)) return false; } return true; }
    // A* (8 vizinhos, custo de conforto) + suavização por linha de visada; retorna lista de [x,y] em metros ou null
    achar(g, a, b, r, lia) {
      const NX = this.NX, NY = this.NY, s = this.cell(a[0], a[1]), t = this.cell(b[0], b[1]), key = (i, j) => j * NX + i;
      const ok = (i, j) => i >= 0 && j >= 0 && i < NX && j < NY && g[key(i, j)] > r && !(lia && this.inRest((i + .5) * R, (j + .5) * R));
      if (!ok(t[0], t[1])) return null;
      if (!ok(s[0], s[1])) { /* sai de um ponto apertado: procura o vizinho livre mais próximo */ let best = null; for (let d = 1; d < 8 && !best; d++) for (let dj = -d; dj <= d; dj++) for (let di = -d; di <= d; di++) if (ok(s[0] + di, s[1] + dj) && (!best || Math.hypot(di, dj) < best[2])) best = [s[0] + di, s[1] + dj, Math.hypot(di, dj)]; if (!best) return null; s[0] = best[0]; s[1] = best[1]; }
      const cost = new Float64Array(NX * NY).fill(1e9), came = new Int32Array(NX * NY).fill(-1), open = [[0, key(s[0], s[1])]]; cost[key(s[0], s[1])] = 0;
      const push = it => { open.push(it); let i = open.length - 1; while (i > 0) { const p = (i - 1) >> 1; if (open[p][0] <= open[i][0]) break;[open[p], open[i]] = [open[i], open[p]]; i = p; } };
      const pop = () => { const top = open[0], last = open.pop(); if (open.length) { open[0] = last; let i = 0; for (; ;) { let l = 2 * i + 1, r2 = l + 1, m = i; if (l < open.length && open[l][0] < open[m][0]) m = l; if (r2 < open.length && open[r2][0] < open[m][0]) m = r2; if (m === i) break;[open[m], open[i]] = [open[i], open[m]]; i = m; } } return top; };
      const goal = key(t[0], t[1]);
      while (open.length) {
        const [, c] = pop(); if (c === goal) break; const ci = c % NX, cj = (c / NX) | 0;
        for (let dj = -1; dj <= 1; dj++) for (let di = -1; di <= 1; di++) {
          if (!di && !dj) continue; const ni = ci + di, nj = cj + dj; if (!ok(ni, nj)) continue; if (di && dj && !(ok(ci + di, cj) && ok(ci, cj + dj))) continue;
          const n = key(ni, nj), nc = cost[c] + (di && dj ? 1.414 : 1) * (1 + 1.2 * Math.max(0, 0.9 - g[n]) / 0.6);
          if (nc < cost[n]) { cost[n] = nc; came[n] = c; push([nc + Math.hypot(t[0] - ni, t[1] - nj), n]); }
        }
      }
      if (came[goal] < 0 && goal !== key(s[0], s[1])) return null;
      const pts = []; for (let c = goal; c >= 0; c = came[c]) pts.push([(c % NX + .5) * R, ((c / NX | 0) + .5) * R]); pts.reverse(); pts[pts.length - 1] = [b[0], b[1]];
      const out = [pts[0]]; let k = 0;
      while (k < pts.length - 1) { let m = pts.length - 1; while (m > k + 1 && !this.los(g, pts[k], pts[m], r, lia)) m--; out.push(pts[m]); k = m; }
      return out.slice(1);
    }
    // ---------------------------------------------------------------- Lia
    pos(e) { return [e.x, e.y]; }
    liaIr(x, y) { const L = this.lia; if (L.state === 'sentada') return; const p = this.achar(this.toalha ? this.c1 : this.base, [L.x, L.y], [x, y], 0.25, true); L.path = p || []; return !!p; }
    liaMover(vx, vy, dt) {
      const L = this.lia; if (L.state === 'sentada' || L.fala > 0) { L.v = [0, 0]; return; }
      L.v = [vx, vy]; if (!vx && !vy) return; L.path = []; const n = Math.hypot(vx, vy), sp = 1.27 * (this.corre ? 1.5 : 1), g = this.toalha ? this.c1 : this.base;
      const dx = vx / n * sp * dt, dy = vy / n * sp * dt;
      if (this.walk(g, L.x + dx, L.y + dy, 0.25, true)) { L.x += dx; L.y += dy; } else if (this.walk(g, L.x + dx, L.y, 0.25, true)) L.x += dx; else if (this.walk(g, L.x, L.y + dy, 0.25, true)) L.y += dy;
      L.face = dir8(dx, dy) || L.face; L.moved = true;
    }
    // ---------------------------------------------------------------- NPCs e fases
    seatDir(id) {
      if (/^mesa_f/.test(id) || /^dom_N/.test(id) || /^conv|^fio|^espera|^coz|^rita/.test(id)) return 'down';
      if (/^banco_|^dom_S/.test(id)) return 'up'; if (id === 'mesa_cab_O' || id === 'dom_O') return 'right'; if (id === 'mesa_cab_L' || id === 'dom_L') return 'left';
      if (/^cri_[12]/.test(id)) return 'right'; if (/^cri_[34]/.test(id)) return 'left'; return 'down';
    }
    destino(ph, k) { const v = this.D.FASE[ph][k]; if (!v) return null; if (v.length === 1) { const s = this.D.SEATS[v[0]]; return { tipo: 'sentar', seat: v[0], x: s[0], y: s[1], ap: s[3] }; }
      if (v[2] === 'chao') { const c = this.D.TOALHA; return { tipo: 'chao', x: v[0], y: v[1], dir: dir8(c.cx - v[0], c.cy - v[1]) }; } return { tipo: 'pe', x: v[0], y: v[1] }; }
    // o caruru só acontece no intervalo D.EVENTO do relógio; antes e depois o quintal é comum e vazio ('N')
    faseDoRelogio() { if (typeof window !== 'undefined' && window.MUNDO_ATIVO && window.MUNDO_ANO !== 1994) return 'N'; const m = this.clock.min % 1440; let f = 'N'; for (const [t0, ph] of this.D.EVENTO) if (m >= t0) f = ph; return f; }
    fase(nome, instante) {
      const D = this.D; this.fasen = nome; this.toalha = nome === 'C1'; this.normal = nome === 'N'; this.ocup = {}; this.log.push(['fase', nome]);
      if (this.toalha && this.lia.state === 'livre') { const T = D.TOALHA, b = T.buffer + 0.1, L0 = this.lia; if (L0.x > T.x0 - b && L0.x < T.x1 + b && L0.y > T.y0 - b && L0.y < T.y1 + b) { L0.y = T.y1 + b + 0.1; L0.path = []; } }
      const L = this.lia; if (instante) { const f = D.FASE[nome].lia; if (f && f.length === 3) { L.x = f[0]; L.y = f[1]; L.face = 'up'; } }
      for (const id in this.npcs) {
        const n = this.npcs[id], d = this.destino(nome, id); n.seat = null; n.path = []; n.via = null; n.anim = 'idle';
        if (!d) { if (n.vis && n.state !== 'saindo') { n.state = 'saindo'; n.alvo = null; n.path = this.rota(n, id === 'rita' ? D.ENTRADAS.portao : D.ENTRADAS.soleira) || []; if (instante) { n.vis = false; n.state = 'fora'; } } continue; }
        n.alvo = d;
        if (instante || !n.vis) { // nasce direto no lugar (instante) ou na entrada (fase em andamento)
          if (instante) { this.colocar(n, d); } else { const e = id === 'rita' ? D.ENTRADAS.portao : D.ENTRADAS.soleira; n.x = e[0]; n.y = e[1] - 0.2; n.vis = true; this.seguir(n, d); }
        } else this.seguir(n, d);
      }
    }
    colocar(n, d) {
      n.vis = true; n.state = 'parado'; n.path = [];
      if (d.tipo === 'sentar') { n.x = d.x; n.y = d.y; n.seat = d.seat; n.state = 'sentado'; n.anim = 'sit'; n.face = this.seatDir(d.seat); this.ocup[d.seat] = n.id; }
      else if (d.tipo === 'chao') { n.x = d.x; n.y = d.y; n.state = 'sentado'; n.anim = 'sit'; n.face = d.dir; n.chao = true; }
      else { n.x = d.x; n.y = d.y; n.face = 'down'; n.chao = false; }
    }
    rota(n, p) { return this.achar(n.id === 'zefa' ? this.base : this.gridDo(n), [n.x, n.y], p, n.r + 0.03, false); }
    seguir(n, d) {
      n.state = 'andando'; n.chao = false;
      const ap = d.tipo === 'sentar' ? d.ap : d.tipo === 'chao' ? [this.D.TOALHA.cx, this.D.TOALHA.y1 + 0.45] : [d.x, d.y];            // meninos entram pelo vão da frente da toalha
      n.path = this.rota(n, ap) || []; n.final = d; if (d.tipo === 'chao') n.path.push([d.x, d.y]);
      if (!n.path.length && dist(n.x, n.y, ap[0], ap[1]) > 0.3) n.state = 'preso';
    }
    npcPasso(n, dt) {
      if (!n.vis || n.state === 'sentado' || n.state === 'parado' || n.state === 'fora') { if (n.state === 'parado') n.anim = 'idle'; return; }
      if (!n.path.length) { // chegou
        if (n.state === 'saindo') { n.vis = false; n.state = 'fora'; return; }
        if (n.final) { const f = n.final; n.final = null; if (f.tipo === 'sentar') { if (this.ocup[f.seat] && this.ocup[f.seat] !== n.id) { n.state = 'parado'; return; } this.colocar(n, f); } else this.colocar(n, f); }
        else n.state = 'parado'; return;
      }
      const p = n.path[0], d = dist(n.x, n.y, p[0], p[1]), sp = (this.D.SPEED[n.id] || 1.1) * dt;
      n.face = dir8(p[0] - n.x, p[1] - n.y) || n.face; n.anim = 'walk';
      if (d <= sp) { n.x = p[0]; n.y = p[1]; n.path.shift(); } else { n.x += (p[0] - n.x) / d * sp; n.y += (p[1] - n.y) / d * sp; }
    }
    // ---------------------------------------------------------------- interação
    textos() { return TXT; }
    candidatos() {
      const L = this.lia, D = this.D, out = [];
      if (L.state === 'sentada') return [{ k: 'levantar', d: 0, label: 'Levantar', run: () => this.levantar() }];
      for (const k in D.STAND) { if (k === 'portao' || k === 'toalha_zefa' || k === 'banner' || !TXT[k]) continue; if (this.normal && /^(M27|F12[ab])$/.test(k)) continue; const s = D.STAND[k], d = dist(L.x, L.y, s[0], s[1]); if (d < 0.9) out.push({ k: 'obj', id: k, d, label: TXT[k][0], run: () => this.examinar(k) }); }
      if (!this.normal) { const v = D.BANNER_VIEW; if (L.x >= v[0] && L.x <= v[2] && L.y >= v[1] && L.y <= v[3] + 0.3) out.push({ k: 'obj', id: 'banner', d: 0.2, label: TXT.banner[0], run: () => this.examinar('banner') }); }
      for (const sid in D.SEATS) { if (this.ocup[sid]) continue; const ap = D.SEATS[sid][3], d = dist(L.x, L.y, ap[0], ap[1]); if (d < 0.7) out.push({ k: 'seat', id: sid, d: d + 0.3, label: 'Sentar', run: () => this.sentar(sid) }); }
      for (const id in this.npcs) { const n = this.npcs[id]; if (!n.vis) continue; const d = dist(L.x, L.y, n.x, n.y); if (d < 1.4) out.push({ k: 'npc', id, d: d - 0.4, label: 'Falar com ' + D.CH[id][0].replace(/ \(.*/, ''), run: () => this.falar(id) }); }
      const s = D.STAND.portao, p = D.OPEN.servico; if (dist(L.x, L.y, s[0], s[1]) < 1.2) out.push({ k: 'obj', id: 'portao', d: 1, label: TXT.portao[0], run: () => this.examinar('portao') });
      if (L.y < 1.3 && L.x > p.x0 - 0.4 && L.x < p.x1 + 0.4) out.push({ k: 'obj', id: 'servico', d: 0.8, label: TXT.servico[0], run: () => this.examinar('servico') });
      return out.sort((a, b) => a.d - b.d);
    }
    acao() { const c = this.candidatos(); if (c.length) { c[0].run(); return c[0]; } return null; }
    examinar(k) { const L = this.lia, s = this.D.STAND[k]; if (s && k !== 'banner') L.face = s[2] === 'up' ? 'up' : s[2] === 'down' ? 'down' : s[2] === 'left' ? 'left' : 'right'; if (k === 'banner') L.face = 'up'; L.anim = 'interact'; L.fala = 1.1; this.msg = { txt: (this.normal && TXTN[k]) || TXT[k][1], t: 6 }; this.log.push(['examinar', k]); this.viu = this.viu || {}; this.viu[k] = 1; }
    falar(id) { const n = this.npcs[id], L = this.lia; L.face = dir8(n.x - L.x, n.y - L.y); L.anim = 'talk'; L.fala = 1.2; this.msg = { txt: (this.D.CH[id][0].replace(/ \(.*/, '')) + ': ' + falaDe(id, this.fasen), t: 6 }; this.log.push(['falar', id]); }
    sentar(sid) { const s = this.D.SEATS[sid], L = this.lia; L.x = s[0]; L.y = s[1]; L.state = 'sentada'; L.seat = sid; L.anim = 'sit'; L.face = this.seatDir(sid); L.path = []; this.ocup[sid] = 'lia'; this.log.push(['sentar', sid]); }
    levantar() { const L = this.lia, sid = L.seat, ap = this.D.SEATS[sid][3]; L.x = ap[0]; L.y = ap[1]; L.state = 'livre'; L.anim = 'idle'; delete this.ocup[sid]; L.seat = null; }
    saindo() { const L = this.lia, s = this.D.OPEN.soleira; return L.y > this.D.D - 0.25 && L.x >= s.x0 && L.x <= s.x1; }
    chegar(p) { const L = this.lia, s = this.D.OPEN.soleira; L.x = (s.x0 + s.x1) / 2; L.y = 7.5; L.face = 'up'; L.state = 'livre'; L.path = []; L.anim = 'idle'; }
    update(dt) {
      this.t += dt; if (!this.clock.paused) this.clock.min += dt * this.clock.rate; this.clock.hh = Math.floor(this.clock.min / 60) % 24; this.clock.mm = Math.floor(this.clock.min % 60);
      if (!this.forcada) { const ph = this.faseDoRelogio(); if (ph !== this.fasen) this.fase(ph, !this.liaPresente); }
      const L = this.lia; L.t += dt; if (L.fala > 0) { L.fala -= dt; if (L.fala <= 0) { L.fala = 0; if (L.state !== 'sentada') L.anim = 'idle'; } }
      if (this.msg) { this.msg.t -= dt; if (this.msg.t <= 0) this.msg = null; }
      if (L.state === 'livre' && L.path.length && !L.fala) { const p = L.path[0], d = dist(L.x, L.y, p[0], p[1]), sp = 1.27 * dt; L.face = dir8(p[0] - L.x, p[1] - L.y) || L.face; L.anim = 'walk'; if (d <= sp) { L.x = p[0]; L.y = p[1]; L.path.shift(); } else { L.x += (p[0] - L.x) / d * sp; L.y += (p[1] - L.y) / d * sp; } }
      else if (L.state === 'livre' && !L.fala) L.anim = (L.v[0] || L.v[1]) ? 'walk' : 'idle';
      for (const id in this.npcs) { const n = this.npcs[id]; n.t += dt; this.npcPasso(n, dt); }
    }
  }
  function dir8(dx, dy) { if (Math.abs(dx) < 1e-6 && Math.abs(dy) < 1e-6) return null; const v = dy < -1e-6 ? 'up' : dy > 1e-6 ? 'down' : '', h = dx < -1e-6 ? 'left' : dx > 1e-6 ? 'right' : ''; if (v && h && Math.abs(dy) > 2.2 * Math.abs(dx)) return v; if (v && h && Math.abs(dx) > 2.2 * Math.abs(dy)) return h; return v && h ? v + '_' + h : (v || h); }
  const TXTN = { M01: 'Uma mesa comprida de madeira, sem toalha. O quintal está sossegado hoje.', F08: 'O fogão a gás está apagado, com a chaleira em cima.', F09: 'A bancada de preparo está limpa, só com a tábua e a faca guardadas.' };   // PROPOSTA de textos do quintal comum
  const TXT = {
    F07: ['Examinar o panelão de caruru', 'O panelão de caruru ferve em fogo de lenha. O quiabo já soltou o ponto, e o cheiro de dendê e camarão seco toma o quintal.'],
    F08: ['Examinar o fogão', 'No fogão a gás, o vatapá e a caçarola de camarão com dendê estão no fogo baixo, tampados.'],
    F09: ['Examinar a bancada de preparo', 'Quiabo cortado, camarão seco, cebola picada e um cesto de temperos. A tábua ainda está úmida da faca.'],
    F10: ['Examinar o tanque', 'O tanque tem uma torneira que pinga. Um balde de água espera na borda.'],
    F11: ['Examinar a talha de barro', 'A talha mantém a água fria. A caneca fica pendurada ao lado.'],
    F12a: ['Examinar o aparador de serviço', 'O aparador de serviço: pilha de pratos, cuia de talheres, bandeja de copos e as travessas esperando a hora de servir.'],
    F12b: ['Examinar as travessas', 'Travessas de caruru, vatapá, arroz e farofa. Ainda não é hora de servir os adultos.'],
    F13: ['Observar a mesa da oferenda', 'A mesa baixa da oferenda. Ninguém além de Dona Zefa e Dona Nena chega perto, e a Lia entende que é para só olhar.'],
    banner: ['Examinar a bandeira dos santos', 'A bandeira de Cosme e Damião, pendurada na parede da casa. Embaixo, no aparador, um prato servido, uma vela e flores brancas: a primeira porção é dos santos.'],
    M01: ['Examinar a mesa longa', 'A mesa longa está posta, com toalha e dez lugares. Pela tradição, os adultos só comem depois das crianças.'],
    M09: ['Examinar a mesinha das crianças', 'A mesinha das crianças, baixa, com um prato de cocada que Tonho trouxe de presente.'],
    M14: ['Observar o dominó', 'A mesa de dominó, com as peças espalhadas. Seu Zé já escolheu o lado.'],
    F14: ['Examinar a mangueira', 'A mangueira é bem mais velha que o quintal. A sombra dela cobre o fundo, perto do muro de Rita.'],
    M22: ['Lavar as mãos', 'A Lia lava as mãos no lavatório antes de ir para perto da comida.'],
    M25: ['Examinar o pilão', 'O pilão guarda o cheiro do tempero que acabou de ser pilado.'],
    M27: ['Observar o tabuleiro', 'O tabuleiro de Dona Nena, com o tacho e a bacia coberta com pano. Acarajé é de tarde.'],
    portao: ['Olhar o portão de Rita', 'O portão dá para a casa de Dona Rita. Daqui se vê o telhado dela, com a lona e o balde no canto.'],
    servico: ['Tentar a porta de serviço', 'Ainda não. A porta de serviço dá para dentro da casa de Dona Zefa, e hoje é dia de quintal.'],
  };
  // Fala por fase: A preparo (12h) · B chegada (13h) · C1 crianças na toalha (14h) · C mesa dos grandes (15h) · D depois da mesa (16h30). Sem a fase, vale N e depois a fala única.
  const POR_FASE = {
    aurea: {
      B: 'Trouxe o cesto de pães. Deixei o balcão sem ninguém pra vir, então hoje quem passa lá espera até amanhã. Hoje o dia é da Zefa.',
      C1: 'Primeiro as crianças, na toalha. Sete pratos pra conferir, Lia. Vai com a Zefa, que eu cuido do pão.',
      C: 'Come primeiro, menina. Depois eu te peço uma coisa, baixinho.',
      D: 'A mesa já foi e agora a conversa vai para o Programa. Eu escuto mais do que falo. Se quiser saber, chegue perto da Dandara e da Zefa e fique quieta.',
      N: 'Esta é a casa da Zefa. Hoje o dia é dela.',
    },
    zefa: {
      A: 'Tem muito caruru pra fazer e pouca gente ainda. Pega uma tarefa comigo, Lia.',
      B: 'Pode entrar. Hoje a casa é de quem chegar.',
      C1: 'Primeiro as crianças, na toalha. Depois os grandes.',
      C: 'A mesa está posta. Come, que a conversa vem depois.',
      D: 'O prato foi, a conversa ficou. Senta onde quiser.',
      N: 'Hoje o quintal está quieto.',
    },
  };
  const falaDe = (id, fase) => { const p = POR_FASE[id]; return (p && (p[fase] || p.N)) || FALA[id] || '…'; };
  const FALA = { zefa: 'Hoje a casa é de quem chegar. Primeiro as crianças, depois os grandes.', aurea: 'Hoje o dia é da Zefa.', raimundo: 'Caruru bom é o que junta gente.', dandara: 'Depois a gente conversa sobre o bairro, com calma.',
    ze: 'Vem, Lia, aprender a contar até seis.', nonato: 'Carreguei a mesa sozinho. Depois do prato, é dominó.', bela: 'Eu fico vendo a porta e o quintal.', cicera: 'Cadê o Júnior? Esse menino some.', junior: 'Eu sei um segredo do quintal!',
    tonho: 'Trouxe cocada. Onde eu ponho?', nena: 'Acarajé é de tarde, minha filha.', davi: 'Se me chamarem, eu toco baixinho.', lucia: 'Vim só acompanhar. Já já eu vou.', rita: 'Meu telhado precisa mesmo de conserto, viu?',
    caio: 'Eu e Bia ajudamos na padaria. Sobra sempre um pão pra mim.', bia: 'Dona Áurea me ensinou a sovar.' };
  for (let i = 1; i <= 6; i++) FALA['m' + i] = ['Posso comer já?', 'Hmm, que cheiro!', 'Cadê meu prato?', 'Eu quero banana!', 'Tá quente?', 'Eu já lavei a mão.'][i - 1];
  Q.Sim = Sim; Q.TXT = TXT; Q.dir8 = dir8;
  if (typeof module !== 'undefined' && module.exports) { module.exports = Q; require('./dialogo.js'); } else root.Quintal = Q;
})(typeof window !== 'undefined' ? window : globalThis);
