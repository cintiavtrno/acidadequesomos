from playwright.sync_api import sync_playwright
url='file:///home/claude/balcao/game/balcao_etapa6_rua.html'
res=[]
def ok(n,c,x=''): res.append(c); print('PASS' if c else 'FAIL',n,x)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1280,'height':800});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
    pg.goto(url+'?t=95&x=262&new=1');pg.wait_for_timeout(700);ev=pg.evaluate
    ev("BALCAO.SIM.lia.x=300;BALCAO.SIM.lia.y=BALCAO.SIM.yw?0:236");ev("BALCAO.abrirMesa()");pg.wait_for_timeout(200);ok('escolha aberta',ev("BALCAO.D.open&&BALCAO.D.id")=='__mesa')
    pg.screenshot(path='out/ctx_escolha.png')
    pg.keyboard.press('1');pg.wait_for_timeout(300);ok('animando',ev("!!BALCAO.CTX.anim"))
    pg.screenshot(path='out/ctx_meio.png');pg.wait_for_timeout(1000)
    ok('contexto mesa ativo',ev("BALCAO.CTX.active")=='mesa' and ev("BALCAO.S.zl")==2)
    m0=ev("JSON.stringify(BALCAO.SIM.mesa.game.placar)+BALCAO.SIM.mesa.stats.jogadas")
    pg.wait_for_timeout(5000);pg.screenshot(path='out/ctx_perto.png')
    ok('partida continua durante o zoom',ev("BALCAO.SIM.mesa.stats.jogadas")>int(m0.split(']')[1]),m0)
    j1=ev("BALCAO.SIM.mesa.stats.jogadas");pg.keyboard.press('Escape');pg.wait_for_timeout(1500)
    ok('câmera voltou',ev("BALCAO.CTX.active")is None and ev("BALCAO.S.zl")==0 and not ev("BALCAO.S.free"),ev("[BALCAO.S.zl,BALCAO.S.free]"))
    pg.wait_for_timeout(2500);ok('partida segue após sair (não reinicia)',ev("BALCAO.SIM.mesa.stats.jogadas")>=j1 and ev("BALCAO.SIM.mesa.game.mao")>=1)
    ok('sem erros',not errs,str(errs[:3]));b.close()
print(sum(res),'/',len(res))
