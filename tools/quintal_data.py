# Fonte única de verdade do projeto espacial do quintal (Etapa 8.3 revisada).
# TUDO aqui está em METROS DO MUNDO:  X para a direita (0..28), Y em profundidade a partir da parede dos fundos (0..8), Z para cima.
# Origem: canto fundo-esquerdo do piso (face interna da parede dos fundos e da lateral esquerda).
# Nada de pixel neste arquivo; pixels só existem nas funções de projeção abaixo (e nas imagens geradas).

W, D = 28.0, 8.0                       # piso: largura x profundidade (m)
PX_X, PX_Y, PX_Z = 24, 16, 24          # projeção 3/4 do jogo: px por metro em X, em Y (profundidade) e em Z (altura)
OX, OY = 24, 124                       # deslocamento do piso no mundo projetado (margem lateral 24 px; fundo do piso em y=124)
MUNDO_PX = (720, 270)                  # tamanho do mundo projetado = 24 + 28*24 + 24 ; 124 + 8*16 = 252 (+18 de borda)
PLANTA_PX_M = 30                       # planta superior: 30 px por metro nos DOIS eixos (vista de cima verdadeira)

def p34(X, Y, Z=0.0):
    """metros do mundo -> pixel do mundo projetado (câmera 3/4 oblíqua, sem cisalhamento em X)"""
    return OX + PX_X * X, OY + PX_Y * Y - PX_Z * Z

def pg(X, Y):
    """metros -> unidade de jogo (px no plano do piso, Z=0): é o que colisão, pontos de parada e navegação usam"""
    return OX + PX_X * X, OY + PX_Y * Y

# ----------------------------------------------------------------------------- objetos
# id, nome, categoria, x, y, w, d, h, colisao, interativo
# categoria: F = estrutural/fixo · M = móvel/deslocável · D = decorativo
# colisao: True (retângulo da base inteira) | False | (dx0,dy0,dx1,dy1) recuos da base
OBJ = [
 # ---- estruturais e fixos
 ('F01', 'Parede da casa de Zefa', 'F', 0.0, -0.30, 11.0, 0.30, 4.0, True, False),
 ('F02', 'Muro dos fundos (divisa)', 'F', 11.0, -0.30, 17.0, 0.30, 2.4, True, False),
 ('F03', 'Muro lateral esquerdo', 'F', -0.30, 0.0, 0.30, 8.0, 2.4, True, False),
 ('F04', 'Muro lateral direito', 'F', 28.0, 0.0, 0.30, 8.0, 2.4, True, False),
 ('F08', 'Fogão a gás 4 bocas', 'F', 3.1, 0.1, 0.9, 0.7, 0.9, True, True),
 ('F09', 'Bancada de preparo', 'F', 4.3, 0.1, 2.5, 0.8, 0.9, True, True),
 ('F10', 'Tanque com torneira', 'F', 0.6, 0.0, 1.0, 0.8, 0.9, True, True),
 ('F11', 'Talha de barro', 'F', 7.0, 0.0, 0.6, 0.6, 1.0, True, True),
 ('F12', 'Aparador de serviço', 'F', 9.8, 0.1, 3.4, 0.9, 0.9, True, True),
 ('F14', 'Tronco da mangueira', 'F', 22.3, 2.4, 0.6, 0.4, 2.8, True, False),      # ø 0,8 m real; colisão só da base (0,6 x 0,4)
 # ---- móveis e deslocáveis
 ('M01', 'Mesa longa', 'M', 11.5, 3.6, 5.0, 1.0, 0.75, True, True),
 ('M02', 'Cadeira fundo 1', 'M', 11.75, 2.7, 0.5, 0.5, 0.9, True, True),
 ('M03', 'Cadeira fundo 2', 'M', 13.05, 2.7, 0.5, 0.5, 0.9, True, True),
 ('M04', 'Cadeira fundo 3', 'M', 14.35, 2.7, 0.5, 0.5, 0.9, True, True),
 ('M05', 'Cadeira fundo 4', 'M', 15.65, 2.7, 0.5, 0.5, 0.9, True, True),
 ('M06', 'Cabeceira oeste', 'M', 10.8, 3.85, 0.5, 0.5, 0.9, True, True),
 ('M07', 'Cabeceira leste', 'M', 16.7, 3.85, 0.5, 0.5, 0.9, True, True),
 ('M08', 'Banco comprido (frente)', 'M', 12.0, 4.7, 3.0, 0.45, 0.45, True, True),
 ('M09', 'Mesinha das crianças', 'M', 17.6, 5.7, 1.8, 0.8, 0.5, True, True),
 ('M10', 'Banquinho crianças 1', 'M', 17.05, 5.75, 0.4, 0.4, 0.3, True, True),
 ('M11', 'Banquinho crianças 2', 'M', 17.05, 6.35, 0.4, 0.4, 0.3, True, True),
 ('M12', 'Banquinho crianças 3', 'M', 19.55, 5.75, 0.4, 0.4, 0.3, True, True),
 ('M13', 'Banquinho crianças 4', 'M', 19.55, 6.35, 0.4, 0.4, 0.3, True, True),
 ('M14', 'Mesa de dominó', 'M', 20.0, 3.8, 1.2, 1.2, 0.75, True, True),
 ('M15', 'Cadeira dominó N', 'M', 20.35, 3.1, 0.5, 0.5, 0.9, True, True),
 ('M16', 'Cadeira dominó S', 'M', 20.35, 5.1, 0.5, 0.5, 0.9, True, True),
 ('M17', 'Cadeira dominó O', 'M', 19.3, 4.25, 0.5, 0.5, 0.9, True, True),
 ('M18', 'Cadeira dominó L', 'M', 21.4, 4.25, 0.5, 0.5, 0.9, True, True),
 ('M20', 'Cadeira de Rita', 'M', 23.8, 2.6, 0.6, 0.6, 1.0, True, True),
 ('M22', 'Lavatório (talha com caneca)', 'M', 10.2, 6.0, 0.5, 0.5, 0.9, True, True),
 ('M27', 'Tabuleiro de Nena (só fase C)', 'M', 17.0, 0.2, 0.9, 0.7, 0.9, True, True),
 # ---- decorativos
 ('D01', 'Vaso em lata (recepção O)', 'D', 0.2, 5.4, 0.4, 0.4, 0.5, True, False),
 ('D02', 'Vaso em lata (recepção L)', 'D', 6.4, 5.6, 0.4, 0.4, 0.5, True, False),
 ('D03', 'Vaso em lata (cozinha)', 'D', 0.2, 4.55, 0.4, 0.4, 0.5, True, False),
 ('D04', 'Vaso em lata (muro)', 'D', 26.8, 0.3, 0.4, 0.4, 0.5, True, False),
]
# aberturas (não colidem; passagem controlada)
OPEN = {
 'soleira':  dict(nome='Soleira / corredor da rua', x0=3.5, x1=5.5, y=8.0, lia=True, npc=True),
 'servico':  dict(nome='Porta de serviço (casa)', x0=8.0, x1=9.2, y=0.0, lia=False, npc=True, w=1.2, h=2.3),
 'portao':   dict(nome='Portão de Rita', x=28.0, y0=3.2, y1=4.4, lia=True, npc=True, w=1.2, h=1.8),
 'janela':   dict(nome='Janela da cozinha', x0=4.8, x1=6.0, y=0.0, z0=1.1, z1=2.1),
}
# puxadinho (cobertura): projeção na planta e geometria 3D
PUX = dict(x0=0.0, x1=7.6, y0=0.0, y1=5.2, z_fundo=3.4, z_frente=2.6)
# mangueira: tronco e copa (elipsoide)
MANGA = dict(tronco=(22.6, 2.6), diam=0.8, h_tronco=2.8, copa_c=(22.6, 2.4, 4.4), copa_r=(3.0, 2.6, 1.6))
# telhado de Rita (casa vizinha, atrás do muro de 2,4 m)
RITA_TELHADO = dict(x0=17.5, x1=27.5, y_beiral=-1.2, z_beiral=3.0, y_cume=-3.2, z_cume=4.2, dano_x0=26.0, dano_x1=27.5)   # dano (lona, telha quebrada, balde) no trecho livre da copa
# zona restrita (oferenda): ninguém para ali, exceto Zefa e Nena
RESTRITA = dict(x0=13.5, y0=0.0, x1=15.7, y1=1.5)
# zonas funcionais (retângulos em metros)
ZONAS = [
 ('Z1 Cozinha', 0.0, 0.0, 7.6, 5.2, '#e9a15b'),
 ('Z2 Serviço', 9.8, 0.0, 13.2, 1.9, '#e8d36a'),
 ('Z3 Mesa', 10.3, 2.4, 17.4, 5.4, '#8fc47a'),
 ('Z3b Crianças', 16.8, 5.5, 20.1, 7.0, '#c9d98a'),
 ('Z4 Convivência (mangueira)', 18.6, 1.0, 27.8, 7.2, '#7aa9d8'),
 ('Z5 Recepção', 0.0, 5.4, 7.6, 8.0, '#b79ad8'),
]
# faixas de circulação preferenciais (custo menor, nunca caminho fixo)
FAIXAS = [
 ('Faixa de trás', 8.0, 1.0, 18.5, 2.6),
 ('Faixa da frente', 0.0, 6.9, 28.0, 8.0),
 ('Eixo da porta de serviço', 7.9, 0.0, 9.3, 7.2),
 ('Corredor da cozinha', 0.0, 1.7, 7.9, 3.0),
]
# ----------------------------------------------------------------------------- personagens
# id, nome, altura(m), raio de corpo para andar (m)
CH = {
 'lia': ('Lia (13)', 1.50, 0.25), 'zefa': ('Dona Zefa', 1.58, 0.27), 'aurea': ('Vó Áurea', 1.60, 0.27), 'raimundo': ('Seu Raimundo', 1.70, 0.27),
 'dandara': ('Dandara', 1.68, 0.27), 'ze': ('Seu Zé', 1.72, 0.27), 'nonato': ('Nonato', 1.78, 0.29), 'bela': ('Dona Bela', 1.60, 0.27),
 'cicera': ('Dona Cícera', 1.58, 0.27), 'junior': ('Júnior', 1.35, 0.20), 'tonho': ('Tonho', 1.72, 0.27), 'nena': ('Dona Nena', 1.62, 0.27),
 'davi': ('Davi', 1.75, 0.26), 'lucia': ('Lúcia', 1.68, 0.26), 'rita': ('Rita', 1.58, 0.26), 'caio': ('Caio (14)', 1.60, 0.23), 'bia': ('Bia (13)', 1.52, 0.22),
}
SIT_BODY = 0.28        # raio do corpo sentado (m); a cadeira/banco já colide
# lugares sentados: id, x, y (centro do corpo sentado), objeto, ponto de aproximação (onde a pessoa para antes de sentar), lado do móvel
SEATS = {
 'mesa_cab_O': (11.05, 4.10, 'M06', (10.0, 4.10)),
 'mesa_cab_L': (16.95, 4.10, 'M07', (18.0, 4.10)),
 'mesa_f1': (12.0, 2.95, 'M02', (12.0, 2.2)), 'mesa_f2': (13.3, 2.95, 'M03', (13.3, 2.2)),
 'mesa_f3': (14.6, 2.95, 'M04', (14.6, 2.2)), 'mesa_f4': (15.9, 2.95, 'M05', (15.9, 2.2)),
 'banco_1': (12.4, 4.92, 'M08', (12.4, 5.9)), 'banco_2': (13.2, 4.92, 'M08', (13.2, 5.9)),
 'banco_3': (14.0, 4.92, 'M08', (14.0, 5.9)), 'banco_4': (14.8, 4.92, 'M08', (14.8, 5.9)),
 'cri_1': (17.25, 5.95, 'M10', (16.4, 5.95)), 'cri_2': (17.25, 6.55, 'M11', (16.4, 6.55)),
 'cri_3': (19.75, 5.95, 'M12', (20.6, 5.95)), 'cri_4': (19.75, 6.55, 'M13', (20.6, 6.55)),
 'dom_N': (20.6, 3.35, 'M15', (20.6, 2.5)), 'dom_S': (20.6, 5.35, 'M16', (20.6, 6.2)),
 'dom_O': (19.55, 4.5, 'M17', (18.7, 4.5)), 'dom_L': (21.65, 4.5, 'M18', (22.3, 4.5)),
 
 'rita': (24.1, 2.9, 'M20', (24.1, 3.8)),
 
 
 
}
# pontos de parada para interagir (x, y, direção do rosto): o corpo fica ao menos 0,45 m do retângulo do objeto
STAND = {
 'F08': (3.55, 1.25, 'up'), 'F09': (5.5, 1.3, 'up'), 'F10': (1.1, 1.2, 'up'), 'F11': (7.3, 1.3, 'up'),
 'F12a': (10.8, 1.55, 'up'), 'F12b': (12.2, 1.55, 'up'), 'M01': (12.65, 3.05, 'down'),
 'M14': (21.9, 3.4, 'left'), 'F14': (22.0, 3.2, 'up'), 'M22': (9.7, 6.25, 'right'),
 'portao': (26.8, 3.8, 'right'), 'telhado': (26.9, 5.7, 'up'),
}
# ----------------------------------------------------------------------------- povoamento por fase (x,y m): corpo em pé ou sentado
FASE = {
 'A': {  # preparo (Lia acabou de chegar)
  'lia': (4.5, 7.5, 'pe'), 'zefa': (3.55, 1.25, 'pe'), 'cicera': (5.5, 1.3, 'pe'), 'nonato': (10.0, 5.6, 'pe'), 'ze': (21.5, 3.3, 'pe'), 'junior': (14.0, 7.2, 'pe'),
 },
 'B': {  # chegada: pico de gente na recepção + Rita no portão
  'lia': (6.0, 7.3, 'pe'), 'zefa': (3.7, 6.5, 'pe'), 'cicera': (5.5, 1.3, 'pe'), 'nonato': (10.2, 5.8, 'pe'), 'ze': (21.5, 3.3, 'pe'), 'junior': (14.0, 7.2, 'pe'),
  'aurea': (4.1, 7.4, 'pe'), 'raimundo': (5.1, 7.5, 'pe'), 'dandara': (3.2, 7.4, 'pe'), 'bela': (4.9, 6.4, 'pe'), 'tonho': (6.9, 6.9, 'pe'),
  'caio': (8.6, 7.4, 'pe'), 'bia': (7.7, 7.5, 'pe'), 'rita': (27.0, 3.8, 'pe'),
 },
 'C': {  # mesa: pico
  'zefa': ('mesa_cab_L',), 'raimundo': ('mesa_cab_O',), 'aurea': ('mesa_f1',), 'ze': ('mesa_f2',), 'bela': ('mesa_f3',), 'dandara': ('mesa_f4',),
  'nonato': ('banco_1',), 'tonho': ('banco_2',), 'lia': ('banco_3',), 'lucia': ('banco_4',),
  'junior': ('cri_1',), 'caio': ('cri_3',), 'bia': ('cri_4',), 'cicera': (11.8, 1.55, 'pe'), 'nena': (17.5, 1.3, 'pe'), 'rita': ('rita',),
 },
 'D': {  # depois da mesa
  'ze': ('dom_N',), 'nonato': ('dom_O',), 'raimundo': ('dom_S',), 'tonho': ('dom_L',),
  'aurea': (24.2, 4.9, 'pe'), 'zefa': (25.0, 4.9, 'pe'), 'dandara': (25.8, 4.9, 'pe'), 'rita': ('rita',), 'davi': (25.6, 6.9, 'pe'),
  'bela': (18.4, 3.0, 'pe'), 'cicera': (16.0, 1.6, 'pe'), 'junior': (18.6, 7.2, 'pe'), 'caio': ('cri_1',), 'bia': ('cri_2',),
  'nena': (17.5, 1.3, 'pe'), 'lucia': (5.3, 7.4, 'pe'), 'lia': (14.0, 7.2, 'pe'),
 },
}
# entradas (onde nascem NPCs que chegam)
ENTRADAS = {'soleira': (4.5, 7.7), 'portao': (27.7, 3.8), 'servico': (8.6, 0.5)}
# âncoras de rota (para testar caminhos autônomos; o jogo usa A* na grade, não segue linhas)
ANCORAS = {
 'soleira': (4.5, 7.5), 'recepcao': (4.0, 6.6), 'cozinha_trempe': (3.55, 1.25), 'cozinha_bancada': (5.5, 1.3), 'servico_aparador': (11.5, 1.55),
 'porta_servico': (8.6, 0.6), 'mesa_oeste': (10.0, 4.1), 'mesa_frente': (13.5, 5.9), 'mesa_leste': (18.0, 4.1), 'criancas': (16.4, 5.95),
 'dominó': (22.5, 4.5), 'cadeira_rita': (24.1, 3.8), 'portao': (26.8, 3.8), 'tabuleiro': (17.5, 1.3),
}
