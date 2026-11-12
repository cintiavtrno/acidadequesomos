// ===== s16_social.js — Etapa 7: simulação social (personalidade, necessidades, decisão, relações, memória, rumores) =====
// DOM-free. Camada ÚNICA sobre os sistemas já existentes: Sim.Relations / Sim.Memory (s4) e o mundo da rua (s15). Não cria outra movimentação:
// quem anda é o próprio mundo (vaiPara/Nav). Aqui só se decide *o que* fazer, *com quem*, *por quê*, e o que isso muda.
// Tudo que é texto, traço, relação inicial e boato é PROPOSTA (precisa de leitura de quem conhece o bairro). Itens com revisar:true: sensíveis.
Sim.Social = {};
(function () {
const S = Sim.Social, clamp = Sim.clamp;

// ---------------------------------------------------------------------------------------------- PERSONAS (seção 1)
// tracos 0..1 · nec = quanto cada necessidade cresce para essa pessoa (1 = padrão)
S.PERSONAS = {
  raimundo: { temperamento: 'reservado, orgulhoso e fiel às suas rotinas; só se abre com quem conhece há tempo', tracos: { sociavel: .45, reservado: .8, desconfiado: .5, pavio: .2, paciencia: .95, curioso: .4, prestativo: .6, fofoqueiro: .1 },
    interesses: ['dominó', 'o bairro', 'a padaria'], preferencias: ['café forte', 'jogo sem pressa'], habitos: ['mesa de dominó pela manhã', 'pão na padaria'], preocupacoes: ['mudanças na rua', 'a casa'],
    opinioes: { programa: -.3, mudancas: -.6, barulho: -.2 }, objetivo: 'continuar na casa e na mesa', nec: { socializar: .7, comer: .8, descansar: .6 },
    sabe: [['i_fiado', 'fato'], ['i_medicao', 'testemunhada']], segredos: ['i_fiado'] },
  ze: { temperamento: 'brincalhão e competitivo; gosta de provocar o parceiro de mesa', tracos: { sociavel: .8, reservado: .2, desconfiado: .2, pavio: .5, paciencia: .5, curioso: .5, prestativo: .5, fofoqueiro: .6 },
    interesses: ['dominó', 'barbearia', 'futebol'], preferencias: ['ganhar na carroça'], habitos: ['dominó'], preocupacoes: ['perder a vez', 'o barulho da obra'], opinioes: { programa: -.1, mudancas: -.2, barulho: .1 },
    objetivo: 'ensinar Lia a contar até seis', nec: { socializar: 1.2, coletivo: 1.3 }, sabe: [['i_fiado', 'suposicao'], ['i_medicao', 'suposicao']], segredos: [] },
  nonato: { temperamento: 'expansivo, vaidoso do jogo e da obra; se irrita rápido e passa rápido', tracos: { sociavel: .75, reservado: .2, desconfiado: .3, pavio: .8, paciencia: .35, curioso: .4, prestativo: .7, fofoqueiro: .45 },
    interesses: ['dominó', 'obra', 'cocada'], preferencias: ['bater de carroça'], habitos: ['dominó', 'pedreiro de ocasião'], preocupacoes: ['pagar o cimento', 'a tia'], opinioes: { programa: .2, mudancas: .1, barulho: .2 },
    objetivo: 'ganhar a partida e terminar o reboco', nec: { socializar: 1, resolver: 1.2, comer: 1.1 }, sabe: [['i_obra', 'fato'], ['i_medicao', 'recebida']], segredos: [] },
  bela: { temperamento: 'observadora, direta e atenta ao que passa na rua; fala pouco, mas fala certo', tracos: { sociavel: .5, reservado: .5, desconfiado: .65, pavio: .3, paciencia: .7, curioso: .8, prestativo: .5, fofoqueiro: .3 },
    interesses: ['costura', 'a rua', 'dominó'], preferencias: ['contar as pedras'], habitos: ['costura na janela do alto', 'dominó'], preocupacoes: ['quem olha a rua de fora'], opinioes: { programa: -.4, mudancas: -.3, barulho: -.3 },
    objetivo: 'descobrir de que lado está quem mede a rua', nec: { informar: 1.3, socializar: .8 }, sabe: [['i_reuniao', 'testemunhada'], ['i_programa', 'suposicao']], segredos: [] },
  cicera: { temperamento: 'acolhedora e atarefada, conhece a vida de meia rua; preocupa-se com o neto', tracos: { sociavel: .85, reservado: .25, desconfiado: .3, pavio: .3, paciencia: .6, curioso: .6, prestativo: .8, fofoqueiro: .8 },
    interesses: ['roupa no varal', 'neto', 'dominó'], preferencias: ['sombra do varal'], habitos: ['varal', 'cadeira da calçada'], preocupacoes: ['Júnior sumir', 'o boato do Programa'], opinioes: { programa: -.5, mudancas: -.3, barulho: 0 },
    objetivo: 'manter o neto por perto e a roupa lavada', nec: { socializar: 1.2, informar: 1.2, comprar: 1 }, sabe: [['i_medicao', 'testemunhada'], ['i_programa', 'boato'], ['i_fiado', 'boato']], segredos: [] },
  junior: { temperamento: 'inquieto, curioso e bom de ouvido; vai aonde tem movimento', tracos: { sociavel: .9, reservado: .1, desconfiado: .1, pavio: .5, paciencia: .15, curioso: .95, prestativo: .6, fofoqueiro: .9 },
    interesses: ['gato', 'mesa de dominó', 'cocada'], preferencias: ['correr'], habitos: ['patrulha da rua'], preocupacoes: ['ser chamado pela avó'], opinioes: { programa: 0, mudancas: 0, barulho: .4 },
    objetivo: 'descobrir tudo que acontece na rua', nec: { socializar: 1.4, comer: 1.3, descansar: .5 }, sabe: [['i_gato', 'testemunhada']], segredos: [] },
  tonho: { temperamento: 'simpático e atento à freguesia; sorri antes de qualquer assunto', tracos: { sociavel: .85, reservado: .25, desconfiado: .3, pavio: .25, paciencia: .6, curioso: .6, prestativo: .6, fofoqueiro: .6 },
    interesses: ['cocada', 'freguesia', 'pontos de venda'], preferencias: ['vender na sombra'], habitos: ['rodar a rua vendendo'], preocupacoes: ['o dia ser fraco'], opinioes: { programa: .1, mudancas: .1, barulho: .1 },
    objetivo: 'vender tudo antes do meio-dia', nec: { trabalhar: 1.3, comer: 1, descansar: 1.1 }, sabe: [['i_obra', 'recebida']], segredos: [] },
  dandara: { temperamento: 'comunicativa, organizada, ama reunião; fala com todo mundo e quer todo mundo junto', tracos: { sociavel: .9, reservado: .15, desconfiado: .3, pavio: .45, paciencia: .5, curioso: .6, prestativo: .85, fofoqueiro: .35 },
    interesses: ['associação', 'quadro de avisos', 'o Programa'], preferencias: ['reunião marcada'], habitos: ['associação', 'visitas'], preocupacoes: ['gente ficar de fora', 'o boato do Programa'], opinioes: { programa: .3, mudancas: .2, barulho: 0 },
    objetivo: 'juntar o bairro antes do Programa chegar', nec: { coletivo: 1.4, informar: 1.1, socializar: 1.2 }, sabe: [['i_reuniao', 'fato'], ['i_programa', 'fato']], segredos: [] },
  lucia: { temperamento: 'metódica e desconfiada de ser mal compreendida; só conta o que tem certeza', tracos: { sociavel: .35, reservado: .65, desconfiado: .6, pavio: .2, paciencia: .6, curioso: .7, prestativo: .5, fofoqueiro: .1 },
    interesses: ['fachadas', 'medidas', 'o relatório'], preferencias: ['dados conferidos'], habitos: ['medir', 'anotar'], preocupacoes: ['ser vista como inimiga', 'errar uma medida'], opinioes: { programa: .6, mudancas: .4, barulho: -.1 },
    objetivo: 'terminar o levantamento sem perder a confiança do bairro', nec: { trabalhar: 1.2, socializar: .6 }, sabe: [['i_programa', 'fato'], ['i_medicao', 'fato']], segredos: ['i_programa'] },
  aurea: { temperamento: 'paciente e discreta; sabe da vida de quem passa no balcão e não conta o que não é dela', tracos: { sociavel: .6, reservado: .75, desconfiado: .35, pavio: .15, paciencia: .85, curioso: .5, prestativo: .8, fofoqueiro: .1 },
    interesses: ['balcão', 'forno', 'caderneta'], preferencias: ['pão quente'], habitos: ['padaria'], preocupacoes: ['o fiado', 'o movimento'], opinioes: { programa: -.1, mudancas: -.4, barulho: -.2 },
    objetivo: 'manter a padaria aberta', nec: {}, sabe: [['i_fiado', 'fato']], segredos: ['i_fiado'], noMapa: false },
};
// relações iniciais entre moradores (independentes da Lia): aff −1..1, trust 0..1, tens 0..1
S.RELACOES = {
  'raimundo>ze': { aff: .5, trust: .7, tens: .05 }, 'ze>raimundo': { aff: .5, trust: .7, tens: .05 },
  'raimundo>nonato': { aff: .25, trust: .5 }, 'nonato>raimundo': { aff: .3, trust: .5 },
  'ze>nonato': { aff: .15, trust: .45, tens: .3 }, 'nonato>ze': { aff: .2, trust: .45, tens: .3 },
  'bela>cicera': { aff: .5, trust: .6 }, 'cicera>bela': { aff: .55, trust: .65 }, 'bela>raimundo': { aff: .3, trust: .6 }, 'raimundo>bela': { aff: .3, trust: .55 },
  'cicera>junior': { aff: .85, trust: .8 }, 'junior>cicera': { aff: .85, trust: .8 }, 'bela>nonato': { aff: .1, trust: .4, tens: .15 }, 'nonato>bela': { aff: .15, trust: .4, tens: .15 },
  'tonho>nonato': { aff: .35, trust: .5 }, 'nonato>tonho': { aff: .3, trust: .5 }, 'tonho>cicera': { aff: .3, trust: .5 }, 'cicera>tonho': { aff: .3, trust: .5 },
  'dandara>raimundo': { aff: .3, trust: .45 }, 'raimundo>dandara': { aff: .2, trust: .35 }, 'dandara>cicera': { aff: .4, trust: .55 }, 'cicera>dandara': { aff: .4, trust: .5 }, 'dandara>bela': { aff: .35, trust: .5 }, 'bela>dandara': { aff: .15, trust: .4 },
  'lucia>raimundo': { aff: 0, trust: .15 }, 'raimundo>lucia': { aff: -.15, trust: .1, tens: .15 }, 'bela>lucia': { aff: -.1, trust: .1, tens: .15 }, 'lucia>bela': { aff: 0, trust: .15 },
  'cicera>lucia': { aff: -.05, trust: .15 }, 'dandara>lucia': { aff: .35, trust: .55 }, 'lucia>dandara': { aff: .4, trust: .6 }, 'ze>lucia': { aff: 0, trust: .15 }, 'junior>lucia': { aff: .1, trust: .3 },
  'aurea>raimundo': { aff: .6, trust: .85 }, 'raimundo>aurea': { aff: .6, trust: .8 }, 'aurea>dandara': { aff: .4, trust: .6 }, 'dandara>aurea': { aff: .45, trust: .6 }, 'aurea>lucia': { aff: .1, trust: .3 }, 'lucia>aurea': { aff: .15, trust: .35 },
  'aurea>cicera': { aff: .3, trust: .5 }, 'cicera>aurea': { aff: .3, trust: .5 },
};

// ---------------------------------------------------------------------------------------------- NECESSIDADES (seção 2)
S.NEC = ['comer', 'trabalhar', 'descansar', 'socializar', 'comprar', 'visitar', 'coletivo', 'resolver', 'informar'];
// crescimento por minuto de jogo (a necessidade vai de 0 a 1 e orienta escolhas; nunca é mostrada)
S.CRESCE = { comer: .0045, trabalhar: .003, descansar: .0035, socializar: .006, comprar: .0035, visitar: .002, coletivo: .004, resolver: .0, informar: .005 };

// ---------------------------------------------------------------------------------------------- INFORMAÇÕES / RUMORES (seção 8)
// versoes[0] = o que de fato aconteceu; as seguintes perdem detalhe ou distorcem. corretas: índices considerados verdadeiros/aproximados.
S.INFOS = {
  i_medicao: { tema: 'programa', sigilo: 0, versoes: ['Uma moça do Programa anda medindo porta, janela e telhado de todo o quarteirão.', 'Tem gente do governo medindo as casas da rua.', 'Estão medindo as casas pra ver quais vão ser tiradas.'], corretas: [0, 1], eu: { id: 'lucia', versoes: ["Estou medindo porta, janela e telhado do quarteirão inteiro.", "Estou medindo as casas da rua.", "Estou medindo as casas pra ver quais entram na lista."] } },
  i_programa: { tema: 'programa', sigilo: .5, revisar: true, versoes: ['O Programa vai pintar e consertar as fachadas, e quem mora continua morando.', 'O Programa vai mexer nas casas, mas tem letra miúda que ninguém leu.', 'O Programa quer comprar os imóveis e tirar os moradores.'], corretas: [0] },
  i_reuniao: { tema: 'associacao', sigilo: 0, versoes: ['Dandara marcou reunião da associação pra sábado, depois do almoço.', 'Vai ter reunião da associação, mas ninguém sabe o dia.', 'A reunião da associação foi cancelada.'], corretas: [0, 1], eu: { id: 'dandara', versoes: ["Marquei a reunião da associação pra sábado, depois do almoço.", "Vai ter reunião da associação, só não fechei o dia.", "A reunião da associação foi cancelada."] } },
  i_fiado: { tema: 'padaria', sigilo: .85, revisar: true, versoes: ['Seu Raimundo leva o pão no fiado e paga na sexta; nunca deixou de pagar.', 'Seu Raimundo anda devendo na padaria.', 'Vó Áurea perde dinheiro com fiado e pode fechar a padaria.'], corretas: [0] },
  i_obra: { tema: 'obra', sigilo: 0, versoes: ['Nonato vai refazer o reboco da casa da tia e paga a obra com café.', 'Nonato pegou uma obra.', 'Nonato anda sem dinheiro e trabalhando de graça.'], corretas: [0, 1], eu: { id: 'nonato', versoes: ["Vou refazer o reboco da casa da minha tia. Ela paga com café.", "Peguei uma obra.", "Estou sem dinheiro e trabalhando de graça."] } },
  i_gato: { tema: 'rua', sigilo: 0, versoes: ['O gato da rua anda dormindo no sobrado; Júnior leva resto de pão pra ele.', 'Júnior anda dando comida pro gato.', 'O gato é de Júnior.'], corretas: [0, 1], eu: { id: 'junior', versoes: ["O gato dorme no sobrado e eu levo resto de pão pra ele.", "Eu dou comida pro gato.", "O gato é meu."] } },
};
// 1994: o que circula na rua já é efeito do Programa (aviso, risco, saída de moradores). Mesmo formato de 1991; só troca o conteúdo.
S.virar94 = () => {
  if (S._v94) return; S._v94 = true;
  S.INFOS.i_medicao = { tema: 'programa', sigilo: 0, versoes: ['O Programa mandou aviso de vistoria para mais três casas do quarteirão, com prazo para desocupar.', 'Mais casa da rua recebeu aviso do Programa.', 'O Programa vai tirar a rua inteira até o fim do ano.'], corretas: [0, 1], eu: { id: 'lucia', versoes: ['Estou conferindo a ficha das casas que já receberam aviso.', 'Estou conferindo as casas da rua.', 'Sou eu que escolho quais casas saem.'] } };
  S.INFOS.i_programa = { tema: 'programa', sigilo: .5, revisar: true, versoes: ['O Programa passou da pintura para a obra pesada: casa interditada, morador indenizado e gente indo embora.', 'O Programa está tirando morador das casas.', 'O Programa vai tirar todo mundo daqui e trazer só turista.'], corretas: [0, 1] };
  S.INFOS.i_reuniao = { tema: 'associacao', sigilo: 0, versoes: ['Dandara marcou reunião da associação para sábado, para ler a lista de quem recebeu aviso.', 'Vai ter reunião da associação, mas ninguém sabe o dia.', 'A reunião da associação foi cancelada.'], corretas: [0, 1], eu: { id: 'dandara', versoes: ['Marquei a reunião da associação para sábado. Vou ler a lista de quem recebeu aviso.', 'Vai ter reunião da associação, só não fechei o dia.', 'A reunião da associação foi cancelada.'] } };
  S.INFOS.i_obra = { tema: 'obra', sigilo: 0, versoes: ['Nonato pegou obra por empreita no casarão da esquina, pago por semana.', 'Nonato pegou uma obra do Programa.', 'Nonato vai embora da rua quando a obra acabar.'], corretas: [0, 1], eu: { id: 'nonato', versoes: ['Peguei obra por empreita no casarão da esquina. Pagam por semana.', 'Peguei uma obra do Programa.', 'Quando a obra acabar eu vou embora da rua.'] } };
  S.INFOS.i_gato = { tema: 'rua', sigilo: 0, versoes: ['O gato da rua agora dorme na casa fechada da esquina; Júnior entra pela janela para levar pão.', 'Júnior anda entrando na casa fechada da esquina.', 'O gato é de Júnior.'], corretas: [0, 1], eu: { id: 'junior', versoes: ['Eu entro pela janela da casa fechada da esquina para levar pão pro gato.', 'Eu entro na casa fechada da esquina.', 'O gato é meu.'] } };
};
if (typeof window !== 'undefined' && window.MUNDO_ANO === 1994) S.virar94();
S.FRAME = {   // como cada tipo de informação é contada
  fato: ['Eu sei que ', 'Olha, '], testemunhada: ['Eu vi: ', 'Vi com meus olhos: '], recebida: ['Me contaram que ', 'Soube que '], suposicao: ['Eu acho que ', 'Pra mim, '], boato: ['Dizem por aí que ', 'Anda correndo que '], incorreta: ['Dizem que '],
};
S.TIPOS = { fato: 'fato conhecido', testemunhada: 'testemunhado', recebida: 'ouvido de terceiros', suposicao: 'suposição', boato: 'boato', incorreta: 'informação incorreta' };

// ---------------------------------------------------------------------------------------------- vozes (falas curtas, PROPOSTA)
S.VOZ = {
  cumprimento: { raimundo: ['Bom dia.', 'Dia.'], ze: ['Fala, {n}!', 'E aí, {n}!'], nonato: ['Fala, {n}!', 'Chegou, {n}!'], bela: ['Bom dia, {n}.', 'Oi, {n}.'], cicera: ['Bom dia, meu bem!', 'Oi, {n}! Tá bom?'], junior: ['Oi, {n}!', 'E aí!'], tonho: ['Bom dia, {n}!', 'Cocada, {n}?'], dandara: ['Bom dia, {n}! Tudo bem?', 'Oi, {n}!'], lucia: ['Bom dia.', 'Olá.'], aurea: ['Bom dia, {n}.', 'Passa aqui, {n}.'] },
  frio: ['(Faz que não vê.)', '(Responde só com a cabeça.)', 'Hum.'],
  papo: { dominó: ['Esse jogo hoje tá devagar.', 'Quem ganhou a última mão?', 'Não vai ter carroça hoje.'], rua: ['A rua tá movimentada hoje.', 'O sol tá forte cedo.', 'Passou muita gente por aqui.'], familia: ['E a família, tudo bem?', 'Como vai a sua gente?'], padaria: ['O pão hoje saiu cedo.', 'Já foi na padaria?'], tempo: ['Vai chover à tarde, vocês vão ver.', 'Que calor bom.'], obra: ['Essa obra não termina nunca.', 'Preciso de cimento.'], programa: ['Anda tanta coisa na rua, né?'] },
  resposta: { aceita: ['É verdade.', 'Pois é.', 'Sempre foi assim.'], duvida: ['Será?', 'Isso eu não sabia.', 'Duvido.'], surpresa: ['Sério?', 'Não me diga!'], evita: ['Prefiro não falar disso.', 'Isso eu não sei, não.', 'Deixa isso pra lá.'] },
  adeus: ['Preciso ir.', 'Depois a gente fala.', 'Tenho que resolver uma coisa.', 'Fica com Deus.'],
  discussao: { prov: ['Isso foi sorte!', 'Sorte é o nome que perdedor dá!', 'Joga direito!'], res: ['Joguei como sempre!', 'Reclama com o dado!', 'Conta as pedras que você vê.'], paz: ['Foi brincadeira, homem.', 'Vamos ver a próxima.', 'Tá certo, tá certo.'], calma: ['Calma, gente.', 'Não precisa disso.'] },
  ajuda: { pede: ['Me dá uma ajuda?', 'Você tem um minuto?'], aceita: ['Pode deixar.', 'Vem cá, deixa comigo.'], recusa: ['Agora não dá.', 'Hoje eu não consigo.'], obrigado: ['Obrigada, viu?', 'Valeu, ajudou muito.'] },
};
S.PROBLEMAS = {   // motivos de pedir ajuda (resolver) — disparam por necessidade, não por horário fixo
  cicera: { id: 'corda', texto: 'A corda do varal arrebentou.', ajuda: ['nonato', 'tonho', 'dandara'], onde: 'varal' },
  dandara: { id: 'aviso', texto: 'Preciso de alguém pra segurar o aviso no quadro.', ajuda: ['nonato', 'cicera', 'tonho'], onde: 'quadro' },
  tonho: { id: 'troco', texto: 'Faltou troco pra cocada.', ajuda: ['bela', 'cicera', 'nonato'], onde: 'obs_2' },
};
const nomeCurto = id => (Sim.Rua.D.pessoas[id] ? Sim.Rua.D.pessoas[id].curto : id);

// ---------------------------------------------------------------------------------------------- SocialMind
Sim.SocialMind = class {
  constructor(w, saved) {
    this.w = w; this.R = w.rng; this.bus = w.bus; saved = saved || {};
    const init = {}; for (const k in S.RELACOES) init[k] = Object.assign({ aff: 0, trust: .1, tens: 0 }, S.RELACOES[k]);
    this.rel = new Sim.Relations(this.bus, init); this.mem = new Sim.Memory(this.bus);
    this.x = {};                                                   // extras por relação: amizade, intimidade, conflito, contatos, ganhos do dia
    this.need = {}; this.infos = {}; this.estado = {}; this.stats = { decisoes: {}, conversas: 0, cumprimentos: 0, discussoes: 0, pazes: 0, ajudas: 0, recusas: 0, compartilhadas: 0, retidas: 0, trocas: 0, abandonos: 0 };
    this.conv = []; this.cd = {}; this.seq = 0; this.tick = 0; this.log = [];
    for (const id in S.PERSONAS) {
      const P = S.PERSONAS[id]; this.need[id] = {}; this.estado[id] = { prox: 20 + this.R() * 40, fez: {}, pedido: null, ocupado: 0 };
      for (const k of S.NEC) this.need[id][k] = clamp(this.R() * .35 + (k === 'socializar' ? .1 : 0), 0, 1);
      for (const [info, tipo] of P.sabe) this.sabe(id, info, tipo, tipo === 'suposicao' ? 2 : tipo === 'boato' ? (info === 'i_fiado' ? 2 : 2) : tipo === 'recebida' ? 1 : 0, .85);
    }
    this.bus.on('dom_bate', d => this.noDomino('bate', d)); this.bus.on('dom_mao', () => this.noDomino('fim_mao'));
    if (saved.rel) this.rel.import(saved.rel); if (saved.mem) this.mem.import(saved.mem); if (saved.infos) this.infos = saved.infos; if (saved.x) this.x = saved.x; if (saved.need) this.need = saved.need;
  }
  exportar() { return { rel: this.rel.export(), mem: this.mem.export(), infos: JSON.parse(JSON.stringify(this.infos)), x: this.x, need: this.need }; }
  P(id) { return S.PERSONAS[id]; } tr(id, k) { const p = S.PERSONAS[id]; return p ? p.tracos[k] : .5; }
  // ---------------------------------------------------------------- relações (seção 5/6)
  ex(a, b) { const k = a + '>' + b; return this.x[k] || (this.x[k] = { amizade: 0, intim: 0, conflito: 0, n: 0, ult: -999, dia: { aff: 0, trust: 0, tens: 0 } }); }
  r(a, b) { return this.rel.get(a, b); }
  // dimensões pedidas: afinidade, confiança, amizade, intimidade, desconfiança, antipatia, conflito, histórico
  dim(a, b) { const r = this.r(a, b), e = this.ex(a, b); return { afinidade: r.aff, confianca: r.trust, amizade: e.amizade, intimidade: e.intim, desconfianca: 1 - r.trust, antipatia: Math.max(0, -r.aff), conflito: Math.max(e.conflito, r.tens), contatos: e.n, historico: this.rel.hist.filter(h => h.a === a && h.b === b).length }; }
  // todo ganho tem teto diário e rendimento decrescente: uma conversa nunca transforma desconhecidos em amigos
  contato(a, b, tipo, mag) {
    mag = mag == null ? 1 : mag; const r = this.r(a, b), e = this.ex(a, b), fa = this.w.t;
    const T = { conversa: { aff: .012, trust: .01 }, cumprimento: { aff: .004, trust: .002 }, ajuda: { aff: .035, trust: .04 }, jogo: { aff: .006, trust: .004 }, pazes: { aff: .02, trust: .015, tens: -.12 }, ajudou_lia: { aff: .05, trust: .06 }, discussao: { aff: -.03, trust: -.03, tens: .16 }, provocacao: { aff: .008, tens: .03 }, desfeita: { aff: -.05, trust: -.06, tens: .1 }, indevida: { aff: -.06, trust: -.14, tens: .12 }, informacao: { aff: .01, trust: .02 }, recusa: { aff: -.01, trust: -.01 } }[tipo]; if (!T) return;
    const d = {}; for (const k of ['aff', 'trust', 'tens']) {
      if (T[k] == null) continue; let v = T[k] * mag;
      if (k === 'trust' && v > 0) v *= (1 - this.tr(a, 'desconfiado') * .6);             // desconfiado confia devagar
      if (k === 'tens' && v > 0) v *= (.6 + this.tr(a, 'pavio'));                         // pavio curto esquenta mais
      if (v > 0 && k !== 'tens') { v *= (1 - r[k] * .5); const cap = k === 'aff' ? .07 : .06; const room = Math.max(0, cap - e.dia[k]); v = Math.min(v, room); e.dia[k] += v; }
      d[k] = v;
    }
    this.rel.change(a, b, d, tipo); e.n++; e.ult = this.w.clock.min;
    if (r.aff > .25 && r.trust > .35 && (tipo === 'conversa' || tipo === 'ajuda' || tipo === 'pazes')) e.amizade = clamp(e.amizade + .012 * (1 - e.amizade), 0, 1);
    if (e.amizade > .45 && r.trust > .6 && (tipo === 'conversa' || tipo === 'ajuda')) e.intim = clamp(e.intim + .008 * (1 - e.intim), 0, 1);
    if (tipo === 'discussao' || tipo === 'desfeita' || tipo === 'indevida') e.conflito = clamp(e.conflito + .15, 0, 1); if (tipo === 'pazes') e.conflito = clamp(e.conflito - .2, 0, 1);
  }
  // ---------------------------------------------------------------- memória (seção 7)
  lembrar(quem, tipo, o) {
    const id = tipo + ':' + (o.com || '-') + ':' + (++this.seq), L = this.mem.list(quem);
    this.mem.remember(quem, id, Object.assign({ tipo, rel: .5, pol: 0, min: this.w.clock.min }, o));
    if (L.length > 14) { let w = 0, wi = 0; L.forEach((f, i) => { const s = (f.rel || .3) * (1 - (this.w.clock.min - (f.min || 0)) / 600); if (i === 0 || s < w) { w = s; wi = i; } }); L.splice(wi, 1); }
  }
  lembranca(quem, tipo, com) { return this.mem.list(quem).filter(f => f.tipo === tipo && (!com || f.com === com)); }
  melhorLembrancaDeLia(id) {
    const L = this.mem.list(id).filter(f => f.com === 'lia' && ['lia_ajudou', 'lia_indevida', 'lia_conversou', 'lia_ouviu'].includes(f.tipo)); if (!L.length) return null;
    return L.sort((a, b) => (b.rel || 0) - (a.rel || 0))[0];
  }
  // ---------------------------------------------------------------- informações (seção 8)
  sabe(quem, info, tipo, versao, conf, via) { const h = this.infos[info] || (this.infos[info] = {}); if (h[quem] && h[quem].versao <= versao) return false; h[quem] = { tipo, versao: versao || 0, conf: conf == null ? .7 : conf, via: via || null, min: this.w.clock.min, duvida: false }; return true; }
  tem(quem, info) { return !!(this.infos[info] && this.infos[info][quem]); }
  texto(info, h) { const I = S.INFOS[info] || this.dinamicas && this.dinamicas[info]; return I ? I.versoes[Math.min(h.versao, I.versoes.length - 1)] : ''; }
  conhecidas(quem) { return Object.keys(this.infos).filter(i => this.infos[i][quem]); }
  // quer e pode contar? depende de relação, sigilo, traços e do momento
  disposicao(de, para, info) {
    const h = this.infos[info] && this.infos[info][de]; if (!h) return -1; const I = S.INFOS[info] || (this.dinamicas || {})[info] || { sigilo: 0 };
    const tr = this.r(de, para).trust, P = S.PERSONAS[de];
    if ((P.segredos || []).includes(info) && tr < .72) return -1;                       // segredo: só com muita confiança
    if (para !== 'lia' && this.tem(para, info)) return -1;   // já sabe
    const quer = this.tr(de, 'sociavel') * .35 + this.tr(de, 'fofoqueiro') * .5 + (I.sigilo ? 0 : .15) - this.tr(de, 'reservado') * .3 - I.sigilo * (1 - tr) * .9 - this.tr(de, 'desconfiado') * (1 - tr) * .5 + this.r(de, para).aff * .15;
    return quer;
  }
  // de conta `info` a `para`: nova crença, possivelmente degradada/reinterpretada
  contar(de, para, info) {
    const h = this.infos[info][de], I = S.INFOS[info] || this.dinamicas[info], tr = this.r(para, de).trust; if (!h) return null;
    let versao = h.versao;
    if (h.tipo !== 'fato' && h.tipo !== 'testemunhada' || this.R() < .12) { if (this.R() < .2 + this.tr(de, 'fofoqueiro') * .3 && versao < I.versoes.length - 1) versao++; }   // cada boca perde ou muda algo
    const antigo = this.infos[info][para];
    let tipo = (h.tipo === 'fato' || h.tipo === 'testemunhada') ? 'recebida' : (h.tipo === 'suposicao' ? 'boato' : 'boato'); let duvida = false;
    if (antigo && antigo.versao !== versao && ['fato', 'testemunhada'].includes(antigo.tipo)) { duvida = true; tipo = antigo.tipo; versao = antigo.versao; }   // quem viu com os próprios olhos não troca de versão
    else if (!I.corretas.includes(versao) && tr > .45 && this.tr(para, 'desconfiado') > .55) { duvida = true; }                                                   // desconfiado desconta o que parece exagero
    const conf = clamp((h.conf * .85) * (.55 + tr * .6), .1, .95);
    if (!antigo || versao >= antigo.versao || antigo.tipo === 'boato') this.infos[info][para] = { tipo, versao, conf, via: de, min: this.w.clock.min, duvida };
    this.stats.compartilhadas++; this.bus.emit('rumor', { de, para, info, versao, tipo, duvida });
    this.contato(de, para, 'informacao', .6);
    this.lembrar(para, 'recebeu_info', { com: de, info, rel: .4 });
    // se a informação diz respeito a alguém que descobre que foi a Lia quem espalhou, a confiança cai (revelação indevida)
    return { versao, tipo, duvida };
  }
  // fala de repasse (bolha): enquadra pelo tipo; incorreta/boato ganham ressalva
  fala(de, info) { const h = this.infos[info][de]; const I0 = S.INFOS[info], r = this.R(); if (I0 && I0.eu && I0.eu.id === de) return I0.eu.versoes[Math.min(h.versao, I0.eu.versoes.length - 1)]; const tp = h.tipo, fr = S.FRAME[tp] || S.FRAME.boato; const txt = this.texto(info, h); return fr[Math.floor(r * fr.length)] + (/^(Uma|Um|O|A|Os|As|Tem|Vai|Estão|Foi|Teve)\b/.test(txt) ? txt.charAt(0).toLowerCase() + txt.slice(1) : txt); }
  // Lia pergunta "o que andam comentando?"
  comentarios(id) {
    const lia = this.w.trust[id] || 0; const out = [];
    for (const info of this.conhecidas(id)) {
      if (id === 'lia') continue; const h = this.infos[info][id]; const I = S.INFOS[info] || (this.dinamicas || {})[info]; if (!I) continue;
      const tr = lia, P = S.PERSONAS[id];
      if ((P.segredos || []).includes(info) && tr < .72) { out.push({ info, retido: true }); continue; }
      if (I.sigilo * (1 - tr) * this.tr(id, 'reservado') > .25) { out.push({ info, retido: true }); continue; }
      out.push({ info, tipo: h.tipo, versao: h.versao, texto: this.fala(id, info), duvida: h.duvida, revisar: !!I.revisar });
    }
    return out;
  }
  liaOuve(id, info, versao, tipo) { const h = this.infos[info] || (this.infos[info] = {}); const velho = h.lia; const novo = { tipo: tipo || 'recebida', versao, conf: .6, via: id, min: this.w.clock.min, duvida: false }; if (!velho || (versao < velho.versao && ['fato', 'testemunhada'].includes(novo.tipo)) || tipo === 'testemunhada') h.lia = novo; else if (velho && velho.versao !== versao) { velho.duvida = true; (velho.outras = velho.outras || []).push({ via: id, versao }); } return h.lia; }
  // Lia conta a alguém algo que ouviu de outro: pode ferir a confiança de quem confiou nela
  revelarA(id, info) {
    const h = this.infos[info] && this.infos[info].lia; if (!h) return null; const I = S.INFOS[info]; const origem = h.via; const novo = !this.tem(id, info);
    this.sabe(id, info, 'recebida', h.versao, .5, 'lia'); this.stats.trocas++;
    if (I && I.sigilo >= .5 && origem && origem !== id) {
      this.lembrar(origem, 'lia_indevida', { com: 'lia', info, rel: .9, pol: -1, txt: 'Lia contou o que eu disse em confiança.', pendente: true });
      // a notícia chega à origem quando a informação volta por outras vias; consequência já registrada como pendência com efeito probabilístico
      this.pend = this.pend || []; this.pend.push({ origem, info, em: this.w.clock.min + 25 });
    }
    return { novo, id, info };
  }
  // ---------------------------------------------------------------- decisão (seções 2–4)
  livre(n) {
    if (n.state === 'Away' || n.alpha < .9 || this.w.congelado === n.id) return false;
    if (n.estado.sus) return false; const sit = n.state === 'Sitting';
    if (sit && this.w.assentos[n.seat] && this.w.assentos[n.seat].dominio) return false;      // dominó: segue jogando (só fala de passagem)
    if (n.state === 'Idle' && !n.task) return true; if (sit && !n.task) return true;
    if (n.task && n.task.tipo === 'patrulha' && n.state === 'Idle' && n.estado.parada) return true;
    return false;
  }
  proxTarefa(n) { const ag = this.w.ag[n.id] || []; return ag[n.idx] ? ag[n.idx].t : 1e9; }
  visiveis() { return Object.values(this.w.npcs).filter(m => m.state !== 'Away' && m.alpha > .9); }
  util(n, m) {   // vontade de conversar de n com m
    if (m.id === n.id || !this.estavel(m)) return -9; if (n.state === 'Sitting' && Math.hypot(n.x - m.x, n.y - m.y) > 70) return -9; const r = this.r(n.id, m.id), e = this.ex(n.id, m.id), d = Math.hypot(n.x - m.x, n.y - m.y);
    if (this.w.clock.min - e.ult < 25) return -9;                                        // acabaram de conversar
    const mem = this.lembranca(n.id, 'desentendimento', m.id).length; const evita = (r.tens > .5 || e.conflito > .45) ? -.7 : 0;
    const info = this.conhecidas(n.id).some(i => this.disposicao(n.id, m.id, i) > .1) ? .15 : 0;
    return this.need[n.id].socializar * .8 + r.aff * .5 + (r.trust - .3) * .25 + this.tr(n.id, 'sociavel') * .3 + info + evita - mem * .2 - d / 700 - (d > 480 ? 9 : 0);
  }
  estavel(m) { if (m.state === 'Away' || m.alpha < .9 || m.state === 'Walking' || m.state === 'SitIn' || m.state === 'SitOut' || m.state === 'Entering' || m.state === 'Exiting') return false; if (m.estado.papo) return false; if (m.state === 'Sitting' && this.w.assentos[m.seat] && this.w.assentos[m.seat].dominio) return false; if (this.w.congelado === m.id) return false; return true; }
  deliberar(n) {
    const w = this.w, id = n.id, nd = this.need[id], P = S.PERSONAS[id], est = this.estado[id], min = w.clock.min, opcoes = [];
    const dead = this.proxTarefa(n);
    // 1) conversar
    for (const m of this.visiveis()) { if (m.id === id) continue; const u = this.util(n, m); if (u > -5) opcoes.push({ k: 'conversar', alvo: m.id, u }); }
    // 2) comprar pão (hábito + necessidade; só quem circula livre; padaria aberta; no máximo 1 vez por manhã)
    if (['cicera', 'nonato', 'tonho', 'junior', 'bela'].includes(id) && w.integrado && !est.fez.comprar && min > 450 && min < 650 && n.seat !== 'E' && !(w.assentos[n.seat] && w.assentos[n.seat].dominio)) opcoes.push({ k: 'comprar', u: nd.comprar * 1.1 + nd.comer * .5 + (this.tr(id, 'sociavel') - .5) * .1 - .15 });
    // 3) descansar num banco (quem anda muito)
    if (['tonho', 'junior', 'dandara', 'lucia'].includes(id) && n.state === 'Idle') opcoes.push({ k: 'descansar', u: nd.descansar * 1.1 - .12 });
    // 4) observar a partida (curiosos)
    if (n.state === 'Idle' && this.tr(id, 'curioso') > .55) opcoes.push({ k: 'observar', u: nd.informar * .6 + nd.coletivo * .4 + this.tr(id, 'curioso') * .3 - .35 });
    // 5) pedir ajuda (resolver)
    if (S.PROBLEMAS[id] && nd.resolver > .3 && !est.pedido && this.candAjuda(id).length) opcoes.push({ k: 'ajuda', u: nd.resolver * 1.2 + this.tr(id, 'sociavel') * .2 - .1 });
    // 6) ficar (baseline: dá histerese e evita mudar de atividade o tempo todo)
    opcoes.push({ k: 'ficar', u: .26 + (n.state === 'Sitting' ? .12 : 0) });
    opcoes.forEach(o => { o.u += (this.R() - .5) * .08; if (est.fez[o.k + '_t'] != null && min - est.fez[o.k + '_t'] < 45 && o.k !== 'conversar' && o.k !== 'ficar') o.u -= .3; });
    opcoes.sort((a, b) => b.u - a.u); const o = opcoes[0];
    if (o.k !== 'conversar' && o.k !== 'ficar' && min - (est.ultAtiv == null ? -999 : est.ultAtiv) < 20) { est.prox = min + 4; return; }   // não troca de atividade a toda hora
    if (o.k !== 'conversar' && o.k !== 'ficar') est.ultAtiv = min;
    if (o.k === 'ficar' || o.u < .24) { est.prox = min + 3 + this.R() * 4; this.nota(id, 'ficar'); return; }
    if (dead - min < 6 && o.k !== 'conversar') { est.prox = min + 2; return; }          // vai começar a próxima tarefa: não se mete em outra
    est.fez[o.k + '_t'] = min; this.executar(n, o, dead); est.prox = min + 6 + this.R() * 6; this.stats.decisoes[o.k] = (this.stats.decisoes[o.k] || 0) + 1; this.nota(id, o.k);
  }
  nota(id, k) { this.log.push({ t: Math.round(this.w.clock.min), id, k }); if (this.log.length > 300) this.log.shift(); }
  executar(n, o, dead) {
    const w = this.w, id = n.id, min = w.clock.min;
    if (o.k === 'conversar') return this.iniciarPapo(n, w.npcs[o.alvo], dead);
    if (o.k === 'comprar') { this.desvio(n, [{ tipo: 'ir', spot: 'porta_padaria' }, { tipo: 'visita', dur: 4 + this.R() * 4 }]); this.estado[id].fez.comprar = true; this.need[id].comprar = 0; this.need[id].comer = Math.max(0, this.need[id].comer - .5); return; }
    if (o.k === 'descansar') { const reservados = new Set(); for (const q in w.ag) for (const t of w.ag[q]) if (t.tipo === 'sentar' && t.t > min - 5 && t.t < min + 45) reservados.add(t.assento); const livres = ['banquinho_1', 'banquinho_2', 'banco_b', 'banco_a', 'cad_calcada_1'].filter(s => !w.assentos[s].ocup && !reservados.has(s)); if (!livres.length) return; const s = livres[Math.floor(this.R() * livres.length)]; this.desvio(n, [{ tipo: 'sentar', assento: s }, { tipo: 'esperar', dur: 6 + this.R() * 8, anim: 'idle', repouso: true }, { tipo: 'levantar' }], dead); this.need[id].descansar = 0; return; }
    if (o.k === 'observar') { const sp = ['obs_1', 'obs_2', 'obs_3', 'obs_4'][Math.floor(this.R() * 4)]; this.desvio(n, [{ tipo: 'ir', spot: sp }, { tipo: 'olhar_mesa', dur: 5 + this.R() * 5 }], dead); this.need[id].informar = Math.max(0, this.need[id].informar - .3); this.need[id].coletivo = Math.max(0, this.need[id].coletivo - .2); return; }
    if (o.k === 'ajuda') return this.pedirAjuda(n);
  }
  // insere um desvio na frente da agenda: o que ia fazer continua depois (inclusive voltar a sentar no mesmo lugar)
  desvio(n, tarefas, ate) {
    const w = this.w, ag = w.ag[n.id], t0 = w.clock.min, ins = [];
    if (n.state === 'Sitting' && n.seat) { const s = n.seat; ins.push({ t: t0, tipo: 'levantar', esp: 1 }); ins.push(...tarefas.map(t => Object.assign({ t: t0, esp: 1 }, t))); ins.push({ t: t0, tipo: 'sentar', assento: s, esp: 1 }); }
    else { ins.push(...tarefas.map(t => Object.assign({ t: t0, esp: 1 }, t))); if (n.task && n.task.tipo === 'patrulha') { n.estado.retoma = n.task; n.task = null; ag.splice(n.idx, 0, ...ins, Object.assign({}, n.estado.retoma, { t: t0, ret: 1 })); n.estado.retoma = null; return; } }
    ag.splice(n.idx, 0, ...ins);
  }
  // ---------------------------------------------------------------- conversas espontâneas (seção 4/6/8)
  iniciarPapo(a, b, dead) {
    const w = this.w; if (!this.estavel(b)) return false; const c = { a: a.id, b: b.id, fase: 0, tt: 0, rep: 0, dead, ini: w.clock.min, tema: null };
    c.tema = this.escolherTema(a.id, b.id); a.estado.papo = c; b.estado.papo = c; if (a.task && a.task.tipo === 'patrulha') a.estado.retoma = a.task; a.task = { tipo: 'papo_ctl', esp: 1 };
    const lado = b.x < a.x ? 1 : -1; const perto = Math.hypot(a.x - b.x, a.y - b.y) <= 46;
    if (perto) { c.fase = 1; a.face = b.x < a.x ? 'left' : 'right'; b.face = a.x < b.x ? 'left' : 'right'; if (b.state === 'Idle') b.estado.pausa = w.t + 20; }
    else { const f = Sim.Nav.nearestFree(b.x + lado * 30, b.y + 6); if (!w.vaiPara(a, f[0], f[1], () => { c.fase = 1; })) { this.fimPapo(c, 'sem_caminho'); return false; } }
    this.conv.push(c); this.bus.emit('papo_inicio', { a: a.id, b: b.id }); return true;
  }
  escolherTema(a, b) {
    for (const i of this.conhecidas(a)) if (this.disposicao(a, b, i) > .12 && this.R() < .75) return { k: 'info', info: i };
    const A = S.PERSONAS[a], pool = ['dominó', 'rua', 'tempo', 'padaria', 'familia'].filter(t => t !== 'familia' || this.r(a, b).trust > .45); if (A.interesses.some(i => /obra/.test(i))) pool.push('obra');
    return { k: 'papo', tema: pool[Math.floor(this.R() * pool.length)] };
  }
  linhaVoz(lst, n, outro) { return lst[Math.floor(this.R() * lst.length)].replace('{n}', nomeCurto(outro)); }
  stepPapo(c, dt) {
    const w = this.w, a = w.npcs[c.a], b = w.npcs[c.b]; c.tt += dt;
    if (!a || !b || a.state === 'Away' || b.state === 'Away') return this.fimPapo(c, 'saiu');
    if (c.fase === 0) { if (c.tt > 45) this.fimPapo(c, 'demora'); if (b.state === 'Walking') return this.fimPapo(c, 'alvo_saiu'); return; }
    if (b.state === 'Walking' || b.state === 'SitOut') return this.fimPapo(c, 'alvo_saiu');
    if (w.clock.min >= c.dead - 1 && c.rep > 0) return this.fimPapo(c, 'hora');
    if (c.fase === 1) { c.fase = 2; c.tt = 0; this.abertura(c, a, b); }
    else if (c.fase === 2 && c.tt > 3.4) { c.fase = 3; c.tt = 0; this.resposta(c, a, b); }
    else if (c.fase === 3 && c.tt > 3.4) {
      c.rep++; const abandono = this.r(c.a, c.b).tens * .55 + (1 - this.tr(c.a, 'paciencia')) * .2 + (1 - this.tr(c.b, 'paciencia')) * .12 + c.rep * .22 + (w.clock.min >= c.dead - 3 ? .5 : 0) - this.r(c.a, c.b).aff * .15;
      if (c.rep >= 3 || w.rng() < abandono) { const quem = this.R() < .5 ? a : b; if (c.rep < 3) { this.stats.abandonos++; quem.falar(this.linhaVoz(S.VOZ.adeus, quem, quem === a ? c.b : c.a), 2.6); this.contato(quem === a ? c.b : c.a, quem.id, 'recusa', .3); } return this.fimPapo(c, 'fim'); }
      c.tema = this.escolherTema(c.a, c.b); c.fase = 2; c.tt = 0; this.abertura(c, a, b);
    }
  }
  abertura(c, a, b) {
    a.setAnim('talk'); a.face = b.x < a.x ? 'left' : 'right'; if (b.state === 'Idle' || b.state === 'Sitting') b.face = a.x < b.x ? 'left' : 'right';
    const T = c.tema; if (T.k === 'info') { const txt = this.fala(c.a, T.info); a.falar(txt.length > 96 ? txt.slice(0, 94) + '…' : txt, 3.4); }
    else { const l = S.VOZ.papo[T.tema] || S.VOZ.papo.rua; a.falar(this.linhaVoz(l, a, c.b), 3.2); }
    if (this.w.nearLia && this.w.nearLia(a, b)) this.ouviuLia(c);
  }
  resposta(c, a, b) {
    a.setAnim('idle'); b.setAnim(b.state === 'Sitting' ? b.anim : 'talk'); const T = c.tema;
    if (T.k === 'info') {
      const disp = this.disposicao(c.a, c.b, T.info), I = S.INFOS[T.info] || this.dinamicas[T.info];
      const r = this.contar(c.a, c.b, T.info); const h = this.infos[T.info][c.b];
      const k = r.duvida ? 'duvida' : (!I.corretas.includes(h.versao) && this.tr(c.b, 'desconfiado') > .5) ? 'duvida' : this.tr(c.b, 'curioso') > .6 ? 'surpresa' : 'aceita'; b.falar(this.linhaVoz(S.VOZ.resposta[k], b, c.a), 3);
      if (!this.estado[c.a]) return; this.need[c.b].informar = Math.max(0, this.need[c.b].informar - .25); this.need[c.a].informar = Math.max(0, this.need[c.a].informar - .1);
      if (this.R() < .35) this.lembrar(c.b, 'recebeu_info', { com: c.a, info: T.info, rel: .45 });
    } else { const l = S.VOZ.resposta.aceita; b.falar(this.linhaVoz(l, b, c.a), 3); }
    this.contato(c.a, c.b, 'conversa'); this.contato(c.b, c.a, 'conversa'); this.stats.conversas++; this.need[c.a].socializar = Math.max(0, this.need[c.a].socializar - .35); this.need[c.b].socializar = Math.max(0, this.need[c.b].socializar - .3);
    this.lembrar(c.a, 'conversou', { com: c.b, rel: .3 }); this.lembrar(c.b, 'conversou', { com: c.a, rel: .3 });
    this.bus.emit('papo_espontaneo', { a: c.a, b: c.b, tema: T.k === 'info' ? T.info : T.tema });
  }
  fimPapo(c, motivo) {
    const w = this.w, a = w.npcs[c.a], b = w.npcs[c.b]; if (a) { a.estado.papo = null; if (a.task && a.task.tipo === 'papo_ctl') { a.task = a.estado.retoma || null; a.estado.retoma = null; } a.setAnim(a.state === 'Sitting' ? 'sit' : 'idle'); } if (b) { b.estado.papo = null; b.estado.pausa = 0; if (b.state === 'Idle') b.setAnim('idle'); }
    this.conv = this.conv.filter(x => x !== c); this.bus.emit('papo_fim', { a: c.a, b: c.b, motivo });
  }
  ouviuLia(c) { if (c.ouvido) return; c.ouvido = true; const T = c.tema; if (T.k === 'info') { const h = this.infos[T.info][c.a]; this.liaOuve(c.a, T.info, h.versao, 'testemunhada'); this.bus.emit('lia_ouviu', { info: T.info, de: c.a, para: c.b }); } }
  // ---------------------------------------------------------------- cumprimentos ao passar
  cumprimentos() {
    const w = this.w, V = this.visiveis();
    for (let i = 0; i < V.length; i++) for (let j = i + 1; j < V.length; j++) {
      const a = V[i], b = V[j]; if (a.state !== 'Walking' && b.state !== 'Walking') continue; if (a.estado.papo || b.estado.papo) continue;
      const d = Math.hypot(a.x - b.x, (a.y - b.y) * 1.3); if (d > 40) continue; const k = [a.id, b.id].sort().join('~'); if ((this.cd[k] || -999) > w.t - 120) continue; this.cd[k] = w.t;
      for (const [x, y] of [[a, b], [b, a]]) {
        const r = this.r(x.id, y.id); if (x.say) continue;
        if (r.tens > .45 || r.aff < -.1) { if (w.rng() < .6) x.falar(S.VOZ.frio[Math.floor(w.rng() * S.VOZ.frio.length)], 2.4); this.contato(x.id, y.id, 'desfeita', .15); this.bus.emit('frieza', { de: x.id, para: y.id }); continue; }
        if (r.aff > .2 || r.trust > .4 || w.rng() < this.tr(x.id, 'sociavel') * .5) { const l = S.VOZ.cumprimento[x.id] || ['Bom dia.']; x.falar(this.linhaVoz(l, x, y.id), 2.4); this.contato(x.id, y.id, 'cumprimento'); this.stats.cumprimentos++; this.bus.emit('cumprimento', { de: x.id, para: y.id }); }
      }
    }
  }
  // ---------------------------------------------------------------- pedidos de ajuda (seção 4)
  candAjuda(id) { return S.PROBLEMAS[id].ajuda.map(h => this.w.npcs[h]).filter(h => h && this.estavel(h) && !h.estado.papo && this.r(id, h.id).tens < .5); }
  pedirAjuda(n) {
    const id = n.id, Pb = S.PROBLEMAS[id], w = this.w, est = this.estado[id]; const cand = this.candAjuda(id);
    if (!cand.length) { est.prox = w.clock.min + 6; return; }
    cand.sort((x, y) => (this.r(id, y.id).trust + this.tr(y.id, 'prestativo')) - (this.r(id, x.id).trust + this.tr(x.id, 'prestativo'))); const h = cand[0];
    const ped = est.pedido = { de: id, para: h.id, fase: 0, tt: 0, ini: w.clock.min }; if (n.task && n.task.tipo === 'patrulha') n.estado.retoma = n.task; n.task = { tipo: 'papo_ctl', esp: 1 }; n.estado.papo = { ajuda: true }; h.estado.papo = { ajuda: true };
    const f = Sim.Nav.nearestFree(h.x + (h.x < n.x ? 28 : -28), h.y + 6); if (!w.vaiPara(n, f[0], f[1], () => { if (est.pedido === ped) ped.fase = 1; })) { est.pedido = null; n.estado.papo = null; h.estado.papo = null; n.task = n.estado.retoma || null; n.estado.retoma = null; return; }
    this.ajudas = this.ajudas || []; this.ajudas.push(ped);
  }
  stepAjuda(p, dt) {
    const w = this.w, a = w.npcs[p.de], b = w.npcs[p.para], Pb = S.PROBLEMAS[p.de]; p.tt += dt; const est = this.estado[p.de];
    const fim = () => { a.estado.papo = null; b.estado.papo = null; if (a.task && a.task.tipo === 'papo_ctl') { a.task = a.estado.retoma || null; a.estado.retoma = null; } a.setAnim('idle'); b.setAnim(b.state === 'Sitting' ? 'sit' : 'idle'); est.pedido = null; this.ajudas = this.ajudas.filter(x => x !== p); this.need[p.de].resolver = 0; };
    if (b.state === 'Away' || a.state === 'Away') return fim();
    if (p.fase === 0) { if (p.tt > 40) fim(); return; }
    if (p.fase === 1) { a.face = b.x < a.x ? 'left' : 'right'; a.setAnim('talk'); a.falar(Pb.texto + ' ' + this.linhaVoz(S.VOZ.ajuda.pede, a, p.para), 4); p.fase = 2; p.tt = 0; return; }
    if (p.fase === 2 && p.tt > 4) {
      const prob = .25 + this.r(p.para, p.de).trust * .5 + this.tr(p.para, 'prestativo') * .35 - this.r(p.para, p.de).tens * .6 - (b.state === 'Acting' ? .1 : 0);
      p.aceita = w.rng() < prob; b.falar(this.linhaVoz(p.aceita ? S.VOZ.ajuda.aceita : S.VOZ.ajuda.recusa, b, p.de), 3); p.fase = 3; p.tt = 0; if (!p.aceita) { this.stats.recusas++; this.contato(p.de, p.para, 'recusa'); this.lembrar(p.de, 'ajuda_negada', { com: p.para, rel: .5, pol: -.4 }); return fim(); } return;
    }
    if (p.fase === 3 && p.tt > 3.2) { a.setAnim('interact'); b.setAnim('interact'); p.fase = 4; p.tt = 0; return; }
    if (p.fase === 4 && p.tt > 5) { a.falar(this.linhaVoz(S.VOZ.ajuda.obrigado, a, p.para), 3); this.contato(p.de, p.para, 'ajuda'); this.contato(p.para, p.de, 'ajuda', .6); this.stats.ajudas++; this.lembrar(p.de, 'recebeu_ajuda', { com: p.para, rel: .7, pol: 1 }); this.lembrar(p.para, 'ajudou', { com: p.de, rel: .5, pol: .5 }); this.bus.emit('ajuda', { de: p.de, para: p.para }); return fim(); }
  }
  // ---------------------------------------------------------------- dominó: discussão e pazes
  noDomino(ev, d) {
    const w = this.w, m = w.mesa; const jog = Object.values(w.assentos).filter(a => a.dominio && a.ocup && a.ocup !== 'lia').map(a => a.ocup); if (ev === 'trancou') return;
    if (ev === 'bate') {
      const venc = d.id; if (!venc || venc === 'lia') return;
      const adv = Sim.Rua.D.ordem.filter(q => Sim.Rua.D.dupla[q] !== Sim.Rua.D.dupla[d.s]).map(q => w.assentos[q].ocup).filter(x => x && x !== 'lia');
      for (const x of adv) {
        const agro = (Sim.Rua.D.jogo[x] || { agro: .4 }).agro, t = this.r(x, venc).tens, forca = d.tipo === 'cruzada' ? 1.3 : d.tipo === 'laelo' ? 1.1 : d.tipo === 'carroca' ? .8 : .5;
        const p = clamp((agro * .2 + t * .6 + this.tr(x, 'pavio') * .2) * forca - this.r(x, venc).aff * .2, 0, .7);
        if (w.rng() < p && (this.cd['disc'] || -999) < w.t - 60) { this.cd['disc'] = w.t; return this.discussao(x, venc, d); }
      }
    }
    if (ev === 'fim_mao') { for (const a of jog) for (const b of jog) if (a < b && this.r(a, b).tens > .2 && this.ex(a, b).conflito > .1 && w.rng() < .45 + this.r(a, b).aff * .4) this.pazes(a, b); }
  }
  discussao(x, v, d) {
    const w = this.w, nx = w.npcs[x], nv = w.npcs[v]; if (!nx || !nv) return;
    const forte = this.r(x, v).tens > .35 || this.tr(x, 'pavio') > .7 && w.rng() < .5;
    nx.falar(S.VOZ.discussao.prov[Math.floor(w.rng() * 3)], 2.6); setTimeoutish(w, 2.2, () => nv.falar(S.VOZ.discussao.res[Math.floor(w.rng() * 3)], 2.6));
    if (forte) { this.contato(x, v, 'discussao'); this.contato(v, x, 'discussao', .6); this.stats.discussoes++; this.lembrar(x, 'desentendimento', { com: v, rel: .8, pol: -1, txt: 'discussão na mesa' }); this.lembrar(v, 'desentendimento', { com: x, rel: .8, pol: -1, txt: 'discussão na mesa' }); }
    else { this.contato(x, v, 'provocacao'); this.contato(v, x, 'provocacao'); this.stats.provocacoes = (this.stats.provocacoes || 0) + 1; }
    // quem vê, lembra e pode reagir; a história vira uma informação testemunhada
    const dyn = this.dinamicas = this.dinamicas || {}; const id = 'i_disc_' + (++this.seq); dyn[id] = { tema: 'rua', sigilo: 0, corretas: [0, 1], versoes: [(forte ? 'Seu ' : '') + nomeCurto(x) + ' e ' + nomeCurto(v) + ' discutiram feio na mesa de dominó.', 'Teve confusão na mesa de dominó.', 'O dominó acabou em briga de verdade.'] };
    const test = [...Object.values(w.npcs).filter(n => n.state !== 'Away' && n.alpha > .9 && Math.hypot(n.x - nx.x, n.y - nx.y) < 150).map(n => n.id)];
    for (const q of test) { if (q !== x && q !== v) this.lembrar(q, 'presenciou_discussao', { com: x, com2: v, rel: .6 }); this.sabe(q, id, 'testemunhada', 0, .9); if (q !== x && q !== v && forte && this.tr(q, 'prestativo') > .55 && w.rng() < .6) setTimeoutish(w, 3.4, () => w.npcs[q] && w.npcs[q].falar(S.VOZ.discussao.calma[Math.floor(w.rng() * 2)], 2.4)); }
    if (w.nearLia && w.nearLia(nx, nv)) this.liaOuve(x, id, 0, 'testemunhada');
    this.bus.emit('discussao', { x, v, forte, testemunhas: test });
  }
  pazes(a, b) { const na = this.w.npcs[a], nb = this.w.npcs[b]; if (!na || !nb) return; na.falar(S.VOZ.discussao.paz[Math.floor(this.w.rng() * 3)], 2.4); this.contato(a, b, 'pazes'); this.contato(b, a, 'pazes'); this.stats.pazes++; this.bus.emit('pazes', { a, b }); }
  // Lia entrou para jogar quando faltava gente: ajudou a mesa
  liaAjudouMesa(outros) { for (const o of outros) { this.contato(o, 'lia', 'ajudou_lia'); this.lembrar(o, 'lia_ajudou', { com: 'lia', rel: .8, pol: 1, txt: 'Lia completou a mesa quando faltava um.' }); } this.bus.emit('lia_ajudou', { outros }); }
  liaConversou(id) { this.lembrar(id, 'lia_conversou', { com: 'lia', rel: .35 }); this.contato(id, 'lia', 'conversa'); this.need[id].socializar = Math.max(0, this.need[id].socializar - .3); }
  // ---------------------------------------------------------------- tique principal
  update(dt) {
    const w = this.w, min = w.clock.min; this.tick += dt;
    for (const c of this.conv.slice()) this.stepPapo(c, dt);
    for (const p of (this.ajudas || []).slice()) this.stepAjuda(p, dt);
    if (this.timers) { this.timers = this.timers.filter(t => { t.s -= dt; if (t.s <= 0) { t.fn(); return false; } return true; }); }
    if (this.tick < .5) return; const step = this.tick; this.tick = 0; const dmin = step * (w.clock.rate || .25);
    for (const id in this.need) { const P = S.PERSONAS[id]; for (const k of S.NEC) { if (k === 'resolver') { if (S.PROBLEMAS[id] && min > 460 && this.need[id].resolver < .6 && w.rng() < .0035 * dmin * 6) this.need[id].resolver += .35 + w.rng() * .2; continue; } this.need[id][k] = clamp(this.need[id][k] + S.CRESCE[k] * dmin * ((P.nec && P.nec[k]) || 1), 0, 1); } }
    // necessidades satisfeitas por estar fazendo algo: sentar descansa, jogar satisfaz o coletivo
    for (const id in w.npcs) { const n = w.npcs[id]; if (n.state === 'Sitting') { this.need[id].descansar = Math.max(0, this.need[id].descansar - .004 * dmin * 6); if (w.assentos[n.seat] && w.assentos[n.seat].dominio && w.mesa.fase === 'jogando') { this.need[id].coletivo = Math.max(0, this.need[id].coletivo - .01 * dmin * 6); this.need[id].socializar = Math.max(0, this.need[id].socializar - .002 * dmin * 6); } } if (n.state !== 'Away' && n.task && n.task.tipo === 'patrulha' && id === 'tonho') this.need[id].trabalhar = Math.max(0, this.need[id].trabalhar - .006 * dmin * 6); }
    this.cumprimentos();
    for (const n of Object.values(w.npcs)) { const est = this.estado[n.id]; if (min < est.prox || !this.livre(n)) continue; this.deliberar(n); }
    // interrupção educada: o horário da agenda chegou
    for (const n of Object.values(w.npcs)) if (n.estado.papo && n.estado.papo.a === n.id && min >= this.proxTarefa(n) + 1) this.fimPapo(n.estado.papo, 'agenda');
    // consequência de revelação indevida
    this.pend = (this.pend || []).filter(p => { if (min < p.em) return true; this.contato(p.origem, 'lia', 'indevida'); this.w.trust[p.origem] = clamp((this.w.trust[p.origem] || 0) - .1, 0, 1); this.bus.emit('confianca_quebrada', { id: p.origem, info: p.info }); return false; });
  }
};
Object.assign(Sim.SocialMind.prototype, {
  // saudação à Lia que depende do que o morador lembra (não repete como se nunca a tivesse visto)
  saudacaoLia(id) {
    const f = this.melhorLembrancaDeLia(id); if (!f) return null; const v = this.r(id, 'lia');
    const T = {
      lia_ajudou: { raimundo: 'Lia. Obrigado por ontem na mesa, viu?', ze: 'Olha a Lia! A que completou a mesa!', nonato: 'A Lia salvou o jogo, hein!', bela: 'Lia. Valeu pela mesa.', cicera: 'Minha filha, que bom te ver! Obrigada pela ajuda.', _: 'Oi, Lia. Não esqueci que você ajudou.' },
      lia_conversou: { raimundo: 'De novo por aqui, Lia.', ze: 'Voltou pra aprender, né?', nonato: 'E aí, Lia! Já de volta?', bela: 'Oi, Lia. Já falamos hoje.', cicera: 'Oi, Lia! Passou por aqui de novo.', _: 'Oi, Lia. A gente já conversou.' },
      lia_indevida: { _: 'Hum. Lia.' },
    }[f.tipo]; if (!T) return null;
    if (f.tipo === 'lia_indevida' || v.tens > .3) return T._ || 'Hum.';
    return T[id] || T._;
  },
  // "O que andam comentando?" — devolve linhas e atualiza o caderno
  perguntarComentarios(id) {
    const out = [], L = this.comentarios(id); const dizivel = L.filter(c => !c.retido);
    if (!dizivel.length) return [{ quem: id, texto: L.length ? S.VOZ.resposta.evita[Math.floor(this.R() * 3 % S.VOZ.resposta.evita.length)] : 'Nada de novo, Lia.' }];
    const c = dizivel.sort((a, b) => (this.feitas && this.feitas[id + a.info] ? 1 : 0) - (this.feitas && this.feitas[id + b.info] ? 1 : 0) || a.versao - b.versao)[0];
    this.feitas = this.feitas || {}; this.feitas[id + c.info] = 1;
    out.push({ quem: id, texto: c.texto, revisar: c.revisar });
    const t = this.liaOuve(id, c.info, c.versao, c.tipo === 'fato' || c.tipo === 'testemunhada' ? 'recebida' : c.tipo);
    this.caderno = this.caderno || {}; this.caderno[c.info] = { versao: t.versao, tipo: t.tipo, via: t.via, duvida: !!t.duvida };
    out.push({ quem: 'nota', texto: 'Anotado (' + S.TIPOS[t.tipo] + (t.duvida ? ', versões diferentes' : '') + '): ' + this.texto(c.info, t) });
    this.contato(id, 'lia', 'informacao', .5); this.lembrar(id, 'lia_conversou', { com: 'lia', rel: .35 }); this.bus.emit('comentario', { id, info: c.info, tipo: t.tipo });
    return out;
  },
  // Vó Áurea (fora do mapa) troca informação com quem passa na padaria
  encontroPadaria(id) {
    const a = 'aurea'; if (!this.need[id]) return; this.need[id].comprar = 0; this.need[id].comer = Math.max(0, this.need[id].comer - .5);
    for (const info of this.conhecidas(a)) if (this.disposicao(a, id, info) > .2 && this.R() < .5) { this.contar(a, id, info); break; }
    for (const info of this.conhecidas(id)) if (info !== 'i_fiado' && this.disposicao(id, a, info) > .3 && this.R() < .4) { this.contar(id, a, info); break; }
    this.contato(id, a, 'conversa', .7); this.contato(a, id, 'conversa', .7); this.bus.emit('encontro_padaria', { id });
  },
});
function setTimeoutish(w, s, fn) { const sm = w.social; sm.timers = sm.timers || []; sm.timers.push({ s, fn }); }
})();
