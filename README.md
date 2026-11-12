# O balcão da vó — Pelourinho (protótipo jogável)

Jogo de simulação social em pixel art (HTML/canvas, sem dependências), ambientado no Pelourinho, Salvador.
Câmera lateral na rua e três-quartos nos interiores.

**Jogar:** abra `index.html` (o mundo conectado: rua, padaria, casa de Seu Raimundo e quintal de Dona Zefa, no dia do caruru, 1994).
Setas/WASD andam · E interage · B caderninho · clique anda até o ponto · no quintal, 1–5 trocam a fase do dia.

O jogo ocupa 100% da janela mantendo 16:9: resolução lógica 480×270, ampliação inteira por vizinho mais próximo e redução suave final só quando a escala não é inteira (`game/fit.js`).

## Pastas
- `game/` — HTMLs autônomos por etapa (`balcao_etapa7_mundo.html` é o mundo completo), templates e `fit.js` (escalonamento responsivo).
- `quintal/` — jogo do quintal (simulação, render, dados exportados `qdata.json`).
- `mundo/` — shell que liga os quatro ambientes.
- `chars/`, `assets/` — rig 3D → sprites 3/4 (8 direções) e folhas de arte.
- `tools/` — geradores de arte (`quintal_art.py`, pxl), builders (`build_*_html.py`) e testes de dados.
- `tests/` — suítes de simulação.

Reconstruir (a partir de `tools/`): `python3 build_html.py && python3 build_casa_html.py && python3 build_rua_html.py && python3 build_quintal_html.py && python3 build_mundo_html.py`.
