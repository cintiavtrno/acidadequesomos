// ===== s96_elenco.js — elenco e marcações da rua de 1996 (dados; troca-se sem mexer no motor) =====
// Os moradores com nome falam (sim/s96_trama.js liga o id do ator a quem fala); os demais são figurantes e só têm a descrição.
// Coordenadas: x do mundo; sy = distância dos pés abaixo do encosto da parede (calçada 0–21, meio-fio 22–27, rua 28+). y real = yw(x) + sy.
// Sprites: <who>_side. Camadas: 'sorted' (profundidade por y), 'wall' (na parede, atrás do guarda-corpo, recortado em clip px acima da laje).
Sim96.Elenco = (function () {
  const A = [];
  const add = d => { A.push(d); return d; };
  const R = (a, b) => [a, b];

  // ---------------- palco (x 720–1124) ----------------
  // percussionistas: duas fileiras escalonadas; cada um alterna tocar parado e andar tocando até outra marca, em horários diferentes
  const marcas = [[790, 35], [838, 40], [888, 34], [940, 40], [990, 35], [1040, 40]];
  const desl = [-34, 30, -26, 36, -30, 26];
  marcas.forEach((m, i) => {
    const id = 'perc' + (i + 1), [x, sy] = m, x2 = x + desl[i];
    add({ id, who: id, nome: 'Percussionista', papel: 'percussionista do bloco', x, sy, face: 'down', anim: 'drum',
      obs: ['Surdo de couro pendurado no ombro. Toca olhando para o chão, no tempo do grupo.', 'Repique alto, baquetas finas. Troca de lugar com o vizinho a cada refrão.', 'Caixa pequena e camisa listrada. Sorri sozinho quando acerta a virada.',
        'Surdo grande, passo curto. Marca o tempo com a cabeça.', 'Tambor de mão, camisa vermelha. Cobre o espaço entre dois colegas.', 'Repique. Olha para o colega ao lado para entrar no tempo.'][i],
      plano: [{ fica: R(2 + i * 1.7, 5 + i * 1.7), anim: 'drum', face: 'down' }, { vai: [x2, sy], anim: 'drumwalk', fim: 'down', fimAnim: 'drum' }, { fica: R(6, 10), anim: 'drum', face: 'down' },
        { fica: R(1.5, 2.5), anim: 'idle', face: 'down' }, { vai: [x, sy], anim: 'drumwalk', fim: 'down', fimAnim: 'drum' }, { fica: R(7, 11), anim: 'drum', face: 'down' }] });
  });
  add({ id: 'cantor', who: 'cantor', nome: 'O cantor', papel: 'o cantor da gravação', x: 915, sy: 44, face: 'down', anim: 'sway',
    obs: 'Camiseta branca com um símbolo da paz no peito. Dança pouco e olha para as sacadas.',
    plano: [{ fica: R(5, 8), anim: 'sway', face: 'down' }, { fica: R(2.5, 4), anim: 'wave', face: 'down' }, { fica: R(3, 5), anim: 'pose', face: 'down' }, { vai: [868, 44], anim: 'walk', fim: 'down', fimAnim: 'sway' },
      { fica: R(5, 8), anim: 'sway', face: 'down' }, { fica: R(3, 4), anim: 'pose', face: 'down' }, { vai: [962, 44], anim: 'walk', fim: 'down', fimAnim: 'sway' }, { fica: R(5, 7), anim: 'sway', face: 'down' }, { vai: [915, 44], anim: 'walk', fim: 'down', fimAnim: 'sway' }] });

  // ---------------- equipe de filmagem ----------------
  add({ id: 'cam_op_a', who: 'cam2o', nome: 'Operador de câmera', papel: 'operador da câmera fixa', x: 684, sy: 40, face: 'right', anim: 'film',
    obs: 'Mão no tripé, olho no visor. Levanta a cabeça quando alguém grita corta.', plano: [{ fica: R(7, 12), anim: 'film', face: 'right' }, { fica: R(2, 3.5), anim: 'idle', face: 'right' }] });
  add({ id: 'cam_op_b', who: 'cam3o', nome: 'Operador de câmera', papel: 'operador da câmera fixa', x: 1162, sy: 40, face: 'left', anim: 'film',
    obs: 'Boné cinza e a lente do outro lado do palco. Confere o enquadramento a cada troca de tomada.', plano: [{ fica: R(6, 11), anim: 'film', face: 'left', ini: 3 }, { fica: R(2, 4), anim: 'idle', face: 'left' }] });
  add({ id: 'cam_ombro', who: 'cam1', nome: 'Câmera de ombro', papel: 'câmera de ombro', x: 790, sy: 31, face: 'down', anim: 'film',
    obs: 'Câmera no ombro, passos lentos junto ao meio-fio. Acompanha os tambores de perto.',
    plano: [{ fica: R(5, 8), anim: 'film', face: 'down' }, { vai: [1040, 31], anim: 'camwalk', fim: 'down', fimAnim: 'film' }, { fica: R(5, 8), anim: 'film', face: 'down' }, { vai: [790, 31], anim: 'camwalk', fim: 'down', fimAnim: 'film' }] });
  add({ id: 'assist_a', who: 'assist', nome: 'Assistente', papel: 'assistente de produção', x: 868, sy: 19, face: 'down', anim: 'note',
    obs: 'Prancheta e rádio. Anota o horário de cada tomada.',
    plano: [{ fica: R(6, 9), anim: 'note', face: 'down' }, { fica: R(3, 5), anim: 'radio', face: 'right' }, { vai: [778, 20], anim: 'walk', fim: 'right', fimAnim: 'radio' }, { fica: R(4, 6), anim: 'radio', face: 'right' }, { vai: [868, 19], anim: 'walk', fim: 'down', fimAnim: 'note' }] });
  add({ id: 'assist_b', who: 'assist2', nome: 'Assistente', papel: 'assistente de produção', x: 1068, sy: 20, face: 'left', anim: 'radio',
    obs: 'Fone de ouvido e rádio. Chama a equipe de som antes de cada tomada.',
    plano: [{ fica: R(5, 8), anim: 'radio', face: 'left' }, { fica: R(3, 5), anim: 'note', face: 'down' }, { vai: [1010, 20], anim: 'walk', fim: 'left', fimAnim: 'radio' }, { fica: R(4, 6), anim: 'radio', face: 'left' }, { vai: [1068, 20], anim: 'walk', fim: 'left', fimAnim: 'radio' }] });
  add({ id: 'carga', who: 'carga', nome: 'Carregador', papel: 'equipe de carga', x: 1262, sy: 24, face: 'left', anim: 'carry',
    obs: 'Carrega um case de equipamento do ponto de apoio até a base. Faz a viagem sem pressa, desviando dos cabos.',
    plano: [{ fica: R(4, 6), anim: 'carry', face: 'left' }, { vai: [900, 24], anim: 'carrywalk', fim: 'down', fimAnim: 'carry' }, { fica: R(5, 7), anim: 'carry', face: 'down' }, { vai: [1262, 24], anim: 'carrywalk', fim: 'right', fimAnim: 'carry' }] });
  add({ id: 'diretor', who: 'diretor', nome: 'Diretor', papel: 'diretor do clipe', x: 936, sy: 18, face: 'down', anim: 'watch',
    obs: 'Colete de bolsos e chapéu de pescador. Olha para a rua inteira antes de olhar para o monitor.',
    plano: [{ fica: R(7, 10), anim: 'watch', face: 'down' }, { fica: R(3, 4.5), anim: 'point', face: 'down' }, { vai: [884, 18], anim: 'walk', fim: 'down', fimAnim: 'watch' }, { fica: R(6, 9), anim: 'watch', face: 'down' }, { fica: R(3, 4), anim: 'point', face: 'down' },
      { vai: [972, 18], anim: 'walk', fim: 'down', fimAnim: 'watch' }, { fica: R(6, 9), anim: 'watch', face: 'down' }, { vai: [936, 18], anim: 'walk', fim: 'down', fimAnim: 'watch' }] });

  // ---------------- mesa de dominó (sentados nas cadeiras da cena) ----------------
  const dom = (id, who, nome, papel, x, sy, face, obs) => add({ id, who, nome, papel, x, sy, face, anim: 'sit', vies: 0.1, fixo: true, obs, plano: [{ fica: R(4, 8), anim: 'sit' }, { fica: R(1, 1.6), anim: 'play' }, { fica: R(3, 7), anim: 'think' }, { fica: R(1, 1.6), anim: 'play' }] });
  dom('dom_E', 'ze', 'Seu Zé', 'jogador de dominó', 252, 15, 'right', 'Chapéu de palha e camisa clara. Joga olhando a rua e conta as pedras de cabeça.');
  dom('dom_D', 'nonato', 'Nonato', 'jogador de dominó', 306, 15, 'left', 'Bate a pedra na mesa com força. Camisa amarela, a de sempre.');
  dom('dom_F', 'bela', 'Dona Bela', 'jogadora de dominó', 278, 8, 'down', 'Costureira. Pensa muito antes de jogar.');
  dom('dom_T', 'cicera', 'Dona Cícera', 'jogadora de dominó', 278, 22, 'up', 'Lava roupa para o bairro. Joga de costas para a rua.');

  // ---------------- moradores nos seus lugares ----------------
  add({ id: 'tonho', who: 'tonho', nome: 'Tonho', papel: 'vendedor de cocada', x: 344, sy: 8, face: 'down', anim: 'idle', obs: 'Vende cocada e queijadinha numa banca de tabuleiro, perto da padaria.',
    plano: [{ fica: R(5, 9), anim: 'idle', face: 'down' }, { fica: R(3, 5), anim: 'talk', faces: ['down', 'right'] }, { fica: R(2, 4), anim: 'wave', face: 'down' }] });
  add({ id: 'aurea', who: 'aurea', nome: 'Dona Áurea', papel: 'dona da padaria', x: 510, sy: 4, face: 'down', anim: 'idle', fixo: true, obs: 'Avental azul. Fica na porta da padaria e olha a rua.',
    plano: [{ fica: R(6, 10), anim: 'idle', face: 'down' }, { fica: R(3, 5), anim: 'talk', faces: ['down', 'left', 'right'] }, { fica: R(5, 8), anim: 'idle', face: 'right' }] });
  add({ id: 'dandara', who: 'dandara', nome: 'Dandara', papel: 'líder da associação', x: 772, sy: 8, face: 'up', anim: 'idle', obs: 'Lê o quadro de avisos da associação.',
    plano: [{ fica: R(5, 8), anim: 'idle', face: 'up' }, { fica: R(5, 8), anim: 'talk', face: 'right' }, { fica: R(3, 5), anim: 'idle', face: 'down' }] });
  add({ id: 'junior', who: 'junior', nome: 'Júnior', papel: 'menino da rua', x: 340, sy: 18, face: 'down', anim: 'idle', obs: 'Corre de uma ponta a outra da calçada. Quer ver a câmera de perto.',
    plano: [{ fica: R(1, 2), anim: 'idle', face: 'down' }, { vaiAle: { x: [330, 480], sy: [12, 21] }, anim: 'walk', fim: 'down' }, { fica: R(1, 3), anim: 'react', face: 'down' }, { vaiAle: { x: [330, 480], sy: [12, 21] }, anim: 'walk', fim: 'down' }] });

  // ---------------- público atrás das barreiras (calçada, x 722–1124) ----------------
  const pub = (id, who, nome, x, sy, faces, obs, extra) => add(Object.assign({ id, who, nome, papel: 'público', x, sy, face: 'down', anim: 'idle', obs,
    plano: [{ fica: R(4, 9), anim: 'idle', faces }, { fica: R(2, 4), anim: 'talk', faces }, { fica: R(2, 3.5), anim: 'react', face: 'down' }, { fica: R(4, 8), anim: 'idle', faces }, { fica: R(2, 3), anim: 'wave', face: 'down' }] }, extra || {}));
  pub('pub1', 'zefa', 'Dona Zefa', 738, 13, ['down', 'right'], 'De touca azul, atrás da barreira, olhando o palco.');
  pub('pub2', 'nena', 'Moradora', 758, 15, ['down', 'left'], 'Vestido branco. Conversa com quem está ao lado.');
  pub('pub3', 'rita', 'Moradora', 814, 16, ['down'], 'Cabelo branco e blusa lilás. Chegou cedo para pegar lugar.');
  pub('pub4', 'caio', 'Morador', 1008, 16, ['down', 'right'], 'Camisa branca, mãos no bolso, olhando o palco.');
  pub('pub5', 'davi', 'Morador', 1058, 14, ['down', 'left'], 'Camisa verde, alto. Enxerga por cima dos outros.');
  pub('pub6', 'bia', 'Moradora', 1092, 16, ['down', 'right'], 'Blusa rosa. Acompanha cada movimento do palco.');
  pub('pub7', 'zefa', 'Moradora', 1034, 12, ['down', 'left'], 'Aplaude antes da hora e ri de si mesma.', { who: 'nena' });
  pub('kid1', 'm1', 'Criança', 748, 14, ['down'], 'Criança que arrisca um passo além da barreira e volta correndo.', { plano: [{ fica: R(1, 3), anim: 'idle', face: 'down' }, { vaiAle: { x: [730, 790], sy: [10, 16] }, anim: 'walk', fim: 'down' }, { fica: R(1, 2.5), anim: 'react', face: 'down' }] });
  pub('kid2', 'm2', 'Criança', 1072, 15, ['down'], 'Criança que balança no pé da barreira.', { plano: [{ fica: R(1, 3), anim: 'idle', face: 'down' }, { vaiAle: { x: [1050, 1110], sy: [10, 16] }, anim: 'walk', fim: 'down' }, { fica: R(1, 2.5), anim: 'wave', face: 'down' }] });
  pub('kid3', 'm3', 'Criança', 1022, 17, ['down'], 'Criança nas pontas dos pés, tentando ver o monitor da produção.');
  pub('kid4', 'm4', 'Criança', 1000, 12, ['down'], 'Criança parada na calçada, de olho nos tambores.', { plano: [{ fica: R(3, 6), anim: 'idle', face: 'down' }, { fica: R(2, 3), anim: 'react', face: 'down' }] });
  // passantes em outros trechos da calçada (rua vive fora do palco)
  const pas = (id, who, nome, papel, x0, x1, obs) => add({ id, who, nome, papel, x: x0, sy: 14, face: 'right', anim: 'idle', obs,
    plano: [{ fica: R(2, 6), anim: 'idle', face: 'right' }, { vai: [x1, 15], anim: 'walk', fim: 'left', fimAnim: 'idle' }, { fica: R(3, 7), anim: 'talk', face: 'left' }, { vai: [x0, 14], anim: 'walk', fim: 'right', fimAnim: 'idle' }] });
  pas('pas1', 'm5', 'Criança', 'criança', 130, 322, 'Vai de uma ponta a outra da calçada.');
  pas('pas2', 'caio', 'Morador', 'morador', 1180, 1380, 'Anda pela calçada olhando a rua interditada.');
  pas('pas3', 'bia', 'Moradora', 'moradora', 600, 664, 'Passa perto da padaria olhando o equipamento.');
  pas('pas4', 'm6', 'Criança', 'criança', 1262, 1350, 'Brinca perto do vaso de latas.');

  // ---------------- sacadas e portas (moradores nos pontos altos e nos vãos) ----------------
  // sacada: y = base do prédio − 97 (laje); o corpo fica atrás do guarda-corpo (clip px acima da laje)
  const sac = (id, who, nome, pred, x, obs, face) => add({ id, who, nome, papel: 'morador na sacada', predio: pred, x, sy: 0, face: face || 'down', anim: 'idle', camada: 'wall', clip: 22, fixo: true, obs,
    plano: [{ fica: R(5, 10), anim: 'idle', face: face || 'down' }, { fica: R(2, 4), anim: 'talk', faces: ['down', 'left', 'right'] }, { fica: R(2, 3), anim: 'wave', face: 'down' }, { fica: R(5, 9), anim: 'idle', face: face || 'down' }] });
  sac('sac1', 'nena', 'Moradora', 'sobrado', 286, 'Debruçada na sacada do sobrado, olhando a gravação.');
  sac('sac2', 'rita', 'Moradora', 'padaria', 438, 'Da sacada da padaria vê o palco inteiro de cima.');
  sac('sac3', 'davi', 'Morador', 'padaria', 582, 'Apoiado no guarda-corpo, de frente para o palco.');
  sac('sac4', 'bia', 'Moradora', 'rosa', 1270, 'Sacada do casarão rosa. Acena para quem passa embaixo.');
  sac('sac5', 'zefa', 'Moradora', 'azul', 728, 'Na sacada em frente à câmera fixa. Ajeita a touca quando olha para a lente.');
  sac('sac6', 'caio', 'Morador', 'creme', 944, 'Do alto vê o grupo dos tambores inteiro.');
  add({ id: 'porta1', who: 'nena', nome: 'Moradora', papel: 'moradora na porta', x: 1370, sy: 5, face: 'down', anim: 'idle', fixo: true, obs: 'Na porta do sobrado lilás, olhando a rua.',
    plano: [{ fica: R(5, 9), anim: 'idle', face: 'down' }, { fica: R(2, 4), anim: 'talk', faces: ['down', 'left'] }, { fica: R(2, 3), anim: 'hang', face: 'up' }] });
  add({ id: 'porta2', who: 'rita', nome: 'Dona Rita', papel: 'moradora na porta', x: 1036, sy: 5, face: 'down', anim: 'idle', fixo: true, obs: 'Na porta do prédio de tijolo aparente, o único sem pintura nova nesse trecho.',
    plano: [{ fica: R(6, 10), anim: 'idle', face: 'down' }, { fica: R(2, 4), anim: 'talk', faces: ['down', 'right'] }] });

  // ---------------- objetos descritivos da parede (placas e letreiros) ----------------
  const objetos = [
    { id: 'placa_bread', nome: 'plaqueta bilíngue', rect: [604, 164, 26, 22], x: 617, sy: 16, desc: 'Plaqueta esmaltada ao lado do arco da padaria: BREAD e PAO, sem til. Em 1994 era uma plaquinha azul pendurada. Agora está presa no meio da parede.' },
    { id: 'letreiro_assoc', nome: 'letreiro da associação', rect: [760, 135, 72, 11], x: 796, sy: 15, desc: 'ASSOCIACAO, pintado de novo na fachada azul, na mesma altura dos outros letreiros da rua. A associação ainda funciona no mesmo sobrado.' },
    { id: 'placa_paz', nome: 'placa de rua em azulejo', rect: [696, 134, 38, 14], x: 714, sy: 15, desc: 'Placa de azulejo: R. DA PAZ. É a placa mais nova da rua.' },
    { id: 'porta_sobrado', nome: 'porta do sobrado', rect: [206, 172, 18, 40], x: 214, sy: 10, fala: 'raimundo', desc: 'A porta do sobrado está fechada. Pela fresta se ouve um rádio baixo.' },
    { id: 'letreiro_barbearia', nome: 'letreiro da barbearia', rect: [89, 128, 58, 11], x: 118, sy: 15, desc: 'BARBEARIA, pintado em letras claras sobre fundo verde. A porta está aberta e ninguém espera na calçada.' },
  ];
  return { atores: A, objetos };
})();
