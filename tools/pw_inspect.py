import sys
from playwright.sync_api import sync_playwright
from PIL import Image, ImageStat
page = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch(args=['--no-sandbox', '--allow-file-access-from-files']); pg = b.new_page(viewport={'width': 1280, 'height': 760})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file:///home/claude/balcao/game/' + page + '?new=1&t=10:30'); pg.wait_for_timeout(1200)
    ids = pg.evaluate("INSPECT.filter(i=>i.scene===S.scene).map(i=>i.id)")
    bad = []
    for i in ids:
        pg.evaluate("(id)=>{focusOn(id)}", i); pg.wait_for_timeout(250)
        box = pg.evaluate("(()=>{const r=document.querySelector('canvas').getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()")
        pg.screenshot(path='/tmp/_i.png', clip={'x': box[0], 'y': box[1], 'width': box[2], 'height': box[3]})
        im = Image.open('/tmp/_i.png').convert('L'); m = ImageStat.Stat(im).mean[0]; z = pg.evaluate("S.zl+' '+V.z+' '+V.left+','+V.top")
        print(i, 'brilho médio', round(m), 'zl/z/view', z); 
        if m < 25: bad.append(i)
        pg.screenshot(path=f'/tmp/ins_{i}.png', clip={'x': box[0], 'y': box[1], 'width': box[2], 'height': box[3]})
    print('PRETOS:', bad, errs); b.close()
