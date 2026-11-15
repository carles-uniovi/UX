/* Motor puro compartido por el navegador y las pruebas de Node. */
((scope) => {
  const normalise = value => String(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[’']/g, '');
  function tokens(value) {
    return [...new Set(normalise(value).match(/[\p{L}\p{N}]+/gu) || [])];
  }
  function search(items, query) {
    const words = tokens(String(query).slice(0, 160));
    if (!words.length) return [];
    return items.map((item, order) => {
      const title = normalise(item.title);
      const category = normalise(item.category);
      const body = normalise(item.text);
      if (!words.every(word => `${title} ${category} ${body}`.includes(word))) return null;
      const score = words.reduce((total, word) => total + (title.includes(word) ? 8 : 0) + (category.includes(word) ? 3 : 0) + (body.includes(word) ? 1 : 0), 0);
      return { ...item, score, order };
    }).filter(Boolean).sort((a, b) => b.score - a.score || a.order - b.order);
  }
  scope.SiteSearch = { normalise, tokens, search };
})(typeof window === 'undefined' ? globalThis : window);
