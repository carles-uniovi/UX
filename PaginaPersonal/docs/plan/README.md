# Plan y registro de prompts

Esta carpeta documenta el desarrollo del sitio ADWeb por fases y reúne los prompts asociados a cada una.

La guía actual está en [leeme.txt](../../leeme.txt) y los detalles en [documentacion.md](../../documentacion.md). Las menciones a README en el historial describen el nombre anterior.

## Alcance del registro

No se ha encontrado un registro de las conversaciones originales en los archivos del proyecto. Por ese motivo, los prompts de desarrollo de [prompts.md](prompts.md) son una **reconstrucción orientativa basada en el enunciado y la implementación actual**. No permiten afirmar cuál fue su redacción original ni el orden real en que se ejecutaron.

La numeración establece un orden lógico para explicar el trabajo. La única petición transcrita literalmente es la de documentación, disponible en esta conversación. Los resultados asociados indican qué partes del proyecto se relacionan con cada prompt; no acreditan que se ejecutase ese texto concreto ni que todas las verificaciones propuestas se hayan realizado.

## Fases

| Fase | Objetivo | Archivos relacionados |
| --- | --- | --- |
| 1. Estructura | Organizar cinco páginas y una navegación común a partir del enunciado. | `index.html`, `trayectoria.html`, `hobbies.html`, `intereses.html`, `contacto.html` |
| 2. Contenido | Incorporar la presentación, trayectoria, aficiones e intereses personales. | Las cinco páginas e `img/` |
| 3. Diseño adaptable | Crear una hoja de estilos compartida y distribuciones flexibles. | `css/styles.css` |
| 4. Temas | Explorar paletas e incorporar el selector de modo claro y oscuro. | `work/paletas-oscuras.html`, `css/styles.css`, `js/theme.js` |
| 5. Multimedia | Reproducir canciones y tráileres en un diálogo. | `intereses.html`, `js/media-dialog.js`, `css/styles.css`, `docs/media/` |
| 6. Contacto y recursos | Presentar correos y perfiles con iconos locales y créditos. | `contacto.html`, `img/contacto/`, `css/styles.css` |
| 7. Revisión | Revisar navegación, recursos, adaptación y controles de teclado. | HTML, CSS y JavaScript del sitio |
| 8. Documentación | Describir el proyecto y registrar los prompts. | `README.md`, `docs/plan/` |

Los textos completos se encuentran en [prompts.md](prompts.md).

## Cómo mantener el registro

Cuando se recuperen prompts originales, sustituir las reconstrucciones correspondientes e indicar su procedencia. Para nuevas intervenciones, añadir el texto literal del prompt, su objetivo, los archivos afectados y el resultado observado. Separar siempre las peticiones reales de las propuestas o reconstrucciones, y registrar fechas únicamente cuando se conozcan.
