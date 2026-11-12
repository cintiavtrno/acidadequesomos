// ===== s8_events.js — EventSystem de acontecimentos (por hora ou por condição) + conhecimento, objetivos e Caderninho =====
// Um evento acontece uma vez; ele só lê e escreve variáveis do mundo (relações, humor, memória), nunca o desenho.
Sim.Events = class {
  constructor(w) {
    this.w = w; this.done = {};
    this.defs = [
      { id: 'radio', hora: 550, run: w => {                                          // 09:10 — o rádio da vó anuncia o Programa
        w.flags.radio_tocou = true; w.bus.emit('radio', {});
        let k = 0; for (const id of ['raimundo', 'dandara', 'lucia']) { const n = w.npcs[id]; if (!n || n.loc !== 'padaria' || n.state === 'Away') continue; const m = { raimundo: 'preocupado', dandara: 'irritada', lucia: 'constrangida' }[id]; w.setMood(id, m, 110); setTimeout0(w, k++ * 1.4, () => w.reage('radio', id, null)); }
        setTimeout0(w, k * 1.4 + .5, () => w.reage('radio', 'aurea', null));
        if (w.cena === 'interior' && Sim.dist(w.lia, { x: w.pontos.radio[0], y: w.pontos.radio[1] }) < 150) w.knowledge.award('kp_radio', { via: 'ouvida' }); else w.bus.emit('perdeu', { o: 'radio' });
        w.rel.change('dandara', 'lucia', { aff: -.03, tens: .08 }, 'radio');
      } },
      { id: 'procura', cond: w => this.procura(w) },
      { id: 'dia_fim', hora: 1140, run: w => w.endDay() },
    ];
  }
  procura(w) {                                                                        // "alguém procura outro": quem ficou sente falta de quem já saiu
    for (const x of ['raimundo', 'dandara', 'lucia']) { const X = w.npcs[x]; if (!X || X.loc !== 'padaria' || X.state !== 'Sitting' || X.ses.procurou) continue;
      for (const y of ['raimundo', 'dandara', 'lucia']) { const Y = w.npcs[y]; if (y === x || !Y || !Y.ses.saiu || Y.loc !== 'rua' || w.rel.get(x, y).aff < .2 || w.mem.has(x, 'procurou_' + y)) continue;
        X.ses.procurou = true; w.mem.remember(x, 'procurou_' + y); w.dialogue.speak(X, { raimundo: 'Dandara já passou por aqui?', dandara: 'Seu Raimundo já veio e foi, né?', lucia: 'A senhora viu Seu Raimundo hoje?' }[x]); w.bus.emit('procura', { quem: x, procura: y });
        setTimeout0(w, 3.2, () => { const vo = w.npcs.aurea; w.dialogue.speak(vo, Y.ses.gaveUp ? 'Foi embora sem esperar, coitada.' : 'Veio, foi. Quem tem pressa não senta.'); }); return true; } }
    return false;
  }
  update(dt) {
    const w = this.w; this.tc = (this.tc || 0) - dt;
    for (const e of this.defs) {
      if (e.hora != null) { if (!this.done[e.id] && w.clock.min >= e.hora) { this.done[e.id] = true; e.run(w); } }
      else if (this.tc <= 0) e.cond(w);                                              // condicionais: repetíveis, checadas a cada 2 s
    }
    if (this.tc <= 0) this.tc = 2;
  }
};
function setTimeout0(w, secs, fn) { w.timers.push({ t: secs, fn }); }                // temporizador de simulação (pausa junto com o jogo)

// Conhecimento: cada ponto é um fato que Lia entendeu, por conversa, observação ou objeto. Vai para o Caderninho.
Sim.Knowledge = class {
  constructor(w) { this.w = w; this.got = {}; }
  has(id) { return !!this.got[id]; }
  award(id, o) {
    if (this.got[id]) return false; const kp = Sim.Data.conhecimentos.find(k => k.id === id); if (!kp) return false;
    this.got[id] = Object.assign({ t: this.w.clock.min, dia: this.w.clock.day }, o || {}); const ob = this.w.objectives;
    this.w.bus.emit('conhecimento', { id, kp, via: (o || {}).via }); ob.check(kp.obj); return true;
  }
  count(quem) { return Sim.Data.conhecimentos.filter(k => k.quem === quem && this.got[k.id]).length; }
  export() { return JSON.parse(JSON.stringify(this.got)); }
  import(o) { this.got = o || {}; }
};
Sim.Objectives = class {
  constructor(w) { this.w = w; this.done = {}; }
  list() { return Sim.Data.objetivos.map(o => { const n = this.n(o.id); return Object.assign({}, o, { n, feito: !!this.done[o.id] || n >= o.meta, total: Sim.Data.conhecimentos.filter(k => k.obj === o.id).length }); }); }
  n(id) { return Sim.Data.conhecimentos.filter(k => k.obj === id && this.w.knowledge.has(k.id)).length; }
  check(id) { if (!id) return; const o = Sim.Data.objetivos.find(x => x.id === id); if (!o || this.done[id]) return; if (this.n(id) >= o.meta) { this.done[id] = true; this.w.bus.emit('objetivo_concluido', { id, o }); } }
};
// Caderninho: páginas por pessoa (nível, pontos, entradas) + lugares + objetivos. Construído a partir do conhecimento e das relações.
Sim.Diary = {
  pages(w) {
    const nivelDe = n => { let r = Sim.Data.nivelPessoa[0][1]; for (const [m, t] of Sim.Data.nivelPessoa) if (n >= m) r = t; return r; };
    const pess = ['raimundo', 'dandara', 'lucia', 'aurea'].map(id => { const P = Sim.Data.pessoas[id], pts = w.knowledge.count(id), ent = Sim.Data.conhecimentos.filter(k => k.quem === id && w.knowledge.has(k.id));
      return { id, nome: P.nome, papel: P.papel, pontos: pts, de: Sim.Data.conhecimentos.filter(k => k.quem === id).length, nivel: nivelDe(pts), confianca: w.rel.nivel(id, 'lia'), trust: w.rel.get(id, 'lia').trust, entradas: ent.map(k => ({ id: k.id, titulo: k.titulo, texto: k.texto, revisar: !!k.revisar })) }; });
    const lug = Sim.Data.conhecimentos.filter(k => k.quem === 'lugar' && w.knowledge.has(k.id)).map(k => ({ id: k.id, titulo: k.titulo, texto: k.texto, revisar: !!k.revisar }));
    return { pessoas: pess, lugares: lug, lugaresTotal: Sim.Data.conhecimentos.filter(k => k.quem === 'lugar').length, objetivos: w.objectives.list(), pontos: Object.keys(w.knowledge.got).length, total: Sim.Data.conhecimentos.length };
  }
};
