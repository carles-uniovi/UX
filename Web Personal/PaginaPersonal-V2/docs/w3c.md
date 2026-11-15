# Validación oficial W3C

Realizada el **14 de noviembre de 2026**, tras la autorización explícita del autor para enviar los HTML y el CSS a los servicios W3C.

| Servicio | Configuración | Resultado final |
| --- | --- | --- |
| [Nu HTML Checker](https://validator.w3.org/nu/) | Los 18 HTML completos, respuesta JSON | **0 errores y 0 advertencias**. Ningún mensaje en las 18 respuestas. |
| [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) | Archivo `css/styles.css`, perfil `css3`, medio `all`, advertencias `2`, respuesta SOAP 1.2 | **0 errores, 128 advertencias**. El servicio devuelve `validity=true`. |

## Correcciones y comprobación de los resultados

El primer análisis HTML encontró 12 errores: tres enlaces de audio con espacios en Intereses y Lectura, repetidos en español e inglés. Se codifican ahora los nombres en las URL, conservando los archivos originales. También aparecieron dos advertencias por el contenedor `article` de lectura sin título propio. Se utiliza un `div`: la estructura sigue contando con el título del `main` y los encabezados de sus secciones.

En la primera revisión CSS se sustituyó `clip-path`, no reconocido por ese analizador, por `clip: rect(...)`, que el servicio aceptó con una advertencia de obsolescencia. También se retiró `-apple-system`, señalado como extensión del fabricante.

En la revisión de advertencias se elimina también `clip`: el texto accesible se coloca con una sangría de 2 px dentro de una caja absoluta de 1 px, sin salto de línea y con desbordamiento oculto. Se conservan los textos y los nombres accesibles; no se utiliza `display:none`. Su funcionamiento con tecnología de apoyo real sigue pendiente.

Se explicitan los colores de texto en cabecera, tarjetas, paneles, ayuda, menú desplegable y otras superficies con fondo propio. El fondo blanco de los logotipos tiene ahora texto oscuro para que el texto alternativo de una imagen fallida resulte legible también en modo oscuro. Se retiran la regla `.lead` no utilizada, estilos de tema sobreescritos por los botones de icono, una declaración de impresión redundante y dos variaciones mínimas de cabecera.

El resultado baja de **145 a 128 advertencias**, con el mismo perfil y nivel 2 de advertencias. Se eliminan 17 avisos: 10 por color ausente, 1 por fondo ausente, 5 por redefinición y 1 por propiedad obsoleta. No se han ocultado avisos ni añadido fondos artificiales a todos los textos para modificar el contador.

Las respuestas originales y corregidas se guardan en `auditoria/`. Los hashes SHA-256 de **los 18 HTML y la hoja CSS final** coinciden con los archivos enviados. Se conserva el análisis inicial como historial de las correcciones; no debe confundirse con el resultado final.

## Clasificación de las 128 advertencias CSS restantes

| Tipo devuelto por Jigsaw | Cantidad | Interpretación y tratamiento |
| --- | --- | --- |
| `redefinition` | 91 | Sobrescrituras que se conservan por la cascada y los puntos de cambio, por ejemplo rejillas, separación, tamaños y colores de impresión. Eliminarlas solo para reducir el contador suprimiría ajustes adaptables o de interacción. Su efecto final debe comprobarse en navegador. |
| `no-background-color` | 31 | Textos, enlaces y estados que comparten el fondo del contenedor. Añadir un fondo opaco a cada regla alteraría la composición y los estados de interacción. El analizador no demuestra un contraste incorrecto; hay que comprobar la combinación efectiva. |
| `no-color` | 3 | Fondo del iframe, fondo oscurecido del diálogo y punto decorativo de la línea académica. No contienen texto propio al que asignar color. El contenido del iframe tiene sus propios estilos. |
| `css-variable` | 3 | El servicio indica que no comprueba estáticamente las variables CSS por su naturaleza dinámica. Las paletas de ambos temas se verifican además con el comprobador local. |

Las advertencias se han consultado con el nivel máximo usado en esta revisión, sin ocultarlas. No se presenta el resultado como «cero problemas». La paleta calculada mantiene un contraste mínimo de 7,34:1, pero eso no verifica todos los fondos efectivos, estados o contenido de terceros.

Las [instrucciones del validador CSS](https://jigsaw.w3.org/css-validator/manual.html) diferencian los errores de las advertencias. El [alcance de Nu HTML Checker](https://validator.w3.org/nu/about.html) también indica que su resultado no es una certificación general. Siguen pendientes Lighthouse, dispositivos, tecnologías de apoyo y la accesibilidad real de los medios.

## Evidencias y repetición

- [Respuestas HTML finales](auditoria/w3c-html.json).
- [Respuesta CSS final](auditoria/w3c-css.xml) y [hash de la hoja validada](auditoria/w3c-css.json).
- [Resumen y lista completa de advertencias](auditoria/w3c-resumen.json).
- [CSS antes de reducir advertencias](auditoria/w3c-css-antes-advertencias.xml) y [hash de esa versión](auditoria/w3c-css-antes-advertencias.json).
- [Hallazgos HTML iniciales](auditoria/w3c-html-inicial.json) y [primer análisis CSS](auditoria/w3c-css-inicial.xml).

`scripts/validate-w3c.py` realiza el envío cuando se ejecuta expresamente; no forma parte de la generación ni de las pruebas locales. La autorización debe cubrir el contenido que se vaya a enviar. El modo `--changed-only --html-only` reutiliza respuestas cuyo hash no haya cambiado, y valida de nuevo los HTML modificados. `--css-only` envía únicamente la hoja de estilos.

La entrada directa de Jigsaw devolvió inicialmente HTTP 500 con la excepción `Reader used`. Se obtuvo una respuesta válida al usar su formulario de subida de archivos multipart, manteniendo el mismo CSS y configuración. Ese error del servicio no se contabiliza como un error de la hoja.
