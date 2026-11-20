"""Resume evidencias reales de TAW, AChecker y WAVE, sin ejecutar ni simular motores.

Lee las capturas de texto guardadas desde las interfaces oficiales. Conserva
criterios, recuentos, fecha y archivo de origen para revisar cada afirmación.
"""
from collections import Counter
from pathlib import Path
import csv
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/accesibilidad'


def metadata(path):
    text = path.read_text(encoding='utf-8')
    url = re.search(r'^URL: (.+)$', text, re.M).group(1)
    date = re.search(r'^Captured UTC: (.+)$', text, re.M).group(1)
    page, tool = path.stem.rsplit('-', 1)
    return text, dict(page=page, tool=tool, phase=path.parent.name,
                      url=url, date=date, evidence=path.relative_to(ROOT).as_posix(),
                      evidence_sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def taw(text):
    starts = list(re.finditer(r'^(\s*)- row "(\d\.\d\.\d[^\n]*)":\s*$', text, re.M))
    rows = []
    for match in starts:
        indent = len(match.group(1).split('\n')[-1])
        tail = text[match.end():]
        next_row = re.search(r'^' + ' ' * indent + r'- row ', tail, re.M)
        block = tail[:next_row.start()] if next_row else tail
        cells = re.findall(r'^' + ' ' * (indent + 2) + r'- cell(?: "(.*?)")?:?\s*$', block, re.M)
        if len(cells) < 6:
            raise ValueError('No se reconocen las seis columnas TAW: ' + match.group(2))
        cells = cells[:6]
        rows.append(dict(criterion=cells[0].removesuffix(' ayuda'), level=cells[1], result=cells[2],
                         errors=int(cells[3] or 0), warnings=int(cells[4] or 0), unverified=int(cells[5] or 0)))
    if len(rows) < 50 or 'heading "Resumen"' not in text:
        raise ValueError('TAW no contiene un análisis completo; no se interpreta como cero errores')
    return dict(tool='TAW', standard='WCAG 2.1 AAA', rows=rows,
                **{k: sum(r[k] for r in rows) for k in ('errors', 'warnings', 'unverified')})


def achecker(text):
    if not re.search(r'NO ERRORS|No known problems', text, re.I):
        raise ValueError('AChecker requiere estudiar el bloque de errores, sin deducir cero')
    warnings = text.split('\nWARNINGS\n')[-1]
    lines = [line.strip() for line in warnings.splitlines() if line.strip()]
    titles = [lines[i - 1] for i, line in enumerate(lines) if line == 'Line number']
    return dict(tool='AChecker', standard='WCAG 2.0 AAA Markup', errors=0,
                warnings=len(titles), warningTypes=dict(Counter(titles)))


def wave(text):
    counts = []
    for label in ('Errors', 'Contrast Errors', 'Alerts'):
        match = re.search(r'- text: "?(\d+)"?\s*\n\s*- text: ' + re.escape(label) + r'\s*$', text, re.M)
        if not match:
            raise ValueError('WAVE no contiene el recuento ' + label)
        counts.append(int(match.group(1)))
    types = re.findall(r'- heading "(\d+ (?:Redundant[^"\n]*|Audio/Video|YouTube video|Noscript element)) Reference" \[level=4\]', text)
    return dict(tool='WAVE', standard='Reglas WAVE, estilos activos', errors=counts[0],
                contrastErrors=counts[1], alerts=counts[2], alertTypes=types)


def main():
    results = []
    for phase in ('inicial', 'final'):
        for file in sorted((EVIDENCE / phase).glob('*.txt')):
            if not re.search(r'-(taw|achecker|wave)\.txt$', file.name):
                continue
            text, entry = metadata(file)
            tool = entry['tool']
            entry.update({'taw': taw, 'achecker': achecker, 'wave': wave}[tool](text))
            results.append(entry)
    (EVIDENCE / 'resultados.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    fields = ['phase', 'page', 'tool', 'standard', 'errors', 'contrastErrors', 'warnings', 'alerts', 'unverified', 'date', 'url', 'evidence']
    with (EVIDENCE / 'resultados.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)
    for phase in ('inicial', 'final'):
        selected = [r for r in results if r['phase'] == phase]
        if selected:
            print(phase, len(selected), 'análisis; errores por herramienta:',
                  {t: sum(r['errors'] + r.get('contrastErrors', 0) for r in selected if r['tool'] == t) for t in ('TAW', 'AChecker', 'WAVE')})


if __name__ == '__main__':
    main()
