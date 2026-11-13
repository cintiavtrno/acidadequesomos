// ===== s96_trama.js — a trama de 1996: falas, anotações, missões e fim da parte jogável =====
// DOM-free. Sem relógio: é um dia parado, a gravação do clipe. Texto simples, e tudo o que toca política ou história vem marcado rev (proposta, precisa de revisão).
// O que 1996 ensina e 1991/1994 não ensinaram:
//   · a rua como imagem: o clipe não é do Programa, mas mostra a rua que ele quer mostrar (pintada, policiada, desejada);
//   · a segunda fase do Programa (1996–1999): menos obra pesada, busca de dinheiro de fora, eventos para a classe média de Salvador;
//   · quem ficou e quem saiu: freguesia que sumiu, casa fora da lista, associação com lista menor;
//   · o que um dia de evento rende: o caixa de um dia e o mês que continua igual.
// O que a Lia guardou em 1991 e 1994 (localStorage do jogo e do quintal) abre atalhos, acrescenta falas e vira "ligações" no caderno.
Sim96.Trama = (function () {
  const T = {};
  const KEY = 'balcao_rua96_v1';

  T.NOMES = { lia: 'Lia', aurea: 'Dona Áurea', dandara: 'Dandara', tonho: 'Tonho', bela: 'Dona Bela', ze: 'Seu Zé', cicera: 'Dona Cícera', nonato: 'Nonato', junior: 'Júnior', zefa: 'Dona Zefa', rita: 'Dona Rita', assist_a: 'Assistente', assist_b: 'Assistente', raimundo: 'Seu Raimundo' };
  T.COR = { lia: '#9fd3a8', aurea: '#8fc0e8', dandara: '#e8a36b', tonho: '#e8cf6b', bela: '#d99ad0', ze: '#c9b08a', cicera: '#9fd0c4', nonato: '#e0c27a', junior: '#f0a0a0', zefa: '#9ab8e8', rita: '#d8b0e0', assist_a: '#c8c8c8', assist_b: '#c8c8c8', raimundo: '#d9b98c' };
  // id do ator no elenco → quem fala
  T.QUEM = { aurea: 'aurea', dandara: 'dandara', tonho: 'tonho', dom_F: 'bela', dom_E: 'ze', dom_T: 'cicera', dom_D: 'nonato', junior: 'junior', pub1: 'zefa', porta2: 'rita', assist_a: 'assist_a', assist_b: 'assist_b' };
  T.FIOS = [['clipe', 'O clipe e a imagem da rua'], ['fase2', 'A segunda fase do Programa'], ['ficou', 'Quem ficou e quem saiu'], ['renda', 'O que um dia de evento rende']];
  T.OPINIOES = ['kp_96_tonho', 'kp_96_saiu', 'kp_96_seguranca', 'kp_96_zefa'];

  // ---------------------------------------------------------------- anotações: id → [título, texto, fio, revisar]
  T.KP = {
    kp_96_gravacao: ['A rua fechada', 'A rua está fechada para a gravação de um clipe. A produção veio de fora, com equipe, câmera e grade, e a polícia fecha as esquinas. O clipe não é do Programa.', 'clipe', 1],
    kp_96_cenario: ['Nome de cenário', 'Na folha da locação a equipe chama os prédios pela cor e pela varanda. Não há nome de morador.', 'clipe'],
    kp_96_policia: ['Polícia nas esquinas', 'A polícia fecha as esquinas e quem mora passa depois de explicar o endereço. A produção pede silêncio quando a luz vermelha acende.', 'clipe', 1],
    kp_96_monitor: ['O que o monitor mostra', 'O monitor da produção mostra o palco e a fachada pintada. O prédio de tijolo aparente, mais à direita, fica fora do quadro.', 'clipe'],
    kp_96_tijolo: ['O prédio sem tinta', 'Dona Rita mora no prédio de tijolo aparente. Pintaram os dois vizinhos e o dela não, porque a casa não estava na lista.', 'clipe', 1],
    kp_96_vitrine: ['A rua como vitrine', 'O clipe não é do Programa, mas mostra a rua que ele quer mostrar: pintada, policiada e desejada. Quem mora aparece pouco, ou aparece atrás da grade.', 'clipe', 1],
    kp_96_fase2: ['A segunda fase', 'De 1996 a 1999 o Programa entra na segunda fase: a obra pesada diminui e o órgão procura dinheiro de fora. A aposta no turista de 1994 não bastou.', 'fase2', 1],
    kp_96_obra: ['A empreita acabou', 'Nonato terminou a parede da esquina em 1994 e não veio outro contrato. A obra pesada diminuiu.', 'fase2', 1],
    kp_96_quadro: ['A programação do mês', 'O quadro da associação agora traz a programação de eventos do mês no Centro Histórico, com o nome do órgão que organiza no rodapé. Em 1994 era só o cartaz do Dia & Noite.', 'fase2', 1],
    kp_96_evento: ['Evento para gente de Salvador', 'A segunda fase aposta em eventos culturais para atrair a classe média e alta de Salvador. A associação não é contra, mas quer ser chamada antes de o evento ser marcado.', 'fase2', 1],
    kp_96_saiu: ['Quem já foi', 'Dona Bela tinha metade das freguesas em 1994 e hoje atende cinco casas. Quem saiu levou a freguesia.', 'ficou'],
    kp_96_ficou: ['Quem ficou', 'A associação continua no mesmo sobrado, com lista de reunião menor porque mora menos gente.', 'ficou'],
    kp_96_padaria: ['A padaria fica', 'Dona Áurea fica. O aluguel é de loja para turista, e o pão de todo dia ainda é de quem mora.', 'ficou', 1],
    kp_96_raimundo: ['A porta do sobrado', 'Seu Raimundo não quis figurar no clipe e olha a rua pela fresta. A vizinha do lado foi embora e o Programa continua insistindo com ele.', 'ficou', 1],
    kp_96_mesa: ['A cadeira emprestada', 'Seu Raimundo não desceu para o dominó. Dona Cícera joga no lugar dele.', 'ficou'],
    kp_96_zefa: ['Quem gosta do que vê', 'Dona Zefa gosta da rua nova: calçada, luz, polícia e neto na porta sem medo. A casa dela foi restaurada.', 'ficou'],
    kp_96_pedido: ['A encomenda da produção', 'A produção encomendou pão e café para a equipe e pagou adiantado. A padaria vendeu num dia mais do que costuma, e amanhã volta ao movimento normal.', 'renda'],
    kp_96_tonho: ['Um dia que rende', 'Tonho vendeu num dia o que vende de terça a quinta. Amanhã desmontam o palco e o movimento volta ao normal.', 'renda'],
    kp_96_publico: ['Quem veio ver', 'A plateia tem turista de ônibus e gente de Salvador, de carro, que antes não vinha ao Centro. Compram e vão embora antes de escurecer.', 'renda'],
    kp_96_seguranca: ['Quem vem porque tem polícia', 'Seu Zé atende gente de Salvador que antes evitava o Centro e agora vem, com polícia na esquina. Eles vão embora antes de escurecer.', 'renda', 1],
  };

  // ---------------------------------------------------------------- ligações com o que a Lia guardou em 1991 e 1994 (aparecem no caderno)
  // se: anotações de 1996 necessárias; mem: qualquer anotação anterior (rua 1991/1994 ou quintal 1994). Sem mem, vale só pelo que se aprendeu hoje.
  T.LIGACOES = [
    { se: ['kp_96_evento'], mem: ['kp_94_lucia_evento', 'q_lucia_evento'], t: 'Em 1994 Lúcia falou de um evento maior, ainda conversa de corredor. Em 1996 a conversa tem forma: eventos culturais para gente de Salvador.', rev: 1 },
    { se: ['kp_96_fase2'], mem: ['kp_94_programa', 'kp_programa'], t: 'O Programa que começou com pintura e conserto em 1991 e virou remoção em 1994 entra, em 1996, numa fase de menos obra e mais evento. Quem decide continua sendo o órgão.', rev: 1 },
    { se: ['kp_96_fase2'], mem: ['kp_94_lucia_aposta', 'q_zefa_turista', 'kp_94_tonho_turista'], t: 'A aposta de 1994 era que o turista sustentasse a rua sozinho. Em 1996 o próprio Programa muda a conta e passa a procurar o morador de Salvador.', rev: 1 },
    { se: ['kp_96_tonho'], mem: ['kp_94_tonho_turista', 'kp_94_tonho_show', 'q_tonho_show'], t: 'Tonho disse em 1994 que o show de graça trazia gente que não gasta. Em 1996 ele vende num dia a semana inteira, mas o dia seguinte continua fora do controle dele.' },
    { se: ['kp_96_raimundo'], mem: ['kp_94_ray_aviso', 'q_raimundo_sobrado', 'kp_94_ray_marca', 'kp_94_obj_aviso'], t: 'O aviso e a marca de tinta de 1994 continuam no sobrado de Seu Raimundo. Ele ainda não saiu.' },
    { se: ['kp_96_vitrine'], mem: ['kp_rua_olhar', 'kp_94_rua_olhar'], t: 'Dona Bela notou em 1991 e em 1994 gente de fora olhando as casas. Em 1996 quem olha são câmeras, e a rua inteira está enquadrada.' },
    { se: ['kp_96_saiu'], mem: ['kp_94_bela_freguesas', 'kp_94_ray_vazias'], t: 'As casas fechadas da rua de cima em 1994 viraram freguesia a menos para Dona Bela em 1996.' },
    { se: ['kp_96_ficou'], mem: ['kp_associacao', 'kp_94_obj_faixa'], t: 'A associação de 1991 continua sendo o lugar onde quem mora se organiza, agora com uma lista menor.' },
    { se: ['kp_96_tijolo'], mem: ['q_rita_telhado'], t: 'O telhado de lona de Dona Rita em 1994 e o prédio sem tinta em 1996 podem ser a mesma casa fora da lista.', rev: 1 },
    { se: ['kp_96_obra'], mem: ['kp_94_nonato_obra'], t: 'O contrato de Nonato acabava com a fachada, como ele avisou em 1994. A obra pesada acabou antes de outra começar.' },
    { se: ['kp_96_vitrine', 'kp_96_fase2'], t: 'A imagem da rua pesa na segunda fase: rua limpa e segura atrai quem mora em Salvador e atrai dinheiro de fora.', rev: 1 },
    { se: ['kp_96_pedido', 'kp_96_tonho'], t: 'Evento paga por dia. Quem vive de venda precisa de movimento todos os dias.' },
  ];

  // ---------------------------------------------------------------- conversas
  // Linha: [quem, texto, memória?]. quem 'nota' é um aviso de Lia. O 3º item (lista de anotações antigas) faz a linha aparecer só se a Lia as tiver.
  // Assunto: { id, label, ver(E), lin, da: [anotações], faz }
  const F = {};
  T.FALAS = F;

  F.aurea = {
    saudar: ['Lia. Chegou na hora. A rua está parada e o forno não.', 'Pode falar, Lia. Estou de olho no balcão e no palco.'],
    rep: 'Já te contei o que eu sabia sobre isso, Lia.',
    topicos: [
      { id: 'encomenda', label: 'A encomenda da produção', ver: E => !E.flag('cesta') && !E.flag('entregue'), faz: 'pegarCesta', lin: [
        ['aurea', 'A produção encomendou pão e café para a equipe inteira. Veio um rapaz com uma lista e pagou adiantado.'],
        ['aurea', 'Fiz o dobro da fornada. Leva esta cesta para a assistente da produção. Ela fica no meio da rua, perto do monitor, com uma prancheta.'],
        ['aurea', 'Em 94 eu fazia uma fornada dessas para a rua inteira e ainda sobrava pão. Hoje uma encomenda só dá conta dela.', ['q_aurea_freguesia']],
        ['nota', 'Lia pegou a cesta de pão. Ela fica com você até a entrega.']] },
      { id: 'cesta', label: 'Onde entrego a cesta?', ver: E => E.flag('cesta') && !E.flag('entregue'), lin: [
        ['aurea', 'Para a assistente da produção. Ela anda entre o monitor e a câmera, com uma prancheta e um rádio.']] },
      { id: 'como_foi', label: 'Como foi a encomenda?', ver: E => E.flag('entregue') && !E.flag('m1'), faz: 'm1fim', da: ['kp_96_pedido'], lin: [
        ['aurea', 'Ela pagou sem pechinchar e pediu nota. Eu nunca tinha emitido nota de um pedido desse tamanho.'],
        ['aurea', 'Hoje o caixa fecha cheio. Amanhã a equipe desmonta tudo e a padaria volta a vender para quem mora, que é pouca gente.']] },
      { id: 'padaria', label: 'A padaria', ver: () => true, da: ['kp_96_padaria'], lin: [
        ['aurea', 'A padaria fica. O aluguel novo é de loja de turista e eu pago, porque o forno é meu e o freguês é daqui.'],
        ['lia', 'A plaquinha em inglês ainda está lá fora.', ['kp_94_obj_turista', 'q_aurea_papel']],
        ['aurea', 'Virou plaqueta de esmalte, presa na parede. Parece que agora faz parte da fachada.', ['kp_94_obj_turista', 'q_aurea_papel']]] },
      { id: 'fechar', label: 'Fechar o dia', ver: E => E.flag('m1') && E.flag('m2') && E.flag('m3') && !E.flag('fim'), faz: 'fim', lin: [
        ['aurea', 'Fechou a conta do dia? Então senta. Eu conto o troco e você escreve no caderno o que viu.'],
        ['nota', 'O dia na rua chegou ao fim.']] },
    ],
  };

  F.dandara = {
    saudar: ['Lia. Veio ver a gravação ou veio me ajudar?', 'Lia, chega mais perto. Aqui a gente escuta melhor.'],
    rep: 'Já falei disso, Lia. Se ficou dúvida, olha de novo o que a gente viu.',
    topicos: [
      { id: 'clipe', label: 'A gravação', ver: () => true, faz: 'm2inicio', da: ['kp_96_gravacao'], lin: [
        ['dandara', 'É gravação de clipe. Veio gente de fora, com câmera e tambor contratado, e a polícia fechou as esquinas. Dizem que o maior astro do planeta pediu esta rua.'],
        ['dandara', 'O clipe não é do Programa. Quem organiza é a produção.'],
        ['dandara', 'Mas olha o que ela filma: fachada pintada, calçada limpa, polícia na esquina. Vai olhar o monitor da produção, ali na base, e conversa com Dona Rita, na porta do prédio de tijolo. Depois volta aqui.']] },
      { id: 'camera', label: 'O que a câmera vê', ver: E => E.tem('kp_96_monitor') && E.tem('kp_96_tijolo'), faz: 'm2fim', da: ['kp_96_vitrine'], lin: [
        ['lia', 'No monitor só entra a parede pintada. O prédio de Dona Rita ficou de fora.'],
        ['dandara', 'Isso. O Programa queria mostrar uma rua limpa, segura e desejada, e agora o mundo inteiro vai ver.'],,
        ['dandara', 'Quem mora aqui não aparece na imagem, ou aparece atrás da grade.'],
        ['dandara', 'Dona Bela já te falou de gente olhando as casas. Antes olhavam com os olhos. Hoje é com câmera.', ['kp_rua_olhar', 'kp_94_rua_olhar']]] },
      { id: 'fase2', label: 'O Programa agora', ver: E => E.tem('kp_96_vitrine') || E.mem(['kp_94_programa', 'kp_94_lucia_evento', 'q_lucia_evento', 'kp_94_dandara_dn', 'q_dandara_dn']), faz: 'm3inicio', da: ['kp_96_fase2'], lin: [
        ['dandara', 'O Programa entrou numa segunda fase, de 1996 a 1999. A obra pesada diminuiu e o órgão procura dinheiro de fora para continuar.'],
        ['dandara', 'Em 94 eu te contei que ele começou com pintura e virou remoção. Agora a pressa é mostrar resultado.', ['kp_94_programa']],
        ['dandara', 'A aposta era o turista sustentar a rua sozinho. Não deu. De terça a quinta ela esvazia e o caixa não fecha.'],
        ['lia', 'A Lúcia falou de um evento maior, que ainda era conversa de corredor.', ['kp_94_lucia_evento', 'q_lucia_evento']],
        ['dandara', 'Pois é. A conversa saiu do corredor.', ['kp_94_lucia_evento', 'q_lucia_evento']],
        ['dandara', 'O plano novo é encher a rua de evento para gente de Salvador, de classe média, que tem salário e carro. Converse com três vizinhos sobre como a rua está hoje e me conta o que ouviu.']] },
      { id: 'evento', label: 'O que os vizinhos disseram', ver: E => E.tem('kp_96_fase2') && E.opin() >= 3 && !E.flag('m3'), faz: 'm3fim', da: ['kp_96_evento'], lin: [
        ['lia', 'Cada um fez a conta do seu jeito. Quem vende conta o caixa e quem mora conta quem saiu.'],
        ['dandara', 'Evento enche a rua por um dia e o caixa de quem vende por mais um. Quem mora precisa de casa, luz e água, e isso não aparece no palco.'],
        ['dandara', 'A associação não é contra evento. Quer ser chamada antes de ele ser marcado. Hoje o convite chega pronto.']] },
      { id: 'associacao', label: 'A associação hoje', ver: () => true, da: ['kp_96_ficou'], lin: [
        ['dandara', 'A associação continua no mesmo sobrado azul, com a mesma mesa. A lista da reunião é menor, porque mora menos gente.']] },
    ],
  };

  F.tonho = {
    saudar: ['Cocada, queijadinha! Hoje eu vendi a semana antes do almoço.'],
    rep: 'Já te falei, Lia. Quer cocada?',
    topicos: [
      { id: 'venda', label: 'A venda de hoje', ver: () => true, da: ['kp_96_tonho'], lin: [
        ['tonho', 'Fiz de um dia o que eu fazia de terça a quinta. Veio gente de ônibus, equipe, polícia, todo mundo com fome.'],
        ['lia', 'Em 94 o senhor dizia que de terça a quinta passa um ou outro.', ['kp_94_tonho_turista', 'q_tonho_show', 'kp_94_tonho_show']],
        ['tonho', 'Pois é. Amanhã desmontam o palco e eu volto para o isopor cheio. O dia compensa, o mês continua o mesmo.']] },
      { id: 'plateia', label: 'Quem veio hoje', ver: () => true, da: ['kp_96_publico'], lin: [
        ['tonho', 'Tem turista de ônibus e tem gente de Salvador, de carro, que eu nunca tinha visto por aqui. Perguntam o preço, pagam sem reclamar e vão embora antes de escurecer.']] },
    ],
  };

  F.bela = {
    saudar: ['Lia. Senta direito. Estou contando pedra e contando gente.'],
    rep: 'Já falei, menina. Presta atenção na pedra.',
    topicos: [
      { id: 'freguesas', label: 'As freguesas', ver: () => true, da: ['kp_96_saiu'], lin: [
        ['lia', 'A senhora tinha dito que metade da freguesia já tinha saído.', ['kp_94_bela_freguesas']],
        ['bela', 'Agora são cinco casas. Entrego a pé.'],
        ['bela', 'Evento é bom para quem vende comida. Bainha ninguém compra em palco, e quem vem de carro não leva roupa para consertar.']] },
    ],
  };

  F.ze = {
    saudar: ['Menina! A rua cheia e a barbearia vazia. Me explica isso.'],
    rep: 'Já te contei, Lia. Joga uma pedra.',
    topicos: [
      { id: 'barbearia', label: 'A barbearia', ver: () => true, da: ['kp_96_seguranca'], lin: [
        ['ze', 'Turista tira foto da cadeira e não senta.'],
        ['ze', 'Gente de Salvador que tinha medo de passar aqui vem agora, corta o cabelo, olha a polícia na esquina e vai embora antes de escurecer.'],
        ['ze', 'Se o evento traz freguês que volta, eu gosto. Se traz quem passa uma vez só, é feira.']] },
    ],
  };

  F.cicera = {
    saudar: ['Lia. Quem passa hoje está só de passagem.'],
    rep: 'Já te falei, Lia. Pega o lençol.',
    topicos: [
      { id: 'esquinas', label: 'As esquinas fechadas', ver: () => true, da: ['kp_96_policia'], lin: [
        ['cicera', 'Fecharam as duas esquinas de cima com policial e fita. Quem mora passa, mas explica o endereço. Eu expliquei o meu duas vezes.']] },
    ],
  };

  F.nonato = {
    saudar: ['E aí, Lia. A mão está parada.'],
    rep: 'Já te contei, Lia. Não tem mais o que dizer.',
    topicos: [
      { id: 'empreita', label: 'A obra da esquina', ver: () => true, da: ['kp_96_obra'], lin: [
        ['lia', 'A parede da esquina, Nonato. O senhor ainda levanta?', ['kp_94_nonato_obra']],
        ['nonato', 'Terminei em 94 e não veio outro contrato. Dizem que a obra pesada diminuiu e que o órgão está atrás de dinheiro de fora.'],
        ['nonato', 'Hoje meu primo carrega case para a produção. Paga por dia, uma vez só.']] },
    ],
  };

  F.junior = {
    saudar: ['Lia! Você viu a câmera grande?'],
    rep: 'Já te falei, Lia! Vem ver a câmera.',
    topicos: [
      { id: 'camera', label: 'A câmera', ver: () => true, lin: [
        ['junior', 'Eu cheguei perto e um homem de colete disse que ali é área da produção. Só pode olhar atrás da grade.'],
        ['junior', 'Eu olho. Mas daqui eu não vejo o monitor.']] },
      { id: 'casa', label: 'A casa da esquina', ver: E => E.mem(['kp_94_junior_casa', 'kp_gato', 'kp_94_junior_foto']), lin: [
        ['junior', 'A casa da esquina agora tem tábua na porta e uma fita. O gato vem comer pão na padaria.']] },
    ],
  };

  F.zefa = {
    saudar: ['Lia! Olha a rua. Eu falei que um dia a gente ia aparecer na televisão.'],
    rep: 'Já te falei, minha filha. Aproveita o dia.',
    topicos: [
      { id: 'rua', label: 'A rua hoje', ver: () => true, da: ['kp_96_zefa'], lin: [
        ['zefa', 'Eu acho lindo. Calçada nova, luz, polícia, neto na porta sem medo. Quem diz que o Programa não presta devia olhar para esta rua hoje.'],
        ['lia', 'A senhora disse no caruru que a sua casa foi restaurada.', ['q_zefa_casa', 'q_zefa_reforma']],
        ['zefa', 'E foi, graças a Deus. Eu sei que nem todo mundo teve a mesma sorte, mas não vou fingir que não gosto.', ['q_zefa_casa', 'q_zefa_reforma']]] },
    ],
  };

  F.rita = {
    saudar: ['Lia. Vem cá na porta. Olha o meu prédio.'],
    rep: 'Já te contei, Lia. O prédio continua do mesmo jeito.',
    topicos: [
      { id: 'tinta', label: 'O prédio sem pintura', ver: () => true, da: ['kp_96_tijolo'], lin: [
        ['rita', 'Pintaram o prédio da esquerda e o da direita. O meu ficou como estava. Perguntei ao rapaz da tinta e ele disse que a minha casa não estava na lista.'],
        ['lia', 'E o telhado, Dona Rita?', ['q_rita_telhado']],
        ['rita', 'A lona continua lá. O laudo disse que não vale o conserto, e eu não posso consertar sozinha.', ['q_rita_telhado']]] },
    ],
  };

  F.assist_a = {
    saudar: ['Oi! Você é de onde? Eu só consigo falar um minuto.'],
    rep: 'Já falei, desculpa. Preciso voltar para a prancheta.',
    topicos: [
      { id: 'entrega', label: 'A cesta da padaria', ver: E => E.flag('cesta') && !E.flag('entregue'), faz: 'entregarCesta', lin: [
        ['lia', 'A Vó Áurea mandou esta cesta. É o pedido da produção.'],
        ['assist_a', 'Ah, a padaria! Obrigada. Deixa em cima do case. O café é para o pessoal do som e o pão é para quem sobrar.'],
        ['nota', 'Cesta entregue. Falta contar para a Vó Áurea como foi.']] },
      { id: 'locacao', label: 'Como vocês chamam a rua', ver: () => true, da: ['kp_96_cenario'], lin: [
        ['assist_a', 'A gente chama os prédios pela cor e pela varanda: o azul da varanda, o rosa, o creme. Na folha da locação não tem nome de morador.']] },
    ],
  };

  F.assist_b = {
    saudar: ['Shh. Quando a luz vermelha acende, ninguém fala.'],
    rep: 'Já falei, desculpa. A luz vai acender de novo.',
    topicos: [
      { id: 'silencio', label: 'O silêncio da gravação', ver: () => true, da: ['kp_96_policia'], lin: [
        ['assist_b', 'Quando a luz vermelha acende, ninguém fala e ninguém bate porta. A polícia fecha as esquinas e a gente cuida do resto.'],
        ['assist_b', 'Os vizinhos têm ajudado. Quem queria atravessar a rua teve que esperar, e foi o mais difícil.']] },
    ],
  };

  // Seu Raimundo fala pela fresta da porta do sobrado (não há sprite dele na rua de 1996)
  F.raimundo = {
    saudar: ['(A voz vem de dentro, pela fresta.) Quem é? Ah, Lia. Entra não. Estou olhando a rua daqui.'],
    rep: 'Já te disse, Lia. Vai lá, que a rua está cheia.',
    topicos: [
      { id: 'clipe', label: 'A gravação', ver: () => true, da: ['kp_96_raimundo'], lin: [
        ['raimundo', 'Aqui ninguém me chamou para figurar. Fico em casa.'],
        ['raimundo', 'O sobrado é o que sobrou da minha mãe. A vizinha do lado já foi embora e o Programa não me larga.'],
        ['lia', 'O aviso ainda está na porta?', ['kp_94_ray_aviso', 'q_raimundo_sobrado', 'kp_94_obj_aviso']],
        ['raimundo', 'Está. O papel é o mesmo, e a tinta laranja também.', ['kp_94_ray_aviso', 'q_raimundo_sobrado', 'kp_94_obj_aviso']]] },
      { id: 'mesa', label: 'O dominó', ver: E => E.tem('kp_96_raimundo'), da: ['kp_96_mesa'], lin: [
        ['raimundo', 'Quem sentou no meu lugar? A Cícera? Ela joga melhor que eu. Diga que a cadeira é emprestada.']] },
    ],
  };

  // ---------------------------------------------------------------- objetos (substituem a descrição da cena quando há anotação)
  T.OBJ = {
    base_monitor: { kp: 'kp_96_monitor', desc: 'No monitor de tubo aparece, em preto e branco, o palco e a fachada azul ao fundo. A parede pintada enche o quadro. O prédio de tijolo aparente, mais à direita, não entra.' },
    quadro_avisos: { kp: 'kp_96_quadro', desc: 'Quadro da associação: reunião de moradores, rifa de uma geladeira e, no meio, uma folha impressa com a programação de eventos do mês no Centro Histórico. No rodapé, o nome do órgão que organiza.' },
    mesa_domino: { desc: 'A mesa continua verde, com a garrafa térmica no canto. Falta uma pessoa: Seu Raimundo não desceu hoje.' },
  };

  // ---------------------------------------------------------------- missões
  T.MISSOES = [
    { id: 'm1', titulo: 'A encomenda da produção', passos: E => E.flag('m1') ? 3 : E.flag('entregue') ? 2 : E.flag('cesta') ? 1 : 0,
      txt: ['Falar com Dona Áurea, na porta da padaria.', 'Levar a cesta para a assistente da produção, perto do monitor.', 'Contar para Dona Áurea como foi.'] },
    { id: 'm2', titulo: 'O que a câmera vê', passos: E => E.flag('m2') ? 3 : (E.flag('m2inicio') ? 1 + (E.tem('kp_96_monitor') && E.tem('kp_96_tijolo') ? 1 : 0) : 0),
      txt: ['Falar com Dandara, na frente da associação.', E => 'Olhar o monitor da produção (' + (E.tem('kp_96_monitor') ? 'feito' : 'falta') + ') e conversar com Dona Rita, no prédio de tijolo (' + (E.tem('kp_96_tijolo') ? 'feito' : 'falta') + ').', 'Voltar para Dandara.'] },
    { id: 'm3', titulo: 'A rua e os eventos', passos: E => E.flag('m3') ? 3 : (E.flag('m3inicio') ? 1 + (E.opin() >= 3 ? 1 : 0) : 0),
      txt: ['Perguntar a Dandara sobre o Programa.', E => 'Ouvir três vizinhos: Tonho, Dona Bela, Seu Zé ou Dona Zefa (' + Math.min(3, E.opin()) + ' de 3).', 'Voltar para Dandara.'] },
  ];

  // ---------------------------------------------------------------- motor
  T.criar = function (o) {
    o = o || {};
    const st = o.storage || (typeof localStorage !== 'undefined' ? localStorage : null);
    const forcar = o.mem || null;   // 'tudo' simula quem jogou 1991 e 1994 por inteiro (teste)
    let S = { kp: {}, feitos: {}, flags: {}, visitas: {}, n: 0 };
    const ler = k => { try { return st ? JSON.parse(st.getItem(k) || 'null') : null; } catch (e) { return null; } };
    const gravar = () => { try { if (st) st.setItem(KEY, JSON.stringify(S)); } catch (e) { } };
    const prev = ler(KEY); if (prev && !o.novo) S = Object.assign(S, prev);
    const antigas = new Set();
    for (const k of ['balcao_rua_v1', 'balcao_quintal_kp']) { const j = ler(k); if (j && j.kp) Object.keys(j.kp).forEach(x => antigas.add(x)); }
    const E = {
      tem: id => !!S.kp[id],
      mem: ids => forcar === 'tudo' ? true : (ids || []).some(i => antigas.has(i)),
      flag: k => !!S.flags[k],
      opin: () => T.OPINIOES.filter(k => S.kp[k]).length,
      antigas: () => forcar === 'tudo' ? 'tudo' : antigas.size,
    };
    const ganhar = id => { if (!T.KP[id] || S.kp[id]) return false; S.kp[id] = { n: ++S.n }; gravar(); return true; };
    const ACOES = {
      pegarCesta: () => { S.flags.cesta = 1; }, entregarCesta: () => { S.flags.entregue = 1; }, m1fim: () => { S.flags.m1 = 1; },
      m2inicio: () => { S.flags.m2inicio = 1; }, m2fim: () => { S.flags.m2 = 1; }, m3inicio: () => { S.flags.m3inicio = 1; }, m3fim: () => { S.flags.m3 = 1; }, fim: () => { S.flags.fim = 1; },
    };
    const linhas = ls => ls.filter(l => !l[2] || E.mem(l[2])).map(l => ({ quem: l[0], texto: l[1], nota: l[0] === 'nota', rev: false }));
    return {
      E, T,
      get s() { return S; },
      nome: q => T.NOMES[q] || q,
      falante: id => T.QUEM[id] || (F[id] ? id : null),
      tem: E.tem, flag: E.flag,
      abrir(q) {
        const f = F[q]; if (!f) return null; const n = S.visitas[q] = (S.visitas[q] || 0) + 1; gravar();
        return { quem: q, saudacao: f.saudar[(n - 1) % f.saudar.length], topicos: this.topicos(q) };
      },
      topicos(q) {
        const f = F[q]; if (!f) return [];
        return f.topicos.filter(t => t.ver(E)).map(t => ({ id: t.id, label: t.label, feito: !!S.feitos[q + '.' + t.id] }));
      },
      perguntar(q, id) {
        const f = F[q], t = f && f.topicos.find(x => x.id === id); if (!t || !t.ver(E)) return { linhas: [], novas: [] };
        const chave = q + '.' + id, ja = !!S.feitos[chave];
        if (ja && !t.faz) return { linhas: [{ quem: q, texto: f.rep, nota: false }], novas: [] };
        const out = linhas(t.lin), novas = [];
        if (!ja) { S.feitos[chave] = 1; if (t.faz) ACOES[t.faz](); for (const k of (t.da || [])) if (ganhar(k)) { novas.push(k); out.push({ quem: 'nota', texto: 'Anotado: ' + T.KP[k][0], nota: true }); } gravar(); }
        else return { linhas: [{ quem: q, texto: f.rep, nota: false }], novas: [] };
        return { linhas: out, novas };
      },
      exam(id) {
        const x = T.OBJ[id]; if (!x) return null; const nova = x.kp ? ganhar(x.kp) : false; return { texto: x.desc, kp: x.kp || null, nova, titulo: x.kp ? T.KP[x.kp][0] : null };
      },
      missoes() {
        return T.MISSOES.map(m => { const p = m.passos(E), feito = p >= 3, ativo = p > 0 || m.id === 'm1' || m.id === 'm2' || m.id === 'm3'; return { id: m.id, titulo: m.titulo, passo: p, feito, ativo, atual: feito ? null : (typeof m.txt[p] === 'function' ? m.txt[p](E) : m.txt[p]) }; });
      },
      podeFechar: () => E.flag('m1') && E.flag('m2') && E.flag('m3'),
      fim: () => E.flag('fim'),
      diario() {
        const notas = Object.keys(S.kp).sort((a, b) => S.kp[a].n - S.kp[b].n).map(id => ({ id, titulo: T.KP[id][0], texto: T.KP[id][1], fio: T.KP[id][2], rev: !!T.KP[id][3] }));
        const lig = T.LIGACOES.filter(l => l.se.every(k => S.kp[k]) && (!l.mem || E.mem(l.mem))).map(l => ({ texto: l.t, rev: !!l.rev, antiga: !!l.mem }));
        return { notas, total: Object.keys(T.KP).length, ligacoes: lig };
      },
      pular() { S.flags.fim = 1; S.flags.pulou = 1; gravar(); },
      zerar() { S = { kp: {}, feitos: {}, flags: {}, visitas: {}, n: 0 }; gravar(); },
    };
  };
  return T;
})();
