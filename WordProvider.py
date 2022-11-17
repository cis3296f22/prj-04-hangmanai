import requests
from bs4 import BeautifulSoup

class WordProvider():
    def __init__(self, url='https://www.ef.edu/english-resources/english-vocabulary/top-3000-words/'):
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
        self.word_list = []
        self.Get_html(url)

    def Get_html(self, url):
        response = requests.get(url, headers=self.headers)
        print(response)
        if response.status_code == 200:
            self.Parse_html(response.text)
        else:
            print("ERROR: ", response.status_code)

    def Parse_html(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        div = soup.find('div', class_="cefcom-container")
        ps = div.find_all('p')[1]

        self.word_list = str(ps).replace("<p>", "").replace("</p>", "").split("<br/>")

    def get_easy(self):
        easy_words = self.word_list
        return list(filter(lambda x: 0 < len(x) < 4, easy_words))

    def get_median(self):
        median_words = self.word_list
        return list(filter(lambda x: 4 < len(x) < 8, median_words))

    def get_hard(self):
        hard_words = self.word_list
        return list(filter(lambda x: len(x) > 8, hard_words))


if __name__ == '__main__':
    wp = WordProvider()
    print(wp.get_easy())





