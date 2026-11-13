// ===== objects.js — sistema de objetos reutilizável (A cidade que somos · Etapa 3) =====
// Catálogo (assets/objects/catalog.json) + cena (scene_padaria.json). Cada objeto: categoria, classe, dimensão, apoio (âncora), colisão, interação, camada.
// Camadas: wall (parede, antes de tudo) · floor (ordenado pelos pés) · on (apoiado em outro objeto) · front (sobreposto à frente de um móvel).
const ObjectSys = {
  cat: null, scene: null, imgs: {}, bySprite: {}, state: {}, handlers: {}, t: 0,
  init(cat, scene, imgs) {
    this.cat = cat; this.scene = scene; this.imgs = imgs;
    for (const a of cat.assets) this.bySprite[a.sprite] = a;
    for (const i of scene.interativos) if (i.states || i.tipo === 'alternar') this.state[i.id] = 0;
    this.solids = scene.colisao_arquitetura.concat(scene.instancias.filter(i => i.collide).map(i => i.collide));
  },
  on(ev, fn) { (this.handlers[ev] = this.handlers[ev] || []).push(fn); },
  emit(ev, d) { (this.handlers[ev] || []).forEach(f => f(d)); },
  visible(i) { return !i.visivel_se || (this.state[i.visivel_se[0]] || 0) === i.visivel_se[1]; },
  drawInst(ctx, i) {
    let key = i.sprite; if (i.frames > 1) key = i.asset + '#' + (Math.floor(this.t * (i.fps || 6)) % i.frames);
    const a = this.bySprite[key]; if (!a) return;
    const [x, y, w, h] = a.rect; ctx.drawImage(this.imgs['obj_' + a.categoria], x, y, w, h, i.sx, i.sy, w, h);
  },
  layer(name) { return this.scene.instancias.filter(i => i.layer === name && this.visible(i)); },
  // entidades ordenáveis por profundidade (pés): floor, on e front
  entities(ctx) {
    return this.scene.instancias.filter(i => i.layer !== 'wall' && this.visible(i)).map(i => ({ y: i.base, draw: () => this.drawInst(ctx, i) }));
  },
  drawWall(ctx) { for (const i of this.layer('wall')) this.drawInst(ctx, i); },
  hit(x, y) { for (const o of this.scene.interativos) { const [a, b, w, h] = o.rect; if (x >= a && x < a + w && y >= b && y < b + h) return o; } return null; },
  toggle(id) { const o = this.scene.interativos.find(i => i.id === id); const n = (o && o.states ? o.states.length : 2); this.state[id] = ((this.state[id] || 0) + 1) % n; this.emit('estado', { id, estado: this.state[id], nome: o && o.states ? o.states[this.state[id]] : this.state[id] }); return this.state[id]; },
  tick(dt) { this.t += dt; }
};
