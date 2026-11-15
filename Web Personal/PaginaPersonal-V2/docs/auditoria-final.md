# Revisión de V2 frente a las valoraciones

Revisión realizada el **14 de noviembre de 2026**, después de los cambios de interfaz, los tráileres de YouTube y la apertura de enlaces externos en otra pestaña.

## Resultado

Se han contrastado los **21 criterios** de la métrica en las **cinco hojas de los tres archivos** de valoraciones. Las comprobaciones locales de las **18 páginas** pasan: 548 rutas y anclas, 70 entradas de búsqueda, 15 pruebas del motor y 13 pruebas de interacción con DOM simulado. Las 18 páginas responden HTTP 200. La paleta de texto mantiene un contraste mínimo calculado de 7,34:1.

Hay una implementación para las carencias de navegación, ayuda, idiomas, búsqueda, contacto, experiencia, referencias y actualización. Eso no permite atribuir una nueva calificación ni dar por comprobados los criterios que exigen herramientas o usuarios reales.

## Fuentes comprobadas

- [Autoevaluación, IA y calibración](../../valoraciones/Metrica-WebPersonal-IA-v2-UO319242.xlsx): `Autoevaluación!C14:G39`, `Evaluación-IA!C14:I39` y `Calibración-IA!C10:L35`.
- [Evaluación UO294013](../../valoraciones/ValladaresGarcia-Carles-Tanda1_UO294013-Evaluador.xlsx): `WebPersonal!C15:G40`.
- [Evaluación UO294768](../../valoraciones/Valladares-García-Carles_Tanda1-UO294768-Evaluador.xlsx): `WebPersonal!C15:G40`.

Se releen 105 filas de criterio, incluidas sus observaciones. Los originales no se modifican. La [extracción local](auditoria/metricas-origen.json) conserva celdas y hashes de las fuentes, sin los prompts de evaluación. Las diferencias de puntuación entre evaluadores se mantienen como valoraciones de V1, no como resultados actuales.

## Correcciones encontradas en esta revisión

1. **Idioma en lectura:** el generador conservaba el saludo valenciano pero perdía su `lang="ca"` al construir `lectura.html`. Se conserva ahora la marca en ambos idiomas.
2. **Separación de texto:** en lectura se juntaban el nombre del autor al perder un salto y las etiquetas con sus direcciones de contacto. Se preservan los espacios y separadores y se muestran los cinco contactos en líneas propias. Los enlaces siguen siendo comprensibles sin imágenes y sin CSS.
3. **Impresión:** el tema oscuro podía dejar colores secundarios claros al imprimir. El estilo de impresión redefine también las variables de ese tema para usar texto oscuro y fondo blanco. La corrección se revisa en código; falta comprobar una impresión real.
4. **Validación oficial, tras autorización del autor:** Nu HTML Checker detectó 12 errores por los espacios de los enlaces de las tres canciones en Intereses y Lectura, en ambos idiomas. Se codifican ahora esas URL. Se sustituye el contenedor `article` de lectura por un `div`, ya que su título pertenece al `main`, eliminando dos advertencias. Los 18 HTML finales no tienen mensajes del validador.
5. **CSS oficial:** se elimina la extensión tipográfica `-apple-system`. En una revisión posterior se elimina también la propiedad obsoleta `clip`, se emparejan colores en superficies con fondo propio y se retiran reglas redundantes. Las advertencias bajan de 145 a 128 con el mismo nivel de análisis. La hoja final devuelve cero errores; los avisos conservados se clasifican en el [informe W3C](w3c.md).

El comprobador añade controles de idioma en lectura, separación de contactos y ausencia de saltos de nivel en los encabezados.

## Estado de los 21 criterios

«Implementado» indica que se ha encontrado la solución en las páginas y el código. «Pendiente de medición» implica que no se ha podido ejecutar la herramienta o interacción real que requiere el criterio.

| Criterio | Resultado y evidencia actual | Límite o siguiente comprobación |
| --- | --- | --- |
| 1.1 Comprensibilidad | Implementado: menú persistente, página activa, migas, índices, mapa y accesos de portada. Anclas existentes. | Confirmar comprensión con usuarios. |
| 1.2 Ayuda y retroalimentación | Implementado: Ayuda, instrucciones de búsqueda, resultados, ausencia de coincidencias, confirmación de copia y errores de reproducción. | Probar anuncios con lector de pantalla y errores reales del navegador. |
| 1.3 Estética | Identidad y encabezados morados comunes; se aplican las correcciones solicitadas en las capturas. | Revisión visual del resultado pendiente; no se asigna nota estética. |
| 1.4 Adaptabilidad medida | CSS adaptable y menú compacto con controles de cabecera de 44 px. | Pendiente de navegador/dispositivos y zoom. No se deduce adaptación correcta solo del CSS. |
| 1.5 Internacionalización | Nueve páginas por idioma, traducciones de mensajes y enlace a la página equivalente. Saludo valenciano marcado también en lectura. | Revisión lingüística humana y pronunciación con tecnología de apoyo. |
| 1.6 Redes sociales | GitHub personal/universitario y LinkedIn propio en Contacto. | No se añaden perfiles inexistentes; el LinkedIn de referencia está separado. |
| 2.1 Solo teclado | Salto al contenido, foco visible, botones nativos, menú y diálogo con gestión de foco y Escape en el código. Pruebas simuladas superadas. | Falta recorrido real, especialmente con foco dentro del iframe de YouTube. |
| 2.2 Sin gráficos | Enlaces con nombre textual o accesible, contenido estático y lectura completa de las cinco secciones. Se corrigen los separadores de contactos. | La página propia de lectura es una alternativa; no garantiza la extracción del modo lector de Chrome. |
| 2.3 Accesibilidad con herramientas | Etiquetas, ARIA, encabezados, contraste y ausencia de reproducción automática comprobados localmente. | Pendientes TAW, AChecker, WAVE y revisión manual. YouTube no acredita por sí solo AAA. |
| 3.1 Buscador | 35 entradas por idioma; 15 pruebas pasan: tildes, varias palabras, relevancia, vacíos y destinos concretos. | Falta prueba de interfaz y anuncios con navegador real. |
| 3.2 Navegación | Menú, mapa, lectura, índices y rutas verificadas. Externos en pestaña nueva; navegación interna en la actual. | Validar foco y percepción de los cambios de contexto en navegador. |
| 4.1 Aficiones | Se conservan los ocho contenidos de aficiones y los nueve de intereses, con textos y medios. | Se respeta la preferencia del autor por descripciones breves expresada en la calibración. |
| 4.2 Formación y trabajo | Tres etapas académicas, proyecto del sitio, prácticas en Medicarama (2025) y trabajo en V2c (2026). | Las empresas y años son los aportados; no se inventan funciones o logros. |
| 4.3 Contacto | Dos correos, dos GitHub y LinkedIn propio; copia opcional y enlaces de correo. | Confirmar apertura y copia en dispositivos reales. No hace falta simular un formulario sin envío. |
| 4.4 Referencias | Perfil público de un colega en un apartado propio, enlazado desde Trayectoria. | Es una referencia personal aportada por el autor; no acredita un aval de las empresas. |
| 5.1 Ausencia de errores | Rutas, identificadores, jerarquía y sintaxis pasan. Se corrigen lectura e impresión en esta auditoría. | Falta fotografía personal real: la portada sigue mostrando el gato con descripción veraz. |
| 5.2 Validación HTML | W3C Nu HTML Checker: 18 páginas, cero errores y cero advertencias. | Respuestas y hashes conservados en `auditoria/w3c-html.json`. No equivale a certificación de accesibilidad. |
| 5.3 Validación CSS | W3C CSS Validator, perfil CSS3, advertencias nivel 2: cero errores y 128 advertencias. | Se clasifican las 91 redefiniciones, 34 avisos de cascada de color y 3 de variables en `w3c.md`. |
| 5.4 Actualización | Fecha de revisión visible en todas las páginas, con `time` y fecha legible por máquina. | Mantener la fecha vinculada a revisiones reales. |
| 6.1 Rendimiento medido | Recursos locales optimizados y carga de YouTube solo al abrir un tráiler. | Pendiente Lighthouse. Las puntuaciones antiguas de las hojas no se reutilizan. |
| 6.2 Tiempo de carga | Sin precarga de canciones; iframe bajo demanda; HTTP 200 en las 18 páginas. | HTTP 200 no mide FCP/LCP ni tiempos de navegación. Mediciones en navegador pendientes. |

## Recorrido por páginas

| Páginas, en español e inglés | Contenido y controles revisados |
| --- | --- |
| Sobre mí | Identidad, descripción de imagen correcta, saludo con idioma y cuatro accesos a secciones. |
| Trayectoria | Formación, proyecto, dos experiencias y enlace a la referencia. |
| Aficiones | Ocho contenidos distribuidos en videojuegos, rol y judo. |
| Intereses | Nueve contenidos; tres canciones locales y dos enlaces oficiales de YouTube con diálogo. |
| Contacto | Cinco contactos propios y una referencia separada. |
| Ayuda | Siete preguntas, instrucciones vigentes y vías alternativas. |
| Mapa | Destinos internos al contenido concreto; sin anclas inexistentes. |
| Buscar | Etiqueta, instrucciones, estado accesible, índice del idioma y alternativas sin JavaScript. |
| Lectura | Cinco secciones, sin imágenes, con contactos separados, idioma del saludo y enlaces de retorno. |

El [inventario de páginas](auditoria/paginas.json) registra los archivos y sus hashes al terminar la revisión local.

## Pendientes que impiden cerrar la evaluación completa

- **Acceso a navegador:** la herramienta informa que no hay navegador ni aplicación nativa conectados. No se han podido medir las pantallas, el zoom, Lighthouse, la reproducción ni el teclado real.
- **Accesibilidad multimedia:** comprobar subtítulos y pistas de cada tráiler, calidad de alternativas y necesidades de las canciones. Activar los controles de YouTube no garantiza que todas las alternativas existan.
- **Fotografía personal:** se necesita una fotografía del autor para completar el requisito original. No se sustituye el gato por una imagen ficticia.
- **Usuarios reales:** ejecutar el protocolo de tanda 2 y registrar resultados observados. No se inventan tiempos, opiniones, mapas de calor ni seguimiento de ojos.

La revisión local queda realizada. La calificación final debe apoyarse en las comprobaciones pendientes y en la valoración del evaluador, no en una nota calculada a partir de la existencia del código.

La validación W3C se ejecutó posteriormente al recibir autorización expresa del autor para el envío de HTML y CSS. El bloqueo previo ya está resuelto. Los JSON actuales contienen resultados de la validación realizada, y los archivos con sufijo `-inicial` conservan los hallazgos previos a las correcciones.
