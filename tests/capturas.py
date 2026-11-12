import base64, io
from playwright.sync_api import sync_playwright
from PIL import Image
url = 'file:///home/claude/balcao/game/balcao_etapa6_rua.html'
def grab(pg):
    d = pg.evaluate("document.getElementById('c').toDataURL('image/png')"); return Image.open(io.BytesIO(base64.b64decode(d.split(',')[1]))).convert('RGB')
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(); errs = []
    def page(q, wait=900):
        pg = b.new_page(viewport={'width': 1280, 'height': 800}); pg.on('pageerror', lambda e: errs.append(str(e))); pg.goto(url + q); pg.wait_for_timeout(wait); return pg
    # visão geral: 3 recortes costurados
    full = Image.new('RGB', (1130, 270))
    for cam in (0, 325, 650):
        pg = page('?new=1&t=125&x=%d&z=0&vx=%d' % (cam + 240, cam + 240)); full.paste(grab(pg), (cam, 0)); pg.close()
    full.save('out/rua_visao_geral.png')
    spots = {'dominó': ('?new=1&t=95&x=300&z=2&vx=240&vy=212', 'rua_dom.png'), 'oiti_canteiros': ('?new=1&t=125&x=1040&z=2&vx=1030&vy=212', 'rua_oiti.png'), 'padaria_frente': ('?new=1&t=125&x=430&z=2&vx=470&vy=190', 'rua_padaria.png'),
             'associacao': ('?new=1&t=135&x=700&z=2&vx=740&vy=190', 'rua_assoc.png'), 'varal_b5': ('?new=1&t=15&x=930&z=2&vx=1000&vy=195', 'rua_varal.png'), 'orelhao': ('?new=1&t=185&x=580&z=2&vx=620&vy=205', 'rua_orelhao.png'), 'barbearia': ('?new=1&t=60&x=100&z=2&vx=100&vy=200', 'rua_barbearia.png')}
    for k, (q, f) in spots.items():
        pg = page(q); grab(pg).save('out/' + f); pg.close()
    print(errs); b.close()
