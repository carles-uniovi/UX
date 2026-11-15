"""Envía HTML y CSS a los validadores públicos W3C y conserva sus respuestas.

Se ejecuta expresamente para una auditoría, no al generar el sitio.
"""
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import json
import time
import sys
import uuid
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'docs/auditoria'
OUTPUT.mkdir(exist_ok=True)
results = []
cache = {}
if '--changed-only' in sys.argv and (OUTPUT / 'w3c-html.json').exists():
    cache = {entry['file']: entry for entry in json.loads((OUTPUT / 'w3c-html.json').read_text(encoding='utf-8')) if 'response' in entry}
pages = [] if '--css-only' in sys.argv else sorted(ROOT.glob('*.html')) + sorted((ROOT / 'en').glob('*.html'))
for page in pages:
    data = page.read_bytes()
    entry = {'file': page.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(data).hexdigest()}
    if cache.get(entry['file'], {}).get('sha256') == entry['sha256']:
        results.append(cache[entry['file']])
        continue
    try:
        request = Request('https://validator.w3.org/nu/?out=json', data=data, headers={'Content-Type': 'text/html; charset=utf-8', 'User-Agent': 'PersonalWebsiteV2-Audit/1.0'})
        with urlopen(request, timeout=20) as response:
            entry['response'] = json.load(response)
        messages = entry['response'].get('messages', [])
        print(entry['file'], [(m.get('type'), m.get('subType'), m.get('message')) for m in messages], flush=True)
    except Exception as error:
        entry['unavailable'] = f'{type(error).__name__}: {error}'
        print('HTML validator unavailable:', entry['unavailable'], flush=True)
        results.append(entry)
        break
    results.append(entry)
    time.sleep(1)
if results:
    (OUTPUT / 'w3c-html.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
if '--html-only' in sys.argv:
    sys.exit(0)
css = (ROOT / 'css/styles.css').read_bytes()
entry = {'file': 'css/styles.css', 'sha256': hashlib.sha256(css).hexdigest()}
try:
    # La entrada directa form-urlencoded devuelve "Reader used" en el servicio
    # actual. La subida multipart usa su formulario oficial de validación de archivos.
    boundary = 'WebsiteAudit' + uuid.uuid4().hex
    parts = []
    for name, value in {'profile': 'css3', 'warning': '2', 'output': 'soap12', 'lang': 'en', 'usermedium': 'all'}.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="styles.css"\r\nContent-Type: text/css\r\n\r\n'.encode() + css + b'\r\n')
    parts.append(f'--{boundary}--\r\n'.encode())
    request = Request('https://jigsaw.w3.org/css-validator/validator', data=b''.join(parts), headers={'Content-Type': 'multipart/form-data; boundary=' + boundary, 'User-Agent': 'PersonalWebsiteV2-Audit/1.0'})
    with urlopen(request, timeout=20) as response:
        xml = response.read().decode('utf-8')
    (OUTPUT / 'w3c-css.xml').write_text(xml, encoding='utf-8')
    entry['response_file'] = 'w3c-css.xml'
    print('CSS validator: response saved.', flush=True)
except Exception as error:
    entry['unavailable'] = f'{type(error).__name__}: {error}'
    if isinstance(error, HTTPError):
        (OUTPUT / 'w3c-css-error.txt').write_text(error.read().decode('utf-8', errors='replace'), encoding='utf-8')
    print('CSS validator unavailable:', entry['unavailable'], flush=True)
(OUTPUT / 'w3c-css.json').write_text(json.dumps(entry, ensure_ascii=False, indent=2), encoding='utf-8')
