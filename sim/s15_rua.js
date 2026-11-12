// ===== s15_rua.js — mundo da rua (Etapa 6): moradores com agenda, mesa de dominó viva, bichos, interações da Lia =====
// DOM-free. O jogo só desenha o que este mundo diz (posição, animação, direção, fala). A rua não está ligada à padaria nem à casa (Etapa 7).
(function () {
  const RD = Sim.Rua.D, yw = RD.yw, clamp = Sim.clamp;
  const dirDe = (dx, dy) => Math.abs(dx) >= Math.abs(dy) * 0.55 ? (dx < 0 ? 'left' : 'right') : (dy < 0 ? 'up' : 'down');

  class Walker {
    constructor(w, id) {
      this.w = w; this.id = id; this.def = RD.pessoas[id]; this.x = -50; this.y = 230; this.face = 'down'; this.anim = 'idle'; this.at = Math.random() * 3; this.state = 'Away';
      this.path = []; this.i = 0; this.tw = 0; this.say = null; this.seat = null; this.alpha = 1; this.sitT = 0; this.from = null; this.to = null; this.fadeT = 0;
      this.task = null; this.espera = 0; this.cool = 0; this.greetAt = -999; this.estado = {}; this.loc = 'rua';
      this.vel = RD.vel[id] || 20;
    }
    get sy() { return this.y - yw(this.x); }
    setAnim(a) { if (this.anim !== a) { this.anim = a; this.at = 0; } }
    falar(txt, ttl) { this.say = { text: txt, ttl: ttl || 3.2 }; this.w.bus.emit('fala', { id: this.id, texto: txt }); }
  }

  Sim.Rua.World = class {
    constructor(o) {
      o = o || {}; this.scene = o.scene; this.seed = o.seed || 1991; this.rng = Sim.RNG(this.seed); this.bus = new Sim.EventSystem();
      this.clock = new Sim.WorldClock({ start: o.start != null ? o.start : RD.dia.inicio, rate: o.rate || 0.25, openAt: RD.dia.inicio, closeAt: RD.dia.fim });
      this.integrado = !!o.integrado; this.lib = {}; this.liaFora = false; this.ag = this.integrado ? RD.agendaMundo() : JSON.parse(JSON.stringify(RD.agenda));
      this.W = RD.W; this.VH = RD.VH; this.persist = o.persist || {}; this.hooks = o.hooks || {};
      this.solids = (this.scene.solids || []).filter(s => !/^(cad_|banquinho_)/.test(s.id)).map(s => ({ id: s.id, x0: s.x0, x1: s.x1, sy0: s.sy0, sy1: s.sy1 }));
      this.trust = Object.assign({ raimundo: .34, dandara: .22, lucia: .06, ze: .2, nonato: .15, bela: .18, cicera: .2, junior: .3, tonho: .2 }, this.persist.trust || {});
      this.kp = Object.assign({}, this.persist.kp || {}); this.viv = Object.assign({}, this.persist.viv || {}); this.vivT = {}; this.feitos = Object.assign({}, this.persist.feitos || {}); this.lia = { x: 430, y: yw(430) + 12, face: 'right', seat: null, sentada: false };
      this.t = 0; this.ev = [];
      this.grade();
      this.initNav();
      this.npcs = {}; for (const id of Object.keys(RD.pessoas)) { this.npcs[id] = new Walker(this, id); this.npcs[id].idx = 0; }
      this.assentos = {}; for (const k in RD.assentos) this.assentos[k] = { def: RD.assentos[k], ocup: null, dominio: true };
      for (const k in RD.assentosRua) this.assentos[k] = { def: Object.assign({ id: k }, RD.assentosRua[k]), ocup: null };
      this.mesa = new MesaDomino(this);
      this.gato = { x: 186, y: yw(186) + 10, estado: 'dorme', at: 0, t: 0, alvo: null, vel: 0 };
      this.pombos = [0, 1, 2].map(i => ({ x: 450 + i * 24, y: yw(470) + 40 + (i % 2) * 4, f: 0, at: Math.random() * 2, estado: 'bicando', alvo: null, home: [450 + i * 24, 40 + (i % 2) * 4], t: 0 }));
      // posição inicial: quem não tem tarefa de 'sair' nasce Away
      this.liaTrust = {};
      this.social = new Sim.SocialMind(this, this.persist.soc);
    }
    // ---------------- navegação ----------------
    initNav() {
      const self = this;
      Sim.Nav.init({ X0: 0, X1: this.W, YB: 205, YF: 262, EXIT_X: 0, blocked: (x, y) => self.blocked(x, y) });
    }
    grade() {   // cache 1 px da colisão (A* chama blocked milhares de vezes)
      const W = this.W, H = this.VH + 1; this.G1 = new Uint8Array(W * H);
      for (let yy = 0; yy < H; yy++) for (let xx = 0; xx < W; xx++) this.G1[yy * W + xx] = this.blockedRaw(xx, yy) ? 1 : 0;
    }
    blocked(x, y) {
      x = Math.round(x); y = Math.round(y); if (x < 0 || x >= this.W || y < 0 || y > this.VH) return true; return this.G1[y * this.W + x] === 1;
    }
    blockedRaw(x, y, margem) {
      if (x < 6 || x > this.W - 6) return true;
      if (y < yw(x) + 8 || y > this.VH - 3) return true;
      const m = margem == null ? 0 : margem;
      for (const s of this.solids) { const a = yw((s.x0 + s.x1) / 2) + s.sy0, b = yw((s.x0 + s.x1) / 2) + s.sy1; if (x >= s.x0 - m && x <= s.x1 + m && y >= a - m && y <= b + m) return true; }
      return false;
    }
    spot(n) { const s = RD.spots[n]; if (!s) throw new Error('spot ?' + n); return { x: s.x, y: yw(s.x) + s.sy, face: s.face }; }
    // ---------------- NPC ----------------
    update(dt) {
      this.t += dt; const d = this.clock.tick(dt); this.dmin = d;
      for (const id in this.npcs) this.updateNpc(this.npcs[id], dt);
      this.mesa.update(dt);
      this.social.update(dt); this.updateViv(dt);
      this.updateBichos(dt); this.updateGreetings(dt);
      if (this.clock.min >= RD.dia.fim && !this.clock.ended) { this.clock.ended = true; this.bus.emit('dia_fim', { resumo: this.resumo() }); }
    }
    lugar(n, sp) { n.x = sp.x; n.y = sp.y; if (sp.face) n.face = sp.face; }
    proximaTarefa(n) {
      const ag = this.ag[n.id] || []; if (n.idx >= ag.length) { n.task = null; return; }
      const t = ag[n.idx]; if (this.clock.min < t.t) return;
      n.task = Object.assign({}, t, { ini: this.clock.min, fase: 0, tt: 0 }); n.idx++;
    }
    updateNpc(n, dt) {
      n.at += dt; if (n.say) { n.say.ttl -= dt; if (n.say.ttl <= 0) n.say = null; }
      if (!n.task) this.proximaTarefa(n);
      if (this.congelado === n.id && n.state === 'Walking') { n.setAnim('idle'); return; }   // fala com a Lia: espera
      const t = n.task;
      switch (n.state) {
        case 'Walking': this.passo(n, dt); break;
        case 'SitIn': case 'SitOut': this.deslizar(n, dt); break;
        case 'Entering': n.fadeT += dt; n.alpha = clamp(1 - n.fadeT / .5, 0, 1); if (n.fadeT >= .5) { n.state = 'Away'; n.alpha = 0; if (n.task && n.task.tipo === 'entrar') n.task = null; } break;
        case 'Exiting': n.fadeT += dt; n.alpha = clamp(n.fadeT / .5, 0, 1); if (n.fadeT >= .5) { n.alpha = 1; n.state = 'Idle'; n.setAnim('idle'); if (n.task && n.task.tipo === 'sair') n.task = null; } break;
        case 'Acting': n.tw -= dt; if (n.anim === 'interact' && n.at > 2.4) { n.at = 0; } if (n.tw <= 0) { n.state = 'Idle'; n.setAnim('idle'); if (n.task && ['esperar', 'olhar_mesa', 'conversar'].includes(n.task.tipo)) n.task = null; } break;
        case 'Sitting': this.sentadoTick(n, dt); break;
        case 'Idle': n.setAnim(n.anim === 'idle' || n.anim === 'walk' ? 'idle' : n.anim); break;
      }
      const t2 = n.task;
      if (t2 && t2.tipo === 'patrulha' && n.estado.papo && n.state === 'Idle') return;   // parado ouvindo alguém
      if (!t2 || t2 !== t && (n.state === 'Away') || n.state === 'Walking' || n.state === 'SitIn' || n.state === 'SitOut' || n.state === 'Entering' || n.state === 'Exiting') return;
      this.executar(n, t2, dt);
    }
    executar(n, t, dt) {
      switch (t.tipo) {
        case 'sair': {
          if (n.state !== 'Away') { n.task = null; break; }
          if (t.aguarda && !this.lib[n.id + ':' + t.aguarda]) break;               // dentro de outro ambiente: sai quando aquele mundo liberar
          if (t.aguarda) this.lib[n.id + ':' + t.aguarda] = false;
          const sp = this.spot(t.porta); this.lugar(n, sp);
          if (t.porta.startsWith('borda')) { n.state = 'Idle'; n.alpha = 1; n.face = t.porta === 'borda_E' ? 'right' : 'left'; n.task = null; this.bus.emit('entra_rua', { id: n.id }); }
          else { n.state = 'Exiting'; n.fadeT = 0; n.alpha = 0; n.face = 'down'; n.setAnim('idle'); this.bus.emit('porta', { id: n.id, porta: t.porta, saiu: true }); }
          break;
        }
        case 'ir': {
          if (n.state === 'Sitting') { this.levantarAgora(n); break; }
          const sp = this.spot(t.spot); if (!this.vaiPara(n, sp.x, sp.y, () => { n.face = sp.face || n.face; n.setAnim('idle'); n.task = null; })) n.task = null;
          break;
        }
        case 'entrar': {
          const sp = this.spot(t.porta); const perto = Math.hypot(n.x - sp.x, n.y - sp.y) < 4;
          if (!perto) { this.vaiPara(n, sp.x, sp.y, () => { }); break; }
          n.face = sp.face; if (t.porta.startsWith('borda')) { n.state = 'Away'; n.alpha = 0; n.task = null; }
          else { n.state = 'Entering'; n.fadeT = 0; this.bus.emit('porta', { id: n.id, porta: t.porta, saiu: false }); }
          break;
        }
        case 'sentar': this.sentar(n, t); break;
        case 'levantar': if (n.state === 'Sitting') this.levantarAgora(n); n.task = null; break;
        case 'esperar': {
          if (t.repouso && n.state === 'Sitting') { if (t.fimR == null) t.fimR = this.clock.min + t.dur; else if (this.clock.min >= t.fimR) n.task = null; break; }
          if (n.state !== 'Idle') break; n.state = 'Acting'; n.tw = t.dur / (this.clock.rate || 1); n.setAnim(t.anim || 'idle'); if (t.anim === 'hang' || t.anim === 'interact') n.face = t.anim === 'hang' ? 'up' : n.face;
          if (t.anim === 'interact' && this.near(n, 'fachada')) n.face = 'up'; break;
        }
        case 'olhar_mesa': { if (n.state !== 'Idle') break; n.face = n.x < RD.mesa.x ? 'right' : 'left'; n.state = 'Acting'; n.tw = t.dur / (this.clock.rate || 1); n.setAnim('idle'); n.estado.olhando = true; break; }
        case 'conversar': this.conversar(n, t); break;
        case 'patrulha': this.patrulha(n, t, dt); break;
        case 'visita': {   // compra rápida na padaria (abstrata: dentro, fora da rua, sem trocar de ambiente)
          if (n.state === 'Idle') { const sp = this.spot('porta_padaria'); n.face = 'up'; n.estado.volta = this.clock.min + t.dur; n.state = 'Entering'; n.fadeT = 0; }
          else if (n.state === 'Away' && this.clock.min >= (n.estado.volta || 0)) { const sp = this.spot('porta_padaria'); this.lugar(n, sp); n.state = 'Exiting'; n.fadeT = 0; n.alpha = 0; n.face = 'down'; n.task = null; this.social.encontroPadaria(n.id); this.bus.emit('compra', { id: n.id }); }
          break;
        }
      }
    }
    near(n, tag) { return true; }
    vaiPara(n, x, y, fim) {
      if (n.state === 'Away') return false;
      if (Math.hypot(n.x - x, n.y - y) < 2.5) { n.state = 'Idle'; fim && fim(); return true; }
      if (n.semCaminho && this.t < n.semCaminho) return false;
      const p = Sim.Nav.path(n.x, n.y, x, y); if (!p) { n.semCaminho = this.t + 3; this.bus.emit('sem_caminho', { id: n.id, x, y }); return false; }
      n.path = p.slice(); n.fim = fim || null; n.state = 'Walking'; n.setAnim('walk'); return true;
    }
    passo(n, dt) {
      let k = n.path[0]; if (!k) { n.state = 'Idle'; n.setAnim('idle'); const f = n.fim; n.fim = null; f && f(); return; }
      const dx = k[0] - n.x, dy = k[1] - n.y, dist = Math.hypot(dx, dy), step = n.vel * (n.id === 'tonho' && n.estado.pressa ? 1.4 : 1) * dt;
      if (dist <= step) { n.x = k[0]; n.y = k[1]; n.path.shift(); if (!n.path.length) { n.state = 'Idle'; n.setAnim('idle'); const f = n.fim; n.fim = null; f && f(); } return; }
      n.x += dx / dist * step; n.y += dy / dist * step; n.face = dirDe(dx, dy); n.setAnim('walk');
    }
    // ---------------- assentos ----------------
    sentar(n, t) {
      const A = this.assentos[t.assento]; if (!A) { n.task = null; return; }
      if (n.state === 'Sitting') { n.task = null; return; }
      if (A.ocup && A.ocup !== n.id) {            // ocupado: espera por perto
        if (n.state === 'Idle' && !n.estado.esperaDesde) n.estado.esperaDesde = this.clock.min;
        if (n.state === 'Idle') { n.setAnim('idle'); }
        if (A.ocup === 'lia' && this.clock.min - (n.estado.esperaDesde || 0) > 1.2) this.bus.emit('lugar_pedido', { id: n.id, assento: t.assento });
        return;
      }
      n.estado.esperaDesde = null;
      const ap = A.def.aprox, ax = ap[0], ay = yw(ap[0]) + ap[1];
      if (Math.hypot(n.x - ax, n.y - ay) > 3) { this.vaiPara(n, ax, ay, () => { }); return; }
      A.ocup = n.id; n.seat = t.assento; n.state = 'SitIn'; n.sitT = 0; n.from = [n.x, n.y]; n.to = [A.def.x, yw(A.def.x) + A.def.sy]; n.face = A.def.face; n.task = null; n.setAnim('sit');
      this.bus.emit('senta', { id: n.id, assento: t.assento });
    }
    deslizar(n, dt) {
      n.sitT += dt; const k = clamp(n.sitT / .55, 0, 1), e = k * k * (3 - 2 * k);
      n.x = n.from[0] + (n.to[0] - n.from[0]) * e; n.y = n.from[1] + (n.to[1] - n.from[1]) * e;
      if (k >= 1) {
        if (n.state === 'SitIn') { n.state = 'Sitting'; n.setAnim('sit'); } else { n.state = 'Idle'; n.setAnim('idle'); }
      }
    }
    levantarAgora(n) {
      const A = this.assentos[n.seat]; if (!A) { n.state = 'Idle'; return; }
      const ap = A.def.aprox; n.from = [n.x, n.y]; n.to = [ap[0], yw(ap[0]) + ap[1]]; n.state = 'SitOut'; n.sitT = 0; n.setAnim('idle');
      A.ocup = null; const s = n.seat; n.seat = null; this.bus.emit('levanta', { id: n.id, assento: s });
    }
    sentadoTick(n, dt) {
      const A = this.assentos[n.seat]; if (!A) return;
      if (!A.dominio) {                          // assento da rua: variação de animação
        n.cool -= dt; if (n.cool <= 0) { n.cool = 4 + Math.random() * 6; n.setAnim(['sit', 'sit', 'think'][Math.floor(Math.random() * 3)]); }
        if (n.id === 'lucia' && n.seat.startsWith('banco')) { n.setAnim(n.at % 6 < 3 ? 'think' : 'sit'); }
      }
    }
    // ---------------- conversa entre pessoas ----------------
    conversar(n, t) {
      const alvo = this.npcs[t.com]; const par = RD.papos.find(p => p[0] === n.id + '>' + t.com);
      if (!alvo || !par || alvo.state === 'Away') { n.estado.papo = null; n.task = null; return; }
      let P = n.estado.papo; if (!P) P = n.estado.papo = { fase: 0, tt: 0 };
      if (n.state !== 'Idle' && n.state !== 'Acting') return;
      if (P.fase === 0) {                                      // chegar perto
        if (Math.hypot(n.x - alvo.x, n.y - alvo.y) <= 48) { P.fase = 1; P.tt = 0; n.face = alvo.x < n.x ? 'left' : 'right'; n.state = 'Idle'; }
        else {
          const lado = alvo.x < n.x ? 1 : -1, f = Sim.Nav.nearestFree(alvo.x + lado * 30, alvo.y + 6);
          if (!this.vaiPara(n, f[0], f[1], () => { })) { P.fase = 1; }   // sem caminho: fala de onde está
          return;
        }
      }
      P.tt += 1 / 60;
      if (P.fase === 1) { n.face = alvo.x < n.x ? 'left' : 'right'; n.setAnim('talk'); n.falar(par[1][0], 3.6); P.fase = 2; P.tt = 0; }
      else if (P.fase === 2 && P.tt > 3.8) { alvo.falar(par[1][1], 3.6); P.fase = 3; P.tt = 0; n.setAnim('idle'); }
      else if (P.fase === 3 && P.tt > 3.8) { n.estado.papo = null; n.task = null; n.setAnim('idle'); this.bus.emit('papo', { a: n.id, b: t.com }); }
    }
    // ---------------- patrulha ----------------
    patrulha(n, t, dt) {
      if (this.clock.min >= t.ate) { n.task = null; return; }
      if (n.state === 'Idle') {
        n.cool -= dt;
        if (n.estado.parada) {
          if (n.cool > 0) return; n.estado.parada = false;
        }
        if (n.cool <= 0 || !n.estado.parada) {
          const lista = t.spots.filter(s => s !== n.estado.ult); const s = lista[Math.floor(this.rng() * lista.length)]; n.estado.ult = s;
          const sp = this.spot(s); n.estado.pressa = n.id === 'junior' ? true : false;
          this.vaiPara(n, sp.x, sp.y, () => this.chegouPatrulha(n, t, s, sp));
        }
      }
    }
    chegouPatrulha(n, t, s, sp) {
      n.face = sp.face || n.face; n.estado.parada = true;
      const r = this.rng;
      if (n.id === 'tonho') {
        n.cool = 4 + r() * 6; n.setAnim('talk'); n.face = r() < .5 ? 'left' : 'right';
        if (r() < .7) n.falar(['Olha a cocada!', 'Cocada, queijadinha!', 'Quem quer cocada fresquinha?'][Math.floor(r() * 3)], 3);
      } else if (n.id === 'junior') {
        n.cool = 2 + r() * 3;
        if (s === 'gato') { n.setAnim('interact'); n.face = 'right'; this.afagarGato('junior'); }
        else if (s === 'poste_1') { n.setAnim('wave'); n.face = 'up'; }
        else if (s.startsWith('obs')) { n.setAnim('idle'); n.face = n.x < RD.mesa.x ? 'right' : 'left'; n.cool = 3 + r() * 4; n.estado.olhando = true; }
        else { n.setAnim(r() < .5 ? 'wave' : 'idle'); }
      } else n.cool = 3;
      this.bus.emit('chegou', { id: n.id, spot: s });
    }
    // ---------------- bichos ----------------
    afagarGato(quem) { const g = this.gato; g.estado = 'afago'; g.t = 2.6; g.at = 0; this.bus.emit('gato', { quem }); }
    updateBichos(dt) {
      const g = this.gato; g.at += dt; g.t -= dt;
      if (g.estado === 'afago' && g.t <= 0) { g.estado = 'dorme'; }
      // pombos fogem de gente a menos de 26 px e voltam depois
      const gente = [...Object.values(this.npcs).filter(n => n.state !== 'Away' && n.alpha > .4), { x: this.lia.x, y: this.lia.y }];
      for (const p of this.pombos) {
        p.at += dt; p.t -= dt;
        const homeX = p.home[0], homeY = yw(homeX) + p.home[1];
        const perto = gente.find(q => Math.hypot(q.x - p.x, (q.y - p.y) * 1.2) < 26);
        if (perto && p.estado !== 'foge') { p.estado = 'foge'; p.t = 3 + Math.random() * 2; const dir = p.x < perto.x ? -1 : 1; p.alvo = [clamp(p.x + dir * (40 + Math.random() * 30), 20, this.W - 20), clamp(p.y + (Math.random() - .5) * 8, yw(p.x) + 30, this.VH - 4)]; }
        if (p.estado === 'foge') { const dx = p.alvo[0] - p.x, dy = p.alvo[1] - p.y, d = Math.hypot(dx, dy); if (d > 1) { p.x += dx / d * 70 * dt; p.y += dy / d * 70 * dt; p.f = 0; p.face = dx < 0 ? 'left' : 'right'; } if (p.t <= 0) { p.estado = 'volta'; } }
        else if (p.estado === 'volta') { const dx = homeX - p.x, dy = homeY - p.y, d = Math.hypot(dx, dy); if (d > 1.5) { p.x += dx / d * 12 * dt; p.y += dy / d * 12 * dt; p.f = 0; p.face = dx < 0 ? 'left' : 'right'; } else p.estado = 'bicando'; }
        else { p.f = (Math.floor(p.at * 2.6 + p.home[0]) % 3 === 0) ? 1 : 0; }
      }
    }
    nearLia(a, b) { if (this.liaFora) return false; const L = this.lia; return Math.hypot(a.x - L.x, a.y - L.y) < 150 || Math.hypot(b.x - L.x, b.y - L.y) < 150; }
    liberar(id, chave) { this.lib[id + ':' + chave] = true; this.bus.emit('liberado', { id, chave }); }
    updateGreetings(dt) {
      if (this.liaFora) return; const L = this.lia;
      for (const id in this.npcs) {
        const n = this.npcs[id]; if (n.state === 'Away' || n.alpha < .6) continue;
        const d = Math.hypot(n.x - L.x, (n.y - L.y) * 1.3);
        if (d < 46 && this.t - n.greetAt > 90 && !n.say && n.state !== 'Walking' && !(this.mesa.ativoDe(n.id) && this.mesa.fase === 'jogando')) {
          n.greetAt = this.t; const f = RD.falas[id].saudar, mem = this.social.saudacaoLia(id); n.falar(mem || (f[Math.floor(this.rng() * f.length)].split('.')[0].split('?')[0] + (id === 'tonho' ? '!' : '.')), 3.2); this.bus.emit('saudou', { id });
        }
      }
    }
    // ---------------- interação da Lia ----------------
    nivel(id) { return Math.min(3, Math.floor((this.trust[id] || 0) / .25)); }
    // ---------------- vivências da Lia: o que ela viu/ouviu/fez (dá motivo aos assuntos) ----------------
    marcar(f) { if (this.viv[f]) return false; this.viv[f] = this.clock.min; this.bus.emit('vivencia', { f }); return true; }
    tem(f) { return !!this.viv[f]; }
    updateViv(dt) {
      if (this.liaFora) return; const L = this.lia, N = this.npcs, V = this.vivT;
      const perto = (n, r) => n && n.state !== 'Away' && n.alpha > .6 && Math.hypot(n.x - L.x, (n.y - L.y) * 1.3) < r;
      const acum = (k, c, lim) => { V[k] = c ? (V[k] || 0) + dt : Math.max(0, (V[k] || 0) - dt * .5); if (V[k] >= lim) this.marcar(k); };
      acum('viu_jogo', Math.hypot(RD.mesa.x - L.x, (yw(RD.mesa.x) + 16 - L.y) * 1.2) < 95 && this.mesa.fase === 'jogando', 4);
      const lu = N.lucia; acum('viu_medicao', perto(lu, 170) && lu.state === 'Acting' && lu.anim === 'interact', 2);
      const ci = N.cicera; acum('viu_varal', perto(ci, 150) && ci.state === 'Acting', 1.5);
      acum('viu_tonho', perto(N.tonho, 150), 1.5); acum('viu_junior', perto(N.junior, 190), 1.2);
      acum('viu_gato', Math.hypot(this.gato.x - L.x, (this.gato.y - L.y) * 1.3) < 80, 1.2);
      if (this.kp.kp_obj_obra) this.marcar('viu_obra'); if (this.kp.kp_gato) this.marcar('viu_gato');
      if (this.kp.kp_obj_quadro) { this.marcar('viu_aviso'); this.marcar('ouviu_reuniao'); this.marcar('ouviu_programa'); }
      if (this.viv.viu_medicao) this.marcar('ouviu_programa');
    }
    gateOk(id, t, g) {
      const nv = this.nivel(id); return g.quando.length === 0 || g.quando.some(q => q.startsWith('apos:') ? !!this.feitos[q.slice(5)] : q.startsWith('nivel:') ? nv >= +q.slice(6) : this.tem(q));
    }
    topicos(id) {
      const F = RD.falas[id], G = RD.gates[id] || {}, nv = this.nivel(id), out = [];
      for (const t of Object.keys(F.perguntar)) {
        if (!F.perguntar[t].some(r => !r.conf || (nv >= r.conf[0] && nv <= r.conf[1]))) continue;
        const g = G[t] || { label: t, quando: [], ask: 'Posso perguntar sobre isso?' }; if (!this.gateOk(id, t, g)) continue;
        out.push({ id: t, label: g.label, ask: g.ask, feito: !!this.feitos[id + ':' + t] });
      }
      if (this.social.comentarios(id).length && nv >= 1) out.push({ id: 'comentarios', label: 'O que andam comentando', ask: 'E aí, o que andam comentando por aqui?', feito: false });
      return out;
    }
    abrirConversa(id) {
      const n = this.npcs[id], F = RD.falas[id]; if (!n || n.state === 'Away') return null;
      const sa = this.social.saudacaoLia(id) || F.saudar[Math.floor(this.rng() * F.saudar.length)];
      return { id, saudacao: sa, topicos: this.topicos(id).map(t => t.id), semAssunto: !this.topicos(id).length ? RD.dicaSemAssunto : null, nivel: this.nivel(id) };
    }
    ouvir(id) { const F = RD.falas[id]; return [{ quem: id, texto: F.ouvir[Math.floor(this.rng() * F.ouvir.length)], nota: true }]; }
    perguntar(id, top) {
      const G0 = (RD.gates[id] || {})[top], ask = top === 'comentarios' ? 'E aí, o que andam comentando por aqui?' : G0 && G0.ask;
      if (top === 'comentarios') { const o = [{ quem: 'lia', texto: ask }].concat(this.social.perguntarComentarios(id)); if (o.some(l => l.quem === 'nota' && /programa|medindo|casas/i.test(l.texto))) this.marcar('ouviu_programa'); if (o.some(l => /reunião/i.test(l.texto))) this.marcar('ouviu_reuniao'); this.trust[id] = clamp((this.trust[id] || 0) + .02, 0, 1); this.salvar(); return o; }
      const F = RD.falas[id], lst = (F.perguntar[top] || []).filter(r => !r.conf || (this.nivel(id) >= r.conf[0] && this.nivel(id) <= r.conf[1]));
      if (!lst.length) return [{ quem: id, texto: 'Hoje não, Lia.' }];
      // prefere resposta ainda não dada
      this.dados = this.dados || {}; let r = lst.find(x => !this.dados[id + top + x.t]) || lst[lst.length - 1]; this.dados[id + top + r.t] = 1;
      this.feitos[id + ':' + top] = this.clock.min; if (top === 'programa' || top === 'medir') this.marcar('ouviu_programa');
      const out = (ask ? [{ quem: 'lia', texto: ask }] : []).concat([{ quem: id, texto: r.t, revisar: !!r.revisar }]);
      if (r.kp) { const nv = this.ganhar(r.kp); if (nv) out.push({ quem: 'nota', texto: 'Anotado: ' + RD.kp[r.kp][0] }); }
      this.trust[id] = clamp((this.trust[id] || 0) + .06, 0, 1); this.bus.emit('conversa', { id, top }); this.social.liaConversou(id);
      if (id === 'ze' && top === 'lia_jogar') this.liaConvidada = true;
      return out;
    }
    ganhar(id) { if (this.kp[id]) return false; this.kp[id] = { t: this.clock.min }; this.bus.emit('conhecimento', { id, kp: { titulo: RD.kp[id][0], texto: RD.kp[id][1] } }); this.salvar(); return true; }
    examinar(inst) {   // inst = instância da cena
      const kpMap = { mesa_domino: 'kp_obj_mesa', quadro_avisos: 'kp_obj_quadro', orelhao_1: 'kp_obj_orelhao', poste_1: 'kp_obj_poste', poste_2: 'kp_obj_poste', poste_3: 'kp_obj_poste', cavalete_pao: 'kp_obj_cavalete', bike_1: 'kp_obj_bike', lixeira_1: 'kp_obj_lixeira', lixeira_2: 'kp_obj_lixeira', obra_1: 'kp_obj_obra', caixote_1: 'kp_obj_caixote' };
      const k = kpMap[inst.id]; let novo = false; if (k) novo = this.ganhar(k);
      return { texto: inst.desc || inst.nome, nome: inst.nome, novo, kp: k ? RD.kp[k][0] : null };
    }
    afagar() { this.afagarGato('lia'); this.ganhar('kp_gato') ; return '(O gato ronrona e fecha o olho de novo.)'; }
    salvar() { if (this.hooks.save) this.hooks.save({ trust: this.trust, kp: this.kp, dia: this.persist.dia || 1, soc: this.social.exportar(), viv: this.viv, feitos: this.feitos }); }
    resumo() {
      return { jogos: this.mesa.stats, placar: this.mesa.game.placar.slice(), partidas: this.mesa.game.partidas.slice(), kp: Object.keys(this.kp).length, papos: this.bus.count('papo'), portas: this.bus.count('porta') };
    }
    pessoasVisiveis() { return Object.values(this.npcs).filter(n => n.state !== 'Away' && n.alpha > 0); }
  };

  // =============================================================== mesa de dominó viva
  class MesaDomino {
    constructor(w) {
      this.w = w; this.game = new Sim.Domino(w.rng, RD.ordem, RD.dupla); this.fase = 'esperando'; this.tt = 0; this.stats = { maos: 0, jogadas: 0, passes: 0, batidas: 0, trancadas: 0 };
      this.ultimas = []; this.pensando = null; this.dormeAte = 0; this.ocup = {}; this.pausaMsg = 0; this.ultimaBatida = null; this.toc = 0;
      this.liaMao = null;     // mão da Lia quando ela ocupa um lugar
    }
    ocupante(s) { return this.w.assentos[s].ocup; }
    ativoDe(id) { return Object.values(this.w.assentos).some(a => a.dominio && a.ocup === id && this.w.npcs[id] && this.w.npcs[id].state === 'Sitting'); }
    todosSentados() {
      return RD.ordem.every(s => { const o = this.ocupante(s); if (!o) return false; if (o === 'lia') return this.w.lia.sentada; const n = this.w.npcs[o]; return n && n.state === 'Sitting'; });
    }
    pessoa(s) { const o = this.ocupante(s); return o === 'lia' ? this.w.lia : this.w.npcs[o]; }
    setAnimSeat(s, a, dir) { const o = this.ocupante(s); if (!o || o === 'lia') return; const n = this.w.npcs[o]; if (n.state === 'Sitting') n.setAnim(a); }
    falaSeat(s, txt, ttl) { const o = this.ocupante(s); if (o && o !== 'lia') this.w.npcs[o].falar(txt, ttl || 2.4); else if (o === 'lia') this.w.bus.emit('lia_fala', { texto: txt }); }
    update(dt) {
      this.tt += dt; const g = this.game, w = this.w;
      if (this.toc > 0) this.toc -= dt;
      const todos = this.todosSentados();
      if (!todos) {
        if (this.fase === 'jogando' || this.fase === 'embaralhando' || this.fase === 'reagindo') { this.fase = 'pausado'; this.pausaT = 0; }
        if (this.fase === 'pausado') { this.pausaT += dt; if (this.pausaT > 3 && this.pausaMsg < w.t - 25) { this.pausaMsg = w.t; const vaz = RD.ordem.find(s => !this.ocupante(s) || (this.ocupante(s) !== 'lia' && w.npcs[this.ocupante(s)].state !== 'Sitting')); const quem = RD.ordem.find(s => this.ocupante(s) && s !== vaz && w.npcs[this.ocupante(s)] && w.npcs[this.ocupante(s)].state === 'Sitting' && RD.dupla[s] !== RD.dupla[vaz]); if (quem) this.falaSeat(quem, ['Cadê o parceiro?', 'Vai esperar ele voltar?', 'Sem o quarto a mesa fica manca.'][Math.floor(w.rng() * 3)], 3.5); } }
        else this.fase = 'esperando';
        for (const s of RD.ordem) { const o = this.ocupante(s); if (o && o !== 'lia' && w.npcs[o].state === 'Sitting' && (w.npcs[o].anim === 'think' || w.npcs[o].anim === 'play')) w.npcs[o].setAnim('sit'); }
        return;
      }
      if (!this.lataFeita) {                                                  // antes da primeira mão: a lata colaborativa (proposta, revisar)
        const L = this.lata = this.lata || { i: 0, t: 2 }; L.t -= dt;
        if (L.t <= 0) {
          const e = RD.lata[L.i++];
          if (!e) { this.lataFeita = true; if (RD.ordem.some(s => this.ocupante(s) === 'lia')) w.knowledge.award('kp_lata', { via: 'ouvida' }); }
          else { const s = RD.ordem.find(q => this.ocupante(q) === e[0]); if (s) { this.falaSeat(s, e[1], 3.6); L.t = 3.9; } }
        }
        return;
      }
      if (this.fase === 'esperando' || this.fase === 'pausado') { this.pensando = null; if (g.estado !== 'jogando') { this.fase = 'reagindo'; this.tt = 4.4; } else if (g.cadeia.length) { this.fase = 'jogando'; this.tt = 0; } else { this.fase = 'embaralhando'; this.tt = 0; } }
      if (this.fase === 'embaralhando') {
        if (this.tt > 4.2) { this.fase = 'jogando'; this.tt = 0; this.novoTurno(); }
        else for (const s of RD.ordem) { const n = this.ocupante(s) !== 'lia' && this.w.npcs[this.ocupante(s)]; if (n && n.anim !== 'sit' && this.tt < 0.2) n.setAnim('sit'); }
        return;
      }
      if (this.fase === 'reagindo') { if (this.tt > 5.2) { g.proximaMao(); this.w.bus.emit('dom_mao', {}); this.liaMao = null; this.fase = 'embaralhando'; this.tt = 0; this.stats.maos++; for (const s of RD.ordem) this.setAnimSeat(s, 'sit'); } return; }
      if (this.fase === 'jogando') this.turno(dt);
    }
    novoTurno() { const g = this.game, s = g.vez; this.pensando = { s, t: 0, dur: this.duracao(s), joga: null }; this.setAnimSeat(s, 'think'); }
    duracao(s) { const o = this.ocupante(s), j = RD.jogo[o] || { pensa: [2, 4] }; const [a, b] = j.pensa; return a + this.w.rng() * (b - a); }
    turno(dt) {
      const g = this.game, w = this.w, P = this.pensando; if (!P) { this.novoTurno(); return; }
      if (g.estado !== 'jogando') { this.fase = 'reagindo'; this.tt = 4.4; return; }
      const o = this.ocupante(P.s);
      if (P.jogou) {
        P.t += dt;
        if (P.t >= P.espera) {   // fim do gesto
          this.pensando = null; this.setAnimSeat(P.s, 'sit');
          if (g.estado === 'jogando') this.novoTurno(); else this.fimDeMao(P);
        }
        return;
      }
      if (o === 'lia') { w.bus.emit('lia_vez', { s: P.s }); P.liaEsperando = true; return; }
      P.t += dt;
      if (P.t < P.dur) return;
      const j = RD.jogo[o] || { agro: .5, fala: .4 }; const leg = g.legais(P.s);
      if (!leg.length) { const r = g.passar(P.s); if (!r) { this.pensando = null; return; } this.stats.passes++; this.toc = .6; this.setAnimSeat(P.s, 'play'); this.falaSeat(P.s, RD.dom.passa[Math.floor(w.rng() * RD.dom.passa.length)], 2); w.bus.emit('dom_passa', { s: P.s, id: o }); P.jogou = true; P.espera = .9; if (r && r.tranca) this.tranca(r); return; }
      const c = g.escolher(P.s, j.agro); const r = g.jogar(P.s, c.t, c.lado); this.stats.jogadas++; this.ultimas.push({ s: P.s, t: c.t, lado: c.lado }); if (this.ultimas.length > 8) this.ultimas.shift();
      this.setAnimSeat(P.s, 'play'); this.toc = .6; if (w.rng() < j.fala * .45) this.falaSeat(P.s, RD.dom.joga[Math.floor(w.rng() * RD.dom.joga.length)], 1.8);
      w.bus.emit('dom_joga', { s: P.s, id: o, t: c.t, lado: c.lado, pontas: r.pontas }); P.jogou = true; P.espera = .85; P.res = r;
      if (r.bate) this.bateu(r);
    }
    // jogada da Lia (UI): devolve true se aceita
    liaJoga(t, lado) {
      const P = this.pensando, g = this.game; if (!P || this.ocupante(P.s) !== 'lia' || P.jogou) return false;
      const r = g.jogar(P.s, t, lado); if (!r) return false; this.stats.jogadas++; this.ultimas.push({ s: P.s, t, lado: r.lado }); if (this.ultimas.length > 8) this.ultimas.shift();
      this.toc = .6; this.w.bus.emit('dom_joga', { s: P.s, id: 'lia', t, lado: r.lado, pontas: r.pontas }); P.jogou = true; P.espera = .6; P.res = r; P.t = 0; if (r.bate) this.bateu(r); return true;
    }
    liaPassa() {
      const P = this.pensando, g = this.game; if (!P || this.ocupante(P.s) !== 'lia' || P.jogou) return false;
      if (g.legais(P.s).length) return false; const r = g.passar(P.s); this.stats.passes++; this.toc = .6; this.w.bus.emit('dom_passa', { s: P.s, id: 'lia' }); P.jogou = true; P.espera = .6; P.t = 0; if (r.tranca) this.tranca(r); return true;
    }
    bateu(r) {
      const { s, tipo, pts, dupla } = r.bate, w = this.w; this.stats.batidas++; this.ultimaBatida = { s, tipo, pts, dupla };
      const o = this.ocupante(s); const txt = RD.dom.bate[tipo][Math.floor(w.rng() * RD.dom.bate[tipo].length)];
      this.setAnimSeat(s, 'react'); if (o !== 'lia') this.falaSeat(s, txt, 3); else w.bus.emit('lia_fala', { texto: txt });
      for (const q of RD.ordem) { if (q === s) continue; const same = RD.dupla[q] === RD.dupla[s]; this.setAnimSeat(q, same ? 'react' : 'think'); if (w.rng() < .6) this.falaSeat(q, (same ? RD.dom.reage_bom : RD.dom.reage_ruim)[Math.floor(w.rng() * 3)], 3); }
      w.bus.emit('dom_bate', { s, id: o, tipo, pts, dupla, placar: this.game.placar.slice(), partida: r.partida });
      this.toc = 1.2; this.fase = 'reagindo'; this.tt = 0; this.pensando = { jogou: true, t: 0, espera: 99, s };
    }
    tranca(r) { const w = this.w; this.stats.trancadas++; for (const q of RD.ordem) { this.setAnimSeat(q, 'think'); } this.falaSeat(r.s || this.game.vez, RD.dom.tranca[Math.floor(w.rng() * 2)], 3); w.bus.emit('dom_tranca', { placar: this.game.placar.slice(), dupla: r.tranca.dupla }); this.fase = 'reagindo'; this.tt = 0; this.pensando = { jogou: true, t: 0, espera: 99, s: this.game.vez }; }
    fimDeMao(P) { }
    // dados para o painel "observar a mesa"
    painel() {
      const g = this.game; return { cadeia: g.cadeia.map(c => c.t), pontas: g.pontas, placar: g.placar.slice(), partidas: g.partidas.slice(), vez: g.vez, resta: Object.fromEntries(RD.ordem.map(s => [s, g.maos[s].length])), mao: g.mao,
        fase: this.fase, nomes: Object.fromEntries(RD.ordem.map(s => { const o = this.ocupante(s); return [s, o ? (o === 'lia' ? 'Lia' : RD.pessoas[o].curto) : '—']; })), ultima: this.ultimaBatida };
    }
    // Lia ocupa uma cadeira vaga (com a mão do ocupante anterior)
    liaSenta(s) { const A = this.w.assentos[s]; if (A.ocup) return false; const outros = RD.ordem.map(q => this.w.assentos[q].ocup).filter(x => x && x !== 'lia'); const faltava = this.fase === 'pausado' || outros.length < 3; A.ocup = 'lia'; this.w.lia.seat = s; if (faltava && outros.length) this.w.social.liaAjudouMesa(outros); return true; }
    liaLevanta() { const s = this.w.lia.seat; if (!s) return; const A = this.w.assentos[s]; A.ocup = null; this.w.lia.seat = null; this.w.lia.sentada = false; if (this.pensando && this.pensando.liaEsperando) this.pensando = null; }
    minhaMao() { const s = this.w.lia.seat; return s ? this.game.maos[s] : null; }
    legaisLia() { const s = this.w.lia.seat; return s ? this.game.legais(s) : []; }
  }
  Sim.Rua.MesaDomino = MesaDomino;
})();
