import base64, json, sys
A = '../assets/'
names = ['street_far', 'street_world', 'bakery_interior_base', 'bakery_counter', 'mannequin_adult', 'mannequin_lia']
def uri(n): return 'data:image/png;base64,' + base64.b64encode(open(A + n + '.png', 'rb').read()).decode()
t = open('../game/template.html').read()
# dev (arquivos soltos) e standalone (data URI)
dev = {n: '../assets/' + n + '.png' for n in names}
open('../game/index_dev.html', 'w').write(t.replace('/*ASSETS*/{}', json.dumps(dev)))
open('../game/balcao_etapa1_cenario_base.html', 'w').write(t.replace('/*ASSETS*/{}', json.dumps({n: uri(n) for n in names})))
print('ok')
