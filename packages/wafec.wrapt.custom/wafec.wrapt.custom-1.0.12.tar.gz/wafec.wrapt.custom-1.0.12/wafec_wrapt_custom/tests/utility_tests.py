import unittest

from wafec_wrapt_custom.utility import fullname, starts_with
from wafec_wrapt_custom.tests.foo.bar import Bar


class FooBar(object):
    pass


class UtilityTests(unittest.TestCase):
    def setUp(self):
        self.black_list = ['test1.', 'test2.test3.']

    def test_fullname_when_none(self):
        fn = fullname(None)
        self.assertIsNone(fn)

    def test_fullname(self):
        bar = Bar()
        fn = fullname(bar)
        self.assertEqual('wafec_wrapt_custom.tests.foo.bar.Bar', fn)

    def test_fullname_with_locals(self):
        foobar = FooBar()
        fn = fullname(foobar)
        self.assertEqual('utility_tests.FooBar', fn)

    def test_starts_with(self):
        result = starts_with(self.black_list, 'test1.Bar')
        self.assertTrue(result)

    def test_starts_with_when_not_present(self):
        result = starts_with(self.black_list, 'test3.Bar')
        self.assertFalse(result)

    def test_starts_with_when_none(self):
        result = starts_with(self.black_list, None)
        self.assertFalse(result)

    def test_starts_with_when_collection_is_none(self):
        result = starts_with(None, 'test3.Bar')
        self.assertFalse(result)

