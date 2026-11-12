"""Etapa 6 — objetos da rua (sprites ordenados pela linha de base). Vista frontal/lateral (side-view). 1 m = 24 px."""
import random, math, json
from pxl import *
from facade import STONE, CAL, IRON, BRICK
from rua6_art import *
from rua6_font import text, width

PRO = {}      # id -> dict(draw=fn, meta)
def prop(id, w, h, ax, ay, **meta):
    def deco(fn): PRO[id] = dict(fn=fn, w=w, h=h, ax=ax, ay=ay, meta=meta); return fn
    return deco
def sh(c, cx, y, rx, a=70):
    for dx in range(-rx, rx + 1):
        hh = 1 if abs(dx) < rx * .75 else 0
        for dy in range(0, hh + 1): 
            if c.get(cx + dx, y + dy)[3] == 0: c.pset(cx + dx, y + dy, (22, 16, 38, a))
IR = IRON; ST_ = STONE

# ------------------------------------------------------------------ mesa de dominó (1 m × 1 m, tampo a 0,75 m)
@prop('mesa_domino', 40, 26, 20, 24, nome='mesa de dominó', tipo='examinar', classe='UTILIZÁVEL', size_m=(1.0, 0.75, 1.0), stand=(0, 14), collide=(-14, -4, 14, 4), zoom=2,
      desc='Mesa quadrada de madeira, pintada de verde há muito tempo; o tampo tem as marcas de cada partida. Garrafa térmica de café e copinhos num canto.')
def d_mesa(c, rng=random.Random(3)):
    ax, ay = 20, 24
    sh(c, ax, ay - 1, 15)
    # pernas (traseiras mais escuras, dianteiras claras)
    for x in (ax - 12, ax + 10):
        c.rect(x, ay - 15, 2, 15, WOODD[1])
    for x in (ax - 13, ax + 11):
        for j in range(0, 15):
            c.pset(x, ay - 15 + j, WOOD[3]); c.pset(x + 1, ay - 15 + j, WOOD[2]); c.pset(x + 2, ay - 15 + j, WOOD[1]) if j > 1 else None
        c.pset(x + 1, ay - 1, WOOD[0])
    c.rect(ax - 14, ay - 14, 28, 3, WOOD[2]); c.hline(ax - 14, ay - 14, 28, WOOD[3]); c.hline(ax - 14, ay - 12, 28, WOOD[1])
    c.rect(ax - 17, ay - 20, 34, 3, mix((70, 120, 92), WOOD[3], .22)); c.hline(ax - 17, ay - 20, 34, (136, 176, 140)); c.hline(ax - 16, ay - 19, 32, (96, 146, 112))
    c.rect(ax - 17, ay - 17, 34, 3, (52, 94, 76)); c.hline(ax - 17, ay - 17, 34, (84, 128, 100)); c.hline(ax - 17, ay - 15, 34, (34, 62, 52))
    c.vline(ax - 17, ay - 20, 5, (112, 156, 124)); c.vline(ax + 16, ay - 20, 5, (30, 54, 46))
    for x in (ax - 10, ax - 4, ax + 6, ax + 12): c.pset(x, ay - 16, WOOD[3]); c.pset(x + 1, ay - 17, WOOD[2])
    # garrafa térmica + dois copinhos (café da padaria)
    tx = ax - 12
    c.rect(tx, ay - 29, 4, 9, (60, 90, 150)); c.rect(tx, ay - 30, 4, 2, (196, 196, 204)); c.vline(tx, ay - 29, 9, (110, 140, 196)); c.vline(tx + 3, ay - 29, 9, (36, 56, 100)); c.pset(tx + 1, ay - 31, (150, 150, 160))
    for x in (ax + 8, ax + 12):
        c.rect(x, ay - 23, 3, 3, (236, 232, 218)); c.pset(x, ay - 23, (252, 250, 240)); c.pset(x + 2, ay - 22, (190, 184, 170)); c.pset(x + 1, ay - 23, (96, 58, 36))

# ------------------------------------------------------------------ cadeiras (madeira com palhinha), vistas de perfil, frente e costas
def _chair_profile(c, flip):
    """Cadeira de perfil: assento a 0,45 m (11 px), encosto até 25 px. O encosto fica atrás de quem senta."""
    W, ay = 26, 28
    ax = 13
    draw = C(W, 32)
    # pernas: duas visíveis; traseiras prolongam-se no encosto
    def leg(x, top, col): 
        for j in range(top, ay): draw.pset(x, j, col[2]); draw.pset(x + 1, j, col[1]) if j > top + 1 else None
    leg(ax - 8, ay - 25, WOOD); leg(ax - 7, ay - 25, WOOD)
    draw.rect(ax - 8, ay - 25, 2, 14, WOOD[2]); draw.vline(ax - 8, ay - 25, 25, WOOD[3]); draw.vline(ax - 7, ay - 25, 25, WOOD[2])
    for j in range(ay - 11, ay): draw.pset(ax + 6, j, WOOD[2]); draw.pset(ax + 7, j, WOOD[1])
    # travessas do encosto
    for yy in (ay - 23, ay - 19, ay - 15):
        draw.rect(ax - 8, yy, 2, 2, WOOD[3]); 
    # assento (palhinha): topo claro e frente
    draw.rect(ax - 8, ay - 12, 16, 2, STRAW_[3]); draw.hline(ax - 8, ay - 12, 16, STRAW_[4]); draw.hline(ax - 8, ay - 10, 16, WOOD[1]); draw.hline(ax - 8, ay - 11, 16, STRAW_[2])
    for i in range(0, 16, 2): draw.pset(ax - 8 + i, ay - 11, STRAW_[1])
    draw.rect(ax - 8, ay - 10, 16, 1, WOOD[2])
    # travessa baixa entre as pernas
    draw.hline(ax - 7, ay - 5, 14, WOOD[1])
    c.im.alpha_composite(draw.im if not flip else draw.im.transpose(Image.FLIP_LEFT_RIGHT), (0, 0))
from PIL import Image
STRAW_ = ramp(44, 0.55, (0.34, 0.46, 0.58, 0.70, 0.80))
@prop('cad_dir', 26, 32, 13, 28, nome='cadeira (frente para a direita)', tipo='nenhum', classe='UTILIZÁVEL', size_m=(0.45, 1.0, 0.45), collide=(-8, -3, 8, 3))
def d_cad_dir(c): sh(c, 13, 27, 9); _chair_profile(c, flip=False)
@prop('cad_esq', 26, 32, 13, 28, nome='cadeira (frente para a esquerda)', tipo='nenhum', classe='UTILIZÁVEL', size_m=(0.45, 1.0, 0.45), collide=(-8, -3, 8, 3))
def d_cad_esq(c): sh(c, 13, 27, 9); _chair_profile(c, flip=True)
@prop('cad_fundo', 22, 32, 11, 28, nome='cadeira (de frente para a câmera)', tipo='nenhum', classe='UTILIZÁVEL', size_m=(0.45, 1.0, 0.45), collide=(-7, -3, 7, 3))
def d_cad_fundo(c):
    ax, ay = 11, 28; sh(c, ax, ay - 1, 9)
    for x in (ax - 7, ax + 6): c.rect(x, ay - 25, 2, 25, WOOD[2]); c.vline(x, ay - 25, 25, WOOD[3]); c.vline(x + 1, ay - 25, 25, WOOD[1])
    c.rect(ax - 7, ay - 25, 15, 2, WOOD[3]); c.hline(ax - 7, ay - 25, 15, WOOD[4])
    c.rect(ax - 6, ay - 17, 13, 1, WOOD[2]); c.rect(ax - 6, ay - 20, 13, 1, WOOD[2])
    c.rect(ax - 8, ay - 12, 17, 2, STRAW_[3]); c.hline(ax - 8, ay - 12, 17, STRAW_[4]); c.hline(ax - 8, ay - 10, 17, WOOD[1])      # só a borda do assento aparece sob o corpo
@prop('cad_costas', 22, 22, 11, 20, nome='encosto (cadeira de costas para a câmera)', tipo='nenhum', classe='UTILIZÁVEL', size_m=(0.45, 0.6, 0.1), layer='over')
def d_cad_costas(c):
    ax = 11; sh(c, ax, 19, 9)
    for x in (ax - 7, ax + 6): c.rect(x, 0, 2, 12, WOOD[2]); c.vline(x, 0, 12, WOOD[3]); c.vline(x + 1, 0, 12, WOOD[1])
    c.rect(ax - 7, 0, 15, 2, WOOD[3]); c.hline(ax - 7, 0, 15, WOOD[4]); c.rect(ax - 6, 8, 13, 1, WOOD[2]); c.rect(ax - 6, 4, 13, 1, WOOD[2])

# ------------------------------------------------------------------ cadeira de calçada (fio plástico) e banquinho
@prop('cad_calcada', 22, 30, 11, 27, nome='cadeira de fio', tipo='nenhum', classe='UTILIZÁVEL', size_m=(0.45, 0.9, 0.4), collide=(-7, -3, 7, 3))
def d_cad_calcada(c):
    ax, ay = 11, 27; sh(c, ax, ay - 1, 9)
    COR = ramp(8, .55, (.26, .36, .47, .58, .68))
    for j in range(0, 12): c.pset(ax - 8, ay - 24 + j, FERRO[3]); c.pset(ax - 7, ay - 24 + j + 1, FERRO[2])
    for j in range(0, 12): c.pset(ax + 6, ay - 11 + j, FERRO[2]); c.pset(ax + 7, ay - 11 + j, FERRO[1])
    for j in range(0, 11): c.pset(ax - 6, ay - 11 + j, FERRO[1])
    # encosto e assento trançados
    c.rect(ax - 8, ay - 24, 3, 14, COR[2])
    for j in range(0, 14, 2): c.pset(ax - 8, ay - 24 + j, COR[4]); c.pset(ax - 7, ay - 24 + j + 1, COR[1])
    c.rect(ax - 8, ay - 12, 16, 3, COR[3]); c.hline(ax - 8, ay - 12, 16, COR[4])
    for i in range(0, 16, 2): c.pset(ax - 8 + i, ay - 10, COR[1])
@prop('banquinho', 16, 18, 8, 16, nome='banquinho', tipo='nenhum', classe='UTILIZÁVEL', size_m=(0.35, 0.4, 0.35), collide=(-5, -3, 5, 3))
def d_banquinho(c):
    ax, ay = 8, 16; sh(c, ax, ay - 1, 7)
    for x in (ax - 5, ax + 4): c.rect(x, ay - 10, 2, 10, WOOD[2]); c.vline(x, ay - 10, 10, WOOD[3])
    c.rect(ax - 6, ay - 12, 13, 3, WOOD[3]); c.hline(ax - 6, ay - 12, 13, WOOD[4]); c.hline(ax - 6, ay - 10, 13, WOOD[1]); c.hline(ax - 5, ay - 5, 10, WOOD[1])

# ------------------------------------------------------------------ canteiros e árvores
@prop('canteiro_oiti', 96, 120, 48, 112, nome='canteiro com oiti', tipo='examinar', classe='DECORATIVO', size_m=(2.2, 4.4, 0.9), collide=(-27, -5, 27, 3), stand=(0, 14), zoom=1,
      desc='Oiti novo plantado num canteiro de alvenaria caiada. A sombra dele é a mais disputada da rua.')
def d_oiti(c, rng=random.Random(14)):
    ax, ay = 48, 112
    # sombra no chão (calçada): elipse larga, translúcida, projetada para a direita
    for y in range(-4, 6):
        for x in range(-34, 40):
            if ((x - 6) / 36) ** 2 + (y / 5.2) ** 2 <= 1: 
                if c.get(ax + x, ay + y)[3] == 0: c.pset(ax + x, ay + y, (22, 18, 44, 86))
    # tronco
    trunk(c, ax, ay - 8, ay - 60, 5, 4, rng, BARK, lean=0.15)
    for (dx, dy, L) in [(-1, -48, -12), (1, -52, 12), (0, -58, -4)]:
        for k in range(L // abs(L) * 0, L, 1 if L > 0 else -1):
            pass
    for t in range(14): c.pset(ax - 1 - t // 2, ay - 52 - t, BARK[2]); c.pset(ax - t // 2, ay - 52 - t, BARK[3])
    for t in range(14): c.pset(ax + 1 + t // 2, ay - 55 - t, BARK[2]); c.pset(ax + t // 2, ay - 55 - t, BARK[3])
    # copa: três massas de folhagem sobrepostas
    leafmass(c, ax - 14, ay - 80, 20, 14, rng, LEAF, n=90, cell=(5, 3))
    leafmass(c, ax + 14, ay - 76, 22, 15, rng, LEAF, n=96, cell=(5, 3))
    leafmass(c, ax - 1, ay - 94, 22, 14, rng, LEAF, n=90, cell=(5, 3), hole=.06)
    leafmass(c, ax, ay - 70, 26, 11, rng, LEAF, n=80, cell=(5, 3))
    for _ in range(18): c.pset(ax + rng.randint(-34, 34), ay - rng.randint(60, 104), LEAF[0]) if c.get(ax, ay)[3] or True else None
    # canteiro (alvenaria caiada) + terra + capim
    whitewash_box(c, ax - 27, ay - 8, 54, 12, rng, top=2)
    c.rect(ax - 25, ay - 8, 50, 2, (74, 52, 36)); 
    for _ in range(10): c.pset(ax + rng.randint(-24, 22), ay - 8, (96, 70, 48))
    for x in (ax - 22, ax - 14, ax + 12, ax + 20): grass_tuft(c, x, ay - 7, rng, 4, 4)
    for x in (ax - 24, ax + 22): c.vline(x, ay + 4, 2, CAL[1]) if False else None
    # galho caído de folhas (restos no canteiro)
    for _ in range(5): c.pset(ax + rng.randint(-20, 18), ay + rng.randint(5, 6), (140, 110, 60, 200))

@prop('canteiro_jardim', 84, 50, 42, 46, nome='canteiro de jardim', tipo='examinar', classe='DECORATIVO', size_m=(3.0, 1.4, 0.6), collide=(-36, -4, 36, 2), stand=(0, 13), zoom=2,
      desc='Canteiro comprido de alvenaria com crótons, hibisco e uma trepadeira. Alguém rega todo fim de tarde.')
def d_jardim(c, rng=random.Random(7)):
    ax, ay = 42, 46
    leafmass(c, ax - 24, ay - 17, 13, 9, rng, LEAF2, n=26, cell=(4, 3)); flower_dots(c, ax - 24, ay - 19, 10, 6, rng, FLOR_A, 7)
    leafmass(c, ax - 6, ay - 21, 14, 14, rng, LEAF, n=40, cell=(4, 3)); flower_dots(c, ax - 6, ay - 25, 11, 8, rng, FLOR_V, 10)
    leafmass(c, ax + 14, ay - 15, 12, 8, rng, LEAF3, n=24, cell=(4, 3))
    leafmass(c, ax + 28, ay - 19, 12, 11, rng, LEAF, n=30, cell=(4, 3)); flower_dots(c, ax + 28, ay - 22, 9, 6, rng, FLOR_M, 8)
    leafmass(c, ax, ay - 11, 36, 4, rng, LEAF, n=70, cell=(4, 3))
    whitewash_box(c, ax - 38, ay - 8, 76, 10, rng, top=2)
    c.rect(ax - 36, ay - 8, 72, 2, (74, 52, 36))
    for x in (ax - 30, ax - 12, ax + 6, ax + 22, ax + 34): grass_tuft(c, x, ay - 7, rng, 3, 3, LEAF2)
    for x in (ax - 30, ax + 22): sh(c, x, ay + 2, 3, 40)

# ------------------------------------------------------------------ vasos de porta
@prop('vaso_espada', 22, 46, 11, 44, nome='vaso de espada-de-são-jorge', tipo='examinar', classe='DECORATIVO', size_m=(0.4, 1.0, 0.4), collide=(-5, -3, 5, 2), stand=(0, 13), zoom=3,
      desc='Espada-de-são-jorge num vaso de barro grande, ao lado da porta. Quase toda casa daqui tem uma.')
def d_espada(c, rng=random.Random(5)):
    ax, ay = 11, 44; sh(c, ax, ay - 1, 8)
    pot_clay(c, ax, ay, 12, 11); sword_plant(c, ax, ay - 11, 30, rng, n=8)
@prop('vaso_latas', 36, 30, 18, 28, nome='plantas em latas', tipo='examinar', classe='DECORATIVO', size_m=(1.0, 0.8, 0.3), collide=(-14, -3, 14, 2), stand=(0, 13), zoom=3,
      desc='Latas de tinta e de óleo servindo de vaso: samambaia, pimenta, manjericão. Cada uma com o resto da cor que já foi parede.')
def d_latas(c, rng=random.Random(9)):
    ax, ay = 18, 28; sh(c, ax, ay - 1, 15)
    can_pot(c, ax - 10, ay, 8, 9, LATA, rng); fern(c, ax - 10, ay - 9, 8, 11, rng, LEAF2)
    can_pot(c, ax, ay, 8, 8, LATA2, rng); leafmass(c, ax, ay - 14, 5, 6, rng, LEAF, n=10); flower_dots(c, ax, ay - 14, 5, 5, rng, FLOR_V, 6)
    can_pot(c, ax + 10, ay, 8, 10, ramp(48, .55, (.28, .38, .50, .60, .70)), rng); leafmass(c, ax + 10, ay - 16, 6, 6, rng, LEAF3, n=12)
@prop('vaso_palmeira', 30, 62, 15, 60, nome='palmeira-ráfia em vaso', tipo='examinar', classe='DECORATIVO', size_m=(0.7, 2.1, 0.7), collide=(-6, -3, 6, 2), stand=(0, 13), zoom=2,
      desc='Palmeira-ráfia num vaso de cimento. Vive à sombra da varanda e nunca morreu, o que é quase um milagre.')
def d_palmeira(c, rng=random.Random(11)):
    ax, ay = 15, 60; sh(c, ax, ay - 1, 11)
    for j in range(13):
        ww = 14 - (j < 2) * 2
        c.rect(ax - ww // 2, ay - 13 + j, ww, 1, ramp(40, .06, (.34, .44, .56, .66, .76))[3 if j < 2 else 2]); c.pset(ax - ww // 2, ay - 13 + j, ramp(40, .06, (.34, .44, .56, .66, .76))[4]); c.pset(ax + ww // 2 - 1, ay - 13 + j, ramp(40, .06, (.34, .44, .56, .66, .76))[1])
    for t in range(0, 34): 
        c.pset(ax + (t // 12) - 1, ay - 13 - t, BARK[2]); c.pset(ax + (t // 12), ay - 13 - t, BARK[1])
    for i in range(10):
        a = -math.pi / 2 + (i - 4.5) * 0.30
        L = rng.randint(18, 26)
        for s in range(L):
            t = s / L; x = ax + 1 + math.cos(a) * s * 0.8 + (s * s / 70.0) * (1 if a > -math.pi / 2 else -1) * 0.55
            y = ay - 46 + math.sin(a) * s * 0.9 + (s * s / 70.0)
            c.pset(round(x), round(y), LEAF[3 - (t > .5)] if t < .85 else LEAF[1]); c.pset(round(x), round(y) + 1, LEAF[1])

# ------------------------------------------------------------------ mobiliário urbano
@prop('poste', 28, 196, 14, 192, nome='poste de concreto', tipo='examinar', classe='DECORATIVO', size_m=(0.3, 8.0, 0.3), collide=(-3, -3, 3, 2), stand=(0, 14), zoom=1,
      desc='Poste de concreto com transformador e fios que seguem para as casas. Já foi usado como quadro de avisos por toda a vizinhança.')
def d_poste(c, rng=random.Random(2)):
    ax, ay = 14, 192; sh(c, ax, ay - 1, 5)
    CONC = ramp(48, .06, (.34, .44, .56, .66, .78))
    for y in range(0, 190):
        w = 6 if y > 40 else 5
        for i in range(w):
            u = i / (w - 1); c.pset(ax - w // 2 + i, y + 2, CONC[4 if u < .2 else 3 if u < .5 else 2 if u < .8 else 1])
    for y in range(120, 190, 14): c.hline(ax - 3, y + 2, 6, CONC[1])
    # base com pintura (faixa preta e branca)
    for y in range(164, 190):
        if (y // 5) % 2: c.rect(ax - 3, y + 2, 6, 1, (30, 28, 34))
    # travessa de ferro com isoladores
    c.rect(ax - 12, 14, 25, 2, IR[3]); c.hline(ax - 12, 14, 25, IR[4]); c.hline(ax - 12, 16, 25, IR[1])
    for x in (-10, -4, 4, 10): c.rect(ax + x - 1, 8, 3, 6, (92, 150, 150)); c.rect(ax + x - 1, 7, 3, 1, (150, 200, 196)); c.pset(ax + x + 1, 10, (50, 90, 96))
    # transformador (lata cinza)
    for j in range(24):
        for i in range(12):
            u = i / 11; c.pset(ax + 5 + i - 1, 38 + j, mix(IR[4], (170, 178, 186), .55) if u < .2 else mix(IR[3], (130, 138, 150), .5) if u < .6 else mix(IR[2], (100, 106, 120), .4))
    c.rect(ax + 4, 36, 14, 2, IR[4]); c.rect(ax + 4, 62, 14, 1, IR[1])
    for x in (ax + 8, ax + 12): c.rect(x, 33, 2, 3, (92, 150, 150))
    # braço da luminária
    c.rect(ax - 18, 78, 14, 2, IR[3]); c.rect(ax - 22, 80, 8, 3, IR[2]); c.rect(ax - 21, 83, 6, 1, (248, 236, 170)); c.hline(ax - 22, 79, 8, IR[4])
    # cartazes colados (lambe-lambe)
    for (y, cc) in [(102, [(214, 84, 66), (240, 120, 100), (252, 232, 200)]), (118, [(236, 200, 70), (250, 224, 120), (120, 60, 30)])]:
        c.rect(ax - 3, y, 6, 12, cc[0]); c.hline(ax - 3, y, 6, cc[1]); c.hline(ax - 2, y + 4, 4, cc[2]); c.hline(ax - 2, y + 7, 3, cc[2])

@prop('orelhao', 24, 44, 12, 42, nome='orelhão', tipo='examinar', classe='UTILIZÁVEL', size_m=(0.6, 1.6, 0.6), collide=(-4, -3, 4, 2), stand=(0, 13), zoom=3,
      desc='Orelhão de fibra azul, daqueles de ficha. Alguém rabiscou um número de telefone na cúpula.')
def d_orelhao(c, rng=random.Random(4)):
    ax, ay = 12, 42; sh(c, ax, ay - 1, 7)
    AZ = ramp(212, .60, (.20, .30, .42, .54, .66))
    for y in range(0, 22): c.pset(ax, ay - 1 - y, IR[2]); c.pset(ax - 1, ay - 1 - y, IR[3]); c.pset(ax + 1, ay - 1 - y, IR[1])
    c.rect(ax - 4, ay - 3, 9, 2, IR[3])
    # cúpula
    for y in range(-11, 3):
        half = int(round(math.sqrt(max(0, 11 ** 2 - (y * 11 / 12) ** 2)) * 1.0))
        half = min(11, max(0, int(11 * math.sqrt(max(0, 1 - ((y + 0) / 12.0) ** 2)))))
        for x in range(-half, half + 1):
            u = (x + half) / max(1, 2 * half)
            col = AZ[4] if (u < .18 and y < 0) else AZ[3] if u < .5 else AZ[2] if u < .82 else AZ[1]
            c.pset(ax + x, 22 + y, col)
    c.hline(ax - 11, 24, 23, AZ[1]); c.hline(ax - 10, 25, 21, AZ[0])
    # abertura (cavidade do telefone, mais escura) e fone
    c.rect(ax - 6, 20, 13, 5, (22, 28, 50)); c.hline(ax - 6, 20, 13, (14, 18, 34)); c.rect(ax - 4, 21, 8, 2, (60, 76, 120)); c.rect(ax - 3, 23, 6, 2, (236, 232, 218)); c.pset(ax + 4, 22, (230, 190, 70))
    c.rect(ax - 8, 14, 17, 1, (240, 236, 224))                                                    # faixa branca

@prop('lixeira', 16, 28, 8, 26, nome='lixeira de tela', tipo='examinar', classe='DECORATIVO', size_m=(0.4, 0.8, 0.4), collide=(-4, -3, 4, 2), stand=(0, 13), zoom=3,
      desc='Cesto de tela de aço preso num pé de ferro. Sacos de pão vazios, copo de café, papel de bala.')
def d_lixeira(c, rng=random.Random(6)):
    ax, ay = 8, 26; sh(c, ax, ay - 1, 6)
    for y in range(0, 12): c.pset(ax, ay - 1 - y, IR[2]); c.pset(ax + 1, ay - 1 - y, IR[1])
    c.rect(ax - 3, ay - 2, 8, 2, IR[3])
    for j in range(11):
        for i in range(11):
            x = ax - 5 + i; y = 2 + j
            if i in (0, 10) or j in (0, 10) or (i + j) % 3 == 0: c.pset(x, y, IR[3] if i < 5 else IR[2] if i < 8 else IR[1])
            else: c.pset(x, y, (30, 24, 34))
    c.rect(ax - 6, 1, 13, 2, IR[4]); c.hline(ax - 6, 0, 13, IR[4])
    for (x, y, col) in [(-3, 6, (236, 232, 218)), (0, 7, (210, 60, 50)), (2, 5, (240, 200, 70))]: c.rect(ax + x, y + 2, 3, 2, col)

@prop('banco', 52, 28, 26, 25, nome='banco de madeira', tipo='nenhum', classe='UTILIZÁVEL', size_m=(1.8, 0.8, 0.5), collide=(-23, -3, 23, 2), stand=(0, 13),
      desc='Banco de ripas sobre pés de concreto, de frente para a rua.')
def d_banco(c, rng=random.Random(8)):
    ax, ay = 26, 25; sh(c, ax, ay - 1, 23)
    CONC = ramp(48, .06, (.34, .44, .56, .66, .78))
    for x in (ax - 21, ax + 17): 
        c.rect(x, ay - 11, 5, 11, CONC[2]); c.vline(x, ay - 11, 11, CONC[4]); c.vline(x + 4, ay - 11, 11, CONC[1]); c.hline(x, ay - 1, 5, CONC[0])
    for k, y in enumerate((ay - 20, ay - 17, ay - 14)):                               # encosto de ripas
        c.rect(ax - 24, y, 49, 2, WOOD[3]); c.hline(ax - 24, y, 49, WOOD[4]); c.hline(ax - 24, y + 1, 49, WOOD[1])
    for x in (ax - 22, ax + 20): c.rect(x, ay - 21, 2, 11, WOOD[1])
    c.rect(ax - 24, ay - 11, 49, 3, WOOD[2]); c.hline(ax - 24, ay - 11, 49, WOOD[4]); c.hline(ax - 24, ay - 9, 49, WOOD[0])
    for x in (ax - 10, ax + 6): c.pset(x, ay - 10, WOOD[0])

@prop('bicicleta', 40, 26, 20, 24, nome='bicicleta encostada', tipo='examinar', classe='DECORATIVO', size_m=(1.7, 1.1, 0.4), collide=(-18, -2, 18, 2), stand=(0, 13), zoom=2,
      desc='Bicicleta de entregador com cesto de vime no guidão. A corrente tem mais graxa que tinta.')
def d_bike(c, rng=random.Random(10)):
    ax, ay = 20, 24; sh(c, ax, ay - 1, 17)
    RED = ramp(2, .55, (.24, .34, .45, .56, .66))
    def wheel(cx):
        for a in range(0, 360, 8):
            x = cx + round(math.cos(math.radians(a)) * 9); y = ay - 10 + round(math.sin(math.radians(a)) * 9)
            c.pset(x, y, (28, 24, 32)); 
            if a % 24 == 0: c.pset(cx + round(math.cos(math.radians(a)) * 5), ay - 10 + round(math.sin(math.radians(a)) * 5), IR[4])
        for a in range(0, 360, 8):
            c.pset(cx + round(math.cos(math.radians(a)) * 8), ay - 10 + round(math.sin(math.radians(a)) * 8), (58, 54, 64))
    wheel(ax - 12); wheel(ax + 12)
    c.line(ax - 12, ay - 10, ax - 2, ay - 14, RED[3]); c.line(ax - 2, ay - 14, ax + 8, ay - 20, RED[3]); c.line(ax + 8, ay - 20, ax + 12, ay - 10, RED[2])
    c.line(ax - 12, ay - 10, ax - 2, ay - 6, RED[2]); c.line(ax - 2, ay - 6, ax - 2, ay - 14, RED[2]); c.line(ax - 2, ay - 6, ax + 12, ay - 10, RED[1])
    c.line(ax - 4, ay - 18, ax - 2, ay - 15, (30, 26, 30)); c.hline(ax - 7, ay - 19, 6, (30, 26, 30))                   # selim
    c.line(ax + 8, ay - 20, ax + 9, ay - 23, IR[3]); c.hline(ax + 6, ay - 24, 5, IR[3])
    c.rect(ax + 8, ay - 22, 8, 5, STRAW_[2]); c.hline(ax + 8, ay - 22, 8, STRAW_[4]); c.hline(ax + 8, ay - 17, 8, WOOD[1])   # cesto
    for k in range(0, 8, 2): c.pset(ax + 8 + k, ay - 20, STRAW_[1])

@prop('cavalete_pao', 40, 40, 20, 38, nome='cavalete da padaria', tipo='examinar', classe='UTILIZÁVEL', size_m=(0.9, 1.0, 0.5), collide=(-12, -3, 12, 2), stand=(0, 13), zoom=3,
      desc='Cavalete de lousa na porta da padaria. A letra é da Vó; o preço é do dia.')
def d_cavalete(c, rng=random.Random(12)):
    ax, ay = 20, 38; sh(c, ax, ay - 1, 14)
    for x, d in ((ax - 13, 1), (ax + 12, -1)): 
        for j in range(0, 30): c.pset(x + (j // 15) * d, ay - 1 - j, WOOD[3 if d > 0 else 1]); c.pset(x + 1 + (j // 15) * d, ay - 1 - j, WOOD[2])
    c.rect(ax - 12, ay - 31, 25, 21, WOOD[2]); c.hline(ax - 12, ay - 31, 25, WOOD[4]); c.vline(ax - 12, ay - 31, 21, WOOD[3]); c.vline(ax + 12, ay - 31, 21, WOOD[1]); c.hline(ax - 12, ay - 11, 25, WOOD[1])
    c.rect(ax - 10, ay - 29, 21, 17, (34, 44, 46)); c.hline(ax - 10, ay - 29, 21, (58, 70, 68))
    MINI = {'P': ('###', '#.#', '###', '#..', '#..'), 'A': ('.#.', '#.#', '###', '#.#', '#.#'), 'O': ('###', '#.#', '#.#', '#.#', '###'), 'C': ('###', '#..', '#..', '#..', '###'), 'F': ('###', '#..', '##.', '#..', '#..'), 'E': ('###', '#..', '##.', '#..', '###')}
    def mini(x, y, word, col):
        for ch in word:
            for j, row in enumerate(MINI[ch]):
                for i, v in enumerate(row):
                    if v == '#': c.pset(x + i, y + j, col)
            x += 4
    mini(ax - 5, ay - 27, 'PAO', (244, 238, 220)); mini(ax - 7, ay - 20, 'CAFE', (240, 214, 120))
    c.hline(ax - 10, ay - 12, 21, (180, 176, 164)); c.pset(ax - 6, ay - 12, (236, 232, 218)); c.pset(ax - 5, ay - 12, (236, 232, 218))   # giz

@prop('caixote_laranja', 26, 20, 13, 18, nome='caixote de laranjas', tipo='examinar', classe='DECORATIVO', size_m=(0.6, 0.5, 0.4), collide=(-9, -2, 9, 2), stand=(0, 13), zoom=3,
      desc='Caixote de feira com laranjas-bahia que o menino da banca deixou. Ninguém mexe.')
def d_caixote(c, rng=random.Random(13)):
    ax, ay = 13, 18; sh(c, ax, ay - 1, 11)
    OR = ramp(30, .85, (.38, .48, .58, .68, .78))
    for i in range(-9, 9, 3): 
        for j in range(3): blob(c, ax + i + 1, ay - 13 - (j == 1) * 1, 2, 2, OR[2 + (i + j) % 3])
    c.rect(ax - 10, ay - 10, 21, 10, WOOD[2]); c.hline(ax - 10, ay - 10, 21, WOOD[4]); c.hline(ax - 10, ay - 6, 21, WOOD[1]); c.vline(ax - 10, ay - 10, 10, WOOD[3]); c.vline(ax + 10, ay - 10, 10, WOOD[1]); c.hline(ax - 10, ay - 1, 21, WOOD[0])
    for x in (ax - 5, ax + 3): c.pset(x, ay - 8, WOOD[0]); c.pset(x + 1, ay - 3, WOOD[3])

@prop('pilha_obra', 40, 26, 20, 24, nome='tijolos e sacos de cimento', tipo='examinar', classe='DECORATIVO', size_m=(1.5, 0.8, 0.6), collide=(-17, -3, 17, 2), stand=(0, 13), zoom=2,
      desc='Pilha de tijolos e dois sacos de cimento. Alguém está consertando o reboco da casa, devagar, no tempo do dinheiro.')
def d_obra(c, rng=random.Random(15)):
    ax, ay = 20, 24; sh(c, ax, ay - 1, 18)
    for r in range(5):
        for i in range(4 - (r > 2) * 1):
            x = ax - 18 + i * 8 + (r % 2) * 4; y = ay - 3 - r * 4
            c.rect(x, y - 2, 7, 3, BRICK[2 + (i + r) % 2]); c.hline(x, y - 2, 7, BRICK[3]); c.hline(x, y, 7, BRICK[0]); c.vline(x + 6, y - 2, 3, BRICK[1])
    for k, x in enumerate((ax + 2, ax + 12)):
        y = ay - 8 + k * 3
        c.rect(x, y, 12, 7, (182, 170, 148)); c.hline(x, y, 12, (216, 206, 184)); c.hline(x, y + 6, 12, (118, 108, 92)); c.vline(x + 11, y, 7, (140, 130, 112))
        c.rect(x + 3, y + 2, 6, 2, (50, 80, 130)); c.rect(x - 1, y - 1, 1, 8, (160, 148, 126))

# ------------------------------------------------------------------ elementos de parede (camada 'wall': atrás dos personagens, à frente da fachada)
@prop('quadro_avisos', 34, 30, 17, 28, nome='quadro de avisos', tipo='examinar', classe='EXAMINÁVEL', size_m=(0.9, 0.8, 0.05), collide=None, stand=(0, 14), zoom=3, layer='wall', ywall=-34,
      desc='Quadro de cortiça da associação: reunião de moradores, rifa de uma geladeira, aviso sobre a água, anúncio de aluguel de cômodo.')
def d_quadro(c, rng=random.Random(16)):
    c.rect(0, 0, 34, 26, WOOD[2]); c.hline(0, 0, 34, WOOD[4]); c.vline(0, 0, 26, WOOD[3]); c.vline(33, 0, 26, WOOD[1]); c.hline(0, 25, 34, WOOD[0])
    c.rect(2, 2, 30, 22, (170, 124, 80)); 
    for _ in range(40): c.pset(rng.randint(2, 31), rng.randint(2, 23), (146, 104, 66))
    papers = [(3, 3, 9, 12, (240, 236, 222)), (14, 4, 8, 7, (240, 214, 120)), (23, 3, 8, 11, (236, 150, 130)), (14, 13, 8, 9, (150, 196, 210)), (4, 17, 8, 6, (240, 236, 222)), (24, 16, 7, 7, (240, 236, 222))]
    for (x, y, w, h, col) in papers:
        c.rect(x, y, w, h, col); c.hline(x, y, w, mix(col, (255, 255, 255), .5)); c.vline(x + w - 1, y, h, mix(col, (60, 40, 40), .25))
        for j in range(2, h - 1, 2): c.hline(x + 1, y + j, max(2, w - 3 - (j % 3)), mix(col, (60, 50, 50), .55))
        c.pset(x + w // 2, y, (200, 50, 40))
    c.shade(0, 26, 34, 2, SH2)

@prop('gato', 18, 14, 9, 12, nome='gato', tipo='examinar', classe='DECORATIVO', size_m=(0.4, 0.3, 0.2), collide=None, stand=(0, 13), zoom=3, frames=2,
      desc='Gato malhado dormindo no calor da pedra. Abre um olho quando você passa.')
def d_gato(c, rng=random.Random(17), f=0):
    ax, ay = 9, 12
    GA = ramp(30, .50, (.26, .36, .48, .60, .72)); GB = ramp(36, .12, (.24, .34, .46, .58, .70))
    sh(c, ax, ay - 1, 8)
    for y in range(-5, 1):
        for x in range(-7, 7):
            if (x / 7.3) ** 2 + ((y + 2.4) / 3.4) ** 2 <= 1: c.pset(ax + x, ay + y - 1, GA[3 if y < -3 else 2 if y < -1 else 1])
    for x in range(-6, 5, 3): c.hline(ax + x, ay - 4, 2, GA[0])                                                  # listras
    for y in range(-4, 0):
        for x in range(4, 9):
            if ((x - 6.4) / 3) ** 2 + ((y + 1.8) / 2.6) ** 2 <= 1: c.pset(ax + x, ay + y - 1, GB[3 if y < -2 else 2])
    c.pset(ax + 6, ay - 6, GB[1]); c.pset(ax + 8, ay - 6, GB[1]); c.pset(ax + 6, ay - 7, GB[2]); c.pset(ax + 8, ay - 7, GB[2])    # orelhas
    c.pset(ax + 7, ay - 4, (30, 24, 30) if f == 0 else (120, 200, 90)); c.pset(ax + 8, ay - 3, (240, 170, 160))
    c.hline(ax - 8, ay - 1 + (f == 1), 3, GA[1])                                                                  # rabo

@prop('pombo', 12, 12, 6, 10, nome='pombo', tipo='nenhum', classe='DECORATIVO', size_m=(0.3, 0.25, 0.15), collide=None, frames=3)
def d_pombo(c, rng=random.Random(18), f=0):
    ax, ay = 6, 10
    P = ramp(220, .08, (.28, .38, .50, .62, .74))
    sh(c, ax, ay, 4, 50)
    for y in range(-5, 0):
        for x in range(-4, 4):
            if (x / 4.2) ** 2 + ((y + 2.5) / 2.8) ** 2 <= 1: c.pset(ax + x, ay + y, P[3 if y < -3 else 2 if x > -2 else 1])
    c.rect(ax + 2 - (f == 1) * 0, ay - 8 + (f == 1) * 4, 3, 3, P[2]); c.pset(ax + 4, ay - 7 + (f == 1) * 4, (210, 150, 40)); c.pset(ax + 3, ay - 7 + (f == 1) * 4, (24, 20, 30))
    c.hline(ax - 5, ay - 3, 2, P[1]); c.pset(ax - 1, ay, (200, 90, 80)); c.pset(ax + 1, ay, (200, 90, 80))
    c.pset(ax + 1, ay - 5, (120, 160, 110))

def render(id, f=None):
    p = PRO[id]; c = C(p['w'], p['h'])
    import inspect
    if 'f' in inspect.signature(p['fn']).parameters: p['fn'](c, f=f or 0)
    else: p['fn'](c)
    return c

def build_atlas(path_png='../assets/street6/props.png', path_json='../assets/street6/props.json'):
    items = []
    for id, p in PRO.items():
        fr = p['meta'].get('frames', 1)
        for f in range(fr):
            items.append((id, f, render(id, f)))
    # empacotamento em prateleiras
    W = 640; x = y = 2; rowh = 0; pos = {}
    for id, f, c in sorted(items, key=lambda t: -t[2].h):
        if x + c.w + 2 > W: x = 2; y += rowh + 2; rowh = 0
        pos[(id, f)] = (x, y); x += c.w + 2; rowh = max(rowh, c.h)
    H = y + rowh + 2
    sheet = C(W, H)
    for (id, f, c) in items: sheet.paste(c, *pos[(id, f)])
    sheet.save(path_png)
    meta = {}
    for id, p in PRO.items():
        fr = p['meta'].get('frames', 1)
        meta[id] = dict(w=p['w'], h=p['h'], ax=p['ax'], ay=p['ay'], frames=[list(pos[(id, f)]) for f in range(fr)], **{k: v for k, v in p['meta'].items() if k != 'frames'})
    json.dump(meta, open(path_json, 'w'), indent=1, ensure_ascii=False)
    return sheet, meta

if __name__ == '__main__':
    sheet, meta = build_atlas()
    print(sheet.w, sheet.h, len(meta))
    sheet.im.resize((sheet.w * 2, sheet.h * 2), Image.NEAREST).save('/tmp/props6.png')
