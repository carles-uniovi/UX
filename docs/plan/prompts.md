# Prompts de desarrollo

Los prompts 1 a 7 son **reconstrucciones orientativas**, redactadas a partir del [enunciado](../enunciado.md) y del código actual. No son transcripciones de las conversaciones utilizadas durante el desarrollo. El prompt 8 reproduce la petición real de documentación.

## 1. Estructura inicial del sitio

**Origen:** reconstrucción. **Objetivo:** organizar el sitio según los requisitos del trabajo.

```text
A partir del enunciado de docs/enunciado.md, crea un sitio web personal
ADWeb con al menos cinco páginas: Sobre mí, Trayectoria, Hobbies,
Intereses y Contacto. Usa HTML semántico, una navegación común y un pie
con el nombre y el identificador del estudiante. Enlaza las páginas
mediante rutas relativas e indica cuál está activa. Prepara carpetas
para estilos, scripts, imágenes y recursos multimedia.
```

**Implementación relacionada:** los cinco HTML de la raíz, su cabecera y pie compartidos, los enlaces de navegación y el atributo `aria-current="page"`.

## 2. Contenido personal e imágenes

**Origen:** reconstrucción. **Objetivo:** distribuir el contenido personal entre las páginas.

```text
Incorpora la información proporcionada por el autor para presentar a
Carles Valladares García. En Sobre mí incluye su fotografía y una breve
presentación; en Trayectoria, sus estudios en la UV, la UPV y la
Universidad de Oviedo. Organiza Hobbies en videojuegos, D&D y judo,
e Intereses en música, películas, series y animanga. Usa los recursos
locales de img/, textos alternativos y encabezados jerárquicos.
Mantén un tono personal y cercano y deja los datos de contacto en su
página específica.
```

**Implementación relacionada:** presentación en `index.html`, secciones académicas en `trayectoria.html`, categorías en `hobbies.html` e `intereses.html`, e imágenes organizadas por página.

## 3. Diseño visual y adaptación a pantallas

**Origen:** reconstrucción. **Objetivo:** aplicar una apariencia coherente y adaptable.

```text
Centraliza el diseño de las cinco páginas en css/styles.css. Usa una
tipografía del sistema, un ancho de contenido limitado y espaciados
consistentes. Emplea Grid y Flexbox para la trayectoria, las categorías
y el contacto. Adapta la cabecera y las secciones a pantallas pequeñas,
permite que los textos largos se ajusten y conserva las proporciones
de las imágenes. Incluye estilos de foco visibles para los controles.
```

**Implementación relacionada:** hoja de estilos común, tarjetas de categorías, cuadrícula de contacto y consultas de medios para reorganizar la cabecera y la trayectoria.

## 4. Paletas y selector de tema

**Origen:** reconstrucción. **Objetivo:** incorporar los modos claro y oscuro.

```text
Prepara una muestra de varias paletas oscuras para comparar fondo,
superficies, texto y acento. Incorpora al sitio una paleta oscura de
grafito y lavanda y un tema claro con acento violeta, definidos mediante
propiedades personalizadas de CSS. Añade un botón en la cabecera para
alternar los temas y guarda la elección en localStorage. Aplica el tema
guardado antes de cargar los estilos y permite usar el selector aunque
el almacenamiento no esté disponible. Refleja el estado del botón con
aria-pressed y revisa la presentación de los logotipos en ambos temas.
```

**Implementación relacionada:** muestra en `work/paletas-oscuras.html`, variables de color en `css/styles.css`, selector en los cinco HTML y persistencia mediante `js/theme.js`.

## 5. Audio y vídeo en un diálogo

**Origen:** reconstrucción. **Objetivo:** asociar canciones y tráileres a las tarjetas de Intereses.

```text
Usa los MP3 y MP4 de docs/media/ para incorporar reproducción a las
tarjetas de música y películas de Intereses. Identifica el tipo y la ruta
con atributos data-media-type y data-media-src. Crea los botones desde
un script compartido y abre un elemento dialog con el título de la
tarjeta y un reproductor audio o video con controles nativos. Intenta
iniciar la reproducción al abrir y muestra un mensaje si el navegador
la bloquea. Permite cerrar el diálogo con su botón, con Escape o desde
el fondo; al cerrarlo, detén la reproducción y libera el recurso.
```

**Implementación relacionada:** atributos de las tarjetas en `intereses.html`, reproductor en `js/media-dialog.js`, estilos del diálogo y archivos locales de `docs/media/`. El script también se carga en `hobbies.html`, donde actualmente no hay tarjetas con recursos multimedia asociados.

## 6. Página de contacto y créditos de iconos

**Origen:** reconstrucción. **Objetivo:** organizar las vías de contacto y documentar los recursos utilizados.

```text
Organiza Contacto en dos bloques: personal y universidad. En cada uno
muestra el correo con un enlace mailto y el perfil de GitHub. Usa iconos
SVG locales de correo y GitHub, mantén su legibilidad en ambos temas
y adapta las tarjetas al ancho disponible. En los enlaces que abren
otra pestaña incluye la indicación accesible y los atributos rel
correspondientes. Documenta la procedencia y las modificaciones de los
iconos y conserva la licencia del recurso de Bootstrap Icons.
```

**Implementación relacionada:** `contacto.html`, estilos de contacto, `img/contacto/README.md`, iconos SVG y `img/contacto/BOOTSTRAP-LICENSE.txt`.

## 7. Revisión del sitio

**Origen:** reconstrucción. **Objetivo:** proponer comprobaciones coherentes con la implementación.

```text
Revisa que las cinco páginas estén enlazadas y que carguen sus imágenes,
estilos, scripts y archivos multimedia. Comprueba el diseño en pantallas
pequeñas y grandes, los dos temas y la persistencia de la preferencia.
Revisa la jerarquía de encabezados, los textos alternativos, las etiquetas
de los controles y el foco visible. Comprueba con teclado el selector
de tema, la apertura del reproductor y su cierre con Escape. Confirma
que la reproducción se detiene al cerrar el diálogo y registra los
problemas observados sin dar por realizadas comprobaciones pendientes.
```

**Implementación relacionada:** navegación común, atributos semánticos y accesibles, estilos de foco, tema persistente y cierre del reproductor. Este apartado describe una propuesta de revisión; no registra una ejecución histórica ni resultados de pruebas.

## 8. Documentación del proyecto

**Origen:** petición literal del autor en esta conversación. **Objetivo:** crear el README y la carpeta de prompts.

```text
Vamos a documentar el proyecto.
Un readme describiendolo y dentro de docs una carpeta "plan" donde indiquemos los diferentes prompts empleados para el desarrollo de esta
```

**Resultado:** `README.md` describe el proyecto, las páginas, las tecnologías y su justificación, la ejecución local y los recursos. `docs/plan/README.md` organiza las fases y explica el alcance del registro; este archivo reúne los prompts e identifica su procedencia.
