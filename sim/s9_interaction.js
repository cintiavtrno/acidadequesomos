// ===== s9_interaction.js — InteractionSystem: o que Lia pode fazer com pessoas e objetos (Ouvir · Perguntar · Ajudar · Pressionar · examinar) =====
// Só lógica: devolve falas, efeitos e pontos de conhecimento. A interface mostra; o jogo move a Lia.
Sim.Interaction = class {
  constructor(w) { this.w = w; }
  rotulos() { return {
    rua: 'Como anda a rua?', casa: 'E a sua casa?', caderneta: 'E a caderneta?', programa: 'O que é esse Programa?', papel: 'Tem algum papel por aí?', caderno: 'O que é esse caderno?', mae: 'Como vai sua mãe?', lucia: 'O que acha da moça da prancheta?',
    prancheta: 'O que a senhora anota aí?', raimundo: 'Conhece Seu Raimundo?', altar: 'O nicho de São Jorge...', gaveta: 'O que a senhora guarda na gaveta?', agua: 'Oferecer um copo d\'água', vez: 'Pedir a vez para ela', trena: 'Segurar a trena', sovar: 'Ajudar a sovar a massa' }; }
  topicos(id) { const w = this.w; return { raimundo: ['rua', 'casa', 'caderneta', 'programa', 'papel'], dandara: ['rua', 'programa', 'caderno', 'mae', 'lucia'], lucia: ['programa', 'rua', 'prancheta'].concat(w.mem.has('lucia', 'viu_fiado') ? ['raimundo'] : []), aurea: ['rua', 'caderneta', 'altar', 'gaveta', 'casa'] }[id] || []; }
  ajudas(id) {
    const w = this.w, n = w.npcs[id], r = [];
    if (id === 'raimundo') r.push({ id: 'agua', ok: w.carry === 'copo', motivo: 'Precisa de um copo d\'água. O filtro de barro fica perto da porta.' });
    if (id === 'dandara') { const q = w.service.queue, i = q.indexOf('dandara'); r.push({ id: 'vez', ok: i > 0 && !(w.service.job && w.service.job.cust === q[i - 1]), motivo: i < 0 ? 'Ela não está na fila.' : 'Ela já é a próxima.' }); }
    if (id === 'lucia') r.push({ id: 'trena', ok: n.state === 'Measuring' && !!n.ses.medindo, motivo: 'Ela só precisa de ajuda quando está medindo.' });
    if (id === 'aurea') r.push({ id: 'sovar', ok: !w.service.queue.length && !w.service.job && n.state === 'Work', motivo: 'Tem gente na fila; a vó não larga o balcão.' });
    return r;
  }
  saudar(id) { const w = this.w, c = w.dialogue.ctx(id, { presente: null }); const f = w.dialogue.line(id, 'saudar', c); return f ? f.texto : '...'; }
  abrir(id) { const n = this.w.npcs[id]; n.dialogLia = true; this.w.bus.emit('dialogo', { id }); const d = Sim.dir8(this.w.lia.x - n.x, this.w.lia.y - n.y); if (d && n.state !== 'Sitting') n.face = d; return { saudacao: this.saudar(id), topicos: this.topicos(id), ajudas: this.ajudas(id), pressionar: id === 'aurea' }; }
  fechar(id) { const n = this.w.npcs[id]; if (n) n.dialogLia = false; }
  aplicar(verbo, id, arg) {
    const w = this.w, n = w.npcs[id], R = w.rel, L = [], rot = this.rotulos(), c = () => w.dialogue.ctx(id, {}), say = (f) => f && L.push({ quem: id, texto: f.texto, revisar: f.revisar });
    if (verbo === 'ouvir') {
      L.push({ quem: 'nota', texto: 'Você fica em silêncio e escuta.' }); const f = w.dialogue.line(id, 'ouvir', c()); say(f);
      R.change(id, 'lia', { trust: .012 }, 'ouviu');
      if (id === 'raimundo' && n.state === 'Praying') w.knowledge.award('kp_raimundo_reza', { via: 'observou' });
      if (id === 'raimundo' && (n.ses.fiadoDito || ['Waiting', 'Ordering'].includes(n.state))) w.knowledge.award('kp_raimundo_fiado', { via: 'ouviu' });
      if (id === 'lucia') w.knowledge.award('kp_lucia_ouvir', { via: 'ouviu' });
      if (id === 'dandara' && n.zona() === 'fila') w.knowledge.award('kp_dandara_ata', { via: 'observou' });
    } else if (verbo === 'perguntar') {
      L.push({ quem: 'lia', texto: rot[arg] }); const f = w.dialogue.line(id, 'perguntar', c(), arg); say(f); R.change(id, 'lia', { trust: .01 }, 'perguntou:' + arg);
      const nv = R.nivel(id, 'lia'), K = { 'raimundo.caderneta': 'kp_raimundo_sexta', 'raimundo.casa': 'kp_raimundo_casa', 'dandara.programa': 'kp_dandara_programa', 'dandara.caderno': 'kp_dandara_ata', 'dandara.mae': 'kp_dandara_mae', 'lucia.programa': 'kp_lucia_programa', 'lucia.raimundo': 'kp_lucia_fiado', 'aurea.caderneta': 'kp_vo_fiado', 'aurea.altar': 'kp_vo_altar' }[id + '.' + arg];
      if (K) w.knowledge.award(K, { via: 'perguntou' }); if (id === 'dandara' && arg === 'caderno' && nv >= 1) w.knowledge.award('kp_dandara_freira', { via: 'perguntou' }); if (id === 'lucia' && arg === 'prancheta' && nv >= 1) w.knowledge.award('kp_lucia_prancheta', { via: 'perguntou' });
      if (id === 'raimundo' && arg === 'papel') w.mem.remember('raimundo', 'lia_perguntou_papel');
      if (id === 'lucia' && arg === 'programa') w.mem.remember('lucia', 'lia_perguntou_programa');
    } else if (verbo === 'ajudar') {
      const a = this.ajudas(id).find(x => x.id === arg); L.push({ quem: 'lia', texto: rot[arg] }); if (!a || !a.ok) { L.push({ quem: 'nota', texto: a ? a.motivo : '...' }); return { linhas: L }; }
      if (arg === 'agua') { w.carry = null; say(w.dialogue.line('raimundo', 'ajudar', c(), 'agua')); R.change('raimundo', 'lia', { trust: .14, aff: .08 }, 'agua'); w.mem.remember('raimundo', 'lia_ajudou_agua', { publico: true }); w.knowledge.award('kp_raimundo_agua', { via: 'ajudou' }); w.needs(n, 'cansaco', -.1); }
      if (arg === 'vez') {
        const q = w.service.queue, i = q.indexOf('dandara'), ant = q[i - 1], N = w.npcs[ant]; if (w.service.cedeVez(ant, 'dandara')) {
          say(w.dialogue.line('dandara', 'ajudar', c(), 'vez')); R.change('dandara', 'lia', { trust: .13, aff: .1 }, 'vez'); w.mem.remember('dandara', 'lia_deu_vez', { publico: true }); w.knowledge.award('kp_dandara_vez', { via: 'ajudou' });
          const rx = Sim.Data.reacoes.furada[ant]; if (rx) w.dialogue.speak(N, rx);
          if (ant === 'lucia') { R.change('lucia', 'lia', { trust: -.04, aff: -.05 }, 'furou_fila'); w.mem.remember('lucia', 'lia_furou_fila', { publico: true }); w.setMood('lucia', 'constrangida', 60); }
          else R.change(ant, 'lia', { trust: .02 }, 'cedeu_vez'); w.bus.emit('furou_fila', { quem: 'dandara', passou: ant });
        }
      }
      if (arg === 'trena') { say(w.dialogue.line('lucia', 'ajudar', c(), 'trena')); R.change('lucia', 'lia', { trust: .13, aff: .1 }, 'trena'); w.mem.remember('lucia', 'lia_trena', { publico: true }); w.knowledge.award('kp_lucia_trena', { via: 'ajudou' }); n.ses.mediuExtra = true; }
      if (arg === 'sovar') { say(w.dialogue.line('aurea', 'ajudar', c(), 'sovar')); R.change('aurea', 'lia', { trust: .05, aff: .03 }, 'sovou'); w.knowledge.award('kp_vo_ajuda', { via: 'ajudou' }); w.bus.emit('sovou', {}); }
    } else if (verbo === 'pressionar' && id === 'aurea') {
      L.push({ quem: 'lia', texto: 'Vó, eu sei que tem algo na gaveta.' }); const first = !w.flags.lia_pressionou; say(w.dialogue.line('aurea', 'pressionar', c(), 'gaveta'));
      if (first) { w.flags.lia_pressionou = true; R.change('aurea', 'lia', { trust: -.05 }, 'pressionou'); w.mem.remember('aurea', 'lia_pressionou'); }
      else { w.knowledge.award('kp_vo_proposta', { via: 'pressionou' }); R.change('aurea', 'lia', { trust: -.03 }, 'pressionou2'); }
      w.bus.emit('pressionou', { vez: first ? 1 : 2 });
    }
    return { linhas: L };
  }
  // objetos: examinar / usar / alternar. Devolve texto e efeitos; o jogo faz o gesto e mostra.
  objeto(o, ctx) {
    const w = this.w, D = Sim.Data.objetos[o.id], r = { texto: D ? D.texto(w, ctx || {}) : (o.desc || o.title || ''), kp: null };
    if (o.id === 'aparador') { w.carry = 'copo'; r.texto = 'Você enche um copo com a água do filtro de barro. Fresquinha.'; }
    if (o.id === 'gaveta_1') { const perto = !!w.npcs.aurea && w.npcs.aurea.state !== 'Away' && Sim.dist(w.lia, w.npcs.aurea) < 90; r.texto = D.texto(w, { vo_longe: !perto }); if (perto) { w.dialogue.speak(w.npcs.aurea, 'Aí não, minha filha.'); w.mem.remember('aurea', 'lia_xeretou_gaveta'); w.rel.change('aurea', 'lia', { trust: -.03 }, 'xeretou_gaveta'); return r; } }
    if (D && D.kp) { r.kp = D.kp; w.knowledge.award(D.kp, { via: 'examinou' }); }
    if (D && D.kps) D.kps.forEach(k => w.knowledge.award(k, { via: 'examinou' }));
    w.bus.emit('objeto', { id: o.id });
    return r;
  }
};
