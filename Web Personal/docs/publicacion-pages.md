# Publicación por versiones en GitHub Pages

## Direcciones

| Dirección | Contenido |
| --- | --- |
| <https://carles-uniovi.github.io/UX/> | Portada de selección de versiones |
| <https://carles-uniovi.github.io/UX/v1/> | `Web Personal/PaginaPersonal` |
| <https://carles-uniovi.github.io/UX/v2/> | `Web Personal/PaginaPersonal-V2` |
| <https://carles-uniovi.github.io/UX/v3/> | `Web Personal/PaginaPersonal-V3`, versión final |

Las tres versiones tienen direcciones independientes. La tanda 2 se realizó sobre V2 con Clarity; V3 conserva sus contenidos y aplica las mejoras documentadas en su carpeta, sin registrar sesiones del estudio.

## Funcionamiento

El workflow [pages.yml](../../.github/workflows/pages.yml) se ejecuta al modificar las carpetas de las versiones, el empaquetador o el propio workflow en `main`. También permite ejecución manual desde GitHub Actions. GitHub Pages debe tener **GitHub Actions** como fuente de publicación; el repositorio ya utilizaba esta configuración.

El script [build-pages.py](../scripts/build-pages.py) copia cada versión a su propio directorio dentro de `.pages-site/`, sin modificar sus HTML, estilos, JavaScript ni recursos. Comprueba que los enlaces locales y los recursos referenciados por HTML y CSS existan en el paquete. Incluye las páginas españolas e inglesas de V2 y V3. Publica los medios necesarios de `docs/media`, pero excluye informes, plantillas de participantes, scripts de mantenimiento y demás documentación.

Cada despliegue de Pages sustituye el paquete publicado completo. Por eso el workflow **siempre empaqueta todas las versiones disponibles**, aunque solo haya cambiado una. Las fuentes de V1 y V2 se conservan en sus carpetas; para añadir V3 se crea una carpeta nueva. No renombrar V2 como V3 ni borrar las versiones previas. Las URLs son estables, pero modificar los archivos de una versión también actualizará lo que se ve en su URL: conservar una referencia de commit por tanda y evitar cambios durante las sesiones.

El workflow anterior todavía apuntaba a `PaginaPersonal` en la raíz del repositorio. La nueva configuración utiliza las rutas actuales bajo `Web Personal`.

## Comprobar localmente

Desde `Web Personal`, con Python 3.12 o posterior:

```powershell
python scripts/build-pages.py
python -m http.server 8000 --bind 127.0.0.1 --directory .pages-site
```

Abrir <http://127.0.0.1:8000/>, <http://127.0.0.1:8000/v1/>, <http://127.0.0.1:8000/v2/> y <http://127.0.0.1:8000/v3/>. Detener con `Ctrl+C`. `.pages-site/` es un directorio generado e ignorado por Git; no se mantiene una segunda copia de las webs en el repositorio.

## Versión final V3

V3 contiene 18 páginas y mantiene los destinos de las tres tareas realizadas sobre V2. El empaquetador añade su enlace a la portada y publica las tres versiones. Análisis, validación y evidencias en [PaginaPersonal-V3/README.md](../PaginaPersonal-V3/README.md).

## Registro de la tanda 2

Las tres sesiones se realizaron en V2 con **Microsoft Clarity**, proyecto `zg4r78nft3`, que requiere enlace de prueba y aceptación explícita. Clarity registra interacciones, no seguimiento ocular. V3 no incluye esa integración ni mezcla sus visitas con los resultados de la tanda.

V1 y V2 comparten la clave de tema `adweb-theme`; V3 usa `adweb-v3-theme`. Cambiar de versión conserva las preferencias correspondientes sin alterar el estado del estudio anterior.
