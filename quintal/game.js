// ===== game.js — laço, câmera, entrada, HUD do quintal =====
(function (Q) {
  'use strict';
  const FN = { N: 'N · quintal comum', A: 'A · manhã, preparo', B: 'B · chegada', C1: 'C1 · sete meninos comem', C: 'C · adultos à mesa', D: 'D · fim de tarde' };
  Q.Game = function (cv, D, CharLib, ui) {
    const sim = new Q.Sim(D, { rate: window.MUNDO_RATE || 3 }); const R = new Q.Render(cv, sim, CharLib), keys = {}; let last = 0, ativo = true, toastT = 0, saiu = 0, cadDirty = 1, dlgSig = '';
    sim.chegar(); this.sim = sim; this.R = R; this.keys = keys;
    const el = id => document.getElementById(id), toast = (t, s) => { el('toast').textContent = t; el('toast').style.opacity = 1; toastT = s || 3; };
    const scale = () => { const k = fitDisplay(cv, 480, 270); document.documentElement.style.fontSize = Math.max(12, Math.min(22, 4.2 * k + 5)) + 'px'; return k; };
    addEventListener('resize', scale); scale();
    const press = e => {
      const k = e.key.toLowerCase(); if (['arrowup', 'arrowdown', 'arrowleft', 'arrowright', ' '].includes(k)) e.preventDefault();
      if (e.type === 'keyup') { keys[k] = 0; return; } keys[k] = 1;
      if (e.repeat) return;
      if (sim.conversa) { if (k === 'escape') { sim.fecharConversa(); return; } const bs = el('dlg').querySelectorAll('button'); const b = k === '0' ? el('dlg').querySelector('button[data-zero]') : /^[1-9]$/.test(k) ? bs[+k - 1] : null; if (b) { b.click(); e.preventDefault(); } return; }
      if (k === 'b') { const c = el('cad'); c.style.display = c.style.display === 'block' ? 'none' : 'block'; cadDirty = 1; return; }
      if (k === 'e' || k === 'enter' || k === ' ') { const c = sim.acao(); if (c) toast(c.label.replace(/^Examinar |^Observar /, '')); }
      const f = window.MUNDO_ATIVO ? null : { '0': 'N', '1': 'A', '2': 'B', '3': 'C1', '4': 'C', '5': 'D' }[k]; if (f) { sim.forcada = true; sim.fase(f); toast('Fase ' + FN[f] + ' (forçada · tecla 9 volta ao relógio)', 3); }
      if (k === '9' && !window.MUNDO_ATIVO) { sim.forcada = false; toast('Fase pelo relógio', 2); }
      if (k === 'shift') sim.corre = 1;
    };
    addEventListener('keydown', press); addEventListener('keyup', e => { press(e); if (e.key === 'Shift') sim.corre = 0; });
    cv.addEventListener('pointerdown', e => {
      const r = cv.getBoundingClientRect(), px = (e.clientX - r.left) / r.width * 480 + R.cam, py = (e.clientY - r.top) / r.height * 270;
      const X = (px - 24) / 24, Y = (py - 124) / 16; if (sim.conversa) sim.fecharConversa(); if (sim.lia.state === 'sentada') { sim.levantar(); return; }
      for (const id in sim.npcs) { const n = sim.npcs[id]; if (n.vis && Math.hypot(n.x - X, n.y - Y) < 0.55) { if (Math.hypot(n.x - sim.lia.x, n.y - sim.lia.y) < 1.4) sim.falar(id); else sim.liaIr(n.x, n.y + 0.5); return; } }
      sim.liaIr(Math.max(0.2, Math.min(27.8, X)), Math.max(0.3, Math.min(7.95, Y)));
    });
    this.parar = () => { ativo = false; sim.liaPresente = false; }; this.seguir = () => { ativo = true; last = 0; sim.liaPresente = true; };
    this.passo = dt => {
      let vx = (keys.d || keys.arrowright ? 1 : 0) - (keys.a || keys.arrowleft ? 1 : 0), vy = (keys.s || keys.arrowdown ? 1 : 0) - (keys.w || keys.arrowup ? 1 : 0);
      if (sim.conversa && (vx || vy)) sim.fecharConversa();
      if (sim.lia.state === 'sentada' && (vx || vy)) sim.levantar();
      if (sim.lia.state === 'livre') { if (vx || vy) sim.liaMover(vx, vy, dt); }
      sim.update(dt);
      if (saiu > 0) saiu -= dt;
      else if (sim.saindo() && sim.lia.state === 'livre' && (vy > 0 || sim.lia.path.length === 0)) {
        saiu = 1.5; sim.lia.path = []; sim.lia.y = D.D - 0.5;
        if (ui && ui.sair) ui.sair(); else toast('Saída para a rua (só no mundo conectado)', 2);
      }
    };
    const esc = t => String(t).replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c])), nome = id => D.CH[id][0].replace(/ \(.*/, '');
    // painel de conversa (mesmo jeito da rua: Cumprimentar · Perguntar · Ficar ouvindo) e caderninho do quintal
    this.painel = () => {
      while (sim.novas && sim.novas.length) { const id = sim.novas.shift(); toast('Anotação nova · ' + sim.kp[id].titulo, 4.5); cadDirty = 1; }
      const d = el('dlg'), c = sim.conversa;
      if (!c) { if (d.style.display !== 'none') { d.style.display = 'none'; dlgSig = ''; } }
      else {
        const sig = c.id + '|' + c.modo + '|' + c.linhas.map(l => l.texto).join('¦') + '|' + sim.topicosDe(c.id).map(t => t.id + t.feito).join(',');
        if (sig !== dlgSig) {
          dlgSig = sig; const tp = sim.topicosDe(c.id); let h = '<h3>' + esc(nome(c.id)) + '</h3>';
          h += c.linhas.map(l => l.quem === 'nota' ? '<div class="line nota">' + esc(l.texto) + '</div>' : '<div class="line"><b>' + esc(l.quem === 'lia' ? 'Lia' : nome(l.quem)) + ':</b> ' + esc(l.texto) + (l.rev ? ' <span class="rev">· proposta, precisa de revisão cultural</span>' : '') + '</div>').join('');
          h += '<div class="opts">';
          if (c.modo === 'raiz') {
            h += '<button data-a="saudar">1 · Cumprimentar</button>'; let n = 2;
            if (sim.temAssunto(c.id)) h += '<button data-a="topicos">' + (n++) + ' · Perguntar</button>';
            h += '<button data-a="ouvir">' + n + ' · Ficar ouvindo</button><button data-a="sair" data-zero="1">0 · Sair</button>';
          } else {
            if (!tp.length) h += '<div class="line nota">' + esc(sim.dicaSemAssunto) + '</div>';
            tp.forEach((t, i) => { h += '<button data-a="perguntar" data-g="' + t.id + '">' + (i + 1) + ' · ' + esc(t.label) + (t.feito ? ' ✓' : '') + '</button>'; });
            h += '<button data-a="voltar" data-zero="1">0 · Voltar</button>';
          }
          d.innerHTML = h + '</div>'; d.style.display = 'block';
        }
      }
      if (cadDirty) { cadDirty = 0; const cd = el('cad'); const L = sim.notas().sort((a, b) => a.min - b.min); cd.innerHTML = '<h3>Caderninho do quintal · ' + L.length + '</h3>' + (L.length ? L.map(n => '<div class="it"><b>' + esc(n.titulo) + '</b><br>' + esc(n.texto) + '</div>').join('') : '<div class="it">Ainda não anotei nada aqui. Converse com as pessoas e olhe o quintal.</div>'); }
    };
    el('dlg').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; sim.conversaAcao(b.dataset.a, b.dataset.g); e.stopPropagation(); });
    this.desenhar = dt => {
      R.frame(dt); const h = sim.clock; el('clock').innerHTML = '<b>' + String(h.hh).padStart(2, '0') + ':' + String(h.mm).padStart(2, '0') + '</b> · quintal de Dona Zefa' + (sim.normal ? '' : ' · caruru · ' + FN[sim.fasen]);
      const c = sim.candidatos(), pr = el('prompt'); if (c.length) { pr.style.opacity = 1; pr.innerHTML = '<span class="k">E</span> ' + c[0].label; } else pr.style.opacity = 0;
      this.painel();
      if (sim.msg) { el('fala').style.opacity = 1; el('fala').textContent = sim.msg.txt; } else el('fala').style.opacity = 0;
      if (sim.exam) { /* reservado */ }
      if (toastT > 0) { toastT -= dt; if (toastT <= 0) el('toast').style.opacity = 0; }
    };
    const laco = now => { requestAnimationFrame(laco); if (!ativo) return; const dt = last ? Math.min(0.1, (now - last) / 1000) : 0.016; last = now; this.passo(dt); this.desenhar(dt); };
    this.iniciar = () => requestAnimationFrame(laco);
    toast('Setas/WASD andam · E interage e conversa · B abre o caderninho do quintal', 6);
  };
})(window.Quintal);
