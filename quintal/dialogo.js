// ===== dialogo.js — conversa investigativa e anotações do quintal (1994) =====
// DOM-free. Acrescenta ao Quintal.Sim o mesmo jeito de conversar da rua: Cumprimentar, Perguntar, Ficar ouvindo.
// Cada pessoa só tem certos assuntos em certas fases do caruru, e vários só aparecem depois que a Lia olhou algo no quintal ou ouviu outra pessoa.
// As anotações (this.kp) são o que conta para a meta de 6 anotações novas de 1994. Fora do caruru (fase N) não há anotação.
(function (root) {
  'use strict';
  const Q = (typeof module !== 'undefined' && module.exports) ? require('./quintal.js') : root.Quintal;
  const Sim = Q.Sim, KEY = 'balcao_quintal_kp';

  // ---------------------------------------------------------------- anotações: id → [título, texto, precisa de revisão]
  const K = {
    // o que se vê no quintal
    q_banner: ['A bandeira dos santos', 'Bandeira de Cosme e Damião na parede da casa. Embaixo, um prato servido, uma vela e flores brancas. A primeira porção é dos santos.'],
    q_oferenda: ['A mesa baixa', 'Só Dona Zefa e Dona Nena chegam perto da mesa da oferenda. Eu olhei de longe.'],
    q_mesa: ['A mesa dos adultos', 'Dez lugares com toalha. Os adultos só comem depois das crianças.'],
    q_portao: ['O portão da Rita', 'O portão do fundo dá na casa da Rita. De lá se vê o telhado dela, com a lona e o balde no canto.'],
    q_mangueira: ['A mangueira', 'A mangueira é mais velha que o quintal. A sombra cobre o fundo e passa do muro.'],
    // o que as pessoas contam
    q_quiabo: ['O quiabo fino', 'Dona Zefa corta o quiabo fino e molha a faca antes de cada corte, para não babar. O dendê entra depois.', true],
    q_zefa_pai: ['Por que a Zefa faz o caruru', 'O pai de Dona Zefa fazia o caruru todo ano. Quando ele parou, o quintal ficou anos sem festa. Ela voltou a fazer quando a rua pediu.', true],
    q_zefa_casa: ['A casa da Zefa', 'A casa de Dona Zefa foi medida pelo Programa. Ela deixou medir, ofereceu café e ainda não sabe o que escreveram na ficha.'],
    q_aurea_balcao: ['A padaria sem balcão', 'Vó Áurea deixou o balcão sem ninguém. Disse que o pão espera um dia e o convite da Zefa não esperava.'],
    q_aurea_papel: ['O papel da padaria', 'A padaria ganhou fachada nova do Programa e, junto, um papel com valor de aluguel. Vó Áurea leu três vezes e não assinou.', true],
    q_raimundo_sobrado: ['O amarelo do sobrado', 'O Programa repintou o sobrado de Seu Raimundo. Ele deixou, desde que fosse o mesmo amarelo de antes.'],
    q_lista: ['A lista do Programa', 'A lista do Programa saiu. Tem nome de morador, nome de dono e casas sem nome nenhum. Dandara vai ler tudo na reunião de sábado.', true],
    q_comodos: ['Quem não está na lista', 'Quem aluga cômodo não aparece na lista. A associação vai casa por casa conferir.', true],
    q_lucia_convite: ['Lúcia no caruru', 'Dona Zefa convidou Lúcia pessoalmente. Disse que quem mede a rua também come nela.'],
    q_lucia_ficha: ['A ficha de cada fachada', 'Agora Lúcia confere o que já foi consertado. Cada fachada tem uma ficha com foto do antes e do depois.'],
    q_rita_telhado: ['O telhado da Rita', 'O telhado da Rita está na lista do Programa. Chegou a lona; o resto do material ainda não.', true],
    q_rita_sombra: ['A sombra da mangueira', 'A mangueira é de Dona Zefa e a sombra cai na casa da Rita. Nunca precisaram combinar nada sobre isso.'],
    q_nonato_empreita: ['Nonato e a empreita', 'Nonato fez o reboco da tia e pegou mais duas obras do Programa por empreita. O material chega atrasado e ele cobra no mês seguinte.', true],
    q_ze_cadeira: ['A cadeira nova do Seu Zé', 'Seu Zé ganhou uma cadeira nova de barbearia, do Programa. Veio com um papel e um cadeado.'],
    q_bela_panos: ['Os panos dos meninos', 'Dona Bela costurou um pano para cada menino. No fim, cada um leva o seu para casa.'],
    q_cicera_junior: ['Júnior e o varal', 'Dona Cícera sabia do bairro pelo varal. Agora sabe pelo Júnior, que conta tudo.'],
    q_junior_mangueira: ['Júnior na mangueira', 'Júnior subiu na mangueira antes de todo mundo chegar. De lá se vê o telhado da Rita e a fila do portão.'],
    q_tonho_cocada: ['A cocada de presente', 'A mãe do Tonho fez cinquenta cocadas para o caruru. Hoje ele não vende, só dá.'],
    q_nena_tabuleiro: ['O tabuleiro de Dona Nena', 'Dona Nena cuida da oferenda com Dona Zefa. O acarajé dela só sai quando o sol baixa.', true],
    q_davi_cantiga: ['A música do fim de tarde', 'Davi toca baixinho. Dona Zefa pediu cantiga de roda para os meninos.'],
    q_caio_bia: ['Caio e Bia na padaria', 'Caio e Bia ajudam Vó Áurea no balcão, e sempre sobra um pão para eles.'],
    q_bia_massa: ['Bia e a massa', 'Bia aprendeu a sovar com Vó Áurea, sem relógio, só pelo ponto da massa.'],
    // o que se ouve sem perguntar
    q_prazo: ['O prazo do Programa', 'Lúcia disse à Dandara que o prazo da obra vem do papel e não consulta o bairro.', true],
    q_pratos: ['Os pratos das crianças', 'Os pratos das crianças são todos iguais. Ninguém ganha mais que o outro.'],
  };

  // objeto examinado → o que a Lia passa a ter visto (viu_x) e a anotação que ele rende, se houver
  const OBJ = { banner: ['banner', 'q_banner'], F13: ['oferenda', 'q_oferenda'], M01: ['mesa', 'q_mesa'], portao: ['portao', 'q_portao'], F14: ['mangueira', 'q_mangueira'], M09: ['cocada'], M27: ['tabuleiro'] };

  // ---------------------------------------------------------------- assuntos: pessoa → assunto → { label, ask, resp, kp, fases, quando }
  // fases: em quais fases o assunto existe (omitido = todas do caruru). quando: basta uma condição: 'viu_x' (a Lia olhou) ou 'apos:pessoa:assunto' (já perguntou).
  const ALL = ['A', 'B', 'C1', 'C', 'D'], DEPOIS_A = ['B', 'C1', 'C', 'D'], MESA = ['C1', 'C', 'D'], FIM = ['C', 'D'];
  const T = {
    zefa: {
      quiabo: { label: 'O quiabo', fases: ['A', 'B'], ask: 'Dona Zefa, como a senhora corta o quiabo?', resp: 'Fino, e com a faca molhada. Faca seca puxa a baba. O dendê só entra quando o quiabo já soltou o ponto.', kp: 'q_quiabo' },
      pai: { label: 'A bandeira', quando: ['viu_banner'], ask: 'A bandeira é de Cosme e Damião, não é? A senhora faz todo ano?', resp: 'Meu pai fazia. Quando ele parou, o quintal ficou quieto uns anos. Voltei a fazer porque a rua veio me pedir.', kp: 'q_zefa_pai' },
      casa: { label: 'A casa', fases: FIM, ask: 'Dona Zefa, a moça do Programa também mediu a sua casa?', resp: 'Mediu. Eu abri o portão e ofereci café. O que ela escreveu na ficha eu não li, e acho que ela também não me mostrou.', kp: 'q_zefa_casa' },
    },
    aurea: {
      balcao: { label: 'O balcão', fases: DEPOIS_A, ask: 'Vó, e a padaria? Ficou sem ninguém?', resp: 'Ficou. O pão espera um dia. A Zefa me convidou e eu não ia dizer que não. Amanhã eu abro cedo.', kp: 'q_aurea_balcao' },
      papel: { label: 'O papel', fases: MESA, quando: ['apos:aurea:balcao'], ask: 'A senhora recebeu algum papel do Programa, vó?', resp: 'Veio com a tinta da fachada. Tem um valor de aluguel que eu nunca combinei com ninguém. Li três vezes e deixei na gaveta.', kp: 'q_aurea_papel' },
    },
    raimundo: {
      sobrado: { label: 'O sobrado', fases: DEPOIS_A, ask: 'Seu Raimundo, o sobrado foi pintado de novo?', resp: 'Foi. Deixei, com uma condição: o amarelo tinha que ser o de antes. Mandei trazer a lata e comparei com a parede velha.', kp: 'q_raimundo_sobrado' },
    },
    dandara: {
      lista: { label: 'A lista', fases: DEPOIS_A, ask: 'Dandara, a lista do Programa saiu?', resp: 'Saiu. Tem nome de morador, tem nome de dono, e tem casa sem nome nenhum. Sábado eu leio tudo na reunião da associação.', kp: 'q_lista' },
      comodos: { label: 'Quem ficou fora', fases: FIM, quando: ['apos:dandara:lista'], ask: 'Quem são as casas sem nome?', resp: 'Quem aluga cômodo. Não aparece em papel nenhum. A associação vai de porta em porta conferir, e eu preciso de gente que saiba quem mora onde.', kp: 'q_comodos' },
    },
    lucia: {
      convite: { label: 'O convite', fases: MESA, ask: 'Lúcia, a senhora veio por causa da Dona Zefa?', resp: 'Ela me chamou pessoalmente. Disse que quem mede a rua também come nela. Vim, porque recusar seria pior.', kp: 'q_lucia_convite' },
      ficha: { label: 'O trabalho', fases: FIM, quando: ['apos:lucia:convite'], ask: 'E o que a senhora faz agora na rua?', resp: 'Confiro o que já foi consertado. Cada fachada tem uma ficha com foto do antes e do depois. Assino embaixo.', kp: 'q_lucia_ficha' },
    },
    rita: {
      telhado: { label: 'O telhado', fases: DEPOIS_A, quando: ['viu_portao'], ask: 'Dona Rita, o seu telhado entrou no Programa?', resp: 'Entrou. Chegou a lona. O resto do material está para chegar, e já vai pro terceiro mês.', kp: 'q_rita_telhado' },
      sombra: { label: 'A mangueira', fases: FIM, quando: ['apos:rita:telhado', 'viu_mangueira'], ask: 'A mangueira dá sombra na sua casa?', resp: 'Dá. A árvore é da Zefa e a sombra é minha. Nunca falamos disso, não precisou.', kp: 'q_rita_sombra' },
    },
    nonato: {
      empreita: { label: 'A obra', ask: 'Nonato, terminou a obra da sua tia?', resp: 'Terminei, e peguei mais duas do Programa. É por empreita. O material chega atrasado e eu cobro no mês seguinte, quando eles pagam.', kp: 'q_nonato_empreita' },
    },
    ze: {
      cadeira: { label: 'A barbearia', ask: 'Seu Zé, a barbearia ainda funciona?', resp: 'Funciona. Ganhei uma cadeira nova do Programa. Veio com um papel e um cadeado, pra ninguém levar.', kp: 'q_ze_cadeira' },
    },
    bela: {
      panos: { label: 'Os panos', fases: DEPOIS_A, quando: ['viu_toalha', 'viu_mesa'], ask: 'Dona Bela, foi a senhora que costurou os panos dos meninos?', resp: 'Fui. Um pano para cada menino. Quando acaba o caruru cada um leva o seu dobrado debaixo do braço.', kp: 'q_bela_panos' },
    },
    cicera: {
      junior: { label: 'O Júnior', ask: 'Dona Cícera, o Júnior cresceu bastante, não?', resp: 'Cresceu e agora me conta tudo. Antes eu sabia do bairro pelo varal. Hoje sei pelo menino, e ele conta até o que eu não pedi.', kp: 'q_cicera_junior' },
    },
    junior: {
      mangueira: { label: 'A mangueira', quando: ['viu_mangueira'], ask: 'Júnior, você subiu na mangueira?', resp: 'Subi cedo, antes de todo mundo chegar. De lá eu vejo o telhado da Rita, a lona e até quem está na fila do portão.', kp: 'q_junior_mangueira' },
    },
    tonho: {
      cocada: { label: 'A cocada', fases: DEPOIS_A, quando: ['viu_cocada'], ask: 'Tonho, essa cocada é pra vender?', resp: 'Hoje não. Minha mãe fez cinquenta e mandou trazer. É presente pros meninos. Vender no caruru dá azar.', kp: 'q_tonho_cocada' },
    },
    nena: {
      tabuleiro: { label: 'O tabuleiro', fases: MESA, quando: ['viu_oferenda', 'viu_tabuleiro'], ask: 'Dona Nena, o acarajé sai hoje?', resp: 'Sai quando o sol baixar. Agora eu estou com a Zefa na oferenda. Cada coisa tem sua hora, minha filha.', kp: 'q_nena_tabuleiro' },
    },
    davi: {
      cantiga: { label: 'A música', fases: ['D'], ask: 'Seu Davi, o senhor vai tocar?', resp: 'Baixinho, no fim. Dona Zefa pediu cantiga de roda pros meninos, e eu toco o que ela pede.', kp: 'q_davi_cantiga' },
    },
    caio: {
      padaria: { label: 'A padaria', fases: DEPOIS_A, ask: 'Caio, você trabalha na padaria da minha avó?', resp: 'Ajudo. Carrego as forma e varro de tarde. Sempre sobra um pão pra mim e um pra Bia.', kp: 'q_caio_bia' },
    },
    bia: {
      massa: { label: 'A massa', fases: DEPOIS_A, ask: 'Bia, é verdade que a minha avó te ensinou a sovar?', resp: 'Ensinou. Ela não olha relógio. Aperta a massa com o calo do polegar e diz se está no ponto.', kp: 'q_bia_massa' },
    },
  };

  // ---------------------------------------------------------------- ficar ouvindo: pessoa → { fase: [texto, anotação?] }, '*' vale para qualquer fase
  const OUVE = {
    zefa: { '*': ['(Dona Zefa mexe o panelão devagar e fala baixo, como quem conversa com os santos.)'] },
    aurea: { '*': ['(Vó Áurea ajeita os pães no cesto e conta de cabeça quantos são.)'] },
    raimundo: { '*': ['(Seu Raimundo senta, tira o chapéu e fica olhando o quintal sem dizer nada.)'] },
    dandara: { D: ['(Dandara pergunta a Lúcia se o prazo da obra é o do papel ou o do bairro. Lúcia responde que é o do papel.)', 'q_prazo'], C: ['(Dandara conta assinaturas no caderno, mexendo os lábios.)'], '*': ['(Dandara folheia o caderno procurando um nome.)'] },
    lucia: { D: ['(Lúcia explica à Dandara que o prazo da obra vem do papel. Dandara anota, séria.)', 'q_prazo'], '*': ['(Lúcia olha as fachadas do quintal vizinho e não tira a prancheta do braço.)'] },
    cicera: { '*': ['(Dona Cícera conta à Dona Nena que o neto mexe em tudo. Dona Nena responde que é assim que se aprende.)'] },
    junior: { '*': ['(Júnior sussurra o que viu da mangueira para quem passa perto.)'] },
    nena: { '*': ['(Dona Nena cobre a bacia com o pano e confere a vela da oferenda.)'] },
    m: { C1: ['(Um menino conta os pratos baixinho e confere se o dele é igual ao dos outros.)', 'q_pratos'], '*': ['(O menino está de olho no prato e não ouve mais nada.)'] },
  };
  const OUVE_PADRAO = '(A conversa é baixa e miúda. Dá para ouvir o nome do caruru e o do santo, mais nada.)';

  // ---------------------------------------------------------------- Sim: estado de conversa e anotações
  const P = Sim.prototype;
  P._d = function () {
    if (this.kp) return this;
    this.kp = {}; this.viv = {}; this.feitos = {}; this.novas = []; this.conversa = null;
    try { if (typeof window !== 'undefined' && window.MUNDO_ATIVO && typeof localStorage !== 'undefined') { const s = JSON.parse(localStorage.getItem(KEY) || 'null'); if (s) { this.kp = s.kp || {}; this.viv = s.viv || {}; this.feitos = s.feitos || {}; } } } catch (e) { }
    return this;
  };
  P.salvarKp = function () { try { if (typeof window !== 'undefined' && window.MUNDO_ATIVO && typeof localStorage !== 'undefined') localStorage.setItem(KEY, JSON.stringify({ kp: this.kp, viv: this.viv, feitos: this.feitos })); } catch (e) { } };
  P.ganhar = function (id) {
    this._d(); const k = K[id]; if (!k || this.kp[id] || this.normal) return false;
    this.kp[id] = { id, titulo: k[0], texto: k[1], fase: this.fasen, min: Math.round(this.clock.min) }; this.novas.push(id); this.log.push(['nota', id]); this.salvarKp(); return true;
  };
  P.notas = function () { this._d(); return Object.values(this.kp); };
  P.ver = function (v) { this._d(); if (!this.viv[v]) { this.viv[v] = 1; this.salvarKp(); } };

  // examinar: o que a Lia olha vira vivência e, em alguns casos, anotação
  const ex0 = P.examinar;
  P.examinar = function (k) { ex0.call(this, k); this._d(); const o = OBJ[k]; if (o && !this.normal) { this.ver('viu_' + o[0]); if (o[1]) this.ganhar(o[1]); } };

  // conversa
  const falar0 = P.falar;
  P.falar = function (id) {
    falar0.call(this, id); this._d(); const n = this.npcs[id], L = this.lia, sd = (this.msg && this.msg.txt || '').replace(/^[^:]*: /, '');
    if (n && n.state === 'parado') n.face = Q.dir8(L.x - n.x, L.y - n.y) || n.face;
    this.conversa = { id, modo: 'raiz', linhas: [{ quem: id, texto: sd }] }; this.msg = null; return this.conversa;
  };
  P.fecharConversa = function () { this.conversa = null; };
  P.topicosDe = function (id) {
    this._d(); const t = T[id] || {}, f = this.fasen, out = []; if (this.normal) return out;
    for (const tid in t) {
      const a = t[tid]; if (a.fases && !a.fases.includes(f)) continue;
      if (a.quando && !a.quando.some(c => c.startsWith('apos:') ? this.feitos[c.slice(5)] : this.viv[c])) continue;
      out.push({ id: tid, label: a.label, feito: !!this.feitos[id + ':' + tid] });
    }
    return out;
  };
  P.temAssunto = function (id) { return !!T[id]; };
  P.perguntar = function (id, tid) {
    this._d(); const a = T[id] && T[id][tid]; if (!a) return [];
    this.feitos[id + ':' + tid] = 1; const ganhou = a.kp && this.ganhar(a.kp), out = [{ quem: 'lia', texto: a.ask }, { quem: id, texto: a.resp, rev: !!(a.kp && K[a.kp][2]) }];
    if (ganhou) out.push({ quem: 'nota', texto: 'Anotado: ' + K[a.kp][0] }); else this.salvarKp();
    return out;
  };
  P.ouvir = function (id) {
    this._d(); const o = OUVE[/^m\d$/.test(id) ? 'm' : id] || {}, e = o[this.fasen] || o['*'] || [OUVE_PADRAO], out = [{ quem: 'nota', texto: e[0], nota: true }];
    this.ver('ouviu_' + id); if (e[1] && this.ganhar(e[1])) out.push({ quem: 'nota', texto: 'Anotado: ' + K[e[1]][0] });
    return out;
  };
  // ação do painel: saudar | topicos | voltar | ouvir | perguntar(arg = assunto) | sair
  P.conversaAcao = function (a, arg) {
    const c = this.conversa; if (!c) return null; const id = c.id;
    if (a === 'sair') { this.conversa = null; return null; }
    if (a === 'topicos') c.modo = 'topicos';
    else if (a === 'voltar') c.modo = 'raiz';
    else if (a === 'saudar') { c.linhas = [{ quem: 'lia', texto: 'Oi!' }, c.linhas[0] && c.linhas[0].quem === id ? c.linhas[0] : { quem: id, texto: '…' }]; c.modo = 'raiz'; }
    else if (a === 'ouvir') { c.linhas = this.ouvir(id); c.modo = 'raiz'; }
    else if (a === 'perguntar') { c.linhas = this.perguntar(id, arg); c.modo = 'raiz'; }
    return c;
  };
  P.dicaSemAssunto = 'Você ainda não tem um motivo para puxar esse assunto. Olhe o quintal, escute as conversas e volte.';

  // vivência da toalha (as crianças comendo) e conversa que não segura quem foi embora ou mudou de fase
  const up0 = P.update;
  P.update = function (dt) {
    up0.call(this, dt); this._d(); const L = this.lia, T0 = this.D.TOALHA;
    if (this.fasen === 'C1' && Math.hypot(L.x - T0.cx, L.y - T0.cy) < 5.5) this.ver('viu_toalha');
    if (this.conversa) { const n = this.npcs[this.conversa.id]; if (!n || !n.vis || Math.hypot(L.x - n.x, L.y - n.y) > 2.4) this.conversa = null; }
  };
  const pp0 = P.npcPasso;
  P.npcPasso = function (n, dt) { if (this.conversa && this.conversa.id === n.id) { if (n.state === 'andando') n.anim = 'idle'; return; } return pp0.call(this, n, dt); };

  Q.Dialogo = { K, T, OBJ, OUVE };
  if (typeof module !== 'undefined' && module.exports) module.exports = Q.Dialogo;
})(typeof window !== 'undefined' ? window : globalThis);
