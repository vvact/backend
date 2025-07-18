# products/tests/test_sample.py
from django.test import TestCase

class SampleTest(TestCase):
    def test_math(self):
        self.assertEqual(1 + 1, 2)
