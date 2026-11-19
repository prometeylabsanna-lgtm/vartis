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
        self.assertContains(response, 'Експрес-перевірка контрагентів — VI Analysis')
        self.assertContains(response, 'Комплексна допомога бізнесу')
        self.assertContains(response, 'Консалтинг')
        self.assertContains(response, 'Глибока аналітика')

    def test_home_hides_invisible_direction(self):
        from src.pages.models import HomeDirection

        sync_home()
        card = HomeDirection.objects.get(title='Консалтинг')
        card.is_visible = False
        card.save(update_fields=['is_visible'])
        response = self.client.get('/')
        self.assertNotContains(response, 'Експертна підтримка бізнесу в питаннях аналізу ситуацій')

    def test_seed_keeps_custom_home_title(self):
        page = HomePage.load()
        page.hero_title = 'Мій заголовок'
        page.save(update_fields=['hero_title'])
        sync_home()
        page.refresh_from_db()
        self.assertEqual(page.hero_title, 'Мій заголовок')


class AboutStatAdminSplitTests(TestCase):
    def test_sidebar_has_two_stat_menus(self):
        from config.settings.base import _vartis_unfold_navigation

        nav = str(_vartis_unfold_navigation())
        self.assertIn('/admin/pages/aboutintrostat/', nav)
        self.assertIn('/admin/pages/aboutkeystat/', nav)
        self.assertNotIn('/admin/pages/aboutstat/', nav)

    def test_changelists_show_only_own_block(self):
        from django.contrib.auth import get_user_model

        from src.pages.models import AboutPage, AboutStat

        get_user_model().objects.create_superuser('adm', 'a@example.com', 'pw')
        self.client.force_login(
            get_user_model().objects.get(username='adm'),
        )
        page = AboutPage.load()
        AboutStat.objects.create(page=page, block=AboutStat.BLOCK_INTRO, value='25+', label='стрічка про нас')
        AboutStat.objects.create(page=page, block=AboutStat.BLOCK_KEY, value='1000', label='ключ перевірок')
        intro = self.client.get('/admin/pages/aboutintrostat/').content.decode()
        key = self.client.get('/admin/pages/aboutkeystat/').content.decode()
        self.assertIn('стрічка про нас', intro)
        self.assertNotIn('ключ перевірок', intro)
        self.assertIn('ключ перевірок', key)
        self.assertNotIn('стрічка про нас', key)


class TeamMemberAdminEditorTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model

        from src.pages.models import AboutPage, TeamMember

        get_user_model().objects.create_superuser('adm', 'a@example.com', 'pw')
        self.client.force_login(get_user_model().objects.get(username='adm'))
        self.member = TeamMember.objects.create(
            page=AboutPage.load(),
            name='Тест',
            role='Директор',
            bio='Прямий текст біографії',
            expertise=['Пункт один', 'Пункт два'],
            career_path=[{'t': 'Посада тестова', 'y': 'Нині'}],
            order=0,
        )

    def test_change_form_shows_rows_not_json(self):
        response = self.client.get(f'/admin/pages/teammember/{self.member.pk}/change/')
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertNotIn('name="expertise"', body)
        self.assertNotIn('name="career_path"', body)
        self.assertNotIn('["Пункт один"', body)
        self.assertIn('name="expertise_item"', body)
        self.assertIn('name="career_path_t"', body)
        self.assertIn('Пункт один', body)
        self.assertIn('Посада тестова', body)
        self.assertIn('cms-list', body)
        self.assertIn('cms-tinymce', body)
        self.assertIn('js/admin/cms_tinymce.js', body)

    def test_save_list_rows_without_json_textarea(self):
        response = self.client.post(
            f'/admin/pages/teammember/{self.member.pk}/change/',
            {
                'name': 'Тест',
                'role': 'Директор',
                'regalia': '',
                'email': '',
                'bio': '<p>Оновлена біо</p>',
                'photo_position': '50% 20%',
                'order': '0',
                'expertise_item': ['Новий пункт', 'Другий'],
                'career_path_t': ['Нова посада', ''],
                'career_path_y': ['2024', ''],
            },
        )
        self.assertEqual(response.status_code, 302, response.content[:500])
        self.member.refresh_from_db()
        self.assertEqual(self.member.expertise, ['Новий пункт', 'Другий'])
        self.assertEqual(self.member.career_path, [{'t': 'Нова посада', 'y': '2024'}])
        self.assertIn('Оновлена біо', self.member.bio)

    def test_about_renders_rich_bio(self):
        from src.core.richtext import sanitize_html

        html = sanitize_html(
            '<p>Абзац <span style="color: #b58b4a">золото</span>'
            '<script>alert(1)</script></p>'
        )
        self.assertIn('color: #b58b4a', html)
        self.assertIn('золото', html)
        self.assertNotIn('script', html)
        self.member.bio = '<p>Абзац <strong>жирний</strong></p>'
        self.member.save(update_fields=['bio'])
        response = self.client.get('/pro-kompaniiu/')
        self.assertContains(response, 'Абзац')
        self.assertContains(response, '<strong>жирний</strong>', html=True)
