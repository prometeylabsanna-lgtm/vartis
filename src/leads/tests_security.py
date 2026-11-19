from django.core.cache import cache
from django.test import TestCase

from .forms import LeadForm, clean_source_page
from .models import Lead


def _payload(**overrides):
    data = {
        'name': 'Іван Тест',
        'phone': '0671234567',
        'email': 'ivan@example.com',
        'message': 'pytest',
        'consent': 'on',
        'form_variant': 'footer',
        'form_id': 'lead-form-footer',
        'source_page': '/pro-kompaniiu/',
        'honeypot': '',
    }
    data.update(overrides)
    return data


class LeadMessageLimitTests(TestCase):
    def test_message_over_2000_rejected(self):
        form = LeadForm(_payload(message='а' * 2001))
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)

    def test_message_2000_accepted(self):
        form = LeadForm(_payload(message='а' * 2000))
        self.assertTrue(form.is_valid(), form.errors)


class LeadSourcePageTests(TestCase):
    def test_keeps_internal_path(self):
        self.assertEqual(clean_source_page('/pro-kompaniiu/'), '/pro-kompaniiu/')

    def test_drops_external_and_header_injection(self):
        self.assertEqual(clean_source_page('https://evil.example/'), '')
        self.assertEqual(clean_source_page('/ok/\r\nBcc: x'), '')
        self.assertEqual(clean_source_page('/foo/../bar'), '')


class LeadSubmitHardeningTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = self.client_class()

    def test_honeypot_is_silent_success(self):
        before = Lead.objects.count()
        response = self.client.post('/leads/submit/', _payload(honeypot='bot'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Дякуємо', response.content.decode())
        self.assertEqual(Lead.objects.count(), before)

    def test_unsafe_source_is_not_stored(self):
        response = self.client.post(
            '/leads/submit/',
            _payload(source_page='https://evil.example/\nBcc: x'),
        )
        self.assertEqual(response.status_code, 200)
        lead = Lead.objects.latest('id')
        self.assertEqual(lead.source_page, '')

    def test_internal_source_is_stored(self):
        self.client.post('/leads/submit/', _payload())
        lead = Lead.objects.latest('id')
        self.assertEqual(lead.source_page, '/pro-kompaniiu/')

    def test_unknown_variant_is_not_modal(self):
        response = self.client.post(
            '/leads/submit/',
            _payload(form_variant='xmodal', email='bad'),
        )
        self.assertEqual(response.status_code, 422)
        self.assertNotContains(response, 'lead-modal-title', status_code=422)

    def test_sixth_submit_is_limited(self):
        for _ in range(5):
            response = self.client.post('/leads/submit/', _payload())
            self.assertEqual(response.status_code, 200)
        before = Lead.objects.count()
        response = self.client.post('/leads/submit/', _payload())
        self.assertEqual(response.status_code, 429)
        self.assertIn('Забагато спроб', response.content.decode())
        self.assertEqual(Lead.objects.count(), before)
