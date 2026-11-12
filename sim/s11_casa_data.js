// ===== s11_casa_data.js — dados da casa de Seu Raimundo (Etapa 5 · Fase A): atividades, falas, objetos examináveis e pontos de conhecimento =====
// Nada aqui altera a padaria até Sim.Casa.install() rodar (o mundo da casa chama isso ao ser criado). Toda fala é PROPOSTA.
Sim.Data.casa = {
  // Atividades da rotina (NPCSchedule + NPCDecisionSystem). dur em minutos de jogo; janela = [início, fim] em minutos do dia.
  // fases: sequência de lugares. zona = rótulo de contexto das falas ("onde ele está").
  atividades: [
    { id: 'cama',   zona: 'cama',     fases: [{ ponto: 'cama', face: 'right', anim: 'interact' }], dur: [3, 4], janela: [420, 445], peso: 2.6, nome: 'arruma a cama' },
    { id: 'planta', zona: 'planta',   fases: [{ ponto: 'planta', face: 'up', anim: 'interact' }], dur: [2, 3], janela: [420, 450], peso: 2.1, nome: 'rega a planta' },
    { id: 'reza',   zona: 'oratorio', fases: [{ ponto: 'oratorio', face: 'up', anim: 'idle', reza: true }], dur: [3, 5], janela: [420, 450], peso: 2.4, devocao: true, nome: 'reza' },
    { id: 'janela', zona: 'janela',   fases: [{ seat: 'balanco_1', anim: 'sit' }], dur: [9, 15], janela: [440, 1140], peso: 1.0, cansaco: true, nome: 'embala na cadeira de balanço, ao lado da janela' },
    { id: 'radio',  zona: 'radio',    fases: [{ ponto: 'radio', face: 'up', anim: 'interact_high' }], dur: [3, 5], janela: [630, 1140], peso: 1.3, nome: 'liga o rádio' },
    { id: 'cafe',   zona: 'fogao',    fases: [{ ponto: 'fogao', face: 'up', anim: 'interact', fogao: 1, nome: 'coa o café' }, { seat: 'cad_esq', anim: 'sit', zona: 'mesa', nome: 'toma o café sentado' }], dur: [4, 5], dur2: [8, 11], janela: [635, 700], peso: 2.4, fome: true, nome: 'faz café' },
    { id: 'mesa',   zona: 'mesa',     fases: [{ seat: 'cad_frente', anim: 'sit' }], dur: [6, 10], janela: [640, 1140], peso: 1.1, nome: 'mexe nas pedras de dominó' },
    { id: 'cozinha', zona: 'fogao',   fases: [{ ponto: 'fogao', face: 'up', anim: 'interact', fogao: 1 }], dur: [11, 16], janela: [690, 720], peso: 2.8, fome: true, nome: 'cozinha o almoço' },
  ],
  saidaPadaria: { a: 432, jit: 4 },           // ~07:12 sai pela rua, chega na padaria (sobrado vizinho) ~07:20 (Etapa 4)
  voltaPadaria: { a: 600, jit: 4 },           // ~10:00, hora em que Lia pode levar a sacola esquecida (proposta)
  // frase da Lia que explica POR QUE ela puxa o assunto (PROPOSTA)
  cafeJuntosDef: { id: 'cafe_juntos', zona: 'fogao', ctrl: true, fases: [{ ponto: 'fogao', face: 'up', anim: 'interact', fogao: 1, nome: 'coa o café' }, { seat: 'cad_dir', anim: 'sit', zona: 'mesa', nome: 'toma o café com a Lia' }], dur: [1, 1], janela: [0, 999], peso: 0 },
  asks: {
    rua: 'Seu Raimundo, como anda a rua daqui de cima?', casa: 'O senhor sempre morou aqui?', mae: 'Vi o retrato e a foto do forno... sua mãe fazia pão pra rua toda?',
    retrato: 'Essa moldura oval é a sua mãe?', forno: 'A foto do forno de lenha... era o forno da sua mãe?', programa: 'Ouvi falarem de um Programa, de gente medindo as casas. O que é isso?',
    papel: 'Alguém deixou algum papel do Programa aqui pro senhor?', assinar: 'Se chegar um cadastro, o senhor vai assinar?', domino: 'Vi a caixa de dominó e o jogo na calçada. O senhor joga?',
  },
  // CAFÉ NA MESA (PROPOSTA): cena guiada com escolhas; as opções só aparecem se a Lia tem motivo (viu o retrato, ouviu do Programa...)
  cena: {
    abertura: [
      { quem: 'nota', texto: 'Ele serve o café em duas xícaras de louça e empurra o açucareiro para o seu lado da mesa.' },
      { quem: 'raimundo', texto: 'Pronto. Café bom se toma sentado. Pode soprar, que tá quente.' },
    ],
    opcoes: {
      jeito: { t: 'Esse café é o seu jeito de receber?', quando: () => true,
        linhas: [{ quem: 'lia', texto: 'Esse café é o seu jeito de receber?' }, { quem: 'raimundo', texto: 'É o que me ensinaram. Duas colheres de pó, água quase fervendo, sem pressa. Quem tem pressa bebe café ruim.' }], kp: 'kp_c_cafe', trust: .02 },
      casa: { t: 'O senhor me conta da casa?', quando: () => true,
        linhas: [{ quem: 'lia', texto: 'O senhor me conta da casa? Cada coisa parece ter história.' }, { quem: 'raimundo', texto: 'Tem. A colcha de retalhos foi feita pra casa cheia. A mesa eu ponho pra um, mas deixo a outra cadeira puxada. Hábito. Pode ser que alguém chegue.' }], kps: ['kp_c_colcha', 'kp_c_mesa'], trust: .03 },
      retrato: { t: 'Foi sua mãe que ensinou, a do retrato?', quando: (w) => w.knowledge.has('kp_c_retrato') || w.knowledge.has('kp_c_foto'),
        linhas: (w) => [{ quem: 'lia', texto: 'Foi a sua mãe que ensinou? A do retrato, de lenço?' }, w.rel.nivel('raimundo', 'lia') >= 2
          ? { quem: 'raimundo', texto: 'Foi. Ela deixava o pão de sexta na porta de cada vizinho. Quem podia pagava na hora, quem não podia pagava depois. Dali eu aprendi que dívida se paga olhando nos olhos, e que isso é coisa de gente honrada.' }
          : { quem: 'raimundo', texto: 'Foi. Mas hoje não é dia de contar tudo, filha. Volta outro dia e a gente conversa.' }], kpSe: ['kp_c_mae', 2], trust: .03 },
      programa: { t: 'O que o senhor acha do que andam fazendo na rua?', quando: (w) => !!w.viv.ouviu_programa,
        linhas: [{ quem: 'lia', texto: 'Vi gente medindo as casas. O que o senhor acha disso?' }, { quem: 'raimundo', texto: 'Medir, medem. Perguntar, não perguntam. Eu não assino o que não sei ler, e o que sei ler eu mostro pra Áurea antes.' }], kp: 'kp_c_assinar', trust: .03, marca: 'p_programa' },
      calar: { t: '(Tomar o café em silêncio.)', quando: () => true,
        linhas: [{ quem: 'nota', texto: 'Vocês bebem sem falar. Lá fora a rua faz barulho; aqui dentro ninguém precisa encher o tempo.' }, { quem: 'raimundo', texto: 'Gosto de quem sabe calar. É raro.' }], trust: .05, silencio: true },
    },
    fechar: { t: 'Agradecer o café e levantar', linhas: [{ quem: 'lia', texto: 'Obrigada pelo café, Seu Raimundo.' }, { quem: 'raimundo', texto: 'Volta quando quiser. Café aqui não falta, e a conversa também não.' }] },
    convite: { quem: 'raimundo', texto: 'E passa na calçada, que o dominó anda precisando de olhos novos. Falta uma pedra, mas a gente dá um jeito.' },
  },
  rotulos: {
    rua: 'Como anda a rua?', mae: 'Como era sua mãe?', casa: 'Sempre morou aqui?', retrato: 'Essa moldura é sua mãe?', forno: 'Aquele forno da fotografia...',
    programa: 'O que é esse Programa?', papel: 'Tem algum papel por aí?', assinar: 'O senhor vai assinar o cadastro?', domino: 'O senhor joga dominó?',
    cafe: 'Ajudar a coar o café', agua: 'Oferecer um copo d\'água', regar: 'Ajudar com a planta',
  },
  falas: {
    visita: [
      F('rc_v0', 'Ô de casa! Entra, entra.'),
      F('rc_v1', 'Lia? Chegou cedo. O café ainda tá no pó.', { hora: [420, 500] }),
      F('rc_v2', 'Fecha a porta, minha filha, que a corrente de ar vem.'),
      F('rc_v3', 'A neta da Áurea na minha sala. Isso pede café.', { conf: [2, 3] }),
    ],
    saudar: [
      F('rc_s0', 'Entra, minha filha. A porta tá só encostada.'),
      F('rc_s1', 'Lia! Senta aí, que o café sai já.', { conf: [2, 3] }),
      F('rc_s2', '(Seu Raimundo ajeita a colcha com as duas mãos, devagar.)', { loc: 'cama' }),
      F('rc_s3', 'Tô regando. Planta também tem fila.', { loc: 'planta' }),
      F('rc_s4', 'Shh... só um instante.', { loc: 'oratorio' }, { revisar: true }),
      F('rc_s5', 'Vou tomar o café sentado, que a perna reclama.', { loc: 'mesa' }),
      F('rc_s6', 'Daqui eu vejo quem passa. E quem não passa mais.', { loc: 'janela' }),
      F('rc_s7', 'O rádio fala baixo, mas fala muito.', { loc: 'radio' }),
      F('rc_s8', 'Cuidado com o fogão, filha. É velho e teimoso.', { loc: 'fogao' }),
      F('rc_s9', 'Obrigado pela água da outra vez, viu? Fica à vontade.', { mem: 'lia_ajudou_agua' }),
    ],
    ouvir: [
      F('rc_o0', '(Ele cantarola uma melodia sem letra enquanto ajeita a colcha.)', { loc: 'cama' }),
      F('rc_o1', '(A água cai devagar no vaso. Ele fala baixinho com a folhagem.)', { loc: 'planta' }),
      F('rc_o2', '(Ele murmura uma reza de olhos fechados. Você espera.)', { loc: 'oratorio' }, { revisar: true }),
      F('rc_o3', '(Seu Raimundo olha a rua em silêncio, balançando bem devagar.)', { loc: 'janela' }),
      F('rc_o4', '(O rádio fala do Programa. Ele abaixa o volume e fica olhando o aparelho.)', { loc: 'radio' }),
      F('rc_o5', '(O pó é medido com a colher, duas vezes, sem pressa.)', { loc: 'fogao', estado: 'coando' }),
      F('rc_o6', '(Ele passa o polegar nas pedras da caixa, uma a uma, como quem conta.)', { loc: 'mesa' }),
      F('rc_o7', 'Em casa o dia é comprido. Por isso eu saio cedo.'),
    ],
    perguntar: {
      rua: [F('rc_pr0', 'Daqui de cima a rua parece parada. Mas tá tudo mudando por baixo.'), F('rc_pr1', 'Todo dia alguém sai e não volta pra rua. Uns vão pra longe, outros vão pro papel.', { conf: [2, 3] })],
      mae: [F('rc_pm0', 'Minha mãe? Fazia o pão da sexta. Por enquanto é só isso que eu conto.', { conf: [0, 1] }),
            F('rc_pm1', 'Ela deixava o pão de sexta na porta de cada um. Quem podia pagava na hora; quem não podia, depois. Dali eu aprendi que dívida se paga olhando nos olhos, e que isso é coisa de gente honrada.', { conf: [2, 3] })],
      casa: [F('rc_pk0', 'Essa casa tem mais lembrança que móvel. Gosto assim.'), F('rc_pk1', 'Cada coisa aqui tem de onde veio. Pergunta que eu conto.', { conf: [1, 3] })],
      retrato: [F('rc_pt0', 'É ela. Não gostava de retrato, mas deixou esse. Disse que era pra eu não esquecer a cara de brava.')],
      forno: [F('rc_pf0', 'O forno da minha mãe. Antes do sol ela já tava com a lenha acesa. A Áurea sabe.'), F('rc_pf1', 'A sexta começou ali: pão quente de manhã, conta fechada à noite. Eu só não quis mudar.', { conf: [1, 3] })],
      programa: [F('rc_pp0', 'Já me falaram de papel e de medida. Só não falaram de quem fica.'), F('rc_pp1', 'Aqui dentro quem manda é o morador. Eu só não sei até quando.', { conf: [2, 3] })],
      papel: [F('rc_pa0', 'Papel? Só o da caderneta. Por enquanto.')],
      assinar: [F('rc_pg0', 'Assinar? Eu não assino o que não sei ler, e o que sei ler eu mostro pra Áurea antes.')],
      domino: [F('rc_pd0', 'Se jogo? Falta só uma pedra, mas a gente dá um jeito. Passa na calçada um dia desses pra ver.', { conf: [1, 3] }), F('rc_pd1', 'Jogo, claro. Mas dominó se aprende olhando. Aparece.', { conf: [0, 0] })],
    },
    ajudar: { cafe: [F('rc_aj0', 'Isso, duas colheres. Mais amarga, menos é água suja.')], agua: [F('rc_aj1', 'Ah, a água da talha. Deus lhe pague, minha filha.')], regar: [F('rc_aj2', 'Tá vendo? Folha que recebe, devolve.')] },
    murmurio: [
      F('rc_m0', '(cantarola sem letra)', { loc: 'cama' }), F('rc_m1', 'Dobra aqui, dobra ali...', { loc: 'cama' }),
      F('rc_m2', 'Bebe, que hoje o sol vem forte.', { loc: 'planta' }), F('rc_m3', '(reza baixinho)', { loc: 'oratorio' }, { revisar: true }),
      F('rc_m4', 'Hum. Aquele ali é o filho da Neide...', { loc: 'janela' }), F('rc_m5', 'Hoje a rua tá mais quieta.', { loc: 'janela' }),
      F('rc_m6', '(abaixa o volume do rádio)', { loc: 'radio' }), F('rc_m7', 'Duas colheres. Nem mais, nem menos.', { loc: 'fogao', estado: 'coando' }),
      F('rc_m8', 'Faltou sal. Sempre falta no começo.', { loc: 'fogao' }), F('rc_m9', 'Seis-seis... onde foi parar o seis-seis.', { loc: 'mesa' }),
    ],
    reacao_exame: {
      retrato_1: [F('rc_re0', 'Pode olhar. Com os olhos só, hein.', { conf: [0, 1] }), F('rc_re1', 'Essa é ela. Tinha um olhar que desmontava qualquer discussão.', { conf: [2, 3] })],
      foto_forno_1: [F('rc_re2', 'Esse forno quem acendia era ela.')],
      oratorio_1: [F('rc_re3', 'Aí a gente conversa em voz baixa, filha.')],
      domino_1: [F('rc_re4', 'Já viu que falta uma. Fui eu que fiz a outra.', { conf: [1, 3] })],
      cama_1: [F('rc_re5', 'A cama eu arrumo sozinho. Sempre arrumei.')],
    },
    chegou: [F('rc_ch0', 'Ufa. A escada é a parte mais comprida do dia.'), F('rc_ch1', 'Em casa. Que bom.')],
    saiu: [F('rc_sa0', 'Vou lá na Áurea, que o café não se toma sozinho.')],
  },
  objetos: {
    fogao_1: { kp: 'kp_c_fogao', texto: w => w.obj('fogao_1') ? 'Fogão de quatro bocas, uma delas acesa. A cafeteira esquenta; o cheiro de pó chega até a porta.' : 'Fogão de quatro bocas. Só duas têm uso; as outras estão limpas demais pra quem cozinha todo dia.' },
    talha_1: { kp: 'kp_c_talha', texto: () => 'Um filtro de barro com tampa de madeira e torneira, sobre o suporte encostado na parede, e uma caneca esmaltada embaixo. Você enche a caneca; a água é fresca.' },
    foto_forno_1: { kp: 'kp_c_foto', texto: () => 'Uma mulher de avental na porta de um forno de lenha. Na borda, a lápis, uma data: uma sexta-feira.' },
    sacola_1: { kp: 'kp_c_sacola', texto: () => 'Uma sacola de pano remendada, as alças gastas. Está no prego, ao lado do chapéu de palha, como quem deixa tudo pronto pra sair.' },
    balanco_1: { kp: null, texto: () => 'Cadeira de balanço de madeira escura, com encosto de palhinha e uma almofada de retalho. Fica ao lado da janela, virada para dentro de casa.' },
    oratorio_1: { kp: 'kp_c_oratorio', texto: w => 'Oratório de madeira de porta aberta: uma estampa do Senhor do Bonfim, fitas penduradas e uma vela' + (w.obj('oratorio_1') ? ' acesa.' : ' pequena.') },
    retrato_1: { kp: 'kp_c_retrato', texto: () => 'Retrato oval em sépia: uma senhora de lenço branco na cabeça, séria. É o mesmo lenço da moça de uma das fotografias da padaria.' },
    armario_1: { kp: 'kp_c_armario', texto: () => 'Guarda-roupa de duas portas, uma com espelho. Pela fresta: um paletó de domingo bem passado e camisas gastas nos punhos, remendadas com linha da mesma cor.' },
    criado_1: { kp: 'kp_c_radio', texto: () => 'Criado-mudo com um rádio de pilha e óculos de haste colada com esparadrapo. O dial está na mesma estação do rádio da vó.' },
    cama_1: { kp: 'kp_c_colcha', texto: () => 'Cama de solteiro com colcha de retalhos. A colcha é grande demais para uma cama só. Alguém a fez pensando numa casa mais cheia.' },
    mesa_1: { kp: 'kp_c_mesa', texto: () => 'Mesa de toalha branca posta para um, mas com a segunda cadeira puxada, como se alguém pudesse chegar.' },
    domino_1: { kp: 'kp_c_domino', texto: () => 'Caixa de dominó de madeira. Faltava a pedra seis-seis; alguém fez outra, de madeira, e pintou os pontos à mão.' },
    janela_sacada: { kp: 'kp_c_janela', texto: () => 'A porta-janela dá para a sacada de ferro e para a fachada rosa do outro lado da rua. Da cadeira de balanço, ao lado, ele escuta quem passa.' },
    cad_frente: { kp: null, texto: () => 'Cadeira da mesa.' }, cad_esq: { kp: null, texto: () => 'Cadeira da mesa.' }, cad_dir: { kp: null, texto: () => 'Cadeira da mesa.' }, cad_sul: { kp: null, texto: () => 'Cadeira da mesa.' }, cad_frente2: { kp: null, texto: () => 'Cadeira da mesa.' }, cad_sul2: { kp: null, texto: () => 'Cadeira da mesa.' },
  },
  kps: [
    K('kp_c_visita', 'Receber visita', 'Seu Raimundo me recebeu na porta de casa e falou em café antes de perguntar o que eu queria.', 'raimundo'),
    K('kp_c_cafe', 'O café dele', 'Coei o café com Seu Raimundo. Ele mede o pó com a colher do jeito que a mãe media: duas, nem mais, nem menos.', 'raimundo', { obj: 'fiado' }),
    K('kp_c_sacola_pao', 'O pão esquecido', 'Levei o pão que Seu Raimundo deixou no balcão. Ele agradeceu duas vezes e disse que a cabeça anda cheia de lembrança e vazia de sacola.', 'raimundo'),
    K('kp_c_rotina', 'A manhã dele', 'Ele arruma a cama, rega a planta, reza e só depois sai pra padaria. Não pula nenhuma etapa.', 'raimundo'),
    K('kp_c_mae', 'O pão de sexta', 'A mãe dele deixava o pão na porta de cada vizinho. Quem podia pagava na hora; quem não podia, na sexta. O fiado dele vem de casa; a mãe já anotava assim.', 'raimundo', { obj: 'fiado' }),
    K('kp_c_convite', 'O convite do dominó', 'Seu Raimundo me chamou pra ver o dominó na calçada. Disse que dominó se aprende olhando.', 'raimundo'),
    K('kp_c_assinar', 'O que ele não assina', 'Seu Raimundo só assina o que sabe ler, e mostra pra vó antes. Isso também é um jeito de se proteger do Programa.', 'raimundo', { obj: 'programa' }),
    K('kp_c_fogao', 'O fogão', 'Quatro bocas, duas em uso. O resto está limpo demais pra quem cozinha todo dia.', 'lugar'),
    K('kp_c_talha', 'O filtro de barro', 'Um filtro de barro com tampa de madeira, num suporte encostado na parede, e uma caneca esmaltada embaixo. Combina com o filtro da padaria: a mesma água de barro.', 'lugar'),
    K('kp_c_foto', 'O forno da mãe', 'Foto do forno de lenha com uma mulher de avental na porta. A data, a lápis, é de uma sexta.', 'lugar', { obj: 'fiado' }),
    K('kp_c_sacola', 'A sacola do prego', 'Sacola de pano remendada, alças gastas, pendurada ao lado do chapéu. Parece sempre pronta pra sair.', 'lugar'),
    K('kp_c_oratorio', 'O oratório dele', 'Uma estampa do Senhor do Bonfim, fitas e uma vela. Na padaria ele reza diante do nicho da vó; aqui, sozinho.', 'lugar', { revisar: true }),
    K('kp_c_retrato', 'A mãe, de lenço', 'Retrato oval de uma senhora de lenço branco. O mesmo lenço da moça da fotografia da padaria.', 'lugar', { obj: 'fiado' }),
    K('kp_c_armario', 'O paletó de domingo', 'Um paletó bem passado e camisas remendadas com linha da mesma cor. Cuida do que tem.', 'lugar'),
    K('kp_c_radio', 'O rádio de cabeceira', 'Está na mesma estação do rádio da vó. Óculos com a haste colada com esparadrapo ao lado.', 'lugar'),
    K('kp_c_colcha', 'A colcha de retalhos', 'Grande demais para uma cama só. Alguém a fez pensando numa casa mais cheia do que esta hoje.', 'lugar'),
    K('kp_c_mesa', 'A mesa posta para um', 'A toalha branca, a segunda cadeira puxada. Como se alguém pudesse chegar.', 'lugar'),
    K('kp_c_domino', 'A caixa de dominó', 'Faltava o seis-seis; ele fez outra pedra de madeira e pintou os pontos. Joga assim mesmo.', 'lugar'),
    K('kp_c_cafe_juntos', 'Café na mesa dele', 'Tomei café sentada na mesa de Seu Raimundo. Ele serve devagar, fala pouco e conta mais quando ninguém pergunta tudo de uma vez.', 'raimundo'),
    K('kp_c_janela', 'A janela da sacada', 'Sentado ali ao lado, ele escuta a rua inteira passar. Ele reconhece quem passa, quem entra e quem deixou de vir.', 'lugar'),
  ],
};

// Instala os dados da casa uma única vez (o mundo da casa chama isto; a padaria não).
Sim.Casa = Sim.Casa || {};
Sim.Casa.install = function () {
  if (Sim.Casa.installed) return; Sim.Casa.installed = true;
  const C = Sim.Data.casa;
  Sim.Data.conhecimentos = Sim.Data.conhecimentos.concat(C.kps);
  Object.assign(Sim.Data.objetos, C.objetos);
  Sim.Data.cfgCasa = true;
};
