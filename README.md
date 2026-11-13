# O balcão da vó — Pelourinho (protótipo jogável)

Jogo de simulação social em pixel art (HTML/canvas, sem dependências), ambientado no Pelourinho, Salvador.
Câmera lateral na rua e três-quartos nos interiores.

**Jogar:** abra `index.html` (o mundo conectado: rua, padaria, casa de Seu Raimundo e quintal de Dona Zefa, no dia do caruru, 1994).
Setas/WASD andam · E interage (no balcão da padaria, E atende o próximo da fila) · B caderninho · clique anda até o ponto · 1991 são quatro dias sem cronômetro; o quintal só abre em 1994 (em 1991 a casa de Dona Zefa é só apontada, não se entra).

O jogo ocupa 100% da janela mantendo 16:9: resolução lógica 480×270, ampliação inteira por vizinho mais próximo e redução suave final só quando a escala não é inteira (`game/fit.js`).

## Pastas
- `game/` — HTMLs autônomos por etapa (`balcao_etapa7_mundo.html` é o mundo completo), templates e `fit.js` (escalonamento responsivo).
- `quintal/` — jogo do quintal (simulação, render, dados exportados `qdata.json`).
- `mundo/` — shell que liga os quatro ambientes.
- `chars/`, `assets/` — rig 3D → sprites 3/4 (8 direções) e folhas de arte.
- `tools/` — geradores de arte (`quintal_art.py`, pxl), builders (`build_*_html.py`) e testes de dados.
- `tests/` — suítes de simulação.

Reconstruir: `sh tools/build_all.sh`. Ele monta padaria, casa, rua, quintal e o mundo, e grava o resultado em `game/balcao_etapa7_mundo.html` **e em `index.html`**. O `index.html` é o jogável, então depois de mexer em qualquer arquivo de `sim/`, `mundo/`, `quintal/`, `game/*template*` ou `assets/`, rode o build antes de subir.

Tempo: o relógio é diegético e não pune quem explora. 1991 corre a 0,8 min de jogo por segundo e 1994 a 0,5 (`RATE_ANO` no shell); 24 minutos por dia é só referência de teste. O relógio pausa em conversa, caderninho, menus e telas do shell, e anda a 30% quando a Lia fica parada por 12 s. Às 20h ele para (`M.NOITE_FIXA`, `clock.hold`) e o dia não termina sozinho: a Lia pode seguir andando de noite. Dormir é escolha do jogador (porta da escada da padaria ou botão no chip, a partir das 15h). 1994 é uma fase curta em torno do caruru, sem prazo: abre às 11h30 e o jogador a encerra quando as anotações essenciais estão feitas. Os ambientes ligam `semFimDeDia` pelo adaptador de `mundo/mundo.js`.

Dias: o shell conta os dias da fase em `localStorage` (`balcao_dia`). 1991 tem quatro dias (`DIAS_91`); ao dormir no quarto, a rua abre o dia seguinte com saudações próprias (`RD.saudarDia`), conversa de dia (`RD.hoje`, tópico "E hoje?") e as pistas daquele dia (`RD.kpDia`, 20 pistas). Depois do dia 4 vem a tela final com "Seguir para 1994". Acontecimentos (`acontecimentos()` em `sim/s15_rua.js`): dia 3, 9h, técnicos pregam o papel do Programa no quadro e Lúcia passa a marcar as portas a giz; dias 2 e 4, fim da tarde, chuva (Cícera recolhe a roupa, Júnior e a mesa vão para a padaria); dia 4, 18h, reunião da associação (cartaz no poste). Atividades que nascem do dia: ajudar Cícera com a roupa (durante a chuva) e segurar a trena de Lúcia (dia 3 em diante). `tests/acontecimentos.js` cobre tudo isso.

Tarde (12h em diante): em 1991 o elenco volta à rua, a mesa de dominó reabre e Dandara e Lúcia passam na padaria. Seu Raimundo sai de casa de novo às 15h. Em 1994 todos vão ao caruru no quintal e a rua fica vazia depois das 13h. A mesa de dominó volta a encher por volta das 12h30 (Seu Raimundo senta às 13h, quando a casa o libera). A agenda está em `RD.tarde` (`sim/s13_rua_data.js`).

1994 na padaria: às 12h15 a vó deixa o balcão e vai ao caruru. A padaria segue aberta e quem atende é a Lia. No quintal, as falas da Áurea e da Zefa mudam conforme a fase do caruru (`POR_FASE` em `quintal/quintal.js`).

Missão da sacola (1991, uma vez só): Seu Raimundo esquece o pão no balcão, em cima do tampo entre a vitrine e a caixa (a sacola é desenhada lá). Pegar com E marca como pega e a sacola passa a ser desenhada na mão de Lia, na rua e em casa. Entregar a ele no sobrado (E ou clique nele) marca como entregue e encerra a missão. Seu Raimundo só chega em casa por volta das 10h; antes disso o jogo avisa. O estado (`nada → balcao → lia → entregue`) fica em `localStorage` (`balcao_sacola`) e atravessa os dias; depois de entregue nunca mais aparece. Código em `Sim.Sacola` (`sim/s1_core.js`).

Quintal em 1994: conversa igual à da rua (Cumprimentar · Perguntar · Ficar ouvindo). Os assuntos de cada pessoa dependem da fase do caruru e do que a Lia já viu ou ouviu; vários só aparecem depois de examinar um objeto ou de perguntar outra coisa. Dados e regras em `quintal/dialogo.js` (anotações `K`, assuntos `T`, o que se ouve `OUVE`). As anotações do quintal ficam em `balcao_quintal_kp` e contam para a meta de 6 novas.

1994, a mensagem: de 1992 a 1995 o Programa acelera (obra pesada, casa interditada, morador saindo). Em 1991 a rua só recebe a notícia; em 1994 já vive o efeito. A aposta desta etapa é que turistas do Brasil e de fora sustentem sozinhos o comércio local. Quem sente que não basta (Tonho, Áurea, Zé, Bela, Lúcia) deixa a pista de que a fase 2, de 1996, troca a estratégia por eventos culturais que atraiam moradores de Salvador. Dona Zefa fala a favor do Programa: a casa dela foi restaurada e devolvida ao dono.
- Texto: `Sim.Rua.D.virar94()` (`sim/s13_rua_data.js`) troca falas, assuntos, comportas e anotações da rua; `Sim.Social.virar94()` (`sim/s16_social.js`) troca o que circula entre os moradores; `Sim.Data.virar94()` (`sim/s3_data.js`) e `Sim.Casa.virar94()` (`sim/s11_casa_data.js`) fazem o mesmo na padaria e na casa; o quintal tem as falas em `quintal/dialogo.js`. Cada função roda sozinha quando o iframe nasce com `window.MUNDO_ANO === 1994` e é idempotente.
- Cenário: `game/cenario94.js` (fonte 3×5 própria, tudo em canvas, sem tocar nos PNG de 1991). Rua: aviso de vistoria, fita zebrada e X laranja no sobrado de Seu Raimundo, janela tapada com tábua e rachadura, plaquinha BREAD/PÃO ao lado do arco da padaria, faixa AQUI MORA GENTE na associação, casa verde tapada com andaime, tela e placa de obra. Padaria: plaquinha em inglês e aviso de aluguel novo na vidraça. Casa: aviso na parede, caixas sobre o guarda-roupa e mala fechada na cama.
- Objetos novos da rua (examináveis, cada um rende anotação): `aviso_sobrado`, `marca_sobrado`, `placa_padaria`, `faixa_assoc`, `tapume_verde`, `placa_obra` (lista `OBJ94` em `game/rua_template.html`).
- Pelourinho Dia & Noite (1994): nasce logo depois da entrega das primeiras etapas da reforma. Shows de graça todos os dias nos largos (Terreiro de Jesus, Pedro Archanjo, Tereza Batista, Quincas Berro D'Água), com artistas, grupos, teatro, dança e capoeira contratados pelo governo, para manter a rua cheia de dia e de noite e fazer girar bares, restaurantes e lojas de artesanato dos casarões. Aparece na fala de Dandara e de Tonho (rua e quintal), na de Zefa (quintal), no cartaz do quadro de avisos da rua, na pasta da gaveta da padaria e na abertura da fase. A mudança de estratégia para eventos que atraem a classe média de Salvador continua em 1996 e só aparece como conversa de corredor, pela Lúcia.
- Gaveta da padaria: a vó só barra se está presente e perto (antes ela barrava mesmo depois de sair para o caruru). Em 1994 a gaveta rende o aluguel novo e a pasta do Dia & Noite; os objetivos do painel também são os de 1994 (A casa de Seu Raimundo · A aposta do Programa).
- Café com Seu Raimundo: em 1994 não exige intimidade e vale até 15h; em 1991 vale até 14h30 (ele fica em casa de 10h às 15h) e exige um mínimo de confiança.
- Dona Nena (quintal): fala desde a primeira fase, sem depender de examinar o tabuleiro; tópicos tabuleiro, caruru e noite.
- Rua 1991: a pista da lata (`kp_lata`) deixou de travar. A gaiola (como objeto examinável) e a pilha de tijolos e cimento (objeto, pista `kp_obj_obra` e pista `kp_obra_tijolo`) saíram, a pedido; a gaiola segue desenhada na fachada. Nonato mantém a conversa sobre o trabalho dele, sem anotação.
- Jogo novo zera as pistas: abrir `?new=1`, "Recomeçar do início" e a tela final de 1994 apagam tudo o que o jogo guardou (`zerarJogo()` no shell, tudo o que começa com `balcao`). "Recomeçar o dia" e a passagem de 1991 para 1994 continuam guardando.
- Quintal: sumiu a etiqueta pixelada com o nome de quem está perto; o aviso "E Falar com …" já traz o nome em fonte nítida.
- Entrada rápida: a Lia abre 1994 na rua, ao lado do arco da padaria, às 11h30. A padaria, a rua e o sobrado ficam abertos antes do caruru.
- Todo texto de 1994 é proposta; o que toca política, história ou ritual vem marcado `revisar` e passa por leitura cultural e histórica antes de valer como final.

Investigação de 1991 (hoje 26 pistas, eram 29). Em 1991 o relógio andava a 1,5 min de jogo por segundo, então a janela de cada pessoa durava segundos reais, e as comportas escondidas (vivência, confiança) faziam o jogador parar em 12 pistas. O que mudou:
- Ritmo: 0,8 min de jogo por segundo em 1991 e 0,5 em 1994. As pessoas e o horário seguem os mesmos.
- Caminhos alternativos: cada comporta aceita mais de uma origem (ver a cena, ouvir a conversa, ler o quadro de avisos, ouvir de outra pessoa, ter perguntado antes outro assunto, ou um primeiro nível de confiança). Lista em `RD.gates` (`quando`). Cícera ganhou uma segunda janela no varal às 14h30.
- Confiança: sobe só com assunto novo (+0,06; +0,03 se o assunto tinha comporta), por ajudar a mesa de dominó (+0,08) e por conversas relevantes; repetir a pergunta devolve uma fala de repetição (`RD.repete`) e não rende nada. "Ficar ouvindo" rende só nas três primeiras vezes por pessoa.
- Retorno ao jogador: assunto bloqueado mostra um pensamento da Lia (`RD.dicasTopico`), assunto esgotado leva ` ✓`, assunto com resposta ainda não ouvida leva ` · tem mais`, e uma vivência nova vira um aviso curto "Lia · …" (`RD.vivDica`). Nunca aparecem números nem condições.
- Testemunhas: `kp_rua_olhar` (Cícera), `kp_programa` (Raimundo), `kp_associacao` (Bela), `kp_lata` (Zé) podem ser descobertas por outra pessoa, para nenhuma central depender de uma janela só.
- Contadores: o painel da rua, o chip do shell e o caderninho não mostram mais "n de N" em 1991; dizem "a rua ainda tem o que contar" (ou "já te contou o essencial" quando a meta interna de 10 é cumprida). O número aparece só na tela final de 1991. O contador de 1994 ("anotações novas n/6") continua porque é a meta explícita do caruru.
- Diário (B): cada anotação mostra quem disse e a hora ("Ouvido de X · hh:mm") ou onde foi vista, e há as seções "Para entender", "Despertou curiosidade" e "Hipóteses de Lia" (`SIM.diario()`).
- Classificação das 29 (central, complementar, exploratória) e o fio de cada uma ficam em `RD.kpMeta`. Texto político novo vem marcado `revisar`.
- Testes: `node tests/investigacao.js [sementes] [--relatorio]` roda três perfis (explorador livre, conversador, observador) no dia inteiro com a agenda da tarde e confere que quase toda partida entende ao menos 3 dos 4 fios da história, que nenhuma fica abaixo de 2 e que nenhum perfil chega a um assunto sem dica.

1996 (parte jogável, `rua96.html`): o dia da gravação do clipe, sem relógio. Abre pela própria página (`rua96.html`), com os dados em `sim/s96_trama.js` (falas, 20 anotações, 3 missões, 12 ligações) e o elenco em `sim/s96_elenco.js`. Texto proposto, marcado `revisar` onde toca política ou história.
- O que 1996 ensina e 1991/1994 não ensinaram: a rua como imagem (o clipe não é do Programa, mas mostra a rua que ele quer mostrar); a segunda fase do Programa (1996–1999: menos obra pesada, dinheiro de fora, eventos para a classe média de Salvador); quem ficou e quem saiu; o que um dia de evento rende. Não aparece pessoa real nem o ano 2000.
- Missões (qualquer ordem): A encomenda da produção (Dona Áurea → assistente → Dona Áurea), O que a câmera vê (Dandara, monitor da produção, Dona Rita), A rua e os eventos (Dandara e três vizinhos). Com as três feitas, Dona Áurea fecha o dia e aparece a tela final com as ligações.
- Ligação com 1991 e 1994: a página lê as anotações guardadas em `balcao_rua_v1` (rua) e `balcao_quintal_kp` (quintal). Isso abre assuntos (por exemplo, "O Programa agora" com `kp_94_lucia_evento`), acrescenta falas e escreve as "Ligações com 1991 e 1994" no caderno (B). `?mem=tudo` simula quem jogou tudo; `?novo=1` recomeça; `?semintro=1` pula a abertura.
- Controles: E fala ou examina (o morador mais perto, com preferência para quem fala), clique anda até o ponto, B caderninho, 1/2/0 escolhem na conversa. O progresso fica em `balcao_rua96_v1`.
- Reconstruir: `python3 tools/build_rua96_html.py`. Testes: `node tests/rua96_sim.js` e `node tests/rua96_trama.js`.

Testes: `node tests/<suite>.js` com `suite`, `casa_suite`, `rua_suite`, `social_suite`, `mundo_suite`, `quintal_suite`, `lia_atende`, `vizinhanca`, `sacola`, `ano94` e `investigacao`. Todas rodam sem falhas e de forma reprodutível.
