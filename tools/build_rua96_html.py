"""Monta a página jogável da rua de 1996 (etapa D): cenário de assets/street96, elenco de 1996 e motor leve (sim/s96_*.js).
Não altera 1991/1994. Saída: game/balcao_rua96.html e rua96.html (raiz do repositório)."""
import base64, json, re, os
B = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/'
A = B + 'assets/'
T = open(B + 'game/rua96_template.html').read()
old = open(B + 'game/template.html').read()
css = re.search(r'<style>(.*?)</style>', old, re.S).group(1)
fit = re.search(r'<script>(// fit\.js.*?)</script>', open(B + 'game/rua_template.html').read(), re.S).group(1)
def uri(p): return 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
S = A + 'street96/'
FARL = {'far_' + k: uri(S.rsplit('street96', 1)[0] + 'far/rua96_%s.png' % k) for k in ['sky', 'clouds', 'hill', 'casas']}
assets = {'far': uri(S + 'far.png'), 'world': uri(S + 'world.png'), 'front': uri(S + 'front.png'), 'props': uri(S + 'props.png')}
assets.update(FARL)
atlas = {}
elenco = open(B + 'sim/s96_elenco.js').read()
import subprocess
js = "const fs=require('fs');eval(fs.readFileSync('%ssim/s1_core.js','utf8')+';global.Sim=Sim;');eval(fs.readFileSync('%ssim/s96_rua.js','utf8')+';global.Sim96=Sim96;');eval(fs.readFileSync('%ssim/s96_elenco.js','utf8'));console.log(JSON.stringify([...new Set(Sim96.Elenco.atores.map(a=>a.who))]))" % (B, B, B)
whos = sorted(json.loads(subprocess.check_output(['node', '-e', js])))
for who in whos:
    assets[who + '_side'] = uri(A + 'chars/%s_side.png' % who); atlas[who + '_side'] = json.load(open(A + 'chars/%s_side.json' % who))
assets['lia_side6'] = uri(A + 'chars/lia_side6.png'); atlas['lia_side6'] = json.load(open(A + 'chars/lia_side6.json'))
scene = json.load(open(S + 'scene_rua96.json')); props = json.load(open(S + 'props.json'))
sim = '\n'.join(open(B + 'sim/' + f).read() for f in ['s1_core.js', 's2_nav.js', 's96_rua.js', 's96_elenco.js', 's96_trama.js'])
def put(k, v):
    global T
    assert k in T, k
    T = T.replace(k, v, 1)
put('/*CSS*/', css); put('/*FITJS*/', fit); put('/*CHARS_JS*/', open(B + 'game/chars.js').read()); put('/*SIM_JS*/', sim)
put('/*ASSETS*/{}', json.dumps(assets)); put('/*CHARATLAS*/{}', json.dumps(atlas)); put('/*SCENE*/{}', json.dumps(scene, ensure_ascii=False)); put('/*PROPS*/{}', json.dumps(props, ensure_ascii=False))
for out in (B + 'game/balcao_rua96.html', B + 'rua96.html'):
    open(out, 'w').write(T); print(out, round(len(T) / 1024), 'KB')
print('sprites:', len(whos), whos)
