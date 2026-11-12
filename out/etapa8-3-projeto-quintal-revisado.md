# Etapa 8.3 (revisada) — Projeto espacial do Quintal do Caruru (1994)

**Status: proposta de documentação. Nada foi implementado e nenhum sprite de cenário foi produzido.**
Fonte única dos números: `tools/quintal_data.py` (metros). Verificação: `tools/teste_quintal.py` — **33 de 33 checagens passam**. Imagens geradas por `tools/gerar_quintal.py` a partir dos mesmos dados; planta e vista 3/4 mostram o mesmo ambiente, com os mesmos IDs e posições. Itens marcados `revisar` precisam de olhar de quem conhece a cultura de axé.

## 0. O que foi corrigido em relação à primeira versão

| # | Problema encontrado | Correção |
|---|---|---|
| 1 | Planta a 26 px/m e vista 3/4 salva em 2× mas declarada 720×270; medidas misturavam metros e pixels projetados | Um só sistema em metros (seção 1). Planta a 30 px/m; vista 3/4 gravada em 720×270 (1×) e 1440×540 (2×, mesmo mundo) |
| 2 | Telhado do puxadinho desenhado como faixa sobre a parede (errado sob a projeção) | Telhado em **corte**: só a viga do beiral frontal e a junção com a parede; a telha não cobre o chão (seção 5) |
| 3 | Copa da mangueira sobrepunha o telhado de Rita | Muro de divisa de 3 m → **2,4 m**; telhado de Rita fica visível e o dano fica fora da silhueta da copa |
| 4 | Faixa da frente com folga mínima insuficiente | Faixa da frente começa em Y = 6,9 m; **folga mínima 1,10 m** (banco de espera em X ≈ 0,9) |
| 5 | Crianças coladas (0,50 m) e Júnior dentro da mesa | Banquinhos reespaçados a 0,6 m; mesinha das crianças em (17,6; 5,7); Júnior reposicionado |
| 6 | Talha inalcançável por causa do vaso; pontos de interação a mais de 0,9 m do objeto | Vaso D03 movido; pontos de M01 e M14 reajustados |
| 7 | Pessoas sentadas escondidas na vista 3/4 | Ordenação pela borda frontal do móvel (+0,01 m); pés a Z = 0,35 m |

## 1. Sistema de coordenadas e escalas

**Mundo em metros.** X para a direita (0–28), Y de profundidade a partir do muro dos fundos (0–8), Z para cima. Origem = canto de trás à esquerda do piso. Piso: **28 × 8 m (224 m²)**; paredes de 0,3 m ficam fora do piso.

**Projeção 3/4 (mesma da casa e da padaria, oblíqua sem cisalhamento em X):**
- `sx = 24 + 24·X`
- `sy = 124 + 16·Y − 24·Z`

Ou seja: 24 px por metro em X e em Z, **16 px por metro em Y** (a profundidade é comprimida em 2/3). O mundo do quintal tem **720 × 270 px**: piso de 672 × 128 px (y 124→252), mais 24 px de margem de cada lado e faixa inferior de 18 px.

**Unidades de jogo (colisão/navegação):** pixels do chão, `pg = (24 + 24·X, 124 + 16·Y)` (Z = 0), no mesmo formato `collide:[x0,y0,x1,y1]` de `scene_casa.json`. Nunca somar altura (Z) a uma caixa de colisão.

**Planta superior:** vista de topo verdadeira, **30 px/m nos dois eixos** (940 × 402 px, com margens e legenda). Por isso a planta *parece* mais "alta" que a vista 3/4: ela não comprime Y. Para comparar, converta sempre via metros, não via pixels.

**Escala humana:** adulto 1,75 m = 42 px de altura; célula do sprite 40 × 52 px com pés em (20, 46); Lia em 1994 ≈ 1,50 m ≈ 36 px. Alturas e raios de cada personagem estão em `quintal_data.CH`.

**Verificação de tamanhos reais das imagens** (lidos com PIL): planta/colisões/rotas 940 × 402; ocupação 760 × 1080; vista 3/4 720 × 270 (1×) e 1440 × 540 (2×, idêntica em conteúdo); vista anotada 1440 × 540. O teste confere `mundo_px = (720, 270)` e a projeção de cada objeto.

### Camadas de render (de trás para a frente)
1. Céu e telhados vizinhos → 2. Paredes (casa 4 m, muro 2,4 m) → 3. Telhado de Rita e elementos do puxadinho (parede) → 4. Piso + decalques (cimento sob o puxadinho, sombras) → 5. Objetos e personagens ordenados pelo y da base (sentados: logo depois da borda frontal do móvel) → 6. Copa da mangueira (translúcida só onde cobre cabeças) → 7. Vapor/efeitos → 8. UI e fades.

## 2. Teste de ocupação com o elenco em escala real

Elenco em cena: **17 pessoas incluindo Lia** (16 NPCs): Zefa (anfitriã), Áurea, Raimundo, Dandara, Zé, Nonato, Bela, Cícera, Júnior, Tonho, Nena, Davi, Lúcia (condicional), Rita, Caio, Bia. Nenhum personagem foi redimensionado.

Área de piso 224 m²; ocupada por objetos 29,8 m²; **área livre para adulto 155,8 m² (70%)**, calculada com folga do corpo (raio 0,30 m adultos, 0,25 Lia, 0,22 crianças).

| Fase | Pessoas | Menor distância entre duas pessoas | Área livre por pessoa | Resultado |
|---|---|---|---|---|
| A — preparo | 6 | 1,39 m | 26,0 m² | ok |
| B — chegada | 14 | 0,90 m | 11,1 m² | ok |
| C — mesa | 16 | 0,60 m | 9,7 m² | ok |
| D — festa | 17 | 0,60 m | 9,2 m² | ok |

Distâncias mínimas adotadas: em pé–em pé ≥ 0,75 m; em pé–sentado ≥ 0,65; sentado–sentado ≥ 0,55 (exceção intencional: pares próximos como Caio–Bia, 0,60 m, por serem os dois mais jovens). Alcance de interação 0,9 m. **28 assentos para 17 pessoas.** Todos os assentos e pontos de interação são alcançáveis desde a soleira por Lia e por NPC, com folga para puxar a cadeira (≥ 0,25 m no ponto de aproximação). Nenhuma pessoa nas fases A–D fica sob a copa da mangueira.

Áreas livres por zona: Z1 recepção 39,5 m² (59% livre); Z2 preparo 6,5 m² (37%); Z3 mesa 21,3 m² (34%); Z3b crianças 5,0 m² (11%, cheia por desenho); Z4 convivência 57,0 m² (77%); Z5 Rita/descanso 19,8 m² (78%).

Imagem: `quintal_ocupacao.png` (4 painéis A–D).

## 3. Circulação

**Entradas e saídas (todas em metros):**
- **Soleira** X 3,5–5,5 m em Y = 8 (2,0 m): entrada de Lia e dos NPCs vindos da rua; janela da casa em X 4,8–6,0 (Z 1,1–2,1).
- **Porta de serviço** X 8,0–9,2 m em Y = 0 (1,2 × 2,3 m): só NPCs (fade); Lia recebe "Ainda não" — o interior da casa de Zefa não está construído.
- **Portão de Rita** em X = 28, Y 3,2–4,4 m: Rita e quem vem da casa dela.
- **Zona restrita da oferenda** X 13,5–15,7, Y 0–1,5 m: só Zefa e Nena ficam em pé ali (`revisar`).

**Tipos de circulação**
- *Lia e visitantes:* soleira → recepção → mesa/convivência; livre, sem trilhos.
- *Serviço (NPC de apoio):* cozinha (trempe, fogão, bancada) → aparador de serviço → mesa. Dois caminhos: **faixa de trás** (Y 1,0–2,6) e **faixa da frente** (Y ≥ 6,9, folga mínima 1,10 m). Se um deles estiver bloqueado, o outro existe: cozinha→mesa a 18,0 m pela faixa de trás ou 16,8 m pela da frente.
- *Preparação:* triângulo trempe–bancada–tanque (fogão e talha vizinhos), com bancos baixos e pilão no meio, tudo sob o puxadinho.
- *Convivência:* dominó e banco de conversa à direita; Rita na cadeira reservada, perto do portão.

**Roteamento autônomo.** Grade de 0,1 m; célula caminhável quando a distância até o obstáculo ≥ raio do corpo; rota por A* com custo de conforto (preferência por corredores livres, não trilhos fixos). As rotas medidas passam a ≥ 0,5 m do eixo do corpo a obstáculos e quase todas a ≥ 0,6 m. 19 rotas testadas (ex.: soleira → recepção 1,2 m; soleira → trempe 7,3 m; soleira → mesa 9,7 m; soleira → dominó 20,0 m; porta de serviço → aparador 3,8 m; portão → cadeira de Rita 2,8 m; portão → mesa 16,3 m; trempe → portão 26,2 m); Lia e NPC têm o mesmo percurso. Nenhuma rota atravessa móvel, parede ou zona restrita. Imagem: `quintal_rotas.png`.

## 4. Mangueira

- **Tronco:** ø 0,8 m visual; **colisão 0,6 × 0,4 m** (X 22,3–22,9; Y 2,4–2,8); altura do tronco até a copa 2,8 m.
- **Copa:** elipsoide centrado em (22,6; 2,4; 4,4) m, raios (3,0; 2,6; 1,6) m → silhueta projetada com caixa **sx 494–638, sy 0–113** (nunca cobre atividade no nível do piso; a borda inferior fica em sy 113, acima do início do piso, y 124).
- **Cabeça sob a copa:** só em uma faixa de trás (~6,5 m², Y ≤ 1,85 m, X 19–26,5 m), onde a cabeça de um adulto em pé passa sob a copa. Ali a copa fica **translúcida** (recorte). Nenhum objeto interativo nessa área e nenhum ponto de pé das fases A–D.
- **Sem colisão da copa**; só o tronco colide. Sombra no chão como decalque, sem efeito de jogo.
- **Telhado de Rita não é encoberto:** o dano (lona/telha/balde) fica em X 26,0–27,5 m, fora da silhueta da copa. Ponto de interação "olhar o telhado": (26,9; 5,7), virado para cima.
- **Leitura e interação preservadas:** teste de sobreposição passa (nenhum interativo sob a copa).

## 5. Telhado e arquitetura

**Puxadinho (cozinha de fogo):** 0–7,6 m em X × 0–5,2 m em Y; telha de **Z 3,4 m na parede a 2,6 m na frente**; apoiado em dois esteios (F05 e F06, 0,3 × 0,3 × 2,6 m) em Y = 4,8. **Função:** proteger do sol e da chuva trempe/panelão, fogão, bancada, tanque, talha, bancos, pilão e lenha (12 itens, todos conferidos: F05–F11, M23–M26, D03). **Render em corte:** só a viga do beiral frontal (sy 144,8 px) e a junção com a parede (sy 42,4 px); a telha **não** é desenhada sobre o piso; o chão sob ele é cimento mais escuro com decalque de sombra. Isso mantém a leitura de pessoas e objetos.

**Parede da casa de Zefa (F01):** X 0–11 m, 4 m de altura; **muro dos fundos (F02):** X 11–28 m, **2,4 m**; muros laterais 2,4 m. **Telhado de Rita** além do muro: beiral Z = 3 m a Y = −1,2 m (sy 32,8), cume cortado pelo topo; dano à direita do portão.

**Ligação com a casa:** porta de serviço (X 8,0–9,2 m, Y = 0) abre para o fim da bancada e o aparador; a soleira e a janela dão para a recepção. Caminho de serviço porta → aparador 3,8 m.

## 6. Áreas funcionais

| Zona | Uso | Principais objetos | Interações |
|---|---|---|---|
| Z1 Recepção (frente, X 0–8) | chegar, esperar, lavar mãos | banco de espera (M21), vasos (D01, D02), lavatório (M22) | sentar, lavar |
| Z2 Preparo (puxadinho, X 0–7,6) | descascar, cortar, cozinhar o caruru | trempe/panelão F07, fogão F08, bancada F09, tanque F10, talha F11, bancos M23–M24, pilão M25, lenha M26 | mexer, provar, descascar, servir água |
| Z3 Mesa (X 10,8–17) | refeição | mesa longa M01 + 4 cadeiras + 2 cabeceiras + banco da frente (10 lugares), aparador F12 | pôr mesa, sentar, servir |
| Z3b Crianças (X 17–20, Y 5,7–6,4) | refeição das crianças | mesinha M09 + 4 banquinhos | sentar, comer |
| Z4 Convivência (X 19–26) | dominó, conversa | mesa M14 + 4 cadeiras, banco M19, meio-fio F15 | jogar/olhar, conversar |
| Z5 Rita e descanso (direita, perto do portão) | Rita sentada, conversa, telhado | cadeira de Rita M20 | sentar, olhar telhado |
| Oferenda (fundo) | só observar | mesa baixa F13 (`revisar`), tabuleiro M27 (fase C, `revisar`) | observar |

## 7. Classificação dos elementos

Total: **27 móveis (M), 11 fixos (F05–F15) + 4 paredes (F01–F04), 4 decorativos (D01–D04)** ; 35 interativos; todos os 46 itens têm colisão.
- **Estrutural/fixo:** paredes e muros F01–F04; esteios F05–F06; trempe, fogão, bancada, tanque, talha, aparador, mesa da oferenda, tronco, meio-fio (F07–F15).
- **Móvel** (pode mudar de lugar por fase): mesas, cadeiras, bancos, mesinha, tabuleiro, lenha, pilão (M01–M27).
- **Decorativo:** vasos em lata D01–D04.
- **Interativo:** 35 (cada um com ponto de uso a ≤ 0,9 m do objeto e direção do personagem definida).
- **Obstáculo de colisão:** todos os F e M; sem colisão: sombras, decalques, copa.

## 8. Mapa de colisões e interações
Imagem `quintal_colisoes.png`: caixas de colisão em pixels de jogo, pontos de interação e direção, zona restrita, faixas preferidas. Os retângulos de colisão de cada objeto estão na tabela da seção 9 (formato `[x0,y0,x1,y1]`).

## 9. Inventário de objetos

| ID | Nome | Categoria | X,Y (m) | L×P×A (m) | L×P×A (px) | Colisão (px de jogo) | Colide | Interativo | Uso |
|---|---|---|---|---|---|---|---|---|---|
| F01 | Parede da casa de Zefa | Fixo | 0.00, -0.30 | 11.00 × 0.30 × 4.00 | 264 × 5 × 96 | [24, 119, 288, 124] | sim | não | Fundo da cozinha e porta de serviço; 4 m (sy 28) |
| F02 | Muro dos fundos (divisa) | Fixo | 11.00, -0.30 | 17.00 × 0.30 × 2.40 | 408 × 5 × 58 | [288, 119, 696, 124] | sim | não | Divisa com a casa de Rita; 2,4 m (sy 66) |
| F03 | Muro lateral esquerdo | Fixo | -0.30, 0.00 | 0.30 × 8.00 × 2.40 | 7 × 128 × 58 | [17, 124, 24, 252] | sim | não | Limite esquerdo |
| F04 | Muro lateral direito | Fixo | 28.00, 0.00 | 0.30 × 8.00 × 2.40 | 7 × 128 × 58 | [696, 124, 703, 252] | sim | não | Limite direito; contém o portão de Rita |
| F05 | Esteio do puxadinho A | Fixo | 2.50, 4.80 | 0.30 × 0.30 × 2.60 | 7 × 5 × 62 | [84, 201, 91, 206] | sim | não | Apoio do puxadinho |
| F06 | Esteio do puxadinho B | Fixo | 7.20, 4.80 | 0.30 × 0.30 × 2.60 | 7 × 5 × 62 | [197, 201, 204, 206] | sim | não | Apoio do puxadinho |
| F07 | Trempe + panelão de caruru | Fixo | 1.40, 0.60 | 1.30 × 1.00 × 0.50 | 31 × 16 × 12 | [58, 134, 89, 150] | sim | sim | Cozinhar o caruru; mexer, provar; vapor |
| F08 | Fogão a gás 4 bocas | Fixo | 3.10, 0.10 | 0.90 × 0.70 × 0.90 | 22 × 11 × 22 | [98, 126, 120, 137] | sim | sim | Cozinhar o complemento; ligar/desligar |
| F09 | Bancada de preparo | Fixo | 4.30, 0.10 | 2.50 × 0.80 × 0.90 | 60 × 13 × 22 | [127, 126, 187, 138] | sim | sim | Descascar e cortar; bacias; tábua |
| F10 | Tanque com torneira | Fixo | 0.20, 3.50 | 1.00 × 0.80 × 0.90 | 24 × 13 × 22 | [29, 180, 53, 193] | sim | sim | Lavar panela; torneira pingando |
| F11 | Talha de barro | Fixo | 7.00, 0.10 | 0.60 × 0.60 × 1.00 | 14 × 10 × 24 | [192, 126, 206, 135] | sim | sim | Servir água na caneca |
| F12 | Aparador de serviço | Fixo | 9.80, 0.10 | 3.40 × 0.90 × 0.90 | 82 × 14 × 22 | [259, 126, 341, 140] | sim | sim | Servir pratos; travessas, cuias, pilha de pratos |
| F13 | Mesa baixa da oferenda (revisar) | Fixo | 14.00, 0.20 | 1.20 × 0.90 × 0.70 | 29 × 14 × 17 | [360, 127, 389, 142] | sim | sim | Oferenda: só observar (revisar) |
| F14 | Tronco da mangueira | Fixo | 22.30, 2.40 | 0.60 × 0.40 × 2.80 | 14 × 6 × 67 | [559, 162, 574, 169] | sim | não | Árvore; sombra; sem interação |
| F15 | Meio-fio de pedra | Fixo | 25.00, 6.40 | 2.50 × 0.40 × 0.35 | 60 × 6 × 8 | [624, 226, 684, 233] | sim | sim | Sentar (2); Davi toca baixo |
| M01 | Mesa longa | Móvel | 11.50, 3.60 | 5.00 × 1.00 × 0.75 | 120 × 16 × 18 | [300, 182, 420, 198] | sim | sim | Pôr a mesa; ver lugares; 10 lugares |
| M02 | Cadeira fundo 1 | Móvel | 11.75, 2.70 | 0.50 × 0.50 × 0.90 | 12 × 8 × 22 | [306, 167, 318, 175] | sim | sim | Assento (de frente para a câmera) |
| M03 | Cadeira fundo 2 | Móvel | 13.05, 2.70 | 0.50 × 0.50 × 0.90 | 12 × 8 × 22 | [337, 167, 349, 175] | sim | sim | Assento |
| M04 | Cadeira fundo 3 | Móvel | 14.35, 2.70 | 0.50 × 0.50 × 0.90 | 12 × 8 × 22 | [368, 167, 380, 175] | sim | sim | Assento |
| M05 | Cadeira fundo 4 | Móvel | 15.65, 2.70 | 0.50 × 0.50 × 0.90 | 12 × 8 × 22 | [400, 167, 412, 175] | sim | sim | Assento |
| M06 | Cabeceira oeste | Móvel | 10.80, 3.85 | 0.50 × 0.50 × 0.90 | 12 × 8 × 22 | [283, 186, 295, 194] | sim | sim | Assento (perfil) |
| M07 | Cabeceira leste | Móvel | 16.70, 3.85 | 0.50 × 0.50 × 0.90 | 12 × 8 × 22 | [425, 186, 437, 194] | sim | sim | Assento (perfil, anfitriã) |
| M08 | Banco comprido (frente) | Móvel | 12.00, 4.70 | 3.00 × 0.45 × 0.45 | 72 × 7 × 11 | [312, 199, 384, 206] | sim | sim | Assento ×4 (de costas para a câmera) |
| M09 | Mesinha das crianças | Móvel | 17.60, 5.70 | 1.80 × 0.80 × 0.50 | 43 × 13 × 12 | [446, 215, 490, 228] | sim | sim | Mesa baixa das crianças |
| M10 | Banquinho crianças 1 | Móvel | 17.05, 5.75 | 0.40 × 0.40 × 0.30 | 10 × 6 × 7 | [433, 216, 443, 222] | sim | sim | Assento criança |
| M11 | Banquinho crianças 2 | Móvel | 17.05, 6.35 | 0.40 × 0.40 × 0.30 | 10 × 6 × 7 | [433, 226, 443, 232] | sim | sim | Assento criança |
| M12 | Banquinho crianças 3 | Móvel | 19.55, 5.75 | 0.40 × 0.40 × 0.30 | 10 × 6 × 7 | [493, 216, 503, 222] | sim | sim | Assento criança |
| M13 | Banquinho crianças 4 | Móvel | 19.55, 6.35 | 0.40 × 0.40 × 0.30 | 10 × 6 × 7 | [493, 226, 503, 232] | sim | sim | Assento criança |
| M14 | Mesa de dominó | Móvel | 20.00, 3.80 | 1.20 × 1.20 × 0.75 | 29 × 19 × 18 | [504, 185, 533, 204] | sim | sim | Olhar/jogar dominó |
| M15 | Cadeira dominó N | Móvel | 20.35, 3.10 | 0.50 × 0.50 × 0.90 | 12 × 8 × 22 | [512, 174, 524, 182] | sim | sim | Assento |
| M16 | Cadeira dominó S | Móvel | 20.35, 5.10 | 0.50 × 0.50 × 0.90 | 12 × 8 × 22 | [512, 206, 524, 214] | sim | sim | Assento |
| M17 | Cadeira dominó O | Móvel | 19.30, 4.25 | 0.50 × 0.50 × 0.90 | 12 × 8 × 22 | [487, 192, 499, 200] | sim | sim | Assento |
| M18 | Cadeira dominó L | Móvel | 21.40, 4.25 | 0.50 × 0.50 × 0.90 | 12 × 8 × 22 | [538, 192, 550, 200] | sim | sim | Assento |
| M19 | Banco de conversa | Móvel | 24.00, 4.60 | 2.00 × 0.50 × 0.45 | 48 × 8 × 11 | [600, 198, 648, 206] | sim | sim | Assento ×3; conversa |
| M20 | Cadeira de Rita | Móvel | 23.80, 2.60 | 0.60 × 0.60 × 1.00 | 14 × 10 × 24 | [595, 166, 610, 175] | sim | sim | Assento reservado de Rita |
| M21 | Banco de espera | Móvel | 0.80, 6.40 | 1.60 × 0.50 × 0.45 | 38 × 8 × 11 | [43, 226, 82, 234] | sim | sim | Assento ×2; espera |
| M22 | Lavatório (talha com caneca) | Móvel | 9.20, 5.60 | 0.50 × 0.50 × 0.90 | 12 × 8 × 22 | [245, 214, 257, 222] | sim | sim | Lavar as mãos antes de comer |
| M23 | Banco baixo de cozinha 1 | Móvel | 2.40, 3.00 | 0.60 × 0.50 × 0.45 | 14 × 8 × 11 | [82, 172, 96, 180] | sim | sim | Assento; bacia de quiabo |
| M24 | Banco baixo de cozinha 2 | Móvel | 3.60, 3.30 | 0.60 × 0.50 × 0.45 | 14 × 8 × 11 | [110, 177, 125, 185] | sim | sim | Assento; bacia de quiabo |
| M25 | Pilão | Móvel | 5.40, 2.70 | 0.50 × 0.50 × 0.50 | 12 × 8 × 12 | [154, 167, 166, 175] | sim | sim | Pilar tempero |
| M26 | Pilha de lenha | Móvel | 0.20, 0.50 | 0.70 × 2.20 × 0.70 | 17 × 35 × 17 | [29, 132, 46, 167] | sim | sim | Pegar lenha; some conforme o uso |
| M27 | Tabuleiro de Nena (só fase C) | Móvel | 17.00, 0.20 | 0.90 × 0.70 × 0.90 | 22 × 11 × 22 | [432, 127, 454, 138] | sim | sim | Aparece na fase C; acarajé (revisar) |
| D01 | Vaso em lata (recepção O) | Decorativo | 0.20, 5.40 | 0.40 × 0.40 × 0.50 | 10 × 6 × 12 | [29, 210, 38, 217] | sim | não | Planta em lata |
| D02 | Vaso em lata (recepção L) | Decorativo | 6.40, 5.60 | 0.40 × 0.40 × 0.50 | 10 × 6 × 12 | [178, 214, 187, 220] | sim | não | Planta em lata |
| D03 | Vaso em lata (cozinha) | Decorativo | 0.20, 4.55 | 0.40 × 0.40 × 0.50 | 10 × 6 × 12 | [29, 197, 38, 203] | sim | não | Planta em lata |
| D04 | Vaso em lata (muro) | Decorativo | 26.80, 0.30 | 0.40 × 0.40 × 0.50 | 10 × 6 × 12 | [667, 129, 677, 135] | sim | não | Planta em lata |
## 10. Justificativa das dimensões finais

- **28 × 8 m.** Cabe 17 pessoas com 9,2 m² livres por pessoa na fase mais cheia e 70% de piso livre; 8 m de profundidade dão duas faixas (trás e frente) sem encostar a mesa na parede e cabem em 128 px de piso, mantendo o mundo em 720 × 270 px (1,5 vez a largura da tela de 480 px: a câmera acompanha Lia).
- **Muro 2,4 m (antes 3 m).** Permite ver o telhado de Rita e o dano sem que a copa o esconda.
- **Puxadinho 7,6 × 5,2 m.** Abriga o trabalho de preparo com 37% de piso livre (6,5 m²) e deixa passar uma pessoa entre bancos (≥ 0,5 m) mesmo com 4 usuários.
- **Mesa longa 5,0 × 1,0 m** com 10 lugares e **faixa da frente com folga mínima 1,10 m**: duas pessoas se cruzam atrás do banco sem tocar.
- **Mangueira** com copa sobre o fundo direito: dá sombra e identidade ao quintal sem tapar atividade; tronco com colisão pequena (0,6 × 0,4 m) para não bloquear o caminho.

## 11. Pendências

Seguem abertas: P1 (chegada pela rua ou por corredor), P2 (interior da casa de Zefa), P3 (oferenda visível, `revisar`), P4 (reuso de assets da casa), P5 (mangueira como "quintal de ninguém"), P6 (família de Caio e Bia), P7 (detalhes de Rita e fim do telhado), P8 (momento do mutirão), P9 (mundo rolando × 480 px), P10 (16 NPCs e desempenho), P11 (itens opcionais), P12 (sua mensagem terminou em "e criar também" — o que faltava?). Também: a pergunta da cadeira de Bela (Etapa 9) e a revisão cultural da oferenda, da roupa de Nena e do instrumento de Davi.

## 12. Arquivos
`out/quintal_planta_rev.png`, `out/quintal_vista34_rev_720x270.png`, `out/quintal_vista34_rev_1440x540.png`, `out/quintal_vista34_rev_anotada_1440x540.png`, `out/quintal_ocupacao.png`, `out/quintal_rotas.png`, `out/quintal_colisoes.png`, `out/quintal_teste.json`; código em `tools/quintal_data.py`, `tools/teste_quintal.py`, `tools/gerar_quintal.py`.
