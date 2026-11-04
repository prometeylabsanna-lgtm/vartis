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
