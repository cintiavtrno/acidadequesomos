// ===== s12_casa.js — o mundo da casa: Seu Raimundo em casa (rotina, decisão, estados) + interação da Lia =====
// Reaproveita da Etapa 4: relógio, EventSystem, Nav, relações, memória, conhecimento, objetivos, DialogueSystem e as peças de movimento do NPC.
// Preparado para a Etapa 6: usa as mesmas chaves de persistência (rel/mem/kp) e guarda o estado da casa em persist.casa, para a casa e a padaria
// compartilharem o mesmo mundo e nada reiniciar quando Lia entra ou sai.
// Estados do Raimundo: Away (na padaria/rua) · Entering · Idle · Walking · Doing · SeatingIn · Sitting · Standing · Leaving
Sim.HomeNPC = class {
  constructor(w, id, def) {
    this.w = w; this.id = id; this.def = def; this.isVo = false;
    this.x = 240; this.y = 222; this.face = 'up'; this.anim = 'idle'; this.at = 0; this.state = 'Idle'; this.stateT = 0; this.loc = 'casa'; this.path = []; this.say = null;
    this.mood = 'normal'; this.moodT = 0; this.dialogLia = false; this.dialogT = 0; this.needs = Object.assign({}, def.necessidades || {}); this.ses = {}; this.seat = null;
    this.speed = Sim.cfg.speedPx[id] || 16; this.act = null; this.arrived = false; this.blockT = 0; this.murT = 8; this.feitas = {}; this.ultima = null;
  }
  zona() { return this.act ? (this.act.faseZona || this.act.def.zona) : null; }
  estadoFala() { return this.act && this.act.def.id === 'cafe' && this.act.i === 0 && this.state === 'Doing' ? 'coando' : null; }
  others() { return this.w.mobiles().filter(o => o !== this); }
};
for (const k of ['setState', 'setAnim', 'goTo', 'stepMove', 'slideTo', 'tickSlide']) Sim.HomeNPC.prototype[k] = Sim.NPC.prototype[k];

Sim.HomeStates = {
  Away(n, w) {
    if (n.loc !== 'rua') return;
    if (w.clock.min >= n.volta && !w.clock.ended) {
      n.loc = 'casa'; n.x = w.pontos.porta[0]; n.y = w.pontos.porta[1] + 3; n.face = 'up'; n.setState('Entering'); w.bus.emit('chegou_casa', { id: n.id });
      const d = Sim.Nav.nearestFree(w.pontos.entrada[0], w.pontos.entrada[1]); n.goTo(d[0], d[1], false);
    }
  },
  Entering(n, w, dt) { if (!n.stepMove(dt) && n.arrived) { n.setAnim('idle'); n.setState('Idle'); w.dialogue.speak(n, w.casaPick('chegou')); n.needs.cansaco = Math.max(n.needs.cansaco, .8); } },
  Idle(n, w, dt) {
    n.setAnim('idle'); if (n.stateT < .8) return;
    if (w.clock.min >= n.sai && !n.ses.saiu && !w.clock.ended) { n.ses.saiu = true; w.dialogue.speak(n, w.casaPick('saiu')); n.act = null; const p = w.pontos.porta; n.goTo(p[0], p[1] + 2, false); n.setState('Leaving'); return; }
    w.decide(n);
  },
  Walking(n, w, dt) {
    if (n.path.length) { n.stepMove(dt); if (n.stateT > 40) { n.act = null; n.setState('Idle'); } return; }
    const a = n.act, f = a.def.fases[a.i];
    if (f.seat) {
      const s = w.seats[f.seat]; if (!s || (w.seatOcc[s.id] && w.seatOcc[s.id] !== n.id)) { n.act = null; n.setState('Idle'); return; }
      w.seatOcc[s.id] = n.id; n.seat = s; n.slideTo(s.x, s.y, .45, () => { n.setState('Sitting'); n.setAnim('sit'); n.face = s.face; w.beginPhase(n); }); n.setState('SeatingIn'); return;
    }
    n.face = f.face || 'up'; n.setAnim(f.anim || 'interact'); n.setState('Doing'); w.beginPhase(n);
  },
  Doing(n, w, dt) { w.tickAct(n, dt, false); },
  SeatingIn() {},
  Sitting(n, w, dt) { const s = n.seat; n.face = s.face; n.setAnim('sit'); w.tickAct(n, dt, true); },
  Standing() {},
  Leaving(n, w, dt) {
    if (n.path.length) { n.stepMove(dt); return; }
    n.loc = 'rua'; n.setState('Away'); n.ses.voltou = false; w.bus.emit('saiu_casa', { id: n.id });
  },
};

Sim.CasaWorld = class {
  constructor(o) {
    Sim.Casa.install(); o = o || {};
    this.scene = o.scene; this.hooks = o.hooks || { objs: {} }; this.seed = o.seed || 1991; this.rng = Sim.RNG(this.seed);
    this.persist = Object.assign({ evita: {}, fiado: {}, dia: 1, rel: null, mem: null, kp: null, casa: null }, o.persist || {});
    this.bus = new Sim.EventSystem(); this.clock = new Sim.WorldClock({ start: o.start != null ? o.start : 420, rate: o.rate || 1, openAt: 420, closeAt: 720, day: this.persist.dia });
    this.pontos = this.scene.pontos; this.flags = {}; this.timers = []; this.cena = 'casa'; this.carry = null; this.fim = false;
    this.lia = { x: 240, y: 222, face: 'up', seat: null, state: 'idle' };
    this.rel = new Sim.Relations(this.bus, Sim.Data.relacoes); if (this.persist.rel) this.rel.import(this.persist.rel);
    this.mem = new Sim.Memory(this.bus); if (this.persist.mem) this.mem.import(this.persist.mem);
    this.knowledge = new Sim.Knowledge(this); if (this.persist.kp) this.knowledge.import(this.persist.kp);
    this.objectives = new Sim.Objectives(this); for (const ob of Sim.Data.objetivos) this.objectives.check(ob.id);
    this.dialogue = new Sim.Dialogue(this); this.interaction = new Sim.CasaInteraction(this);
    this.viv = Object.assign({}, this.persist.viv || {}); this.cafe = null; this.pedido = null;
    this.stats = { atividades: 0, visitas_lia: 0, conversas_lia: 0, observadas: {}, kp_novos: 0 };
    this.seats = {}; this.seatOcc = {}; this.vistas = {};
    for (const s of this.scene.seats) { const S = Object.assign({}, s), ap = Sim.Nav.approach(S); S.ap = ap; if (ap) { S.ax = ap[0]; S.ay = ap[1]; } this.seats[s.id] = S; }
    const def = Sim.Data.pessoas.raimundo; this.npcs = { raimundo: new Sim.HomeNPC(this, 'raimundo', def) };
    const R = this.npcs.raimundo, C = Sim.Data.casa; R.sai = C.saidaPadaria.a + this.rng.range(-C.saidaPadaria.jit, C.saidaPadaria.jit); R.volta = C.voltaPadaria.a + this.rng.range(-C.voltaPadaria.jit, C.voltaPadaria.jit);
    for (const k in R.needs) R.needs[k] = Sim.clamp(R.needs[k] + this.rng.range(-.1, .1), 0, 1);
    this.start = { kp: Object.keys(this.knowledge.got).length, rel: this.rel.export() };
    this.posicaoInicial(); this.restore();
    this.bus.on('conhecimento', () => this.guardar()); this.bus.on('objetivo_concluido', () => this.guardar());
  }
  posicaoInicial() {                                                   // onde ele está quando o relógio começa (a rotina é por hora, não por "abrir a casa")
    const R = this.npcs.raimundo, m = this.clock.min; R.x = this.pontos.sala[0]; R.y = this.pontos.sala[1];
    if (m >= R.sai) R.ses.saiu = true;
    if (m >= R.sai && m < R.volta) { R.loc = 'rua'; R.state = 'Away'; }
  }
  marcar(f) { if (this.viv[f]) return false; this.viv[f] = this.clock.min; this.bus.emit('vivencia', { f }); return true; }
  mobiles() { return Object.values(this.npcs); }
  presente(id) { const n = this.npcs[id]; return !!n && n.loc === 'casa' && n.state !== 'Away'; }
  obj(id) { return this.hooks.getObj ? this.hooks.getObj(id) : (this.hooks.objs[id] || 0); }
  setObj(id, v) { if (this.hooks.setObj) this.hooks.setObj(id, v); else this.hooks.objs[id] = v; this.bus.emit('estado_objeto', { id, v }); }
  flag(id) { return !!this.flags[id]; }
  needs(n, k, d) { n.needs[k] = Sim.clamp(n.needs[k] + d, 0, 1); }
  setMood(id, m, s) { const n = this.npcs[id]; if (n) { n.mood = m; n.moodT = s || 60; } }
  liaPerto(o, r) { return Sim.dist(this.lia, o) <= r; }
  casaPick(kind, extra) { const n = this.npcs.raimundo, c = this.ctx(extra); const f = this.dialogue.pick(Sim.Data.casa.falas[kind], c); return f ? f.texto : ''; }
  ctx(extra) { const n = this.npcs.raimundo; return Object.assign({ id: 'raimundo', loc: n.zona(), estado: n.estadoFala(), nivel: this.rel.nivel('raimundo', 'lia'), humor: n.mood, hora: this.clock.min }, extra || {}); }
  // ---- NPCDecisionSystem: necessidade × traço × janela do dia × recência + ruído com semente
  decide(n) {
    const w = this, m = w.clock.min, C = Sim.Data.casa; let best = null, bs = -1;
    for (const a of C.atividades) {
      if (m < a.janela[0] || m > a.janela[1]) continue;
      if (a.id === 'cafe' && n.feitas.cafe) continue; if (a.id === 'cozinha' && n.feitas.cozinha) continue;
      if ((a.id === 'cama' || a.id === 'planta' || a.id === 'reza') && n.feitas[a.id] && m < 600) continue;
      if (a.fases[0].seat && w.seatOcc[a.fases[0].seat] && w.seatOcc[a.fases[0].seat] !== n.id) continue;
      let s = a.peso; if (a.cansaco) s *= .5 + n.needs.cansaco * 1.2; if (a.fome) s *= .6 + n.needs.fome * 1.2; if (a.devocao) s *= .7 + (n.def.tracos.religioso || .5) * .8;
      s *= 1 - Math.min(.8, (n.feitas[a.id] || 0) * .35); if (n.ultima === a.id) s *= .15; s += w.rng() * .5;
      if (n.mood === 'preocupado' && a.id === 'reza') s *= 1.6; if (n.mood === 'preocupado' && a.id === 'janela') s *= 1.3;
      if (s > bs) { bs = s; best = a; }
    }
    if (!best) { n.setAnim('idle'); n.face = 'up'; return; }
    const d = best.dur, dur = d[0] + (d[1] - d[0]) * w.rng();
    n.act = { def: best, i: 0, fim: 0, dur, ini: m, faseZona: null }; n.feitas[best.id] = (n.feitas[best.id] || 0) + 1; n.ultima = best.id; w.stats.atividades++;
    w.bus.emit('atividade', { id: best.id, nome: best.nome });
    w.goPhase(n);
  }
  goPhase(n) {
    const a = n.act, f = a.def.fases[a.i]; a.faseZona = f.zona || null;
    let p; if (f.seat) { const s = this.seats[f.seat]; p = s.ap || [s.x, s.y + 8]; } else p = this.pontos[f.ponto];
    n.goTo(p[0], p[1]); n.setState('Walking');
  }
  beginPhase(n) {
    const a = n.act, f = a.def.fases[a.i], m = this.clock.min, d = a.i === 0 ? a.def.dur : (a.def.dur2 || a.def.dur);
    a.dur = d[0] + (d[1] - d[0]) * this.rng(); a.fim = m + a.dur; a.faseZona = f.zona || null; a.t0 = m;
    if (f.fogao) this.setObj('fogao_1', 1);
    if (f.reza) { this.setObj('oratorio_1', 1); this.bus.emit('rezou', { id: n.id }); }
    n.murT = 3 + this.rng() * 5; this.bus.emit('atividade_inicio', { id: a.def.id, fase: a.i });
  }
  endPhase(n, sitting) {
    const a = n.act, f = a.def.fases[a.i];
    if (f.reza) this.setObj('oratorio_1', 0); if (f.fogao) this.setObj('fogao_1', 0);
    if (a.i + 1 < a.def.fases.length) {
      const prox = a.def.fases[a.i + 1]; a.i++;
      if (sitting) { n.slideTo(n.seat.ax, n.seat.ay, .4, () => { this.seatOcc[n.seat.id] = null; n.seat = null; this.goPhase(n); }); n.setState('Standing'); }
      else this.goPhase(n); return;
    }
    if (a.def.id === 'cafe') n.feitas.cafe = 1; if (a.def.id === 'cozinha') n.feitas.cozinha = 1;
    this.bus.emit('atividade_fim', { id: a.def.id });
    const nec = a.def; if (nec.cansaco) n.needs.cansaco = Math.max(0, n.needs.cansaco - .35); if (nec.fome) n.needs.fome = Math.max(0, n.needs.fome - .4); if (nec.devocao) n.needs.social = Math.max(0, n.needs.social - .05);
    if (a.def.id === 'reza' && n.mood === 'preocupado') this.setMood('raimundo', 'normal');
    n.act = null;
    if (sitting) { n.slideTo(n.seat.ax, n.seat.ay, .4, () => { this.seatOcc[n.seat.id] = null; n.seat = null; n.setAnim('idle'); n.setState('Idle'); }); n.setState('Standing'); }
    else { n.setAnim('idle'); n.setState('Idle'); }
  }
  tickAct(n, dt, sitting) {
    const a = n.act; if (!a) { n.setState('Idle'); return; }
    const m = this.clock.min, perto = this.liaPerto(n, 120);
    // observar: Lia por perto vê o que ele faz; três coisas diferentes viram "a manhã dele"
    if (perto && m - a.t0 > a.dur * .35) { if (!this.vistas[a.def.id]) { this.vistas[a.def.id] = true; this.bus.emit('observou', { id: a.def.id }); if (Object.keys(this.vistas).length >= 3) this.knowledge.award('kp_c_rotina', { via: 'observou' }); } }
    if (a.def.fases[a.i].reza && perto && Sim.dist(this.lia, n) < 90 && m - a.t0 > 1) this.knowledge.award('kp_raimundo_reza', { via: 'observou' });
    // murmúrios (só quando alguém está por perto para ouvir; sem repetir a mesma fala)
    n.murT -= dt; if (n.murT <= 0) { n.murT = 12 + this.rng() * 14; if (perto && !n.say && !n.dialogLia) { const f = this.dialogue.pick(Sim.Data.casa.falas.murmurio, this.ctx()); if (f) this.dialogue.speak(n, f.texto, 3.2); } }
    if (a.def.ctrl) return;                                    // cena guiada (café na mesa): quem encerra a fase é a cena
    if (n.dialogLia) return;                                   // conversando com a Lia: o relógio da atividade espera (a casa não pula etapas)
    if (m >= a.fim) this.endPhase(n, sitting);
  }
  update(dt) {
    if (this.fim && this.clock.ended) return;
    dt = Math.min(dt, .25); this.bus.t += dt; this.clock.tick(dt);
    for (const t of this.timers.slice()) { t.t -= dt; if (t.t <= 0) { this.timers.splice(this.timers.indexOf(t), 1); t.fn(); } }
    if (this.dialogosPausa > 0) this.dialogosPausa -= dt;
    this.tickRaimundo(dt); this.tickVisita(dt); this.interaction.tickCafe(dt);
    if (this.clock.min >= 720 && !this.fim) this.endDay();
  }
  tickRaimundo(dt) {
    const n = this.npcs.raimundo; n.stateT += dt; n.at += dt;
    if (n.say) { n.say.ttl -= dt; if (n.say.ttl <= 0) n.say = null; }
    if (n.moodT > 0) { n.moodT -= dt; if (n.moodT <= 0) n.mood = 'normal'; }
    for (const k in n.needs) n.needs[k] = Math.min(1, n.needs[k] + dt * (k === 'social' ? .0012 : .0008));
    if (n.dialogLia && n.state !== 'Away') {                    // quem conversa com a Lia para um instante (no máximo 15 s)
      n.dialogT += dt;
      if (n.dialogT < 15 && ['Idle', 'Walking', 'Entering', 'Doing', 'Sitting', 'Leaving'].includes(n.state) && !n.slide) { n.setAnim(n.state === 'Sitting' ? 'sit' : 'talk'); if (n.state !== 'Sitting') n.face = Sim.dir8(this.lia.x - n.x, this.lia.y - n.y) || n.face; return; }
    } else n.dialogT = 0;
    if (n.tickSlide(dt)) return;
    Sim.HomeStates[n.state] && Sim.HomeStates[n.state](n, this, dt);
  }
  tickVisita(dt) {                                             // Raimundo reage à chegada da Lia
    const n = this.npcs.raimundo; if (n.loc !== 'casa' || n.state === 'Away' || this.flags.visitou) return;
    if (this.liaPerto(n, 150) && Math.abs(this.lia.y - n.y) < 120) {
      this.flags.visitou = true; this.mem.remember('raimundo', 'lia_visitou_casa', { publico: true, alias: 'soube_visita_casa' }); this.stats.visitas_lia++; this.bus.emit('visita', {});
      const t = this.casaPick('visita'); if (t) this.dialogue.speak(n, t, 4);
    }
  }
  // ---- persistência: a casa continua de onde parou (Etapa 6 usa o mesmo formato)
  exportar() {
    const n = this.npcs.raimundo;
    return { min: this.clock.min, dia: this.clock.day, obj: { fogao_1: this.obj('fogao_1'), oratorio_1: this.obj('oratorio_1') }, flags: this.flags, vistas: this.vistas,
      raimundo: { x: n.x, y: n.y, face: n.face, loc: n.loc, state: n.state === 'Away' ? 'Away' : 'Idle', feitas: n.feitas, ultima: n.ultima, sai: n.sai, volta: n.volta, needs: n.needs, mood: n.mood, saiu: !!n.ses.saiu } };
  }
  restore() {
    const c = this.persist.casa; if (!c || c.dia !== this.clock.day) return;
    this.clock.min = Math.max(this.clock.min, c.min); this.flags = c.flags || {}; this.vistas = c.vistas || {};
    for (const k in c.obj) this.setObj(k, c.obj[k]);
    const n = this.npcs.raimundo, r = c.raimundo; Object.assign(n, { x: r.x, y: r.y, face: r.face, loc: r.loc, feitas: r.feitas || {}, ultima: r.ultima, sai: r.sai, volta: r.volta, needs: r.needs || n.needs, mood: r.mood || 'normal' });
    n.ses.saiu = r.saiu; n.state = r.state === 'Away' ? 'Away' : 'Idle';
  }
  guardar(fim) { this.persist.rel = this.rel.export(); this.persist.mem = this.mem.export(); this.persist.kp = this.knowledge.export(); this.persist.viv = this.viv; this.persist.casa = this.exportar(); if (this.hooks.save) this.hooks.save(this.persist, !!fim); }
  step(secs, dt) { dt = dt || .1; for (let t = 0; t < secs; t += dt) this.update(dt); }
  endDay() {
    this.clock.ended = true; this.fim = true; const kpn = Object.keys(this.knowledge.got).length - this.start.kp;
    const ant = this.start.rel, mud = [];
    for (const k in this.rel.m) { const a = ant[k], b = this.rel.m[k]; if (!a) continue; const d = (b.trust - a.trust) + (b.aff - a.aff); if (Math.abs(d) >= .04) mud.push({ par: k, aff: +(b.aff - a.aff).toFixed(2), trust: +(b.trust - a.trust).toFixed(2) }); }
    const r = { dia: this.clock.day, atividades: this.stats.atividades, visitas: this.stats.visitas_lia, vistas: Object.keys(this.vistas), pontos_novos: kpn, pontos: Object.keys(this.knowledge.got).length,
      objetivos: this.objectives.list().map(o => ({ id: o.id, titulo: o.titulo, n: o.n, meta: o.meta, feito: o.feito })), mudancas: mud };
    this.persist.dia = this.clock.day + 1; this.guardar(true); this.bus.emit('dia_fim', { resumo: r }); return r;
  }
};

// ---- InteractionSystem da casa: mesmos verbos da padaria (Ouvir · Perguntar · Ajudar) e examinar objetos
Sim.CasaInteraction = class {
  constructor(w) { this.w = w; }
  rotulos() { return Sim.Data.casa.rotulos; }
  // assuntos CONTEXTUAIS: só aparecem se a Lia tem motivo (viu o retrato, ouviu falar do Programa, viu o jogo...)
  topicos(id) {
    const w = this.w, k = w.knowledge, v = w.viv, f = w.flags, t = ['rua', 'casa'];
    const vRet = k.has('kp_c_retrato'), vFoto = k.has('kp_c_foto');
    if (vRet) t.push('retrato'); if (vFoto) t.push('forno'); if (vRet || vFoto) t.push('mae');
    if (v.ouviu_programa) t.push('programa'); if (v.ouviu_programa) t.push('papel'); if (f.p_programa || f.p_papel) t.push('assinar');
    if (k.has('kp_c_domino') || v.viu_jogo) t.push('domino');
    return t;
  }
  ajudas(id) {
    const w = this.w, n = w.npcs[id], a = n.act, r = [];
    r.push({ id: 'cafe', ok: !!a && a.def.id === 'cafe' && a.i === 0 && n.state === 'Doing', motivo: 'Só dá pra ajudar enquanto ele está coando o café, de manhã tarde.' });
    r.push({ id: 'agua', ok: w.carry === 'copo', motivo: 'Precisa de um copo d\'água. A talha de barro fica perto da cozinha.' });
    r.push({ id: 'regar', ok: !!a && a.def.id === 'planta' && n.state === 'Doing', motivo: 'Só enquanto ele está regando, de manhã cedo.' });
    return r;
  }
  saudar(id) { const w = this.w, f = w.dialogue.pick(Sim.Data.casa.falas.saudar, w.ctx()); return f ? f.texto : '...'; }
  abrir(id) { const w = this.w, n = w.npcs[id]; n.dialogLia = true; w.stats.conversas_lia++; w.bus.emit('dialogo', { id }); const d = Sim.dir8(w.lia.x - n.x, w.lia.y - n.y); if (d && n.state !== 'Sitting') n.face = d;
    w.knowledge.award('kp_c_visita', { via: 'conversou' });
    return { saudacao: this.saudar(id), topicos: this.topicos(id), ajudas: this.ajudas(id), pressionar: false, extra: this.cafeJuntos() }; }
  fechar(id) { const n = this.w.npcs[id]; if (n) n.dialogLia = false; if (this.w.cafe && this.w.cafe.fase === 'conversa') this.cena('fechar'); }
  aplicar(verbo, id, arg) {
    const w = this.w, n = w.npcs[id], R = w.rel, L = [], rot = this.rotulos(), F_ = Sim.Data.casa.falas, c = () => w.ctx(), K = w.knowledge, say = f => f && L.push({ quem: id, texto: f.texto, revisar: f.revisar });
    if (verbo === 'ouvir') {
      L.push({ quem: 'nota', texto: 'Você fica em silêncio e escuta.' }); say(w.dialogue.pick(F_.ouvir, c())); R.change(id, 'lia', { trust: .012 }, 'ouviu');
      if (n.zona() === 'oratorio') K.award('kp_raimundo_reza', { via: 'observou' }); if (n.zona() === 'radio') w.marcar('ouviu_programa');
    } else if (verbo === 'perguntar') {
      L.push({ quem: 'lia', texto: (Sim.Data.casa.asks || {})[arg] || rot[arg] }); w.flags['p_' + arg] = true; say(w.dialogue.pick(F_.perguntar[arg], c())); R.change(id, 'lia', { trust: .01 }, 'perguntou:' + arg); const nv = R.nivel(id, 'lia');
      if (arg === 'mae' && nv >= 2) K.award('kp_c_mae', { via: 'perguntou' }); if (arg === 'casa') K.award('kp_raimundo_casa', { via: 'perguntou' });
      if (arg === 'forno' && nv >= 1) K.award('kp_raimundo_sexta', { via: 'perguntou' }); if (arg === 'assinar') K.award('kp_c_assinar', { via: 'perguntou' });
      if (arg === 'domino' && nv >= 0) { w.flags.convite_domino = true; w.mem.remember('raimundo', 'convidou_dominó'); K.award('kp_c_convite', { via: 'perguntou' }); }
      if (arg === 'papel') w.mem.remember('raimundo', 'lia_perguntou_papel');
    } else if (verbo === 'ajudar') {
      const a = this.ajudas(id).find(x => x.id === arg); L.push({ quem: 'lia', texto: rot[arg] }); if (!a || !a.ok) { L.push({ quem: 'nota', texto: a ? a.motivo : '...' }); return { linhas: L }; }
      say(w.dialogue.pick(F_.ajudar[arg], c()));
      if (arg === 'cafe') { R.change(id, 'lia', { trust: .12, aff: .08 }, 'cafe'); w.mem.remember(id, 'lia_coou_cafe', { publico: true, alias: 'soube_cafe' }); K.award('kp_c_cafe', { via: 'ajudou' }); n.act.fim = Math.max(w.clock.min + .5, n.act.fim - 1.5); }
      if (arg === 'agua') { w.carry = null; R.change(id, 'lia', { trust: .14, aff: .08 }, 'agua'); w.mem.remember(id, 'lia_ajudou_agua', { publico: true }); K.award('kp_raimundo_agua', { via: 'ajudou' }); }
      if (arg === 'regar') { R.change(id, 'lia', { trust: .06, aff: .04 }, 'regou'); n.act.fim = Math.max(w.clock.min + .3, n.act.fim - 1); }
    }
    return { linhas: L };
  }
  // ---------------- café na mesa (cena guiada) ----------------
  cafeJuntos() {
    const w = this.w, n = w.npcs.raimundo, t = 'Tomar café juntos';
    if (w.cafe) return { t, ok: false, motivo: 'O café já está servido.' };
    if (w.flags.cafe_juntos) return { t, ok: false, motivo: 'Vocês já tomaram café juntos hoje. Ele conta que não é de repetir o que já disse.' };
    if (!w.presente('raimundo')) return { t, ok: false, motivo: 'Ele não está em casa.' };
    if (w.rel.nivel('raimundo', 'lia') < 1) return { t, ok: false, motivo: 'Ele ainda não tem intimidade pra te convidar à mesa. Ouça, ajude em casa e volte a falar.' };
    if (['Entering', 'Leaving', 'SeatingIn', 'Standing', 'Walking'].includes(n.state) && n.state !== 'Walking') return { t, ok: false, motivo: 'Ele está no meio de um movimento. Espere um instante.' };
    if (n.act && n.act.def.id === 'reza') return { t, ok: false, motivo: 'Ele está rezando. Espere.' };
    if (w.clock.min > 700) return { t, ok: false, motivo: 'Já é quase hora do almoço; ele vai pro fogão.' };
    return { t, ok: true };
  }
  soltar(n, fn) {
    if (n.state === 'Sitting' && n.seat) { const S = n.seat; n.slideTo(S.ax, S.ay, .4, () => { this.w.seatOcc[S.id] = null; n.seat = null; n.setState('Idle'); fn(); }); n.setState('Standing'); }
    else { n.act = null; fn(); }
  }
  iniciarCafe() {
    const w = this.w, n = w.npcs.raimundo, c = this.cafeJuntos(); if (!c.ok) return false;
    n.dialogLia = false; n.act = null;
    w.cafe = { fase: 'preparo', t: 0, feitos: {}, n: 0, aviso: 0 };
    w.dialogue.speak(n, 'Senta aí na mesa, filha. O café sai já.', 3.6);
    const go = () => { n.act = { def: Sim.Data.casa.cafeJuntosDef, i: 0, fim: 1e9, dur: 0, ini: w.clock.min, faseZona: null }; w.goPhase(n); };
    this.soltar(n, go); w.pedido = { tipo: 'sentar', id: 'cad_esq' }; w.bus.emit('cafe_inicio', {});
    return true;
  }
  abortarCafe() { const w = this.w, n = w.npcs.raimundo; if (!w.cafe) return; w.cafe = null; n.dialogLia = false; if (n.act && n.act.def.ctrl) { n.act = null; if (n.state === 'Doing') { n.setAnim('idle'); n.setState('Idle'); } } w.pedido = { tipo: 'levantar' }; }
  tickCafe(dt) {
    const w = this.w, c = w.cafe; if (!c) return; const n = w.npcs.raimundo; c.t += dt;
    if (c.t > 150 && c.fase !== 'conversa') return this.abortarCafe();
    if (c.fase === 'preparo') {
      if (n.state === 'Doing' && n.act && n.act.def.ctrl && !c.coando) { c.coando = true; c.t0 = c.t; w.dialogue.speak(n, 'Duas colheres. Nem mais, nem menos.', 3.2); }
      if (c.coando && c.t - c.t0 > 4.5) { c.fase = 'sentando'; c.t = 0; w.endPhase(n, false); }
    } else if (c.fase === 'sentando') {
      if (c.t > 14 && !c.lembrou) { c.lembrou = true; w.dialogue.speak(n, 'Pode sentar, filha. A cadeira não morde.', 3.4); w.pedido = { tipo: 'sentar', id: 'cad_esq' }; }
      if (n.state === 'Sitting' && n.seat && n.seat.id === 'cad_dir' && w.lia.sentada === 'cad_esq') { c.fase = 'conversa'; c.t = 0; n.dialogLia = true; n.setAnim('sit'); w.pedido = { tipo: 'abrirCena' }; }
    } else if (c.fase === 'fim') {
      if (!w.lia.sentada || c.t > 6) { w.cafe = null; n.dialogLia = false; w.flags.cafe_juntos = true; w.endPhase(n, n.state === 'Sitting'); w.bus.emit('cafe_fim', {}); }
    }
  }
  cenaOpcoes() {
    const w = this.w, c = w.cafe, C = Sim.Data.casa.cena, out = [];
    for (const k in C.opcoes) { if (k === 'calar') continue; const o = C.opcoes[k]; if (c.feitos[k] || !o.quando(w)) continue; out.push({ id: k, t: o.t }); }
    if (!c.feitos.calar && c.n < 3) out.push({ id: 'calar', t: C.opcoes.calar.t });
    out.push({ id: 'fechar', t: C.fechar.t }); return out;
  }
  cenaInicio() { const w = this.w; return { linhas: Sim.Data.casa.cena.abertura.slice(), opcoes: this.cenaOpcoes(), fim: false }; }
  cena(id) {
    const w = this.w, c = w.cafe, C = Sim.Data.casa.cena, R = w.rel, n = w.npcs.raimundo; if (!c) return { linhas: [], opcoes: [], fim: true };
    if (id === 'fechar' || c.n >= 3) {
      const L = C.fechar.linhas.slice(); R.change('raimundo', 'lia', { trust: .08, aff: .08 }, 'cafe_juntos'); w.mem.remember('raimundo', 'lia_cafe_juntos', { publico: true, alias: 'soube_cafe_juntos' }); w.knowledge.award('kp_c_cafe_juntos', { via: 'cafe' });
      if (!w.flags.convite_domino && R.nivel('raimundo', 'lia') >= 1) { L.push(C.convite); w.flags.convite_domino = true; w.mem.remember('raimundo', 'convidou_dominó'); w.knowledge.award('kp_c_convite', { via: 'cafe' }); }
      c.fase = 'fim'; c.t = 0; w.pedido = { tipo: 'levantar' }; this.fechar('raimundo'); return { linhas: L, opcoes: [], fim: true };
    }
    const o = C.opcoes[id]; if (!o || c.feitos[id]) return { linhas: [], opcoes: this.cenaOpcoes(), fim: false };
    c.feitos[id] = true; c.n++; const L = (typeof o.linhas === 'function' ? o.linhas(w) : o.linhas).slice();
    if (o.trust) R.change('raimundo', 'lia', { trust: o.trust, aff: o.trust * .6 }, 'cafe:' + id);
    if (o.kp && w.knowledge.award(o.kp, { via: 'cafe' })) L.push({ quem: 'nota', texto: 'Anotado: ' + (Sim.Data.conhecimentos.find(k => k.id === o.kp) || {}).titulo });
    for (const k of (o.kps || [])) if (w.knowledge.award(k, { via: 'cafe' })) L.push({ quem: 'nota', texto: 'Anotado: ' + (Sim.Data.conhecimentos.find(x => x.id === k) || {}).titulo });
    if (o.kpSe && R.nivel('raimundo', 'lia') >= o.kpSe[1] && w.knowledge.award(o.kpSe[0], { via: 'cafe' })) L.push({ quem: 'nota', texto: 'Anotado: ' + (Sim.Data.conhecimentos.find(x => x.id === o.kpSe[0]) || {}).titulo });
    if (o.marca) w.flags[o.marca] = true; w.bus.emit('cena_cafe', { id });
    return { linhas: L, opcoes: this.cenaOpcoes(), fim: false };
  }
  objeto(o, ctx) {
    const w = this.w, D = Sim.Data.objetos[o.id], r = { texto: D ? D.texto(w, ctx || {}) : (o.desc || o.title || ''), kp: null }, n = w.npcs.raimundo;
    if (o.id === 'talha_1') { w.carry = 'copo'; r.texto = 'Você enche a caneca esmaltada na talha de barro. A água está fresca.'; }
    if (D && D.kp) { r.kp = D.kp; w.knowledge.award(D.kp, { via: 'examinou' }); }
    if (n.loc === 'casa' && n.state !== 'Away' && Sim.dist(w.lia, n) < 130 && !n.say) {         // ele comenta quando alguém mexe no que é dele
      const l = Sim.Data.casa.falas.reacao_exame[o.id]; if (l) { const f = w.dialogue.pick(l, w.ctx()); if (f) w.dialogue.speak(n, f.texto, 3.6); }
    }
    w.bus.emit('objeto', { id: o.id });
    return r;
  }
};
