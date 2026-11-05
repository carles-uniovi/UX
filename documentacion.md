# ADWeb · Sitio web personal

La guía breve de ejecución y entrega está en [leeme.txt](leeme.txt).

Sitio web personal de **Carles Valladares García (UO319242)**, desarrollado para el trabajo «Sitio ADWeb» de la asignatura Estándares Web Corporativos del Máster en Ingeniería Web de la Universidad de Oviedo.

El proyecto presenta información personal, trayectoria académica, aficiones, intereses culturales y vías de contacto. Consta de cinco páginas enlazadas mediante una navegación común y combina textos, fotografías, iconos, audios y vídeos. El [enunciado del trabajo](docs/enunciado.md) recoge los requisitos y su posterior uso en la asignatura Experiencia de Usuario (UX).

## Páginas

| Página | Contenido |
| --- | --- |
| [Sobre mí](index.html) | Fotografía, nombre y presentación personal. |
| [Trayectoria](trayectoria.html) | Estudios en la Universitat de València, la Universitat Politècnica de València y la Universidad de Oviedo. |
| [Hobbies](hobbies.html) | Videojuegos, Dungeons & Dragons y judo. |
| [Intereses](intereses.html) | Música, películas, series y animanga; reproducción de canciones y tráileres. |
| [Contacto](contacto.html) | Correos y perfiles de GitHub personales y universitarios. |

## Funcionalidades y diseño

- **Diseño adaptable:** distribución mediante Grid y Flexbox, imágenes flexibles y ajustes para pantallas pequeñas.
- **Temas claro y oscuro:** selector en la cabecera, con preferencia guardada en `localStorage` bajo la clave `adweb-theme`. El tema inicial es claro; si el almacenamiento está bloqueado, el selector funciona durante la visita a esa página.
- **Reproducción multimedia:** las tarjetas de música y películas abren un diálogo con controles nativos de audio o vídeo. Al cerrarlo se detiene la reproducción y se libera el recurso.
- **Navegación y accesibilidad:** estructura semántica, jerarquía de encabezados, textos alternativos, indicación de la página activa, etiquetas para los botones y estilos de foco visibles. Estas medidas describen la implementación; no constituyen una certificación de accesibilidad.
- **Recursos locales:** fotografías, iconos y archivos multimedia se sirven desde el proyecto. Algunas imágenes se cargan de forma diferida mediante `loading="lazy"`.

## Tecnologías y justificación

| Tecnología | Uso y motivo de elección |
| --- | --- |
| HTML | Organiza el contenido de las cinco páginas mediante elementos semánticos. Resulta adecuado para un sitio informativo estático y permite usar controles multimedia y diálogos del navegador. |
| CSS | Centraliza el aspecto visual en una hoja compartida. Grid, Flexbox y las consultas de medios adaptan la distribución; las propiedades personalizadas permiten mantener los dos temas. Se utiliza anidamiento CSS nativo. |
| JavaScript sin frameworks | Añade el selector de tema y el reproductor en diálogo mediante la API del DOM. Las interacciones son pequeñas y no requieren dependencias, instalación de paquetes ni compilación. |
| SVG y formatos de imagen | Los SVG permiten representar iconos y logotipos escalables; las fotografías y portadas usan PNG, JPEG, WebP y AVIF según el recurso. |
| MP3 y MP4 | Almacenan las canciones y los tráileres que se reproducen con los elementos nativos `audio` y `video`. |

No se emplean frameworks, bibliotecas de JavaScript, backend ni base de datos. Los iconos de correo proceden de Bootstrap Icons como archivos SVG independientes: no se incorpora el framework Bootstrap. Su ventaja es disponer de un recurso reconocible y reutilizable sin añadir una biblioteca al sitio.

## Cómo abrir el sitio

Para una consulta rápida, abre `index.html` en un navegador moderno. Conserva la estructura de carpetas para que funcionen las rutas relativas de imágenes, estilos, scripts y multimedia.

Para trabajar con una dirección HTTP local, desde esta carpeta puedes usar un servidor estático. Por ejemplo, si tienes Python instalado:

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

Después abre `http://localhost:8000/`. Detén el servidor con `Ctrl+C`. Python es una opción para servir los archivos, no una dependencia del sitio.

El navegador debe admitir anidamiento CSS nativo, el elemento `dialog` y los formatos multimedia utilizados. JavaScript habilita el cambio de tema y los botones de reproducción; el contenido y los enlaces de las páginas pueden consultarse sin él.

## Estructura del proyecto

```text
.
├── leeme.txt                 # Guía breve de entrega
├── documentacion.md          # Documentación ampliada
├── index.html
├── trayectoria.html
├── hobbies.html
├── intereses.html
├── contacto.html
├── css/
│   └── styles.css            # Estilos compartidos y temas
├── js/
│   ├── theme.js              # Selector y persistencia del tema
│   └── media-dialog.js       # Reproductor multimedia en diálogo
├── img/                      # Imágenes organizadas por página
├── docs/
│   ├── enunciado.md          # Requisitos del trabajo
│   ├── media/                # Audios MP3 y vídeos MP4
│   └── plan/                 # Documentación de los prompts por fases
└── work/
    └── paletas-oscuras.html   # Muestra de alternativas de color
```

## Edición y comprobaciones

El contenido se modifica directamente en cada HTML. Los cambios visuales comunes se realizan en `css/styles.css`, y los recursos se añaden en la subcarpeta correspondiente de `img/` o en `docs/media/`.

Para asociar una tarjeta de `intereses.html` a un archivo multimedia, su sección utiliza `data-media-type="audio"` o `data-media-type="video"` y `data-media-src` con la ruta del archivo. Debe incluir una imagen y un encabezado `h3`, que el script utiliza para crear el botón y el título del diálogo.

Después de editar, conviene comprobar:

1. La navegación entre las cinco páginas y la carga de los recursos locales.
2. La distribución en pantallas estrechas y anchas, en ambos temas.
3. La conservación del tema al cambiar de página o recargar.
4. La reproducción de audios y vídeos, y su detención al cerrar el diálogo.
5. La navegación con teclado, el foco visible y el cierre del diálogo con Escape.

## Plan y prompts de desarrollo

La carpeta [docs/plan](docs/plan/README.md) organiza las fases de desarrollo y los prompts asociados. Al no disponer de las conversaciones originales en el proyecto, los prompts de desarrollo se presentan como una **reconstrucción orientativa a partir del código actual**, no como una transcripción del historial real.

## Créditos de los recursos

La procedencia de los iconos de contacto se documenta en [img/contacto/README.md](img/contacto/README.md). La licencia MIT de Bootstrap Icons se conserva en [BOOTSTRAP-LICENSE.txt](img/contacto/BOOTSTRAP-LICENSE.txt). Las fotografías, portadas, logotipos, canciones y tráileres restantes corresponden a sus respectivos autores o titulares; este documento no les atribuye una licencia de redistribución.
