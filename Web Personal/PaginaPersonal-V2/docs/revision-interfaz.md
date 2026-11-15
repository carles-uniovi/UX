# Revisión de la interfaz a partir de las capturas

Cambios solicitados por el autor el 14 de noviembre de 2026. Se aplican a las nueve páginas en ambos idiomas.

| Problema observado | Cambio aplicado |
| --- | --- |
| Cabecera de dos filas y controles que saltaban de línea en móvil. | Una fila con marca, navegación de escritorio y controles de 44 px. Hasta 64 em el menú se abre sobre el contenido y permanece cerrado inicialmente. Se elimina el subtítulo de la marca. |
| El buscador ocupaba un formulario completo en todas las páginas. | Acceso mediante una lupa; el formulario está en la página de búsqueda. |
| Dos nombres de idioma y botón de tema con texto consumían espacio. | Un enlace EN o ES al otro idioma y botón de tema con icono, nombre accesible y tooltip. |
| Migas, nombre del autor, título grande, descripción e índice retrasaban el contenido. | Migas pequeñas, título de 1,75–2,15 rem, sin nombre ni introducción repetidos. Índice de categorías sin caja de fondo ni etiqueta visible redundante. |
| Pie con ayudas, redes y navegación repetida, todos con la misma apariencia. | Tres enlaces de apoyo: Ayuda, Mapa del sitio y Lectura, en color secundario y subrayados al interactuar. Las redes se reúnen en Contacto; se retira la fila adicional de mapa y vuelta arriba. |
| Los reproductores desplegados alteraban la altura y alineación de las tarjetas. | Un diálogo compartido, creado con controles nativos al activarlo. Cerrar con la cruz, Escape o el fondo detiene y libera el medio y devuelve el foco al enlace. |
| Faltaba el LinkedIn propio. | Se añade al bloque personal de Contacto y al mapa, lectura e índice de búsqueda. El perfil del colega sigue separado como referencia. |

## Texto retirado o abreviado

- «Mi espacio personal» bajo la marca, y nombre del autor sobre cada título interior.
- Pie de foto «La foto que me acompañaba en la primera versión».
- Párrafos de introducción que enumeraban lo que aparecía inmediatamente debajo.
- Explicación de que los correos abren una aplicación y GitHub se abre en la misma pestaña.
- «Escribir un correo» y «Ver perfil en GitHub», repetidos dentro de enlaces ya identificados.
- Notas bajo los reproductores acerca de letras y transcripciones. La falta de alternativas verificadas sigue recogida en la documentación de accesibilidad.
- Repetición de empresa y año en las tarjetas de experiencia, ya indicados en su encabezado.
- Lema «De la teoría a la práctica» y explicación detallada de las funciones de la propia web en la tarjeta del proyecto.
- Instrucciones sobre cómo usar el índice de lectura. Los enlaces del índice y de retorno se mantienen.

La ayuda conserva las explicaciones necesarias para usar los controles. Los nombres accesibles de botones y enlaces se mantienen aunque su texto no sea visible. Sin JavaScript, el menú sigue accesible y los enlaces multimedia abren el archivo directamente.

## Verificación

Se comprobaron las 18 páginas, 548 rutas y anclas y 70 entradas de búsqueda. Pasan 15 pruebas del buscador y 13 pruebas de las interacciones con un DOM simulado. Se conserva el contraste mínimo de paleta de 7,34:1.

No había navegador conectado para revisar visualmente el resultado. Quedan por comprobar en navegador las anchuras de 320 a 1440 px, el zoom, las posiciones al saltar a una ancla y el comportamiento nativo del diálogo. Las medidas de CSS describen la implementación, no una medición de capturas del resultado.

Los tr?ileres se sustituyen posteriormente por YouTube dentro del mismo di?logo. V?ase [youtube.md](youtube.md).
