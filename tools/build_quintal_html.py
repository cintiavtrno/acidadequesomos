"""Monta o quintal jogável (Etapa 8.6) → game/balcao_etapa8_quintal.html (HTML autônomo). Rodar de tools/."""
import base64, json
A = '../assets/chars/'
T = open('../quintal/template.html', encoding='utf-8').read()
D = json.load(open('../quintal/qdata.json'))
QUEM = ['lia', 'aurea', 'raimundo', 'dandara', 'lucia', 'ze', 'nonato', 'bela', 'cicera', 'junior', 'tonho', 'zefa', 'nena', 'davi', 'rita', 'caio', 'bia'] + ['m%d' % i for i in range(1, 7)]
AT, IMG = {}, {}
for w in QUEM:
    for p in ('tq',):
        try: AT[w + '_' + p] = json.load(open(A + w + '_' + p + '.json'))
        except FileNotFoundError: continue
        IMG[w + '_' + p] = 'data:image/png;base64,' + base64.b64encode(open(A + w + '_' + p + '.png', 'rb').read()).decode()
QA = '../assets/quintal/'
for n, f in (('q_base', 'quintal_base'), ('q_copa', 'mangueira_copa'), ('q_mobiliario', 'mobiliario'), ('q_equipamentos', 'equipamentos'), ('q_decorativos', 'decorativos'), ('q_itens', 'itens')):
    IMG[n] = 'data:image/png;base64,' + base64.b64encode(open(QA + f + '.png', 'rb').read()).decode()
T = T.replace('/*QCAT*/{}', open(QA + 'catalog_quintal.json', encoding='utf-8').read())
rd = lambda f: open(f, encoding='utf-8').read().replace('</script', '<\\/script')
T = T.replace('/*CHARS_JS*/', rd('../game/chars.js')).replace('/*QUINTAL_JS*/', rd('../quintal/quintal.js')).replace('/*RENDER_JS*/', rd('../quintal/render.js')).replace('/*GAME_JS*/', rd('../quintal/game.js'))
T = T.replace('/*PAL*/{}', open('../quintal/pal.json').read()).replace('/*QDATA*/{}', json.dumps(D)).replace('/*ATLAS*/{}', json.dumps(AT)).replace('/*IMGS*/{}', json.dumps(IMG))
open('../game/balcao_etapa8_quintal.html', 'w', encoding='utf-8').write(T)
print('ok', round(len(T) / 1e6, 2), 'MB', sorted(AT))
