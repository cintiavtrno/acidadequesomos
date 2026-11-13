from lib import *
from p1 import tabela

def rua_esquema():
    # esquema da rua de 1991 em escala: x de 0 a 1130
    W = 1130.0; k = 150.0 / W  # mm
    pts = [(72, 'prédio 0', 'b'), (164, 'sobrado de Seu Raimundo', 'a'), (240, 'mesa de dominó', 'm'), (470, 'padaria', 'a'), (614, 'porta lateral', 'b'), (718, 'quadro de avisos', 'm'),
           (756, 'associação', 'a'), (846, 'casa verde (Nonato)', 'b'), (990, 'casarão rosa (Cícera)', 'a'), (1078, 'varal e oiti', 'm')]
    s = '<svg width="150mm" height="30mm" viewBox="0 0 150 30" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:1mm 0 1mm 0">'
    s += '<line x1="0" y1="14" x2="150" y2="14" stroke="#2a2638" stroke-width=".35"/>'
    for i, (x, t, kind) in enumerate(pts):
        X = x * k
        if kind == 'a': s += '<rect x="%.2f" y="12.4" width="3.2" height="3.2" fill="#2a2638"/>' % (X - 1.6)
        elif kind == 'm': s += '<circle cx="%.2f" cy="14" r="1.8" fill="#b23a2c"/>' % X
        else: s += '<polygon points="%.2f,12 %.2f,14 %.2f,16 %.2f,14" fill="#2f4c86"/>' % (X, X + 1.8, X, X - 1.8)
        up = (i % 2 == 0)
        y = 8 if up else 23
        s += '<line x1="%.2f" y1="%s" x2="%.2f" y2="%s" stroke="#2a2638" stroke-width=".18"/>' % (X, 9.6 if up else 16.4, X, 12.2 if up else 18.4)
        s += '<text x="%.2f" y="%s" font-family="Caveat" font-weight="700" font-size="3.2" fill="#2f4c86" text-anchor="middle">%s</text>' % (X, 8.4 if up else 22, t)
    s += '<text x="0" y="29" font-family="Inter" font-size="2.3" fill="#5d5046">x = 0</text><text x="150" y="29" font-family="Inter" font-size="2.3" fill="#5d5046" text-anchor="end">x = 1130 px (47 m)</text></svg>'
    return s

def cap_narrativa():
    ex = next(e for e in D['rua91'] if e['id'] == 'kp_ray_sobrado')
    src = D['src91']['kp_ray_sobrado'][0]
    return h1(6, 'Da narrativa ao jogo') + f'''
<p class="lead">A história de <i>O balcão da vó</i> nasceu como tese sobre uma política urbana e virou um conjunto de pistas, pessoas e lugares. Este capítulo mostra os passos dessa conversão.</p>
<h2>A tese e os fios</h2>
<p>A tese é que a recuperação do Centro Histórico mudou quem vive no lugar. Ela é grande demais para caber numa cena, e por isso o jogo a divide em fios, e cada fio é uma pergunta que a rua responde em partes.</p>
{tabela(['Fase','Fios','Pergunta que o fio responde'], [
['1991','Medição · Programa · Associação · Olhares','Quem está medindo, o que é o Programa, quem reage e quem olha a rua de fora.'],
['1994','O sobrado · A aposta no turista · O Dia & Noite · Quem ficou fora','O que o Programa fez em três anos e quem sente isso.'],
['1996','O clipe e a imagem da rua · A segunda fase do Programa · Quem ficou e quem saiu · O que um dia de evento rende','Para quem a rua está sendo feita agora.']])}
{ap('Um fio só vale se uma pessoa da rua tem razão para contá-lo. Sem essa razão, o texto vira cartaz.')}
<h2>Dos fios às pistas</h2>
<p>Cada fio se desfaz em pistas, e cada pista é uma frase curta e concreta que a Lia escreve no caderninho. Em 1991 as 20 pistas da rua têm uma categoria. As <b>centrais</b> contam a história principal. As <b>complementares</b> aprofundam pessoas e hábitos. As <b>exploratórias</b> premiam quem presta atenção a objetos. O gabarito do capítulo 9 traz a categoria de cada pista.</p>
<h2>Um exemplo completo</h2>
<p>A pista <span class="pen">{ex['id']}</span> mostra o caminho inteiro, do texto à regra.</p>
{tabela(['Etapa','Conteúdo'], [
['Pista no caderninho',f"<b>{esc(ex['t'])}.</b> {esc(ex['x'])}"],
['Quem conta','Seu Raimundo, no assunto "O sobrado".'],
['Quando abre','Depois de ter visto a medição, de ter ouvido falar do Programa ou de ter confiança de nível 1. Basta uma das três.'],
['Por que três caminhos','Quem passou pela medição de Lúcia chega com a pergunta pronta. Quem leu o quadro sabe do Programa. Quem ajudou a mesa de dominó já tem confiança.'],
['Fio e categoria','Medição, central.'],
['Se o jogador chegar cedo','Seu Raimundo responde que o assunto tem mais história. A Lia pensa que alguém talvez tenha visto a casa do lado ser medida.']])}
<h2>Da sala de escrita ao navegador</h2>
<ol>
<li><b>Escrever a verdade da cena.</b> O que aconteceu, a quem, em que ordem.</li>
<li><b>Dividir em fios.</b> Cada fio recebe uma pergunta.</li>
<li><b>Quebrar em pistas.</b> Frases de uma ou duas linhas, em voz de Lia.</li>
<li><b>Dar a cada pista dois ou mais caminhos.</b> Ver, ouvir, perguntar antes ou ter confiança.</li>
<li><b>Colocar cada fala numa pessoa e num horário.</b> A agenda do morador decide quando ele está disponível.</li>
<li><b>Desenhar a cena que carrega a pista.</b> O aviso no sobrado, a faixa na associação, o X de tinta.</li>
<li><b>Rodar os perfis simulados.</b> Três perfis de jogador, que não conhecem o gabarito, jogam o dia inteiro e mostram quais pistas ficam raras.</li>
<li><b>Passar por revisão cultural e histórica.</b> Todo texto que toca política, história ou ritual espera por essa leitura.</li>
</ol>
<h2>Como uma fase conversa com a outra</h2>
<p>O jogo guarda o que a Lia anotou em 1991 e 1994. Em 1996 o caderno escreve as ligações, ou seja, frases que só aparecem para quem tem a pista antiga. A matriz completa está no capítulo 11. Três exemplos mostram o princípio.</p>
{tabela(['Se a Lia tem...','E aprende em 1996...','O caderno escreve'], [
['A aposta no turista, de 1994','A segunda fase do Programa',esc(D['lig96'][2]['t'])],
['A marca de tinta e o aviso no sobrado','A porta fechada de Seu Raimundo',esc(D['lig96'][4]['t'])],
['O telhado de lona de Dona Rita','O prédio sem tinta',esc(D['lig96'][8]['t'])]])}
'''

def cap_level():
    return h1(7, 'Level design') + f'''
<p class="lead">O mundo do jogo cabe numa rua curta, em duas casas e num quintal. Esse tamanho foi escolhido para que o jogador reconheça cada pessoa e cada porta no segundo dia.</p>
<h2>Medidas do mundo</h2>
<p>Uma unidade vale 24 pixels e representa um metro. A tela tem 480 por 270 pixels lógicos, então mostra cerca de 20 metros de largura. A rua de 1991 mede 1130 pixels, ou 47 metros. A de 1996 foi ampliada para 1500 pixels, ou 62,5 metros, para caber o palco da gravação.</p>
{ap('A rua tem declive: a linha da parede desce 1 pixel a cada 70 de x. Ninguém percebe, mas a rua parece rua.')}
<p>As camadas desenham de trás para a frente: o fundo distante (<span class="pen">far</span>), o mundo, os objetos, os personagens ordenados por profundidade, as sacadas (<span class="pen">wall</span>) e os elementos da frente. O jogador anda numa faixa navegável de calçada, meio-fio e rua.</p>
<figure class="fw"><img src="{IMG}world91.png" style="width:170mm"><figcaption>A rua de 1991 inteira, com 2260 pixels de largura em ampliação de 2×. A casa amarela à esquerda é o sobrado de Seu Raimundo, a padaria fica no centro e a associação à direita, em azul.</figcaption></figure>
<h2>A rua de 1991, ponto a ponto</h2>
{rua_esquema()}
<p>Os quadrados são portas de moradores e estabelecimentos. Os losangos são portas secundárias. Os círculos são lugares de encontro. A distribuição segue uma ideia: a mesa de dominó, à esquerda e perto do sobrado, é o centro de gravidade da manhã, e o quadro de avisos, mais à direita, faz o papel de jornal da rua.</p>
<h3>Princípios que guiaram a posição das coisas</h3>
<ul>
<li>A pessoa fica onde a pista faz sentido. Cícera lava roupa no varal, Tonho vende junto ao dominó depois das dez, Dandara lê o quadro.</li>
<li>O jogador atravessa a rua de ponta a ponta ao menos uma vez por dia, porque as portas importantes ficam em extremos.</li>
<li>Os pontos de observação (<span class="pen">obs_1</span> a <span class="pen">obs_4</span>) ficam ao lado da mesa. Quem fica ali assiste ao jogo sem entrar nele.</li>
<li>A padaria no meio funciona como casa de recolhimento: quando a chuva chega, Júnior e a mesa de dominó vão para dentro.</li>
</ul>
<h2>Os interiores</h2>
<div class="pair">{fig('m_padaria.png','A padaria. Balcão com vitrine à esquerda, forno de lenha ao fundo, nicho de São Jorge, a lousa do fiado e a porta da escada.')}{fig('m_casa.png','A casa de Seu Raimundo. Mesa posta para um, colcha de retalhos, oratório do Senhor do Bonfim.')}</div>
<p>Os dois interiores usam projeção de três-quartos. Cada objeto da cena que carrega pista é examinável. Na padaria são 13 lugares e 25 pistas de pessoas e hábitos; na casa são 12 objetos e 8 pistas ligadas a Seu Raimundo, todas listadas no gabarito do capítulo 9.</p>
<h2>O quintal de Dona Zefa</h2>
<p>O quintal mede 28 por 8 metros. A casa fica ao fundo à esquerda, a mesa dos adultos ao centro, o portão de Dona Rita à direita e a mangueira no canto direito. A toalha das crianças tem 3 por 3 metros e fica perto do fogão. Uma área restrita perto da cozinha só aceita Dona Zefa e Dona Nena.</p>
<div class="pair">{fig('quintal_planta.png','Planta do quintal, com paredes, mesa, toalha, mangueira e portão.')}{fig('quintal_rotas.png','Rotas dos personagens. As linhas mostram por onde cada um anda nas cinco fases do caruru.')}</div>
<p>O quintal tem cinco fases ao longo da tarde: A, preparo, às 12h; B, chegada, às 13h; C1, as crianças na toalha, às 14h; C, a mesa dos grandes, às 15h; D, depois da mesa, às 16h30. Cada pessoa tem posição e fala própria em cada fase, e as pistas dependem de a Lia estar no lugar certo.</p>
<h2>A rua de 1996</h2>
<p>A rua de 1996 muda para receber a gravação. O palco ocupa a faixa entre x 720 e 1124. Seis percussionistas alternam tocar parado e andar tocando, três câmeras filmam de ângulos diferentes, e barreiras separam o público da equipe. Moradores aparecem nas sacadas e nas portas, atrás do guarda-corpo. O prédio de tijolo aparente, de Dona Rita, fica fora do quadro do monitor.</p>
{fig('cena96.png','A rua de 1996. Equipe de gravação em primeiro plano, plateia atrás das barreiras e moradores nas sacadas.', 'fw')}
<h2>Como o cenário foi planejado</h2>
<ol>
<li>Planta com medidas em metros e pontos nomeados (<span class="pen">spots</span>), para a agenda dos moradores.</li>
<li>Mapa de colisões, que impede atravessar móveis e paredes. O teste de colisão percorre 17 mil amostras e não encontra violação.</li>
<li>Rotas dos personagens, que ligam um ponto ao seguinte.</li>
<li>Arte final por camadas, com as pistas visuais: o aviso, a faixa, o X de tinta.</li>
</ol>
'''

FICHAS = [
 ('lia','Lia','Neta de Dona Áurea · protagonista','Tem 10 anos em 1991, 13 em 1994 e 15 em 1996. Atende no balcão da padaria, anda pela rua, pergunta direto e anota tudo no caderninho. Não julga quem fala. Seu lugar na rua é o de quem escuta sem ter poder sobre nada.','Voz: pergunta curta, curiosa. Nunca faz sermão. Nos pensamentos, explica o que não entendeu.'),
 ('aurea','Dona Áurea','Dona da padaria · avó de Lia','Mantém o forno de lenha aceso antes do sol. Usa avental azul e fica na porta olhando a rua. Trata o fiado como confiança e nunca apagou a linha de Seu Raimundo na lousa. Reza no nicho de São Jorge, que é também outro nome que a avó dela não dizia em voz alta. Em 1994 recebe um aluguel novo, de loja para turista, e deixa o papel na gaveta. Em 1996 fica.','Voz: frases curtas e práticas, sem explicar sentimento. O pão e o forno vêm antes do assunto.'),
 ('raimundo','Seu Raimundo','Vizinho do sobrado amarelo','Joga dominó devagar de propósito. Aprendeu com o pai, na mesma calçada. Paga na sexta, costume da mãe, e guarda a casa dela. Só assina o que sabe ler e mostra para a vó antes. Em 1994 a casa recebe aviso de risco e ele ainda não assinou. Em 1996 olha a rua pela fresta e não desce para o dominó.','Voz: cerimoniosa e lenta. Fala em café antes de perguntar o que a pessoa quer.'),
 ('ze','Seu Zé','Jogador de dominó · aposentado','Chapéu de palha, camisa clara, conta as pedras de cabeça. Tem a barbearia da esquina. É parceiro de Seu Raimundo na mesa. Deixa Lia jogar quando alguém levantar, se ela mostrar que sabe contar. Em 1994 turista entra para fotografar a cadeira, e em 1996 atende gente de Salvador que volta porque tem polícia na esquina.','Voz: bem-humorada, com provocação de mesa.'),
 ('nonato','Nonato','Jogador de dominó · pedreiro de ocasião','Camisa amarela e batida forte da pedra. Gosta de caderno e de papel, ao contrário de Raimundo e Bela. Em 1994 trabalha por empreita nas obras do Programa e levanta a parede de uma casa cujos donos já saíram. Em 1996 o contrato acabou e não veio outro.','Voz: direta e ruidosa. Comemora cada jogada.'),
 ('bela','Dona Bela','Costureira · jogadora de dominó','Pensa muito antes de jogar. Conta as pedras que já saíram. Em 1994 perdeu metade da freguesia, e em 1996 atende cinco casas. Em 1994 costura um pano para cada menino do caruru.','Voz: calma e observadora. Vê tudo da janela.'),
 ('cicera','Dona Cícera','Moradora do casarão rosa · lava roupa para o bairro','Reconhece cada pano pelo cheiro. Joga dominó de costas para a rua e entra na mesa por volta das dez no lugar de Bela. É avó de Júnior. Em 1994 lava para metade da rua que lavava antes. Em 1996 joga no lugar de Seu Raimundo.','Voz: rápida, curiosa, comentarista.'),
 ('junior','Júnior','Menino da rua · neto de Cícera','Corre pela calçada de ponta a ponta. Afaga o gato sem nome. Em 1994 entra pela janela de uma casa fechada e conta o que viu: uma cadeira, um prato na pia, um calendário. Um turista deu uma moeda a ele para sair numa foto. Em 1996 quer ver a câmera de perto.','Voz: curta e animada, com perguntas.'),
 ('tonho','Tonho','Vendedor de cocada e queijadinha','Carrega as cocadas que a mãe faz de madrugada. Vende na sombra do beiral antes das dez e junto ao dominó depois. Em 1994 vende o dobro no fim de semana e quase nada de terça a quinta. No caruru, só dá cocada. Em 1996 vende num dia o que vendia de terça a quinta.','Voz: simpática e comercial. Conta o caixa antes de contar a opinião.'),
 ('dandara','Dandara','Líder da associação de moradores','Guarda a ata num caderno de capa dura e aprendeu a escrever com uma freira. Pede a vez e anota a gentileza. Quer que quem mora continue morando, e isso não está escrito em papel nenhum. Em 1994 faz a lista de quem recebeu aviso. Em 1996 a lista da reunião é menor, porque mora menos gente.','Voz: firme e organizada. Pede que a pessoa volte depois e conte o que viu.'),
 ('lucia','Lúcia','Técnica do Programa de recuperação','Mede portas, janelas e telhados com uma trena e uma prancheta. Escreve o mínimo na coluna de observações. Quer um relatório honesto. Em 1994 faz a ficha de cada casa que sai e assina embaixo sem saber para onde as pessoas vão. Em 1996 não aparece na rua.','Voz: técnica, com cuidado. Evita adjetivo.'),
 ('zefa','Dona Zefa','Dona do quintal · faz o caruru','De touca azul. Corta o quiabo fino molhando a faca antes de cada corte. O pai dela fazia o caruru todo ano, e quando ele parou o quintal ficou anos sem festa. Defende o Programa: a casa dela foi restaurada e devolvida ao dono. Em 1996 gosta da rua nova.','Voz: acolhedora e segura. Reconhece que nem todo mundo teve a mesma sorte.'),
 ('nena','Dona Nena','Vendedora de acarajé · ajuda no caruru','Veste branco. Cuida da vela e do azeite do caruru e, com Dona Zefa, da oferenda. Explica a ordem: as crianças comem primeiro, na toalha, com a mão. O acarajé só sai quando o sol baixa. Em 1994 vende mais com show até tarde, mas o ponto depende do fiscal.','Voz: tranquila, de quem conhece a ordem das coisas.'),
 ('rita','Dona Rita','Moradora do prédio de tijolo aparente','Cabelo branco e blusa lilás. O portão do fundo do quintal dá na casa dela. O laudo de 1994 diz que o telhado não vale conserto. A lona e o balde no canto são o que sobrou. Em 1996 mora no único prédio sem tinta nova daquele trecho.','Voz: seca, sem queixa.'),
 ('davi','Davi','Morador · toca no caruru','Alto, de camisa verde. Toca baixinho e Dona Zefa pediu cantiga de roda para os meninos.','Voz: poucas falas, só de música.'),
 ('caio','Caio','Morador · ajuda na padaria','Camisa branca, mãos no bolso. Ajuda Dona Áurea no balcão com Bia, e sempre sobra um pão para eles.','Voz: curta.'),
 ('bia','Bia','Moradora · aprendiz de Dona Áurea','Blusa rosa. Aprendeu a sovar sem relógio, pelo ponto da massa.','Voz: curta, animada com a massa.'),
]

def ficha_html(f):
    sid, nome, papel, texto, voz = f
    return f'<div class="fp"><div class="sp"><img src="{IMG}sp_{sid}.png"></div><div><h3>{esc(nome)}</h3><div class="pap">{esc(papel)}</div><p>{texto}</p><p class="soft"><b>{voz}</b></p></div></div>'

def cap_personagens():
    h = h1(8, 'Personagens') + f'''
<p class="lead">O elenco tem 17 pessoas com nome e fala e um grupo de figurantes de 1996. As fichas abaixo resumem quem cada um é, o que muda de fase em fase e como fala.</p>
<p>Cada pessoa tem agenda própria, assento e ritmo de caminhada. Os sprites vêm de um boneco 3D que é renderizado em oito direções. As cores usadas nas legendas de conversa também são do elenco.</p>
{fig('elenco_idle.png','O elenco principal, em posição de espera. Da esquerda para a direita: Lia, Dona Áurea, Seu Raimundo, Seu Zé, Nonato, Dona Bela, Dona Cícera, Júnior, Tonho, Dandara e Lúcia.', 'fw')}
'''
    for f in FICHAS: h += ficha_html(f)
    h += '''<h2>A equipe de gravação de 1996</h2>
<p>A equipe não tem nome. As descrições aparecem como observações quando o jogador examina cada figura.</p>'''
    prod = [('diretor','Diretor','Colete de bolsos e chapéu de pescador. Olha a rua inteira antes de olhar o monitor.'),
            ('assist','Assistentes de produção','Prancheta e rádio. Anotam o horário de cada tomada. Chamam a equipe de som. A assistente recebe a cesta de pão de Dona Áurea.'),
            ('perc1','Percussionistas','Seis, em duas fileiras. Alternam tocar parados e andar tocando. Um deles marca o tempo com a cabeça.'),
            ('cam1','Operadores de câmera','Três câmeras: duas fixas e uma de ombro que acompanha os tambores.'),
            ('cantor','O cantor','Camiseta branca com um símbolo da paz. Dança pouco e olha para as sacadas. É um figurante sem nome e sem fala. O jogo não nomeia nem mostra nenhuma pessoa real.')]
    for sid, nome, t in prod:
        h += f'<div class="fp"><div class="sp"><img src="{IMG}sp_{sid}.png"></div><div><h3>{nome}</h3><p>{t}</p></div></div>'
    return h
