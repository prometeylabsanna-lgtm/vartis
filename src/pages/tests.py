from django.test import TestCase

from src.pages.design_copy_deep import DEEP
from src.pages.models import ServicePage


class DeepCopyTests(TestCase):
    def test_example_and_faq_match_client_edit(self):
        self.assertIn('товари визначеного сегменту', DEEP['example_lead'])
        self.assertNotIn('цигарки', DEEP['example_lead'])
        self.assertIn('кількість товару', DEEP['ex_limits'][0])
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
