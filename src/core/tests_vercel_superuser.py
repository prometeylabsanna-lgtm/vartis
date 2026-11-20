import os
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase

from src.core.bootstrap_vercel import DEMO_PASSWORD, DEMO_USERNAME, ensure_demo_superuser


class VercelDemoSuperuserTests(TestCase):
    def test_without_vercel_does_not_create_admin(self):
        env = {k: v for k, v in os.environ.items() if k != 'VERCEL'}
        with mock.patch.dict(os.environ, env, clear=True):
            ensure_demo_superuser()
        self.assertFalse(
            get_user_model().objects.filter(username=DEMO_USERNAME).exists()
        )

    def test_vercel_creates_admin_admin(self):
        with mock.patch.dict(os.environ, {'VERCEL': '1'}):
            ensure_demo_superuser()
        user = get_user_model().objects.get(username=DEMO_USERNAME)
        self.assertTrue(user.check_password(DEMO_PASSWORD))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_admin_login_accepts_admin_admin(self):
        with mock.patch.dict(os.environ, {'VERCEL': '1'}):
            ensure_demo_superuser()
        response = self.client.post(
            '/admin/login/',
            {'username': DEMO_USERNAME, 'password': DEMO_PASSWORD, 'next': '/admin/'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/', response.headers['Location'])
