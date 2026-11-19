"""Роздача media. SVG відкривається як файл, не як сторінка."""

from pathlib import PurePosixPath

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.views.static import serve

_SVG_SUFFIXES = {'.svg', '.svgz'}


def media_serve(request: HttpRequest, path: str) -> HttpResponse:
    response = serve(request, path, document_root=str(settings.MEDIA_ROOT))
    suffix = PurePosixPath(path).suffix.lower()
    if suffix not in _SVG_SUFFIXES:
        return response
    filename = _download_name(path)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response['X-Content-Type-Options'] = 'nosniff'
    response['Content-Security-Policy'] = "default-src 'none'; sandbox"
    return response


def _download_name(path: str) -> str:
    name = PurePosixPath(path).name or 'file.svg'
    cleaned = ''.join(ch for ch in name if ch.isprintable() and ch not in '"\\')
    return cleaned or 'file.svg'
