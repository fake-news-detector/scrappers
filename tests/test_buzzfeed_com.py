import unittest
import requests

from scrappers.buzzfeed_com import find_titles_from_category_page, append_to_csv
from tests.helpers import trim, load_fixture
from unittest.mock import MagicMock
from collections import namedtuple
import pandas as pd
import os


def scrape_mocked(fixture_file, url, scrape_fn):
    fixture = load_fixture("buzzfeed_com", fixture_file, url)
    MockedRequest = namedtuple('MockedRequest', 'text')
    original_get = requests.get

    requests.get = MagicMock(return_value=MockedRequest(text=fixture))
    result = scrape_fn()
    requests.get = original_get

    return result


class BuzzFeedComTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.maxDiff = None

    def test_find_titles_from_category_page(self):
        result = scrape_mocked("lol.html",
                               "https://www.buzzfeed.com/br/feedpage/feed/search_buzzes?page=1&page_name=badge&tags.tag_name=lol",
                               lambda: find_titles_from_category_page("lol", 1))

        self.assertEqual(
            result[0], {
                'title': '20 imagens que, por incrível que pareça, não são de pirocas enormes',
                'url': 'https://www.buzzfeed.com/daves4/animais-penis-enormes-rola-penis'
            })
        self.assertEqual(
            result[-1], {
                'title': 'Só quem não tem frescura para comer reconhece o valor destas delícias',
                'url': 'https://www.buzzfeed.com/jasminnahar/teste-frescura-comida'
            })

    def test_append_to_csv(self):
        os.remove("temp.csv")
        append_to_csv('temp.csv', [{'title': 'foo', 'url': 'bar'}])
        df = pd.read_csv('temp.csv')
        self.assertEqual(df['title'][0], "foo")
        self.assertEqual(df['url'][0], "bar")

        append_to_csv('temp.csv', [{'title': 'baz', 'url': 'qux'}])
        df = pd.read_csv('temp.csv')
        self.assertEqual(df['title'][1], "baz")
        self.assertEqual(df['url'][1], "qux")
