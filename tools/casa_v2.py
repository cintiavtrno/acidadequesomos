"""Casa de Seu Raimundo — revisão visual (mobiliário reconstruído, tapete têxtil, contato com piso/parede).
Convenção: y = linha dos pés da frente; profundidade de piso 16 px/m; a face de cima dos móveis encostados na parede aparece (câmera 3/4 elevada)."""
import math
from pxl import *
from interior import TIMB, WOOD, LEAF, STRAW, BREAD, CLAY, RED, SACK, ell
from facade import IRON
from objlib import shadow, ENAM
from PIL import Image

DK = (24, 14, 34)
def sh(c, x, y, w, h, a=46):                                   # sombra de contato retangular (semi-transparente, só no sprite)
    for yy in range(h):
        c.hline(x, y + yy, w, (18, 10, 28, a - yy * 8 if a - yy * 8 > 10 else 10))

def post(c, x, y0, y1, w=2):                                   # peça vertical de madeira com luz à esquerda
    c.rect(x, y0, w, y1 - y0, TIMB[2]); c.vline(x, y0, y1 - y0, TIMB[3]); c.vline(x + w - 1, y0, y1 - y0, TIMB[1])

# ---------------------------------------------------------------- mesa de convivência (≈ +30%): 40 × 17 px de piso, tampo a 0,75 m
def d_mesa(c, x, y):
    w = 60; ex = 6; x0 = x - w // 2
    shadow(c, x, y + 1, w + 8, 78); sh(c, x0 + 3, y - 15, w - 6, 14, 40)        # sombra projetada sob o tampo
    for lx in (x0 + 1, x0 + w - 4):                                              # pernas torneadas da frente
        post(c, lx, y - 14, y, 3); c.rect(lx - 1, y - 14, 5, 2, TIMB[3]); c.hline(lx - 1, y - 14, 5, TIMB[4]); c.rect(lx, y - 8, 3, 1, TIMB[1]); c.hline(lx, y - 1, 3, TIMB[0])
    c.rect(x0 + 4, y - 7, w - 8, 1, TIMB[1])                                      # travessa
    c.rect(x0 + 1, y - 18, w - 2, 4, TIMB[2]); c.hline(x0 + 1, y - 18, w - 2, TIMB[4]); c.hline(x0 + 1, y - 15, w - 2, TIMB[0])   # saia
    for k in range(x0 + 6, x0 + w - 6, 8): c.vline(k, y - 17, 2, TIMB[1])
    c.rect(x0, y - 20, w, 3, TIMB[3]); c.hline(x0, y - 20, w, TIMB[4]); c.vline(x0, y - 20, 3, TIMB[4]); c.vline(x0 + w - 1, y - 20, 3, TIMB[2])   # espessura do tampo
    # tampo: toalha de crochê branca (plano de cima), caída na frente com barrado azul e picote
    c.rect(x0, y - 36 - ex, w, 16 + ex, SACK[3]); c.hline(x0, y - 36 - ex, w, SACK[2])
    for k in range(0, 16 + ex): c.pset(x0, y - 36 - ex + k, SACK[4]); c.pset(x0 + w - 1, y - 36 - ex + k, SACK[2])
    c.rect(x0 + 2, y - 34 - ex, w - 4, 12 + ex, SACK[4]); c.hline(x0 + 2, y - 34 - ex, w - 4, SACK[3]); c.hline(x0 + 2, y - 23, w - 4, SACK[3])   # miolo mais claro (luz da janela)
    c.rect(x0 + 1, y - 21, w - 2, 1, ENAM[2])                                      # filete azul da borda
    for k in range(x0 + 3, x0 + w - 3, 3): c.pset(k, y - 25 - ex // 2, mix(SACK[3], ENAM[2], .5))   # bordado azul ponteado
    c.rect(x0 + 1, y - 20, w - 2, 7, SACK[3]); c.hline(x0 + 1, y - 20, w - 2, SACK[2])      # caída da toalha na frente
    c.rect(x0 + 1, y - 15, w - 2, 1, ENAM[3]); c.rect(x0 + 1, y - 14, w - 2, 1, ENAM[2])
    for k in range(x0 + 1, x0 + w - 1, 2): c.pset(k, y - 13, SACK[3] if (k // 2) % 2 else SACK[2])   # picote do crochê
    c.vline(x0 + 1, y - 20, 7, SACK[4]); c.vline(x0 + w - 2, y - 20, 7, SACK[1])
    c.shade(x0 + 1, y - 19, w - 2, 2, SH1)
    # xícaras esmaltadas postas nos lugares laterais
    for cx in (x0 + 6, x0 + 14, x0 + w - 18, x0 + w - 9):
        c.rect(cx, y - 27, 4, 4, ENAM[4]); c.hline(cx, y - 27, 4, ENAM[4]); c.rect(cx + 1, y - 26, 2, 1, TIMB[1]); c.pset(cx + 4, y - 26, ENAM[3]); c.pset(cx + 4, y - 25, ENAM[3]); c.hline(cx, y - 23, 4, ENAM[1])

# ---------------------------------------------------------------- cadeiras (assento de palha, estrutura de madeira escura), 4 vistas
def _seat_top(c, x0, w, yb, d):                                 # plano do assento (palha trançada)
    c.rect(x0, yb - d, w, d, STRAW[3]); c.hline(x0, yb - d, w, STRAW[4])
    for k in range(d):
        for i in range(0, w, 2):
            if (i // 2 + k) % 2 == 0: c.pset(x0 + i + (k % 2), yb - d + k, STRAW[2])
    c.vline(x0, yb - d, d, STRAW[4]); c.vline(x0 + w - 1, yb - d, d, STRAW[2])

def d_cad_f(c, x, y):          # vista de frente (lugar do fundo, de frente para a câmera)
    w = 13; x0 = x - w // 2
    shadow(c, x, y, w + 4, 70)
    post(c, x0, y - 29, y - 4); post(c, x0 + w - 2, y - 29, y - 4)               # montantes traseiros (sobem até o encosto)
    c.rect(x0, y - 29, w, 3, TIMB[3]); c.hline(x0, y - 29, w, TIMB[4]); c.hline(x0, y - 27, w, TIMB[1])   # travessa superior
    for yy in (y - 24, y - 20): c.rect(x0 + 2, yy, w - 4, 2, TIMB[2]); c.hline(x0 + 2, yy, w - 4, TIMB[3]); c.hline(x0 + 2, yy + 1, w - 4, TIMB[1])
    _seat_top(c, x0 - 1, w + 2, y - 11, 6)
    c.rect(x0 - 1, y - 11, w + 2, 2, TIMB[3]); c.hline(x0 - 1, y - 11, w + 2, TIMB[4]); c.hline(x0 - 1, y - 9, w + 2, TIMB[0])
    post(c, x0, y - 9, y); post(c, x0 + w - 2, y - 9, y); c.hline(x0 + 2, y - 4, w - 4, TIMB[1]); c.hline(x0, y - 1, 2, TIMB[0]); c.hline(x0 + w - 2, y - 1, 2, TIMB[0])

def d_cad_b(c, x, y):          # vista de costas (lugar da frente, encosto voltado para a câmera)
    w = 13; x0 = x - w // 2
    shadow(c, x, y, w + 4, 70)
    post(c, x0, y - 9, y); post(c, x0 + w - 2, y - 9, y); c.hline(x0, y - 1, 2, TIMB[0]); c.hline(x0 + w - 2, y - 1, 2, TIMB[0])
    c.rect(x0 - 1, y - 13, w + 2, 3, TIMB[1]); c.hline(x0 - 1, y - 13, w + 2, TIMB[2])   # sob o assento
    c.rect(x0, y - 28, w, 16, TIMB[2]); c.vline(x0, y - 28, 16, TIMB[3]); c.vline(x0 + w - 1, y - 28, 16, TIMB[1])
    c.rect(x0, y - 29, w, 3, TIMB[3]); c.hline(x0, y - 29, w, TIMB[4]); c.hline(x0, y - 27, w, TIMB[1])
    for yy in (y - 24, y - 20, y - 16): c.rect(x0 + 2, yy, w - 4, 2, TIMB[3]); c.hline(x0 + 2, yy, w - 4, TIMB[4]); c.hline(x0 + 2, yy + 1, w - 4, TIMB[0])

def d_cad_s(c, x, y, face):    # perfil: face='right' → quem senta olha para a direita (encosto à esquerda)
    w = 11; x0 = x - w // 2; fl = face == 'left'
    X = lambda dx, ww=1: (x0 + (w - dx - ww)) if fl else (x0 + dx)
    shadow(c, x, y, w + 5, 70)
    c.rect(X(0, 2), y - 29, 2, 25, TIMB[2]); c.vline(X(0, 2) + (1 if fl else 0), y - 29, 25, TIMB[3] if not fl else TIMB[1])          # montante traseiro
    c.rect(X(0, 3), y - 29, 3, 3, TIMB[3]); c.hline(X(0, 3), y - 29, 3, TIMB[4])
    for yy in (y - 23, y - 19): c.rect(X(1, 1), yy, 1, 2, TIMB[1])
    sx = x0 - 1 if not fl else x0 - 1
    _seat_top(c, x0 - 1, w + 2, y - 11, 5)
    c.rect(x0 - 1, y - 11, w + 2, 2, TIMB[3]); c.hline(x0 - 1, y - 11, w + 2, TIMB[4]); c.hline(x0 - 1, y - 9, w + 2, TIMB[0])
    c.rect(X(w - 3, 2), y - 9, 2, 9, TIMB[2]); c.vline(X(w - 3, 2), y - 9, 9, TIMB[3] if not fl else TIMB[1])          # perna da frente
    c.rect(X(0, 2), y - 9, 2, 9, TIMB[2]); c.vline(X(0, 2), y - 9, 9, TIMB[3] if not fl else TIMB[1])                 # perna de trás
    c.hline(x0 + 2, y - 4, w - 4, TIMB[1]); c.hline(X(w - 3, 2), y - 1, 2, TIMB[0]); c.hline(X(0, 2), y - 1, 2, TIMB[0])

# ---------------------------------------------------------------- cadeira de balanço (3/4, virada para o interior; braços, encosto de palhinha, patins curvos)
def d_cadeira_balanco(c, x, y):
    shadow(c, x, y + 2, 28, 70)
    # patins curvos (lado visível à esquerda em perfil; lado direito de frente)
    pts = [(x - 13, y - 11), (x - 12, y - 6), (x - 10, y - 2), (x - 6, y + 1), (x - 1, y + 2)]
    for (a, b), (a2, b2) in zip(pts, pts[1:]): c.line(a, b, a2, b2, TIMB[3]); c.line(a, b + 1, a2, b2 + 1, TIMB[0])
    c.line(x + 7, y - 3, x + 8, y + 1, TIMB[2]); c.line(x + 8, y + 1, x + 9, y + 2, TIMB[3]); c.hline(x + 5, y + 2, 5, TIMB[0])
    c.line(x - 1, y + 2, x + 9, y + 2, TIMB[3]); c.hline(x - 1, y + 3, 10, TIMB[0])
    # lado em perfil (esquerda da tela): montante de trás, braço inclinado, perna
    post(c, x - 12, y - 31, y - 9, 2); c.rect(x - 13, y - 31, 4, 2, TIMB[3]); c.hline(x - 13, y - 31, 4, TIMB[4])
    c.line(x - 12, y - 24, x - 6, y - 21, TIMB[3]); c.line(x - 12, y - 25, x - 6, y - 22, TIMB[4]); c.line(x - 12, y - 23, x - 6, y - 20, TIMB[1])
    c.line(x - 11, y - 8, x - 8, y - 3, TIMB[2])                                  # perna de trás sobre o patim
    # frente: encosto de palhinha, assento, braço direito, pernas
    post(c, x - 6, y - 36, y - 11, 2); post(c, x + 6, y - 36, y - 11, 2)
    c.rect(x - 7, y - 38, 16, 3, TIMB[3]); c.hline(x - 7, y - 38, 16, TIMB[4]); c.hline(x - 7, y - 36, 16, TIMB[1])     # travessa curva do alto
    c.rect(x - 4, y - 35, 10, 18, STRAW[2])
    for k in range(0, 18, 2): c.hline(x - 4, y - 35 + k, 10, STRAW[3] if k % 4 == 0 else STRAW[1])
    for k in range(0, 10, 2): c.vline(x - 4 + k, y - 35, 18, STRAW[1] if k % 4 == 0 else STRAW[4])
    c.vline(x - 4, y - 35, 18, TIMB[1]); c.vline(x + 5, y - 35, 18, TIMB[1]); c.hline(x - 4, y - 17, 10, TIMB[1])
    _seat_top(c, x - 8, 17, y - 11, 7)
    c.rect(x - 5, y - 17, 12, 3, RED[3]); c.hline(x - 5, y - 17, 12, RED[4]); c.hline(x - 5, y - 15, 12, RED[1]); c.pset(x - 2, y - 16, SACK[3]); c.pset(x + 3, y - 16, SACK[3])   # almofada de retalho
    c.rect(x - 8, y - 11, 17, 2, TIMB[3]); c.hline(x - 8, y - 11, 17, TIMB[4]); c.hline(x - 8, y - 9, 17, TIMB[0])
    post(c, x - 7, y - 9, y - 1, 2); post(c, x + 6, y - 9, y - 1, 2)
    c.rect(x + 8, y - 24, 4, 2, TIMB[3]); c.hline(x + 8, y - 24, 4, TIMB[4]); post(c, x + 9, y - 22, y - 11, 2)        # braço direito (visto de frente)

# ---------------------------------------------------------------- guarda-roupa (encostado à parede: base a 9 px do rodapé; face de cima visível)
def d_armario(c, x, y):
    w, h = 36, 56; x0 = x - w // 2
    shadow(c, x, y, w + 4, 80); sh(c, x0 + 2, y - 2, w - 4, 2, 60)
    for lx in (x0 + 1, x0 + w - 4): c.rect(lx, y - 4, 3, 4, TIMB[1]); c.vline(lx, y - 4, 4, TIMB[2]); c.hline(lx, y - 1, 3, TIMB[0])
    # face de cima (profundidade 9 px) encostada na parede
    tp = mix(TIMB[3], TIMB[4], .45)
    c.rect(x0 - 1, y - h - 9, w + 2, 9, tp); c.hline(x0 - 1, y - h - 9, w + 2, TIMB[2]); c.vline(x0 - 1, y - h - 9, 9, TIMB[4]); c.vline(x0 + w, y - h - 9, 9, TIMB[2])
    for k in range(x0 + 3, x0 + w - 3, 5): c.pset(k, y - h - 6 + (k // 5) % 3, mix(tp, SACK[3], .35))               # poeira
    c.shade(x0 - 1, y - h - 9, w + 2, 2, SH1)
    # frente
    c.rect(x0, y - h, w, h - 4, TIMB[2]); c.vline(x0, y - h, h - 4, TIMB[3]); c.vline(x0 + w - 1, y - h, h - 4, TIMB[1])
    c.rect(x0 - 1, y - h, w + 2, 4, TIMB[3]); c.hline(x0 - 1, y - h, w + 2, TIMB[4]); c.hline(x0 - 1, y - h + 3, w + 2, TIMB[0])      # cornija
    # portas com almofadas (esquerda: espelho)
    for i, dx0 in enumerate((x0 + 2, x0 + w // 2 + 1)):
        dw = w // 2 - 3
        c.rect(dx0, y - h + 6, dw, h - 24, TIMB[1]); c.rect(dx0 + 1, y - h + 7, dw - 2, h - 26, TIMB[3]); c.hline(dx0 + 1, y - h + 7, dw - 2, TIMB[4]); c.vline(dx0 + 1, y - h + 7, h - 26, TIMB[4])
    mx, my, mw, mh = x0 + 4, y - h + 9, w // 2 - 7, 24
    c.rect(mx - 1, my - 1, mw + 2, mh + 2, TIMB[1]); c.rect(mx, my, mw, mh, (150, 180, 196)); c.poly([(mx + 1, my + mh - 2), (mx + 6, my + 1), (mx + 8, my + 1), (mx + 3, my + mh - 2)], (206, 228, 236)); c.hline(mx, my, mw, (112, 138, 156))
    rx, ry, rw_, rh_ = x0 + w // 2 + 4, y - h + 9, w // 2 - 7, 24                                                        # almofada entalhada da porta direita
    c.rect(rx, ry, rw_, rh_, TIMB[2]); c.hline(rx, ry, rw_, TIMB[4]); c.vline(rx, ry, rh_, TIMB[3]); c.vline(rx + rw_ - 1, ry, rh_, TIMB[1]); c.hline(rx, ry + rh_ - 1, rw_, TIMB[1])
    c.poly([(rx + rw_ // 2, ry + 6), (rx + rw_ - 3, ry + 12), (rx + rw_ // 2, ry + 18), (rx + 2, ry + 12)], TIMB[1])
    c.rect(x0 + w // 2 - 1, y - h + 6, 2, h - 24, TIMB[0])                                                             # junção das portas
    c.rect(x0 + w // 2 - 3, y - 34, 1, 5, BREAD[3]); c.pset(x0 + w // 2 - 3, y - 34, BREAD[4]); c.rect(x0 + w // 2 + 2, y - 34, 1, 5, BREAD[3]); c.pset(x0 + w // 2 + 2, y - 34, BREAD[4])   # puxadores
    # gavetas
    for i, dx0 in enumerate((x0 + 2, x0 + w // 2 + 1)):
        dw = w // 2 - 3; c.rect(dx0, y - 15, dw, 9, TIMB[1]); c.rect(dx0 + 1, y - 14, dw - 2, 7, TIMB[3]); c.hline(dx0 + 1, y - 14, dw - 2, TIMB[4]); c.hline(dx0 + 1, y - 8, dw - 2, TIMB[1])
        c.rect(dx0 + dw // 2 - 1, y - 11, 3, 1, BREAD[3]); c.pset(dx0 + dw // 2, y - 11, BREAD[4])
    c.hline(x0, y - 5, w, TIMB[0]); c.shade(x0, y - 6, w, 2, SH1)

# ---------------------------------------------------------------- filtro de barro sobre suporte de madeira (encostado à parede), com caneca
def d_talha(c, x, y):
    w = 22; x0 = x - w // 2
    shadow(c, x, y, w + 4, 80)
    for lx in (x0 + 1, x0 + w - 4): post(c, lx, y - 16, y, 3); c.hline(lx, y - 1, 3, TIMB[0])                        # pernas da frente
    c.rect(x0 + 3, y - 7, w - 6, 2, TIMB[2]); c.hline(x0 + 3, y - 7, w - 6, TIMB[3]); c.hline(x0 + 3, y - 5, w - 6, TIMB[0])  # prateleira baixa
    c.rect(x0 + 4, y - 14, 7, 7, CLAY[1]); c.hline(x0 + 4, y - 14, 7, CLAY[2]); c.hline(x0 + 5, y - 15, 5, CLAY[3])      # pote de barro embaixo (reserva de água)
    c.rect(x0, y - 19, w, 3, TIMB[2]); c.hline(x0, y - 19, w, TIMB[4]); c.hline(x0, y - 17, w, TIMB[0])                  # saia
    top = mix(TIMB[3], TIMB[4], .5)
    c.rect(x0 - 1, y - 27, w + 2, 8, top); c.hline(x0 - 1, y - 27, w + 2, TIMB[2]); c.vline(x0 - 1, y - 27, 8, TIMB[4]); c.vline(x0 + w, y - 27, 8, TIMB[2]); c.hline(x0 - 1, y - 20, w + 2, TIMB[4])
    for k in range(x0 + 2, x0 + w - 2, 6): c.pset(k, y - 23, TIMB[2]); c.pset(k + 1, y - 22, TIMB[2])               # veio
    # filtro (corpo cerâmico com tampa), no fundo do tampo
    fx = x - 4; fb = y - 24
    c.poly([(fx - 7, fb - 14), (fx + 7, fb - 14), (fx + 8, fb - 7), (fx + 6, fb), (fx - 6, fb), (fx - 8, fb - 7)], CLAY[2])
    c.vline(fx - 7, fb - 13, 11, CLAY[4]); c.vline(fx - 6, fb - 12, 10, CLAY[3]); c.vline(fx + 7, fb - 13, 11, CLAY[1]); c.hline(fx - 7, fb - 8, 15, CLAY[3]); c.hline(fx - 6, fb - 7, 13, CLAY[1])
    c.rect(fx - 8, fb - 17, 16, 3, CLAY[3]); c.hline(fx - 8, fb - 17, 16, CLAY[4]); c.hline(fx - 8, fb - 15, 16, CLAY[1])              # borda
    c.rect(fx - 6, fb - 20, 12, 3, TIMB[3]); c.hline(fx - 6, fb - 20, 12, TIMB[4]); c.pset(fx, fb - 21, TIMB[1]); c.pset(fx - 1, fb - 21, TIMB[2]); c.pset(fx + 1, fb - 21, TIMB[2])   # tampa de madeira
    c.rect(fx - 2, fb - 6, 4, 2, BREAD[3]); c.pset(fx - 2, fb - 6, BREAD[4]); c.rect(fx - 1, fb - 4, 2, 2, BREAD[2]); c.pset(fx, fb - 2, (150, 190, 214))   # torneira de latão e gota
    # caneca esmaltada sob a torneira (na frente do corpo)
    mx = fx - 2; my = y - 21
    c.rect(mx, my - 5, 5, 5, ENAM[4]); c.hline(mx, my - 5, 5, ENAM[4]); c.vline(mx + 4, my - 5, 5, ENAM[2]); c.hline(mx, my - 1, 5, ENAM[1]); c.pset(mx + 5, my - 4, ENAM[3]); c.pset(mx + 6, my - 3, ENAM[3]); c.pset(mx + 5, my - 2, ENAM[3]); c.hline(mx + 1, my - 5, 3, (190, 220, 236))
    c.shade(x0 - 1, y - 19, w + 2, 2, SH1)

# ---------------------------------------------------------------- planta em vaso de barro (costela-de-adão), folhas com volume
def d_planta_casa(c, x, y):
    shadow(c, x, y, 18, 70)
    c.hline(x - 7, y - 1, 15, CLAY[0]); c.rect(x - 6, y - 3, 13, 2, CLAY[1]); c.hline(x - 6, y - 3, 13, CLAY[2])            # prato
    c.poly([(x - 6, y - 14), (x + 6, y - 14), (x + 5, y - 3), (x - 5, y - 3)], CLAY[2]); c.vline(x - 6, y - 13, 9, CLAY[4]); c.vline(x - 5, y - 13, 9, CLAY[3]); c.vline(x + 5, y - 13, 9, CLAY[1]); c.hline(x - 5, y - 7, 11, CLAY[1])
    c.rect(x - 7, y - 17, 15, 4, CLAY[3]); c.hline(x - 7, y - 17, 15, CLAY[4]); c.hline(x - 7, y - 14, 15, CLAY[1]); c.rect(x - 6, y - 18, 13, 1, (62, 42, 34))   # borda + terra
    base = (x, y - 18)
    leaves = [(-74, 11, 4), (-46, 16, 5), (-20, 21, 5), (4, 24, 5), (28, 20, 5), (52, 15, 4), (74, 10, 4)]
    for ang, L, W in sorted(leaves, key=lambda t: -abs(t[0])):
        a = math.radians(ang); pts_l, pts_r, mid = [], [], []
        for i in range(0, 13):
            t = i / 12; px = base[0] + math.sin(a) * L * t * 1.0; py = base[1] - math.cos(a) * L * t + (L * .45 * t * t if abs(ang) > 40 else L * .18 * t * t)
            wv = W * math.sin(math.pi * min(1, t * 1.05)) ** .75 * .5 + .4; nx, ny = math.cos(a), math.sin(a)
            pts_l.append((round(px - nx * wv), round(py - ny * wv * .0 - 0))); pts_r.append((round(px + nx * wv), round(py))); mid.append((round(px), round(py)))
        dark = LEAF[1] if abs(ang) > 60 else LEAF[2]; lite = LEAF[3] if ang < 20 else LEAF[2]
        c.poly(pts_l + mid[::-1], lite if ang < 0 else dark); c.poly(pts_r + mid[::-1], dark if ang < 0 else lite)
        for p, q in zip(mid, mid[1:]): c.line(p[0], p[1], q[0], q[1], LEAF[4] if ang < 10 else LEAF[3])
        c.pset(*pts_l[-3], LEAF[4]) if ang < 0 else None

# ---------------------------------------------------------------- tapete têxtil (desenhado no piso do cenário-base; sem alpha)
def draw_rug(c, rx0, ry0, rw, rh, seed=5):
    import random; rng = random.Random(seed)
    F, F2 = (142, 76, 62), (160, 92, 72); OCH, TEAL, CRE, NAV = (200, 160, 94), (92, 122, 116), (214, 202, 176), (66, 82, 108)
    def edge(x, k): return int(round(.8 * math.sin(x / 7.0 + k) + rng.choice((0, 0, 0, 1)) * .0))
    for y in range(ry0 - 2, ry0 + rh + 3):
        for x in range(rx0 - 1, rx0 + rw + 1):
            dx = min(x - rx0, rx0 + rw - 1 - x); dy = min(y - ry0, ry0 + rh - 1 - y) + (edge(x, 1) if y < ry0 + rh // 2 else edge(x, 3))
            d = min(dx + (edge(y, 5) if x < rx0 + rw // 2 else edge(y, 7)), dy)
            if d < 0: continue
            if d <= 1: col = NAV
            elif d <= 4: col = CRE if (x + y) % 4 else mix(CRE, (170, 150, 130), .5)
            elif d <= 5: col = NAV
            elif d <= 8: col = OCH if (d == 6 or d == 8) else F
            elif d == 9: col = NAV
            else:
                col = F if (x + y) % 2 else F2
                if y % 3 == 0: col = mix(col, DK, .10)
            if (x * 7 + y * 13) % 41 == 0 and d > 1: col = mix(col, (236, 222, 200), .25)       # fio claro solto
            c.pset(x, y, col)
    # motivo central: fileira de losangos (ocre/azul-petróleo/creme)
    cy = ry0 + rh // 2; n = (rw - 28) // 16
    for k in range(n):
        cx = rx0 + 14 + 8 + k * 16 + ((rw - 28) - n * 16) // 2
        for r_, col in ((8, OCH), (6, F), (5, TEAL), (2, CRE)):
            c.poly([(cx, cy - r_), (cx + r_ + 1, cy), (cx, cy + r_), (cx - r_ - 1, cy)], col)
        for sx in (-1, 1): c.pset(cx + sx * 11, cy, OCH); c.pset(cx + sx * 12, cy - 1, OCH); c.pset(cx + sx * 12, cy + 1, OCH)
    # franjas nas pontas, de comprimento irregular
    for yy in range(ry0 + 1, ry0 + rh - 1, 2):
        for side in (-1, 1):
            L = 2 + (yy * 5 + side) % 3; x1 = rx0 - 1 if side < 0 else rx0 + rw
            for k in range(L): c.pset(x1 + side * k, yy, CRE if k < L - 1 else mix(CRE, (150, 130, 110), .5))
    # espessura e contato: 1 px escuro na borda inferior + sombra no assoalho
    c.hline(rx0 + 1, ry0 + rh, rw - 2, mix(NAV, DK, .45)); c.shade(rx0, ry0 + rh + 1, rw, 1, SH2); c.shade(rx0 + 2, ry0 + rh + 2, rw - 2, 1, SH1)
    c.shade(rx0 + rw, ry0 + 2, 1, rh, SH1)
