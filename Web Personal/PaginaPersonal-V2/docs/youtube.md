# Tráileres de YouTube

Se sustituyen los dos MP4 de V2 por los vídeos publicados por sus distribuidores:

- [Spider-Man: Into the Spider-Verse · Sony Pictures Entertainment](https://www.youtube.com/watch?v=g4Hbz2jLxvQ).
- [Scott Pilgrim vs. the World · Universal Pictures](https://www.youtube.com/watch?v=7wd5KEaOtm4).

Las tarjetas conservan la ventana emergente y el enlace original como alternativa. El iframe se crea solo al abrir un tráiler, utiliza `youtube-nocookie.com`, tiene título accesible y mantiene controles, teclado y pantalla completa. No se activa reproducción automática. Al cerrar se descarga el iframe y se devuelve el foco al enlace.

Se solicitan subtítulos mediante `cc_load_policy=1` y el idioma de la página mediante `cc_lang_pref` y `hl`, siguiendo la [documentación oficial de parámetros de YouTube](https://developers.google.com/youtube/player_parameters). Estos parámetros no crean subtítulos ni pistas de audio inexistentes. Los idiomas, traducciones y cambios de audio que muestre el reproductor dependen de las pistas disponibles en cada vídeo. No se declara conformidad AAA por cambiar de reproductor.

«Ver en YouTube» está siempre disponible dentro del diálogo, también si el propietario bloquea la incrustación, el navegador restringe contenido externo o falta el identificador de origen. Se recomienda servir el sitio por HTTP: abrir un HTML con `file://` puede impedir que YouTube reciba el referente necesario. No se detectan automáticamente los errores internos del iframe, por ser de otro origen.

Las copias MP4 se retiran exclusivamente de V2. Los audios locales y la V1 se conservan.

## Verificación

Pasan las comprobaciones de estructura, 15 pruebas de búsqueda y 13 pruebas con DOM simulado. Estas últimas comprueban los parámetros del iframe, título, enlace a YouTube, validación del identificador y descarga al cerrar.

Queda pendiente una prueba real por HTTP para confirmar reproducción, disponibilidad y calidad de los subtítulos, pistas de audio, teclado dentro del iframe, cierre desde el reproductor y comportamiento en móvil. No había un navegador conectado para comprobar esos aspectos. La selección oficial del vídeo se ha contrastado con resultados de YouTube; no se ha comprobado su accesibilidad multimedia completa.
