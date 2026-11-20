"""Мова публічного сайту і примусова українська в адмінці."""

from django.conf import settings
from django.utils import translation


class ForceAdminUkrainianMiddleware:
    """Адмінка лишається українською, навіть якщо на сайті відкрито English."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (request.path or '').startswith('/admin'):
            translation.activate('uk')
            request.LANGUAGE_CODE = 'uk'
        return self.get_response(request)


class PublicLanguageCookieMiddleware:
    """Запамʼятовує мову сторінки для POST /leads/submit/ без мовного префікса."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path or ''
        # LocaleMiddleware при prefix_default_language=False примусово ставить uk
        # на шляхах без префікса. Заявка має лишитися мовою сторінки, з якої її надіслали.
        if path.startswith('/leads/'):
            cookie = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, '')
            lang = 'en' if str(cookie).startswith('en') else 'uk'
            translation.activate(lang)
            request.LANGUAGE_CODE = lang
        response = self.get_response(request)
        if path.startswith('/admin') or path.startswith('/static') or path.startswith('/media'):
            return response
        lang = translation.get_language() or 'uk'
        lang = 'en' if lang.startswith('en') else 'uk'
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path='/',
            secure=request.is_secure(),
            httponly=False,
            samesite='Lax',
        )
        return response
