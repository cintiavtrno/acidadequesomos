import sys, json
from playwright.sync_api import sync_playwright
q = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else None; wait = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
with sync_playwright() as p:
    b = p.chromium.launch(args=['--no-sandbox', '--allow-file-access-from-files']); pg = b.new_page(viewport={'width': 980, 'height': 640})
    msgs = []; pg.on('console', lambda m: msgs.append(m.type + ': ' + m.text)); pg.on('pageerror', lambda e: msgs.append('ERR ' + str(e)))
    pg.goto('file:///home/claude/balcao/game/index_casa_dev.html?' + q); pg.wait_for_timeout(wait)
    print('\n'.join(msgs[:10])); print(pg.title())
    if out: pg.screenshot(path=out)
    b.close()
