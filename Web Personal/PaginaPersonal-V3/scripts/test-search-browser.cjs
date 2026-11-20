/* Pruebas funcionales del buscador en Chrome real mediante Playwright.
   Ejecutar: node scripts/test-search-browser.cjs
   Dependencia de desarrollo: playwright (o UX_PLAYWRIGHT con su ruta).
   UX_CHROME permite seleccionar otro ejecutable de Chrome/Chromium.
   Solo sirve archivos locales en 127.0.0.1, no consulta la web publicada.
   Guarda resultados, versiones, hashes y capturas en docs/buscador-pruebas/. */
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const http = require('node:http');
const { pathToFileURL } = require('node:url');
const { createHash } = require('node:crypto');
const { chromium } = require(process.env.UX_PLAYWRIGHT || 'playwright');
const root = path.resolve(__dirname, '..');
const output = path.join(root, 'docs/buscador-pruebas');
const executablePath = process.env.UX_CHROME || (process.platform === 'win32'
  ? 'C:/Program Files/Google/Chrome/Application/chrome.exe' : undefined);
const mime = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.avif': 'image/avif' };

(async () => {
  await fs.mkdir(output, { recursive: true });
  // El puerto libre y el cierre en finally evitan interferir con otros servicios.
  const server = http.createServer(async (request, response) => {
    try {
      const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
      const target = path.resolve(root, '.' + (pathname.endsWith('/') ? pathname + 'index.html' : pathname));
      if (!target.startsWith(root + path.sep)) { response.writeHead(403).end(); return; }
      const data = await fs.readFile(target);
      response.writeHead(200, { 'Content-Type': mime[path.extname(target)] || 'application/octet-stream' }).end(data);
    } catch { response.writeHead(404).end(); }
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  let browser;
  const report = { date: new Date().toISOString(), node: process.version,
    platform: process.platform, playwright: require(path.join(path.dirname(require.resolve(process.env.UX_PLAYWRIGHT || 'playwright')), 'package.json')).version,
    method: 'Chrome headless real; sitio local; sin emulación de teléfono físico',
    viewport: { width: 1366, height: 900 }, tests: [], pageErrors: [], failedRequests: [], hashes: {} };
  async function check(id, name, run) {
    try {
      const observed = await run();
      report.tests.push({ id, name, passed: true, observed });
      console.log(`OK ${id}: ${name}`);
    } catch (error) {
      report.tests.push({ id, name, passed: false, error: String(error) });
      console.error(`ERROR ${id}: ${name}: ${error.message}`);
    }
  }
  try {
    browser = await chromium.launch({ executablePath, headless: true });
    report.browser = browser.version();
    const context = await browser.newContext({ viewport: report.viewport, locale: 'es-ES', colorScheme: 'light' });
    const requests = [];
    function observe(page) {
      page.on('pageerror', error => report.pageErrors.push(String(error)));
      page.on('requestfailed', request => report.failedRequests.push({ url: request.url(), error: request.failure()?.errorText }));
      page.on('request', request => requests.push(request.url()));
    }
    const page = await context.newPage(); observe(page);
    const query = page.locator('#query');
    const links = page.locator('#search-results h2 a');
    const status = page.locator('#search-status');
    const screenshot = name => page.screenshot({ path: path.join(output, name), fullPage: true });
    const waitStatus = text => page.waitForFunction(value => document.querySelector('#search-status').textContent === value, text);
    const go = suffix => page.goto(base + suffix, { waitUntil: 'networkidle' });

    await check('N01', 'Acceso desde las 18 cabeceras', async () => {
      const names = ['index', 'trayectoria', 'hobbies', 'intereses', 'contacto', 'ayuda', 'mapa', 'buscar', 'lectura'];
      for (const prefix of ['', '/en']) for (const name of names) {
        await go(`${prefix}/${name}.html`);
        assert.equal(await page.locator('.header-tools a[title]').first().getAttribute('href'), 'buscar.html');
      }
      await go('/index.html');
      await page.getByRole('link', { name: 'Buscar', exact: true }).click();
      await query.waitFor(); assert.equal(new URL(page.url()).pathname, '/buscar.html');
      return { cabeceras: 18, destino: '/buscar.html' };
    });
    await check('N02', 'Estado inicial sin consulta', async () => {
      await waitStatus('Escribe una palabra para buscar en el sitio.');
      assert.equal(await links.count(), 0);
      assert.equal(await page.locator('#search-empty').isVisible(), false);
      await screenshot('01-inicial.png');
      return { status: await status.textContent(), results: 0, screenshot: '01-inicial.png' };
    });
    await check('N03', 'Actualización al escribir sin peticiones de datos de búsqueda', async () => {
      // Espera también a las cargas tardías de la navegación anterior (favicon)
      // antes de medir las peticiones atribuibles a escribir una consulta.
      await page.waitForLoadState('networkidle');
      const before = requests.length;
      await query.fill('judo'); await waitStatus('3 resultados para «judo».');
      assert.equal(await links.count(), 3);
      assert.equal(new URL(page.url()).searchParams.get('q'), 'judo');
      report.requestsDuringSearch = requests.slice(before);
      // Chrome puede volver a solicitar el icono al cambiar q con replaceState.
      // Se registra esa carga local; cualquier otra petición hace fallar el caso.
      const searchRequests = report.requestsDuringSearch.filter(url => url !== base + '/img/favicon.svg');
      assert.deepEqual(searchRequests, []);
      const targets = await links.evaluateAll(nodes => nodes.map(node => node.getAttribute('href')));
      assert.deepEqual(targets.slice(0, 2), ['hobbies.html#practicar-judo', 'hobbies.html#ensenar-judo']);
      await screenshot('02-judo.png');
      return { status: await status.textContent(), targets, searchRequests: 0,
        incidentalRequests: report.requestsDuringSearch, screenshot: '02-judo.png' };
    });
    await check('N04', 'Envío con botón y canción del índice', async () => {
      await query.fill('sota el cel'); await page.getByRole('button', { name: 'Buscar', exact: true }).click();
      assert.equal(await links.first().getAttribute('href'), 'intereses.html#gavina');
      return { query: 'sota el cel', first: await links.first().getAttribute('href') };
    });
    await check('N05', 'Enter, mayúsculas y ausencia de tildes', async () => {
      await query.fill('INGENIERIA WEB'); await query.press('Enter');
      assert.equal(await links.first().getAttribute('href'), 'trayectoria.html#uniovi-title');
      assert.equal(await status.evaluate(node => node === document.activeElement), true);
      return { first: await links.first().getAttribute('href'), focusMovesToSummary: true };
    });
    await check('N06', 'Consulta sin coincidencias', async () => {
      await query.fill('zzzinexistentezzz'); await query.press('Enter');
      assert.equal(await links.count(), 0);
      assert.equal(await page.locator('#search-empty').isVisible(), true);
      assert.equal(await page.locator('#search-empty a').getAttribute('href'), 'mapa.html');
      await screenshot('03-sin-resultados.png');
      return { status: await status.textContent(), alternativesVisible: true, screenshot: '03-sin-resultados.png' };
    });
    await check('N07', 'Vaciar elimina resultados y q', async () => {
      await query.fill(''); await waitStatus('Escribe una palabra para buscar en el sitio.');
      assert.equal(await links.count(), 0);
      assert.equal(new URL(page.url()).searchParams.has('q'), false);
      return { results: 0, qRemoved: true };
    });
    await check('N08', 'Solo signos no muestra resultados arbitrarios', async () => {
      await query.fill('¿?!!!'); await query.press('Enter');
      assert.equal(await links.count(), 0);
      assert.equal(await status.textContent(), 'Escribe una palabra para buscar en el sitio.');
      return { query: '¿?!!!', results: 0 };
    });
    await check('N09', 'URL con q y recarga', async () => {
      await go('/buscar.html?q=Ingenieria+Web');
      assert.equal(await query.inputValue(), 'Ingenieria Web');
      const before = await links.evaluateAll(nodes => nodes.map(node => node.getAttribute('href')));
      await page.reload({ waitUntil: 'networkidle' });
      assert.deepEqual(await links.evaluateAll(nodes => nodes.map(node => node.getAttribute('href'))), before);
      return { query: await query.inputValue(), targetsBeforeAndAfter: before };
    });
    await check('N10', 'Resultado abre la sección concreta', async () => {
      await links.first().click(); await page.waitForURL('**/trayectoria.html#uniovi-title');
      assert.equal(await page.locator('#uniovi-title').count(), 1);
      return { destination: new URL(page.url()).pathname + new URL(page.url()).hash };
    });
    await check('N11', 'Índice inglés y navegación dentro de en/', async () => {
      await go('/en/buscar.html?q=teaching');
      assert.equal(await status.textContent(), '1 result for “teaching”.');
      assert.equal(await links.first().getAttribute('href'), 'hobbies.html#ensenar-judo');
      await screenshot('04-ingles.png');
      await links.first().click(); await page.waitForURL('**/en/hobbies.html#ensenar-judo');
      assert.equal(await page.locator('html').getAttribute('lang'), 'en');
      return { status: '1 result for “teaching”.', destination: '/en/hobbies.html#ensenar-judo', screenshot: '04-ingles.png' };
    });
    await check('N12', 'Cambio de idioma conserva la consulta en el buscador equivalente', async () => {
      await go('/buscar.html?q=judo'); await page.getByRole('link', { name: 'EN: English', exact: true }).click();
      await query.waitFor(); assert.equal(await query.inputValue(), 'judo');
      assert.equal(new URL(page.url()).pathname, '/en/buscar.html');
      assert.equal(new URL(page.url()).searchParams.get('q'), 'judo');
      assert.equal(await links.count(), 3);
      return { destination: '/en/buscar.html', queryPreserved: true };
    });
    await check('N13', 'Límite de 160 al teclear y al abrir una URL', async () => {
      await go('/buscar.html'); await query.pressSequentially('a'.repeat(180));
      assert.equal((await query.inputValue()).length, 160);
      await go('/buscar.html?q=' + encodeURIComponent('judo' + ' '.repeat(156) + 'zzzzz'));
      assert.equal((await query.inputValue()).length, 160);
      assert.equal(await links.count(), 3);
      return { typedLength: 160, urlLengthAfterTrim: 160, results: 3 };
    });
    await check('N14', 'Texto con sintaxis HTML se presenta sin ejecutarse', async () => {
      let dialogs = 0; const onDialog = dialog => { dialogs++; dialog.dismiss(); }; page.on('dialog', onDialog);
      const payload = '<img src=x onerror=alert(1)>';
      await query.fill(payload); await query.press('Enter');
      assert.equal(await links.count(), 0);
      assert.equal(await page.locator('#search-status img, #search-results img').count(), 0);
      assert.ok((await status.textContent()).includes(payload));
      assert.equal(dialogs, 0); page.off('dialog', onDialog);
      return { literalText: true, injectedElements: 0, dialogs };
    });
    await check('N15', 'Recorrido con teclado, foco y región de estado', async () => {
      await go('/buscar.html');
      for (let count = 0; count < 25 && !await query.evaluate(node => node === document.activeElement); count++) await page.keyboard.press('Tab');
      assert.equal(await query.evaluate(node => node === document.activeElement), true);
      const outline = await query.evaluate(node => getComputedStyle(node).outlineStyle);
      assert.notEqual(outline, 'none');
      await page.keyboard.type('judo'); await page.keyboard.press('Enter');
      assert.equal(await status.getAttribute('role'), 'status');
      assert.equal(await status.getAttribute('aria-live'), 'polite');
      assert.equal(await status.evaluate(node => node === document.activeElement), true);
      await page.keyboard.press('Tab');
      assert.equal(await links.first().evaluate(node => node === document.activeElement), true);
      await page.keyboard.press('Enter'); await page.waitForURL('**/hobbies.html#practicar-judo');
      return { inputReachedByTab: true, outline, statusRole: 'status', ariaLive: 'polite', firstResultOpenedByEnter: true };
    });
    await check('N16', 'Resultados en viewport estrecho de 320 x 568', async () => {
      await page.setViewportSize({ width: 320, height: 568 }); await go('/buscar.html?q=judo');
      const dimensions = await page.evaluate(() => ({ viewport: innerWidth, content: document.documentElement.scrollWidth }));
      assert.ok(dimensions.content <= dimensions.viewport);
      assert.equal(await links.count(), 3);
      await screenshot('05-movil.png');
      return { ...dimensions, results: 3, screenshot: '05-movil.png' };
    });
    await check('N17', 'Buscador con tema oscuro', async () => {
      await page.setViewportSize(report.viewport);
      await page.locator('.theme-toggle').click();
      assert.equal(await page.locator('html').getAttribute('data-theme'), 'dark');
      assert.equal(await links.count(), 3); await screenshot('06-oscuro.png');
      return { theme: 'dark', results: 3, screenshot: '06-oscuro.png' };
    });
    await check('N18', 'Sin JavaScript ofrece mapa y versión de lectura', async () => {
      const noJs = await browser.newContext({ javaScriptEnabled: false, viewport: report.viewport });
      try {
        const alternative = await noJs.newPage(); observe(alternative);
        await alternative.goto(base + '/buscar.html', { waitUntil: 'networkidle' });
        assert.equal(await alternative.locator('noscript .callout').isVisible(), true);
        assert.deepEqual(await alternative.locator('noscript a').evaluateAll(nodes => nodes.map(node => node.getAttribute('href'))), ['mapa.html', 'lectura.html']);
        await alternative.screenshot({ path: path.join(output, '07-sin-javascript.png'), fullPage: true });
        await alternative.locator('noscript a').first().click(); await alternative.waitForURL('**/mapa.html');
        return { alternativeLinks: ['mapa.html', 'lectura.html'], mapOpened: true, screenshot: '07-sin-javascript.png' };
      } finally { await noJs.close(); }
    });
    await check('N19', 'Apertura directa file:// en español', async () => {
      const fileUrl = pathToFileURL(path.join(root, 'buscar.html')).href;
      await page.goto(fileUrl + '?q=judo', { waitUntil: 'load' });
      assert.equal(await links.count(), 3);
      await query.fill('sota el cel'); await query.press('Enter');
      assert.equal(await links.first().getAttribute('href'), 'intereses.html#gavina');
      await screenshot('08-archivo-local.png');
      await links.first().click(); await page.waitForURL('**/intereses.html#gavina');
      return { initialResults: 3, newQueryWorks: true, protocol: new URL(page.url()).protocol, target: 'intereses.html#gavina', screenshot: '08-archivo-local.png' };
    });
    await check('N20', 'Apertura directa file:// en inglés', async () => {
      await page.goto(pathToFileURL(path.join(root, 'en/buscar.html')).href + '?q=teaching', { waitUntil: 'load' });
      assert.equal(await status.textContent(), '1 result for “teaching”.');
      await links.first().click(); await page.waitForURL('**/en/hobbies.html#ensenar-judo');
      return { protocol: 'file:', target: 'en/hobbies.html#ensenar-judo', results: 1 };
    });
    await check('N21', 'Sin errores JavaScript ni cargas fallidas', async () => {
      assert.deepEqual(report.pageErrors, []); assert.deepEqual(report.failedRequests, []);
      return { pageErrors: 0, failedRequests: 0 };
    });
    await context.close();
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
    // Identifica la copia local realmente probada sin depender del estado de Git.
    for (const file of ['buscar.html', 'en/buscar.html', 'css/styles.css', 'js/search-core.js', 'js/search-index.js', 'js/search.js', 'scripts/build.py', 'scripts/test-search.cjs', 'scripts/test-search-browser.cjs', 'scripts/check.py']) {
      report.hashes[file] = createHash('sha256').update(await fs.readFile(path.join(root, file))).digest('hex');
    }
    report.summary = { passed: report.tests.filter(test => test.passed).length, failed: report.tests.filter(test => !test.passed).length, total: report.tests.length };
    await fs.writeFile(path.join(output, 'resultado-navegador.json'), JSON.stringify(report, null, 2) + '\n');
  }
  console.log(`${report.summary.passed}/${report.summary.total} pruebas en navegador superadas.`);
  if (report.summary.failed) process.exitCode = 1;
})().catch(error => { console.error(error); process.exitCode = 1; });
