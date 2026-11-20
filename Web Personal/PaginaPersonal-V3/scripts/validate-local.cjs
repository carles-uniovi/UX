/* HTML con Nu Html Checker y CSS con css-tree. Todo se ejecuta localmente.
   UX_QA_ROOT: npm install --prefix <ruta> vnu-jar@26.11.19 css-tree@3.2.1
   UX_JAVA: Java 17+; los validadores no forman parte de la web publicada. */
const fs = require('node:fs/promises'), path = require('node:path'), os = require('node:os');
const { spawnSync } = require('node:child_process');
const { createHash } = require('node:crypto');
const root = path.resolve(__dirname, '..'), out = path.join(root, 'docs/auditoria-v3');
const qaRoot = process.env.UX_QA_ROOT || path.join(os.tmpdir(), 'ux-v3-qa-01a1f4');
const tree = require(require.resolve('css-tree', { paths: [qaRoot] }));
(async () => {
  await fs.mkdir(out, { recursive: true });
  const files = [];
  for (const directory of ['', 'en']) for (const name of await fs.readdir(path.join(root, directory))) {
    if (name.endsWith('.html')) files.push(path.join(root, directory, name));
  }
  const jar = path.join(qaRoot, 'node_modules/vnu-jar/build/dist/vnu.jar');
  const result = spawnSync(process.env.UX_JAVA || 'java', ['-jar', jar, '--format', 'json', ...files], { encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 });
  if (result.error) throw result.error;
  let messages;
  try { messages = JSON.parse(result.stderr.trim() || result.stdout.trim()).messages; }
  catch { throw new Error('Nu Checker no devolvió JSON: ' + result.stderr.slice(0, 1200)); }
  const hashes = Object.fromEntries(await Promise.all(files.map(async name => [path.relative(root, name).replaceAll('\\', '/'), createHash('sha256').update(await fs.readFile(name)).digest('hex')])));
  const html = { date: new Date().toISOString(), tool: 'Nu Html Checker 26.11.19 (local, Java)', pages: files.length,
    hashes, errors: messages.filter(m => m.type === 'error').length,
    warnings: messages.filter(m => m.subType === 'warning').length, messages };
  await fs.writeFile(path.join(out, 'html-local.json'), JSON.stringify(html, null, 2));
  console.log(`HTML: ${html.pages} páginas; ${html.errors} errores; ${html.warnings} advertencias.`);
  const css = await fs.readFile(path.join(root, 'css/styles.css'), 'utf8');
  const errors = [], unchecked = [];
  const ast = tree.parse(css, { positions: true, onParseError: error => errors.push({ type: 'parse', message: error.message, line: error.line }) });
  let declarations = 0;
  tree.walk(ast, { visit: 'Declaration', enter(node) {
    declarations++;
    if (node.property.startsWith('--')) return;
    const match = tree.lexer.matchProperty(node.property, node.value);
    if (match.error) {
      const item = { property: node.property, value: tree.generate(node.value), line: node.loc.start.line, message: match.error.message };
      if (item.value.includes('var(') || /Unknown property|not supported/i.test(item.message)) unchecked.push(item);
      else errors.push(item);
    }
  }});
  const cssResult = { date: html.date, tool: 'css-tree 3.2.1 (local)', sha256: createHash('sha256').update(css).digest('hex'),
    declarations, errors, unchecked, limitation: 'Las variables CSS y propiedades sin gramática en css-tree se analizan sintácticamente; su valor se comprueba además en el navegador. No equivale a una certificación W3C.' };
  await fs.writeFile(path.join(out, 'css-local.json'), JSON.stringify(cssResult, null, 2));
  console.log(`CSS: ${declarations} declaraciones; ${errors.length} errores; ${unchecked.length} valores fuera del comprobador gramatical.`);
  if (html.errors || errors.length || ![0,1].includes(result.status)) process.exitCode = 1;
})().catch(error => { console.error(error); process.exitCode = 1; });
