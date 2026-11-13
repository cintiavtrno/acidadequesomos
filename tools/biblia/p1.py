from lib import *

def tabela(cab, linhas, cls=''):
    h = '<table class="%s"><tr>%s</tr>' % (cls, ''.join('<th>%s</th>' % c for c in cab))
    for l in linhas: h += '<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in l)
    return h + '</table>'

def capa():
    return f'''<section class="cover t-az">
<img src="{IMG}cena94.png" style="position:absolute;left:0;top:0;width:210mm;height:128mm;object-fit:cover;object-position:35% 50%">
<div style="position:absolute;left:16mm;top:146mm"><img src="{IMG}c_titulo2.png" style="width:150mm;height:auto"></div>
<div style="position:absolute;left:16mm;top:206mm;font:800 22pt/1.1 'InterD';color:#f7f0de;letter-spacing:-.01em">Bíblia do jogo</div>
<div style="position:absolute;left:16mm;top:220mm;width:120mm;font:500 10.6pt/1.5 'InterD';color:#dbe6fa">Personagens, fases, pistas e respostas, level design, arte e escrita de um jogo de investigação social no Pelourinho, Salvador, entre 1991 e 1996.</div>
<div style="position:absolute;left:16mm;bottom:16mm;font:700 9pt/1.5 'Inter';color:#f7f0de">Cíntia Vitorino Independent Games<br><span style="color:#cfdcf4;font-weight:400">Protótipo jogável com 1991, 1994 e 1996 · versão 1.1 · novembro de 2026</span></div>
</section>'''

def sumario_html(itens):
    # itens: lista de (nivel, num, titulo, pagina)
    h = '<section class="front t-am" style="page:am"><h1 class="first" style="break-before:auto"><span>Sumário</span></h1><div class="sum"><ul>'
    for nv, n, t, p in itens:
        h += '<li class="l%d"><span class="n">%s</span><span class="t">%s</span><span class="p">%s</span></li>' % (nv, n, esc(t), p)
    return h + '</ul></div></section>'

def nota_leitura():
    return h1('', 'Como ler este documento') .replace('<span class="n"></span>', '') + f'''
<p class="lead">Este documento reúne tudo o que define <i>A cidade que somos</i>: o que o jogo propõe, quem vive nele, o que cada fase ensina, onde está cada pista, como o cenário foi feito e como o texto deve soar.</p>
{ap('Escrevi como se fosse o caderninho da Lia: o que está em letra manuscrita é anotação de quem fez.')}
<p>O jogo existe como protótipo jogável. Tudo o que está descrito aqui foi conferido no código e nos testes do repositório. Quando uma informação ainda não existe no jogo, o texto diz isso de forma direta e marca como pendência.</p>
<p>Há três marcações recorrentes.</p>
<ul>
<li><span class="rev">revisar</span> indica texto que toca política, história ou ritual. Ele vale como proposta até passar por leitura cultural e histórica de quem conhece o bairro e a tradição.</li>
<li>Os quatro símbolos do gabarito, mostrados abaixo, dizem como cada pista chega à Lia. Cada forma tem um significado fixo em todas as fases.</li>
<li>Nomes de arquivo e de módulo aparecem entre aspas simples quando o leitor técnico precisar achá-los no repositório.</li>
</ul>
<div class="leg v">
<span>{SH['q']}<span><b>Conversa.</b> A pista vem de uma pergunta feita a alguém.</span></span>
<span>{SH['t']}<span><b>Escuta.</b> A pista vem de ouvir ou observar pessoas sem perguntar.</span></span>
<span>{SH['c']}<span><b>Objeto ou lugar.</b> A pista vem de examinar algo na cena.</span></span>
<span>{SH['l']}<span><b>Ajuda.</b> A pista vem de fazer algo por alguém.</span></span></div>
<h2>Como o documento está organizado</h2>
<p>Os capítulos 1 a 3 explicam o jogo: o tema, a ficha que responde às perguntas de design e as inspirações. Os capítulos 4 e 5 trazem o MDA e o GDD. O capítulo 6 mostra como a narrativa vira sistema e o capítulo 7 descreve o level design. O capítulo 8 apresenta os personagens. Os capítulos 9 a 11 percorrem as três fases com o gabarito completo das pistas. O capítulo 12 trata dos resultados possíveis. Os capítulos 13 a 16 cobrem a cultura que alimenta a história, a arte, as ferramentas equivalentes e o guia de escrita. O capítulo 17 lista o que falta.</p>
'''

def cap_jogo():
    return h1(1, 'O jogo') + f'''
<p class="lead">A cidade que somos é um jogo de investigação social em pixel art. O jogador é Lia, neta de Dona Áurea, e passa os dias na padaria da família, na calçada e nas casas vizinhas do Pelourinho, em Salvador.</p>
<h2>Premissa</h2>
<p>Em 1991 o rádio anuncia o Programa, um plano de recuperação do Centro Histórico. Gente de fora mede as fachadas, cola avisos no quadro da associação e marca portas a giz. Ninguém na rua sabe direito o que vai mudar.</p>
{ap('Lia tem 10 anos em 1991, 13 em 1994 e 15 em 1996.')}
<p>Lia conversa com os moradores, ajuda quem pede ajuda e anota o que descobre no caderninho. O jogo acompanha a rua em três momentos: quatro dias de 1991, o caruru de Dona Zefa em 1994 e o dia da gravação de um clipe em 1996.</p>
<h2>Tema</h2>
<p>O tema é o que acontece com quem mora num bairro quando o bairro vira projeto. O Programa restaura fachadas, e a pergunta do jogo é quem fica para ver o resultado. A resposta aparece em casas fechadas, freguesia que some, aluguel novo e uma rua pintada que sai bonita na câmera.</p>
<p>Cada morador tem razões próprias. Dona Zefa gosta do Programa, porque a casa dela foi restaurada. Dandara desconfia, porque prometem restaurar tudo e não dizem quem fica. Seu Raimundo guarda uma casa que foi da mãe dele. Tonho precisa de movimento todos os dias. O jogo não escolhe um lado e deixa a Lia, e quem joga, reunir as razões.</p>
<p>Os temas menores sustentam o central: o fiado e a confiança entre vizinhos, a lata que a mesa de dominó mantém para quem aperta, a fé em São Jorge e no Senhor do Bonfim, o caruru de Cosme e Damião e a rua como imagem que o mundo vê.</p>
<h2>Estrutura em três anos</h2>
{tabela(['Fase','O que acontece','Duração e relógio','O que ensina'], [
['1991','O Programa foi anunciado. A rua inteira ouviu no rádio.','Quatro dias. O relógio corre a 0,8 min de jogo por segundo e pausa em conversa e caderninho.','Quem é quem, a confiança entre vizinhos, a medição das casas, o quadro de avisos e a associação.'],
['1994','Três anos depois, obra pesada, casa interditada e gente saindo. Dona Zefa faz um caruru e convida a rua.','Um dia, das 11h30 em diante, sem prazo. O jogador encerra quando as anotações essenciais estão feitas.','O efeito do Programa nas fachadas e nas famílias, a aposta no turista e o Pelourinho Dia & Noite.'],
['1996','A rua fecha para a gravação de um clipe. A segunda fase do Programa muda a estratégia.','Um dia parado, sem relógio, com três missões em qualquer ordem.','A rua como imagem, quem ficou e quem saiu, e o que um dia de evento rende.']])}
<p>O progresso atravessa as fases. A fase de 1996 lê o que a Lia anotou em 1991 e 1994 e usa isso para abrir assuntos e escrever as ligações no caderno.</p>
'''

def cap_ficha():
    return h1(2, 'A ficha do jogo') + f'''
<p class="lead">Este capítulo responde, ponto a ponto, às perguntas de design que orientam o projeto: o tipo de relação entre jogadores e personagens, o que o jogador faz, que experiências o jogo oferece e que sistema ele propõe.</p>
<h2>Relações e regras</h2>
{ap('O jogo é de uma pessoa só. A cooperação e a negociação acontecem com os moradores, que são personagens da simulação.')}
{tabela(['Dimensão','Como aparece no jogo'], [
['Cooperação','Presente e central. Ajudar rende confiança: segurar a trena de Lúcia, sovar a massa com a vó, levar o pão de Seu Raimundo, coar o café, apoiar a mesa de dominó. A confiança abre assuntos que ficam fechados para quem só pergunta.'],
['Competição','Ausente. Não há pontuação, ranking, adversário nem derrota. O relógio não pune quem explora.'],
['Semicooperação','Presente na relação com os moradores. Cada pessoa coopera com Lia segundo o próprio interesse: Dandara quer uma testemunha, Lúcia quer medir sem conflito, Dona Zefa quer plateia para o caruru. Os interesses se cruzam e às vezes se contradizem.'],
['Regras ocultas','Presentes e centrais. As comportas das conversas (<span class="pen">quando</span>) dependem do que a Lia viu, ouviu ou perguntou antes, e da confiança de cada pessoa. O jogador nunca vê números nem condições. Vê apenas pensamentos da Lia que dão pistas de onde procurar.'],
['Negociação','Presente em escala pequena. Pedir a vez na fila da padaria, pressionar a vó sobre a proposta da gaveta, escolher o assunto que a pessoa aceita ouvir naquele momento. Não há troca de recursos.']])}
<h2>O que os jogadores fazem</h2>
{tabela(['Verbo','Situação no jogo'], [
['Explorar','Andar pela rua, entrar na padaria, na casa de Seu Raimundo e no quintal, examinar objetos e olhar quem está fazendo o quê.'],
['Deduzir','Ligar o que foi visto e ouvido: o papel no quadro, a medição, a marca de tinta no sobrado. O caderninho guarda hipóteses e o jogo mostra as ligações ao fim de 1996.'],
['Negociar','Escolher o que perguntar, a quem e quando. Repetir a pergunta não rende nada, e a confiança só cresce com assunto novo.'],
['Resolver problemas','As três missões de 1996: entregar a encomenda, descobrir o que a câmera mostra e o que ela esconde, e reunir a opinião de três vizinhos.'],
['Gerir recursos','Em escala pequena. Os recursos são o tempo do dia, a atenção dos moradores e a confiança. A padaria também tem fila, e a Lia atende quando a vó sai para o caruru em 1994.'],
['Interpretar personagem','O jogador é Lia, neta e atendente de balcão. O que ela pode perguntar, e como pergunta, nasce da idade e do lugar dela na rua.'],
['Construir','Não há construção de mundo. O caderninho é a única coisa que o jogador monta.'],
['Competir','Não.']])}
<h2>Experiências que o jogo propõe</h2>
<p>Usando as oito formas de prazer do MDA, o jogo trabalha cinco delas de forma deliberada. A <b>descoberta</b> vem de achar a pista certa na hora certa. A <b>narrativa</b> aparece quando as peças de uma fase se juntam. O <b>companheirismo</b> nasce das relações com os moradores. A <b>expressão</b> aparece no caderninho e nas hipóteses. A <b>sensação</b> vem do pixel art e da calma da rua.</p>
<p>A <b>fantasia</b> e o <b>passatempo</b> aparecem em escala menor, e o <b>desafio</b> é deliberadamente baixo. O jogo existe para que o jogador preste atenção, e as decisões de design evitam a pressa.</p>
<h2>O sistema que o jogo propõe</h2>
<p>O sistema é de <b>conhecimento condicionado por confiança</b>. Cada morador guarda assuntos. Um assunto abre quando a Lia viu algo relacionado, ouviu de outra pessoa, perguntou antes um assunto vizinho ou atingiu um nível de confiança. A resposta vira uma anotação no caderninho, com quem disse e a que horas.</p>
<p>Em volta desse sistema há uma simulação social: os moradores seguem agendas, sentam à mesa de dominó, saem para a padaria, conversam entre si e comentam o que a Lia fez. A rua continua mesmo quando a Lia fica parada.</p>
<h2>Gênero, acaso, suporte, espaço e finalidade</h2>
{tabela(['Item','Definição'], [
['Gênero','Simulação social com investigação narrativa, no formato do jogo introspectivo e sem pressa. Em pixel art, com câmera lateral na rua e três-quartos nos interiores.'],
['Acaso e informação','Sem dado nem sorteio de resultado. Uma semente varia horários e pequenos gestos dos moradores. A informação é imperfeita para o jogador, que descobre aos poucos, e não há informação escondida de outros jogadores, porque o jogo é individual.'],
['Suporte','Digital. HTML e canvas, sem dependências, em arquivos únicos que abrem no navegador. O jogo foi pensado para teclado e mouse. A versão para toque não foi testada.'],
['Espaço','Uma rua do Pelourinho em corte lateral, a padaria, a casa de Seu Raimundo e o quintal de Dona Zefa. Resolução lógica de 480 por 270 pixels, ampliada em múltiplos inteiros.'],
['Finalidade','Fazer o jogador sentir o que uma política urbana muda no dia a dia de quem mora no lugar. O jogo registra a memória do bairro sem apresentá-la como lição.'],
['Público','A idade-alvo ainda não foi definida. [a definir]']])}
'''

def cap_insp():
    return h1(3, 'Inspirações') + f'''
<p class="lead">Três jogos orientaram decisões diferentes: o ritmo e o espaço pequeno, o ciclo de dias e a vida social visível.</p>
<h2>inKONBINI: One Store. Many Stories</h2>
<p>É um jogo de aventura e simulação da Nagai Industries, que se passa numa loja de conveniência de cidade pequena, inspirada no Japão do começo dos anos 1990. A protagonista é Makoto, estudante que cuida da loja durante o verão. <span class="rev">Fonte: páginas de loja e de imprensa sobre o jogo.</span></p>
{ap('O que peguei: uma loja pequena como centro, o ano fixado no começo dos 1990 e o balcão como lugar de ouvir gente.')}
<p>O jogo mostra que um espaço pequeno e conhecido sustenta muitas histórias, e que organizar a loja e conversar com os fregueses podem ser a mesma atividade. <i>A cidade que somos</i> adota essa ideia na padaria: a Lia atende, escuta a fila e cada freguês deixa uma pista. A diferença é que a investigação sai do balcão e segue para a rua, e a escala é um bairro.</p>
<p>Outra herança é o ritmo. O inKONBINI não cobra eficiência do jogador. Aqui o relógio é diegético, pausa em conversa e no caderninho, e a noite só chega quando a Lia escolhe dormir.</p>
<h2>Dave the Diver</h2>
<p>Lançado em 2023 pela Mintrocket, selo da Nexon, o jogo divide o dia em duas partes: de dia o jogador mergulha no Blue Hole atrás de ingredientes e à noite ajuda a servir num restaurante de sushi. O jogo é em pixel art e combina aventura, gestão e narrativa.</p>
<p>A lição aproveitada é a estrutura de ciclo. Cada dia tem um tempo de explorar e um tempo de voltar para casa, e o que foi coletado fora alimenta o que acontece dentro. Em <i>A cidade que somos</i>, o dia na rua alimenta a noite no quarto acima da padaria, e o caderninho carrega as descobertas para o dia seguinte. Cada dia de 1991 abre com saudações próprias e novos acontecimentos: o papel no quadro no terceiro dia, a chuva no segundo e no quarto, a reunião da associação no quarto dia.</p>
<h2>Habbo Hotel</h2>
<p>Lançado em 2000 pela finlandesa Sulake, o Habbo é um mundo virtual em pixel art isométrico, com avatares, salas públicas e conversa em tempo real. Ele funciona como um lugar onde os outros jogadores estão sempre presentes.</p>
<p>A herança aqui é visual e social. Pessoas pequenas num espaço compartilhado, com cadeiras, mesas e portas que contam quem usa o quê, produzem a sensação de vida mesmo sem texto. A mesa de dominó, a fila da padaria e as sacadas de 1996 vêm dessa ideia. O jogador vê a rua habitada antes de falar com alguém. <i>A cidade que somos</i> é para uma pessoa só, e os outros habitantes são simulados.</p>
<h2>O que o jogo faz por conta própria</h2>
<p>O chão do jogo é uma pesquisa de campo local. A rua, as casas, as comidas, os santos e as conversas partem do Pelourinho. O caruru, o dominó na calçada, a lata do bairro e a mesa posta para um são cenas que o jogo constrói com material do lugar, e nenhuma das três inspirações acima tem equivalente.</p>
'''

def cap_mda():
    return h1(4, 'MDA: mecânicas, dinâmicas e estética') + f'''
<p class="lead">O MDA separa o que o designer constrói, o que acontece quando alguém joga e o que o jogador sente. Este capítulo usa o modelo para mostrar por que cada regra do jogo existe.</p>
<div class="mda">
<div><h3>Mecânicas</h3><ul>
<li>Relógio diegético que pausa em conversa e caderninho e desacelera quando a Lia fica parada por 12 segundos.</li>
<li>Conversa em três verbos: cumprimentar, perguntar e ficar ouvindo.</li>
<li>Assuntos com comportas: ver, ouvir, perguntar antes ou ter confiança.</li>
<li>Confiança por pessoa. Sobe com assunto novo e com ajuda. Repetir não rende.</li>
<li>Caderninho com anotações, curiosidades e hipóteses.</li>
<li>Agenda dos moradores, com horário e variação.</li>
<li>Ajudar: trena, massa, café, pão, roupa na chuva.</li>
<li>Pular: dia seguinte ou fase seguinte, a qualquer momento.</li>
</ul></div>
<div><h3>Dinâmicas</h3><ul>
<li>Observar antes de perguntar, porque ver abre assunto.</li>
<li>Esperar a janela de cada pessoa. Cícera está no varal em dois horários.</li>
<li>Ouvir de um morador o que outro não contaria.</li>
<li>Voltar mais tarde a quem respondeu pouco.</li>
<li>Seguir um fio da história ou deixar a curiosidade escolher.</li>
<li>Ver a mesma rua mudar em 1994 e 1996.</li>
<li>Ligar o que as fases anteriores mostraram.</li>
</ul></div>
<div><h3>Estética</h3><ul>
<li>Descoberta: a pista certa na hora certa.</li>
<li>Narrativa: o Programa visto de baixo.</li>
<li>Companheirismo: confiança dos vizinhos.</li>
<li>Expressão: o caderninho e as hipóteses.</li>
<li>Sensação: pixel art, luz de manhã, chuva no fim da tarde.</li>
<li>Desafio baixo, de propósito.</li>
</ul></div>
</div>
<h2>Do design à experiência</h2>
<p>Um exemplo mostra como as três camadas se encaixam. A mecânica diz que a pergunta sobre o Programa a Seu Raimundo só abre se a Lia viu a medição, ouviu falar do Programa ou já tem confiança de nível 1. A dinâmica resultante é que quem passou pela medição de Lúcia chega a Seu Raimundo com a pergunta pronta, e quem não passou tenta outro caminho. A estética que o jogador sente é a de ter achado o assunto, e a de ter sido aceita por quem não fala de qualquer coisa.</p>
{ap('A regra de ouro das comportas: sempre dois ou mais caminhos. Nenhuma pista central depende de uma janela só.')}
<h2>Decisões que seguem do MDA</h2>
<ul>
<li>Sem punição de tempo. O relógio para às 20h e o dia não termina sozinho.</li>
<li>Sem números na tela em 1991. O painel diz que a rua ainda tem o que contar, e a contagem só aparece na tela final.</li>
<li>Assunto bloqueado mostra um pensamento da Lia, nunca uma condição. Assunto esgotado leva um sinal de conferido, e resposta ainda não ouvida leva "tem mais".</li>
<li>Testemunhas redundantes: quatro pistas centrais podem ser descobertas por mais de uma pessoa.</li>
<li>Cada pista pode ser ignorada. O botão de pular existe para que quem quer seguir adiante possa fazê-lo.</li>
</ul>
'''

def cap_gdd():
    return h1(5, 'GDD: documento de design') + f'''
<p class="lead">Esta é a descrição técnica e funcional do protótipo, no estado em que o repositório está hoje.</p>
<h2>Visão geral</h2>
{tabela(['Item','Valor'], [
['Título','A cidade que somos'],
['Estúdio','Cíntia Vitorino Independent Games'],
['Plataforma','Navegador, em arquivos HTML únicos. Teclado e mouse.'],
['Resolução','480 por 270 pixels lógicos, em proporção 16:9, ampliados em múltiplos inteiros por vizinho mais próximo, com redução suave só quando a escala não é inteira.'],
['Câmera','Lateral e ortográfica na rua. Três-quartos nos interiores e no quintal.'],
['Jogadores','Um.'],
['Linguagem','Português do Brasil.'],
['Repositório','cintiavtrno/acidadequesomos']])}
<h2>Loop principal</h2>
<p>Cada dia de 1991 repete o mesmo ciclo: acordar na padaria, descer, atender ou sair para a rua, conversar e observar, ajudar quem pedir, anotar no caderninho e, quando entardece, subir a escada para dormir. O dia seguinte abre com saudações próprias, conversas "E hoje?" e as pistas que só existem naquele dia. Depois do quarto dia, a tela final oferece seguir para 1994.</p>
<h2>Controles</h2>
{tabela(['Entrada','Ação'], [
['Setas ou WASD','Andar.'],['E','Interagir: falar, examinar, atender o próximo da fila.'],['Clique no chão','Andar até o ponto.'],['B','Abrir o caderninho.'],['1, 2, 0','Escolher na conversa: cumprimentar, perguntar, sair.'],['Esc','Fechar janelas.'],['Botão no alto','Pular para o próximo dia ou fase.']])}
<h2>Sistemas</h2>
<h3>Relógio</h3>
<p>O relógio é diegético. 1991 corre a 0,8 minuto de jogo por segundo e 1994 a 0,5. Ele pausa em conversa, caderninho, menus e telas do shell, e anda a 30% quando a Lia fica parada por 12 segundos. Às 20h ele para. O jogador pode seguir andando de noite, e dormir é escolha dele, pela porta da escada da padaria ou pelo botão do chip a partir das 15h. 1996 não tem relógio.</p>
<h3>Conversa e confiança</h3>
<p>A conversa tem três verbos. Cumprimentar abre a fala do dia. Perguntar mostra os assuntos disponíveis daquela pessoa. Ficar ouvindo rende só nas três primeiras vezes por pessoa. A confiança sobe 0,06 com assunto novo, mais 0,03 se o assunto tinha comporta, e 0,08 por ajudar a mesa de dominó. Repetir a pergunta devolve uma fala de repetição e não muda nada.</p>
<h3>Comportas</h3>
<p>Cada assunto tem uma lista de condições, em que uma basta: ter visto algo (<span class="pen">viu_jogo</span>, <span class="pen">viu_medicao</span>), ter ouvido (<span class="pen">ouviu_programa</span>, <span class="pen">ouviu_reuniao</span>), ter conversado antes (<span class="pen">apos:ze:jogo</span>) ou ter confiança (<span class="pen">nivel:1</span>). O capítulo 9 traduz cada uma em linguagem de jogador no gabarito.</p>
<h3>Caderninho</h3>
<p>O caderninho guarda cada anotação com quem disse e a hora. Tem três seções: Para entender, Despertou curiosidade e Hipóteses de Lia. As anotações de 1991 e do quintal de 1994 ficam gravadas e alimentam 1996.</p>
<h3>Simulação social</h3>
<p>Os moradores têm agenda (<span class="pen">RD.agenda</span>), assentos, andar próprio e conversas entre si. Conversas e ajudas mudam a confiança, e a notícia de uma ajuda circula entre os moradores. Os testes cobrem fila, desistência, uso de objetos, colisão e coerência entre estado e animação.</p>
<h3>Persistência</h3>
<p>O progresso fica no navegador. Chaves: balcao_rua_v1 (rua), balcao_quintal_kp (quintal), balcao_rua96_v1 (1996), balcao_dia, balcao_ano e balcao_base. O parâmetro <span class="pen">?new=1</span> zera tudo. Recomeçar o dia e passar de 1991 para 1994 preservam o que foi guardado.</p>
<h2>Interface</h2>
<div class="pair">{fig('ui_dialogo.png','Padaria: balcão, forno e a lousa do fiado. A interface é discreta e a cena ocupa a tela.')}{fig('f_conversa.png','Conversa em 1996. A fala de Dandara aparece sobre a rua, com as três escolhas embaixo.')}</div>
<h2>Requisitos técnicos</h2>
<p>O jogo é construído em JavaScript puro com canvas e não usa bibliotecas. Os dados e a simulação ficam em módulos sem DOM que rodam em Node, o que permite testar o jogo sem navegador. Rodar tudo: <span class="pen">sh tools/build_all.sh</span>. O resultado é gravado em <span class="pen">game/balcao_etapa7_mundo.html</span> e em <span class="pen">index.html</span>. 1996 monta com <span class="pen">python3 tools/build_rua96_html.py</span> e abre em <span class="pen">rua96.html</span>.</p>
'''
