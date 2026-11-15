# Herramientas para la evaluación de la tanda 2

Revisión documental: **15 de noviembre de 2026**. Preferencia indicada: **priorizar herramientas gratuitas**. Selección para el piloto: **GazeRecorder online**. Se prepara la [publicación de V2 en GitHub Pages](../../docs/publicacion-pages.md) para probarla por URL. Sin cuentas, contratación ni seguimiento activado; todavía no se ha realizado la prueba funcional.

## Qué necesitamos obtener

El [enunciado, Evaluación - Tanda 2](../../enunciado.md) permite una herramienta que cubra ambas funciones. Para esta evaluación buscamos tres evidencias diferenciadas:

1. Seguimiento de la mirada durante la navegación: recorrido o reproducción de la mirada.
2. Mapa de calor de la mirada, generado con las muestras de esa sesión.
3. Mapa de calor de clics o toques, como complemento solicitado para esta prueba.

Las capturas deben realizarse mientras cada participante ejecuta la tarea en la **V2 real**, conservando su navegación y buscador. Una predicción de atención sobre una captura, el movimiento del ratón o una grabación de pantalla sin datos oculares no sustituyen al seguimiento de ojos. Con una webcam se estima la mirada; la calidad debe comprobarse después de calibrar.

Se propone U01 en ordenador de escritorio con webcam, U02 en tableta y U03 en teléfono con cámara frontal. Cada persona utiliza exclusivamente su dispositivo asignado. Una emulación móvil en un ordenador no sustituye la prueba en teléfono.

## Comparativa

| Opción | Mirada y mapa ocular | Clics / toques | Uso externo e impacto en V2 | Coste y limitación decisiva |
| --- | --- | --- | --- | --- |
| **GazeRecorder online** | El proveedor anuncia seguimiento con cámara, grabaciones y mapas oculares | Documenta datos de clics; **no queda confirmado un mapa de calor de clics independiente y exportable en el acceso gratuito** | La FAQ anuncia evaluación de webs por URL sin añadir scripts, y soporte de PC y móvil. Tableta, navegación entre páginas y buscador deben probarse | Primera candidata para un piloto sin pago. No hay confirmación documental suficiente de cuotas, exportaciones y gratuidad online para todo el estudio |
| **GazeRecorder de escritorio** | Seguimiento por webcam, grabación y mapa ocular dinámico | Mapa de clics no confirmado | Aplicación externa para PC; no resuelve por sí sola las sesiones reales de tableta y teléfono | Descarga gratuita para uso no comercial. **No confundir esta licencia con el servicio online** |
| **RealEye** | Seguimiento, mapas y reproducción de mirada documentados | El análisis permite visualizar clics; comprobar que la salida elegida satisface el mapa de clics requerido | Screen Recording evalúa la web real externamente, pero no funciona en smartphones. Embedded Website requiere SDK y configurar áreas de interés | Ofrece prueba temporal y planes educativos. No es la primera elección con prioridad gratuita; la modalidad y el plan importan |
| **WebGazer.js + mapas de mirada y clics preparados para el estudio** | WebGazer proporciona muestras estimadas de mirada; habría que guardar recorridos y generar mapas | Habría que registrar clics/toques y representarlos por separado | Requiere desarrollo en una copia de evaluación de V2; hay que preservar sesión y calibración al cambiar de página | Sin suscripción al servicio, con trabajo de implementación. WebGazer terminó su mantenimiento oficial en febrero de 2026; compatibilidad y calidad en los dispositivos concretos pendientes |
| **Microsoft Clarity**, como segunda herramienta | No proporciona seguimiento ocular por cámara; sus mapas de atención no lo sustituyen | Mapas de clics y desplazamiento en ordenador, tableta y móvil | Necesita código de seguimiento en las páginas; su extensión es para consultar datos de páginas ya instrumentadas | Servicio gratuito. Complementaría al seguimiento ocular si este no cubre los clics; compatibilidad simultánea aún por verificar |

Fuentes de GazeRecorder: [funciones generales](https://gazerecorder.com/), [FAQ sobre datos de ojos/clics, dispositivos y webs por URL](https://gazerecorder.com/faq/), [seguimiento móvil](https://gazerecorder.com/mobile-eye-tracking/), [descarga gratuita no comercial](https://gazerecorder.com/download-gazerecorder/) y [funciones de la aplicación de escritorio](https://gazerecorder.com/gazerecorder/). Son capacidades anunciadas por el proveedor, todavía sin comprobar en esta web. El portal de la aplicación no se pudo consultar mediante la herramienta de investigación (respuesta HTTP 403); esto no demuestra que no funcione en un navegador normal.

Fuentes de RealEye: [tipos de estudio](https://realeye.io/support/comparing-study-types), [limitaciones móviles](https://www.realeye.io/support/what-you-cannot-test-with-realeye), [mapas y visualización de clics](https://realeye.io/support/how-to-analyze-heatmaps) y [Embedded Website](https://realeye.io/support/embedded-website-tests-for-aggregated-results). La selección de un plan con pruebas móviles no elimina la limitación de Screen Recording. El motor Webcam v3 no admite teléfonos ni tabletas; para esos dispositivos la documentación indica v1.

Sobre el coste: la [oferta educativa de RealEye](https://realeye.io/for-education) anuncia una prueba de siete días y un plan Student de 49 USD/mes con estudios de hasta 60 segundos. Ese límite puede truncar esta tarea y no conviene adaptar la prueba de usabilidad a él. El plan Solo Researcher figura a 249 USD/mes, hasta cinco minutos y con exportación. Confirmar funciones de la prueba temporal, soporte móvil y exportaciones antes de elegirlo; precios sujetos a cambios.

Fuentes de la alternativa abierta: [repositorio y funciones de WebGazer](https://github.com/brownhci/WebGazer) y [última versión planificada, 3.5.3](https://github.com/brownhci/WebGazer/releases). No es una aplicación de informes lista para usar: necesitaría el registro y análisis descritos en la tabla.

Fuentes de Clarity: [funciones de los mapas](https://learn.microsoft.com/en-us/clarity/heatmaps-overview), [gratuidad y dispositivos](https://learn.microsoft.com/en-us/clarity/faq) y [requisito de código y limitaciones de los mapas](https://learn.microsoft.com/en-us/clarity/heatmaps/heatmaps-features).

## Recomendación para decidir

**Primera candidata: GazeRecorder online, condicionada a un piloto gratuito.** Es la opción externa que más se aproxima documentalmente al flujo deseado sin modificar V2. Antes de seleccionarla definitivamente hay que demostrar que el acceso disponible permite las tres sesiones, la navegación real en los tres dispositivos y guardar las tres evidencias, especialmente el mapa de clics. No se considera confirmada como solución gratuita completa.

Si ofrece mirada y mapa ocular sin coste, pero no mapa de clics, la segunda opción sería **GazeRecorder online + Microsoft Clarity**, tras verificar que capturan la misma sesión. Esta combinación implicaría añadir Clarity a una copia de evaluación. La compatibilidad no se da por supuesta por el hecho de funcionar ambas en navegador.

Si el acceso online exige pagar o no funciona en un dispositivo, la alternativa sin suscripción es preparar **WebGazer con registro y mapas propios**. Supone más desarrollo y también exige un piloto en tableta y teléfono. RealEye queda como alternativa si se dispone de una licencia institucional o una prueba temporal suficiente.

**Conclusión de la revisión:** no se ha confirmado una aplicación externa, gratuita y lista para usar que cumpla todos los requisitos en los tres dispositivos. Se ha elegido probar primero GazeRecorder online y mantenerlo para las sesiones reales solo si supera las comprobaciones siguientes. La configuración del estudio se hará después de publicar las versiones.

## Piloto de aceptación, previo a los tres participantes

Usar una persona de prueba distinta de U01–U03 y una búsqueda distinta de la tarea evaluada. No mezclar sus datos con los resultados. Repetir en los tres dispositivos reales.

| Comprobación | Ordenador | Tableta | Teléfono |
| --- | --- | --- | --- |
| Acceso gratuito disponible, sin contratar un plan | [pendiente] | [pendiente] | [pendiente] |
| Permiso de cámara y calibración válidos | [pendiente] | [pendiente] | [pendiente] |
| La mirada sigue zonas conocidas de la pantalla tras calibrar | [pendiente] | [pendiente] | [pendiente] |
| La portada, enlaces internos, búsqueda y desplazamiento funcionan | [pendiente] | [pendiente] | [pendiente] |
| Continúa capturando mirada y clics/toques al cambiar de página | [pendiente] | [pendiente] | [pendiente] |
| Se guarda reproducción o recorrido ocular de toda la tarea | [pendiente] | [pendiente] | [pendiente] |
| Se guarda mapa ocular de las páginas visitadas | [pendiente] | [pendiente] | [pendiente] |
| Se guarda mapa de clics/toques distinguible del mapa ocular | [pendiente] | [pendiente] | [pendiente] |
| Las evidencias pueden descargarse o conservarse para el informe | [pendiente] | [pendiente] | [pendiente] |
| Duración, número de sesiones y acceso a resultados suficientes | [pendiente] | [pendiente] | [pendiente] |
| Si hay dos herramientas: capturan a la vez sin interferencias | [pendiente / no aplica] | [pendiente / no aplica] | [pendiente / no aplica] |

No aprobar una opción si falta captura ocular en un dispositivo. Registrar los fallos y decidir una alternativa antes de convocar a los participantes. No reemplazar una sesión de navegación por una exposición a imágenes estáticas.

V2 actualmente se abre como archivos o por servidor local. Para servicios externos por URL puede ser necesaria una dirección HTTPS accesible desde todos los dispositivos. `localhost` en el teléfono se refiere al propio teléfono; compartir el servidor del ordenador por HTTP en la red no garantiza permisos de cámara. Resolver la dirección y los permisos en el piloto, antes de la incorporación.

## Registro de la elección definitiva

| Campo | Completar tras decidir y validar |
| --- | --- |
| Herramienta ocular y modalidad exacta | [pendiente] |
| Herramienta de mapas oculares | [pendiente] |
| Herramienta de mapas de clics/toques | [pendiente] |
| Plan, coste total y límites comprobados | [pendiente] |
| Fecha de caducidad de prueba y de acceso a resultados | [pendiente / no aplica] |
| Versión y configuración | [pendiente] |
| URL de la copia V2 evaluada | [pendiente] |
| Evidencias del piloto por dispositivo | [pendiente] |
| Incidencias y resolución | [pendiente] |
| Decisión y fecha | [pendiente] |

Después de elegir: preparar el entorno, ejecutar el piloto, activar la captura durante las tareas y rellenar la [plantilla de seguimiento](plantilla-seguimiento-tanda2.md). Conservar mapas separados por página, dispositivo y tipo de dato; no superponer coordenadas de diseños distintos en un único mapa.
