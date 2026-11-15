/* Pruebas del motor real y su índice generado. Sin dependencias ni red. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const context = { window: {} };
vm.createContext(context);
for (const file of ['search-core.js', 'search-index.js']) {
  vm.runInContext(fs.readFileSync(path.join(root, 'js', file), 'utf8'), context);
}
const { search, normalise } = context.window.SiteSearch;
const { es, en } = context.window.SEARCH_INDEX;
let checks = 0;
function check(name, operation) { operation(); checks++; console.log('OK:', name); }
check('ignora tildes y mayúsculas', () => assert.equal(normalise('MÚSICA'), 'musica'));
check('búsqueda concreta de deporte', () => {
  const matches = search(es, 'judo');
  assert.equal(matches.filter(item => item.url.startsWith('hobbies.html#')).length, 2);
  assert.ok(matches.slice(0, 2).every(item => item.url.startsWith('hobbies.html#')));
});
check('título de una canción interna', () => assert.equal(search(es, 'sota el cel')[0].url, 'intereses.html#gavina'));
check('formación con y sin tildes', () => assert.equal(search(es, 'INGENIERIA WEB')[0].url, 'trayectoria.html#uniovi-title'));
check('varias palabras requieren coincidencia conjunta', () => assert.equal(search(es, 'robe matematicas').length, 0));
check('índice inglés', () => assert.equal(search(en, 'teaching')[0].url, 'hobbies.html#ensenar-judo'));
check('fragmentos parciales', () => assert.equal(search(es, 'petun')[0].url, 'intereses.html#las-petunias'));
check('correo con puntuación', () => assert.equal(search(es, 'carlesvallgar@gmail.com')[0].url, 'contacto.html#personal'));
check('consulta vacía y solo signos', () => {
  for (const value of ['', '   ', '¿?!!!']) assert.equal(search(es, value).length, 0);
});
check('sin coincidencias', () => assert.equal(search(es, 'zzzinexistentezzz').length, 0));
check('consulta parecida a código no ejecuta nada', () => {
  assert.equal(search(es, '<img src=x onerror=alert(1)>').length, 0);
  assert.equal(context.window.alert, undefined);
});
check('mayor relevancia del título', () => {
  const data = [
    { title: 'Otro', category: 'Prueba', text: 'judo', url: 'a' },
    { title: 'Judo', category: 'Prueba', text: 'Deporte', url: 'b' },
  ];
  assert.equal(search(data, 'judo')[0].url, 'b');
});
check('orden estable', () => assert.equal(JSON.stringify(search(es, 'musica')), JSON.stringify(search(es, 'musica'))));
check('consulta acotada a 160 caracteres', () => assert.equal(search(es, 'judo' + ' '.repeat(156) + 'zzzzz').length, search(es, 'judo').length));
check('toda entrada tiene destino y texto', () => {
  for (const language of [es, en]) for (const item of language) {
    assert.ok(/^[\w-]+\.html#[\w-]+$/.test(item.url));
    assert.ok(item.title && item.text && item.category);
  }
});
console.log(`${checks} pruebas superadas.`);
