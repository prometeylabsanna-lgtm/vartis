from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import RequestFactory, TestCase

from src.blog.models import Article
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
        self.assertContains(response, 'lang-switch--desktop')
        self.assertContains(response, 'hreflang="uk"')
        self.assertContains(response, 'hreflang="en"')
        self.assertContains(response, 'og:locale" content="en_US"')

        aliased = self.client.get('/en/services/konsaltynh/')
        self.assertEqual(aliased.status_code, 301)
        self.assertEqual(aliased.headers['Location'], '/en/services/consulting/')

    def test_empty_english_falls_back_to_ukrainian(self):
        page = ServicePage.objects.get(slug='konsaltynh')
        page.hero_text_en = ''
        page.save(update_fields=['hero_text_en'])
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
