# Buscador de V3

Buscador local bilingüe, sin servidor de búsqueda ni peticiones a una API. El generador `scripts/build.py` crea 35 entradas por idioma en `js/search-index.js`. Cada entrada contiene título, categoría, texto y destino con ancla. `js/search-core.js` normaliza mayúsculas y tildes, separa términos, exige coincidencia conjunta y ordena por relevancia, con prioridad del título y desempate estable. Se conservan las rutas de V2.

`js/search.js` presenta los resultados con nodos DOM y `textContent`, sin interpretar la consulta como HTML. La consulta se limita a 160 caracteres y se conserva en `?q=` al compartir, recargar y cambiar a la página equivalente del otro idioma. El formulario funciona al escribir con espera de 200 ms, con Enter o con el botón Buscar. Los cambios al teclear no desplazan el foco. Enter o Buscar llevan al resumen anunciado por `role="status"`; el siguiente Tab alcanza el primer resultado.

V3 añade Limpiar, que elimina consulta, resultados y `q` y devuelve el foco al campo. Los ejemplos permiten volver a buscar Judo, Música o Contacto. Sin coincidencias se ofrece una orientación y el mapa del sitio. Sin JavaScript se conserva el acceso al mapa y a la versión de lectura. La apertura mediante `file://` está comprobada en ambos idiomas.

## Pruebas

- `node scripts/test-search.cjs`: 15 casos del motor, incluidos tildes, términos múltiples, puntuación, relevancia, entrada vacía y texto con sintaxis HTML.
- `node scripts/test-search-browser.cjs`: 21 casos en Chrome, incluidos las 18 cabeceras, consultas compartidas, idioma, teclado, móvil, modo oscuro, ausencia de JS y archivos locales.
- `node scripts/test-final-browser.cjs`: recuperación con ejemplos, Limpiar, destinos de las tres tareas y visibilidad del destino bajo la cabecera, además de las comprobaciones generales de V3.

Resultados y ocho capturas del buscador: [resultado-navegador.json](buscador-pruebas/resultado-navegador.json). Son pruebas técnicas reproducibles; no contienen opiniones ni sesiones nuevas de usuarios.
