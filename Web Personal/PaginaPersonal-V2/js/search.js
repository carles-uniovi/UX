/* El índice es un script local para admitir también la apertura con file://.
   textContent y nodos de texto evitan interpretar como HTML lo que se busca. */
(() => {
  const english = document.documentElement.lang === 'en';
  const input = document.querySelector('#query');
  const form = input.closest('form');
  const status = document.querySelector('#search-status');
  const results = document.querySelector('#search-results');
  const empty = document.querySelector('#search-empty');
  const index = window.SEARCH_INDEX[english ? 'en' : 'es'];
  input.value = (new URLSearchParams(location.search).get('q') || '').slice(0, 160);
  function render() {
    const query = input.value.trim();
    results.replaceChildren();
    empty.hidden = true;
    if (!SiteSearch.tokens(query).length) {
      status.textContent = english ? 'Enter a word to search the site.' : 'Escribe una palabra para buscar en el sitio.';
      return;
    }
    const matches = SiteSearch.search(index, query);
    status.textContent = english ? `${matches.length} ${matches.length === 1 ? 'result' : 'results'} for “${query}”.` : `${matches.length} ${matches.length === 1 ? 'resultado' : 'resultados'} para «${query}».`;
    empty.hidden = matches.length > 0;
    for (const item of matches) {
      const li = document.createElement('li');
      const category = document.createElement('p');
      category.className = 'result-category';
      category.textContent = item.category;
      const title = document.createElement('h2');
      const link = document.createElement('a');
      link.href = item.url;
      link.textContent = item.title;
      title.append(link);
      const text = document.createElement('p');
      // Muestra un fragmento alrededor de la primera coincidencia del cuerpo.
      const position = Math.max(0, SiteSearch.normalise(item.text).indexOf(SiteSearch.tokens(query)[0]));
      const start = Math.max(0, position - 55);
      text.textContent = (start ? '…' : '') + item.text.slice(start, start + 230) + (item.text.length > start + 230 ? '…' : '');
      li.append(category, title, text);
      results.append(li);
    }
  }
  // Reemplazar la consulta evita generar una entrada del historial por pulsación.
  function updateUrl() {
    const url = new URL(location.href);
    if (input.value.trim()) url.searchParams.set('q', input.value.trim());
    else url.searchParams.delete('q');
    try { history.replaceState(null, '', url); } catch { /* Algunos navegadores restringen file://. */ }
  }
  form.addEventListener('submit', event => { event.preventDefault(); updateUrl(); render(); });
  let pending;
  input.addEventListener('input', () => {
    clearTimeout(pending);
    pending = setTimeout(() => { updateUrl(); render(); }, 200);
  });
  render();
})();
