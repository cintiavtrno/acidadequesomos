// ===== s3_data.js — dados da simulação (pessoas, rotinas, falas, pontos de conhecimento, objetivos) =====
// Toda fala nova é PROPOSTA (precisa de aprovação). Falas de reza/saudação religiosa têm revisar:true → revisão de quem é da cultura do axé.
// Linguagem: português baiano sem caricatura de sotaque. Nada aqui cita pessoa real; figuras de poder são fictícias.
Sim.Data = {};
Sim.Data.dia = { inicio: '07:00', abre: '07:00', fecha: '19:00' };

// ---- lugares (plano para NPCs acessarem outros ambientes; só 'padaria' e 'rua' existem nesta etapa) ----
Sim.Data.locais = {
  rua: { nome: 'Rua', liga: ['padaria', 'largo', 'sobrado_raimundo'] },
  padaria: { nome: 'Padaria', liga: ['rua', 'casa_vo'], porta: 'porta', ativo: true },
  casa_vo: { nome: 'Casa da Vó (escada)', liga: ['padaria'], reservado: true },
  sobrado_raimundo: { nome: 'Sobrado de Seu Raimundo', liga: ['rua'], reservado: true, nota: 'Cenário a enviar; fogão e panelas da Etapa 3 pertencem a ele.' },
  largo: { nome: 'Largo', liga: ['rua'], reservado: true },
};

// ---- pessoas ----
// traços 0..1 · necessidades 0..1 (sobem com o tempo) · rotina: visitas do dia · pedido: o que pede no balcão
Sim.Data.pessoas = {
  aurea: { nome: 'Vó Áurea', curto: 'Vó', cor: '#e8c9a0', papel: 'dona da padaria', tracos: { paciente: .7, sociavel: .6, reservada: .7, religiosa: .8 }, interesses: ['balcão', 'forno', 'nicho', 'caderneta'], velocidade: 'aurea' },
  raimundo: {
    nome: 'Seu Raimundo', curto: 'Raimundo', cor: '#9fb4c8', papel: 'vizinho do sobrado amarelo', idade: 70,
    tracos: { sociavel: .8, paciencia: .95, religioso: .9, orgulhoso: .7, desconfiado: .35 },
    interesses: ['conversa', 'reza', 'fiado', 'dominó'], necessidades: { cansaco: .55, social: .8, fome: .6 }, humor: 'normal',
    visitas: [{ a: '07:20', jit: 5, estadia: [150, 200] }], pedido: { itens: { cafe: 1, pao: 2 }, fiado: true, papo: 16 }, paciencia: 85,
    assentos: ['banco_1', 'chair_b_l', 'chair_a_l'], reza: true, olha: 0,
  },
  dandara: {
    nome: 'Dandara', curto: 'Dandara', cor: '#c88aa0', papel: 'líder da associação de moradores', idade: 41,
    tracos: { sociavel: .6, paciencia: .35, determinada: .9, desconfiada: .6 },
    interesses: ['ata', 'associação', 'mãe doente'], necessidades: { cansaco: .35, social: .55, fome: .4 }, humor: 'normal',
    olha: 2, visitas: [{ a: '07:45', jit: 3, estadia: [110, 165] }], pedido: { itens: { pao: 6, cafe: 1 }, fiado: false, fiadoChance: .3, papo: 4 }, paciencia: 30,
    assentos: ['chair_a_back', 'chair_a_r', 'chair_b_back'],
  },
  lucia: {
    nome: 'Lúcia', curto: 'Lúcia', cor: '#e8a050', papel: 'técnica do Programa', idade: 34,
    tracos: { sociavel: .35, paciencia: .6, metodica: .9, cuidadosa: .8 },
    interesses: ['medir', 'prancheta', 'café'], necessidades: { cansaco: .5, social: .3, fome: .5 }, humor: 'normal',
    visitas: [{ a: '07:38', jit: 3, estadia: [100, 160] }], pedido: { itens: { cafe: 1, pao: 1 }, fiado: false, fiadoChance: .12, papo: 2 }, paciencia: 50,
    assentos: ['chair_a_l', 'chair_b_f', 'banco_2'], mede: ['porta', 'balcao', 'vitrine'], olha: 4,
  },
};
Sim.Data.precos = { pao: 0.5, cafe: 0.7, bolo: 2.0 };
Sim.Data.estoque = { pao: 24, cafe: 16, bolo: 6 };

// relações iniciais. 'lia>x' = confiança de x em Lia (0..1) e afinidade; 'a>b' entre moradores (afinidade -1..1, tensão 0..1)
Sim.Data.relacoes = {
  'raimundo>lia': { aff: .55, trust: .34 }, 'dandara>lia': { aff: .2, trust: .22 }, 'lucia>lia': { aff: 0, trust: .06 }, 'aurea>lia': { aff: .95, trust: .62 },
  'raimundo>dandara': { aff: .5, trust: .5 }, 'dandara>raimundo': { aff: .55, trust: .5 },
  'raimundo>lucia': { aff: .1, trust: .1 }, 'lucia>raimundo': { aff: .2, trust: .2 },
  'dandara>lucia': { aff: -.25, trust: .05 }, 'lucia>dandara': { aff: -.05, trust: .1 },
  'raimundo>aurea': { aff: .7, trust: .8 }, 'dandara>aurea': { aff: .5, trust: .6 }, 'lucia>aurea': { aff: .2, trust: .2 },
};

// ---- falas ----
// quando: { loc: zona, estado, conf:[min,max] (nível de confiança em Lia 0..3), humor:[...], mem:id, semMem:id, hora:[min,max] (em minutos), presente:id, flag:id }
// Mais condições satisfeitas = fala mais específica = escolhida primeiro. Falas já ditas esperam antes de voltar (DialogueSystem).
const F = (id, texto, quando, extra) => Object.assign({ id, texto, quando: quando || {} }, extra || {});
Sim.Data.falas = {
  aurea: {
    saudar: [
      F('a_s0', 'Deus te abençoe, minha filha.'),
      F('a_s1', 'Pode falar, que eu escuto com as mãos na massa.', { loc: 'posto' }),
      F('a_s2', 'Um minutinho que a fila não espera, mas eu converso.', { estado: 'servindo' }),
      F('a_s3', 'Hoje a rua tá agitada, repara.', { hora: [545, 700] }),
      F('a_s4', 'Tu mexeu na gaveta, eu sei. Deixa pra lá.', { mem: 'lia_xeretou_gaveta' }),
    ],
    ouvir: [
      F('a_o0', '(A vó cantarola baixinho enquanto embrulha o pão.)', { estado: 'servindo' }),
      F('a_o1', '(Ela olha o forno, depois o nicho, como quem confere se tudo ficou no lugar.)'),
      F('a_o2', '(A vó fecha o rádio com a ponta do dedo.)', { flag: 'radio_tocou' }),
    ],
    perguntar: {
      rua: [F('a_pr0', 'A rua é a casa maior. Tem gente que entra sem bater, mas tem que aprender a pedir licença.'), F('a_pr1', 'Cada porta daqui sabe o nome de quem mora. Isso vale mais que placa.', { conf: [2, 3] })],
      caderneta: [F('a_pc0', 'A caderneta é que cobra, minha filha. Eu só anoto.'), F('a_pc1', 'Fiado é confiança. Dívida é coisa de banco.', { conf: [2, 3] })],
      altar: [F('a_pa0', 'É São Jorge. E é o outro nome também, o que a minha avó não dizia alto. É os dois.', { }, { revisar: true }), F('a_pa1', 'A vela fica acesa porque a rua precisa de quem guarde.', { conf: [2, 3] }, { revisar: true })],
      gaveta: [F('a_pg0', 'Gaveta é de papel, minha filha. E papel a gente não mostra pra todo mundo.'), F('a_pg1', 'Hoje não. Quando eu decidir o que fazer, tu sabe primeiro.', { flag: 'lia_pressionou' })],
      casa: [F('a_pk0', 'Lá em cima é nossa casa. Um dia a gente sobe junto e eu te mostro com calma.')],
    },
    pressionar: {
      gaveta: [F('a_pp0', 'Lia. Não insiste. Tem coisa que a vó guarda pra não pesar em ninguém.'), F('a_pp1', 'Tá bom, tá bom. É uma proposta. Querem alugar o ponto pra um café, pagando o dobro. Eu não respondi ainda, e tu não conta pra ninguém.', { flag: 'lia_pressionou' })],
    },
    ajudar: { sovar: [F('a_aj0', 'Assim, com a palma da mão. A massa sente a pressa de quem mexe.')] },
    balcao: [
      F('a_b0', 'Já vai, já vai.'), F('a_b1', 'Toma, cuidado que tá quente.'), F('a_b2', 'Anotado na caderneta.', { estado: 'fiado' }),
      F('a_b3', 'Pagou, tá pago. Obrigada, minha filha.', { estado: 'pago' }), F('a_b4', 'Só mais um segundo, que o pão não deixa a gente na mão.'),
    ],
  },
  raimundo: {
    saudar: [
      F('r_s0', 'Bom dia, minha filha. A vó tá bem?'),
      F('r_s1', 'Ah, a neta da Áurea. Chega aqui, senta um pouco.', { conf: [2, 3] }),
      F('r_s2', 'Hoje o balcão tá devagar, mas eu não tenho pressa.', { loc: 'fila' }),
      F('r_s3', 'Pode sentar, o café ainda tá quente.', { loc: 'mesa' }),
      F('r_s4', 'Shh... deixa eu terminar aqui.', { loc: 'altar' }, { revisar: true }),
      F('r_s5', 'Ouvi o rádio. Não sei não, Lia...', { humor: ['preocupado'] }),
      F('r_s6', 'Tu sempre aparece na hora da sede, não é? Deus lhe pague.', { mem: 'lia_ajudou_agua' }),
      F('r_s7', 'Dandara tá ali. Fala com ela, que ela entende dessas coisas de papel.', { presente: 'dandara' }),
    ],
    ouvir: [
      F('r_o0', '(Seu Raimundo confere os bolsos devagar, como quem já sabe o que vai achar.)', { loc: 'fila' }),
      F('r_o1', 'Minha mãe tomava café aqui, nesse mesmo canto. Dizia que o dela era o mais forte da rua.', { loc: 'mesa' }),
      F('r_o2', '(Ele murmura uma reza baixinho, de olhos fechados. Você espera.)', { loc: 'altar' }, { revisar: true }),
      F('r_o3', 'Dizem que vão medir tudo. Medir pra quê? A casa tá de pé.', { humor: ['preocupado'] }),
      F('r_o4', 'Tempo bom pra conversa fiada. Mas tem conversa que pesa.'),
    ],
    perguntar: {
      rua: [F('r_pr0', 'A rua mudou menos que a gente. Mas tá mudando, filha.'), F('r_pr1', 'Antes todo mundo sabia o nome de todo mundo. Agora vem gente com prancheta e sabe só o número.', { conf: [1, 3] })],
      casa: [F('r_pk0', 'A casa amarela? É minha casa, filha. Já foi da minha mãe.'), F('r_pk1', 'Ela cuidava de cada janela. Eu só tento não deixar a casa cair.', { conf: [1, 3] })],
      caderneta: [F('r_pc0', 'Pago sexta. Sempre paguei sexta. Minha mãe fazia assim.'), F('r_pc1', 'Se a Áurea anota, é porque confia. Isso pesa mais que dívida, viu?', { conf: [1, 3] })],
      programa: [F('r_pp0', 'Programa? Ouvi falar. Quando falam muito alto é porque já decidiram.'), F('r_pp1', 'Se mexerem na minha casa, eu quero ver de que lado fica o santo.', { conf: [2, 3] }, { revisar: true })],
      papel: [F('r_pa0', 'Papel? Só o da caderneta. Por enquanto.')],
    },
    ajudar: { agua: [F('r_aj0', 'Ah, obrigado, minha filha. Água de filtro de barro é outra coisa. Minha mãe dizia que ensina paciência.')] },
    papo: [F('r_pb0', 'A senhora lembra do forno de lenha da minha mãe, Áurea?'), F('r_pb1', 'Sexta eu acerto. Nunca falhei sexta.')],
    pedido: [F('r_pd0', 'Um cafezinho e dois pães com manteiga. Anota aí, que sexta eu acerto.')],
  },
  dandara: {
    saudar: [
      F('d_s0', 'Bom dia, Lia. Tá cheio hoje.'),
      F('d_s1', 'Se a fila andar, eu agradeço. Tenho reunião daqui a pouco.', { loc: 'fila' }),
      F('d_s2', 'Lia! Chegou na hora. Preciso de gente que escute.', { conf: [2, 3] }),
      F('d_s3', 'Não esqueci a vez que tu me deu. Anotei.', { mem: 'lia_deu_vez' }),
      F('d_s4', 'Soube que cuidou de Seu Raimundo. Isso conta aqui na rua.', { mem: 'soube_agua' }),
      F('d_s5', 'Esperei, esperei, e nada. Hoje não é dia bom.', { humor: ['irritada'] }),
      F('d_s6', 'Bom dia. Desculpa a pressa, mas minha mãe espera o pão.', { loc: 'vitrine' }),
    ],
    ouvir: [
      F('d_o0', '(Dandara folheia um caderno de capa dura e confere linhas numeradas.)', { loc: 'fila' }),
      F('d_o1', 'Tem gente que acha que associação é só ata. Ata é o começo.', { loc: 'mesa' }),
      F('d_o2', 'Minha mãe tá mal, e eu aqui contando pão. Mas é isso.'),
    ],
    perguntar: {
      rua: [F('d_pr0', 'A rua tem voz demais e ouvido de menos.'), F('d_pr1', 'Cada casa tem um motivo pra ficar. Eu só junto os motivos.', { conf: [1, 3] })],
      programa: [F('d_pp0', 'O Programa? Prometem restaurar tudo. Só não dizem quem fica.'), F('d_pp1', 'Fizeram levantamento de casa por casa sem avisar. Eu quero a lista com os nomes dos moradores.', { conf: [1, 3] })],
      caderno: [F('d_pd0', 'É a ata. Quem não escreve, esquecem.'), F('d_pd1', 'Aprendi a escrever com uma freira. Era pra rezar, mas deu pra anotar muita coisa.', { conf: [1, 3] })],
      mae: [F('d_pm0', 'Minha mãe tá doente. Por isso eu não posso me demorar.'), F('d_pm1', 'Ela gosta de bolo de aipim. Quando sobra, eu levo.', { conf: [1, 3] })],
      lucia: [F('d_pl0', 'A moça da prancheta? Educada. E é isso que me dá mais medo.'), F('d_pl1', 'Ela não é má. Mas faz a conta que mandam, e a conta não conhece ninguém.', { conf: [2, 3] })],
    },
    ajudar: { vez: [F('d_aj0', 'Obrigada, Lia. Tenho pressa mesmo. Vou anotar a gentileza.')] },
    pedido: [F('d_pd2', 'Seis pães pra levar e um cafezinho. Rápido, Dona Áurea, se der.')],
    papo: [F('d_pb0', 'A senhora viu a lista nova, Dona Áurea?')],
  },
  lucia: {
    saudar: [
      F('l_s0', 'Bom dia. Lia, não é? A neta da dona Áurea.'),
      F('l_s1', 'Oi, Lia. Não vou te atrapalhar.', { conf: [1, 3] }),
      F('l_s2', 'Só o café, por favor. A manhã tá comprida.', { loc: 'fila' }),
      F('l_s3', 'Cuidado aí, tô medindo.', { loc: 'medindo' }),
      F('l_s4', 'A ajudante de trena! Bom ver você.', { mem: 'lia_trena' }),
      F('l_s5', 'Não precisava ter visto aquilo. Mas já vi.', { humor: ['constrangida'] }),
    ],
    ouvir: [
      F('l_o0', '(Lúcia confere a trena e anota: "pé-direito dois e quarenta; balcão sete e sessenta".)', { loc: 'medindo' }),
      F('l_o1', 'Eu só meço. Quem decide é outro andar.', { loc: 'mesa' }),
      F('l_o2', '(Ela sublinha alguma coisa na prancheta e vira a folha para você não ler.)'),
    ],
    perguntar: {
      programa: [F('l_pp0', 'É um programa de recuperação do centro histórico. Eu faço o levantamento.'), F('l_pp1', 'O levantamento é casa por casa. Algumas já têm lista. Outras ainda não.', { conf: [1, 3] }), F('l_pp2', 'Tem casa na lista sem nome de morador. Isso não é bom sinal, e eu não deveria te contar.', { conf: [2, 3] })],
      rua: [F('l_pr0', 'Uma rua bonita. Difícil de medir.'), F('l_pr1', 'O que sobra na planilha é o que mais pesa aqui.', { conf: [2, 3] })],
      prancheta: [F('l_pn0', 'Medidas, só. Nada de pessoa.'), F('l_pn1', 'As pessoas entram na coluna de observações. Eu escrevo o menos que posso.', { conf: [1, 3] })],
      raimundo: [F('l_pi0', 'Seu Raimundo? Educado.'), F('l_pi1', 'Ele pede fiado com tanta dignidade que dá vontade de não anotar.', { mem: 'viu_fiado' })],
    },
    ajudar: { trena: [F('l_aj0', 'Segura aqui. Ponta no chão. Obrigada. Dois e quarenta.')] },
    pedido: [F('l_pd0', 'Um café sem açúcar e um pão simples. Obrigada.')],
    papo: [F('l_pb0', 'A senhora tem o número de quem mora no andar de cima?')],
  },
};

// ---- conversas espontâneas entre moradores (cada roteiro: pares, condição, falas, efeitos) ----
// cond(w, a, b) decide se o roteiro cabe agora. Cada roteiro só se repete se esperar bastante (DialogueSystem).
Sim.Data.conversas = [
  { id: 'rd_mae', par: ['raimundo', 'dandara'], min_aff: 0, falas: [['dandara', 'Seu Raimundo, minha mãe mandou lembrança.'], ['raimundo', 'Como ela tá?'], ['dandara', 'Mal-humorada, que é sinal de que melhora.'], ['raimundo', 'Diz que a casa amarela tá de portas abertas pra ela.']], efeito: { aff: .05 }, tema: 'mae' },
  { id: 'rd_cadastro', par: ['raimundo', 'dandara'], min_aff: 0, falas: [['dandara', 'Tão pedindo nome de morador de porta em porta.'], ['raimundo', 'Eu não assino nada sem a Áurea ler.'], ['dandara', 'Faz bem. Quem assina sem ler vira número.']], efeito: { aff: .04 }, tema: 'cadastro', ouvido: 'kp_conversa_rd' },
  { id: 'rd_vez', par: ['raimundo', 'dandara'], min_aff: .2, cond: w => w.service.queue.indexOf('raimundo') >= 0 && w.service.queue.indexOf('dandara') > w.service.queue.indexOf('raimundo'), falas: [['raimundo', 'Passa na frente, Dandara. Eu tenho todo o tempo do mundo.'], ['dandara', 'Não precisa, Seu Raimundo.'], ['raimundo', 'Precisa sim. Quem tem causa não espera.']], efeito: { aff: .06, cede: ['raimundo', 'dandara'] }, tema: 'vez' },
  { id: 'dl_tensao', par: ['dandara', 'lucia'], min_aff: -1, falas: [['dandara', 'Bom dia, dona Lúcia. Já mediu a rua inteira?'], ['lucia', 'Só estou começando, Dandara.'], ['dandara', 'E a gente entra em qual coluna da planilha?'], ['lucia', 'Eu não escolho as colunas.']], efeito: { aff: -.06, tens: .1 }, tema: 'programa', ouvido: 'kp_conversa_dl' },
  { id: 'rl_prancheta', par: ['raimundo', 'lucia'], min_aff: -1, falas: [['lucia', 'Seu Raimundo, bom dia.'], ['raimundo', 'Bom dia, doutora.'], ['lucia', 'Não sou doutora.'], ['raimundo', 'Mas anda de prancheta, é a mesma coisa.']], efeito: { aff: .03 }, tema: 'prancheta' },
  { id: 'rl_fiado', par: ['lucia', 'raimundo'], min_aff: -1, cond: w => w.mem.has('lucia', 'viu_fiado'), falas: [['raimundo', 'A senhora anotou meu nome aí na prancheta?'], ['lucia', 'Só o que preciso, Seu Raimundo.'], ['raimundo', 'O que a senhora precisa é diferente do que eu preciso. Mas tudo bem.']], efeito: { aff: -.02 }, tema: 'fiado' },
];
// conversa de balcão com a Vó (acontece durante o atendimento; não depende da Lia)
Sim.Data.bate_papo_balcao = {
  raimundo: [[['raimundo', 'A senhora lembra do forno de lenha da minha mãe, Áurea?'], ['aurea', 'Lembro. Ela batia na porta antes do sol.'], ['raimundo', 'E nunca falhou a sexta.'], ['aurea', 'Nunca. Nem tu.']]],
  dandara: [[['dandara', 'A senhora viu a lista nova, Dona Áurea?'], ['aurea', 'Vi. Vi e fiquei calada, que é pior.']]],
  lucia: [[['lucia', 'A senhora tem o número de quem mora no andar de cima?'], ['aurea', 'Tenho. Mas é conversa pra outra hora, minha filha.']]],
};

// reações curtas (balões) a acontecimentos
Sim.Data.reacoes = {
  radio: { raimundo: 'Escutou isso, Áurea? Já falaram em medir tudo.', dandara: 'Aí está. Já falaram. Falta só dizer a quem.', lucia: '(Lúcia abaixa os olhos para a prancheta.)', aurea: '(A vó baixa o volume do rádio.)' },
  desistiu: { raimundo: 'Ih, a fila tá longa. Volto mais tarde.', dandara: 'Eu volto depois. Não dá pra esperar.', lucia: 'Preciso voltar ao trabalho.' },
  furada: { raimundo: 'Pode passar, minha filha.', lucia: '(Lúcia ergue as sobrancelhas, mas não diz nada.)', dandara: 'Obrigada. Eu retribuo.' },
  // proposta: fala extra quando o vizinho pede fiado (revisar)
  pedidoFiado: { dandara: 'A reunião atrasou o pagamento do mês. Anota pra mim, Dona Áurea? Semana que vem eu acerto.', lucia: 'Esqueci a carteira no escritório. A senhora anota até amanhã?' },
  fiado_visto: { raimundo: 'Anota aí, Áurea. Sexta eu acerto.', lucia: '(Lúcia anota algo na prancheta, discreta.)' },
  fila_cheia: { raimundo: 'Tá cheio hoje, hein.', dandara: 'Assim eu não chego na reunião.', lucia: 'Vou esperar. Não tem problema.' },
  procura: { lucia: 'A senhora viu Seu Raimundo hoje?', raimundo: 'Dandara já passou por aqui?', dandara: 'Seu Raimundo já veio, Dona Áurea?' },
  vela: { aurea: '(A vó acende a vela do nicho e fica um instante parada.)' },
  forno: { aurea: '(O forno estala; a vó ajeita a lenha e sorri.)' },
};

// ---- pontos de conhecimento (alimentam o Caderninho) ----
// pessoa/lugar: onde aparece. obj: objetivos que contam. texto: o que Lia anota (tom dela, curto).
const K = (id, titulo, texto, quem, extra) => Object.assign({ id, titulo, texto, quem }, extra || {});
Sim.Data.conhecimentos = [
  // fiado de Seu Raimundo
  K('kp_caderneta', 'A caderneta da vó', 'A linha de Seu Raimundo é a mais comprida. Tem risco de sexta em sexta, e nunca um "devendo".', 'raimundo', { obj: 'fiado' }),
  K('kp_lousa', 'A lousa do fiado', 'A lousa diz "fiado até sexta". A vó nunca apagou a linha dele.', 'aurea', { obj: 'fiado' }),
  K('kp_raimundo_fiado', 'Anota na caderneta', 'Ouvi Seu Raimundo pedir pra anotar. Ele fala "sexta eu acerto" como quem faz promessa, não pedido.', 'raimundo', { obj: 'fiado' }),
  K('kp_raimundo_sexta', 'Sexta, o dia dele', 'Pagar na sexta era o costume da mãe dele. Ele guardou o costume junto com a casa.', 'raimundo', { obj: 'fiado' }),
  K('kp_raimundo_agua', 'A água do filtro', 'Levei água do filtro pra Seu Raimundo. Ele falou da mãe: "a água de barro ensina paciência".', 'raimundo', { obj: 'fiado' }),
  K('kp_raimundo_reza', 'Diante do nicho', 'Seu Raimundo reza baixinho diante do nicho de São Jorge antes de sair. Esperei sem atrapalhar.', 'raimundo', { obj: 'fiado', revisar: true }),
  K('kp_vo_fiado', 'O que a vó pensa do fiado', 'A vó disse que quem cobra é a caderneta, não ela. Pra ela, fiado é confiança.', 'aurea', { obj: 'fiado' }),
  // o que vem aí
  K('kp_radio', 'O rádio da vó', 'O rádio anunciou um Programa de recuperação do centro histórico. A vó baixou o volume.', 'aurea', { obj: 'programa' }),
  K('kp_calendario', 'Sexta circulada', 'No calendário, uma sexta está circulada de vermelho. Todo mundo parece contar os dias até ela.', 'aurea', { obj: 'programa' }),
  K('kp_lucia_ouvir', 'Lúcia mede tudo', 'Lúcia anota medidas da padaria: pé-direito, balcão, janela. Diz que só mede.', 'lucia', { obj: 'programa' }),
  K('kp_lucia_programa', 'O levantamento', 'O Programa faz um levantamento casa por casa. Algumas casas já têm lista; outras não.', 'lucia', { obj: 'programa' }),
  K('kp_dandara_programa', 'Quem fica?', 'Dandara diz que prometem restaurar tudo e não dizem quem fica. Quer a lista com os nomes.', 'dandara', { obj: 'programa' }),
  K('kp_conversa_dl', 'Dandara e a prancheta', 'Ouvi Dandara perguntar em qual coluna a gente entra. Lúcia respondeu que não escolhe as colunas.', 'dandara', { obj: 'programa' }),
  K('kp_lucia_trena', 'Segurar a trena', 'Segurei a trena de Lúcia. Ela escreve o mínimo na coluna de observações e deixa sobrar "sem nome do morador".', 'lucia', { obj: 'programa' }),
  // pessoas (fora dos dois objetivos)
  K('kp_raimundo_casa', 'A casa amarela', 'A casa amarela foi da mãe de Seu Raimundo. Ele fala dela com carinho e preocupação.', 'raimundo'),
  K('kp_conversa_rd', 'Dandara e Seu Raimundo', 'Ouvi os dois falarem do cadastro: "quem assina sem ler vira número".', 'raimundo'),
  K('kp_dandara_ata', 'A ata', 'Dandara guarda a ata num caderno de capa dura. "Quem não escreve, esquecem."', 'dandara'),
  K('kp_dandara_freira', 'A freira', 'Dandara aprendeu a escrever com uma freira, e usa isso pra anotar tudo da rua.', 'dandara'),
  K('kp_dandara_mae', 'A mãe de Dandara', 'A mãe de Dandara está doente. Por isso ela vive com pressa.', 'dandara'),
  K('kp_dandara_vez', 'A vez dela', 'Pedi a vez para Dandara. Ela disse que vai anotar a gentileza.', 'dandara'),
  K('kp_lucia_prancheta', 'A coluna de observações', 'As pessoas entram na coluna de observações. Lúcia escreve o menos que pode.', 'lucia'),
  K('kp_lucia_fiado', 'Lúcia viu o fiado', 'Lúcia viu Seu Raimundo pedir fiado. Disse que dá vontade de não anotar.', 'lucia'),
  K('kp_vo_proposta', 'A proposta da gaveta', 'Insisti, e a vó contou: querem alugar o ponto para um café, pagando o dobro. Ela ainda não respondeu.', 'aurea', { obj: null }),
  K('kp_vo_altar', 'São Jorge e o outro nome', 'A vó disse que é São Jorge e é também o nome que a avó dela não dizia alto. É os dois.', 'aurea', { revisar: true }),
  K('kp_vo_ajuda', 'Sovar com a vó', 'Sovei a massa com a vó. Ela disse que a massa sente a pressa de quem mexe.', 'aurea'),
  // lugares e objetos (os "ovos de páscoa")
  K('kp_altar', 'O nicho de São Jorge', 'Nicho com a imagem do santo, vela, copo d\'água e flores. A vó acende a vela todo dia de manhã.', 'lugar', { revisar: true }),
  K('kp_quadro', 'Quadro do Bonfim', 'Um quadro da colina do Bonfim, com fitinhas coloridas. Cada fitinha é um pedido de alguém da rua.', 'lugar'),
  K('kp_fotos', 'Retratos na parede', 'Três retratos antigos. Reconheci o balcão atrás de uma moça de lenço: a mãe de alguém desta rua.', 'lugar'),
  K('kp_filtro', 'O filtro de barro', 'Os vizinhos enchem garrafa no filtro e ninguém paga. Faz parte da casa.', 'lugar'),
  K('kp_gaveta', 'A gaveta do balcão', 'Papéis, lápis, um caderno. Uma folha dobrada com números e a palavra "dobro".', 'lugar'),
  K('kp_estante', 'Estante de potes', 'Rádio, potes, latas e cestos. Cada pote tem nome escrito na tampa, com a letra da vó.', 'lugar'),
  K('kp_janela', 'Janela do quintal', 'A janela dá para o quintal de folhagens. A vó diz que a mangueira é "de ninguém e de todo mundo".', 'lugar'),
  K('kp_forno', 'O forno de lenha', 'O forno é aceso antes do sol. A vó diz que ele só funciona direito se alguém conversa com ele.', 'lugar'),
  K('kp_caixa', 'A caixa registradora', 'O caixa só guarda o que é pago na hora. O fiado é contado à parte, na caderneta.', 'lugar'),
  K('kp_vitrine', 'A vitrine', 'Pães e bolos do dia. A vitrine é o primeiro lugar onde todo cliente para e pensa.', 'lugar'),
  K('kp_banco', 'O banco do nicho', 'Um banco comprido encostado na parede, de frente pro nicho. Parece feito pra esperar rezando.', 'lugar'),
  K('kp_bancada', 'A bancada da massa', 'Aqui a vó abre a massa. Tem marcas de dedos na madeira, de muitos anos.', 'lugar'),
  K('kp_escada', 'A porta da escada', 'A porta que sobe pra nossa casa. Depois das três da tarde dá para subir e dormir quando a Lia quiser.', 'lugar'),
];
// níveis do Caderninho por pessoa (quantos pontos de conhecimento viram qual rótulo)
Sim.Data.nivelPessoa = [[0, 'Ainda estou conhecendo'], [2, 'Já me conhece'], [4, 'Confia em mim'], [7, 'Sei o que pesa nela']];

// ---- objetivos (dois ao mesmo tempo; Lia não precisa fazer tudo, e nem tudo é possível saber hoje) ----
Sim.Data.objetivos = [
  { id: 'fiado', titulo: 'O fiado de Seu Raimundo', dica: 'Entender por que ele "paga na sexta".', meta: 5, aviso: 'A linha dele é a mais comprida da caderneta.', fim: 'Entendi o fiado de Seu Raimundo. Resta saber o que ele guarda dentro da casa.' },
  { id: 'programa', titulo: 'O que vem aí', dica: 'Escutar a rua sobre o Programa.', meta: 5, aviso: 'Todo mundo comenta, ninguém explica.', fim: 'Já sei o bastante pra perguntar às pessoas certas. Falta o papel, e falta saber quem fica.' },
];
// ---- textos de objetos examináveis (podem variar conforme o estado do mundo) ----
Sim.Data.objetos = {
  altar_sao_jorge: { kp: 'kp_altar', texto: w => w.obj('altar_vela') ? 'Nicho de São Jorge. A vela está acesa, o copo d\'água cheio, as flores do dia. A vó o chama de São Jorge; Seu Raimundo, de Ogum. É os dois.' : 'O nicho de São Jorge: imagem, copo d\'água, flores. A vela ainda não foi acesa hoje.' },
  quadro_1: { kp: 'kp_quadro', texto: () => 'Quadro da colina do Bonfim, com fitinhas coloridas amarradas na moldura.' },
  fotos_1: { kp: 'kp_fotos', texto: () => 'Três retratos antigos. Numa delas, uma moça de lenço atrás do mesmo balcão.' },
  aparador: { kp: 'kp_filtro', texto: () => 'O filtro de barro. Uma caneca pendurada no gancho; ninguém paga por água nesta casa.' },
  gaveta_1: { kp: 'kp_gaveta', texto: (w, ctx) => ctx.vo_longe ? 'Papéis, lápis, um caderno. Uma folha dobrada traz números e a palavra "dobro".' : 'Gaveta com papéis e lápis. A vó está olhando; melhor não mexer agora.' },
  estante: { kp: 'kp_estante', texto: () => 'Estante com potes, latas e cestos. Cada tampa tem um nome, na letra da vó.' },
  radio: { kp: null, texto: w => w.flag('radio_tocou') ? 'O rádio de pilha, baixinho. Ainda se ouve o fim de uma notícia sobre o Programa.' : 'Rádio de pilha na estante, ligado em volume baixo, com música.' },
  janela_quintal: { kp: 'kp_janela', texto: () => 'A janela do quintal: folhagens, a sombra da mangueira. A vó diz que ela é de ninguém e de todo mundo.' },
  calendario: { kp: 'kp_calendario', texto: () => 'Calendário de parede. Uma sexta está circulada de vermelho.' },
  lousa_fiado: { kp: 'kp_lousa', texto: () => 'Lousa do cardápio. Embaixo, em giz: "fiado até sexta". Uma linha tem o nome de Seu Raimundo há mais tempo que as outras.' },
  caderneta: { kp: 'kp_caderneta', texto: w => 'Caderneta de capa vermelha. Seu Raimundo aparece ' + (w.service.fiado.raimundo ? 'com ' + w.service.fiado.raimundo.n + ' anotação(ões) hoje' : 'sem anotação de hoje, ainda') + ', e muitas outras de sextas passadas.' },
  caixa: { kp: 'kp_caixa', texto: w => 'Caixa registradora. Hoje já entrou ' + w.service.caixa.toFixed(2).replace('.', ',') + '. O fiado não entra aqui.' },
  vitrine: { kp: 'kp_vitrine', texto: w => 'Vitrine: ' + w.service.stock.pao + ' pães, ' + w.service.stock.bolo + ' bolos.' },
  forno_lenha: { kp: 'kp_forno', texto: w => w.obj('forno_aceso') ? 'O forno de lenha, aceso desde cedo. O calor chega até o balcão.' : 'O forno de lenha, ainda frio; a vó vai acendê-lo.' },
  bancada: { kp: 'kp_bancada', texto: () => 'Bancada de trabalho. Marcas de dedos na madeira, de muitos anos de massa.' },
  banco_altar: { kp: 'kp_banco', texto: () => 'Um banco comprido encostado na parede, de frente pro nicho.' },
  porta_escada_1: { kp: 'kp_escada', texto: w => w.obj('porta_escada_1') ? (w.semFimDeDia && w.clock.min >= 900 ? 'A porta da escada está aberta. Lá em cima é a nossa casa: dá para subir e dormir quando você quiser.' : 'A porta da escada está aberta. Ainda não é hora de subir.') : 'A porta da escada, fechada. Lá em cima fica a nossa casa.' },
};

// ---- 1994 na padaria: quem passa pelo balcão já conta o efeito do Programa (aviso, saída de moradores, turista). Proposta; revisar. ----
Sim.Data.virar94 = () => {
  if (Sim.Data._v94) return; Sim.Data._v94 = true;
  const P = Sim.Data.falas;
  P.raimundo.perguntar.rua = [F('r_pr0', 'A rua de cima está quase toda fechada. Quem aceitou o dinheiro foi para longe, e de lá não volta.'), F('r_pr1', 'Antes todo mundo sabia o nome de todo mundo. Agora vem gente de máquina fotográfica e sabe só o número da casa.', { conf: [1, 3] })];
  P.raimundo.perguntar.programa = [F('r_pp0', 'Colaram um aviso na minha porta. Diz que a casa está em risco. Eu ainda não assinei nada.'), F('r_pp1', 'Eles apostam que turista sustenta o comércio sozinho. Eu nunca vi turista pedir fiado.', { conf: [2, 3] }, { revisar: true })];
  P.raimundo.perguntar.papel = [F('r_pa0', 'Papel, tenho dois: o da caderneta e o do aviso. Só o primeiro eu entendo.')];
  P.dandara.perguntar.programa = [F('d_pp0', 'O Programa saiu da pintura e entrou na obra pesada. Já tem casa interditada e família indo embora.'), F('d_pp1', 'Eu quero a lista de quem recebeu aviso, com nome. A associação lê tudo no sábado.', { conf: [1, 3] })];
  P.dandara.perguntar.lucia = [F('d_pl0', 'A moça da prancheta agora assina ficha de saída. Educada como sempre, e é isso que me dá medo.'), F('d_pl1', 'Ela não é má. Mas a ficha vira valor de indenização, e a conta não conhece ninguém.', { conf: [2, 3] })];
  P.lucia.perguntar.programa = [F('l_pp0', 'O levantamento acabou e agora vem a fase de obra. Eu confiro as fichas das casas que já têm aviso.'), F('l_pp1', 'O Programa apostou que o turista de fora sustenta o comércio da rua. Eu escrevi que ainda é cedo para saber.', { conf: [1, 3] }, { revisar: true }), F('l_pp2', 'No órgão já se fala em programar festa e show, para trazer gente de Salvador. Ainda é conversa de corredor.', { conf: [2, 3] }, { revisar: true })];
  P.lucia.perguntar.prancheta = [F('l_pn0', 'Hoje é ficha de casa: nome de quem mora, quantos são, valor oferecido.'), F('l_pn1', 'Eu escrevo o menos que posso. Mesmo assim é o que decide.', { conf: [1, 3] })];
  P.dandara.perguntar.programa.push(F('d_pp2', 'Agora tem o Dia & Noite: show de graça todo dia nos largos, para a rua não esvaziar. Eu vou. Só pergunto quem mora nos casarões que viram bar.', { conf: [2, 3] }, { revisar: true }));
  // objetivos e anotações de 1994
  const O = id => Sim.Data.objetivos.find(o => o.id === id), KK = id => Sim.Data.conhecimentos.find(k => k.id === id);
  Object.assign(O('fiado'), { titulo: 'A casa de Seu Raimundo', dica: 'Entender o que ele guarda dentro de casa e o que o aviso ameaça.', aviso: 'O sobrado está marcado e ele ainda não assinou.', fim: 'Entendi o que está em jogo no sobrado de Seu Raimundo. Falta saber o que ele vai decidir.' });
  Object.assign(O('programa'), { titulo: 'A aposta do Programa', dica: 'Descobrir o que o Programa espera da rua: turista, show de graça e quem fica.', aviso: 'Tem cartaz novo na rua e papel novo na gaveta.', fim: 'Entendi a aposta: turista e show de graça para encher a rua. Falta saber se a rua cheia é a rua de quem mora.' });
  Object.assign(KK('kp_radio'), { titulo: 'O rádio da vó', texto: 'O rádio fala das ruas reformadas e do Pelourinho Dia & Noite, com show de graça todo dia nos largos. A vó ouve calada.' });
  Object.assign(KK('kp_lucia_programa'), { titulo: 'A ficha vira valor', texto: 'Lúcia faz a ficha de cada casa que sai. A ficha entra no cadastro, e o cadastro define a indenização.' });
  Object.assign(KK('kp_dandara_programa'), { titulo: 'Do conserto à remoção', texto: 'Dandara diz que o Programa saiu da pintura e entrou em obra pesada, com casa interditada e gente indo embora. Quer a lista de quem recebeu aviso.' });
  Object.assign(KK('kp_gaveta'), { titulo: 'A gaveta do balcão', texto: 'O aluguel novo da padaria, com valor de loja para turista, e uma pasta do Programa.' });
  Sim.Data.conhecimentos.push(
    K('kp_gaveta_aluguel', 'O aluguel novo', 'Na gaveta, o papel do aluguel novo da padaria, num valor de loja para turista. Tem um número riscado a lápis e outro escrito por cima. A vó ainda não respondeu.', 'lugar', { obj: 'programa' }),
    K('kp_gaveta_dn', 'A pasta do Dia & Noite', 'Na gaveta, uma pasta do Programa: agenda semanal de shows de graça nos largos (Terreiro de Jesus, Pedro Archanjo, Tereza Batista e Quincas Berro D\'Água) e uma lista de bares e lojas de artesanato dos casarões que devem lucrar com o movimento.', 'lugar', { obj: 'programa', revisar: true }));
  Sim.Data.objetos.gaveta_1 = { kp: 'kp_gaveta', kps: ['kp_gaveta_aluguel', 'kp_gaveta_dn'], texto: (w, ctx) => ctx.vo_longe
    ? 'Você abre a gaveta. Em cima, o papel do aluguel novo, com um valor riscado a lápis e outro por cima. Embaixo, uma pasta do Programa: PELOURINHO DIA & NOITE, agenda de shows de graça nos largos, e uma lista de bares e lojas dos casarões que devem lucrar com o movimento.'
    : 'Gaveta com papéis e lápis. A vó está olhando; melhor não mexer agora.' };
  Sim.Data.bate_papo_balcao = {
    raimundo: [[['raimundo', 'A senhora ainda tem o forno aceso, Áurea?'], ['aurea', 'Tenho. Mas vendo menos pão do que fazia.'], ['raimundo', 'Falta quem coma.'], ['aurea', 'Falta quem more.']]],
    dandara: [[['dandara', 'A senhora vai à reunião de sábado, Dona Áurea?'], ['aurea', 'Vou. Levo o papel do aluguel pra ler junto com os outros.']]],
    lucia: [[['lucia', 'Dona Áurea, preciso conferir a ficha da padaria.'], ['aurea', 'Confere. A ficha eu quero ver depois.']]],
  };
  Object.assign(Sim.Data.reacoes, { fila_cheia: { raimundo: 'Cheio assim eu não via desde antes do aviso.', dandara: 'Metade é gente de fora que só compra água.', lucia: 'Vou esperar. Não tem problema.' } });
};
if (typeof window !== 'undefined' && window.MUNDO_ANO === 1994) Sim.Data.virar94();

