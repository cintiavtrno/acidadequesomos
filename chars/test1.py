import sys, time
from PIL import Image
from pipeline import *
poses=[('front',0),('side R',math.pi/2),('back',math.pi),('side L',3*math.pi/2),('dl',math.radians(315)),('ur',math.radians(135))]
for who in ('lia','aurea'):
  for D,name in ((0,'side'),(16,'tq')):
    t=time.time(); ims=[frame(who,dict(yaw=y),D) for n,y in poses]
    sh=Image.new('RGBA',(CW*len(ims)+4*len(ims),CH),(96,104,110,255))
    for i,im in enumerate(ims): sh.alpha_composite(im,(i*(CW+4),0))
    sh.resize((sh.width*4,sh.height*4),Image.NEAREST).save(f'/tmp/t_{who}_{name}.png'); print(who,name,round(time.time()-t,1),'s')
