# UX

Proyectos de la asignatura Experiencia de Usuario del Máster en Ingeniería Web de la Universidad de Oviedo.

## Página personal

El sitio web está en [`PaginaPersonal/`](PaginaPersonal/). Incluye presentación, trayectoria académica, hobbies, intereses y contacto.

Consulta su [README](PaginaPersonal/README.md) para abrirlo y revisar la documentación.

Para servirlo desde la raíz del repositorio:

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Después visita <http://127.0.0.1:8000/PaginaPersonal/>.

## GitHub Pages

El workflow [pages.yml](.github/workflows/pages.yml) publica el contenido de `PaginaPersonal/` en GitHub Pages al actualizar esa carpeta en `main`. También puede ejecutarse desde Actions con **Run workflow**.

En Settings → Pages, la fuente de publicación debe ser **GitHub Actions**. La cuenta y la visibilidad del repositorio deben permitir GitHub Pages.

La dirección del sitio será <https://carles-uniovi.github.io/UX/>. Las rutas relativas de imágenes, estilos, scripts y multimedia se conservan.
