// ===== dialogo.js — conversa investigativa e anotações do quintal (1994) =====
// DOM-free. Acrescenta ao Quintal.Sim o mesmo jeito de conversar da rua: Cumprimentar, Perguntar, Ficar ouvindo.
// Cada pessoa só tem certos assuntos em certas fases do caruru, e vários só aparecem depois que a Lia olhou algo no quintal ou ouviu outra pessoa.
// As anotações (this.kp) são o que conta para a meta de 6 anotações novas de 1994. Fora do caruru (fase N) não há anotação.
(function (root) {
  'use strict';
  const Q = (typeof module !== 'undefined' && module.exports) ? require('./quintal.js') : root.Quintal;
  const Sim = Q.Sim, KEY = 'balcao_quintal_kp';

  // ---------------------------------------------------------------- anotações: id → [título, texto, precisa de revisão]
  // 1994: de 1992 a 1995 o Programa acelera (obra pesada, casa interditada, morador saindo). Dona Zefa defende a reforma e quase todo o resto da mesa sente o custo.
  // A aposta desta etapa: turistas do Brasil e de fora sustentam o comércio da rua sozinhos. Textos propostos; o que toca política, história ou ritual vai marcado para revisão.
  const K = {
    // o que se vê no quintal
    q_banner: ['A bandeira dos santos', 'Bandeira de Cosme e Damião na parede da casa. Embaixo, um prato servido, uma vela e flores brancas. A primeira porção é dos santos.', true],
    q_oferenda: ['A mesa baixa', 'Só Dona Zefa e Dona Nena chegam perto da mesa da oferenda. Eu olhei de longe.', true],
    q_mesa: ['A mesa dos adultos', 'Dez lugares com toalha. Os adultos só comem depois das crianças.'],
    q_portao: ['O portão da Rita', 'O portão do fundo dá na casa da Rita. De lá se vê o telhado dela, com a lona e o balde no canto.'],
    q_mangueira: ['A mangueira', 'A mangueira é mais velha que o quintal. A sombra cobre o fundo e passa do muro.'],
    // o que as pessoas contam
    q_quiabo: ['O quiabo fino', 'Dona Zefa corta o quiabo fino e molha a faca antes de cada corte, para não babar. O dendê entra depois.', true],
    q_zefa_pai: ['Por que a Zefa faz o caruru', 'O pai de Dona Zefa fazia o caruru todo ano. Quando ele parou, o quintal ficou anos sem festa. Ela voltou a fazer quando a rua pediu.', true],
    q_zefa_reforma: ['Zefa a favor do Programa', 'Dona Zefa defende o Programa: calçada nova, luz, polícia na esquina e o bairro no jornal. Para ela a rua passou vinte anos esquecida e agora tem quem olhe.', true],
    q_zefa_turista: ['A aposta no turista', 'Dona Zefa acredita que o turista de outros estados e de fora do país sustenta sozinho o comércio da rua. Quer vender caruru para ele.', true],
    q_zefa_casa: ['A casa que fica', 'A casa de Dona Zefa entrou entre as que o Programa restaura e devolve ao dono. Ela reconhece que nem todo mundo na rua teve a mesma sorte.', true],
    q_aurea_balcao: ['A padaria sem balcão', 'Vó Áurea deixou o balcão sem ninguém. Disse que o pão espera um dia e o convite da Zefa não esperava.'],
    q_aurea_freguesia: ['Quem compra o pão', 'Vó Áurea diz que o turista entra, tira foto do forno e leva uma água. O pão de todo dia era de quem mora, e com casa vazia ela faz a mesma fornada e sobra pão.', true],
    q_aurea_papel: ['O aluguel novo', 'Junto com a fachada nova veio um papel com o aluguel novo da padaria, num valor de loja para turista. Vó Áurea leu três vezes e deixou na gaveta.', true],
    q_raimundo_sobrado: ['O aviso do sobrado', 'Colaram um aviso na porta do sobrado: a casa está em risco e precisa ser desocupada. Seu Raimundo recebeu oferta de indenização e de uma casa longe do centro. Ainda não assinou.', true],
    q_raimundo_vazias: ['As casas da rua de cima', 'Quem aceitou a indenização foi para o subúrbio. A rua de cima está quase toda fechada, e quase ninguém volta para visitar.', true],
    q_lista: ['A lista de avisos', 'A lista do Programa tem nome de morador, nome de dono e casas sem nome nenhum. Dandara vai ler tudo na reunião de sábado.', true],
    q_comodos: ['Quem aluga cômodo', 'Quem aluga cômodo não aparece em papel nenhum, então a indenização não passa por ele. A associação vai de porta em porta conferir quem mora onde.', true],
    q_lucia_convite: ['Lúcia no caruru', 'Dona Zefa convidou Lúcia pessoalmente. Disse que quem mede a rua também come nela. Lúcia veio sabendo que muita gente aqui não queria vê-la.'],
    q_lucia_ficha: ['A ficha vira valor', 'Lúcia agora faz a ficha de cada casa que sai: quem mora, quantos são e o valor oferecido. Ela assina embaixo e não sabe para onde essas pessoas vão.', true],
    q_lucia_evento: ['Conversa de corredor', 'Lúcia conta que o turista enche a rua no fim de semana e em dia de show, e que na terça a conta do comércio não fecha. No órgão do Programa já se fala em um evento maior, para trazer gente de Salvador. Ainda não há plano escrito.', true],
    q_zefa_dn: ['Pelourinho Dia & Noite', 'Dona Zefa gosta do Dia & Noite: show de graça todo dia nos largos reformados, com banda, teatro, dança e capoeira. Para ela, rua cheia de dia e de noite é o Programa funcionando.', true],
    q_tonho_show: ['Quando o show acaba', 'Tonho vende bem na roda de capoeira e na banda do Terreiro, mas a rua esvazia assim que o grupo termina. Show de graça traz gente que não gasta.', true],
    q_dandara_dn: ['Quem toca e quem mora', 'Dandara vai aos shows, mas lembra que o governo paga cachê a quem toca no largo e não paga nada a quem morava no casarão ao lado e foi embora.', true],
    q_rita_telhado: ['O telhado da Rita', 'O laudo diz que o telhado da Rita não vale conserto, mas ela não pode consertar por conta própria. A lona é o que sobrou.', true],
    q_rita_sombra: ['A sombra da mangueira', 'A mangueira é de Dona Zefa e a sombra cai na casa da Rita. Se a Rita for embora, a sombra fica sem quem use.'],
    q_nonato_empreita: ['Obra que acaba', 'Nonato trabalha por empreita nas obras do Programa e levanta a parede de uma casa cujos donos já saíram. Recebe por semana, e o contrato acaba com a fachada.', true],
    q_ze_turista: ['A cadeira que vira foto', 'Na barbearia entra turista para fotografar a cadeira. Corte mesmo, só dos clientes de sempre, e eles estão saindo da rua.', true],
    q_bela_panos: ['Os panos dos meninos', 'Dona Bela costurou um pano para cada menino. No fim, cada um leva o seu para casa.'],
    q_bela_freguesas: ['As freguesas que saíram', 'Dona Bela perdeu metade da freguesia de costura com as mudanças. Entrega de ônibus e a passagem come o ganho.', true],
    q_cicera_junior: ['Júnior e o varal', 'Dona Cícera sabia do bairro pelo varal. Agora sabe pelo Júnior, que conta tudo.'],
    q_cicera_varal: ['O varal mais curto', 'Dona Cícera lava para a metade da rua que lavava antes. Duas casas vizinhas ficaram vazias.'],
    q_junior_mangueira: ['Júnior na mangueira', 'Júnior subiu na mangueira antes de todo mundo chegar. De lá se vê o telhado da Rita e a fila do portão.'],
    q_junior_casa: ['A casa fechada', 'Júnior entra pela janela de uma casa fechada da esquina. Ficaram uma cadeira, um prato na pia e um calendário na parede.'],
    q_tonho_cocada: ['A cocada de presente', 'A mãe do Tonho fez cinquenta cocadas para o caruru. Hoje ele não vende, só dá.'],
    q_tonho_turista: ['Turista só no fim de semana', 'Tonho vende o dobro no sábado e no domingo, quando chegam os ônibus de turistas. De terça a quinta, quase nada.', true],
    q_nena_tabuleiro: ['O tabuleiro de Dona Nena', 'Dona Nena cuida da oferenda com Dona Zefa. O acarajé dela só sai quando o sol baixa.', true],
    q_davi_cantiga: ['A música do fim de tarde', 'Davi toca baixinho. Dona Zefa pediu cantiga de roda para os meninos.'],
    q_caio_bia: ['Caio e Bia na padaria', 'Caio e Bia ajudam Vó Áurea no balcão, e sempre sobra um pão para eles.'],
    q_bia_massa: ['Bia e a massa', 'Bia aprendeu a sovar com Vó Áurea, sem relógio, só pelo ponto da massa.'],
    // o que se ouve sem perguntar
    q_prazo: ['O prazo do Programa', 'Lúcia disse à Dandara que o prazo da obra vem do papel e não consulta o bairro.', true],
    q_zefa_raimundo: ['Zefa e Raimundo discordam', 'Dona Zefa diz a Seu Raimundo que o Programa vai trazer freguês para todo mundo. Ele responde que freguês é quem mora.', true],
    q_pratos: ['Os pratos das crianças', 'Os pratos das crianças são todos iguais. Ninguém ganha mais que o outro.'],
  };

  // objeto examinado → o que a Lia passa a ter visto (viu_x) e a anotação que ele rende, se houver
  const OBJ = { banner: ['banner', 'q_banner'], F13: ['oferenda', 'q_oferenda'], M01: ['mesa', 'q_mesa'], portao: ['portao', 'q_portao'], F14: ['mangueira', 'q_mangueira'], M09: ['cocada'], M27: ['tabuleiro'] };

  // ---------------------------------------------------------------- assuntos: pessoa → assunto → { label, ask, resp, kp, fases, quando }
  // fases: em quais fases o assunto existe (omitido = todas do caruru). quando: basta uma condição: 'viu_x' (a Lia olhou) ou 'apos:pessoa:assunto' (já perguntou).
  const ALL = ['A', 'B', 'C1', 'C', 'D'], DEPOIS_A = ['B', 'C1', 'C', 'D'], MESA = ['C1', 'C', 'D'], FIM = ['C', 'D'];
  const T = {
    zefa: {
      quiabo: { label: 'O quiabo', fases: ['A', 'B'], ask: 'Dona Zefa, como a senhora corta o quiabo?', resp: 'Fino, e com a faca molhada. Faca seca puxa a baba. O dendê só entra quando o quiabo já soltou o ponto.', kp: 'q_quiabo' },
      pai: { label: 'A bandeira', quando: ['viu_banner'], ask: 'A bandeira é de Cosme e Damião, não é? A senhora faz todo ano?', resp: 'Meu pai fazia. Quando ele parou, o quintal ficou quieto uns anos. Voltei a fazer porque a rua veio me pedir.', kp: 'q_zefa_pai' },
      reforma: { label: 'O Programa', fases: DEPOIS_A, ask: 'Dona Zefa, o que a senhora acha do que está acontecendo na rua?', resp: 'Acho bom, Lia. Vinte anos esse bairro caindo e ninguém olhava. Agora tem calçada nova, tem luz, tem polícia na esquina. Meu quintal nunca recebeu tanta visita.', kp: 'q_zefa_reforma' },
      turista: { label: 'O turista', fases: MESA, quando: ['apos:zefa:reforma'], ask: 'E o comércio da rua, Dona Zefa? Quem vai comprar?', resp: 'O povo de fora. Vem com dinheiro e não regateia. Se a rua tem turista, tem freguês para todo mundo: o barbeiro, a Áurea, o Tonho. Foi o que o governo disse na reunião e eu acredito. Quero vender caruru para eles.', kp: 'q_zefa_turista' },
      dn: { label: 'Os shows nos largos', fases: MESA, quando: ['apos:zefa:reforma'], ask: 'Dona Zefa, o que é esse palco no Terreiro de Jesus?', resp: 'É o Pelourinho Dia & Noite, menina. Saiu logo depois que entregaram as primeiras ruas reformadas. Todo dia tem show de graça, em hora diferente: banda, teatro, dança, mestre de capoeira. Terreiro de Jesus, Largo Pedro Archanjo, Largo Tereza Batista, Largo Quincas Berro D\'Água. Antes a rua era escura depois das seis. Agora tem gente até tarde.', kp: 'q_zefa_dn' },
      casa: { label: 'A casa', fases: FIM, quando: ['apos:zefa:reforma'], ask: 'Dona Zefa, a sua casa também entrou no Programa?', resp: 'Entrou entre as que o Programa conserta e devolve para o dono. Refizeram o telhado e não me cobraram nada. Por isso eu falo bem, e sei que nem todo mundo pode falar igual.', kp: 'q_zefa_casa' },
    },
    aurea: {
      balcao: { label: 'O balcão', fases: DEPOIS_A, ask: 'Vó, e a padaria? Ficou sem ninguém?', resp: 'Ficou. O pão espera um dia. A Zefa me convidou e eu não ia dizer que não. Amanhã eu abro cedo.', kp: 'q_aurea_balcao' },
      freguesia: { label: 'Quem compra', fases: MESA, quando: ['apos:aurea:balcao'], ask: 'Vó, o movimento da padaria mudou?', resp: 'Turista entra, olha o forno, tira foto e leva uma água. O pão de todo dia era de quem mora. Com a casa vazia, eu faço a mesma fornada e sobra.', kp: 'q_aurea_freguesia' },
      papel: { label: 'O papel', fases: FIM, quando: ['apos:aurea:freguesia'], ask: 'A senhora recebeu algum papel do Programa, vó?', resp: 'Veio com a tinta da fachada. É o aluguel novo, num valor de loja para turista. Li três vezes e deixei na gaveta.', kp: 'q_aurea_papel' },
    },
    raimundo: {
      sobrado: { label: 'O sobrado', fases: DEPOIS_A, ask: 'Seu Raimundo, o que é aquele aviso na porta do sobrado?', resp: 'Vistoria. Diz que a casa corre risco e eu tenho prazo para sair. Corre mesmo, porque faz anos que não me deixam mexer no telhado. Me ofereceram indenização e uma casa longe daqui. Eu ainda não assinei.', kp: 'q_raimundo_sobrado' },
      vazias: { label: 'A rua de cima', fases: MESA, quando: ['apos:raimundo:sobrado'], ask: 'A rua de cima está tão fechada. Aonde foi essa gente?', resp: 'Aceitaram o dinheiro e foram para o subúrbio. A família que morava na esquina saiu em março. Vêm aqui de visita de vez em quando, de ônibus, e a visita fica cada vez mais curta.', kp: 'q_raimundo_vazias' },
    },
    dandara: {
      lista: { label: 'A lista', fases: DEPOIS_A, ask: 'Dandara, a lista do Programa saiu?', resp: 'Saiu a lista de quem recebeu aviso. Tem nome de morador, tem nome de dono, e tem casa sem nome nenhum. Sábado eu leio tudo na reunião da associação.', kp: 'q_lista' },
      dn: { label: 'Os shows nos largos', fases: FIM, quando: ['apos:dandara:lista'], ask: 'Dandara, a senhora vai aos shows do Terreiro?', resp: 'Vou, e é bom. O governo contrata o grupo e paga o cachê. A família da esquina saiu em março e não recebeu cachê nenhum. A rua cheia de noite precisa de gente que more nela de dia.', kp: 'q_dandara_dn' },
      comodos: { label: 'Quem ficou fora', fases: FIM, quando: ['apos:dandara:lista'], ask: 'Quem são as casas sem nome?', resp: 'Quem aluga cômodo. Não aparece em papel nenhum, então a indenização não passa por ele. A associação vai de porta em porta conferir, e eu preciso de gente que saiba quem mora onde.', kp: 'q_comodos' },
    },
    lucia: {
      convite: { label: 'O convite', fases: MESA, ask: 'Lúcia, a senhora veio por causa da Dona Zefa?', resp: 'Ela me chamou pessoalmente. Disse que quem mede a rua também come nela. Vim. Sei que muita gente aqui preferia que eu não viesse.', kp: 'q_lucia_convite' },
      ficha: { label: 'O trabalho', fases: FIM, quando: ['apos:lucia:convite'], ask: 'E o que a senhora faz agora na rua?', resp: 'Faço a ficha de cada casa que sai. Quem mora, quantos são, o valor oferecido. Eu assino embaixo e não sei para onde essas pessoas vão.', kp: 'q_lucia_ficha' },
      evento: { label: 'O turista e o comércio', fases: ['D'], quando: ['apos:lucia:ficha'], ask: 'Lúcia, o turista está enchendo a rua como o Programa previa?', resp: 'Enche no fim de semana e em dia de show do Dia & Noite. Na terça a rua esvazia, e a conta do comércio não fecha só com isso. No corredor do órgão já se fala em um evento maior, para trazer gente de Salvador mesmo, que mora na cidade e tem carro. Ainda é conversa. Não está em papel nenhum.', kp: 'q_lucia_evento' },
    },
    rita: {
      telhado: { label: 'O telhado', fases: DEPOIS_A, quando: ['viu_portao'], ask: 'Dona Rita, o seu telhado entrou no Programa?', resp: 'Entrou na lista. Veio a lona e um laudo que diz que o telhado não vale conserto. Eu disse que consertava com meu dinheiro e responderam que não pode mexer.', kp: 'q_rita_telhado' },
      sombra: { label: 'A mangueira', fases: FIM, quando: ['apos:rita:telhado', 'viu_mangueira'], ask: 'A mangueira dá sombra na sua casa?', resp: 'Dá. A árvore é da Zefa e a sombra é minha. Se eu me mudar, a sombra fica sem quem use.', kp: 'q_rita_sombra' },
    },
    nonato: {
      empreita: { label: 'A obra', ask: 'Nonato, a obra que o senhor pegou é a da esquina?', resp: 'É. Empreita do Programa. Levanto parede de casa que a família já deixou. Pagam por semana, e o contrato acaba quando acabar a fachada. Depois eu não sei.', kp: 'q_nonato_empreita' },
    },
    ze: {
      turista: { label: 'A barbearia', ask: 'Seu Zé, a barbearia ainda funciona?', resp: 'Funciona, mas o freguês mudou. Turista entra para tirar foto da cadeira, pergunta se pode sentar sem cortar. Corte mesmo é só dos de sempre, e esses estão saindo da rua.', kp: 'q_ze_turista' },
    },
    bela: {
      panos: { label: 'Os panos', fases: DEPOIS_A, quando: ['viu_toalha', 'viu_mesa'], ask: 'Dona Bela, foi a senhora que costurou os panos dos meninos?', resp: 'Fui. Um pano para cada menino. Quando acaba o caruru cada um leva o seu dobrado debaixo do braço.', kp: 'q_bela_panos' },
      freguesas: { label: 'A costura', fases: FIM, quando: ['apos:bela:panos', 'viu_toalha'], ask: 'Dona Bela, as suas freguesas ainda moram por aqui?', resp: 'As da rua de cima foram embora, uma atrás da outra. Eu entrego de ônibus, e a passagem come o ganho da bainha.', kp: 'q_bela_freguesas' },
    },
    cicera: {
      junior: { label: 'O Júnior', ask: 'Dona Cícera, o Júnior cresceu bastante, não?', resp: 'Cresceu e agora me conta tudo. Antes eu sabia do bairro pelo varal. Hoje sei pelo menino, e ele conta até o que eu não pedi.', kp: 'q_cicera_junior' },
      varal: { label: 'O varal', fases: FIM, quando: ['apos:cicera:junior'], ask: 'O varal da senhora anda mais vazio, Dona Cícera?', resp: 'Lavo para a metade da rua que lavava. A casa da frente fechou, a da esquina também. Pano sem dono eu não lavo.', kp: 'q_cicera_varal' },
    },
    junior: {
      mangueira: { label: 'A mangueira', quando: ['viu_mangueira'], ask: 'Júnior, você subiu na mangueira?', resp: 'Subi cedo, antes de todo mundo chegar. De lá eu vejo o telhado da Rita, a lona e até quem está na fila do portão.', kp: 'q_junior_mangueira' },
      casa: { label: 'A casa fechada', fases: DEPOIS_A, quando: ['apos:junior:mangueira', 'ouviu_cicera'], ask: 'Júnior, a sua avó diz que você entra nas casas fechadas.', resp: 'Entro. Tem uma na esquina com a janela sem tranca. Ficou uma cadeira, um prato na pia e um calendário na parede. Eu vou lá dar pão para o gato.', kp: 'q_junior_casa' },
    },
    tonho: {
      cocada: { label: 'A cocada', fases: DEPOIS_A, quando: ['viu_cocada'], ask: 'Tonho, essa cocada é pra vender?', resp: 'Hoje não. Minha mãe fez cinquenta e mandou trazer. É presente pros meninos. Vender no caruru dá azar.', kp: 'q_tonho_cocada' },
      show: { label: 'Os shows', fases: FIM, quando: ['apos:tonho:turista'], ask: 'Tonho, o show no Terreiro ajuda a vender?', resp: 'Ajuda. Na roda de capoeira eu vendo antes e depois, e a banda da noite é boa de isopor. Só que o grupo acaba e em dez minutos a rua está vazia. Show de graça traz gente que não gasta.', kp: 'q_tonho_show' },
      turista: { label: 'O turista', fases: FIM, quando: ['apos:tonho:cocada'], ask: 'Tonho, e o turista, compra cocada?', resp: 'Compra, e paga mais. Sábado e domingo eu vendo o dobro. De terça a quinta passa um ônibus de manhã e acabou. Se eu vivesse só do turista, comia dois dias.', kp: 'q_tonho_turista' },
    },
    nena: {
      tabuleiro: { label: 'O tabuleiro', fases: MESA, quando: ['viu_oferenda', 'viu_tabuleiro'], ask: 'Dona Nena, o acarajé sai hoje?', resp: 'Sai quando o sol baixar. Agora eu estou com a Zefa na oferenda. Cada coisa tem sua hora, minha filha.', kp: 'q_nena_tabuleiro' },
    },
    davi: {
      cantiga: { label: 'A música', fases: ['D'], ask: 'Seu Davi, o senhor vai tocar?', resp: 'Baixinho, no fim. Dona Zefa pediu cantiga de roda pros meninos, e eu toco o que ela pede.', kp: 'q_davi_cantiga' },
    },
    caio: {
      padaria: { label: 'A padaria', fases: DEPOIS_A, ask: 'Caio, você trabalha na padaria da minha avó?', resp: 'Ajudo. Carrego as forma e varro de tarde. Sempre sobra um pão pra mim e um pra Bia.', kp: 'q_caio_bia' },
    },
    bia: {
      massa: { label: 'A massa', fases: DEPOIS_A, ask: 'Bia, é verdade que a minha avó te ensinou a sovar?', resp: 'Ensinou. Ela não olha relógio. Aperta a massa com o calo do polegar e diz se está no ponto.', kp: 'q_bia_massa' },
    },
  };

  // ---------------------------------------------------------------- ficar ouvindo: pessoa → { fase: [texto, anotação?] }, '*' vale para qualquer fase
  const OUVE = {
    zefa: { D: ['(Dona Zefa diz a Seu Raimundo que o Programa vai trazer freguês para todo mundo. Seu Raimundo responde que freguês é quem mora.)', 'q_zefa_raimundo'], '*': ['(Dona Zefa mexe o panelão devagar e fala baixo, como quem conversa com os santos.)'] },
    aurea: { '*': ['(Vó Áurea ajeita os pães no cesto e conta de cabeça quantos são.)'] },
    raimundo: { D: ['(Seu Raimundo ouve a Zefa falar do Programa. Não responde logo. Quando responde, é sobre freguês.)', 'q_zefa_raimundo'], '*': ['(Seu Raimundo senta, tira o chapéu e olha por cima do muro, na direção do sobrado.)'] },
    dandara: { D: ['(Dandara pergunta a Lúcia se o prazo da obra é o do papel ou o do bairro. Lúcia responde que é o do papel.)', 'q_prazo'], C: ['(Dandara conta assinaturas no caderno, mexendo os lábios.)'], '*': ['(Dandara folheia o caderno procurando um nome.)'] },
    lucia: { D: ['(Lúcia explica à Dandara que o prazo da obra vem do papel. Dandara anota, séria.)', 'q_prazo'], '*': ['(Lúcia olha as fachadas do quintal vizinho e não tira a prancheta do braço.)'] },
    cicera: { '*': ['(Dona Cícera conta à Dona Nena que o neto mexe em tudo. Dona Nena responde que é assim que se aprende.)'] },
    junior: { '*': ['(Júnior sussurra o que viu da mangueira para quem passa perto.)'] },
    nena: { '*': ['(Dona Nena cobre a bacia com o pano e confere a vela da oferenda.)'] },
    m: { C1: ['(Um menino conta os pratos baixinho e confere se o dele é igual ao dos outros.)', 'q_pratos'], '*': ['(O menino está de olho no prato e não ouve mais nada.)'] },
  };
  const OUVE_PADRAO = '(A conversa é baixa e miúda. Dá para ouvir o nome do caruru e o do santo, mais nada.)';

  // ---------------------------------------------------------------- Sim: estado de conversa e anotações
  const P = Sim.prototype;
  P._d = function () {
    if (this.kp) return this;
    this.kp = {}; this.viv = {}; this.feitos = {}; this.novas = []; this.conversa = null;
    try { if (typeof window !== 'undefined' && window.MUNDO_ATIVO && typeof localStorage !== 'undefined') { const s = JSON.parse(localStorage.getItem(KEY) || 'null'); if (s) { this.kp = s.kp || {}; this.viv = s.viv || {}; this.feitos = s.feitos || {}; } } } catch (e) { }
    return this;
  };
  P.salvarKp = function () { try { if (typeof window !== 'undefined' && window.MUNDO_ATIVO && typeof localStorage !== 'undefined') localStorage.setItem(KEY, JSON.stringify({ kp: this.kp, viv: this.viv, feitos: this.feitos })); } catch (e) { } };
  P.ganhar = function (id) {
    this._d(); const k = K[id]; if (!k || this.kp[id] || this.normal) return false;
    this.kp[id] = { id, titulo: k[0], texto: k[1], fase: this.fasen, min: Math.round(this.clock.min) }; this.novas.push(id); this.log.push(['nota', id]); this.salvarKp(); return true;
  };
  P.notas = function () { this._d(); return Object.values(this.kp); };
  P.ver = function (v) { this._d(); if (!this.viv[v]) { this.viv[v] = 1; this.salvarKp(); } };

  // examinar: o que a Lia olha vira vivência e, em alguns casos, anotação
  const ex0 = P.examinar;
  P.examinar = function (k) { ex0.call(this, k); this._d(); const o = OBJ[k]; if (o && !this.normal) { this.ver('viu_' + o[0]); if (o[1]) this.ganhar(o[1]); } };

  // conversa
  const falar0 = P.falar;
  P.falar = function (id) {
    falar0.call(this, id); this._d(); const n = this.npcs[id], L = this.lia, sd = (this.msg && this.msg.txt || '').replace(/^[^:]*: /, '');
    if (n && n.state === 'parado') n.face = Q.dir8(L.x - n.x, L.y - n.y) || n.face;
    this.conversa = { id, modo: 'raiz', linhas: [{ quem: id, texto: sd }] }; this.msg = null; return this.conversa;
  };
  P.fecharConversa = function () { this.conversa = null; };
  P.topicosDe = function (id) {
    this._d(); const t = T[id] || {}, f = this.fasen, out = []; if (this.normal) return out;
    for (const tid in t) {
      const a = t[tid]; if (a.fases && !a.fases.includes(f)) continue;
      if (a.quando && !a.quando.some(c => c.startsWith('apos:') ? this.feitos[c.slice(5)] : this.viv[c])) continue;
      out.push({ id: tid, label: a.label, feito: !!this.feitos[id + ':' + tid] });
    }
    return out;
  };
  P.temAssunto = function (id) { return !!T[id]; };
  P.perguntar = function (id, tid) {
    this._d(); const a = T[id] && T[id][tid]; if (!a) return [];
    this.feitos[id + ':' + tid] = 1; const ganhou = a.kp && this.ganhar(a.kp), out = [{ quem: 'lia', texto: a.ask }, { quem: id, texto: a.resp, rev: !!(a.kp && K[a.kp][2]) }];
    if (ganhou) out.push({ quem: 'nota', texto: 'Anotado: ' + K[a.kp][0] }); else this.salvarKp();
    return out;
  };
  P.ouvir = function (id) {
    this._d(); const o = OUVE[/^m\d$/.test(id) ? 'm' : id] || {}, e = o[this.fasen] || o['*'] || [OUVE_PADRAO], out = [{ quem: 'nota', texto: e[0], nota: true }];
    this.ver('ouviu_' + id); if (e[1] && this.ganhar(e[1])) out.push({ quem: 'nota', texto: 'Anotado: ' + K[e[1]][0] });
    return out;
  };
  // ação do painel: saudar | topicos | voltar | ouvir | perguntar(arg = assunto) | sair
  P.conversaAcao = function (a, arg) {
    const c = this.conversa; if (!c) return null; const id = c.id;
    if (a === 'sair') { this.conversa = null; return null; }
    if (a === 'topicos') c.modo = 'topicos';
    else if (a === 'voltar') c.modo = 'raiz';
    else if (a === 'saudar') { c.linhas = [{ quem: 'lia', texto: 'Oi!' }, c.linhas[0] && c.linhas[0].quem === id ? c.linhas[0] : { quem: id, texto: '…' }]; c.modo = 'raiz'; }
    else if (a === 'ouvir') { c.linhas = this.ouvir(id); c.modo = 'raiz'; }
    else if (a === 'perguntar') { c.linhas = this.perguntar(id, arg); c.modo = 'raiz'; }
    return c;
  };
  P.dicaSemAssunto = 'Você ainda não tem um motivo para puxar esse assunto. Olhe o quintal, escute as conversas e volte.';

  // vivência da toalha (as crianças comendo) e conversa que não segura quem foi embora ou mudou de fase
  const up0 = P.update;
  P.update = function (dt) {
    up0.call(this, dt); this._d(); const L = this.lia, T0 = this.D.TOALHA;
    if (this.fasen === 'C1' && Math.hypot(L.x - T0.cx, L.y - T0.cy) < 5.5) this.ver('viu_toalha');
    if (this.conversa) { const n = this.npcs[this.conversa.id]; if (!n || !n.vis || Math.hypot(L.x - n.x, L.y - n.y) > 2.4) this.conversa = null; }
  };
  const pp0 = P.npcPasso;
  P.npcPasso = function (n, dt) { if (this.conversa && this.conversa.id === n.id) { if (n.state === 'andando') n.anim = 'idle'; return; } return pp0.call(this, n, dt); };

  Q.Dialogo = { K, T, OBJ, OUVE };
  if (typeof module !== 'undefined' && module.exports) module.exports = Q.Dialogo;
})(typeof window !== 'undefined' ? window : globalThis);
