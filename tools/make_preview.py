from PIL import Image, ImageDraw, ImageFont
from build_street import *
import street
world = Image.open('../assets/street_world.png'); far = Image.open('../assets/street_far.png')
base = Image.open('../assets/bakery_interior_base.png'); counter = Image.open('../assets/bakery_counter.png')
adult = Image.open('../assets/mannequin_adult.png'); lia = Image.open('../assets/mannequin_lia.png')
def spr(sh, row=0, ph=0, flip=False):
    f = sh.crop((ph * 16, row * 44, ph * 16 + 16, row * 44 + 44))
    return f.transpose(Image.FLIP_LEFT_RIGHT) if flip else f
def put(im, sh, x, y, row=0, flip=False):
    # sombra
    d = ImageDraw.Draw(im, 'RGBA'); d.rectangle([x - 5, y - 1, x + 4, y - 1], fill=(18, 10, 28, 90)); d.rectangle([x - 6, y, x + 5, y], fill=(18, 10, 28, 90)); d.rectangle([x - 4, y + 1, x + 3, y + 1], fill=(18, 10, 28, 90))
    im.alpha_composite(spr(sh, row, 0, flip), (x - 8, y - 43))
def street_view(cam):
    v = view(C_from(world), C_from(far), cam) if False else None
def sv(cam):
    v = Image.new('RGBA', (480, 270)); fx = int(cam * 0.35)
    v.paste(far.crop((fx, 0, fx + 480, 270)), (0, 0)); v.alpha_composite(world.crop((cam, 0, cam + 480, 270)))
    return v
A = sv(300); put(A, lia, 470 - 300, street.f_ground(470)); put(A, adult, 528 - 300, street.f_ground(528), 0, True)
B = sv(0); put(B, lia, 150, street.f_ground(150))
Cc = sv(650); put(Cc, adult, 400, street.f_ground(1050))
I = base.copy()
put(I, adult, 262, 152, 1); put(I, lia, 240, 232, 2)
I2 = base.copy(); put(I2, lia, 190, 212, 0); I2.alpha_composite(counter); put(I2, adult, 262, 152, 1)
# monta: antes do balcão o personagem de trás deve ser desenhado antes -> refaz
I = base.copy(); put(I, adult, 262, 152, 1); I.alpha_composite(counter); put(I, lia, 240, 232, 2)
S = 2
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18) if True else None
try: fsm = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
except Exception: fsm = None
W = 480 * S * 2 + 30; H = 60 + 270 * S + 50 + 270 * S + 50
out = Image.new('RGB', (W, H), (20, 15, 18)); d = ImageDraw.Draw(out)
def tile(im, x, y, label, sub=None):
    out.paste(im.convert('RGB').resize((480 * S, 270 * S), Image.NEAREST), (x, y))
    d.text((x, y - 24), label, fill=(240, 226, 204), font=font)
    if sub: d.text((x, y + 270 * S + 6), sub, fill=(150, 136, 120), font=fsm)
d.text((10, 8), 'O balcão da vó — Etapa 1: cenário-base (1991, manhã) · 480×270 nativo, mostrado a 2×', fill=(240, 226, 204), font=font)
y1 = 60; y2 = y1 + 270 * S + 50
tile(A, 10, y1, 'Rua · side-view (câmera ortográfica lateral)', 'porta da padaria: 52×66 px (2,2 × 2,75 m) · Lia 33 px · adulto 42 px')
tile(I, 20 + 480 * S, y1, 'Interior · 3/4 oblíquo (frente + topo)', 'pé direito 4 m (96 px) · piso 16 px/m de profundidade · adulto atrás do balcão: oclusão correta')
tile(B, 10, y2, 'Rua · extremo esquerdo (rua sobe)', 'sobrado amarelo de Seu Raimundo à esquerda da padaria')
tile(Cc, 20 + 480 * S, y2, 'Rua · extremo direito (desce para o largo)', 'casa de porta azul, fachada verde e casa baixa; telhados escalonam com o declive')
out.save('../preview/etapa1_previa.png'); print(out.size)
