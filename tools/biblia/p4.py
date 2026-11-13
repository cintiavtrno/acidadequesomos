from lib import *
from p1 import tabela

def n_rev():
    n = 0
    for k in ('padaria', 'casa', 'rua91', 'rua94', 'quintal', 'k96'):
        n += sum(1 for e in D[k] if e.get('rev'))
    n += sum(1 for l in D['lig96'] if l.get('rev'))
    return n

def cap_cultura():
    return h1(13, 'A cultura que alimenta o jogo') + f'''
<p class="lead">Cada elemento cultural do jogo cumpre dois papéis: dá ambiente à cena e conduz uma parte da história. Este capítulo mostra onde cada um aparece e o que ele faz na narrativa.</p>
<p>Tudo o que toca ritual, política ou história está marcado <span class="rev">revisar</span> e espera leitura de quem conhece a tradição e o bairro. O que está aqui descreve a intenção do jogo. As fontes ficam listadas no fim do capítulo.</p>
<h2>O Pelourinho e o Programa</h2>
<p>O Centro Histórico de Salvador foi tombado pelo Iphan em 1984 e reconhecido pela Unesco como Patrimônio Cultural da Humanidade em 1985. O Pelourinho é o miolo desse conjunto. O nome vem do poste onde se castigavam publicamente pessoas escravizadas, e o largo guarda essa história. <span class="rev">revisar</span></p>
{ap('O Programa do jogo é inspirado no programa real de recuperação do Centro Histórico, iniciado no começo dos anos 1990.')}
<p>A literatura sobre o programa real descreve etapas numeradas, a partir de 1992, que somam obras em quadras e edifícios e a saída de milhares de famílias. A estimativa de uma pesquisadora é de cerca de 1.900 famílias entre 1992 e 1999. O jogo reduz isso a duas fases, de 1992 a 1995 e de 1996 a 1999, e dá nome de personagem ao que as estatísticas mostram. <span class="rev">revisar</span></p>
<p>O recorte do jogo é o de quem mora. Por isso Lúcia mede casa por casa, Dandara guarda a ata da vizinhança e Dona Zefa e Seu Raimundo discordam sobre o Programa. O jogo mostra mais de um lado porque a rua teve mais de um.</p>
<h2>Senhor do Bonfim</h2>
<p>A fita do Senhor do Bonfim é amarrada no pulso com três nós, e cada nó guarda um pedido que se realiza quando a fita arrebenta sozinha. A festa tem a lavagem da colina, no mês de janeiro, e o culto mistura devoção católica e tradição do candomblé, em que o Senhor do Bonfim é associado a Oxalá. <span class="rev">revisar</span></p>
<p>No jogo, o Bonfim aparece em dois lugares. Na padaria, um quadro da colina com fitinhas coloridas, e a Lia anota que cada fitinha é um pedido de alguém da rua. Na casa de Seu Raimundo, uma estampa do Senhor do Bonfim com fitas e vela, num oratório. A fé de Seu Raimundo é privada e a da padaria é coletiva, e as duas dizem que a rua pede coisas junta.</p>
<h2>São Jorge</h2>
<p>O nicho de São Jorge fica na parede da padaria, e a vó acende a vela todo dia de manhã. Ela diz que é São Jorge e que é também o nome que a avó dela não dizia alto, os dois ao mesmo tempo. O jogo deixa o outro nome sem dizer, porque quem escuta é a Lia e a Lia não sabe tudo. A correspondência entre santo católico e orixá muda de uma cidade para outra, e por isso o texto precisa de leitura de quem conhece a tradição de Salvador. <span class="rev">revisar</span></p>
<h2>Cosme e Damião e o caruru</h2>
<p>Na Bahia, o caruru de Cosme e Damião, também chamado caruru de sete meninos, é oferecido em setembro, com festa maior no dia 27. A tradição manda servir uma primeira porção à imagem dos santos, depois a sete crianças, e só então aos adultos. O prato leva quiabo cortado, camarão seco e azeite de dendê. A festa foi reconhecida como patrimônio imaterial da Bahia em 2024. <span class="rev">revisar</span></p>
<p>O quintal de Dona Zefa em 1994 segue esse desenho. A bandeira de Cosme e Damião fica na parede da casa, com um prato servido, uma vela e flores brancas, e a Lia anota que a primeira porção é dos santos. Só Dona Zefa e Dona Nena chegam perto da mesa da oferenda. Às 14h os sete meninos comem na toalha, com a mão. Às 15h os adultos comem na mesa de dez lugares, depois das crianças. O pai de Dona Zefa fazia o caruru todo ano e, quando ele parou, o quintal ficou anos sem festa. Ela voltou a fazer quando a rua pediu.</p>
{fig('cenaq.png','Quintal de Dona Zefa em 1994. A toalha das crianças e a mesa dos adultos organizam a cena.')}
<p>A estrutura do caruru sustenta a fase de 1994. Ela reúne a rua num só lugar, dá a cada pessoa um assento e uma hora, e deixa que as conversas sobre o Programa aconteçam entre os pratos, com a Lia olhando de fora.</p>
<h2>Dominó, lata e fiado</h2>
<p>A mesa de dominó na calçada é o centro social da rua. Seu Raimundo aprendeu com o pai, na mesma calçada, no tempo do lampião a gás, e joga devagar de propósito, porque quem tem pressa joga a pedra errada. Na mesa também se explica a lata do bairro: quem pode põe um trocado, quem aperta tira, sem perguntar.</p>
<p>O fiado da padaria tem o mesmo desenho. A lousa diz "fiado até sexta" e a vó nunca apagou a linha de Seu Raimundo, que tem risco de sexta em sexta e nunca um "devendo". As duas práticas mostram uma economia que não passa por papel e que o levantamento de Lúcia não alcança.</p>
<h2>Comidas e vendedores</h2>
<p>Tonho carrega as cocadas que a mãe faz de madrugada. Dona Nena vende acarajé, que só sai quando o sol baixa. Dona Zefa corta o quiabo fino e molha a faca antes de cada corte, para não babar. Na padaria, o forno de lenha é aceso antes do sol e a massa é sovada sem relógio, pelo ponto. Cada comida tem um lugar na rua e um horário.</p>
<h2>Pelourinho Dia & Noite</h2>
<p>Em 1994 o jogo apresenta o Pelourinho Dia & Noite como o projeto de shows de graça nos largos Terreiro de Jesus, Pedro Archanjo, Tereza Batista e Quincas Berro D'Água, para manter a rua cheia de dia e de noite. Dandara vai aos shows, mas lembra que o governo paga cachê a quem toca no largo e não paga nada a quem morava no casarão ao lado e foi embora. Dona Nena vende mais acarajé agora que há show até tarde, mas o ponto depende do fiscal.</p>
<p><span class="rev">revisar</span> Uma reportagem de 2015 descreve um projeto de mesmo nome como retomada de uma ação executada no governo de Paulo Souto, que governou a Bahia de 1995 a 1999. O jogo o coloca em 1994. A data precisa ser conferida antes de o texto valer como final.</p>
<h2>O clipe de 1996</h2>
<p>A gravação de 1996 parte de um fato do bairro: a gravação de um clipe no Pelourinho em meados dos anos 1990. O jogo conta o evento pela perspectiva de quem mora. A produção ocupa a rua, a polícia fecha as esquinas, e o monitor mostra a parede pintada e deixa de fora o prédio de tijolo de Dona Rita. A gravação não faz parte do Programa e mostra a rua que o Programa quer mostrar. <span class="rev">revisar</span></p>
<p>Duas decisões protegem o jogo. Nenhuma pessoa real aparece, fala ou é nomeada: o cantor é um figurante sem nome e sem fala. O jogo também não cita letras de música nem falas de terceiros.</p>
<h2>Fontes deste capítulo</h2>
<ul class="src">
<li>Brasil de Fato, "Festa do Caruru de Cosme e Damião agora é patrimônio imaterial da Bahia", 27 set. 2024. brasildefato.com.br</li>
<li>A Tarde, "Caruru de São Cosme e Damião se torna patrimônio imaterial da Bahia". atarde.com.br</li>
<li>Bahia Notícias, "Entenda o que leva a tradição do Bonfim a ser uma das mais famosas da Bahia". bahianoticias.com.br</li>
<li>Banda B, "Pesquisador estima prazo de validade da fitinha do Bonfim". bandab.com.br</li>
<li>Fernandes, A. V. C., "Museus do Centro Histórico de Salvador: impactos do Programa de Recuperação da década de 1990". anais do Even3.</li>
<li>ANPUR, "Pelourinho: entre a gentrificação e a coesão social". anais.anpur.org.br</li>
<li>Le Monde Diplomatique Brasil, "A expulsão da população negra do Centro Histórico de Salvador". diplomatique.org.br</li>
<li>Bahia Notícias, "Remodelação do Pelourinho Dia e Noite terá ações na área social", 30 jul. 2015. bahianoticias.com.br</li>
</ul>
'''

def cap_arte():
    return h1(14, 'Arte e técnica') + f'''
<p class="lead">A arte do jogo é pixel art feita por geração controlada: scripts desenham fachadas, objetos e personagens a partir de regras de cor, escala e luz. As escolhas valem para qualquer ferramenta, e o capítulo seguinte lista os programas que chegam aos mesmos resultados.</p>
<h2>Princípios visuais</h2>
<ul>
<li><b>Grade em metros.</b> Um metro vale 24 pixels. As proporções de cada pessoa (pelve, coxa, canela, tronco, braço e cabeça) são definidas em metros no esqueleto, e a Lia tem medidas próprias, de criança.</li>
<li><b>Sem suavização.</b> Todo desenho usa pixels inteiros, sem antialias, e o jogo é ampliado só em múltiplos inteiros por vizinho mais próximo.</li>
<li><b>Rampas de cinco tons com mudança de matiz.</b> As sombras tendem ao azul e ao roxo e as luzes ao amarelo.</li>
<li><b>Duas câmeras.</b> A rua é lateral e ortográfica, e os interiores são três-quartos oblíquos, com 24 pixels por metro na vertical e 16 por metro de profundidade no piso.</li>
<li><b>Uma paleta por material.</b> Pedra, cal, telha, musgo, ferro, tijolo e vidro têm rampas próprias, e cada fachada recebe uma cor de parede e uma de acabamento.</li>
</ul>
{fig('rua_dom.png','Mesa de dominó em 1991, em zoom. Fachada em cal, calçada em pedra e personagens com 40 por 52 pixels de célula.', 'fw')}
<h2>Personagens: do volume 3D ao sprite</h2>
{ap('Cada pessoa tem um jeito de andar: o ciclo de passos de Seu Raimundo dura 1,10 s e o de Júnior 0,56 s.')}
<p>Os personagens nascem de volumes 3D simples, montados por um esqueleto de cinemática direta com IK de dois ossos nos braços e pernas. Um renderizador próprio projeta cada pose com as mesmas câmeras do jogo, e um pós-processamento acrescenta as linhas internas, o rosto e o contorno. O resultado é cortado em células de 40 por 52 pixels, com a âncora dos pés no ponto (20, 46).</p>
<p>Cada folha tem animações de espera, caminhada, virada, fala, interação com objetos baixos e altos e, nos interiores, sentar. A rua usa quatro direções e os interiores oito. A passada está ligada à velocidade do jogo, então ninguém patina. Cada pessoa tem um perfil de caminhada próprio, com duração do ciclo, comprimento do passo, balanço e inclinação.</p>
<div class="pair">{fig('lia_walk.png','Ciclo de caminhada da Lia, de lado.')}{fig('props.png','Folha de objetos da rua: poste, árvore, vasos, cavalete da padaria, bancos e bicicleta.')}</div>
<h2>Cenário: fachadas, ruas e objetos</h2>
<p>As fachadas são geradas por código, com regras de composição: beirais, dois pavimentos, larguras e faixas de calçada e rua. A rua de 1991 usa uma composição aprovada, e a de 1996 a reaproveita com conservação desigual: tinta nova nas fachadas do palco, tijolo aparente no prédio de Dona Rita e uma inclinação mais suave da rua.</p>
<p>A rua é separada em camadas: fundo distante, o mundo, os objetos, os personagens ordenados por profundidade, as sacadas e os elementos da frente, como os fios e o poste. Letreiros e avisos usam fontes pixeladas próprias, de 5 por 7 pixels nos letreiros pintados e de 3 por 5 nos textos pequenos de 1994.</p>
{fig('far.png','Camada de fundo da rua: céu, morros e a torre ao longe.', 'fw')}
<p>Cada objeto da padaria nasce com uma ficha: desenho em três-quartos, classificação, dimensão, ponto de apoio, colisão e interação. Um catálogo em JSON liga a ficha à simulação, e é ele que diz onde alguém pode sentar, o que se examina e onde não se anda. O quintal segue o mesmo fluxo, com base de 720 por 270 pixels, copa da mangueira em camada separada e um catálogo de posições em pixels do mundo.</p>
<div class="pair">{fig('quintal_colisoes.png','Mapa de colisões e interações do quintal, em metros, com pontos de parada, alcance de interação e áreas livres.')}{fig('padaria.png','A padaria montada: base do interior mais objetos, com colisão e pontos de interação já definidos.')}</div>
<h2>Montagem e verificação</h2>
<p>Os scripts de montagem juntam os módulos de simulação, o mapa de cada ambiente e as imagens em base64 num HTML único. Cada fase vira um arquivo que abre no navegador sem servidor. As capturas de tela para conferência saem de scripts de navegador automatizado, e as comparações de antes e depois ficam salvas na pasta do jogo.</p>
<h2>Interface e tipografia</h2>
<p>O caderninho usa uma fonte manuscrita, a mesma que aparece nas anotações deste documento. A interface é discreta: a cena ocupa a tela inteira, com painel de conversa e caderninho que abrem quando necessários. Os textos de interface usam fonte nítida e ficam sobre a cena.</p>
<div class="pair">{fig('f_caderno.png','O caderninho de 1996, com as anotações da Lia, as ligações e as hipóteses.')}{fig('t30_fim96.png','A tela final de 1996, com o resumo e as ligações com 1991 e 1994.')}</div>
'''

def cap_ferr():
    rows = [
     ['Sprites, tiles e objetos em pixel art','Scripts em Python desenham pixel a pixel, com paleta por material e rampas de cinco tons.','Aseprite, Pixelorama, LibreSprite, Piskel, GraphicsGale, Pyxel Edit, Photoshop com lápis de 1 pixel, Krita.'],
     ['Rampas de cor com mudança de matiz','Funções de cor geram a rampa a partir de um matiz, com sombra ao azul e luz ao amarelo.','Aseprite com paleta indexada, Lospec Palette List para partir de rampas prontas, GrafxKid e Pyxel Edit.'],
     ['Personagens a partir de volumes 3D','Esqueleto, volumes e renderizador próprios, com pós-processamento de linhas e rosto.','Blender com câmera ortográfica e resolução baixa, MagicaVoxel, Mixamo para movimentos prontos e Aseprite para limpar os frames.'],
     ['Animações de caminhada e gestos','Clipes escritos por função de pose, com passada ligada à velocidade.','Linha do tempo do Aseprite, Spine ou DragonBones para esqueleto 2D, Blender para 3D.'],
     ['Folhas e atlas de sprites','Montagem em células de 40 por 52 e exportação em JSON.','Exportação do Aseprite, TexturePacker, free-tex-packer, ShoeBox.'],
     ['Fachadas e ruas geradas','Geradores com regras de composição, paleta por material e camadas.','Tiled ou LDtk com tilesets e camadas, Aseprite para os tiles, Wave Function Collapse integrado ao Tiled, Substance Designer para texturas procedurais.'],
     ['Colisão, rotas e pontos nomeados','Mapas em metros, com retângulos de colisão, pontos de parada e rotas.','Camadas de objetos do Tiled ou LDtk, NavigationRegion2D no Godot, NavMesh no Unity.'],
     ['Agenda dos moradores e simulação social','Módulos em JavaScript sem DOM, com agenda, assentos, filas e conversa entre moradores.','Behavior trees no Unity ou no Godot, Behaviac, State Machines, Yarn Spinner para os estados de conversa.'],
     ['Conversa com comportas e anotações','Dados de assuntos com condições (ver, ouvir, perguntar antes, confiança) e anotações com fio e categoria.','Ink com Inky, Yarn Spinner, Twine, articy:draft, Dialogic no Godot. Um grafo no Obsidian ou numa planilha ajuda a planejar as comportas.'],
     ['Fontes pixeladas','Matrizes de 5 por 7 e de 3 por 5 pixels desenhadas em código.','Aseprite, BitFontMaker2, FontForge, Pixel Font Generator.'],
     ['Motor e montagem do jogo','HTML e canvas sem bibliotecas, arquivos únicos com imagens em base64.','Godot 4, Unity, GameMaker, Construct 3, Phaser 3, PixiJS, RPG Maker.'],
     ['Testes de simulação','Suítes em Node com perfis de jogador simulados e sementes.','GUT no Godot, Unity Test Framework, bots de playtest automatizados.'],
     ['Capturas e verificação visual','Navegador automatizado por script.','Playwright, Puppeteer, ScreenToGif, OBS.'],
     ['Controle de versão','Git, com o código e as imagens no mesmo repositório.','Git com GitHub, Git LFS para arquivos grandes, Plastic SCM.'],
     ['Áudio, que ainda não existe no protótipo','Não há áudio.','Audacity, Reaper, LMMS, BFXR ou ChipTone para efeitos, FMOD ou Wwise para integração.'],
     ['Este documento','HTML e CSS convertidos em PDF por navegador.','InDesign, Affinity Publisher, Scribus, Figma ou Canva para a diagramação.']]
    return h1(15, 'Ferramentas: o que o código fez e o que chega ao mesmo resultado') + f'''
<p class="lead">O jogo foi feito com scripts, mas cada resultado visual e de sistema tem programas de mercado que o produzem por outro caminho. A tabela abaixo serve para apresentar o processo a quem trabalha com essas ferramentas.</p>
{tabela(['Resultado','Como foi feito no projeto','Programas que chegam ao mesmo resultado'], rows, 'w')}
<h2>Como combinar as ferramentas</h2>
<p>Um fluxo de mercado equivalente começa no Aseprite, para sprites e tiles, com a paleta indexada de rampas de cinco tons. Os personagens podem sair do Blender, em câmera ortográfica e baixa resolução, e passar pelo Aseprite para o acabamento. As ruas e os interiores se montam no Tiled ou no LDtk, com camadas de fundo, mundo e frente, e uma camada de objetos para colisão, pontos de parada e rotas. As conversas ficam em Ink ou Yarn Spinner, com variáveis para o que a Lia viu, ouviu e perguntou. O Godot 4 reúne tudo, com navegação pelo NavigationAgent2D para a agenda dos moradores e um sistema de salvamento para o caderninho.</p>
<p>O que não muda de um caminho para outro é o desenho do sistema: a grade em metros, a paleta por material, as comportas com mais de uma entrada e a rua que continua mesmo com a Lia parada.</p>
'''

def cap_escrita():
    return h1(16, 'Guia de escrita') + f'''
<p class="lead">O texto do jogo passou por muitas revisões. Este guia reúne o que ficou decidido para que as próximas fases e a próxima pessoa que escreva comecem do estilo certo.</p>
<h2>Princípios</h2>
<ul>
<li><b>Português do Brasil, direto.</b> Frases curtas, verbo no lugar do adjetivo, o concreto antes da opinião.</li>
<li><b>Fala simples.</b> Cada pessoa fala como falaria na rua, sem discurso e sem explicar o que sente.</li>
<li><b>A Lia escuta.</b> As anotações do caderninho têm uma ou duas frases, em voz de menina que presta atenção. Elas dizem o que foi visto ou ouvido e não concluem por ninguém.</li>
<li><b>Sem juízo sobre pessoas.</b> Quando um personagem precisa ser criticado, a fala descreve o fato e deixa o leitor concluir.</li>
<li><b>Objeto primeiro.</b> A descrição de um objeto diz o que se vê, depois, se couber, o que a Lia nota. A frase seguinte não resume o que a primeira disse.</li>
</ul>
<h2>O que evitar</h2>
<p>O texto de IA tem marcas fáceis de reconhecer. O jogo as evita, e a revisão procura por elas.</p>
<ul>
<li>Comparações de negação seguida de afirmação, do tipo "não é X, é Y".</li>
<li>Frase-gancho muito curta, seguida de explicação.</li>
<li>Dois-pontos que introduzem uma máxima.</li>
<li>Frases de fecho em aforismo e paralelismos invertidos.</li>
<li>Listas de três adjetivos ou de três frases com a mesma forma.</li>
<li>Expressões de transição como "e aqui está o ponto", "mais do que isso" e "no fim do dia".</li>
<li>Gerúndio de abertura e a construção "acabam + gerúndio".</li>
<li>Vírgula antes de novo sujeito com "e", quando um ponto resolve.</li>
<li>Frases todas com o mesmo comprimento.</li>
<li>Travessão. O jogo usa vírgula, ponto e dois-pontos.</li>
</ul>
<h2>Exemplos do próprio jogo</h2>
{tabela(['Onde','Texto','Por que funciona'], [
['A lousa do fiado','A lousa diz "fiado até sexta". A vó nunca apagou a linha dele.','Duas frases de tamanhos diferentes. O fato vem primeiro e a relação aparece sem explicação.'],
['A mesa posta para um','A toalha branca, a segunda cadeira puxada. Como se alguém pudesse chegar.','Descreve o que se vê e deixa a leitora concluir.'],
['O quiabo fino','Dona Zefa corta o quiabo fino e molha a faca antes de cada corte, para não babar.','O gesto e o motivo, sem elogio à cozinheira.'],
['O prazo do Programa','Lúcia disse à Dandara que o prazo da obra vem do papel e não consulta o bairro.','Uma crítica sem adjetivo. O fato carrega o peso.']])}
<h2>Política, história e ritual</h2>
<p>Todo texto que toca política, história ou ritual vai marcado <span class="rev">revisar</span> e só vale como final depois de leitura cultural e histórica. O jogo registra hoje <b>{n_rev()}</b> entradas marcadas entre as pistas, e a revisão do texto corrido das conversas fica em aberto.</p>
<h2>Pessoas reais, letras e citações</h2>
<ul>
<li>Nenhuma pessoa real aparece, fala ou é nomeada.</li>
<li>O texto não reproduz letras de música nem trechos de livros e artigos.</li>
</ul>
<h2>Passos de revisão</h2>
<ol>
<li>Ler em voz alta e cortar onde o fôlego acabar.</li>
<li>Procurar as marcas da lista acima.</li>
<li>Conferir se a fala é da pessoa certa, no horário certo e com a confiança certa.</li>
<li>Marcar <span class="rev">revisar</span> onde houver política, história ou ritual.</li>
</ol>
'''

def cap_estado():
    return h1(17, 'Estado do protótipo e pendências') + f'''
<p class="lead">O protótipo abre no navegador e percorre três fases. Este capítulo diz o que existe, o que foi testado e o que está em aberto.</p>
<h2>O que existe</h2>
{tabela(['Parte','Estado'], [
['1991','Jogável: quatro dias, rua, padaria e casa de Seu Raimundo, 78 pistas.'],
['1994','Jogável: rua e quintal em cinco fases do caruru, 69 pistas.'],
['1996','Jogável: dia da gravação, três missões, 20 pistas e 12 ligações.'],
['Botão de pular','Funciona em 1991, 1994 e 1996. O progresso passa para a fase seguinte.'],
['Persistência','No navegador, com chaves por parte do jogo.'],
['Fase seguinte a 1996','Não existe neste protótipo.']])}
<h2>O que foi testado</h2>
<p>O repositório tem suítes de simulação que rodam sem navegador: padaria, casa, rua, social, mundo, quintal, atendimento da Lia, vizinhança, sacola, ano de 1994 e investigação. Os resultados registrados mostram 14 testes passando e nenhum falhando na suíte de simulação da padaria. O teste de investigação de 1991 passa com os perfis simulados, e o de 1996 confirma 20 anotações, 13 falantes e 12 ligações.</p>
<h2>Pendências</h2>
{tabela(['Pendência','Detalhe'], [
['Revisão cultural e histórica',f'{n_rev()} entradas de pista e a maior parte do texto corrido de conversas estão marcadas para leitura de quem conhece o bairro e as tradições.'],
['Data do Pelourinho Dia & Noite','O jogo coloca em 1994. Uma reportagem sugere execução no governo de 1995 a 1999. Conferir e ajustar.'],
['Santo e orixá','A correspondência de São Jorge com um orixá varia por cidade. O texto deixa o nome sem dizer e precisa de leitura.'],
['Etapas do Programa','O jogo usa duas fases. A literatura descreve etapas numeradas. Alinhar o texto à terminologia que o projeto quiser adotar.'],
['Áudio','Não há áudio no protótipo. Música, ambiência e efeitos estão em aberto.'],
['Toque e celular','Pensado para teclado e mouse. A versão para toque não foi testada.'],
['Público-alvo','A faixa etária ainda não foi definida.'],
['Acessibilidade','Contraste, tamanho de fonte e navegação por teclado não foram auditados.'],
['Testes com jogadores','Os perfis são simulados. As leituras do capítulo 12 precisam ser observadas com pessoas.'],
['História completa','Falta a tela final depois de 1996 e a decisão de como o jogo se encerra.'],
['Idade da Lia','A idade em 1996 (15 anos) foi calculada a partir de 1991 e 1994. Conferir.']])}
<h2>Próximos passos sugeridos</h2>
<ol>
<li>Rodar a revisão cultural e histórica nos textos marcados.</li>
<li>Jogar as três fases com algumas pessoas e anotar onde a atenção cai.</li>
<li>Escolher a faixa etária e ajustar o texto a ela.</li>
<li>Decidir como o jogo termina depois de 1996.</li>
<li>Começar o desenho de áudio.</li>
</ol>
<h2>Créditos</h2>
<p>O balcão da vó é um jogo da Cíntia Vitorino Independent Games. Texto, direção, design de jogo e roteiro de Cíntia Vitorino. Programação, arte em pixel art e este documento foram feitos com Claude, da Anthropic. O protótipo e o código-fonte estão em github.com/cintiavtrno/acidadequesomos.</p>
'''
