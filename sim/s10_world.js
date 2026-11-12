// ===== s10_world.js — World: liga todos os sistemas, avança o tempo e guarda/recupera o progresso =====
// O jogo (HTML) só faz três coisas com ele: w.update(dt), w.lia = posição da Lia, e ler o estado para desenhar.
Sim.World = class {
  constructor(o) {
    o = o || {}; this.scene = o.scene; this.hooks = o.hooks || { objs: {} }; this.seed = o.seed || 1991; this.rng = Sim.RNG(this.seed);
    this.persist = Object.assign({ evita: {}, fiado: {}, dia: 1, rel: null, mem: null, kp: null }, o.persist || {});
    this.bus = new Sim.EventSystem(); this.clock = new Sim.WorldClock({ start: o.start != null ? o.start : 420, rate: o.rate || 1, openAt: 420, closeAt: 1140, day: this.persist.dia });
    this.pontos = this.scene.pontos; this.flags = {}; this.timers = []; this.cena = 'interior'; this.carry = null; this.fim = false;
    this.lia = { x: 240, y: 222, face: 'up', seat: null, state: 'idle' };
    this.rel = new Sim.Relations(this.bus, Sim.Data.relacoes); if (this.persist.rel) this.rel.import(this.persist.rel);
    this.mem = new Sim.Memory(this.bus); if (this.persist.mem) this.mem.import(this.persist.mem);
    this.knowledge = new Sim.Knowledge(this); if (this.persist.kp) this.knowledge.import(this.persist.kp);
    this.objectives = new Sim.Objectives(this); for (const ob of Sim.Data.objetivos) this.objectives.check(ob.id);
    this.dialogue = new Sim.Dialogue(this); this.convs = new Sim.Conversations(this); this.service = new Sim.Service(this); this.vo = new Sim.VoCtrl(this);
    this.events = new Sim.Events(this); this.interaction = new Sim.Interaction(this);
    this.service.fiado = JSON.parse(JSON.stringify(this.persist.fiado || {}));
    this.stats = { visitas: 0, servidos: 0, sem_lia: 0, desistencias: 0, esperas: [], conversas: 0, boatos: 0 };
    this.seats = {}; this.seatOcc = {}; this.medidas = { porta: [252, 222], balcao: [176, 199], vitrine: [112, 199] };
    for (const s of this.scene.seats) { const S = Object.assign({}, s), ap = Sim.Nav.approach(S); S.ap = ap; if (ap) { S.ax = ap[0]; S.ay = ap[1]; } this.seats[s.id] = S; }
    this.npcs = {}; for (const id of Object.keys(Sim.Data.pessoas)) { const n = new Sim.NPC(this, id, Sim.Data.pessoas[id]); this.npcs[id] = n; if (!n.isVo) this.agenda(n); }
    this.start = { rel: this.rel.export(), kp: Object.keys(this.knowledge.got).length };
    this.bus.on('conversa_inicio', () => this.stats.conversas++); this.bus.on('boato', () => this.stats.boatos++);
    this.bus.on('conhecimento', () => this.guardar()); this.bus.on('objetivo_concluido', () => this.guardar());
  }
  agenda(n) {                                                                       // NPCSchedule: visitas do dia com folga sorteada (semente)
    n.visitas = n.def.visitas.map(v => ({ at: this.clock.at(v.a) + this.rng.range(-v.jit, v.jit), estadia: v.estadia }));
    for (const k in n.needs) n.needs[k] = Sim.clamp(n.needs[k] + this.rng.range(-.1, .1), 0, 1);
  }
  mobiles() { return Object.values(this.npcs); }
  presente(id) { const n = this.npcs[id]; return !!n && n.loc === 'padaria' && n.state !== 'Away' && !n.isVo || id === 'aurea'; }
  liaPerto(o, r) { return this.cena === 'interior' && Sim.dist(this.lia, o) <= r; }
  obj(id) { return this.hooks.getObj ? this.hooks.getObj(id) : (this.hooks.objs[id] || 0); }
  setObj(id, v) { if (this.hooks.setObj) this.hooks.setObj(id, v); else this.hooks.objs[id] = v; this.bus.emit('estado_objeto', { id, v }); }
  flag(id) { return !!this.flags[id]; }
  needs(n, k, d) { n.needs[k] = Sim.clamp(n.needs[k] + d, 0, 1); }
  setMood(id, m, secs) { const n = this.npcs[id]; if (!n) return; n.mood = m; n.moodT = secs || 60; this.bus.emit('humor', { id, m }); }
  reage(tipo, id, ev, outro) { const t = (Sim.Data.reacoes[tipo] || {})[id]; const n = this.npcs[id]; if (t && n && (n.loc === 'padaria' || id === 'aurea') && n.state !== 'Away') this.dialogue.speak(n, t); }
  update(dt) {
    if (this.fim && this.clock.ended) { return; }
    dt = Math.min(dt, .25); this.bus.t += dt; this.clock.tick(dt);
    for (const t of this.timers.slice()) { t.t -= dt; if (t.t <= 0) { this.timers.splice(this.timers.indexOf(t), 1); t.fn(); } }
    this.events.update(dt);
    for (const n of this.mobiles()) n.tick(dt);
    this.service.update(dt); this.convs.update(dt);
  }
  step(secs, dt) { dt = dt || .1; for (let t = 0; t < secs; t += dt) this.update(dt); }
  endDay() {
    this.clock.ended = true; this.fim = true; const st = this.stats, esp = st.esperas;
    for (const n of this.mobiles()) { if (n.isVo) continue; if (n.seat) { this.seatOcc[n.seat.id] = null; } }
    const ant = this.start.rel, mud = [];
    for (const k in this.rel.m) { const a = ant[k], b = this.rel.m[k]; if (!a) continue; const d = (b.trust - a.trust) + (b.aff - a.aff); if (Math.abs(d) >= .04) mud.push({ par: k, aff: +(b.aff - a.aff).toFixed(2), trust: +(b.trust - a.trust).toFixed(2) }); }
    const r = { dia: this.clock.day, servidos: st.servidos, desistencias: st.desistencias, espera_media: esp.length ? Math.round(esp.reduce((a, b) => a + b, 0) / esp.length) : 0, atendeu_com_lia_fora: st.sem_lia,
      fiado: Object.entries(this.service.fiado).map(([k, v]) => ({ id: k, n: v.n, valor: +v.valor.toFixed(2) })), caixa: +this.service.caixa.toFixed(2), conversas: st.conversas, boatos: st.boatos,
      pontos_novos: Object.keys(this.knowledge.got).length - this.start.kp, pontos: Object.keys(this.knowledge.got).length, objetivos: this.objectives.list().map(o => ({ id: o.id, titulo: o.titulo, n: o.n, meta: o.meta, feito: o.feito })), mudancas: mud };
    this.persist.dia = this.clock.day + 1; this.guardar(true); this.bus.emit('dia_fim', { resumo: r }); return r;
  }
  guardar(fim) { this.persist.rel = this.rel.export(); this.persist.mem = this.mem.export(); this.persist.kp = this.knowledge.export(); this.persist.fiado = JSON.parse(JSON.stringify(this.service.fiado)); if (this.hooks.save) this.hooks.save(this.persist, !!fim); }
};
// armazenamento do progresso (conhecimento, relações, memória, fiado, dia). Protegido: sem localStorage ou com ?new=1 começa do zero.
Sim.Save = {
  key: 'balcao_etapa4_v1',
  load() { try { const s = (typeof localStorage !== 'undefined') && localStorage.getItem(this.key); return s ? JSON.parse(s) : null; } catch (e) { return null; } },
  save(p) { try { if (typeof localStorage !== 'undefined') localStorage.setItem(this.key, JSON.stringify(p)); } catch (e) { } },
  clear() { try { if (typeof localStorage !== 'undefined') localStorage.removeItem(this.key); } catch (e) { } }
};
