import json
from playwright.sync_api import sync_playwright
url = 'file:///home/claude/balcao/game/balcao_etapa6_rua.html'
res = []
def ok(name, cond, extra=''): res.append((name, bool(cond), extra)); print(('PASS' if cond else 'FAIL'), name, extra)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 800}); errs = []
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(url + '?t=215&x=190&new=1'); pg.wait_for_timeout(600)
    ev = lambda s: pg.evaluate(s)
    ok('relógio 10:35+', ev("BALCAO.SIM.clock.min") >= 635)
    ok('Raimundo longe da mesa', ev("BALCAO.SIM.npcs.raimundo.state") != 'Sitting')
    ok('E vago', ev("!BALCAO.SIM.assentos.E.ocup"))
    ok('mesa pausada', ev("BALCAO.SIM.mesa.fase") in ('pausado', 'esperando'))
    # conversa
    ev("BALCAO.abrirConversa('ze')"); pg.wait_for_timeout(200)
    ok('diálogo aberto', ev("BALCAO.D.open") and 'Seu Zé' in pg.inner_text('#dlg'))
    pg.screenshot(path='out/ui_dialogo.png')
    ev("dlgAct('topicos')"); pg.wait_for_timeout(100); t = pg.inner_text('#dlg'); ok('tópicos contextuais (sem motivo, só o que ela já pode perguntar)', 'Posso jogar' not in t and ('motivo' in t or 'Observe' in t or len(t) > 40))
    ev("dlgAct('perguntar','lia_jogar')"); pg.wait_for_timeout(150)
    ok('resposta de Zé', 'contar até seis' in pg.inner_text('#dlg'))
    ok('kp convite', ev("!!BALCAO.SIM.kp.kp_dom_convite"))
    ok('convidada', ev("!!BALCAO.SIM.liaConvidada"))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(100); ok('diálogo fechado', not ev("BALCAO.D.open"))
    # ir e sentar
    ev("entrarMesa('E')"); pg.wait_for_timeout(9000)
    st = ev("[BALCAO.LS.mode, BALCAO.SIM.lia.seat, BALCAO.SIM.lia.x, BALCAO.SIM.lia.y]"); print(st)
    ok('Lia sentada em E', st[0] == 'seated' and st[1] == 'E')
    pg.wait_for_timeout(5000)
    ok('mesa jogando com Lia', ev("BALCAO.SIM.mesa.fase") in ('jogando', 'embaralhando', 'reagindo'), ev("BALCAO.SIM.mesa.fase"))
    # espera vez da Lia
    jog = 0
    for i in range(60):
        pg.wait_for_timeout(1500)
        if ev("BALCAO.S.mesaOpen"):
            vez = ev("(() => { const P = BALCAO.SIM.mesa.pensando; return !!(P && P.liaEsperando && !P.jogou) })()")
            if vez:
                lg = ev("BALCAO.SIM.mesa.legaisLia().map(o=>o.t)")
                if lg: ev("liaJoga(%d,%d)" % (lg[0][0], lg[0][1])); jog += 1
                else: ev("liaPassa()"); jog += 1
                if jog == 1: pg.screenshot(path='out/ui_mesa_painel.png')
        if jog >= 3: break
    ok('Lia jogou 3 vezes', jog >= 3, str(jog))
    ev("closeMesa()"); pg.wait_for_timeout(300); pg.screenshot(path='out/ui_lia_sentada.png')
    st = ev("BALCAO.SIM.mesa.stats"); print(st); ok('jogadas totais', st['jogadas'] > 3)
    ev("levantar()"); pg.wait_for_timeout(1500); ok('Lia levantou', ev("BALCAO.LS.mode") == 'free' and ev("!BALCAO.SIM.assentos.E.ocup"))
    # examinar objeto
    ev("BALCAO.examinar(BALCAO.SIM.scene.inst.find(i=>i.id==='orelhao_1'))"); pg.wait_for_timeout(200); ok('kp orelhão', ev("!!BALCAO.SIM.kp.kp_obj_orelhao"))
    ev("BALCAO.toggleNotes(true)"); pg.wait_for_timeout(200); pg.screenshot(path='out/ui_notas.png'); ok('anotações', 'Anotações da rua' in pg.inner_text('#notes'))
    ok('sem erros de console', not errs, str(errs[:3]))
    b.close()
print(sum(1 for r in res if r[1]), '/', len(res))
