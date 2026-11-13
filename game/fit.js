// fit.js — ocupa 100% da janela preservando 16:9 e pixel art nítida; câmera suave e paralaxe sem tremor.
// O jogo continua desenhando em VW×VH lógicos (480×270) no canvas original, que fica transparente por cima e só recebe cliques;
// a imagem visível é um canvas de exibição: ampliação inteira por vizinho mais próximo (n = ⌈escala⌉) e, se a escala não for inteira,
// redução suave final até o tamanho exato da janela (sem pixels de larguras desiguais nem sprites borrados).
// Câmera suave: o jogo move a câmera em número fracionário (Cam.follow, mola amortecida) e escreve em fitSub a fração de pixel que sobra;
// aqui a imagem é deslocada nessa fração, já ampliada, em passos de 1/n de pixel lógico. Tudo o que é desenhado dentro do jogo continua
// em pixel inteiro, então nada treme e os pixels mantêm sempre a mesma largura.
// Paralaxe: o fundo (céu, nuvens, morro, casario) não entra no canvas do jogo. Plx desenha cada camada aqui, também já ampliada,
// com a sua própria velocidade e a sua própria fração de pixel.
(function () {
  let disp, dctx, inter, ictx, src, W = 0, H = 0, n = 1, iw = 0, ih = 0, VWr = 480, VHr = 270;
  // fundo ambiente: onde a janela é mais larga/alta que 16:9, as faixas laterais mostram uma versão borrada e escurecida da própria cena (sem esticar o jogo)
  let amb, actx, ambN = 0;
  function ambiente() {
    if (!amb) { amb = document.createElement('canvas'); amb.width = 96; amb.height = 54; amb.setAttribute('aria-hidden', 'true'); actx = amb.getContext('2d'); amb.style.cssText = 'position:fixed;left:-6%;top:-6%;width:112%;height:112%;z-index:-1;pointer-events:none;filter:blur(10px) brightness(.85) saturate(1.15);image-rendering:auto'; document.body.prepend(amb); document.body.style.background = 'transparent'; }
    actx.drawImage(disp, 0, 0, 96, 54);
  }
  window.fitSub = { x: 0, y: 0 };      // fração de pixel (em pixels lógicos do canvas do jogo) que a imagem desloca para a esquerda e para cima
  window.fitBackdrop = null;           // função (g, k, tw, th): desenha o fundo atrás do jogo; k = pixels de tela por pixel lógico
  function blit() {
    requestAnimationFrame(blit); if (!disp || !src || document.hidden) return;
    if ((ambN++ % 8) === 0 && (innerWidth * VHr > innerHeight * VWr * 1.02 || innerHeight * VWr > innerWidth * VHr * 1.02)) ambiente();
    let g, tw, th, k;
    if (inter) { g = ictx; tw = iw; th = ih; k = n; } else { g = dctx; tw = W; th = H; k = W / VWr; }
    g.imageSmoothingEnabled = false; g.clearRect(0, 0, tw, th);
    if (window.fitBackdrop) window.fitBackdrop(g, k, tw, th);
    const sx = Math.max(0, Math.round(window.fitSub.x * k)), sy = Math.max(0, Math.round(window.fitSub.y * k));
    g.drawImage(src, 0, 0, VWr, VHr, -sx, -sy, tw, th);
    if (sx > 0) g.drawImage(src, VWr - 1, 0, 1, VHr, tw - sx, -sy, sx, th);      // borda que o deslocamento descobre: repete a última coluna/linha
    if (sy > 0) g.drawImage(src, 0, VHr - 1, VWr, 1, -sx, th - sy, tw, sy);
    if (inter) { dctx.imageSmoothingEnabled = true; dctx.imageSmoothingQuality = 'high'; dctx.drawImage(inter, 0, 0, W, H); }
  }
  window.fitDisplay = function (cv, VW, VH) {
    const w = innerWidth, h = innerHeight; if (w < 2 || h < 2) return 1;
    const s = Math.min(w / VW, h / VH), cw = Math.round(VW * s), ch = Math.round(VH * s), dpr = window.devicePixelRatio || 1;
    cv.style.width = cw + 'px'; cv.style.height = ch + 'px';
    if (!disp) {
      src = cv; disp = document.createElement('canvas'); disp.setAttribute('aria-hidden', 'true'); dctx = disp.getContext('2d');
      disp.style.cssText = 'position:absolute;left:0;top:0;pointer-events:none;image-rendering:pixelated'; cv.style.position = 'relative'; cv.style.opacity = '0';
      cv.parentNode.insertBefore(disp, cv); requestAnimationFrame(blit);
    }
    VWr = VW; VHr = VH; W = Math.max(1, Math.round(cw * dpr)); H = Math.max(1, Math.round(ch * dpr)); disp.width = W; disp.height = H; disp.style.width = cw + 'px'; disp.style.height = ch + 'px';
    n = Math.min(8, Math.max(1, Math.ceil(W / VW)));
    if (W === VW * n && H === VH * n || n === 1 && W <= VW) inter = null;
    else { inter = inter || document.createElement('canvas'); iw = VW * n; ih = VH * n; inter.width = iw; inter.height = ih; ictx = inter.getContext('2d'); }
    return s;
  };

  // ---------------------------------------------------------------- câmera: mola criticamente amortecida
  // Cam.damp: aproxima cur de alvo sem oscilar e sem passar do ponto; smooth ≈ tempo (s) para chegar perto. vel é a velocidade atual.
  // Cam.follow(st, tx, ty, dt): segue (tx,ty) escrevendo st.vx e st.vy em número fracionário. Olha um pouco para onde a pessoa anda (avanço).
  // Passe o alvo já em pixel inteiro: a mola filtra os degraus de 1 px e a pessoa fica quase parada na tela enquanto anda.
  const Cam = {
    damp(cur, tgt, vel, smooth, dt) {
      const om = 2 / Math.max(0.0001, smooth), x = om * dt, e = 1 / (1 + x + 0.48 * x * x + 0.235 * x * x * x), ch = cur - tgt, tmp = (vel + om * ch) * dt;
      return { x: tgt + (ch + tmp) * e, v: (vel - om * tmp) * e };
    },
    reset(st) { st._kx = st._ky = st._sp = st._lead = 0; st._px = null; },
    follow(st, tx, ty, dt, o) {
      o = o || {}; dt = Math.min(Math.max(dt, 0), 0.05); if (dt <= 0) return;
      const lead = o.lead != null ? o.lead : 18, tr = o.smooth || 0.22;
      if (st._px == null) { st._px = tx; st._sp = 0; st._lead = 0; st._kx = st._ky = 0; }
      const sp = (tx - st._px) / dt; st._px = tx; st._sp += (sp - st._sp) * Math.min(1, dt * 8);
      const want = Math.max(-lead, Math.min(lead, st._sp * 0.3)); st._lead += (want - st._lead) * Math.min(1, dt * 2.5);
      const a = Cam.damp(st.vx, tx + st._lead, st._kx || 0, tr, dt), b = Cam.damp(st.vy, ty, st._ky || 0, tr * 1.3, dt);
      st.vx = a.x; st._kx = a.v; st.vy = b.x; st._ky = b.v;
    }
  };
  window.Cam = Cam;

  // ---------------------------------------------------------------- paralaxe
  // Plx.layers: lista do fundo para o primeiro plano, cada uma { img, f, fy, tile, drift }.
  //   f = fração do deslocamento da câmera (0 = parada no céu, 1 = anda junto com o mundo), fy = o mesmo na vertical (padrão f),
  //   tile = repete na horizontal, drift = px de camada por segundo que a camada anda sozinha (nuvens).
  // Plx.view = { x, y, z }: canto superior esquerdo da janela no mundo (com fração) e zoom. O jogo atualiza a cada quadro.
  const reduz = typeof matchMedia === 'function' && matchMedia('(prefers-reduced-motion: reduce)').matches;
  window.Plx = {
    layers: [], view: { x: 0, y: 0, z: 1 },
    draw(g, k, tw, th) {
      const V = this.view, kz = k * V.z, t = reduz ? 0 : performance.now() / 1000;
      for (const L of this.layers) {
        const im = L.img; if (!im || !im.width) continue;
        const lw = im.width, lh = im.height, py = V.y * (L.fy != null ? L.fy : L.f), syI = Math.floor(py), dy = -Math.round((py - syI) * kz);
        const sh = Math.min(Math.ceil(th / kz) + 1, lh - syI); if (sh <= 0) continue;
        let px = V.x * L.f + (L.drift || 0) * t;
        if (L.tile) {
          px = ((px % lw) + lw) % lw; let sxI = Math.floor(px), x = -Math.round((px - sxI) * kz);
          while (x < tw) { const sw = Math.min(lw - sxI, Math.ceil((tw - x) / kz)); g.drawImage(im, sxI, syI, sw, sh, x, dy, sw * kz, sh * kz); x += sw * kz; sxI = 0; }
        } else {
          px = Math.max(0, Math.min(lw - 1, px)); const sxI = Math.floor(px), dx = -Math.round((px - sxI) * kz), sw = Math.min(lw - sxI, Math.ceil(tw / kz) + 1);
          g.drawImage(im, sxI, syI, sw, sh, dx, dy, sw * kz, sh * kz);
        }
      }
    }
  };
  window.fitBackdrop = function (g, k, tw, th) { if (window.Plx.layers.length) window.Plx.draw(g, k, tw, th); };
})();
