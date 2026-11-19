from django.test import TestCase
from django.urls import reverse

CREDIT_URL = 'https://www.prometeylabs.com/corporate-website-v2/'


class FooterDeveloperLinkTests(TestCase):
    def test_home_has_nofollow_credit_link(self):
        response = self.client.get(reverse('pages:home'))
        self.assertContains(response, CREDIT_URL)
        self.assertContains(response, 'nofollow')
        self.assertContains(response, '>PrometeyLabs</a>')
        self.assertContains(response, 'site-footer__credit-link')

    def test_inner_pages_show_credit_without_link(self):
        for url_name in ('pages:about', 'pages:privacy', 'pages:contacts'):
            response = self.client.get(reverse(url_name))
            self.assertContains(response, 'PrometeyLabs')
            self.assertNotContains(response, CREDIT_URL)
            self.assertNotContains(response, 'site-footer__credit-link')


class PublicUrlTests(TestCase):
    def test_translit_paths(self):
        self.assertEqual(reverse('pages:about'), '/pro-kompaniiu/')
        self.assertEqual(reverse('pages:privacy'), '/polityka-konfidentsiinosti/')

    def test_cases_catalog_is_removed(self):
        home = self.client.get(reverse('pages:home'))
        self.assertNotContains(home, 'href="/keisy/"')
        self.assertNotContains(home, '>Кейси<')
        listing = self.client.get('/keisy/')
        self.assertEqual(listing.status_code, 404)
        detail = self.client.get('/keisy/nelehalni-pidaktsyzni-tovary/')
        self.assertEqual(detail.status_code, 404)
        sitemap = self.client.get('/sitemap.xml').content.decode()
        self.assertNotIn('/keisy/', sitemap)
        llms = self.client.get('/llms.txt').content.decode()
        self.assertNotIn('/keisy/', llms)
        self.assertNotIn('Кейси', llms)
        from django.contrib.auth import get_user_model

        from config.settings.base import _vartis_unfold_navigation

        sidebar = str(_vartis_unfold_navigation())
        self.assertNotIn('Кейси', sidebar)
        self.assertNotIn('/admin/cases/', sidebar)
        user_model = get_user_model()
        admin_user = user_model.objects.create_superuser(
            'cases-admin', 'cases-admin@example.com', 'secret-pass',
        )
        self.client.force_login(admin_user)
        admin_list = self.client.get('/admin/cases/casestudy/')
        self.assertEqual(admin_list.status_code, 404)
        admin_page = self.client.get('/admin/cases/casespage/')
        self.assertEqual(admin_page.status_code, 404)

    def test_contacts_show_official_details_without_telegram_number(self):
        response = self.client.get(reverse('pages:contacts'))
        self.assertContains(response, '+380 75 535 99 18')
        self.assertContains(response, 'tel:+380755359918')
        self.assertContains(response, 'info@vartis.in.ua')
        self.assertContains(response, 'Ігорівська')
        self.assertContains(response, 'https://wa.me/380755359918')
        self.assertContains(response, 'https://signal.me/#p/+380755359918')
        self.assertContains(response, 'https://t.me/+380733088462')
        self.assertContains(response, '>Telegram<')
        self.assertNotContains(response, 'Хрещатик')
        self.assertNotContains(response, 'info@vartis.ua')
        body = response.content.decode()
        visible = body.replace('https://t.me/+380733088462', '')
        self.assertNotIn('380733088462', visible)

    def test_legacy_khreshchatyk_map_is_replaced(self):
        from src.core.models import SiteSettings

        SiteSettings.objects.update_or_create(
            pk=1,
            defaults={
                'phone': '+380 75 535 99 18',
                'email': 'info@vartis.in.ua',
                'address': '04070, м. Київ, вулиця Ігорівська, буд. 11Б (Бізнес-Центр Ігорівський)',
                'map_embed_url': 'https://maps.google.com/maps?q=Київ,+вул.+Хрещатик,+1&hl=uk&z=16&output=embed',
                'telegram_url': 'https://t.me/+380733088462',
            },
        )
        response = self.client.get(reverse('pages:contacts'))
        self.assertNotContains(response, 'Хрещатик')
        self.assertContains(response, 'Ігорівська')

    def test_privacy_has_official_contacts_not_stub(self):
        from src.pages.models_contacts import PrivacyPage
        from src.pages.privacy_copy import apply_approved_privacy

        apply_approved_privacy(PrivacyPage.load())
        response = self.client.get(reverse('pages:privacy'))
        self.assertNotContains(response, 'Тимчасовий текст')
        self.assertNotContains(response, '[Email]')
        self.assertNotContains(response, '[дата]')
        self.assertContains(response, 'Редакція від 19 листопада 2026')
        self.assertContains(response, 'info@vartis.in.ua')
        self.assertContains(response, '+380 75 535 99 18')
        self.assertContains(response, 'Ігорівська')

    def test_cookie_banner_shows_until_consent(self):
        response = self.client.get(reverse('pages:home'))
        self.assertContains(response, 'data-cookie-banner')
        self.assertContains(response, 'data-action="accept-cookies"')
        self.client.cookies['vartis_cookie_consent'] = '1'
        hidden = self.client.get(reverse('pages:home'))
        self.assertNotContains(hidden, 'data-cookie-banner')

    def test_home_process_steps_have_no_final_period(self):
        response = self.client.get(reverse('pages:home'))
        self.assertContains(response, 'Зʼясовуємо, яку інформацію потрібно отримати та на які питання відповісти<')
        self.assertNotContains(response, 'питання відповісти.')


class SitemapTests(TestCase):
    def test_privacy_is_yearly_and_article_lastmod_is_publish_date(self):
        from datetime import date

        from src.blog.models import Article

        Article.objects.create(
            slug='test-lastmod',
            title='Тест',
            category='Аналітика',
            published_at=date(2024, 3, 2),
            excerpt='Коротко',
        )
        response = self.client.get('/sitemap.xml')
        body = response.content.decode()
        self.assertContains(response, '/polityka-konfidentsiinosti/')
        self.assertIn('<changefreq>yearly</changefreq>', body)
        self.assertIn('<lastmod>2024-03-02</lastmod>', body)
        self.assertNotIn('/keysy/', body)
        self.assertNotIn('/keisy/', body)
