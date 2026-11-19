from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.utils import timezone

from axes.models import AccessAttempt

from src.core.client_ip import client_ip


class ClientIpTests(TestCase):
    def test_real_ip_wins(self):
        request = RequestFactory().get(
            '/',
            HTTP_X_REAL_IP='203.0.113.8',
            HTTP_X_FORWARDED_FOR='198.51.100.2',
            REMOTE_ADDR='127.0.0.1',
        )
        self.assertEqual(client_ip(request), '203.0.113.8')

    def test_forwarded_uses_rightmost(self):
        request = RequestFactory().get(
            '/',
            HTTP_X_FORWARDED_FOR='198.51.100.2, 203.0.113.9',
            REMOTE_ADDR='10.0.0.1',
        )
        self.assertEqual(client_ip(request), '203.0.113.9')


class AdminLockoutTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        user_model.objects.create_user(
            username='lock-user',
            password='Vartis-lock-8841',
            is_staff=True,
            is_superuser=True,
        )
        user_model.objects.create_user(
            username='other-user',
            password='Vartis-lock-8841',
            is_staff=True,
            is_superuser=True,
        )

    def _login(self, username, password, ip='127.0.0.1'):
        return self.client.post(
            '/admin/login/',
            {'username': username, 'password': password},
            REMOTE_ADDR=ip,
        )

    def test_fifth_failure_locks_login(self):
        for _ in range(4):
            response = self._login('lock-user', 'wrong-password')
            self.assertNotEqual(response.status_code, 429)
        response = self._login('lock-user', 'wrong-password')
        self.assertEqual(response.status_code, 429)
        self.assertContains(
            response,
            'Забагато невдалих спроб входу',
            status_code=429,
        )
        response = self._login('lock-user', 'Vartis-lock-8841')
        self.assertEqual(response.status_code, 429)

    def test_same_ip_locks_another_username(self):
        for _ in range(5):
            self._login('lock-user', 'wrong-password', ip='203.0.113.10')
        response = self._login('other-user', 'Vartis-lock-8841', ip='203.0.113.10')
        self.assertEqual(response.status_code, 429)

    def test_login_works_after_cooloff(self):
        for _ in range(5):
            self._login('lock-user', 'wrong-password', ip='203.0.113.20')
        AccessAttempt.objects.filter(ip_address='203.0.113.20').update(
            attempt_time=timezone.now() - timedelta(minutes=6),
        )
        response = self._login('lock-user', 'Vartis-lock-8841', ip='203.0.113.20')
        self.assertEqual(response.status_code, 302)
