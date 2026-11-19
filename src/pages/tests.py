from django.test import TestCase

from src.pages.canon_seed import sync_all, sync_home
from src.pages.design_copy_deep import DEEP
from src.pages.models import HomePage, ServicePage


class DeepCopyTests(TestCase):
    def test_example_and_faq_match_client_edit(self):
        self.assertIn('товари визначеного сегменту', DEEP['example_lead'])
        self.assertNotIn('цигарки', DEEP['example_lead'])
        self.assertIn('кількість точок', DEEP['ex_limits'][0])
        questions = [item[0] for item in DEEP['faqs']]
        self.assertFalse(any('як виглядає звіт' in question for question in questions))

    def test_profile_scroller_is_on_service_page(self):
        ServicePage.objects.create(
            slug='konsaltynh',
            title='Консалтинг',
            is_published=True,
        )
        ServicePage.objects.create(
            slug='zakhyst-vid-vytoku',
            title='Захист',
            is_published=True,
        )
        response = self.client.get('/posluhy/konsaltynh/')
        self.assertContains(response, 'data-dir-scroller')
        self.assertContains(response, 'data-dir-prev')
        self.assertContains(response, 'data-dir-next')

    def test_home_renders_model_copy(self):
        sync_all()
        response = self.client.get('/')
        self.assertContains(response, 'ризики на переваги')
        self.assertContains(response, 'Залишити заявку')

    def test_seed_keeps_custom_home_title(self):
        page = HomePage.load()
        page.hero_title = 'Мій заголовок'
        page.save(update_fields=['hero_title'])
        sync_home()
        page.refresh_from_db()
        self.assertEqual(page.hero_title, 'Мій заголовок')
