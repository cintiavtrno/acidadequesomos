import sys
from playwright.sync_api import sync_playwright
page = sys.argv[1]; out = sys.argv[2]; tab = sys.argv[3] if len(sys.argv) > 3 else 'entender'; sp = int(sys.argv[4]) if len(sys.argv) > 4 else 0
with sync_playwright() as p:
    b = p.chromium.launch(args=['--no-sandbox', '--allow-file-access-from-files']); pg = b.new_page(viewport={'width': 1280, 'height': 760})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file:///home/claude/balcao/game/' + page + '?new=1&t=10:30'); pg.wait_for_timeout(1200)
    pg.evaluate("""([tab,sp])=>{for(const k of Sim.Data.conhecimentos){try{SIM.knowledge.award(k.id)}catch(e){}} DIARY.tab=tab;DIARY.sp=sp;toggleDiary(true);}""", [tab, sp])
    pg.wait_for_timeout(400); pg.screenshot(path=out); print(errs); b.close()
