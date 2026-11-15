"""Empaqueta las versiones completas en rutas independientes para GitHub Pages.

Ejecutar desde cualquier carpeta: python "Web Personal/scripts/build-pages.py".
Solo publica HTML y recursos del sitio, no informes ni fichas de participantes.
"""
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from shutil import copy2
from urllib.parse import unquote, urlsplit
import re


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '.pages-site'
VERSIONS = [('v1', 'PaginaPersonal'), ('v2', 'PaginaPersonal-V2'), ('v3', 'PaginaPersonal-V3')]
ASSET_DIRS = ('css', 'js', 'img', 'docs/media')
ASSET_TYPES = {'.css', '.js', '.svg', '.png', '.jpg', '.jpeg', '.webp', '.avif', '.gif',
               '.ico', '.mp3', '.mp4', '.webm', '.ogg', '.wav', '.woff', '.woff2', '.ttf'}


class References(HTMLParser):
    """Incluye las fuentes multimedia que el JavaScript carga al abrir un diálogo."""
    def __init__(self, content):
        super().__init__()
        self.urls = []
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ('href', 'src', 'data-media-src') and value:
                self.urls.append(value)


def check_reference(page, url, output):
    parts = urlsplit(url)
    if parts.scheme or parts.netloc or not parts.path:
        return
    # Las rutas de las webs deben seguir funcionando bajo /UX/vN/.
    if parts.path.startswith('/'):
        raise ValueError(f'Ruta absoluta incompatible con subdirectorios: {page}: {url}')
    target = (page.parent / unquote(parts.path)).resolve()
    if not target.is_relative_to(output.resolve()) or not target.is_file():
        raise ValueError(f'Recurso local ausente o fuera del paquete: {page}: {url}')


def build():
    for version, source_name in VERSIONS[:2]:
        if not (ROOT / source_name / 'index.html').is_file():
            raise ValueError(f'Falta la versión obligatoria {version}: {source_name}')

    # No se elimina recursivamente ninguna carpeta. Se rechaza una salida con
    # enlaces y se borran solo los archivos generados dentro del destino fijo.
    if OUTPUT.is_symlink() or OUTPUT.is_junction():
        raise ValueError(f'El destino no puede ser un enlace: {OUTPUT}')
    OUTPUT.mkdir(exist_ok=True)
    old_paths = list(OUTPUT.rglob('*'))
    if any(p.is_symlink() or p.is_junction() for p in old_paths):
        raise ValueError('El paquete anterior contiene enlaces; no se modifica')
    for path in old_paths:
        if not path.resolve().is_relative_to(OUTPUT.resolve()):
            raise ValueError(f'Ruta fuera del destino: {path}')
    for path in old_paths:
        if path.is_file():
            path.unlink()
    for path in sorted(old_paths, key=lambda p: len(p.parts), reverse=True):
        if path.is_dir():
            path.rmdir()

    available = []
    for version, source_name in VERSIONS:
        source = ROOT / source_name
        if not (source / 'index.html').is_file():
            continue
        available.append(version)
        files = list(source.glob('*.html')) + list((source / 'en').glob('*.html'))
        for folder in ASSET_DIRS:
            files.extend(p for p in (source / folder).rglob('*')
                         if p.is_file() and p.suffix.lower() in ASSET_TYPES)
        for path in files:
            if path.is_symlink() or not path.resolve().is_relative_to(source.resolve()):
                raise ValueError(f'Recurso fuera de la versión: {path}')
            destination = OUTPUT / version / path.relative_to(source)
            destination.parent.mkdir(parents=True, exist_ok=True)
            copy2(path, destination)

    links = '\n'.join(
        f'<li><a href="{version}/">Versión {escape(version[1:])}</a></li>'
        for version in available
    )
    future = '' if 'v3' in available else '<p>La versión 3 se publicará después de la segunda evaluación.</p>'
    (OUTPUT / 'index.html').write_text(f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Versiones de la web personal · Carles Valladares</title>
  <style>
    :root {{ color-scheme: light; font-family: system-ui, sans-serif; color: #252036; background: #f6f3fb; }}
    body {{ max-width: 44rem; margin: 10vh auto; padding: 1.5rem; line-height: 1.6; }}
    h1 {{ line-height: 1.2; }}
    ul {{ padding: 0; list-style: none; display: grid; gap: 1rem; }}
    a {{ display: block; padding: 1rem 1.5rem; background: #fff; border: 2px solid #624297; border-radius: .75rem; color: #4e287b; font-weight: 700; }}
    a:hover {{ background: #eee6fa; }}
    a:focus-visible {{ outline: 3px solid #252036; outline-offset: 4px; }}
  </style>
</head>
<body>
  <main>
    <p>Experiencia de Usuario · Carles Valladares García</p>
    <h1>Versiones de la web personal</h1>
    <p>Selecciona la versión que quieres consultar.</p>
    <nav aria-label="Versiones disponibles"><ul>{links}</ul></nav>
    {future}
  </main>
</body>
</html>
''', encoding='utf-8')
    (OUTPUT / '.nojekyll').touch()
    # Revisar el paquete final, no solo las fuentes: detecta recursos omitidos.
    pages = list(OUTPUT.rglob('*.html'))
    for page in pages:
        for url in References(page.read_text(encoding='utf-8')).urls:
            if url.endswith('/') and not urlsplit(url).scheme:
                url += 'index.html'
            check_reference(page, url, OUTPUT)
    for sheet in OUTPUT.rglob('*.css'):
        for url in re.findall(r'url\(\s*[\'"]?([^\)\'"\s]+)', sheet.read_text(encoding='utf-8')):
            check_reference(sheet, url, OUTPUT)
    print(f'Paquete: {OUTPUT}')
    print(f'Versiones: {", ".join(available)} · {len(pages)} HTML · referencias locales verificadas')


if __name__ == '__main__':
    build()
