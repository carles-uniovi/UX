/* Mediciones Lighthouse locales de V3. No son pruebas con usuarios. */
const fs = require('node:fs/promises'), path = require('node:path'), http = require('node:http'), os = require('node:os');
const { pathToFileURL } = require('node:url');
const root = path.resolve(__dirname, '..'), out = path.join(root, 'docs/auditoria-v3');
const qaRoot = process.env.UX_QA_ROOT || path.join(os.tmpdir(), 'ux-v3-qa-01a1f4');
(async () => {
  await fs.mkdir(out, { recursive: true });
  const { default: lighthouse } = await import(pathToFileURL(path.join(qaRoot, 'node_modules/lighthouse/core/index.js')).href);
  const { default: desktopConfig } = await import(pathToFileURL(path.join(qaRoot, 'node_modules/lighthouse/core/config/desktop-config.js')).href);
  const launcher = await import(pathToFileURL(path.join(qaRoot, 'node_modules/chrome-launcher/dist/index.js')).href);
  const mime = { '.html':'text/html; charset=utf-8', '.js':'text/javascript', '.css':'text/css', '.png':'image/png', '.jpg':'image/jpeg', '.webp':'image/webp', '.svg':'image/svg+xml', '.avif':'image/avif' };
  const server = http.createServer(async (req, res) => {
    try {
      const name = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
      const p = path.resolve(root, '.' + name + (name.endsWith('/') ? 'index.html' : ''));
      if (!p.startsWith(root + path.sep)) return res.writeHead(403).end();
      const data = await fs.readFile(p);
      res.writeHead(200, {'Content-Type':mime[path.extname(p)] || 'application/octet-stream'}).end(data);
    } catch { res.writeHead(404).end(); }
  });
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  let chrome; const results = [];
  try {
    chrome = await launcher.launch({ chromePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', chromeFlags: ['--headless=new', '--disable-gpu'] });
    for (const [page, device] of [['index.html','mobile'],['index.html','desktop'],['buscar.html?q=judo','mobile'],['contacto.html','mobile']]) {
      const desktop = device === 'desktop';
      const { lhr } = await lighthouse('http://127.0.0.1:' + server.address().port + '/' + page, {
        port: chrome.port, output: 'json', logLevel: 'error',
        onlyCategories: ['performance','accessibility','best-practices','seo'],
        formFactor: device, screenEmulation: desktop ? { mobile: false, width: 1366, height: 900, deviceScaleFactor: 1, disabled: false } : undefined,
        throttlingMethod: 'simulate',
      }, desktop ? desktopConfig : undefined);
      const name = page.split('?')[0].replace('.html','') + '-' + device;
      await fs.writeFile(path.join(out, 'lighthouse-' + name + '.json'), JSON.stringify(lhr, null, 2));
      const summary = { page, device, version: lhr.lighthouseVersion, fetchTime: lhr.fetchTime,
        scores: Object.fromEntries(Object.entries(lhr.categories).map(([key,value]) => [key, Math.round(value.score*100)])),
        metrics: Object.fromEntries(['first-contentful-paint','largest-contentful-paint','cumulative-layout-shift','total-blocking-time'].map(key => [key,lhr.audits[key].numericValue])),
        failedAudits: Object.values(lhr.audits).filter(a => a.score !== null && a.score < 1).map(a => ({ id:a.id, title:a.title, score:a.score, displayValue:a.displayValue })) };
      results.push(summary); console.log(JSON.stringify(summary.scores), name);
    }
  } finally {
    await chrome?.kill(); await new Promise(r => server.close(r));
    await fs.writeFile(path.join(out, 'lighthouse-resumen.json'), JSON.stringify(results, null, 2));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
