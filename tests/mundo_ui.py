# Testes do mundo integrado no navegador (Etapa 7). Uso: python3 tests/mundo_ui.py
import json, sys
from playwright.sync_api import sync_playwright
URL = 'file:///home/claude/balcao/game/balcao_etapa7_mundo.html'
res = []
def ok(n, c, x=''):
    res.append(bool(c)); print(('PASS ' if c else 'FAIL ') + n + (' · ' + str(x) if x != '' else ''))
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 800}); errs = []
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(URL + '?new=1&skip=1&ano=1994'); pg.wait_for_function('window.MUNDO', timeout=30000); pg.wait_for_timeout(1500)
    ev = lambda s: pg.evaluate(s)
    ok('mundo montado, rua ativa', ev('MUNDO.cena()') == 'rua')
    ok('três jogos carregados, só um visível', ev("[...document.querySelectorAll('iframe')].filter(f=>f.classList.contains('on')).length") == 1)
    pg.screenshot(path='out/m_rua.png')
    # Lia caminha até a porta da padaria e usa a dica contextual
    ev("MUNDO.W('rua').BALCAO.SIM.lia.x = 470; MUNDO.W('rua').BALCAO.SIM.lia.y = MUNDO.W('rua').eval('Sim.Rua.D.yw(470)')+12"); pg.wait_for_timeout(500)
    hint = ev("(()=>{const t=JSON.parse(MUNDO.W('rua').document.title);return t.hint})()")
    ok('dica contextual na porta da padaria', hint and 'padaria' in hint.lower(), hint)
    ev("MUNDO.W('rua').BALCAO.pressAction()"); pg.wait_for_timeout(1500)
    ok('Lia entrou na padaria (3/4)', ev('MUNDO.cena()') == 'padaria')
    pg.screenshot(path='out/m_padaria.png')
    pos = ev("(()=>{const S=MUNDO.W('padaria').BALCAO.S;return [Math.round(S.p.x),Math.round(S.p.y),S.scene]})()")
    ok('Lia chega na entrada da padaria', pos[2] == 'interior' and abs(pos[0]-240) < 6 and pos[1] > 200, pos)
    # sair andando para baixo até a soleira
    pg.keyboard.down('ArrowDown'); pg.wait_for_timeout(1800); pg.keyboard.up('ArrowDown'); pg.wait_for_timeout(1500)
    ok('saindo pela soleira volta à rua', ev('MUNDO.cena()') == 'rua', ev('MUNDO.cena()'))
    lp = ev("(()=>{const L=MUNDO.W('rua').BALCAO.SIM.lia;return [Math.round(L.x),Math.round(L.y)]})()")
    ok('Lia reaparece diante da porta da padaria', abs(lp[0]-470) < 4, lp)
    pg.screenshot(path='out/m_rua2.png')
    # casa
    ev("MUNDO.W('rua').BALCAO.SIM.lia.x = 164; MUNDO.W('rua').BALCAO.SIM.lia.y = MUNDO.W('rua').eval('Sim.Rua.D.yw(164)')+12"); pg.wait_for_timeout(500)
    ev("MUNDO.W('rua').BALCAO.pressAction()"); pg.wait_for_timeout(1500)
    ok('entrou na casa de Seu Raimundo', ev('MUNDO.cena()') == 'casa')
    pg.screenshot(path='out/m_casa.png')
    pg.keyboard.down('ArrowDown'); pg.wait_for_timeout(1800); pg.keyboard.up('ArrowDown'); pg.wait_for_timeout(1500)
    ok('descendo a escada volta à rua', ev('MUNDO.cena()') == 'rua')
    # continuidade: Raimundo vai à padaria pela rua e a Lia o encontra lá
    ev("MUNDO.mundo.avancarAte(525)"); pg.wait_for_timeout(300)
    ev("MUNDO.W('rua').BALCAO.SIM.lia.x = 470; MUNDO.W('rua').BALCAO.SIM.lia.y = MUNDO.W('rua').eval('Sim.Rua.D.yw(470)')+12"); pg.wait_for_timeout(400)
    onde = ev('MUNDO.onde()'); ok('às 08:45 Raimundo está na padaria (ou a caminho)', onde['raimundo'] in ('padaria', 'rua'), onde)
    ev("MUNDO.mundo.avancarAte(580)")
    ev("MUNDO.W('rua').BALCAO.pressAction()"); pg.wait_for_timeout(1500)
    r = ev("(()=>{const n=MUNDO.W('padaria').BALCAO.SIM.npcs.raimundo;return [n.state,n.loc]})()")
    ok('Lia entra e encontra Seu Raimundo na padaria', ev('MUNDO.cena()') == 'padaria' and r[1] == 'padaria', r)
    pg.screenshot(path='out/m_padaria_raimundo.png')
    ev("MUNDO.mundo.ir('padaria:porta')"); pg.wait_for_timeout(1500)
    ev("MUNDO.mundo.avancarAte(720)")
    c = ev("(()=>{const n=MUNDO.W('casa').BALCAO.SIM.npcs.raimundo;return [n.state,n.loc]})()")
    ok('depois do pão, Seu Raimundo voltou para casa', c[1] == 'casa' and c[0] != 'Away', c)
    ok('ninguém duplicado', ev('MUNDO.duplicados().length') == 0, ev('MUNDO.duplicados()'))
    ok('sem erros de console', not errs, errs[:3])
    b.close()
print(sum(res), '/', len(res)); sys.exit(0 if all(res) else 1)
