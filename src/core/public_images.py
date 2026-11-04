"""Публічні URL картинок: design/seed → static (надійно на Vercel), custom → media."""

from __future__ import annotations

from django.templatetags.static import static

# basename (нижній регістр) → шлях у static/
SEED_BASENAME_TO_STATIC: dict[str, str] = {
    'hero.png': 'images/hero.webp',
    'hero.webp': 'images/hero.webp',
    'about-bg.png': 'images/about-bg.webp',
    'about-bg.webp': 'images/about-bg.webp',
    'dir-1.png': 'images/services/dir-1.webp',
    'dir-2.png': 'images/services/dir-2.webp',
    'dir-3.png': 'images/services/dir-3.webp',
    'dir-4.png': 'images/services/dir-4.webp',
    'dash.jpg': 'images/blog/dash.webp',
    'dash.webp': 'images/blog/dash.webp',
    'lock.jpg': 'images/blog/lock.webp',
    'lock.webp': 'images/blog/lock.webp',
    'sign.jpg': 'images/blog/sign.webp',
    'sign.webp': 'images/blog/sign.webp',
    'laptop.jpg': 'images/blog/laptop.webp',
    'laptop.webp': 'images/blog/laptop.webp',
    'law.jpg': 'images/blog/law.webp',
    'law.webp': 'images/blog/law.webp',
    'magn.jpg': 'images/blog/magn.webp',
    'magn.webp': 'images/blog/magn.webp',
    'meet.jpg': 'images/blog/meet.webp',
    'meet.webp': 'images/blog/meet.webp',
    'hand.jpg': 'images/blog/hand.webp',
    'hand.webp': 'images/blog/hand.webp',
    'fin.jpg': 'images/blog/fin.webp',
    'fin.webp': 'images/blog/fin.webp',
    'cyber.jpg': 'images/blog/cyber.webp',
    'cyber.webp': 'images/blog/cyber.webp',
    'city.jpg': 'images/blog/city.webp',
    'city.webp': 'images/blog/city.webp',
    'charts.jpg': 'images/blog/charts.webp',
    'charts.webp': 'images/blog/charts.webp',
    'article.jpg': 'images/blog/article.webp',
    'article.png': 'images/blog/article.webp',
    'article.webp': 'images/blog/article.webp',
    'abroskin.jpg': 'images/team/abroskin.webp',
    'abroskin.webp': 'images/team/abroskin.webp',
    'tikhonov.jpg': 'images/team/tikhonov.webp',
    'tikhonov.webp': 'images/team/tikhonov.webp',
}


def _basename(name: str) -> str:
    return (name or '').rsplit('/', 1)[-1].lower()


def _stem(name: str) -> str:
    base = _basename(name)
    return base.rsplit('.', 1)[0] if base else ''


def seed_static_path(field_name: str | None) -> str | None:
    """Якщо це design/seed-файл — шлях у static, інакше None."""
    if not field_name:
        return None
    base = _basename(field_name)
    if base in SEED_BASENAME_TO_STATIC:
        return SEED_BASENAME_TO_STATIC[base]
    # Django інколи додає суфікс: hero_AbCdEf.png
    stem = _stem(field_name)
    for seed_name, static_path in SEED_BASENAME_TO_STATIC.items():
        seed_stem = seed_name.rsplit('.', 1)[0]
        if stem == seed_stem or stem.startswith(f'{seed_stem}_'):
            return static_path
    return None


def public_image_url(field, fallback_static: str | None = None) -> str:
    """
    URL для <img>/CSS.
    1) seed/design basename → /static/...
    2) кастомний upload, якщо файл є в storage → media url
    3) fallback_static
    """
    name = getattr(field, 'name', None) if field else None
    mapped = seed_static_path(name)
    if mapped:
        return static(mapped)

    if field and name:
        try:
            if field.storage.exists(name):
                return field.url
        except (ValueError, OSError):
            pass

    if fallback_static:
        return static(fallback_static)
    return ''
