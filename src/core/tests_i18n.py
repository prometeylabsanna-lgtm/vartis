from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import RequestFactory, SimpleTestCase, TestCase
from django.utils import translation

from src.blog.models import Article
from src.core.i18n_seed.fill import open_for_english
from src.core.models import SiteSettings
from src.pages.models import ServicePage
from src.pages.views import server_error


class EnglishLocaleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_content')
        call_command('seed_en')

    def test_english_service_hero_and_canonical_slug(self):
        response = self.client.get('/en/services/consulting/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Expert support for business')
        self.assertContains(response, 'What consulting includes')
        self.assertContains(response, 'Request a consultation')
        self.assertContains(response, 'lang-switch--desktop')
        self.assertContains(response, 'hreflang="uk"')
        self.assertContains(response, 'hreflang="en"')
        self.assertContains(response, 'og:locale" content="en_US"')

        aliased = self.client.get('/en/services/konsaltynh/')
        self.assertEqual(aliased.status_code, 301)
        self.assertEqual(aliased.headers['Location'], '/en/services/consulting/')

    def test_empty_english_falls_back_to_ukrainian(self):
        page = ServicePage.objects.get(slug='konsaltynh')
        with translation.override('uk'):
            page.hero_text_uk = 'Експертна підтримка'
            page.hero_text_en = ''
            page.save(update_fields=['hero_text_uk', 'hero_text_en'])
        response = self.client.get('/en/services/consulting/')
        self.assertContains(response, 'Експертна підтримка')

    def test_article_switcher_uses_paired_slug(self):
        self.assertTrue(Article.objects.filter(slug='perevirka-kontrahenta').exists())
        response = self.client.get('/blog/perevirka-kontrahenta/')
        self.assertContains(response, 'href="/en/blog/counterparty-check/"')
        home = self.client.get('/')
        self.assertRegex(home.content.decode(), r'href="/en/"\s+class="lang-switch__btn')
        english_home = self.client.get('/en/')
        self.assertRegex(english_home.content.decode(), r'href="/"\s+class="lang-switch__btn')
        self.assertRegex(english_home.content.decode(), r'href="/en/"\s+class="lang-switch__btn[^"]* is-active')
        about = self.client.get('/pro-kompaniiu/')
        self.assertRegex(about.content.decode(), r'href="/en/about/"\s+class="lang-switch__btn')
        english = self.client.get('/en/blog/counterparty-check/')
        self.assertEqual(english.status_code, 200)
        self.assertContains(english, 'Counterparty screening: how to see hidden risks')

    def test_english_lead_thanks_and_phone_error(self):
        self.client.get('/en/')
        thanks = self.client.post('/leads/submit/', {
            'name': 'Ivan Test',
            'phone': '0671234567',
            'email': 'ivan@example.com',
            'message': 'hello',
            'consent': 'on',
            'form_variant': 'footer',
            'form_id': 'lead-form-footer',
            'source_page': '/en/',
            'honeypot': '',
        }, HTTP_HX_REQUEST='true')
        self.assertEqual(thanks.status_code, 200)
        self.assertIn('Thank you for your request', thanks.content.decode())

        error = self.client.post('/leads/submit/', {
            'name': 'Ivan Test',
            'phone': '123',
            'email': 'ivan@example.com',
            'message': 'hello',
            'consent': 'on',
            'form_variant': 'footer',
            'form_id': 'lead-form-footer',
            'source_page': '/en/',
            'honeypot': '',
        }, HTTP_HX_REQUEST='true')
        self.assertEqual(error.status_code, 422)
        self.assertIn('Enter a number as +380', error.content.decode())

    def test_admin_stays_ukrainian_with_english_cookie(self):
        get_user_model().objects.create_superuser('adm', 'a@example.com', 'pw')
        self.client.force_login(get_user_model().objects.get(username='adm'))
        self.client.cookies['django_language'] = 'en'
        response = self.client.get('/admin/')
        self.assertEqual(response.headers.get('Content-Language'), 'uk')
        self.assertContains(response, 'lang="uk"')
        settings = SiteSettings.load()
        form = self.client.get(f'/admin/core/sitesettings/{settings.pk}/change/')
        self.assertEqual(form.headers.get('Content-Language'), 'uk')
        self.assertContains(form, 'ВАРТІС')
        self.assertContains(form, 'Українська')
        self.assertContains(form, 'English')

    def test_custom_500_both_languages_without_database(self):
        factory = RequestFactory()
        with self.assertNumQueries(0):
            ukrainian = server_error(factory.get('/500/'))
            english = server_error(factory.get('/en/500/'))
        self.assertEqual(ukrainian.status_code, 500)
        self.assertIn('Внутрішня помилка сервера', ukrainian.content.decode())
        self.assertIn('href="/"', ukrainian.content.decode())
        self.assertEqual(english.status_code, 500)
        self.assertIn('Internal server error', english.content.decode())
        self.assertIn('href="/en/"', english.content.decode())

    def test_sitemap_lists_english_alternate(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn('/en/services/consulting/', body)
        self.assertIn('hreflang="en"', body)
        self.assertIn('hreflang="uk"', body)


class EnglishDeployHookTests(TestCase):
    def test_vercel_bootstrap_always_calls_seed_en(self):
        from pathlib import Path

        import src.core.bootstrap_vercel as mod

        text = Path(mod.__file__).read_text(encoding='utf-8')
        self.assertIn("call_command('seed_en'", text)
        after_ukrainian = text.split("vercel seed_site_blocks failed")[-1]
        self.assertIn("call_command('seed_en'", after_ukrainian)
        self.assertGreater(
            text.find("call_command('seed_en'"),
            text.find('if needs_seed:'),
        )
        from src.core.management.commands.seed_content import Command as SeedContent
        from src.core.i18n_seed import apply_english_copy
        import inspect

        self.assertIn('under_ukrainian', inspect.getsource(SeedContent.handle))
        self.assertIn('under_ukrainian', inspect.getsource(apply_english_copy))

    def test_seed_content_alone_fills_english_home(self):
        translation.activate('en')
        try:
            call_command('seed_content')
        finally:
            translation.deactivate()
        settings = SiteSettings.load()
        self.assertEqual(settings.nav_about_en, 'About')
        page = ServicePage.objects.get(slug='konsaltynh')
        self.assertEqual(page.scope_title_uk, 'Що входить у консалтинг')
        self.assertEqual(page.scope_title_en, 'What consulting includes')
        self.assertEqual(page.cta_primary_en, 'Request a consultation')
        response = self.client.get('/en/')
        self.assertContains(response, 'Leave a request')
        self.assertContains(response, 'What we do')


class EnglishFillGateTests(SimpleTestCase):
    def test_cyrillic_in_english_slot_is_replaced(self):
        self.assertTrue(
            open_for_english('Що входить у консалтинг', 'Опис напряму', 'Опис напряму'),
        )

    def test_custom_english_is_kept(self):
        self.assertFalse(
            open_for_english('Custom title', 'Що входить у консалтинг', 'Опис напряму'),
        )
