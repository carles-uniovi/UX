/* Verifica las barreras de captura y la continuidad de consentimiento sin red. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../js/clarity-study.js'), 'utf8');
const key = 'ux-clarity-tanda2';
class Element {
  constructor(tag) { this.tagName = tag; this.children = []; this.events = {}; }
  append(...els) { this.children.push(...els); }
  setAttribute() {}
  addEventListener(name, fn) { this.events[name] = fn; }
  showModal() { this.open = true; }
  close() { this.open = false; }
  remove() { this.removed = true; }
  click() { if (!this.disabled) this.events.click?.(); }
}
function setup({ query = '', project = 'test123', stored, blocked = false, protocol = 'https:' } = {}) {
  const head = new Element('head'), body = new Element('body'), footer = new Element('footer');
  const data = new Map(stored ? [[key, JSON.stringify(stored)]] : []);
  const location = { href: `${protocol}//example.test/v2/index.html${query}`, protocol, reloads: 0,
    reload() { this.reloads++; } };
  const context = { window: { UX_CLARITY_PROJECT_ID: project }, URL, Date, location,
    history: { replaceState(_a, _b, url) { location.href = url; } },
    sessionStorage: { getItem: k => data.get(k), removeItem: k => data.delete(k),
      setItem(k, value) { if (blocked) throw Error('denied'); data.set(k, value); } },
    document: { documentElement: { lang: 'es' }, head, body,
      createElement: tag => new Element(tag), querySelector: () => footer } };
  vm.runInNewContext(source, context);
  return { ...context, data, head, body, footer,
    dialog: body.children[0], calls: () => Array.from(context.window.clarity?.q || [], args => Array.from(args)) };
}
assert.equal(setup().head.children.length, 0, 'Una visita normal no carga Clarity');
const s = setup({ query: '?prueba=U01' });
assert.equal(s.head.children.length, 0, 'No cargar antes de aceptar');
s.dialog.children[2].click();
assert.equal(s.head.children[0].src, 'https://www.clarity.ms/tag/test123');
assert.equal(s.calls()[0][1].analytics_Storage, 'granted');
assert.equal(s.calls()[0][1].ad_Storage, 'denied');
assert(s.calls().some(c => c[1] === 'participante' && c[2] === 'U01'));
assert(!s.location.href.includes('prueba='));
const state = JSON.parse(s.data.get(key));
assert.equal(setup({ stored: state }).head.children.length, 1, 'Continúa entre páginas');
const pilot = setup({ query: '?prueba=PILOTO-PC' }); pilot.dialog.children[2].click();
assert(pilot.calls().some(c => c[1] === 'fase' && c[2] === 'piloto'));
const rejected = setup({ query: '?prueba=U02' }); rejected.dialog.children[3].click();
assert.equal(rejected.head.children.length, 0);
const missing = setup({ query: '?prueba=U01', project: '' });
assert(missing.dialog.children[2].disabled);
assert.equal(missing.head.children.length, 0);
const blocked = setup({ query: '?prueba=U01', blocked: true }); blocked.dialog.children[2].click();
assert.equal(blocked.head.children.length, 0, 'Sin almacenamiento no iniciar');
assert.equal(setup({ query: '?prueba=INVALID' }).head.children.length, 0);
assert.equal(setup({ query: '?prueba=U01', protocol: 'file:' }).head.children.length, 0);
assert.equal(setup({ stored: { ...state, started: Date.now() - 3600001 } }).head.children.length, 0);
assert.equal(setup({ stored: { ...state, project: 'other' } }).head.children.length, 0);
s.head.children[0].onerror();
assert.match(s.footer.children[0].children[0].textContent, /No iniciar/);
s.footer.children[0].children[1].click();
assert.equal(s.data.has(key), false);
assert.equal(s.location.reloads, 1);
assert(s.calls().some(c => c[0] === 'consent' && c[1] === false));
assert.equal(setup().head.children.length, 0, 'Tras finalizar, no reiniciar en la portada');
console.log('Clarity: consentimiento, exclusión de visitas normales, continuidad, etiquetas y finalización correctos.');
