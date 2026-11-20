"""Derivados WebP de la fotografía existente. Requiere Pillow solo al regenerarlos."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'img/index/ignasi.png'
with Image.open(source) as original:
    image = original.convert('RGB')
    for width in (400, 640, 817):
        size = (width, round(image.height * width / image.width))
        target = ROOT / f'img/index/ignasi-{width}.webp'
        image.resize(size, Image.Resampling.LANCZOS).save(target, 'WEBP', quality=82, method=6)
        print(f'{target.name}: {target.stat().st_size} bytes (original {source.stat().st_size}).')
