import importlib

from django.apps import apps as django_apps
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from src.core.contact_defaults import DEMO_TELEGRAM_URL, resolve_public_contacts
from src.core.models import SiteBlock, SiteSettings

labels_migration = importlib.import_module('src.core.migrations.0010_ua_site_block_labels')


class TelegramChatUrlTests(TestCase):
    def test_empty_chat_url_falls_back_to_number_link(self):
        SiteSettings.objects.update_or_create(pk=1, defaults={'telegram_chat_url': '', 'telegram_url': ''})
        self.assertEqual(resolve_public_contacts(SiteSettings.load())['telegram_url'], DEMO_TELEGRAM_URL)

    def test_empty_chat_url_uses_stored_fallback(self):
        SiteSettings.objects.update_or_create(
            pk=1, defaults={'telegram_chat_url': '', 'telegram_url': 'https://t.me/+380000000001'},
        )
        self.assertEqual(resolve_public_contacts(SiteSettings.load())['telegram_url'], 'https://t.me/+380000000001')

    def test_chat_url_wins_and_renders_on_contacts_and_footer(self):
        SiteSettings.objects.update_or_create(
            pk=1,
            defaults={'telegram_chat_url': 'https://t.me/vartis_chat', 'telegram_url': 'https://t.me/+380733088462'},
        )
        body = self.client.get(reverse('pages:contacts')).content.decode()
        self.assertGreaterEqual(body.count('https://t.me/vartis_chat'), 2)  # плитка + футер
        self.assertNotIn('380733088462', body)

    def test_admin_contacts_tab_has_chat_field(self):
        user = get_user_model().objects.create_superuser('adm', 'a@example.com', 'pw')
        self.client.force_login(user)
        html = self.client.get(reverse('admin:core_sitesettings_change', args=[SiteSettings.load().pk])).content.decode()
        self.assertIn('name="telegram_chat_url"', html)
        self.assertIn('Telegram: посилання на чат компанії', html)


class AdminUkrainianTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser('adm', 'a@example.com', 'pw')

    def setUp(self):
        self.client.force_login(self.user)

    def test_changelist_action_bar_is_ukrainian(self):
        html = self.client.get(reverse('admin:leads_lead_changelist')).content.decode()
        self.assertIn('Виберіть дію', html)
        self.assertNotIn('>Run<', html)
        for english in ('Select action', 'Toggle sidebar', 'Open command tool', 'Run the selected action'):
            self.assertNotIn(english, html)

    def test_unfold_chrome_is_ukrainian(self):
        html = self.client.get(reverse('admin:index')).content.decode()
        for english in ('Available shortcuts', 'Toggle dark/light mode', 'Create new record', 'Navigate'):
            self.assertNotIn(english, html)
        self.assertIn('Доступні гарячі клавіші', html)

    def test_axes_admin_labels_are_ukrainian(self):
        html = self.client.get(reverse('admin:index')).content.decode()
        self.assertNotIn('Access attempts', html)
        self.assertNotIn('Access failures', html)
        self.assertNotIn('Access logs', html)
        self.assertIn('Безпека входу', html)
        self.assertIn('Спроби входу', html)
        self.assertIn('Невдалі входи', html)
        self.assertIn('Журнал входів', html)

    def test_style_form_has_no_glass_toggle(self):
        html = self.client.get(
            reverse('admin:core_homestylesettings_change', args=[1]),
        ).content.decode()
        self.assertNotIn('Скло (glass)', html)
        self.assertNotIn('name="glass_enabled"', html)

    def test_hero_labels_are_ukrainian(self):
        html = self.client.get(reverse('admin:core_homeherosettings_change', args=[1])).content.decode()
        self.assertIn('Заголовок першого екрана', html)
        self.assertNotIn('Hero заголовок', html)

    def test_label_migration_is_idempotent_and_keeps_custom(self):
        SiteBlock.objects.create(page='about', key='zz_custom', label='Hero заголовок')
        SiteBlock.objects.create(page='about', key='zz_mine', label='Моя назва')
        labels_migration.forwards(django_apps, None)
        labels_migration.forwards(django_apps, None)
        self.assertEqual(SiteBlock.objects.get(key='zz_custom').label, 'Заголовок першого екрана')
        self.assertEqual(SiteBlock.objects.get(key='zz_mine').label, 'Моя назва')
