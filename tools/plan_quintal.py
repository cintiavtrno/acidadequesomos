# Gera a planta esquemática (vista superior) e a vista 3/4 de referência do quintal (Etapa 8.3). Não é arte final.
from PIL import Image, ImageDraw, ImageFont
import os
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
import glob
_f=(glob.glob('/usr/share/fonts/**/DejaVuSans.ttf',recursive=True) or [None])[0]
F = ImageFont.truetype(_f,10) if _f else ImageFont.load_default()
# x,y,w,d,h (m); y=0 = parede de fundo
O = [
 ('lenha',0.2,0.5,0.7,2.2,.7,'#a9774a'),('trempe+panelão',1.4,0.6,1.3,1.0,.5,'#7a4b32'),('fogão gás',3.1,0.1,0.9,0.7,.9,'#d8d4cc'),
 ('bancada',4.3,0.1,2.5,0.8,.9,'#b88a5a'),('talha',7.0,0.1,0.6,0.6,1.0,'#b5623f'),('tanque',0.2,3.5,1.0,0.8,.9,'#9aa7a8'),
 ('banco',2.4,3.0,0.6,0.5,.45,'#a9774a'),('banco',3.6,3.3,0.6,0.5,.45,'#a9774a'),('pilão',5.4,2.7,0.5,0.5,.5,'#8b6a4a'),
 ('esteio',2.5,4.8,0.3,0.3,2.6,'#6b4a2f'),('esteio',7.2,4.8,0.3,0.3,2.6,'#6b4a2f'),
 ('aparador serviço',9.8,0.1,3.4,0.9,.9,'#b88a5a'),('oferenda',14.0,0.2,1.2,0.9,.7,'#eadfd0'),
 ('MESA',11.5,3.6,5.0,1.0,.75,'#c79a63'),('cad',11.75,2.7,.5,.5,.9,'#a9774a'),('cad',13.05,2.7,.5,.5,.9,'#a9774a'),('cad',14.35,2.7,.5,.5,.9,'#a9774a'),('cad',15.65,2.7,.5,.5,.9,'#a9774a'),
 ('cab',10.8,3.85,.5,.5,.9,'#a9774a'),('cab',16.7,3.85,.5,.5,.9,'#a9774a'),('banco longo',12.0,4.7,3.0,0.45,.45,'#a9774a'),
 ('mesa crianças',17.8,5.8,1.8,0.8,.5,'#c79a63'),('mangueira',22.2,2.0,0.8,0.8,6.0,'#5b4330'),('mesa dominó',20.0,3.8,1.2,1.2,.75,'#c79a63'),
 ('cad',20.35,3.1,.5,.5,.9,'#a9774a'),('cad',20.35,5.1,.5,.5,.9,'#a9774a'),('cad',19.3,4.2,.5,.5,.9,'#a9774a'),('cad',21.4,4.2,.5,.5,.9,'#a9774a'),
 ('banco conversa',24.0,4.6,2.0,0.5,.45,'#a9774a'),('cadeira Rita',23.8,2.6,.6,.6,1.0,'#8d5a6a'),('meio-fio',25.0,6.4,2.5,0.4,.35,'#9a958b'),
 ('banco espera',0.8,6.4,1.6,0.5,.45,'#a9774a'),('lavatório',9.2,5.6,.5,.5,.9,'#b5623f'),
]
ZONES = [('Z1 COZINHA',0,0,7.6,5.0,'#e9a15b'),('Z2 SERVIÇO',9.8,0,3.4,1.0,'#e8d36a'),('Z3 MESA',10.5,2.6,6.7,2.6,'#8fc47a'),
 ('Z4 MANGUEIRA / CONVIVÊNCIA',18.5,1.0,9.0,6.2,'#7aa9d8'),('Z5 RECEPÇÃO',0,5.3,7.4,2.7,'#b79ad8'),('OFERENDA',13.8,0,1.6,1.1,'#f0b6c8')]
NPC = [('Lia',4.5,7.5,'#2aa198'),('Zefa',2.0,2.1,'#d9534f'),('Cícera',2.9,3.7,'#e6c33a'),('Nonato',10.0,5.6,'#e6c33a'),('Zé',21.0,2.8,'#6fa8dc'),('Júnior',14.0,7.2,'#e0705a')]
ROUTES = [[(4.5,8),(4.5,7.2),(10.2,7.2),(10.2,5.6)],[(8.6,0.3),(8.6,2.0),(17.3,2.0),(18.4,3.0),(18.4,7.2)],[(3.2,2.2),(8.6,2.2)],[(1.0,7.4),(27,7.4)],[(28,3.8),(24.7,3.8),(24.1,3.2)]]
def plan():
    S=26; ML=40; MT=40; W=int(28*S)+ML*2; H=int(8*S)+MT+70
    im=Image.new('RGB',(W,H),'#f4efe6'); d=ImageDraw.Draw(im)
    P=lambda x,y:(ML+x*S,MT+y*S)
    d.rectangle([*P(0,0),*P(28,8)],fill='#e9dcc3',outline='#333',width=1)
    for i in range(0,29,2):
        d.line([*P(i,0),*P(i,8)],fill='#d6c8aa'); d.text((P(i,0)[0]-4,MT-26),str(i)+'m',fill='#555',font=F)
    for j in range(0,9,2): d.line([*P(0,j),*P(28,j)],fill='#d6c8aa'); d.text((8,P(0,j)[1]-4),str(j)+'m',fill='#555',font=F)
    ov=Image.new('RGBA',im.size,(0,0,0,0)); od=ImageDraw.Draw(ov)
    for n,x0,y0,w_,d_,c in ZONES:
        x1,y1=x0+w_,y0+d_; rgb=tuple(int(c[i:i+2],16) for i in (1,3,5)); od.rectangle([*P(x0,y0),*P(x1,y1)],fill=rgb+(70,),outline=rgb+(200,))
    im.paste(Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB')); d=ImageDraw.Draw(im)
    for n,x0,y0,x1,y1,c in ZONES: d.text((P(x0,y0)[0]+3,P(x0,y0)[1]+2),n,fill='#222',font=F)
    # copa da mangueira
    cx,cy=P(22.6,2.4); r=3.4*S; d.ellipse([cx-r,cy-r,cx+r,cy+r],outline='#3c7a3c',width=2)
    d.text((cx-22,cy-r-12),'copa (overlay)',fill='#3c7a3c',font=F)
    for n,x,y,w,dd,h,c in O:
        d.rectangle([*P(x,y),*P(x+w,y+dd)],fill=c,outline='#333')
        if n not in('cad','cab','banco','esteio'): d.text((P(x,y)[0]+2,P(x,y)[1]+1),n[:12],fill='#111',font=F)
    # paredes
    d.rectangle([*P(0,-0.25),*P(28,0)],fill='#8a7a66'); d.text((P(11.2,-0.25)[0],P(11,-.25)[1]+1),'parede da casa (0–11 m) · muro 3 m (11–28 m)',fill='#fff',font=F)
    d.rectangle([*P(7.9,-0.25),*P(9.2,0)],fill='#2f6f8f'); d.text((P(7.0,-0.25)[0],P(7,-.25)[1]+10),'porta de serviço',fill='#2f6f8f',font=F)
    d.rectangle([*P(4.8,-0.25),*P(6.0,0)],fill='#d9c35a')
    d.rectangle([*P(28,3.2),*P(28.25,4.4)],fill='#2f6f8f'); d.text((P(25.4,3.2)[0],P(25,3.2)[1]-12),'portão de Rita →',fill='#2f6f8f',font=F)
    d.rectangle([*P(3.5,8),*P(5.5,8.25)],fill='#2f6f8f'); d.text((P(3.3,8.25)[0],P(3,8.3)[1]+2),'soleira / corredor da rua',fill='#2f6f8f',font=F)
    for r in ROUTES:
        d.line([P(*p) for p in r],fill='#d62728',width=2)
        a=P(*r[-1]); d.ellipse([a[0]-3,a[1]-3,a[0]+3,a[1]+3],fill='#d62728')
    for n,x,y,c in NPC:
        p=P(x,y); d.ellipse([p[0]-6,p[1]-6,p[0]+6,p[1]+6],fill=c,outline='#000'); d.text((p[0]-8,p[1]+7),n,fill='#000',font=F)
    ly=MT+8*S+20
    d.text((ML,ly),'Planta esquemática (vista superior) · 1 m = 26 px nesta imagem · quintal 28 m × 8 m · chão y=0 (fundos) a y=8 (frente)',fill='#000',font=F)
    d.text((ML,ly+14),'Vermelho = rotas · pontos coloridos = posições iniciais da fase A · entradas: soleira (convidados), porta de serviço (Zefa/casa), portão (Rita)',fill='#000',font=F)
    d.text((ML,ly+28),'Zonas: laranja cozinha · amarelo serviço · verde mesa · azul mangueira/convivência · roxo recepção · rosa oferenda (revisar)',fill='#000',font=F)
    im.save('out/quintal_planta.png')
def vista():
    Z=2; W,H=720,270; im=Image.new('RGB',(W*Z,H*Z),'#cfe3ee'); d=ImageDraw.Draw(im)
    X=lambda m:(24+24*m)*Z; Y=lambda m:(124+16*m)*Z
    d.rectangle([0,0,W*Z,28*Z],fill='#bcd9ea')  # céu / telhados vizinhos
    d.rectangle([0,28*Z,264*Z+24*Z,124*Z],fill='#e2b98a')   # parede da casa 0-11 m
    d.rectangle([(24+264)*Z,52*Z,W*Z,124*Z],fill='#d9c9a8')  # muro 3 m
    d.rectangle([0,124*Z,W*Z,252*Z],fill='#c9a77c'); d.rectangle([0,252*Z,W*Z,270*Z],fill='#8a7a66')
    d.rectangle([X(8.0),(124-55)*Z,X(9.2),124*Z],fill='#2f6f8f'); d.rectangle([X(4.8),(124-60)*Z,X(6.0),(124-36)*Z],fill='#e6d27a')
    d.polygon([(X(21),52*Z),(X(27.5),52*Z),(X(27.5),30*Z),(X(23),20*Z)],fill='#b5623f')  # telhado de Rita sobre o muro
    d.text((X(21.3),38*Z),'telhado de Rita (fundo)',fill='#fff',font=F)
    d.rectangle([X(0),30*Z,X(7.6),44*Z],fill='#a14b2e'); d.text((X(1),32*Z),'telhado do puxadinho (só sobre a parede)',fill='#fff',font=F)
    order=sorted(O,key=lambda o:o[2]+o[4])
    items=[(o[2]+o[4],'o',o) for o in order]+[(y+0.0,'n',(n,x,y,c)) for n,x,y,c in NPC]
    items.sort(key=lambda t:t[0]); k=0
    for base,t,o in items:
        if t=='o':
            n,x,y,w,dd,h,c=o; x0=X(x); x1=X(x+w); yb=Y(y+dd); yt=yb-h*24*Z
            if n=='mangueira': d.rectangle([x0,Y(2.0)-150*Z,x1,yb],fill='#5b4330'); d.ellipse([X(19.4),0,X(25.8),90*Z],fill='#4f8a4a'); continue
            d.rectangle([x0,yt,x1,yb],fill=c,outline='#333'); d.rectangle([x0,yb-dd*16*Z,x1,yb],outline='#555')
        else:
            n,x,y,c=o; px=X(x); yb=Y(y); d.rectangle([px-5*Z,yb-42*Z,px+5*Z,yb],fill=c,outline='#000'); d.text((px-8*Z,yb+2),n,fill='#000',font=F)
        k+=1
    d.text((6,6),'Vista 3/4 de referência (720×270 px, câmera 480×270 segue Lia) · 1 m = 24 px (alturas) · 16 px/m (profundidade) · ordem = base y',fill='#000',font=F)
    d.text((6,18),'Copa da mangueira = camada de cima (translúcida quando alguém está sob ela) · telhado do puxadinho só sobre a parede, sem cobrir o chão',fill='#000',font=F)
    im.save('out/quintal_vista34.png')
plan(); vista(); print('ok')
