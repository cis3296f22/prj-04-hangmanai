from unittest import TestCase
from urllib3.util import url

import random
import requests
from bs4 import BeautifulSoup


class TestWordProvider(TestCase):

    def test__init__(self, url='https://www.ef.edu/english-resources/english-vocabulary/top-3000-words/'):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
        self.word_list = []
        self.Get_html(url)
        self.assertTrue(True)

    def test_Get_html(self):
        response = requests.get(url, headers=self.headers)
        print(response)
        if response.status_code == 200:
            assert True
        else:
            assert False

    def test_Parse_html(self):
        soup = BeautifulSoup(self, 'html.parser')
        div = soup.find('div', class_="cefcom-container")
        ps = div.find_all('p')[1]
        self.word_list = str(ps).replace("<p>", "").replace("</p>", "").split("<br/>")
        self.assertTrue(True)

    def test_get_easy(self):
        easy_words = self.word_list
        easy_words.len(lambda x: 0 < len(x) < 4, easy_words)
        self.assertTrue(True)

    def test_get_median(self):
        median_words = self.word_list
        median_words.len(lambda x: 4 < len(x) < 8, median_words)
        self.assertTrue(True)

    def test_get_hard(self):
        hard_words = self.word_list
        hard_words.len(lambda x: len(x) > 8, hard_words)
        self.assertTrue(True)

    def test_getEasyWordRandom(self):
        words = self.get_easy()
        rm = random.choice(words)
        self.assertEqual(rm,self.easy_words)

    def test_getMedianWordRandom(self):
        words = self.get_median()
        rm = random.choice(words)
        self.assertEqual(rm, self.median_words)

    def test_getHardWordRandom(self):
        words = self.get_hard()
        rm = random.choice(words)
        self.assertEqual(rm, self.hard_words)


