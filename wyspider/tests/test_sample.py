import unittest
import sys
sys.path.append("../..")
from wyspider.spiders import wybugspider
from wyspider.tests import fake_response_from_file


class SpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = wybugspider.WySpider()

    def _test_item_results(self, results, expected_length):
        count = 0
        for item in results:
            self.assertIsNotNone(item['fbid'])
            self.assertIsNotNone(item['title'])
        self.assertEqual(count, expected_length)

    def test_parse(self):
        results = self.spider.parse(fake_response_from_file('sample.html'))
        self._test_item_results(results, 10)
