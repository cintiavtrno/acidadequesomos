// ===== musica.js — lo-fi gerado na hora (Web Audio), sem arquivo de áudio e sem internet =====
// Piano elétrico em acordes de sétima e nona, baixo macio, bateria preguiçosa com swing, uma melodia que aparece de vez em quando
// e o chiado de disco por baixo. Tudo passa por um filtro que abafa o som (o "lo" do lo-fi).
// Opções (localStorage): 'acq_musica' = '0' desliga; 'acq_vol' = '1' baixo, '2' médio (padrão), '3' alto.
(function () {
  'use strict';
  if (window.__MUSICA) return;
  const AC = window.AudioContext || window.webkitAudioContext; if (!AC) return;
  const ler = (k, d) => { try { const v = localStorage.getItem(k); return v === null ? d : v; } catch (e) { return d; } };
  const VOL = { '1': .1, '2': .18, '3': .3 };
  let ctx = null, mestre, filtro, ligada = ler('acq_musica', '1') !== '0', nivel = ler('acq_vol', '2');

  const BPM = 72, BAT = 60 / BPM, COLCHEIA = BAT / 2, SWING = .09;
  const hz = m => 440 * Math.pow(2, (m - 69) / 12);
  // Fmaj9 · Em7 · Dm9 · Cmaj7 — dois ciclos, o segundo com o último acorde trocado por um Bbmaj7 (respiro antes de voltar)
  const ACORDES = [[53, 57, 60, 64, 67], [52, 55, 59, 62], [50, 53, 57, 60, 64], [48, 52, 55, 59, 62],
                   [53, 57, 60, 64, 67], [52, 55, 59, 62], [50, 53, 57, 60, 64], [46, 50, 53, 57, 60]];
  const ESCALA = [72, 74, 76, 79, 81, 84];       // pentatônica de dó por cima

  let ruido = null;
  function bufRuido() {
    if (ruido) return ruido;
    ruido = ctx.createBuffer(1, ctx.sampleRate * 2, ctx.sampleRate);
    const d = ruido.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
    return ruido;
  }
  function env(g, t, a, pico, dec, fim) { g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(pico, t + a); g.gain.exponentialRampToValueAtTime(fim || 0.0001, t + a + dec); }

  function piano(m, t, dur, vel) {
    const g = ctx.createGain(), o1 = ctx.createOscillator(), o2 = ctx.createOscillator(), trem = ctx.createOscillator(), tg = ctx.createGain();
    o1.type = 'sine'; o2.type = 'triangle'; o1.frequency.value = hz(m); o2.frequency.value = hz(m) * 1.003;
    trem.frequency.value = 4.2; tg.gain.value = .25 * vel; trem.connect(tg); tg.connect(g.gain);
    const g2 = ctx.createGain(); g2.gain.value = .35; o2.connect(g2); g2.connect(g); o1.connect(g); g.connect(filtro);
    env(g, t, .02, .22 * vel, dur, .0001);
    for (const o of [o1, o2, trem]) { o.start(t); o.stop(t + dur + .1); }
  }
  function baixo(m, t, dur) {
    const g = ctx.createGain(), o = ctx.createOscillator(); o.type = 'sine'; o.frequency.value = hz(m - 12);
    o.connect(g); g.connect(filtro); env(g, t, .03, .35, dur, .0001); o.start(t); o.stop(t + dur + .1);
  }
  function bumbo(t) {
    const g = ctx.createGain(), o = ctx.createOscillator(); o.type = 'sine';
    o.frequency.setValueAtTime(110, t); o.frequency.exponentialRampToValueAtTime(42, t + .18);
    o.connect(g); g.connect(filtro); env(g, t, .005, .55, .3); o.start(t); o.stop(t + .4);
  }
  function ruidoCurto(t, tipo, freq, pico, dec) {
    const s = ctx.createBufferSource(), f = ctx.createBiquadFilter(), g = ctx.createGain();
    s.buffer = bufRuido(); f.type = tipo; f.frequency.value = freq; s.connect(f); f.connect(g); g.connect(filtro);
    env(g, t, .004, pico, dec); s.start(t, Math.random()); s.stop(t + dec + .05);
  }
  const caixa = t => ruidoCurto(t, 'bandpass', 1800, .16, .18);
  const chimbal = (t, v) => ruidoCurto(t, 'highpass', 7000, .05 * v, .05);
  function melodia(t) {
    const m = ESCALA[(Math.random() * ESCALA.length) | 0], g = ctx.createGain(), o = ctx.createOscillator(), vib = ctx.createOscillator(), vg = ctx.createGain();
    o.type = 'sine'; o.frequency.value = hz(m); vib.frequency.value = 5; vg.gain.value = 3; vib.connect(vg); vg.connect(o.frequency);
    o.connect(g); g.connect(filtro); env(g, t, .06, .07, 1.1); o.start(t); vib.start(t); o.stop(t + 1.3); vib.stop(t + 1.3);
  }
  function chiado() {        // disco girando: estalos esparsos e um chiado baixinho em loop
    const n = ctx.sampleRate * 4, b = ctx.createBuffer(1, n, ctx.sampleRate), d = b.getChannelData(0);
    for (let i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * .012 + (Math.random() < .0004 ? (Math.random() * 2 - 1) * .5 : 0);
    const s = ctx.createBufferSource(), f = ctx.createBiquadFilter(), g = ctx.createGain();
    s.buffer = b; s.loop = true; f.type = 'bandpass'; f.frequency.value = 3000; f.Q.value = .4; g.gain.value = .5;
    s.connect(f); f.connect(g); g.connect(mestre); s.start();
  }

  let compasso = 0, passo = 0, proximo = 0;
  function agenda(ate) {
    if (ate === undefined) { if (!ctx || ctx.state !== 'running') return; ate = ctx.currentTime + .4; }
    while (proximo < ate) {
      const t = proximo + (passo % 2 ? SWING : 0), ac = ACORDES[compasso % ACORDES.length];
      const semBateria = compasso % 16 >= 14;                     // a cada 16 compassos a bateria descansa dois
      if (passo === 0) { ac.forEach((m, i) => piano(m, t + i * .025, BAT * 3.2, .9)); baixo(ac[0], t, BAT * 1.6); }
      if (passo === 5) { ac.slice(1).forEach((m, i) => piano(m, t + i * .02, BAT * 1.4, .55)); }
      if (passo === 4) baixo(ac[0] + (compasso % 2 ? 7 : 0), t, BAT * 1.2);
      if (!semBateria) {
        if (passo === 0 || passo === 5) bumbo(t);
        if (passo === 2 || passo === 6) caixa(t);
        chimbal(t, passo % 2 ? .6 : 1);
      }
      if (passo % 2 === 0 && Math.random() < .14) melodia(t);
      proximo += COLCHEIA; passo = (passo + 1) % 8; if (passo === 0) compasso++;
    }
  }

  function monta() {
    mestre = ctx.createGain(); mestre.gain.value = ligada ? VOL[nivel] || .18 : 0;
    filtro = ctx.createBiquadFilter(); filtro.type = 'lowpass'; filtro.frequency.value = 2200; filtro.Q.value = .6;
    const comp = ctx.createDynamicsCompressor(); filtro.connect(comp); comp.connect(mestre); mestre.connect(ctx.destination);
    chiado(); proximo = ctx.currentTime + .2;
  }
  function cria() { if (ctx) return; ctx = new AC(); monta(); setInterval(() => agenda(), 120); }
  // prévia sem tocar: grava N segundos num buffer (usado para testar e gerar um .wav de amostra)
  async function grava(seg) {
    const salvo = ctx; ctx = new OfflineAudioContext(2, Math.round(44100 * seg), 44100); ruido = null; compasso = passo = 0;
    const lig = ligada; ligada = true; monta(); agenda(seg); ligada = lig;
    const buf = await ctx.startRendering(); ctx = salvo; ruido = null; return buf;
  }
  function tenta() { try { cria(); if (ctx.state === 'suspended') ctx.resume(); } catch (e) { } }
  // o navegador só deixa tocar depois que alguém aperta algo (no Orange Pi o instalador libera isso logo ao abrir)
  tenta(); setInterval(() => { if (ligada) tenta(); }, 1000);
  for (const ev of ['keydown', 'pointerdown']) addEventListener(ev, tenta, true);

  function aplica() { if (!ctx) return; mestre.gain.setTargetAtTime(ligada ? VOL[nivel] || .18 : 0, ctx.currentTime, .3); }
  window.__MUSICA = {
    tenta,
    grava,
    ligada: () => ligada,
    nivel: () => nivel,
    liga(v) { ligada = !!v; try { localStorage.setItem('acq_musica', v ? '1' : '0'); } catch (e) { } if (v) tenta(); aplica(); },
    volume(n) { nivel = String(n); try { localStorage.setItem('acq_vol', nivel); } catch (e) { } aplica(); },
  };
})();
