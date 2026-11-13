import math, os
from PIL import Image, ImageDraw
import drv96
OUT='/home/claude/out96/final'; os.makedirs(OUT, exist_ok=True)
BG=(214,200,170,255); CW,CH=40,52
P=['perc1','perc2','perc3','perc4','perc5','perc6']; C=['cantor']; E=['cam1','cam2','assist','carga','diretor']
DIRS=[('baixo',0),('direita',90),('cima',180),('esquerda',270)]
def grid(items, scale):   # items: list of frame lists (all same length) -> list of images
    n=max(len(i) for i in items); out=[]
    for k in range(n):
        im=Image.new('RGBA',((CW+2)*len(items)+2,CH+4),BG)
        for j,fr in enumerate(items): im.alpha_composite(fr[k%len(fr)],(2+j*(CW+2),2))
        out.append(im.resize((im.width*scale,im.height*scale),Image.NEAREST))
    return out
def gif(frames,path,ms):
    frames[0].convert('P',palette=Image.ADAPTIVE).save(path,save_all=True,append_images=[f.convert('P',palette=Image.ADAPTIVE) for f in frames[1:]],duration=ms,loop=0,disposal=2)
# 1) elenco parado: 4 direções por personagem
rows=[]
for w in P+C+E:
    rows.append([drv96.fr(w,'idle',0,y) for _,y in DIRS])
sc=6; cols=4
W=(CW+2)*cols+2; H=(CH+2)*len(rows)+2
im=Image.new('RGBA',(W,H),BG)
for r,fs in enumerate(rows):
    for c,f in enumerate(fs): im.alpha_composite(f,(2+c*(CW+2),2+r*(CH+2)))
im.resize((W*sc,H*sc),Image.NEAREST).save(f'{OUT}/elenco_parado.png')
# 2) caminhada e animações por grupo (direita), GIF
def anim_set(whos, a, n, yaw): return [[drv96.fr(w,a,k,yaw) for k in range(n)] for w in whos]
gif(grid(anim_set(P,'drum',4,90),6),f'{OUT}/percussionistas_tocando_lado.gif',170)
gif(grid(anim_set(P,'drum',4,0),6),f'{OUT}/percussionistas_tocando_frente.gif',170)
gif(grid(anim_set(P,'drumwalk',8,90),6),f'{OUT}/percussionistas_andando_lado.gif',110)
gif(grid(anim_set(P,'drumwalk',8,0),6),f'{OUT}/percussionistas_andando_frente.gif',110)
gif(grid(anim_set(C,'walk',8,90)+anim_set(C,'walk',8,0)+anim_set(C,'sway',4,0)*2+anim_set(C,'wave',4,0)*2+anim_set(C,'pose',4,0)*2,6),f'{OUT}/cantor.gif',130)
gif(grid(anim_set(E,'walk',8,90)+anim_set(E,'walk',8,0),6),f'{OUT}/equipe_andando.gif',110)
gif(grid([[drv96.fr('cam1','film',k,90) for k in range(4)],[drv96.fr('cam2','film',k,90) for k in range(4)],[drv96.fr('assist','note',k,0) for k in range(4)],[drv96.fr('assist','radio',k,90) for k in range(4)],[drv96.fr('carga','carry',k,90) for k in range(4)],[drv96.fr('diretor','watch',k,0) for k in range(4)],[drv96.fr('diretor','point',k,90) for k in range(4)]],6),f'{OUT}/equipe_trabalhando.gif',220)
print('ok')
