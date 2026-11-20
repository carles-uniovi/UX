/* El índice es un script local para admitir también la apertura con file://.
   textContent y nodos de texto evitan interpretar como HTML lo que se busca. */
(() => {
  // Los destinos son relativos: el índice inglés se resuelve dentro de en/.
  const english = document.documentElement.lang === 'en';
  const input = document.querySelector('#query');
  const form = input.closest('form');
  const status = document.querySelector('#search-status');
  const results = document.querySelector('#search-results');
  const empty = document.querySelector('#search-empty');
  const clear = document.querySelector('.search-clear');
  const language = document.querySelector('.language-switch');
  const index = window.SEARCH_INDEX[english ? 'en' : 'es'];
  // Recupera enlaces compartidos o recargados y limita consultas externas largas.
  input.value = (new URLSearchParams(location.search).get('q') || '').slice(0, 160);
  function render() {
    const query = input.value.trim();
    if (clear) clear.hidden = !input.value;
    // Cambiar de idioma conserva la consulta, sin interpretarla como HTML.
    if (language) {
      const path = language.getAttribute('href').split('?')[0];
      language.href = path + (query ? '?q=' + encodeURIComponent(query) : '');
    }
    results.replaceChildren();
    // Una lista vacía no representa resultados ni debe anunciarse como tal.
    results.hidden = true;
    empty.hidden = true;
    // Vacío o solo signos: se pide una palabra, sin mostrar todos los contenidos.
    if (!SiteSearch.tokens(query).length) {
      status.textContent = english ? 'Enter a word to search the site.' : 'Escribe una palabra para buscar en el sitio.';
      return;
    }
    const matches = SiteSearch.search(index, query);
    results.hidden = matches.length === 0;
    const list = document.createElement('ol');
    list.className = 'search-results';
    if (matches.length) results.append(list);
    // #search-status es una región aria-live polite en el HTML generado.
    status.textContent = english ? `${matches.length} ${matches.length === 1 ? 'result' : 'results'} for “${query}”.` : `${matches.length} ${matches.length === 1 ? 'resultado' : 'resultados'} para «${query}».`;
    empty.hidden = matches.length > 0;
    for (const item of matches) {
      // Solo se crean elementos conocidos. Nunca se concatena la consulta en HTML.
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
      list.append(li);
    }
  }
  // Reemplazar la consulta evita generar una entrada del historial por pulsación.
  function updateUrl() {
    const url = new URL(location.href);
    if (input.value.trim()) url.searchParams.set('q', input.value.trim());
    else url.searchParams.delete('q');
    try { history.replaceState(null, '', url); } catch { /* Algunos navegadores restringen file://. */ }
  }
  // Enter o el botón ejecutan la búsqueda inmediatamente sin recargar la página.
  form.addEventListener('submit', event => {
    event.preventDefault();
    clearTimeout(pending);
    updateUrl();
    render();
    // Enter lleva al resumen; el siguiente Tab accede al primer resultado.
    if (SiteSearch.tokens(input.value).length) status.focus();
    else input.focus();
  });
  clear?.addEventListener('click', () => {
    clearTimeout(pending);
    input.value = '';
    updateUrl();
    render();
    input.focus();
  });
  let pending;
  input.addEventListener('input', () => {
    // Agrupa pulsaciones: el temporizador anterior se cancela y se esperan 200 ms.
    clearTimeout(pending);
    pending = setTimeout(() => { updateUrl(); render(); }, 200);
  });
  // Presenta el estado inicial o los resultados de q al abrir la página.
  render();
})();
