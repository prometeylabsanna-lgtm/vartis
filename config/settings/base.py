from pathlib import Path

from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# TODO(prod): прибрати default — SECRET_KEY лише з env / Vercel secrets
SECRET_KEY = config(
    'SECRET_KEY',
    default='TODO-VERCEL-DEMO-INSECURE-SECRET-KEY-REPLACE-BEFORE-PROD',
)

DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.forms',
    'django_htmx',
    'csp',
    'src.core',
    'src.pages',
    'src.blog',
    'src.cases',
    'src.leads',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'src.core.context_processors.site_settings',
                'src.core.cms_context.site_cms',
            ],
        },
    },
]

# Щоб admin/unfold віджети брали overrides з templates/ (URL, file input тощо).
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'uk'
TIME_ZONE = 'Europe/Kyiv'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = []
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@vartis.ua')
LEAD_EMAIL_TO = config('LEAD_EMAIL_TO', default='')
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN', default='')
TELEGRAM_CHAT_ID = config('TELEGRAM_CHAT_ID', default='')
CRM_WEBHOOK_URL = config('CRM_WEBHOOK_URL', default='')
GTM_ID = config('GTM_ID', default='')

CONTENT_SECURITY_POLICY = {
    # Unfold/Alpine на /admin/ потребує eval для x-show тощо — інакше #modal-overlay лишається видимим.
    'EXCLUDE_URL_PREFIXES': ('/admin/',),
    'DIRECTIVES': {
        'default-src': ["'self'"],
        'script-src': ["'self'", 'https://www.googletagmanager.com', 'https://cdn.jsdelivr.net'],
        'style-src': ["'self'", 'https://fonts.googleapis.com', 'https://cdn.jsdelivr.net'],
        'font-src': ["'self'", 'https://fonts.gstatic.com', 'data:'],
        'img-src': ["'self'", 'data:', 'https:'],
        'frame-src': ["'self'", 'https://www.google.com', 'https://maps.google.com'],
        'connect-src': ["'self'", 'https://www.google-analytics.com'],
    },
}

def _vartis_unfold_navigation():
    from src.core.site_content_registry import build_content_sidebar_groups

    cms_groups = build_content_sidebar_groups()
    return [
        {
            'title': 'Налаштування',
            'separator': True,
            'items': [
                {
                    'title': 'Налаштування сайту',
                    'icon': 'settings',
                    'link': '/admin/core/sitesettings/1/change/',
                },
                {
                    'title': 'Недавні дії',
                    'icon': 'history',
                    'link': '/admin/recent-actions/',
                },
            ],
        },
        *cms_groups,
        {
            'title': 'Контент',
            'separator': True,
            'items': [
                {
                    'title': 'Блог',
                    'icon': 'article',
                    'link': '/admin/blog/article/',
                },
                {
                    'title': 'Кейси',
                    'icon': 'folder',
                    'link': '/admin/cases/casestudy/',
                },
                {
                    'title': 'Заявки',
                    'icon': 'mail',
                    'link': '/admin/leads/lead/',
                },
            ],
        },
    ]


UNFOLD = {
    'SITE_TITLE': 'Vartis Intelligence',
    'SITE_HEADER': 'Vartis Intelligence',
    'SITE_URL': '/',
    'SITE_LOGO': {
        'light': '/static/images/logo.png',
        'dark': '/static/images/logo.png',
    },
    'SITE_FAVICONS': [
        {
            'rel': 'icon',
            'sizes': 'any',
            'href': '/static/images/favicon.ico',
        },
        {
            'rel': 'icon',
            'type': 'image/png',
            'sizes': '32x32',
            'href': '/static/images/favicon.png',
        },
        {
            'rel': 'apple-touch-icon',
            'sizes': '180x180',
            'href': '/static/images/apple-touch-icon.png',
        },
    ],
    'SHOW_HISTORY': True,
    'COLORS': {
        'primary': {
            '50': 'oklch(97% 0.01 250)',
            '100': 'oklch(94% 0.02 250)',
            '200': 'oklch(86% 0.04 250)',
            '300': 'oklch(74% 0.06 250)',
            '400': 'oklch(58% 0.08 250)',
            '500': 'oklch(42% 0.08 250)',
            '600': 'oklch(34% 0.07 250)',
            '700': 'oklch(28% 0.06 250)',
            '800': 'oklch(22% 0.05 250)',
            '900': 'oklch(16% 0.04 250)',
            '950': 'oklch(12% 0.03 250)',
        },
    },
    # Лише брендинг адмінки. site_content.css підключається в CMS-шаблоні.
    'STYLES': [
        '/static/css/admin/vartis_unfold.css',
    ],
    'SIDEBAR': {
        'show_search': True,
        'show_all_applications': False,
        'navigation': _vartis_unfold_navigation(),
    },
}
