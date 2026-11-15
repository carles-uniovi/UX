# Buscador: funcionamiento y pruebas

## Uso

El icono de lupa de la cabecera lleva al buscador desde cualquier página. En `buscar.html`, el formulario actualiza los resultados al escribir, después de 200 ms, o al enviarlo. La URL conserva `q`, por ejemplo `buscar.html?q=Ingenieria+Web`, y puede volver a abrirse.

Cada resultado incluye la categoría, el título y un fragmento del texto. El enlace lleva a una sección concreta, no solamente a la portada de la página. La búsqueda española usa el contenido español y la inglesa el inglés. Los enlaces de resultados son relativos al directorio del idioma.

## Implementación

1. `scripts/build.py` genera `js/search-index.js` con 35 entradas por idioma. Cada entrada tiene `url`, `title`, `text` y `category`. Incluye presentación, formación, proyecto, experiencia en Medicarama y V2c, aficiones, obras, títulos de canciones, contacto, LinkedIn propio, referencia personal por LinkedIn y preguntas de ayuda.
2. `js/search-core.js` normaliza a minúsculas, elimina diacríticos y apóstrofos, y separa palabras Unicode. Recorta la consulta a 160 caracteres y elimina términos repetidos.
3. Una entrada coincide si contiene todas las palabras en el conjunto de título, categoría y texto. Admite fragmentos de palabra. No aplica sinónimos, corrección de escritura ni búsqueda semántica.
4. Cada coincidencia en el título suma 8 puntos, en la categoría 3 y en el cuerpo 1. Se ordena por puntuación descendente y, en empates, por el orden del índice.
5. `js/search.js` presenta el resultado con nodos de texto y `textContent`. La consulta del visitante no se interpreta como HTML. No hay peticiones a un servidor ni transmisión a servicios externos.
6. Se anuncian el número de resultados, las consultas vacías y la ausencia de coincidencias con una región de estado. Sin JavaScript se ofrecen el mapa del sitio y la versión de lectura como alternativas.

El índice se carga con una etiqueta `script`, en lugar de `fetch`, para que también funcione al abrir el proyecto directamente con `file://`. Las páginas normales no cargan el índice ni el motor. Los scripts tienen comentarios que explican las decisiones y las alternativas ante restricciones del navegador.

## Informe de pruebas del motor

Ejecutado el 14 de noviembre de 2026 mediante `node scripts/test-search.cjs`, con Node.js 24.15.0. Resultado: **15 pruebas superadas**. Se utiliza el mismo motor y el mismo índice que entrega la web.

| Caso | Resultado comprobado |
| --- | --- |
| `MÚSICA` | Se normaliza a `musica`. |
| `judo` | Encuentra los dos contenidos de judo y los sitúa antes que la ayuda que menciona el término. |
| `sota el cel` | Enlaza a `intereses.html#gavina`. |
| `INGENIERIA WEB` | Primer resultado: `trayectoria.html#uniovi-title`. |
| `robe matematicas` | No combina contenidos de entradas diferentes; sin coincidencias. |
| `teaching`, en inglés | Encuentra `hobbies.html#ensenar-judo` en el idioma inglés. |
| `petun` | Encuentra Las Petunias por coincidencia parcial. |
| Dirección de correo personal | Encuentra el contacto personal pese a la puntuación de la dirección. |
| Consulta vacía, espacios y signos | Devuelve una lista vacía, sin resultados arbitrarios. |
| Palabra inexistente | Sin coincidencias. |
| Cadena con sintaxis de HTML | El motor la trata como términos; no la ejecuta. La interfaz usa nodos de texto. |
| Coincidencia en título frente a cuerpo | El título se ordena primero. |
| Misma consulta repetida | Orden de resultados estable. |
| Más de 160 caracteres | Se ignora el contenido que excede el límite. |
| Integridad del índice | Entradas con destino local, título, categoría y texto. |

La comprobación adicional `python scripts/check.py` verifica que todos los destinos y anclas del índice existen en ambos idiomas. También consulta las 18 páginas mediante HTTP.

## Pruebas de interfaz pendientes

No había un navegador conectado para ejecutar la interfaz real. Quedan por comprobar: acceso mediante la lupa de la cabecera, lectura de los anuncios con tecnología de apoyo, actualización al escribir, foco y teclado, recarga de una URL con `q`, navegación tras pulsar un resultado y funcionamiento real con `file://`. Los resultados anteriores acreditan el motor y las rutas, no estas interacciones de navegador.

Al cambiar el contenido, regenera las páginas y el índice con `python scripts/build.py`, ejecuta ambas comprobaciones y repite los casos de interfaz afectados. Si añades idiomas, adapta `LABELS`, los textos y la selección del índice en `search.js`.
