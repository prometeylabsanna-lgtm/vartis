"""Context processor: CMS-блоки з кешем."""

from __future__ import annotations

from django.core.cache import cache

from src.core.models import SiteBlock
from src.core.models_cms import SITE_BLOCKS_CACHE_KEY


def get_site_blocks() -> dict[str, SiteBlock]:
    cached = cache.get(SITE_BLOCKS_CACHE_KEY)
    if cached is not None:
        return cached
    data = {b.cache_key: b for b in SiteBlock.objects.filter(is_active=True)}
    cache.set(SITE_BLOCKS_CACHE_KEY, data, 300)
    return data


def site_cms(request):
    try:
        site_blocks = get_site_blocks()
    except Exception:
        site_blocks = {}
    return {"site_blocks": site_blocks}
