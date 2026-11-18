"""Стисла картинка 1200×630 для og:image, щоб месенджери не відкидали важкий PNG."""

from __future__ import annotations

import logging
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from src.core.seo import media_or_static_absolute

logger = logging.getLogger(__name__)

OG_WIDTH = 1200
OG_HEIGHT = 630
OG_MAX_BYTES = 300_000


def _cover(img: Image.Image) -> Image.Image:
    img = img.convert('RGB')
    scale = max(OG_WIDTH / img.width, OG_HEIGHT / img.height)
    resized = img.resize((max(1, round(img.width * scale)), max(1, round(img.height * scale))), Image.Resampling.LANCZOS)
    left = max(0, (resized.width - OG_WIDTH) // 2)
    top = max(0, (resized.height - OG_HEIGHT) // 2)
    return resized.crop((left, top, left + OG_WIDTH, top + OG_HEIGHT))


def ensure_og_jpeg(source: Path) -> Path | None:
    dest = source.with_name(f'{source.stem}-og.jpg')
    try:
        fresh = dest.exists() and dest.stat().st_mtime >= source.stat().st_mtime and dest.stat().st_size <= OG_MAX_BYTES
    except OSError:
        return None
    if fresh:
        return dest
    try:
        with Image.open(source) as img:
            canvas = _cover(img)
    except (UnidentifiedImageError, OSError, ValueError):
        logger.exception('og image failed for %s', source)
        return None
    for quality in (82, 72, 62, 52, 42):
        canvas.save(dest, 'JPEG', quality=quality, optimize=True, progressive=True)
        if dest.stat().st_size <= OG_MAX_BYTES:
            return dest
    return dest


def og_image_from_field(request, image_field) -> str:
    if not image_field:
        return ''
    try:
        source = Path(image_field.path)
    except (NotImplementedError, ValueError, OSError):
        return media_or_static_absolute(request, getattr(image_field, 'url', '') or '')
    if not source.exists():
        return media_or_static_absolute(request, image_field.url)
    dest = ensure_og_jpeg(source)
    if dest is None:
        return media_or_static_absolute(request, image_field.url)
    folder = image_field.url.rsplit('/', 1)[0]
    return media_or_static_absolute(request, f'{folder}/{dest.name}')
