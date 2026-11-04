"""X-Robots-Tag для staging / preview середовищ."""

from src.core.seo import seo_indexing_allowed


class SeoRobotsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if seo_indexing_allowed(request):
            return response
        # Не перетираємо явний заголовок від проксі/хостингу, якщо він уже жорсткіший.
        existing = response.get('X-Robots-Tag', '')
        if 'noindex' not in existing.lower():
            response['X-Robots-Tag'] = 'noindex, nofollow'
        return response
