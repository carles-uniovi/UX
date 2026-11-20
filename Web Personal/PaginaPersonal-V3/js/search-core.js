/* Motor puro compartido por el navegador y las pruebas de Node.
   No lee el DOM ni realiza peticiones: recibe el índice y devuelve coincidencias.
   Funcionamiento y mantenimiento: docs/buscador.md. */
((scope) => {
  // NFD separa las letras de sus marcas; se eliminan tildes y apóstrofos
  // para comparar «MÚSICA» con «musica» y «Baldur’s» con «baldurs».
  const normalise = value => String(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[’']/g, '');
  // Conserva letras y números Unicode. Set evita puntuar dos veces una
  // palabra repetida; los espacios y los signos no constituyen términos.
  function tokens(value) {
    return [...new Set(normalise(value).match(/[\p{L}\p{N}]+/gu) || [])];
  }
  function search(items, query) {
    // El límite también se aplica aquí: no depende del maxlength del formulario.
    const words = tokens(String(query).slice(0, 160));
    if (!words.length) return [];
    return items.map((item, order) => {
      const title = normalise(item.title);
      const category = normalise(item.category);
      const body = normalise(item.text);
      // AND entre términos dentro de una misma entrada. includes admite
      // fragmentos de palabra, sin corrección ortográfica ni búsqueda por frases.
      if (!words.every(word => `${title} ${category} ${body}`.includes(word))) return null;
      // Cada término aporta 8/3/1 puntos si aparece en título/categoría/texto.
      // Se suman los campos coincidentes, no el número de apariciones del término.
      const score = words.reduce((total, word) => total + (title.includes(word) ? 8 : 0) + (category.includes(word) ? 3 : 0) + (body.includes(word) ? 1 : 0), 0);
      return { ...item, score, order };
    }).filter(Boolean).sort((a, b) => b.score - a.score || a.order - b.order);
  }
  // order resuelve empates por posición original, sin alterar el índice.
  // La misma API puede cargarse en la web o en un entorno sin navegador.
  scope.SiteSearch = { normalise, tokens, search };
})(typeof window === 'undefined' ? globalThis : window);
