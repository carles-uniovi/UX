"""Comprueba estructura, rutas, anclas, traducciones, contraste y servicio HTTP.

No sustituye a un validador HTML/CSS ni a las pruebas reales de accesibilidad.
Ejecutar desde cualquier carpeta: python scripts/check.py
"""
from collections import Counter
from functools import partial
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import urlsplit, unquote, quote
from urllib.request import urlopen
import json
import re

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.links, self.labelled, self.images = path, [], [], [], []
        self.headings, self.fields, self.labels, self.tags = [], [], [], []
        self.media_links, self.footer_links, self.dialogs = [], [], []
        self.anchors = []
        self.header_forms = 0
        self.part_languages = []
        self.lang, self.stack = '', []
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if tag == 'html': self.lang = attrs.get('lang')
        elif attrs.get('lang'): self.part_languages.append(attrs['lang'])
        if attrs.get('id'): self.ids.append(attrs['id'])
        for name in ('href', 'src', 'action'):
            if attrs.get(name): self.links.append(attrs[name])
        for name in ('aria-labelledby', 'aria-describedby', 'aria-controls'):
            self.labelled.extend(attrs.get(name, '').split())
        if tag == 'img': self.images.append(attrs)
        if re.fullmatch('h[1-6]', tag): self.headings.append(int(tag[1]))
        if tag == 'input': self.fields.append(attrs)
        if tag == 'label': self.labels.append(attrs.get('for'))
        if tag == 'a': self.anchors.append(attrs)
        if tag == 'form' and 'header' in self.stack: self.header_forms += 1
        if tag == 'a' and 'footer' in self.stack: self.footer_links.append(attrs.get('href'))
        if tag == 'a' and 'media-trigger' in attrs.get('class', '').split(): self.media_links.append(attrs)
        if tag == 'dialog': self.dialogs.append(attrs)
        if tag in ('audio', 'video'):
            assert 'autoplay' not in attrs, f'{self.path}: reproducción automática'
            assert attrs.get('preload') == 'none', f'{self.path}: precarga multimedia'
            assert 'controls' in attrs, f'{self.path}: faltan controles'
        if tag not in ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'):
            self.stack.append(tag)

    def handle_endtag(self, tag):
        assert self.stack and self.stack[-1] == tag, f'{self.path}: cierre HTML inesperado: {tag}'
        self.stack.pop()


def contrast(first, second):
    def luminance(color):
        if len(color) == 4: color = '#' + ''.join(c * 2 for c in color[1:])
        channels = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
        channels = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in channels]
        return sum(a*b for a, b in zip(channels, (.2126, .7152, .0722)))
    light, dark = sorted([luminance(first), luminance(second)], reverse=True)
    return (light + .05) / (dark + .05)


def main():
    files = sorted(ROOT.glob('*.html')) + sorted((ROOT / 'en').glob('*.html'))
    assert len(files) == 18
    pages = {path.resolve(): Page(path) for path in files}
    links_checked = 0
    for path, page in pages.items():
        relative = path.relative_to(ROOT)
        assert page.lang == ('en' if relative.parts[0] == 'en' else 'es'), relative
        assert page.tags.count('main') == 1 and page.headings.count(1) == 1, relative
        assert not page.stack, f'{relative}: etiquetas HTML sin cerrar'
        assert all(after <= before + 1 for before, after in zip(page.headings, page.headings[1:])), f'{relative}: salto de nivel de encabezado'
        assert not [key for key, count in Counter(page.ids).items() if count > 1], relative
        assert set(page.labelled) <= set(page.ids), f'{relative}: referencias ARIA inexistentes'
        assert all('alt' in img and 'width' in img and 'height' in img for img in page.images), relative
        assert all(field.get('id') in page.labels for field in page.fields), relative
        assert page.header_forms == 0, f'{relative}: formulario redundante en cabecera'
        assert page.footer_links == ['ayuda.html', 'mapa.html', 'lectura.html'], f'{relative}: navegación del pie'
        for anchor in page.anchors:
            href = anchor.get('href', '')
            if href.startswith(('https://', 'http://')):
                assert anchor.get('target') == '_blank', f'{relative}: enlace externo en la misma pestaña'
                assert {'noopener', 'noreferrer'} <= set(anchor.get('rel', '').split()), relative
            elif href and 'media-trigger' not in anchor.get('class', ''):
                assert anchor.get('target') != '_blank', f'{relative}: navegación interna en otra pestaña'
        if path.name == 'intereses.html':
            assert len(page.media_links) == 5 and len(page.dialogs) == 1, relative
            assert page.dialogs[0].get('id') == 'media-player'
            assert all(link.get('data-media-type') in ('audio', 'youtube') and link.get('data-media-title') for link in page.media_links)
            youtube_links = [link for link in page.media_links if link['data-media-type'] == 'youtube']
            assert len(youtube_links) == 2
            for link in youtube_links:
                assert re.fullmatch(r'[A-Za-z0-9_-]{11}', link.get('data-youtube-id', ''))
                assert link['href'] == 'https://www.youtube.com/watch?v=' + link['data-youtube-id']
            assert not set(page.tags).intersection(('audio', 'video')), f'{relative}: reproductores dentro de tarjetas'
        if path.name == 'lectura.html':
            assert not page.images, f'{relative}: imágenes en versión de lectura'
            assert 'ca' in page.part_languages, f'{relative}: se ha perdido el idioma del saludo valenciano'
            reading_html = path.read_text(encoding='utf-8')
            assert 'Carles Valladares García' in reading_html
            assert reading_html.count('class="reading-contact"') == 5, f'{relative}: contactos sin separar'
            assert ': <strong>carlesvallgar@gmail.com' in reading_html
            assert set(f'leer-{name}' for name in ('index', 'trayectoria', 'hobbies', 'intereses', 'contacto')) <= set(page.ids)
        for link in page.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc: continue
            destination = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            assert destination.is_relative_to(ROOT), f'{relative}: ruta fuera de V3: {link}'
            assert destination.is_file(), f'{relative}: falta {link}'
            if parsed.fragment and destination in pages:
                assert unquote(parsed.fragment) in pages[destination].ids, f'{relative}: ancla inexistente {link}'
            links_checked += 1
    source = (ROOT / 'js/search-index.js').read_text(encoding='utf-8')
    indexes = json.loads(source.split('window.SEARCH_INDEX = ', 1)[1].strip().removesuffix(';'))
    for lang, entries in indexes.items():
        assert len(entries) == 35 and len({entry['url'] for entry in entries}) == len(entries)
        for entry in entries:
            parsed = urlsplit(entry['url'])
            destination = (ROOT / ('en' if lang == 'en' else '') / parsed.path).resolve()
            assert parsed.fragment in pages[destination].ids
            assert entry['title'] and entry['text'] and entry['category']
    css = (ROOT / 'css/styles.css').read_text(encoding='utf-8')
    palettes = re.findall(r':root(?:\[data-theme="dark"\])?\s*\{([^}]+)\}', css)
    ratios = []
    for name, block in zip(('claro', 'oscuro'), palettes):
        palette = dict(re.findall(r'--([a-z-]+):\s*(#[\da-fA-F]{3,6});', block))
        for foreground in ('text', 'muted', 'accent'):
            for background in ('bg', 'surface', 'soft'):
                ratio = contrast(palette[foreground], palette[background])
                assert ratio >= 7, f'Contraste {name} {foreground}/{background}: {ratio:.2f}'
                ratios.append(ratio)
        assert contrast(palette['on-accent'], palette['accent']) >= 7
        for background in ('bg', 'surface'):
            assert contrast(palette['control'], palette[background]) >= 3

    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, *args): pass

    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        for path in files:
            url = f'http://127.0.0.1:{server.server_port}/' + quote(path.relative_to(ROOT).as_posix())
            with urlopen(url, timeout=5) as response:
                assert response.status == 200 and 'text/html' in response.headers['Content-Type']
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
    print(f'OK: {len(files)} páginas; {links_checked} rutas/anclas; {sum(map(len, indexes.values()))} entradas; 18 respuestas HTTP 200.')
    print(f'OK: contraste mínimo del texto de la paleta: {min(ratios):.2f}:1; controles >= 3:1.')
    print('La estructura y el contraste calculado no equivalen a conformidad WCAG completa. Auditoría propia en docs/verificacion-v3.md.')


if __name__ == '__main__':
    main()
