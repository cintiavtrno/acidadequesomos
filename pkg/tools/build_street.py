import sys
from PIL import Image
from street import *
from far import far_layer, FAR_W

def run():
    world, placed = compose_street()
    far = far_layer()
    world.save('../assets/street_world.png')
    far.save('../assets/street_far.png')
    return world, placed, far

def view(world, far, cam, par=0.35):
    v = Image.new('RGBA', (VW, VH))
    fx = int(cam * par)
    v.paste(far.im.crop((fx, 0, fx + VW, VH)), (0, 0))
    v.alpha_composite(world.im.crop((cam, 0, cam + VW, VH)))
    return v

if __name__ == '__main__':
    world, placed, far = run()
    for cam in (0, 320, 650):
        view(world, far, cam).resize((VW * 2, VH * 2), Image.NEAREST).save(f'../preview/street_cam{cam}.png')
    print([(p['name'], p['x0'], p.get('door_x'), p['ytop']) for p in placed])
