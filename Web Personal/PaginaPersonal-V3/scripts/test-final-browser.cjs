/* Verificación técnica de V3 en Chrome real. No simula usuarios ni sus opiniones.
   Requiere UX_PLAYWRIGHT y axe-core en UX_QA_ROOT (dependencias solo de desarrollo).
   Sirve V3 en un subdirectorio; no envía tráfico a Clarity ni a YouTube. */
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const http = require('node:http');
const os = require('node:os');
const { chromium } = require(process.env.UX_PLAYWRIGHT || 'playwright');
const root = path.resolve(__dirname, '..');
const output = path.join(root, 'docs/auditoria-v3');
const qaRoot = process.env.UX_QA_ROOT || path.join(os.tmpdir(), 'ux-v3-qa-01a1f4');
const axePath = require.resolve('axe-core/axe.min.js', { paths: [qaRoot] });
const names = ['index', 'trayectoria', 'hobbies', 'intereses', 'contacto', 'ayuda', 'mapa', 'buscar', 'lectura'];
const pages = names.flatMap(n => [n + '.html', 'en/' + n + '.html']);
const mime = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.avif': 'image/avif' };
(async () => {
  await fs.mkdir(output, { recursive: true });
  const report = { date: new Date().toISOString(), tests: [], layouts: [], axe: [], pageErrors: [], remoteRequests: [],
    method: 'Chrome real headless; dispositivos simulados y zoom de texto/reflujo; sin nueva tanda humana.' };
  const server = http.createServer(async (request, response) => {
    try {
      const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
      if (!pathname.startsWith('/v3/')) return response.writeHead(404).end();
      const target = path.resolve(root, '.' + pathname.slice(3) + (pathname.endsWith('/') ? 'index.html' : ''));
      if (!target.startsWith(root + path.sep)) return response.writeHead(403).end();
      const data = await fs.readFile(target);
      response.writeHead(200, { 'Content-Type': mime[path.extname(target)] || 'application/octet-stream' }).end(data);
    } catch { response.writeHead(404).end(); }
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = 'http://127.0.0.1:' + server.address().port + '/v3/';
  let browser;
  async function check(name, run) {
    try { const observed = await run(); report.tests.push({ name, passed: true, observed }); console.log('OK:', name); }
    catch (error) { report.tests.push({ name, passed: false, error: String(error) }); console.error('ERROR:', name, error.message); }
  }
  try {
    browser = await chromium.launch({ executablePath: process.env.UX_CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true });
    report.browser = browser.version();
    const context = await browser.newContext({ viewport: { width: 1366, height: 900 }, locale: 'es-ES' });
    await context.route('https://www.youtube-nocookie.com/**', route => route.fulfill({ contentType: 'text/html', body: '<!doctype html><title>YouTube test double</title><button>Play</button>' }));
    const page = await context.newPage();
    page.on('pageerror', error => report.pageErrors.push(String(error)));
    page.on('request', request => { if (!request.url().startsWith('http://127.0.0.1:')) report.remoteRequests.push(request.url()); });
    const go = name => page.goto(base + name, { waitUntil: 'load' });
    const snapshot = name => page.screenshot({ path: path.join(output, name), fullPage: true });
    await check('Buscar y Menú con texto visible y controles de 44 px', async () => {
      await page.setViewportSize({ width: 320, height: 568 }); await go('index.html');
      for (const selector of ['.header-tools a[title="Buscar"]', '.menu-toggle', '.language-switch', '.theme-toggle']) {
        const box = await page.locator(selector).boundingBox(); assert(box && box.height >= 44 && box.width >= 44);
      }
      assert.equal(await page.locator('.menu-toggle span').innerText(), 'Menú');
      assert.equal(await page.locator('.header-tools a[title="Buscar"] span').innerText(), 'Buscar');
      await page.getByRole('button', { name: 'Menú', exact: true }).click();
      assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'), 'true');
      assert(await page.locator('.primary-nav a').first().evaluate(n => document.activeElement === n));
      await snapshot('01-menu-movil.png');
      await page.keyboard.press('Escape');
      assert(await page.locator('.menu-toggle').evaluate(n => document.activeElement === n));
      return { width: 320, touchTargets: 4, escapeReturnsFocus: true };
    });
    await check('Limpiar elimina consulta y URL y devuelve foco al campo', async () => {
      await go('buscar.html?q=judo');
      await page.getByRole('button', { name: 'Limpiar', exact: true }).click();
      assert.equal(await page.locator('#query').inputValue(), '');
      assert(!new URL(page.url()).searchParams.has('q'));
      assert.equal(await page.locator('#search-results li').count(), 0);
      assert(await page.locator('#query').evaluate(n => document.activeElement === n));
      assert(!await page.locator('.search-clear').isVisible());
      return { empty: true, qRemoved: true, focus: 'query' };
    });
    await check('Ejemplos permiten recuperar una búsqueda sin resultados', async () => {
      await go('buscar.html?q=zzzinexistentezzz');
      assert(await page.locator('#search-empty').isVisible());
      await page.locator('.search-examples').getByRole('link', { name: 'Judo', exact: true }).click();
      await page.waitForURL('**/buscar.html?q=judo');
      await page.waitForFunction(() => document.querySelectorAll('#search-results li').length === 3);
      assert.equal(await page.locator('#search-results li').count(), 3);
      return { recoveredWith: 'judo', results: 3 };
    });
    await check('Las tres tareas mantienen sus destinos de V2', async () => {
      for (const [query, destination] of [['judo', 'hobbies.html#practicar-judo'], ['SOTA EL CEL', 'intereses.html#gavina'], ['UO319242@uniovi.es', 'contacto.html#universidad']]) {
        await go('buscar.html?q=' + encodeURIComponent(query));
        assert.equal(await page.locator('#search-results h2 a').first().getAttribute('href'), destination);
      }
      return { queries: 3, destinationsPreserved: true };
    });
    await check('La cabecera no oculta el destino de los resultados', async () => {
      await page.setViewportSize({ width: 390, height: 844 }); await go('buscar.html?q=judo');
      await page.locator('#search-results h2 a').first().click();
      await page.waitForURL('**/hobbies.html#practicar-judo');
      await page.locator('#practicar-judo').waitFor();
      const geometry = await page.evaluate(() => ({ header: document.querySelector('.site-header').getBoundingClientRect().bottom,
        heading: document.querySelector(location.hash).getBoundingClientRect().top, offset: getComputedStyle(document.documentElement).getPropertyValue('--header-height') }));
      assert(geometry.heading >= geometry.header - 1, JSON.stringify(geometry));
      return geometry;
    });
    await check('Copia de correo con confirmación local junto al botón', async () => {
      await go('contacto.html');
      await page.evaluate(() => Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText: async value => { window.__copied = value; } } }));
      const button = page.locator('.copy-email[data-email="UO319242@uniovi.es"]');
      await button.click();
      await page.waitForFunction(() => document.querySelector('#copy-status-universidad').textContent.includes('Dirección copiada:'));
      assert.equal(await page.evaluate(() => window.__copied), 'UO319242@uniovi.es');
      assert.equal(await button.textContent(), 'Copiado');
      const status = await page.locator('#copy-status-universidad').boundingBox();
      const btn = await button.boundingBox(); assert(status.y >= btn.y && status.y - btn.y < 100);
      await snapshot('02-contacto-copiado.png');
      return { copied: 'UO319242@uniovi.es', localFeedback: true, api: 'double controlado' };
    });
    await check('Copia bloqueada conserva la dirección y ofrece selección manual', async () => {
      await go('contacto.html');
      await page.evaluate(() => Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText: async () => { throw new Error('NotAllowedError'); } } }));
      await page.getByRole('button', { name: 'Copiar correo personal', exact: true }).click();
      await page.waitForFunction(() => document.querySelector('#copy-status-personal').textContent.includes('no está disponible'));
      assert.equal(await page.evaluate(() => getSelection().toString()), 'carlesvallgar@gmail.com');
      assert(!await page.getByRole('button', { name: 'Copiar correo personal', exact: true }).isDisabled());
      return { fallbackSelection: true, api: 'rechazo simulado' };
    });
    await check('Tema oscuro: etiqueta de acción actualizada y almacenamiento propio de V3', async () => {
      await go('buscar.html?q=musica'); await page.locator('.theme-toggle').click();
      assert.equal(await page.locator('html').getAttribute('data-theme'), 'dark');
      assert.equal(await page.locator('.theme-toggle').getAttribute('aria-label'), 'Activar modo claro');
      assert.equal(await page.evaluate(() => localStorage.getItem('adweb-v3-theme')), 'dark');
      assert.equal(await page.evaluate(() => localStorage.getItem('adweb-theme')), null);
      await snapshot('03-busqueda-oscura.png');
      await page.locator('.theme-toggle').click();
      return { currentAction: 'Activar modo claro', independentPreference: true };
    });
    await check('Salto al contenido y navegación de teclado sin foco oculto', async () => {
      await page.setViewportSize({ width: 1366, height: 900 }); await go('contacto.html');
      await page.keyboard.press('Tab'); assert(await page.locator('.skip-link').evaluate(n => document.activeElement === n));
      await page.keyboard.press('Enter'); assert.equal(await page.evaluate(() => document.activeElement.id), 'contenido');
      const hidden = [];
      for (let i = 0; i < 24; i++) {
        await page.keyboard.press('Tab');
        const result = await page.evaluate(() => {
          const n = document.activeElement, header = document.querySelector('.site-header'), r = n.getBoundingClientRect();
          return { name: n.textContent.slice(0, 60), obscured: n !== document.body && !n.matches('.skip-link') && !header.contains(n) &&
            r.bottom > 0 && r.top < header.getBoundingClientRect().bottom - 1 };
        });
        if (result.obscured) hidden.push(result);
      }
      assert.deepEqual(hidden, []);
      return { tabStops: 24, obscuredFocus: 0 };
    });
    await check('Diálogo multimedia: sin autoplay, Escape libera el medio y restaura foco', async () => {
      await go('intereses.html');
      const trigger = page.locator('[data-media-type="audio"]').first(); await trigger.click();
      assert(await page.locator('#media-player').evaluate(n => n.open));
      assert.equal(await page.locator('audio').getAttribute('preload'), 'none');
      assert.equal(await page.locator('audio').getAttribute('autoplay'), null);
      await page.keyboard.press('Escape');
      await page.waitForFunction(() => !document.querySelector('#media-player').open && !document.querySelector('#media-stage').children.length);
      assert.equal(await page.locator('audio').count(), 0);
      assert(await trigger.evaluate(n => document.activeElement === n));
      return { audioNotAutoplaying: true, focusRestored: true };
    });
    await check('No carga Clarity en V3, tampoco con enlaces antiguos del estudio', async () => {
      await go('index.html?prueba=U01');
      assert.equal(await page.locator('[src*="clarity"]').count(), 0);
      assert.equal(await page.locator('#ux-study-dialog, .ux-study-controls').count(), 0);
      assert(!report.remoteRequests.some(url => url.includes('clarity.ms')));
      return { studyRequests: 0 };
    });
    await check('Reflujo de las 18 páginas en ocho tamaños de pantalla', async () => {
      const sizes = [[320,568],[375,667],[390,844],[768,1024],[1024,768],[1366,768],[1920,1080],[844,390]];
      for (const [width, height] of sizes) {
        await page.setViewportSize({ width, height });
        for (const name of pages) {
          await go(name);
          const metrics = await page.evaluate(() => ({ width: innerWidth, content: document.documentElement.scrollWidth }));
          report.layouts.push({ page: name, width, height, ...metrics });
          assert(metrics.content <= width + 1, name + ' ' + JSON.stringify(metrics));
        }
      }
      return { combinations: report.layouts.length, horizontalOverflow: 0 };
    });
    await check('Reflujo equivalente a 400% y texto ampliado al 200%', async () => {
      await page.setViewportSize({ width: 320, height: 256 }); await go('contacto.html');
      assert.equal(await page.locator('.site-header').evaluate(n => getComputedStyle(n).position), 'relative');
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
      await page.setViewportSize({ width: 390, height: 844 }); await go('index.html');
      await page.addStyleTag({ content: 'html { font-size: 200%; }' });
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
      await snapshot('04-texto-200.png');
      return { reflow: '320x256 equivale a 1280px al 400%, no zoom nativo', textZoom: '200%' };
    });
    await check('Auditoría axe de las 18 páginas en ambos temas', async () => {
      await page.setViewportSize({ width: 1366, height: 900 });
      for (const theme of ['light', 'dark']) for (const name of pages) {
        await go(name);
        await page.evaluate(value => { document.documentElement.dataset.theme = value; }, theme);
        await page.addScriptTag({ path: axePath });
        const result = await page.evaluate(async () => {
          const r = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a','wcag2aa','wcag2aaa','wcag21a','wcag21aa','wcag22aa','best-practice'] } });
          return { version: r.testEngine.version, violations: r.violations, incomplete: r.incomplete.map(i => ({ id: i.id, nodes: i.nodes.map(n => ({ target: n.target, failureSummary: n.failureSummary })) })) };
        });
        report.axe.push({ page: name, theme, ...result });
      }
      const violations = report.axe.flatMap(r => r.violations.map(v => ({ page: r.page, theme: r.theme, id: v.id, nodes: v.nodes.map(n => n.target) })));
      assert.deepEqual(violations, []);
      return { axe: report.axe[0].version, scans: report.axe.length, violations: 0, incomplete: report.axe.reduce((n, r) => n + r.incomplete.length, 0) };
    });
    await check('Escritorio final y cero errores de JavaScript', async () => {
      await page.setViewportSize({ width: 1366, height: 900 }); await go('index.html'); await snapshot('05-portada-escritorio.png');
      assert.deepEqual(report.pageErrors, []);
      return { pageErrors: 0, screenshot: '05-portada-escritorio.png' };
    });
    await context.close();
    await check('Si falla site.js, se recupera la navegación móvil', async () => {
      const partial = await browser.newContext({ viewport: { width: 320, height: 568 } });
      await partial.route('**/js/site.js', route => route.abort());
      const p = await partial.newPage();
      try {
        await p.goto(base + 'index.html');
        assert(await p.locator('.primary-nav').isVisible());
        await p.locator('.primary-nav a[href="contacto.html"]').click();
        assert.equal(await p.locator('#email-universidad').textContent(), 'UO319242@uniovi.es');
        return { navigation: true, failedScript: 'site.js' };
      } finally { await partial.close(); }
    });
    await check('Sin JavaScript: menú, contactos y alternativa de búsqueda disponibles', async () => {
      const noJs = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 320, height: 568 } });
      const p = await noJs.newPage();
      try {
        await p.goto(base + 'index.html'); assert(await p.locator('.primary-nav').isVisible());
        await p.locator('.primary-nav a[href="contacto.html"]').click();
        assert.equal(await p.locator('#email-universidad').textContent(), 'UO319242@uniovi.es');
        await p.goto(base + 'buscar.html'); assert(await p.locator('noscript').isVisible());
        await p.locator('noscript a[href="mapa.html"]').click(); assert(p.url().endsWith('/mapa.html'));
        return { navigation: true, addresses: true, searchAlternative: true };
      } finally { await noJs.close(); }
    });
  } finally {
    await browser?.close(); await new Promise(resolve => server.close(resolve));
    report.summary = { passed: report.tests.filter(t => t.passed).length, failed: report.tests.filter(t => !t.passed).length, total: report.tests.length };
    await fs.writeFile(path.join(output, 'resultado-tecnico.json'), JSON.stringify(report, null, 2) + '\n');
  }
  console.log(JSON.stringify(report.summary));
  if (report.summary.failed) process.exitCode = 1;
})().catch(error => { console.error(error); process.exitCode = 1; });
