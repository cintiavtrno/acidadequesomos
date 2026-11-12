// ===== s6_npc.js — NPCController: máquina de estados (NPCStateMachine), decisão (NPCDecisionSystem) e rotina (NPCSchedule) =====
// Estados dos clientes: Away · Entering · Idle · Observing · Waiting · Ordering · Seating · Sitting · Standing · Praying · Measuring · Approaching · Leaving
// Estados da Vó:        Work · Walking · Interacting · Serving · TalkLia
// A animação é consequência do estado (anim/face), nunca uma sequência fixa.
Sim.NPC = class {
  constructor(w, id, def) {
    this.w = w; this.id = id; this.def = def; this.isVo = id === 'aurea';
    this.x = 240; this.y = 240; this.face = 'down'; this.anim = 'idle'; this.at = 0; this.state = this.isVo ? 'Work' : 'Away'; this.stateT = 0;
    this.loc = this.isVo ? 'padaria' : 'rua'; this.path = []; this.say = null; this.mood = 'normal'; this.moodT = 0; this.chat = null; this.dialogLia = false;
    this.needs = Object.assign({}, def.necessidades || {}); this.ses = {}; this.seat = null; this.wait = 0; this.blockT = 0; this.visitas = []; this.vi = 0;
    this.speed = Sim.cfg.speedPx[id] || 24; this.plan = null; this.arrived = false;
    if (this.isVo) { this.x = 196; this.y = 168; this.anim = 'serve_idle'; }
  }
  setState(s) { if (this.state === s) return; const antes = this.state; this.state = s; this.stateT = 0; this.w.bus.emit('estado_npc', { id: this.id, de: antes, para: s }); }
  setAnim(a) { if (this.anim !== a) { this.anim = a; this.at = 0; } }
  zona() {
    if (this.isVo) return 'posto';
    return { Waiting: 'fila', Ordering: 'fila', Sitting: 'mesa', Seating: 'mesa', Praying: 'altar', Observing: 'vitrine', Measuring: 'medindo' }[this.state] || null;
  }
  estadoFala() { return this.isVo ? (this.state === 'Serving' ? 'servindo' : null) : null; }
  // ---- movimento ----
  goTo(x, y, snap) {
    const N = Sim.Nav, g = snap === false ? [x, y] : N.nearestFree(x, y); this.path = N.path(this.x, this.y, g[0], g[1]) || [g]; this.arrived = false; this.blockT = 0;
    this.goal = g; return this.path.length > 0;
  }
  others() { return this.w.mobiles().filter(o => o !== this); }
  stepMove(dt) {
    if (!this.path.length) { this.arrived = true; return false; }
    const t = this.path[0], dx = t[0] - this.x, dy = t[1] - this.y, d = Math.hypot(dx, dy), vy = 16 / 24;
    if (d < 1.2) { this.path.shift(); if (!this.path.length) { this.arrived = true; return false; } return true; }
    // cortesia: espera quem está parado logo à frente; depois de um tempo, contorna
    for (const o of this.others()) { if (o.state === 'Away' || o.loc !== this.loc) continue; const ox = o.x - this.x, oy = o.y - this.y; if (Math.hypot(ox, oy) < 9 && (ox * dx + oy * dy) > 0) { this.blockT += dt; if (this.blockT > .9) { this.blockT = 0; const sx = dy / d * 10, sy = -dx / d * 10; const nx = this.x + sx, ny = this.y + sy; if (Sim.Nav.free(nx, ny)) this.path.unshift([nx, ny]); } this.setAnim('idle'); return true; } }
    this.blockT = 0;
    const k = Math.min(d, this.speed * dt * (Math.abs(dy) > Math.abs(dx) ? vy : 1)) / d, nx = this.x + dx * k, ny = this.y + dy * k;
    if (Sim.Nav.free(nx, ny) || this.sliding) { this.x = nx; this.y = ny; } else { this.path = []; this.arrived = true; return false; }
    this.face = Sim.dir8(dx, dy) || this.face; this.setAnim(this.isVo ? 'walk' : 'walk'); return true;
  }
  slideTo(x, y, dur, done) { this.slide = { x0: this.x, y0: this.y, x1: x, y1: y, t: 0, dur, done }; }
  tickSlide(dt) { const s = this.slide; if (!s) return false; s.t += dt; const k = Math.min(1, s.t / s.dur); this.x = s.x0 + (s.x1 - s.x0) * k; this.y = s.y0 + (s.y1 - s.y0) * k; this.setAnim('walk'); if (k >= 1) { this.slide = null; if (s.done) s.done(); } return true; }
  tick(dt) {
    this.stateT += dt; this.at += dt;
    if (this.say) { this.say.ttl -= dt; if (this.say.ttl <= 0) this.say = null; }
    if (this.moodT > 0) { this.moodT -= dt; if (this.moodT <= 0) this.mood = 'normal'; }
    for (const k in this.needs) this.needs[k] = Math.min(1, this.needs[k] + dt * (k === 'social' ? .0012 : .0008));
    if (this.isVo) return this.w.vo.tick(this, dt);
    if (this.dialogLia) {                                  // quem está conversando com a Lia para um instante (no máximo 15 s) em vez de sair andando
      this.dialogT = (this.dialogT || 0) + dt;
      if (this.dialogT < 15 && ['Idle', 'Entering', 'Approaching', 'Leaving', 'Seating', 'Observing'].includes(this.state) && !this.slide) { this.setAnim('talk'); const L = this.w.lia; this.face = Sim.dir8(L.x - this.x, L.y - this.y) || this.face; return; }
    } else this.dialogT = 0;
    if (this.tickSlide(dt)) return;
    Sim.States[this.state] && Sim.States[this.state](this, this.w, dt);
  }
};

// ---- estados dos clientes ----
Sim.States = {
  Away(n, w) {
    if (n.loc !== 'rua') return;
    const v = n.visitas[n.vi]; if (!v || w.clock.min < v.at || !w.clock.isOpen() || w.persist.evita[n.id] >= 2 && !v.retry) return;
    n.vi++; n.loc = 'padaria'; n.x = 240; n.y = 240; n.face = 'up'; n.ses = { chegou: w.clock.min, saiAs: w.clock.min + w.rng.range(v.estadia[0], v.estadia[1]), served: false, gaveUp: false, retry: !!v.retry, rezou: false, mediu: 0, sentou: 0, olhou: false, fila0: null };
    n.setState('Entering'); w.bus.emit('chegou', { id: n.id }); w.stats.visitas++;
    const door = Sim.Nav.nearestFree(240, w.pontos.porta[1] - 14); n.goTo(door[0], door[1], false);
  },
  Entering(n, w, dt) { if (!n.stepMove(dt) && n.arrived) { n.setAnim('idle'); n.setState('Idle'); } },
  Idle(n, w, dt) {
    n.setAnim('idle'); if (n.stateT < .5 + (n.id.length % 3) * .15) return;
    Sim.Decision.decide(n, w);
  },
  Observing(n, w, dt) {
    if (n.path.length) { n.stepMove(dt); return; }
    n.face = 'up'; n.setAnim('idle');
    if (n.stateT > n.ses.olharT) { n.ses.olhou = true; n.setState('Idle'); }
  },
  Waiting(n, w, dt) {                                  // a fila é controlada pelo ServiceSystem (posição, paciência, ordem)
    if (n.path.length) { n.stepMove(dt); return; }
    n.face = 'up'; n.setAnim(n.chat ? 'talk' : 'idle');
    if (n.chat) { const o = w.npcs[n.chat.a === n.id ? n.chat.b : n.chat.a]; if (o) n.face = Sim.dir8(o.x - n.x, o.y - n.y) || n.face; }
  },
  Ordering(n, w, dt) { n.face = 'up'; n.setAnim('talk'); },
  Seating(n, w, dt) {
    if (n.path.length) { n.stepMove(dt); return; }
    if (!n.arrived && !n.seat) return;
    const s = n.seat; if (!s || w.seatOcc[s.id] !== n.id) { n.setState('Idle'); return; }
    n.slideTo(s.x, s.y, .45, () => { n.setState('Sitting'); n.setAnim('sit'); n.face = s.face; n.ses.sentou++; n.ses.sitUntil = w.clock.min + w.rng.range(18, 40); w.bus.emit('sentou', { id: n.id, seat: s.id }); });
    n.setState('SeatingIn');
  },
  SeatingIn() {},
  Sitting(n, w, dt) {
    const s = n.seat; n.face = s.face; n.setAnim(n.chat ? 'sit' : 'sit');
    const forcar = !w.clock.isOpen() || w.clock.min >= n.ses.saiAs; if (w.clock.min < n.ses.sitUntil && !forcar) return;
    if (n.chat || n.dialogLia) return;
    n.slideTo(n.seat.ax, n.seat.ay, .4, () => { w.seatOcc[n.seat.id] = null; n.seat = null; n.setAnim('idle'); n.setState('Idle'); }); n.setState('Standing');
  },
  Standing() {},
  Praying(n, w, dt) {
    if (n.path.length) { n.stepMove(dt); return; }
    n.face = 'up'; n.setAnim('idle');
    if (!n.ses.rezando) { n.ses.rezando = true; n.say = { text: '(reza baixinho)', ttl: 4 }; w.bus.emit('rezou', { id: n.id }); if (n.ses.rezou) n.ses.rezou2 = true; n.ses.rezou = true; w.needs(n, 'social', .05); }
    if (n.stateT > 9) { n.ses.rezando = false; if (n.mood === 'preocupado') w.setMood(n.id, 'normal'); n.setState('Idle'); }
  },
  Measuring(n, w, dt) {
    const S = n.ses; if (n.path.length) { n.stepMove(dt); return; }
    const alvo = n.def.mede[S.mediu]; if (!alvo) { n.setState('Idle'); return; }
    n.face = 'up'; n.setAnim('interact');
    if (!S.medindo) { S.medindo = true; S.t0 = n.stateT; w.bus.emit('medindo', { id: n.id, ponto: alvo }); }
    if (n.stateT - S.t0 > 6) { S.medindo = false; S.mediu++; if (S.mediu === 1) w.mem.remember('lucia', 'mediu_sala', { publico: true, alias: 'soube_mediu' }); n.setAnim('idle'); n.setState('Idle'); }
  },
  Approaching(n, w, dt) {
    const t = w.npcs[n.ses.alvoId]; if (!t || t.state === 'Away' || t.loc !== 'padaria') { n.setState('Idle'); return; }
    if (n.path.length) { n.stepMove(dt); if (n.stateT > 14) n.setState('Idle'); return; }
    n.face = Sim.dir8(t.x - n.x, t.y - n.y) || n.face; n.setAnim('idle'); w.needs(n, 'social', -.0); n.ses.fala_c = (n.ses.fala_c || 0) + 1;
    const s = w.convs.script(n, t); if (s && w.convs.eligible(n) && w.convs.eligible(t)) w.convs.start(n, t, s); else if (n.stateT > 2) n.setState('Idle');
    if (n.chat) { n.setState('Idle'); n.ses.paradoConv = w.clock.min; }
  },
  Leaving(n, w, dt) {
    if (n.path.length) { n.stepMove(dt); return; }
    n.loc = 'rua'; n.setState('Away'); n.x = 240; n.y = 250; w.bus.emit('saiu', { id: n.id }); n.ses.saiu = true;
  },
};
// os estados em transição (SeatingIn / Standing) só mexem na posição; garantimos que existam
Sim.States.SeatingIn = (n) => { n.setAnim('walk'); };
Sim.States.Standing = (n) => { n.setAnim('walk'); };

// ---- decisão: utilidade = necessidade × traço × contexto + ruído (semente) ----
Sim.Decision = {
  decide(n, w) {
    const d = n.def, S = n.ses, rng = w.rng, o = [], add = (a, s, p) => o.push({ a, s: s + rng() * .1, p });
    const sair = !w.clock.isOpen() || w.clock.min >= S.saiAs || w.clock.min >= w.clock.closeAt - 8;
    if (!S.served && !S.gaveUp) {
      if (!S.olhou && d.olha !== 0) add('vitrine', 2, null); else if (w.service.temVaga()) add('fila', 2); else add('vitrine', 1.2, 'espera');
    } else if (S.gaveUp) add('sair', 2);
    else {
      if (d.reza && w.obj('altar_vela') && (!S.rezou || (n.mood === 'preocupado' && !S.rezou2)) && w.clock.min > S.chegou + 3) add('rezar', .55 + d.tracos.religioso * .35 + (n.mood === 'preocupado' ? .5 : 0));
      if (d.mede && S.mediu < d.mede.length) add('medir', .95);
      const seat = this.seatFor(n, w); if (seat && S.sentou < 2) add('sentar', n.needs.cansaco * .8 + n.needs.social * .35 + (seat.companhia ? .35 : 0) + (S.rezou || S.mediu ? .15 : .1), seat);
      const par = this.partner(n, w); if (par && !sair) add('conversar', n.needs.social * .75 + (w.rel.get(n.id, par.id).aff > .3 ? .25 : 0) - (S.paradoConv && w.clock.min - S.paradoConv < 25 ? .6 : 0), par);
      add('sair', sair ? 3 : .08 + (1 - n.needs.social) * .1);
    }
    o.sort((a, b) => b.s - a.s); const e = o[0]; this.exec(n, w, e.a, e.p);
  },
  seatFor(n, w) {                                       // assento preferido livre; ganha bônus quem senta perto de alguém com quem se dá bem
    let best = null;
    const ids = n.def.assentos.slice(); for (const id in w.seats) if (!ids.includes(id)) { const s = w.seats[id]; if (s.ap && !w.seatOcc[id] && w.mobiles().some(o => o !== n && o.seat && Math.hypot(o.seat.x - s.x, o.seat.y - s.y) < 62 && w.rel.get(n.id, o.id).aff > .3)) ids.push(id); }
    for (const id of ids) { const s = w.seats[id]; if (!s || w.seatOcc[id] || !s.ap) continue; let comp = false; for (const o of w.mobiles()) if (o !== n && o.seat && Math.hypot(o.seat.x - s.x, o.seat.y - s.y) < 60 && w.rel.get(n.id, o.id).aff > .2) comp = true; if (!best || (comp && !best.companhia)) best = Object.assign({ companhia: comp }, s); }
    return best;
  },
  partner(n, w) {
    let b = null, bs = 0; for (const id in w.npcs) { const o = w.npcs[id]; if (o === n || o.isVo || o.loc !== 'padaria' || !w.convs.eligible(o) || ['Away', 'Entering'].includes(o.state)) continue; const s = w.rel.get(n.id, id).aff + .3 - Sim.dist(n, o) / 400; if (s > bs) { bs = s; b = o; } }
    return b;
  },
  exec(n, w, a, p) {
    const S = n.ses, P = w.pontos;
    if (a === 'vitrine') { const pt = P.vitrine[(n.id.length) % P.vitrine.length]; n.goTo(pt[0], pt[1]); S.olharT = p ? 4 : (n.def.olha != null ? n.def.olha : 3); n.setState('Observing'); }
    else if (a === 'fila') { w.service.entrar(n); }
    else if (a === 'rezar') { n.goTo(P.altar[0], P.altar[1] + 12); n.setState('Praying'); }
    else if (a === 'medir') { const k = n.def.mede[S.mediu]; const pt = w.medidas[k]; n.goTo(pt[0], pt[1]); n.setState('Measuring'); }
    else if (a === 'sentar') { w.seatOcc[p.id] = n.id; n.seat = w.seats[p.id]; n.goTo(p.ap[0], p.ap[1], false); n.setState('Seating'); }
    else if (a === 'conversar') { const t = p; const off = [[-16, 0], [16, 0], [0, 14]]; let g = null; for (const [dx, dy] of off) if (Sim.Nav.free(t.x + dx, t.y + dy)) { g = [t.x + dx, t.y + dy]; break; } if (!g) { n.setState('Idle'); S.paradoConv = w.clock.min; return; } S.alvoId = t.id; n.goTo(g[0], g[1], false); n.setState('Approaching'); }
    else if (a === 'sair') this.sair(n, w);
  },
  sair(n, w) {
    if (n.seat) { w.seatOcc[n.seat.id] = null; n.seat = null; }
    w.service.sair(n); const dx = Sim.Nav.nearestFree(240, w.pontos.porta[1] - 6); n.goTo(dx[0], dx[1]); n.path.push([240, 244]); n.setState('Leaving'); w.bus.emit('saindo', { id: n.id, atendido: n.ses.served, desistiu: n.ses.gaveUp });
    const v = n.def.visitas[0];
    if (n.ses.gaveUp && !n.ses.retry && (w.persist.evita[n.id] || 0) < 2) n.visitas.push({ at: w.clock.min + 22 + w.rng.range(0, 6), retry: true, estadia: [30, 50] });
  },
};
