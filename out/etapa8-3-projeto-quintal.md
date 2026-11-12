# Etapa 8.3 — Projeto espacial do quintal do caruru · 1994 (proposta para validação)

Nada foi desenhado nem implementado. Anexos: `quintal_planta.png` (planta de cima) e `quintal_vista34.png` (como o espaço aparece na câmera 3/4 do jogo, com a ordem de sobreposição). São esquemas de projeto, não arte.
Textos novos e tudo que mexe com cultura do axé são **proposta**; `revisar` = precisa de leitura de quem é da cultura.

## 0. Decisões da etapa anterior que entram aqui

- **Aprovado:** Zefa é a anfitriã nova; não criamos Nego e Dinho; Nonato cobre o mutirão e a obra. **Falas e personagens que já existem ficam como estão**: nada foi alterado nas fichas deles.
- **Rita entra em cena** (era só citada). **Caio e Bia entram** (empregados da padaria em 2000; Caio volta como entregador em 2026). O elenco passa de 14 para **17 pessoas em cena, contando a Lia (16 NPCs)**. Fichas curtas na seção 9.
- **Sua mensagem terminou em "e criar também…".** Não sei o que faltava. Não bloqueia esta etapa; me diga e eu incluo.

## 1. Continuidade com o que já existe

| Item | Valor aprovado | No quintal |
|---|---|---|
| Janela do jogo | 480×270 px, ampliação só em múltiplos inteiros | igual; o mundo é mais largo e a câmera segue a Lia (como na rua) |
| Escala | 1 m = 24 px (altura e fachadas); **16 px/m de profundidade no piso** | igual |
| Câmera | Rua: lateral. Padaria e casa: **3/4 oblíqua** (frente + topo, anda em profundidade, oclusão por y) | **3/4**, igual à casa. Justificativa: o quintal tem mesas e circulação em profundidade. Nada de perspectiva nova |
| Personagens | célula 40×52, pés em (20,46); adulto 42 px, Lia 33 px (1991) | Lia 1994 com ~36 px |
| Pé-direito | 4 m = 96 px; porta da padaria 52×66 px | parede da casa 4 m; muro 3 m = 72 px |
| Mesa da casa | 2,5 m × 1 m (60×17 px) | mesa longa 5 m × 1 m, mesma construção |
| Piso | ladrilho 0,5 m = 12×8 px | idem nos trechos de cimento |
| Linha de base | todo objeto e personagem ordenado pelo y dos pés/base | idem |

Reaproveitar **como referência e, quando couber, como arte**: fogão e panela da casa, talha de barro, cesto de pão, mesa e cadeiras da casa (já corrigidas para fechar a mesa), mesa de dominó da rua.

## 2. Descrição arquitetônica

Um quintal de casa baixa de Pelourinho, **atrás da casa de Zefa**, longo e estreito, com um puxadinho de cozinha e uma árvore grande, não um salão de eventos.

- **Formato:** retângulo de **28 m × 8 m de piso** (672 × 128 px), mais faixa de 24 px de muro em cada lado. Mundo: **720 × 270 px**.
- **Fundos, esquerda (0–11 m):** a parede da casa de Zefa, 4 m, reboco ocre-rosado com desgaste localizado (marca de umidade embaixo, reboco caído perto da janela, nada decorativo). Tem:
  - **porta de serviço** 1,2 × 2,3 m (29×55 px), com dois degraus, aberta para a cozinha interna;
  - **janela da cozinha** 1,2 × 1,0 m, em cima da bancada, com venezianas de madeira.
- **Fundos, direita (11–28 m):** **muro de 3 m** (72 px), alvenaria rebocada, com buracos de reparo. **Por cima do muro aparece o telhado da casa de Rita**, com telhas quebradas e uma lona (item interativo).
- **Puxadinho da cozinha:** cobertura de telha sobre barrotes, de 0 a 7,6 m, apoiada em **dois esteios** de madeira (colisão). A cobertura **só é desenhada sobre a parede**, para não esconder o chão e as pessoas (corte 3/4).
- **Lateral direita:** muro com **portão de Rita** (1,1 × 1,8 m), de ferro e madeira, em y = 3,2–4,4 m.
- **Frente (borda inferior):** **soleira / corredor da rua** de 2 m (x = 3,5–5,5 m), mesmo padrão da padaria e da casa. O corredor sai pelo zaguão e dá na rua; não é desenhado, é transição.
- **Piso (três tratamentos):** cimento queimado vermelho sob o puxadinho; **lajeado de pedra irregular** no corredor e na faixa central; **terra batida** sob a mangueira.
- **Vegetação permanente:** **uma mangueira** grande (tronco à direita, copa por cima) e **vasos em latas** (dois na recepção, um na cozinha, um junto ao muro; plantas simples, nada de decoração de salão).
- **Acesso à casa:** só pela porta de serviço. **O interior da casa de Zefa não será construído nesta fase** (item P2).

## 3. Dimensões propostas

| Medida | Metros | Pixels (mundo) |
|---|---|---|
| Piso (largura × profundidade) | 28 × 8 | 672 × 128 |
| Mundo | — | 720 × 270 |
| Piso: x = 24 + 24·x_m ; y = 124 + 16·y_m | x 0→28 m | x 24→696 ; y 124→252 |
| Parede da casa (altura) | 4 | 96 (y 28→124) |
| Muro (altura) | 3 | 72 |
| Faixa frontal (parede baixa / borda) | — | y 252→270 |
| Área útil de circulação (sem móveis) | ≈ 52% do piso | — |
| Câmera | 480 × 270 | mostra ~2/3 do quintal; roda do mouse e botões, como na rua |

Por que 28 m × 8 m: com 16 NPCs + Lia, uma mesa de 10 lugares, dominó, cozinha e árvore, **menos de 6 m de profundidade espreme as passagens** e **menos de 24 m de largura obriga as zonas a se sobrepor**. Alternativa: 480 px de largura (cabe numa tela, sem rolagem), com **zonas coladas e passagem de 0,8 m**; não recomendo.

## 4. Organização funcional

Coordenadas em metros (x, y), y = 0 nos fundos.

| Zona | Local | Dimensão | Objetos | Quem usa | Atividades | Interações da Lia | Restrições |
|---|---|---|---|---|---|---|---|
| **Z1 Cozinha ao ar livre** | x 0–7,6 · y 0–5 | 7,6 × 5 m | trempe + panelão, lenha, fogão a gás, bancada, talha, tanque, 2 bancos, pilão, esteios | Zefa, Cícera, Nena, Lia, Nonato (lenha) | cozinhar, descascar, lavar | mexer o panelão, descascar quiabo, lavar panela, servir água | panelão e fogão: colisão; ninguém atravessa o fogo; faixa de 1 m na frente |
| **Z2 Serviço** | x 9,8–13,2 · y 0–1 | 3,4 × 1 m (+1,3 m de passagem) | aparador com panelas, travessas, cuias, pratos, talheres | Zefa, Cícera, Dandara, Lia | servir, organizar | **servir prato**, entregar a quem pede | passagem de trás (y 1,2–2,5) sempre livre |
| **Oferenda** `revisar` | x 14–15,2 · y 0,2–1,1 | 1,2 × 0,9 m | mesa baixa com toalha branca, pratos cobertos | Zefa, Nena | cuidar, não circular | **só examinar**; não mexe | recuo de **1,5 m** sem móveis; ninguém passa na frente; NPCs não param ali |
| **Z3 Mesa** | x 10,5–17,2 · y 2,6–5,2 | 6,7 × 2,6 m | mesa 5×1 m, 4 cadeiras (fundo), 2 cabeceiras, banco de 3 m (frente) | quase todos na fase C | sentar, comer, conversar | pôr a mesa, sentar, escolher lugar, levar prato | 10 lugares; **banco da frente mostra as costas** de quem senta (máx. 4); cadeiras puxadas 0,6 m |
| **Mesa das crianças** | x 17,8–19,6 · y 5,8–6,6 | 1,8 × 0,8 m | mesinha + 4 banquinhos | Júnior, Caio, Bia | comer, brincar | sentar com eles | altura baixa; sem bloquear a faixa da frente |
| **Z4 Mangueira / convivência** | x 18,5–27,5 · y 1–7,2 | 9 × 6,2 m | tronco, dominó + 4 cadeiras, banco de conversa, cadeira de Rita, meio-fio de pedra | Zé, Raimundo, Nonato, Bela, Rita, Davi, Dandara | dominó, conversa, descanso, música baixa | jogar ou olhar o dominó, sentar com Rita, ouvir | tronco com colisão; copa translúcida quando alguém está sob ela |
| **Telhado de Rita** | fundo, x 21–27,5 | 6,5 m de faixa | telhado visto sobre o muro | — | — | **examinar** (telhas, lona, balde) | sem colisão (fundo) |
| **Portão de Rita** | lateral direita, y 3,2–4,4 | 1,2 m | portão | Rita, Zefa | passar prato, entrar e sair | abrir, levar prato | colisão fechado; aberto passa |
| **Z5 Recepção** | x 0–7,4 · y 5,3–8 | 7,4 × 2,7 m | banco de espera, 2 vasos, lavatório (talha com caneca) | Zefa (recebe), quem chega | cumprimentar, lavar as mãos | falar com quem chega | não bloquear soleira (2 m) |
| **Circulação** | faixa frontal y 6,8–8 (toda a largura); passagem de trás y 1,2–2,5; eixo da porta de serviço x 8–10 | ≥ 1 m | — | todos | andar | — | **nenhum objeto** |

## 5. Dimensionamento e povoamento

- **Lugares sentados:** 10 (mesa) + 4 (crianças) + 4 (dominó) + 3–4 (banco de conversa) + Rita + meio-fio (2) + banco de espera (2) + bancos de cozinha (2) = **~28 lugares para 17 pessoas**. Ninguém precisa ficar em pé por falta de lugar.
- **Pico simultâneo:** fase C, **15 a 16 pessoas** (Lúcia e Davi variam).
- **Densidade:** a área livre (~52%) dá ~6,5 m² por pessoa; nenhuma pessoa a menos de 1 m de outra em circulação normal.
- **Parece cheio, não amontoado:** quatro focos de atividade (cozinha, serviço, mesa, mangueira) e a faixa da frente sempre ocupada por quem anda.

**Posições iniciais (início da fase A, antes de a Lia chegar a pé)**

| Personagem | Posição (x, y m) | Atividade | Circula em |
|---|---|---|---|
| Lia | soleira (4,5 · 7,5) | chega | tudo |
| Zefa | (2,0 · 2,1) | mexe o panelão | Z1, Z2, mesa, recepção |
| Cícera | (2,9 · 3,7) | descasca quiabo no banco | Z1, Z2 |
| Nonato | (10,0 · 5,6) | monta a mesa | mesa, lenha, portão |
| Zé | (21,0 · 2,8) | arruma o dominó | Z4 |
| Júnior | (14,0 · 7,2) | corre na faixa da frente | todo o quintal (menos Z1 e oferenda) |

**Entradas na fase B (escalonadas, 1–2 min de jogo entre uma e outra):** Áurea → Raimundo → Dandara → Bela → Tonho (pela soleira); Caio e Bia (pela soleira, junto de quem os trouxe, P6); **Rita (pelo portão, ajudada por Zefa)**. **Fase C:** Nena (tabuleiro, soleira). **Fase D:** Davi (soleira, convidado a tocar baixo) e Lúcia (soleira, condicional).

Atividades por personagem continuam como na 8.2 (aprovadas); só **Rita, Caio e Bia** são novos (seção 9).

## 6. Inventário

Dimensões em **m (px)**: largura × profundidade × altura. Perspectiva: **3/4** salvo onde indicado. "Col." = colisão; "Int." = interativo; "Est." = estados.

### Arquitetônicos
| Elemento | Qtd | Dimensão | Local | Col. | Int. | Est. |
|---|---|---|---|---|---|---|
| Parede da casa de Zefa | 1 | 11 × 0,3 × 4 (264×96) | fundos x 0–11 | sim (linha) | não | desgaste localizado |
| Muro de fundo | 1 | 17 × 0,3 × 3 (408×72) | fundos x 11–28 | sim | não | — |
| Muros laterais | 2 | faixa 24 px | x = 0 e 28 | sim | não | — |
| Porta de serviço | 1 | 1,2 × 2,3 (29×55) + 2 degraus | x 8,0–9,2 | **não** (NPC atravessa com fade) | sim: "Entrar" → "Ainda não" (P2) | aberta |
| Janela da cozinha | 1 | 1,2 × 1 | x 4,8–6 | — | não | aberta / vapor |
| Portão de Rita | 1 | 1,1 × 1,8 | y 3,2–4,4, lateral | sim (fechado) | sim | **aberto/fechado** |
| Soleira / corredor | 1 | 2 m | x 3,5–5,5, borda inferior | não | transição | — |
| Cobertura do puxadinho | 1 | 7,6 m de faixa | só sobre a parede | não | não | — |
| Esteios | 2 | 0,3 × 0,3 × 2,6 | (2,5 · 4,8), (7,2 · 4,8) | sim | não | — |
| Piso (3 tipos) | — | 672 × 128 | todo | — | — | — |
| **Telhado de Rita (fundo)** | 1 | 6,5 m de faixa | x 21–27,5 | não | **sim: examinar** | **lona / telha nova** (definir na 8.4) |

### Mobiliário
| Elemento | Qtd | Dimensão | Local | Col. | Int. | Est. |
|---|---|---|---|---|---|---|
| Mesa longa | 1 | 5 × 1 × 0,75 (120×16×18) | (11,5 · 3,6) | sim | sim (pôr, examinar) | vazia / posta / servida / suja |
| Cadeira (fundo da mesa, de frente) | 4 | 0,5 × 0,5 × 0,9 | y 2,7 | sim (pé) | assento | puxada / empurrada |
| Cadeira de cabeceira (perfil) | 2 | idem | (10,8 · 3,85), (16,7 · 3,85) | sim | assento | idem |
| Banco comprido (frente da mesa) | 1 | 3 × 0,45 × 0,45 | (12 · 4,7) | sim | assento (4) | — |
| Mesinha das crianças + banquinhos | 1 + 4 | 1,8 × 0,8 × 0,5 | (17,8 · 5,8) | sim | assento (4) | — |
| Mesa de dominó + 4 cadeiras | 1 + 4 | 1,2 × 1,2 | (20 · 3,8) | sim | sim (olhar, jogar) | peças espalhadas / arrumadas |
| Banco de conversa | 1 | 2 × 0,5 × 0,45 | (24 · 4,6) | sim | assento (3) | — |
| Cadeira de Rita (espaldar com almofada) | 1 | 0,6 × 0,6 × 1 | (23,8 · 2,6) | sim | assento reservado | ocupada / vazia |
| Meio-fio de pedra | 1 | 2,5 × 0,4 × 0,35 | (25 · 6,4) | sim | assento (2) | — |
| Banco de espera | 1 | 1,6 × 0,5 | (0,8 · 6,4) | sim | assento (2) | — |
| Aparador de serviço | 1 | 3,4 × 0,9 × 0,9 | (9,8 · 0,1) | sim | sim | travessas cheias / vazias |
| Bancada de preparo | 1 | 2,5 × 0,8 × 0,9 | (4,3 · 0,1) | sim | sim | vazia / com quiabo |
| Bancos baixos de cozinha | 2 | 0,6 × 0,5 × 0,45 | (2,4 · 3), (3,6 · 3,3) | sim | assento | com bacia |
| Mesa baixa da oferenda `revisar` | 1 | 1,2 × 0,9 × 0,7 | (14 · 0,2) | sim | só examinar | posta / coberta |

### Objetos funcionais
| Elemento | Qtd | Dimensão | Local | Col. | Int. | Est. |
|---|---|---|---|---|---|---|
| Trempe de tijolos + panelão de caruru | 1 | 1,3 × 1 × 0,5 | (1,4 · 0,6) | sim | **sim (mexer, provar)** | apagado / fervendo (vapor, 4 quadros) |
| Pilha de lenha | 1 | 0,7 × 2,2 × 0,7 | (0,2 · 0,5) | sim | sim (pegar) | cheia / baixa |
| Fogão a gás 4 bocas + panela | 1 | 0,9 × 0,7 × 0,9 | (3,1 · 0,1) | sim | sim | desligado / ligado |
| Talha de barro com caneca | 1 | 0,6 × 0,6 × 1 | (7 · 0,1) | sim | sim (servir água) | cheia / baixa |
| Tanque com torneira | 1 | 1 × 0,8 × 0,9 | (0,2 · 3,5) | sim | sim (lavar) | pingando / parado |
| Pilão | 1 | 0,5 × 0,5 × 0,5 | (5,4 · 2,7) | sim | sim | — |
| Bacias de quiabo | 2 | 0,5 ø | sobre os bancos | não (apoiadas) | sim (descascar) | cheia / vazia |
| Conjunto de panelas e travessas | 1 | sobre o aparador | z2 | — | sim | cheias / vazias |
| Pilhas de pratos / talheres / cuias | 3 conj. | — | z2 | — | sim | — |
| Jarras d'água / suco | 2 | — | aparador, mesa | — | sim | — |
| Pratos postos na mesa | 10 (decalque) | — | mesa | — | — | postos / usados |
| Toalha da mesa | 1 | cobre a mesa | mesa | — | — | por fase |
| Lavatório (talha com caneca) | 1 | 0,5 × 0,5 × 0,9 | (9,2 · 5,6) | sim | sim (lavar mãos) | — |
| Cesto de pães (Áurea), cocada (Tonho), tabuleiro e tacho (Nena), instrumento (Davi) | 4 | carregados | trazidos por quem chega | — | — | **aparecem quando a pessoa chega** |

### Decorativos
| Elemento | Qtd | Dimensão | Local | Col. | Int. |
|---|---|---|---|---|---|
| **Mangueira** (tronco 0,8 m; copa ø ~7 m, **camada de cima**) | 1 | tronco 19×24 px; sprite ~140×170 | (22,2 · 2,0) | só o tronco | não |
| Vasos em lata | 4 | 0,4 × 0,4 | recepção ×2, cozinha, muro | sim | não |

**Não incluídos de propósito:** varal, bandeirolas, gato, cartazes, enfeites de festa. Cada um só entra se a história pedir (itens opcionais P11).

### Interativos (resumo para a 8.4)
Panelão, bancada/bacias, tanque, talha, aparador, mesa, assentos, dominó, cadeira e portão de Rita, telhado de Rita, oferenda (só ver), porta de serviço, lavatório, mesa de Nena e instrumento de Davi (quando chegam).

## 7. Planta e perspectiva

**Planta:** `quintal_planta.png`. **Vista da câmera:** `quintal_vista34.png`.

**Como o espaço aparece no jogo (3/4):**
- A câmera vê a **frente** das paredes e dos móveis e o **topo** do piso. O quintal é desenhado em **720×270**; a janela de 480×270 acompanha a Lia, com margem de 24 px.
- Quem fica mais **ao fundo (y menor)** é coberto por quem está mais à **frente**.
- Quem senta no **banco da frente da mesa** aparece **de costas**; por isso só quatro lugares ali e as cabeceiras de perfil (mesmo cuidado que a mesa da casa).

**Ordem de camadas (de baixo para cima):**
1. Céu e telhados vizinhos (faixa de 28 px)
2. Parede da casa e muros (frente)
3. Telhado de Rita e cobertura do puxadinho (só sobre a parede)
4. Piso e decalques (lajeado, cimento, terra, tapetes de luz)
5. Sombras no chão (mangueira, esteios): transparentes, nunca bloqueiam
6. **Objetos e personagens, juntos, ordenados pelo y da base/pés** (inclui tronco da mangueira)
7. **Copa da mangueira** (translúcida quando alguém está sob ela)
8. Vapor, fumaça, efeitos
9. Interface, fades de transição

## 8. Regras técnicas

- **Unidades:** pixels do mundo (720×270). x = 24 + 24·x_m ; y = 124 + 16·y_m.
- **Limites de movimento:** x ∈ [32, 688], y ∈ [132, 246] (mesmos 8 px de folga da casa). A soleira abre em x = 192 ± 24 px (mesmo critério da casa).
- **Colisão:** retângulo na **linha de base** de cada objeto (como em `scene_casa.json`: `collide: [x0,y0,x1,y1]`); a mesa colide só na base, não no tampo.
- **Passagens mínimas:** 0,8 m (20 px) na largura, 0,9 m (14 px) na profundidade entre dois retângulos; **1 m** nas faixas de circulação.
- **Zonas de interação:** ponto de parada (`stand`) em frente a cada objeto, a 8–12 px da base, com a pessoa virada para o objeto (como a casa). **Dois pontos de parada por mesa, assento ou bancada longa.**
- **Assentos:** posição de aproximação diferente do ponto sentado, para quem senta nunca atravessar o móvel (como `cad_*` da casa).
- **Posicionamento dos personagens:** pés na linha de base, nunca dentro do retângulo de colisão; sentado só nos pontos previstos.
- **Impedir sobreposição:** teste automático de que nenhum objeto invade as faixas de circulação nem a soleira, nem o recuo da oferenda; teste de 17 NPCs sem atravessar colisão (como os 17 mil pontos da suíte da casa).
- **Compatibilidade com os sistemas atuais:**
  - **Movimentação e NPCs:** mesmo `Nav` (grade + A*), mesma máquina de estados, assentos reservados pela agenda, decisão por utilidade (simulação social já aprovada).
  - **Transição:** nova cena `quintal` (3/4) com porta `rua:porta_zefa` ↔ `quintal:porta`, como `padaria` e `casa`; convidados entram pela soleira, Rita pelo portão, Zefa e quem for à cozinha pela porta de serviço (fade, como a porta da padaria).
  - **Capítulo de 1994:** é um dia separado (como o de 1991), não uma extensão dele; estado salvo como herança para 1996.
- **Carga:** 16 NPCs simultâneos é mais que o dobro da rua (10). Meta: simulação a 60 fps com 16 NPCs; testar antes de povoar.

## 9. Elenco acrescentado nesta etapa (fichas curtas · proposta)

- **Rita (~55)** — vizinha, doente, mora na casa ao lado (a do telhado). Aparência: cabelo preso, vestido simples de estampa miúda, xale leve, anda devagar; usa a cadeira reservada. **Personalidade:** complexa, franca, cansada de esperar. **Posição:** é a **voz que valida o Programa**: diz que "alguém precisa mesmo consertar o meu telhado" e que prefere a obra a esperar a chuva. Não é vilã nem ingênua; sabe que a ajuda vem com preço. Atrito com **Raimundo e Bela**, que veem o Programa como ameaça; **Dandara** a ouve sem concordar; **Lúcia** é a pessoa que ela procura. **Caruru:** chega pelo portão, ajudada por Zefa; senta na sombra; Zefa manda um prato dela primeiro. **Reação a Lia:** pede que ela olhe o telhado dela do quintal. **Autonomia:** conversa com Zefa, observa o dominó, tem conversas curtas com Lúcia. **Visual novo:** sprites lateral e 3/4, sentar na cadeira com almofada, olhar para cima (telhado), receber prato.
- **Caio (14)** — rapaz do bairro; **Bia (13)** — menina do bairro. Mesma turma de Júnior e Lia. **Função:** ajudar a carregar e servir; olham a Lia como a mais velha da turma; em 2000 são contratados para a padaria (Bia no caixa, Caio no café) e em 2026 Caio é entregador. Aparência: roupas simples de uso, Caio de boné, Bia com cabelo preso; sem parentesco definido (P6). **Visual novo:** sprites lateral e 3/4 de cada um; correr, carregar, sentar na mesa das crianças.
- **Lia (1994, 13 anos):** nova versão (mais alta), mesma identidade.

## 10. Referências visuais necessárias

1. Cenário aprovado da casa (para a mesa, o piso, a luz) e a escala gráfica do jogo.
2. A mesa de dominó e as cadeiras da rua (reuso).
3. Fotos de **quintais e puxadinhos de casas de Salvador**, com fogão a lenha, tanque, muro com reparo e telhado de telha (**você escolhe as imagens**; não copiamos nenhuma).
4. Mangueira de rua do Nordeste (porte, copa, sombra).
5. Telhado de telha de barro com lona (para o de Rita).
6. **Revisão cultural** (de quem seja da cultura do axé) para a oferenda, a roupa de Nena e o instrumento de Davi **antes** de qualquer desenho.

## 11. Pendências que dependem de aprovação

| # | Pendência | Recomendação |
|---|---|---|
| P1 | Como a Lia chega: pela rua (1994) até a porta de Zefa, ou o capítulo abre já no corredor do quintal | abrir no corredor; rua de 1994 só se a 8.1 pedir |
| P2 | Interior da casa de Zefa: construir ou só mostrar a porta | não construir agora; "Ainda não" |
| P3 | Oferenda: visível no quintal, ou só dentro de casa e fora da vista | visível, discreta, sem imagens; mas só com revisão cultural |
| P4 | Reusar a arte da casa (fogão, talha, cesto, mesa) com variação de cor | sim |
| P5 | A mangueira é a mesma do "quintal de ninguém" do GDD (1991)? | sim: o quintal de Zefa faz fundo com ele |
| P6 | Caio e Bia: de que família/quem os traz | vêm com Cícera e Nonato (ajudantes) |
| P7 | Rita: idade, doença (só "doente", sem nome), e o estado final do telhado (lona / telha nova) conforme a escolha da Lia | definir na 8.4 |
| P8 | Mutirão do telhado de Rita (GDD cita "mutirão do telhado" em 1991): acontece nesse dia ou é consequência | consequência, visível em 1996 |
| P9 | Mundo de 28 m × 8 m com câmera rolando, ou 480 px sem rolagem | 28 × 8 m |
| P10 | Meta de desempenho: 16 NPCs a 60 fps | testar antes de povoar |
| P11 | Itens opcionais (varal, gato, bandeirolas): entram? | não, por enquanto |
| P12 | O que faltava em "e criar também…" | me diga |
