from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from PIL import Image

from src.core.image_webp import convert_upload_to_webp


def _png_bytes(size=(32, 32), color=(20, 40, 80)) -> bytes:
    buf = BytesIO()
    Image.new('RGB', size, color).save(buf, format='PNG')
    return buf.getvalue()


def _gif_animated_bytes() -> bytes:
    buf = BytesIO()
    frames = [
        Image.new('RGB', (16, 16), (255, 0, 0)),
        Image.new('RGB', (16, 16), (0, 255, 0)),
    ]
    frames[0].save(
        buf,
        format='GIF',
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
    )
    return buf.getvalue()


class ConvertUploadToWebpTests(SimpleTestCase):
    def test_png_becomes_webp(self):
        uploaded = SimpleUploadedFile('hero.png', _png_bytes(), content_type='image/png')
        out = convert_upload_to_webp(uploaded)
        self.assertIsNotNone(out)
        self.assertTrue(out.name.endswith('.webp'))
        img = Image.open(BytesIO(out.read()))
        self.assertEqual(img.format, 'WEBP')

    def test_already_webp_skipped(self):
        buf = BytesIO()
        Image.new('RGB', (8, 8), (1, 2, 3)).save(buf, format='WEBP', quality=88)
        uploaded = SimpleUploadedFile('a.webp', buf.getvalue(), content_type='image/webp')
        self.assertIsNone(convert_upload_to_webp(uploaded))

    def test_svg_skipped(self):
        uploaded = SimpleUploadedFile(
            'logo.svg',
            b'<svg xmlns="http://www.w3.org/2000/svg"></svg>',
            content_type='image/svg+xml',
        )
        self.assertIsNone(convert_upload_to_webp(uploaded))

    def test_animated_gif_skipped(self):
        uploaded = SimpleUploadedFile(
            'anim.gif',
            _gif_animated_bytes(),
            content_type='image/gif',
        )
        self.assertIsNone(convert_upload_to_webp(uploaded))
