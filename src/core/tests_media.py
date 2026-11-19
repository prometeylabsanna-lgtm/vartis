import tempfile
from pathlib import Path

from django.test import RequestFactory, SimpleTestCase, override_settings

from src.core.views_media import media_serve


class SvgDownloadTests(SimpleTestCase):
    def test_svg_is_attachment_and_webp_is_not(self):
        factory = RequestFactory()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'probe.svg').write_text(
                '<svg xmlns="http://www.w3.org/2000/svg"></svg>',
                encoding='utf-8',
            )
            (root / 'photo.webp').write_bytes(b'RIFF')
            with override_settings(MEDIA_ROOT=str(root)):
                svg = media_serve(factory.get('/media/probe.svg'), 'probe.svg')
                image = media_serve(factory.get('/media/photo.webp'), 'photo.webp')
            try:
                self.assertEqual(svg.status_code, 200)
                self.assertIn('attachment', svg['Content-Disposition'])
                self.assertIn('probe.svg', svg['Content-Disposition'])
                self.assertIn('nosniff', svg['X-Content-Type-Options'])
                self.assertIn('sandbox', svg['Content-Security-Policy'])
                self.assertEqual(image.status_code, 200)
                self.assertNotIn('attachment', image.get('Content-Disposition', ''))
            finally:
                svg.close()
                image.close()
