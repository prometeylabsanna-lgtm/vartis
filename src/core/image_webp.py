"""Конвертація завантажених зображень у WebP (без ресайзу)."""

from __future__ import annotations

import logging
from io import BytesIO
from pathlib import PurePosixPath

from django.core.files.base import ContentFile
from PIL import Image, UnidentifiedImageError

logger = logging.getLogger(__name__)

WEBP_QUALITY = 88
_SKIP_EXT = {'.svg', '.svgz'}
_ALREADY_WEBP = {'.webp'}


def _is_animated_gif(img: Image.Image) -> bool:
    if img.format != 'GIF':
        return False
    try:
        return bool(getattr(img, 'is_animated', False) and img.n_frames > 1)
    except (AttributeError, ValueError):
        return False


def convert_upload_to_webp(uploaded_file, *, quality: int = WEBP_QUALITY) -> ContentFile | None:
    """
    Повертає ContentFile (.webp) або None, якщо конвертація не потрібна/неможлива.
    Не чіпає: SVG, уже WebP, анімований GIF.
    """
    if not uploaded_file:
        return None

    name = getattr(uploaded_file, 'name', '') or ''
    ext = PurePosixPath(name).suffix.lower()
    if ext in _SKIP_EXT or ext in _ALREADY_WEBP:
        return None

    raw = getattr(uploaded_file, 'file', uploaded_file)
    try:
        if hasattr(raw, 'seek'):
            raw.seek(0)
        img = Image.open(raw)
        img.load()
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        logger.warning('webp skip (cannot open %s): %s', name, exc)
        try:
            if hasattr(raw, 'seek'):
                raw.seek(0)
        except Exception:
            pass
        return None

    if _is_animated_gif(img):
        try:
            if hasattr(raw, 'seek'):
                raw.seek(0)
        except Exception:
            pass
        return None

    if (img.format or '').upper() == 'WEBP':
        try:
            if hasattr(raw, 'seek'):
                raw.seek(0)
        except Exception:
            pass
        return None

    if img.mode in ('RGBA', 'LA'):
        converted = img.convert('RGBA')
    elif img.mode == 'P':
        converted = img.convert('RGBA') if 'transparency' in img.info else img.convert('RGB')
    elif img.mode != 'RGB':
        converted = img.convert('RGB')
    else:
        converted = img

    buf = BytesIO()
    converted.save(buf, format='WEBP', quality=quality, method=6)
    buf.seek(0)

    base = PurePosixPath(name).name
    new_name = str(PurePosixPath(base).with_suffix('.webp'))
    return ContentFile(buf.read(), name=new_name)
