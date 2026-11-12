// ===== s14_rua_domino.js — partida de dominó (4 jogadores, duplas, 28 pedras) =====
// Lógica pura (sem tela). Regras PROPOSTA (variações locais devem ser revisadas por quem joga):
// · 6 pedras para cada um, 4 "dormem". Começa quem tem a carroça mais alta (ou a maior pedra).
// · Passa quando não tem pedra: bate na mesa. · Bate quem esvazia a mão: simples 1, carroça 2, lá e lô 3, cruzada 4 pontos para a dupla.
// · Trancado: ganha a dupla com menos pontos na mão (1 ponto); empate não pontua. · Partida até 6 pontos.
(function () {
  const pips = t => t[0] + t[1];
  Sim.Domino = class {
    constructor(rng, ordem, dupla, o) {
      this.rng = rng; this.ordem = ordem.slice(); this.dupla = dupla; this.meta = (o && o.meta) || 6;
      this.placar = [0, 0]; this.mao = 0; this.partidas = [0, 0]; this.log = [];
      this.novaMao(null);
    }
    novaMao(inicia) {
      const r = this.rng, all = []; for (let a = 0; a <= 6; a++) for (let b = a; b <= 6; b++) all.push([a, b]);
      for (let i = all.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [all[i], all[j]] = [all[j], all[i]]; }
      this.maos = {}; this.ordem.forEach((s, i) => { this.maos[s] = all.slice(i * 6, i * 6 + 6); }); this.dorme = all.slice(24);
      this.cadeia = []; this.pontas = null; this.passes = 0; this.estado = 'jogando'; this.vencedor = null; this.ultimo = null; this.mao++;
      // abertura
      let best = null, who = null;
      for (const s of this.ordem) for (const t of this.maos[s]) { const k = t[0] === t[1] ? 100 + t[0] : pips(t); if (best == null || k > best) { best = k; who = s; } }
      this.vez = inicia && this.ordem.includes(inicia) ? inicia : who; this.abre = this.vez; this.abertura = true;
      if (inicia) this.abertura = false, this.abertura = true;      // primeira jogada: qualquer pedra (a mais alta da mão do iniciador)
      this.log.push({ ev: 'mao', n: this.mao, abre: this.vez });
    }
    legais(s) {
      const m = this.maos[s]; if (this.abertura) {
        // quem abre joga a pedra mais alta (carroça de sena, etc.)
        let b = null; for (const t of m) { const k = t[0] === t[1] ? 100 + t[0] : pips(t); if (!b || k > b.k) b = { t, k }; }
        return [{ t: b.t, lado: 'L' }];
      }
      const out = [], [l, r] = this.pontas;
      for (const t of m) {
        if (t[0] === l || t[1] === l) out.push({ t, lado: 'L' });
        if ((t[0] === r || t[1] === r) && !(l === r && out.some(o => o.t === t))) out.push({ t, lado: 'R' });
        else if ((t[0] === r || t[1] === r) && l === r && !out.some(o => o.t === t)) out.push({ t, lado: 'R' });
      }
      return out;
    }
    tipoBatida(t) {
      if (!this.pontas) return 'simples';
      const [l, r] = this.pontas, fitL = t[0] === l || t[1] === l, fitR = t[0] === r || t[1] === r, dbl = t[0] === t[1];
      if (dbl && fitL && fitR && l === r) return 'cruzada';
      if (!dbl && fitL && fitR && ((t[0] === l && t[1] === r) || (t[1] === l && t[0] === r))) return 'laelo';
      if (dbl) return 'carroca';
      return 'simples';
    }
    jogar(s, t, lado) {
      if (s !== this.vez || this.estado !== 'jogando') return null;
      const L = this.legais(s).find(o => o.t === t && (lado == null || o.lado === lado)); if (!L) return null;
      lado = L.lado; const mao = this.maos[s], i = mao.indexOf(t); const ultima = mao.length === 1;
      const tipo = ultima ? this.tipoBatida(t) : null;
      mao.splice(i, 1);
      if (this.abertura) { this.cadeia.push({ t, dobra: t[0] === t[1] }); this.pontas = [t[0], t[1]]; this.abertura = false; }
      else {
        const [l, r] = this.pontas;
        if (lado === 'L') { const out = t[0] === l ? t[1] : t[0]; this.cadeia.unshift({ t, dobra: t[0] === t[1], flip: t[0] === l }); this.pontas[0] = out; }
        else { const out = t[0] === r ? t[1] : t[0]; this.cadeia.push({ t, dobra: t[0] === t[1], flip: t[1] === r }); this.pontas[1] = out; }
      }
      this.passes = 0; this.ultimo = { s, t, lado, jogada: true };
      const res = { ev: 'joga', s, t, lado, pontas: this.pontas.slice(), resta: mao.length };
      this.log.push(res);
      if (!mao.length) return this._bate(s, tipo, res);
      this._proxima(); return res;
    }
    passar(s) {
      if (s !== this.vez || this.estado !== 'jogando') return null;
      if (this.legais(s).length) return null;
      this.passes++; this.ultimo = { s, passou: true };
      const res = { ev: 'passa', s }; this.log.push(res);
      if (this.passes >= 4) return this._tranca(res);
      this._proxima(); return res;
    }
    _proxima() { const i = this.ordem.indexOf(this.vez); this.vez = this.ordem[(i + 1) % this.ordem.length]; }
    _bate(s, tipo, res) {
      const pts = { simples: 1, carroca: 2, laelo: 3, cruzada: 4 }[tipo], d = this.dupla[s];
      this.placar[d] += pts; this.estado = 'batida'; this.vencedor = s;
      const out = Object.assign(res, { bate: { s, tipo, pts, dupla: d } }); this.log.push({ ev: 'bate', s, tipo, pts, dupla: d });
      if (this.placar[d] >= this.meta) { this.partidas[d]++; out.partida = d; }
      return out;
    }
    _tranca(res) {
      const tot = [0, 0]; for (const s of this.ordem) for (const t of this.maos[s]) tot[this.dupla[s]] += pips(t);
      this.estado = 'trancado'; let d = tot[0] < tot[1] ? 0 : tot[1] < tot[0] ? 1 : null; if (d != null) this.placar[d] += 1;
      this.vencedor = null; const out = Object.assign(res, { tranca: { tot, dupla: d } }); this.log.push({ ev: 'tranca', tot, dupla: d });
      if (d != null && this.placar[d] >= this.meta) { this.partidas[d]++; out.partida = d; }
      return out;
    }
    fimDePartida() { return this.placar[0] >= this.meta || this.placar[1] >= this.meta; }
    proximaMao() {
      if (this.fimDePartida()) { this.placar = [0, 0]; }
      const inicia = this.estado === 'batida' ? this.vencedor : null;
      this.novaMao(inicia);
    }
    // escolha de pedra por personalidade (agro 0..1): agressivo joga dobradas e pedras altas; cauteloso guarda dobradas e mira nas pontas que tem
    escolher(s, agro, ruido) {
      const L = this.legais(s); if (!L.length) return null; if (L.length === 1) return L[0];
      const mao = this.maos[s], cont = {}; mao.forEach(t => { cont[t[0]] = (cont[t[0]] || 0) + 1; cont[t[1]] = (cont[t[1]] || 0) + 1; });
      let best = null;
      for (const o of L) {
        const t = o.t, out = this.abertura ? t[0] : (o.lado === 'L' ? (t[0] === this.pontas[0] ? t[1] : t[0]) : (t[0] === this.pontas[1] ? t[1] : t[0]));
        let k = pips(t) * (0.3 + agro) + (t[0] === t[1] ? (agro > 0.5 ? 3 : -0.5) : 0) + (cont[out] || 0) * (1.4 - agro) + (this.rng() - 0.5) * (ruido == null ? 2.2 : ruido);
        if (!best || k > best.k) best = { o, k };
      }
      return best.o;
    }
    resumo() { return { placar: this.placar.slice(), mao: this.mao, vez: this.vez, pontas: this.pontas ? this.pontas.slice() : null, cadeia: this.cadeia.length, estado: this.estado }; }
  };
})();
