from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from src.core.block_defaults import BLOCK_DEFAULTS, RICHTEXT_KEYS
from src.core.models import SiteBlock, SiteSettings
from src.core.site_content_registry import CONTENT_SECTIONS, all_registry_block_keys


class CmsRegistryTests(TestCase):
    def test_unique_admin_model_names(self):
        names = [s.admin_model_name for s in CONTENT_SECTIONS]
        self.assertEqual(len(names), len(set(names)))

    def test_registry_keys_have_defaults(self):
        for page, key in all_registry_block_keys():
            self.assertIn((page, key), BLOCK_DEFAULTS)

    def test_richtext_keys_are_registered(self):
        for pair in RICHTEXT_KEYS:
            self.assertIn(pair, BLOCK_DEFAULTS)


class CmsAdminSmokeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        SiteSettings.load()
        user_model = get_user_model()
        cls.user = user_model.objects.create_superuser('cms', 'cms@test.local', 'cms')

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)

    def test_hero_section_get_has_tinymce_and_preview(self):
        response = self.client.get('/admin/core/homeherosettings/1/change/')
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn('cms-tinymce', body)
        self.assertIn('site-content-editor__img-preview', body)
        self.assertIn('site-content-editor__tabs', body)
        self.assertIn('cmsTab', body)

    def test_sidebar_lists_are_under_pages(self):
        from src.core.site_content_registry import build_content_sidebar_groups

        groups = {g['title']: g['items'] for g in build_content_sidebar_groups()}
        home_titles = [i['title'] for i in groups['Головна']]
        self.assertIn('Картки переваг', home_titles)
        self.assertIn('Кроки процесу', home_titles)
        about_titles = [i['title'] for i in groups['Про компанію']]
        self.assertIn('Команда (список)', about_titles)
        self.assertNotIn('Списки', groups)
        self.assertNotIn('Оболонка', groups)
        self.assertIn('Шапка', groups)
        self.assertIn('Підвал', groups)

    def test_recent_actions_page(self):
        response = self.client.get('/admin/recent-actions/')
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn('Недавні дії', body)
        self.assertIn('recent-actions-page', body)
        self.assertIn('recent-actions-page__empty', body)
        self.assertIn('Поки немає записаних дій', body)
        self.assertIn('На головну адмінки', body)

    def test_site_settings_has_seo_tab_and_url_wrap(self):
        response = self.client.get('/admin/core/sitesettings/1/change/')
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn('activeFieldsetTab', body)
        self.assertIn('SEO', body)
        self.assertIn('vartis-url-field', body)
        self.assertIn('Логотип сайту', body)
        self.assertIn('id_logo', body)

    def test_admin_branding_logo_and_favicon(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn('/static/images/logo.png', body)
        self.assertIn('/static/images/favicon', body)
        self.assertIn('vartis-admin-logo', body)
        self.assertIn('vartis-admin-logo__img--light', body)
        self.assertIn('vartis-admin-logo__img--dark', body)
        self.assertNotIn('hidden dark:block', body)

    def test_changelist_filters_are_top_dropdowns(self):
        response = self.client.get('/admin/blog/article/')
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertNotIn('За Категорія', body)
        self.assertNotIn('За Опубліковано', body)
        self.assertIn('Категорія', body)
        self.assertIn('Опубліковано', body)
        self.assertIn('unfold-admin-autocomplete', body)
        self.assertNotIn('filter-open-button', body)
        self.assertIn('name="category"', body)
        self.assertIn('name="is_published__exact"', body)
        self.assertIn('vartis-changelist-toolbar', body)
        self.assertIn('vartis-filters-row', body)

    def test_leads_date_filter_uk_placeholders(self):
        response = self.client.get('/admin/leads/lead/')
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn('Створено', body)
        self.assertIn('placeholder="Від"', body)
        self.assertIn('placeholder="До"', body)
        self.assertNotIn('Date from', body)
        self.assertNotIn('Date to', body)
        self.assertIn('vartis-filter__dates', body)
        self.assertNotIn('name="created_at_from_0"', body)

    def test_empty_results_uk(self):
        response = self.client.get('/admin/blog/article/', {'q': '__no_such_article__'})
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn('Нічого не знайдено', body)
        self.assertIn('Скинути фільтри', body)
        self.assertNotIn('No results found', body)
        self.assertNotIn('Reset filters', body)

    def test_admin_index_hides_sidebar_recent_actions(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertNotIn('id="content-related"', body)
        self.assertNotIn('id="recent-actions-module"', body)

    def test_hero_section_post_saves_block(self):
        SiteBlock.objects.update_or_create(
            page='home',
            key='hero_cta',
            defaults={'text_html': 'Старий CTA', 'label': 'CTA', 'content_type': 'text'},
        )
        response = self.client.post(
            '/admin/core/homeherosettings/1/change/',
            {
                'section_visible': 'on',
                'block__home__seo_title__text_html': 'SEO',
                'block__home__seo_description__text_html': 'Desc',
                'block__home__h1__text_html': 'H1',
                'block__home__hero_title__text_html': 'Title',
                'block__home__hero_text__text_html': '<p>Text</p>',
                'block__home__hero_cta__text_html': 'Новий CTA',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            SiteBlock.objects.get(page='home', key='hero_cta').text_html,
            'Новий CTA',
        )
