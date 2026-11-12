import sys, json, asyncio
from playwright.sync_api import sync_playwright
url = 'file:///home/claude/balcao/game/balcao_etapa6_rua.html'
def run(q, out, wait=800, w=1280, h=800, actions=None):
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': w, 'height': h}); errs = []
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None); pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(url + q); pg.wait_for_timeout(wait)
        if actions: actions(pg)
        pg.screenshot(path=out); t = pg.title(); b.close(); return errs, t
if __name__ == '__main__':
    e, t = run(sys.argv[1], sys.argv[2]); print(e[:5]); print(t[:400])
