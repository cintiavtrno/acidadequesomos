from PIL import Image
from pipeline import *
from anim import *
import sys
who=sys.argv[1]; D=int(sys.argv[2]); anim=sys.argv[3]; yaw=math.radians(float(sys.argv[4]))
n=ANIMS[anim][0]
ims=[frame(who,pose_for(who,anim,k,yaw),D) for k in range(n)]
sh=Image.new('RGBA',(CW*n,CH),(96,104,110,255))
for i,im in enumerate(ims): sh.alpha_composite(im,(i*CW,0))
sh=sh.resize((sh.width*4,sh.height*4),Image.NEAREST); sh.save(f'/tmp/a_{who}_{anim}.png')
