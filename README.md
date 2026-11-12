# O balcão da vó — Pelourinho (protótipo jogável)

Jogo de simulação social em pixel art (HTML/canvas, sem dependências), ambientado no Pelourinho, Salvador.
Câmera lateral na rua e três-quartos nos interiores.

**Jogar:** abra `index.html` (o mundo conectado: rua, padaria, casa de Seu Raimundo e quintal de Dona Zefa, no dia do caruru, 1994).
Setas/WASD andam · E interage (no balcão da padaria, E atende o próximo da fila) · B caderninho · clique anda até o ponto · 07:00→19:00 em ~4 min; o quintal só vira caruru à tarde (12h–19h).

O jogo ocupa 100% da janela mantendo 16:9: resolução lógica 480×270, ampliação inteira por vizinho mais próximo e redução suave final só quando a escala não é inteira (`game/fit.js`).

## Pastas
- `game/` — HTMLs autônomos por etapa (`balcao_etapa7_mundo.html` é o mundo completo), templates e `fit.js` (escalonamento responsivo).
- `quintal/` — jogo do quintal (simulação, render, dados exportados `qdata.json`).
- `mundo/` — shell que liga os quatro ambientes.
- `chars/`, `assets/` — rig 3D → sprites 3/4 (8 direções) e folhas de arte.
- `tools/` — geradores de arte (`quintal_art.py`, pxl), builders (`build_*_html.py`) e testes de dados.
- `tests/` — suítes de simulação.

Reconstruir: `sh tools/build_all.sh`. Ele monta padaria, casa, rua, quintal e o mundo, e grava o resultado em `game/balcao_etapa7_mundo.html` **e em `index.html`**. O `index.html` é o jogável, então depois de mexer em qualquer arquivo de `sim/`, `mundo/`, `quintal/`, `game/*template*` ou `assets/`, rode o build antes de subir.

Dia: 07:00 às 19:00 em todos os ambientes (a padaria não fecha antes). Às 19:00 o shell encerra o dia. Com a meta da fase cumprida, o jogo segue para a próxima. Sem ela, "Recomeçar o dia" volta para a manhã e mantém as anotações.

Tarde (12h–19h): em 1991 o elenco volta à rua, a mesa de dominó reabre e Dandara e Lúcia passam na padaria. Seu Raimundo sai de casa de novo às 15h. Em 1994 todos vão ao caruru no quintal e a rua fica vazia depois das 13h. A agenda está em `RD.tarde` (`sim/s13_rua_data.js`).
