from django.test import Client, TestCase

from .forms import LeadForm, normalize_ua_phone
from .models import Lead


class NormalizeUaPhoneTests(TestCase):
    def test_plus380(self):
        self.assertEqual(normalize_ua_phone('+380671234567'), '+380671234567')

    def test_local_zero(self):
        self.assertEqual(normalize_ua_phone('067 123-45-67'), '+380671234567')

    def test_invalid_length(self):
        self.assertIsNone(normalize_ua_phone('09876567876'))
        self.assertIsNone(normalize_ua_phone('123'))


class LeadFormValidationTests(TestCase):
    def _data(self, **overrides):
        data = {
            'name': "О'Браєн-Тест",
            'phone': '+380671234567',
            'email': 'user@domain.com',
            'message': 'hi',
            'consent': True,
            'honeypot': '',
        }
        data.update(overrides)
        return data

    def test_valid(self):
        form = LeadForm(self._data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_name_digits_rejected(self):
        form = LeadForm(self._data(name='User123'))
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_phone_non_ua_rejected(self):
        form = LeadForm(self._data(phone='+12025550123'))
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_email_invalid(self):
        form = LeadForm(self._data(email='not-an-email'))
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_consent_required(self):
        form = LeadForm(self._data(consent=False))
        self.assertFalse(form.is_valid())
        self.assertIn('consent', form.errors)


class LeadSubmitViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_submit_saves_lead(self):
        before = Lead.objects.count()
        response = self.client.post('/leads/submit/', {
            'name': 'Іван Тест',
            'phone': '0671234567',
            'email': 'ivan@example.com',
            'message': 'pytest',
            'consent': 'on',
            'form_variant': 'footer',
            'form_id': 'lead-form-footer',
            'source_page': '/',
            'honeypot': '',
        }, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), before + 1)
        lead = Lead.objects.latest('id')
        self.assertEqual(lead.phone, '+380671234567')
        self.assertIn('Дякуємо', response.content.decode())

    def test_submit_invalid_returns_422(self):
        response = self.client.post('/leads/submit/', {
            'name': 'User123',
            'phone': '123',
            'email': 'bad',
            'consent': 'on',
            'form_variant': 'footer',
            'form_id': 'lead-form-footer',
            'source_page': '/',
            'honeypot': '',
        }, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 422)
        html = response.content.decode()
        self.assertIn('is-invalid', html)
