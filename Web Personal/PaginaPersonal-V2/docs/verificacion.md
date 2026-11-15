# Verificación de V2

Fecha: **14 de noviembre de 2026**. Entrega local, sin publicación ni cambios en la V1.

La [auditoría final](auditoria-final.md) vuelve a contrastar los 21 criterios de las tres hojas de cálculo y documenta las correcciones. Después de la autorización expresa del autor, se ejecutan los validadores oficiales W3C y se corrigen los problemas encontrados. Los resultados están en [w3c.md](w3c.md).

## Comprobaciones ejecutadas

| Comprobación | Herramienta | Resultado |
| --- | --- | --- |
| Generación de contenido y traducciones | `python scripts/build.py` | 18 páginas y 70 entradas de búsqueda. |
| Estructura y recursos | `python scripts/check.py` | 548 rutas/anclas verificadas; sin destinos locales inexistentes. |
| Etiquetas e identificadores | Mismo comprobador | Un `main` y un `h1` por página; identificadores únicos, referencias ARIA existentes e inputs etiquetados. |
| Destino de enlaces | Mismo comprobador | Enlaces externos con `target="_blank"` y `rel="noopener noreferrer"` en ambos idiomas y lectura. La navegación interna conserva la pestaña actual. Los enlaces alternativos del diálogo abren otra pestaña. |
| Imágenes | Mismo comprobador | Atributos `alt`, anchura y altura presentes. Alternativa de portada corregida tras inspeccionar el archivo. |
| Peso de imágenes | Optimización local de copias con Pillow | PNG, JPEG y WebP utilizados: 6.898.457 → 2.482.311 bytes; lado máximo 960 px. Los originales de V1 se conservan. Se retiran 17 copias de recursos no usados. |
| Idiomas | Mismo comprobador | Atributos `lang` españoles e ingleses, páginas equivalentes y destinos existentes. |
| Lectura alternativa | Mismo comprobador | Las cinco secciones están presentes y la versión de lectura no contiene imágenes. |
| Multimedia | Comprobador estático y `node scripts/test-ui.cjs` | Tres audios locales y dos tráileres de YouTube; un diálogo por idioma. Audio con `preload="none"`; iframe bajo demanda con controles, teclado y subtítulos solicitados. Cierre y liberación comprobados con DOM simulado. |
| Contraste de la paleta | Cálculo de luminancia relativa en `check.py` | Mínimo 7,34:1 para texto, texto secundario y acento sobre fondo, superficie y fondo suave, en los dos temas. Texto sobre botón de acento ≥7:1; bordes de controles ≥3:1. |
| Servicio HTTP | Servidor Python temporal + consultas HTTP | Las 18 páginas respondieron 200 con tipo HTML; servidor cerrado al finalizar. |
| Búsqueda | `node scripts/test-search.cjs` | 15 pruebas superadas. Véase el informe del buscador. |
| Menú y diálogo | `node scripts/test-ui.cjs` | 13 pruebas superadas con DOM simulado: apertura, foco, Escape, limpieza, reapertura, errores, parámetros de YouTube, identificadores y enlaces alternativos. No es una prueba en navegador. |
| Sintaxis JavaScript | `node --check` en los cuatro scripts escritos y el índice generado | Sin errores de sintaxis. |
| HTML oficial | W3C Nu HTML Checker | 18 páginas: cero errores y cero advertencias, con hashes de los archivos finales. |
| CSS oficial | W3C CSS Validator, CSS3 y advertencias nivel 2 | Cero errores y 128 advertencias clasificadas en `w3c.md`. |

Estas comprobaciones no evalúan automáticamente todo WCAG, los estilos calculados por un navegador ni la corrección completa de HTML y CSS.

## Límite de la revisión visual

Se han usado las capturas aportadas por el autor para identificar los problemas de la primera interfaz de V2. Al intentar revisar los cambios, la herramienta volvió a devolver que no había anfitrión de navegador ni superficie nativa conectada. No se han tomado capturas del resultado ni se asignan puntuaciones de rendimiento, adaptabilidad o accesibilidad. Las trece pruebas de DOM simulado verifican la lógica del script, sin medir el diseño ni las funciones nativas del navegador. No se han confirmado los subtítulos ni las pistas de audio concretas de los tráileres; véase `youtube.md`.

## Revisión manual antes de la tanda 2

1. Abrir las páginas en ordenador, tableta y teléfono. Revisar 320, 375, 768, 1024 y 1440 px, ambos temas y ambas lenguas. Confirmar ausencia de desplazamiento horizontal y texto o controles recortados.
2. Probar zoom del 200 % y 400 %. Comprobar que la cabecera permite llegar al contenido y que las anclas no quedan tapadas. Verificar el cambio entre menú compacto y navegación de escritorio.
3. Recorrer solo con teclado: salto inicial, navegación, formularios, idioma, tema, ayuda y reproductores. Confirmar foco visible, orden comprensible, Escape en el menú móvil y ausencia de trampas.
4. Desactivar imágenes, CSS y JavaScript por separado. Confirmar navegación por texto, alternativa de lectura y acceso a ayuda. Probar además el modo lector propio del navegador, cuyo comportamiento puede variar.
5. Ejecutar los casos de interfaz de `buscador.md`, incluidos cero resultados, URL recargada, apertura directa de archivos y cambios de idioma.
6. Probar audio y vídeo en navegador, carga y volumen. Cerrar el diálogo con la cruz, Escape y el fondo: comprobar que se detiene el medio, vuelve el foco al enlace y se puede abrir otro. Confirmar recorrido de teclado dentro del diálogo y acceso directo al archivo sin JavaScript. Añadir subtítulos/transcripciones verificados antes de declarar accesibilidad multimedia.
7. Repetir la validación W3C si cambia HTML o CSS. La V2 actual ya cuenta con resultados propios, sin reutilizar los de V1. Revisar las advertencias CSS documentadas y sus contrastes efectivos.
8. Ejecutar Lighthouse con configuración y dispositivo documentados. Guardar rendimiento, tiempos de carga y accesibilidad. Comprobar también con TAW, AChecker y WAVE cuando corresponda según el enunciado y su disponibilidad. Revisar manualmente las advertencias y falsos positivos.
9. Revisar con un lector de pantalla los encabezados, regiones, estado de resultados, etiquetas y cambios de idioma. Verificar los contrastes efectivos de todos los estados, incluidos hover, foco y colores forzados.

## Información pendiente del autor

- Fotografía personal real para cumplir completamente el enunciado original. Se conserva la imagen del gato con descripción veraz.
- Fechas de estudios u otros proyectos verificables, si se desean añadir. La experiencia en Medicarama de 2025 y V2c de 2026 ya está incorporada con los datos facilitados.
- Subtítulos, transcripciones y otras alternativas multimedia que requiera la evaluación de accesibilidad.

La fecha visible de actualización debe cambiarse únicamente cuando se revise de nuevo el sitio. Las pruebas con usuarios y los informes de las siguientes fases siguen pendientes de realización real.

El perfil de LinkedIn facilitado para la referencia personal se conserva con su URL exacta. Se intentó consultarlo y el servicio de navegación no pudo recuperar la página; no se han extraído ni atribuido al colega cargos, empresas o avales adicionales.
