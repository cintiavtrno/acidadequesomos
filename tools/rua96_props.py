"""Etapa C de 1996 — objetos da gravação e do cotidiano, no mesmo pipeline de props de 1991 (rua6_props): vista lateral, 1 m = 24 px,
âncora no ponto de contato com o chão, luz do alto à esquerda, mesma rampa e contorno suave. Registra os novos sprites em RP.PRO."""
import random, math
from pxl import *
from facade import STONE, CAL, IRON
from rua6_art import *
from rua6_font import text, width
import rua6_props as RP
from rua6_props import prop, sh

CAMC = ramp(230, .10, (.07, .12, .19, .28, .40))       # corpo de câmera / equipamentos pretos
CASE = ramp(220, .07, (.13, .22, .33, .46, .60))       # road case de metal escuro
ALU = ramp(215, .06, (.30, .44, .58, .72, .86))        # alumínio / cantoneiras
YELL = ramp(48, .80, (.30, .42, .54, .66, .78))
REDC = ramp(4, .60, (.22, .32, .44, .56, .68))
BLUEC = ramp(214, .45, (.20, .30, .42, .54, .66))
CANV = ramp(40, .20, (.40, .52, .64, .74, .84))
WHT = ramp(46, .10, (.62, .74, .84, .92, .97))

def blk(c, x, y, w, h, R, edge=True):
    """Bloco com luz do alto-esquerda: topo e lado esquerdo claros, base e lado direito escuros."""
    c.rect(x, y, w, h, R[2])
    c.hline(x, y, w, R[4]); c.vline(x, y, h, R[3]); c.hline(x, y + h - 1, w, R[1]); c.vline(x + w - 1, y, h, R[1])
    c.pset(x, y + h - 1, R[1]); c.pset(x + w - 1, y, R[3])

def cantos(c, x, y, w, h):
    for (cx, cy) in ((x, y), (x + w - 2, y), (x, y + h - 2), (x + w - 2, y + h - 2)): c.rect(cx, cy, 2, 2, ALU[3]); c.pset(cx, cy, ALU[4])

def road_case(c, x, y, w, h, R=CASE, rodas=True):
    blk(c, x, y, w, h, R); cantos(c, x, y, w, h)
    c.hline(x + 2, y + h // 2, w - 4, R[1]); c.hline(x + 2, y + h // 2 + 1, w - 4, R[3])          # junta da tampa
    c.rect(x + w // 2 - 2, y + 2, 4, 2, ALU[2]); c.pset(x + w // 2 - 2, y + 2, ALU[4])             # trava
    if rodas:
        for rx in (x + 1, x + w - 3): c.rect(rx, y + h, 2, 2, (30, 28, 34))

# ------------------------------------------------------------------ câmera em tripé (lente para a direita; a outra é o espelho)
def _camera_body(c, x, y):
    """Câmera de vídeo profissional de ombro (anos 90), de perfil, lente à direita; x,y = canto superior esquerdo do corpo."""
    blk(c, x, y, 15, 8, CAMC); c.hline(x + 1, y + 1, 13, CAMC[3])
    blk(c, x - 4, y + 1, 5, 7, CAMC)                          # bateria atrás
    c.rect(x - 3, y + 3, 3, 1, YELL[2])                       # etiqueta da bateria
    blk(c, x + 3, y - 3, 6, 3, CAMC)                          # visor
    c.rect(x + 4, y - 2, 2, 1, (120, 150, 170))
    blk(c, x + 15, y + 1, 5, 6, CAMC); c.vline(x + 20, y + 2, 4, (88, 118, 140))                 # corpo da lente
    blk(c, x + 20, y + 1, 4, 6, CAMC); c.vline(x + 22, y + 2, 4, (66, 96, 122)); c.vline(x + 23, y + 2, 4, (120, 150, 170))   # parasol e vidro
    c.rect(x + 6, y + 8, 4, 2, CAMC[1])                       # base da câmera

@prop('tripe_cam_d', 44, 48, 22, 46, nome='câmera em tripé (lente para a direita)', tipo='examinar', classe='DECORATIVO', size_m=(0.9, 1.9, 0.9), collide=(-3, -3, 3, 2), stand=(0, 13), zoom=2,
      desc='Câmera profissional de vídeo sobre um tripé alto de alumínio. O cabo desce pelo chão em direção ao monitor da produção.')
def d_tripe_d(c):
    sh(c, 22, 45, 13)
    top = (22, 22)
    for (fx, w_) in ((9, 0), (35, 0)):                        # pernas externas (apoiadas no chão)
        c.line(top[0], top[1], fx, 45, ALU[1]); c.line(top[0] + 1, top[1], fx + 1, 45, ALU[3]); c.pset(fx, 46, (30, 28, 34)); c.pset(fx + 1, 46, (30, 28, 34))
    c.line(top[0], top[1], 22, 45, ALU[2]); c.pset(22, 46, (30, 28, 34))                         # perna do fundo (central)
    c.rect(top[0] - 4, top[1] - 1, 9, 3, ALU[2]); c.hline(top[0] - 4, top[1] - 1, 9, ALU[4])    # cabeça do tripé
    c.line(top[0] + 4, top[1], top[0] + 9, top[1] + 4, ALU[2]); c.pset(top[0] + 9, top[1] + 5, ALU[3])   # barra de pan
    _camera_body(c, 11, 11)
    c.hline(14, 21, 13, CAMC[0])

@prop('tripe_cam_e', 44, 48, 22, 46, nome='câmera em tripé (lente para a esquerda)', tipo='examinar', classe='DECORATIVO', size_m=(0.9, 1.9, 0.9), collide=(-3, -3, 3, 2), stand=(0, 13), zoom=2,
      desc='Câmera profissional de vídeo sobre tripé, virada para o palco. O cabo segue pela sarjeta até a base de produção.')
def d_tripe_e(c):
    t = C(44, 48); d_tripe_d(t)
    for y in range(48):
        for x in range(44): c.pset(43 - x, y, t.get(x, y))

# ------------------------------------------------------------------ monitor de referência sobre case
@prop('monitor_case', 34, 36, 17, 34, nome='monitor de referência sobre case', tipo='examinar', classe='UTILIZÁVEL', size_m=(0.9, 1.2, 0.6), collide=(-13, -3, 13, 2), stand=(0, 13), zoom=3,
      desc='Monitor de tubo apoiado num case de transporte, ligado por cabo à câmera. Mostra em preto e branco o que a câmera enquadra.')
def d_monitor(c):
    sh(c, 17, 33, 14)
    road_case(c, 3, 21, 28, 12)
    blk(c, 8, 7, 18, 14, CAMC); c.rect(10, 9, 14, 10, (30, 40, 48)); c.hline(10, 9, 14, (70, 92, 104)); c.vline(10, 9, 10, (58, 78, 90))
    for i in range(0, 12, 3): c.hline(11 + i, 13, 2, (160, 190, 196)); c.hline(11 + i, 16, 2, (90, 120, 130))   # imagem estática de baixa resolução
    c.rect(22, 20, 2, 1, (210, 70, 60))                                                                          # led
    c.pset(16, 6, CAMC[3]); c.pset(17, 5, CAMC[3]); c.pset(15, 6, CAMC[2])                                       # antena/ventilação
    c.vline(30, 24, 7, (24, 22, 28)); c.hline(27, 31, 4, (24, 22, 28))                                          # cabo caindo pelo lado

@prop('case_pilha', 32, 32, 16, 30, nome='cases de equipamento', tipo='examinar', classe='DECORATIVO', size_m=(1.1, 1.1, 0.6), collide=(-13, -3, 13, 2), stand=(0, 13), zoom=3,
      desc='Cases rígidos de transporte, empilhados junto à parede, com as cantoneiras de alumínio e etiquetas de rotas de turnê.')
def d_pilha(c):
    sh(c, 16, 29, 14)
    road_case(c, 2, 17, 28, 13); road_case(c, 5, 5, 22, 12, R=BLUEC, rodas=False)
    c.rect(8, 8, 6, 3, (236, 232, 218)); c.hline(9, 9, 4, (60, 60, 70))                                        # etiqueta
    c.rect(20, 20, 4, 2, YELL[3])

@prop('case_camera', 36, 30, 18, 28, nome='câmera de ombro sobre case', tipo='examinar', classe='DECORATIVO', size_m=(1.2, 0.9, 0.6), collide=(-14, -3, 14, 2), stand=(0, 13), zoom=3,
      desc='Uma câmera de ombro de reserva, deitada sobre um case aberto, com a bateria encaixada e a alça solta.')
def d_case_cam(c):
    sh(c, 18, 27, 15)
    road_case(c, 3, 17, 30, 11)
    _camera_body(c, 11, 6)
    c.line(12, 16, 17, 13, CAMC[1]); c.line(17, 13, 24, 15, CAMC[1])                                           # alça

# ------------------------------------------------------------------ cadeira dobrável de equipe (lona), de perfil
def _dobravel(c, flip=False):
    ax, ay = 10, 26
    def X(x): return (19 - x) if flip else x
    def p(x, y, col): c.pset(X(x), y, col)
    sh(c, 10, 26, 8)
    for j in range(14):                                                    # perna de trás cruzando a da frente (X)
        p(5 + j // 2, ay - 12 + j, WOOD[1]); p(15 - j // 2, ay - 12 + j, WOOD[2]); p(4 + j // 2, ay - 12 + j, WOOD[1]) if j % 2 else None
    for x in range(4, 16): p(x, ay - 12, CANV[3]); p(x, ay - 11, CANV[2]); p(x, ay - 10, CANV[1])           # assento de lona
    p(4, ay - 12, CANV[4]); p(15, ay - 11, CANV[1])
    for j in range(10): p(4, ay - 13 - j, WOOD[2]); p(5, ay - 13 - j, WOOD[1])                              # montante do encosto
    for x in range(3, 8): p(x, ay - 22, CANV[3]); p(x, ay - 21, CANV[2]); p(x, ay - 20, CANV[1]); p(x, ay - 19, CANV[2])    # encosto de lona
    p(3, ay - 22, CANV[4])
    for x in range(8, 17): p(x, ay - 17, WOOD[3]); p(x, ay - 16, WOOD[2])                                  # braço
    p(16, ay - 16, WOOD[1]); p(16, ay - 15, WOOD[1])

@prop('cad_dobravel_d', 20, 28, 10, 26, nome='cadeira dobrável (frente para a direita)', tipo='nenhum', classe='UTILIZÁVEL', size_m=(0.5, 1.0, 0.5), collide=(-6, -3, 6, 2))
def d_dob_d(c): _dobravel(c, False)
@prop('cad_dobravel_e', 20, 28, 10, 26, nome='cadeira dobrável (frente para a esquerda)', tipo='nenhum', classe='UTILIZÁVEL', size_m=(0.5, 1.0, 0.5), collide=(-6, -3, 6, 2))
def d_dob_e(c): _dobravel(c, True)

# ------------------------------------------------------------------ microfones
@prop('mic_pedestal', 14, 46, 7, 44, nome='microfone em pedestal', tipo='examinar', classe='DECORATIVO', size_m=(0.4, 1.8, 0.4), collide=(-2, -2, 2, 1), stand=(0, 13), zoom=3,
      desc='Pedestal de microfone com tripé de base, apontado para o grupo. O cabo corre pela sarjeta.')
def d_mic(c):
    c.vline(7, 12, 32, ALU[1]); c.vline(6, 12, 32, ALU[3]); c.vline(8, 12, 32, ALU[0])
    c.line(7, 40, 2, 44, ALU[2]); c.line(7, 40, 12, 44, ALU[1]); c.line(7, 40, 7, 44, ALU[2])
    c.rect(4, 4, 6, 9, CAMC[2]); c.hline(4, 4, 6, CAMC[4]); c.vline(4, 4, 9, CAMC[3]); c.vline(9, 4, 9, CAMC[0])
    for y in range(5, 12, 2): c.hline(5, y, 4, CAMC[1])
    c.rect(5, 12, 4, 2, ALU[2])

@prop('mic_boom', 42, 54, 12, 52, nome='microfone em girafa', tipo='examinar', classe='DECORATIVO', size_m=(1.4, 2.1, 0.5), collide=(-3, -2, 3, 1), stand=(0, 13), zoom=3,
      desc='Girafa de microfone com protetor de pelo, estendida por cima do grupo para captar os tambores.')
def d_boom(c):
    c.vline(12, 10, 42, ALU[1]); c.vline(11, 10, 42, ALU[3]); c.vline(13, 10, 42, ALU[0])
    c.line(12, 48, 6, 52, ALU[2]); c.line(12, 48, 18, 52, ALU[1]); c.line(12, 48, 12, 52, ALU[2])
    c.line(12, 10, 30, 5, ALU[2]); c.line(12, 11, 30, 6, ALU[1])
    c.rect(28, 2, 12, 6, (86, 78, 74)); c.hline(28, 2, 12, (126, 116, 108)); c.hline(28, 7, 12, (50, 44, 44))   # protetor de pelo
    for x in range(29, 40, 2): c.pset(x, 3, (150, 140, 128))
    c.rect(11, 9, 3, 3, ALU[3])

# ------------------------------------------------------------------ barreira de público (grade metálica)
@prop('barreira', 52, 28, 26, 26, nome='barreira de organização do público', tipo='examinar', classe='DECORATIVO', size_m=(2.0, 1.1, 0.5), collide=(-24, -2, 24, 1), stand=(0, 13), zoom=2,
      desc='Grade metálica de contenção, com pés em T. Marca o limite entre o público e a área de gravação, com passagem aberta.')
def d_barreira(c):
    sh(c, 26, 26, 24)
    for x in (3, 24, 47):
        c.vline(x, 3, 22, ALU[1]); c.vline(x + 1, 3, 22, ALU[3])
    for y in (3, 12, 22):
        c.hline(3, y, 46, ALU[2]); c.hline(3, y + 1, 46, ALU[0])
    for x in range(9, 46, 5):
        if x not in (23, 24, 25): c.vline(x, 5, 17, ALU[1])
    for x in (0, 21, 44):
        c.hline(x, 25, 8, ALU[2]); c.hline(x, 26, 8, ALU[0])                                                   # pés
    c.rect(18, 7, 14, 5, YELL[2]); c.hline(18, 7, 14, YELL[4]); c.hline(18, 11, 14, YELL[1])                    # faixa de sinalização
    for x in (20, 24, 28): c.pset(x, 9, (30, 28, 34))

# ------------------------------------------------------------------ cabos
@prop('cabo_seg', 100, 6, 50, 3, nome='cabo de produção', tipo='nenhum', classe='DECORATIVO', size_m=(4.2, 0.05, 0.05), collide=None)
def d_cabo(c, rng=random.Random(96)):
    for x in range(100):
        y = 2 + (1 if 34 < x < 66 else 0) + (1 if 10 < x < 24 and x % 3 else 0)
        c.pset(x, y, (30, 26, 34)); c.pset(x, y + 1, (14, 12, 18)) if x % 2 else c.pset(x, y + 1, (44, 40, 50))
    for x in (12, 41, 72): c.rect(x, 1, 3, 3, YELL[2]); c.pset(x, 1, YELL[4])                                  # fita de identificação

@prop('cabo_desce', 34, 18, 4, 16, nome='cabo com protetor de passagem', tipo='nenhum', classe='DECORATIVO', size_m=(1.4, 0.7, 0.2), collide=None)
def d_desce(c):
    c.line(2, 1, 12, 8, (30, 26, 34)); c.line(2, 2, 12, 9, (14, 12, 18)); c.line(12, 8, 16, 14, (30, 26, 34))
    for x in range(14, 33): c.pset(x, 15, (30, 26, 34)); c.pset(x, 14, (44, 40, 50))
    c.rect(14, 11, 12, 5, YELL[2]); c.hline(14, 11, 12, YELL[4]); c.hline(14, 15, 12, YELL[1])                 # rampa amarela e preta
    for x in range(15, 26, 4): c.rect(x, 12, 2, 3, (30, 28, 34))

# ------------------------------------------------------------------ cotidiano: banca de tabuleiro
@prop('banca_tabuleiro', 40, 32, 20, 30, nome='banca de vendedor com tabuleiro', tipo='examinar', classe='UTILIZÁVEL', size_m=(1.3, 1.0, 0.7), collide=(-15, -3, 15, 2), stand=(0, 13), zoom=3,
      desc='Tabuleiro de madeira forrado de pano sobre cavaletes, com cocadas e doces embalados em papel. Um guarda-sol pequeno protege do sol da tarde.')
def d_banca(c, rng=random.Random(97)):
    sh(c, 20, 29, 17)
    for x in (6, 31):                                                                                        # cavaletes em X
        c.line(x, 14, x + 4, 29, WOOD[1]); c.line(x + 4, 14, x, 29, WOOD[2]); c.line(x + 1, 14, x + 5, 29, WOOD[1])
    c.rect(3, 12, 34, 3, WOOD[2]); c.hline(3, 12, 34, WOOD[3]); c.hline(3, 14, 34, WOOD[1])               # tampo
    c.rect(3, 11, 34, 1, (236, 232, 218))                                                                    # toalha de renda na borda
    for x in range(4, 36, 2): c.pset(x, 12, (236, 232, 218))
    for (x, col) in ((7, (214, 166, 80)), (12, (236, 214, 150)), (17, (214, 166, 80)), (22, (150, 96, 52)), (27, (236, 214, 150))):   # doces
        c.rect(x, 7, 4, 4, col); c.hline(x, 7, 4, mix(col, (255, 250, 230), .4)); c.hline(x, 10, 4, mix(col, (60, 30, 20), .35))
    c.vline(19, 0, 8, WOOD[2])                                                                               # haste do guarda-sol
    for i in range(-10, 11): c.pset(19 + i, 1 + abs(i) // 4, (210, 84, 64) if (i // 3) % 2 else (240, 224, 196))
    c.hline(11, 3, 17, (140, 54, 44))

if __name__ == '__main__':
    from PIL import Image
    ids = ['tripe_cam_d', 'tripe_cam_e', 'monitor_case', 'case_pilha', 'case_camera', 'cad_dobravel_d', 'cad_dobravel_e', 'mic_pedestal', 'mic_boom', 'barreira', 'cabo_seg', 'cabo_desce', 'banca_tabuleiro']
    W_ = sum(RP.PRO[i]['w'] + 8 for i in ids); im = Image.new('RGBA', (W_, 64), (214, 200, 170, 255)); x = 4
    for i in ids:
        c = RP.render(i); im.alpha_composite(c.im, (x, 4)); x += RP.PRO[i]['w'] + 8
    im.resize((im.width * 5, im.height * 5), Image.NEAREST).save('/home/claude/out96/props96_sheet.png'); print(im.size)
