"""Ліміт POST заявки: 5 запитів за 10 хвилин з однієї IP."""

from django.core.cache import cache

from src.core.client_ip import client_ip

WINDOW_SECONDS = 10 * 60
MAX_SUBMITS = 5


def lead_submit_limited(request) -> bool:
    key = f'leads:submit:{client_ip(request)}'
    if cache.add(key, 1, timeout=WINDOW_SECONDS):
        return False
    try:
        count = cache.incr(key)
    except ValueError:
        cache.set(key, 1, timeout=WINDOW_SECONDS)
        return False
    return count > MAX_SUBMITS
