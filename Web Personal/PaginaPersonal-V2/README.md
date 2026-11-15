# Página personal · V2

Segunda versión del sitio de Carles Valladares García, UO319242, para Experiencia de Usuario del Máster en Ingeniería Web. Parte de `../PaginaPersonal` y de `../enunciado.md`. La V1 y las valoraciones originales se conservan intactas.

## Abrir

Abre [index.html](index.html) en un navegador. No requiere instalación ni compilación. Los tráileres de YouTube necesitan conexión; para reproducirlos incrustados, sirve esta carpeta por HTTP:

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

Visita <http://127.0.0.1:8000/> y detén el servidor con `Ctrl+C`.

## Qué incluye

- Las cinco secciones originales: Sobre mí, Trayectoria, Aficiones e Intereses, y Contacto.
- Español e inglés en nueve páginas por idioma, con cambio a la página equivalente.
- Buscador de contenido, ayuda, mapa del sitio y versión de lectura de las cinco secciones personales.
- Cabecera de una fila, navegación móvil desplegable, migas compactas y acceso directo a categorías.
- Temas claro y oscuro, foco visible y controles de cabecera de 44 px. Música local y tráileres de YouTube en una ventana emergente, con sus controles originales.
- Pie con ayuda, mapa y lectura; las redes sociales se reúnen en Contacto.
- Corrección de erratas y de la descripción de la foto de portada, que muestra un gato, no al autor.
- Experiencia en Medicarama (prácticas en 2025) y V2c (trabajo en 2026), y enlace al LinkedIn de un colega como referencia personal.
- LinkedIn propio en Contacto, separado de la referencia personal.
- Enlaces externos en pestaña nueva; navegación interna en la actual. Los reproductores conservan su diálogo y sus enlaces alternativos abren otra pestaña.
- Fecha visible de revisión: 14 de noviembre de 2026.

HTML, CSS plano y JavaScript sin dependencias de ejecución. Se mantiene la identidad morada de la V1. No se añaden perfiles sociales, empleos, titulaciones adicionales ni personas de referencia sin datos aportados por el autor.

## Comprobar

Desde esta carpeta, con Python 3.9 o posterior y Node.js moderno:

```powershell
python scripts/check.py
node scripts/test-search.cjs
node scripts/test-ui.cjs
node --check js/theme.js
node --check js/site.js
node --check js/search-core.js
node --check js/search.js
```

La comprobación Python arranca un servidor temporal en un puerto libre, consulta las páginas por HTTP y lo cierra al terminar. No deja servicios activos.

## Editar

El contenido y las traducciones se mantienen juntos en [scripts/build.py](scripts/build.py). Tras modificarlos:

```powershell
python scripts/build.py
python scripts/check.py
node scripts/test-search.cjs
node scripts/test-ui.cjs
```

El generador escribe los 18 HTML y `js/search-index.js`. Los estilos se editan en `css/styles.css`; las interacciones, en `js/`. Las copias de recursos existentes no se sobrescriben, para conservar sus optimizaciones. Para reimportar una imagen de la V1, elimina solo su copia de V2 antes de regenerar. Para incorporar contenido nuevo al buscador, utiliza `record(...)` en el generador y actualiza la comprobación del tamaño del índice si corresponde.

Las páginas generadas se entregan listas para usar; Python solo es una herramienta de mantenimiento. Los nombres de archivo de las páginas inglesas coinciden con los españoles para mantener rutas y equivalencias sencillas.

## Documentación

- [Última auditoría frente a los 21 criterios de las valoraciones](docs/auditoria-final.md).
- [Resultados oficiales W3C y clasificación de advertencias CSS](docs/w3c.md).
- [Mejoras y trazabilidad de la métrica](docs/mejoras-v2.md).
- [Funcionamiento y pruebas del buscador](docs/buscador.md).
- [Resultados de verificación y comprobaciones manuales pendientes](docs/verificacion.md).
- [Preparación de las pruebas de usabilidad de la tanda 2](docs/usabilidad-tanda2.md).
- [Revisión de la interfaz a partir de las capturas](docs/revision-interfaz.md).
- [Tráileres de YouTube y opciones de accesibilidad](docs/youtube.md).

No se ha publicado ni desplegado esta versión. La validación W3C devuelve cero errores en los 18 HTML y en la hoja CSS; las advertencias CSS están documentadas. Estos resultados no equivalen a una puntuación nueva de Lighthouse ni a conformidad WCAG AAA. Faltan subtítulos y transcripciones verificados del contenido multimedia y una fotografía real del autor.

## Recursos

Las imágenes, logotipos y canciones proceden de la V1 y corresponden a sus respectivos titulares. Los tráileres se reproducen desde los canales oficiales de Sony Pictures Entertainment y Universal Pictures en YouTube; ya no se incluyen sus copias MP4 en V2. Los originales de V1 se conservan. Los iconos de Bootstrap de la V1 no se utilizan en esta versión. El favicon es un SVG de texto con las iniciales del autor.
