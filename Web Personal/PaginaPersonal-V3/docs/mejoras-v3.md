# Análisis y mejoras de V3

Revisión final: 20/11/2026. Se parte de una copia independiente de V2. No se modifica la versión utilizada en la tanda 2.

## Evidencia de partida

El evaluador comunica éxito en las tres tareas y ausencia de dificultades al navegar. La pericia informática es una estimación del evaluador, no una valoración de satisfacción.

| Participante | Perfil | Dispositivo comunicado | Tarea final | Tiempo aproximado | Pericia |
| --- | --- | --- | --- | --- | --- |
| U01 | Hombre, 24 años, estudiante de Economía | PC, Chrome | Encontrar el deporte y comprobar si también lo enseña | 15 s | 7/10 |
| U02 | Hombre, 20 años, estudiante de Telecomunicaciones | Tableta, Chrome | Encontrar el título de la canción de Gavina.mp3 | 34 s | 6/10 |
| U03 | Hombre, 26 años, trabajador de Unicaja | Móvil, MobileSafari | Localizar y copiar el correo universitario | 12 s | 8/10 |

Los tiempos son duraciones de sesión de Clarity. El responsable indica que la sesión se cerró uno o dos segundos después de completar la tarea: se conservan los valores como aproximación, sin restar un margen fijo. U01 corresponde a la repetición con tarea intercambiada; el primer intento sin grabación localizada queda fuera. Clarity clasifica U02 como PC, aunque se comunica una tableta.

Las tareas son diferentes y la muestra contiene tres personas. El éxito comunicado no permite concluir que cualquier usuario resolverá cualquier tarea ni comparar la eficiencia de los dispositivos. No se dispone de valoraciones numéricas de la aplicación, citas literales, revisión completa de las reproducciones ni exportaciones de mapas de calor para este análisis. No se inventan esas evidencias.

## Decisiones e implementación

La navegación por secciones, las categorías, los contenidos personales y los destinos de las tres tareas se conservan: no hay evidencia para reorganizarlos. Se aplican mejoras pequeñas con beneficios comprobables.

| Elemento revisado en V2 | Mejora de V3 | Justificación y comprobación |
| --- | --- | --- |
| Buscar y menú identificados principalmente mediante iconos | Texto visible «Buscar» y «Menú», manteniendo los iconos y objetivos táctiles de 44 px | Hace explícitas las acciones sin exigir reconocer símbolos. Comprobado a 320 px y con teclado. No es una queja atribuida a los participantes. |
| Confirmación de copia alejada de la dirección | Botones «Copiar correo personal/universitario» y mensaje junto a cada dirección; «Copiado» y alternativa de selección manual si el navegador bloquea el portapapeles | Refuerza la certeza de la tarea de U03 y permite recuperarse de restricciones de permisos. Probadas copia correcta y copia denegada. |
| Recuperación y continuidad de búsqueda | Botón Limpiar, ejemplos Judo/Música/Contacto, consulta conservada al cambiar idioma | Reduce el esfuerzo para corregir o repetir una consulta. El envío lleva el foco al resumen; el siguiente Tab accede al primer resultado. Al escribir no se roba el foco. |
| Cabecera fija con altura variable por zoom y traducción | Desplazamiento de anclas calculado con la altura real; cabecera deja de ser fija en pantallas de poca altura | Evita que un destino o el foco queden tapados. Pruebas de reflujo, texto ampliado y destino de resultados. |
| Textos secundarios pequeños y controles con nombres accesibles mejorables | Ajustes de tamaño y espaciado; nombres de marca e idioma coherentes con su texto visible; acción de cambio de tema actualizada | Mayor legibilidad y mejor identificación mediante tecnologías de apoyo. Axe había detectado diferencias entre texto y nombre; se corrigieron antes del cierre. |
| Portada PNG de 859.649 bytes | WebP de 400, 640 y 817 px, con `srcset`/`sizes`: 18.068, 33.188 y 46.630 bytes | El navegador elige el tamaño adecuado. Reducción del 94,6–97,9 % respecto al PNG solicitado en V2. Se mantiene la fotografía original y su descripción. |
| Menú móvil y controles activados después del primer pintado | Se reserva el espacio de los controles y se recoge el menú antes del primer pintado; recuperación de enlaces si falla `site.js` | Lighthouse detectó desplazamientos durante la carga. Se corrigió el estado inicial y se midió de nuevo. Sin JavaScript los enlaces siguen visibles. |
| Metadatos de idiomas con URL relativa | Canonical y versiones equivalentes ES/EN con direcciones públicas absolutas | Lighthouse detectó `hreflang` relativo. Se corrige en las 18 páginas, conservando enlaces internos relativos para apertura local. |
| Integración de registro específica de la tanda | V3 no carga Clarity ni muestra el consentimiento del estudio; preferencia de tema propia | Las nuevas visitas no se mezclan con las grabaciones de V2. No se modifica ni se elimina el proyecto de Clarity. |

## Correcciones de accesibilidad posteriores

La comprobación con TAW, AChecker y WAVE motivó cambios adicionales: nombres de tráileres y saltos de Lectura que distinguen destinos, creación de la lista del buscador solo cuando contiene resultados, eliminación de alternativas y títulos redundantes, explicación de abreviaturas e instrucciones de contacto más claras. El detalle H48 de TAW permitió contrastar una alerta sobre prosa inglesa que no representa una lista; se reformuló conservando su significado y estructura.

La medición real de líneas de Lectura detectó máximos de 89/87 caracteres ES/EN; con 60ch pasan a 75/73. Se comprobaron interlineado, separación de párrafos, reflujo y colores forzados. Las pruebas de apoyo incluyen ahora 18 casos de interfaz y accesibilidad.

El [estudio de accesibilidad](accesibilidad-v3.md) conserva los resultados iniciales/finales, explica advertencias y revisa cada criterio no verificado. También identifica barreras multimedia pendientes: los tres MP3 carecen de alternativa textual y las alternativas de los tráileres no están plenamente acreditadas. Estos hallazgos no se ocultan tras los contadores automáticos.

## Cierre

La V3 se entrega como versión final, con verificación técnica propia. No se ha hecho una nueva tanda con participantes ni se presenta la automatización como sustituto de esa evaluación. Los resultados se detallan en [verificacion-v3.md](verificacion-v3.md), con evidencias generadas para V3.
