// ===== controle.js — joystick sem programa externo =====
// Lê o controle pelo Gamepad API do navegador e transforma cada botão em ação para quem está na tela:
// a abertura, as telas do shell, o ambiente ativo (rua, padaria, casa, quintal) ou a rua de 1996.
//
// Funções (o mesmo jogo para qualquer controle):
//   setas, direcional ou analógico ... andar e escolher
//   ok ............................... falar, examinar, entrar, confirmar (E / Enter)
//   volta ............................ voltar e fechar (Esc)
//   cad .............................. caderninho (B)
//   pula ............................. Pular (próximo dia ou próximo ano), o botão "Pular ▸" do canto
//   R1 ............................... botão do alto (esperar o anoitecer, subir para dormir)
//   start ............................ volta para o menu principal
//   caderninho aberto ................ L1/R1 trocam a aba e ◀ ▶ (ou L2/R2) viram a página (padaria e casa); ▲ ▼ rolam (rua, quintal, 1996)
// Nas conversas as setas passam pelas respostas (a escolhida fica com contorno) e "ok" escolhe.
//
// Botões, pela posição (igual em controle de PlayStation e em controle genérico numerado):
//   de cima (triângulo, 1) = caderninho · da direita (bola, 2) = falar/confirmar · de baixo (X, 3) = voltar · da esquerda (quadrado, 4) = pular
// As dicas da tela mostram ① ② ③ ④ (Opções > Botões na tela troca para △ ◯ ✕ □; localStorage 'acq_formas').
// Outro arranjo: Opções > Configurar controle (o mapa aprendido fica em localStorage 'acq_controle').
(function () {
  'use strict';
  if (window.__CONTROLE) return;
  const STD = { ok: { b: 1 }, volta: { b: 0 }, cad: { b: 3 }, pula: { b: 2 }, l1: { b: 4 }, r1: { b: 5 }, l2: { b: 6 }, r2: { b: 7 }, start: { b: 9 }, select: { b: 8 } };
  const GEN = { ok: { b: 1 }, volta: { b: 2 }, cad: { b: 0 }, pula: { b: 3 }, l1: { b: 4 }, r1: { b: 5 }, l2: { b: 6 }, r2: { b: 7 }, start: { b: 9 }, select: { b: 8 } };
  const FORMA = { ok: '◯', volta: '✕', cad: '△', pula: '□' };
  const NOME = { l1: 'L1', r1: 'R1', l2: 'L2', r2: 'R2', start: 'START' };
  const NUM = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯';
  const APRENDE = [['ok', 'CONFIRMAR E FALAR'], ['volta', 'VOLTAR E FECHAR'], ['cad', 'ABRIR O CADERNINHO'], ['pula', 'PULAR O DIA'], ['l1', 'ABA ANTERIOR DO CADERNO (L1)'], ['r1', 'PRÓXIMA ABA E ESPERAR O ANOITECER (R1)'], ['start', 'VOLTAR AO MENU (START)']];
  const FUNCOES = ['ok', 'volta', 'cad', 'pula', 'l1', 'r1', 'l2', 'r2', 'start', 'select'];
  const lerMapa = () => { try { return JSON.parse(localStorage.getItem('acq_controle')); } catch (e) { return null; } };
  let mapa = lerMapa(), padrao = true, nomeCtrl = '';
  const NOME_SHELL = !!document.getElementById('f_rua');    // index.html (shell) ou rua96.html
  const perfil = () => mapa || (padrao ? STD : GEN);
  const NUMERO = { cad: '①', ok: '②', volta: '③', pula: '④' };
  const formas = () => { try { return localStorage.getItem('acq_formas') === '1'; } catch (e) { return false; } };
  function glifo(n) {
    if (!mapa) return (formas() ? FORMA[n] : NUMERO[n]) || NOME[n] || n;
    const e = perfil()[n];
    if (!mapa && NOME[n]) return NOME[n];
    return e && e.b >= 0 ? (NUM[e.b] || 'B' + (e.b + 1)) : (NOME[n] || '•');
  }

  // ---------------------------------------------------------------- para quem vão as ações
  function alvo() {
    const ab = document.getElementById('abertura'); if (ab && ab.contentWindow) return { w: ab.contentWindow, tipo: 'abertura' };
    const h = document.getElementById('hist'); if (h && h.style.display === 'flex') return { w: window, tipo: 'shell' };
    if (NOME_SHELL) { try { const id = mundo.cenas.atual; return { w: document.getElementById('f_' + id).contentWindow, tipo: 'jogo' }; } catch (e) { return { w: window, tipo: 'shell' }; } }
    return { w: window, tipo: 'jogo' };
  }
  function tecla(w, key, tipo, repeat) { try { w.document.dispatchEvent(new w.KeyboardEvent(tipo, { key, bubbles: true, cancelable: true, repeat: !!repeat })); } catch (e) { } }

  // ---------------------------------------------------------------- respostas das conversas e botões das janelas do jogo
  const JANELAS = ['#dlg', '#mesa', '#fimcard', '#daycard'];
  function janela(w) {
    try {
      const d = w.document;
      for (const s of JANELAS) {
        const el = d.querySelector(s); if (!el || w.getComputedStyle(el).display === 'none') continue;
        const bs = [...el.querySelectorAll('button')].filter(b => !b.disabled && b.offsetParent !== null);
        if (bs.length) return { el, bs };
      }
    } catch (e) { }
    return null;
  }
  // caderninho: na padaria e na casa ele tem abas (Entender, Pessoas, Lugares) e páginas; na rua, em 1996 e no quintal é uma lista que rola
  function caderno(w) {
    try {
      const d = w.document;
      const di = d.querySelector('#diary'); if (di && w.getComputedStyle(di).display !== 'none') return { tipo: 'abas' };
      for (const s of ['#notes', '#cad']) { const el = d.querySelector(s); if (el && w.getComputedStyle(el).display !== 'none') return { tipo: 'lista', el }; }
    } catch (e) { }
    return null;
  }
  function trocaAba(w, d) { try { w.eval("(()=>{const i=TABS.findIndex(t=>t[0]===DIARY.tab);diaryTab(TABS[(i+" + d + "+TABS.length)%TABS.length][0])})()"); } catch (e) { } }
  function rola(c, d) { c.el.scrollBy({ top: d * 70, behavior: 'smooth' }); }
  const marcados = new WeakMap();
  function marca(j) {
    let i = j.el.__gpSel | 0; if (i >= j.bs.length) i = j.bs.length - 1; j.el.__gpSel = i;
    j.bs.forEach((b, k) => { const on = k === i; if (on && !marcados.get(b)) { b.style.outline = '3px solid #f0c98c'; b.style.outlineOffset = '2px'; marcados.set(b, 1); } else if (!on && marcados.get(b)) { b.style.outline = ''; b.style.outlineOffset = ''; marcados.delete(b); } });
  }
  function moveJanela(j, d) { j.el.__gpSel = ((j.el.__gpSel | 0) + d + j.bs.length) % j.bs.length; marca(j); }
  function pular() {
    if (NOME_SHELL) { try { menuPular(); } catch (e) { } }
    else { const p = document.getElementById('pbtn'); p && p.click(); }
  }

  // ---------------------------------------------------------------- leitura do controle
  const segura = {};
  const ESPERA = 380, RITMO = 140;
  let base = null;                      // repouso dos eixos (gatilhos que descansam em -1 não viram seta presa)
  function botao(gp, e) { if (!e || e.b === undefined || e.b < 0) return false; const b = gp.buttons[e.b]; return !!b && (b.pressed || b.value > .5); }
  function estado(gp) {
    const m = perfil(), s = {};
    for (const n of FUNCOES) s[n] = botao(gp, m[n]);
    if (gp.mapping === 'standard') { s.cima = botao(gp, { b: 12 }); s.baixo = botao(gp, { b: 13 }); s.esq = botao(gp, { b: 14 }); s.dir = botao(gp, { b: 15 }); }
    else { s.cima = s.baixo = s.esq = s.dir = false; }
    if (!base || base.length !== gp.axes.length) base = gp.axes.map(v => Math.abs(v) > .5 ? v : 0);
    // eixos em pares (0,1), (2,3), (4,5), (6,7): analógicos e direcional de controle genérico
    for (let i = 0; i + 1 < gp.axes.length && i < 8; i += 2) {
      const x = (gp.axes[i] || 0) - base[i], y = (gp.axes[i + 1] || 0) - base[i + 1];
      if (Math.abs(gp.axes[i] || 0) > 1.05 || Math.abs(gp.axes[i + 1] || 0) > 1.05) continue;     // "hat" de alguns controles chega como um eixo só, fora de [-1, 1]
      if (y < -.5) s.cima = true; if (y > .5) s.baixo = true; if (x < -.5) s.esq = true; if (x > .5) s.dir = true;
    }
    return s;
  }
  const SETA = { cima: 'ArrowUp', baixo: 'ArrowDown', esq: 'ArrowLeft', dir: 'ArrowRight' };
  function aperta(n) {
    const a = alvo(), w = a.w, j = a.tipo === 'jogo' ? janela(w) : null, c = a.tipo === 'jogo' && !j ? caderno(w) : null;
    if (c) {                                                       // caderninho aberto
      if (c.tipo === 'lista' && (n === 'cima' || n === 'baixo')) { rola(c, n === 'cima' ? -1 : 1); return null; }
      if (c.tipo === 'abas' && (n === 'l1' || n === 'r1')) { trocaAba(w, n === 'l1' ? -1 : 1); return null; }
      if (c.tipo === 'abas' && (n === 'l2' || n === 'r2')) { tecla(w, n === 'l2' ? 'ArrowLeft' : 'ArrowRight', 'keydown'); return { w, key: n === 'l2' ? 'ArrowLeft' : 'ArrowRight' }; }
      if (n === 'ok' || n === 'volta' || n === 'cad') { tecla(w, 'b', 'keydown'); return { w, key: 'b' }; }
    }
    if (SETA[n]) {
      if (j) { moveJanela(j, n === 'cima' || n === 'esq' ? -1 : 1); return null; }
      tecla(w, SETA[n], 'keydown'); return { w, key: SETA[n] };
    }
    if (n === 'ok') {
      if (j) { const i = j.el.__gpSel | 0; j.el.__gpSel = 0; j.bs[i] && j.bs[i].click(); return null; }
      const k = a.tipo === 'jogo' ? 'e' : 'Enter'; tecla(w, k, 'keydown'); return { w, key: k };
    }
    if (n === 'volta') { tecla(w, 'Escape', 'keydown'); return { w, key: 'Escape' }; }
    if (n === 'cad' && a.tipo === 'jogo') { tecla(w, 'b', 'keydown'); return { w, key: 'b' }; }
    if (n === 'pula' && a.tipo === 'jogo') { pular(); return null; }
    if (n === 'r1' && a.tipo === 'jogo') { const b = document.getElementById('cb') || document.getElementById('ce'); if (b) b.click(); return null; }
    if (n === 'start') return null;     // start age ao soltar, se foi apertado sozinho (start + select é o desligar)
    return null;
  }

  // aprender um controle diferente: espera um botão sair do repouso
  let aprendendo = null;
  function aprender(gp) {
    const A = aprendendo; if (!A.base) { A.base = gp.buttons.map(b => b.pressed || b.value > .5); return; }
    if (A.solta) { if (gp.buttons.some((b, i) => (b.pressed || b.value > .5) && !A.base[i])) return; A.solta = false; return; }
    let e = null;
    gp.buttons.forEach((b, i) => { if (!e && (b.pressed || b.value > .5) && !A.base[i]) e = { b: i }; });
    if (!e) return;
    A.m[APRENDE[A.i][0]] = e; A.i++; A.solta = true;
    if (A.i >= APRENDE.length) {
      const pad = padrao ? STD : GEN; for (const n of FUNCOES) if (!A.m[n]) A.m[n] = pad[n];
      mapa = A.m; try { localStorage.setItem('acq_controle', JSON.stringify(mapa)); } catch (x) { } const f = A.fim; aprendendo = null; atualizaDicas(); f && f();
    } else A.passo && A.passo(APRENDE[A.i][1], A.i);
  }

  let antes = {}, comSelect = false;
  // SELECT + START por 3 s: o programa desligar_controle.py do Orange Pi desliga a placa; aqui a tela mostra a contagem
  let deslT = 0, deslEl = null;
  function desligando(on, now) {
    if (!on || !tvAtivo()) { if (deslEl) { deslEl.remove(); deslEl = null; } deslT = 0; return; }
    if (!deslT) deslT = now;
    if (!deslEl) { deslEl = document.createElement('div'); deslEl.style.cssText = 'position:fixed;inset:0;z-index:99;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;background:rgba(13,8,11,.88);color:#f1e2be;font:600 28px/1.3 system-ui,sans-serif;text-align:center'; document.body.appendChild(deslEl); }
    const f = Math.min(1, (now - deslT) / 3000);
    deslEl.innerHTML = f < 1 ? 'Desligando a placa…<small style="font-size:17px;opacity:.75">continue segurando SELECT + START · solte para cancelar</small><i style="display:block;width:340px;height:6px;background:rgba(241,226,190,.2)"><i style="display:block;height:100%;width:' + Math.round(f * 100) + '%;background:#e3a93b"></i></i>'
      : 'Desligando.<small style="font-size:17px;opacity:.75">O jogo fica salvo. Quando a tela apagar, pode tirar a placa da tomada.</small>';
  }
  function laco(now) {
    const gps = navigator.getGamepads ? [...navigator.getGamepads()].filter(Boolean) : [];
    const gp = gps[0];
    if (gp) {
      nomeCtrl = gp.id;
      // só controle de marca (PlayStation, Xbox, 8BitDo) segue a ordem "padrão" do navegador; os genéricos numerados 1 2 3 4
      // chegam com o botão 1 no índice 0, mesmo quando o navegador diz que são padrão
      const deMarca = /sony|playstation|dualshock|dualsense|wireless controller|054c|xbox|xinput|045e|microsoft|8bitdo|2dc8|nintendo|057e/i.test(gp.id);
      const pd = gp.mapping === 'standard' && deMarca; if (padrao !== pd) { padrao = pd; atualizaDicas(); }
      if (aprendendo) aprender(gp);
      else {
        const s = estado(gp);
        for (const n in s) {
          if (s[n] && !antes[n]) { ligaGlifos(); const r = aperta(n); segura[n] = { prox: now + ESPERA, r }; }
          else if (s[n] && segura[n] && SETA[n] && now >= segura[n].prox) {          // segurar a seta repete (menus e listas); andar usa a tecla presa
            segura[n].prox = now + RITMO; const r = segura[n].r;
            if (r) tecla(r.w, r.key, 'keydown', true);
            else { const a = alvo(), j = a.tipo === 'jogo' ? janela(a.w) : null; if (j) moveJanela(j, n === 'cima' || n === 'esq' ? -1 : 1); else { const c = a.tipo === 'jogo' ? caderno(a.w) : null; if (c && c.tipo === 'lista' && (n === 'cima' || n === 'baixo')) rola(c, n === 'cima' ? -1 : 1); } }
          } else if (!s[n] && antes[n]) {
            const g = segura[n]; if (g && g.r) tecla(g.r.w, g.r.key, 'keyup'); delete segura[n];
            if (n === 'start' && !comSelect && alvo().tipo !== 'abertura') { if (NOME_SHELL) location.reload(); else location.href = 'index.html'; }
          }
        }
        if (s.start && s.select) comSelect = true; else if (!s.start) comSelect = false;
        desligando(s.start && s.select, now);
        antes = s;
        const a = alvo(); if (a.tipo === 'jogo') { const j = janela(a.w); if (j) marca(j); }
      }
    }
    requestAnimationFrame(laco);
  }
  requestAnimationFrame(laco);

  // ---------------------------------------------------------------- dicas na tela: "E", "B", "Esc" viram os botões do controle
  // Liga quando alguém aperta um botão do controle (fica lembrado em localStorage 'acq_glifos').
  // O texto é trocado NA HORA em que o jogo escreve (innerHTML/textContent), então nada pisca entre a letra e o botão.
  let glifos = (() => { try { return localStorage.getItem('acq_glifos') === '1'; } catch (e) { return false; } })();
  const COR = { '◯': '#e8505b', '✕': '#6f9ff0', '△': '#44c08a', '□': '#e07fc4', '①': '#44c08a', '②': '#e8505b', '③': '#6f9ff0', '④': '#e07fc4' };   // números nas cores do controle genérico (1 verde, 2 vermelho, 3 azul, 4 rosa)
  function tabela() {
    const ok = glifo('ok'), volta = glifo('volta'), cad = glifo('cad');
    return {
      tecla: { 'E': ok, 'e': ok, 'Enter': ok, 'B': cad, 'b': cad, 'Esc': volta, 'WASD': 'analógico', 'W A S D': 'analógico' },
      textos: [[/\(E\)/g, '(' + ok + ')'], [/\(Esc\)/g, '(' + volta + ')'], [/\(B\)/g, '(' + cad + ')'], [/\bEsc para\b/g, volta + ' para'], [/\b([Aa]perte) E\b/g, '$1 ' + ok], [/\btecla E\b/g, 'botão ' + ok],
        [/^E · /, ok + ' · '], [/qualquer tecla de movimento/g, 'o direcional'], [/\bclique: ir até \/ falar( \/ examinar)?/g, ''], [/^E (Falar|falar|Examinar|examinar|Entrar|entrar|Pegar|pegar|Sentar|sentar|Atender|atender|Conversar|conversar)/, ok + ' $1']],
    };
  }
  let T = tabela();
  const ehTecla = el => el && el.nodeType === 1 && (el.tagName === 'KBD' || (el.classList && el.classList.contains('k')));
  function trocaTexto(s, el) {
    if (ehTecla(el)) { const v = T.tecla[s.trim()]; return v || s; }
    let n = s; for (const [re, by] of T.textos) n = n.replace(re, by);
    if (el && el.tagName === 'BUTTON' && el.closest && el.closest('#dlg')) n = n.replace(/^\d+ · /, '');    // conversa: sem 1, 2, 0 na frente
    return n;
  }
  function trocaHTML(s) {
    s = s.replace(/(<kbd[^>]*>|<span[^>]*class="k"[^>]*>)([^<]{1,8})(<\/)/g, (m, a, k, c) => { const v = T.tecla[k.trim()]; return v ? a + v + c : m; });
    s = s.replace(/(<button[^>]*>)\d+ · /g, '$1');
    s = s.replace(/(<button id="c[be]"[^>]*>)([^<]*)(<\/button>)/g, (m, a, t, c) => a + t + ' · ' + glifo('r1') + c);
    return s.split(/(<[^>]*>)/).map(p => p[0] === '<' ? p : trocaTexto(p, null)).join('');
  }
  function embrulha(w) {
    if (!w || w.__gpEmbrulho) return; w.__gpEmbrulho = true;
    try {
      const EP = w.Element.prototype, dh = Object.getOwnPropertyDescriptor(EP, 'innerHTML');
      Object.defineProperty(EP, 'innerHTML', { configurable: true, get: dh.get, set(v) { dh.set.call(this, glifos && typeof v === 'string' ? trocaHTML(v) : v); } });
      const NP = w.Node.prototype, dt = Object.getOwnPropertyDescriptor(NP, 'textContent');
      Object.defineProperty(NP, 'textContent', { configurable: true, get: dt.get, set(v) { dt.set.call(this, glifos && this.nodeType === 1 && v != null ? trocaTexto(String(v), this) : v); } });
    } catch (e) { }
  }
  function passa(doc) {       // passe completo: o que já estava escrito antes de o controle ser usado
    if (!doc || !doc.body) return;
    for (const el of doc.querySelectorAll('.k,kbd')) { const v = T.tecla[el.textContent.trim()]; if (v && el.textContent !== v) { el.firstChild ? el.firstChild.nodeValue = v : el.append(v); if (COR[v]) { el.style.color = COR[v]; el.style.fontWeight = '700'; } } }
    const tw = doc.createTreeWalker(doc.body, 4, { acceptNode: x => /^(SCRIPT|STYLE|TEXTAREA|KBD)$/.test(x.parentNode && x.parentNode.nodeName) || ehTecla(x.parentNode) ? 2 : 1 });
    let x; while ((x = tw.nextNode())) { const n = trocaTexto(x.nodeValue, x.parentNode); if (n !== x.nodeValue) x.nodeValue = n; }
    try {
      const tb = doc.querySelector('#diary .tabs');
      if (tb && !tb.querySelector('.gpdica')) { const sp = doc.createElement('span'); sp.className = 'gpdica'; sp.style.cssText = 'display:block;width:100%;text-align:center;font:600 11px system-ui,sans-serif;color:#5a4030;opacity:.8;margin-top:4px;pointer-events:none'; tb.appendChild(sp); }
      if (tb) tb.querySelector('.gpdica').textContent = glifo('l1') + ' ' + glifo('r1') + ' trocam a aba · ◀ ▶ viram a página · ' + glifo('cad') + ' fecha';
      for (const q of ['#notes h2', '#cad h3']) { const h = doc.querySelector(q); if (h && !h.querySelector('.gpdica')) { const sp = doc.createElement('small'); sp.className = 'gpdica'; sp.style.cssText = 'margin-left:.8em;font:600 .7em system-ui,sans-serif;opacity:.7'; sp.textContent = '▲ ▼ rolam · ' + glifo('cad') + ' fecha'; h.appendChild(sp); } }
      const pu = doc.getElementById('pular') || doc.getElementById('pbtn'); if (pu) { const t = 'Pular ' + glifo('pula'); if (pu.textContent !== t) pu.textContent = t; }
    } catch (e) { }
  }
  function janelas() {
    const ws = [window];
    if (NOME_SHELL) for (const id of ['rua', 'padaria', 'casa', 'quintal']) { try { const w = document.getElementById('f_' + id).contentWindow; if (w && w.document && w.document.body) ws.push(w); } catch (e) { } }
    return ws;
  }
  function atualizaDicas() { T = tabela(); if (glifos) for (const w of janelas()) { embrulha(w); passa(w.document); } }
  setInterval(() => { if (glifos) for (const w of janelas()) { embrulha(w); passa(w.document); } }, 1500);
  // ponteiro do mouse: some enquanto se joga com o controle (ele ficava piscando em cima do jogo); volta se o mouse mexer
  let semCursor = false;
  function cursor(esconde) {
    if (semCursor === esconde) return; semCursor = esconde;
    const ws = janelas(); const ab = document.getElementById('abertura'); if (ab && ab.contentWindow) ws.push(ab.contentWindow);
    for (const w of ws) { try { const d = w.document; let st = d.getElementById('gp-sem-cursor');
      if (esconde && !st) { st = d.createElement('style'); st.id = 'gp-sem-cursor'; st.textContent = '*,*::before,*::after{cursor:none!important}'; (d.head || d.documentElement).appendChild(st); }
      if (!esconde && st) st.remove();
      if (!w.__gpMouse) { w.__gpMouse = true; w.addEventListener('mousemove', e => { if (e.isTrusted && (Math.abs(e.movementX) + Math.abs(e.movementY)) > 2) cursor(false); }, true); } } catch (e) { } }
  }
  setInterval(() => { if (semCursor) { semCursor = false; cursor(true); } }, 2000);

  // ---------------------------------------------------------------- modo TV: letras maiores e sem a faixa de ajuda do topo
  // Automático em placas (ARM, como o Orange Pi); no computador fica como sempre foi. localStorage 'acq_tv' = '1' liga, '0' desliga.
  const tvAuto = () => /arm|aarch/i.test(navigator.platform || '') || ((navigator.hardwareConcurrency || 8) <= 4 && (navigator.deviceMemory || 8) <= 2);
  const tvAtivo = () => { try { const v = localStorage.getItem('acq_tv'); if (v === '1') return true; if (v === '0') return false; } catch (e) { } return tvAuto(); };
  const TV_CENA = 'html,#ui{font-size:clamp(15px,2.75vh,32px)!important}#hud,#zoombar{display:none!important}' +
    '#objs,#mis{font-size:.8em!important;max-width:32%!important;opacity:.93}#clock{font-size:.95em!important}';
  const TV_SHELL = '#chip{zoom:1.4}#pular{zoom:1.4}#hist .card{zoom:1.25}';
  function aplicaTV() {
    const on = tvAtivo();
    for (const w of janelas()) { try { const d = w.document; let st = d.getElementById('gp-tv');
      if (on && !st) { st = d.createElement('style'); st.id = 'gp-tv'; st.textContent = (w === window && NOME_SHELL) ? TV_SHELL : TV_CENA; (d.head || d.documentElement).appendChild(st); }
      if (!on && st) st.remove(); } catch (e) { } }
  }
  setInterval(aplicaTV, 1500); setTimeout(aplicaTV, 200);    // janelas novas (abertura, ambientes que acabaram de carregar)
  function ligaGlifos() { cursor(true); if (glifos) return; glifos = true; try { localStorage.setItem('acq_glifos', '1'); } catch (e) { } atualizaDicas(); }
  if (glifos) setTimeout(atualizaDicas, 0);

  window.__CONTROLE = {
    conectado: () => { const g = navigator.getGamepads ? [...navigator.getGamepads()].filter(Boolean) : []; return g.length ? (g[0].mapping === 'standard' ? 'padrão' : 'outro') : ''; },
    configurado: () => !!mapa,
    nome: () => nomeCtrl,
    glifo,
    aprender(passo, fim) { aprendendo = { i: 0, m: {}, passo, fim, base: null, solta: true }; passo && passo(APRENDE[0][1], 0); },
    cancelar() { aprendendo = null; },
    padrao() { mapa = null; try { localStorage.removeItem('acq_controle'); } catch (e) { } atualizaDicas(); },
    total: APRENDE.length,
    formas: v => { try { localStorage.setItem('acq_formas', v ? '1' : '0'); } catch (e) { } atualizaDicas(); },
    usaFormas: formas,
    tv: () => { try { return localStorage.getItem('acq_tv'); } catch (e) { return null; } },
    tvAtivo,
    defineTV: v => { try { if (v === null) localStorage.removeItem('acq_tv'); else localStorage.setItem('acq_tv', v); } catch (e) { } aplicaTV(); },
    glifos: v => { glifos = !!v; try { localStorage.setItem('acq_glifos', v ? '1' : '0'); } catch (e) { } if (v) atualizaDicas(); },
  };
})();
