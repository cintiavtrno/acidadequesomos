import json, math, os
from PIL import Image
from pipeline import frame, CW, CH, SCALE
from anim import ANIMS, pose_for, GAIT, speed
OUT='/home/claude/balcao/assets/chars'; os.makedirs(OUT, exist_ok=True)
DIRS4={'down':0,'right':90,'up':180,'left':270}
DIRS8={'down':0,'down_right':45,'right':90,'up_right':135,'up':180,'up_left':225,'left':270,'down_left':315}
SERVE=['serve_idle','serve_wrap','serve_give','serve_write','serve_greet']
PAD=2
def build(who, persp):
    D=0 if persp=='side' else 16
    dirs=DIRS4 if persp=='side' else DIRS8
    names=['idle','walk','turn','talk','interact','interact_high']+(['sit'] if persp=='tq' else [])
    rows=[]
    for a in names:
        for dn,y in dirs.items(): rows.append((a,dn,y))
    if who=='aurea' and persp=='tq':
        for a in SERVE: rows.append((a,'down',0))
    cols=8
    W=cols*(CW+PAD)+PAD; H=len(rows)*(CH+PAD)+PAD
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); atlas=dict(cell=[CW,CH],anchor=[20,46],pad=PAD,cols=cols,persp=persp,rows={},speed_mps=speed(who)*SCALE[who],scale=SCALE[who],gait=GAIT[who])
    for r,(a,dn,y) in enumerate(rows):
        n=ANIMS[a][0]
        for k in range(n):
            im=frame(who,pose_for(who,a,k,math.radians(y)),D)
            sh.alpha_composite(im,(PAD+k*(CW+PAD),PAD+r*(CH+PAD)))
        fps=ANIMS[a][1] or (8/GAIT[who]['T'])
        atlas['rows'][f'{a}/{dn}']=dict(row=r,n=n,fps=fps,loop=ANIMS[a][2])
    sh.save(f'{OUT}/{who}_{persp}.png'); json.dump(atlas,open(f'{OUT}/{who}_{persp}.json','w'),indent=1)
    return sh,rows
if __name__=='__main__':
    import sys
    whos=sys.argv[1].split(',') if len(sys.argv)>1 else ['lia','aurea','raimundo','dandara','lucia']
    for who in whos:
        for p in (('tq',) if who in ('raimundo','dandara','lucia') else ('side','tq')):
            sh,rows=build(who,p); print(who,p,sh.size,len(rows))
