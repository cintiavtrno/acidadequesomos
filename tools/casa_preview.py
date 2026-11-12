import json
from PIL import Image
base = Image.open('../assets/casa_interior_base.png').convert('RGBA'); sc = json.load(open('../assets/objects/scene_casa.json')); cat = json.load(open('../assets/objects/catalog_casa.json'))
sheet = Image.open('../assets/objects/casa_objetos.png').convert('RGBA'); by = {a['sprite']: a for a in cat['assets']}
def draw(i, on=None):
    key = i['sprite'] + ('#0' if i['frames'] > 1 else '')
    a = by[key]; x, y, w, h = a['rect']; base.alpha_composite(sheet.crop((x, y, x + w, y + h)), (int(i['sx']), int(i['sy'])))
for i in sorted([i for i in sc['instancias'] if i['layer'] == 'wall' and 'visivel_se' not in i], key=lambda i: i['base']): draw(i)
for i in sorted([i for i in sc['instancias'] if i['layer'] != 'wall' and 'visivel_se' not in i], key=lambda i: i['base']): draw(i)
import sys
z = int(sys.argv[1]) if len(sys.argv) > 1 else 2
base.resize((480 * z, 270 * z), Image.NEAREST).save('/tmp/casa_prev.png')
