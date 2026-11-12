"""Biblioteca de objetos da padaria (Etapa 3). Cada asset: desenho 3/4 oblíquo (1 m = 24 px; piso 16 px/m), classificação,
dimensão, ponto de apoio (âncora = centro do contato com o chão), colisão, interação. Saída: folhas por categoria + catalog.json + scene_padaria.json."""
import json, math, random, os
from PIL import Image
from pxl import *
from facade import CAL, STONE, BRICK, IRON, MOSS, TELHA, GLASS
from interior import TIMB, WOOD, LEAF, STRAW, BREAD, CLAY, RED, SACK, VOID, FILT, ell, fy, YB, X0, X1, YF

ALU = ramp(210, 0.07, (0.28, 0.40, 0.54, 0.68, 0.82))
ENAM = ramp(200, 0.40, (0.20, 0.30, 0.42, 0.54, 0.66))
OUT = '../assets/objects/'
CELL = (96, 96); AXY = (48, 84)            # tela de desenho e âncora padrão (pés)

def new(): return C(CELL[0], CELL[1])
def shadow(c, x, y, w, a=70):
    for k, al in enumerate((a + 10, a - 20)): c.hline(x - w // 2 - 1 + k, y + k - 1, w + 2 - 2 * k, (18, 10, 28, al))

# ------------------------------------------------------------------ desenhos
def d_banco(c, x, y):
    w = 36; x0 = x - w // 2; shadow(c, x, y, w)
    c.rect(x0 + 1, y - 29, w - 2, 11, TIMB[2]); c.hline(x0 + 1, y - 29, w - 2, TIMB[4]); c.vline(x0 + 1, y - 29, 11, TIMB[3]); c.vline(x0 + w - 2, y - 29, 11, TIMB[1])
    for i in range(1, 6): c.vline(x0 + 1 + i * 6, y - 28, 10, TIMB[0])                           # ripas do encosto
    for lx in (x0 + 2, x0 + w - 5): c.rect(lx, y - 9, 3, 9, TIMB[2]); c.vline(lx, y - 9, 9, TIMB[3]); c.vline(lx + 2, y - 9, 9, TIMB[1])
    c.rect(x0 + 5, y - 5, w - 10, 2, TIMB[1])
    c.rect(x0, y - 12, w, 3, TIMB[2]); c.hline(x0, y - 10, w, TIMB[1])
    c.rect(x0, y - 18, w, 6, TIMB[3]); c.hline(x0, y - 18, w, TIMB[4]); c.hline(x0 + 1, y - 15, w - 2, TIMB[2]); c.hline(x0, y - 12, w, TIMB[4])

def d_fogao(c, x, y):
    w = 20; x0 = x - 10; shadow(c, x, y, w + 2)
    c.rect(x0 + 1, y - 3, 3, 3, IRON[1]); c.rect(x0 + w - 4, y - 3, 3, 3, IRON[1])
    c.rect(x0, y - 35, w, 5, SACK[2]); c.hline(x0, y - 35, w, SACK[4]); c.hline(x0, y - 31, w, SACK[1])      # espelho traseiro
    c.rect(x0, y - 30, w, 9, IRON[2]); c.hline(x0, y - 30, w, IRON[3]); c.vline(x0, y - 30, 9, IRON[3]); c.vline(x0 + w - 1, y - 30, 9, IRON[1]) # tampo (0,6 m de fundo)
    for bx, by in ((x0 + 5, y - 27), (x0 + 15, y - 27), (x0 + 5, y - 24), (x0 + 15, y - 24)):
        ell(c, bx, by, 3.4, 1.6, IRON[0]); ell(c, bx, by, 2.2, 1.0, IRON[3]); c.pset(bx, by, IRON[0])
    c.rect(x0, y - 21, w, 18, SACK[3]); c.vline(x0, y - 21, 18, SACK[4]); c.vline(x0 + w - 1, y - 21, 18, SACK[1]); c.hline(x0, y - 21, w, SACK[4]); c.hline(x0, y - 4, w, SACK[1])
    for i in range(4): c.rect(x0 + 3 + i * 4, y - 20, 2, 2, IRON[1]); c.pset(x0 + 3 + i * 4, y - 20, IRON[4])
    c.rect(x0 + 2, y - 16, w - 4, 11, SACK[2]); c.rect(x0 + 4, y - 13, w - 8, 6, IRON[0]); c.hline(x0 + 4, y - 13, w - 8, IRON[1]); c.pset(x0 + 5, y - 12, IRON[3]); c.pset(x0 + 6, y - 11, IRON[2])
    c.hline(x0 + 3, y - 17, w - 6, IRON[4])

def d_panela(c, x, y):          # y = base do fundo
    c.rect(x - 4, y - 6, 9, 6, ALU[2]); c.vline(x - 4, y - 6, 6, ALU[4]); c.vline(x + 4, y - 6, 6, ALU[1]); c.hline(x - 4, y - 1, 9, ALU[1])
    c.rect(x - 5, y - 7, 11, 2, ALU[3]); c.hline(x - 5, y - 7, 11, ALU[4]); c.hline(x - 4, y - 8, 9, ALU[3]); c.pset(x, y - 9, IRON[3]); c.pset(x - 1, y - 9, ALU[3])
    c.rect(x + 6, y - 6, 3, 1, IRON[1]); c.rect(x - 8, y - 6, 3, 1, IRON[1])

def d_cafeteira(c, x, y):
    c.poly([(x - 3, y), (x + 3, y), (x + 2, y - 8), (x - 2, y - 8)], ENAM[2]); c.vline(x - 2, y - 7, 6, ENAM[4]); c.vline(x + 2, y - 7, 6, ENAM[1])
    c.hline(x - 3, y - 9, 7, ENAM[3]); c.pset(x, y - 10, IRON[3]); c.pset(x - 4, y - 8, ENAM[3]); c.pset(x - 5, y - 9, ENAM[3])
    c.vline(x + 4, y - 7, 5, IRON[1]); c.pset(x + 3, y - 7, IRON[1]); c.pset(x + 3, y - 3, IRON[1]); c.hline(x - 2, y - 1, 5, ENAM[0])

def d_planta(c, x, y):
    rng = random.Random(8); shadow(c, x, y, 14)
    c.rect(x - 6, y - 9, 12, 9, CLAY[2]); c.vline(x - 6, y - 9, 9, CLAY[4]); c.vline(x + 5, y - 9, 9, CLAY[1]); c.hline(x - 7, y - 11, 14, CLAY[3]); c.hline(x - 7, y - 12, 14, CLAY[4]); c.hline(x - 5, y - 1, 10, CLAY[0])
    c.hline(x - 6, y - 5, 12, CLAY[1])
    for k in range(11):
        a = math.radians(-80 + k * 16 + rng.uniform(-5, 5)); L = rng.randint(14, 26); bx, by = x, y - 11
        tx, ty = bx + math.sin(a) * L, by - math.cos(a) * L * 0.9
        mx, my = (bx + tx) / 2 + math.cos(a) * 4, (by + ty) / 2 + math.sin(a) * 2
        col = LEAF[2 + (k % 3) % 2]
        c.poly([(bx - 1, by), (mx - 2, my), (tx, ty), (mx + 2, my + 1), (bx + 1, by)], col)
        c.line(bx, by, tx, ty, LEAF[4] if k % 2 else LEAF[3])
    c.shade(x - 9, y - 13, 18, 3, SH1)

def d_quadro(c, x, y):          # âncora = base central; 20x15 px (0,8 x 0,6 m)
    x0 = x - 10; t = y - 15
    c.rect(x0, t, 20, 15, TIMB[1]); c.hline(x0, t, 20, TIMB[3]); c.vline(x0, t, 15, TIMB[3]); c.hline(x0, y - 1, 20, TIMB[0])
    c.rect(x0 + 2, t + 2, 16, 11, (90, 140, 190))
    for j in range(11): c.hline(x0 + 2, t + 2 + j, 16, mix((120, 175, 215), (210, 210, 190), j / 11.0))
    c.poly([(x0 + 2, t + 13), (x0 + 6, t + 8), (x0 + 11, t + 10), (x0 + 18, t + 7), (x0 + 18, t + 13)], LEAF[2])            # colina
    c.rect(x0 + 9, t + 5, 5, 4, CAL[4]); c.rect(x0 + 8, t + 4, 2, 5, CAL[3]); c.rect(x0 + 13, t + 4, 2, 5, CAL[3]); c.pset(x0 + 11, t + 6, IRON[1])
    for i, col in enumerate(((60, 150, 90), (230, 200, 70), (90, 140, 210))): c.pset(x0 + 3 + i, t + 3, col)                  # fitinhas

def d_fotos(c, x, y):           # três retratos emoldurados, em pequenos tamanhos diferentes
    sets = [(-9, -12, 7, 10), (-1, -14, 8, 11), (8, -11, 6, 9)]
    for dx, dy, w, h in sets:
        x0, t = x + dx - w // 2, y + dy
        c.rect(x0, t, w, h, TIMB[2] if w != 8 else CAL[4]); c.hline(x0, t, w, TIMB[4]); c.rect(x0 + 1, t + 1, w - 2, h - 2, (196, 170, 128))
        c.rect(x0 + 1, t + h - 4, w - 2, 3, (120, 92, 72)); c.rect(x0 + w // 2 - 1, t + 2, 2, 2, (70, 44, 34)); c.hline(x0 + 1, t + 1, w - 2, (216, 192, 150))
    c.hline(x - 6, y - 14, 1, TIMB[0])

def d_prateleira(c, x, y):      # 34 px de largura; tábua + mãos-francesas; louças e utensílios
    x0 = x - 17
    c.rect(x0, y - 3, 34, 3, TIMB[2]); c.hline(x0, y - 3, 34, TIMB[4]); c.hline(x0, y - 1, 34, TIMB[1])
    for bx in (x0 + 4, x0 + 28): c.poly([(bx, y), (bx + 3, y), (bx, y + 5)], TIMB[1])
    for k in range(4): ell(c, x0 + 5, y - 4 - k, 4, 1.2, CAL[4 - (k % 2)]); c.hline(x0 + 2, y - 4 - k, 6, CAL[2])      # pilha de pratos
    for k in range(3):
        mx = x0 + 13 + k * 5; c.rect(mx, y - 7, 4, 4, ENAM[2]); c.vline(mx, y - 7, 4, ENAM[4]); c.hline(mx, y - 7, 4, ENAM[4]); c.hline(mx, y - 4, 4, ENAM[0]); c.pset(mx + 4, y - 6, ENAM[3])
    c.rect(x0 + 28, y - 8, 5, 5, CLAY[2]); c.hline(x0 + 28, y - 8, 5, CLAY[4])                                           # pote com utensílios
    for k, col in enumerate((TIMB[3], STRAW[3], TIMB[4])): c.vline(x0 + 29 + k, y - 12, 4, col)

def d_bandeja(c, x, y):
    ell(c, x, y - 2, 9, 3.4, ALU[2]); ell(c, x, y - 3, 8, 2.8, ALU[3]); c.hline(x - 7, y - 4, 14, ALU[4])
    for k in range(5): px = x - 6 + k * 3; ell(c, px + 1, y - 5, 2.4, 1.8, BREAD[3]); c.pset(px, y - 6, BREAD[4]); c.pset(px + 1, y - 4, BREAD[1])

def d_chama(c, x, y, f):        # chamas azuis do bico (2 quadros); x,y = centro do queimador
    for dx in (-3, 3):
        h = 2 if (f + (dx > 0)) % 2 else 1
        c.pset(x + dx, y + 1, (70, 120, 235)); c.pset(x + dx, y, (190, 225, 255) if h == 2 else (70, 120, 235))
        if h == 2: c.pset(x + dx, y - 1, (70, 120, 235))
def d_vapor(c, x, y, f):
    for k in range(4):
        px = x + (1 if (k + f) % 2 else -1) * (k % 2); c.pset(px, y - k * 2 - f, (236, 236, 240, 150 - k * 30)); c.pset(px + 1, y - k * 2 - f - 1, (236, 236, 240, 100 - k * 20))

def d_gaveta_aberta(c, x, y):   # sobreposta à frente do balcão: gaveta puxada ~3 px, com papéis, lápis e caderneta
    x0 = x - 16
    c.rect(x0, y - 18, 32, 4, VOID); c.rect(x0 + 2, y - 17, 8, 3, CAL[4]); c.line(x0 + 3, y - 16, x0 + 9, y - 16, CAL[2]); c.rect(x0 + 12, y - 17, 7, 3, RED[2]); c.hline(x0 + 12, y - 17, 7, RED[4])
    c.line(x0 + 21, y - 15, x0 + 29, y - 17, STRAW[3])
    c.rect(x0, y - 14, 32, 14, WOOD[1]); c.hline(x0, y - 14, 32, WOOD[3]); c.vline(x0, y - 14, 14, WOOD[0]); c.hline(x0, y - 1, 32, WOOD[0]); c.vline(x0 + 31, y - 14, 14, WOOD[3])
    c.rect(x0 + 13, y - 9, 5, 3, IRON[4]); c.hline(x0 + 13, y - 6, 5, IRON[1])
    c.hline(x0, y, 32, (20, 12, 30, 110)); c.hline(x0 + 1, y + 1, 30, (20, 12, 30, 70))

def d_porta_aberta(c, x, y):    # vão da escada com a folha aberta para dentro e degraus subindo
    x0 = x - 11
    c.rect(x0, y - 54, 22, 54, (28, 22, 30))
    for k in range(7): c.rect(x0 + 4, y - 4 - k * 5, 18, 4, mix((88, 70, 62), (28, 22, 30), k / 8.0)); c.hline(x0 + 4, y - 4 - k * 5, 18, mix((150, 120, 100), (40, 30, 36), k / 8.0))
    c.rect(x0, y - 54, 5, 54, WOOD[1]); c.vline(x0, y - 54, 54, WOOD[3]); c.vline(x0 + 4, y - 54, 54, WOOD[0]); c.rect(x0 + 1, y - 46, 3, 16, WOOD[2]); c.rect(x0 + 1, y - 26, 3, 16, WOOD[2])
    c.pset(x0 + 3, y - 30, IRON[4])
    c.rect(x0 + 5, y - 54, 17, 3, (40, 30, 36))

def d_vela(c, x, y, f):          # chama da vela do nicho (2 quadros), x,y = ponta do pavio
    c.pset(x, y, (255, 214, 120)); c.pset(x, y - 1, (255, 170, 70) if f else (255, 200, 100)); c.pset(x, y - 2, (240, 120, 50)) if f else None
    c.pset(x - 1, y, (255, 190, 90, 120)); c.pset(x + 1, y, (255, 190, 90, 120))
def d_brasa(c, x, y, f):         # brasa na boca do forno (2 quadros), x = centro, y = piso da boca
    rng = random.Random(4 + f)
    for i in range(-12, 13):
        if rng.random() < 0.55: c.pset(x + i, y - rng.randint(0, 2), [(150, 40, 24), (214, 86, 34), (246, 150, 56)][rng.randint(0, 2)])
    for i in range(-8, 9, 4): c.pset(x + i + f, y - 3 - (i % 3), (255, 200, 90, 200))
    c.rect(x - 14, y - 6, 28, 1, (255, 120, 40, 40))

# ------------------------------------------------------------------ catálogo
# classe: DECORATIVO | EXAMINAVEL | UTILIZAVEL | FUNCIONAL ; tipo: nenhum | examinar | usar | alternar | funcao
def A(id, nome, cat, classe, tipo, draw=None, size_m=(0, 0, 0), collide=None, stand=None, face='up', anim='interact', layer='floor', area=None, states=None, supports=None, zoom=2, desc='', frames=1, png=None, baked=False):
    return dict(id=id, nome=nome, categoria=cat, classe=classe, interacao=tipo, draw=draw, size_m=size_m, collide=collide, stand=stand, face=face, anim=anim, layer=layer,
                area=area, states=states, supports=supports, zoom=zoom, desc=desc, frames=frames, png=png, baked=baked)

ASSETS = [
 # --- mobiliário
 A('balcao', 'Balcão e vitrine', 'mobiliario', 'FUNCIONAL', 'funcao', png='prop_counter', size_m=(7.7, 0.8, 1.0), face='up', zoom=1, desc='Balcão de atendimento com vitrine, caixa e caderneta.'),
 A('mesa_redonda', 'Mesa redonda', 'mobiliario', 'UTILIZAVEL', 'usar', png='prop_table_a', size_m=(1.0, 1.0, 0.75), desc='Mesa redonda de madeira para dois a quatro lugares.'),
 A('mesa_toalha', 'Mesa com toalha xadrez', 'mobiliario', 'UTILIZAVEL', 'usar', png='prop_table_b', size_m=(1.0, 1.0, 0.75), desc='Mesa redonda com toalha xadrez vermelha.'),
 A('cadeira_frente', 'Cadeira (de frente)', 'mobiliario', 'UTILIZAVEL', 'usar', png='prop_chair_a_back', size_m=(0.42, 0.42, 0.95)),
 A('cadeira_frente_b', 'Cadeira (de frente, mesa 2)', 'mobiliario', 'UTILIZAVEL', 'usar', png='prop_chair_b_back', size_m=(0.42, 0.42, 0.95)),
 A('cadeira_perfil_e_b', 'Cadeira (perfil esquerdo, mesa 2)', 'mobiliario', 'UTILIZAVEL', 'usar', png='prop_chair_b_l', size_m=(0.42, 0.42, 0.95)),
 A('cadeira_costas', 'Cadeira (de costas)', 'mobiliario', 'UTILIZAVEL', 'usar', png='prop_chair_b_f', size_m=(0.42, 0.42, 0.95)),
 A('cadeira_perfil_e', 'Cadeira (perfil esquerdo)', 'mobiliario', 'UTILIZAVEL', 'usar', png='prop_chair_a_l', size_m=(0.42, 0.42, 0.95)),
 A('cadeira_perfil_d', 'Cadeira (perfil direito)', 'mobiliario', 'UTILIZAVEL', 'usar', png='prop_chair_a_r', size_m=(0.42, 0.42, 0.95)),
 A('aparador', 'Aparador do filtro', 'mobiliario', 'EXAMINAVEL', 'examinar', png='prop_aparador', size_m=(1.1, 0.9, 1.2), zoom=2, desc='Aparador de madeira que apoia o filtro de barro.'),
 A('banco_madeira', 'Banco de madeira com encosto', 'mobiliario', 'UTILIZAVEL', 'usar', draw=d_banco, size_m=(1.5, 0.4, 1.2), collide=[-18, -6, 18, 0], stand=[0, 9], face='up', anim='interact', desc='Banco comprido de madeira, encostado na parede.'),
 A('prateleira_louca', 'Prateleira de louças', 'mobiliario', 'DECORATIVO', 'nenhum', draw=d_prateleira, size_m=(1.4, 0.2, 0.35), layer='wall', desc='Prateleira de parede com pratos, canecas e utensílios.'),
 # --- equipamentos
 A('filtro_barro', 'Filtro de barro', 'equipamentos', 'UTILIZAVEL', 'usar', png='prop_filter', size_m=(0.45, 0.45, 1.0), zoom=2, desc='Filtro de barro sobre suporte de madeira.'),
 A('fogao', 'Fogão de 4 bocas', 'equipamentos', 'FUNCIONAL', 'alternar', draw=d_fogao, size_m=(0.8, 0.6, 1.2), collide=[-10, -9, 10, 0], stand=[0, 8], face='up', anim='interact',
   states=['desligado', 'ligado'], supports=[dict(nome='boca_esq', dx=-5, dy=-28), dict(nome='boca_dir', dx=5, dy=-28)], desc='Fogão a gás de quatro bocas, com forno. (Reservado: casa do seu Raimundo.)'),
 A('panela', 'Panela de alumínio', 'equipamentos', 'DECORATIVO', 'nenhum', draw=d_panela, size_m=(0.28, 0.28, 0.20), layer='on', desc='Panela média de alumínio.'),
 A('cafeteira', 'Cafeteira esmaltada', 'equipamentos', 'DECORATIVO', 'nenhum', draw=d_cafeteira, size_m=(0.20, 0.2, 0.30), layer='on'),
 A('bandeja_paes', 'Bandeja de pães', 'equipamentos', 'UTILIZAVEL', 'usar', draw=d_bandeja, size_m=(0.5, 0.35, 0.12), layer='on', desc='Bandeja metálica com pães do dia.'),
 A('chama_fogao', 'Chama do fogão', 'equipamentos', 'DECORATIVO', 'nenhum', draw=lambda c, x, y: d_chama(c, x, y, 0), frames=2, layer='on'),
 A('vapor_panela', 'Vapor da panela', 'equipamentos', 'DECORATIVO', 'nenhum', draw=lambda c, x, y: d_vapor(c, x, y, 0), frames=2, layer='on'),
 # --- decorativos
 A('quadro_bonfim', 'Quadro do Bonfim', 'decorativos', 'EXAMINAVEL', 'examinar', draw=d_quadro, size_m=(0.8, 0.05, 0.6), layer='wall', zoom=3, desc='Quadro com a colina da igreja e fitinhas coloridas.'),
 A('fotografias', 'Fotografias emolduradas', 'decorativos', 'EXAMINAVEL', 'examinar', draw=d_fotos, size_m=(1.0, 0.05, 0.5), layer='wall', zoom=3, desc='Três retratos antigos em molduras pequenas.'),
 A('planta_vaso', 'Vaso de folhagem', 'decorativos', 'DECORATIVO', 'nenhum', draw=d_planta, size_m=(0.8, 0.4, 1.2), collide=[-6, -4, 6, 0], desc='Folhagem em vaso de barro.'),
 A('vela_altar', 'Vela do nicho acesa', 'decorativos', 'DECORATIVO', 'nenhum', draw=lambda c, x, y: d_vela(c, x, y, 0), frames=2, layer='wall'),
 A('brasa_forno', 'Brasa do forno', 'decorativos', 'DECORATIVO', 'nenhum', draw=lambda c, x, y: d_brasa(c, x, y, 0), frames=2, layer='wall'),
 # --- interativos (estados)
 A('gaveta_balcao_aberta', 'Gaveta do balcão (aberta)', 'interativos', 'EXAMINAVEL', 'alternar', draw=d_gaveta_aberta, size_m=(1.0, 0.5, 0.5), layer='front', states=['fechada', 'aberta'], desc='Gaveta com papéis, lápis e um caderno.'),
 A('porta_escada_aberta', 'Porta da escada (aberta)', 'interativos', 'UTILIZAVEL', 'alternar', draw=d_porta_aberta, size_m=(0.9, 0.1, 2.2), layer='wall', states=['fechada', 'aberta'], desc='Porta que sobe para a casa da Vó.'),
]
# fixtures embutidos no cenário-base (sem sprite próprio; só colisão/interação/inspeção)
FIXTURES = [
 dict(id='forno_lenha', nome='Forno de lenha', categoria='equipamentos', classe='FUNCIONAL', interacao='funcao', rect=[118, 90, 90, 62], collide=[118, 132, 208, 152], stand=[160, 0], face='up', anim='interact_high', zoom=2, desc='Forno de alvenaria com chaminé; fica atrás do balcão.', stand_abs=[190, 160]),
 dict(id='lenha', nome='Pilha de lenha', categoria='equipamentos', classe='DECORATIVO', interacao='nenhum', rect=[204, 130, 22, 18], collide=[204, 132, 226, 147]),
 dict(id='bancada', nome='Bancada de trabalho', categoria='mobiliario', classe='UTILIZAVEL', interacao='usar', rect=[222, 100, 82, 50], collide=[222, 132, 304, 149], stand_abs=[262, 154], face='up', anim='interact', zoom=2, desc='Bancada onde a massa é aberta; janela do quintal acima.'),
 dict(id='estante', nome='Estante', categoria='mobiliario', classe='EXAMINAVEL', interacao='examinar', rect=[307, 67, 40, 66], collide=[306, 132, 348, 143], stand_abs=[326, 152], face='up', anim='interact_high', zoom=2, desc='Estante com rádio, potes, latas e cestos.'),
 dict(id='altar_sao_jorge', nome='Altar de São Jorge', categoria='decorativos', classe='EXAMINAVEL', interacao='examinar', rect=[348, 46, 31, 54], stand_abs=[364, 142], face='up', anim='interact_high', zoom=2, desc='Nicho com a imagem do santo, vela, copo d\'água e flores.'),
 dict(id='lousa_fiado', nome='Lousa do fiado', categoria='decorativos', classe='EXAMINAVEL', interacao='examinar', rect=[206, 56, 27, 29], stand_abs=[216, 158], face='up', anim='interact_high', zoom=2, desc='Lousa do cardápio com o aviso do fiado.'),
 dict(id='calendario', nome='Calendário', categoria='decorativos', classe='EXAMINAVEL', interacao='examinar', rect=[282, 70, 16, 21], stand_abs=[298, 154], face='up', anim='interact_high', zoom=3, desc='Calendário de parede.'),
 dict(id='radio', nome='Rádio de pilha', categoria='decorativos', classe='EXAMINAVEL', interacao='examinar', rect=[312, 76, 14, 11], stand_abs=[326, 152], face='up', anim='interact_high', zoom=3, desc='Rádio de pilha na estante.'),
 dict(id='caderneta', nome='Caderneta do fiado', categoria='decorativos', classe='EXAMINAVEL', interacao='examinar', rect=[231, 153, 11, 6], stand_abs=[236, 194], face='up', anim='interact', zoom=3, desc='Caderneta de capa vermelha, sobre o balcão.'),
 dict(id='caixa', nome='Caixa registradora', categoria='equipamentos', classe='EXAMINAVEL', interacao='examinar', rect=[206, 143, 22, 10], stand_abs=[217, 194], face='up', anim='interact', zoom=3, desc='Caixa registradora de teclas.'),
 dict(id='vitrine', nome='Vitrine de pães e bolos', categoria='equipamentos', classe='EXAMINAVEL', interacao='examinar', rect=[88, 131, 64, 26], stand_abs=[120, 194], face='up', anim='interact', zoom=2, desc='Vitrine de vidro com pães e bolos do dia.'),
 dict(id='janela_quintal', nome='Janela do quintal', categoria='decorativos', classe='EXAMINAVEL', interacao='examinar', rect=[232, 58, 62, 46], stand_abs=[262, 154], face='up', anim='interact_high', zoom=2, desc='Janela com vista para as folhagens do quintal.'),
]

def pack(items, w=512):
    """empacota sprites em prateleiras com 2 px de espaçamento; devolve (imagem, {chave:(x,y,w,h)})"""
    x = y = 2; rowh = 0; pos = {}
    for key, im in items:
        if x + im.width + 2 > w: x = 2; y += rowh + 2; rowh = 0
        pos[key] = (x, y, im.width, im.height); x += im.width + 2; rowh = max(rowh, im.height)
    sheet = Image.new('RGBA', (w, y + rowh + 2), (0, 0, 0, 0))
    for key, im in items: sheet.alpha_composite(im, pos[key][:2])
    return sheet, pos

def render_asset(a):
    """-> lista de (chave, Image recortada, ancora(x,y) dentro do recorte)"""
    out = []
    if a['png']:
        im = Image.open(f"../assets/{a['png']}.png"); out.append((a['id'], im, None)); return out
    for f in range(a['frames']):
        c = new(); d = a['draw']
        if a['id'] == 'chama_fogao': d_chama(c, AXY[0], AXY[1], f)
        elif a['id'] == 'vapor_panela': d_vapor(c, AXY[0], AXY[1], f)
        elif a['id'] == 'vela_altar': d_vela(c, AXY[0], AXY[1], f)
        elif a['id'] == 'brasa_forno': d_brasa(c, AXY[0], AXY[1], f)
        else: d(c, *AXY)
        bb = c.im.getbbox(); out.append((a['id'] + (f'#{f}' if a['frames'] > 1 else ''), c.im.crop(bb), (AXY[0] - bb[0], AXY[1] - bb[1])))
    return out

# ------------------------------------------------------------------ cena: padaria
# (fogão, panela, cafeteira, chama e vapor ficam na biblioteca, reservados para a casa do seu Raimundo; não são colocados na padaria)
# x,y = ponto de apoio no chão (centro do contato), em coordenadas de tela do interior. 'sobre' = apoiado em outro objeto (offset de suporte)
SCENE = [
 dict(inst='banco_altar', asset='banco_madeira', x=364, y=150),
 dict(inst='planta_canto', asset='planta_vaso', x=398, y=172),
 dict(inst='quadro_1', asset='quadro_bonfim', x=326, y=62, stand_abs=[326, 152], anim='interact_high'),
 dict(inst='fotos_1', asset='fotografias', x=395, y=66, stand_abs=[395, 143], anim='interact_high'),
 dict(inst='prateleira_1', asset='prateleira_louca', x=248, y=54),
 dict(inst='vela_1', asset='vela_altar', x=356, y=85, visivel_se=['altar_vela', 1]),
 dict(inst='brasa_1', asset='brasa_forno', x=163, y=139, visivel_se=['forno_aceso', 1]),
 dict(inst='gaveta_1', asset='gaveta_balcao_aberta', x=202, y=181, estado_de=None, alvo='balcao'),
 dict(inst='porta_escada_1', asset='porta_escada_aberta', x=393, y=127, estado_de=None),
]

def build():
    cats = {}; catalog = {}
    for a in ASSETS:
        for key, im, anc in render_asset(a):
            cats.setdefault(a['categoria'], []).append((key, im, anc, a))
    sheets = {}
    for cat, lst in cats.items():
        sheet, pos = pack([(k, im) for k, im, _, _ in lst])
        sheet.save(OUT + f'{cat}.png'); sheets[cat] = (sheet.size, pos)
    # propriedades do layout existente (solid/âncora) para os props já aprovados na Etapa 1
    L = json.load(open('../assets/layout.json')); lp = {p['name']: p for p in L['props']}; solids = {tuple(s) for s in L['solids']}
    names = {'balcao': 'counter', 'mesa_redonda': 'table_a', 'mesa_toalha': 'table_b', 'cadeira_frente': 'chair_a_back', 'cadeira_costas': 'chair_b_f',
             'cadeira_perfil_e': 'chair_a_l', 'cadeira_perfil_d': 'chair_a_r', 'aparador': 'aparador', 'filtro_barro': None}
    entries = []
    for cat, lst in cats.items():
        for key, im, anc, a in lst:
            e = {k: a[k] for k in ('id', 'nome', 'categoria', 'classe', 'interacao', 'size_m', 'layer', 'states', 'supports', 'zoom', 'desc', 'frames', 'anim', 'face') if k in a}
            e.update(sprite=key, folha=f'objects/{cat}.png', rect=list(sheets[cat][1][key]), perspectiva='3/4 interior' if True else '', dim_px=[im.width, im.height],
                     ancora=list(anc) if anc else None, collide=a['collide'], stand=a['stand'])
            entries.append(e)
    json.dump(dict(unidade='1 m = 24 px (altura); piso 16 px/m (profundidade); âncora = ponto de apoio no chão', camera='3/4 oblíqua', classes=['DECORATIVO', 'EXAMINAVEL', 'UTILIZAVEL', 'FUNCIONAL'],
                   interacoes=['nenhum', 'examinar', 'usar', 'alternar', 'funcao'], camadas=['wall', 'floor', 'on', 'front'], assets=entries, fixtures=FIXTURES),
              open(OUT + 'catalog.json', 'w'), indent=1, ensure_ascii=False)
    return entries



LEGACY = {'counter': 'balcao', 'table_a': 'mesa_redonda', 'table_b': 'mesa_toalha', 'chair_a_back': 'cadeira_frente', 'chair_b_back': 'cadeira_frente_b',
          'chair_b_f': 'cadeira_costas', 'chair_a_l': 'cadeira_perfil_e', 'chair_b_l': 'cadeira_perfil_e_b', 'chair_a_r': 'cadeira_perfil_d', 'aparador': 'aparador'}
# interações dos itens aprovados na Etapa 1: id da instância -> (ponto onde Lia para, olhar, anim, rect de clique)
LEGACY_INT = {
 'aparador': dict(stand=[114, 222], face='left', rect=[75, 176, 24, 40], extra='filtro_barro'),
 'table_a': dict(stand=[312, 207], face='up'), 'table_b': dict(stand=[396, 214], face='left'),
 'chair_a_l': dict(stand=[278, 201], face='right'), 'chair_a_r': dict(stand=[346, 201], face='left'),
}

def build_scene():
    cat = json.load(open(OUT + 'catalog.json')); by = {}
    for e in cat['assets']: by.setdefault(e['id'], []).append(e)
    L = json.load(open('../assets/layout.json')); solids = L['solids'][4:]
    inst = []; inter = []; blocks = []
    for p, sol in zip(L['props'], solids):                                     # props aprovados (posição herdada)
        aid = LEGACY[p['name']]; e = by[aid][0]; w = e['dim_px'][0]
        inst.append(dict(inst=p['name'], asset=aid, sprite=e['sprite'], sx=p['x'], sy=p['y'], base=p['base'], layer='floor', collide=sol))
        li = LEGACY_INT.get(p['name'])
        cls = e['classe']
        if li:
            aid2 = li.get('extra', aid); e2 = by[aid2][0]
            inter.append(dict(id=p['name'], asset=aid2, nome=e2['nome'], classe=e2['classe'], tipo=e2['interacao'], rect=li.get('rect', [p['x'], p['y'], w, e['dim_px'][1]]),
                              stand=li['stand'], face=li['face'], anim='interact', zoom=e2['zoom'], desc=e2['desc']))
    placed = {}
    for s in SCENE:
        e = by[s['asset']][0]; a = next(x for x in ASSETS if x['id'] == s['asset'])
        if 'sobre' in s:
            host = placed[s['sobre']]; sup = next(q for q in by[host['asset']][0]['supports'] if q['nome'] == s['suporte'])
            ox, oy = s.get('off', [0, 0]); x, y = host['x'] + sup['dx'] + ox, host['y'] + sup['dy'] + oy; sort = host['y'] + 0.2
        else:
            x, y = s['x'], s['y']; sort = y if a['layer'] != 'front' else (L['props'][0]['base'] + 0.5)
        placed[s['inst']] = dict(asset=s['asset'], x=x, y=y)
        anc = e['ancora']; col = None
        if e['collide']: c0 = e['collide']; col = [x + c0[0], y + c0[1], x + c0[2], y + c0[3]]
        rec = dict(inst=s['inst'], asset=s['asset'], sprite=e['sprite'], sx=x - anc[0], sy=y - anc[1], base=sort, layer=e['layer'], collide=col, frames=e['frames'])
        if e['states']: rec['states'] = e['states']
        if s.get('visivel_se'): rec['visivel_se'] = s['visivel_se']
        elif s['asset'].endswith('_aberta'): rec['visivel_se'] = [s['inst'], 1]
        if e['frames'] > 1: rec['fps'] = 6
        inst.append(rec)
        if e['interacao'] != 'nenhum' and e['layer'] != 'on' and not s['asset'].endswith('_aberta') or s['asset'] == 'fogao':
            st = e['stand']; inter.append(dict(id=s['inst'], asset=s['asset'], nome=e['nome'], classe=e['classe'], tipo=e['interacao'], rect=[rec['sx'], rec['sy'], e['dim_px'][0], e['dim_px'][1]],
                                               stand=s.get('stand_abs') or ([x + st[0], y + st[1]] if st else [x, y + 10]), face=e['face'], anim=s.get('anim', e['anim']), zoom=e['zoom'], desc=e['desc']))
    # interativos de estado (sobrepostos a objetos aprovados)
    for sid, asset, nome, stand, face, rect in (('gaveta_1', 'gaveta_balcao_aberta', 'Gaveta do balcão', [202, 195], 'up', [186, 165, 32, 18]),
                                                 ('porta_escada_1', 'porta_escada_aberta', 'Porta da escada', [393, 140], 'up', [382, 73, 22, 56])):
        e = by[asset][0]; inter = [i for i in inter if i['id'] != sid]
        inter.append(dict(id=sid, asset=asset, nome=nome, classe=e['classe'], tipo='alternar', rect=rect, stand=stand, face=face, anim='interact', zoom=e['zoom'], desc=e['desc'], states=e['states']))
    for f in FIXTURES:
        inter.append(dict(id=f['id'], asset=f['id'], nome=f['nome'], classe=f['classe'], tipo=f['interacao'], rect=f['rect'], stand=f.get('stand_abs', [f['rect'][0] + f['rect'][2] // 2, 158]),
                          face=f.get('face', 'up'), anim=f.get('anim', 'interact'), zoom=f.get('zoom', 2), desc=f.get('desc', '')))
        if f.get('collide'): blocks.append(f['collide'])
    inter = [i for i in inter if i['tipo'] != 'nenhum']
    seats = []
    for p in L['props']:
        sd = {'chair_a_back': ('down', 'after'), 'chair_b_back': ('down', 'after'), 'chair_a_l': ('right', 'after'), 'chair_b_l': ('right', 'after'),
              'chair_a_r': ('left', 'after'), 'chair_b_f': ('up', 'before')}.get(p['name'])
        if not sd: continue
        e = by[LEGACY[p['name']]][0]; cx = p['x'] + e['dim_px'][0] // 2
        seats.append(dict(id=p['name'], x=cx, y=p['base'] - 3, face=sd[0], sort=sd[1], base=p['base'], mesa='A' if p['name'].startswith('chair_a') else 'B', stand=[cx, p['base'] + (6 if sd[0] == 'down' else 6)]))
    seats += [dict(id='banco_1', x=355, y=147, face='down', sort='after', base=150, mesa='banco', stand=[355, 158]), dict(id='banco_2', x=373, y=147, face='down', sort='after', base=150, mesa='banco', stand=[373, 158])]
    pontos = dict(porta=[240, 231], fila=[[150, 197], [178, 197], [206, 197], [234, 197]], vitrine=[[104, 196], [128, 196]], vo_posto=[196, 168],
                  vo_x=[124, 236], forno=[190, 160], bancada=[262, 154], altar=[364, 142], filtro=[114, 222], escada=[393, 140], radio=[326, 152], caderneta=[236, 194], janela=[262, 154])
    scene = dict(cena='padaria', seats=seats, pontos=pontos, instancias=inst, interativos=inter, colisao_arquitetura=blocks)
    json.dump(scene, open(OUT + 'scene_padaria.json', 'w'), indent=1, ensure_ascii=False)
    return scene

if __name__ == '__main__':
    e = build(); sc = build_scene(); print(len(e), 'sprites', len(sc['instancias']), 'instancias', len(sc['interativos']), 'interativos')
