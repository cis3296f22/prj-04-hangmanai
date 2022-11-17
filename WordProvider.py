import requests
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

def Get_html(url):
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        Parse_html(response.text)
    else:
        print("ERROR: ", response.status_code)

def Parse_html(content):

    soup = BeautifulSoup(content, 'html.parser')
    div = soup.find('div', class_="cefcom-container")
    ps = div.find_all('p')[1]
    print(str(ps).replace("<p>", "").replace("</p>", "").split("<br/>"))
    word_list = str(ps).replace("<p>", "").replace("</p>", "").split("<br/>")
    easy_words = word_list
    easy_list = filter(lambda x: 0 < len(x) < 4, easy_words)
    print(list(easy_list))
    median_words = word_list
    median_list = filter(lambda x: 4 < len(x) < 8, median_words)
    print(list(median_list))
    hard_words = word_list
    hard_list = filter(lambda x: len(x) > 8, hard_words)
    print(list(hard_list))

def get_easy(ew):
    word_list = [str(ew).replace("<p>", "").replace("</p>", "").split("<br/>")]
    easy_words = word_list
    easy_list = filter(lambda x: 1 < len(x) < 4, easy_words)
    print(easy_list)

def get_median(mw):
    word_list = [str(mw).replace("<p>", "").replace("</p>", "").split("<br/>")]
    median_words = word_list
    median_list = filter(lambda x: 1 < len(x) < 4, median_words)
    print(median_list)

def get_hard(hw):
    word_list = [str(hw).replace("<p>", "").replace("</p>", "").split("<br/>")]
    hard_words = word_list
    hard_list = filter(lambda x: 1 < len(x) < 4, hard_words)
    print(hard_list)


if __name__ == '__main__':
    url = 'https://www.ef.edu/english-resources/english-vocabulary/top-3000-words/'
    Get_html(url)






