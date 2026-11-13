"""Monta o protótipo jogável da casa de Seu Raimundo (Etapa 5 · Fase A) a partir do mesmo motor da padaria (game/template.html),
trocando cenário, objetos, mundo simulado e textos. A padaria (Etapa 4) não é alterada."""
import base64, glob, json, re
A = '../assets/'
T = open('../game/template.html').read()

def sub(old, new, count=1):
    global T
    assert T.count(old) >= 1, 'não achei: ' + old[:70]
    T = T.replace(old, new) if count == 0 else T.replace(old, new, count)

sub('aria-label="Cenário da rua e da padaria"', 'aria-label="Casa de Seu Raimundo"')
sub("scene: Q.get('s') === 'interior' ? 'interior' : 'street',", "scene: 'interior',")
sub('IMG.bakery_interior_base', 'IMG.casa_interior_base')
sub('C94.padaria(ctx)', 'C94.casa(ctx)')
sub('C94.EXTRA', 'C94.EXTRA_CASA', 0)
sub("for (const k of ['lia', 'aurea', 'raimundo', 'dandara', 'lucia'])", "for (const k of ['lia', 'raimundo'])")
T = T.replace('<title>A cidade que somos — Etapa 4: simulação social</title>', '<title>A cidade que somos — Etapa 5 · casa de Seu Raimundo</title>')
T, n = re.subn(r"loc (!==|===) 'padaria'", r"loc \1 'casa'", T); assert n >= 6, n
sub("if (p.y > YF - 1 && Math.abs(p.x - EXIT_X) <= 24) startFade('street');",
    "if (p.y > YF - 1 && Math.abs(p.x - EXIT_X) <= 24) { p.y = YF - 14; p.tx = null; p.ty = null; p.path = []; p.goal = null; say('A escada desce para a rua, no sobrado ao lado da padaria. A passagem entre a casa e a rua entra na Etapa 6.', 5); }")
sub("if (Q.get('go') === '1') beginEnter();", "")
T, n = re.subn(r"  const v = SIM\.npcs\.aurea;[^\n]*\n", '', T); assert n == 1
# mundo simulado
i0 = T.index('SIM = new Sim.World('); i1 = T.index('  bindUI();', i0)
T = T[:i0] + """SIM = new Sim.CasaWorld({ scene: OBJSCENE, seed: +(Q.get('seed') || 1991) + (persist ? persist.dia : 1), start: t0, rate: Q.get('f') === '1' ? 6 : +(Q.get('rate') || 1), persist,
    hooks: { getObj: id => ObjectSys.state[id] || 0, setObj: (id, v) => { ObjectSys.state[id] = v; }, save: p => Sim.Save.save(p) } });
""" + T[i1:]
# relógio, rua, dicas
a = T.index("  $('clock').innerHTML ="); b = T.index("  if (uiT <= 0)", a)
T = T[:a] + """  $('clock').innerHTML = '<b>' + hhmm() + '</b><span>Dia ' + ((window.MUNDO_ATIVO && window.MUNDO_DIA) || w.clock.day) + ' · casa de Seu Raimundo</span>';
  const st = $('street'); const R = w.npcs.raimundo; if (R.state === 'Away' && !w.clock.ended) { st.style.display = 'block'; st.textContent = 'Seu Raimundo saiu · volta por volta das ' + String(Math.floor(R.volta / 60)).padStart(2, '0') + ':' + String(Math.floor(R.volta % 60)).padStart(2, '0') + ''; } else st.style.display = 'none';
""" + T[b:]
sub("if (S.scene === 'street' && nearDoor()) txt = 'E · entrar na padaria';\n  else if (S.scene === 'interior') {", "if (S.scene === 'interior') {")
sub("Desça pela soleira para sair para a rua", "A escada desce para a rua (a descida entra na Etapa 6)")
sub("t.o.id.startsWith('chair') ? 'sentar' : t.o.id === 'aparador' ? 'pegar água' : 'usar'", "SIM.seats[t.o.id] ? 'sentar' : t.o.id === 'talha_1' ? 'pegar água' : 'usar'")
sub("if (seat && o.tipo === 'usar' && o.id.startsWith('chair'))", "if (seat && o.tipo === 'usar')")
T = T.replace("S.scene === 'street' ? 'Rua' : 'Padaria — interior'", "'Casa de Seu Raimundo — interior'")
sub("Lugares e coisas da padaria", "Lugares e coisas"); sub("Examine os objetos da padaria", "Examine os objetos")
sub("Quem conhece o que há dentro do sobrado amarelo ainda não falou.", "Algumas coisas desta casa ele só conta quando confia.")
a = T.index("function updateReport() {"); b = T.index("// ---------- interações da padaria", a)
T = T[:a] + """function updateReport() {
  const w = SIM, n = w.npcs.raimundo;
  document.title = JSON.stringify({ t: w.clock.label(), r: [Math.round(n.x), Math.round(n.y), n.state, n.anim, n.loc, n.act ? n.act.def.id : null, n.act ? n.act.i : null, n.say ? n.say.text : null], obj: ObjectSys.state, carry: w.carry, kp: Object.keys(w.knowledge.got).length, note: S.note ? S.note.text : null, p: [Math.round(S.p.x), Math.round(S.p.y), S.p.anim, S.p.face, S.p.sit ? S.p.sit.phase : null], dlg: D.open ? D.id : null });
}

""" + T[b:]
# tecla N + resumo do dia da casa
sub("if (k === 'b') { toggleDiary(); return; }", "if (k === 'b') { toggleDiary(); return; }\n  if (k === 'n') { avancar(); return; }")
sub("function toggleFast()", """function avancar() {
  if (!SIM) return; const R = SIM.npcs.raimundo, alvo = R.state === 'Away' ? R.volta + .2 : SIM.clock.min + 25;
  SIM.clock.min = Math.max(SIM.clock.min, Math.min(alvo, 719)); toast('<b>Relógio</b> · ' + SIM.clock.label(), 'ev', 1800);
}
function toggleFast()""")
sub("</script>\n</body>", """showDayCard = function (r) {
  const P = Sim.Data.pessoas, el = $('daycard'), nome = id => (P[id] || {}).curto || id; const ATV = { cama: 'arrumar a cama', planta: 'regar a planta', reza: 'rezar', janela: 'olhar a rua', radio: 'ouvir o rádio', cafe: 'fazer café', mesa: 'mexer no dominó', cozinha: 'cozinhar' };
  let h = '<h2><span>O dia na casa de Seu Raimundo</span><span class="x" onclick="document.getElementById(\\'daycard\\').style.display=\\'none\\'">continuar (Esc)</span></h2>';
  h += '<div>Seu Raimundo fez <b>' + r.atividades + '</b> ' + (r.atividades === 1 ? 'coisa' : 'coisas') + ' em casa' + (r.vistas.length ? '. Você viu ele ' + r.vistas.map(v => ATV[v] || v).join(', ') : '. Você não viu o que ele fez') + '.</div>';
  if (r.mudancas.length) h += '<h4>O que mudou entre as pessoas</h4>' + r.mudancas.slice(0, 6).map(m => { const [a, b] = m.par.split('>'); const t = b === 'lia' ? (m.trust >= 0 ? nome(a) + ' confia mais em você' : nome(a) + ' confia menos em você') : (m.aff >= 0 ? nome(a) + ' ficou mais próximo(a) de ' + nome(b) : nome(a) + ' ficou mais distante de ' + nome(b)); return '<div class="kp">' + esc(t) + '</div>'; }).join('');
  h += '<h4>No caderninho</h4>' + r.objetivos.map(o => '<div class="kp"><b>' + esc(o.titulo) + '</b> · ' + Math.min(o.n, o.meta) + '/' + o.meta + (o.feito ? ' ✓' : '') + '</div>').join('') + '<div class="sub" style="margin-top:.3em">' + r.pontos_novos + ' ponto(s) novo(s) hoje · ' + r.pontos + ' no total</div>';
  el.innerHTML = h; el.style.display = 'block';
};
</script>
</body>""")
sub('<span id="msg" aria-live="polite" style="color:#f0c98c"></span>', '<span id="msg" aria-live="polite" style="color:#f0c98c"></span> · <span class="k">N</span> avança o relógio')

# ---- montagem
names = ['casa_interior_base', 'mannequin_adult', 'mannequin_lia', 'lia_tq', 'raimundo_tq', 'obj_casa']
def path(n):
    if n == 'obj_casa': return A + 'objects/casa_objetos.png'
    if n in ('lia_tq', 'raimundo_tq'): return A + 'chars/' + n + '.png'
    return A + n + '.png'
def uri(n): return 'data:image/png;base64,' + base64.b64encode(open(path(n), 'rb').read()).decode()
AT = {n: json.load(open(A + 'chars/' + n + '.json')) for n in ['lia_tq', 'raimundo_tq']}
SIM = '\n'.join(open(f).read() for f in sorted((g for g in glob.glob('../sim/s[0-9]*_*.js') if '/s96_' not in g), key=lambda f: int(re.search(r's(\d+)_', f).group(1))))
L = json.load(open(A + 'layout.json'))
T = (T.replace('/*LAYOUT*/{}', json.dumps(L)).replace('/*CHARS_JS*/', open('../game/chars.js').read() + '\n' + open('../game/cenario94.js').read()).replace('/*CHARATLAS*/{}', json.dumps(AT)).replace('/*OBJECTS_JS*/', open('../game/objects.js').read())
     .replace('/*SIM_JS*/', SIM).replace('/*OBJCAT*/{}', open(A + 'objects/catalog_casa.json').read()).replace('/*OBJSCENE*/{}', open(A + 'objects/scene_casa.json').read()))
open('../game/template_casa_gerado.html', 'w').write(T)
open('../game/index_casa_dev.html', 'w').write(T.replace('/*ASSETS*/{}', json.dumps({n: path(n) for n in names})))
open('../game/balcao_etapa5_casa.html', 'w').write(T.replace('/*ASSETS*/{}', json.dumps({n: uri(n) for n in names})))
print('ok')
