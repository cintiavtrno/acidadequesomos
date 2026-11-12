// ===== s13_rua_data.js — dados da rua (Etapa 6): elenco, assentos, pontos, agenda, falas =====
// Tudo aqui é PROPOSTA (nenhuma fala/rotina nova foi aprovada). Itens com revisar:true precisam de leitura de quem conhece o bairro e a cultura local.
// Coordenadas: x do mundo; sy = linha dos pés abaixo do encosto da parede (0..21 calçada, 22+ meio-fio/rua). y real = yw(x) + sy.
Sim.Rua = { v: '6.0', D: {} };
(function () {
const RD = Sim.Rua.D;
RD.W = 1130; RD.VH = 270;
RD.yw = x => 212 + Math.floor(Math.max(0, x) / 70);
RD.dia = { inicio: 420, fim: 1140 };                   // 07:00–19:00 (proposta: o dia vai até o anoitecer)
const T = s => { const [h, m] = s.split(':').map(Number); return h * 60 + m; };
RD.T = T;

// ---- elenco (folhas *_side; Lia usa lia_side6) ----
RD.pessoas = {
  raimundo: { nome: 'Seu Raimundo', curto: 'Raimundo', cor: '#e8c07a', papel: 'vizinho do sobrado amarelo', ritmo: 0.55 },
  ze:       { nome: 'Seu Zé', curto: 'Zé', cor: '#9fc4d8', papel: 'jogador de dominó, aposentado', ritmo: 0.62 },
  nonato:   { nome: 'Nonato', curto: 'Nonato', cor: '#e8c85a', papel: 'jogador de dominó, pedreiro de ocasião', ritmo: 0.8 },
  bela:     { nome: 'Dona Bela', curto: 'Bela', cor: '#e89ab4', papel: 'jogadora de dominó, costureira', ritmo: 0.7 },
  cicera:   { nome: 'Dona Cícera', curto: 'Cícera', cor: '#f0be4c', papel: 'moradora do casarão rosa, lava roupa para o bairro', ritmo: 0.85 },
  junior:   { nome: 'Júnior', curto: 'Júnior', cor: '#e0705a', papel: 'menino da rua, neto de Cícera', ritmo: 1.55 },
  tonho:    { nome: 'Tonho', curto: 'Tonho', cor: '#8ec8e8', papel: 'vendedor de cocada e queijadinha', ritmo: 0.85 },
  dandara:  { nome: 'Dandara', curto: 'Dandara', cor: '#d594b0', papel: 'líder da associação de moradores', ritmo: 1.0 },
  lucia:    { nome: 'Lúcia', curto: 'Lúcia', cor: '#f5a64a', papel: 'técnica do Programa de recuperação', ritmo: 1.0 },
};
// velocidade de caminhada em px/s (do atlas: speed_mps*24) — valores usados quando o atlas ainda não carregou (testes em Node)
RD.vel = { lia: 30.5, raimundo: 15.7, ze: 13.6, nonato: 19.2, bela: 16.6, cicera: 24, junior: 22.5, tonho: 22, dandara: 26, lucia: 29 };

// ---- mesa de dominó: assentos (cadeira, posição, direção do corpo), ordem do jogo e duplas ----
RD.mesa = { x: 240, sy: 15, w: 34, lado: 17 };
RD.assentos = {
  E: { id: 'E', cadeira: 'cad_dom_E', x: 212, sy: 15, face: 'right', sort: 0.1, aprox: [198, 19] },
  D: { id: 'D', cadeira: 'cad_dom_D', x: 268, sy: 15, face: 'left',  sort: 0.1, aprox: [282, 19] },
  F: { id: 'F', cadeira: 'cad_dom_F', x: 240, sy: 8,  face: 'down',  sort: 0.1, aprox: [224, 9] },
  T: { id: 'T', cadeira: 'cad_dom_T', x: 240, sy: 22, face: 'up',    sort: 0.1, aprox: [240, 27], sobre: 'cad_dom_T_enc' },
};
RD.ordem = ['E', 'T', 'D', 'F'];                       // sentido anti-horário; E e D são dupla (de frente), T e F a outra
RD.dupla = { E: 0, D: 0, T: 1, F: 1 };
RD.jogo = {
  raimundo: { pensa: [3.2, 6.0], agro: .2, fala: .35 }, ze: { pensa: [1.4, 3.2], agro: .7, fala: .6 },
  nonato: { pensa: [1.6, 3.6], agro: .9, fala: .9 }, bela: { pensa: [2.2, 4.4], agro: .3, fala: .4 }, cicera: { pensa: [2.0, 4.6], agro: .5, fala: .6 },
  lia: { pensa: [0, 0], agro: .5, fala: 0 },
};
// outros assentos da rua
RD.assentosRua = {
  cad_calcada_1: { x: 1088, sy: 10, face: 'left',  anim: 'sit', aprox: [1086, 12] },
  banco_a:       { x: 548,  sy: 14, face: 'down',  anim: 'sit', aprox: [548, 22] },
  banco_b:       { x: 576,  sy: 14, face: 'down',  anim: 'sit', aprox: [576, 22] },
  banquinho_1:   { x: 292,  sy: 12, face: 'left',  anim: 'sit', aprox: [304, 17] },
  banquinho_2:   { x: 182,  sy: 21, face: 'right', anim: 'sit', aprox: [172, 24] },
};

// ---- pontos nomeados ----
RD.spots = {
  borda_E: { x: 8, sy: 14, face: 'right' }, borda_D: { x: 1118, sy: 24, face: 'left' },
  porta_b0: { x: 72, sy: 10, face: 'up' }, porta_sobrado: { x: 164, sy: 10, face: 'up' }, porta_padaria: { x: 470, sy: 9, face: 'up' }, porta_lateral: { x: 614, sy: 10, face: 'up' },
  porta_assoc: { x: 756, sy: 10, face: 'up' }, porta_verde: { x: 846, sy: 10, face: 'up' }, porta_b5: { x: 990, sy: 10, face: 'up' },
  obs_1: { x: 192, sy: 18, face: 'right' }, obs_2: { x: 294, sy: 22, face: 'left' }, obs_3: { x: 200, sy: 21, face: 'right' }, obs_4: { x: 278, sy: 22, face: 'left' },
  varal: { x: 1078, sy: 10, face: 'up' }, sombra_oiti: { x: 1063, sy: 24, face: 'down' },
  gato: { x: 176, sy: 15, face: 'right' }, poste_1: { x: 114, sy: 27, face: 'right' }, orelhao: { x: 612, sy: 20, face: 'up' }, quadro: { x: 718, sy: 14, face: 'up' },
  fachada_sobrado: { x: 206, sy: 22, face: 'up' }, fachada_padaria: { x: 400, sy: 20, face: 'up' }, fachada_azul: { x: 700, sy: 21, face: 'up' },
  v1: { x: 340, sy: 20, face: 'right' }, v2: { x: 450, sy: 21, face: 'right' }, v3: { x: 560, sy: 22, face: 'right' }, v4: { x: 690, sy: 21, face: 'right' }, v5: { x: 830, sy: 21, face: 'right' }, v6: { x: 1010, sy: 22, face: 'right' },
  rua_1: { x: 300, sy: 36, face: 'right' }, rua_2: { x: 520, sy: 38, face: 'left' }, rua_3: { x: 760, sy: 36, face: 'right' },
  pombos: { x: 470, sy: 40, face: 'right' },
};

// ---- agenda: tarefas em sequência. t = hora mínima para começar (min) · jit = variação ±min ----
// tipos: sair(porta) · ir(spot) · sentar(assento) · levantar · entrar(porta, dur) · esperar(dur, anim) · olhar_mesa(dur) · conversar(com, dur) · ate(t) · patrulha(spots, ate)
const A = (t, tipo, o) => Object.assign({ t: T(t), tipo }, o || {});
RD.agenda = {
  raimundo: [A('07:03', 'sair', { porta: 'porta_sobrado' }), A('07:04', 'sentar', { assento: 'E' }), A('08:40', 'levantar'), A('08:40', 'ir', { spot: 'porta_padaria' }), A('08:41', 'entrar', { porta: 'porta_padaria', dur: 14 }),
             A('08:56', 'sair', { porta: 'porta_padaria' }), A('08:57', 'sentar', { assento: 'E' }), A('09:58', 'levantar'), A('09:58', 'ir', { spot: 'porta_sobrado' }), A('10:00', 'entrar', { porta: 'porta_sobrado', dur: 300 })],
  ze:       [A('07:00', 'sair', { porta: 'porta_b0' }), A('07:01', 'sentar', { assento: 'D' })],
  nonato:   [A('07:00', 'sair', { porta: 'porta_verde' }), A('07:01', 'sentar', { assento: 'F' }), A('11:20', 'levantar'), A('11:20', 'ir', { spot: 'porta_verde' }), A('11:21', 'entrar', { porta: 'porta_verde', dur: 300 })],
  bela:     [A('07:06', 'sair', { porta: 'porta_assoc' }), A('07:07', 'sentar', { assento: 'T' }), A('10:00', 'levantar'), A('10:00', 'ir', { spot: 'porta_lateral' }), A('10:01', 'entrar', { porta: 'porta_lateral', dur: 300 })],
  cicera:   [A('07:00', 'sair', { porta: 'porta_b5' }), A('07:01', 'ir', { spot: 'varal' }), A('07:02', 'esperar', { dur: 22, anim: 'hang' }), A('07:30', 'sentar', { assento: 'cad_calcada_1' }), A('10:02', 'levantar'), A('10:02', 'ir', { spot: 'obs_2' }),
             A('10:03', 'sentar', { assento: 'T', espera: true }), A('11:40', 'levantar'), A('11:40', 'ir', { spot: 'porta_b5' }), A('11:41', 'entrar', { porta: 'porta_b5', dur: 300 })],
  junior:   [A('07:00', 'sair', { porta: 'porta_b5' }), A('07:01', 'patrulha', { spots: ['gato', 'poste_1', 'obs_2', 'rua_1', 'sombra_oiti', 'v3', 'rua_3', 'v5', 'obs_1'], ate: T('08:55') }), A('08:55', 'ir', { spot: 'porta_b5' }), A('08:56', 'entrar', { porta: 'porta_b5', dur: 6 }),
             A('09:03', 'sair', { porta: 'porta_b5' }), A('09:04', 'patrulha', { spots: ['gato', 'v1', 'obs_2', 'rua_2', 'poste_1', 'sombra_oiti', 'v4', 'obs_3'], ate: T('11:50') })],
  tonho:    [A('07:15', 'sair', { porta: 'borda_E' }), A('07:16', 'patrulha', { spots: ['v1', 'obs_2', 'v2', 'v3', 'v4', 'v5', 'sombra_oiti', 'v6', 'v5', 'v4', 'v3', 'v2', 'obs_1'], ate: T('11:25'), vende: true }), A('11:26', 'ir', { spot: 'borda_D' }), A('11:27', 'entrar', { porta: 'borda_D', dur: 300 })],
  dandara:  [A('07:44', 'sair', { porta: 'borda_E' }), A('07:45', 'ir', { spot: 'obs_1' }), A('07:46', 'conversar', { com: 'raimundo', dur: 4 }), A('07:51', 'ir', { spot: 'porta_assoc' }), A('07:53', 'entrar', { porta: 'porta_assoc', dur: 85 }),
             A('09:20', 'sair', { porta: 'porta_assoc' }), A('09:21', 'ir', { spot: 'quadro' }), A('09:22', 'esperar', { dur: 4, anim: 'interact' }), A('09:27', 'ir', { spot: 'porta_padaria' }), A('09:28', 'entrar', { porta: 'porta_padaria', dur: 34 }),
             A('10:04', 'sair', { porta: 'porta_padaria' }), A('10:05', 'ir', { spot: 'obs_2' }), A('10:06', 'olhar_mesa', { dur: 8 }), A('10:15', 'ir', { spot: 'borda_E' }), A('10:30', 'entrar', { porta: 'borda_E', dur: 300 })],
  lucia:    [A('08:00', 'sair', { porta: 'borda_D' }), A('08:01', 'ir', { spot: 'fachada_azul' }), A('08:02', 'esperar', { dur: 9, anim: 'interact' }), A('08:12', 'ir', { spot: 'fachada_padaria' }), A('08:13', 'esperar', { dur: 10, anim: 'interact' }),
             A('08:25', 'ir', { spot: 'fachada_sobrado' }), A('08:26', 'esperar', { dur: 9, anim: 'interact' }), A('08:37', 'conversar', { com: 'raimundo', dur: 3 }), A('08:42', 'sentar', { assento: 'banco_a' }), A('09:25', 'levantar'),
             A('09:26', 'ir', { spot: 'orelhao' }), A('09:27', 'esperar', { dur: 4, anim: 'talk' }), A('09:33', 'ir', { spot: 'borda_D' }), A('09:50', 'entrar', { porta: 'borda_D', dur: 300 })],
};


// ---- agenda do MUNDO INTEGRADO (Etapa 7): quem entra na padaria só sai quando a simulação da padaria liberar; Raimundo só sai de casa quando a casa liberar ----
// `aguarda` = chave de liberação (casa | padaria). O resto é a agenda aprovada da Etapa 6. Lúcia ganha uma visita à padaria (08:24) depois de medir a fachada.
RD.visitas = { raimundo: [14, 20], dandara: [30, 40], lucia: [9, 13] };
// Tarde (12h–19h). Em 1991 a rua segue viva: quem foi para casa volta, a mesa de dominó reabre e Dandara e Lúcia passam na padaria.
// Em 1994 o elenco está no caruru da Dona Zefa (quintal), então sai da rua a tempo de chegar lá e não volta: ninguém aparece em dois ambientes.
// `aguarda` = só sai quando o outro ambiente liberar (padaria ou casa).
const SPOTS_J = ['gato', 'v2', 'obs_2', 'rua_2', 'poste_1', 'v4', 'sombra_oiti', 'rua_3', 'obs_3'];
const SPOTS_TONHO = ['v6', 'v5', 'v4', 'v3', 'obs_2', 'v2', 'v1', 'obs_1', 'sombra_oiti', 'v6'];
RD.tarde = {
  1991: {
    raimundo: [A('15:00', 'sair', { porta: 'porta_sobrado', aguarda: 'casa' }), A('15:01', 'sentar', { assento: 'E' }), A('17:30', 'levantar'), A('17:30', 'ir', { spot: 'porta_sobrado' }), A('17:32', 'entrar', { porta: 'porta_sobrado' })],
    ze:       [A('17:40', 'levantar'), A('17:41', 'ir', { spot: 'porta_b0' }), A('17:43', 'entrar', { porta: 'porta_b0' })],
    nonato:   [A('14:30', 'sair', { porta: 'porta_verde' }), A('14:31', 'sentar', { assento: 'F' }), A('17:20', 'levantar'), A('17:20', 'ir', { spot: 'porta_verde' }), A('17:22', 'entrar', { porta: 'porta_verde' })],
    cicera:   [A('14:40', 'sair', { porta: 'porta_b5' }), A('14:41', 'ir', { spot: 'obs_2' }), A('14:43', 'sentar', { assento: 'T' }), A('17:00', 'levantar'), A('17:01', 'ir', { spot: 'porta_b5' }), A('17:03', 'entrar', { porta: 'porta_b5' })],
    junior:   [A('14:00', 'patrulha', { spots: SPOTS_J, ate: T('18:30') }), A('18:31', 'ir', { spot: 'porta_b5' }), A('18:33', 'entrar', { porta: 'porta_b5' })],
    tonho:    [A('14:10', 'sair', { porta: 'borda_D' }), A('14:11', 'patrulha', { spots: SPOTS_TONHO, ate: T('18:00'), vende: true }), A('18:01', 'ir', { spot: 'borda_E' }), A('18:03', 'entrar', { porta: 'borda_E' })],
    dandara:  [A('14:20', 'sair', { porta: 'borda_E' }), A('14:21', 'ir', { spot: 'obs_2' }), A('14:22', 'olhar_mesa', { dur: 8 }), A('14:35', 'ir', { spot: 'porta_padaria' }), A('14:36', 'entrar', { porta: 'porta_padaria', dur: 34 }),
               A('15:15', 'sair', { porta: 'porta_padaria', aguarda: 'padaria' }), A('15:16', 'ir', { spot: 'quadro' }), A('15:17', 'esperar', { dur: 4, anim: 'interact' }), A('15:25', 'ir', { spot: 'borda_E' }), A('15:40', 'entrar', { porta: 'borda_E' })],
    lucia:    [A('15:30', 'sair', { porta: 'borda_D' }), A('15:31', 'ir', { spot: 'fachada_azul' }), A('15:32', 'esperar', { dur: 9, anim: 'interact' }), A('15:45', 'ir', { spot: 'porta_padaria' }), A('15:46', 'entrar', { porta: 'porta_padaria' }),
               A('16:05', 'sair', { porta: 'porta_padaria', aguarda: 'padaria' }), A('16:06', 'sentar', { assento: 'banco_a' }), A('17:10', 'levantar'), A('17:11', 'ir', { spot: 'orelhao' }), A('17:12', 'esperar', { dur: 4, anim: 'talk' }), A('17:20', 'ir', { spot: 'borda_D' }), A('17:40', 'entrar', { porta: 'borda_D' })],
  },
  1994: {
    raimundo: [A('12:45', 'sair', { porta: 'porta_sobrado', aguarda: 'casa' }), A('12:46', 'ir', { spot: 'porta_lateral' }), A('12:50', 'entrar', { porta: 'porta_lateral' })],
    ze:       [A('11:50', 'levantar'), A('11:51', 'ir', { spot: 'porta_b0' }), A('11:53', 'entrar', { porta: 'porta_b0' })],
    junior:   [A('11:51', 'ir', { spot: 'porta_b5' }), A('11:53', 'entrar', { porta: 'porta_b5' })],
  },
};
RD.agendaMundo = () => {
  const ag = JSON.parse(JSON.stringify(RD.agenda));
  const ano = (typeof window !== 'undefined' && window.MUNDO_ANO === 1994) ? 1994 : 1991;
  const sairPad = i => Object.assign({}, i, { aguarda: 'padaria' });
  ag.raimundo = ag.raimundo.map(t => t.tipo === 'sair' && t.porta === 'porta_sobrado' ? Object.assign({}, t, { aguarda: 'casa' }) : t.tipo === 'sair' && t.porta === 'porta_padaria' ? sairPad(t) : t);
  ag.dandara = ag.dandara.map(t => t.tipo === 'sair' && t.porta === 'porta_padaria' ? sairPad(t) : t);
  const k = ag.lucia.findIndex(t => t.tipo === 'ir' && t.spot === 'fachada_sobrado');
  ag.lucia.splice(k, 0, A('08:24', 'ir', { spot: 'porta_padaria' }), A('08:24', 'entrar', { porta: 'porta_padaria' }), A('08:25', 'sair', { porta: 'porta_padaria', aguarda: 'padaria' }));
  if (ano === 1994 && RD.virar94) RD.virar94();
  const tarde = RD.tarde[ano]; for (const id in tarde) ag[id] = ag[id].concat(tarde[id].map(t => Object.assign({}, t)));
  return ag;
};

// ---- falas (PROPOSTA). quando: conf [min,max] = nível de confiança em Lia 0..3 ----
RD.falas = {
  raimundo: {
    saudar: ['Bom dia, Lia. Senta aí, mas fala baixo que o Zé tá armando.', 'Ei, Lia. Tá vendo esse jogo? Tá mais devagar que fila de banco.'],
    ouvir: ['(Seu Raimundo ajeita as pedras na mão e olha a mesa sem pressa.)', '(Ele bate de leve o dedo no tampo, pensando.)'],
    perguntar: {
      jogo: [{ t: 'Dominó é conta e é paciência. Quem tem pressa joga a pedra errada.', kp: 'kp_dom_paciencia' }, { t: 'Aprendi com meu pai, nessa mesma calçada, quando aqui ainda tinha lampião a gás.', conf: [2, 3], kp: 'kp_dom_pai' }],
      rua: [{ t: 'A rua mudou de pintura, mas as pessoas são as mesmas.', kp: null }],
      sobrado: [{ t: 'O sobrado é o que a gente tem. Mexeram na casa do lado e eu fiquei olhando, quieto. Eles medem tudo, mas não perguntam nada.', kp: 'kp_ray_sobrado' }],
    },
    ajudar: [],
  },
  ze: {
    saudar: ['Bom dia, menina! Vai ficar olhando ou vai aprender?', 'Olha a Lia! Fica aí, mas não sopra jogada, hein.'],
    ouvir: ['(Seu Zé ri sozinho, olhando as próprias pedras.)'],
    perguntar: {
      jogo: [{ t: 'Dupla joga de frente: eu e Raimundo contra Nonato e Bela. Parceiro fala com a pedra, não com a boca.', kp: 'kp_dom_dupla' }, { t: 'Bate de carroça vale dois. De lá e lô, três. Cruzada, quatro, e aí a mesa treme.', conf: [1, 3], kp: 'kp_dom_batidas' }],
      barbearia: [{ t: 'A barbearia é a minha casa de dia. De noite, é a de Dona Marta, minha sombra.', kp: null }],
      lia_jogar: [{ t: 'Quer jogar? Quando um de nós levantar, a gente vê. Primeiro prova que sabe contar até seis.', kp: 'kp_dom_convite' }],
    },
  },
  nonato: {
    saudar: ['E aí, Lia! Chegou pra ver eu ganhar?', 'Fala, Lia! Hoje eu tô com a mão boa.'],
    ouvir: ['(Nonato bate a pedra com força e olha em volta, esperando aplauso.)'],
    perguntar: {
      jogo: [{ t: 'Bato de carroça toda vez que posso. Dá mais ponto e dá mais vergonha nos outros.', kp: null }],
      obra: [{ t: 'Aquele monte de tijolo é meu. Tô refazendo o reboco da casa de uma tia. Pago com café, não com dinheiro.', kp: 'kp_obra_tijolo' }],
    },
  },
  bela: {
    saudar: ['Bom dia, Lia. Senta direito, minha filha.', 'Oi, meu bem. Tá aprendendo ou só passeando?'],
    ouvir: ['(Dona Bela confere cada pedra duas vezes antes de jogar.)'],
    perguntar: {
      jogo: [{ t: 'Não adianta gritar. Quem conta as pedras que já saíram sabe o que sobra.', kp: 'kp_dom_contar' }],
      costura: [{ t: 'Eu costuro na máquina da janela do alto. Daqui eu vejo o jogo e o movimento. O que passa na rua passa pela minha agulha.', kp: null }],
      rua: [{ t: 'A rua tá sendo olhada por gente de fora. Tem uns que olham pra ajudar e uns que olham pra comprar. Eu ainda não sei qual é qual.', kp: 'kp_rua_olhar', revisar: true }],
    },
  },
  cicera: {
    saudar: ['Menina, tu sumiu! Vem ajudar a esticar esse lençol.', 'Bom dia, Lia! Tá vendo o sol? Roupa seca em dez minutos.'],
    ouvir: ['(Cícera cantarola e prende uma toalha com os pregadores.)'],
    perguntar: {
      varal: [{ t: 'Lavo pra meia rua. Cada pano tem dono; eu conheço pelo cheiro.', kp: 'kp_varal' }],
      junior: [{ t: 'Júnior é meu neto e não para quieto. Se ele passar por aqui, manda ele voltar.', kp: null }],
      jogo: [{ t: 'Às dez eu entro no lugar de Bela, que vai fazer o almoço. Dominó é a hora que eu sento sem culpa.', kp: 'kp_cicera_dom' }],
    },
  },
  junior: {
    saudar: ['Oi, Lia! Quer ver o gato?', 'Lia! Corre comigo até o poste!'],
    ouvir: ['(Júnior pula num pé só ao redor do poste.)'],
    perguntar: {
      gato: [{ t: 'O gato não tem nome. Tem vários. Cada casa chama de um jeito.', kp: 'kp_gato' }],
      jogo: [{ t: 'Os velhos brigam e depois riem. Eu acho que eles gostam é de brigar.', kp: null }],
    },
  },
  tonho: {
    saudar: ['Cocada, queijadinha! Quer provar, Lia?', 'Bom dia! Hoje a cocada saiu com mais coco.'],
    ouvir: ['(Tonho ajeita a caixa de isopor no ombro e olha pro céu, vendo se vai esquentar.)'],
    perguntar: {
      cocada: [{ t: 'Minha mãe faz de madrugada. Eu só carrego e sorrio. O sorriso vende mais que o açúcar.', kp: 'kp_cocada' }],
      rua: [{ t: 'Cada ponto da rua tem seu horário. Na sombra do beiral, antes das dez; perto do dominó, depois, quando perdem.', kp: 'kp_pontos_venda' }],
    },
  },
  dandara: {
    saudar: ['Lia, bom dia. Tem um minuto? A reunião é hoje à noite e preciso de mais assinaturas.', 'Lia. A associação tá aberta, entra quando quiser.'],
    ouvir: ['(Dandara folheia o caderno de capa dura, procurando um nome.)'],
    perguntar: {
      associacao: [{ t: 'É uma casa comum. Quem não tem advogado, tem a gente. O quadro de avisos é nosso jornal.', kp: 'kp_associacao' }],
      programa: [{ t: 'O Programa de recuperação vai pintar e consertar. Eu quero que quem mora aqui continue morando. Isso não está escrito em lugar nenhum.', kp: 'kp_programa', revisar: true }],
    },
  },
  lucia: {
    saudar: ['Bom dia. Se você não se importa, preciso medir esta parede.', 'Oi. Hoje o dia é longo; a prancheta, mais ainda.'],
    ouvir: ['(Lúcia anota algo, mede de novo, anota de novo.)'],
    perguntar: {
      medir: [{ t: 'Eu meço para ninguém ser surpreendido: tamanho da porta, da janela, do telhado. Depois tudo vira número no relatório.', kp: 'kp_lucia_medir' }],
      programa: [{ t: 'O Programa não decide a vida de ninguém. Mas o relatório pode decidir uma obra. Eu quero que ele seja honesto.', kp: 'kp_lucia_programa', revisar: true }],
    },
  },
};
// conversas espontâneas entre pessoas (pares, linhas alternadas)
RD.papos = [
  ['dandara>raimundo', ['Bom dia, Seu Raimundo. O senhor vai à reunião de hoje?', 'Se o Zé deixar eu sair da mesa, vou sim.']],
  ['lucia>raimundo', ['Seu Raimundo, posso medir a calçada do sobrado?', 'Pode, minha filha. Só não leva a rua embora na prancheta.']],
  ['cicera>junior', ['Júnior! Vem cá, menino!', 'Já vou, vó! Só vou ver o gato!']],
  ['tonho>nonato', ['Cocada, Nonato?', 'Depois do jogo, que eu perco a concentração.']],
];
// bolhas de dominó (curtas e espaçadas)
RD.dom = {
  passa: ['Passo.', 'Passei.', '(bate na mesa)', 'Sem pedra.'],
  joga: ['Essa.', 'Joguei.', 'Vai!', 'Toma.'],
  bate: { simples: ['Bati!', 'Acabou!'], carroca: ['Bati de carroça!', 'Carroça!'], laelo: ['De lá e lô!', 'Lá e lô!'], cruzada: ['Cruzada! Quatro!', 'Cruzada!'] },
  tranca: ['Trancou!', 'Ninguém joga mais.'],
  reage_bom: ['Boa, parceiro!', 'Isso!', 'Assim se joga.'], reage_ruim: ['Era essa mesmo?', 'Ai, ai.', 'Vai começar...'],
};
// pontos de conhecimento (vão para as anotações da rua)
// lata colaborativa do bairro, explicada a Lia antes da primeira mão (proposta · revisar com leitura cultural)
RD.lata = [
  ['nonato', 'Antes de embaralhar: a lata passou por aqui hoje?'],
  ['raimundo', 'Passou. Pus a minha. O gás da Dona Cícera acaba essa semana.'],
  ['ze', 'Menina, a lata é assim. Cada um deixa o que pode, e quem está apertado leva o que precisa, sem ter que explicar.'],
  ['bela', 'Fica na mesa da Dona Áurea. Todo mundo sabe onde está e ninguém mexe sem precisar.'],
  ['nonato', 'Eu ainda queria um caderno. Quanto entrou, quanto saiu, tudo escrito.'],
  ['raimundo', 'Com caderno a lata vira cobrança, Nonato. Do jeito que está, ela anda na confiança.'],
  ['bela', 'E de gente que lembra de repor quando o mês melhora.'],
  ['ze', 'Pronto, resolvido. Agora eu embaralho.'],
];
RD.kp = {
  kp_lata: ['A lata do bairro', 'Na mesa do dominó se explica a lata: quem pode põe um trocado, quem aperta tira, sem perguntar. Nonato queria caderno; Raimundo e Bela preferem a confiança.'],
  kp_dom_paciencia: ['Dominó pede paciência', 'Seu Raimundo joga devagar de propósito: quem tem pressa joga a pedra errada.'],
  kp_dom_pai: ['A mesa do pai', 'Seu Raimundo aprendeu dominó com o pai, na mesma calçada, no tempo do lampião a gás.'],
  kp_ray_sobrado: ['O sobrado e as medições', 'Seu Raimundo viu a casa do lado ser medida e ninguém perguntou nada a quem mora.'],
  kp_dom_dupla: ['Dupla de frente', 'No dominó da rua, os parceiros sentam de frente: Zé com Raimundo contra Nonato com Bela.'],
  kp_dom_batidas: ['Tipos de batida', 'Batida simples vale 1; de carroça (com dobrada), 2; de lá e lô (a pedra serve nas duas pontas), 3; cruzada (dobrada nas duas pontas), 4.'],
  kp_dom_convite: ['Um lugar na mesa', 'Seu Zé deixa Lia jogar quando alguém levantar: precisa mostrar que sabe contar.'],
  kp_dom_contar: ['Contar as pedras', 'Dona Bela conta as pedras que já saíram para saber o que ainda pode vir.'],
  kp_obra_tijolo: ['A pilha de tijolos', 'O monte de tijolos e cimento é de Nonato, que refaz o reboco da casa de uma tia e cobra em café.'],
  kp_rua_olhar: ['Olhares de fora', 'Dona Bela nota gente de fora olhando as casas e ainda não sabe se vem ajudar ou comprar.'],
  kp_varal: ['O varal de Cícera', 'Cícera lava roupa para meia rua e reconhece cada pano pelo cheiro.'],
  kp_cicera_dom: ['O dominó de Cícera', 'Por volta das dez, Cícera entra no lugar de Bela, que vai fazer o almoço.'],
  kp_gato: ['O gato sem nome', 'Cada casa chama o gato de um jeito: ele não tem nome, tem vários.'],
  kp_cocada: ['A cocada de Tonho', 'A mãe de Tonho faz as cocadas de madrugada; ele só carrega e sorri.'],
  kp_pontos_venda: ['Pontos de venda', 'Na sombra do beiral antes das dez; junto ao dominó depois, quando alguém perde.'],
  kp_associacao: ['A associação', 'A associação é a casa de quem não tem advogado; o quadro de avisos é o jornal da rua.'],
  kp_programa: ['O Programa e quem mora', 'Dandara quer que quem mora continue morando; isso não está escrito em nenhum papel.'],
  kp_lucia_medir: ['Lúcia mede tudo', 'Lúcia mede portas, janelas e telhados para que ninguém seja surpreendido pelo relatório.'],
  kp_lucia_programa: ['Um relatório honesto', 'Lúcia sabe que o relatório pode decidir uma obra e quer que ele seja honesto.'],
  kp_obj_mesa: ['As marcas da mesa', 'O tampo verde da mesa de dominó tem marcas de anos de partidas: cada riscado é uma batida.'],
  kp_obj_quadro: ['O quadro de avisos', 'Reunião da associação à noite, rifa de uma geladeira, aviso de falta d\'água, aluguel de cômodo.'],
  kp_obj_orelhao: ['O orelhão', 'O orelhão de ficha é o telefone de quase toda a rua; o número rabiscado na cúpula é de um sobrinho do bairro.'],
  kp_obj_poste: ['O poste dos cartazes', 'O poste de concreto serve de jornal: festa, achado, perdido, show.'],
  kp_obj_gaiola: ['A gaiola do sobrado', 'A gaiola ao lado da porta do sobrado tem um canário que canta antes de Seu Raimundo acordar.'],
  kp_obj_cavalete: ['O cavalete da padaria', 'O cavalete da padaria tem letra da Vó e o preço do dia.'],
  kp_obj_bike: ['A bicicleta de entrega', 'A bicicleta com cesto de vime é de um entregador da vizinhança.'],
  kp_obj_lixeira: ['A lixeira de tela', 'A lixeira de tela guarda copo de café e saco de pão: a rua come da padaria.'],
  kp_obj_obra: ['Tijolos e sacos de cimento', 'O reboco de uma casa da rua está sendo refeito aos poucos.'],
  kp_obj_caixote: ['Caixote de laranjas', 'O caixote de laranjas-bahia foi deixado ali pelo menino da banca.'],
};
RD.verbos = { jogo: 'O jogo de dominó', rua: 'A rua', sobrado: 'O sobrado', barbearia: 'A barbearia', lia_jogar: 'Jogar com eles', obra: 'A obra dos tijolos', costura: 'Costura', varal: 'O varal', junior: 'O menino', gato: 'O gato', cocada: 'A cocada', associacao: 'A associação', programa: 'O Programa', medir: 'Medir tudo' };
})();

// ---- assuntos CONTEXTUAIS (PROPOSTA): só aparecem se a Lia tem um motivo, e ela diz qual é ----
// viv = vivências da Lia (viu_jogo, viu_medicao, viu_varal, viu_tonho, viu_junior, viu_gato, viu_obra, viu_aviso, ouviu_programa, ouviu_reuniao)
// quando: lista de requisitos (qualquer um basta) · 'apos:id:topico' = depois de já ter conversado sobre aquilo com a pessoa · 'nivel:N' = confiança mínima
Sim.Rua.D.gates = {
  raimundo: {
    rua: { label: 'A rua', quando: [], ask: 'Seu Raimundo, como o senhor vê a rua hoje?' },
    jogo: { label: 'O jogo', quando: ['viu_jogo'], ask: 'Fiquei olhando a mesa. O senhor joga há muito tempo?' },
    sobrado: { label: 'O sobrado', quando: ['viu_medicao'], ask: 'Vi uma moça medindo as casas aqui perto. O senhor mora no sobrado ao lado, né? Como é isso pra o senhor?' },
  },
  ze: {
    jogo: { label: 'O jogo', quando: ['viu_jogo'], ask: 'Seu Zé, como é essa história de dupla? Fiquei olhando e não entendi.' },
    barbearia: { label: 'A barbearia', quando: ['apos:ze:jogo', 'nivel:1'], ask: 'O senhor falou em barbearia... é sua?' },
    lia_jogar: { label: 'Posso jogar?', quando: ['apos:ze:jogo'], ask: 'Seu Zé, se faltar um na mesa, eu posso jogar?' },
  },
  nonato: {
    jogo: { label: 'O jogo', quando: ['viu_jogo'], ask: 'Nonato, você comemorou tão alto... dá pra explicar essa batida?' },
    obra: { label: 'A obra', quando: ['viu_obra'], ask: 'Vi uma obra aqui na calçada. É sua?' },
  },
  bela: {
    jogo: { label: 'O jogo', quando: ['viu_jogo'], ask: 'Dona Bela, a senhora conta as pedras de cabeça?' },
    costura: { label: 'A costura', quando: ['apos:bela:jogo', 'nivel:1'], ask: 'A senhora costura, não é? Dá pra ver pela mão que não para.' },
    rua: { label: 'A rua', quando: ['viu_medicao', 'apos:bela:costura'], ask: 'A senhora falou em quem olha a rua de fora. Quem é?' },
  },
  cicera: {
    varal: { label: 'O varal', quando: ['viu_varal'], ask: 'Dona Cícera, vi a senhora no varal. Sempre foi aqui na calçada?' },
    junior: { label: 'O Júnior', quando: ['viu_junior'], ask: 'Aquele menino que corre pela rua é seu neto?' },
    jogo: { label: 'O jogo', quando: ['viu_jogo'], ask: 'A senhora também joga, Dona Cícera?' },
  },
  junior: {
    gato: { label: 'O gato', quando: ['viu_gato'], ask: 'Júnior, aquele gato é de quem?' },
    jogo: { label: 'O jogo', quando: ['viu_jogo'], ask: 'Você entende o jogo? Eu fiquei curiosa.' },
  },
  tonho: {
    cocada: { label: 'A cocada', quando: ['viu_tonho'], ask: 'Tonho, a cocada é sua mesmo ou você vende pra alguém?' },
    rua: { label: 'A rua', quando: ['apos:tonho:cocada'], ask: 'Você roda a rua todo dia. Onde vende melhor?' },
  },
  dandara: {
    associacao: { label: 'A associação', quando: ['viu_aviso', 'ouviu_reuniao'], ask: 'Dandara, vi um aviso no quadro. É da associação?' },
    programa: { label: 'O Programa', quando: ['ouviu_programa'], ask: 'Dandara, ouvi falarem de um Programa. O que é isso?' },
  },
  lucia: {
    medir: { label: 'As medições', quando: ['viu_medicao'], ask: 'Eu vi a senhora medindo as fachadas. Pode me explicar o que está fazendo?' },
    programa: { label: 'O Programa', quando: ['ouviu_programa', 'apos:lucia:medir'], ask: 'Ouvi falar do Programa. É por causa dele que a senhora mede tudo?' },
  },
};
Sim.Rua.D.dicaSemAssunto = 'Você ainda não tem um motivo para puxar esse assunto. Observe a rua, examine o que há por perto, e volte.';

// ================================================================ 1994
// 1992–1995: o Programa acelera (obra pesada, casa interditada, moradores saindo). Em 1991 a rua só recebe a notícia; em 1994 ela já mostra o efeito.
// A aposta desta etapa: turistas do Brasil e de fora sustentariam o comércio local sozinhos. As falas daqui são proposta de texto e passam por revisão cultural/histórica.
Sim.Rua.D.virar94 = () => {
  const RD = Sim.Rua.D; if (RD._v94) return; RD._v94 = true;
  if (Sim.Social && Sim.Social.virar94) Sim.Social.virar94();
  const F = RD.falas, G = RD.gates;
  const abre = (id, topicos, label, ask, quando) => { G[id] = G[id] || {}; G[id][topicos] = { label, quando: quando || [], ask }; };
  RD.kpRev = {};
  const kp = (id, titulo, texto, rev) => { RD.kp[id] = [titulo, texto]; if (rev) RD.kpRev[id] = 1; };
  // ---- anotações 1994 (substituem as de 1991 que não valem mais) ----
  ['kp_ray_sobrado', 'kp_rua_olhar', 'kp_programa', 'kp_lucia_programa', 'kp_obra_tijolo'].forEach(k => delete RD.kp[k]);
  kp('kp_94_ray_aviso', 'O aviso na porta', 'Colaram um aviso na porta do sobrado de Seu Raimundo: a casa está em risco. Ele recebeu oferta de indenização e de uma casa longe do centro, e ainda não assinou.', true);
  kp('kp_94_ray_vazias', 'As casas da rua de cima', 'Quem aceitou a indenização foi para o subúrbio. A rua de cima está quase toda fechada e quase ninguém volta para jogar dominó.', true);
  kp('kp_94_ray_marca', 'A marca de tinta', 'O sobrado de Seu Raimundo foi marcado com um X de tinta laranja pelos técnicos da obra.', true);
  kp('kp_94_ze_foto', 'A cadeira que vira foto', 'Na barbearia entra turista para fotografar a cadeira. Corte mesmo, só os de sempre, e esses estão saindo da rua.', true);
  kp('kp_94_nonato_obra', 'Obra por empreita', 'Nonato trabalha por empreita nas obras do Programa. Levanta a parede de uma casa cujos donos já saíram. Recebe por semana e o contrato acaba com a fachada.', true);
  kp('kp_94_bela_freguesas', 'As freguesas que saíram', 'Dona Bela perdeu metade da freguesia de costura com as mudanças. Entrega de ônibus e a passagem come o ganho.', true);
  kp('kp_94_rua_olhar', 'Câmera na janela', 'Turistas fotografam as janelas das casas onde as pessoas moram. Dona Bela ainda não decidiu se sorri ou fecha a janela.', true);
  kp('kp_94_cicera_varal', 'O varal mais curto', 'Dona Cícera lava para a metade da rua que lavava antes. Duas casas vizinhas ficaram vazias.');
  kp('kp_94_junior_casa', 'A casa fechada', 'Júnior entra pela janela de uma casa fechada da esquina. Ficaram uma cadeira, um prato na pia e um calendário na parede.');
  kp('kp_94_junior_foto', 'A foto com o gato', 'Um turista deu uma moeda a Júnior para ele aparecer em uma foto ao lado do gato.');
  kp('kp_94_tonho_turista', 'Turista só no fim de semana', 'Tonho vende o dobro no sábado e no domingo, quando chegam os ônibus de turistas. De terça a quinta, quase nada.', true);
  kp('kp_94_programa', 'Da pintura à remoção', 'Dandara conta que o Programa começou com pintura e conserto e agora tem obra pesada, casa interditada e gente indo embora.', true);
  kp('kp_94_lucia_ficha', 'A ficha vira valor', 'Lúcia agora faz a ficha de cada casa. A ficha alimenta o cadastro, e o cadastro define o valor da indenização.', true);
  kp('kp_94_lucia_aposta', 'A aposta no turista', 'O Programa apostava que turistas do Brasil e de fora sustentariam o comércio da rua sozinhos. Lúcia escreveu no relatório que ainda é cedo para saber.', true);
  kp('kp_94_lucia_evento', 'Conversa de corredor', 'No órgão do Programa já se fala em um evento maior, para trazer moradores de Salvador para a região. Ainda não há plano escrito.', true);
  kp('kp_94_dandara_dn', 'Pelourinho Dia & Noite', 'O Dia & Noite nasceu logo depois da entrega das primeiras etapas da reforma. O governo contrata artistas, grupos, companhias de teatro, dança e mestres de capoeira para show de graça todo dia nos largos. A ideia é rua cheia de dia e de noite para os bares, restaurantes e lojas de artesanato dos casarões girarem.', true);
  kp('kp_94_tonho_show', 'Quando o show acaba', 'Tonho vende antes e depois da roda de capoeira no Terreiro. Quando o grupo termina, a rua esvazia em dez minutos.', true);
  kp('kp_94_obj_dn', 'O cartaz do Dia & Noite', 'O cartaz do Pelourinho Dia & Noite lista a semana: roda de capoeira, banda, teatro e dança, de graça, no Terreiro de Jesus e nos largos Pedro Archanjo, Tereza Batista e Quincas Berro D\'Água.', true);
  kp('kp_associacao', 'A associação', 'A associação confere quem recebeu aviso, quem aceitou indenização e quem ainda mora na casa.');
  kp('kp_obj_quadro', 'O quadro de avisos', 'O quadro tem a convocação da reunião de sábado e uma lista das casas que receberam aviso.');
  kp('kp_obj_obra', 'Tijolos e sacos de cimento', 'A pilha de material é da empreiteira que trabalha no casarão da esquina.');
  kp('kp_94_obj_aviso', 'O papel da vistoria', 'O aviso colado no sobrado fala em vistoria, risco e prazo para desocupar. Tem carimbo e data.', true);
  kp('kp_94_obj_tapume', 'A casa tapada', 'A casa verde está com a porta e a janela baixa tapadas com tábua. O andaime sobe pela fachada inteira.');
  kp('kp_94_obj_placa', 'A placa da obra', 'A placa no andaime anuncia obra do Programa de Recuperação, com a data de 1994.');
  kp('kp_94_obj_faixa', 'Aqui mora gente', 'A associação pendurou na fachada uma faixa com a frase AQUI MORA GENTE.');
  kp('kp_94_obj_turista', 'A placa em inglês', 'A padaria ganhou uma placa pequena em português e em inglês, para quem vem de fora.');
  RD.kpObj94 = { quadro_avisos: 'kp_94_obj_dn', aviso_sobrado: 'kp_94_obj_aviso', marca_sobrado: 'kp_94_ray_marca', tapume_verde: 'kp_94_obj_tapume', placa_obra: 'kp_94_obj_placa', faixa_assoc: 'kp_94_obj_faixa', placa_padaria: 'kp_94_obj_turista' };
  // ---- falas e assuntos ----
  const eu = (id, saudar, ouvir, perguntar, ordem) => { F[id].saudar = saudar; F[id].ouvir = ouvir; Object.keys(F[id].perguntar).forEach(t => { if (t !== 'jogo' && t !== 'lia_jogar' && t !== 'gato') delete F[id].perguntar[t]; if (G[id]) { if (t !== 'jogo' && t !== 'lia_jogar' && t !== 'gato') delete G[id][t]; } }); Object.assign(F[id].perguntar, perguntar); };
  eu('raimundo', ['Lia. Senta aí. O jogo anda com pouca gente, o Zé até parou de reclamar.', 'Ô, Lia. Já viu o que colaram na minha porta?'],
    ['(Seu Raimundo olha a porta do sobrado e depois as pedras, sem jogar nenhuma.)', '(Ele passa o polegar na pedra devagar. Faz tempo que não joga a próxima.)'], {
      sobrado: [{ t: 'Colaram esse aviso na porta no mês passado. Diz que o sobrado corre risco de desabar, e corre mesmo, porque faz anos que não me deixam mexer no telhado. Me ofereceram indenização e uma casa longe daqui. Eu ainda não assinei.', kp: 'kp_94_ray_aviso', revisar: true }],
      rua: [{ t: 'A rua de cima já está quase toda fechada. Quem aceitou o dinheiro foi para o subúrbio, e de lá ninguém vem jogar dominó.', kp: 'kp_94_ray_vazias', revisar: true },
            { t: 'Os rapazes da obra me chamam de seu Raimundo e eu fico quieto. Eles marcaram a minha parede com um X de tinta. Fizeram isso sem bater na porta.', conf: [1, 3], revisar: true }],
    });
  abre('raimundo', 'sobrado', 'O aviso na porta', 'Seu Raimundo, que papel é esse na porta do sobrado?');
  abre('raimundo', 'rua', 'A rua de cima', 'Seu Raimundo, a rua de cima está tão vazia. O que aconteceu?');
  eu('ze', ['Bom dia, menina. Chegou cedo para o caruru da Zefa? Senta um minuto.', 'Lia! Vai na frente, que eu vou depois, quando a cadeira esfriar.'],
    ['(Seu Zé olha a rua, vê gente de câmera e passa um tempo sem falar.)'], {
      barbearia: [{ t: 'Entra turista para tirar foto da cadeira. Pergunta se pode sentar, senta, agradece e sai. Corte mesmo, só os de sempre, e esses estão saindo da rua.', kp: 'kp_94_ze_foto', revisar: true }],
    });
  abre('ze', 'barbearia', 'A barbearia', 'Seu Zé, o movimento da barbearia melhorou com os turistas?');
  eu('nonato', ['E aí, Lia! A mão tá boa, mas o tempo tá curto. A empreita não espera.'], ['(Nonato bate a pedra e olha o relógio de novo.)'], {
      obra: [{ t: 'Peguei empreita nas obras do Programa. Levanto parede de casa que o dono já deixou. Pagam por semana e o contrato vai até o fim da fachada. Depois não sei.', kp: 'kp_94_nonato_obra', revisar: true }],
    });
  abre('nonato', 'obra', 'A obra', 'Nonato, essa obra da esquina é a que você pegou?');
  eu('bela', ['Bom dia, Lia. Senta direito. A rua anda quieta e eu não gosto de rua quieta.'], ['(Dona Bela confere cada pedra duas vezes e olha a janela do alto.)'], {
      costura: [{ t: 'Costuro para muita gente que morava aqui. Metade da freguesia foi para longe, uma atrás da outra. Entrego de ônibus, e a passagem come o ganho da bainha.', kp: 'kp_94_bela_freguesas', revisar: true }],
      rua: [{ t: 'Turista fotografa a janela da minha casa. Eu fico sem saber se sorrio ou fecho a janela.', kp: 'kp_94_rua_olhar', revisar: true }],
    });
  abre('bela', 'costura', 'A costura', 'Dona Bela, as suas freguesas ainda moram por aqui?');
  abre('bela', 'rua', 'Gente de fora', 'Dona Bela, o que a senhora acha dessa gente de câmera na rua?', ['apos:bela:costura']);
  eu('cicera', ['Bom dia, Lia. Vem esticar esse lençol. O varal tá mais vazio que ano passado.'], ['(Cícera prende uma toalha e conta as casas da frente com o olhar.)'], {
      varal: [{ t: 'Eu lavava para meia rua e agora lavo para metade disso. O sobrado da esquina ficou vazio, e a casa da frente também. Pano sem dono eu não lavo.', kp: 'kp_94_cicera_varal' }],
      junior: [{ t: 'Júnior é meu neto e não para quieto. Entra pela janela das casas fechadas. Já mandei parar duas vezes.', kp: null }],
    });
  abre('cicera', 'varal', 'O varal', 'Dona Cícera, o varal está menor do que antes?');
  abre('cicera', 'junior', 'O Júnior', 'Dona Cícera, o Júnior anda por onde?');
  eu('junior', ['Oi, Lia! Eu achei uma casa vazia com calendário na parede!', 'Lia! Eu entrei na casa da esquina pela janela e tem um gato lá dentro. Não conta pra minha avó.'],
    ['(Júnior espia a janela da casa fechada e depois olha para a avó.)'], {
      casa: [{ t: 'Eu entrei pela janela da casa fechada da esquina. Tem cadeira, tem prato na pia e um calendário na parede. Eu fico lá com o gato quando minha avó não está olhando.', kp: 'kp_94_junior_casa' }],
      turista: [{ t: 'Um gringo me deu uma moeda para eu ficar do lado do gato na foto. Eu fiquei. Ele falou uma coisa que eu não entendi e riu.', kp: 'kp_94_junior_foto' }],
      gato: [{ t: 'O gato não tem nome. Eu levo pão pra ele na casa fechada, e ele me espera na janela.', kp: 'kp_gato' }],
    });
  abre('junior', 'casa', 'A casa fechada', 'Júnior, que casa vazia é essa?');
  abre('junior', 'turista', 'Os turistas', 'O pessoal de fora tira foto de você?');
  abre('junior', 'gato', 'O gato', 'Júnior, aquele gato é de quem?');
  eu('tonho', ['Cocada, queijadinha! Quer provar, Lia? Para turista eu cobro mais, mas para você não.'], ['(Tonho ajeita o isopor no ombro e olha para a rua, contando quem passa de câmera.)'], {
      cocada: [{ t: 'Minha mãe faz de madrugada. Eu só carrego e sorrio. O sorriso vende mais que o açúcar.', kp: 'kp_cocada' }],
      show: [{ t: 'Agora tem show de graça no Terreiro, quase todo dia, em hora diferente. Roda de capoeira de tarde, banda de noite. Eu vendo antes e depois. Quando o grupo acaba, em dez minutos a rua está vazia. Show de graça traz gente, mas gente que não gasta.', kp: 'kp_94_tonho_show', revisar: true }],
      rua: [{ t: 'Sábado e domingo eu vendo o dobro, porque vem ônibus de turista. De terça a quinta passa um ou outro, e a cocada volta no isopor. Se eu dependesse só disso, comia dois dias por semana.', kp: 'kp_94_tonho_turista', revisar: true }],
    });
  abre('tonho', 'cocada', 'A cocada', 'Tonho, a cocada é sua mesmo ou você vende para alguém?');
  abre('tonho', 'rua', 'O turista', 'Tonho, o turista compra bastante?');
  abre('tonho', 'show', 'Os shows no Terreiro', 'Tonho, o show no Terreiro ajuda a vender?', ['apos:tonho:rua']);
  eu('dandara', ['Lia, bom dia. A reunião é sábado e a lista de avisados tem mais nome do que eu esperava. Tem um minuto?'], ['(Dandara folheia o caderno de capa dura, riscando um nome e acrescentando outro.)'], {
      dn: [{ t: 'Isso é o Pelourinho Dia & Noite. Saiu logo depois que entregaram as primeiras etapas da reforma. O governo contrata artista, banda, grupo de teatro, de dança, mestre de capoeira, e põe todo dia da semana, em hora diferente, de graça, no Terreiro de Jesus e nos largos Pedro Archanjo, Tereza Batista e Quincas Berro D\'Água. A ideia é rua cheia de dia e de noite para o bar, o restaurante e a loja de artesanato dos casarões girarem. Eu vou aos shows. Pergunto só quem mora nesses casarões.', kp: 'kp_94_dandara_dn', revisar: true }],
      associacao: [{ t: 'Aqui a gente confere quem recebeu aviso, quem aceitou indenização e quem ainda está na casa. Quem não tem advogado tem a associação. O quadro de avisos hoje é lista de casa.', kp: 'kp_associacao' }],
      programa: [{ t: 'O Programa começou com pintura e conserto. Hoje é obra pesada, casa interditada e gente indo embora. A aposta é que o turista sustenta o comércio sozinho. Eu quero ver o caixa de quem vende aqui para saber.', kp: 'kp_94_programa', revisar: true }],
    });
  abre('dandara', 'associacao', 'A associação', 'Dandara, o que a associação está fazendo agora?');
  abre('dandara', 'programa', 'O Programa', 'Dandara, o que mudou no Programa desde que ele foi anunciado?');
  abre('dandara', 'dn', 'O Dia & Noite', 'Dandara, o que é esse palco montado no Terreiro de Jesus?');
  eu('lucia', ['Oi, Lia. Este ano eu assino mais ficha do que meço parede.', 'Bom dia, Lia. O dia está longo e as fichas estão cheias.'], ['(Lúcia confere uma ficha e a fecha devagar, sem dizer o que viu.)'], {
      medir: [{ t: 'Em 91 eu media para o relatório. Agora meço para saber o que se interdita. A ficha da casa vai para o cadastro, e do cadastro sai o valor da indenização.', kp: 'kp_94_lucia_ficha', revisar: true }],
      programa: [{ t: 'O Programa foi desenhado com uma aposta: o turista, de outros estados e de fora do país, sustenta o comércio da rua sozinho. Eu escrevi no relatório que ainda é cedo para saber. Ninguém pediu a minha opinião, mas ela está escrita.', kp: 'kp_94_lucia_aposta', revisar: true },
                 { t: 'Os shows do Dia & Noite seguram a rua no fim de semana, mas de terça a quinta ela esvazia. No corredor do órgão já se fala em programar um evento maior, para trazer gente de Salvador mesmo, que mora na cidade e tem carro. Ainda é conversa. Não está em papel nenhum.', conf: [2, 3], kp: 'kp_94_lucia_evento', revisar: true }],
    });
  abre('lucia', 'medir', 'A ficha da casa', 'Lúcia, a senhora ainda mede a rua?');
  abre('lucia', 'programa', 'A aposta do Programa', 'Lúcia, o turista está enchendo a rua como o Programa previa?');
  // ---- conversas espontâneas e examináveis da rua em 1994 ----
  RD.papos = [
    ['dandara>raimundo', ['Seu Raimundo, o senhor vai à reunião de sábado? Vou ler a lista.', 'Se meu nome estiver nela, eu vou. Se não, eu vou do mesmo jeito.']],
    ['lucia>raimundo', ['Seu Raimundo, eu preciso conferir a ficha do sobrado de novo.', 'Pode conferir, minha filha. A porta já está marcada de qualquer jeito.']],
    ['cicera>junior', ['Júnior! Sai da casa dos outros, menino!', 'Já vou, vó! Só tô dando pão pro gato!']],
    ['tonho>nonato', ['Cocada, Nonato? Hoje sobrou, que o ônibus não veio.', 'Depois, Tonho. Hoje é dia de pagamento e eu vou receber.']],
  ];
  RD.desc94 = {
    quadro_avisos: 'No quadro: reunião da associação no sábado, uma lista datilografada de casas que receberam aviso, um recado de procura-se inquilino e uma rifa de bujão de gás. Por cima de tudo, um cartaz colorido: PELOURINHO DIA & NOITE, shows grátis toda a semana no Terreiro de Jesus e nos largos.',
    obra_1: 'Tijolos e sacos de cimento da empreiteira, empilhados ao lado do casarão da esquina. Já não é obra de quem mora.',
  };
};
