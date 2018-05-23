import unittest
import requests

from scrappers.buzzfeed_com import find_titles_from_category_page, find_timestamp_for_post, add_timestamp_to_posts
from tests.helpers import trim, load_fixture
from unittest.mock import MagicMock
from collections import namedtuple
import pandas as pd
import os


def scrape_mocked(fixture_file, url, scrape_fn):
    fixture = load_fixture("buzzfeed_com", fixture_file, url)
    MockedRequest = namedtuple('MockedRequest', ['text', 'raise_for_status'])
    original_get = requests.get

    requests.get = MagicMock(return_value=MockedRequest(
        text=fixture, raise_for_status=lambda: 0))
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

    def test_find_timestamp_for_post(self):
        url = "https://www.buzzfeed.com/daves4/animais-penis-enormes-rola-penis"
        item = (1, {'url': url})
        result = scrape_mocked(
            "post.html", url, lambda: find_timestamp_for_post(item))

        self.assertEqual(str(result['timestamp']), '2018-05-18 19:22:06')

    def test_add_timestamp_to_posts(self):
        posts = scrape_mocked("lol.html",
                              "https://www.buzzfeed.com/br/feedpage/feed/search_buzzes?page=1&page_name=badge&tags.tag_name=lol",
                              lambda: find_titles_from_category_page("lol", 1))
        posts = [posts[0]]
        url = "https://www.buzzfeed.com/daves4/animais-penis-enormes-rola-penis"
        result = scrape_mocked(
            "post.html", url, lambda: add_timestamp_to_posts(posts))

        self.assertEqual(str(result[0]['timestamp']), '2018-05-18 19:22:06')
