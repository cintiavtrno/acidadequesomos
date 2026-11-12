"""Manequins de escala (NÃO são a arte de Lia): silhuetas neutras só para validar proporção, câmera e oclusão."""
from pxl import *

FW, FH = 16, 44
BODY = ramp(214, 0.14, (0.28, 0.40, 0.52, 0.64, 0.76))
SKIN = ramp(214, 0.10, (0.40, 0.52, 0.64, 0.74, 0.84))

def draw(c, ox, kind, view, phase):
    """kind: 'adult' (42 px = 1,75 m) | 'lia' (33 px = 1,38 m). Âncora dos pés: x=ox+8, y=FH-1."""
    H = 42 if kind == 'adult' else 33
    legs = 20 if kind == 'adult' else 14
    torso = 14 if kind == 'adult' else 11
    sh = 10 if kind == 'adult' else 8            # largura dos ombros
    top = FH - H
    head_y = top; head_h = 7
    cx = ox + 8
    bob = 1 if phase in (1, 3) else 0
    # pernas
    leg_y = FH - legs
    if view == 'side':
        a = [0, 3, 0, -3][phase]
        for k, off in enumerate((a, -a)):
            col = BODY[1] if k == 0 else BODY[2]
            x = cx - 1 + off
            c.rect(x, leg_y - bob, 3, legs + bob, col)
            c.rect(x + (1 if off >= 0 else 0), FH - 2, 4, 2, BODY[0])       # pé
    else:
        a = [0, 1, 0, 1][phase]
        c.rect(cx - 4, leg_y - bob, 3, legs + bob - (a if phase == 1 else 0), BODY[2]); c.rect(cx + 1, leg_y - bob, 3, legs + bob - (a if phase == 3 else 0), BODY[1])
        c.rect(cx - 4, FH - 2 - (a if phase == 1 else 0), 3, 2, BODY[0]); c.rect(cx + 1, FH - 2 - (a if phase == 3 else 0), 3, 2, BODY[0])
        c.vline(cx - 4, leg_y - bob, legs + bob, BODY[3])
    # tronco
    ty = head_y + head_h + 1 - bob
    tw = sh if view != 'side' else 6
    tx = cx - tw // 2
    c.rect(tx, ty, tw, torso, BODY[3] if view != 'back' else BODY[2])
    c.vline(tx, ty, torso, BODY[4]); c.vline(tx + tw - 1, ty, torso, BODY[1]); c.hline(tx, ty + torso - 1, tw, BODY[1])
    # braços
    arm_len = torso - 2
    if view == 'side':
        sw = [0, 2, 0, -2][phase]
        c.rect(cx - 1 - sw, ty + 1, 2, arm_len, BODY[2]); c.vline(cx - 1 - sw, ty + 1, arm_len, BODY[3])
    else:
        c.rect(tx - 2, ty + 1, 2, arm_len, BODY[2]); c.rect(tx + tw, ty + 1, 2, arm_len, BODY[1])
        c.vline(tx - 2, ty + 1, arm_len, BODY[3])
    # cabeça
    hy = head_y - bob
    hw = 6
    c.rect(cx - hw // 2, hy + 1, hw, head_h - 1, SKIN[3]); c.rect(cx - 2, hy, 4, 1, SKIN[3])
    c.vline(cx - hw // 2, hy + 1, head_h - 1, SKIN[4]); c.vline(cx + hw // 2 - 1, hy + 1, head_h - 1, SKIN[1])
    c.hline(cx - hw // 2 + 1, hy + head_h - 1, hw - 2, SKIN[2])
    if view == 'side': c.rect(cx + 2, hy + 3, 1, 2, SKIN[4])                 # marca do rosto (nariz) -> direção
    if view == 'back': c.rect(cx - hw // 2, hy, hw, 3, BODY[1])                # calota (cabelo) para distinguir costas
    if view == 'front': c.hline(cx - 1, hy + 4, 3, SKIN[1])

def sheet(kind):
    views = ['side', 'front', 'back']
    c = C(FW * 4, FH * 3)
    for r, v in enumerate(views):
        for p in range(4):
            t = C(FW, FH); draw(t, 0, kind, v, p)
            c.paste(t, p * FW, r * FH)
    return c

if __name__ == '__main__':
    sheet('adult').save('../assets/mannequin_adult.png'); sheet('lia').save('../assets/mannequin_lia.png')
    from PIL import Image
    a = Image.open('../assets/mannequin_adult.png'); b = Image.open('../assets/mannequin_lia.png')
    out = Image.new('RGBA', (a.width * 2 + 8, a.height), (200, 190, 175, 255)); out.paste(a, (0, 0), a); out.paste(b, (a.width + 8, 0), b)
    out.resize((out.width * 5, out.height * 5), Image.NEAREST).save('../preview/mannequins.png')
