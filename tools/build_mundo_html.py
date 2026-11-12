"""Monta o protótipo do mundo conectado (Etapa 7): um shell com os três jogos já aprovados (rua, padaria, casa), cada um no seu iframe.
Nada dos jogos é reconstruído: os ganchos (portas, chegada da Lia, parâmetros) entram como substituições de texto sobre os HTML já gerados."""
import base64, re, json, os
G = '../game/'
def lerr(n): return open(G + n, encoding='utf-8').read()
def sub(t, old, new, n=1):
    assert t.count(old) >= 1, 'não achei: ' + old[:80]
    return t.replace(old, new, n)

RATE = '3'   # minutos de jogo por segundo real: 07:00→19:00 em ~4 min (uma partida de ~15 min com 4 épocas). PROPOSTA
HEAD = """<script>window.MUNDO_ATIVO = true; window.MUNDO_RATE = 3; window.MUNDO_SAIR = function (c) { parent.MUNDO_BRIDGE.sair(c); }; window.MUNDO_ENTRAR = function (c, p) { return parent.MUNDO_BRIDGE.entrar(c, p); };
(function () { var q = location.search; if (/mundo=1/.test(q)) return; })();</script>
"""
def args(t, extra):  # parâmetros de URL padrão: o srcdoc não tem query; injeta o location.search esperado
    return sub(t, 'const Q = new URLSearchParams(location.search);', "const Q = new URLSearchParams('" + extra + "');")

# --- rua
rua = lerr('balcao_etapa6_rua.html')
rua = args(rua, '?mundo=1&rate=' + RATE + '')
rua = sub(rua, '<head>', '<head>\n' + HEAD)
# --- padaria: sai pela porta da frente → rua
pad = lerr('balcao_etapa4_simulacao.html')
pad = args(pad, '?s=interior&rate=' + RATE + '&mundo=1')
pad = sub(pad, "if (p.y > YF - 1 && Math.abs(p.x - EXIT_X) <= 24) startFade('street');",
          "if (p.y > YF - 1 && Math.abs(p.x - EXIT_X) <= 24) { if (window.MUNDO_ATIVO) { p.y = YF - 14; p.tx = null; p.ty = null; p.path = []; p.goal = null; window.MUNDO_SAIR('padaria'); } else startFade('street'); }")
pad = sub(pad, 'window.BALCAO = {', "window.MUNDO_LIA = function () { S.scene = 'interior'; S.p.x = EXIT_X; S.p.y = YF - 12; S.p.dir = 'u'; S.p.face = 'up'; S.p.tx = null; S.p.ty = null; S.p.path = []; S.p.goal = null; try { if (D.open) closeDialog(); } catch (e) { } snapCamera(); };\nwindow.BALCAO = {")
pad = sub(pad, '<head>', '<head>\n' + HEAD)
# --- quintal (Etapa 8.6): porta lateral da rua → quintal
rua = sub(rua, "porta_sobrado: { cena: 'casa', label: 'Entrar na casa de Seu Raimundo' } };", "porta_sobrado: { cena: 'casa', label: 'Entrar na casa de Seu Raimundo' }, porta_lateral: { cena: 'quintal', label: 'Entrar no quintal de Dona Zefa' } };")
qui = lerr('balcao_etapa8_quintal.html')
qui = sub(qui, '<head>', '<head>\n' + HEAD)
# --- casa: desce a escada → rua
casa = lerr('balcao_etapa5_casa.html')
casa = args(casa, '?rate=' + RATE + '&mundo=1')
casa = re.sub(r"if \(p\.y > YF - 1 && Math\.abs\(p\.x - EXIT_X\) <= 24\) \{ p\.y = YF - 14; p\.tx = null; p\.ty = null; p\.path = \[\]; p\.goal = null; say\('A escada desce para a rua[^\n]*?\); \}",
              "if (p.y > YF - 1 && Math.abs(p.x - EXIT_X) <= 24) { p.y = YF - 14; p.tx = null; p.ty = null; p.path = []; p.goal = null; if (window.MUNDO_ATIVO) window.MUNDO_SAIR('casa'); else say('A escada desce para a rua.', 5); }", casa, count=1)
assert 'MUNDO_SAIR' in casa, 'gancho da casa não aplicado'
casa = sub(casa, 'A escada desce para a rua (a descida entra na Etapa 6)', 'Desça a escada para sair para a rua')
casa = sub(casa, 'window.BALCAO = {', "window.MUNDO_LIA = function () { S.scene = 'interior'; S.p.x = EXIT_X; S.p.y = YF - 14; S.p.dir = 'u'; S.p.face = 'up'; S.p.tx = null; S.p.ty = null; S.p.path = []; S.p.goal = null; try { if (D.open) closeDialog(); } catch (e) { } snapCamera(); };\nwindow.BALCAO = {")
casa = sub(casa, '<head>', '<head>\n' + HEAD)

b64 = lambda t: base64.b64encode(t.encode('utf-8')).decode()
SH = open('../mundo/shell_template.html', encoding='utf-8').read()
SH = SH.replace('/*MUNDO_JS*/', open('../mundo/mundo.js', encoding='utf-8').read().replace('</script', '<\\/script'))
SH = SH.replace('/*SRC*/{}', json.dumps({'rua': b64(rua), 'padaria': b64(pad), 'casa': b64(casa), 'quintal': b64(qui)}))
open(G + 'balcao_etapa7_mundo.html', 'w', encoding='utf-8').write(SH)
print('ok', round(len(SH) / 1e6, 1), 'MB')
