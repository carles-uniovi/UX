# Verificación de V3

Fecha: 20/11/2026. Todas las evidencias de esta carpeta corresponden a V3. Las pruebas automáticas usan Chrome real con tamaños de pantalla simulados; no son una cuarta prueba de usabilidad ni nuevas sesiones físicas de móvil o tableta.

## Resultados

| Comprobación | Resultado | Evidencia |
| --- | --- | --- |
| Generación | 18 páginas, nueve por idioma; 70 entradas de búsqueda | `scripts/build.py` |
| Estructura, rutas, anclas y servidor local | 536 referencias verificadas; 18 respuestas HTTP 200 | `scripts/check.py` |
| Motor de búsqueda | 15/15 casos | `scripts/test-search.cjs` |
| Interacciones con DOM simulado | 13/13 casos: menú y reproductores | `scripts/test-ui.cjs` |
| Buscador en Chrome | 21/21 casos | [resultado-navegador.json](buscador-pruebas/resultado-navegador.json) |
| Verificación final en Chrome | 17/17 casos, incluidos copia correcta/denegada, consulta, foco, tema, multimedia, fallo de JS y ausencia de Clarity | [resultado-tecnico.json](auditoria-v3/resultado-tecnico.json) |
| Adaptabilidad | 144 combinaciones, 18 páginas × ocho tamaños entre 320 y 1920 px; sin desbordamiento horizontal | `layouts` en el resultado técnico |
| Ampliación | Reflujo a 320 × 256, equivalente al área de 1280 px al 400 %, y texto al 200 % | No se presenta como zoom nativo del navegador |
| Accesibilidad automática | Axe 4.14.1: 36 análisis, 18 páginas en claro y oscuro, cero infracciones; 120 grupos de comprobaciones incompletas conservados | `axe` en el resultado técnico |
| HTML | Nu Html Checker 26.11.19, ejecución local: 18 páginas, cero errores y cero advertencias | [html-local.json](auditoria-v3/html-local.json), con hashes |
| CSS | css-tree 3.2.1 local: 607 declaraciones, cero errores detectados; 101 valores con variables fuera de su comprobador gramatical | [css-local.json](auditoria-v3/css-local.json) |
| Paquete Pages | V1, V2 y V3; 42 HTML con referencias locales comprobadas | `../scripts/build-pages.py`, desde la raíz de V3 |
| Conservación de V2 | 165 archivos con el mismo SHA-256 que al inicio de esta tarea | [base-v2.json](base-v2.json) |

El CSS con variables se analiza sintácticamente y se comprueba mediante el renderizado y los estilos calculados de Chrome. Esto no equivale a un resultado del servicio W3C CSS. La revisión automática de permisos rechazó el envío de HTML/CSS al servicio externo W3C por falta de autorización explícita para ese destino; se sustituyó por herramientas locales, sin transmitir el código.

## Lighthouse

Lighthouse 13.6.0 sobre un servidor local, con configuración móvil predeterminada y configuración de escritorio específica. Ejecución final, sin otras pruebas de navegador simultáneas:

| Página/configuración | Rendimiento | Accesibilidad | Buenas prácticas | SEO | LCP | CLS |
| --- | --- | --- | --- | --- | --- | --- |
| Portada, móvil | 100 | 100 | 100 | 100 | 1,35 s | 0 |
| Portada, escritorio | 100 | 100 | 100 | 100 | 0,32 s | 0 |
| Buscar «judo», móvil | 100 | 100 | 100 | 100 | 1,35 s | 0 |
| Contacto, móvil | 100 | 100 | 100 | 100 | 0,98 s | 0 |

Informes completos y condiciones de ejecución en los archivos `auditoria-v3/lighthouse-*.json`; [resumen](auditoria-v3/lighthouse-resumen.json). Son mediciones de laboratorio de estas rutas y condiciones, sujetas a variación. No miden la latencia de GitHub Pages ni el rendimiento de todos los dispositivos y páginas.

## Inspección de avisos y límites

Se revisaron las capturas de portada, menú móvil, confirmación de copia, búsqueda oscura y texto ampliado. El recorrido con Tab verifica el salto al contenido y que el foco no quede bajo la cabecera; Escape cierra menú y reproductor y restaura el foco. Los destinos de judo, canción y correo se mantienen. La copia bloqueada conserva y selecciona la dirección para copia manual.

Los 120 grupos incompletos de axe no se borran ni se presentan como aprobados automáticamente:

- `color-contrast` y `color-contrast-enhanced`: el símbolo decorativo del tema no es texto convencional. Se revisa su color heredado y fondo en ambos temas; la paleta comprueba al menos 7,34:1 para las combinaciones de texto y 3:1 para límites de controles. El símbolo tiene nombre de acción accesible mediante su botón.
- `label-content-name-mismatch`: axe no interpreta el símbolo «◐» como una palabra. Es decorativo (`aria-hidden`); el botón anuncia «Activar modo oscuro/claro» según su estado. Se verificó el cambio de nombre y `aria-pressed`.
- `identical-links-same-purpose`: enlaces repetidos en navegación, portada y lectura se inspeccionan según su contexto. Los destinos locales, anclas y enlaces externos conservan su propósito. Los nombres de tráileres y referencias se entienden junto al título de su tarjeta o sección. La herramienta no puede decidir esa equivalencia semántica por sí sola.

La ausencia de infracciones automáticas no acredita conformidad WCAG AAA. No se han verificado nuevas transcripciones, audiodescripciones o subtítulos completos de las canciones y tráileres externos, ni se ha realizado una sesión con lector de pantalla o personas con discapacidad. No se atribuyen a V3 resultados de TAW, AChecker o WAVE que no se hayan obtenido. La fotografía del gato no se presenta como retrato del autor.

## Capturas

- [Menú móvil](auditoria-v3/01-menu-movil.png).
- [Copia de correo](auditoria-v3/02-contacto-copiado.png).
- [Búsqueda en oscuro](auditoria-v3/03-busqueda-oscura.png).
- [Texto al 200 %](auditoria-v3/04-texto-200.png).
- [Portada de escritorio](auditoria-v3/05-portada-escritorio.png).

El sitio es estático y se entrega como versión final. Las limitaciones anteriores delimitan las evidencias disponibles; no se inventa una nueva evaluación con participantes.
