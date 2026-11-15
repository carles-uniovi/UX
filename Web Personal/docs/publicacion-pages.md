# Publicación por versiones en GitHub Pages

## Direcciones

| Dirección | Contenido |
| --- | --- |
| <https://carles-uniovi.github.io/UX/> | Portada de selección de versiones |
| <https://carles-uniovi.github.io/UX/v1/> | `Web Personal/PaginaPersonal` |
| <https://carles-uniovi.github.io/UX/v2/> | `Web Personal/PaginaPersonal-V2` |
| `https://carles-uniovi.github.io/UX/v3/` | Se publicará cuando exista `Web Personal/PaginaPersonal-V3/index.html` |

Las direcciones V1 y V2 son independientes. V3 no redirige a V2 ni se crea con contenido ficticio. Para las pruebas de GazeRecorder, usar directamente la URL de V2; la portada de selección no forma parte de la tarea de usabilidad.

## Funcionamiento

El workflow [pages.yml](../../.github/workflows/pages.yml) se ejecuta al modificar las carpetas de las versiones, el empaquetador o el propio workflow en `main`. También permite ejecución manual desde GitHub Actions. GitHub Pages debe tener **GitHub Actions** como fuente de publicación; el repositorio ya utilizaba esta configuración.

El script [build-pages.py](../scripts/build-pages.py) copia cada versión a su propio directorio dentro de `.pages-site/`, sin modificar sus HTML, estilos, JavaScript ni recursos. Comprueba que los enlaces locales y los recursos referenciados por HTML y CSS existan en el paquete. Incluye las páginas españolas e inglesas de V2. Publica los medios necesarios de `docs/media`, pero excluye informes, plantillas de participantes, scripts de mantenimiento y demás documentación.

Cada despliegue de Pages sustituye el paquete publicado completo. Por eso el workflow **siempre empaqueta todas las versiones disponibles**, aunque solo haya cambiado una. Las fuentes de V1 y V2 se conservan en sus carpetas; para añadir V3 se crea una carpeta nueva. No renombrar V2 como V3 ni borrar las versiones previas. Las URLs son estables, pero modificar los archivos de una versión también actualizará lo que se ve en su URL: conservar una referencia de commit por tanda y evitar cambios durante las sesiones.

El workflow anterior todavía apuntaba a `PaginaPersonal` en la raíz del repositorio. La nueva configuración utiliza las rutas actuales bajo `Web Personal`.

## Comprobar localmente

Desde `Web Personal`, con Python 3.12 o posterior:

```powershell
python scripts/build-pages.py
python -m http.server 8000 --bind 127.0.0.1 --directory .pages-site
```

Abrir <http://127.0.0.1:8000/>, <http://127.0.0.1:8000/v1/> y <http://127.0.0.1:8000/v2/>. Detener con `Ctrl+C`. `.pages-site/` es un directorio generado e ignorado por Git; no se mantiene una segunda copia de las webs en el repositorio.

## Añadir la siguiente versión

1. Crear `Web Personal/PaginaPersonal-V3` conservando V1 y V2.
2. Incorporar la web completa y su `index.html`, con la misma organización de páginas y recursos. Si requiere otros tipos o directorios de recursos, ampliar el empaquetador.
3. Ejecutar el empaquetador y comprobar los enlaces y las tres rutas.
4. Publicar los cambios en `main`. El script añade V3 a la portada y al paquete automáticamente.

## Prueba de GazeRecorder

La candidata elegida para probar es **GazeRecorder online**. La publicación HTTPS proporciona una dirección accesible desde ordenador, tableta y teléfono; no activa seguimiento por sí misma. Crear y validar el estudio en una fase posterior, empezando por un piloto. Comprobar captura ocular, navegación entre páginas, desplazamiento y exportación de mapas de mirada y clics/toques en los tres dispositivos antes de los participantes reales.

Las versiones comparten origen de navegador y actualmente usan la misma clave de preferencia de tema (`adweb-theme`). Abrir una ruta distinta no borra esa preferencia. Preparar el mismo estado inicial del navegador antes de cada sesión, como indica el protocolo.
