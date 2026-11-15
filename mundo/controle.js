// ===== controle.js — joystick (PlayStation e parecidos) sem programa externo =====
// Lê o controle pelo Gamepad API do navegador e transforma cada botão em tecla para quem está na tela:
// a abertura, as telas do shell, o ambiente ativo (rua, padaria, casa, quintal) ou a rua de 1996.
// Mapa:
//   setas e analógico esquerdo ... andar e escolher
//   bola ......................... interagir / confirmar (E, Enter)
//   X ............................ voltar / fechar (Esc)
//   triângulo .................... caderninho (B)
//   quadrado ..................... Pular
//   R1 ........................... botão do alto (esperar o anoitecer, subir para dormir)
//   L1 / L2 / R2 .................. folhear o caderninho da padaria (L1 volta, R1/R2 avança quando ele está aberto)
//   start (options) .............. volta para o menu principal
// Nas conversas, as setas passam pelas respostas (a escolhida fica com contorno) e a bola escolhe; não precisa mais de 1, 2, 3.
// Controle que não segue o padrão do navegador: Opções > Configurar controle (o mapa aprendido fica em localStorage 'acq_controle').
(function () {
  'use strict';
  if (window.__CONTROLE) return;
  const PADRAO = { cima: { b: 12 }, baixo: { b: 13 }, esq: { b: 14 }, dir: { b: 15 }, bola: { b: 1 }, x: { b: 0 }, tri: { b: 3 }, quad: { b: 2 }, l1: { b: 4 }, r1: { b: 5 }, l2: { b: 6 }, r2: { b: 7 }, start: { b: 9 } };
  const APRENDE = [['cima', 'SETA PARA CIMA'], ['baixo', 'SETA PARA BAIXO'], ['esq', 'SETA PARA A ESQUERDA'], ['dir', 'SETA PARA A DIREITA'], ['bola', 'BOLA (confirmar)'], ['x', 'X (voltar)'], ['tri', 'TRIÂNGULO (caderninho)'], ['quad', 'QUADRADO (pular)'], ['r1', 'R1'], ['start', 'START (menu)']];
  const lerMapa = () => { try { return JSON.parse(localStorage.getItem('acq_controle')); } catch (e) { return null; } };
  let mapa = lerMapa();
  const NOME_SHELL = !!document.getElementById('f_rua');    // index.html (shell) ou rua96.html

  // ---------------------------------------------------------------- para quem vão as teclas
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
  const marcados = new WeakMap();
  function marca(j) {
    let i = j.el.__gpSel | 0; if (i >= j.bs.length) i = j.bs.length - 1; j.el.__gpSel = i;
    j.bs.forEach((b, k) => { const on = k === i; if (on && !marcados.get(b)) { b.style.outline = '3px solid #f0c98c'; b.style.outlineOffset = '2px'; marcados.set(b, 1); } else if (!on && marcados.get(b)) { b.style.outline = ''; b.style.outlineOffset = ''; marcados.delete(b); } });
  }
  function moveJanela(j, d) { j.el.__gpSel = ((j.el.__gpSel | 0) + d + j.bs.length) % j.bs.length; marca(j); }

  // ---------------------------------------------------------------- leitura do controle
  const segura = {};          // ação -> { desde, prox, w, key }
  const ESPERA = 380, RITMO = 140;
  function ativo(gp, m, nome) {
    const e = m[nome]; if (!e) return false;
    if (e.b !== undefined) { const b = gp.buttons[e.b]; return !!b && (b.pressed || b.value > .5); }
    if (e.a !== undefined) { const v = gp.axes[e.a] || 0; return e.s > 0 ? v > .5 : v < -.5; }
    return false;
  }
  function estado(gp) {
    const m = mapa || PADRAO, s = {};
    for (const n in PADRAO) s[n] = ativo(gp, m, n);
    // o analógico esquerdo sempre anda, em qualquer controle
    const ax = gp.axes[0] || 0, ay = gp.axes[1] || 0;
    if (ay < -.5) s.cima = true; if (ay > .5) s.baixo = true; if (ax < -.5) s.esq = true; if (ax > .5) s.dir = true;
    return s;
  }
  const SETA = { cima: 'ArrowUp', baixo: 'ArrowDown', esq: 'ArrowLeft', dir: 'ArrowRight' };
  function aperta(n) {
    const a = alvo(), w = a.w, j = a.tipo === 'jogo' ? janela(w) : null;
    if (SETA[n]) {
      if (j) { moveJanela(j, n === 'cima' || n === 'esq' ? -1 : 1); return null; }
      tecla(w, SETA[n], 'keydown'); return { w, key: SETA[n] };
    }
    if (n === 'bola') {
      if (j) { const i = j.el.__gpSel | 0; j.el.__gpSel = 0; j.bs[i] && j.bs[i].click(); return null; }
      const k = a.tipo === 'jogo' ? 'e' : 'Enter'; tecla(w, k, 'keydown'); return { w, key: k };
    }
    if (n === 'x') { tecla(w, 'Escape', 'keydown'); return { w, key: 'Escape' }; }
    if (n === 'tri' && a.tipo === 'jogo') { tecla(w, 'b', 'keydown'); return { w, key: 'b' }; }
    if (n === 'quad' && a.tipo === 'jogo') {
      if (NOME_SHELL) { try { menuPular(); } catch (e) { } } else { const p = document.getElementById('pbtn'); p && p.click(); }
      return null;
    }
    if (n === 'r1' && a.tipo === 'jogo') { const b = document.getElementById('cb') || document.getElementById('ce'); if (b) { b.click(); return null; } tecla(w, 'ArrowRight', 'keydown'); return { w, key: 'ArrowRight' }; }
    if ((n === 'l1' || n === 'l2') && a.tipo === 'jogo') { tecla(w, 'ArrowLeft', 'keydown'); return { w, key: 'ArrowLeft' }; }
    if (n === 'r2' && a.tipo === 'jogo') { tecla(w, 'ArrowRight', 'keydown'); return { w, key: 'ArrowRight' }; }
    if (n === 'start' && a.tipo !== 'abertura') { if (NOME_SHELL) location.reload(); else location.href = 'index.html'; return null; }
    return null;
  }
  // aprender um controle diferente: espera um botão ou um eixo sair do repouso
  let aprendendo = null;
  function aprender(gp) {
    const A = aprendendo; if (!A.base) { A.base = { b: gp.buttons.map(b => b.pressed || b.value > .5), a: gp.axes.slice() }; return; }
    if (A.solta) { if (gp.buttons.some(b => b.pressed || b.value > .5) || gp.axes.some((v, i) => Math.abs(v - A.base.a[i]) > .5)) return; A.solta = false; return; }
    let e = null;
    gp.buttons.forEach((b, i) => { if (!e && (b.pressed || b.value > .5) && !A.base.b[i]) e = { b: i }; });
    if (!e) gp.axes.forEach((v, i) => { if (!e && Math.abs(v - A.base.a[i]) > .6) e = { a: i, s: v > A.base.a[i] ? 1 : -1 }; });
    if (!e) return;
    A.m[APRENDE[A.i][0]] = e; A.i++; A.solta = true;
    if (A.i >= APRENDE.length) { for (const n in PADRAO) if (!A.m[n]) A.m[n] = { b: -1 }; mapa = A.m; try { localStorage.setItem('acq_controle', JSON.stringify(mapa)); } catch (x) { } const f = A.fim; aprendendo = null; f && f(); }
    else A.passo && A.passo(APRENDE[A.i][1], A.i);
  }
  let antes = {}, nomeCtrl = '';
  function laco(now) {
    const gps = navigator.getGamepads ? [...navigator.getGamepads()].filter(Boolean) : [];
    const gp = gps[0];
    if (gp) {
      nomeCtrl = gp.id;
      if (aprendendo) aprender(gp);
      else {
        const s = estado(gp);
        for (const n in s) {
          if (s[n] && !antes[n]) { ligaGlifos(); const r = aperta(n); segura[n] = { desde: now, prox: now + ESPERA, r }; }
          else if (s[n] && segura[n] && SETA[n] && now >= segura[n].prox) {          // segurar a seta repete (menus e listas); andar usa a tecla presa
            segura[n].prox = now + RITMO; const r = segura[n].r;
            if (r) tecla(r.w, r.key, 'keydown', true); else { const a = alvo(), j = a.tipo === 'jogo' ? janela(a.w) : null; if (j) moveJanela(j, n === 'cima' || n === 'esq' ? -1 : 1); }
          } else if (!s[n] && antes[n]) { const g = segura[n]; if (g && g.r) tecla(g.r.w, g.r.key, 'keyup'); delete segura[n]; }
        }
        antes = s;
        const a = alvo(); if (a.tipo === 'jogo') { const j = janela(a.w); if (j) marca(j); }
      }
    }
    requestAnimationFrame(laco);
  }
  requestAnimationFrame(laco);

  // ---------------------------------------------------------------- dicas na tela: "E", "B", "Esc" viram os botões do controle
  // Liga quando alguém aperta um botão do controle (e fica lembrado em localStorage 'acq_glifos').
  const COR = { '◯': '#e8505b', '✕': '#6f9ff0', '△': '#44c08a', '□': '#e07fc4' };
  const TECLA = { 'E': '◯', 'e': '◯', 'Enter': '◯', 'B': '△', 'b': '△', 'Esc': '✕', 'WASD': 'analógico', 'W A S D': 'analógico' };
  const TROCAS = [[/\(E\)/g, '(◯)'], [/\(Esc\)/g, '(✕)'], [/\(B\)/g, '(△)'], [/\bEsc para\b/g, '✕ para'], [/\b([Aa]perte) E\b/g, '$1 ◯'], [/\btecla E\b/g, 'botão ◯'], [/^E · /, '◯ · '], [/^E (Falar|falar|Examinar|examinar|Entrar|entrar|Pegar|pegar|Sentar|sentar)/, '◯ $1']];
  let glifos = (() => { try { return localStorage.getItem('acq_glifos') === '1'; } catch (e) { return false; } })();
  function trocaTexto(no) {
    let t = no.nodeValue, n = t; for (const [re, by] of TROCAS) n = n.replace(re, by);
    const pai = no.parentNode;
    if (pai && pai.tagName === 'BUTTON' && pai.closest && pai.closest('#dlg') && no === pai.firstChild) n = n.replace(/^\d+ · /, '');   // conversa: sem 1, 2, 0 na frente
    if (n !== t) no.nodeValue = n;
  }
  function trocaEm(raiz) {
    if (!raiz || !raiz.ownerDocument && raiz.nodeType !== 9) return;
    const d = raiz.nodeType === 9 ? raiz : raiz.ownerDocument;
    if (raiz.nodeType === 3) { trocaTexto(raiz); return; }
    if (raiz.nodeType !== 1 && raiz.nodeType !== 9) return;
    const els = raiz.querySelectorAll ? [...raiz.querySelectorAll('.k,kbd')] : []; if (raiz.matches && raiz.matches('.k,kbd')) els.push(raiz);
    for (const el of els) { const v = TECLA[el.textContent.trim()]; if (v && el.textContent !== v) { el.textContent = v; if (COR[v]) { el.style.color = COR[v]; el.style.fontWeight = '700'; } } }
    const w = d.createTreeWalker(raiz, 4, { acceptNode: x => /^(SCRIPT|STYLE|TEXTAREA)$/.test(x.parentNode && x.parentNode.nodeName) ? 2 : 1 });
    let x; while ((x = w.nextNode())) trocaTexto(x);
  }
  function vigia(doc) {
    if (!doc || !doc.body || doc.__glifos) return; doc.__glifos = true; trocaEm(doc.body);
    let pend = new Set(), ag = 0;
    new doc.defaultView.MutationObserver(rs => { for (const r of rs) { if (r.type === 'characterData') pend.add(r.target); else r.addedNodes.forEach(n => pend.add(n)); }
      if (!ag) ag = setTimeout(() => { ag = 0; const p = pend; pend = new Set(); p.forEach(trocaEm); }, 0); }).observe(doc.body, { childList: true, subtree: true, characterData: true });
  }
  function vigiaTudo() {
    if (!glifos) return; vigia(document);
    if (NOME_SHELL) for (const id of ['rua', 'padaria', 'casa', 'quintal']) { try { vigia(document.getElementById('f_' + id).contentDocument); } catch (e) { } }
  }
  setInterval(vigiaTudo, 1000);
  function ligaGlifos() { if (glifos) return; glifos = true; try { localStorage.setItem('acq_glifos', '1'); } catch (e) { } vigiaTudo(); }

  window.__CONTROLE = {
    conectado: () => { const g = navigator.getGamepads ? [...navigator.getGamepads()].filter(Boolean) : []; return g.length ? (g[0].mapping === 'standard' ? 'padrão' : 'outro') : ''; },
    configurado: () => !!mapa,
    nome: () => nomeCtrl,
    aprender(passo, fim) { aprendendo = { i: 0, m: {}, passo, fim, base: null, solta: true }; passo && passo(APRENDE[0][1], 0); },
    cancelar() { aprendendo = null; },
    padrao() { mapa = null; try { localStorage.removeItem('acq_controle'); } catch (e) { } },
    total: APRENDE.length,
    glifos: v => { glifos = !!v; try { localStorage.setItem('acq_glifos', v ? '1' : '0'); } catch (e) { } if (v) vigiaTudo(); },
  };
})();
