// ===== s7_service.js — CustomerServiceSystem (fila, pedidos, estoque, caixa, fiado) e rotina da Vó (NPCController da Vó) =====
// O atendimento é todo da Vó. Ele não pergunta onde a Lia está: com ou sem Lia, a fila anda.
Sim.Service = class {
  constructor(w) { this.w = w; this.queue = []; this.stock = Object.assign({}, Sim.Data.estoque); this.caixa = 0; this.fiado = {}; this.job = null; }
  temVaga() { return this.queue.length < 4; }
  slot(i) { const f = this.w.pontos.fila; return f[f.length - 1 - i]; }                 // 0 = frente (perto da porta/caixa)
  entrar(n) {
    const w = this.w; this.queue.push(n.id); n.ses.pat = n.def.paciencia * w.rng.range(.92, 1.08); n.ses.filaDesde = w.clock.min; n.ses.slotI = -1;
    n.setState('Waiting'); w.bus.emit('fila_entrou', { id: n.id, tam: this.queue.length });
    if (this.queue.length >= 3) w.reage('fila_cheia', n.id, 'fila_cheia');
  }
  sair(n) { if (this.jobLia && this.jobLia.cust === n.id) this.jobLia = null; const i = this.queue.indexOf(n.id); if (i >= 0) this.queue.splice(i, 1); if (this.job && this.job.cust === n.id) this.job = null; }
  cedeVez(a, b, social) {                                                         // b passa à frente de a
    const q = this.queue, ia = q.indexOf(a), ib = q.indexOf(b); if (ia < 0 || ib < 0 || ib < ia || (this.job && this.job.cust === a)) return false;
    q.splice(ib, 1); q.splice(ia, 0, b); this.w.bus.emit('vez_cedida', { de: a, para: b, social: !!social });
    this.w.rel.change(a, b, { aff: .04 }, 'cedeu_vez'); return true;
  }
  desistir(n) {
    const w = this.w; this.sair(n); n.ses.gaveUp = true; w.stats.desistencias++; w.persist.evita[n.id] = (w.persist.evita[n.id] || 0) + 1;
    w.mem.remember('aurea', 'desistiu_' + n.id, { publico: true }); w.mem.remember(n.id, 'esperou_demais');
    w.setMood(n.id, n.id === 'dandara' ? 'irritada' : 'cansado', 70);
    w.rel.change(n.id, 'aurea', { aff: -.04, trust: -.02 }, 'desistiu_fila'); w.bus.emit('desistiu', { id: n.id, esperou: Math.round(w.clock.min - n.ses.filaDesde) });
    w.reage('desistiu', n.id, 'desistiu'); n.setState('Idle');
  }
  update(dt) {
    const w = this.w, v = w.npcs.aurea;
    this.queue.forEach((id, i) => {                                              // posições e paciência
      const n = w.npcs[id]; if (!n) return;
      const doLia = this.jobLia && this.jobLia.cust === id;
      if (n.ses.slotI !== i && !(this.job && this.job.cust === id) && !doLia) { n.ses.slotI = i; const s = this.slot(i); n.goTo(s[0], s[1], false); }
      if ((this.job && this.job.cust === id) || doLia) return;
      if (n.state === 'Waiting') { const mult = n.dialogLia || n.chat ? .4 : (w.vo.ocupadaCom(v) ? 1 : 1.15); n.ses.pat -= dt * mult; if (n.ses.pat <= 0) this.desistir(n); }
    });
    this.tickLia(dt);
    const prox = this.queue.find(id => !(this.jobLia && this.jobLia.cust === id));
    if (!this.job && prox && v.state === 'Work' && !v.plan) {      // a Vó chama o primeiro da fila que já chegou ao lugar (menos quem a Lia está atendendo)
      const n = w.npcs[prox]; if (n && n.state === 'Waiting' && !n.path.length && Math.abs(n.x - this.slot(this.queue.indexOf(prox))[0]) < 3) this.comeca(n, v);
    }
  }
  // ---- Lia atende no balcão (PROPOSTA): pega o próximo da fila que a Vó ainda não chamou; 4,6 s: pedido → separar → cobrar
  podeLia() { for (const id of this.queue) { if (this.job && this.job.cust === id) continue; const n = this.w.npcs[id]; if (n && n.state === 'Waiting' && !n.path.length && n.loc === 'padaria') return n; } return null; }
  liaAtende() {
    const n = this.jobLia ? null : this.podeLia(); if (!n) return null; const w = this.w;
    if (n.dialogLia) w.bus.emit('dialogo_interrompido', { id: n.id });
    this.jobLia = { cust: n.id, t: 0, stage: 'pedir', dit: false }; n.setState('Ordering'); w.bus.emit('lia_atende', { id: n.id }); return n;
  }
  // fiado por visita: Raimundo sempre; os outros, às vezes (proposta)
  fiadoDe(n) { const p = n.def.pedido; if (n.ses.fiado === undefined) n.ses.fiado = p.fiado === true || (!!p.fiadoChance && this.w.rng() < p.fiadoChance); return n.ses.fiado; }
  pedeFiado(n) { const F = Sim.Data.reacoes.pedidoFiado && Sim.Data.reacoes.pedidoFiado[n.id]; if (F && n.def.pedido.fiado !== true && this.fiadoDe(n)) this.w.dialogue.speak(n, F); }
  cancelaLia() { const j = this.jobLia; if (!j) return; const n = this.w.npcs[j.cust]; this.jobLia = null; if (n && n.state === 'Ordering' && this.queue.includes(n.id)) { n.setState('Waiting'); n.ses.slotI = -1; } this.w.bus.emit('lia_largou', { id: j.cust }); }
  tickLia(dt) {
    const j = this.jobLia; if (!j) return; const w = this.w, n = w.npcs[j.cust];
    if (!n || n.loc !== 'padaria') { this.jobLia = null; return; }
    j.t += dt; const p = n.def.pedido;
    if (j.stage === 'pedir') { if (!j.dit) { j.dit = true; const L = w.dialogue.line(n.id, 'pedido', w.dialogue.ctx(n.id)); if (L) w.dialogue.speak(n, L.texto); this.pedeFiado(n); } if (j.t > 1.2) { j.stage = 'preparar'; j.t = 0; } }
    else if (j.stage === 'preparar') { if (j.t > 2.2) { for (const k in p.itens) { const q = Math.min(p.itens[k], this.stock[k]); this.stock[k] -= q; if (q < p.itens[k]) w.bus.emit('falta', { item: k }); } j.stage = 'cobrar'; j.t = 0; this.cobra(n, w.npcs.aurea, true); } }
    else if (j.stage === 'cobrar' && j.t > 1.2) {
      this.jobLia = null; this.sair(n); n.ses.served = true; w.stats.servidos++; w.stats.pela_lia = (w.stats.pela_lia || 0) + 1; w.stats.esperas.push(Math.round(w.clock.min - n.ses.filaDesde));
      w.bus.emit('atendido', { id: n.id, espera: Math.round(w.clock.min - n.ses.filaDesde), por: 'lia' }); n.needs.fome = 0; n.setState('Idle');
    }
  }
  comeca(n, v) {
    const w = this.w; if (n.dialogLia) w.bus.emit('dialogo_interrompido', { id: n.id });
    this.job = { cust: n.id, stage: 'ir', t: 0, wait: Math.round(w.clock.min - n.ses.filaDesde) }; v.setState('Serving'); v.plan = null;
    const x = Sim.clamp(this.slot(0)[0], 124, 236); v.goTo(x, w.pontos.vo_posto[1], false); n.setState('Ordering');
    if (w.cena !== 'interior' || Sim.dist(w.lia, v) > 140) w.stats.sem_lia++;
  }
  // etapas do atendimento (chamado a cada tick pela Vó)
  tickJob(v, dt) {
    const w = this.w, j = this.job; if (!j) { v.setState('Work'); return; }
    const n = w.npcs[j.cust]; if (!n || n.loc !== 'padaria') { this.job = null; v.setState('Work'); return; }
    if (v.dialogLia) { v.setAnim('serve_give'); v.face = 'down'; return; }                 // a Vó para para falar com a Lia: a fila espera
    j.t += dt; const p = n.def.pedido;
    const falar = (id, t) => { const N = w.npcs[id]; w.dialogue.speak(N, t); };
    switch (j.stage) {
      case 'ir': if (!v.stepMove(dt)) { v.face = 'down'; v.setAnim('serve_idle'); j.stage = 'pedir'; j.t = 0; const L = w.dialogue.line(n.id, 'pedido', w.dialogue.ctx(n.id)); if (L) falar(n.id, L.texto); this.pedeFiado(n); if (n.id === 'raimundo' && p.fiado && w.liaPerto(n, 95)) w.knowledge.award('kp_raimundo_fiado', { via: 'ouvida' }); } break;
      case 'pedir': v.face = 'down'; if (j.t > 2.8) { j.stage = 'anotar'; j.t = 0; v.setAnim('serve_write'); const B = w.dialogue.line('aurea', 'balcao', w.dialogue.ctx('aurea', {})); if (B) falar('aurea', B.texto); } break;
      case 'anotar': if (j.t > 2.2) { j.stage = 'preparar'; j.t = 0; v.setAnim('serve_wrap'); } break;
      case 'preparar': if (j.t > 4.2) { for (const k in p.itens) { const q = Math.min(p.itens[k], this.stock[k]); this.stock[k] -= q; if (q < p.itens[k]) w.bus.emit('falta', { item: k }); } j.stage = p.papo && w.rng.chance(.9) ? 'papo' : 'entregar'; j.t = 0; j.i = 0; v.setAnim('serve_idle'); if (j.stage === 'papo') { const bank = Sim.Data.bate_papo_balcao[n.id]; j.papo = bank ? w.rng.pick(bank) : null; j.pw = 0; } } break;
      case 'papo': {
        j.pw -= dt; if (!j.papo || j.i >= j.papo.length) { j.stage = 'entregar'; j.t = 0; v.setAnim('serve_give'); break; }
        if (j.pw <= 0) { const [q, t] = j.papo[j.i++]; falar(q, t); j.pw = w.npcs[q].say.ttl + .4; w.bus.emit('conversa_fala', { quem: q, texto: t, id: 'balcao:' + n.id, perto_lia: w.liaPerto(n, 95) }); }
        v.setAnim(j.i % 2 ? 'serve_idle' : 'serve_wrap'); n.setAnim('talk'); if (j.t > 40) { j.stage = 'entregar'; j.t = 0; } break;
      }
      case 'entregar': v.setAnim('serve_give'); if (j.t > 1.8) { j.stage = 'cobrar'; j.t = 0; v.setAnim('serve_write'); this.cobra(n, v); } break;
      case 'cobrar': if (j.t > (this.fiadoDe(n) ? 3 : 2)) { this.fim(n, v); } break;
    }
  }
  cobra(n, v, mudo) {
    const w = this.w, p = n.def.pedido; let val = 0; for (const k in p.itens) val += p.itens[k] * Sim.Data.precos[k];
    if (this.fiadoDe(n)) {
      const f = this.fiado[n.id] = this.fiado[n.id] || { n: 0, valor: 0 }; f.n++; f.valor += val; w.persist.fiado[n.id] = f;
      w.mem.remember('aurea', 'fiado_' + n.id); const B = w.dialogue.line('aurea', 'balcao', w.dialogue.ctx('aurea', { estado: 'fiado' })); if (B && !mudo) w.dialogue.speak(v, B.texto);
      w.bus.emit('fiado', { id: n.id, valor: val });
      for (const o of w.mobiles()) if (o !== n && !o.isVo && o.loc === 'padaria' && o.state !== 'Away' && Sim.dist(o, n) < 130 && o.id === 'lucia') { w.mem.remember('lucia', 'viu_fiado', { publico: true }); w.setMood('raimundo', 'constrangido', 50); w.reage('fiado_visto', 'raimundo', 'fiado_visto', 'lucia'); w.bus.emit('fiado_visto', { quem: 'lucia' }); }
    } else { this.caixa += val; const B = w.dialogue.line('aurea', 'balcao', w.dialogue.ctx('aurea', { estado: 'pago' })); if (B && !mudo) w.dialogue.speak(v, B.texto); w.bus.emit('pago', { id: n.id, valor: val }); }
  }
  fim(n, v) {
    const w = this.w, j = this.job; this.job = null; this.sair(n); n.ses.served = true; w.stats.servidos++; w.stats.esperas.push(j.wait);
    w.bus.emit('atendido', { id: n.id, espera: j.wait }); n.needs.fome = 0; n.setState('Idle'); v.setState('Work'); v.setAnim('serve_idle'); v.ses = { prox: 1.2 };
  }
};

// ---- rotina da Vó: planos (ir a um lugar e agir) e trabalho de balcão ----
Sim.VoCtrl = class {
  constructor(w) { this.w = w; this.nextForno = 38; this.opened = false; this.restocked = false; this.idleT = 2; }
  ocupadaCom(v) { return v.state === 'Serving'; }
  startPlan(v, steps) { v.plan = steps.slice(); v.setState('Walking'); this.nextStep(v); }
  nextStep(v) {
    const s = v.plan && v.plan.shift(); if (!s) { v.plan = null; v.setState('Work'); v.setAnim('serve_idle'); v.face = 'down'; return; }
    if (s.go) { v.goTo(s.go[0], s.go[1]); v.setState('Walking'); v.setAnim('walk'); } else { v.act = Object.assign({ t: 0, fx: false }, s); v.setState('Interacting'); v.face = s.face || 'up'; v.setAnim(s.act); }
  }
  tick(v, dt) {
    const w = this.w;
    if (v.dialogLia && v.state !== 'Serving') { v.setAnim('serve_give'); v.face = 'down'; return; }
    switch (v.state) {
      case 'Walking': if (!v.stepMove(dt) && v.arrived) this.nextStep(v); break;
      case 'Interacting': { const a = v.act; a.t += dt; if (!a.fx && a.t > a.dur * .5) { a.fx = true; a.efeito && a.efeito(); } if (a.t > a.dur) this.nextStep(v); break; }
      case 'Serving': if (v.path.length) { v.stepMove(dt); if (!v.path.length) v.setAnim('serve_idle'); } else w.service.tickJob(v, dt); if (w.service.job && w.service.job.stage === 'ir' && v.path.length) { v.stepMove(dt); } break;
      default: this.work(v, dt);
    }
    if (v.state === 'Serving' && w.service.job && w.service.job.stage !== 'ir' && v.path.length) { v.path = []; }
  }
  work(v, dt) {
    const w = this.w, S = Sim.Data.dia, c = w.clock;
    if (!this.opened && c.min >= c.at(S.abre)) { this.opened = true; this.abrir(v); return; }
    if (c.min >= 540 && !this.restocked) { this.restocked = true; this.startPlan(v, [{ go: w.pontos.forno }, { act: 'interact_high', dur: 3, face: 'up', efeito: () => { w.service.stock.pao += 12; w.service.stock.cafe += 6; w.bus.emit('reposicao', {}); w.reage('forno', 'aurea', 'forno'); } }, { go: w.pontos.vo_posto }]); return; }
    if (w.service.queue.length) { v.setAnim('serve_idle'); v.face = 'down'; return; }                          // com gente na fila ela não sai do balcão
    this.nextForno -= dt; if (this.nextForno <= 0 && !w.service.job) { this.nextForno = 55 + w.rng() * 25; this.startPlan(v, [{ go: w.pontos.forno }, { act: 'interact_high', dur: 2.4, face: 'up' }, { go: w.pontos.vo_posto }]); return; }
    this.idleT -= dt; if (this.idleT <= 0) { const a = w.rng.pick(['serve_wrap', 'serve_write', 'serve_idle', 'serve_wrap']); v.setAnim(a); this.idleT = 2.2 + w.rng() * 2.4; }
    v.face = 'down'; if (Sim.dist(v, { x: w.pontos.vo_posto[0], y: w.pontos.vo_posto[1] }) > 90 && !v.path.length) v.goTo(w.pontos.vo_posto[0], w.pontos.vo_posto[1]);
  }
  abrir(v) {                                                                            // 07:00: acende o forno e a vela do nicho, e volta ao balcão
    const w = this.w, alt = Sim.Nav.nearestFree(w.pontos.altar[0], w.pontos.altar[1] + 12);
    this.startPlan(v, [{ go: w.pontos.forno }, { act: 'interact_high', dur: 2.6, face: 'up', efeito: () => { w.setObj('forno_aceso', 1); w.bus.emit('forno', {}); } },
      { go: alt }, { act: 'interact_high', dur: 3, face: 'up', efeito: () => { w.setObj('altar_vela', 1); w.bus.emit('vela', {}); w.reage('vela', 'aurea', 'vela'); } }, { go: w.pontos.vo_posto }]);
  }
};
