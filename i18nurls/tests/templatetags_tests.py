from django.utils import translation
from i18nurls.templatetags.i18nurls import override
from i18nurls.tests.base import BaseTestCase


class OverrideTest(BaseTestCase):

    def test_override(self):
        translation.activate('en')
        self.assertEqual('en', translation.get_language())

        with override('nl'):
            self.assertEqual('nl', translation.get_language())

        self.assertEqual('en', translation.get_language())
