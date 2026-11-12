import sys
from playwright.sync_api import sync_playwright
from PIL import Image
ids = sys.argv[1].split(','); out = sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(args=['--no-sandbox', '--allow-file-access-from-files']); pg = b.new_page(viewport={'width': 980, 'height': 640})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    shots = []
    for sid in ids:
        pg.goto('file:///home/claude/balcao/game/index_casa_dev.html?new=1&t=10:30'); pg.wait_for_timeout(900)
        pg.evaluate("""(sid)=>{const n=SIM.npcs.raimundo,s=SIM.seats[sid];n.loc='casa';n.seat=s;n.x=s.x;n.y=s.y;n.face=s.face;n.state='Sitting';n.act=null;n.setAnim&&n.setAnim('sit');SIM.update=()=>{};}""", sid)
        pg.wait_for_timeout(500); pg.screenshot(path='/tmp/_s.png'); shots.append((sid, Image.open('/tmp/_s.png').copy()))
    b.close()
print(errs)

seat_xy = {'cad_frente': (172, 190), 'cad_esq': (145, 200), 'cad_dir': (199, 200), 'cad_sul': (172, 223), 'balanco_1': (207, 144)}
tiles = []
for sid, im in shots:
    x, y = seat_xy[sid]; cx, cy = 130 + x * 1.5, 66 + y * 1.5
    tiles.append(im.crop((int(cx - 60), int(cy - 70), int(cx + 60), int(cy + 50))).resize((360, 360), Image.NEAREST))
sheet = Image.new('RGB', (360 * len(tiles), 360))
for i, t in enumerate(tiles): sheet.paste(t, (360 * i, 0))
sheet.save(out)
