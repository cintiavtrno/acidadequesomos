// fit.js — ocupa 100% da janela preservando 16:9 e pixel art nítida.
// O jogo continua desenhando em VW×VH lógicos (480×270) no canvas original, que fica transparente por cima e só recebe cliques;
// a imagem visível é um canvas de exibição: ampliação inteira por vizinho mais próximo (n = ⌈escala⌉) e, se a escala não for inteira,
// redução suave final até o tamanho exato da janela (sem pixels de larguras desiguais nem sprites borrados).
(function () {
  let disp, dctx, inter, ictx, src, W = 0, H = 0, n = 1, iw = 0, ih = 0, VWr = 480, VHr = 270;
  // fundo ambiente: onde a janela é mais larga/alta que 16:9, as faixas laterais mostram uma versão borrada e escurecida da própria cena (sem esticar o jogo)
  let amb, actx, ambN = 0;
  function ambiente() {
    if (!amb) { amb = document.createElement('canvas'); amb.width = 96; amb.height = 54; amb.setAttribute('aria-hidden', 'true'); actx = amb.getContext('2d'); amb.style.cssText = 'position:fixed;left:-6%;top:-6%;width:112%;height:112%;z-index:-1;pointer-events:none;filter:blur(10px) brightness(.85) saturate(1.15);image-rendering:auto'; document.body.prepend(amb); document.body.style.background = 'transparent'; }
    actx.drawImage(src, 0, 0, 96, 54);
  }
  function blit() {
    requestAnimationFrame(blit); if (!disp || !src || document.hidden) return;
    if ((ambN++ % 8) === 0 && (innerWidth * VHr > innerHeight * VWr * 1.02 || innerHeight * VWr > innerWidth * VHr * 1.02)) ambiente();
    if (inter) { ictx.imageSmoothingEnabled = false; ictx.drawImage(src, 0, 0, iw, ih); dctx.imageSmoothingEnabled = true; dctx.imageSmoothingQuality = 'high'; dctx.drawImage(inter, 0, 0, W, H); }
    else { dctx.imageSmoothingEnabled = false; dctx.drawImage(src, 0, 0, W, H); }
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
})();
