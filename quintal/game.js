// ===== game.js — laço, câmera, entrada, HUD do quintal =====
(function (Q) {
  'use strict';
  const FN = { A: 'A · manhã, preparo', B: 'B · chegada', C1: 'C1 · sete meninos comem', C: 'C · adultos à mesa', D: 'D · fim de tarde' };
  Q.Game = function (cv, D, CharLib, ui) {
    const sim = new Q.Sim(D, { rate: 0.25 }); sim.fase('B'); const R = new Q.Render(cv, sim, CharLib), keys = {}; let last = 0, ativo = true, toastT = 0, saiu = 0;
    sim.chegar(); this.sim = sim; this.R = R; this.keys = keys;
    const el = id => document.getElementById(id), toast = (t, s) => { el('toast').textContent = t; el('toast').style.opacity = 1; toastT = s || 3; };
    const scale = () => { const k = fitDisplay(cv, 480, 270); document.documentElement.style.fontSize = Math.max(12, Math.min(22, 4.2 * k + 5)) + 'px'; return k; };
    addEventListener('resize', scale); scale();
    const press = e => {
      const k = e.key.toLowerCase(); if (['arrowup', 'arrowdown', 'arrowleft', 'arrowright', ' '].includes(k)) e.preventDefault();
      if (e.type === 'keyup') { keys[k] = 0; return; } keys[k] = 1;
      if (e.repeat) return;
      if (k === 'e' || k === 'enter' || k === ' ') { const c = sim.acao(); if (c) toast(c.label.replace(/^Examinar |^Observar /, '')); }
      const f = { '1': 'A', '2': 'B', '3': 'C1', '4': 'C', '5': 'D' }[k]; if (f) { sim.fase(f); toast('Fase ' + FN[f], 3); }
      if (k === 'shift') sim.corre = 1;
    };
    addEventListener('keydown', press); addEventListener('keyup', e => { press(e); if (e.key === 'Shift') sim.corre = 0; });
    cv.addEventListener('pointerdown', e => {
      const r = cv.getBoundingClientRect(), px = (e.clientX - r.left) / r.width * 480 + R.cam, py = (e.clientY - r.top) / r.height * 270;
      const X = (px - 24) / 24, Y = (py - 124) / 16; if (sim.lia.state === 'sentada') { sim.levantar(); return; }
      for (const id in sim.npcs) { const n = sim.npcs[id]; if (n.vis && Math.hypot(n.x - X, n.y - Y) < 0.55) { if (Math.hypot(n.x - sim.lia.x, n.y - sim.lia.y) < 1.4) sim.falar(id); else sim.liaIr(n.x, n.y + 0.5); return; } }
      sim.liaIr(Math.max(0.2, Math.min(27.8, X)), Math.max(0.3, Math.min(7.95, Y)));
    });
    this.parar = () => { ativo = false; }; this.seguir = () => { ativo = true; last = 0; };
    this.passo = dt => {
      let vx = (keys.d || keys.arrowright ? 1 : 0) - (keys.a || keys.arrowleft ? 1 : 0), vy = (keys.s || keys.arrowdown ? 1 : 0) - (keys.w || keys.arrowup ? 1 : 0);
      if (sim.lia.state === 'sentada' && (vx || vy)) sim.levantar();
      if (sim.lia.state === 'livre') { if (vx || vy) sim.liaMover(vx, vy, dt); }
      sim.update(dt);
      if (saiu > 0) saiu -= dt;
      else if (sim.saindo() && sim.lia.state === 'livre' && (vy > 0 || sim.lia.path.length === 0)) {
        saiu = 1.5; sim.lia.path = []; sim.lia.y = D.D - 0.5;
        if (ui && ui.sair) ui.sair(); else toast('Saída para a rua (só no mundo conectado)', 2);
      }
    };
    this.desenhar = dt => {
      R.frame(dt); const h = sim.clock; el('clock').innerHTML = '<b>' + String(h.hh).padStart(2, '0') + ':' + String(h.mm).padStart(2, '0') + '</b> · quintal de Dona Zefa · fase ' + FN[sim.fasen];
      const c = sim.candidatos(), pr = el('prompt'); if (c.length) { pr.style.opacity = 1; pr.innerHTML = '<span class="k">E</span> ' + c[0].label; } else pr.style.opacity = 0;
      if (sim.msg) { el('fala').style.opacity = 1; el('fala').textContent = sim.msg.txt; } else el('fala').style.opacity = 0;
      if (sim.exam) { /* reservado */ }
      if (toastT > 0) { toastT -= dt; if (toastT <= 0) el('toast').style.opacity = 0; }
    };
    const laco = now => { requestAnimationFrame(laco); if (!ativo) return; const dt = last ? Math.min(0.1, (now - last) / 1000) : 0.016; last = now; this.passo(dt); this.desenhar(dt); };
    this.iniciar = () => requestAnimationFrame(laco);
    toast('Setas/WASD andam · E interage · 1–5 trocam a fase · clique anda até o ponto', 5);
  };
})(window.Quintal);
