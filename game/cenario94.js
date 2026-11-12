// ===== cenario94.js — o que muda no cenário em 1994 (rua, padaria, casa) =====
// 1992–1995: obra pesada, casas interditadas e moradores saindo. Em 1991 a rua só recebe a notícia; em 1994 ela já mostra o efeito.
// Tudo aqui é pintado em canvas por cima do cenário de 1991 (que continua igual), no mesmo estilo de pixel: sem contorno preto grosso, cores quentes e apagadas.
// Textos minúsculos usam uma fonte 3×5 própria. Só roda no navegador; o Node nunca carrega este arquivo.
const C94 = (() => {
  const G = {
    'A': '.#.#.#####.##.#', 'B': '##.#.###.#.###.', 'C': '.###..#..#...##', 'D': '##.#.##.##.###.', 'E': '####..##.#..###', 'F': '####..##.#..#..', 'G': '.###..#.##.#.##', 'H': '#.##.#####.##.#',
    'I': '###.#..#..#.###', 'J': '..#..#..##.#.#.', 'L': '#..#..#..#..###', 'M': '#.########.##.#', 'N': '##.#.##.##.##.#', 'O': '.#.#.##.##.#.#.', 'P': '##.#.###.#..#..', 'Q': '.#.#.##.#.##..#', 'R': '##.#.###.#.##.#',
    'S': '.###...#...###.', 'T': '###.#..#..#..#.', 'U': '#.##.##.##.####', 'V': '#.##.##.##.#.#.', 'X': '#.##.#.#.#.##.#', 'Y': '#.##.#.#..#..#.', 'Z': '###..#.#.#..###', 0: '####.##.##.####',
    1: '.#.##..#..#.###', 2: '##...#.#.#..###', 3: '##...#.#...###.', 4: '#.##.####..#..#', 5: '####..##...###.', 6: '.###..####.####', 7: '###..#.#..#..#.', 8: '####.#####.####',
    9: '####.####..###.', '.': '.............#.', '-': '......###......', '!': '.#..#..#.....#.',
  };
  const px = (c, x, y, w, h, col) => { c.fillStyle = col; c.fillRect(Math.round(x), Math.round(y), Math.round(w), Math.round(h)); };
  // texto 3×5 (esc = escala); "Ã" é A com um til
  const txt = (c, s, x, y, col, esc) => {
    esc = esc || 1; let cx = x;
    for (const ch of s) {
      if (ch === ' ') { cx += 4 * esc; continue; }
      const til = ch === 'Ã', k = til ? 'A' : ch, g = G[k]; if (!g) { cx += 4 * esc; continue; }
      c.fillStyle = col;
      for (let i = 0; i < 15; i++) if (g[i] === '#') c.fillRect(cx + (i % 3) * esc, y + Math.floor(i / 3) * esc, esc, esc);
      if (til) { c.fillRect(cx, y - 2 * esc, esc, esc); c.fillRect(cx + esc, y - 3 * esc, esc, esc); c.fillRect(cx + 2 * esc, y - 2 * esc, esc, esc); }
      cx += 4 * esc;
    }
    return cx - x - esc;
  };
  const largura = (s, esc) => s.length * 4 * (esc || 1) - (esc || 1);
  const mk = (w, h) => { const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const c = cv.getContext('2d'); c.imageSmoothingEnabled = false; return [cv, c]; };
  const tabua = (c, x, y, w, h, i) => {   // uma tábua pregada às pressas: cor, veio e dois pregos
    const cor = ['#8a6a43', '#7c5e3a', '#957449'][i % 3];
    px(c, x, y, w, h, cor); px(c, x, y, w, 1, '#a88858'); px(c, x, y + h - 1, w, 1, '#5e452a');
    px(c, x + 2, y + 2, Math.max(1, w - 6), 1, 'rgba(60,40,20,.35)'); px(c, x + 1, y + (h >> 1), 1, 1, '#2d2218'); px(c, x + w - 2, y + (h >> 1), 1, 1, '#2d2218');
  };
  const fita = (c, x0, x1, y, sag) => {   // fita zebrada de interdição
    for (let x = x0; x <= x1; x++) { const t = (x - x0) / (x1 - x0), yy = Math.round(y + sag * 4 * t * (1 - t)); const amarelo = Math.floor((x - x0) / 3) % 2 === 0; px(c, x, yy, 1, 3, amarelo ? '#e2b930' : '#2b2a2e'); }
  };

  // ---------------------------------------------------------------- RUA (mundo 1130×270)
  function rua(W, H) {
    const [cv, c] = mk(W, H);
    // — sobrado de Seu Raimundo (x 110–290): aviso, fita, X de tinta, janela tapada e rachadura
    tabua(c, 229, 60, 24, 7, 0); tabua(c, 228, 69, 25, 7, 1); tabua(c, 229, 78, 23, 7, 2); tabua(c, 228, 87, 25, 7, 0);
    px(c, 232, 59, 3, 36, 'rgba(70,48,28,.55)');
    [[255, 98], [256, 102], [255, 106], [257, 110], [258, 115], [257, 120], [259, 126], [260, 132], [262, 138], [261, 144], [262, 149]].forEach(([x, y]) => { px(c, x, y, 1, 3, '#6a5238'); });
    px(c, 256, 108, 1, 1, '#6a5238'); px(c, 260, 130, 2, 1, '#6a5238');
    px(c, 121, 168, 20, 24, 'rgba(40,24,10,.22)');                  // sombra
    px(c, 120, 166, 20, 24, '#f1ebdb'); px(c, 120, 166, 20, 1, '#fffdf4'); px(c, 120, 189, 20, 1, '#cfc7b3');
    txt(c, 'AVISO', 121, 168, '#a8322a');
    px(c, 122, 176, 16, 1, '#8d857a'); px(c, 122, 179, 12, 1, '#8d857a'); px(c, 122, 182, 16, 1, '#8d857a');
    px(c, 126, 185, 9, 3, '#b5392e'); px(c, 127, 186, 7, 1, '#f1ebdb');   // carimbo
    px(c, 119, 165, 2, 2, '#caa84a'); px(c, 139, 165, 2, 2, '#caa84a');   // fita crepe nos cantos
    fita(c, 146, 183, 170, 2); fita(c, 146, 183, 190, 2);
    // X laranja pintado a spray, com escorrido
    const X = '#d9531e'; for (let i = 0; i < 16; i++) { px(c, 196 + i, 150 + i, 2, 2, X); px(c, 211 - i, 150 + i, 2, 2, X); }
    [[199, 167, 4], [206, 166, 6], [209, 168, 3]].forEach(([x, y, h]) => px(c, x, y, 1, h, X));
    // — padaria (x 290–650): plaquinha em português e inglês ao lado do arco
    px(c, 413, 159, 27, 28, 'rgba(40,20,20,.25)'); px(c, 412, 157, 27, 28, '#e9e2cf'); px(c, 413, 158, 25, 26, '#2f5d8c');
    txt(c, 'BREAD', 416, 162, '#f3eee0'); px(c, 417, 169, 19, 1, '#d8b24a'); txt(c, 'PÃO', 420, 177, '#f3eee0');
    // — associação (x 650–810): faixa de pano esticada entre as janelas
    px(c, 663, 115, 144, 17, 'rgba(30,20,30,.20)');
    px(c, 662, 114, 144, 16, '#eee8d6'); px(c, 662, 114, 144, 1, '#fffdf2'); px(c, 662, 129, 144, 1, '#cbc3ae');
    for (let x = 662; x < 806; x += 24) px(c, x, 130, 12, 1, '#cbc3ae');
    txt(c, 'AQUI MORA GENTE', 662 + Math.floor((144 - largura('AQUI MORA GENTE', 2)) / 2), 118, '#8f1f22', 2);
    px(c, 664, 108, 1, 6, '#6b5a47'); px(c, 804, 108, 1, 6, '#6b5a47');
    // — casa verde (x 810–950): em obra. Porta e janela baixa tapadas, andaime inteiro, tela, placa
    for (let i = 0; i < 5; i++) tabua(c, 834 + i * 5, 158, 5, 49, i);
    px(c, 833, 172, 27, 3, '#4f3a24'); px(c, 833, 196, 27, 3, '#4f3a24');
    for (let i = 0; i < 4; i++) tabua(c, 897, 160 + i * 10, 29, 9, i + 1);
    c.fillStyle = 'rgba(46,76,64,.42)'; c.fillRect(816, 70, 128, 48);
    for (let x = 816; x < 944; x += 3) px(c, x, 70, 1, 48, 'rgba(30,48,42,.30)');
    const FE = '#8d939c', FE2 = '#b9bec6';
    [816, 878, 943].forEach(x => { px(c, x, 66, 2, 142, FE); px(c, x, 66, 1, 142, FE2); });
    [118, 164].forEach(y => { px(c, 816, y, 129, 1, FE2); px(c, 816, y + 1, 129, 2, '#9a7a4e'); px(c, 816, y + 3, 129, 1, '#5e452a'); px(c, 816, y - 8, 129, 1, FE); px(c, 816, y - 16, 129, 1, FE); });
    for (let i = 0; i <= 46; i++) { px(c, 816 + Math.round(i * 62 / 46), 164 - i, 1, 1, FE); px(c, 878 + Math.round(i * 65 / 46), 164 - i, 1, 1, FE); }
    px(c, 815, 206, 5, 2, '#6a5a48'); px(c, 876, 206, 5, 2, '#6a5a48'); px(c, 941, 206, 5, 2, '#6a5a48');
    px(c, 925, 125, 23, 24, 'rgba(30,20,20,.22)'); px(c, 924, 123, 23, 24, '#f2ecdc'); px(c, 924, 123, 23, 3, '#b5392e');
    txt(c, 'OBRA', 928, 129, '#a8322a'); txt(c, '1994', 928, 138, '#3d3a44');
    return cv;
  }

  // ---------------------------------------------------------------- PADARIA (interior 480×270), por cima da parede
  function padaria(c) {
    // plaqueta em inglês e português sob o quadro do fiado (quadro: x 205–231, y 55–84)
    px(c, 208, 88, 31, 23, '#e9e2cf'); px(c, 209, 89, 29, 21, '#2f5d8c');
    txt(c, 'BREAD', 214, 92, '#f3eee0'); px(c, 214, 98, 19, 1, '#d8b24a'); txt(c, 'PÃO', 218, 104, '#f3eee0');
    px(c, 206, 87, 2, 2, '#caa84a'); px(c, 239, 87, 2, 2, '#caa84a');
    // aviso do aluguel novo, colado por dentro da vidraça da janela (vidraça: x 238–273, y 61–101)
    px(c, 241, 86, 30, 15, '#f1ebdb'); px(c, 241, 86, 30, 1, '#fffdf4'); px(c, 241, 100, 30, 1, '#cfc7b3');
    txt(c, 'ALUGUEL', 242, 88, '#a8322a'); txt(c, 'NOVO', 242, 95, '#3d3a44'); px(c, 240, 85, 2, 2, '#caa84a'); px(c, 270, 85, 2, 2, '#caa84a');
  }

  // ---------------------------------------------------------------- CASA (interior 480×270; a câmera mostra x ≈ 45–410)
  function casa(c) {
    // aviso na parede, entre o lampião e a porta-janela
    px(c, 195, 59, 20, 22, 'rgba(40,24,10,.22)'); px(c, 194, 57, 20, 22, '#f1ebdb'); px(c, 194, 57, 20, 1, '#fffdf4'); px(c, 194, 78, 20, 1, '#cfc7b3');
    txt(c, 'AVISO', 195, 59, '#a8322a'); px(c, 196, 66, 16, 1, '#8d857a'); px(c, 196, 69, 11, 1, '#8d857a'); px(c, 198, 72, 9, 3, '#b5392e'); px(c, 199, 73, 7, 1, '#f1ebdb');
    px(c, 193, 56, 2, 2, '#caa84a'); px(c, 213, 56, 2, 2, '#caa84a');
    // caixas amarradas em cima do guarda-roupa (topo em y ≈ 77)
    const cx = (x, y, w, h, i) => { px(c, x, y, w, h, ['#b8925e', '#a98350'][i % 2]); px(c, x, y, w, 2, '#cfae7a'); px(c, x, y + h - 1, w, 1, '#7c5e3a'); px(c, x + (w >> 1), y, 1, h, '#e0cfa8'); px(c, x, y + (h >> 1), w, 1, '#e0cfa8'); };
    cx(349, 69, 16, 8, 0); cx(354, 61, 11, 8, 1);
  }
  // mala fechada com cordão sobre o pé da cama (colcha: x 379–407, y 141–170). A cama é uma entidade da cena, então a mala entra na lista de desenho depois dela.
  function mala(c) { px(c, 383, 150, 22, 11, '#5a3a2a'); px(c, 383, 150, 22, 2, '#7a5640'); px(c, 383, 160, 22, 1, '#3a2418'); px(c, 393, 150, 2, 11, '#c9ad72'); px(c, 389, 154, 10, 1, '#c9ad72'); }
  return { px, txt, largura, rua, padaria, casa, EXTRA: null, EXTRA_CASA: { y: 178, draw: mala } };
})();
