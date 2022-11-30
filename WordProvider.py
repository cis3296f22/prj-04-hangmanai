import random
import urllib
from default_word_list import easy_word_list
from default_word_list import median_word_list
from default_word_list import hard_word_list
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from enum import Enum


class Difficulty(Enum):
    """
        difficulty level

    """
    EASY = 1
    NORMAL = 2
    HARD = 3

class WordProvider():
    """
        Class use for generating a word for the game, based on user's
        difficulty choice

    """
    def __init__(self, url='https://www.ef.edu/english-resources/english-vocabulary/top-3000-words/',
                 difficulty: Difficulty = Difficulty.EASY):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        self.word_list = []
        self.Get_html(url)
        self.difficulty: Difficulty = difficulty
        self.is_internet()

    def is_internet(self):

        """
            check if online or offline

            Parameters:
            self

            Returns:
            Bool

        """
        try:
            urlopen('https://www.google.com', timeout=1)
            return True
        except urllib.error.URLError as Error:

            return False

    def Get_html(self, url):

        """
            Get html response for web scrape

            Parameters:
            url: url of the online dictionary page

            Returns:
            bool

        """
        if self.is_internet() is True:
            response = requests.get(url, headers = self.headers)
            print(response)

            if response.status_code == 200:
                self.Parse_html(response.text)
            else:
                print("ERROR: ", response.status_code)
        else:
            return False

    def Parse_html(self, content):

        """
            Paring the html response to get words

            Parameters:
            content: Content elements in the html

            Returns:
            word_list: list of word from the online dictionary

        """

        soup = BeautifulSoup(content, 'html.parser')
        div = soup.find('div', class_="cefcom-container")
        ps = div.find_all('p')[1]
        self.word_list = str(ps).replace("<p>", "").replace("</p>", "").split("<br/>")

    def get_easy(self) -> list:

        """
            get easy word list

            Parameters:
            self

            Returns:
            list[str]: easy words from the dictionary
            easy_words: return local easy words when no internet

        """

        if self.is_internet() is False:
            easy_words = easy_word_list
            return easy_words
        else:
            easy_words = self.word_list
            return list(filter(lambda x: 0 < len(x) < 4, easy_words))

    def get_median(self):

        """
            get median word list

            Parameters:
            self

            Returns:
            list [str]: median words from the dictionary
            median_words: return local median words when no internet

        """

        if self.is_internet() is False:
            median_words = median_word_list
            return median_words
        else:
            median_words = self.word_list
            return list(filter(lambda x: 4 < len(x) < 8, median_words))

    def get_hard(self):

        """
            get hard word list

            Parameters:
            self

            Returns:
            list [str]: hard words from the dictionary
            hard_words: return local hard words when no internet

        """

        if self.is_internet() is False:
            hard_words = hard_word_list
            return hard_words
        else:
            hard_words = self.word_list
            return list(filter(lambda x: len(x) > 8, hard_words))

    def getEasyWordRandom(self):

        """
            generates an easy word randomly from the easy word list

            Parameters:
            self

            Returns:
            random.choice(words): return a randomly generated easy word

        """

        words = self.get_easy()
        if len(words) == 0:
            return "SAMPLE"
        return random.choice(words)

    def getMediumWordRandom(self):

        """
            generates a median word randomly from the median word list

            Parameters:
            self

            Returns:
            random.choice(words): return a randomly generated median word

        """

        words = self.get_median()
        if len(words) == 0:
            return "SAMPLE"
        return random.choice(words)

    def getHardWordRandom(self):

        """
            generates an hard word randomly from the hard word list

            Parameters:
            self

            Returns:
            random.choice(words): return a randomly generated hard word

        """

        words = self.get_hard()
        if len(words) == 0:
            return "SAMPLE"
        return random.choice(words)

    def setDifficulty(self, difficulty: Difficulty):
        self.difficulty = difficulty

        """
            set the game to a difficulty level

            Parameters:
            difficulty: Difficulty: user's choice of difficulty level

            Returns:
            None

        """


    def getRandomWord(self):

        """
            get a random word based on difficulty

            Parameters:
            self

            Returns:
            getRandomWordByDifficulty: generated a random word based on difficulty

        """

        return self.getRandomWordByDifficulty(self.difficulty)

    def getRandomWordByDifficulty(self, difficulty: Difficulty):

        """
            get a random word based on difficulty

            Parameters:
            difficulty: Difficulty

            Returns:
            geteasyWordRandom(): get an easy word
            getmedianWordRandom(): get a median word
            getHardWordRandom(): get a hard word

        """

        if difficulty == Difficulty.EASY:
            return self.getEasyWordRandom()
        elif difficulty == Difficulty.NORMAL:
            return self.getMediumWordRandom()
        elif difficulty == Difficulty.HARD:
            return self.getHardWordRandom()
        else:
            return "SAMPLE"

    def setWordList(self, words_list):

        """
            set word list

            Parameters:
            words_list: word list

            Returns:
            none

        """

        self.word_list = words_list



if __name__ == '__main__':
    wp = WordProvider()
    print(wp.getEasyWordRandom())
    print(wp.getMediumWordRandom())
    print(wp.getHardWordRandom())




