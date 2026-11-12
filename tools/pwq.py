import sys, json
from playwright.sync_api import sync_playwright
url = sys.argv[1]; out = sys.argv[2]; js = sys.argv[3] if len(sys.argv) > 3 else ''; wait = int(sys.argv[4]) if len(sys.argv) > 4 else 1200
with sync_playwright() as p:
    b = p.chromium.launch(args=['--no-sandbox', '--allow-file-access-from-files']); pg = b.new_page(viewport={'width': 960, 'height': 540})
    msgs = []; pg.on('console', lambda m: msgs.append(m.type + ': ' + m.text)); pg.on('pageerror', lambda e: msgs.append('ERR ' + str(e)))
    pg.goto(url); pg.wait_for_timeout(wait)
    if js: print(pg.evaluate(js)); pg.wait_for_timeout(500)
    print('\n'.join(msgs[:10])); pg.screenshot(path=out); b.close()
