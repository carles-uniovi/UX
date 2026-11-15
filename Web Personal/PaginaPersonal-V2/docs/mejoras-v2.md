# Mejoras de la versión 2

Implementación local realizada el 14 de noviembre de 2026. El objetivo es corregir las carencias detectadas en la tanda 1 y preparar el sitio para su evaluación con usuarios no informáticos. No se presenta una nueva nota estimada como si fuera una evaluación realizada.

## Fuentes y criterio de decisión

- [Enunciado UX](../../enunciado.md), apartado «Web Personal V2».
- [Autoevaluación, evaluación IA y calibración](../../valoraciones/Metrica-WebPersonal-IA-v2-UO319242.xlsx): `Autoevaluación!C14:G39`, `Evaluación-IA!C14:I39` y `Calibración-IA!C10:L35`. Notas almacenadas: 5,3917 en `Autoevaluación!E10` y 5,1583 en `Evaluación-IA!E10`.
- [Evaluación UO294013](../../valoraciones/ValladaresGarcia-Carles-Tanda1_UO294013-Evaluador.xlsx), `WebPersonal!C15:G40`. Nota almacenada: 5,4417 en `E11`.
- [Evaluación UO294768](../../valoraciones/Valladares-García-Carles_Tanda1-UO294768-Evaluador.xlsx), `WebPersonal!C15:G40`. Nota almacenada: 6,5250 en `E11`.

Se han leído los valores y observaciones de los tres archivos, sin modificarlos. La calibración matiza las recomendaciones de la IA: el autor prefiere descripciones breves y no utiliza otras redes sociales. Por ello se mantienen los correos y perfiles reales de GitHub, y se organiza mejor el contenido existente.

El autor ha aportado después las prácticas en Medicarama de 2025 y el trabajo en V2c de 2026, junto con el perfil de LinkedIn de un colega que desea mostrar como referencia personal. Se incorporan esos datos en español, inglés, lectura y búsqueda. No se añaden puestos, responsabilidades ni avales laborales que no haya indicado; el LinkedIn pertenece a la persona de referencia, no al autor.

En la revisión posterior con capturas, el autor también aporta su LinkedIn personal. Se añade como contacto propio, diferenciado del colega de referencia. Se compacta la cabecera, se recorta texto redundante, se reorganiza el pie y se recuperan los reproductores en diálogo; los cambios concretos están en `revision-interfaz.md`.

Las observaciones sobre accesibilidad, formación y CSS difieren entre evaluadores. Se tratan como puntos que deben verificarse de nuevo. Pulsar Tab y Enter es un mecanismo válido de navegación por teclado; se mejora su recorrido mediante salto al contenido, foco visible, controles nativos y alternativas de navegación. El modo lector del navegador puede eliminar la cabecera: se añade una página de lectura propia, sin afirmar que se controle la extracción de Chrome.

## Trazabilidad por criterio

| Criterio | Respuesta en V2 | Evidencia o límite |
| --- | --- | --- |
| 1.1 Comprensibilidad | Página activa, migas en interiores, índice por categorías y mapa con enlaces a contenidos. | `mapa.html`, navegación común y anclas verificadas. |
| 1.2 Ayuda y retroalimentación | Preguntas frecuentes, ayuda de búsqueda, contador de resultados, ausencia de coincidencias y mensajes al copiar correo o fallar un medio. | `ayuda.html`, `buscar.html`, `js/site.js`. |
| 1.3 Estética | Identidad morada conservada, jerarquía tipográfica, portada desarrollada, secciones y encabezados coherentes. | `css/styles.css`; revisión visual pendiente. |
| 1.4 Móvil | Cabecera de una fila, menú desplegable superpuesto, controles de cabecera de 44 px y rejillas adaptables. | Altura mínima de cabecera declarada: 4 rem. Comprobación real en dispositivos pendiente. |
| 1.5 Internacionalización | Traducciones completas español/inglés de las nueve páginas, ayudas y mensajes, con `lang` y enlaces equivalentes. | 18 HTML; controles y rutas de idioma comprobados. Nombres de obras y archivos conservados. |
| 1.6 Redes sociales | GitHub personal y universitario y LinkedIn propio en Contacto. | El LinkedIn del colega se muestra aparte como referencia personal. |
| 2.1 Teclado | Enlace inicial para saltar al contenido, foco visible, menú con Escape y controles nativos. | Implementación revisada; prueba real de teclado y lector de pantalla pendiente. |
| 2.2 Sin gráficos | Todos los destinos de navegación tienen texto; versión de lectura reúne las cinco secciones sin imágenes. | `lectura.html`; sin JS el menú está abierto y el contenido es HTML estático. |
| 2.3 Herramientas de accesibilidad | Etiquetas, estructura, alternativas, contraste de paleta y ausencia de reproducción automática. | Comprobaciones propias superadas. Faltan TAW, AChecker, WAVE y revisión manual. Multimedia sin transcripción/subtítulos verificados: AAA no acreditado. |
| 3.1 Buscador | Acceso mediante lupa, índice bilingüe, coincidencias sin tildes, relevancia y enlaces al apartado concreto. | 35 entradas por idioma y 15 pruebas del motor. `docs/buscador.md`. |
| 3.2 Navegación | Menú, migas compactas, accesos de portada, índices internos y pie de ayuda, mapa y lectura. | 548 rutas y anclas locales comprobadas, incluidos recursos y formularios. |
| 4.1 Aficiones | Se conservan juegos, rol, judo y todos los intereses culturales de la V1. | Se muestran los títulos de las canciones que ya existían en los archivos. No se inventa una «canción favorita». |
| 4.2 Formación y experiencia | Formación reorganizada, proyecto de esta web y experiencia laboral en Medicarama (prácticas, 2025) y V2c (trabajo, 2026). | Empresas y años facilitados por el autor; no se deducen cargos, funciones ni logros. |
| 4.3 Contacto | Direcciones legibles, enlaces a correo, perfiles de GitHub, LinkedIn propio y copia opcional con confirmación o error. | Sin formulario que simule enviar mensajes ni backend innecesario. |
| 4.4 Personas de referencia | Enlace directo al perfil de LinkedIn de un colega como referencia personal, accesible desde Contacto y Trayectoria. | Perfil facilitado por el autor para su inclusión. No se presenta como aval de Medicarama o V2c. |
| 5.1 Errores | Se corrigen «funiconaba», «májica», acentos y expresiones confusas; la foto del gato tiene descripción correcta. | Rutas y sintaxis verificadas. Falta fotografía real del autor, exigida en el enunciado original. |
| 5.2 HTML | Plantilla común, HTML semántico, un `h1` por página y validación oficial W3C Nu. | 18 páginas: cero errores y cero advertencias. Respuestas en `auditoria/w3c-html.json`. |
| 5.3 CSS | CSS plano compartido; validación oficial W3C CSS3 con advertencias nivel 2. | Cero errores y 128 advertencias. Clasificación y límites en `w3c.md`; no se reutilizan resultados de V1. |
| 5.4 Actualización | Fecha real de revisión visible en todas las páginas mediante `time datetime="2026-11-14"`. | Actualizar al revisar contenido; no se usa una fecha automática que simule mantenimiento. |
| 6.1 Rendimiento | Sin fuentes externas ni frameworks; recursos gráficos locales y carga diferida fuera de portada. YouTube solo se carga al abrir un tráiler. Se retiran las copias MP4 de V2. | Las imágenes PNG, JPEG y WebP utilizadas pasan de 6,90 MB a 2,48 MB, aproximadamente un 64 % menos. Sin medición Lighthouse nueva. |
| 6.2 Carga | Audio con `preload="none"` e iframe de YouTube creados bajo demanda, imágenes con dimensiones y JavaScript diferido salvo el tema. | Sin tiempos de carga medidos en navegador. |

## Alcance de esta entrega

Se crea `PaginaPersonal-V2` como carpeta independiente y lista para servir estáticamente. Incluye el buscador opcional porque soluciona una carencia unánime de las métricas, junto con comentarios, documentación y pruebas de funcionamiento del motor.

La tanda 2 se prepara en un protocolo separado. No se añaden servicios de seguimiento ni datos ficticios de participantes. La V3, los informes con resultados de usuarios y las certificaciones de accesibilidad se realizarán con evidencia posterior.
