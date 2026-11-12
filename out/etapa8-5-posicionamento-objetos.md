# Etapa 8.5 — Distribuição, posicionamento e integração dos objetos no quintal (proposta)

**Status: proposta de posicionamento para aprovação. Nada foi implementado, nenhuma animação, nenhum sprite.** Parte da planta revisada (8.3), com os ajustes listados na seção 1. Números: `tools/quintal_data.py` + `tools/quintal_pos.py` (metros do mundo; mesmas unidades e mesma projeção 3/4 da 8.3). Verificação: `teste_quintal.py` (33/33, sem regressão) e `teste_pos.py` (25/25). `revisar` = precisa de olhar de quem é da cultura de axé.

## 0. O que mudou desde a 8.3 revisada

| # | O quê | Por quê |
|---|---|---|
| 1 | **Erro corrigido na minha vista 3/4 anterior**: os objetos eram desenhados com 1 m de altura (usei a coluna errada). Alturas reais agora (esteios 2,6 m, cadeiras 0,9 m, mesas 0,75 m etc.). A planta e as posições não mudam; o teste de "nada interativo sob a copa" foi refeito com a altura certa e continua passando | achado ao montar a 8.5 |
| 2 | **Lavatório M22** de (9,2; 5,6) para **(10,2; 6,0)** | abrir a frente da toalha dos sete meninos; continua perto da mesa (lavar as mãos antes de comer) |
| 3 | **Pontos de uso do aparador** F12a/F12b agora (11,2; 1,32) e (12,3; 1,32), lado a lado (1,10 m) | quem serve e quem recebe cabem juntos; antes eram (10,8; 1,55) e (12,2; 1,55) |
| 4 | **Nova fase C1 — "os meninos comem"** antes da C (mesa) | pela tradição as sete crianças comem primeiro e só depois os adultos (ver seção 4) |
| 5 | Nomes das zonas passam a seguir a sua 8.5: **Z1 Cozinha · Z2 Serviço · Z3 Mesa · Z4 Mangueira e convivência · Z5 Recepção**, mais **ZE** (sete meninos e altar) | na 8.3 revisada Z1 era a recepção e Z5 era Rita; só renomeei, as áreas são as mesmas |

Nada mais da planta aprovada foi mexido (dimensões, paredes, puxadinho, mangueira, mesa, dominó, banco de Rita etc.).

## 1. Decisão sobre Cosme e Damião: bandeira na parede da casa

**Bandeira B01**: pano vertical **1,70 × 2,70 m** (4,59 m²), pendurado por duas varetas, na parede da casa (F01), **X 9,25–10,95 m, Z 1,25–3,95 m**.

**Como cheguei a "40–45%".** A parede da casa mede 11 × 4 m (44 m²), mas só o trecho entre o puxadinho (X 7,6) e o canto (X 11) tem parede livre; descontando a porta de serviço (1,2 × 2,3 m) sobra **10,84 m²**. A bandeira ocupa **42% desse pano livre** (e 10% da parede inteira). 40–45% da parede inteira (18–20 m²) não cabe: cobriria a porta e o puxadinho. Se você quis outra base, é só dizer e eu redimensiono (ex.: 45% do pano livre = 1,8 × 2,7 m, X 9,25–11,05).

Por que ali: está sobre o aparador e alinhada na vista 3/4 com a toalha dos sete meninos (a toalha fica logo abaixo e à esquerda), e é a única parede livre do quintal. Nada sobre o aparador chega perto dela (o mais alto, o vasinho de flores, termina em Z 1,18; a bandeira começa em 1,25).

**Altar**: a bandeira + o **prato dos santos** (primeira porção, `revisar`), uma **vela em pires** e um **vasinho com flores brancas** no extremo oeste do aparador (X 9,9–10,6 m), debaixo da bandeira. Esse trecho de 0,8 m é só para observar; o serviço usa o resto do aparador. A arte da bandeira é esquema na imagem (dois santos gêmeos); **arte final a criar**, e a representação dos santos precisa de revisão cultural (`revisar`).

## 2. Organização por zonas

| Zona | Nome | Retângulo (X0,Y0–X1,Y1 m) |
|---|---|---|
| Z1 | Cozinha e preparação (puxadinho) | 0,0; 0,0 – 7,6; 5,2 |
| Z2 | Serviço e distribuição (aparador, oferenda, tabuleiro de Nena) | 9,8; 0,0 – 18,0; 1,9 |
| Z3 | Mesa e refeição (mesa longa, banco, mesinha, lavatório) | 10,3; 2,4 – 20,1; 7,0 |
| Z4 | Mangueira e convivência (dominó, banco, Rita, meio-fio) | 18,6; 1,0 – 27,8; 7,2 |
| Z5 | Recepção | 0,0; 5,4 – 7,6; 8,0 |
| ZE | Sete meninos e altar | toalha 8,1; 2,9 – 10,3; 5,1 + bandeira em B01 |

Z2, Z3 e Z4 se sobrepõem em faixas de passagem (convenção: vale a zona do objeto).

## 3. Posicionamento técnico por zona

Convenções: X, Y em metros do canto de trás à esquerda do piso (canto do objeto); "Z base · A" é a altura do apoio e a altura do objeto; "Persp." = 3/4 do jogo (24 px/m em X e Z, 16 px/m em Y); **colisão dos objetos menores é herdada do móvel que os apoia** (não bloqueiam sozinhos). Coordenadas em pixels de jogo: `pg = (24 + 24·X, 124 + 16·Y)`. Retângulos de colisão dos objetos aprovados estão na tabela da seção 9 da 8.3 revisada (`claude/etapa8-3-projeto-quintal-revisado.md`), sem alteração, exceto o M22 (agora [269, 220, 281, 228] px).

#### Z1 — Cozinha e preparação
| ID | Nome | X,Y (m) | Z base · A (m) | L×P (m) | Persp. | Orientação | Colisão | Área de interação (ponto de uso) | Camada | Estado inicial |
|---|---|---|---|---|---|---|---|---|---|---|
| F05 | Esteio do puxadinho A | 2.50; 4.80 | 0,00 · 2.60 | 0.30×0.30 | 3/4 | frente | sim | — | L5 (y da base) | fixo |
| F06 | Esteio do puxadinho B | 7.20; 4.80 | 0,00 · 2.60 | 0.30×0.30 | 3/4 | frente | sim | — | L5 (y da base) | fixo |
| F07 | Trempe + panelão de caruru | 1.40; 0.60 | 0,00 · 0.50 | 1.30×1.00 | 3/4 | frente | sim | (2.0; 2.05) up | L5 (y da base) | fixo |
| F08 | Fogão a gás 4 bocas | 3.10; 0.10 | 0,00 · 0.90 | 0.90×0.70 | 3/4 | frente | sim | (3.55; 1.25) up | L5 (y da base) | fixo |
| F09 | Bancada de preparo | 4.30; 0.10 | 0,00 · 0.90 | 2.50×0.80 | 3/4 | frente | sim | (5.5; 1.3) up | L5 (y da base) | fixo |
| F10 | Tanque com torneira | 0.20; 3.50 | 0,00 · 0.90 | 1.00×0.80 | 3/4 | frente | sim | (1.8; 3.9) left | L5 (y da base) | fixo |
| F11 | Talha de barro | 7.00; 0.10 | 0,00 · 1.00 | 0.60×0.60 | 3/4 | frente | sim | (7.3; 1.3) up | L5 (y da base) | fixo |
| M23 | Banco baixo de cozinha 1 | 2.40; 3.00 | 0,00 · 0.45 | 0.60×0.50 | 3/4 | frente | sim | coz_1 aproxima (2.7; 2.6) | L5 (y da base) | na posição |
| M24 | Banco baixo de cozinha 2 | 3.60; 3.30 | 0,00 · 0.45 | 0.60×0.50 | 3/4 | frente | sim | coz_2 aproxima (3.9; 2.9) | L5 (y da base) | na posição |
| M25 | Pilão | 5.40; 2.70 | 0,00 · 0.50 | 0.50×0.50 | 3/4 | frente | sim | (5.65; 3.6) up | L5 (y da base) | na posição |
| M26 | Pilha de lenha | 0.20; 0.50 | 0,00 · 0.70 | 0.70×2.20 | 3/4 | frente | sim | — | L5 (y da base) | na posição |
| D03 | Vaso em lata (cozinha) | 0.20; 4.55 | 0,00 · 0.50 | 0.40×0.40 | 3/4 | frente | sim | — | L5 (y da base) | na posição |

#### Z2 — Serviço e distribuição
| ID | Nome | X,Y (m) | Z base · A (m) | L×P (m) | Persp. | Orientação | Colisão | Área de interação (ponto de uso) | Camada | Estado inicial |
|---|---|---|---|---|---|---|---|---|---|---|
| F12 | Aparador de serviço | 9.80; 0.10 | 0,00 · 0.90 | 3.40×0.90 | 3/4 | frente | sim | F12a (11.2; 1.32) · F12b (12.3; 1.32) | L5 (y da base) | fixo |
| F13 | Mesa baixa da oferenda (revisar) | 14.00; 0.20 | 0,00 · 0.70 | 1.20×0.90 | 3/4 | frente | sim | (14.6; 1.9) up | L5 (y da base) | fixo |
| M27 | Tabuleiro de Nena (só fase C) | 17.00; 0.20 | 0,00 · 0.90 | 0.90×0.70 | 3/4 | frente | sim | (17.45; 1.35) up | L5 (y da base) | só a partir da fase C |

#### Z3 — Mesa e refeição
| ID | Nome | X,Y (m) | Z base · A (m) | L×P (m) | Persp. | Orientação | Colisão | Área de interação (ponto de uso) | Camada | Estado inicial |
|---|---|---|---|---|---|---|---|---|---|---|
| M01 | Mesa longa | 11.50; 3.60 | 0,00 · 0.75 | 5.00×1.00 | 3/4 | frente | sim | (12.65; 3.05) down | L5 (y da base) | na posição |
| M02 | Cadeira fundo 1 | 11.75; 2.70 | 0,00 · 0.90 | 0.50×0.50 | 3/4 | frente (voltada à câmera) | sim | mesa_f1 aproxima (12.0; 2.2) | L5 (y da base) | na posição |
| M03 | Cadeira fundo 2 | 13.05; 2.70 | 0,00 · 0.90 | 0.50×0.50 | 3/4 | frente | sim | mesa_f2 aproxima (13.3; 2.2) | L5 (y da base) | na posição |
| M04 | Cadeira fundo 3 | 14.35; 2.70 | 0,00 · 0.90 | 0.50×0.50 | 3/4 | frente | sim | mesa_f3 aproxima (14.6; 2.2) | L5 (y da base) | na posição |
| M05 | Cadeira fundo 4 | 15.65; 2.70 | 0,00 · 0.90 | 0.50×0.50 | 3/4 | frente | sim | mesa_f4 aproxima (15.9; 2.2) | L5 (y da base) | na posição |
| M06 | Cabeceira oeste | 10.80; 3.85 | 0,00 · 0.90 | 0.50×0.50 | 3/4 | perfil direito | sim | mesa_cab_O aproxima (10.0; 4.1) | L5 (y da base) | na posição |
| M07 | Cabeceira leste | 16.70; 3.85 | 0,00 · 0.90 | 0.50×0.50 | 3/4 | perfil esquerdo | sim | mesa_cab_L aproxima (18.0; 4.1) | L5 (y da base) | na posição |
| M08 | Banco comprido (frente) | 12.00; 4.70 | 0,00 · 0.45 | 3.00×0.45 | 3/4 | costas (de costas para a câmera) | sim | banco_1 aproxima (12.4; 5.9); banco_2 aproxima (13.2; 5.9); banco_3 aproxima (14.0; 5.9); banco_4 aproxima (14.8; 5.9) | L5 (y da base) | na posição |
| M09 | Mesinha das crianças | 17.60; 5.70 | 0,00 · 0.50 | 1.80×0.80 | 3/4 | frente | sim | (18.5; 5.0) down | L5 (y da base) | na posição |
| M10 | Banquinho crianças 1 | 17.05; 5.75 | 0,00 · 0.30 | 0.40×0.40 | 3/4 | frente | sim | cri_1 aproxima (16.4; 5.95) | L5 (y da base) | na posição |
| M11 | Banquinho crianças 2 | 17.05; 6.35 | 0,00 · 0.30 | 0.40×0.40 | 3/4 | frente | sim | cri_2 aproxima (16.4; 6.55) | L5 (y da base) | na posição |
| M12 | Banquinho crianças 3 | 19.55; 5.75 | 0,00 · 0.30 | 0.40×0.40 | 3/4 | frente | sim | cri_3 aproxima (20.6; 5.95) | L5 (y da base) | na posição |
| M13 | Banquinho crianças 4 | 19.55; 6.35 | 0,00 · 0.30 | 0.40×0.40 | 3/4 | frente | sim | cri_4 aproxima (20.6; 6.55) | L5 (y da base) | na posição |
| M22 | Lavatório (talha com caneca) | 10.20; 6.00 | 0,00 · 0.90 | 0.50×0.50 | 3/4 | frente | sim | (9.7; 6.25) right | L5 (y da base) | na posição |

#### Z4 — Mangueira e convivência
| ID | Nome | X,Y (m) | Z base · A (m) | L×P (m) | Persp. | Orientação | Colisão | Área de interação (ponto de uso) | Camada | Estado inicial |
|---|---|---|---|---|---|---|---|---|---|---|
| F14 | Tronco da mangueira | 22.30; 2.40 | 0,00 · 2.80 | 0.60×0.40 | 3/4 | frente | sim | — | L5 (y da base) | fixo |
| F15 | Meio-fio de pedra | 25.00; 6.40 | 0,00 · 0.35 | 2.50×0.40 | 3/4 | frente | sim | fio_1 aproxima (25.6; 7.4); fio_2 aproxima (26.8; 7.4) | L5 (y da base) | fixo |
| M14 | Mesa de dominó | 20.00; 3.80 | 0,00 · 0.75 | 1.20×1.20 | 3/4 | frente | sim | (21.9; 3.4) left | L5 (y da base) | na posição |
| M15 | Cadeira dominó N | 20.35; 3.10 | 0,00 · 0.90 | 0.50×0.50 | 3/4 | frente | sim | dom_N aproxima (20.6; 2.5) | L5 (y da base) | na posição |
| M16 | Cadeira dominó S | 20.35; 5.10 | 0,00 · 0.90 | 0.50×0.50 | 3/4 | costas | sim | dom_S aproxima (20.6; 6.2) | L5 (y da base) | na posição |
| M17 | Cadeira dominó O | 19.30; 4.25 | 0,00 · 0.90 | 0.50×0.50 | 3/4 | perfil direito | sim | dom_O aproxima (18.7; 4.5) | L5 (y da base) | na posição |
| M18 | Cadeira dominó L | 21.40; 4.25 | 0,00 · 0.90 | 0.50×0.50 | 3/4 | perfil esquerdo | sim | dom_L aproxima (22.3; 4.5) | L5 (y da base) | na posição |
| M19 | Banco de conversa | 24.00; 4.60 | 0,00 · 0.45 | 2.00×0.50 | 3/4 | frente | sim | conv_1 aproxima (24.4; 5.7); conv_2 aproxima (25.0; 5.7); conv_3 aproxima (25.6; 5.7) | L5 (y da base) | na posição |
| M20 | Cadeira de Rita | 23.80; 2.60 | 0,00 · 1.00 | 0.60×0.60 | 3/4 | frente | sim | rita aproxima (24.1; 3.8) | L5 (y da base) | na posição |
| D04 | Vaso em lata (muro) | 26.80; 0.30 | 0,00 · 0.50 | 0.40×0.40 | 3/4 | frente | sim | — | L5 (y da base) | na posição |

#### Z5 — Recepção
| ID | Nome | X,Y (m) | Z base · A (m) | L×P (m) | Persp. | Orientação | Colisão | Área de interação (ponto de uso) | Camada | Estado inicial |
|---|---|---|---|---|---|---|---|---|---|---|
| M21 | Banco de espera | 0.80; 6.40 | 0,00 · 0.45 | 1.60×0.50 | 3/4 | frente | sim | espera_1 aproxima (1.2; 7.4); espera_2 aproxima (2.0; 7.4) | L5 (y da base) | na posição |
| D01 | Vaso em lata (recepção O) | 0.20; 5.40 | 0,00 · 0.50 | 0.40×0.40 | 3/4 | frente | sim | — | L5 (y da base) | na posição |
| D02 | Vaso em lata (recepção L) | 6.40; 5.60 | 0,00 · 0.50 | 0.40×0.40 | 3/4 | frente | sim | — | L5 (y da base) | na posição |

#### Arquitetura — Arquitetura (paredes e muros)
| ID | Nome | X,Y (m) | Z base · A (m) | L×P (m) | Persp. | Orientação | Colisão | Área de interação (ponto de uso) | Camada | Estado inicial |
|---|---|---|---|---|---|---|---|---|---|---|
| F01 | Parede da casa de Zefa | 0.00; -0.30 | 0,00 · 4.00 | 11.00×0.30 | 3/4 | frente | sim | — | L2 parede | fixo |
| F02 | Muro dos fundos (divisa) | 11.00; -0.30 | 0,00 · 2.40 | 17.00×0.30 | 3/4 | frente | sim | — | L2 parede | fixo |
| F03 | Muro lateral esquerdo | -0.30; 0.00 | 0,00 · 2.40 | 0.30×8.00 | 3/4 | frente | sim | — | L2 parede | fixo |
| F04 | Muro lateral direito | 28.00; 0.00 | 0,00 · 2.40 | 0.30×8.00 | 3/4 | frente | sim | — | L2 parede | fixo |

#### Objetos menores (S) e do altar/sete meninos (E)

| ID | Nome | Zona | Apoio | X,Y (m) | Z base · A (m) | L×P (m) | Persp. | Orient. | Colisão | Ponto de uso | Camada | Estado inicial |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S01 | Panela de vatapá (fogão) | Z1 | F08 | 3.12; 0.15 | 0.90 · 0.22 | 0.34×0.34 | 3/4 | frente | não (herda do apoio) | (3.55; 1.25) up | L5 | no fogo, tampada |
| S02 | Caçarola de camarão e dendê (fogão) | Z1 | F08 | 3.60; 0.45 | 0.90 · 0.16 | 0.30×0.30 | 3/4 | frente | não (herda do apoio) | (3.55; 1.25) up | L5 | no fogo, tampada |
| S03 | Tábua de corte | Z1 | F09 | 4.45; 0.20 | 0.90 · 0.04 | 0.60×0.40 | 3/4 | frente | não (herda do apoio) | (5.5; 1.3) up | L5 | com cebolas picadas |
| S04 | Bacia de quiabo cortado | Z1 | F09 | 5.15; 0.20 | 0.90 · 0.14 | 0.40×0.40 | 3/4 | frente | não (herda do apoio) | (5.5; 1.3) up | L5 | cheia |
| S05 | Bacia de camarão seco e castanha | Z1 | F09 | 5.65; 0.25 | 0.90 · 0.10 | 0.30×0.30 | 3/4 | frente | não (herda do apoio) | (5.5; 1.3) up | L5 | cheia |
| S06 | Cesto de temperos (cebola, tomate, pimenta) | Z1 | F09 | 6.05; 0.20 | 0.90 · 0.20 | 0.40×0.40 | 3/4 | frente | não (herda do apoio) | (6.2; 1.3) up | L5 | cheio |
| S07 | Faca e colheres de pau (bandeja) | Z1 | F09 | 6.50; 0.20 | 0.90 · 0.03 | 0.25×0.25 | 3/4 | frente | não (herda do apoio) | (6.2; 1.3) up | L5 | arrumados |
| S08 | Balde de água (borda do tanque) | Z1 | F10 | 0.80; 3.62 | 0.90 · 0.30 | 0.35×0.35 | 3/4 | frente | não (herda do apoio) | (1.8; 3.9) left | L5 | cheio |
| S09 | Colher de pau grande (encostada no panelão) | Z1 | F07 | 2.25; 0.95 | 0.50 · 0.08 | 0.10×0.60 | 3/4 | lado | não (herda do apoio) | (2.0; 2.05) up | L5 | no panelão |
| S10 | Bacia de quiabo no chão (trabalho sentado) | Z1 | chão | 3.05; 3.05 | 0.00 · 0.14 | 0.50×0.50 | 3/4 | frente | não (herda do apoio) | (2.9; 2.6) down | L5 | cheia |
| E12 | Prato dos santos (primeira porção) | ZE | F12 | 9.90; 0.55 | 0.90 · 0.03 | 0.30×0.30 | 3/4 | frente | não (herda do apoio) | (11.2; 1.32) up | L5 | servido; `revisar` |
| E13 | Vela em pires | ZE | F12 | 10.30; 0.25 | 0.90 · 0.12 | 0.14×0.14 | 3/4 | frente | não (herda do apoio) | (11.2; 1.32) up | L5 | acesa; `revisar` |
| E14 | Vasinho com flores brancas | ZE | F12 | 10.45; 0.55 | 0.90 · 0.28 | 0.18×0.18 | 3/4 | frente | não (herda do apoio) | (11.2; 1.32) up | L5 | com flores; `revisar` |
| S12 | Pilha de pratos | Z2 | F12 | 10.80; 0.60 | 0.90 · 0.18 | 0.30×0.30 | 3/4 | frente | não (herda do apoio) | (11.2; 1.32) up | L5 | cheia |
| S13 | Travessa de caruru | Z2 | F12 | 11.15; 0.60 | 0.90 · 0.08 | 0.50×0.35 | 3/4 | frente | não (herda do apoio) | (11.2; 1.32) up | L5 | cheia |
| S14 | Travessa de vatapá | Z2 | F12 | 11.75; 0.60 | 0.90 · 0.08 | 0.50×0.35 | 3/4 | frente | não (herda do apoio) | (12.3; 1.32) up | L5 | cheia |
| S15 | Travessa de arroz e farofa | Z2 | F12 | 12.35; 0.60 | 0.90 · 0.08 | 0.55×0.35 | 3/4 | frente | não (herda do apoio) | (12.3; 1.32) up | L5 | cheia |
| S16 | Cuia com talheres | Z2 | F12 | 10.85; 0.25 | 0.90 · 0.10 | 0.22×0.22 | 3/4 | frente | não (herda do apoio) | (11.2; 1.32) up | L5 | cheia |
| S17 | Bandeja de copos | Z2 | F12 | 11.20; 0.20 | 0.90 · 0.10 | 0.50×0.30 | 3/4 | frente | não (herda do apoio) | (11.2; 1.32) up | L5 | cheia |
| S18 | Conchas e colheres de servir | Z2 | F12 | 11.85; 0.22 | 0.90 · 0.10 | 0.30×0.25 | 3/4 | frente | não (herda do apoio) | (12.3; 1.32) up | L5 | penduradas no pote |
| S19 | Jarra de água | Z2 | F12 | 12.30; 0.22 | 0.90 · 0.28 | 0.25×0.25 | 3/4 | frente | não (herda do apoio) | (12.3; 1.32) up | L5 | cheia |
| S20 | Tacho de dendê (tabuleiro) | Z2 | M27 | 17.05; 0.30 | 0.90 · 0.18 | 0.35×0.35 | 3/4 | frente | não (herda do apoio) | (17.45; 1.35) up | L5 | quente; `revisar` |
| S21 | Bacia de massa coberta com pano | Z2 | M27 | 17.50; 0.30 | 0.90 · 0.18 | 0.32×0.32 | 3/4 | frente | não (herda do apoio) | (17.45; 1.35) up | L5 | coberta; `revisar` |
| S22 | Toalha da mesa longa | Z3 | M01 | 11.50; 3.60 | 0.75 · 0.01 | 5.00×1.00 | 3/4 | frente | não (herda do apoio) | (12.65; 3.05) down | L5 | estendida |
| S23 | Travessa central de caruru | Z3 | M01 | 13.55; 3.95 | 0.76 · 0.08 | 0.55×0.35 | 3/4 | frente | não (herda do apoio) | (12.65; 3.05) down | L5 | cheia na fase C |
| S24 | Travessa de vatapá | Z3 | M01 | 14.25; 3.95 | 0.76 · 0.08 | 0.55×0.35 | 3/4 | frente | não (herda do apoio) | (12.65; 3.05) down | L5 | cheia na fase C |
| S25 | Cesto de acarajé e banana frita | Z3 | M01 | 12.65; 3.95 | 0.76 · 0.10 | 0.50×0.35 | 3/4 | frente | não (herda do apoio) | (12.65; 3.05) down | L5 | cheio na fase C |
| S26 | Jarra de água | Z3 | M01 | 15.00; 3.80 | 0.76 · 0.26 | 0.22×0.22 | 3/4 | frente | não (herda do apoio) | (12.65; 3.05) down | L5 | cheia |
| S27 | Jarra de suco | Z3 | M01 | 15.40; 3.80 | 0.76 · 0.26 | 0.22×0.22 | 3/4 | frente | não (herda do apoio) | (12.65; 3.05) down | L5 | cheia |
| S28 | Pratos individuais (10 lugares) | Z3 | M01 | 11.90; 3.70 | 0.76 · 0.03 | 0.30×0.25 | 3/4 | frente | não (herda do apoio) | (12.65; 3.05) down | L5 | postos na fase C; 10 pratos: ver tabela |
| S29 | Prato de cocada (mesinha das crianças) | Z3 | M09 | 17.95; 5.85 | 0.50 · 0.05 | 0.35×0.30 | 3/4 | frente | não (herda do apoio) | (18.5; 5.0) down | L5 | com cocada (presente de Tonho) |
| S30 | Peças de dominó | Z4 | M14 | 20.35; 4.20 | 0.75 · 0.03 | 0.50×0.35 | 3/4 | frente | não (herda do apoio) | (21.9; 3.4) left | L5 | espalhadas na fase D |
| E01 | Toalha de chita dos sete meninos | ZE | chão | 8.10; 2.90 | 0.00 · 0.01 | 2.20×2.20 | 3/4 | frente | não (herda do apoio) | toalha (ver seção 4) | L4 | guardada (fases A–B); posta em C1; recolhida em C/D |
| E02 | Bacia central de caruru | ZE | E01 | 9.00; 3.80 | 0.01 · 0.14 | 0.40×0.40 | 3/4 | frente | não (herda do apoio) | toalha (ver seção 4) | L5 | cheia em C1 |
| E03 | Pratinho de barro 1 | ZE | E01 | 8.72; 3.49 | 0.01 · 0.04 | 0.28×0.28 | 3/4 | frente | não (herda do apoio) | toalha (ver seção 4) | L5 | servido em C1 |
| E04 | Pratinho de barro 2 | ZE | E01 | 8.56; 3.81 | 0.01 · 0.04 | 0.28×0.28 | 3/4 | frente | não (herda do apoio) | toalha (ver seção 4) | L5 | servido em C1 |
| E05 | Pratinho de barro 3 | ZE | E01 | 8.65; 4.15 | 0.01 · 0.04 | 0.28×0.28 | 3/4 | frente | não (herda do apoio) | toalha (ver seção 4) | L5 | servido em C1 |
| E06 | Pratinho de barro 4 | ZE | E01 | 9.46; 4.15 | 0.01 · 0.04 | 0.28×0.28 | 3/4 | frente | não (herda do apoio) | toalha (ver seção 4) | L5 | servido em C1 |
| E07 | Pratinho de barro 5 | ZE | E01 | 9.56; 3.81 | 0.01 · 0.04 | 0.28×0.28 | 3/4 | frente | não (herda do apoio) | toalha (ver seção 4) | L5 | servido em C1 |
| E08 | Pratinho de barro 6 | ZE | E01 | 9.39; 3.49 | 0.01 · 0.04 | 0.28×0.28 | 3/4 | frente | não (herda do apoio) | toalha (ver seção 4) | L5 | servido em C1 |
| E09 | Pratinho de barro 7 | ZE | E01 | 9.06; 3.36 | 0.01 · 0.04 | 0.28×0.28 | 3/4 | frente | não (herda do apoio) | toalha (ver seção 4) | L5 | servido em C1 |
| E10 | Bandeja de doces e banana | ZE | E01 | 9.00; 4.50 | 0.01 · 0.05 | 0.40×0.25 | 3/4 | frente | não (herda do apoio) | toalha (ver seção 4) | L5 | posta em C1 |
| E11 | Sete copinhos (um à direita de cada pratinho; grupo) | ZE | E01 | 9.40; 4.45 | 0.01 · 0.09 | 0.08×0.08 | 3/4 | frente | não (herda do apoio) | toalha (ver seção 4) | L5 | postos em C1 |
| B01 | Bandeira de Cosme e Damião (pano pendurado) | ZE | parede da casa (F01) | 9.25; 0,00 | 1.25 · 2.70 | 1.70×0,02 | 3/4 (plano frontal, encostada) | frente | não (na parede) | ponto de olhar (10,1; 1,95) · área X 9,0–11,3; Y 1,45–2,2 | L3 parede | pendurada desde a fase A | 

#### Roda dos sete meninos (posições em metros; centro da toalha 9,20; 4,00)

| Menino | Quem | Posição (X; Y) | Pratinho (X; Y) | Ângulo (° a partir da câmera) |
|---|---|---|---|---|
| 1 | Júnior (11, existente) | 8.63; 3.37 | 8.87; 3.63 | -138 |
| 2 | figurante infantil M1 | 8.36; 3.91 | 8.70; 3.95 | -96 |
| 3 | figurante infantil M2 | 8.51; 4.50 | 8.79; 4.29 | -54 |
| 4 | figurante infantil M3 | 9.89; 4.50 | 9.61; 4.29 | 54 |
| 5 | figurante infantil M4 | 10.04; 3.91 | 9.70; 3.95 | 96 |
| 6 | figurante infantil M5 | 9.77; 3.37 | 9.54; 3.63 | 138 |
| 7 | figurante infantil M6 | 9.20; 3.15 | 9.20; 3.50 | 180 |

Regras de posicionamento aplicadas: panelas grandes sobre o fogão ou sobre a trempe (fogo) e nunca no chão, **exceto a bacia de quiabo S10**, no chão entre os dois bancos baixos de cozinha porque o trabalho é sentado (descascar); utensílios pequenos sobre a bancada, o aparador ou a mesa; recipientes de água na talha (F11), no balde sobre a borda do tanque (S08) e na jarra do aparador (S19).

## 4. Sete meninos: composição especial

**Tradição que orientou o desenho** (fontes na seção 10): a primeira porção é servida à imagem de Cosme e Damião; em seguida sete crianças são convidadas a comer, antes dos demais; costuma-se estender uma toalha no chão e as crianças sentam em roda, comendo com as mãos em pratinhos de barro ou numa bacia, embora hoje haja variações (misturar meninos e meninas, usar talheres). Há quem diga "até 7 anos", há quem não restrinja; **a idade das crianças é decisão sua e vai como `revisar`** (ver P14).

**Configuração escolhida**: sete **pratinhos de barro individuais**, uma **bacia central de caruru** (reposição) e uma **bandeja de doces e banana**, sete copinhos; comer com as mãos.

| Elemento | Medida | Posição |
|---|---|---|
| E01 Toalha de chita | 2,20 × 2,20 m, ao nível do chão | X 8,1–10,3 · Y 2,9–5,1 (centro 9,20; 4,00) |
| Faixa de respeito | 0,40 m ao redor | X 7,7–10,7 · Y 2,5–5,5 |
| Roda de 7 | raio 0,85 m; distância mínima entre meninos **0,61 m** | roda **aberta para a câmera** (lacuna de 108° na frente), para a comida e os rostos aparecerem |
| Pratinhos | ø 0,28 m, a 0,50 m do centro | um diante de cada menino (alcance 0,35 m) |
| E02 Bacia central | ø 0,40 m | centro da toalha |
| E10 Bandeja | 0,40 × 0,25 m | no vão da frente da roda |

Quem senta: **Júnior (11, existente)** e **6 figurantes infantis novos** (sem nome, 1,05–1,22 m de altura, raio 0,20 m).

**Respeito da composição**: a toalha e sua faixa de 0,4 m não têm nenhuma mesa, cadeira ou banco (testado); na fase C1 viram **obstáculo para toda a navegação**, e só **Zefa** pode dar um passo para dentro da faixa para servir (pelo vão da frente, ponto (9,20; 5,25)); em repouso ela fica no corredor de trás, em (9,20; 2,20). Lia não pisa na toalha.

**Linha do tempo da toalha**: guardada nas fases A–B; **posta na C1**; recolhida na C e na D (os meninos vão para a mesinha M09 ou para o meio-fio, como já estava na planta).

**Legibilidade na câmera 3/4** (visibilidade medida pela sobreposição dos retângulos projetados, ordenada pelo y da base): cada menino fica **54–100%** visível (o pior é o menino 1); bacia 100%, bandeja 100%, pratinhos **43–83%** (os dois pratinhos laterais ficam parcialmente atrás dos vizinhos da frente; é o limite de uma roda vista a 3/4, sem o jogo desenhar o prato maior ou mais claro). Nenhum menino e nenhuma comida fica 100% escondido.

## 5. Relação com os personagens (pontos de interação)

| Pergunta | Resposta (ponto de parada, m) |
|---|---|
| NPC alcança a panela? | Panelão: (2,0; 2,05) · fogão: (3,55; 1,25) · todos a ≤ 0,95 m do braço |
| Quem mexe o alimento? | Zefa/Cícera no panelão (colher S09) e no fogão (S01, S02) |
| Alguém pega prato na bancada/aparador? | Aparador: F12a (11,2; 1,32) pilha de pratos, cuia e copos; F12b (12,3; 1,32) travessas e jarra; 1,10 m entre os dois, então servir e receber cabem lado a lado |
| Lia examina a bandeira dos santos sem atravessar nada? | Sim: ponto (10,1; 1,95) a 1,95 m da parede, no corredor em frente ao aparador (área X 9,0–11,3 · Y 1,45–2,2); alcançável da soleira em 9,2 m sem entrar em nenhuma zona de respeito |
| As sete crianças sentam ao redor? | Sim, roda de 0,85 m, 0,61 m entre elas (seção 4) |
| Convidados circulam sem atravessar a mesa? | Sim: faixas de trás (corredor de 1,5 m entre aparador e faixa de respeito) e da frente; rotas abaixo |
| Lia vê Júnior e os meninos comendo? | Sim, a partir do corredor (10,7; 2,0) ou do vão da frente |

## 6. Rotas livres de circulação (fase C1, com a toalha bloqueada)

| De | Para | Comprimento (Lia / NPC) | Folga do corpo |
|---|---|---|---|
| Soleira | Ponto de olhar a bandeira | 9,2 / 9,2 m | 0,30 m |
| Porta de serviço | Aparador | 2,9 / 2,9 m | 0,30 m |
| Cozinha (trempe) | Aparador | 9,4 / 9,4 m | 0,40 m |
| Aparador | Borda da faixa de respeito (Zefa serve) | 9,7 / 9,8 m | 0,30 m |
| Soleira | Frente da mesa | 9,7 / 9,7 m | 0,50 m |
| Soleira | Dominó | 19,2 / 19,3 m | 0,30 m |
| Recepção | Lavatório | 5,7 / 5,7 m | 0,40 m |
| Cozinha | Mesa (lado oeste, por baixo) | 9,1 / 9,1 m | 0,30 m |
| Portão | Aparador | 15,5 / 15,5 m | 0,30 m |

São referências para a navegação autônoma (A* com custo de conforto), não trilhos; o corredor entre o aparador e a faixa de respeito tem **1,50 m**. Imagem: `quintal_pos_mapa.png` (colisões em vermelho, interação em verde, bandeira em amarelo, rotas coloridas).

## 7. Verificação de compatibilidade com o povoamento

- **Fases A, B, C, D da 8.3**: sem mudança, **33/33** testes continuam passando (com o M22 no novo lugar e a altura corrigida).
- **Fase C1 (nova)**: **22 pessoas** (Lia, 14 adultos e jovens, Júnior e 6 figurantes); menor distância **0,61 m**; **7,1 m² livres por pessoa**; ninguém na toalha nem na faixa de respeito (exceto Zefa na posição de serviço).
- **Objetos menores**: 43 itens; todos dentro do apoio, na altura do topo, sem sobreposição; nenhum no chão sem justificativa; alcance do braço ≤ 0,95 m.
- **Bandeira**: dentro da parede, longe da porta, 42% do pano livre.
- **Aviso de desempenho**: o pico do quintal passa de 17 para **22 pessoas simultâneas** (23 se contar a fase em que Davi chega). Preciso testar a navegação com isso na 8.6 (P10).

## 8. Pendências e decisões

| # | Pendência | Recomendação |
|---|---|---|
| P13 | A mesa da oferenda F13 (X 14,0) e o altar sob a bandeira (X 9,9) ficam a 4 m um do outro. Duas ofertas separadas? | Manter F13 como oferenda à parte e o altar sob a bandeira; ou trocar o aparador e F13 de lugar (F13 sob a bandeira, aparador mais à direita), o que mexe na planta aprovada. Recomendo manter |
| P14 | **Seis figurantes infantis novos** e a idade dos sete meninos (a tradição fala em até 7 anos; Júnior tem 11) | aprovar os figurantes; decidir idade (`revisar`) |
| P15 | Base da porcentagem da bandeira (pano livre, 42%) | confirmar ou pedir outra |
| P16 | Fase C1 antes da C | aprovar; muda a ordem dos eventos do capítulo |
| P17 | Cultural (`revisar`): prato dos santos, vela, flores, representação dos santos na bandeira, tacho de Nena | revisão antes da arte final |
| — | **Assets da etapa anterior**: não encontrei no projeto nem no ambiente os assets da 8.4 (só o esquema da 8.3 e os assets antigos da casa e da padaria) | me enviar, ou eu os produzo na 8.6 |

Itens de arte necessários (nenhum produzido): bandeira de Cosme e Damião, toalha de chita, pratinhos, bacia, bandeja, copinhos, prato dos santos, vela, vasinho, panelas, tábua, bacias, cesto de temperos, balde, travessas, pilha de pratos, jarras, cuia, tacho, bacia coberta, peças de dominó e **6 sprites infantis** (frente, costas, lados e sentado no chão).

## 9. A 8.6 (construção) — ainda não iniciada

A 8.5 pede aprovar o posicionamento antes de implementar, então parei aqui. Para começar a 8.6 preciso da sua aprovação desta etapa (ou dos ajustes), da resposta às pendências acima e dos assets da 8.4 (ou o ok para produzi-los). A ordem obrigatória da 8.6 (arquitetura → piso → permanentes → mobiliário → caruru → profundidade → colisões → navegação → testes com Lia e NPCs) será seguida.

## 10. Fontes (tradição do caruru dos sete meninos)

- Brasil de Fato, "Festa do Caruru de Cosme e Damião agora é patrimônio imaterial da Bahia" (2024): primeira porção à imagem dos santos, depois sete crianças comem, só então os convidados.
- Portal São Francisco, sobre o dia de São Cosme e Damião: roda de sete meninos, toalha no chão, pratinhos de barro ou bacia, sem talheres; variações atuais.
- Brasil de Fato, "Caruru de Cosme e Damião: tradição, agradecimento e fé" (2018): comer com as mãos; doces também são oferecidos às crianças.
- Correio, "Caruru de obrigação: é possível quebrar a promessa?": o significado do número sete e o ritual com os sete meninos.

## 11. Arquivos
`out/quintal_pos_planta.png`, `out/quintal_pos_vista34_720x270.png`, `out/quintal_pos_vista34_1440x540.png`, `out/quintal_pos_vista34_anotada_1440x540.png`, `out/quintal_pos_mapa.png`, `out/quintal_pos_teste.json`; código em `tools/quintal_pos.py`, `tools/teste_pos.py`, `tools/gerar_pos.py`.
