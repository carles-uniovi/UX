# Página personal · V3 final

Versión final del sitio de Carles Valladares García (UO319242), realizada el 20 de noviembre de 2026 a partir de V2 y de las tres pruebas de usabilidad de la tanda 2.

**Web:** <https://carles-uniovi.github.io/UX/v3/>. Se conservan V1 y V2 en sus rutas independientes. También se puede abrir [index.html](index.html) directamente; los tráileres incrustados necesitan conexión y servir la carpeta por HTTP.

Las tres tareas se completaron sin dificultades comunicadas. Se mantiene la estructura y el contenido; se mejoran la identificación de Buscar y Menú, la confirmación al copiar el correo, la recuperación de búsquedas, el foco, la carga móvil y los enlaces entre idiomas. Son mejoras derivadas de una revisión técnica y preventiva, sin atribuir a los participantes problemas que no manifestaron. V3 no incorpora el registro del estudio de Clarity.

## Comprobar y mantener

No hay dependencias de ejecución ni compilación obligatoria. Desde esta carpeta:

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

Abrir <http://127.0.0.1:8000/> y detener con `Ctrl+C`. Para modificar contenido y traducciones, editar `scripts/build.py`; estilos en `css/styles.css`, interacciones en `js/`. Después:

```powershell
python scripts/build.py
python scripts/check.py
node scripts/test-search.cjs
node scripts/test-ui.cjs
```

El generador usa Python estándar y entrega 18 HTML y 70 entradas de búsqueda. Conserva los recursos existentes. Las imágenes WebP de portada ya están incluidas; únicamente para regenerarlas hace falta Pillow y ejecutar `python scripts/optimize-images.py`.

## Comprobaciones de navegador y validadores

Se usaron Chrome, Playwright 1.62.1, axe-core 4.14.1, Lighthouse 13.6.0, Nu Html Checker 26.11.19 y css-tree 3.2.1. Son herramientas de desarrollo, excluidas de la publicación. Para repetirlas, con Node.js moderno, Java 17+ y Chrome instalado:

```powershell
$env:UX_QA_ROOT = Join-Path $env:TEMP 'ux-v3-qa'
npm install --prefix $env:UX_QA_ROOT playwright@1.62.1 axe-core@4.14.1 lighthouse@13.6.0 vnu-jar@26.11.19 css-tree@3.2.1
$env:UX_PLAYWRIGHT = Join-Path $env:UX_QA_ROOT 'node_modules/playwright'
# UX_CHROME y UX_JAVA permiten indicar las rutas locales de Chrome y Java.
node scripts/test-search-browser.cjs
node scripts/test-final-browser.cjs
node scripts/validate-local.cjs
node scripts/audit-lighthouse.cjs
```

Las pruebas locales arrancan y cierran sus propios servidores y no registran sesiones de participantes. La comprobación multimedia automatizada verifica controles y cierre. La evaluación externa con TAW, AChecker y WAVE se realiza sobre las URL públicas y se documenta por separado, junto con la revisión manual de contenido.

Las tres herramientas devuelven cero errores automáticos en las 18 páginas; WAVE también devuelve cero errores de contraste. Se documentan sus advertencias y los 30 criterios no verificados de TAW. Las alternativas multimedia pendientes impiden declarar conformidad WCAG AAA.

## Documentación

- [Análisis y mejoras aplicadas](docs/mejoras-v3.md).
- [Verificación y alcance de los resultados](docs/verificacion-v3.md).
- [Revisión de los 21 criterios de la métrica](docs/autoevaluacion-v3.md).
- [Estudio de accesibilidad con TAW, AChecker y WAVE](docs/accesibilidad-v3.md).
- [Informe de accesibilidad en PDF](output/pdf/UO319242-Informe-accesibilidad-web-personal-V3.pdf).
- [Funcionamiento y pruebas del buscador](docs/buscador-v3.md).
- [Resultados técnicos y capturas](docs/auditoria-v3/resultado-tecnico.json).

La publicación utiliza el workflow de GitHub Pages existente y el empaquetador `../scripts/build-pages.py`, que publica V1, V2 y V3 e incluye solo los medios necesarios de `docs/media`, sin los informes ni los scripts. Los recursos gráficos y musicales conservan los titulares y la procedencia de V1. La foto de portada muestra un gato y se describe como tal.
