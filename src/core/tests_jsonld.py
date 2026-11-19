from django.test import SimpleTestCase

from src.core.seo import json_ld_script


class JsonLdEscapeTests(SimpleTestCase):
    def test_script_breakout_is_escaped(self):
        payload = json_ld_script({'name': '</script><script>alert(1)'})
        self.assertNotIn('<', payload)
        self.assertIn('\\u003c', payload)
