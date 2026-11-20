/* Pruebas de las interacciones reales con un DOM mínimo simulado.
   No acreditan el diseño calculado ni el comportamiento nativo de un navegador. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../js/site.js'), 'utf8');

class Element extends EventTarget {
  constructor() {
    super(); this.attributes = {}; this.dataset = {}; this.children = []; this.textContent = '';
    const values = new Set();
    this.classList = { add: x => values.add(x), remove: x => values.delete(x), contains: x => values.has(x) };
  }
  setAttribute(key, value) { this.attributes[key] = String(value); }
  getAttribute(key) { return this.attributes[key] ?? null; }
  removeAttribute(key) { delete this.attributes[key]; if (key === 'src') this.src = ''; }
  contains(target) { return this === target || this.children.some(child => child.contains(target)); }
  replaceChildren(...children) { this.children = children; }
  querySelector(key) { return this.selectors?.[key] || null; }
  focus() { this.focused = true; }
  pause() { this.paused = true; }
  load() { this.released = true; }
  showModal() { this.open = true; }
  close() { this.open = false; this.dispatchEvent(new Event('close')); }
  getBoundingClientRect() { return { left: 100, right: 500, top: 100, bottom: 400 }; }
}
function fire(target, type, fields = {}) {
  const event = new Event(type, { cancelable: true });
  Object.assign(event, fields);
  target.dispatchEvent(event);
  return event;
}
function setup({ supported = true } = {}) {
  const menu = new Element(), navigation = new Element(), firstLink = new Element();
  navigation.children.push(firstLink); navigation.selectors = { a: firstLink };
  const dialog = new Element(), stage = new Element(), title = new Element();
  const status = new Element(), direct = new Element(), close = new Element();
  dialog.selectors = { '#media-stage': stage, '#media-title': title, '#media-status': status, '#media-direct': direct, '.dialog-close': close };
  if (!supported) dialog.showModal = undefined;
  const audio = new Element(), video = new Element();
  audio.dataset = { mediaType: 'audio', mediaTitle: 'Robe · Del Tiempo Perdido' };
  video.dataset = { mediaType: 'youtube', youtubeId: 'g4Hbz2jLxvQ', mediaTitle: 'Spider-Man · Tráiler oficial' };
  audio.href = 'file:///audio.mp3'; video.href = 'https://www.youtube.com/watch?v=g4Hbz2jLxvQ';
  const document = new Element();
  document.documentElement = { lang: 'es' }; document.body = new Element();
  document.selectors = { '.menu-toggle': menu, '#navigation': navigation, '#media-player': dialog };
  document.querySelectorAll = key => key === '.media-trigger' ? [audio, video] : [];
  document.createElement = type => { const node = new Element(); node.tagName = type; return node; };
  const mobile = new Element(); mobile.matches = true;
  vm.runInNewContext(source, { document, matchMedia: () => mobile, navigator: {} });
  return { document, menu, navigation, firstLink, dialog, stage, title, status, direct, close, audio, video, mobile };
}
let checks = 0;
function check(name, operation) { operation(); checks++; console.log('OK:', name); }
check('menú móvil cerrado inicialmente; abrir desplaza el foco a los enlaces', () => {
  const ui = setup();
  assert.equal(ui.menu.getAttribute('aria-expanded'), 'false');
  fire(ui.menu, 'click');
  assert.equal(ui.menu.getAttribute('aria-expanded'), 'true');
  assert.equal(ui.firstLink.focused, true);
});
check('Escape cierra el menú y devuelve el foco al botón', () => {
  const ui = setup(); fire(ui.menu, 'click'); fire(ui.document, 'keydown', { key: 'Escape' });
  assert.equal(ui.menu.getAttribute('aria-expanded'), 'false');
  assert.equal(ui.menu.focused, true);
});
check('escritorio vuelve a mostrar toda la navegación', () => {
  const ui = setup(); ui.mobile.matches = false; fire(ui.mobile, 'change');
  assert.equal(ui.navigation.dataset.collapsed, 'false');
});
check('audio abre el diálogo sin iniciar reproducción', () => {
  const ui = setup(); const click = fire(ui.audio, 'click', { button: 0 });
  assert.equal(click.defaultPrevented, true);
  assert.equal(ui.dialog.open, true);
  assert.equal(ui.stage.children[0].tagName, 'audio');
  assert.equal(ui.stage.children[0].controls, true);
  assert.equal(ui.stage.children[0].preload, 'none');
  assert.equal(ui.stage.children[0].autoplay, undefined);
  assert.equal(ui.title.textContent, 'Robe · Del Tiempo Perdido');
  assert.equal(ui.close.focused, true);
});
check('cerrar pausa, libera el recurso, limpia la ventana y restaura el foco', () => {
  const ui = setup(); fire(ui.audio, 'click', { button: 0 }); const player = ui.stage.children[0];
  fire(ui.close, 'click');
  assert.equal(ui.dialog.open, false);
  assert.equal(player.paused, true); assert.equal(player.released, true); assert.equal(player.src, '');
  assert.equal(ui.stage.children.length, 0); assert.equal(ui.audio.focused, true);
  assert.equal(ui.document.body.classList.contains('media-open'), false);
});
check('cerrar de forma nativa, como Escape, ejecuta la misma limpieza', () => {
  const ui = setup(); fire(ui.audio, 'click', { button: 0 }); const player = ui.stage.children[0];
  ui.dialog.close();
  assert.equal(player.paused, true); assert.equal(ui.audio.focused, true);
});
check('se puede volver a abrir con otro medio sin conservar el anterior', () => {
  const ui = setup(); fire(ui.audio, 'click', { button: 0 }); ui.dialog.close();
  fire(ui.video, 'click', { button: 0 });
  assert.equal(ui.stage.children.length, 1);
  assert.equal(ui.stage.children[0].tagName, 'iframe');
  assert.equal(ui.stage.children[0].title, 'Spider-Man · Tráiler oficial');
  assert.equal(ui.direct.hidden, false);
  assert.equal(ui.direct.href, ui.video.href);
});
check('YouTube conserva controles, teclado, subtítulos y pantalla completa sin autoplay', () => {
  const ui = setup(); fire(ui.video, 'click', { button: 0 });
  const iframe = ui.stage.children[0]; const url = new URL(iframe.src);
  assert.equal(url.origin, 'https://www.youtube-nocookie.com');
  assert.equal(url.pathname, '/embed/g4Hbz2jLxvQ');
  for (const [key, value] of Object.entries({ controls: '1', disablekb: '0', autoplay: '0', cc_load_policy: '1', hl: 'es' })) assert.equal(url.searchParams.get(key), value);
  assert.equal(iframe.allowFullscreen, true);
  assert.equal(iframe.referrerPolicy, 'strict-origin-when-cross-origin');
});
check('cerrar descarga YouTube y devuelve el foco a su enlace', () => {
  const ui = setup(); fire(ui.video, 'click', { button: 0 }); const iframe = ui.stage.children[0];
  ui.dialog.close();
  assert.equal(iframe.src, 'about:blank');
  assert.equal(ui.stage.children.length, 0);
  assert.equal(ui.video.focused, true);
});
check('un identificador de YouTube inválido no se incrusta', () => {
  const ui = setup(); ui.video.dataset.youtubeId = '../invalid';
  assert.equal(fire(ui.video, 'click', { button: 0 }).defaultPrevented, false);
  assert.equal(ui.stage.children.length, 0);
});
check('un error ofrece el archivo original y los errores antiguos se ignoran', () => {
  const ui = setup(); fire(ui.audio, 'click', { button: 0 }); const previous = ui.stage.children[0];
  fire(previous, 'error'); assert.equal(ui.direct.hidden, false); assert.equal(ui.direct.href, ui.audio.href);
  ui.dialog.close(); fire(previous, 'error'); assert.equal(ui.status.textContent, '');
});
check('sin soporte de dialog se conserva la navegación al archivo', () => {
  const ui = setup({ supported: false });
  assert.equal(fire(ui.audio, 'click', { button: 0 }).defaultPrevented, false);
});
check('Ctrl + clic conserva la apertura nativa del enlace', () => {
  const ui = setup();
  assert.equal(fire(ui.audio, 'click', { button: 0, ctrlKey: true }).defaultPrevented, false);
  assert.equal(ui.dialog.open, undefined);
});
console.log(`${checks} pruebas de interacción simulada superadas.`);
