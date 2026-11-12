// ===== mundo.js — Etapa 7: o mundo integrado (rua · padaria · casa) =====
// DOM-free. Liga os três mundos JÁ APROVADOS sem reconstruí-los. Cada ambiente continua dono da sua simulação, câmera, colisão e interação
// (rua: s15_rua.js · padaria: s10_world.js · casa: s12_casa.js). Este módulo acrescenta só o que faltava entre eles:
//   WorldManager ............ dono do conjunto: relógio mestre, passo dos ambientes inativos, estado da Lia
//   SceneManager ............ registro dos ambientes, qual está ativo, perspectiva de cada um
//   DoorSystem .............. portas funcionais (destino, chegada, estado de acesso) — Lia só passa por elas
//   SceneTransitionSystem ... fade de saída → troca de ambiente/perspectiva → fade de entrada
//   NPCTravelSystem ......... quem sai de um ambiente aparece no outro, pela porta certa, sem teletransporte
//   WorldStateManager ....... confiança e conhecimento compartilhados; EnvironmentPersistence guarda o resumo de cada ambiente
// Adaptadores (Adapters.*) escondem as diferenças dos três mundos. Em Node recebem o `Sim` de um contexto próprio; no navegador, o do iframe.
(function (root) {
  'use strict';
  const M = {};

  // ------------------------------------------------------------------ dados
  M.CENAS = {
    rua: { nome: 'Rua', persp: 'side-view' },
    padaria: { nome: 'Padaria de Vó Aurea', persp: 'três-quartos' },
    casa: { nome: 'Casa de Seu Raimundo', persp: 'três-quartos' },
    quintal: { nome: 'Quintal de Dona Zefa', persp: 'três-quartos' },
  };
  // portas funcionais. `chegada` = onde a Lia aparece no destino. Estado de acesso vem de `acesso()` do DoorSystem.
  M.PORTAS = [
    { id: 'rua:porta_padaria', de: 'rua', para: 'padaria', chegada: 'entrada', texto: 'Entrar na padaria' },
    { id: 'rua:porta_sobrado', de: 'rua', para: 'casa', chegada: 'entrada', texto: 'Entrar na casa de Seu Raimundo' },
    { id: 'padaria:porta', de: 'padaria', para: 'rua', chegada: 'porta_padaria', texto: 'Sair para a rua' },
    { id: 'casa:porta', de: 'casa', para: 'rua', chegada: 'porta_sobrado', texto: 'Descer para a rua' },
    { id: 'rua:porta_lateral', de: 'rua', para: 'quintal', chegada: 'soleira', texto: 'Entrar no quintal de Dona Zefa' },
    { id: 'quintal:porta', de: 'quintal', para: 'rua', chegada: 'porta_lateral', texto: 'Sair para a rua' },
  ];
  // quem viaja entre ambientes (os demais moradores só existem em um ambiente)
  M.VIAJANTES = { raimundo: ['rua', 'padaria', 'casa'], dandara: ['rua', 'padaria'], lucia: ['rua', 'padaria'] };

  // ------------------------------------------------------------------ SceneManager
  class SceneManager {
    constructor() { this.cenas = {}; this.atual = null; }
    registrar(id, adapter) { this.cenas[id] = adapter; adapter.cenaId = id; }
    get(id) { return this.cenas[id]; }
    ids() { return Object.keys(this.cenas); }
    inativas() { return this.ids().filter(i => i !== this.atual).map(i => this.cenas[i]); }
    persp(id) { return M.CENAS[id].persp; }
  }

  // ------------------------------------------------------------------ DoorSystem
  class DoorSystem {
    constructor(w) { this.w = w; this.portas = M.PORTAS.map(p => Object.assign({}, p)); this.usos = 0; }
    porta(id) { return this.portas.find(p => p.id === id) || null; }
    daCena(cena) { return this.portas.filter(p => p.de === cena); }
    // estado de acesso: { ok, motivo }
    acesso(p) {
      const dest = this.w.cenas.get(p.para); if (!dest) return { ok: false, motivo: 'sem destino' };
      // a padaria é da família da Lia: ela entra a qualquer hora (o horário só vale para a freguesia)
      return { ok: true };
    }
    // pedido de passagem: só vale se a Lia está no ambiente de origem e a porta está aberta
    pedir(id) {
      const p = this.porta(id); if (!p) return { ok: false, motivo: 'porta desconhecida' };
      if (this.w.cenas.atual !== p.de) return { ok: false, motivo: 'a Lia não está neste ambiente' };
      if (this.w.trans.ativa) return { ok: false, motivo: 'em transição' };
      const a = this.acesso(p); if (!a.ok) return a;
      this.usos++; this.w.trans.iniciar(p); return { ok: true, porta: p };
    }
  }

  // ------------------------------------------------------------------ SceneTransitionSystem
  // fases: saindo (fade para preto) → troca (no ponto escuro: some um ambiente, aparece o outro, a Lia é posicionada) → entrando (fade de volta)
  class SceneTransitionSystem {
    constructor(w) { this.w = w; this.ativa = null; this.alpha = 0; this.dur = .45; this.log = []; }
    iniciar(porta) { this.ativa = { porta, fase: 'saindo', t: 0 }; this.w.emit('transicao_inicio', { porta: porta.id }); }
    update(dt) {
      const a = this.ativa; if (!a) return; a.t += dt;
      if (a.fase === 'saindo') { this.alpha = Math.min(1, a.t / this.dur); if (a.t >= this.dur) { this.trocar(a.porta); a.fase = 'entrando'; a.t = 0; } }
      else { this.alpha = Math.max(0, 1 - a.t / this.dur); if (a.t >= this.dur) { this.alpha = 0; this.w.emit('transicao_fim', { porta: a.porta.id }); this.ativa = null; } }
    }
    trocar(p) {
      const w = this.w, de = w.cenas.get(p.de), para = w.cenas.get(p.para);
      w.estado.sincronizar(de, para);                       // confiança / conhecimento acompanham a Lia
      de.liaSai(p); w.cenas.atual = p.para; para.liaChega(p);
      this.log.push({ de: p.de, para: p.para, min: Math.round(w.minuto() * 10) / 10, persp: M.CENAS[p.para].persp });
      w.emit('cena', { de: p.de, para: p.para, persp: M.CENAS[p.para].persp });
    }
  }

  // ------------------------------------------------------------------ NPCTravelSystem
  // Cada mudança de ambiente de um morador é um evento visível no ambiente de origem (sai pela porta) e no de destino (entra pela porta).
  class NPCTravelSystem {
    constructor(w) {
      this.w = w; this.onde = {}; this.viagens = [];
      for (const id in M.VIAJANTES) this.onde[id] = id === 'raimundo' ? 'casa' : 'rua';
      const C = w.cenas;
      // rua → padaria / casa (o morador entrou pela porta na rua)
      C.get('rua').sim.bus.on('porta', e => {
        if (e.saiu || !(e.id in M.VIAJANTES)) return;
        if (e.porta === 'porta_padaria') this.ir(e.id, 'rua', 'padaria', () => C.get('padaria').receber(e.id, C.get('rua').visita(e.id)));
        else if (e.porta === 'porta_sobrado' && e.id === 'raimundo') this.ir(e.id, 'rua', 'casa', () => C.get('casa').receberVolta());
      });
      // padaria → rua
      C.get('padaria').sim.bus.on('saiu', e => { if (e.id in M.VIAJANTES && this.onde[e.id] === 'padaria') this.ir(e.id, 'padaria', 'rua', () => C.get('rua').sim.liberar(e.id, 'padaria')); });
      // casa → rua
      C.get('casa').sim.bus.on('saiu_casa', e => { if (this.onde[e.id] === 'casa') this.ir(e.id, 'casa', 'rua', () => C.get('rua').sim.liberar(e.id, 'casa')); });
    }
    ir(id, de, para, fn) { this.onde[id] = para; this.viagens.push({ id, de, para, min: Math.round(this.w.minuto() * 10) / 10 }); fn(); this.w.emit('viagem', { id, de, para }); }
    // invariante: ninguém existe em dois ambientes ao mesmo tempo
    visiveis() {
      const out = {}, C = this.w.cenas;
      for (const id in M.VIAJANTES) {
        out[id] = [];
        const r = C.get('rua').sim.npcs[id]; if (r && r.state !== 'Away' && r.state !== 'Entering' && r.state !== 'Exiting') out[id].push('rua');   // Entering/Exiting = fade de meio segundo na porta, a passagem em si
        const p = C.get('padaria').sim.npcs[id]; if (p && p.state !== 'Away' && p.loc === 'padaria') out[id].push('padaria');
        const c = C.get('casa').sim.npcs[id]; if (c && c.state !== 'Away' && c.loc === 'casa') out[id].push('casa');
      }
      return out;
    }
    duplicados() { const v = this.visiveis(); return Object.keys(v).filter(id => v[id].length > 1).map(id => id + ':' + v[id].join('+')); }
  }

  // ------------------------------------------------------------------ WorldStateManager + EnvironmentPersistence
  class WorldStateManager {
    constructor(w) { this.w = w; this.resumo = {}; }
    // confiança em Lia (rua usa 0..1 por morador; padaria/casa usam relações "x>lia"): mantém o MAIOR valor nos dois lados
    sincronizar(de, para) {
      const rua = this.w.cenas.get('rua'), pad = this.w.cenas.get('padaria'), casa = this.w.cenas.get('casa');
      for (const id in M.VIAJANTES) {
        const a = rua.sim.trust[id] || 0, b = pad.sim.rel.get(id, 'lia').trust, c = casa.sim.rel.get(id, 'lia').trust, m = Math.max(a, b, c);
        rua.sim.trust[id] = m; pad.sim.rel.get(id, 'lia').trust = m; casa.sim.rel.get(id, 'lia').trust = m;
      }
      // vivências (o que a Lia já viu/ouviu) valem em todos os ambientes: servem de motivo para puxar assunto
      { const u = {}; for (const x of [rua.sim.viv, casa.sim.viv, pad.sim.viv]) if (x) for (const k in x) if (x[k]) u[k] = 1;
        for (const x of [rua.sim, casa.sim, pad.sim]) { x.viv = x.viv || {}; for (const k in u) x.viv[k] = x.viv[k] || (typeof x.viv[k] === 'number' ? x.viv[k] : 1); } }
      // relações, memória e conhecimento da padaria e da casa são o mesmo mundo: quem a Lia acabou de deixar vale mais
      if (de.cenaId !== 'rua' && para.cenaId !== 'rua') { /* não há porta direta entre os dois */ }
      const fonte = de.cenaId === 'padaria' ? pad : de.cenaId === 'casa' ? casa : null, alvo = fonte === pad ? casa : fonte === casa ? pad : null;
      if (fonte && alvo) { alvo.sim.rel.import(fonte.sim.rel.export()); alvo.sim.mem.import(JSON.parse(JSON.stringify(fonte.sim.mem.export()))); alvo.sim.knowledge.import(fonte.sim.knowledge.export()); }
      else if (para.cenaId === 'padaria' || para.cenaId === 'casa') { /* entrando num interior vindo da rua: os dois interiores já foram igualados na saída do outro */ const o = para === pad ? casa : pad; if (o) { para.sim.knowledge.import(Object.assign({}, para.sim.knowledge.export(), o.sim.knowledge.export())); } }
      this.guardar();
    }
    guardar() { const w = this.w; this.resumo = { min: w.minuto(), cena: w.cenas.atual, trust: Object.assign({}, w.cenas.get('rua').sim.trust), onde: Object.assign({}, w.viagens.onde) }; }
  }
  // cada ambiente permanece vivo (nada é reinicializado ao entrar); isto só devolve um instantâneo legível para testes e para o relatório
  class EnvironmentPersistence {
    constructor(w) { this.w = w; }
    instantaneo() {
      const C = this.w.cenas, r = C.get('rua').sim, p = C.get('padaria').sim, c = C.get('casa').sim;
      return {
        rua: { mesa: r.mesa.fase, placar: r.mesa.game.placar.slice(), assentos: Object.fromEntries(Object.entries(r.assentos).filter(([k, a]) => a.ocup).map(([k, a]) => [k, a.ocup])), kp: Object.keys(r.kp).length },
        padaria: { servidos: p.stats.servidos, fila: p.service.queue.length, presentes: Object.values(p.npcs).filter(n => !n.isVo && n.state !== 'Away').map(n => n.id), aurea: p.npcs.aurea.state },
        casa: { raimundo: c.npcs.raimundo.state, loc: c.npcs.raimundo.loc, atividades: c.stats.atividades },
      };
    }
  }

  // ------------------------------------------------------------------ WorldManager
  class WorldManager {
    constructor() {
      this.cenas = new SceneManager(); this.portas = new DoorSystem(this); this.trans = new SceneTransitionSystem(this); this.estado = new WorldStateManager(this);
      this.ouvintes = []; this.t = 0; this.sinc = 0; this.viagens = null; this.persist = new EnvironmentPersistence(this);
    }
    iniciar(atual) { this.viagens = new NPCTravelSystem(this); this.cenas.atual = atual; this.ajustarRelogios(); }
    on(fn) { this.ouvintes.push(fn); } emit(tipo, d) { for (const f of this.ouvintes) f(tipo, d); }
    minuto() { return this.cenas.get(this.cenas.atual).sim.clock.min; }
    // relógio mestre = o do ambiente ativo; os outros recebem o mesmo minuto (nunca andam para trás)
    ajustarRelogios() { const m = this.minuto(); for (const c of this.cenas.inativas()) if (c.sim.clock.min < m) c.sim.clock.min = m; }
    // passo do mundo: o ambiente ativo roda no laço do próprio jogo (rAF); os outros rodam aqui, simplificados só na parte visual
    update(dt, opt) {
      this.t += dt; this.trans.update(dt);
      for (const c of (opt && opt.todos ? this.cenas.ids().map(i => this.cenas.get(i)) : this.cenas.inativas())) c.step(dt);
      this.sinc += dt; if (this.sinc >= 1) { this.sinc = 0; this.ajustarRelogios(); }
    }
    // avança `seg` segundos de relógio real simulando TODOS os ambientes (testes e avanço rápido)
    passos(seg, dt) { dt = dt || .1; for (let t = 0; t < seg; t += dt) this.update(dt, { todos: true }); }
    avancarAte(min, dt) { dt = dt || .1; let g = 0; while (this.minuto() < min && g++ < 200000) this.update(dt, { todos: true }); }
    ir(portaId) { return this.portas.pedir(portaId); }
  }
  M.WorldManager = WorldManager; M.SceneManager = SceneManager; M.DoorSystem = DoorSystem; M.SceneTransitionSystem = SceneTransitionSystem; M.NPCTravelSystem = NPCTravelSystem; M.WorldStateManager = WorldStateManager;

  // ------------------------------------------------------------------ adaptadores (um por ambiente)
  // ui = ponte opcional com a tela do ambiente (no navegador: o iframe). Sem ui (testes) só a posição da Lia na simulação é ajustada.
  M.Adapters = {
    rua(Sim, sim, ui) {
      return {
        sim, ui, step(dt) { sim.update(dt); }, visita(id) { return Sim.Rua.D.visitas[id] || [10, 15]; },
        liaSai(p) { sim.liaFora = true; ui && ui.liaSaiu && ui.liaSaiu(); },
        liaChega(p) { const sp = sim.spot(p.chegada); sim.lia.x = sp.x; sim.lia.y = sp.y + 7; sim.lia.face = 'down'; sim.liaFora = false; ui && ui.liaChega && ui.liaChega(p.chegada); },
      };
    },
    padaria(Sim, sim, ui) {
      for (const id in M.VIAJANTES) if (sim.npcs[id]) sim.npcs[id].visitas = [];               // as visitas agora vêm da rua
      if (root && root.MUNDO_ANO === 1994) sim.caruruSaida = 735;                                // 12:15: a vó vai ao caruru e deixa o balcão com a Lia
      return {
        sim, ui, step(dt) { sim.update(dt); },
        receber(id, est) { const n = sim.npcs[id]; if (!n || n.isVo) return false; n.visitas = [{ at: sim.clock.min, estadia: est }]; n.vi = 0; if (sim.persist.evita) sim.persist.evita[id] = 0; return true; },
        liaSai() { ui && ui.liaSaiu && ui.liaSaiu(); }, liaChega() { sim.cena = 'interior'; sim.lia.x = 240; sim.lia.y = 222; ui && ui.liaChega && ui.liaChega(); },
      };
    },
    casa(Sim, sim, ui) {
      const R = sim.npcs.raimundo; R.sai = 423; R.volta = 630; sim.mundoAguarda = true; sim.mundoLibera = false;   // sai às 07:03 e só volta quando a rua entregar (volta=630 só alimenta o texto)
      sim.bus.on('saiu_casa', () => { sim.mundoLibera = false; });   // saiu de novo: a casa espera a rua entregar
      const orig = Sim.HomeStates.Away; Sim.HomeStates.Away = function (n, w, dt) { if (w.mundoAguarda && !w.mundoLibera) return; return orig.call(this, n, w, dt); };
      return {
        sim, ui, step(dt) { sim.update(dt); },
        receberVolta() {   // volta da manhã (~10:00). À tarde ele sai de novo: 15:00 para o dominó (1991) ou 12:45 para o caruru (1994)
          sim.mundoLibera = true; R.volta = sim.clock.min; const so = (root && root.MUNDO_ANO === 1994) ? 765 : 900; R.ses.saiu = sim.clock.min >= so; R.sai = so;
        },
        liaSai() { ui && ui.liaSaiu && ui.liaSaiu(); }, liaChega() { sim.lia.x = 240; sim.lia.y = 222; ui && ui.liaChega && ui.liaChega(); },
      };
    },
  };
  M.Adapters.quintal = function (Sim, sim, ui) {
    return { sim, ui, step(dt) { sim.update(dt); }, liaSai() { ui && ui.liaSaiu && ui.liaSaiu(); }, liaChega() { ui && ui.liaChega && ui.liaChega(); } };
  };
  M.criar = function (cenas, atual) { const w = new WorldManager(); for (const k in cenas) w.cenas.registrar(k, cenas[k]); w.iniciar(atual || 'rua'); return w; };

  if (typeof module !== 'undefined' && module.exports) module.exports = M; else root.Mundo = M;
})(typeof window !== 'undefined' ? window : globalThis);
