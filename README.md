# O balcão da vó — Pelourinho (protótipo jogável)

Jogo de simulação social em pixel art (HTML/canvas, sem dependências), ambientado no Pelourinho, Salvador.
Câmera lateral na rua e três-quartos nos interiores.

**Jogar:** abra `index.html` (o mundo conectado: rua, padaria, casa de Seu Raimundo e quintal de Dona Zefa, no dia do caruru, 1994).
Setas/WASD andam · E interage (no balcão da padaria, E atende o próximo da fila) · B caderninho · clique anda até o ponto · 1991 dura 8 min reais (07h→19h); o quintal só vira caruru em 1994.

O jogo ocupa 100% da janela mantendo 16:9: resolução lógica 480×270, ampliação inteira por vizinho mais próximo e redução suave final só quando a escala não é inteira (`game/fit.js`).

## Pastas
- `game/` — HTMLs autônomos por etapa (`balcao_etapa7_mundo.html` é o mundo completo), templates e `fit.js` (escalonamento responsivo).
- `quintal/` — jogo do quintal (simulação, render, dados exportados `qdata.json`).
- `mundo/` — shell que liga os quatro ambientes.
- `chars/`, `assets/` — rig 3D → sprites 3/4 (8 direções) e folhas de arte.
- `tools/` — geradores de arte (`quintal_art.py`, pxl), builders (`build_*_html.py`) e testes de dados.
- `tests/` — suítes de simulação.

Reconstruir: `sh tools/build_all.sh`. Ele monta padaria, casa, rua, quintal e o mundo, e grava o resultado em `game/balcao_etapa7_mundo.html` **e em `index.html`**. O `index.html` é o jogável, então depois de mexer em qualquer arquivo de `sim/`, `mundo/`, `quintal/`, `game/*template*` ou `assets/`, rode o build antes de subir.

Ritmo: 1991 roda a 1,5 min de jogo por segundo (07h→19h em 8 min). 1994 abre às 11h30, roda a 0,5 (o caruru, 12h→18h, dura cerca de 12 min) e o relógio fica parado às 18h enquanto faltarem as 6 anotações: ninguém sai do quintal e o dia não acaba. As taxas estão no shell (`RATE_ANO`); o build só lê `window.MUNDO_RATE`.

Dias: o shell conta os dias da fase em `localStorage` (`balcao_dia`, mostrado no chip e no relógio de cada ambiente). Em 1991, às 19:00 o shell encerra o dia. Com a meta da fase cumprida, o jogo segue para a próxima. Sem ela, "Recomeçar o dia" volta para a manhã e mantém as anotações.

Tarde (12h–19h): em 1991 o elenco volta à rua, a mesa de dominó reabre e Dandara e Lúcia passam na padaria. Seu Raimundo sai de casa de novo às 15h. Em 1994 todos vão ao caruru no quintal e a rua fica vazia depois das 13h. A agenda está em `RD.tarde` (`sim/s13_rua_data.js`).

1994 na padaria: às 12h15 a vó deixa o balcão e vai ao caruru. A padaria segue aberta e quem atende é a Lia. No quintal, as falas da Áurea e da Zefa mudam conforme a fase do caruru (`POR_FASE` em `quintal/quintal.js`).

Missão da sacola (1991, uma vez só): Seu Raimundo esquece o pão no balcão, em cima do tampo entre a vitrine e a caixa (a sacola é desenhada lá). Pegar com E marca como pega; entregar a ele no sobrado marca como entregue e encerra a missão. O estado (`nada → balcao → lia → entregue`) fica em `localStorage` (`balcao_sacola`) e atravessa os dias; depois de entregue nunca mais aparece. Código em `Sim.Sacola` (`sim/s1_core.js`).

Quintal em 1994: conversa igual à da rua (Cumprimentar · Perguntar · Ficar ouvindo). Os assuntos de cada pessoa dependem da fase do caruru e do que a Lia já viu ou ouviu; vários só aparecem depois de examinar um objeto ou de perguntar outra coisa. Dados e regras em `quintal/dialogo.js` (anotações `K`, assuntos `T`, o que se ouve `OUVE`). As anotações do quintal ficam em `balcao_quintal_kp` e contam para a meta de 6 novas.

1994, a mensagem: de 1992 a 1995 o Programa acelera (obra pesada, casa interditada, morador saindo). Em 1991 a rua só recebe a notícia; em 1994 já vive o efeito. A aposta desta etapa é que turistas do Brasil e de fora sustentem sozinhos o comércio local. Quem sente que não basta (Tonho, Áurea, Zé, Bela, Lúcia) deixa a pista de que a fase 2, de 1996, troca a estratégia por eventos culturais que atraiam moradores de Salvador. Dona Zefa fala a favor do Programa: a casa dela foi restaurada e devolvida ao dono.
- Texto: `Sim.Rua.D.virar94()` (`sim/s13_rua_data.js`) troca falas, assuntos, comportas e anotações da rua; `Sim.Social.virar94()` (`sim/s16_social.js`) troca o que circula entre os moradores; `Sim.Data.virar94()` (`sim/s3_data.js`) e `Sim.Casa.virar94()` (`sim/s11_casa_data.js`) fazem o mesmo na padaria e na casa; o quintal tem as falas em `quintal/dialogo.js`. Cada função roda sozinha quando o iframe nasce com `window.MUNDO_ANO === 1994` e é idempotente.
- Cenário: `game/cenario94.js` (fonte 3×5 própria, tudo em canvas, sem tocar nos PNG de 1991). Rua: aviso de vistoria, fita zebrada e X laranja no sobrado de Seu Raimundo, janela tapada com tábua e rachadura, plaquinha BREAD/PÃO ao lado do arco da padaria, faixa AQUI MORA GENTE na associação, casa verde tapada com andaime, tela e placa de obra. Padaria: plaquinha em inglês e aviso de aluguel novo na vidraça. Casa: aviso na parede, caixas sobre o guarda-roupa e mala fechada na cama.
- Objetos novos da rua (examináveis, cada um rende anotação): `aviso_sobrado`, `marca_sobrado`, `placa_padaria`, `faixa_assoc`, `tapume_verde`, `placa_obra` (lista `OBJ94` em `game/rua_template.html`).
- Entrada rápida: a Lia abre 1994 na rua, ao lado do arco da padaria, às 11h30. A padaria, a rua e o sobrado ficam abertos antes do caruru.
- Todo texto de 1994 é proposta; o que toca política, história ou ritual vem marcado `revisar` e passa por leitura cultural e histórica antes de valer como final.

Testes: `node tests/<suite>.js` com `suite`, `casa_suite`, `rua_suite`, `social_suite`, `mundo_suite`, `quintal_suite`, `lia_atende`, `vizinhanca`, `sacola` e `ano94`. Todas rodam sem falhas e de forma reprodutível.
